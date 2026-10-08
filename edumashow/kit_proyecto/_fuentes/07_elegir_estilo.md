# 07. Cómo elegir la personalidad y describir el restaurante

Tu parte del diseño es pequeña y decisiva: elegir la personalidad y describir el restaurante con datos reales. El motor hace el resto: elige la portada, la carta, la galería, los bordes entre secciones, los botones, el espaciado, la textura y el paquete de animaciones según el perfil, la cocina, las fotos y el logo, y los cambia de una web a otra para que dos restaurantes nunca tengan la misma web.

## Qué personalidad

ELEGANTE: restaurantes de mantel, cocina de autor o de producto, tickets medios y altos, donde lo normal es reservar mesa y comer con calma. Cada plato lleva descripción y precio único. Necesita una foto grande de portada (activo hero) y fotos del local, y un horario por días. Acción principal: reservar mesa (o llamar). Secciones: portada, idea (solo si hay una historia real), carta, ambiente, reserva (si hay reservas), visita y cierre.

URBANO: parrillas, comida callejera, hamburgueserías, taquerías, areperas, pizzerías al corte, locales de pedido para llevar o para llamar, tickets bajos y medios, donde lo normal es mirar el menú y pedir. La carta es un tablero con filtros, precios grandes, variantes (media libra, una libra) y extras, y las descripciones son opcionales. Necesita una galería de 6 a 9 fotos. Acción principal: pedir o llamar. Incluye un ticket en vivo para armar el pedido. Secciones: portada, regla (si hay una medida que dibujar), cómo pedir, carta, fotos, visita y cierre.

Cómo decidir: ¿lo que más hace el cliente es reservar y sentarse? ELEGANTE. ¿Lo que más hace es ver el menú, llamar o pedir para llevar? URBANO. Si el restaurante hace las dos cosas, elige por su acción principal y el tono de su marca (lema, fotos, nombre). Dilo en Decisiones.

## El perfil (esquema 01, sección 4)

Escribe perfil con lo que dice la hoja: servicio (mesa, barra, llevar, reparto), precio de 1 a 4 y hasta tres rasgos de ambiente. Con ellos el motor decide, por ejemplo, entre una portada de papel claro con la foto en un arco, una foto a pantalla completa con una cortina que se abre, un mural de fotos que suben y bajan, polaroids que caen sobre un fondo de puntos o un cartel del color de la marca. No inventes el perfil: si la hoja no lo permite, omite el campo.

## Lo que decide el motor (no lo escribes)

{{OPCIONES}}

Las cifras de arriba son opciones del catálogo actual; el motor combina una de cada dimensión y comprueba que la combinación no se parezca a la de las últimas webs hechas. Si el catálogo se agotara para una racha de restaurantes parecidos, el verificador lo avisa.

## Campos de estilo que sí escribes

- personalidad: "elegante" o "urbano".
- orden_fotos: "antojo" en URBANO cuando juzgaste las fotos (archivo 06). Si no, omítelo.
- paleta: "auto" siempre: con logo (activo logo), la paleta sale de sus colores más un acento de temporada; sin logo, el motor propone un color de marca según el tono de la cocina y lo aparta de los de las últimas webs (anota en Por confirmar que el dueño lo confirme). En los dos casos el motor comprueba todos los pares de contraste. Las paletas con nombre (brasa y fuego) solo se fijan si el dueño lo pide. Un logo de un solo tono (negro, blanco o grises) no trae color de marca: el motor lo trata como un restaurante sin logo y muestra el logo tal cual. matiz (OPCIONAL, un número de 0 a 359): fija el matiz del color de marca propuesto por el motor cuando el dueño o el usuario piden un color (por ejemplo 158 es un verde jade, 262 un azul índigo, 25 un rojo bermellón); no lo escribas si nadie lo pidió.
- tipografia: omítela. El motor elige entre las parejas ya probadas según la cocina, el nombre y las webs anteriores, para no repetir titular en webs seguidas. No fijes una tipografía a mano.

Parejas tipográficas probadas hoy (para que conozcas el abanico; no las eliges tú):
{{PAREJAS}}

## Datos que cambian la web

- Si hay pedido (URBANO): pedido.canal whatsapp si tienes su WhatsApp, o llamada si solo hay teléfono. Si no hay ni teléfono ni WhatsApp, no pongas pedido.
- Si el restaurante reparte con apps: contacto.reparto y textos.reparto_texto.
- Si la hoja trae la nota de Google (4,0 o más): valoracion (esquema 01, sección 8). Aparece en la portada y en la visita, con su enlace y la fecha.
- Con 5 fotos o más en la galería, el motor puede usar el mosaico de recuadros; con menos, otras galerías.
