# Cómo se hacen las webs aquí, y cómo las hacía la conversación anterior

Este documento responde a tres preguntas de Eduardo: si se le sacó el máximo provecho a los estudios, si se puede mejorar mucho y si cada web
tendrá su propia personalidad. Lo que se sabe de la conversación anterior sale de lo que dejó hecho (las muestras Lumbre, Chispa y Coucou, el
Documento Maestro y el kit v4.5) y del texto que Eduardo pegó; no se sabe lo que pensó el otro asistente, solo lo que construyó.

## 1. Respuestas directas

**¿Se le sacó el máximo provecho a los estudios y al motor gráfico? No.** La primera versión de Al Fuego aplicaba bien las reglas de
verdad, accesibilidad y velocidad (cada una con su prueba en el Gate), pero el motor gráfico casi no se veía: la paleta y la tipografía estaban
elegidas a mano, no había ranking de fotos, la idea de la casa no se dibujaba y el menú era una lista larga. Eduardo lo vio y tenía razón.

**¿Se puede mejorar mucho? Sí, y esta versión lo hace en cuatro frentes:** el menú pasa a ser una experiencia (filtros, tarjetas con Agregar, ticket en
vivo, envío por WhatsApp), la página tiene más secciones y más movimiento, el director de estilo deduce paleta, tipografía y orden de fotos de los
datos del restaurante y deja escrita la razón de cada decisión, y el Gate prueba todo eso en un navegador real.

**¿Cada web tendrá su personalidad? Parcialmente, y se dice con claridad qué falta.** Hay dos personalidades de estructura completas (elegante y urbana).
Dentro de cada una, el director cambia paleta (del logo), tipografía del titular (de 13 parejas, 12 ya probadas en el Gate, con rotación para no repetirse), orden de fotos,
forma y movimiento. Todavía no hay una tercera estructura (casual y colorida, como Chispa) ni una rústica: son las siguientes.

## 2. Cómo lo hizo la conversación anterior (lo que se ve en sus archivos)

- Cada muestra era un solo archivo HTML con las fotos incrustadas.
- Los datos del restaurante viajaban en un objeto JSON dentro de la página (el nombre, el WhatsApp, el formato de la moneda, la zona horaria, el
  horario y los platos con su precio). Un único programa común leía ese objeto y activaba lo que encontraba: revelado al desplazarse, importes con
  el mismo formato que en Python, estado abierto o cerrado con la hora del restaurante, panel de Edumashow, filtros de la carta, carrito con hoja de
  pedido, reserva con validación del horario.
- La personalidad salía de variables de CSS y de piezas reutilizables (cinta, panel, tarjetas, sello giratorio, marquesina, hoja del pedido).
- El kit aportaba el método: paleta de la marca más acento de temporada, tipografías libres con rotación, fotos puntuadas por antojo, la idea
  dibujada con una cifra o una regla, y un Gate que no deja salir nada sin prueba.

## 3. Qué hace este repositorio, capa por capa

| Capa | Qué decide o hace | Dónde está | Cómo se comprueba |
|---|---|---|---|
| Datos | La ficha JSON es la única fuente: nada de lo que se ve sale de otro sitio | `edumashow/fichas/`, `motor/generar.py` | G-DATOS compara cada importe, horario, teléfono y WhatsApp con la ficha; las cifras derivadas (precio por libra) se recalculan |
| Paleta | Color de identidad del logo (k-means en OKLab, sin neutros), acento de temporada WGSN x Coloro con relación de tono y unidad, fondos teñidos hacia la marca, ajuste hasta cumplir 4,5 a 1 | `motor/color.py` | G-PALETA mide los pares sobre los colores finales; G-CONTRASTE mide los píxeles reales |
| Tipografía | Pareja elegida por el carácter de la cocina, que cubra todos los caracteres que de verdad se sirven, que esté probada en el Gate (12 de 13) y que no repita fuente ni clase | `motor/tipografia.py`, `motor/estilo.py`, `motor/huella.py`, `gate/parejas_probadas.json` | G-HUELLA (unicidad y rotación) y G-FUENTES |
| Fotos | Siete criterios juzgados mirando cada foto (65 %) y cuatro medidas técnicas (35 %); el orden del mural y de la galería es el del ranking | `motor/antojo.py`, `motor/piezas_urbano.py` | G-ANTOJO comprueba que lo que se ve coincide con el ranking del manifiesto |
| Idea de la casa | La regla de medidas: barras proporcionales a las libras de cada picada con su precio y su precio por libra | `motor/piezas_urbano.py` (regla) | G-DATOS recalcula cada cifra derivada |
| Pedido | Menú con filtros, tarjetas con Agregar y extras, ticket en vivo (lateral en pantallas anchas, hoja desde abajo en el teléfono), mensaje de WhatsApp con total | `motor/pedido.py`, `plantillas/pedido.js`, `plantillas/pedido.css` | G-PEDIDO agrega líneas reales, recalcula el total en Python y lee el mensaje que se abriría |
| Sin JavaScript | Todo se lee igual: fotos, menú con precios, panel de la muestra por enlace, aviso para llamar | `plantillas/base.css` (`:target`), `motor/unico.py` | G-SINJS con el JavaScript apagado |
| Movimiento | Mural, sello, marquesina, barras, entradas, inclinación; pausa que detiene solo lo que se repite; movimiento reducido | `plantillas/urbano.css`, `plantillas/base.css` | G-MOVIMIENTO |
| Velocidad | Sin terceros, fuentes recortadas, imágenes AVIF y WebP, HTML con CSS y JS dentro | `motor/generar.py` | Lighthouse en móvil lento simulado (G-REND) |

## 4. Qué estudios se aplican y dónde

La matriz completa está en `edumashow/nucleo/TRAZABILIDAD.md`: cada regla (79) y cada control del informe del motor gráfico con su estado
(Aplicada, Sin prueba, Parcial, No aplica o Pendiente) y los archivos donde vive. El documento se valida solo: si una regla cita un archivo o
un símbolo que ya no existe, el script falla.

## 5. Lo que se aprendió al probar de verdad (y por qué importa)

- La pausa de animación detenía también las entradas cortas: con la pausa activa, un cambio de categoría dejaba las tarjetas invisibles y la hoja del
  ticket se quedaba fuera de pantalla. Ahora la pausa solo detiene lo que se repite sin fin.
- Un desplazamiento hecho por programa al cargar la página (centrar el filtro activo) hacía que Chrome dejara de medir el pintado principal (LCP) en
  el teléfono y Lighthouse puntuara 0. Ahora ese desplazamiento solo ocurre tras un toque.
- Un nombre de variable de CSS repetido (`--max`) rompía las marcas de la regla: se vio al mirar la captura, no por el Gate.
- Una vista previa que necesitaba JavaScript para mostrar las fotos se veía vacía en visores de teléfono que no lo ejecutan.
- Probar el modo final con un horario de prueba encontró un fallo del propio Gate: leía la tipografía escrita en la ficha ("auto") en vez de la que había
  decidido el director. Se corrigió para que mire la pareja ya resuelta del manifiesto.
- Probar parejas tipográficas dos veces dio resultados distintos por culpa del medidor, no de las webs: contaba como texto sin contraste lo que tapaba la barra
  fija del teléfono. Ahora solo mide lo que la persona ve. Y a una web de prueba que es copia de otra no se le exige ser distinta de las demás (G-HUELLA).
- Una revisión independiente del código (hecha por otro agente, sin tocar nada) encontró dos fallos graves que el Gate no veía porque solo probaba la página recién
  cargada: con una pantalla de 1000 px o más, la pastilla Ver mi pedido abría una hoja que no se dibuja y dejaba la página sin responder, y el aro de foco de los botones
  más y menos y de los filtros quedaba recortado por su contenedor. Se corrigieron y el Gate ahora prueba las dos cosas con el pedido en marcha (pulsa la pastilla desde
  lejos del ticket y mide, con el foco de teclado, que ningún aro quede recortado ni con menos de 3 a 1 de contraste). Las mismas pruebas encontraron el mismo
  problema en las pestañas de Lumbre, que también se corrigió. Otros hallazgos reales que se arreglaron: los extras con precio no se leían sin JavaScript, un extra
  tocado después de Agregar no se sumaba al pedido sin avisar (ahora van antes del botón y se anuncian), el aviso de WhatsApp quedaba con datos viejos, un logo
  de pocos colores rompía el cálculo de la paleta, y la inclinación de las tarjetas con el puntero nunca se veía.
- Un titular muy ancho (la pareja Outfit) llegó a tocar el sello giratorio de la portada en una pantalla de 1440 x 900. El Gate lo detectó y esa pareja
  no se propone mientras la portada no se ajuste.

## 6. Lo que sigue sin estar igual de bien

- Solo dos estructuras de personalidad. Falta una tercera (casual y colorida, con plato flotante) y una rústica.
- El pedido en vivo (filtros, tarjetas con Agregar, ticket y WhatsApp) existe en la personalidad urbana. La elegante (Lumbre) conserva su carta de pestañas y su
  reserva por WhatsApp: llevarle el pedido es el siguiente paso natural.
- Las parejas tipográficas de la personalidad elegante son todas con serifa, así que la regla de rotación (misma clase en 2 de las 4 webs anteriores es fallo)
  obligará a alternar con la urbana o a añadir titulares elegantes sin serifa.
- Sin video de portada ni recortes de platos de estudio (las fotos de Al Fuego son recortes de capturas de 385 px: para la web final hacen falta los originales).
- El director de estilo es heurístico: el tono sale de palabras de la cocina y los pesos de los criterios de antojo son de diseño, no calibrados con clientes.
- Sin datos estructurados (JSON-LD) ni medición propia para el modo final, y sin pruebas en Safari y Firefox reales ni con personas.
- Una muestra de un negocio real solo se enseña primero a su dueño; los datos y las fotos de Al Fuego están por confirmar (`informes/alfuego/por_confirmar.md`).

## 7. Cómo se añade un restaurante

1. Crear su ficha en `edumashow/fichas/` (datos, carta con ids, horario o horario por confirmar, textos, activos con procedencia y, si se ordena por antojo,
   el juicio de cada foto). Para paleta y tipografía automáticas: `"paleta": "auto"` y `"tipografia": "auto"` en `estilo`.
2. Generar: `python3 -m edumashow.motor.generar edumashow/fichas/NUEVA.json --salida muestras`.
3. Verificar: `python3 -m edumashow.gate.verificar edumashow/fichas/NUEVA.json --sitio muestras/NUEVA`. Con APTO se registra su huella de diseño.
   Al entregar una web, conviene escribir en su ficha la pareja y la paleta que el director eligió (están en `decisiones_de_diseno` del manifiesto): así, si
   más adelante se registran otras webs, regenerar la misma ficha no cambia la tipografía por la regla de rotación.
4. Versión de un solo archivo: `python3 -m edumashow.motor.unico muestras/NUEVA muestras/NUEVA.unico.html`.
