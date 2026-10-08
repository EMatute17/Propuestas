/* Módulo particulas: un lienzo en la portada con partículas de un tipo (brasas, chispas, vapor, polvo o burbujas). Se detiene con la pausa,
   con movimiento reducido, fuera de pantalla y en dispositivos modestos. */
EDU.modulo('particulas', function () {
  var E = window.EDU, qs = E.qs, doc = document;
  var raf = window.requestAnimationFrame || function (f) { return setTimeout(function () { f(Date.now()); }, 33); };
  var cv = qs('canvas.particulas'); if (!cv) return false;
  var hero = cv.closest('.hero') || cv.parentNode, caja = cv.parentNode, ctx = cv.getContext ? cv.getContext('2d') : null;
  var claro = cv.getAttribute('data-fondo') === 'claro';
  var TIPOS = {
    brasas:   { s: [[0, 'rgba(255,214,150,1)'], [0.35, 'rgba(255,128,48,.75)'], [1, 'rgba(255,80,20,0)']], mezcla: 'lighter', r: [0.9, 3.2], vy: [14, 50], vx: [-5, 5], onda: 9, a: [0.3, 0.9], sube: 0.85, flick: 6, px: 36000, tam: 7 },
    chispas:  { s: [[0, 'rgba(255,240,190,1)'], [0.3, 'rgba(255,170,40,.85)'], [1, 'rgba(255,90,10,0)']], mezcla: 'lighter', r: [0.6, 2], vy: [50, 130], vx: [-14, 14], onda: 14, a: [0.4, 0.95], sube: 0.8, flick: 11, px: 26000, tam: 6 },
    vapor:    { s: [[0, 'rgba(255,255,255,.55)'], [0.5, 'rgba(255,255,255,.18)'], [1, 'rgba(255,255,255,0)']], sc: [[0, 'rgba(120,96,70,.5)'], [0.5, 'rgba(120,96,70,.16)'], [1, 'rgba(120,96,70,0)']], mezcla: 'source-over', r: [16, 38], vy: [7, 18], vx: [-4, 4], onda: 14, a: [0.06, 0.15], flick: 0, px: 110000, tam: 2, crece: 1 },
    polvo:    { s: [[0, 'rgba(255,236,190,1)'], [0.5, 'rgba(255,220,150,.45)'], [1, 'rgba(255,200,120,0)']], sc: [[0, 'rgba(176,122,40,1)'], [0.5, 'rgba(176,122,40,.4)'], [1, 'rgba(176,122,40,0)']], mezcla: 'lighter', mezclaClaro: 'source-over', r: [0.5, 1.8], vy: [-6, 10], vx: [-8, 8], onda: 6, a: [0.2, 0.6], flick: 3, px: 20000, tam: 7, libre: 1 },
    burbujas: { s: [[0, 'rgba(255,255,255,0)'], [0.72, 'rgba(255,255,255,.05)'], [0.9, 'rgba(255,255,255,.6)'], [1, 'rgba(255,255,255,0)']], sc: [[0, 'rgba(90,70,50,0)'], [0.72, 'rgba(90,70,50,.05)'], [0.9, 'rgba(90,70,50,.45)'], [1, 'rgba(90,70,50,0)']], mezcla: 'source-over', r: [3, 16], vy: [16, 44], vx: [-6, 6], onda: 12, a: [0.3, 0.6], flick: 0, px: 46000, tam: 2 }
  };
  var P = TIPOS[cv.getAttribute('data-tipo')] || TIPOS.brasas;
  var usar = !!ctx && !E.bajo, visible = true, corriendo = false, ultimo = 0, ps = [], w = 0, h = 0, dpr = 1, sprite = null;
  var lerp = function (r) { return r[0] + Math.random() * (r[1] - r[0]); };
  function nueva(inicial) {
    var p = { x: Math.random() * (w || 400), r: lerp(P.r), vy: lerp(P.vy), vx: lerp(P.vx), ph: Math.random() * 6.28, a: lerp(P.a), t: 0, L: P.libre ? 8 + Math.random() * 9 : 0 };
    p.y = (P.libre || inicial) ? Math.random() * (h || 600) : (h || 600) + 12;
    if (P.libre && inicial) p.t = Math.random() * p.L;
    return p;
  }
  function crearSprite() {
    sprite = doc.createElement('canvas'); sprite.width = sprite.height = 48;
    var c = sprite.getContext('2d'), g = c.createRadialGradient(24, 24, 0, 24, 24, 24), st = (claro && P.sc) ? P.sc : P.s;
    st.forEach(function (x) { g.addColorStop(x[0], x[1]); });
    c.fillStyle = g; c.fillRect(0, 0, 48, 48);
  }
  var medir = function () {
    if (!usar) return;
    var r = caja.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    w = Math.max(1, Math.round(r.width)); h = Math.max(1, Math.round(r.height));
    cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var n = Math.max(10, Math.min(60, Math.round(w * h / P.px)));
    while (ps.length < n) ps.push(nueva(true));
    ps.length = n;
  };
  var dibujar = function (t, dt) {
    ctx.clearRect(0, 0, w, h); ctx.globalCompositeOperation = (claro && P.mezclaClaro) || P.mezcla;
    for (var i = 0; i < ps.length; i++) {
      var p = ps[i]; p.t += dt; p.y -= p.vy * dt; p.x += (p.vx + Math.sin(t / 1000 * 0.9 + p.ph) * P.onda) * dt;
      if (P.libre ? p.t >= p.L : p.y < -12 - (P.crece ? p.r * 2 : 0)) { ps[i] = nueva(false); continue; }
      var env = P.libre ? Math.sin(Math.PI * p.t / p.L) : (P.sube ? Math.min(1, p.y / (h * P.sube)) : Math.sin(Math.PI * Math.max(0, Math.min(1, (h - p.y) / h))));
      var fl = P.flick ? 0.72 + 0.28 * Math.sin(t / 1000 * P.flick + p.ph) : 1;
      ctx.globalAlpha = Math.max(0, p.a * env * fl);
      var d = p.r * P.tam * (P.crece ? 1 + (1 - p.y / h) * 0.9 : 1);
      ctx.drawImage(sprite, p.x - d / 2, p.y - d / 2, d, d);
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
  return true;
});
