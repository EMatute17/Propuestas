// Gate dinamico: pruebas en navegador real (Chromium) de un sitio generado, en muchos dispositivos.
// Recoge mediciones y evidencias crudas en un JSON; el veredicto lo emite verificar.py.
// uso: node dinamico.mjs <carpeta_sitio> <carpeta_salida> <ficha.json> [rapido]
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { servir } from './servidor.mjs';

const require = createRequire(import.meta.url);
const axeSrc = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const AQUI = path.dirname(fileURLToPath(import.meta.url));
const { dispositivos } = JSON.parse(fs.readFileSync(path.join(AQUI, 'dispositivos.json'), 'utf8'));
const [carpeta, salida, fichaRuta, modo] = process.argv.slice(2);
const ficha = JSON.parse(fs.readFileSync(fichaRuta, 'utf8'));
const CAP = path.join(salida, 'capturas');
fs.mkdirSync(CAP, { recursive: true });
const lista = modo === 'rapido' ? dispositivos.filter((d) => d.representativo) : dispositivos;

const SOLO = process.env.SOLO || '';   // para depurar: SOLO=pedido ejecuta solo esa prueba
const puede = (n) => !SOLO || SOLO === n;
const registro = [];
const srv = await servir(carpeta, { registro });
const nav = await chromium.launch({ args: ['--no-sandbox'] });
const R = { version_gate: '0.3.0', dispositivos: [], axe: {}, foco: {}, movimiento: {}, funcional: {}, red: {}, contraste: [], zoom: {}, peso: {} };

// Ayudas que se instalan en cada pagina antes de que cargue: miden el aro de foco (que lo recorte un ancestro con overflow, y su contraste)
const AYUDAS_PAGINA = `(() => {
  const recorta = (v) => /(hidden|auto|scroll|clip)/.test(v);
  const rgba = (c) => { const m = (c || '').match(/[\\d.]+/g); return m ? { r: +m[0], g: +m[1], b: +m[2], a: m[3] === undefined ? 1 : +m[3] } : null; };
  const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  window.__gate = {
    // el aro de foco (outline) se recorta si un ancestro con overflow lo deja fuera de su caja: devuelve el ancestro, o null
    anilloRecortado(el) {
      const cs = getComputedStyle(el), w = parseFloat(cs.outlineWidth) || 0;
      if (cs.outlineStyle === 'none' || w === 0) return null;
      const ext = (parseFloat(cs.outlineOffset) || 0) + w, r = el.getBoundingClientRect();
      const aro = { l: r.left - ext, t: r.top - ext, r: r.right + ext, b: r.bottom + ext };
      for (let p = el.parentElement; p && p !== document.documentElement; p = p.parentElement) {
        const o = getComputedStyle(p); if (!recorta(o.overflowX) && !recorta(o.overflowY)) continue;
        const q = p.getBoundingClientRect();
        const v = { l: q.left + (parseFloat(o.borderLeftWidth) || 0), t: q.top + (parseFloat(o.borderTopWidth) || 0), r: q.right - (parseFloat(o.borderRightWidth) || 0), b: q.bottom - (parseFloat(o.borderBottomWidth) || 0) };
        // solo cuenta si el propio elemento cabe en el ancestro: un chip a medio salir de una fila que se desplaza no es un fallo del aro
        if (r.left < v.l - 1 || r.right > v.r + 1 || r.top < v.t - 1 || r.bottom > v.b + 1) continue;
        if ((recorta(o.overflowX) && (aro.l < v.l - 0.5 || aro.r > v.r + 0.5)) || (recorta(o.overflowY) && (aro.t < v.t - 0.5 || aro.b > v.b + 0.5)))
          return p.tagName.toLowerCase() + (typeof p.className === 'string' && p.className ? '.' + p.className.split(' ')[0] : '');
      }
      return null;
    },
    // contraste del aro de foco con el fondo liso que tiene detras (null si el fondo no es liso o no se puede saber)
    contrasteAro(el) {
      const cs = getComputedStyle(el); if (cs.outlineStyle === 'none' || !(parseFloat(cs.outlineWidth) > 0)) return null;
      const aro = rgba(cs.outlineColor); if (!aro) return null;
      let fondo = null, desde = (parseFloat(cs.outlineOffset) || 0) < 0 ? el : el.parentElement;   // con desplazamiento negativo el aro se dibuja sobre el propio elemento
      for (let p = desde; p; p = p.parentElement) {
        const o = getComputedStyle(p);
        if (o.backgroundImage && o.backgroundImage !== 'none') return null;
        const c = rgba(o.backgroundColor); if (c && c.a > 0.95) { fondo = c; break; }
        if (c && c.a > 0) return null;
      }
      if (!fondo) return null;
      const a = lum(aro) + 0.05, b = lum(fondo) + 0.05;
      return Math.round((Math.max(a, b) / Math.min(a, b)) * 100) / 100;
    },
  };
})();`;
// espera a que el scroll suave de la pagina termine (varias lecturas seguidas iguales) en vez de una pausa fija
async function esperarScroll(pag, max = 3500) {
  let ultimo = null, estable = 0; const t0 = Date.now();
  while (Date.now() - t0 < max) {
    const y = await pag.evaluate(() => Math.round(window.scrollY * 10));
    if (y === ultimo) { if (++estable >= 3) return; } else { estable = 0; ultimo = y; }
    await pag.waitForTimeout(90);
  }
}

async function nuevaPagina(d, op = {}) {
  const movil = d.tipo !== 'escritorio';
  const ctx = await nav.newContext({
    viewport: { width: d.w, height: d.h }, deviceScaleFactor: d.dpr, isMobile: movil, hasTouch: movil,
    locale: op.locale || 'es-VE', timezoneId: op.tz || 'America/Caracas', reducedMotion: op.reduce ? 'reduce' : 'no-preference',
  });
  const externas = [], errores = [];
  await ctx.addInitScript({ content: AYUDAS_PAGINA });
  await ctx.route('**/*', (route) => {
    const u = route.request().url();
    if (u.startsWith(srv.url) || u.startsWith('data:') || u.startsWith('blob:')) return route.continue();
    externas.push(u); return route.abort();
  });
  const pag = await ctx.newPage();
  pag.on('console', (m) => { if (m.type() === 'error') errores.push(m.text()); });
  pag.on('pageerror', (e) => errores.push('pageerror: ' + e.message));
  if (op.reloj) await pag.clock.setFixedTime(new Date(op.reloj));
  await pag.goto(srv.url, { waitUntil: 'load' });
  await pag.waitForTimeout(op.espera ?? 2300);
  return { ctx, pag, externas, errores };
}

async function recorrer(pag) {
  const alto = await pag.evaluate(() => document.documentElement.scrollHeight);
  const vh = await pag.evaluate(() => window.innerHeight);
  for (let y = 0; y < alto; y += Math.round(vh * 0.7)) { await pag.evaluate((yy) => window.scrollTo(0, yy), y); await pag.waitForTimeout(130); }
  await pag.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
  await pag.waitForTimeout(1300);
  await esperarFinDeTransiciones(pag);
}

// las entradas (revelados) que aun corren dejan los elementos a medio tamaño: se mide cuando terminan; las animaciones infinitas (fondos, cintas) no se esperan
async function esperarFinDeTransiciones(pag, max = 4500) {
  await pag.waitForFunction(() => document.documentElement.classList.contains('listo'), null, { timeout: max, polling: 100 }).catch(() => {});   // las entradas empiezan cuando las fuentes estan cargadas
  await pag.waitForFunction(() => document.getAnimations().every((a) => {
    if (a.playState !== 'running') return true;
    const t = a.effect && a.effect.getComputedTiming ? a.effect.getComputedTiming() : null;
    return !t || t.iterations === Infinity;
  }), null, { timeout: max, polling: 100 }).catch(() => {});
  await pag.waitForTimeout(120);
}

// ---------------------------------------------------------------- medición del DOM (se ejecuta en la página)
const medirDOM = (ignorarSticky) => {
  const vw = document.documentElement.clientWidth, vh = window.innerHeight, dpr = window.devicePixelRatio || 1;
  const visible = (e) => { const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none') return false; const b = e.getBoundingClientRect(); return b.width >= 1 && b.height >= 1; };
  const eti = (e) => { let s = e.tagName.toLowerCase(); if (e.id) s += '#' + e.id; const c = (e.getAttribute('class') || '').split(/\s+/).filter(Boolean).slice(0, 2).join('.'); if (c) s += '.' + c; const t = (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 22); return s + (t ? ' "' + t + '"' : ''); };
  const enFijo = (e) => { for (let p = e; p && p !== document.body; p = p.parentElement) { if (getComputedStyle(p).position === 'fixed') return true; } return false; };
  const enSticky = (e) => { for (let p = e; p && p !== document.body; p = p.parentElement) { if (getComputedStyle(p).position === 'sticky') return true; } return false; };
  const out = { vw, vh, dpr, scrollW: document.documentElement.scrollWidth, scrollH: document.documentElement.scrollHeight };
  out.desborde = out.scrollW - vw;
  out.animOk = document.documentElement.getAttribute('data-anim-ok') || '';   // módulos del paquete de animaciones que arrancaron

  // ---- primera pantalla (hay que medirla con scroll en 0)
  const hero = document.querySelector('.hero'), h1 = hero && hero.querySelector('h1'), cta = hero && hero.querySelector('.acciones .btn');
  const dentro = (b) => b.top >= -0.5 && b.bottom <= vh + 0.5 && b.left >= -0.5 && b.right <= vw + 0.5;
  const bh = h1 ? h1.getBoundingClientRect() : null, bc = cta ? cta.getBoundingClientRect() : null;
  out.primera = { scrollY: window.scrollY, h1: bh && { top: Math.round(bh.top), bottom: Math.round(bh.bottom), dentro: dentro(bh) }, cta: bc && { top: Math.round(bc.top), bottom: Math.round(bc.bottom), dentro: dentro(bc) } };
  const so = hero && hero.querySelector('.sobre'); out.primera.sobre = so ? { texto: so.textContent.trim().slice(0, 60), dentro: dentro(so.getBoundingClientRect()) } : null;

  // ---- hojas de texto (para solapes y recortes)
  const hojas = [], solapesDeco = [];
  for (const e of document.body.querySelectorAll('*')) {
    if (e.closest('.sr-only') || e.closest('dialog:not([open])') || e.closest('.vista') || e.closest('script,style,noscript,template')) continue;
    if (e.closest('[data-decorativo]')) continue;   // lo decorativo (sello, marquesina) se revisa aparte, como caja
    if (e.classList && e.classList.contains('l')) continue;
    const directo = Array.from(e.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim().length > 0);
    const esControl = /^(A|BUTTON|INPUT|SELECT|TEXTAREA)$/.test(e.tagName) && (e.getAttribute('href') || e.tagName !== 'A');
    if (!(directo || e.tagName === 'H1' || esControl) || !visible(e) || enFijo(e)) continue;
    const b = e.getBoundingClientRect();
    if (b.width < 3 || b.height < 3) continue;   // un elemento recortado a 1 px (texto solo para lectores de pantalla) no se ve
    hojas.push({ e, x0: b.left + window.scrollX, y0: b.top + window.scrollY, x1: b.right + window.scrollX, y1: b.bottom + window.scrollY, nombre: eti(e) });
  }
  // capas decorativas: pueden estar sobre las fotos, nunca sobre un texto ni sobre un control
  for (const dcr of Array.from(document.querySelectorAll('[data-decorativo]')).filter(visible)) {
    const bd = dcr.getBoundingClientRect(), x0 = bd.left + window.scrollX, y0 = bd.top + window.scrollY, x1 = bd.right + window.scrollX, y1 = bd.bottom + window.scrollY;
    for (const a of hojas) {
      if (a.e.contains(dcr) || dcr.contains(a.e)) continue;
      const w = Math.min(x1, a.x1) - Math.max(x0, a.x0), h = Math.min(y1, a.y1) - Math.max(y0, a.y0);
      if (w > 2 && h > 2 && w * h > 12) solapesDeco.push(`capa decorativa ${eti(dcr)} sobre ${a.nombre} (${Math.round(w)}x${Math.round(h)})`);
    }
  }
  const solapes = [];
  for (let i = 0; i < hojas.length && solapes.length < 12; i++) for (let j = i + 1; j < hojas.length; j++) {
    const a = hojas[i], b = hojas[j];
    if (a.e.contains(b.e) || b.e.contains(a.e)) continue;
    const ca = a.e.closest('[data-superpuesto]'); if (ca && ca === b.e.closest('[data-superpuesto]')) continue;   // capas que se superponen a proposito y estan declaradas (G02)
    if (ignorarSticky && (enSticky(a.e) || enSticky(b.e))) continue;   // una barra pegajosa ya pegada arriba tapa lo que pasa por debajo: se comprueba en su sitio natural, con la pagina arriba
    const w = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0), h = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0);
    if (w > 2 && h > 2 && w * h > 12) solapes.push(`${a.nombre} con ${b.nombre} (${Math.round(w)}x${Math.round(h)})`);
  }
  out.solapes = solapes.concat(solapesDeco).slice(0, 12);
  // texto recortado por un ancestro con overflow hidden o clip, o fuera del documento
  const recortes = [];
  for (const a of hojas) {
    const b = a.e.getBoundingClientRect();
    if (b.right > vw + 1 || b.left < -1) {
      let enScroller = false; for (let p = a.e.parentElement; p && p !== document.body; p = p.parentElement) { if (/(auto|scroll)/.test(getComputedStyle(p).overflowX)) { enScroller = true; break; } }
      if (!enScroller) recortes.push(`${a.nombre} fuera de la pantalla (izq ${Math.round(b.left)}, der ${Math.round(b.right)})`);
    }
    for (let p = a.e.parentElement; p && p !== document.body; p = p.parentElement) {
      const cs = getComputedStyle(p);
      if (/(auto|scroll)/.test(cs.overflowX + cs.overflowY)) break;   // dentro de un carrusel: se desplaza por diseño
      if (/(hidden|clip)/.test(cs.overflowX + cs.overflowY)) {
        const r = p.getBoundingClientRect();
        if (b.right > r.right + 2 || b.left < r.left - 2 || b.bottom > r.bottom + 2 || b.top < r.top - 2) { recortes.push(`${a.nombre} recortado por ${eti(p).split(' ')[0]}`); break; }
      }
    }
    const cs0 = getComputedStyle(a.e);
    if (cs0.textOverflow === 'ellipsis' && a.e.scrollWidth > a.e.clientWidth + 1) recortes.push(`${a.nombre} truncado con puntos suspensivos`);
  }
  out.recortes = recortes.slice(0, 12);

  // ---- objetivos tactiles
  const inter = Array.from(document.querySelectorAll('a[href],button,input:not([type=hidden]),select,textarea,summary,[role=tab]')).filter((e) => visible(e) && !e.closest('dialog:not([open])') && !e.closest('.sr-only'));
  const t24 = [], t44 = [];
  for (const e of inter) {
    const b = e.getBoundingClientRect();
    const fueraAbajo = enFijo(e) && (b.top > vh + 2);   // barra fija aun oculta: no cuenta
    if (fueraAbajo) continue;
    if (b.width < 24 || b.height < 24) t24.push(`${eti(e)} ${Math.round(b.width)}x${Math.round(b.height)}`);
    else if (b.width < 44 || b.height < 44) t44.push(`${eti(e)} ${Math.round(b.width)}x${Math.round(b.height)}`);
  }
  out.interactivos = inter.length; out.tactil24 = t24.slice(0, 10); out.tactil44 = t44.slice(0, 12);

  // ---- tamaño de texto efectivo
  let minPx = 99, minEl = '';
  const tam = [];
  for (const a of hojas) {
    const cs = getComputedStyle(a.e), fs = parseFloat(cs.fontSize); const t = (a.e.textContent || '').trim();
    if (t.length < 2) continue;
    if (fs < minPx) { minPx = fs; minEl = a.nombre; }
    if (fs < 14) tam.push(`${a.nombre} ${fs.toFixed(1)}px`);
  }
  out.textoMin = { px: Number(minPx.toFixed(1)), el: minEl, menores14: tam.slice(0, 8) };
  const cuerpo = document.querySelector('.des') || document.querySelector('p');
  out.cuerpoPx = cuerpo ? parseFloat(getComputedStyle(cuerpo).fontSize) : null;

  // ---- imágenes: resolución efectiva
  const imgs = [];
  for (const im of document.querySelectorAll('img')) {
    if (!im.currentSrc || im.closest('.vista') || im.naturalWidth < 2) continue;
    const b = im.getBoundingClientRect(); if (b.width < 1 || b.height < 1) continue;
    const cs = getComputedStyle(im), cubre = cs.objectFit === 'cover';
    const nw = im.naturalWidth, nh = im.naturalHeight;
    const archivo = im.currentSrc.split('/').slice(-1)[0];
    imgs.push({ archivo, clave: archivo.replace(/-\d+\.(avif|webp|jpg|png)$/, ''), cajaW: b.width, cajaH: b.height, cubre });
  }
  out.imagenes = imgs;
  const lg = document.querySelector('.logo-enlace img');
  out.logo = lg ? (() => { const b = lg.getBoundingClientRect(); return { ancho: Math.round(b.width), alto: Math.round(b.height), nw: lg.naturalWidth, nh: lg.naturalHeight, cargada: lg.complete && lg.naturalWidth > 0, fit: getComputedStyle(lg).objectFit, archivo: (lg.currentSrc || '').split('/').slice(-1)[0] }; })() : null;
  const bm = document.querySelector('.barra-movil'); const bmc = bm && getComputedStyle(bm);
  out.barra = bm ? { enlaces: bm.querySelectorAll('a').length, visibilidad: bmc.visibility, display: bmc.display, claseVisible: bm.classList.contains('visible') } : null;
  out.estadoTexto = (document.querySelector('[data-open-text]') || {}).textContent || '';
  out.fuentes = Array.from(document.fonts).map((f) => `${f.family}:${f.status}`);
  out.cookies = document.cookie;
  out.storage = [Object.keys(localStorage).length, Object.keys(sessionStorage).length];
  out.checkboxMarcados = document.querySelectorAll('input[type=checkbox]:checked').length;
  out.dialogosAbiertos = document.querySelectorAll('dialog[open],[role=dialog]:not([hidden])').length;
  return out;
};

// ---------------------------------------------------------------- estructura accesible
const medirEstructura = () => {
  const visible = (e) => { const cs = getComputedStyle(e); return cs.display !== 'none' && cs.visibility !== 'hidden'; };
  const hs = Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6')).filter(visible).map((h) => +h.tagName[1]);
  let saltos = 0; for (let i = 1; i < hs.length; i++) if (hs[i] - hs[i - 1] > 1) saltos++;
  const nombre = (e) => (e.getAttribute('aria-label') || '').trim() || (e.textContent || '').trim() || e.getAttribute('title') || (e.querySelector('img[alt]') || {}).alt || e.getAttribute('aria-labelledby');
  const sinNombre = Array.from(document.querySelectorAll('a[href],button,[role=tab]')).filter(visible).filter((e) => !nombre(e)).length;
  const imgs = Array.from(document.querySelectorAll('img'));
  return {
    lang: document.documentElement.lang, h1: document.querySelectorAll('h1').length, encabezados: hs, saltosEncabezado: saltos,
    landmarks: { header: !!document.querySelector('body > header'), nav: document.querySelectorAll('nav').length, main: document.querySelectorAll('main').length, footer: !!document.querySelector('body > footer') },
    imgSinAlt: imgs.filter((i) => !i.hasAttribute('alt')).length, imgTotal: imgs.length, sinNombre,
    salto: (() => { const s = document.querySelector('.salto'); return s ? { destino: s.getAttribute('href'), existe: !!document.querySelector(s.getAttribute('href')) } : null; })(),
    anclasRotas: Array.from(document.querySelectorAll('a[href^="#"]')).filter((a) => a.getAttribute('href').length > 1 && !document.getElementById(a.getAttribute('href').slice(1))).map((a) => a.getAttribute('href')),
    enlaces: Array.from(document.querySelectorAll('a[href]')).map((a) => a.getAttribute('href')),
  };
};

// ---------------------------------------------------------------- contraste real sobre el fondo (datos crudos; juzga verificar.py)
async function muestrearContraste(pag, d, selectores, etiqueta, antes) {
  if (antes) await antes();
  await pag.evaluate(() => { const b = document.querySelector('[data-pausa]'); const root = document.documentElement; if (!root.classList.contains('pausada') && b) b.click(); });
  await pag.waitForTimeout(500);
  await esperarFinDeTransiciones(pag);   // la cortina de la portada y los revelados terminan antes de medir (con la maquina cargada tardan mas)
  const datos = await pag.evaluate((sels) => {
    const vw = document.documentElement.clientWidth, vh = window.innerHeight, filas = [];
    // lo que tapan las barras fijas o pegadas (la barra de acciones del movil, la del pedido, la de filtros) no lo ve la persona: no se mide
    const cubiertos = Array.from(document.body.querySelectorAll('*')).filter((e) => { const cs = getComputedStyle(e); if (!/^(fixed|sticky)$/.test(cs.position) || cs.visibility === 'hidden' || cs.display === 'none') return false; const b = e.getBoundingClientRect(); return b.width > 1 && b.height > 1 && b.bottom > 0 && b.top < vh; }).map((e) => e.getBoundingClientRect());
    const recortar = ([l, t, w, h]) => {
      let x0 = l, y0 = t, x1 = l + w, y1 = t + h;
      for (const c of cubiertos) {
        if (c.left >= x1 || c.right <= x0 || c.top >= y1 || c.bottom <= y0) continue;
        if (c.top <= y0 && c.bottom >= y1) return null;
        if (c.top > y0 && c.top < y1 && c.bottom >= y1) y1 = c.top;
        else if (c.bottom > y0 && c.bottom < y1 && c.top <= y0) y0 = c.bottom;
      }
      return (x1 - x0 > 1 && y1 - y0 > 1) ? [x0, y0, x1 - x0, y1 - y0] : null;
    };
    for (const sel of sels) for (const e of document.querySelectorAll(sel)) {
      const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none') continue;
      const b = e.getBoundingClientRect(); if (b.width < 2 || b.height < 2 || b.bottom < 0 || b.top > vh || b.right < 0 || b.left > vw) continue;
      let op = 1; for (let p = e; p && p.nodeType === 1; p = p.parentElement) op *= parseFloat(getComputedStyle(p).opacity);
      const m = cs.color.match(/[\d.]+/g).map(Number);
      // las cajas del texto que se ve: lo que solo leen los lectores de pantalla (un texto recortado a 1 px) no se pinta y no se mide; los iconos si
      const oculto = (n) => { for (let p = n.nodeType === 1 ? n : n.parentElement; p && p !== e.parentElement; p = p.parentElement) { const c = getComputedStyle(p), w = p.getBoundingClientRect(); if (/^rect\(0(px)?,? ?0(px)?,? ?0(px)?,? ?0(px)?\)$/.test(c.clip) || (w.width <= 1.5 && w.height <= 1.5 && c.overflow !== 'visible')) return true; } return false; };
      const crudas = [], tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);
      for (let n = tw.nextNode(); n; n = tw.nextNode()) {
        if (n.nodeType === 3) { if (!n.textContent.trim() || oculto(n)) continue; const r1 = document.createRange(); r1.selectNodeContents(n); crudas.push(...Array.from(r1.getClientRects())); }
        else if (/^(svg|img|canvas)$/i.test(n.tagName) && !oculto(n)) crudas.push(n.getBoundingClientRect());
      }
      const rects = crudas.filter((r) => r.width > 1 && r.height > 1 && r.bottom > 0 && r.top < vh && r.right > 0 && r.left < vw && r.width < vw * 1.5)
        // el texto se mide dentro de la caja del propio elemento (sus lineas): el area de contenido de una tipografia con mucho ascendente asoma por encima y por debajo de la linea y es del vecino
        .map((r) => { const l = Math.max(0, r.left, b.left), t = Math.max(0, r.top, b.top), rr = Math.min(vw, r.right, b.right), bb = Math.min(vh, r.bottom, b.bottom); return [l, t, rr - l, bb - t]; })
        .filter(([, , w, h]) => w > 1 && h > 1)
        // solo lo que la persona ve: si otro elemento (la barra pegada de categorias, la barra fija del movil) tapa el centro del texto, no se mide
        .map(recortar).filter(Boolean)
        .filter(([x, y, w, h]) => { const t = document.elementFromPoint(x + w / 2, y + h / 2); return !t || e.contains(t) || t.contains(e); });
      if (!rects.length) continue;
      filas.push({ sel, texto: (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 30), rects, color: m.slice(0, 3), alfa: (m[3] ?? 1) * op, px: parseFloat(cs.fontSize), peso: parseInt(cs.fontWeight, 10) });
    }
    return filas;
  }, selectores);
  const ocultar = await pag.addStyleTag({ content: '*{color:transparent !important;-webkit-text-fill-color:transparent !important;-webkit-text-stroke-color:transparent !important;text-decoration-color:transparent !important;text-shadow:none !important;animation-play-state:paused !important;transition:none !important;caret-color:transparent !important}' });
  await pag.waitForTimeout(250);
  const img = path.join(CAP, `contraste_${d.id}_${etiqueta}.png`);
  await pag.screenshot({ path: img });
  await ocultar.evaluate((el) => el.remove());   // la siguiente zona se mide con el texto visible
  R.contraste.push({ dispositivo: d.id, etiqueta, imagen: path.relative(salida, img), dpr: d.dpr, filas: datos });
}

// ---------------------------------------------------------------- 1) matriz de dispositivos
if (puede('matriz')) {
for (const d of lista) {
  const { ctx, pag, externas, errores } = await nuevaPagina(d);
  const reg = { id: d.id, nombre: d.nombre, tipo: d.tipo, w: d.w, h: d.h, dpr: d.dpr, estres: !!d.estres };
  reg.arriba = await pag.evaluate(medirDOM, false);
  await pag.screenshot({ path: path.join(CAP, `${d.id}.jpg`), type: 'jpeg', quality: 78 });
  if (d.representativo) {
    await muestrearContraste(pag, d, ['.cinta p', '.cinta .cinta-btn', '.hero-barra .marca', '.hero-barra nav a', '.sobre', '.hero h1', '.lema', '.lema-en', '.hero .btn', '.hero .estado', '.pausa', '.hero .acciones .btn.suave'], 'portada');
    await pag.evaluate(() => window.location.reload()); await pag.waitForTimeout(2300);
  }
  await recorrer(pag);
  reg.pagina = await pag.evaluate(medirDOM, true);
  if (d.representativo) {
    reg.estructura = await pag.evaluate(medirEstructura);
    // contraste de las leyendas de la galería sobre las fotos
    await pag.evaluate(() => { const g = document.querySelector('.galeria'); if (g) g.scrollIntoView({ block: 'center' }); });
    await pag.waitForTimeout(900);
    await muestrearContraste(pag, d, ['.galeria figcaption', '.barra-movil a'], 'galeria');
    if (await pag.evaluate(() => !!document.querySelector('.chips'))) {   // menu de tarjetas: barra de filtros, nombres, descripciones, precios y botones
      await pag.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; document.querySelector('.carta-cuerpo').scrollIntoView({ block: 'start' }); window.scrollBy(0, -110); });
      await pag.waitForTimeout(1200);
      await muestrearContraste(pag, d, ['.chip', '.chips-enlaces a', '.cat h3', '.cat-nota', '.nom', '.nom-en', '.des', '.pre', '.eti', '.sup-btn', '.add', '.sup', '.nota-precios', '.carta .sobretitulo'], 'menu');
    }
    // secciones con fondo propio: regla de medidas, como pedir y visita (se espera a que termine el revelado de cada una)
    for (const [sec, sels, nombre] of [
      ['#regla', ['.regla .sobretitulo', '.regla h2', '.regla-txt', '.b-lb', '.b-pre', '.b-xu', '.b-mejor', '.regla .add', '.b-q', '.regla-nota'], 'regla'],
      ['#como-pedir', ['.como h2', '.paso-c h3', '.paso-c p', '.paso-c .n'], 'como'],
      ['#visitanos', ['.visita h2', '.visita address', '.dato h3', '.dato p', '.dato .horario-texto', '.estado', '.horas li', '.visita .btn', '.aviso-datos'], 'visita'],
    ]) {
      if (await pag.evaluate((q) => !!document.querySelector(q), sec)) {
        await pag.evaluate((q) => { document.documentElement.style.scrollBehavior = 'auto'; document.querySelector(q).scrollIntoView(); }, sec);
        await pag.waitForTimeout(2200);
        await muestrearContraste(pag, d, sels, nombre);
      }
    }
  }
  reg.externas = externas; reg.errores = errores;
  R.dispositivos.push(reg);
  await ctx.close();
  console.log('ok', d.id);
}
}

// ---------------------------------------------------------------- 2) axe en tres tamanos
if (puede('axe')) {
const axeDisp = lista.filter((d) => ['iph-390', 'mini-768', 'pc-1440'].includes(d.id));
for (const d of axeDisp) {
  const { ctx, pag } = await nuevaPagina(d);
  await recorrer(pag);
  await pag.addScriptTag({ content: axeSrc });
  R.axe[d.id] = await pag.evaluate(async () => {
    const r = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] } });
    return r.violations.map((v) => ({ id: v.id, impacto: v.impact, nodos: v.nodes.length, ayuda: v.help, ejemplo: (v.nodes[0] && v.nodes[0].target || []).join(' ').slice(0, 80), datos: (() => { const a = v.nodes[0] && v.nodes[0].any && v.nodes[0].any[0]; return a && a.data ? JSON.stringify(a.data).slice(0, 220) : ''; })() }));
  });
  await ctx.close();
}
}

// ---------------------------------------------------------------- 3) teclado y foco
if (puede('foco')) {
async function probarFoco(d) {
  const { ctx, pag } = await nuevaPagina(d);
  await pag.evaluate(() => {
    const vis = (e) => { const cs = getComputedStyle(e); const b = e.getBoundingClientRect(); return cs.display !== 'none' && cs.visibility !== 'hidden' && b.width > 0 && b.height > 0; };
    let n = 0;
    for (const e of document.querySelectorAll('a[href],button,input:not([type=hidden]),select,textarea,summary,[tabindex]')) { if (e.getAttribute('tabindex') === '-1' || !vis(e) || e.closest('dialog:not([open])')) continue; e.setAttribute('data-gate-i', String(n++)); }
    window.__nInter = n; document.documentElement.style.scrollBehavior = 'auto'; if (document.activeElement) document.activeElement.blur(); window.scrollTo(0, 0);
  });
  const total = await pag.evaluate(() => window.__nInter);
  const seq = []; const vistos = new Set();
  for (let i = 0; i < total + 10; i++) {
    await pag.keyboard.press('Tab');
    await pag.waitForTimeout(110);   // una persona no pulsa Tab mas rapido: deja asentarse animaciones y observadores
    const info = await pag.evaluate(() => {
      const el = document.activeElement; if (!el || el === document.body) return null;
      const cs = getComputedStyle(el), b = el.getBoundingClientRect();
      const barra = document.querySelector('.barra-movil'), rb = barra && getComputedStyle(barra).visibility !== 'hidden' && getComputedStyle(barra).display !== 'none' ? barra.getBoundingClientRect() : null;
      const vw = innerWidth, vh = innerHeight;
      const conBarra = !!rb && rb.top < vh - 1 && !el.closest('.barra-movil');
      const limiteInf = conBarra ? rb.top : vh;
      // WCAG 2.4.11: parte del elemento que se ve en la pantalla y fraccion que tapa la barra fija
      const vx0 = Math.max(b.left, 0), vx1 = Math.min(b.right, vw), vy0 = Math.max(b.top, 0), vy1 = Math.min(b.bottom, vh);
      const areaVista = Math.max(0, vx1 - vx0) * Math.max(0, vy1 - vy0);
      const tapada = conBarra ? Math.max(0, Math.min(vx1, rb.right) - Math.max(vx0, rb.left)) * Math.max(0, Math.min(vy1, rb.bottom) - Math.max(vy0, rb.top)) : 0;
      const fraccionTapada = areaVista > 0 ? tapada / areaVista : 0;
      const anillo = (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) || (cs.boxShadow && cs.boxShadow !== 'none');
      // el aro de foco se tiene que ver: al menos un lado completo (de 24 px o mas) dentro de la pantalla y por encima de la barra fija
      const ow = parseFloat(cs.outlineWidth) || 0, oo = parseFloat(cs.outlineOffset) || 0, ex = (cs.outlineStyle !== 'none' && ow > 0) ? oo + ow / 2 : 2;
      const L = b.left - ex, R = b.right + ex, T = b.top - ex, B = b.bottom + ex;
      const dentroX = (x) => x >= 0 && x <= vw, dentroY = (y) => y >= 0 && y <= limiteInf;
      const spanX = Math.min(R, vw) - Math.max(L, 0), spanY = Math.min(B, limiteInf) - Math.max(T, 0);
      const aroVisible = (dentroY(T) && spanX >= 24) || (dentroY(B) && spanX >= 24) || (dentroX(L) && spanY >= 24) || (dentroX(R) && spanY >= 24);
      return { recortado: window.__gate.anilloRecortado(el), contrasteAro: window.__gate.contrasteAro(el), i: el.getAttribute('data-gate-i'), nombre: el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : ''), anillo: !!anillo, estilo: cs.outlineStyle + ' ' + cs.outlineWidth, enPantalla: b.bottom > 0 && b.top < innerHeight + 1 && b.right > 0 && b.left < innerWidth + 1, fraccionTapada, aroVisible };
    });
    if (!info) continue;
    seq.push(info); vistos.add(info.i);
  }
  await ctx.close();
  const faltan = []; for (let k = 0; k < total; k++) if (!vistos.has(String(k))) faltan.push(k);
  return { dispositivo: d.id, interactivos: total, primero: seq[0] && seq[0].nombre, sinAnillo: (() => { const por = {}; for (const x of seq) { por[x.i] = por[x.i] || { nombre: x.nombre, estilo: x.estilo, ok: false }; por[x.i].ok = por[x.i].ok || x.anillo; } return Object.values(por).filter((x) => !x.ok).map((x) => x.nombre + ' [' + x.estilo + ']'); })(), fueraDePantalla: seq.filter((s) => !s.enPantalla).map((s) => s.nombre).slice(0, 6), tapadoPorBarra: seq.filter((s) => s.fraccionTapada >= 0.5).map((s) => s.nombre).slice(0, 6), tapadoParcial: seq.filter((s) => s.fraccionTapada > 0 && s.fraccionTapada < 0.5).map((s) => s.nombre + ' ' + Math.round(s.fraccionTapada * 100) + '%').slice(0, 6), aroNoVisible: seq.filter((s) => !s.aroVisible).map((s) => s.nombre).slice(0, 6), aroRecortado: Array.from(new Set(seq.filter((s) => s.recortado).map((s) => s.nombre + ' (recortado por ' + s.recortado + ')'))).slice(0, 6), aroPocoContraste: Array.from(new Set(seq.filter((s) => s.contrasteAro !== null && s.contrasteAro < 3).map((s) => s.nombre + ' ' + s.contrasteAro + ':1'))).slice(0, 6), noAlcanzados: faltan.length, pasos: seq.length };
}
for (const id of ['pc-1440', 'iph-390', 'se-horiz-667', 'mini-768']) { const d = lista.find((x) => x.id === id); if (d) R.foco[id] = await probarFoco(d); }
}

// ---------------------------------------------------------------- 3b) elementos que avanzan con el scroll
if (puede('scroll')) {
R.scroll = {};
for (const id of ['iph-390', 'pc-1440', 'se-horiz-667']) {
  const d = lista.find((x) => x.id === id); if (!d) continue;
  const { ctx, pag } = await nuevaPagina(d, { espera: 1200 });
  await pag.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; });
  const n = await pag.evaluate(() => document.querySelectorAll('[data-progreso]').length);
  if (n) {
    const puntos = [];
    for (const f of [0.95, 0.4, 0.15]) {
      await pag.evaluate((fr) => { const e = document.querySelector('[data-progreso]'); const t = e.getBoundingClientRect().top + scrollY; window.scrollTo(0, t - innerHeight * fr); }, f);
      await pag.waitForTimeout(450);
      puntos.push(await pag.evaluate((fr) => ({ fr, p: parseFloat(getComputedStyle(document.querySelector('[data-progreso]')).getPropertyValue('--p')), visible: (() => { const r = document.querySelector('[data-progreso]').getBoundingClientRect(); return r.top >= 0 && r.top < innerHeight; })() }), f));
    }
    R.scroll[id] = { elementos: n, puntos };
  }
  await ctx.close();
}
{
  const d = lista.find((x) => x.id === 'iph-390') || lista[0];
  const { ctx, pag } = await nuevaPagina(d, { reduce: true, espera: 1200 });
  const n = await pag.evaluate(() => document.querySelectorAll('[data-progreso]').length);
  if (n) R.scroll.reducido = { elementos: n, p: await pag.evaluate(() => parseFloat(getComputedStyle(document.querySelector('[data-progreso]')).getPropertyValue('--p'))) };
  await ctx.close();
}
{
  // sin JavaScript el efecto tiene que verse completo
  const d = lista.find((x) => x.id === 'iph-390') || lista[0];
  const c2 = await nav.newContext({ viewport: { width: d.w, height: d.h }, javaScriptEnabled: false, locale: 'es-VE' });
  await c2.route('**/*', (route) => (route.request().url().startsWith(srv.url) || route.request().url().startsWith('data:') ? route.continue() : route.abort()));
  const p2 = await c2.newPage(); await p2.goto(srv.url, { waitUntil: 'load' }); await p2.waitForTimeout(600);
  const n2 = await p2.evaluate(() => document.querySelectorAll('[data-progreso]').length);
  if (n2) R.scroll.sinJs = { elementos: n2, p: await p2.evaluate(() => parseFloat(getComputedStyle(document.querySelector('[data-progreso]')).getPropertyValue('--p'))) };
  await c2.close();
}
}

// ---------------------------------------------------------------- 4b) sin JavaScript: lo que ve quien abre la pagina en un visor que no lo ejecuta
if (puede('sinjs')) {
{
  const d = lista.find((x) => x.id === 'iph-390') || lista[0];
  const c3 = await nav.newContext({ viewport: { width: d.w, height: d.h }, deviceScaleFactor: d.dpr, isMobile: true, hasTouch: true, javaScriptEnabled: false, locale: 'es-VE' });
  await c3.route('**/*', (route) => (route.request().url().startsWith(srv.url) || route.request().url().startsWith('data:') ? route.continue() : route.abort()));
  const p3 = await c3.newPage();
  await p3.goto(srv.url, { waitUntil: 'load' }); await p3.waitForTimeout(900);
  await recorrer(p3);   // el motor de pruebas desplaza la pagina; ella no ejecuta nada
  await p3.evaluate(() => window.scrollTo(0, 0)); await p3.waitForTimeout(500);
  R.sinjs = await p3.evaluate(() => {
    const vw = document.documentElement.clientWidth;
    const imgs = Array.from(document.querySelectorAll('img')).filter((i) => i.getAttribute('src') && !i.closest('dialog:not([open])') && !i.closest('.vista') && !i.closest('noscript'));
    const falla = imgs.filter((i) => !(i.complete && i.naturalWidth > 1)).map((i) => (i.getAttribute('alt') || i.getAttribute('src') || '').slice(0, 40));
    const velo = (e) => { let op = 1; for (let p = e; p && p.nodeType === 1; p = p.parentElement) { const c = getComputedStyle(p); if (c.display === 'none' || c.visibility === 'hidden') return null; op *= parseFloat(c.opacity); } return op; };
    const ocultos = [];
    for (const e of document.querySelectorAll('h1,h2,h3,p,figcaption,.btn,.nom,.pre,.lema,.sobre,li,address')) {
      if (e.closest('dialog:not([open])') || e.closest('.sr-only') || e.closest('[hidden]') || e.closest('noscript')) continue;
      const b = e.getBoundingClientRect(); if (b.width < 2 || b.height < 2) continue;
      const op = velo(e); if (op !== null && op < 0.9) ocultos.push((e.className || e.tagName).toString().slice(0, 24) + ' ' + (e.textContent || '').trim().slice(0, 24));
    }
    const pausa = document.querySelector('[data-pausa]');
    const anim = document.getAnimations();
    return {
      desborde: document.documentElement.scrollWidth - vw, imagenes: imgs.length, imagenesFallan: falla.slice(0, 6),
      ocultos: ocultos.slice(0, 8),
      infinitas: anim.filter((a) => a.playState === 'running' && a.effect && a.effect.getComputedTiming().iterations === Infinity).length,
      largas: anim.filter((a) => a.playState === 'running' && a.effect && a.effect.getComputedTiming().endTime > 5000).length,
      pausaVisible: !!pausa && getComputedStyle(pausa).display !== 'none',
      copiarVisible: Array.from(document.querySelectorAll('[data-copiar]')).filter((e) => getComputedStyle(e).display !== 'none').length,
      enlacePanel: (() => { const a = document.querySelector('.cinta [data-abrir-panel]'); return a ? { tag: a.tagName.toLowerCase(), href: a.getAttribute('href') } : null; })(),
    };
  });
  if (R.sinjs.enlacePanel) {
    await p3.goto(srv.url + '#panel-edu', { waitUntil: 'load' }); await p3.waitForTimeout(500);
    R.sinjs.panel = await p3.evaluate(() => {
      const e = document.querySelector('#panel-edu'), b = e.getBoundingClientRect(), vw = document.documentElement.clientWidth, vh = innerHeight;
      const cerrar = e.querySelector('.cerrar');
      return { display: getComputedStyle(e).display, dentro: b.left >= -0.5 && b.right <= vw + 0.5 && b.top >= -0.5, ancho: Math.round(b.width), alto: Math.round(b.height), cabe: b.height <= vh + 1 || getComputedStyle(e).overflowY !== 'visible', cerrar: cerrar ? { tag: cerrar.tagName.toLowerCase(), href: cerrar.getAttribute('href') } : null };
    });
    await p3.click('#panel-edu .cerrar'); await p3.waitForTimeout(400);
    R.sinjs.panelCerrado = await p3.evaluate(() => getComputedStyle(document.querySelector('#panel-edu')).display === 'none');
  }
  await p3.screenshot({ path: path.join(CAP, 'sin_js_iph-390.jpg'), type: 'jpeg', quality: 70 });
  await c3.close();
}
}

// ---------------------------------------------------------------- 4) movimiento reducido y pausa
if (puede('movimiento')) {
{
  const d = lista.find((x) => x.id === 'iph-390') || lista[0];
  const medirMov = () => ({
    infinitas: document.getAnimations().filter((a) => a.playState === 'running' && a.effect && a.effect.getComputedTiming().iterations === Infinity).length,
    corriendo: document.getAnimations().filter((a) => a.playState === 'running').length,
    largas: document.getAnimations().filter((a) => a.playState === 'running' && a.effect && a.effect.getComputedTiming().endTime > 5000).length,
    brasas: (() => { const c = document.querySelector('canvas.particulas, .brasas'); if (!c) return -1; const x = c.getContext('2d'); const dts = x.getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 3; i < dts.length; i += 4 * 17) if (dts[i] > 8) n++; return n; })(),
    letras: Array.from(document.querySelectorAll('.hero h1 .l, .hero h1 [data-anim-titulo]')).every((l) => parseFloat(getComputedStyle(l).opacity) === 1 && ['none', 'matrix(1, 0, 0, 1, 0, 0)'].includes(getComputedStyle(l).transform)),
  });
  const A = await nuevaPagina(d);
  R.movimiento.normal = await A.pag.evaluate(medirMov);
  await A.pag.click('[data-pausa]'); await A.pag.waitForTimeout(700);
  R.movimiento.pausado = await A.pag.evaluate(medirMov);
  R.movimiento.pausaEstado = await A.pag.evaluate(() => ({ aria: document.querySelector('[data-pausa]').getAttribute('aria-pressed'), clase: document.documentElement.classList.contains('pausada'), texto: document.querySelector('[data-pausa-texto]').textContent }));
  await A.ctx.close();
  const B = await nuevaPagina(d, { reduce: true });
  R.movimiento.reducido = await B.pag.evaluate(medirMov);
  await B.ctx.close();
}
}

// ---------------------------------------------------------------- 5) zoom de texto al 200 por ciento
if (puede('zoom')) {
for (const id of ['mini-360', 'pc-1280']) {
  const d = lista.find((x) => x.id === id); if (!d) continue;
  const { ctx, pag } = await nuevaPagina(d);
  await pag.addStyleTag({ content: 'html{font-size:200% !important}' });
  await pag.waitForTimeout(600); await recorrer(pag);
  const m = await pag.evaluate(medirDOM, true);
  R.zoom[id] = { desborde: m.desborde, solapes: m.solapes, recortes: m.recortes };
  await ctx.close();
}
}

// ---------------------------------------------------------------- 6) pruebas funcionales
const F = {};
const dM = lista.find((x) => x.id === 'iph-390') || lista[0];
// 6a) abierto ahora con relojes simulados y otra zona horaria del visitante
if (puede('horario')) {
if (ficha.horario && ficha.negocio) {
  F.horario = [];
  const casos = ficha.gate_pruebas_horario || [];
  for (const c of casos) {
    const { ctx, pag } = await nuevaPagina(dM, { reloj: c.reloj, tz: c.zona_visitante || 'America/Caracas', espera: 700 });
    const txt = await pag.evaluate(() => (document.querySelector('[data-open-text]') || {}).textContent || '');
    F.horario.push({ caso: c.nombre, reloj: c.reloj, esperado: c.esperado, obtenido: txt, ok: txt === c.esperado });
    await ctx.close();
  }
  // horario que cruza la medianoche (se cambia el horario dentro de la página)
  const { ctx, pag } = await nuevaPagina(dM, { espera: 700 });
  const cruce = await pag.evaluate(() => {
    const E = window.EDU, orig = JSON.stringify(E.F.horario), res = [];
    E.F.horario = { lun: [], mar: [], mie: [], jue: [], vie: [['18:00', '02:00']], sab: [], dom: [] };
    const tz = E.F.tz;
    const f = (iso) => { const s = E.estado(new Date(iso)); return s && s.txt; };
    // el instante UTC en el que la hora de pared de la zona de la ficha es la pedida (cada restaurante esta en su zona, no en la de Caracas)
    const aUtc = (y, m, d, hh, mm) => {
      const objetivo = Date.UTC(y, m - 1, d, hh, mm); let t = objetivo;
      for (let i = 0; i < 3; i++) {
        const p = new Intl.DateTimeFormat('en-US', { timeZone: tz, hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }).formatToParts(new Date(t)).reduce((o, x) => (o[x.type] = x.value, o), {});
        t += objetivo - Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute);
      }
      return new Date(t).toISOString();
    };
    res.push(['vie 18:30 hora local (cruce)', f(aUtc(2026, 10, 9, 18, 30)), 'Abierto ahora · cierra a las 02:00']);
    res.push(['sab 01:00 hora local (madrugada del cruce)', f(aUtc(2026, 10, 10, 1, 0)), 'Abierto ahora · cierra a las 02:00']);
    res.push(['sab 02:30 hora local (ya cerrado)', f(aUtc(2026, 10, 10, 2, 30)), 'Cerrado · abre el viernes a las 18:00']);
    E.F.horario = JSON.parse(orig);
    return res.map((r) => ({ caso: r[0], obtenido: r[1], esperado: r[2], ok: r[1] === r[2] }));
  });
  F.horario.push(...cruce);
  await ctx.close();
}
else {
  // sin horario por dias la pagina no puede decir si esta abierto o cerrado: no debe haber ningun estado de apertura
  const { ctx, pag } = await nuevaPagina(dM, { espera: 700 });
  F.apertura = await pag.evaluate(() => ({ elementos: document.querySelectorAll('[data-open]').length, textoEstado: Array.from(document.querySelectorAll('.estado')).map((e) => e.textContent.trim().slice(0, 60)) }));
  await ctx.close();
}
}
// 6b) reserva por WhatsApp: mensaje, destino y validaciones (solo si la ficha tiene reservas)
if (puede('reserva')) {
if (ficha.reservas) {
  const { ctx, pag } = await nuevaPagina(dM, { reloj: '2026-10-07T19:00:00Z', espera: 900 });   // miércoles 15:00 en Caracas
  await pag.evaluate(() => { window.__wa = []; document.addEventListener('edu:wa', (e) => window.__wa.push(e.detail)); });
  await recorrer(pag);
  const antes = await pag.evaluate(() => ({ fecha: document.querySelector('[name=fecha]').value, hora: document.querySelector('[name=hora]').value, personas: document.querySelector('[name=personas]').value, resumen: document.querySelector('[data-r-resumen]').textContent, horas: Array.from(document.querySelectorAll('[name=hora] option')).map((o) => o.value) }));
  // enviar sin nombre: debe avisar y no abrir WhatsApp
  await pag.click('#form-reserva button[type=submit]'); await pag.waitForTimeout(250);
  const sinNombre = await pag.evaluate(() => ({ aviso: (document.querySelector('[data-r-mensaje]') || {}).textContent, visible: !(document.querySelector('[data-r-mensaje]') || {}).hidden, envios: window.__wa.length }));
  await pag.fill('#r-nombre', 'Ana Pérez'); await pag.selectOption('[name=personas]', '4'); await pag.fill('#r-nota', 'Cumpleaños, una silla para bebé');
  await pag.click('#form-reserva button[type=submit]'); await pag.waitForTimeout(400);
  const envio = await pag.evaluate(() => window.__wa.slice());
  // día cerrado (lunes): sin horas y con aviso
  await pag.fill('[name=fecha]', '2026-10-12'); await pag.dispatchEvent('[name=fecha]', 'change'); await pag.waitForTimeout(250);
  const cerrado = await pag.evaluate(() => ({ deshabilitado: document.querySelector('[name=hora]').disabled, aviso: (document.querySelector('[data-r-mensaje]') || {}).textContent }));
  F.reserva = { antes, sinNombre, envio, cerrado };
  await ctx.close();
}
}
// 6c) pestañas de la carta con teclado, y diálogo de la muestra
if (puede('carta')) {
{
  const { ctx, pag } = await nuevaPagina(dM, { espera: 900 });
  await pag.evaluate(() => document.querySelector('.carta').scrollIntoView());
  if (await pag.evaluate(() => !!document.querySelector('[role=tab]'))) {
  const t0 = await pag.evaluate(() => ({ sel: Array.from(document.querySelectorAll('[role=tab]')).map((t) => t.getAttribute('aria-selected')), visibles: Array.from(document.querySelectorAll('[role=tabpanel]')).filter((p) => getComputedStyle(p).display !== 'none').length }));
  await pag.focus(`[id="tab-${ficha.carta[0].id}"]`);   // la primera pestana es la de la primera categoria de la ficha, se llame como se llame
   await pag.keyboard.press('ArrowRight'); await pag.waitForTimeout(500);
  const t1 = await pag.evaluate(() => ({ sel: Array.from(document.querySelectorAll('[role=tab]')).map((t) => t.getAttribute('aria-selected')), activo: document.activeElement.id, visibles: Array.from(document.querySelectorAll('[role=tabpanel]')).filter((p) => getComputedStyle(p).display !== 'none').map((p) => p.id) }));
  await pag.keyboard.press('End'); await pag.waitForTimeout(300);
  const t2 = await pag.evaluate(() => ({ activo: document.activeElement.id }));
  F.pestanas = { t0, t1, t2 };
  }
  // menu con filtros: una categoria a la vez, o todas; el estado se ve (aria-pressed) y la lista queda bajo la barra pegada
  if (await pag.evaluate(() => !!document.querySelector('[data-filtro]'))) {
    await pag.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; document.querySelector('.carta').scrollIntoView(); });
    await pag.waitForTimeout(500);
    const leer = () => pag.evaluate(() => {
      const vis = (e) => getComputedStyle(e).display !== 'none';
      const cats = Array.from(document.querySelectorAll('[data-cat]'));
      const barra = document.querySelector('.chips').getBoundingClientRect();
      const primera = cats.find(vis);
      const t = primera ? primera.querySelector('.tarjeta').getBoundingClientRect() : null;
      return {
        presionados: Array.from(document.querySelectorAll('[data-filtro]')).filter((b) => b.getAttribute('aria-pressed') === 'true').map((b) => b.getAttribute('data-filtro')),
        visibles: cats.filter(vis).map((c) => c.getAttribute('data-cat')), todas: cats.map((c) => c.getAttribute('data-cat')),
        barraTop: Math.round(barra.top), barraAbajo: Math.round(barra.bottom), tarjetaTop: t ? Math.round(t.top) : null,
        tarjetas: cats.filter(vis).reduce((n, c) => n + c.querySelectorAll('.tarjeta').length, 0),
      };
    });
    const ids = await pag.evaluate(() => Array.from(document.querySelectorAll('[data-filtro]')).map((b) => b.getAttribute('data-filtro')));
    const inicial = await leer();
    const pasos = [];
    for (const id of [ids[1], 'todo', ids[ids.length - 2]]) {
      await pag.click(`[data-filtro="${id}"]`); await pag.waitForTimeout(250); await esperarScroll(pag);
      pasos.push({ id, ...(await leer()) });
    }
    // con el teclado: Enter y espacio sobre un filtro
    await pag.focus(`[data-filtro="${ids[0]}"]`); await pag.keyboard.press('Enter'); await pag.waitForTimeout(250); await esperarScroll(pag);
    const enter = await leer();
    await pag.focus(`[data-filtro="${ids[Math.min(2, ids.length - 1)]}"]`); await pag.keyboard.press('Space'); await pag.waitForTimeout(250); await esperarScroll(pag);
    const espacio = await leer();
    await pag.click(`[data-filtro="${ids[0]}"]`); await pag.waitForTimeout(250); await esperarScroll(pag);   // se deja como estaba
    F.filtros = { ids, inicial, pasos, enter, espacio };
  }
  // carta con indice (variante indice_columnas): cada enlace del indice lleva a su categoria, la deja a la vista bajo el indice pegado y la marca como actual
  if (await pag.evaluate(() => !!document.querySelector('.indice [data-cat-link]'))) {
    await pag.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; document.querySelector('.carta').scrollIntoView(); });
    await pag.waitForTimeout(500);
    const ids = await pag.evaluate(() => Array.from(document.querySelectorAll('.indice [data-cat-link]')).map((a) => a.getAttribute('data-cat-link')));
    const leerI = (id) => pag.evaluate((id) => {
      const sec = document.getElementById('cat-' + id), t = sec ? sec.querySelector('.cat-i-titulo') : null, b = t ? t.getBoundingClientRect() : null;
      const ind = document.querySelector('.indice'), pegado = ind && getComputedStyle(ind).position === 'sticky';
      return { id, top: b ? Math.round(b.top) : null, bottom: b ? Math.round(b.bottom) : null, vh: innerHeight, barraAbajo: pegado ? Math.round(ind.getBoundingClientRect().bottom) : 0,
        actual: Array.from(document.querySelectorAll('.indice [aria-current="true"]')).map((a) => a.getAttribute('data-cat-link')), foco: document.activeElement ? document.activeElement.getAttribute('data-cat-link') : null };
    }, id);
    const pasosI = [];
    for (const id of [ids[Math.min(1, ids.length - 1)], ids[ids.length - 1], ids[0]]) {
      await pag.click(`.indice [data-cat-link="${id}"]`); await pag.waitForTimeout(250); await esperarScroll(pag); await pag.waitForTimeout(900);
      pasosI.push(await leerI(id));
    }
    await pag.focus(`.indice [data-cat-link="${ids[Math.min(1, ids.length - 1)]}"]`); await pag.keyboard.press('Enter'); await pag.waitForTimeout(250); await esperarScroll(pag); await pag.waitForTimeout(900);
    F.indice = { ids, pasos: pasosI, enter: await leerI(ids[Math.min(1, ids.length - 1)]) };
  }
  if (ficha.modo === 'muestra') {   // la cinta y el panel de Edumashow solo existen en la muestra
    await pag.evaluate(() => window.scrollTo(0, 0));
    await pag.click('.cinta [data-abrir-panel]'); await pag.waitForTimeout(400);
    const abierto = await pag.evaluate(() => ({ abierto: document.querySelector('#panel-edu').open, foco: document.activeElement.className }));
    await pag.keyboard.press('Escape'); await pag.waitForTimeout(300);
    const cerrado = await pag.evaluate(() => ({ abierto: document.querySelector('#panel-edu').open, foco: document.activeElement.textContent.trim() }));
    F.dialogo = { abierto, cerrado };
  }
  await ctx.close();
}
}
// 6e) pedido: ticket en vivo, totales, mensaje de WhatsApp y destino (solo si la ficha tiene pedido)
if (puede('pedido')) {
if (ficha.pedido) {
  const lineas = (ficha.gate_pruebas_pedido || {}).lineas || [];
  F.pedido = { lineas, dispositivos: {} };
  const leerPedido = () => pagGlobal.evaluate(() => {
    const vis = (e) => { if (!e) return false; const cs = getComputedStyle(e), b = e.getBoundingClientRect(); return cs.display !== 'none' && cs.visibility !== 'hidden' && b.width > 0 && b.height > 0; };
    const barra = document.querySelector('#pedido-barra'), lado = document.querySelector('[data-ticket="lado"]'), hoja = document.querySelector('#hoja-pedido');
    const cont = vis(lado) ? lado : (hoja && hoja.open ? hoja.querySelector('[data-ticket]') : null);
    const t = (e, s_) => { const x = e && e.querySelector(s_); return x ? x.textContent.trim().replace(/\s+/g, ' ') : null; };
    return {
      barraVisible: vis(barra), barraN: t(barra, '[data-barra-n]'), barraTotal: t(barra, '[data-barra-total]'), ladoVisible: vis(lado), hojaAbierta: !!(hoja && hoja.open),
      contenedor: cont ? (cont === lado ? 'lado' : 'hoja') : null,
      lineas: cont ? Array.from(cont.querySelectorAll('.tk-linea')).map((li) => ({ nombre: t(li, '.tk-nom'), detalle: t(li, '.tk-det'), qty: t(li, '.qty'), precio: t(li, '.tk-pre') })) : [],
      total: t(cont, '[data-tk-total]'), n: t(cont, '[data-tk-n]'), unidad: t(cont, '[data-tk-unidad]'), vacioVisible: cont ? vis(cont.querySelector('[data-tk-vacio]')) : null,
      pasosActivos: document.querySelectorAll('.tarjeta .paso:not([hidden])').length,
      almacenamiento: localStorage.length + sessionStorage.length + document.cookie.length,
    };
  });
  var pagGlobal = null;
  for (const idDisp of ['iph-390', 'pc-1440']) {
    const d = lista.find((x) => x.id === idDisp); if (!d) continue;
    const { ctx, pag, errores, externas } = await nuevaPagina(d, { espera: 1000 });
    pagGlobal = pag;
    await pag.evaluate(() => { window.__wa = []; document.addEventListener('edu:wa', (e) => window.__wa.push(e.detail)); document.documentElement.style.scrollBehavior = 'auto'; });
    const Rd = {};
    Rd.antes = await leerPedido();
    await pag.evaluate(() => document.querySelector('.carta').scrollIntoView());
    for (const l of lineas) {
      const info = await pag.evaluate((op) => { const f = document.querySelector(`.op[data-op="${op}"]`); return f ? { cat: f.closest('[data-cat]').getAttribute('data-cat'), item: f.closest('[data-item]').getAttribute('data-item') } : null; }, l.op);
      if (!info) { Rd.faltaOp = (Rd.faltaOp || []).concat(l.op); continue; }
      await pag.click(`[data-filtro="${info.cat}"]`); await pag.waitForTimeout(450);
      for (const sp of (l.suplementos || [])) await pag.click(`[data-item="${info.item}"] .sup-btn[data-sup="${sp}"]`);
      await pag.click(`.op[data-op="${l.op}"] .add`);
      for (let i = 1; i < l.cantidad; i++) await pag.click(`.op[data-op="${l.op}"] .mas-uno`);
      for (const sp of (l.suplementos || [])) await pag.click(`[data-item="${info.item}"] .sup-btn[data-sup="${sp}"]`);   // se apaga para la siguiente
    }
    await pag.waitForTimeout(900);
    Rd.tras = await leerPedido();
    // aros de foco de los controles con el pedido en marcha (contadores, extras, filtros): se miden con el foco de teclado, que es el que los dibuja
    Rd.anillos = [];
    await pag.keyboard.press('Tab');
    const medirAnillos = async (sels, donde) => {
      await pag.keyboard.press('Tab');   // el ultimo gesto cuenta: tras un clic de raton el foco programado no se dibuja como foco de teclado
      const r = await pag.evaluate((ss) => ss.map((sel) => {
        const e = Array.from(document.querySelectorAll(sel)).find((x) => { const b = x.getBoundingClientRect(), cs = getComputedStyle(x); return b.width > 0 && b.height > 0 && cs.visibility !== 'hidden'; });
        if (!e) return { sel, ausente: true };
        e.focus({ preventScroll: true });
        e.scrollIntoView({ block: 'nearest', inline: 'nearest' });   // el navegador acerca a la vista lo que se enfoca con el teclado: dentro de la hoja o del ticket con desplazamiento tambien
        return { sel, enfocado: document.activeElement === e && e.matches(':focus-visible'), recortado: window.__gate.anilloRecortado(e), contraste: window.__gate.contrasteAro(e) };
      }), sels);
      Rd.anillos.push(...r.map((x) => ({ ...x, donde })));
    };
    await medirAnillos(['.filtros .chip', '.tarjeta .paso:not([hidden]) .menos', '.tarjeta .paso:not([hidden]) .mas-uno', '.tarjeta .sup-btn', '.tarjeta .add:not([hidden])'], 'menú');
    if (d.w < 1000) {
      // hoja: se abre desde la barra, con el foco en Cerrar, y Escape la cierra devolviendo el foco
      await pag.click('.pb-ver'); await pag.waitForTimeout(700);
      Rd.hoja = { ...(await leerPedido()), foco: await pag.evaluate(() => document.activeElement.className) };
      await muestrearContraste(pag, d, ['.tk-tit', '.tk-cuenta', '.tk-nom', '.tk-det', '.tk-pre', '.tk-total span', '.tk-total b', '.hoja-pedido .qty', '.hoja-pedido .cerrar'], 'ticket');
      await medirAnillos(['.hoja-pedido .cerrar', '.hoja-pedido .tk-linea .menos', '.hoja-pedido .tk-linea .mas-uno', '.hoja-pedido [name=nombre]', '.hoja-pedido [name=nota]', '.hoja-pedido .tk-enviar', '.hoja-pedido .tk-llamar', '.hoja-pedido .tk-vaciar'], 'hoja');
      // accesibilidad con la hoja abierta y el pedido armado (el axe de las demas pruebas corre con la pagina recien cargada)
      await pag.waitForTimeout(1100);   // al quitar la hoja de estilo de la medicion de contraste las entradas de las tarjetas vuelven a correr: axe las mediria a medias
      await pag.addScriptTag({ content: axeSrc });
      R.axe[d.id + ' con la hoja del pedido abierta'] = await pag.evaluate(async () => {
        const r = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] } });
        return r.violations.map((v) => ({ id: v.id, impacto: v.impact, nodos: v.nodes.length, ayuda: v.help, ejemplo: (v.nodes[0] && v.nodes[0].target || []).join(' ').slice(0, 80), datos: (() => { const a = v.nodes[0] && v.nodes[0].any && v.nodes[0].any[0]; return a && a.data ? JSON.stringify(a.data).slice(0, 220) : ''; })() }));
      });
    } else {
      Rd.hoja = null;
      await muestrearContraste(pag, d, ['.ticket .tk-tit', '.ticket .tk-cuenta', '.ticket .tk-nom', '.ticket .tk-det', '.ticket .tk-pre', '.ticket .tk-total span', '.ticket .tk-total b', '.ticket .qty', '.ticket label', '.ticket .tk-nota'], 'ticket');
      await medirAnillos(['.ticket .tk-linea .menos', '.ticket .tk-linea .mas-uno', '.ticket [name=nombre]', '.ticket [name=nota]', '.ticket .tk-enviar', '.ticket .tk-llamar', '.ticket .tk-vaciar'], 'ticket lateral');
      await pag.waitForTimeout(1100);
      await pag.addScriptTag({ content: axeSrc });
      R.axe[d.id + ' con el ticket lateral armado'] = await pag.evaluate(async () => {
        const r = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] } });
        return r.violations.map((v) => ({ id: v.id, impacto: v.impact, nodos: v.nodes.length, ayuda: v.help, ejemplo: (v.nodes[0] && v.nodes[0].target || []).join(' ').slice(0, 80), datos: (() => { const a = v.nodes[0] && v.nodes[0].any && v.nodes[0].any[0]; return a && a.data ? JSON.stringify(a.data).slice(0, 220) : ''; })() }));
      });
    }
    const cont = d.w < 1000 ? '.hoja-pedido' : '.ticket';
    // quitar uno y volver a ponerlo desde el propio ticket
    const primera = `${cont} .tk-linea:first-child`;
    const antesQty = await pag.evaluate((sel) => document.querySelector(sel + ' .qty').textContent, primera);
    await pag.click(`${primera} .mas-uno`); await pag.waitForTimeout(250);
    Rd.masUno = await leerPedido();
    await pag.click(`${primera} .menos`); await pag.waitForTimeout(250);
    Rd.menosUno = await leerPedido();
    Rd.qtyPrimera = antesQty;
    // enviar sin nombre: avisa y no abre WhatsApp
    await pag.click(`${cont} .tk-enviar`); await pag.waitForTimeout(300);
    Rd.sinNombre = await pag.evaluate((c) => ({ envios: window.__wa.length, aviso: (document.querySelector(c + ' [data-tk-error]') || {}).textContent, visible: !!document.querySelector(c + ' [data-tk-error]') && !document.querySelector(c + ' [data-tk-error]').hidden, foco: document.activeElement.name }), cont);
    await pag.fill(`${cont} [name=nombre]`, 'Ana Pérez'); await pag.fill(`${cont} [name=nota]`, 'Sin cebolla, por favor');
    await pag.click(`${cont} .tk-enviar`); await pag.waitForTimeout(400);
    Rd.envio = await pag.evaluate(() => window.__wa.slice());
    Rd.navegacion = externas.filter((u) => u.includes('wa.me/'));   // lo que el navegador intento abrir de verdad (el contexto corta todo lo externo)
    Rd.noAbrio = await pag.evaluate((c) => { const p_ = document.querySelector(c + ' [data-tk-noabrio]'); return p_ ? { visible: !p_.hidden, href: (p_.querySelector('a') || {}).href || '' } : null; }, cont);
    if (d.w < 1000) {
      await pag.keyboard.press('Escape'); await pag.waitForTimeout(400);
      Rd.cerrada = await pag.evaluate(() => ({ abierta: document.querySelector('#hoja-pedido').open, foco: document.activeElement.className }));
    } else {
      // con el ticket fuera de pantalla aparece la barra para volver a el
      await pag.evaluate(() => document.querySelector('#visitanos').scrollIntoView()); await pag.waitForTimeout(700);
      Rd.barraLejos = await leerPedido();
      // pulsar la pastilla debe llevar al ticket (que va al lado) y dejar la pagina viva: una hoja invisible la dejaria inerte
      await pag.click('.pb-ver'); await pag.waitForTimeout(250); await esperarScroll(pag);
      Rd.pastilla = await pag.evaluate(() => { const l = document.querySelector('[data-ticket="lado"]').getBoundingClientRect(); return { hojaAbierta: document.querySelector('#hoja-pedido').open, modal: !!document.querySelector('dialog:modal'), ticketEnPantalla: l.bottom > 0 && l.top < innerHeight, foco: (document.activeElement.className || document.activeElement.tagName) + '' }; });
      try { await pag.click('.chips .filtros .chip:nth-child(2)', { timeout: 3000 }); Rd.pastilla.responde = true; } catch (e) { Rd.pastilla.responde = false; }
      await pag.evaluate(() => document.querySelector('.carta').scrollIntoView()); await pag.waitForTimeout(700);
    }
    // vaciar
    if (d.w < 1000) { await pag.click('.pb-ver'); await pag.waitForTimeout(500); }
    await pag.click(`${cont} [data-tk-vaciar]`); await pag.waitForTimeout(500);
    Rd.vaciado = { ...(await leerPedido()), foco: await pag.evaluate(() => { const a = document.activeElement; return a && a !== document.body ? ((typeof a.className === 'string' && a.className) || a.id || a.tagName) : 'body'; }) };
    Rd.errores = errores.slice(0, 3);
    F.pedido.dispositivos[idDisp] = Rd;
    await ctx.close();
  }
}
}
R.funcional = F;

// ---------------------------------------------------------------- 6d) peso descargado (inicial y total tras recorrer la pagina)
if (puede('peso')) {
R.peso = {};
for (const id of ['iph-390', 'pc-1440']) {
  const d = lista.find((x) => x.id === id) || dispositivos.find((x) => x.id === id); if (!d) continue;
  const ini = registro.length;
  const { ctx, pag } = await nuevaPagina(d, { espera: 1800 });
  const hasta = registro.length;
  await recorrer(pag);
  const total = registro.length;
  const suma = (a, b) => registro.slice(a, b).filter((r) => r.estado === 200).reduce((n, r) => n + (r.bytes || 0), 0);
  const porTipo = {}; for (const r of registro.slice(ini, total)) if (r.estado === 200) porTipo[r.tipo] = (porTipo[r.tipo] || 0) + (r.bytes || 0);
  R.peso[id] = { inicial: suma(ini, hasta), total: suma(ini, total), peticionesIniciales: hasta - ini, peticionesTotales: total - ini, porTipo };
  await ctx.close();
}
}

// ---------------------------------------------------------------- 7) red: lo que el servidor sirvio y lo que se intento pedir fuera
{
  const locales = registro.filter((r) => r.estado === 200);
  const porTipo = {};
  for (const r of locales) { porTipo[r.tipo] = (porTipo[r.tipo] || 0) + (r.bytes || 0); }
  R.red = { peticiones404: registro.filter((r) => r.estado === 404).map((r) => r.url).slice(0, 10), bytesPorTipo: porTipo, externasIntentadas: Array.from(new Set(R.dispositivos.flatMap((x) => x.externas))) };
}
fs.writeFileSync(path.join(salida, 'dinamico.json'), JSON.stringify(R, null, 1));
await nav.close(); await srv.cerrar();
console.log('dinamico.json escrito', R.dispositivos.length, 'dispositivos');
