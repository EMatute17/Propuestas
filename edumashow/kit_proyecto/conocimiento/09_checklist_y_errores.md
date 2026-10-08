# 09. Checklist antes de responder y errores más comunes

## Checklist

1. ¿Es UN solo restaurante y todos los datos salen de la hoja de entrada? Nada inventado: nombre, dirección, teléfono, horario, platos, precios, ingredientes.
2. ¿id en minúsculas sin tildes, igual que la carpeta de fotos, y cada archivo de foto escrito como id/nombre.ext con los nombres de la hoja?
3. ¿negocio completo (nombre, cocina, ciudad, pais, direccion, zona_horaria, lema, descripcion)? ¿zona_horaria válida? ¿pais de la lista?
4. ¿telefono con signo más y solo dígitos, whatsapp solo dígitos o null? ¿mapa_consulta con nombre y dirección?
5. ¿Horario por días en el formato de listas, o horario_estado por_confirmar con horario_texto (solo URBANO)? ¿Sin inventar días?
6. ¿Cada plato con id único, nombre y precio (número) o variantes, nunca ambos ni ninguno? ¿Los platos sin precio fuera de la carta?
7. ¿ELEGANTE: todos los platos con descripcion, ningún plato con variantes, activo hero, horario por días, y reservas con contacto.whatsapp si hay reserva?
8. ¿URBANO: galería de 6 a 9 fotos, acciones, y los textos obligatorios (incluidos horario_aviso y reparto_texto cuando corresponda)?
9. ¿Cada foto con archivo, alt concreto y procedencia con permiso? ¿Ninguna foto de Instagram ni de otra red (solo el logo puede venir de una red)? ¿Las de banco libre con autor, licencia y url?
10. ¿Las fotos llegan a los tamaños pedidos (portada 2400 px, resto 1600 px, logo 640 px)? Si la hoja no da las medidas, anótalo en Por confirmar.
11. ¿URBANO: antojo en todas las fotos de comida y del local o en ninguna? ¿ELEGANTE: sin antojo? ¿Ninguna foto con el logo de otra marca?
12. ¿estilo con solo la personalidad (y orden_fotos si hay antojo), sin portada, carta, galeria, forma, movimiento ni orden? ¿paleta "auto" (con o sin logo)?
13. ¿perfil con lo que dice la hoja (servicio, precio, ambiente), sin inventar?
14. ¿valoracion solo si la hoja trae nota de 4,0 o más, reseñas, fecha y enlace, copiada tal cual y sin comentarios? ¿Sin ella si no hay dato?
15. ¿muestra: ejemplo_ficticio true solo si el restaurante es inventado; si es real, permiso pendiente, origen_datos y nota_panel?
16. ¿Sin superlativos, escasez, reseñas, premios, promesas de resultados, menciones a inteligencia artificial ni comillas angulares?
17. ¿Respuesta en tres partes: JSON completo en un bloque, Por confirmar y Decisiones?

## Errores que suele dar el validador y cómo se corrigen

- "no es JSON válido": falta o sobra una coma, una comilla o una llave. Devuelve el JSON entero otra vez, sin comentarios dentro.
- "campo requerido": falta una clave obligatoria del esquema 01. Añádela con un dato real; si no lo tienes, pregunta o usa la forma por confirmar.
- "valor no permitido": un campo con un valor fuera de la lista (pais, moneda, tipo de acción, servicio, ambiente...). Cambia al valor exacto de la lista.
- "telefono": formato "+" y de 8 a 15 dígitos, sin espacios ni guiones.
- "whatsapp": solo dígitos con el código de país, sin signo.
- "ids de plato repetidos o no válidos": cada plato necesita un id único con letras, números, guion o guion bajo.
- "debe tener un precio o variantes con precio": un plato con las dos formas o con ninguna.
- "la personalidad elegante exige descripción" o "no muestra variantes": ELEGANTE no admite variantes y pide descripción en cada plato.
- "la personalidad elegante necesita el horario por días": ELEGANTE no admite horario por confirmar; pide el horario por días al usuario.
- "textos.xxx": falta un texto obligatorio de la personalidad. Escríbelo (archivo 05).
- "activos.xxx.archivo (no existe...)": el nombre del archivo no coincide con una foto de la carpeta. Usa los nombres de la hoja de entrada.
- "foto sacada de redes sociales": una foto con origen redes_del_restaurante que no es el logo, o cuyo enlace o nombre menciona Instagram. No se puede usar: quítala de la ficha (y de la galería y de la carta) y pide el original en Por confirmar.
- "mide ... px y se exigen al menos ...": la foto no llega a la calidad pedida. Quítala y pide el original como archivo.
- "marcador de relleno (pendiente de ...)": un texto provisional dentro de un campo. El permiso pendiente va solo en procedencia.permiso (pendiente o concedido); licencia describe el uso, por ejemplo "foto propia del restaurante".
- "una foto de banco libre lleva autor, licencia y enlace": completa procedencia con los tres datos reales de la página de la foto.
- "valoracion.nota ... es menor de 4,0" o "valoracion ... ficticio": quita valoracion (o, en un ejemplo ficticio, pon ejemplo true).
- "valoracion.nota: Google muestra un solo decimal": copia la nota tal cual aparece, por ejemplo 4.6.
- "antojo": un juicio incompleto o fotos sin juicio cuando otras lo tienen. Juzga todas o ninguna (archivo 06).
- "La tipografía no tiene estos caracteres": hay un carácter raro (emoji, símbolo). Quítalo o sustitúyelo por texto.
- "marca prohibida" o "escasez": una frase que no se puede publicar. Reescribe con un dato concreto (archivo 05).
- "estilo.xxx ... no existe en la personalidad": estás fijando a mano una opción que no existe en esa personalidad; quita el campo y deja que el motor elija.
- "la paleta derivada del logo no llega al contraste" o "ningún color de marca propuesto ... llega al contraste": usa una paleta con nombre ("brasa" en ELEGANTE, "fuego" en URBANO).

Cuando el usuario te pegue errores, corrige TODOS, devuelve la ficha entera y no cambies lo que ya estaba bien.
