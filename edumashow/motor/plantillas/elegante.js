/* Personalidad ELEGANTE: calor que sube con el scroll, pestanas de carta,
   vista previa del plato y reserva por WhatsApp. Todo es aditivo: la pagina funciona sin esto. */
(function () {
  'use strict';
  var E = window.EDU, F = E.F, qs = E.qs, qsa = E.qsa, doc = document;
  var raf = window.requestAnimationFrame || function (f) { return setTimeout(function () { f(Date.now()); }, 33); };

  /* la luz de la portada y las partículas son módulos del paquete de animaciones (plantillas/a) */

  /* ---------- idea: el calor sube con el scroll, atado a la posicion de la propia cifra ---------- */
  var idea = qs('.idea');
  if (idea) {
    var cifra = qs('.num', idea), pasos = qsa('.pasos li', idea), pend = false;
    var progreso = function () {
      pend = false;
      var vh = window.innerHeight || 800, p = 1;
      if (!E.reduce && cifra) { var r = cifra.getBoundingClientRect(); p = Math.min(1, Math.max(0, (vh * 0.9 - r.top) / (vh * 0.5))); }
      idea.style.setProperty('--p', p.toFixed(3));
      pasos.forEach(function (li) { li.classList.toggle('on', E.reduce || li.getBoundingClientRect().top < vh * 0.78); });
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
    var activar = function (i, foco, inicial) {
      actual = i;
      bts.forEach(function (b, k) { b.setAttribute('aria-selected', k === i ? 'true' : 'false'); b.tabIndex = k === i ? 0 : -1; });
      pans.forEach(function (p, k) { p.classList.toggle('activo', k === i); });
      indicador();
      /* al cargar no se desplaza la tira: un desplazamiento suave al cargar hace que el navegador deje de medir el pintado del contenido principal (LCP) */
      if (!inicial && !vertical()) { var b = bts[i]; tabs.scrollTo ? tabs.scrollTo({ left: b.offsetLeft - (tabs.clientWidth - b.offsetWidth) / 2, behavior: E.reduce ? 'auto' : 'smooth' }) : 0; }
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
    activar(0, false, true);
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

  /* ---------- galeria: solo es una parada del teclado cuando de verdad se desplaza ---------- */
  var gal = qs('.galeria');
  if (gal) {
    var ajustaGal = function () { if (gal.scrollWidth > gal.clientWidth + 1) gal.setAttribute('tabindex', '0'); else gal.removeAttribute('tabindex'); };
    ajustaGal();
    if ('ResizeObserver' in window) new ResizeObserver(ajustaGal).observe(gal); else window.addEventListener('resize', ajustaGal);
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
