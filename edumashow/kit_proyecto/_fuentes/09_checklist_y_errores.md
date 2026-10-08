# 09. Checklist antes de responder y errores más comunes

## Checklist

1. ¿Es UN solo restaurante y todos los datos salen de la hoja de entrada? Nada inventado: nombre, dirección, teléfono, horario, platos, precios, ingredientes.
2. ¿id en minúsculas sin tildes, igual que la carpeta de fotos, y cada archivo de foto escrito como id/nombre.ext con los nombres de la hoja?
3. ¿negocio completo (nombre, cocina, ciudad, pais, direccion, zona_horaria, lema, descripcion)? ¿zona_horaria válida? ¿pais de la lista?
4. ¿telefono con signo más y solo dígitos, whatsapp solo dígitos o null? ¿mapa_consulta con nombre y dirección?
5. ¿Horario por días en el formato de listas, o horario_estado por_confirmar con horario_texto? ¿Sin inventar días?
6. ¿Cada plato con id único, nombre y precio (número) o variantes, nunca ambos ni ninguno? ¿Los platos sin precio fuera de la carta?
7. ¿ELEGANTE: todos los platos con descripcion, ningún plato con variantes, activo hero, reservas y contacto.whatsapp si hay sección reserva?
8. ¿URBANO: galería de 6 a 9 fotos, acciones, y los textos obligatorios (incluidos horario_aviso y reparto_texto cuando corresponda)?
9. ¿Cada foto con archivo, alt concreto y procedencia con permiso? ¿Antojo en todas las fotos de comida y del local o en ninguna?
10. ¿estilo coherente con la personalidad y orden sin secciones sin datos (idea, reserva, regla, como)? ¿paleta "auto" solo si hay logo?
11. ¿muestra: ejemplo_ficticio true solo si el restaurante es inventado; si es real, permiso pendiente, origen_datos y nota_panel?
12. ¿Sin superlativos, escasez, reseñas, premios, promesas de resultados, menciones a inteligencia artificial ni comillas angulares?
13. ¿Respuesta en tres partes: JSON completo en un bloque, Por confirmar y Decisiones?

## Errores que suele dar el validador y cómo se corrigen

- "no es JSON válido": falta o sobra una coma, una comilla o una llave. Devuelve el JSON entero otra vez, sin comentarios dentro.
- "campo requerido": falta una clave obligatoria del esquema 01. Añádela con un dato real; si no lo tienes, pregunta o usa la forma por confirmar.
- "valor no permitido": un campo con un valor fuera de la lista (pais, moneda, forma, movimiento, tipo de acción...). Cambia al valor exacto de la lista.
- "telefono": formato "+" y de 8 a 15 dígitos, sin espacios ni guiones.
- "whatsapp": solo dígitos con el código de país, sin signo.
- "ids de plato repetidos o no válidos": cada plato necesita un id único con letras, números, guion o guion bajo.
- "debe tener un precio o variantes con precio": un plato con las dos formas o con ninguna.
- "la personalidad elegante exige descripción" o "no muestra variantes": ELEGANTE no admite variantes y pide descripción en cada plato.
- "textos.xxx": falta un texto obligatorio de la personalidad. Escríbelo (archivo 05).
- "activos.xxx.archivo (no existe...)": el nombre del archivo no coincide con una foto de la carpeta. Usa los nombres de la hoja de entrada.
- "antojo": un juicio incompleto o fotos sin juicio cuando otras lo tienen. Juzga todas o ninguna (archivo 06).
- "La tipografía no tiene estos caracteres": hay un carácter raro (emoji, símbolo). Quítalo o sustitúyelo por texto.
- "marca prohibida" o "escasez": una frase que no se puede publicar. Reescribe con un dato concreto (archivo 05).
- "paleta auto necesita activos.logo": si no hay logo, usa la paleta "brasa" (ELEGANTE) o "fuego" (URBANO).
- "la paleta derivada del logo no llega al contraste": usa una paleta con nombre.

Cuando el usuario te pegue errores, corrige TODOS, devuelve la ficha entera y no cambies lo que ya estaba bien.
