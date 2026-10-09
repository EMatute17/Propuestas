/* carta indice_columnas: el índice marca la categoría que se está leyendo (y, en el móvil, la mantiene a la vista). Sin esto, el índice son enlaces normales. */
(function () {
  'use strict';
  var E = window.EDU, qs = E.qs, qsa = E.qsa;
  var enlaces = qsa('[data-cat-link]'), cats = qsa('.cat-i');
  if (!enlaces.length || !cats.length || !('IntersectionObserver' in window)) return;
  var lista = qs('.indice ol'), actual = null, fijo = 0;
  var marcar = function (id) {
    if (id === actual) return; actual = id;
    enlaces.forEach(function (a) { if (a.getAttribute('data-cat-link') === id) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
    var on = qs('[aria-current="true"]', lista);
    if (on && lista && lista.scrollWidth > lista.clientWidth + 1 && window.getComputedStyle(lista).display === 'flex') {
      lista.scrollTo({ left: on.parentNode.offsetLeft - (lista.clientWidth - on.offsetWidth) / 2, behavior: E.reduce ? 'auto' : 'smooth' });
    }
    else if (on && lista && lista.scrollHeight > lista.clientHeight + 1) {   /* en escritorio, con muchas categorías, el índice es una columna que se desplaza: la marcada queda a la vista */
      var rl = lista.getBoundingClientRect(), ra = on.getBoundingClientRect();
      if (ra.top < rl.top || ra.bottom > rl.bottom) lista.scrollTo({ top: lista.scrollTop + (ra.top - rl.top) - (lista.clientHeight - ra.height) / 2, behavior: E.reduce ? 'auto' : 'smooth' });
    }
  };
  var io = new IntersectionObserver(function (es) {
    if (Date.now() < fijo) return;   // tras elegir una categoría en el índice, el desplazamiento no cambia la marca
    es.forEach(function (e) { if (e.isIntersecting) marcar(e.target.id.replace(/^cat-/, '')); });
  }, { rootMargin: '-30% 0px -60% 0px', threshold: 0 });
  // lo que la persona elige queda marcado aunque la categoría sea corta o la última de la página (no llegaría a la franja de lectura)
  enlaces.forEach(function (a) {
    a.addEventListener('click', function () { fijo = Date.now() + (E.reduce ? 500 : 1100); marcar(a.getAttribute('data-cat-link')); });
  });
  cats.forEach(function (c) { io.observe(c); });
})();
