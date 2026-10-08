# Comparación antes y después: Lumbre

Antes es la Lumbre original de la primera sesión. Después es la Lumbre nueva, generada por el motor y verificada por el Gate. Las dos se midieron con el mismo método: Chromium, servidor local con compresión y Lighthouse con móvil lento simulado (mediana de 3 pasadas).

Esta tabla mide velocidad y cumplimiento de reglas verificables. No mide ventas, reservas ni lo que opinan los visitantes: eso solo se sabe con personas reales y con datos del restaurante.

## Velocidad y peso

| Medida | Antes | Después |
|---|---|---|
| Rendimiento móvil (Lighthouse) | 77 | 99 |
| Accesibilidad (Lighthouse) | 94 | 100 |
| Buenas prácticas (Lighthouse) | 100 | 100 |
| SEO básico (Lighthouse), muestra con noindex | 91 | 66 |
| SEO básico (Lighthouse), modo final sin noindex | no aplica | 100 |
| LCP en móvil lento | 4,1 s | 2,2 s |
| Peso transferido (móvil) | 662 KB | 180 KB |
| CLS | 0 | 0 |
| Rendimiento en escritorio | 99 | 100 |

El SEO de la muestra baja a propósito: la muestra lleva noindex para que no aparezca en buscadores (regla R-MUE-01) y Lighthouse resta por eso. La original no lo llevaba y era un defecto. El modo final no lleva noindex.

La primera auditoría dio 61 en móvil para la original porque se midió el archivo sin compresión; con compresión, como la sirve un hosting normal, son los números de arriba. Se usa la medida con compresión para que la comparación sea justa.

## Las 24 comprobaciones automáticas

Cumplen: antes 14 de 24 (58,3 por ciento), después 24 de 24 (100,0 por ciento).

Ojo con cómo leerlo: estas 24 comprobaciones salen de las mismas reglas con las que se construyó la web nueva, así que era de esperar que las cumpliera. Sirven para ver qué defectos tenía la original y para vigilar que no vuelvan, no como prueba independiente de que la nueva funcione mejor para un restaurante.

| Comprobación | Antes | Después |
|---|---|---|
| Idioma declarado | no | sí |
| Título y meta descripción | no | sí |
| Aviso de muestra: noindex | no | sí |
| Un solo h1 | sí | sí |
| Encabezados sin saltos | no | sí |
| Marcas de región (header, main, footer) | sí | sí |
| Imágenes con texto alternativo | sí | sí |
| Contraste AA según axe | sí | sí |
| Sin otros fallos graves de axe | no | sí |
| Objetivos táctiles de al menos 24 px | sí | sí |
| Objetivos táctiles de al menos 44 px | no | sí |
| Foco visible con teclado | sí | sí |
| Sin desborde horizontal a 320 px | sí | sí |
| Respeta movimiento reducido | sí | sí |
| Nombre y acción en la primera pantalla del móvil | sí | sí |
| Enlace de contacto válido | sí | sí |
| Anclas internas sin romper | sí | sí |
| Fuentes cargadas | sí | sí |
| Texto menor de 14 px no pasa del 10 por ciento | no | sí |
| Rendimiento móvil de 90 o más | no | sí |
| LCP de 2,5 s o menos | no | sí |
| CLS de 0,1 o menos | sí | sí |
| Peso de 1,5 MB o menos | sí | sí |
| Vista previa social (Open Graph) | no | sí |

Problemas de accesibilidad que detecta axe: antes heading-order[moderate]x1, html-has-lang[serious]x1, region[moderate]x3; después ninguno.

## Cobertura de pruebas

- Antes: una sola pantalla de móvil (390 px) y el desborde a 320 px.
- Después: 27 dispositivos emulados (de 280 a 3440 px de ancho, horizontales y plegables), texto al 200 por ciento, teclado, contraste medido sobre píxeles reales, movimiento reducido, pausa y 11 casos de horario con relojes simulados.

## Lo que no se puede comparar con números

- Si el diseño nuevo gusta más o convence más: solo lo dicen personas reales y, después, los datos del restaurante.
- Cuánto mejora el negocio: depende de la carta, el precio, la zona y la gestión del local, y no se promete ningún porcentaje.
- Safari y Firefox reales: se probó Chromium emulando los dispositivos.
