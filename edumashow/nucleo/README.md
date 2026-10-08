# Núcleo de conocimiento de Edumashow

Aquí vive el conocimiento único que sale de los cinco estudios de Eduardo (alianzas, psicología, UX, conducta y motor gráfico), más las normas técnicas (WCAG 2.2, Core Web Vitals) y las medidas hechas en este proyecto.

El conocimiento no se pega como texto en ningún prompt. Se ejecuta: cada regla tiene un tipo, una prioridad y una prueba en el Gate, así que no cuesta tokens por página.

## Lo que hay que saber de los estudios

- Ninguno trata de webs de restaurante. Se escribieron para propuestas en PDF de un creador a marcas. Las reglas web son traducciones, y los análisis lo marcan fila por fila.
- De 170 reglas extraídas de los cuatro estudios de conocimiento: el 16 por ciento se apoya en fuentes primarias o metaanálisis, el 64 por ciento son criterios del autor sin cita, y solo el 24 por ciento se puede comprobar del todo en un navegador.
- Los dos estudios predictivos son especificaciones sin datos ni pesos calibrados. Por eso el motor no pronostica ventas: mide cumplimiento de reglas y tareas probadas.
- En lo que coinciden los cuatro: datos reales con fuente, un siguiente paso claro, menos fricción, honestidad antes que persuasión, no prometer resultados y medir antes de creer.
- Lo que ningún estudio cubre y se cubre con normas y medidas propias: animación, velocidad de carga, móvil de gama media, carta, WhatsApp, apetito.

## Cómo se resuelven los choques

Las reglas se ordenan por prioridad (ver reglas.json). Gana siempre la de menor número:

0. Verdad, legalidad y ética
1. Accesibilidad y legibilidad
2. Tarea del visitante: un siguiente paso claro y poca fricción
3. Rendimiento en móvil lento
4. Identidad y estética del restaurante
5. Persuasión (solo como hipótesis a probar)
6. Variedad entre webs

Choques reales que se detectaron y cómo se resuelven:

- Variedad frente a adaptar solo por diferencias verificables: la variedad nace de los datos reales del restaurante (cocina, precios, ciudad, marca, fotos). Si dos restaurantes dan entradas casi iguales, las variantes se asignan al azar y se registra la semilla.
- Animación frente a velocidad: ningún estudio lo cubre. Manda el presupuesto medido (R-REN-01) y el movimiento es aditivo: la página es completa sin él.
- Medir frente a privacidad: conteo agregado sin identificadores, o consentimiento.
- La mejor interfaz del mundo: el estudio de UX lo llama no justificable. Lo que sí se mide es ser mejor que un comparador definido en tareas definidas.

## Archivos

- reglas_fuente.py: fuente única de las reglas. Ejecutarlo regenera reglas.json y lo valida (campos obligatorios, sin comillas angulares).
- reglas.json: el núcleo ejecutable que lee el Gate.

## Aviso legal

Las notas marcadas como fuera de los estudios (comunicación comercial no solicitada, uso del nombre y las fotos de un local, reseñas, RGPD y cookies, alérgenos) deben validarse con asesoría legal. Este proyecto no es asesoría legal.
