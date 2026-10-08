/* Módulo texto_corre: una banda de texto muy grande que se desliza de lado según se recorre la página. */
EDU.modulo('texto_corre', function () {
  var E = window.EDU, qs = E.qs;
  var raf = window.requestAnimationFrame || function (f) { return setTimeout(function () { f(Date.now()); }, 33); };
  var pista = qs('.pista-t'); if (!pista) return false;
  var banda = pista.parentNode, pend = false;
  var act = function () {
    pend = false;
    if (!E.animar()) { pista.style.transform = ''; return; }
    var r = banda.getBoundingClientRect(), vh = window.innerHeight || 800;
    if (r.bottom < -100 || r.top > vh + 100) return;
    var p = (vh - r.top) / (vh + r.height);
    pista.style.transform = 'translate3d(' + (-p * 34).toFixed(2) + '%,0,0)';
  };
  var pedir = function () { if (!pend) { pend = true; raf(act); } };
  window.addEventListener('scroll', pedir, { passive: true }); window.addEventListener('resize', pedir, { passive: true });
  document.addEventListener('edu:movimiento', pedir);
  act();
  return true;
});
