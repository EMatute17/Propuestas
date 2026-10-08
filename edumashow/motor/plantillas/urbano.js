/* Personalidad URBANA: filtros del menu y la pegatina de la portada.
   Todo es aditivo: la pagina funciona sin esto. */
(function () {
  'use strict';
  var E = window.EDU, qs = E.qs, qsa = E.qsa, doc = document;
  var raf = window.requestAnimationFrame || function (f) { return setTimeout(function () { f(Date.now()); }, 33); };

  /* dispositivo modesto: el mural y la luz se quedan quietos y no hay brasas */
  if (E.bajo) doc.documentElement.classList.add('bajo');
  var hero = qs('.hero');

  /* las partículas de la portada son un módulo del paquete de animaciones (plantillas/a) */

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
})();
