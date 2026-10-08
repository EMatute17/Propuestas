/* Módulo inclinacion: las tarjetas marcadas con data-tilt se inclinan hacia el puntero (solo con ratón y movimiento permitido). */
EDU.modulo('inclinacion', function () {
  var E = window.EDU, qsa = E.qsa;
  var els = qsa('[data-tilt]'); if (!els.length) return false;
  if (E.bajo || !(window.matchMedia && window.matchMedia('(hover:hover) and (pointer:fine)').matches)) return true;
  els.forEach(function (el) {
    el.addEventListener('pointermove', function (ev) {
      if (!E.animar()) return;
      var r = el.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width - 0.5, y = (ev.clientY - r.top) / r.height - 0.5;
      el.style.setProperty('--rx', (x * 7).toFixed(2) + 'deg'); el.style.setProperty('--ry', (-y * 7).toFixed(2) + 'deg');
    });
    el.addEventListener('pointerleave', function () { el.style.removeProperty('--rx'); el.style.removeProperty('--ry'); });
  });
  return true;
});
