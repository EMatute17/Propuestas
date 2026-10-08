/* Edumashow - comportamiento comun de las paginas. Sin librerias, sin peticiones de red.
   Lee window.__F (la ficha) y activa solo lo que encuentra en la pagina. */
(function () {
  'use strict';
  var F = window.__F || {};
  var doc = document, root = doc.documentElement;
  var qs = function (s, c) { return (c || doc).querySelector(s); };
  var qsa = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var mq = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  var EDU = window.EDU = { qs: qs, qsa: qsa, F: F, reduce: mq.matches, pausado: false, bajo: false };
  if (mq.addEventListener) mq.addEventListener('change', function (e) { EDU.reduce = e.matches; doc.dispatchEvent(new CustomEvent('edu:movimiento')); });

  /* dispositivo modesto: menos efectos (ahorro de datos, poca memoria o pocos nucleos) */
  try {
    var cx = navigator.connection || {};
    EDU.bajo = !!(cx.saveData || (navigator.deviceMemory && navigator.deviceMemory <= 2) || (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 2));
  } catch (e) {}
  EDU.animar = function () { return !EDU.reduce && !EDU.pausado; };

  /* ---------- las fuentes primero, para que el titular no parpadee ---------- */
  var listo = function () { root.classList.add('listo'); };
  try {
    var cargas = (F.fuentes_carga || []).map(function (f) { return doc.fonts.load(f); });
    var t = setTimeout(listo, 1500);
    Promise.all(cargas).then(function () { clearTimeout(t); listo(); }, listo);
  } catch (e) { listo(); }

  /* ---------- revelado al hacer scroll (red de seguridad: todo se ve aunque falle el observador) ---------- */
  var rv = qsa('.rv');
  function mostrarTodo() { rv.forEach(function (e) { e.classList.add('in'); }); }
  if (EDU.reduce || !('IntersectionObserver' in window)) { mostrarTodo(); }
  else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    rv.forEach(function (e) { io.observe(e); });
    setTimeout(mostrarTodo, 4000);
  }

  /* ---------- abierto ahora, segun la hora del restaurante ---------- */
  var DIAS = ['dom', 'lun', 'mar', 'mie', 'jue', 'vie', 'sab'];
  var NOMBRES = { lun: 'el lunes', mar: 'el martes', mie: 'el miércoles', jue: 'el jueves', vie: 'el viernes', sab: 'el sábado', dom: 'el domingo' };
  function ahoraEn(tz, fecha) {
    var f = fecha || new Date();
    try {
      var p = new Intl.DateTimeFormat('en-US', { timeZone: tz, weekday: 'short', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).formatToParts(f);
      var o = {}; p.forEach(function (x) { o[x.type] = x.value; });
      var map = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
      return { d: map[o.weekday], m: parseInt(o.hour, 10) * 60 + parseInt(o.minute, 10), fecha: o.year + '-' + o.month + '-' + o.day };
    } catch (e) {
      var n = f; var mm = ('0' + (n.getMonth() + 1)).slice(-2), dd = ('0' + n.getDate()).slice(-2);
      return { d: n.getDay(), m: n.getHours() * 60 + n.getMinutes(), fecha: n.getFullYear() + '-' + mm + '-' + dd };
    }
  }
  var mins = function (h) { var a = h.split(':'); return parseInt(a[0], 10) * 60 + parseInt(a[1], 10); };
  function estado(fecha) {
    var H = F.horario; if (!H || !F.tz) return null;
    var n = ahoraEn(F.tz, fecha), hoy = DIAS[n.d], ayer = DIAS[(n.d + 6) % 7], i, a, b;
    var cruza = (H[ayer] || []).filter(function (t) { var x = mins(t[0]), y = mins(t[1]); return y <= x && n.m < y; })[0];
    if (cruza) return { ab: true, txt: 'Abierto ahora · cierra a las ' + cruza[1], hoy: hoy };
    var tr = H[hoy] || [];
    for (i = 0; i < tr.length; i++) {
      a = mins(tr[i][0]); b = mins(tr[i][1]); if (b <= a) b += 1440;
      if (n.m >= a && n.m < b) return { ab: true, txt: 'Abierto ahora · cierra a las ' + tr[i][1], hoy: hoy };
      if (n.m < a) return { ab: false, txt: 'Cerrado · abre hoy a las ' + tr[i][0], hoy: hoy };
    }
    for (i = 1; i <= 7; i++) {
      var dn = DIAS[(n.d + i) % 7], tt = H[dn] || [];
      if (tt.length) return { ab: false, txt: 'Cerrado · abre ' + (i === 1 ? 'mañana' : NOMBRES[dn]) + ' a las ' + tt[0][0], hoy: hoy };
    }
    return { ab: false, txt: 'Cerrado', hoy: hoy };
  }
  EDU.ahoraEn = ahoraEn; EDU.estado = estado; EDU.mins = mins; EDU.DIAS = DIAS;
  function pintarEstado() {
    var s = estado(); if (!s) return;
    qsa('[data-open]').forEach(function (e) {
      e.classList.toggle('is-open', s.ab); e.classList.toggle('is-closed', !s.ab);
      var t = qs('[data-open-text]', e) || e; t.textContent = s.txt;
    });
    qsa('[data-dia]').forEach(function (e) {
      var hoy = e.getAttribute('data-dia') === s.hoy;
      e.classList.toggle('hoy', hoy); if (hoy) e.setAttribute('aria-current', 'true'); else e.removeAttribute('aria-current');
    });
    EDU.estadoActual = s;
  }
  pintarEstado(); setInterval(pintarEstado, 60000);

  /* ---------- panel informativo de la muestra ---------- */
  var panel = qs('#panel-edu'), ultimoFoco = null;
  function abrirPanel(ev) {
    if (!panel) return; if (ev && ev.preventDefault) ev.preventDefault(); ultimoFoco = doc.activeElement;
    if (typeof panel.showModal === 'function') { try { panel.showModal(); } catch (e) { panel.setAttribute('open', ''); } } else { panel.setAttribute('open', ''); }
    var c = qs('.cerrar', panel); if (c) c.focus();
  }
  function cerrarPanel(ev) {
    if (!panel) return; if (ev && ev.preventDefault) ev.preventDefault();
    if (typeof panel.close === 'function') { try { panel.close(); } catch (e) { panel.removeAttribute('open'); } } else { panel.removeAttribute('open'); }
    if (ultimoFoco && ultimoFoco.focus) ultimoFoco.focus();
  }
  qsa('[data-abrir-panel]').forEach(function (b) { b.addEventListener('click', abrirPanel); });
  qsa('[data-cerrar-panel]').forEach(function (b) { b.addEventListener('click', cerrarPanel); });
  if (panel) panel.addEventListener('click', function (e) { if (e.target === panel) cerrarPanel(e); });
  if (panel) panel.addEventListener('close', function () { if (doc.location.hash === '#panel-edu') { try { history.replaceState(null, '', doc.location.pathname + doc.location.search); } catch (x) {} } });
  qsa('[data-copiar]').forEach(function (b) {
    b.addEventListener('click', function () {
      var tx = b.getAttribute('data-copiar'), ok = function () { var o = b.textContent; b.textContent = 'Copiado'; setTimeout(function () { b.textContent = o; }, 1600); };
      try { navigator.clipboard.writeText(tx).then(ok, function () { seleccionar(b); }); } catch (e) { seleccionar(b); }
    });
  });
  function seleccionar(b) { var s = b.previousElementSibling; if (!s) return; var r = doc.createRange(); r.selectNodeContents(s); var g = window.getSelection(); g.removeAllRanges(); g.addRange(r); }

  /* ---------- pausa del movimiento automatico (WCAG 2.2.2) ---------- */
  var bp = qs('[data-pausa]');
  if (bp) bp.addEventListener('click', function () {
    EDU.pausado = !EDU.pausado;
    root.classList.toggle('pausada', EDU.pausado);
    bp.setAttribute('aria-pressed', EDU.pausado ? 'true' : 'false');
    var t = qs('[data-pausa-texto]', bp); if (t) t.textContent = EDU.pausado ? 'Reanudar animación' : 'Pausar animación';
    doc.dispatchEvent(new CustomEvent('edu:movimiento'));
  });

  /* ---------- WhatsApp ---------- */
  function waLink(texto) { return 'https://wa.me/' + F.wa + '?text=' + encodeURIComponent(texto); }
  function abrirWA(texto, aviso) {
    var url = waLink(texto);
    if (aviso) { aviso.hidden = false; var a = qs('a', aviso); if (a) a.href = url; }
    var a2 = doc.createElement('a'); a2.href = url; a2.target = '_blank'; a2.rel = 'noopener'; a2.style.display = 'none';
    doc.body.appendChild(a2); a2.click(); a2.remove();
    doc.dispatchEvent(new CustomEvent('edu:wa', { detail: { url: url, texto: texto } }));
  }
  EDU.waLink = waLink; EDU.abrirWA = abrirWA;

  /* ---------- la portada descuenta la altura real de la cinta (puede partirse en varias lineas con texto grande) ---------- */
  var cinta = qs('.cinta');
  if (cinta) {
    var medirCinta = function () { doc.documentElement.style.setProperty('--cinta-real', cinta.offsetHeight + 'px'); };
    medirCinta();
    if ('ResizeObserver' in window) new ResizeObserver(medirCinta).observe(cinta);
  }

  /* ---------- barra fija de acciones en movil: aparece al salir de la portada y se oculta en la reserva ---------- */
  var barra = qs('.barra-movil'), hero = qs('.hero'), res = qs('#reservar');
  if (barra && hero && 'IntersectionObserver' in window) {
    var enHero = true, enRes = false;
    barra.inert = true;   /* oculta: no se puede enfocar ni leer mientras no se ve (tambien durante la animacion) */
    var act = function () { var ver = !enHero && !enRes; barra.classList.toggle('visible', ver); barra.inert = !ver; };
    new IntersectionObserver(function (es) { enHero = es[0].isIntersecting; act(); }, { threshold: 0.05 }).observe(hero);
    if (res) new IntersectionObserver(function (es) { enRes = es[0].isIntersecting; act(); }, { threshold: 0.2 }).observe(res);
  } else if (barra) { barra.classList.add('visible'); }
})();
