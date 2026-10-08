# Archivo de los cinco estudios de Eduardo

Aquí están guardados completos, y con su lectura, los cinco documentos que dieron origen al núcleo: alianzas con creadores, psicología, UX, conducta y motor gráfico. El núcleo ejecutable (`../reglas.json`) dice qué se hace; este archivo dice de dónde sale y deja a mano todo lo que los estudios contienen y las reglas no recogieron.

Es material de consulta interno. No se pega como texto en ningún prompt, no se entrega a clientes y ninguna de sus cifras se cita como promesa de resultados.

## Qué hay

| Ruta | Contenido |
|---|---|
| `SINTESIS.md` | Lectura cruzada: cómo encajan los cinco, qué dicen igual, discrepancias, cifras clave, huecos, candidatas a reglas y guía de qué leer según el encargo |
| `analisis/XX_*.md` | Una lectura por estudio: ficha, tesis, hallazgos numerados con su nivel de evidencia, especificaciones, reglas explícitas, límites, referencias e interpretación para Edumashow |
| `texto/XX_*.md` | Texto completo del PDF convertido a Markdown, con marcas de página, tablas y enlaces |
| `MAPA_REGLAS.md` | Qué estudio apoya cada una de las reglas unificadas (generado) |
| `archivo_fuente.py` | Genera `MAPA_REGLAS.md` y valida el archivo. Ejecutarlo tras cualquier cambio |

## Los cinco estudios

| Clave | Documento | Páginas | Corte |
|---|---|---|---|
| AL | Motor predictivo para propuestas y alianzas con creadores (estudio científico y especificación ampliada, versión 2) | 55 | 3 oct 2026 |
| PS | Psicología humana histórica y actual (síntesis crítica) | 9 | 26 sep 2026 |
| UX | Motor predictivo de UX para propuestas de colaboración (estudio de viabilidad y especificación) | 40 | 26 sep 2026 |
| CO | Ciencias del comportamiento y de la conducta | 11 | 28 sep 2026 |
| GR | Motor gráfico para propuestas comerciales (estudio y especificación, versión 1.0) | 33 | 3 oct 2026 |

Ninguno trata de webs de restaurante. Se escribieron para propuestas en PDF de un creador a marcas.

## Cómo se cita

- Página: AL p.14 es la página 14 de ese PDF según el número del pie. La portada es la p.1. En el texto completo, las marcas **[p.N]** señalan el comienzo de cada página.
- Hallazgo: H-XX-NN (por ejemplo H-UX-05) es un hallazgo numerado del análisis de ese estudio.
- Referencia del estudio: [S12] en AL; [1] a [48] en PS, CO, UX y GR, tal como las numera cada uno.
- Los ids AL-nn, PS-nn, UX-nn y CO-nn que aparecen en `../reglas.json` y en `../TRAZABILIDAD.md` vienen de una primera extracción que no se conservó y no coinciden con los H-XX-NN. Las páginas que acompañan a esos ids sí valen.

## Niveles de evidencia

Los mismos que usa `../reglas_fuente.py`, con una precisión para las fuentes que cita cada estudio:

- N: norma o requisito técnico (por ejemplo WCAG 2.2).
- M: medida hecha en este proyecto.
- E1: resultado primario o metaanálisis revisado por pares, citado con datos.
- E2: fuente citada pero sin revisión por pares o comprobada solo por su resumen (preprint, documentación o anuncio de un proveedor, ficha institucional).
- E3: criterio, propuesta o cálculo ilustrativo del autor del estudio.
- E4: afirmación sin respaldo.

Ninguna E1 de estos estudios es evidencia sobre webs de restaurante.

## Cómo se hizo

- Se leyeron los cinco PDF completos. Cada análisis lo escribió Edumashow a partir de esa lectura; los números se cotejaron contra el texto completo.
- El texto completo se extrajo del PDF por programa (posición de las palabras, tamaño de letra, tablas y enlaces) y se comprobó por conjunto de palabras contra el texto que extrae el propio PDF: no falta ninguna palabra salvo las cabeceras y pies repetidos de cada página.
- Los PDF originales no están en el repositorio. Para regenerar el texto hace falta volver a aportarlos.

## Reglas del archivo

- Comillas: nunca las angulares; todo el archivo usa comillas rectas (las del PDF se normalizan). `scripts/revisar_comillas.py` lo comprueba.
- Marca: el estudio de UX nombra al creador original de las propuestas. En el texto completo ese nombre se sustituye por [el creador] y en los análisis se escribe el creador. Nada del kit de propuestas anterior se copia al repositorio: los estudios citan documentos privados de ese kit que no se han visto.
- El archivo nombra herramientas y modelos de IA solo porque los estudios los citan como objeto de investigación (por ejemplo los experimentos de persuasión y de pronóstico con modelos de lenguaje). Nada de eso se copia a una web ni a un entregable: la regla G-MARCA sigue mandando sobre lo que se entrega.
- Los hallazgos que un estudio comprobó solo por resumen se marcan en el análisis. Los enlaces de las referencias se conservaron tal cual y no se han vuelto a verificar en línea.
- Las notas marcadas como fuera de los estudios (comunicación comercial no solicitada, uso del nombre y las fotos de un local, reseñas, RGPD y cookies, alérgenos) deben validarse con asesoría legal. Este proyecto no es asesoría legal.
