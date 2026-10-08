/* Módulo luz: un resplandor en la portada que sigue al puntero (y, sin puntero, pasea solo despacio). */
EDU.modulo('luz', function () {
  var E = window.EDU, qs = E.qs, doc = document;
  var raf = window.requestAnimationFrame || function (f) { return setTimeout(function () { f(Date.now()); }, 33); };
  var hero = qs('.hero'); if (!hero || !qs('.luz', hero)) return false;
  var cx = 62, cy = 36, tx = cx, ty = cy, apuntando = false, visible = true, corriendo = false, t0 = 0, ultimo = 0, rect = null;
  var medir = function () { rect = hero.getBoundingClientRect(); };
  medir();
  window.addEventListener('resize', function () { clearTimeout(medir.t); medir.t = setTimeout(medir, 200); }, { passive: true });
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
  var paso = function (t) {
    if (!corriendo) return;
    if (!visible || doc.hidden || !E.animar()) { corriendo = false; return; }
    if (t - ultimo >= 32) { ultimo = t; pintar(t); }
    raf(paso);
  };
  var arrancar = function () {
    if (corriendo || !visible || doc.hidden || !E.animar()) return;
    corriendo = true; if (!t0) t0 = performance.now(); ultimo = 0; raf(paso);
  };
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) arrancar(); }, { threshold: 0 }).observe(hero);
  doc.addEventListener('visibilitychange', function () { if (!doc.hidden) arrancar(); });
  doc.addEventListener('edu:movimiento', arrancar);
  arrancar();
  return true;
});
