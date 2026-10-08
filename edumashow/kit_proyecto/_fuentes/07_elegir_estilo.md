# 07. Cómo elegir el estilo

Hay dos personalidades completas. El motor decide solo la paleta y la tipografía; tú eliges la personalidad y las secciones.

## Qué personalidad

ELEGANTE: restaurantes de mantel, cocina de autor o de producto, tickets medios y altos, donde lo normal es reservar mesa y comer con calma. La carta va en pestañas y cada plato lleva descripción. Necesita una foto grande de portada (activo hero) y fotos del local. Acción principal: reservar mesa (o llamar). Movimiento lento. Secciones: portada, idea (si hay una historia real), carta, ambiente, reserva (si hay reservas), visita y cierre.

URBANO: parrillas, comida callejera, hamburgueserías, taquerías, areperas, pizzerías al corte, locales de pedido para llevar o para llamar, tickets bajos y medios, donde lo normal es mirar el menú y pedir. La carta es un tablero de tarjetas con filtros, precios grandes, variantes (media libra, una libra) y extras, y las descripciones son opcionales. Necesita una galería de 6 a 9 fotos (alimentan el mural de portada). Acción principal: pedir o llamar. Movimiento rápido. Incluye un ticket en vivo para armar el pedido. Secciones: portada, regla (si hay una medida que dibujar), como pedir, carta, fotos, visita y cierre.

Cómo decidir: ¿lo que más hace el cliente es reservar y sentarse? ELEGANTE. ¿Lo que más hace es ver el menú, llamar o pedir para llevar? URBANO. Si el restaurante hace las dos cosas, elige por su acción principal y el tono de su marca (lema, fotos, nombre). Dilo en Decisiones.

## Campos de estilo según la personalidad

ELEGANTE: personalidad "elegante"; portada "luz_brasas"; carta "pestanas_lista"; galeria "mosaico"; forma "recta"; movimiento "lento". Orden: ["portada", "idea", "carta", "ambiente", "reserva", "visita", "cierre"] (quita idea si no hay historia real y reserva si no hay reservas).

URBANO: personalidad "urbano"; portada "mural_columnas"; carta "chips_tablero"; galeria "cuadricula_ig"; forma "recta"; movimiento "rapido". Orden: ["portada", "regla", "como", "carta", "fotos", "visita", "cierre"] (quita regla si no hay una categoría con medidas, y como si no hay pedido). Con fotos juzgadas: orden_fotos "antojo".

## Paleta y tipografía

- paleta "auto" siempre que el restaurante tenga logo (activo logo): la paleta sale de los colores del logo más un acento de temporada, y el motor comprueba todos los pares de contraste. Sin logo: "brasa" (ELEGANTE) o "fuego" (URBANO).
- tipografia "auto" siempre. El motor elige entre las parejas ya probadas según la cocina, el nombre y las webs anteriores, para no repetir titular en webs seguidas. No fijes una tipografía a mano.

Parejas probadas hoy (para que conozcas el abanico; no las eliges tú):
{{PAREJAS}}

## Forma

"recta" (esquinas rectas, más seria) o "suave" (esquinas redondeadas, más amable). Por defecto, recta. Elige suave solo si la marca del restaurante es claramente redondeada y amable (heladerías, panaderías, cafeterías).

## Datos que cambian el estilo

- Si hay pedido (URBANO): pedido.canal whatsapp si tienes su WhatsApp, o llamada si solo hay teléfono. Si no hay ni teléfono ni WhatsApp, no pongas pedido ni la sección como.
- Si el restaurante reparte con apps: contacto.reparto y textos.reparto_texto.
