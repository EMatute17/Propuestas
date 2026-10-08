/* Módulo subrayado: bajo cada título de sección se dibuja un trazo a mano cuando llega a la pantalla. */
EDU.modulo('subrayado', function () {
  var E = window.EDU, qsa = E.qsa;
  var hs = qsa('main h2'); if (!hs.length) return false;
  hs.forEach(function (h) { h.classList.add('sub'); });
  var encender = function () { hs.forEach(function (h) { h.classList.add('on'); }); };
  if (E.reduce || !('IntersectionObserver' in window)) { encender(); return true; }
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); } }); }, { threshold: 0.5 });
  hs.forEach(function (h) { io.observe(h); });
  setTimeout(encender, 5000);
  return true;
});
