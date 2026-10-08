/* Módulo paralaje: las fotos marcadas con data-paralaje se desplazan un poco menos que la página (solo en pantallas anchas y con movimiento permitido). */
EDU.modulo('paralaje', function () {
  var E = window.EDU, qsa = E.qsa;
  var raf = window.requestAnimationFrame || function (f) { return setTimeout(function () { f(Date.now()); }, 33); };
  var els = qsa('[data-paralaje]'); if (!els.length) return false;
  if (!(window.matchMedia && window.matchMedia('(min-width:900px)').matches)) return true;
  var pend = false;
  var mover = function () {
    pend = false; var vh = window.innerHeight || 800;
    els.forEach(function (el) {
      if (!E.animar()) { el.style.transform = ''; return; }
      var r = el.parentNode.getBoundingClientRect(); if (r.bottom < -80 || r.top > vh + 80) return;
      var k = ((r.top + r.height / 2) - vh / 2) / vh, fuerza = parseFloat(el.getAttribute('data-paralaje')) || 4;
      el.style.transform = 'translate3d(0,' + (k * -fuerza).toFixed(2) + '%,0) scale(1.1)';
    });
  };
  var pedir = function () { if (!pend) { pend = true; raf(mover); } };
  window.addEventListener('scroll', pedir, { passive: true }); window.addEventListener('resize', pedir, { passive: true });
  document.addEventListener('edu:movimiento', pedir);
  mover();
  return true;
});
