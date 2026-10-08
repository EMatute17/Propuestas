# 04. Reglas que aplican a quien escribe la ficha

Estas son las reglas del núcleo de conocimiento de Edumashow que dependen de lo que tú escribes. Salen de cinco estudios (alianzas, psicología, UX, conducta y motor gráfico) más normas técnicas, y se resumen aquí; cada una cita su identificador y el nivel de evidencia (E1 baja, E2 media, E3 alta; N norma o decisión del proyecto; M medida propia).

Las 51 reglas restantes (rendimiento, legibilidad técnica, medición y proceso) las cumple el motor y las prueba el verificador: no te tocan.

## Cómo se resuelven los choques

Cuando dos reglas chocan gana la que lleva el número más bajo, porque el número es un orden de importancia como un podio: el 0 (verdad, legalidad y ética) pasa por encima del 1, el 1 por encima del 2, y así hasta el 6 (variedad entre webs), que cede ante todas las demás. Número bajo quiere decir más importante, no menos. Entre dos reglas con el mismo número, el bloqueo gana al defecto y el defecto a la hipótesis. Una regla con número más alto nunca se cumple a costa de una con número más bajo.

Los puestos: 0, verdad, legalidad y ética; 1, accesibilidad y legibilidad; 2, tarea del visitante: un siguiente paso claro y poca fricción; 3, rendimiento en móvil lento; 4, identidad y estética del restaurante; 5, persuasión (solo como hipótesis a probar); 6, variedad entre webs (gate de unicidad).

## Datos y honestidad

- R-DAT-01 (bloqueo, evidencia E3): Todo dato factual visible (nombre, dirección, teléfono, horario, plato, precio, promoción, alérgeno) consta en la ficha confirmada con su fuente y fecha. Cero valores heredados de otra muestra o plantilla y cero marcadores de relleno. Tú: Cada dato visible sale de la hoja de entrada; nada se hereda de un ejemplo.
- R-DAT-02 (bloqueo, evidencia E3): Un dato ausente se omite o se muestra como por confirmar. Nunca aparece como 0, gratis o sin alérgenos por falta de dato: cero, desconocido y no aplicable no son lo mismo. Tú: Si falta un dato, omite el campo o usa la forma por confirmar; nunca pongas 0, gratis ni sin alérgenos.
- R-DAT-03 (bloqueo, evidencia E3): Cada importe del HTML, de los metadatos y del mensaje de WhatsApp coincide uno a uno con la ficha. Un solo formato de moneda y decimales por página. La web no añade condiciones, depósitos ni descuentos que la ficha no tenga. Tú: Escribe cada precio como número exacto de la carta; no añadas descuentos, depósitos ni condiciones.
- R-DAT-04 (bloqueo, evidencia E3): Cada imagen y video declara su procedencia (propia del restaurante, licenciada de banco libre, de referencia o generada; las de redes sociales solo para el logo, ver R-FOT-01) y su licencia en el manifiesto de activos. Una imagen de referencia, de banco o generada no se presenta como el plato o el local reales: se rotula como imagen de ejemplo. Tú: Cada foto lleva procedencia y permiso; las de referencia o generadas solo valen en un ejemplo ficticio.
- R-DAT-05 (bloqueo, evidencia E3): Toda afirmación factual (premios, antigüedad, superlativos, valoraciones, cifras) lleva fuente y fecha en la ficha. Sin fuente no se publica. Tú: No escribas premios, antigüedad ni cifras sin fuente y fecha; la nota de Google va solo en valoracion.
- R-DAT-06 (defecto, evidencia E3): Los datos volátiles (carta, precios, horarios, promociones) llevan fecha de última confirmación y se revalidan antes de cada entrega. Una promoción vencida no se muestra. Tú: Pon la fecha de hoy en confirmacion.fecha y di en la nota de dónde salen los datos.
- R-DAT-08 (bloqueo, evidencia E3): Si falta un dato crítico (carta, horario o contacto) el motor omite el bloque y lo declara como limitación, o se abstiene de generar. No rellena con texto verosímil, ni platos de ejemplo, ni lorem ipsum. Tú: Si falta la carta, el horario o un contacto, pídelos: el motor no construye sin ellos.

## Ética y marca

- R-ETI-01 (prohibido, evidencia E3): Prohibida la escasez o urgencia inventada: cuentas atrás, quedan N mesas, últimas mesas, solo hoy. Solo se admite si se alimenta de un dato real, vigente y verificable del restaurante. Tú: No escribas escasez ni urgencia (últimas mesas, solo hoy, quedan N).
- R-ETI-02 (prohibido, evidencia E3): Prohibidos los testimonios, reseñas, valoraciones, cifras de clientes o premios inventados. Los ejemplos ficticios de una muestra se rotulan como ejemplo. Una valoración real cita plataforma y fecha. Tú: No escribas testimonios, estrellas ni premios inventados; en un ejemplo ficticio se rotula como ejemplo.
- R-ETI-03 (prohibido, evidencia E3): Prohibido prometer resultados cuantificados (más reservas, más ventas, un porcentaje de mejora) y mostrar porcentajes con falsa precisión. Una nota de calidad nunca se presenta como probabilidad de éxito. Tú: No prometas ventas, reservas ni porcentajes.
- R-ETI-05 (prohibido, evidencia E2): Sin refuerzo variable (ruletas, rasca y gana, premios sorpresa) ni copy encuadrado en pérdida por defecto (no te quedes sin mesa). Ninguna constante universal de aversión a la pérdida. Tú: No escribas ruletas, premios sorpresa ni frases que asusten por lo que se pierde.
- R-ETI-06 (prohibido, evidencia E1): No se infiere ni se usa un perfil psicológico, estado emocional, salud o vulnerabilidad del dueño o del comensal para decidir diseño o texto. La personalización parte de necesidades observadas (sala, recoger, envío, grupo, idioma, hora). Tú: No infieras el estado de ánimo, la salud ni el perfil psicológico de nadie.
- R-ETI-09 (bloqueo, evidencia E1): No se declara probado con usuarios lo que fue simulación, ni accesible o conforme a WCAG sin su alcance, ni el mejor sin un comparador y tareas definidos. Tú: No digas que la web está probada con usuarios ni que cumple WCAG sin decir el alcance.
- R-ETI-10 (bloqueo, evidencia N): Alérgenos, dietas y precios finales se muestran como texto real y solo si constan en la ficha. Ausencia de dato no es ausencia de alérgeno. Tú: No menciones alérgenos ni dietas salvo que consten en la hoja, tal cual.
- R-ETI-11 (bloqueo, evidencia N): Los entregables no mencionan herramientas de IA, nombres de modelos ni de otras agencias. Solo llevan la marca Edumashow. Esto no autoriza presentar imágenes generadas como reales. Tú: No menciones herramientas de IA ni modelos; la marca es Edumashow.
- R-ETI-12 (bloqueo, evidencia N): Comillas: nunca se usan las comillas angulares dobles; siempre comillas rectas. Orden permanente de Eduardo. Tú: Usa solo comillas rectas.

## Fotos

- R-FOT-01 (bloqueo, evidencia N): Ninguna foto viene de Instagram ni de otra red social; solo el logo puede tomarse del perfil del restaurante, y se sube en la mayor calidad disponible. Las demás fotos son originales enviados por el restaurante como archivo (no capturas ni reenviadas por una red) o de un banco libre con la licencia comprobada, y su origen consta en el manifiesto. Las fotos de referencia o generadas solo se admiten en un ejemplo ficticio rotulado. Tú: Ninguna foto de Instagram ni de otra red, salvo el logo. Las demás: archivos originales del restaurante o de banco libre con autor, licencia y enlace.
- R-FOT-02 (bloqueo, evidencia N): Calidad máxima de las fotos: cada foto es un original sin ampliar ni recomprimir, con un lado largo de al menos 2400 px en la portada, 1600 px en las demás y 640 px en el logo, y ninguna se muestra ampliada. La regla no admite excepciones: una foto que no llega se sustituye. Tú: Usa solo fotos que lleguen a 2400 px (portada), 1600 px (resto) y 640 px (logo); si no llegan, no las uses y pide el original como archivo.

## Calificación de Google

- R-VAL-01 (bloqueo, evidencia N): Si el restaurante tiene en Google una calificación de 4,0 o más, la web la muestra (estrellas, nota y número de reseñas) con enlace a su ficha de Google Maps. Solo se publica un dato real con fuente, fecha de consulta y enlace; nunca se inventa, se redondea hacia arriba ni se muestra una nota menor de 4,0. Sin dato real no hay calificación. Tú: Escribe valoracion solo con la nota real de Google de 4,0 o más, con reseñas y fecha; sin dato, sin valoracion.
- R-VAL-02 (prohibido, evidencia N): No se copia ningún comentario de clientes, ni bueno ni malo, ni se muestran extractos: la nota y el número de reseñas ya resumen todos. Está prohibido mostrar comentarios inventados o escoger solo los favorables como si fueran el conjunto. Tú: Nunca copies comentarios de clientes, buenos ni malos: la nota y el número de reseñas bastan.

## Siguiente paso y redacción

- R-SIG-01 (bloqueo, evidencia E3): En el primer viewport de móvil (de 320 a 430 px de ancho) hay un h1 con el nombre, la cocina o la zona, y un CTA primario a un canal real (WhatsApp, teléfono o mapa) completamente visible, sin scroll ni menú previo. Tú: Elige acciones que el restaurante atiende de verdad; la primera de hero es la principal.
- R-SIG-03 (bloqueo, evidencia E1): Los contactos abren la acción directamente: tel: para llamar y wa.me con el mensaje prellenado (restaurante y acción) para WhatsApp, sin páginas intermedias ni registro. Tú: Da el teléfono con código de país y el WhatsApp solo con dígitos: así los contactos abren la acción directa.
- R-SIG-05 (defecto, evidencia E2): Cada botón dice lo que ocurre al pulsarlo (Reservar mesa, Pedir por WhatsApp, Cómo llegar), nunca Haz clic aquí, y su activación produce una respuesta visible. El rótulo coincide con la conducta objetivo declarada en la ficha. Tú: Etiqueta cada botón con un verbo que diga lo que pasa al pulsarlo.
- R-SIG-06 (defecto, evidencia E3): El precio de cada plato es visible junto a su nombre y las condiciones de reserva o pedido (cancelación, mínimo, zona y coste de envío, plazos) se ven antes del paso final. Tú: El precio va junto al nombre del plato; no lo escondas en la descripción.
- R-SIG-10 (proceso, evidencia E3): La web no promete lo que el restaurante no atiende (reserva por WhatsApp sin respuesta, reparto sin confirmar). El restaurante confirma cada promesa operativa antes de publicar. Tú: No ofrezcas lo que el restaurante no atiende (reserva sin WhatsApp, reparto sin confirmar).
- R-SIG-11 (defecto, evidencia E2): Titulares y CTA literales, sin vacíos de curiosidad (No imaginaras que lleva este plato). Los textos son concretos (ingredientes, técnica, origen) y concisos, sin superlativos sin respaldo. Tú: Titulares literales y concretos, sin vacíos de curiosidad.
- R-SIG-12 (defecto, evidencia E1): Escaneo: cada sección tiene un encabezado que declara su función (Carta, Reservar, Visítanos) y jerarquía tipográfica visible, sin muros de texto. No se fija un número mágico de platos o secciones: se prueba por tarea. Tú: Cada sección con un encabezado que dice qué hay.

## Identidad

- R-IDE-01 (defecto, evidencia E3): Cada web tiene identidad propia a partir de datos reales del restaurante (cocina, rango de precios, ciudad, marca, fotos). Toda variación se traza a un campo de la ficha; cambiar colores o adjetivos al azar no cuenta como adaptación. Tú: Usa las palabras, los platos, la zona y el lema del propio restaurante; nada genérico.
- R-IDE-04 (defecto, evidencia E3): Los activos de marca aprobados por el restaurante (logo, colores, tipografías, fotos) son restricciones fijas. La variación solo actúa sobre lo no fijado. Tú: El logo, los colores y las fotos del restaurante son fijos: no los cambies.
- R-IDE-07 (defecto, evidencia E3): Las fotos de comida se ordenan por antojo: cada foto se juzga mirándola con 7 criterios (textura, reconocible, acción, protagonista, luz cálida lateral, señal de calor, mano o cubierto) con 0, 1 o 2, y ese juicio pesa el 65 %; el 35 % son medidas técnicas objetivas (nitidez en la zona del plato, calidez, saturación y contraste). Solo cuentan las fotos reales y sin marcas ajenas, y el orden que se ve en el mural y la galería es el del ranking, con el motivo de cada foto escrito en la ficha. Tú: Si ordenas por antojo, juzga mirando cada foto con los siete criterios y escribe el motivo.

## Persuasión

- R-PER-02 (hipotesis, evidencia E1): La prueba social y las normas (el más pedido) solo se usan con dato real y fechado, y se les asigna un efecto esperado pequeño. No sustituyen a la reducción de fricción. Tú: La prueba social solo con dato real y fechado (la nota de Google).

## Variedad

- R-VAR-04 (bloqueo, evidencia N): Ninguna web se parece a otra: la composición (portada, carta, galería, ornamento, botones, navegación y paquete de animaciones) se elige de un catálogo según los datos reales del restaurante (cocina, nivel de precio, ambiente, servicio, fotos y logo), con rotación frente a las webs ya hechas, y nunca por defecto. Cada elección y su motivo constan en el manifiesto. Tú: No fijes la composición del diseño: aporta el perfil y los datos, y el motor varía la web.

## Muestras

- R-MUE-03 (bloqueo, evidencia E3): Las necesidades del restaurante se formulan como hipótesis o pregunta, nunca como hecho, y sin aludir a presupuesto, margen ni motivos privados. Tú: Habla de las necesidades del restaurante como pregunta o hipótesis, nunca como hecho.
- R-MUE-05 (bloqueo, evidencia N): No se usan nombre, logo, fotos ni carta de un negocio real sin su permiso. La muestra para un prospecto real se enseña primero a su dueño. La cinta visible y el noindex evitan que se confunda con el sitio oficial. Tú: No uses nombre, logo, fotos ni carta de un negocio real sin permiso: permiso pendiente.

