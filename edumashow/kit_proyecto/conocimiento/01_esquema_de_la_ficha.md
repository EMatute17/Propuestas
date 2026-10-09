# 01. Esquema de la ficha (motor 0.3.0, Gate 0.3.0, reglas 0.3.0)

La ficha es un archivo JSON con todo lo que se sabe de UN restaurante. El motor solo lee la ficha: lo que no esté en ella no sale en la web. El archivo 10 es el mismo esquema en formato JSON Schema.

Reglas de forma: números como números (25, no "25"); precios sin símbolo ni texto; fechas AAAA-MM-DD; horas HH:MM en 24 h; comillas rectas; ningún campo con valor de relleno. Un campo opcional que no sabes se omite entero (no pongas texto vacío ni "N/A").

Leyenda: OBLIGATORIO siempre; OPCIONAL; URBANO o ELEGANTE cuando solo vale para una personalidad (el archivo 07 explica cuál elegir).

## 1. Identificación y estado de los datos

- id (OBLIGATORIO): palabra corta en minúsculas, sin tildes ni espacios, con guion bajo si hace falta. Ejemplo: donchucho. Es también el nombre de la carpeta de fotos.
- version (OBLIGATORIO): "1.0.0" (la versión de la ficha: una ficha nueva siempre empieza en "1.0.0").
- modo (OBLIGATORIO): "muestra" (la muestra gratuita para un prospecto). Solo "final" si te piden la web completa de un cliente que ya aceptó, con datos confirmados.
- idioma (OBLIGATORIO): "es".
- confirmacion (OBLIGATORIO): estado, fecha y nota.
  - estado: "ejemplo" (restaurante ficticio), "por_confirmar" (negocio real con datos tomados de sus redes o de lo que te pasaron) o "confirmado" (solo en modo final). Sigue lo que dice la hoja en "real o ejemplo inventado": si dice ejemplo, usa "ejemplo" aunque la hoja traiga un Instagram o una nota de Google (también son de ejemplo); si no lo dice o se contradice, usa "por_confirmar".
  - fecha: la de hoy, AAAA-MM-DD. nota: de dónde salen los datos, en una frase honesta.

## 2. Negocio (OBLIGATORIO)

negocio: nombre, cocina, ciudad, pais, direccion, zona_horaria, lema, descripcion (todos obligatorios) y lema_en (OPCIONAL).

- nombre: tal como lo escribe el restaurante.
- cocina: de dos a cinco palabras que dicen qué sirven ("Churrascaria", "Cocina de brasa y pasta fresca", "Arepas y comida callejera").
- pais: código de dos letras. Válidos: DE (Alemania), AR (Argentina), BO (Bolivia), BR (Brasil), CA (Canadá), CL (Chile), CO (Colombia), CR (Costa Rica), EC (Ecuador), SV (El Salvador), ES (España), US (Estados Unidos), FR (Francia), GT (Guatemala), HN (Honduras), IT (Italia), MX (México), NI (Nicaragua), PA (Panamá), PY (Paraguay), PE (Perú), PT (Portugal), PR (Puerto Rico), GB (Reino Unido), DO (República Dominicana), UY (Uruguay), VE (Venezuela).
- direccion: la dirección completa en una línea, como la escribe el restaurante.
- zona_horaria: nombre IANA de su ciudad. Ejemplos: America/Caracas, America/Bogota, America/Mexico_City, America/Lima, America/Santiago, America/Argentina/Buenos_Aires, Europe/Madrid, America/New_York, America/Chicago, America/Los_Angeles, America/Santo_Domingo, America/Panama, America/Guayaquil, America/Montevideo, America/Asuncion, America/La_Paz, America/Costa_Rica, America/Guatemala, America/El_Salvador, America/Tegucigalpa, America/Managua, America/Puerto_Rico, America/Sao_Paulo, Europe/Lisbon, Europe/Paris, Europe/Rome, Europe/Berlin, Europe/London, America/Toronto.
- lema: una frase corta del restaurante (de 3 a 12 palabras). Si tiene lema propio, úsalo tal cual. Si no lo tiene, escribe una frase descriptiva y verificable sobre su cocina (no un eslogan inventado con superlativos). Ver 05.
- descripcion: de 100 a 160 caracteres. Es lo que se ve al compartir el enlace: cocina, ciudad y siguiente paso. Sin superlativos.

## 3. Contacto (OBLIGATORIO el bloque; cada campo es OPCIONAL salvo mapa_consulta)

contacto:
- mapa_consulta (OBLIGATORIO): nombre y dirección para buscar en el mapa. Ejemplo: "Parrilla Don Chucho, Calle 85 # 14-20, Bogotá".
- telefono: formato internacional, signo más y solo dígitos, de 8 a 15. Ejemplo: "+576011112233". telefono_visible: como se ve en pantalla, "601 111 2233".
- whatsapp: solo dígitos con el código de país, sin signo ni espacios. Ejemplo: "573001112233". Pon null si no tienes el WhatsApp del restaurante. Escribe aquí el WhatsApp real del restaurante que da la hoja: en una muestra de un ejemplo ficticio y en los pedidos de cualquier muestra, el motor manda los mensajes de prueba al WhatsApp de Edumashow, nunca al del restaurante.
- instagram y tiktok (OPCIONAL): {"usuario": "parrilladonchucho", "url": "https://www.instagram.com/parrilladonchucho/"}. Solo si los tienes. Es un enlace de contacto: de ahí no se toman fotos.
- reparto (OPCIONAL): [{"nombre": "DoorDash"}, {"nombre": "Uber Eats"}] si el restaurante dice que está en esas apps. Si lo pones, textos.reparto_texto es obligatorio y debe llevar {apps}.

conducta (OPCIONAL, recomendado): {"objetivo": "pedir", "canal": "whatsapp"}. objetivo: reservar, llamar o pedir. canal: whatsapp o telefono. Es lo que el restaurante hace de verdad.

acciones (OBLIGATORIO en URBANO; en ELEGANTE se omite si hay reservas): los botones de la portada y de la barra fija del móvil.
- Forma: {"hero": [...], "barra": [...]}. Cada elemento es {"tipo": "...", "etiqueta": "..."} (la etiqueta es OPCIONAL). hero: hasta dos acciones. barra: hasta tres.
- tipo: reservar (necesita reservas), carta, mapa, llamar (necesita telefono), whatsapp (necesita contacto.whatsapp), instagram (necesita contacto.instagram).
- La primera acción de hero es la principal y debe llevar a un canal real que el restaurante atiende: llamar, whatsapp, mapa o reservar; en URBANO con pedido, carta con la etiqueta "Armar mi pedido" también vale, porque el ticket termina en su WhatsApp o en una llamada. Etiquetas con verbo: "Armar mi pedido", "Pedir", "Reservar mesa".

## 4. Perfil del restaurante (OPCIONAL, muy recomendable)

perfil guía la adaptación del diseño y de las animaciones a ESTE restaurante. Escribe solo lo que dice la hoja o lo que se ve con claridad (la carta, las fotos); si dudas, omítelo y dilo en Decisiones.
- servicio: lista con uno o más de mesa, barra, llevar, reparto.
- precio: número de 1 a 4 según el nivel de la carta respecto a su ciudad (1 económico, 2 medio, 3 alto, 4 muy alto).
- ambiente: hasta tres de familiar, romantico, juvenil, nocturno, tradicional, moderno, terraza, playero, festivo, tranquilo.
Ejemplo: {"servicio": ["llevar", "mesa"], "precio": 2, "ambiente": ["familiar", "juvenil"]}.

## 5. Dinero y horario

- moneda (OBLIGATORIO): una de ARS (AR), BOB (BO), BRL (BR), CAD (CA), CHF, CLP (CL), COP (CO), CRC (CR), DOP (DO), EUR (DE, ES, FR, IT, PT), GBP (GB), GTQ (GT), HNL (HN), MXN (MX), NIO (NI), PEN (PE), PYG (PY), USD (EC, PA, PR, SV, US, VE), UYU (UY), VES. Entre paréntesis, los países que la usan; en un país puede usarse otra (en Venezuela y en Ecuador se paga en USD).
- Horario, una de dos formas (OBLIGATORIO una de las dos):
  - Con horario por días: horario = {"lun": [["12:00","22:00"]], "mar": [...], "mie": ..., "jue": ..., "vie": ..., "sab": ..., "dom": ...}. Cada día es una lista de tramos [apertura, cierre]. Día cerrado: []. Dos turnos: [["12:00","15:30"],["19:00","23:00"]]. Si cierra pasada la medianoche: ["18:00","02:00"]. Un tramo que cruza la medianoche va en el día en que abre (viernes ["17:00","01:00"] es el viernes hasta la una de la madrugada del sábado). Un horario como "todos los días menos los martes" se escribe día por día, con martes: []. Solo si el restaurante da los horarios por día. ELEGANTE exige esta forma.
  - Sin horario por días (por ejemplo, solo "11 a 10"): horario_estado = "por_confirmar" y horario_texto = el texto tal como lo dijo el restaurante ("11:00 a. m. a 10:00 p. m."). No inventes los días. Solo en URBANO, y entonces textos.horario_aviso es obligatorio.

## 6. Carta (OBLIGATORIO)

carta = lista de categorías. Cada categoría: id (palabra corta sin tildes, única), titulo, platos (OBLIGATORIOS) y chip (OPCIONAL, etiqueta corta de una palabra para el filtro), nota (OPCIONAL, una línea bajo el título), foto (OPCIONAL, clave de un activo), presentacion (OPCIONAL, "lista" para acompañantes, bebidas y postres compactos; URBANO).

Cada plato:
- id (OBLIGATORIO): único en toda la carta; solo letras, números, guion y guion bajo. Convención: categoria-1, categoria-2.
- nombre (OBLIGATORIO), nombre_en (OPCIONAL, si el restaurante lo da en inglés), lang (OPCIONAL, para nombres en otro idioma, "it").
- descripcion: en ELEGANTE se escribe siempre que la hoja dé algo que contar, de 8 a 18 palabras con los ingredientes y la técnica. Si la hoja no da los ingredientes de un plato, no los deduzcas del nombre: escribe solo lo que el nombre dice con certeza (aunque queden menos de 8 palabras) y anótalo en Por confirmar. Si ni el nombre dice más (un vino, un whisky, una bebida de marca), omite la descripción: la web muestra solo el nombre. Nunca repitas el nombre como descripción. OPCIONAL en URBANO.
- Precio, una de dos formas (OBLIGATORIO una):
  - precio: número. Ejemplo: 25 o 9.5. En ELEGANTE solo se admite esta forma.
  - variantes (solo URBANO): [{"etiqueta": "½ lb", "precio": 24000}, {"etiqueta": "1 lb", "precio": 44000}]. Ejemplo: media libra y una libra.
  - Nunca las dos a la vez ni ninguna.
  - Única excepción: si el restaurante no publica ningún precio, pon en la raíz de la ficha "carta_sin_precios": true. Entonces NINGÚN plato lleva precio, variantes ni suplementos, textos.carta_nota es obligatoria y dice la verdad ("Carta sin precios publicados. Consulta los importes por WhatsApp."), y no se usan pedido ni idea (no hay con qué sumar). Es todo o nada: si unos platos tienen precio y otros no, no uses esta marca y aplica la regla de abajo.
- suplementos (OPCIONAL, URBANO con pedido): extras con precio. [{"etiqueta": "Con tocino", "precio": 4000}].
- foto (OPCIONAL): clave de un activo, para platos con foto propia.
- medida (OPCIONAL): número (libras, piezas) solo si la ficha usa la sección regla (ver idea).

Si un plato no tiene precio publicado, no lo pongas en la carta (pon el aviso en Por confirmar). Un precio ausente nunca se escribe como 0.

## 7. Galería, textos y activos

galeria (OBLIGATORIO en URBANO, recomendado en ELEGANTE): [{"foto": "clave_del_activo", "pie": "Texto corto"}]. En URBANO, de 6 a 9 fotos (alimentan la portada); si la hoja trae menos, la web se publica igual con las que haya y se anota en Por confirmar que faltan fotos. En ELEGANTE, de 3 a 6 del local; con 5 o más el motor puede elegir el mosaico de recuadros.

textos (OBLIGATORIO): frases cortas de las secciones. Claves obligatorias:
- URBANO: carta_titulo, carta_sobretitulo, fotos_sobretitulo, fotos_titulo, fotos_texto, fotos_aria, visita_titulo. Además: horario_aviso si horario_estado es por_confirmar; reparto_texto (con {apps}) si hay reparto. OPCIONALES: carta_nota, nav_carta, nav_fotos, nav_regla, carta_todo, horario_pendiente, marquesina.
- ELEGANTE: carta_titulo, carta_sobretitulo, ambiente_titulo, reserva_titulo, reserva_texto, visita_titulo. OPCIONALES (se muestran en la web): carta_nota (por ejemplo, que los precios son referenciales o que no incluyen el IVA), ambiente_texto (aclarar que las fotos son de ejemplo), hero_pie (pie de la foto de portada, por ejemplo "Imagen de ejemplo de banco libre.") y horario_aviso (cuando el horario no está confirmado).
- Cómo redactar cada una: archivo 05.

activos (OBLIGATORIO): un objeto cuyas claves son nombres cortos de foto (picada, costilla, logo, hero, sala_azul). Cada activo:
- archivo (OBLIGATORIO): ruta relativa a la carpeta de fotos: "id_del_restaurante/nombre_del_archivo.jpg". Usa exactamente los nombres de archivo que da la hoja de entrada.
- alt (OBLIGATORIO): qué se ve, en una frase concreta ("Picada de costilla, chorizo y papa criolla sobre una tabla de madera"). Nada de "foto de comida".
- procedencia (OBLIGATORIO en un negocio real; opcional si la ficha tiene procedencia_activos general): origen, descripcion, licencia, permiso y, para banco libre, autor y url.
  - origen permitido: propia_del_restaurante (el archivo original que envió el restaurante; en un ejemplo ficticio, aunque la hoja diga que las envió la dueña, usa referencia) o banco_libre (con autor, licencia y url de la página de la foto). redes_del_restaurante SOLO para el activo logo. referencia y generada SOLO en un ejemplo ficticio.
  - Prohibido: una foto que muestra el logo o el nombre de otra marca, o una marca de agua (ni en la galería ni en la carta): déjala fuera y anótalo en Por confirmar.
  - Prohibido: cualquier foto de Instagram, Facebook, TikTok u otra red, aunque sea del propio restaurante. Si la hoja dice que una foto sale de una red, no la uses (salvo el logo) y pide el original en Por confirmar.
  - permiso: pendiente o concedido (negocio real). El permiso se escribe solo aquí: licencia describe el uso ("foto propia del restaurante") y no lleva textos provisionales como "pendiente de..." (el validador los rechaza como marcador de relleno).
- Tamaño de los originales (el validador los mide): hero al menos 2400 px de lado largo; el resto de fotos al menos 1600 px; el logo al menos 640 px. Sin ampliar ni recomprimir. Si una foto no llega, no se usa: pide el original como archivo (en WhatsApp, enviado como documento y no como foto).
- antojo (OPCIONAL; ver 06): {"juicio": {siete criterios con 0, 1 o 2}, "real": true, "sin_marcas_ajenas": true, "nota": "..."}.
- hero (ELEGANTE, OBLIGATORIO): el activo con clave hero es la foto grande de la portada; foco opcional [x, y] entre 0 y 1.
- logo (OPCIONAL): el activo con clave logo. Con logo, la paleta sale de sus colores; sin logo, el motor propone el color de marca según la cocina (el dueño lo confirma).
- procedencia_activos (OPCIONAL, a nivel de la ficha): una procedencia común para todos los activos que no declaren la suya.

## 8. Calificación de Google (OPCIONAL)

valoracion: {"fuente": "google", "nota": 4.6, "resenas": 412, "fecha": "2026-10-08", "url": "https://maps.app.goo.gl/..."}
- Solo si la hoja trae la nota que el restaurante tiene en Google, el número de reseñas y el día en que se miró, y la nota es de 4,0 o más. Copia la nota tal cual (un decimal), sin redondear hacia arriba.
- url (OPCIONAL): enlace a su ficha de Google Maps. Sin url, el enlace busca el local en Google Maps con mapa_consulta.
- Sin dato o con menos de 4,0: no pongas valoracion y anótalo en Por confirmar. Nunca inventes una nota.
- La web no copia comentarios de clientes (ni buenos ni malos): solo la nota y el número de reseñas. En un restaurante ficticio, valoracion lleva "ejemplo": true y se rotula como ejemplo; en uno real, nunca.

## 9. Estilo (OBLIGATORIO, pero casi todo lo decide el motor)

estilo: {"personalidad": "urbano"} y, en URBANO con fotos juzgadas, "orden_fotos": "antojo". El archivo 07 explica cómo elegir la personalidad.
- personalidad (OBLIGATORIO): "elegante" o "urbano".
- orden_fotos: "antojo" ordena las fotos del mural y la galería por el juicio de antojo (necesita antojo en todas las fotos de comida y del local). Si no, omítelo.
- paleta: "auto" (por defecto): con logo sale de sus colores; sin logo, el motor propone un color de marca según la cocina y se anota para confirmarlo con el dueño. Las paletas con nombre ("brasa", "fuego") solo se fijan si el dueño lo pide. tipografia: omítela o escribe "auto".
- NO escribas portada, carta, galeria, ornamento, boton, densidad, textura, animaciones, forma, movimiento ni orden: el motor elige cada una según el perfil, la cocina, las fotos y el logo, y las varía de una web a otra. Solo se fijan a mano si el dueño lo pidió expresamente; dilo en Decisiones.

## 10. Solo ELEGANTE

- reservas (OBLIGATORIO si la acción principal es reservar mesa, sea por WhatsApp o por teléfono; si la hoja no da máximo de personas, intervalos ni antelación, usa exactamente estos valores y dilo en Decisiones): {"maximo_personas": 12, "personas_por_defecto": 2, "paso_minutos": 30, "ultima_antes_del_cierre_min": 60, "antelacion_min": 60, "hora_preferida": "20:00"}. Requiere contacto.whatsapp del restaurante (la reserva llega a ese número), salvo que sea un ejemplo ficticio.
- historia (OPCIONAL): {"cifra": 14, "unidad": "horas de brasa", "texto": "...", "pasos": [{"titulo": "...", "texto": "..."}]}. SOLO con hechos que el restaurante te dio. Si no te dio una cifra y una historia reales, no la escribas. La historia de la ficha de ejemplo es ficticia: copia la forma, nunca los datos.

## 11. Solo URBANO

- pedido (OPCIONAL, recomendado): activa el ticket en vivo. {"canal": "whatsapp", "nota_ejemplo": "Una indicación para la cocina"}. canal: "whatsapp" o "llamada" (si no hay WhatsApp, "llamada" y contacto.telefono es obligatorio). En una muestra el pedido llega a Edumashow como prueba.
- idea (OPCIONAL): la sección regla dibuja barras proporcionales a una medida (libras, piezas) con precio por unidad. Solo si una categoría tiene al menos dos platos con medida y un precio único cada uno (por ejemplo las picadas de 1, 2, 3 y 5 libras). {"tipo": "medida", "categoria": "picadas", "unidad": "lb", "por": "por libra", "sobretitulo": "...", "titulo": "...", "texto": "...", "texto_js": "...", "mejor": "Menor precio por libra", "nota": "..."}. Si no hay una categoría así, omite idea.

## 12. Solo en una muestra

muestra (OBLIGATORIO en modo muestra):
- Restaurante ficticio: {"ejemplo_ficticio": true, "base_url": null}.
- Negocio real: {"ejemplo_ficticio": false, "permiso": "pendiente", "origen_datos": "de dónde salen los datos", "nota_panel": "qué falta por confirmar con el restaurante", "incluye": ["tres frases sobre lo que recibe el dueño"], "base_url": null}. No prometas resultados en incluye.

## 13. Lo que NO escribes

gate_pruebas_pedido, gate_pruebas_horario y excepciones_gate son de las pruebas, no tuyos: el validador los completa. Si ves estos campos en algún ejemplo antiguo, no los copies. Tampoco escribas firma ni ningún campo que no esté en este esquema: el validador rechaza los campos desconocidos.
