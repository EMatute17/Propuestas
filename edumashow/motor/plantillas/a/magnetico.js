/* Módulo magnetico: los botones grandes siguen un poco al puntero mientras está encima (solo con ratón y movimiento permitido). */
EDU.modulo('magnetico', function () {
  var E = window.EDU, qsa = E.qsa;
  var btns = qsa('.hero .btn, .reserva .btn, .cierre-muestra .btn, .visita .btn'); if (!btns.length) return false;
  if (E.bajo || !(window.matchMedia && window.matchMedia('(hover:hover) and (pointer:fine)').matches)) return true;
  btns.forEach(function (b) {
    b.addEventListener('pointermove', function (e) {
      if (!E.animar()) return;
      var r = b.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
      b.style.translate = (x * 12).toFixed(1) + 'px ' + (y * 8).toFixed(1) + 'px';
    });
    b.addEventListener('pointerleave', function () { b.style.translate = ''; });
  });
  return true;
});
