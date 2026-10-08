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
| Pedido desde la web | El ticket de la muestra manda el pedido por WhatsApp a Edumashow, rotulado como prueba. No se menciona recogida ni entrega propia | Es parte de la muestra, no un dato del restaurante | Preguntar al dueño si quiere recibir pedidos por WhatsApp (y a qué número), si son para recoger o también a domicilio propio, y si quiere una nota con los acompañantes de los platos especiales |
| Medida de las picadas | 1, 2, 3 y 5 libras; el precio por libra se calcula (25, 22,50, 22 y 23 dólares) | Nombre y precio de cada picada en el menú impreso | Si cambian los precios, el cálculo se rehace solo. La etiqueta Menor precio por libra sale de ese cálculo y no es una promoción |

## Fotos y logo

- Son recortes de capturas de pantalla del Instagram público del restaurante (385 px de ancho cada foto). Alcanzan para la muestra,
  pero para la web final hay que pedir las fotos originales al restaurante (o hacer una sesión de fotos).
- El permiso de uso está pendiente en cada foto y en el logo. Se muestra la muestra primero al dueño; si no la quiere, se retira con
  el enlace del pie (pedir que retiren esta muestra).
- Ninguna foto usada muestra personas. Se descartó una foto del perfil donde sale una persona.
- Cada recorte conserva su caja y el hash de la captura original en `edumashow/activos/origen/alfuego/recortes.json`.
- El orden de las fotos en el mural y en la galería sale de un ranking de antojo (7 criterios juzgados mirando cada foto y 4 medidas técnicas; la tabla está en el informe del Gate). Los juicios son de quien preparó la muestra: si el dueño prefiere otro orden, se cambian en la ficha. La foto del lomo con la tabla del logo se ve muy pulida: confirmar con el restaurante que es una foto suya real, no una ilustración.

## Lo que no se ha puesto a propósito

- Reseñas, seguidores, premios, antigüedad o frases como el mejor de Miami: no hay datos verificados.
- La promoción 2 libras de carne por 54 dólares que aparece en una publicación: es de una publicación puntual y puede estar vencida.
- Reservas: el restaurante no las ofrece en lo que se vio. La acción principal es llamar.

## Cuando el dueño conteste

Se completan en `edumashow/fichas/alfuego.json`: `horario` por días (y se quita `horario_estado`), `confirmacion.estado` en confirmado,
precios corregidos, enlaces de las apps de reparto, y `muestra.permiso` en concedido. Se pasa el modo a final, se genera y se
verifica de nuevo con el Gate: el paquete nuevo tiene otro hash.
