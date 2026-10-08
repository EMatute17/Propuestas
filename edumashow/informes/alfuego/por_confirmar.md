# Al Fuego Grill: lo que falta confirmar con el restaurante

La muestra se hizo solo con lo que Eduardo envió: capturas del Instagram público @alfuego_grill, el volante y el menú impreso.
Nada de esto lo ha confirmado el restaurante. Esta lista es lo que hay que llevarle al dueño antes de publicar nada.

## Datos que salen de las capturas (hay que confirmarlos)

| Dato | Lo que dice la muestra | De dónde sale | Duda |
|---|---|---|---|
| Teléfono | 786 728 2934 (llamada en un toque) | Volante, perfil y menú impreso | Ninguna: coincide en las tres fuentes |
| Dirección | 9100 S Dixie Hwy, Miami, FL 33156 | Volante, perfil y menú impreso | Confirmar que es un local fijo y no un trailer que cambia de sitio (el mapa apunta a esa dirección) |
| Horario | 11:00 a. m. a 10:00 p. m. | Texto de un video de su Instagram | Faltan los días de atención. Mientras no se confirmen la web no dice si está abierto o cerrado |
| Precios | Todos los del menú impreso (62 platos y bebidas) | Foto del menú impreso | Confirmar que están vigentes. Un precio impreso puede haber cambiado |
| Chuletas de cordero | Media libra 16 y una libra 30 | Menú impreso | La porción de media libra se lee 11/2 lb en la imagen: puede ser un error de imprenta. La web lo avisa en esa tarjeta |
| Filete mignon con tocino | Más 2 dólares | Menú impreso (con bacon +2) | Confirmar que el 2 son dólares |
| Contenido de tostones, sandwich y tacos | Los ingredientes entre paréntesis del menú, tal como se imprimen | Menú impreso | Confirmar si son opciones a elegir o ingredientes fijos |
| Pedidos a domicilio | DoorDash y Uber Eats | Logotipos al pie del menú impreso | Faltan los enlaces a sus páginas en cada app. Sin ellos la web solo los nombra |
| Redes | Instagram y TikTok (@alfuego_grill) | Perfil de Instagram y volante | Facebook aparece en el menú, pero su nombre no se puede verificar como dirección: no se enlaza |
| Lema | Sabor · Calidad · Pasión / Flavor · Quality · Passion | Volante | Ninguna |

## Fotos y logo

- Son recortes de capturas de pantalla del Instagram público del restaurante (385 px de ancho cada foto). Alcanzan para la muestra,
  pero para la web final hay que pedir las fotos originales al restaurante (o hacer una sesión de fotos).
- El permiso de uso está pendiente en cada foto y en el logo. Se muestra la muestra primero al dueño; si no la quiere, se retira con
  el enlace del pie (pedir que retiren esta muestra).
- Ninguna foto usada muestra personas. Se descartó una foto del perfil donde sale una persona.
- Cada recorte conserva su caja y el hash de la captura original en `edumashow/activos/origen/alfuego/recortes.json`.

## Lo que no se ha puesto a propósito

- Reseñas, seguidores, premios, antigüedad o frases como el mejor de Miami: no hay datos verificados.
- La promoción 2 libras de carne por 54 dólares que aparece en una publicación: es de una publicación puntual y puede estar vencida.
- Reservas: el restaurante no las ofrece en lo que se vio. La acción principal es llamar.

## Cuando el dueño conteste

Se completan en `edumashow/fichas/alfuego.json`: `horario` por días (y se quita `horario_estado`), `confirmacion.estado` en confirmado,
precios corregidos, enlaces de las apps de reparto, y `muestra.permiso` en concedido. Se pasa el modo a final, se genera y se
verifica de nuevo con el Gate: el paquete nuevo tiene otro hash.
