/* Personalidad URBANA: brasas que suben sobre el mural y categorias del menu que se resaltan al desplazarse.
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

  /* ---------- menu: la categoria que se esta viendo se marca en la barra de categorias ---------- */
  var chips = qs('.chips');
  if (chips) {
    var enlaces = qsa('a', chips), cats = enlaces.map(function (a) { return qs(a.getAttribute('href')); });
    var lista = qs('ul', chips), activo = -2, pend = false, seccion = qs('.carta');
    var marcar = function (i) {
      if (i === activo) return; activo = i;
      enlaces.forEach(function (a, k) { if (k === i) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
      if (i >= 0 && lista && lista.scrollWidth > lista.clientWidth + 1) {   /* la categoria activa se centra en la barra si esta se desplaza */
        var r = enlaces[i].parentNode.getBoundingClientRect(), rl = lista.getBoundingClientRect();
        var izq = lista.scrollLeft + (r.left - rl.left) - (lista.clientWidth - r.width) / 2;
        if (lista.scrollTo) lista.scrollTo({ left: izq, behavior: E.reduce ? 'auto' : 'smooth' }); else lista.scrollLeft = izq;
      }
    };
    var calcular = function () {
      pend = false;
      var linea = chips.offsetHeight + 28, k = -1, rs = seccion ? seccion.getBoundingClientRect() : null;
      for (var i = 0; i < cats.length; i++) { if (cats[i] && cats[i].getBoundingClientRect().top <= linea) k = i; }
      if (rs && rs.bottom < linea) k = -1;
      marcar(k);
    };
    var pedir = function () { if (!pend) { pend = true; raf(calcular); } };
    window.addEventListener('scroll', pedir, { passive: true }); window.addEventListener('resize', pedir, { passive: true });
    enlaces.forEach(function (a, i) { a.addEventListener('click', function () { marcar(i); }); });
    calcular();
  }
})();
