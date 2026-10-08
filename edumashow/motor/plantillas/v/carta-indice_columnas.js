/* carta indice_columnas: el índice marca la categoría que se está leyendo (y, en el móvil, la mantiene a la vista). Sin esto, el índice son enlaces normales. */
(function () {
  'use strict';
  var E = window.EDU, qs = E.qs, qsa = E.qsa;
  var enlaces = qsa('[data-cat-link]'), cats = qsa('.cat-i');
  if (!enlaces.length || !cats.length || !('IntersectionObserver' in window)) return;
  var lista = qs('.indice ol'), actual = null;
  var marcar = function (id) {
    if (id === actual) return; actual = id;
    enlaces.forEach(function (a) { if (a.getAttribute('data-cat-link') === id) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
    var on = qs('[aria-current="true"]', lista);
    if (on && lista && lista.scrollWidth > lista.clientWidth + 1 && window.getComputedStyle(lista).display === 'flex') {
      lista.scrollTo({ left: on.parentNode.offsetLeft - (lista.clientWidth - on.offsetWidth) / 2, behavior: E.reduce ? 'auto' : 'smooth' });
    }
  };
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) marcar(e.target.id.replace(/^cat-/, '')); });
  }, { rootMargin: '-30% 0px -60% 0px', threshold: 0 });
  cats.forEach(function (c) { io.observe(c); });
})();
