/* Módulo progreso: una barra fina arriba que se llena con el avance de la lectura. */
EDU.modulo('progreso', function () {
  var E = window.EDU, doc = document;
  var raf = window.requestAnimationFrame || function (f) { return setTimeout(function () { f(Date.now()); }, 33); };
  var barra = doc.createElement('div'); barra.className = 'progreso'; barra.setAttribute('aria-hidden', 'true'); doc.body.appendChild(barra);
  var pend = false;
  var act = function () {
    pend = false; var h = doc.documentElement.scrollHeight - (window.innerHeight || 800);
    barra.style.setProperty('--prog', h > 0 ? Math.min(1, (window.pageYOffset || 0) / h).toFixed(4) : 0);
  };
  window.addEventListener('scroll', function () { if (!pend) { pend = true; raf(act); } }, { passive: true });
  window.addEventListener('resize', act, { passive: true });
  act();
  return true;
});
