/* Edumashow - pedido: ticket en vivo, barra del pedido y envio por WhatsApp.
   Sin librerias, sin almacenamiento y sin peticiones de red: el carrito existe solo en esta pagina abierta.
   Todo es aditivo: sin JavaScript la carta se lee igual y se ofrece llamar. */
(function () {
  'use strict';
  var E = window.EDU, P = E && E.F && E.F.pedido;
  if (!P) return;
  var doc = document, root = doc.documentElement, qs = E.qs, qsa = E.qsa, T = P.t, M = E.F.fmt || { pla: '{n}', miles: ',', dec: '.', es4: false, fijos: false };

  /* ---------- dinero: igual que dinero.formato_importe de Python, en centavos para no arrastrar errores de coma flotante ---------- */
  function num(c) {
    var ent = Math.floor(c / 100), d = c % 100, s = d < 10 ? '0' + d : String(d), t;
    if (M.es4 && ent < 10000) t = String(ent); else t = String(ent).replace(/\B(?=(\d{3})+(?!\d))/g, M.miles);
    if (s !== '00' || M.fijos) t += M.dec + s;
    return t;
  }
  var fmt = function (c) { return M.pla.replace('{n}', num(c)); };
  E.fmt = fmt;
  var cent = function (d) { return Math.round(parseFloat(d.value) * 100); };

  /* ---------- estado: las lineas del ticket ---------- */
  var lineas = [], nombre = '', nota = '';
  var barra = qs('#pedido-barra'), hoja = qs('#hoja-pedido'), vivo = qs('#pedido-vivo'), vivoHoja = qs('#pedido-vivo-hoja'), molde = qs('#tk-molde'), lado = qs('[data-ticket="lado"]');
  var tickets = [], ladoVisible = false;
  var ancho = window.matchMedia ? window.matchMedia('(min-width:1000px)') : null;   /* desde aqui el ticket va al lado y no hay hoja */

  var buscar = function (k) { for (var i = 0; i < lineas.length; i++) { if (lineas[i].k === k) return lineas[i]; } return null; };
  var unitario = function (l) { var s = l.base; for (var i = 0; i < l.sups.length; i++) s += l.sups[i].c; return s; };
  var totalLinea = function (l) { return l.qty * unitario(l); };
  var total = function () { var s = 0; for (var i = 0; i < lineas.length; i++) s += totalLinea(lineas[i]); return s; };
  var cuenta = function () { var s = 0; for (var i = 0; i < lineas.length; i++) s += lineas[i].qty; return s; };
  var unidad = function (n) { return n === 1 ? T.productos_uno : T.productos_varios; };
  var detalle = function (l) {
    var p = []; if (l.etiqueta) p.push(l.etiqueta);
    for (var i = 0; i < l.sups.length; i++) p.push(l.sups[i].n.toLowerCase());
    return p.join(', ');
  };
  var nombreLargo = function (l) { var d = detalle(l); return l.nombre + (d ? ', ' + d : ''); };

  /* ---------- lectura de una fila del menu ---------- */
  function supsDe(fila) {
    var tarjeta = fila.closest('[data-item]'), out = [];
    qsa('.sup-btn[aria-pressed="true"]', tarjeta).forEach(function (b) {
      out.push({ i: parseInt(b.getAttribute('data-sup'), 10), n: qs('.sup-et', b).textContent.trim(), c: cent(qs('data.pre', b)) });
    });
    return out;
  }
  var clave = function (op, sups) { return op + '|' + sups.map(function (s) { return s.i; }).join(','); };

  function cambiarFila(fila, d, origen) {
    var tarjeta = fila.closest('[data-item]'), op = fila.getAttribute('data-op'), sups = supsDe(fila), k = clave(op, sups), l = buscar(k);
    if (!l) {
      if (d <= 0) return;
      var et = qs('.eti', fila);
      l = { k: k, op: op, item: tarjeta.getAttribute('data-item'), nombre: qs('.nom', tarjeta).textContent.trim(), etiqueta: et ? et.textContent.trim() : '', sups: sups, base: cent(qs('data.pre', fila)), qty: 0 };
      lineas.push(l);
    }
    l.qty += d;
    if (l.qty <= 0) lineas.splice(lineas.indexOf(l), 1);
    despues(l, d, origen);
  }
  function cambiarLinea(k, d, origen) {
    var l = buscar(k); if (!l) return;
    l.qty += d;
    if (l.qty <= 0) lineas.splice(lineas.indexOf(l), 1);
    despues(l, d, origen);
  }
  function despues(l, d, origen) {
    var desde = (d > 0 && origen && origen.getBoundingClientRect) ? origen.getBoundingClientRect() : null;   /* antes de pintar: Agregar se oculta al pintar */
    pintar();
    anunciar((d > 0 ? T.agregado : T.quitado) + ': ' + nombreLargo(l) + '. ' + (lineas.length ? cuenta() + ' ' + unidad(cuenta()) + ' ' + T.en_el_pedido + ', ' + fmt(total()) : T.vacio_aviso));
    if (desde) volar(desde);
  }
  /* con la hoja abierta el resto de la pagina es inerte: el aviso para lectores de pantalla tiene que estar dentro de la hoja */
  function anunciar(txt) {
    var z = (hoja && hoja.open && vivoHoja) ? vivoHoja : vivo;
    if (!z) return;
    z.textContent = '';
    setTimeout(function () { z.textContent = txt; }, 40);
  }

  /* ---------- pintar todo a partir del estado ---------- */
  function poner(el, v) { v = String(v); if (el && el.textContent !== v) el.textContent = v; }
  function pintarFilas() {
    qsa('[data-item] .op').forEach(function (f) {
      var add = qs('.add', f), paso = qs('.paso', f); if (!add || !paso) return;
      var l = buscar(clave(f.getAttribute('data-op'), supsDe(f))), q = l ? l.qty : 0;
      add.hidden = q > 0; paso.hidden = q === 0; poner(qs('.qty', paso), q);
    });
    qsa('[data-item]').forEach(function (t) {
      var id = t.getAttribute('data-item'), hay = false;
      for (var i = 0; i < lineas.length; i++) { if (lineas[i].item === id) { hay = true; break; } }
      t.classList.toggle('en-pedido', hay);
    });
    qsa('.sups-det').forEach(function (d) {   /* el boton de extras plegados cuenta los elegidos: (8) o (2/8) */
      var n = qsa('.sup-btn[aria-pressed="true"]', d).length, c = qs('.sups-n', d);
      if (c) c.textContent = '(' + (n ? n + '/' : '') + qsa('.sup-btn', d).length + ')';
      d.classList.toggle('con-sel', n > 0);
    });
    qsa('[data-ref-q]').forEach(function (b) {
      var op = b.getAttribute('data-ref-q'), q = 0;
      for (var i = 0; i < lineas.length; i++) { if (lineas[i].op === op) q += lineas[i].qty; }
      b.hidden = q === 0; poner(b, '×' + q);
    });
  }
  function pintarBarra() {
    if (!barra) return;
    var n = cuenta(), ver = n > 0 && !ladoVisible;
    barra.hidden = !ver;
    root.classList.toggle('con-pedido', ver);
    poner(qs('[data-barra-n]', barra), n);
    poner(qs('[data-barra-total]', barra), fmt(total()));
    qs('.pb-ver', barra).setAttribute('aria-label', T.ver + ': ' + n + ' ' + unidad(n) + ', ' + fmt(total()));
  }

  function paso(k, nom, qty) {
    var s = doc.createElement('span'); s.className = 'paso';
    s.innerHTML = '<button type="button" class="menos" data-menos><span aria-hidden="true"></span></button><output class="qty"></output><button type="button" class="mas-uno" data-mas><span aria-hidden="true"></span></button>';
    var b = qsa('button', s);
    b[0].setAttribute('aria-label', T.quitar_uno + ' ' + nom); b[1].setAttribute('aria-label', T.agregar_uno + ' ' + nom);
    qs('output', s).textContent = qty;
    return s;
  }
  function crearLinea(l) {
    var li = doc.createElement('li'); li.className = 'tk-linea'; li.setAttribute('data-k', l.k);
    var info = doc.createElement('div'); info.className = 'tk-info';
    var n = doc.createElement('span'); n.className = 'tk-nom'; n.textContent = l.nombre; info.appendChild(n);
    var dt = detalle(l);
    if (dt) { var d = doc.createElement('span'); d.className = 'tk-det'; d.textContent = dt; info.appendChild(d); }
    li.appendChild(info); li.appendChild(paso(l.k, nombreLargo(l), l.qty));
    var pr = doc.createElement('span'); pr.className = 'tk-pre'; li.appendChild(pr);
    return li;
  }
  function pintarTicket(tk) {
    var el = tk.el, ul = qs('[data-tk-lineas]', el), n = cuenta(), i, li, hijos;
    hijos = Array.prototype.slice.call(ul.children);
    hijos.forEach(function (x) { if (!buscar(x.getAttribute('data-k'))) ul.removeChild(x); });
    for (i = 0; i < lineas.length; i++) {
      li = null; hijos = ul.children;
      for (var j = 0; j < hijos.length; j++) { if (hijos[j].getAttribute('data-k') === lineas[i].k) { li = hijos[j]; break; } }
      if (!li) { li = crearLinea(lineas[i]); ul.appendChild(li); }
      poner(qs('.qty', li), lineas[i].qty); poner(qs('.tk-pre', li), fmt(totalLinea(lineas[i])));
    }
    poner(qs('[data-tk-n]', el), n); poner(qs('[data-tk-unidad]', el), unidad(n));
    poner(qs('[data-tk-total]', el), fmt(total()));
    qs('[data-tk-vacio]', el).hidden = n > 0; qs('[data-tk-cuerpo]', el).hidden = n === 0;
    el.classList.toggle('con-lineas', n > 0);
    /* los avisos de un envio o una copia anteriores ya no valen: el pedido cambio */
    qsa('[data-tk-noabrio],[data-tk-copiado]', el).forEach(function (a) { a.hidden = true; });
  }
  function pintar() {
    pintarFilas(); pintarBarra();
    tickets.forEach(pintarTicket);
  }

  /* ---------- mensaje de WhatsApp ---------- */
  function mensaje() {
    var L = [P.prefijo + T.saludo, ''];
    lineas.forEach(function (l) { L.push('• ' + l.qty + ' × ' + nombreLargo(l) + ' — ' + fmt(totalLinea(l))); });
    L.push('', T.total + ': ' + fmt(total()));
    if (P.canal === 'whatsapp' && nombre.trim()) L.push(T.a_nombre + ': ' + nombre.trim());
    if (nota.trim()) L.push(T.notas + ': ' + nota.trim());
    return L.join('\n');
  }

  /* ---------- una instancia del ticket (la lateral y la hoja) ---------- */
  function nuevoTicket(cont, v) {
    if (!cont || !molde) return;
    cont.innerHTML = molde.innerHTML.replace(/\{v\}/g, v);
    var tit = qs('.tk-tit', cont); if (tit && v === 'hoja') tit.setAttribute('aria-level', '2');
    var tk = { el: cont, v: v }; tickets.push(tk);
    cont.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('button') : null; if (!b || !cont.contains(b)) return;
      var li = b.closest('.tk-linea');
      if (li && (b.classList.contains('menos') || b.classList.contains('mas-uno'))) {
        var k = li.getAttribute('data-k'), menos = b.classList.contains('menos'), sigue = buscar(k) && buscar(k).qty > 1;
        var vecino = li.nextElementSibling || li.previousElementSibling;
        cambiarLinea(k, menos ? -1 : 1);
        if (menos && !sigue) { var f = vecino && qs('button', vecino); if (f) f.focus(); else { var t0 = qs('.tk-tit', cont); if (t0) { t0.setAttribute('tabindex', '-1'); t0.focus(); } } }
      } else if (b.hasAttribute('data-tk-vaciar')) { vaciar(); }
      else if (b.classList.contains('tk-copiar')) { copiar(cont); }
    });
    cont.addEventListener('input', function (e) {
      var t = e.target; if (!t || !t.name) return;
      if (t.name === 'nombre') nombre = t.value; else if (t.name === 'nota') nota = t.value; else return;
      tickets.forEach(function (o) { var a = qs('[name="' + t.name + '"]', o.el); if (a && a.value !== t.value) a.value = t.value; });
      var er = qs('[data-tk-error]', cont); if (er) er.hidden = true;
    });
    var form = qs('form', cont);
    if (form) form.addEventListener('submit', function (e) { e.preventDefault(); enviar(cont, form); });
    var ta = qs('textarea', cont); if (ta && P.ejemplo_nota) ta.setAttribute('placeholder', P.ejemplo_nota);
    pintarTicket(tk);
  }
  function enviar(cont, form) {
    if (!lineas.length) return;
    var er = qs('[data-tk-error]', cont);
    if (P.canal === 'whatsapp' && !nombre.trim()) {
      if (er) { er.textContent = T.falta_nombre; er.hidden = false; }
      var inp = qs('[name="nombre"]', cont); if (inp) inp.focus();
      return;
    }
    if (er) er.hidden = true;
    E.abrirWA(mensaje(), qs('[data-tk-noabrio]', form), P.wa);
  }
  function copiar(cont) {
    var texto = mensaje(), aviso = qs('[data-tk-copiado]', cont);
    var ok = function () { if (aviso) aviso.hidden = false; };
    var respaldo = function () {
      var a = doc.createElement('textarea'); a.value = texto; a.setAttribute('readonly', ''); a.style.position = 'fixed'; a.style.opacity = '0';
      doc.body.appendChild(a); a.select(); try { doc.execCommand('copy'); ok(); } catch (x) {} a.remove();
    };
    try { navigator.clipboard.writeText(texto).then(ok, respaldo); } catch (x) { respaldo(); }
  }
  function vaciar() {
    var enHoja = !!(hoja && hoja.open);
    lineas = []; pintar(); anunciar(T.vacio_aviso);
    if (enHoja) cerrarHoja();
    else enfocarTicket();   /* el boton de vaciar se oculta con el cuerpo del ticket: el foco pasa al titulo */
  }
  /* lleva el foco a un sitio que existe: el titulo del ticket lateral o, si no hay, el encabezado de la carta */
  function enfocarTicket() {
    var t = (visibleEnPantalla(lado) && qs('.tk-tit', lado)) || qs('#t-carta'); if (!t) return;
    t.setAttribute('tabindex', '-1');
    try { t.focus({ preventScroll: true }); } catch (e) { t.focus(); }
  }

  /* ---------- hoja del ticket (pantallas estrechas) ---------- */
  var abridor = null;
  /* desde 1000 px la hoja no se dibuja (hay ticket al lado): abrirla dejaria la pagina inerte con un dialogo invisible. Se lleva a la persona al ticket */
  function irAlTicket() {
    var t = lado || qs('.carta-cuerpo'); if (!t) return;
    t.scrollIntoView({ block: 'center', behavior: E.animar() ? 'smooth' : 'auto' });
    enfocarTicket();
  }
  function abrirHoja(ev) {
    if (!hoja) return;
    if (ancho && ancho.matches) { irAlTicket(); return; }
    abridor = (ev && ev.currentTarget) || doc.activeElement;   /* en Safari y Firefox de Mac un boton tocado no recibe el foco: activeElement seria el body */
    if (typeof hoja.showModal === 'function') { try { hoja.showModal(); } catch (e) { hoja.setAttribute('open', ''); } } else { hoja.setAttribute('open', ''); }
    var c = qs('.cerrar', hoja); if (c) c.focus();
  }
  function visibleEnPantalla(e) { return !!(e && e.getClientRects && e.getClientRects().length); }
  function cerrarHoja() {
    if (!hoja) return;
    if (typeof hoja.close === 'function') { try { hoja.close(); } catch (e) { hoja.removeAttribute('open'); } } else { hoja.removeAttribute('open'); }
    if (abridor && abridor.focus && doc.contains(abridor) && visibleEnPantalla(abridor)) abridor.focus();   /* si la barra se oculto (pedido vacio), el foco va a un sitio que existe */
    else enfocarTicket();
  }
  qsa('[data-abrir-hoja]').forEach(function (b) { b.addEventListener('click', abrirHoja); });
  qsa('[data-cerrar-hoja]').forEach(function (b) { b.addEventListener('click', cerrarHoja); });
  if (hoja) hoja.addEventListener('click', function (e) { if (e.target === hoja) cerrarHoja(); });

  /* ---------- animacion: la bolita sale del boton y llega al ticket ---------- */
  function volar(a) {
    if (!E.animar() || !a || !doc.body.animate) return;
    requestAnimationFrame(function () {
      var meta = (barra && !barra.hidden) ? qs('.pb-n', barra) : (ladoVisible ? qs('[data-tk-total]', lado) : null);
      if (!meta) return;
      var b = meta.getBoundingClientRect();
      if (!a.width || !b.width) return;
      var dot = doc.createElement('span'); dot.className = 'vuela'; dot.setAttribute('aria-hidden', 'true');
      dot.style.left = (a.left + a.width / 2 - 8) + 'px'; dot.style.top = (a.top + a.height / 2 - 8) + 'px';
      doc.body.appendChild(dot);
      var dx = (b.left + b.width / 2) - (a.left + a.width / 2), dy = (b.top + b.height / 2) - (a.top + a.height / 2);
      var an = dot.animate([{ transform: 'translate(0,0) scale(1)', opacity: 1 }, { transform: 'translate(' + dx * 0.55 + 'px,' + (dy * 0.55 - 40) + 'px) scale(1.15)', opacity: 1, offset: 0.55 }, { transform: 'translate(' + dx + 'px,' + dy + 'px) scale(.35)', opacity: .2 }], { duration: 620, easing: 'cubic-bezier(.4,.1,.3,1)' });
      var fin = function () { dot.remove(); var d = (barra && !barra.hidden) ? barra : lado; if (d) { d.classList.remove('pop'); void d.offsetWidth; d.classList.add('pop'); } };
      an.onfinish = fin; an.oncancel = fin;
    });
  }

  /* ---------- conexiones ---------- */
  doc.addEventListener('click', function (e) {
    var t = e.target; if (!t || !t.closest) return;
    var add = t.closest('.add[data-add]');
    if (add) { var f = add.closest('.op'); cambiarFila(f, 1, add); var q = qs('.mas-uno', f); if (q && !q.closest('[hidden]')) q.focus(); return; }
    var mas = t.closest('[data-item] .mas-uno'), menos = t.closest('[data-item] .menos');
    if (mas) { cambiarFila(mas.closest('.op'), 1, mas); return; }
    if (menos) { var fm = menos.closest('.op'), sigue = buscar(clave(fm.getAttribute('data-op'), supsDe(fm))).qty > 1; cambiarFila(fm, -1); if (!sigue) { var a2 = qs('.add', fm); if (a2) a2.focus(); } return; }
    var sup = t.closest('.sup-btn');
    if (sup) {
      var enc = sup.getAttribute('aria-pressed') !== 'true';
      sup.setAttribute('aria-pressed', enc ? 'true' : 'false'); pintarFilas();
      anunciar(qs('.sup-et', sup).textContent.trim() + ': ' + (enc ? T.extra_si : T.extra_no));
      return;
    }
    var ref = t.closest('[data-add-ref]');
    if (ref) { var fr = qs('[data-item] .op[data-op="' + ref.getAttribute('data-add-ref') + '"]'); if (fr) cambiarFila(fr, 1, ref); }
  });

  if (lado) {
    nuevoTicket(lado, 'lado');
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { ladoVisible = es[0].isIntersecting; pintarBarra(); }, { threshold: 0.05 }).observe(lado);
  }
  if (hoja) nuevoTicket(qs('[data-ticket="hoja"]', hoja), 'hoja');
  /* si la pantalla pasa a ser ancha con la hoja abierta, se cierra: ya hay ticket al lado */
  if (window.matchMedia) {
    var ancho = window.matchMedia('(min-width:1000px)');
    var cambio = function () { if (ancho.matches && hoja && hoja.open) cerrarHoja(); };
    if (ancho.addEventListener) ancho.addEventListener('change', cambio);
  }
  pintar();
})();
