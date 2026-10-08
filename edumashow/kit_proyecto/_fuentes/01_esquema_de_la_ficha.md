# 01. Esquema de la ficha (motor {{VERSION}})

La ficha es un archivo JSON con todo lo que se sabe de UN restaurante. El motor solo lee la ficha: lo que no esté en ella no sale en la web.

Reglas de forma: números como números (25, no "25"); precios sin símbolo ni texto; fechas AAAA-MM-DD; horas HH:MM en 24 h; comillas rectas; ningún campo con valor de relleno. Un campo opcional que no sabes se omite entero (no pongas texto vacío ni "N/A").

Leyenda: OBLIGATORIO siempre; OPCIONAL; URBANO o ELEGANTE cuando solo vale para una personalidad (el archivo 07 explica cuál elegir).

## 1. Identificación y estado de los datos

- id (OBLIGATORIO): palabra corta en minúsculas, sin tildes ni espacios, con guion bajo si hace falta. Ejemplo: alfuego. Es también el nombre de la carpeta de fotos.
- version (OBLIGATORIO): "1.0.0".
- modo (OBLIGATORIO): "muestra" (la muestra gratuita para un prospecto). Solo "final" si te piden la web completa de un cliente que ya aceptó, con datos confirmados.
- idioma (OBLIGATORIO): "es".
- confirmacion (OBLIGATORIO): estado, fecha y nota.
  - estado: "ejemplo" (restaurante ficticio), "por_confirmar" (negocio real con datos tomados de sus redes o de lo que te pasaron) o "confirmado" (solo en modo final).
  - fecha: la de hoy, AAAA-MM-DD. nota: de dónde salen los datos, en una frase honesta.

## 2. Negocio (OBLIGATORIO)

negocio: nombre, cocina, ciudad, pais, direccion, zona_horaria, lema, descripcion (todos obligatorios) y lema_en (OPCIONAL).

- nombre: tal como lo escribe el restaurante.
- cocina: de dos a cinco palabras que dicen qué sirven ("Churrascaria", "Cocina de brasa y pasta fresca", "Arepas y comida callejera").
- pais: código de dos letras. Válidos: {{PAISES}}.
- direccion: la dirección completa en una línea, como la escribe el restaurante.
- zona_horaria: nombre IANA de su ciudad. Ejemplos: America/Caracas, America/Bogota, America/Mexico_City, America/Lima, America/Santiago, America/Argentina/Buenos_Aires, Europe/Madrid, America/New_York, America/Chicago, America/Los_Angeles, America/Santo_Domingo, America/Panama, America/Guayaquil, America/Montevideo, America/Asuncion, America/La_Paz, America/Costa_Rica, America/Guatemala, America/El_Salvador, America/Tegucigalpa, America/Managua, America/Puerto_Rico, America/Sao_Paulo, Europe/Lisbon, Europe/Paris, Europe/Rome, Europe/Berlin, Europe/London, America/Toronto.
- lema: una frase corta del restaurante (de 3 a 12 palabras). Si tiene lema propio, úsalo tal cual. Si no lo tiene, escribe una frase descriptiva y verificable sobre su cocina (no un eslogan inventado con superlativos). Ver 05.
- descripcion: de 100 a 160 caracteres. Es lo que se ve al compartir el enlace: cocina, ciudad y siguiente paso. Sin superlativos.

## 3. Contacto (OBLIGATORIO el bloque; cada campo es OPCIONAL salvo mapa_consulta)

contacto:
- mapa_consulta (OBLIGATORIO): nombre y dirección para buscar en el mapa. Ejemplo: "Al Fuego Grill, 9100 S Dixie Hwy, Miami, FL 33156".
- telefono: formato internacional, signo más y solo dígitos, de 8 a 15. Ejemplo: "+17867282934". telefono_visible: como se ve en pantalla, "786 728 2934".
- whatsapp: solo dígitos con el código de país, sin signo ni espacios. Ejemplo: "584127705633". Pon null si no tienes el WhatsApp del restaurante. En una muestra, los mensajes de prueba van al WhatsApp de Edumashow, nunca al del restaurante.
- instagram y tiktok (OPCIONAL): {"usuario": "alfuego_grill", "url": "https://www.instagram.com/alfuego_grill/"}. Solo si los tienes.
- reparto (OPCIONAL): [{"nombre": "DoorDash"}, {"nombre": "Uber Eats"}] si el restaurante dice que está en esas apps. Si lo pones, textos.reparto_texto es obligatorio y debe llevar {apps}.

conducta (OPCIONAL, recomendado): {"objetivo": "llamar", "canal": "telefono"}. objetivo: reservar, llamar o pedir. canal: whatsapp o telefono. Es lo que el restaurante hace de verdad.

acciones (OBLIGATORIO en URBANO; en ELEGANTE se omite si hay reservas): los botones de la portada y de la barra fija del móvil.
- Forma: {"hero": [...], "barra": [...]}. Cada elemento es {"tipo": "...", "etiqueta": "..."} (la etiqueta es OPCIONAL). hero: hasta dos acciones. barra: hasta tres.
- tipo: reservar (necesita reservas), carta, mapa, llamar (necesita telefono), whatsapp (necesita contacto.whatsapp), instagram (necesita contacto.instagram).
- La primera acción de hero es la principal y debe ser lo que el restaurante realmente atiende. Etiquetas con verbo: "Armar mi pedido", "Pedir", "Reservar mesa".

## 4. Dinero y horario

- moneda (OBLIGATORIO): {{MONEDAS}}.
- Horario, una de dos formas (OBLIGATORIO una de las dos):
  - Con horario por días: horario = {"lun": [["12:00","22:00"]], "mar": [...], "mie": ..., "jue": ..., "vie": ..., "sab": ..., "dom": ...}. Cada día es una lista de tramos [apertura, cierre]. Día cerrado: []. Dos turnos: [["12:00","15:30"],["19:00","23:00"]]. Si cierra pasada la medianoche: ["18:00","02:00"]. Solo si el restaurante da los horarios por día.
  - Sin horario por días (por ejemplo, solo "11 a 10"): horario_estado = "por_confirmar" y horario_texto = el texto tal como lo dijo el restaurante ("11:00 a. m. a 10:00 p. m."). No inventes los días. En URBANO, textos.horario_aviso es obligatorio.

## 5. Carta (OBLIGATORIO)

carta = lista de categorías. Cada categoría: id (palabra corta sin tildes, única), titulo, platos (OBLIGATORIOS) y chip (OPCIONAL, etiqueta corta de una palabra para el filtro), nota (OPCIONAL, una línea bajo el título), foto (OPCIONAL, clave de un activo), presentacion (OPCIONAL, "lista" para acompañantes, bebidas y postres compactos; URBANO).

Cada plato:
- id (OBLIGATORIO): único en toda la carta; solo letras, números, guion y guion bajo. Convención: categoria-1, categoria-2.
- nombre (OBLIGATORIO), nombre_en (OPCIONAL, si el restaurante lo da en inglés), lang (OPCIONAL, para nombres en otro idioma, "it").
- descripcion: OBLIGATORIA en ELEGANTE (de 8 a 18 palabras: ingredientes y técnica); OPCIONAL en URBANO.
- Precio, una de dos formas (OBLIGATORIO una):
  - precio: número. Ejemplo: 25 o 9.5. En ELEGANTE solo se admite esta forma.
  - variantes (solo URBANO): [{"etiqueta": "½ lb", "precio": 15}, {"etiqueta": "1 lb", "precio": 27}]. Ejemplo: media libra y una libra.
  - Nunca las dos a la vez ni ninguna.
- suplementos (OPCIONAL, URBANO con pedido): extras con precio. [{"etiqueta": "Con tocino", "precio": 2}].
- foto (OPCIONAL): clave de un activo, para platos con foto propia.
- medida (OPCIONAL): número (libras, piezas) solo si la ficha usa la sección regla (ver idea).

Si un plato no tiene precio publicado, no lo pongas en la carta (pon el aviso en Por confirmar). Un precio ausente nunca se escribe como 0.

## 6. Galería, textos y activos

galeria (OBLIGATORIO en URBANO, recomendado en ELEGANTE): [{"foto": "clave_del_activo", "pie": "Texto corto"}]. En URBANO, de 6 a 9 fotos (alimentan el mural de la portada). En ELEGANTE, de 3 a 6 del local.

textos (OBLIGATORIO): frases cortas de las secciones. Claves obligatorias:
- URBANO: carta_titulo, carta_sobretitulo, fotos_sobretitulo, fotos_titulo, fotos_texto, fotos_aria, visita_titulo. Además: horario_aviso si horario_estado es por_confirmar; reparto_texto (con {apps}) si hay reparto. OPCIONALES: carta_nota, nav_carta, nav_fotos, nav_regla, carta_todo, horario_pendiente.
- ELEGANTE: carta_titulo, carta_sobretitulo, ambiente_titulo, reserva_titulo, reserva_texto, visita_titulo.
- Cómo redactar cada una: archivo 05.

activos (OBLIGATORIO): un objeto cuyas claves son nombres cortos de foto (picada, lomo, logo, hero, sala_azul). Cada activo:
- archivo (OBLIGATORIO): ruta relativa a la carpeta de fotos: "id_del_restaurante/nombre_del_archivo.jpg". Usa exactamente los nombres de archivo que da la hoja de entrada.
- alt (OBLIGATORIO): qué se ve, en una frase concreta ("Picada de carnes a la parrilla sobre una tabla de madera"). Nada de "foto de comida".
- procedencia (OBLIGATORIO en un negocio real; opcional si la ficha tiene procedencia_activos general): origen (propia_del_restaurante, redes_del_restaurante, banco_libre, referencia o generada), descripcion, licencia, permiso (pendiente o concedido). Para banco libre añade autor y url de la fuente.
- antojo (OPCIONAL; ver 06): {"juicio": {siete criterios con 0, 1 o 2}, "real": true, "sin_marcas_ajenas": true, "nota": "..."}.
- hero (ELEGANTE, OBLIGATORIO): el activo con clave hero es la foto grande de la portada; foco opcional [x, y] entre 0 y 1.
- logo (OBLIGATORIO si estilo.paleta es "auto"): el activo con clave logo; la paleta sale de sus colores.
- procedencia_activos (OPCIONAL, a nivel de la ficha): una procedencia común para todos los activos que no declaren la suya.

## 7. Estilo (OBLIGATORIO). El archivo 07 explica cómo decidir.

estilo: personalidad ("elegante" o "urbano"), paleta, tipografia, portada, carta, galeria, forma, movimiento, orden y, en URBANO, orden_fotos.
- paleta: "auto" (sale del logo; necesita activos.logo) o el nombre de una paleta hecha a mano: {{PALETAS}}. tipografia: siempre "auto".
- portada: "luz_brasas" (ELEGANTE) o "mural_columnas" (URBANO). carta: "pestanas_lista" (ELEGANTE) o "chips_tablero" (URBANO). galeria: "mosaico" (ELEGANTE) o "cuadricula_ig" (URBANO).
- forma: "recta" o "suave". movimiento: "lento" (ELEGANTE) o "rapido" (URBANO).
- orden: lista de secciones. ELEGANTE: portada, idea, carta, ambiente, reserva, visita, cierre. URBANO: portada, regla, como, carta, fotos, visita, cierre. Quita las que no tengas datos para llenar: idea necesita historia; reserva necesita reservas; regla necesita idea; como necesita pedido.
- orden_fotos: "antojo" ordena las fotos del mural y la galería por el juicio de antojo (necesita antojo en las fotos de comida). Si no, omítelo.

## 8. Solo ELEGANTE

- reservas (OBLIGATORIO si orden lleva reserva): {"maximo_personas": 12, "personas_por_defecto": 2, "paso_minutos": 30, "ultima_antes_del_cierre_min": 60, "antelacion_min": 60, "hora_preferida": "20:00"}. Requiere contacto.whatsapp del restaurante (la reserva llega a ese número), salvo que sea un ejemplo ficticio.
- historia (OBLIGATORIO si orden lleva idea): {"cifra": 14, "unidad": "horas de brasa", "texto": "...", "pasos": [{"titulo": "...", "texto": "..."}]}. SOLO con hechos que el restaurante te dio. Si no te dio una cifra y una historia reales, quita idea del orden. La historia de la ficha de ejemplo es ficticia: copia la forma, nunca los datos.

## 9. Solo URBANO

- pedido (OPCIONAL, recomendado): activa el ticket en vivo. {"canal": "whatsapp", "nota_ejemplo": "Una indicación para la cocina"}. canal: "whatsapp" o "llamada" (si no hay WhatsApp, "llamada" y contacto.telefono es obligatorio). En una muestra el pedido llega a Edumashow como prueba.
- idea (OPCIONAL): la sección regla dibuja barras proporcionales a una medida (libras, piezas) con precio por unidad. Solo si una categoría tiene al menos dos platos con medida y un precio único cada uno (por ejemplo las picadas de 1, 2, 3 y 5 libras). {"tipo": "medida", "categoria": "picadas", "unidad": "lb", "por": "por libra", "sobretitulo": "...", "titulo": "...", "texto": "...", "texto_js": "...", "mejor": "Menor precio por libra", "nota": "..."}. Si no hay una categoría así, quita regla del orden y omite idea.

## 10. Solo en una muestra

muestra (OBLIGATORIO en modo muestra):
- Restaurante ficticio: {"ejemplo_ficticio": true, "base_url": null}.
- Negocio real: {"ejemplo_ficticio": false, "permiso": "pendiente", "origen_datos": "de dónde salen los datos", "nota_panel": "qué falta por confirmar con el restaurante", "incluye": ["tres frases sobre lo que recibe el dueño"], "base_url": null}. No prometas resultados en incluye.

## 11. Lo que NO escribes

gate_pruebas_pedido, gate_pruebas_horario y excepciones_gate son de las pruebas, no tuyos: el validador los completa. Si ves estos campos en los ejemplos, no los copies.

## 12. Valores de ejemplo para la hoja

{{PAREJAS}}
