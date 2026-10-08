/* Personalidad ELEGANTE: luz de vela, brasas, calor que sube con el scroll, pestanas de carta,
   vista previa del plato y reserva por WhatsApp. Todo es aditivo: la pagina funciona sin esto. */
(function () {
  'use strict';
  var E = window.EDU, F = E.F, qs = E.qs, qsa = E.qsa, doc = document;
  var raf = window.requestAnimationFrame || function (f) { return setTimeout(function () { f(Date.now()); }, 33); };

  /* ---------- portada: luz que sigue al puntero y brasas que suben ---------- */
  var hero = qs('.hero');
  if (hero) {
    var cv = qs('.brasas', hero), ctx = cv && cv.getContext ? cv.getContext('2d') : null;
    var cx = 62, cy = 36, tx = cx, ty = cy, apuntando = false, visible = true, corriendo = false, t0 = 0, ultimo = 0;
    var rect = null, ps = [], w = 0, h = 0, dpr = 1, sprite = null;
    var usarBrasas = !!ctx && !E.bajo;

    var medir = function () {
      rect = hero.getBoundingClientRect();
      if (!usarBrasas) return;
      dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      w = Math.max(1, Math.round(rect.width)); h = Math.max(1, Math.round(rect.height));
      cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.max(14, Math.min(46, Math.round(w * h / 38000)));
      while (ps.length < n) ps.push(nueva(true));
      ps.length = n;
    };
    function nueva(inicial) {
      return { x: Math.random() * (w || 400), y: inicial ? Math.random() * (h || 600) : (h || 600) + 12, r: 0.9 + Math.random() * 2.3,
        vy: 14 + Math.random() * 36, vx: -5 + Math.random() * 10, ph: Math.random() * 6.28, a: 0.3 + Math.random() * 0.6 };
    }
    function crearSprite() {
      sprite = doc.createElement('canvas'); sprite.width = sprite.height = 32;
      var c = sprite.getContext('2d'), g = c.createRadialGradient(16, 16, 0, 16, 16, 16);
      g.addColorStop(0, 'rgba(255,214,150,1)'); g.addColorStop(0.35, 'rgba(255,128,48,.75)'); g.addColorStop(1, 'rgba(255,80,20,0)');
      c.fillStyle = g; c.fillRect(0, 0, 32, 32);
    }
    if (usarBrasas) crearSprite();
    medir();
    window.addEventListener('resize', function () { clearTimeout(medir.t); medir.t = setTimeout(function () { medir(); }, 200); }, { passive: true });
    hero.addEventListener('pointermove', function (e) {
      if (e.pointerType === 'touch') return;
      if (!rect || Math.abs(rect.top) > 4) rect = hero.getBoundingClientRect();
      tx = ((e.clientX - rect.left) / rect.width) * 100; ty = ((e.clientY - rect.top) / rect.height) * 100; apuntando = true;
    }, { passive: true });
    hero.addEventListener('pointerleave', function () { apuntando = false; });

    var pintar = function (t) {
      var s = (t - t0) / 1000;
      if (!apuntando) { tx = 56 + Math.sin(s * 0.33) * 22; ty = 38 + Math.sin(s * 0.5 + 1.3) * 12; }
      cx += (tx - cx) * 0.06; cy += (ty - cy) * 0.06;
      var parpadeo = 1 + Math.sin(s * 7.1) * 0.012 + Math.sin(s * 3.3 + 2) * 0.02;
      hero.style.setProperty('--mx', cx.toFixed(2) + '%'); hero.style.setProperty('--my', cy.toFixed(2) + '%');
      hero.style.setProperty('--rad', (46 * parpadeo).toFixed(2) + 'vmax');
    };
    var dibujar = function (t, dt) {
      ctx.clearRect(0, 0, w, h); ctx.globalCompositeOperation = 'lighter';
      for (var i = 0; i < ps.length; i++) {
        var p = ps[i]; p.y -= p.vy * dt; p.x += (p.vx + Math.sin(t / 1000 * 0.9 + p.ph) * 9) * dt;
        if (p.y < -12) { ps[i] = nueva(false); continue; }
        var vida = Math.min(1, p.y / (h * 0.85)), fl = 0.72 + 0.28 * Math.sin(t / 1000 * 6 + p.ph);
        ctx.globalAlpha = p.a * vida * fl; var d = p.r * 7; ctx.drawImage(sprite, p.x - d / 2, p.y - d / 2, d, d);
      }
      ctx.globalAlpha = 1;
    };
    var paso = function (t) {
      if (!corriendo) return;
      if (!visible || doc.hidden || !E.animar()) { corriendo = false; return; }
      if (t - ultimo >= 32) {
        var dt = Math.min(0.06, (t - ultimo) / 1000); ultimo = t; pintar(t);
        if (usarBrasas) dibujar(t, dt);
      }
      raf(paso);
    };
    var arrancar = function () {
      if (corriendo || !visible || doc.hidden) return;
      if (!E.animar()) { if (usarBrasas) ctx.clearRect(0, 0, w, h); return; }
      corriendo = true; if (!t0) t0 = performance.now(); ultimo = 0; raf(paso);
    };
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) arrancar(); }, { threshold: 0 }).observe(hero);
    doc.addEventListener('visibilitychange', function () { if (!doc.hidden) arrancar(); });
    doc.addEventListener('edu:movimiento', function () { if (!E.animar() && usarBrasas) ctx.clearRect(0, 0, w, h); arrancar(); });
    arrancar();
  }

  /* ---------- idea: el calor sube con el scroll ---------- */
  var idea = qs('.idea');
  if (idea) {
    var pasos = qsa('.pasos li', idea), pend = false;
    var progreso = function () {
      pend = false;
      var r = idea.getBoundingClientRect(), vh = window.innerHeight || 800;
      var p = E.reduce ? 1 : Math.min(1, Math.max(0, (vh * 0.9 - r.top) / (r.height * 0.85)));
      idea.style.setProperty('--p', p.toFixed(3));
      pasos.forEach(function (li, i) { li.classList.toggle('on', p >= (i + 0.6) / (pasos.length + 0.4)); });
    };
    var pedir = function () { if (!pend) { pend = true; raf(progreso); } };
    window.addEventListener('scroll', pedir, { passive: true }); window.addEventListener('resize', pedir, { passive: true }); progreso();
  }

  /* ---------- carta: pestanas accesibles ---------- */
  var tabs = qs('.tabs');
  if (tabs) {
    var bts = qsa('[role=tab]', tabs), pans = qsa('.panel-cat'), ind = qs('.tab-ind', tabs), actual = 0;
    var vertical = function () { return window.getComputedStyle(tabs).flexDirection === 'column'; };
    var indicador = function () {
      var b = bts[actual]; if (!b || !ind) return;
      if (vertical()) { tabs.style.setProperty('--ind-y', b.offsetTop + 'px'); tabs.style.setProperty('--ind-h', b.offsetHeight + 'px'); }
      else { tabs.style.setProperty('--ind-x', b.offsetLeft + 'px'); tabs.style.setProperty('--ind-w', b.offsetWidth + 'px'); }
    };
    var activar = function (i, foco) {
      actual = i;
      bts.forEach(function (b, k) { b.setAttribute('aria-selected', k === i ? 'true' : 'false'); b.tabIndex = k === i ? 0 : -1; });
      pans.forEach(function (p, k) { p.classList.toggle('activo', k === i); });
      indicador();
      if (!vertical()) { var b = bts[i]; tabs.scrollTo ? tabs.scrollTo({ left: b.offsetLeft - (tabs.clientWidth - b.offsetWidth) / 2, behavior: E.reduce ? 'auto' : 'smooth' }) : 0; }
      if (foco) bts[i].focus();
    };
    bts.forEach(function (b, i) {
      b.addEventListener('click', function () { activar(i, false); });
      b.addEventListener('keydown', function (e) {
        var k = e.key, n = bts.length, j = -1;
        if (k === 'ArrowRight' || k === 'ArrowDown') j = (i + 1) % n;
        else if (k === 'ArrowLeft' || k === 'ArrowUp') j = (i + n - 1) % n;
        else if (k === 'Home') j = 0; else if (k === 'End') j = n - 1;
        if (j >= 0) { e.preventDefault(); activar(j, true); }
      });
    });
    activar(0, false);
    window.addEventListener('resize', indicador, { passive: true });
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(indicador);
  }

  /* ---------- carta: vista previa del plato al pasar el puntero (escritorio) ---------- */
  var vista = qs('.vista');
  if (vista && window.matchMedia && window.matchMedia('(hover:hover) and (min-width:900px)').matches) {
    var img = qs('img', vista), x = 0, y = 0, vx = 0, vy = 0, act = false, bucle = false;
    var mover = function () {
      vx += (x - vx) * 0.16; vy += (y - vy) * 0.16;
      var giro = act && E.animar() ? ((x - vx) * 0.04).toFixed(2) : 0;
      vista.style.transform = 'translate3d(' + (vx + 28).toFixed(1) + 'px,' + (vy - 130).toFixed(1) + 'px,0) rotate(' + giro + 'deg)';
      if (act || Math.abs(x - vx) > 0.5) raf(mover); else bucle = false;
    };
    qsa('.plato[data-vista]').forEach(function (p) {
      var src = p.getAttribute('data-vista');
      p.addEventListener('pointerenter', function (e) { img.src = src; act = true; vista.classList.add('on'); x = vx = e.clientX; y = vy = e.clientY; if (!bucle) { bucle = true; raf(mover); } });
      p.addEventListener('pointermove', function (e) { x = e.clientX; y = e.clientY; });
      p.addEventListener('pointerleave', function () { act = false; vista.classList.remove('on'); });
    });
  }

  /* ---------- galeria: paralaje suave en escritorio ---------- */
  var figs = qsa('.galeria figure');
  if (figs.length && window.matchMedia && window.matchMedia('(min-width:900px)').matches) {
    var pend2 = false;
    var par = function () {
      pend2 = false; if (!E.animar()) return; var vh = window.innerHeight || 800;
      figs.forEach(function (f) {
        var r = f.getBoundingClientRect(); if (r.bottom < -50 || r.top > vh + 50) return;
        var k = ((r.top + r.height / 2) - vh / 2) / vh, im = qs('img', f); if (im) im.style.transform = 'translate3d(0,' + (k * -4).toFixed(2) + '%,0) scale(1.08)';
      });
    };
    var pedir2 = function () { if (!pend2) { pend2 = true; raf(par); } };
    window.addEventListener('scroll', pedir2, { passive: true }); window.addEventListener('resize', pedir2, { passive: true }); par();
  }

  /* ---------- reserva por WhatsApp ---------- */
  var fr = qs('#form-reserva');
  if (fr && F.horario && F.tz) {
    var R = F.reservas || {}, fi = qs('[name=fecha]', fr), hi = qs('[name=hora]', fr), pi = qs('[name=personas]', fr), ni = qs('[name=nombre]', fr), no = qs('[name=nota]', fr);
    var msg = qs('[data-r-mensaje]', fr), resumen = qs('[data-r-resumen]', fr);
    var nombresDia = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];
    var hh = function (m) { m = ((m % 1440) + 1440) % 1440; return ('0' + Math.floor(m / 60)).slice(-2) + ':' + ('0' + (m % 60)).slice(-2); };
    var partes = function (s) { var p = s.split('-'); return { y: +p[0], m: +p[1], d: +p[2] }; };
    var diaSemana = function (s) { var p = partes(s); return new Date(Date.UTC(p.y, p.m - 1, p.d, 12)).getUTCDay(); };
    var sumaDias = function (s, n) { var p = partes(s), d = new Date(Date.UTC(p.y, p.m - 1, p.d + n, 12)); return d.getUTCFullYear() + '-' + ('0' + (d.getUTCMonth() + 1)).slice(-2) + '-' + ('0' + d.getUTCDate()).slice(-2); };
    var etiqueta = function (s) { var p = partes(s); return nombresDia[diaSemana(s)] + ' ' + p.d + '/' + ('0' + p.m).slice(-2); };
    var franjas = function (s) {
      var tr = F.horario[E.DIAS[diaSemana(s)]] || [], out = [], paso = R.paso || 30, ult = R.ultima || 60, ahora = E.ahoraEn(F.tz), min = s === ahora.fecha ? ahora.m + (R.antelacion || 60) : -1;
      tr.forEach(function (t) { var a = E.mins(t[0]), b = E.mins(t[1]); if (b <= a) b += 1440; for (var m = a; m <= b - ult; m += paso) { if (m > min) out.push(m); } });
      return out;
    };
    var hoy = E.ahoraEn(F.tz).fecha; fi.min = hoy; fi.max = sumaDias(hoy, 90);
    var rellenar = function (conservar) {
      var s = fi.value, fr_ = s ? franjas(s) : [], previa = conservar ? hi.value : '';
      hi.innerHTML = '';
      if (!s) { hi.disabled = true; return; }
      if (!fr_.length) {
        hi.disabled = true; var o = doc.createElement('option'); o.value = ''; o.textContent = 'Sin horarios'; hi.appendChild(o);
        var sig = null; for (var k = 1; k <= 14 && !sig; k++) { var s2 = sumaDias(s, k); if (franjas(s2).length) sig = s2; }
        msg.textContent = 'Ese día no hay mesas disponibles.' + (sig ? ' El próximo día con horario es el ' + etiqueta(sig) + '.' : ''); msg.hidden = false; resumenar(); return;
      }
      hi.disabled = false; msg.hidden = true;
      var pref = E.mins(R.preferida || '20:00'), mejor = fr_[0];
      fr_.forEach(function (m) { if (Math.abs(m - pref) < Math.abs(mejor - pref)) mejor = m; });
      fr_.forEach(function (m) { var o = doc.createElement('option'); o.value = hh(m); o.textContent = hh(m); hi.appendChild(o); });
      hi.value = previa && qs('option[value="' + previa + '"]', hi) ? previa : hh(mejor);
      resumenar();
    };
    var resumenar = function () {
      if (!resumen) return;
      if (!fi.value || !hi.value) { resumen.textContent = ''; return; }
      var p = pi.value; resumen.textContent = 'Mesa para ' + p + (p === '1' ? ' persona' : ' personas') + ' el ' + etiqueta(fi.value) + ' a las ' + hi.value + '.';
    };
    var primero = hoy; for (var q = 0; q <= 14; q++) { var s3 = sumaDias(hoy, q); if (franjas(s3).length) { primero = s3; break; } }
    fi.value = primero; pi.value = String(R.personas || 2); rellenar(false);
    fi.addEventListener('change', function () { rellenar(true); });
    hi.addEventListener('change', resumenar); pi.addEventListener('change', resumenar);
    fr.addEventListener('submit', function (e) {
      e.preventDefault();
      var nombre = (ni.value || '').trim();
      if (!nombre) { msg.textContent = 'Escribe tu nombre para que podamos confirmarte.'; msg.hidden = false; ni.focus(); return; }
      if (!fi.value || !hi.value || hi.disabled) { msg.textContent = 'Elige un día y una hora con servicio.'; msg.hidden = false; fi.focus(); return; }
      msg.hidden = true;
      var p = pi.value, nota = (no.value || '').trim();
      var t = (F.prefijo_wa || '') + 'Hola ' + F.nombre + ', soy ' + nombre + '. Quisiera reservar una mesa para ' + p + (p === '1' ? ' persona' : ' personas') + ' el ' + etiqueta(fi.value) + ' a las ' + hi.value + '.' + (nota ? '\n' + nota : '') + '\n¿Hay disponibilidad?';
      E.abrirWA(t, qs('[data-aviso-wa]', fr));
    });
  }
})();
