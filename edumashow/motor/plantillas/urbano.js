/* Personalidad URBANA: brasas que suben sobre el mural, filtros del menu e inclinacion de las tarjetas con el puntero.
   Todo es aditivo: la pagina funciona sin esto. */
(function () {
  'use strict';
  var E = window.EDU, qs = E.qs, qsa = E.qsa, doc = document;
  var raf = window.requestAnimationFrame || function (f) { return setTimeout(function () { f(Date.now()); }, 33); };

  /* dispositivo modesto: el mural y la luz se quedan quietos y no hay brasas */
  if (E.bajo) doc.documentElement.classList.add('bajo');

  /* ---------- portada: brasas que suben ---------- */
  var hero = qs('.hero');
  if (hero) {
    var cv = qs('.brasas', hero), ctx = cv && cv.getContext ? cv.getContext('2d') : null;
    var visible = true, corriendo = false, ultimo = 0, ps = [], w = 0, h = 0, dpr = 1, sprite = null;
    var usar = !!ctx && !E.bajo;

    function nueva(inicial) {
      return { x: Math.random() * (w || 400), y: inicial ? Math.random() * (h || 600) : (h || 600) + 12, r: 0.8 + Math.random() * 2.4,
        vy: 26 + Math.random() * 54, vx: -6 + Math.random() * 12, ph: Math.random() * 6.28, a: 0.35 + Math.random() * 0.6 };
    }
    function crearSprite() {
      sprite = doc.createElement('canvas'); sprite.width = sprite.height = 32;
      var c = sprite.getContext('2d'), g = c.createRadialGradient(16, 16, 0, 16, 16, 16);
      g.addColorStop(0, 'rgba(255,226,160,1)'); g.addColorStop(0.35, 'rgba(255,140,40,.8)'); g.addColorStop(1, 'rgba(255,80,10,0)');
      c.fillStyle = g; c.fillRect(0, 0, 32, 32);
    }
    var medir = function () {
      if (!usar) return;
      var r = hero.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      w = Math.max(1, Math.round(r.width)); h = Math.max(1, Math.round(r.height));
      cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.max(16, Math.min(54, Math.round(w * h / 30000)));
      while (ps.length < n) ps.push(nueva(true));
      ps.length = n;
    };
    var dibujar = function (t, dt) {
      ctx.clearRect(0, 0, w, h); ctx.globalCompositeOperation = 'lighter';
      for (var i = 0; i < ps.length; i++) {
        var p = ps[i]; p.y -= p.vy * dt; p.x += (p.vx + Math.sin(t / 1000 * 1.1 + p.ph) * 11) * dt;
        if (p.y < -12) { ps[i] = nueva(false); continue; }
        var vida = Math.min(1, p.y / (h * 0.8)), fl = 0.7 + 0.3 * Math.sin(t / 1000 * 7 + p.ph);
        ctx.globalAlpha = p.a * vida * fl; var d = p.r * 7; ctx.drawImage(sprite, p.x - d / 2, p.y - d / 2, d, d);
      }
      ctx.globalAlpha = 1;
    };
    var paso = function (t) {
      if (!corriendo) return;
      if (!visible || doc.hidden || !E.animar()) { corriendo = false; return; }
      if (t - ultimo >= 32) { var dt = Math.min(0.06, (t - ultimo) / 1000); ultimo = t; dibujar(t, dt); }
      raf(paso);
    };
    var arrancar = function () {
      if (!usar || corriendo || !visible || doc.hidden) return;
      if (!E.animar()) { ctx.clearRect(0, 0, w, h); return; }
      corriendo = true; ultimo = 0; raf(paso);
    };
    if (usar) {
      crearSprite(); medir();
      window.addEventListener('resize', function () { clearTimeout(medir.t); medir.t = setTimeout(medir, 200); }, { passive: true });
      if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) arrancar(); }, { threshold: 0 }).observe(hero);
      doc.addEventListener('visibilitychange', function () { if (!doc.hidden) arrancar(); });
      doc.addEventListener('edu:movimiento', function () { if (!E.animar()) ctx.clearRect(0, 0, w, h); arrancar(); });
      arrancar();
    }
  }

  /* ---------- pegatina: es decorativa. Si en esta pantalla (texto muy grande, ventana baja, titular largo) taparia texto o botones, se quita ---------- */
  var peg = qs('.pegatina');
  if (peg && hero) {
    var choca = function () {
      var a = peg.getBoundingClientRect(), tapa = false;
      if (!a.width) return false;
      qsa('*', hero).forEach(function (e) {
        if (tapa || peg.contains(e) || e.contains(peg) || e.closest('.hero-fondo,[data-decorativo],.sr-only')) return;
        var directo = false, i, n;
        for (i = 0; i < e.childNodes.length; i++) { n = e.childNodes[i]; if (n.nodeType === 3 && n.textContent.replace(/\s+/g, '')) { directo = true; break; } }
        if (!(directo || e.tagName === 'H1' || e.tagName === 'A' || e.tagName === 'BUTTON')) return;
        var b = e.getBoundingClientRect();
        if (b.width < 3 || b.height < 3) return;
        var w = Math.min(a.right, b.right) - Math.max(a.left, b.left), h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        if (w > 2 && h > 2 && w * h > 12) tapa = true;
      });
      return tapa;
    };
    var revisarPeg = function () { peg.classList.remove('oculta'); if (choca()) peg.classList.add('oculta'); };
    var pendientePeg = 0;
    var programarPeg = function () { if (pendientePeg) return; pendientePeg = raf(function () { pendientePeg = 0; revisarPeg(); }); };
    window.addEventListener('resize', programarPeg, { passive: true });
    if ('ResizeObserver' in window) { var roPeg = new ResizeObserver(programarPeg); roPeg.observe(hero); var cuerpoPeg = qs('.hero-cuerpo', hero); if (cuerpoPeg) roPeg.observe(cuerpoPeg); }
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(programarPeg);
    programarPeg();
  }

  /* ---------- menu: una categoria a la vez, o todas ---------- */
  var filtros = qsa('[data-filtro]');
  if (filtros.length) {
    var cats = qsa('[data-cat]'), cuerpo = qs('.carta-cuerpo'), barra = qs('.chips'), fila = qs('.filtros');
    var actual = null;
    var mostrar = function (id, desplazar) {
      actual = id;
      filtros.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-filtro') === id ? 'true' : 'false'); });
      cats.forEach(function (c) { c.hidden = !(id === 'todo' || c.getAttribute('data-cat') === id); });
      /* el filtro activo queda a la vista si la barra se desplaza. Solo tras un toque: un desplazamiento al cargar la pagina hace que el navegador
         deje de medir el pintado del contenido principal (LCP) */
      if (fila && desplazar) {
        var on = qs('[aria-pressed="true"]', fila);
        if (on && fila.scrollWidth > fila.clientWidth + 1) {
          var r = on.getBoundingClientRect(), rf = fila.getBoundingClientRect();
          var izq = fila.scrollLeft + (r.left - rf.left) - (fila.clientWidth - r.width) / 2;
          if (fila.scrollTo) fila.scrollTo({ left: izq, behavior: E.reduce ? 'auto' : 'smooth' }); else fila.scrollLeft = izq;
        }
      }
      if (desplazar && cuerpo && barra) {   /* si se esta mas abajo del comienzo de la lista, se vuelve a su inicio, justo bajo la barra */
        var top = cuerpo.getBoundingClientRect().top - barra.offsetHeight - 12;
        if (top < 0) window.scrollTo({ top: window.pageYOffset + top, behavior: E.reduce ? 'auto' : 'smooth' });
      }
    };
    filtros.forEach(function (b) { b.addEventListener('click', function () { mostrar(b.getAttribute('data-filtro'), true); }); });
    /* un enlace con #cat-algo abre esa categoria; si el enlace esta mal escrito (un % suelto, comillas) se ignora y se abre la primera */
    var enlace = /^#cat-(.+)$/.exec(window.location.hash || ''), inicial = filtros[0].getAttribute('data-filtro');
    if (enlace) {
      var pedida = enlace[1];
      try { pedida = decodeURIComponent(pedida); } catch (x) { pedida = ''; }
      cats.forEach(function (c) { if (c.getAttribute('data-cat') === pedida) inicial = pedida; });
    }
    mostrar(inicial, false);
  }

  /* ---------- inclinacion al pasar el puntero (solo con raton y si el movimiento esta permitido) ---------- */
  var fino = window.matchMedia && window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  if (fino && !E.bajo) {
    qsa('[data-tilt]').forEach(function (el) {
      el.addEventListener('pointermove', function (ev) {
        if (!E.animar()) return;
        var r = el.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width - 0.5, y = (ev.clientY - r.top) / r.height - 0.5;
        el.style.setProperty('--rx', (x * 7).toFixed(2) + 'deg'); el.style.setProperty('--ry', (-y * 7).toFixed(2) + 'deg');
      });
      el.addEventListener('pointerleave', function () { el.style.removeProperty('--rx'); el.style.removeProperty('--ry'); });
    });
  }
})();
