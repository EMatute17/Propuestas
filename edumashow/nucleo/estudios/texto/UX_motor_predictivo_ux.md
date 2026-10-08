> Texto completo del PDF aportado por Eduardo (Estudio_motor_predictivo_UX_propuestas_2026_1.pdf, 40 páginas), convertido a Markdown por Edumashow para consulta. Las marcas **[p.N]** indican el cambio de página (numeración del pie del PDF). Se quitan cabeceras y pies repetidos, las comillas se normalizan a rectas, las tablas pasan a Markdown y se conservan los enlaces del PDF. El nombre del creador original se sustituye por [el creador] por la regla de marca del proyecto; no cambia ningún dato.
> Archivo de consulta: el conocimiento ejecutable vive en reglas.json; este texto no se pega en prompts ni se entrega a clientes. Lectura analítica en ../analisis/.

**[p.1]**

# ESTUDIO DE VIABILIDAD Y ESPECIFICACIÓN • 26 SEPTIEMBRE 2026 — Un motor predictivo de UX para propuestas de colaboración

### Base científica, filtros de entrega y protocolo para demostrar mejoras

Preparado para Eduardo. Aplicación inicial: propuestas comerciales de [el creador] y su recorrido desde la recepción hasta la decisión y la ejecución de la colaboración.

| Lo que sí se puede construir | Lo que la evidencia no permite prometer |
|---|---|
| Un control obligatorio que impida liberar archivos cuando falten pruebas exigidas o fallen reglas verificables. | Conocer el 100% de la experiencia de todas las personas, detectar todos los errores posibles o garantizar cada aceptación. |
| Un sistema que compare diseños y estime resultados dentro de poblaciones y condiciones validadas. | Ser el mejor motor del mundo por su complejidad, número de variables, cantidad de agentes o una autoevaluación de 10/10. |
| Un proceso que aprenda de usuarios, resultados comerciales y errores documentados. | Que observar patrones pruebe causalidad o que millones de simulaciones equivalgan a millones de usuarios reales. |

**Conclusión principal.** Es viable desarrollar un motor avanzado y especializado. Su excelencia tendría que demostrarse con comparaciones independientes, datos relevantes y resultados fuera de la muestra. La garantía defendible es sobre un proceso y sus controles definidos, nunca sobre una experiencia humana absoluta.

**Estado del trabajo:** estudio y arquitectura propuestos. No se ha entrenado ni desplegado un motor, ejecutado un experimento con marcas, certificado el kit ni demostrado una mejora de conversión. Las cifras científicas se atribuyen a sus fuentes; los ejemplos propios se identifican como cálculos o escenarios.

Incluye: mapa de disciplinas, evidencia histórica y 2024-2026, catálogo de filtros, metadatos, modelos, potencia estadística, validación independiente y aplicación al Documento Maestro v4.3.

**[p.2]**

## GUÍA DE LECTURA — Dónde encontrar cada respuesta

El documento distingue **evidencia publicada**, **reglas propias del proyecto** y **diseño de ingeniería propuesto**. Una fuente sobre comportamiento humano orienta hipótesis; un filtro obligatorio necesita una prueba concreta; una afirmación de mejora exige resultados.

| Pregunta | Páginas |
|---|---|
| ¿Es posible lo que quieres y qué puede garantizarse? | 3-5 |
| ¿Quiénes aportan a la UX más allá del tridente? | 6-8 |
| ¿Qué dicen la historia y los estudios recientes? | 9-13 |
| ¿A quién estudiar y qué datos medir? | 14-18 |
| ¿Cómo funciona la arquitectura y cuáles son los filtros? | 19-24 |
| ¿Qué modelos, muestras y experimentos hacen falta? | 25-29 |
| ¿Cómo se incorpora al sistema [el creador]? | 30-34 |
| ¿Cuáles son las fuentes y qué se consultó? | 35-40 |

### Lectura rápida para tomar decisiones

Empieza por la viabilidad de la página 3, revisa los filtros de las páginas 20-22 y la integración con tu Documento Maestro en la página 30. La página 27 explica por qué pocas aceptaciones todavía no permiten afirmar precisión. La página 32 organiza la implementación.

### Lectura técnica para construirlo

Usa los campos de datos de la página 18, la arquitectura de la 19, el control de liberación de la 23 y las pruebas del verificador de la 24. Después define el resultado predictivo, el experimento y el criterio de promoción del modelo. Ninguna de estas páginas declara que el sistema ya esté programado.

Los 33 filtros son un catálogo inicial de familias de comprobación. Al implementarlo deben desglosarse y vincularse con **cada requisito aplicable** del Documento Maestro y del encargo; no sustituyen ni agotan sus reglas detalladas. Una regla sin implementación o evidencia permanece pendiente.

**[p.3]**

## 01 • DECISIÓN — Qué parte de tu objetivo es alcanzable

| Objetivo | Veredicto | Condición para sostenerlo |
|---|---|---|
| Bloquear propuestas que incumplen parámetros | Sí, dentro del sistema | Todos los caminos de entrega deben pasar por el verificador; ausencia de prueba equivale a bloqueo. |
| Detectar problemas de UX antes de enviar | Sí, parcialmente | Combinar controles automáticos, revisión experta y evidencia con personas representativas. |
| Elegir entre alternativas | Sí, condicionado | Definir para quién, qué tarea, qué objetivo y qué perjuicios no se aceptan. |
| Dar probabilidades fiables | Posible, por demostrar | Resultados etiquetados, validación externa, calibración, incertidumbre y vigilancia de cambios. |
| Optimizar todos los objetivos a la vez | No en general | Hay conflictos: novedad frente a familiaridad, detalle frente a esfuerzo, velocidad frente a deliberación. |
| Dominar UX al 100% / ganar siempre | No justificable | La experiencia depende de contexto, expectativas, capacidades, organización y tiempo. [1, 2, 4] |
| Ser el mejor en un dominio concreto | Meta evaluable | Superioridad replicada frente a competidores definidos, en tareas y poblaciones publicadas. |

### La formulación que sí conviene perseguir

Construir el sistema que reduzca los defectos evitables, facilite una decisión informada y produzca la mayor mejora comercial comprobable para tus propuestas, manteniendo límites mínimos de comprensión, accesibilidad y honestidad.

Un resultado "apto para entrega" debe significar que se cumplieron las reglas y revisiones aplicables de una versión concreta. Un resultado "preferido" debe indicar por qué ganó una alternativa. Una probabilidad de aceptación requiere otra evidencia distinta. Ninguna de estas tres salidas debe sustituir a las otras.

Una empresa puede entender perfectamente una propuesta y rechazarla por presupuesto. También puede aceptar una propuesta confusa porque ya conoce al creador. Por eso aceptación y UX se relacionan, pero no son la misma variable.

**[p.4]**

## 02 • MÉTODO DE INVESTIGACIÓN — Cómo se construyó este estudio

Se realizó una revisión integrativa dirigida, con búsqueda web y contraste en artículos científicos, repositorios de autores y universidades, documentación de organismos de normalización y publicaciones de sus creadores. El corte de consulta es el **26 de septiembre de 2026**. No es una revisión sistemática exhaustiva ni un metaanálisis nuevo.

| Tipo de evidencia | Uso correcto en este estudio |
|---|---|
| Metaanálisis y revisiones | Identificar resultados agregados, heterogeneidad, problemas de medición y límites de transferencia. |
| Experimentos y estudios originales | Examinar cómo se midió el efecto, quién participó y en qué tarea se observó. |
| Estándares y guías oficiales | Definir requisitos o métodos de evaluación; no atribuirles efectos causales sobre ventas. |
| Fuentes profesionales de sus autores | Obtener heurísticas y métodos prácticos. Su prestigio no reemplaza una prueba empírica. |
| Documento Maestro v4.3 | Identificar requisitos propios. Es una especificación del proyecto, no evidencia externa de eficacia. |
| Diseño y cálculos de este informe | Propuestas de ingeniería y ejemplos explícitos; no resultados observados de [el creador]. |

### Criterios de selección y verificación

Se priorizaron fuentes con autor, fecha, método y vínculo verificable; estudios que distinguen percepción y desempeño; resultados recientes pertinentes; y trabajos históricos que todavía orientan hipótesis medibles. Se descartó usar como prueba una lista comercial de "leyes UX", una promesa de neuromarketing o cifras sin trazabilidad.

Cuando el editor bloqueó el texto completo, se contrastó el resumen en el repositorio institucional o de los autores. El nivel de acceso está indicado en las referencias. No se declara haber reanalizado los datos crudos, leído capítulos íntegros restringidos ni auditado la integridad de cada experimento original.

Los tamaños muestrales de distintos metaanálisis no se suman: pueden compartir estudios y participantes. Un artículo publicado o revisado por pares tampoco se convierte en una verdad universal. La calidad depende del diseño, sesgos, replicación y pertinencia al caso.

**[p.5]**

## 03 • TU PLANTEAMIENTO — El tridente es útil, pero no contiene toda la UX

UX Researcher, UX/UI Designer y Product Analyst son tres funciones importantes. No existe un "dueño de la verdad" que domine la mente o la matemática al 100%. La división tampoco es una ley científica: una persona puede combinar competencias y un equipo grande puede equivocarse de forma coordinada.

| Función | Qué aporta | Qué no puede demostrar por sí sola |
|---|---|---|
| Investigación de usuarios | Necesidades, tareas, contexto, barreras y causas plausibles mediante observación y estudios. | Que las entrevistas representen al mercado completo o que lo declarado prediga la compra. |
| Diseño de interacción y visual | Alternativas, jerarquía, navegación, legibilidad, respuesta del sistema y composición. | Que una apariencia premium produzca comprensión o mejores resultados en todas las personas. |
| Analítica y experimentación | Medición del comportamiento, incertidumbre, experimentos y resultados comparables. | Que una correlación explique por qué ocurre un problema o que una métrica agote la experiencia. |

### Quién decide qué es mejor

Los usuarios aportan experiencia real; el negocio define objetivos y restricciones; investigadores y especialistas interpretan evidencia; ingeniería garantiza ejecución; y una persona responsable asume la decisión de liberar. El conocimiento debe circular entre estas funciones desde el descubrimiento hasta el seguimiento.

NN/g es una referencia profesional reconocida, pero no una "biblia" capaz de certificar toda la UX. Sus propias guías explican que una evaluación heurística no reemplaza las pruebas con usuarios. Material Design es un sistema de diseño de su creador, no una prueba de que cualquier propuesta construida con sus patrones vaya a ser superior. [4]

El mapa de las tres páginas siguientes reúne 30 funciones relevantes. Es una taxonomía práctica propuesta, no un censo de todos los profesionales del mundo ni una afirmación de que debas contratar 30 personas. Algunas funciones pueden combinarse; la independencia de la verificación sí debe preservarse.

**[p.6]**

## 04 • MAPA DE ESPECIALISTAS A — Ciencias humanas e investigación

| Función o disciplina | Contribución y método | Aplicación al motor |
|---|---|---|
| 1. UXR cualitativo | Entrevistas, observación contextual, sesiones de usabilidad y síntesis de incidentes. | Detectar vocabulario confuso y condiciones que el destinatario no entiende. |
| 2. UXR cuantitativo | Encuestas, muestreo, comparación de tareas y análisis de incertidumbre. | Estimar comprensión y esfuerzo por población y dispositivo. |
| 3. Psicología cognitiva | Atención, memoria, búsqueda, carga mental, aprendizaje y decisión. | Hipótesis de jerarquía y agrupación; medición por tarea. [5-8] |
| 4. Ciencia de la percepción | Contraste, agrupación, figura-fondo, tipografía y visión. | Detectar interferencias y probar dónde se encuentra la información. [9] |
| 5. Ergonomía / factores humanos | Capacidades físicas, cognitivas y organizativas del sistema. | Revisar lectura, manipulación, fatiga y restricciones de trabajo. [2] |
| 6. Antropología / etnografía | Prácticas reales, cultura de trabajo, improvisación y contexto social. | Entender cómo un dueño comparte la propuesta con su socio. [11] |
| 7. Sociología / investigación cultural | Normas, roles, poder de decisión y diferencias entre grupos. | Evitar usar país como sustituto de preferencias individuales. [20] |
| 8. Economía conductual / decisión | Elección, incertidumbre, comparación, preferencias y valor percibido. | Probar cantidad y presentación de opciones; no asumir un número mágico. [18, 19] |
| 9. Psicometría | Validez, fiabilidad y comparabilidad de instrumentos. | Impedir que preguntas inventadas se vendan como escalas validadas. [16] |
| 10. ResearchOps / ciencia de encuestas | Reclutamiento, consentimiento, incentivos, calidad y archivo de evidencias. | Mantener un panel pertinente y un registro reutilizable de hallazgos. |

Estas funciones explican por qué alguien tuvo una experiencia, a quién se puede generalizar y qué queda sin observar. Un panel compuesto solo por amigos, diseñadores o seguidores del creador no representa automáticamente a quienes aprueban presupuestos.

**[p.7]**

## 05 • MAPA DE ESPECIALISTAS B — Diseño, contenido y experiencia completa

| Función o disciplina | Contribución y método | Aplicación al motor |
|---|---|---|
| 11. Arquitectura de información | Organización, etiquetas, búsqueda y estructura del contenido. | Que se encuentren inversión, entregables, pruebas y siguiente paso. |
| 12. Diseño de interacción | Recorridos, acciones, estados, recuperación y navegación. | Comprobar apertura de enlaces, regreso al documento y respuesta al CTA. |
| 13. Diseño visual / editorial | Jerarquía, ritmo, retícula, espacios y consistencia de composición. | Revisión del PDF renderizado, no solo de su texto o coordenadas. |
| 14. UX writing / lingüística | Claridad, vocabulario, significado, microtexto y pragmática. | Evitar ambigüedad entre precio, consumo, producción y plataformas. |
| 15. Estrategia de contenido | Propósito, evidencia, orden de argumentos y mantenimiento. | Vincular cada afirmación con una fuente y una necesidad de decisión. |
| 16. Accesibilidad / diseño inclusivo | Tecnologías de apoyo, visión, movilidad, cognición y barreras. | Orden de lectura, alternativas textuales y tareas con usuarios diversos. [22-25] |
| 17. Diseño de servicios / CX | Experiencia anterior y posterior al contacto y coordinación interna. | Evaluar correo, propuesta, negociación, producción y renovación. |
| 18. Localización / comunicación intercultural | Idioma, usos locales, monedas, formatos y expectativas. | Adaptar expresiones y condiciones según información confirmada. |
| 19. Marca / dirección de arte | Identidad, tono, pertinencia y calidad percibida. | Usar referencias aprobadas como nivel, con una idea propia y coherente. |
| 20. Diseño afectivo / experiencia de producto | Sensación, significado y emoción en relación con un producto. | Examinar atractivo y confianza sin confundirlos con éxito de tarea. [13] |

La propuesta es una experiencia documental, comercial y de servicio. Los gestos o menús importan cuando existen, pero copiar una lista de parámetros de una aplicación interactiva puede introducir filtros irrelevantes.

**[p.8]**

## 06 • MAPA DE ESPECIALISTAS C — Datos, ingeniería y responsabilidad

| Función o disciplina | Contribución y método | Aplicación al motor |
|---|---|---|
| 21. Product Analyst / CRO | Embudo, cohortes, diagnóstico y conversión. | Distinguir entrega, respuesta, negociación, aceptación y renovación. |
| 22. Estadística / ciencia experimental | Potencia, estimación, aleatorización, dependencia y multiplicidad. | Separar señales reales de ruido y resultados exploratorios de confirmatorios. |
| 23. Ciencia causal / econometría | Efectos de intervenciones y sesgos de selección. | Estudiar si cambiar diseño mejora resultados manteniendo una comparación válida. |
| 24. ML / modelado predictivo | Aprendizaje supervisado, regularización, calibración e incertidumbre. | Predicciones con límites por país, marca, tipo de oferta y periodo. |
| 25. Visión artificial / document AI | Extracción de estructura, geometría, imágenes y representación visual. | Identificar posibles defectos y asistir la revisión; no leer emociones como hechos. |
| 26. Ingeniería de datos | Identidad, esquemas, validación, versiones y trazabilidad. | Conectar un resultado con el archivo exacto y evitar duplicados o fuga de datos. |
| 27. Software / QA / accesibilidad técnica | Renderizado, comprobaciones, integración y pruebas de fallos. | Crear una vía de entrega que realmente falle de forma cerrada. |
| 28. MLOps / fiabilidad | Versiones de modelos, monitorización, alertas y reversión. | Impedir que un cambio de modelo invalide silenciosamente la evaluación anterior. |
| 29. Privacidad, seguridad y ética | Minimización de datos, permisos, retención y usos aceptables. | Proteger evidencias y evitar rastreo oculto o afirmaciones engañosas. [33] |
| 30. Producto, ventas y especialistas del negocio | Viabilidad, objetivos, negociación, operación y costes. | Definir qué mejora importa y comprobar que la colaboración puede ejecutarse. |

Los destinatarios reales, personas con discapacidad, equipos de marketing, socios y responsables de operación son colaboradores esenciales aunque no tengan un cargo "UX". La responsabilidad última de liberar una propuesta no se debe diluir en una votación entre modelos.

**[p.9]**

## 07 • FUNDAMENTOS HISTÓRICOS — Qué sigue siendo útil y qué debe contextualizarse

| Origen | Aporte | Traducción correcta a tus propuestas |
|---|---|---|
| Gestalt, siglo XX; revisión 2012 [9] | Agrupación y organización figura-fondo. | Usar proximidad y alineación para relacionar elementos; no deducir conversión de una retícula. |
| Hick, 1952 [5] | Relación entre información y tiempo de elección en tareas experimentales. | Probar complejidad de decisiones; no concluir que toda propuesta debe tener exactamente tres opciones. |
| Fitts, 1954 [6] | Relación entre movimiento, distancia y tamaño del objetivo. | Hacer enlaces utilizables; no convertir su ley en una ecuación de aceptación comercial. |
| Miller, 1956; Cowan, 2001 [7, 8] | Capacidad y agrupación de información bajo condiciones definidas. | Reducir necesidad de recordar; "7±2" o "4" no son límites universales de páginas o bullets. |
| Card, Moran y Newell, 1983 [10] | Modelos de tareas y desempeño humano-computadora. | Descomponer acciones observables; un flujo de lectura persuasiva requiere validación adicional. |
| Suchman, 1987 [11] | Acción situada y límites de los planes como explicación total. | Observar entorno y relaciones: la lectura real puede interrumpirse o delegarse. |
| Norman, 1988 [12] | Comprensibilidad del diseño y relación entre intención, acción y respuesta. | Que el siguiente paso y sus consecuencias sean claros. |
| Sweller, 1988 [41] | Carga cognitiva en aprendizaje y resolución de problemas. | Hipótesis de reducción de esfuerzo; transferencia a venta B2B por probar. |
| Nielsen/Molich, 1990; Brooke, 1996 [4, 26] | Inspección heurística y medición de usabilidad percibida. | Métodos complementarios; ninguno certifica perfección. |
| Desmet/Hekkert, 2007; HEART, 2010 [13, 27] | Experiencia afectiva y métricas centradas en objetivos de usuario. | Separar sensación, significado, tareas y resultados en un conjunto de medidas. |

La antigüedad no invalida un hallazgo y la novedad no lo hace superior. Los principios deben conservar su ámbito de aplicación y revisarse frente a tareas, dispositivos y expectativas actuales.

**[p.10]**

## 08 • EVIDENCIA RECIENTE — Estética, esfuerzo y desempeño son dimensiones distintas

**Estética y desempeño: Schlamann, Nestler y Thielsch, 2026.** Metaanálisis preregistrado: 31 estudios, 234 tamaños de efecto y 18.794 participantes; efecto positivo agregado g = 0,29, con heterogeneidad alta no explicada. La selección exigía una manipulación estética detectada en las valoraciones. El resultado respalda estudiar la estética junto con desempeño; g no equivale a 29% más ventas. No ofrece una probabilidad de aceptación para un PDF. [14]

**Preferencia y carga mental: Hertzum, 2025.** Metaanálisis de 144 estudios: la preferencia se relacionó más fuertemente con menor carga percibida que con tiempo o errores. Solo en 2% de los estudios un sistema preferido imponía una carga significativamente mayor. Predominan tareas utilitarias; el hallazgo no identifica un diseño ganador para tus marcas. [15]

**Usabilidad percibida frente a ejecución: Hertzum, 2026.** Metaanálisis de 105 estudios. El sistema con mayor SUS tenía peor desempeño temporal en 24% y peor desempeño en errores en 23% de los estudios; en 10% imponía mayor carga. Una valoración de facilidad puede mejorar sin que todas las medidas objetivas mejoren. Estos porcentajes son de estudios, no de destinatarios comerciales. [17]

**Calidad de la medición: Perrig y colaboradores, 2024.** Revisión de CHI 2019-2022: 153 artículos examinados, 60 elegibles, 85 escalas y 172 constructos. Solo 20% de los artículos justificó completamente la selección de escalas y 36,67% informó alguna evaluación de su calidad. La popularidad de una escala no corrige un uso inadecuado. [16]

**Implicación de diseño propuesta:** el motor debe mantener un perfil de medidas separado. Un diseño atractivo no compensa un precio incomprensible; una lectura rápida no compensa condiciones mal entendidas; una puntuación de facilidad no prueba eficacia comercial.

Acceso: resúmenes y metadatos institucionales para [15, 17], artículo abierto para [16], resumen editorial y repositorio de datos/código de autores para [14]. No se reestimaron los efectos.

**[p.11]**

## 09 • EVIDENCIA COMPLEMENTARIA — Por qué las reglas universales fallan

**Cantidad de opciones.** Scheibehenne, Greifeneder y Todd (2010) sintetizaron 63 condiciones de 50 experimentos, N = 5.036. El efecto medio de sobrecarga fue prácticamente nulo: D = 0,02; IC 95% de -0,09 a 0,12, con variación entre estudios. Chernev, Böckenholt y Goodman (2015), en 99 observaciones y N = 7.202, identificaron moderadores como complejidad, dificultad, incertidumbre de preferencias y objetivo. No hay una cantidad universalmente óptima de planes. [18, 19]

**Preferencia visual y diversidad.** Reinecke y Gajos (2014) reunieron 2,4 millones de valoraciones de atractivo de sitios, de casi 40.000 participantes. Encontraron diferencias ligadas a antecedentes de los participantes. Esto justifica estudiar heterogeneidad; no permite deducir el gusto de una persona por su nacionalidad. [20]

**Primera impresión.** Los experimentos de Lindgaard y colaboradores (2006) estudiaron juicios de atractivo de páginas web con exposiciones de 50 milisegundos. Detectar una impresión rápida no demuestra comprensión del precio, memoria posterior ni intención de contratar. Una portada debe atraer y dar paso a una tarea que se pueda completar. [21]

**Replicación.** Camerer y colaboradores (2018) replicaron 21 experimentos de ciencias sociales de Nature y Science: 13 mostraron un efecto significativo en la dirección original; el efecto de réplica fue, en promedio, aproximadamente la mitad del original. Este conjunto no representa toda la psicología, pero obliga a tratar con cuidado las promesas basadas en un estudio famoso. [34]

### Cómo debe usar el motor un hallazgo

Registrar qué se manipuló, qué se midió, en qué población, el tamaño del efecto y la incertidumbre; formular una hipótesis local; diseñar una prueba; y actualizar la decisión con su resultado. Una evidencia sobre supermercados, pacientes o sitios web puede orientar una hipótesis sobre propuestas B2B, pero no proporciona por sí sola su efecto.

**[p.12]**

## 10 • IA Y FRONTERA ACTUAL — Lo nuevo acelera la evaluación; no elimina al usuario

**Usuarios sintéticos.** Seshadri y colaboradores (2026) compararon simulación con participantes de Estados Unidos, India, Kenia y Nigeria en tareas de agentes de atención comercial. Cambiar el modelo simulador alteró el éxito hasta 9 puntos porcentuales; aparecieron diferencias de calibración y de patrones de error respecto a humanos. Es evidencia de un entorno de agentes, no de propuestas, y justifica limitar la transferencia. Se consultó el manuscrito v2; también se verificó su registro en ACL 2026. [35]

**Jueces basados en LLM.** La investigación de Zheng y colaboradores estudia fortalezas y sesgos al usar modelos como evaluadores. La aplicación propuesta aquí es revisar afirmaciones o localizar posibles problemas, con una rúbrica y ejemplos de referencia. No se debe convertir el acuerdo entre modelos en validación humana independiente. [36]

**Predicción de mirada.** DeepGaze IIE es un ejemplo científico de modelado de saliencia y calibración dentro y fuera del dominio. Una predicción de fijaciones no mide comprensión, deseo, confianza, emoción o compra. Usarla sobre un PDF comercial exige validar ese dominio y esa tarea. Los mapas de calor del cursor tampoco son equivalentes a eye tracking. [37]

| Actualización verificada | Consecuencia |
|---|---|
| ISO 9241-210:2019, confirmada en 2025 [1] | Mantener diseño centrado en personas como marco del proceso. |
| WCAG 2.2: recomendación consultada de diciembre de 2024 [22] | Usar criterios aplicables y pruebas humanas; no declarar que un escáner verifica todo. |
| WCAG 3.0: Working Draft de 10 septiembre 2026 [40] | Seguir su evolución; no tratar el borrador como estándar de conformidad terminado. |
| PDF/UA-2, ISO 14289-2:2024 [25] | La accesibilidad del PDF requiere estructura semántica; aspecto visual correcto no basta. |

No se encontraron fundamentos para prometer un simulador que conozca todas las respuestas humanas o un evaluador universal de UX. Esta revisión tampoco acredita acceso a modelos privados, "secretos" empresariales o datos propietarios no publicados.

**[p.13]**

## 11 • HALLAZGOS MENOS OBVIOS — Qué conviene entender antes de programar

| Idea tentadora | Criterio defendible para el motor |
|---|---|
| Más tiempo de lectura siempre es mejor | Puede significar interés o confusión. Interpretarlo junto con comprensión y tarea completada. |
| La propuesta con más clics tiene mejor UX | Los clics pueden surgir por curiosidad, errores o búsqueda fallida. Medir si acercan a una decisión informada. |
| Un score de 95 implica 95% de éxito | Una rúbrica y una probabilidad son objetos distintos. Prohibir esa conversión sin modelo validado. |
| Cinco usuarios garantizan encontrar casi todo | Las rondas pequeñas son útiles para descubrimiento; no certifican ausencia de fallos ni precisión poblacional. [3] |
| La ciencia dice cuál color vende más | El color opera en un contexto de marca, contraste y población. Las tendencias no son ensayos de conversión. [20] |
| Si la IA imita a un dueño, ya fue probado | La simulación es una fuente de hipótesis y pruebas de software, no una muestra humana. [35] |
| Unanimidad de expertos elimina incertidumbre | Pueden compartir sesgos. Registrar discrepancias y contrastar con tareas reales. [4] |
| Cuantos más filtros, mejor | Un filtro inválido puede bloquear buenos diseños. Medir falsos bloqueos y defectos que escapan. |
| Pasó QA; no tiene errores | Pasó lo que QA pudo comprobar en esas condiciones. Debe constar cobertura, versión y límites. [24] |
| Millones de variables revelan todos los patrones | Sin resultados pertinentes, aumentan posibilidades de sobreajuste. La validación decide qué complejidad aporta. [29] |

Estos son límites metodológicos y oportunidades de mejora, no secretos ocultos. El avance competitivo más defendible es reunir mejores evidencias propias y ejecutar decisiones trazables, incluso cuando la conclusión sea "todavía no sabemos".

**[p.14]**

## 12 • DEFINIR LA EXPERIENCIA — La unidad de análisis es una persona haciendo una tarea

Para el caso inicial, el usuario primario es quien evalúa o aprueba una colaboración. Puede ser dueño, gerente, responsable de marketing, agencia o socio. Los espectadores del contenido son otra población. Los datos de retención de un Reel no miden directamente la facilidad con que una marca entiende la propuesta.

| Momento del recorrido | Tarea observable | Fallo relevante |
|---|---|---|
| Recepción | Reconocer quién escribe y decidir abrir. | Remitente o asunto confuso; archivo que no se puede abrir. |
| Orientación | Entender qué idea se propone y para qué marca. | Promesa genérica o producto equivocado. |
| Evaluación | Encontrar entregables y comprobar evidencias. | Contenido ambiguo o enlaces que llevan a otra pieza. |
| Decisión | Identificar inversión, responsabilidades y siguiente paso. | Confundir tarifa con consumo o no saber cómo responder. |
| Consulta interna | Compartir y explicar el acuerdo a otra persona. | Condiciones dispersas o dependencia del autor para entenderlo. |
| Ejecución y continuidad | Cumplir lo acordado y evaluar renovación. | Aceptación inicial que termina en cambios, decepción o conflicto. |

### Objetivos propuestos, en orden

**1. Requisitos mínimos:** veracidad, coherencia comercial, acceso al contenido y ausencia de defectos bloqueantes. **2. Resultado UX:** decisión informada con esfuerzo razonable y comprensión correcta. **3. Resultado comercial:** colaboración viable, margen y continuidad. Los pesos de preferencia entre objetivos deben ser explícitos y revisables.

Se propone registrar ventanas de 14, 30 y 90 días para respuesta, contratación y ejecución o renovación, respectivamente. Son decisiones iniciales de diseño del registro, no plazos científicamente universales; deben ajustarse al ciclo comercial real antes de comparar resultados.

**[p.15]**

## 13 • MÉTRICAS — Qué observar y qué no inferir automáticamente

| Dimensión | Medida propuesta | Interpretación y límite |
|---|---|---|
| Comprensión | Respuestas correctas sobre entregables, importe, moneda, consumo y siguiente paso. | Criterio primario de tarea. Definir la respuesta correcta antes del estudio. |
| Encontrabilidad | Tiempo hasta localizar precio, evidencia o contacto; éxito con o sin ayuda. | Comparar tareas equivalentes. No penalizar deliberación razonada. |
| Esfuerzo | Valoración posterior a tarea y, si procede, NASA-TLX. | Autoinforme; no es una lectura objetiva de la mente. [28] |
| Atractivo | Preferencia entre variantes y valoración visual separada. | Contrabalancear orden y ocultar autoría cuando sea viable. |
| Confianza informada | Qué evidencia considera creíble y qué dudas quedan. | Una puntuación sola no sustituye explicación ni comprobación de hechos. |
| Accesibilidad | Tareas con lector de pantalla, zoom y acceso a enlaces. | Complementar inspección semántica y revisión manual. [23-25] |
| Conversión | Aceptaciones definidas / oportunidades asignadas elegibles. | No confundir con apertura, respuesta o aceptación del diseño por Eduardo. |
| Calidad posterior | Cambios de condiciones, cancelaciones, entrega, renovación y margen. | Una conversión temprana puede ocultar una experiencia posterior negativa. |
| Calidad del filtro | Defectos omitidos, falsos bloqueos, cobertura y tiempo de revisión. | El verificador debe ser evaluado como un producto propio. |

En un PDF enviado por correo o mensajería normalmente no se observa de forma fiable cuánto se leyó ni el recorrido entre páginas. No inventar telemetría. Si se usa un visor instrumentado, validar eventos, permisos y limitaciones; los accesos de bots o previsualizadores no prueban lectura humana.

Con HEART se parte de objetivos, luego señales y métricas. En una propuesta de contacto único no tiene sentido forzar métricas de adopción o retención diaria propias de aplicaciones. La adaptación del marco debe conservar la tarea real. [27]

**[p.16]**

## 14 • PRUEBAS CON PERSONAS — Protocolo inicial para tus propuestas

**Reclutamiento.** Incluir perfiles que realmente revisen presupuestos de colaboración. Cubrir los contextos iniciales de España y Venezuela, familiaridad con creadores, diferentes tamaños de negocio y las condiciones de lectura prioritarias. No utilizar país o edad para asignar preferencias sin observarlas.

**Descubrimiento.** Como punto de partida operativo, realizar rondas de 5 a 8 personas por contexto prioritario, corregir y volver a probar. Este número es una decisión de trabajo para encontrar problemas, no una garantía de cobertura ni un tamaño suficiente para un A/B comercial. [3]

**Tareas sin inducir respuesta.** "Explícame qué se está proponiendo"; "¿qué recibiría tu negocio?"; "¿cuánto pagaría y qué más aportaría?"; "comprueba un ejemplo"; "si quisieras avanzar, ¿qué harías?". Evitar preguntas como "¿ves qué clara y premium está?"

**Observación.** Registrar éxito, errores, petición de ayuda, dudas, tiempo, lectura del precio y navegación. Si se necesita medir tiempo natural, separar esa medición del pensamiento en voz alta, que puede modificar la ejecución.

**Comparación.** Usar dos variantes con contenido comercial equivalente. Contrabalancear el orden, controlar aprendizaje y mantener el mismo dispositivo o asignarlo por diseño. Preguntar preferencia después de realizar las tareas.

**Salida de cada ronda.** Incidentes con ubicación, evidencia, gravedad, población afectada, hipótesis de causa, corrección propuesta y comprobación posterior. Un resumen como "gustó mucho" no es una evidencia suficiente.

### Objetivos iniciales que deben validarse

Para el piloto se propone exigir cero errores críticos observados de precio, moneda o entregables, comprensión correcta de las cinco condiciones centrales y capacidad de completar el siguiente paso sin ayuda. Estos son criterios de aceptación propuestos; los tamaños de muestra e intervalos determinan cuánto puede generalizarse su cumplimiento.

No se necesita un panel nuevo para cada cambio de un nombre o una foto. Las pruebas pueden cubrir familias de diseños y contextos, con vigencia y alcance declarados. Cambios sustanciales de estructura, oferta, idioma o audiencia activan una nueva evaluación.

**[p.17]**

## 15 • ESCALAS Y VALIDEZ — Medir bien importa más que añadir cuestionarios

**SUS.** Instrumento de 10 ítems para usabilidad percibida, con puntuación de 0 a 100; no es un porcentaje de éxito. Se administra después de interactuar con el sistema. No basta con cambiar palabras para declarar que conserva validez sobre una propuesta comercial. Un umbral como 80 sería una meta interna, no una garantía científica. [26]

**UEQ.** Distingue atractivo y dimensiones pragmáticas y hedónicas. Utilizar una versión lingüística documentada y el procedimiento de sus autores. Si ciertos ítems no encajan con un documento estático, justificar la elección de otro instrumento o validar la adaptación; no rellenar respuestas como si el modelo fuera un humano. [42]

**NASA-TLX.** Evalúa carga subjetiva en seis dimensiones. Registrar si se usa el procedimiento ponderado o una variante sin ponderar y mantenerlo consistente. Para una tarea breve puede ser excesivo: conviene escoger la medida según la pregunta de investigación. [28]

### Controles psicométricos del motor propuesto

| Control | Qué debe quedar documentado |
|---|---|
| Constructo | Qué significa comprensión, confianza o atractivo y qué queda fuera. |
| Instrumento | Origen, idioma, versión, ítems, escala y regla de puntuación. |
| Adaptación | Cambios frente a la versión original y evidencia de que siguen midiendo lo previsto. |
| Fiabilidad | Consistencia pertinente a la medida; un alfa alto por sí solo no demuestra validez. |
| Validez | Relación con tareas y criterios externos, estructura y posible sesgo de respuesta. |
| Comparación entre grupos | Examinar comparabilidad antes de atribuir diferencias a país o público. |
| Carga de investigación | Elegir pocas medidas relevantes para no deteriorar la propia experiencia del estudio. |

Las preguntas propias sobre precio y entregables son pruebas de comprensión de contenido específico. Deben llamarse así. No necesitan presentarse como una escala psicológica universal para ser útiles. [16]

**[p.18]**

## 16 • DATOS Y METADATOS — La base mínima que permite aprender de verdad

| Entidad | Campos esenciales propuestos |
|---|---|
| Propuesta | proposal_id, versión, fecha, marca, país, ciudad, idioma, objetivo, precio, moneda, responsabilidades y oferta confirmada. |
| Archivo y diseño | Hash del PDF final, plantilla/familia, estructura, fuentes, imágenes y origen, enlaces, tamaño, renderer y versión del generador. |
| Afirmaciones | Texto o identificador, fuente, fecha consultada, ubicación, permiso de uso si procede, tipo: dato/inferencia/supuesto. |
| Estudio UX | study_id, protocolo, tareas, reclutamiento, dispositivo, contexto, consentimiento, criterios, desviaciones y evidencia anonimizada. |
| Observación | Participante seudónimo, variante asignada, orden, respuestas, errores, tiempos, medidas y datos ausentes. |
| Oportunidad comercial | Empresa/grupo decisor, relación previa, canal, fechas, asignación, cambios de oferta y seguimiento. |
| Resultado | Respuesta, aceptación al precio original, negociación, rechazo, pendiente, fecha y motivo conocido; resultado de ejecución. |
| Evaluación | rule_id, versión, estado, evidencia, gravedad, evaluador, fecha, hash inspeccionado y motivo de no aplicabilidad. |
| Modelo | Versión de datos, variables disponibles al decidir, particiones, algoritmo, calibración, métricas y ámbito de validez. |

### Reglas de calidad del dato

Una fila de resultado representa una oportunidad definida, no cada página, cada lectura o cada mensaje de seguimiento. Varias personas de la misma empresa requieren agrupar la dependencia. Un "aprobado" de Eduardo valida su preferencia interna, no la contratación de la marca.

Distinguir "sin respuesta a 30 días" de rechazo explícito y de expediente pendiente con solo tres días de observación. Los resultados tardíos exigen actualizar el estado o utilizar análisis de tiempo hasta evento. Nunca completar razones desconocidas con intuiciones del modelo.

"Metadatos" son datos sobre el origen, contexto y procesamiento; "metaanálisis" es síntesis estadística de estudios. Ninguno crea por sí mismo observaciones de tus destinatarios. No se ha incorporado aquí una base verificada de 742.137 propuestas ni de millones de marcas.

**[p.19]**

## 17 • ARQUITECTURA — Un sistema híbrido con salidas separadas

| Capa | Función y salida |
|---|---|
| 1. Especificación versionada | Reglas del usuario, requisitos del caso, ámbito y catálogo de comprobaciones aplicables. |
| 2. Registro de evidencia | Fuentes, activos, resultados, participantes, permisos y enlaces entre versiones. |
| 3. Generación de alternativas | Conceptos y diseños candidatos; no puede modificar la política que lo evaluará. |
| 4. Verificación determinista | Comparación de campos y reglas exactas, integridad de archivo, enlaces y geometría. |
| 5. Inspección multimodal | Revisión de páginas renderizadas, OCR y posibles contradicciones de texto e imagen. |
| 6. Evaluación experta y humana | Evidencia de comprensión, accesibilidad, pertinencia y desempeño en contexto. |
| 7. Predicción calibrada | Estimaciones de resultados y sus límites cuando los datos permiten validarlas. |
| 8. Selección de alternativa | Comparación de objetivos y sensibilidad solo entre candidatos admisibles. |
| 9. Control de liberación | Emite permiso ligado al archivo exacto si las pruebas exigidas son satisfactorias. |
| 10. Seguimiento y aprendizaje | Resultados, incidentes, cambios del contexto, nueva validación y reversión cuando corresponda. |

Las tres salidas centrales son: **estado de conformidad**, **perfil UX** y **estimación comercial**. Si falta evidencia predictiva, la tercera debe decir "no estimable de forma validada". Las dos primeras siguen siendo útiles sin fabricar probabilidades.

La recuperación de evidencia mediante búsquedas o embeddings ayuda a encontrar antecedentes parecidos. No convierte similitud en causalidad ni reemplaza un modelo entrenado sobre resultados. Las evaluaciones generadas por IA se guardan como juicios asistidos, separadas de observaciones humanas.

Diseño de ingeniería propuesto. NIST aporta una estructura de gobierno y medición de riesgos [33]; no certifica que esta arquitectura concreta sea la más avanzada o que ya esté implementada.

**[p.20]**

## 18 • FILTROS A — Contenido, hechos y condiciones comerciales

Catálogo inicial propuesto. **B**: bloquea ante incumplimiento o falta de prueba crítica. **R**: exige revisión documentada. Toda regla debe tener responsable y una forma de comprobarse. Las reglas particulares se basan en el Documento Maestro v4.3. [44]

| ID / tipo | Criterio | Prueba exigida |
|---|---|---|
| C01 · B | Marca, país, precio y moneda confirmados. | Comparar solicitud autoritativa con datos y PDF final; cero valores heredados sin confirmación. |
| C02 · B | Responsabilidades y entregables coherentes. | Reel, colaboración, cuenta de TikTok, historias y consumo según encargo y reglas vigentes. |
| C03 · B | Inversión localizada correctamente. | Tarifa solo en módulo de inversión; distinguir precios de carta y cifras de evidencia. |
| C04 · B | Afirmaciones y cifras trazables. | Fuente y fecha para visualizaciones, premios, sede, producto o cualquier afirmación factual. |
| C05 · B | Tres evidencias del grupo correcto. | Identidad de cada vídeo, imagen y cifra; enlace correspondiente y set autorizado. |
| C06 · B | No atribuir a la marca un producto ajeno. | Procedencia de imagen y relación con el texto; no presentar una referencia como plato exacto. |
| C07 · B | Condiciones económicas sin contradicción. | Importe, divisa, netos o BCV según caso; no inferir obligaciones nuevas. |
| C08 · B | CTA realizable y claro. | Canal real, acción identificable y ausencia de enlaces ficticios. |
| C09 · B | Ausencia de contenido prohibido por encargo. | Sin QR ni fotos generadas o de Instagram para producto; excepciones expresas como logo. |
| C10 · R | Idea y argumento comercial pertinentes. | Activo real de la marca, beneficio concreto y relación con ejecución propuesta. |

La puntuación comercial nunca compensa C01-C09. Si el CTA lleva a un recurso que requiere iniciar sesión o que no se puede comprobar, queda como revisión pendiente; una respuesta HTTP por sí sola no demuestra que el destino funciona para el receptor.

Cada afirmación de derechos, acceso o procedencia debe apoyarse en evidencia. Si no puede probarse que una imagen es real, una etiqueta automática "real=True" no resuelve la incertidumbre. La ausencia de créditos se logra eligiendo activos compatibles con ese uso, no suponiendo permisos.

**[p.21]**

## 19 • FILTROS B — Calidad del PDF y acceso al contenido

| ID / tipo | Criterio propuesto | Prueba sobre la versión final |
|---|---|---|
| V01 · B | Archivo íntegro y texto disponible. | Abrir, renderizar y extraer contenido; verificar glifos, números y fuentes. |
| V02 · B | Cero solapamientos dañinos. | Texto/texto, texto/caja, texto/imagen, líneas y bordes: geometría más lectura del render. |
| V03 · B | Contraste suficiente. | Texto normal 4,5:1 y grande 3:1 según condiciones aplicables; revisar fondo real bajo el texto. [22] |
| V04 · B | Legibilidad en el contexto de lectura. | Prueba en visores y teléfonos previstos; el tamaño tipográfico del archivo no basta. |
| V05 · B | Imágenes y logos conformes al encargo. | Píxeles nativos, tamaño de colocación, recorte y fidelidad visual; ampliación no crea detalle nativo. |
| V06 · B | Enlaces correctos y utilizables. | Destino real, rectángulo clicable, orden y acceso en dispositivos previstos. |
| V07 · R | Jerarquía y orden coherentes. | Título, evidencia y precio se encuentran sin competir; lectura comprobada. |
| V08 · R | Espacios y divisores funcionales. | Respiración deliberada y retícula consistente; cero huecos accidentales ni líneas que cruzan contenido. |
| V09 · B | Estructura accesible cuando se exige. | Etiquetas, orden semántico, idioma, alternativas y validación manual; declarar alcance. [23-25] |
| V10 · R | Identidad propia con patrón comprensible. | Evaluación de concepto y tratamiento; no penalizar por compartir convenciones útiles. |
| V11 · B | El archivo entregado es el revisado. | Hash idéntico al evaluado; cualquier edición posterior invalida el permiso. |
| V12 · R | Peso compatible con canal y contexto. | Presupuesto de bytes fijado antes de exportar; revisar compresión y apertura real. |

Para una web, el mínimo WCAG 2.2 de ciertos objetivos de puntero es 24 × 24 píxeles CSS con excepciones. No se convierte automáticamente a 24 puntos en un PDF: tamaño de página, zoom y visor cambian el área efectiva. [22]

**[p.22]**

## 20 • FILTROS C — Evidencia y liberación

| ID / tipo | Condición | Tratamiento de incumplimiento |
|---|---|---|
| E01 · B | Protocolo UX aplicable vigente. | Bloquear si una nueva familia de diseño o población exige prueba y todavía no existe. |
| E02 · B | Sin incidentes críticos abiertos. | Corregir y revalidar; una firma no transforma un error material en cumplimiento. |
| E03 · R | Comprensión y esfuerzo dentro de objetivos. | Comparar con línea base y mostrar tamaño de muestra e incertidumbre. |
| E04 · B | Medidas y etiquetas consistentes. | Invalidar conclusiones que mezclan entrevistas, simulación o aceptación de Eduardo con contratación. |
| P01 · B para predecir | Modelo validado para el uso. | Retirar probabilidad; se puede evaluar por reglas si la política permite modo sin predicción. |
| P02 · B para predecir | Entrada dentro del ámbito aceptable. | Abstenerse ante datos faltantes relevantes o cambio importante de contexto. |
| P03 · B para predecir | Probabilidades calibradas y evaluadas fuera de muestra. | No publicar porcentaje de éxito a partir de una puntuación experta. |
| P04 · R | Comparación robusta de alternativas. | Si la elección cambia con supuestos plausibles, declarar incertidumbre y priorizar prueba. |
| L01 · B | Todas las reglas aplicables satisfechas. | FAIL, ERROR, MISSING o REVIEW pendiente impiden liberación. |
| L02 · B | Evidencia vigente y ligada a archivo/política. | Cambio de archivo o requisitos anula evaluación anterior. |
| L03 · B | Vía de entrega bajo control. | No permitir exportación al cliente por rutas que omitan el permiso de liberación. |

### Cómo evitar un bloqueo eterno por no tener un predictor

Definir desde el inicio dos políticas explícitas: **entrega con conformidad y revisión UX**, y **entrega con predicción validada adicional**. P01-P03 son obligatorios para afirmar probabilidades; no para fingir que no se puede mejorar nada hasta reunir miles de resultados. El modo seleccionado aparece en la auditoría interna.

Cambiar una regla exige versionar la política y revalidar. NOT_APPLICABLE necesita una razón comprobable; no sustituye una prueba pendiente.

**[p.23]**

## 21 • CONTROL OBLIGATORIO — Cómo impedir de verdad una entrega incumplidora

Una instrucción textual como "revisa todo antes de entregar" ayuda, pero no impone control de acceso. Se propone que el generador escriba únicamente en borradores y que un componente independiente autorice el envío del archivo cuyo hash ha sido evaluado.

### Contrato mínimo de cada comprobación

| Campo | Ejemplo conceptual |
|---|---|
| Identidad | rule_id: C01; policy_version: ux-propuestas-1.0 |
| Aplicabilidad | Siempre para propuestas comerciales; requiere marca/país/precio/divisa. |
| Método | Comparación entre brief confirmado y contenido extraído del PDF final. |
| Estado | PASS / FAIL / REVIEW / MISSING / ERROR / NOT_APPLICABLE |
| Evidencia | Referencia al brief, página, fragmento, hash y versión del verificador. |
| Responsable | Verificador determinista; discrepancias a revisión humana identificada. |
| Validez | Solo para el hash y la política registrados; evidencias externas con vigencia definida. |

### Lógica de liberación propuesta

1. Congelar brief, reglas y archivo candidato. 2. Calcular qué pruebas corresponden. 3. Ejecutarlas y comprobar que sus evidencias existen. 4. Resolver revisiones requeridas. 5. Bloquear si falta algo o queda un fallo. 6. Emitir un permiso verificable vinculado al hash del PDF y de la política. 7. La vía de entrega compara ambos antes de permitir salida.

El generador no debe poder alterar resultados ni fabricar firmas. Los fallos de un verificador, timeout, OCR o renderer nunca cuentan como aprobado. Debe existir trazabilidad del responsable y protección contra reutilizar un informe anterior para un archivo modificado.

Este esquema puede impedir liberaciones fuera de política dentro de un sistema correctamente integrado. No puede impedir que alguien descargue un borrador y lo envíe por una vía externa sin control. Tampoco elimina errores desconocidos del propio verificador.

**[p.24]**

## 22 • PROBAR EL VERIFICADOR — El filtro también puede equivocarse

Antes de usarlo como barrera de salida se necesita un banco de casos correctos y defectuosos, anotados por revisores competentes. Debe incluir errores históricos de tus propuestas y casos que obliguen a distinguir un defecto de una decisión visual válida.

| Familia de prueba | Ejemplos que debe resolver |
|---|---|
| Semántica comercial | Moneda equivocada; precio contradictorio; confundir visualizaciones con tarifa; consumo sin definir. |
| Geometría y renderizado | Texto tapado por caja; acento cortado; línea sobre postre; tipografía sustituida; capas invisibles. |
| Evidencia y vínculos | Miniatura correcta con vídeo equivocado; enlace roto; cifras de fechas distintas; captura alterada. |
| Integración | Archivo cambiado después del PASS; auditoría ausente; regla nueva; renderer caído; datos incompletos. |
| Accesibilidad | Orden de lectura incorrecto pese a apariencia buena; CTA visual sin vínculo; imagen esencial sin alternativa. |
| Falsos positivos | Espacio intencional; foto de referencia correctamente usada; cifra de menú igual a la tarifa; nombre propio exento. |
| Contenido no confiable | Texto en una web o documento que instruye al evaluador a ignorar reglas o a inventar un PASS. |

### Métricas que debe publicar internamente

**Sensibilidad por gravedad:** qué fracción de defectos conocidos detecta. **Precisión:** cuántos bloqueos corresponden a errores reales. **Falsa liberación:** proporción de documentos defectuosos que pasan. **Falso bloqueo:** documentos correctos retenidos. **Cobertura:** pruebas aplicables completadas, con su calidad de evidencia.

Un objetivo inicial propuesto es bloquear todos los defectos críticos del banco de aceptación y no dejar revisiones pendientes. Alcanzarlo significa superar ese banco, no cero defectos en el mundo. El conjunto de prueba final debe permanecer separado de los ejemplos usados para ajustar el motor.

La revisión visual automática no debe evaluarse con etiquetas creadas únicamente por el mismo modelo. Incluir desacuerdos entre personas, adjudicación y evidencia renderizada. Las pruebas humanas y las herramientas técnicas se complementan. [4, 24]

**[p.25]**

## 23 • MODELOS CANDIDATOS — No hay un algoritmo que sea el mejor antes de compararlo

| Familia | Uso razonable | Límite principal |
|---|---|---|
| Reglas deterministas | Cumplimiento exacto, integridad y validación comercial. | No predicen experiencia humana ni detectan toda ambigüedad. |
| Tasas base / beta-binomial | Referencia simple y actualización de tasas por resultados. | Pocos casos producen intervalos amplios; agrupaciones pequeñas son inestables. |
| Regresión regularizada | Relación interpretable entre pocas variables relevantes y resultado. | Forma funcional limitada; correlación no implica efecto de cambiar una variable. |
| Modelo bayesiano jerárquico | Compartir información entre países, tipos de negocio o formatos. | Los supuestos y priors importan; no rescata datos sin pertinencia. |
| Gradient boosting tabular | Relaciones no lineales cuando hay volumen y variedad suficientes. | Sobreajuste, cambio de distribución y necesidad de calibración. |
| Supervivencia / riesgos competitivos | Tiempo hasta respuesta, aceptación o rechazo y expedientes incompletos. | Requiere fechas, seguimiento y supuestos adecuados sobre censura. |
| Texto, visión y embeddings | Representar contenido y diseño, recuperar comparables y detectar anomalías. | Variables de alta dimensión, sesgos y similitud engañosa. |
| Modelos causales / uplift | Efecto diferencial de variantes con datos de intervención adecuados. | Necesitan identificación causal; no basta historial seleccionado. |
| Bandits / optimización bayesiana | Aprender entre alternativas admisibles y gestionar exploración. | Asignación adaptativa complica inferencia; exige registro de probabilidades y resultados. |
| Predicción conforme | Conjuntos o intervalos de predicción con cobertura bajo supuestos. | Cobertura marginal no es certeza individual; cambios de distribución pueden invalidarla. [32] |

Para empezar, se propone comparar reglas y tasas base con un modelo pequeño regularizado o jerárquico. La complejidad se incorpora únicamente si mejora resultados de validación, estabilidad y coste de decisión. No es necesario entrenar un modelo fundacional propio para crear un sistema avanzado.

**[p.26]**

## 24 • PREDICCIÓN Y DECISIÓN — Qué debería calcular y cómo debe explicarlo

**Estimando definido.** Por ejemplo: probabilidad de aceptación al precio original en 30 días, para una nueva oportunidad elegible de un contexto especificado, usando únicamente información disponible antes del envío. Cambiar plazo, definición de aceptación o población cambia el problema.

### Modelo ilustrativo, no entrenado

logit(p) = intercepto + efecto de contexto + efecto de tipo de negocio + coeficientes de características disponibles antes del envío.

Los coeficientes se estiman con resultados y regularización; no se inventan. Si se usan niveles jerárquicos, el grado de intercambio de información depende del modelo y de los datos.

El archivo puede tener variables como orden de módulos, claridad de oferta o evidencia disponible. Los antecedentes de la relación y el canal también importan. No incorporar como predictor una negociación posterior, el número de seguimientos futuro ni otra señal que revele el resultado que se intenta anticipar.

| Salida | Evaluación necesaria |
|---|---|
| Probabilidad de aceptación | Brier score o log loss, comparación con tasa base y gráfico de calibración. La AUC mide discriminación, no calibración. |
| Intervalo / incertidumbre | Explicar si cubre parámetros, una tasa poblacional o un resultado futuro; no intercambiar significados. |
| Elección entre variantes | Comparar objetivos bajo restricciones, incertidumbre y coste; registrar cuánto cambia con supuestos plausibles. |
| Efecto de modificar diseño | Requiere experimento o identificación causal válida. La predicción observacional sola no lo demuestra. |

Guo y colaboradores muestran por qué la confianza de una red no debe aceptarse como probabilidad calibrada. La calibración se aprende con datos separados del ajuste y se revisa por contexto; la validación final no se reutiliza para escoger continuamente el ganador. [29, 31]

La decisión puede ser "A y B son indistinguibles con la evidencia actual". Elegir A por menor coste o menor riesgo en ese caso es una decisión explícita, no una superioridad estadística inventada.

**[p.27]**

## 25 • POTENCIA Y MUESTRA — Cuántos datos hacen falta depende de la pregunta

Para dos proporciones independientes, asignación 1:1, contraste bilateral, alfa 0,05 y potencia 80%, se calcularon los siguientes tamaños aproximados con la fórmula normal para diferencia de proporciones. No son resultados ni tasas actuales de [el creador].

| Escenario hipotético | Mejora absoluta | Muestra por variante | Total |
|---|---|---|---|
| Aceptación: 20% a 25% | 5 puntos | 1.094 | 2.188 |
| Aceptación: 20% a 30% | 10 puntos | 294 | 588 |
| Aceptación: 50% a 55% | 5 puntos | 1.565 | 3.130 |
| Comprensión: 80% a 90% | 10 puntos | 199 | 398 |

Fórmula utilizada: n ≈ [z(0,975)√(2 p̄(1-p̄)) + z(0,80)√(p₀(1-p₀)+p₁(1-p₁))]² / (p₁-p₀)²; p̄=(p₀+p₁)/2. Se redondeó hacia arriba. El cálculo omite pérdidas, agrupación por empresa, multiplicidad y desviaciones de ejecución; esas condiciones pueden aumentar la muestra.

### Cero fallos observados no significa riesgo cero

Bajo ensayos Bernoulli independientes y representativos, con 0 fallos en n casos, el límite superior unilateral exacto de 95% para la tasa de fallo es 1 - 0,05^(1/n). Con 5 casos es aproximadamente 45,1%; con 30, 9,5%; con 100, 3,0%; con 300, 1,0%. Un banco de errores construido artificialmente no representa automáticamente la prevalencia real.

### Tres tamaños de muestra diferentes

Descubrir problemas, estimar una tasa con precisión y detectar una mejora entre variantes requieren diseños distintos. Desarrollar un predictor añade otro problema: depende del número de parámetros, prevalencia del resultado y rendimiento esperado. Riley y colaboradores ofrecen un marco formal; su aplicación aquí requiere adaptación, no importar umbrales clínicos como garantía comercial. [30]

Quince resultados permiten iniciar un registro y actualizar una tasa con incertidumbre. No bastan por definición para demostrar probabilidades personalizadas fiables por país, producto y precio. Contar páginas, visitas o simulaciones como oportunidades independientes produciría una precisión ficticia.

**[p.28]**

## 26 • EXPERIMENTO DE CAMPO — Cómo demostrar que mejora tus propuestas

**Definir una comparación justa.** Línea base: proceso vigente y sus mejores propuestas aprobadas. Tratamiento: mismo encargo atendido con los filtros y selección propuestos. Mantener oferta, precio y seguimiento equivalentes cuando se quiera atribuir el efecto al diseño; si cambia todo el proceso, declarar que se evalúa el paquete completo.

**Aleatorizar por oportunidad o empresa.** Asignar antes del envío. Evitar que la misma empresa reciba variantes rivales o que cada equipo seleccione los clientes más favorables. Estratificar por factores importantes cuando haya suficiente muestra, sin crear decenas de grupos vacíos.

**Preregistrar.** Definir hipótesis, resultado principal, diferencia mínima relevante, horizonte, muestra, exclusiones, métricas de protección y regla de parada. No detener al ver por primera vez un p menor de 0,05; para mirar repetidamente, usar un diseño secuencial válido.

**Verificar ejecución.** Comprobar asignación, duplicados, entregabilidad y posibles desbalances de muestra. Microsoft documenta cómo los errores de métricas y el Sample Ratio Mismatch pueden invalidar conclusiones aparentemente convincentes. [38, 39]

**Analizar como se asignó.** La comparación principal conserva la asignación aleatoria. Registrar cambios y pérdidas; evitar analizar solo quienes abrieron o respondieron, porque eso puede introducir selección posterior al tratamiento.

**Reportar utilidad práctica.** Diferencia absoluta y relativa, intervalo, costes, margen, comprensión, cancelaciones y resultados por contexto con incertidumbre. Un resultado no significativo no demuestra igualdad ni ausencia de efecto.

Cuando el volumen comercial no permite detectar mejoras pequeñas, usar estudios de comprensión para eliminar fricciones claras, mantener hipótesis comerciales prudentes y acumular evidencia. El control de calidad sigue aportando valor aunque no se pueda demostrar aún un aumento de contratación.

Antes de generalizar a nuevos países o tipos de negocio, repetir validación externa. Una mejora observada en propuestas de restaurantes españoles no prueba que funcione igual en automoción venezolana.

**[p.29]**

## 27 • CRITERIO DE LIDERAZGO — Qué exigir para llamarlo superior

| Dimensión de comparación | Prueba propuesta |
|---|---|
| Cumplimiento | Mismo banco ciego de propuestas correctas y defectuosas, con jueces independientes y gravedad fijada. |
| Experiencia | Mismas tareas y participantes comparables; comprensión, esfuerzo, acceso y preferencia medidos por separado. |
| Predicción | Prueba temporal intacta y empresas fuera de entrenamiento; tasas base y modelos sencillos como referencias. |
| Resultado comercial | Experimento prospectivo frente al sistema vigente y otros métodos relevantes disponibles. |
| Generalización | Resultados por contexto, dispositivo, idioma y tipo de oferta; no ocultar segmentos donde falla. |
| Eficiencia | Tiempo humano, coste por propuesta, latencia, falsos bloqueos y mantenimiento. |
| Transparencia | Protocolo, versiones, exclusiones, incertidumbre y documentación suficiente para reproducción. |

### Controles contra una evaluación complaciente

Separar datos por empresa, periodo y familias de propuestas cuando corresponda. No poner casi duplicados en entrenamiento y prueba. Mantener también un conjunto prospectivo que no haya influido en reglas, prompts o selección de modelos. Cawley y Talbot documentan cómo escoger sobre repetidos resultados de validación puede sesgar la evaluación. [29]

Una evaluación externa útil compara el motor completo con tu proceso actual, una revisión humana experta, reglas automáticas sencillas y un modelo genérico bajo recursos comparables. Las ablaciones prueban cuánto aporta cada componente: más módulos no implica más mejora.

Una afirmación defendible sería: "superó a los sistemas A y B en estas tareas, poblaciones, métricas y fechas". No sería defendible transformar ese resultado en "domina absolutamente toda la UX" o "es el mejor del mundo" sin un ámbito definido.

**[p.30]**

## 28 • APLICACIÓN AL SISTEMA ACTUAL — Qué conserva y qué debe probar el Documento Maestro

Se revisó el texto actual del **Documento Maestro - Propuestas [el creador] v4 (2).pdf**, cuyo contenido se identifica como v4.3 del 25/09/2026. Esta revisión estudia la especificación; no ejecuta ni audita su implementación en el ZIP. [44]

| Elemento del documento | Tratamiento recomendado |
|---|---|
| 0 FALLOS, QA geométrico y revisión visual | Conservar como barrera. Añadir evidencia por regla y validación del archivo final; no llamarlo ausencia absoluta de defectos. |
| Precio solo en inversión, país y moneda del encargo | Conservar como requisitos comerciales propios. No presentarlos como leyes universales de conversión. |
| Fotos reales, 3 evidencias y links correctos | Conservar trazabilidad. La identidad y procedencia no se verifican con un booleano autodeclarado. |
| Aprendizaje segmentado con 15 resultados | Tratarlo como comienzo de actualización exploratoria; exigir validación y calibración antes de afirmar precisión. |
| Pesos 65% juicio / 35% técnico para antojo | Son una regla de diseño del kit. No equivalen a coeficientes científicos ni a medición de deseo humano. |
| Paleta WGSN, 60/30/10 y tipografías | Conservar si son requisitos creativos vigentes. El beneficio comercial local debe medirse; no atribuir eficacia al prestigio de una tendencia. |
| 8 pt de texto mínimo / revisión al 50% | No basta para legibilidad móvil. Probar tamaño efectivo en el visor y comprensión; resolver conflictos de espacio sin encoger información crítica. |
| Creative Independence Gate | Mantener identidad propia; distinguir copia de concepto de convenciones útiles de lectura. No variar por variar a costa de comprensión. |
| Sin huecos y divisores con respiración | Conservar intención visual. Diferenciar hueco accidental de espacio que ayuda a agrupar y leer. |
| Analogías con motores de grandes empresas | Exigir comparación real; usar la misma familia matemática no implica igual eficacia, datos ni infraestructura. |

Estas recomendaciones no reescriben tus reglas aprobadas. Proponen una capa adicional de evidencia y controles, y señalan qué afirmaciones técnicas necesitan demostración antes de convertirse en garantías.

**[p.31]**

## 29 • EJEMPLO DE FUNCIONAMIENTO — Una propuesta atractiva puede quedar bloqueada

**Escenario ficticio.** Restaurante de España, tarifa confirmada de 350 €, consumo a cargo del restaurante, entregables definidos y grupo europeo de tres evidencias. Se ilustra cómo operarían los controles; no se evaluó una marca real ni se inventaron sus resultados.

| Hallazgo del caso simulado | Estado | Acción |
|---|---|---|
| Diseño A muestra 350 $ en el PDF aunque el brief dice euros. | FAIL C01/C07 | Bloqueo. Corregir moneda y volver a validar archivo completo. |
| Diseño B corrige moneda, pero el tercer link pertenece a otro vídeo. | FAIL C05 | Bloqueo. Identificar pieza y comprobar destino. |
| Diseño C resuelve enlaces; la cifra queda parcialmente tapada por una caja. | FAIL V02 | Bloqueo aunque el texto extraído siga mostrando la tarifa. |
| Diseño D corrige lo anterior; utiliza una estructura nueva sin evidencia UX aplicable. | MISSING E01 | Realizar la revisión o estudio exigido por la política de esa familia. |
| Versión final cumple controles y revisiones; predictor comercial no validado. | APTO en modo sin predicción | Entregar si la política elegida lo permite. No adjuntar una probabilidad inventada. |

### Comparar dos variantes que ya cumplen

Si ambas son admisibles, el motor puede comparar comprensión, facilidad, atractivo y coste. La alternativa que gusta más no gana automáticamente si induce más errores de condiciones. Si no existe diferencia concluyente, se conserva incertidumbre y puede elegirse la más sencilla de producir o la más consistente con la marca.

Salida interna mínima: archivo/hash, versión de política, modo, pruebas realizadas, fallos abiertos, revisiones, alcance de evidencia humana, predicción disponible o no, motivo de elección y próximos datos necesarios. Ninguna nota global sustituye ese registro.

**[p.32]**

## 30 • PUESTA EN MARCHA — Secuencia de implementación con criterios de salida

| Fase | Trabajo concreto | Se avanza cuando |
|---|---|---|
| 1. Contrato y línea base | Consolidar reglas v4.3, ejemplos aprobados, defectos históricos y definiciones de resultado. | Cada requisito tiene origen, prueba, responsable y aplicabilidad. |
| 2. Control técnico | Construir validadores, renderizado, informe de evidencia y permiso de entrega ligado al hash. | Pasa el banco de aceptación y se demuestra que rutas inválidas quedan bloqueadas. |
| 3. Investigación inicial | Probar comprensión, precio, entregables y CTA en contextos prioritarios. | Se corrigen incidentes críticos y se documenta qué familias de diseño cubre la evidencia. |
| 4. Registro prospectivo | Guardar oportunidades, asignaciones, seguimiento y resultados reales. | Hay etiquetas consistentes y se distinguen rechazo, negociación y pendientes. |
| 5. Predicción en observación | Comparar modelos pequeños y bases sin que decidan envíos por sí solos. | Superan referencias con calibración y utilidad suficientes en datos separados. |
| 6. Experimento comercial | Comparar proceso nuevo y vigente con diseño y muestra adecuados. | Se sostiene mejora útil sin deterioro de comprensión, operación o margen. |
| 7. Escala y vigilancia | Nuevos contextos, seguimiento de deriva, incidentes y reversión. | Cada expansión conserva evidencia y posibilidad de retirar predicciones no fiables. |

Equipo mínimo propuesto por competencias: dirección de investigación, diseño editorial/contenido, ingeniería de validación y datos/experimentos, con revisión de accesibilidad y negocio. Pueden combinarse funciones, pero quien genera no debe ser la única fuente de validación.

No se fija un precio ni un calendario ficticio: faltan estado real del código, acceso a datos, disponibilidad de destinatarios, ritmo de propuestas y necesidades de integración. El coste debe presupuestarse como horas de investigación y revisión + captación de participantes + ingeniería + infraestructura + mantenimiento. El gasto de cómputo puede ser menor que el de conseguir resultados fiables.

**[p.33]**

## 31 • MANTENIMIENTO — Cómo aprender sin degradar lo que ya funciona

**Versiones controladas.** Congelar reglas, rúbricas, modelos, prompts, datos y renderizador de cada entrega. Reentrenar no autoriza automáticamente a promover un modelo nuevo; debe repetir las pruebas relevantes y superar una comparación definida.

**Incidentes como evidencia.** Cada corrección de Eduardo debe clasificarse: regla comercial, defecto de implementación, criterio creativo, barrera UX o preferencia personal. Convertir lo verificable en caso de prueba, evitando transformar cada preferencia aislada en una ley psicológica.

**Vigencia de la evidencia.** Comprobar resultados de fuentes, enlaces, ofertas y documentos según su volatilidad. Revisar mediciones y calibración cuando cambie el tipo de cliente, formato, idioma, precio, canal o proporción de resultados.

**Abstención y reversión.** Suspender predicciones si faltan variables clave, se deteriora la calibración o aparecen entradas sin precedentes relevantes. Conservar un proceso válido de reglas y revisión para mantener operación sin fingir confianza.

**Aprendizaje seguro.** Explorar entre alternativas que ya cumplen el mínimo de calidad. Registrar probabilidades de asignación si se utiliza un bandit; mantener evaluación independiente porque el sistema puede aprender de su propia selección sesgada.

**Privacidad proporcional.** Recoger solo los datos necesarios para la pregunta. Seudonimizar estudios, limitar acceso y retención, y documentar permisos de grabación o instrumentación. Para obligaciones legales concretas se necesita una revisión por jurisdicción; no se presupone cumplimiento por usar una herramienta. [33]

La mejora continua se demuestra con una serie de resultados, no con el número de reglas añadidas. Un modelo que mantiene calidad con menos datos sensibles, menos falsos bloqueos o menor esfuerzo humano puede ser mejor aunque sea matemáticamente más sencillo.

**[p.34]**

## 32 • RESPUESTA A TU OBJETIVO — La ambición correcta es verificable

**Sí es posible crear un motor avanzado de UX para tus propuestas.** La combinación más defendible es investigación con personas, diseño editorial de calidad, validadores técnicos, estadística, aprendizaje calibrado y una barrera real de entrega. No existe fundamento para prometer dominio de la UX al 100% ni una lista finita que contenga a todas las personas y disciplinas que podrán aportar al campo.

### Qué queda especificado en este estudio

Un mapa de 30 funciones; una base histórica y reciente; 33 filtros iniciales agrupados en contenido, visual, evidencia y liberación; un contrato de evaluación; una arquitectura; medidas de calidad; modelos candidatos; ejemplos de potencia; protocolo de comparación y una ruta de incorporación al Documento Maestro.

### Qué todavía no está demostrado

La capacidad real del kit actual para aplicar cada regla, la tasa de defectos que deja pasar, la experiencia de los destinatarios, la calidad de un predictor de contratación y el aumento de aceptación frente a tu proceso actual. Tampoco se han ejecutado pruebas con personas ni se ha hecho una nueva síntesis estadística de datos crudos.

### Primer resultado de ingeniería que conviene exigir

Un prototipo de verificador capaz de recibir el brief y el PDF final, producir un informe por regla y bloquear efectivamente los casos defectuosos conocidos. A continuación, demostrar que los documentos admitidos son comprensibles para destinatarios reales. El predictor comercial se incorpora cuando haya evidencia para calibrarlo.

**La garantía razonable:** "Esta versión cumplió todas las reglas aplicables y las revisiones exigidas, con estas pruebas y estos límites".

**La meta científica:** "El sistema mejora de forma reproducible una experiencia y unos resultados definidos". Ambas son exigentes, útiles y comprobables.

Las referencias siguientes permiten distinguir resultados científicos, métodos, normas y requisitos privados. Los umbrales y decisiones de ingeniería no derivados de una norma se han presentado como propuestas que requieren validación.

**[p.35]**

## REFERENCIAS • 1 — Fuentes y nivel de acceso

**[1]** ISO (2019; confirmación 2025). ISO 9241-210:2019. Ergonomics of human-system interaction: Human-centred design for interactive systems.

[Abrir fuente verificable](https://www.iso.org/standard/77520.html)

Ficha y resumen oficiales; no se leyó el texto completo de pago.

**[2]** International Ergonomics Association. What Is Ergonomics (HFE)?

[Abrir fuente verificable](https://iea.cc/about/what-is-ergonomics/)

Definición y ámbitos de la asociación internacional.

**[3]** Nielsen, J. (2000). Why You Only Need to Test with 5 Users. Nielsen Norman Group.

[Abrir fuente verificable](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/)

Guía profesional del autor sobre rondas formativas; no garantía estadística universal.

**[4]** Moran, K. y Gordon, K. (2023). How to Conduct a Heuristic Evaluation. NN/g.

[Abrir fuente verificable](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/)

Texto profesional íntegro consultado; distingue heurísticas y estudios con usuarios.

**[5]** Hick, W. E. (1952). On the Rate of Gain of Information. Quarterly Journal of Experimental Psychology. DOI: 10.1080/17470215208416600.

[Abrir fuente verificable](https://journals.sagepub.com/doi/10.1080/17470215208416600)

Resumen editorial del experimento original.

**[6]** Fitts, P. M. (1954). The information capacity of the human motor system in controlling the amplitude of movement. DOI: 10.1037/h0055392.

[Abrir fuente verificable](https://pubmed.ncbi.nlm.nih.gov/13174710/)

Registro de la publicación original, contrastado con DOI y copia académica.

**[7]** Miller, G. A. (1956). The magical number seven, plus or minus two. Psychological Review, 63(2), 81-97. DOI: 10.1037/h0043158.

[Abrir fuente verificable](https://pubmed.ncbi.nlm.nih.gov/13310704/)

Registro bibliográfico y resumen de fuente primaria.

**[8]** Cowan, N. (2001). The magical number 4 in short-term memory: a reconsideration of mental storage capacity.

[Abrir fuente verificable](https://pubmed.ncbi.nlm.nih.gov/11515286/)

Resumen de revisión teórica; condiciones de medida, no regla de diseño de menús.

Fecha de consulta: 26/09/2026. Los enlaces son clicables. "Consultado" no significa reanalizado ni reproducido experimentalmente. Las referencias privadas no constituyen prueba científica externa.

**[p.36]**

## REFERENCIAS • 2 — Fuentes y nivel de acceso

**[9]** Wagemans, J. y colaboradores (2012). A century of Gestalt psychology in visual perception: I. Perceptual grouping and figure-ground organization.

[Abrir fuente verificable](https://pmc.ncbi.nlm.nih.gov/articles/PMC3482144/)

Revisión científica abierta; base de agrupación perceptual.

**[10]** Card, S. K., Moran, T. P. y Newell, A. (1983). The Psychology of Human-Computer Interaction.

[Abrir fuente verificable](https://www.routledge.com/The-Psychology-of-Human-Computer-Interaction/Card-Moran-Newell/p/book/9780898598599)

Ficha y descripción editorial; no se declara lectura íntegra del libro.

**[11]** Suchman, L. A. (1987). Plans and Situated Actions: The Problem of Human-Machine Communication. Cambridge University Press.

[Abrir fuente verificable](https://assets.cambridge.org/97805213/37397/frontmatter/9780521337397_frontmatter.pdf)

Identidad editorial contrastada. El argumento se contrastó también en el resumen de Conclusion to the 1st Edition, Cambridge Core.

**[12]** Norman, D. (1988). The Design of Everyday Things.

[Abrir fuente verificable](https://jnd.org/books/the-design-of-everyday-things-1st-ed/)

Página del autor y descripción de la primera edición; referencia histórica.

**[13]** Desmet, P. y Hekkert, P. (2007). Framework of Product Experience. International Journal of Design, 1(1), 57-66.

[Abrir fuente verificable](https://www.ijdesign.org/index.php/IJDesign/article/view/66)

Artículo y resumen de sus autores; marco conceptual.

**[14]** Schlamann, M., Nestler, S. y Thielsch, M. T. (2026). Attractive Things Do Work Better: A Meta-Analysis on Visual Aesthetics and User Performance. DOI: 10.1080/10447318.2026.2664081.

[Abrir fuente verificable](https://zenodo.org/records/18777943)

Resumen editorial contrastado y materiales de autores, DOI del repositorio: 10.5281/zenodo.18777943. Datos y scripts disponibles; no reanalizados.

**[15]** Hertzum, M. (2025). Understanding Preference: A Meta-Analysis of User Studies. International Journal of Human-Computer Studies, 195, 103408. DOI: 10.1016/j.ijhcs.2024.103408.

[Abrir fuente verificable](https://forskning.ruc.dk/en/publications/understanding-preference-a-meta-analysis-of-user-studies/)

Resumen y metadatos del repositorio institucional. Año del volumen 2025; DOI contiene 2024.

**[16]** Perrig, S. A. C. y colaboradores (2024). Measurement practices in user experience (UX) research: a systematic quantitative literature review. Frontiers in Computer Science, 6. DOI: 10.3389/fcomp.2024.1368860.

[Abrir fuente verificable](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2024.1368860/full)

Artículo abierto consultado, con método y resultados de la revisión.

Fecha de consulta: 26/09/2026. Los enlaces son clicables. "Consultado" no significa reanalizado ni reproducido experimentalmente. Las referencias privadas no constituyen prueba científica externa.

**[p.37]**

## REFERENCIAS • 3 — Fuentes y nivel de acceso

**[17]** Hertzum, M. (2026). System Usability Scale: A Meta-Analysis of How SUS Relates to Workload, Task Time, and Error Rate. DOI: 10.1080/10447318.2026.2625260.

[Abrir fuente verificable](https://forskning.ruc.dk/en/publications/system-usability-scale-a-meta-analysis-of-how-sus-relates-to-work/)

Resumen institucional y publicación online de 16/02/2026. Texto editorial directo bloqueado durante consulta.

**[18]** Scheibehenne, B., Greifeneder, R. y Todd, P. M. (2010). Can There Ever Be Too Many Options? A Meta-Analytic Review of Choice Overload. DOI: 10.1086/651235.

[Abrir fuente verificable](https://scheibehenne.com/ScheibehenneGreifenederTodd2010.pdf)

PDF del autor consultado; efecto e intervalo de confianza verificados en el cuerpo.

**[19]** Chernev, A., Böckenholt, U. y Goodman, J. (2015). Choice overload: A conceptual review and meta-analysis. DOI: 10.1016/j.jcps.2014.08.002.

[Abrir fuente verificable](https://myscp.onlinelibrary.wiley.com/doi/full/10.1016/j.jcps.2014.08.002)

Resumen editorial; 99 observaciones y N=7.202. No se reestimaron efectos ni moderadores.

**[20]** Reinecke, K. y Gajos, K. Z. (2014). Quantifying Visual Preferences Around the World. CHI 2014, 11-20.

[Abrir fuente verificable](https://www.eecs.harvard.edu/~kgajos/papers/2014/reinecke14visual.shtml)

Página de los autores con resumen, publicación y recursos.

**[21]** Lindgaard, G., Fernandes, G., Dudek, C. y Brown, J. (2006). Attention web designers: You have 50 milliseconds to make a good first impression! DOI: 10.1080/01449290500330448.

[Abrir fuente verificable](https://doi.org/10.1080/01449290500330448)

Registro y resumen editorial. Se limita la inferencia a primera impresión visual.

**[22]** W3C (2024). Web Content Accessibility Guidelines (WCAG) 2.2. Recomendación de 12/12/2024.

[Abrir fuente verificable](https://www.w3.org/TR/2024/REC-WCAG22-20241212/)

Texto normativo consultado en la ruta vigente; aplicabilidad y excepciones deben revisarse por criterio.

**[23]** W3C. Guidance on Applying WCAG 2 to Non-Web Information and Communications Technologies (WCAG2ICT).

[Abrir fuente verificable](https://www.w3.org/TR/wcag2ict/)

Guía para tecnologías no web; no convierte todo criterio web en idéntica prueba para PDF.

**[24]** W3C WAI. Evaluating Web Accessibility Overview.

[Abrir fuente verificable](https://www.w3.org/WAI/test-evaluate/)

Guía oficial: herramientas y evaluación humana complementarias.

Fecha de consulta: 26/09/2026. Los enlaces son clicables. "Consultado" no significa reanalizado ni reproducido experimentalmente. Las referencias privadas no constituyen prueba científica externa.

**[p.38]**

## REFERENCIAS • 4 — Fuentes y nivel de acceso

**[25]** PDF Association (2024). ISO 14289-2 / PDF/UA-2.

[Abrir fuente verificable](https://pdfa.org/iso-14289-2-pdfua-2/)

Descripción oficial del estándar para PDF 2.0; no certificación de los documentos de este proyecto.

**[26]** Brooke, J. (1996). SUS: A quick and dirty usability scale.

[Abrir fuente verificable](https://digital.ahrq.gov/sites/default/files/docs/survey/systemusabilityscale%2528sus%2529_comp%255B1%255D.pdf)

Capítulo original alojado por AHRQ; contexto, instrumento y método de puntuación.

**[27]** Rodden, K., Hutchinson, H. y Fu, X. (2010). Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications.

[Abrir fuente verificable](https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/)

Publicación original de Google Research; marco HEART.

**[28]** NASA. NASA Task Load Index (TLX).

[Abrir fuente verificable](https://www.nasa.gov/human-systems-integration-division/nasa-task-load-index-tlx/)

Página oficial del instrumento y dimensiones de carga subjetiva.

**[29]** Cawley, G. C. y Talbot, N. L. C. (2010). On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation. JMLR, 11, 2079-2107.

[Abrir fuente verificable](https://www.jmlr.org/beta/papers/v11/cawley10a.html)

Artículo de métodos; validación y sesgo de selección.

**[30]** Riley, R. D. y colaboradores (2020). Calculating the sample size required for developing a clinical prediction model. BMJ, 368:m441.

[Abrir fuente verificable](https://www.bmj.com/content/368/bmj.m441)

Marco de tamaño muestral. Se usa su principio metodológico, sin trasladar garantías clínicas a ventas.

**[31]** Guo, C., Pleiss, G., Sun, Y. y Weinberger, K. Q. (2017). On Calibration of Modern Neural Networks. ICML, PMLR 70, 1321-1330.

[Abrir fuente verificable](https://proceedings.mlr.press/v70/guo17a.html)

Publicación primaria sobre calibración de probabilidades.

**[32]** Angelopoulos, A. N. y Bates, S. (2021; versión 2022). A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification. arXiv:2107.07511.

[Abrir fuente verificable](https://arxiv.org/abs/2107.07511)

Manuscrito tutorial de autores; posterior tratamiento en Foundations and Trends in Machine Learning (2023).

Fecha de consulta: 26/09/2026. Los enlaces son clicables. "Consultado" no significa reanalizado ni reproducido experimentalmente. Las referencias privadas no constituyen prueba científica externa.

**[p.39]**

## REFERENCIAS • 5 — Fuentes y nivel de acceso

**[33]** NIST (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0). DOI: 10.6028/NIST.AI.100-1.

[Abrir fuente verificable](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)

Marco voluntario de gestión. Consultado también perfil de IA generativa (2024), DOI: 10.6028/NIST.AI.600-1.

**[34]** Camerer, C. F. y colaboradores (2018). Evaluating the replicability of social science experiments in Nature and Science between 2010 and 2015. Nature Human Behaviour, 2, 637-644.

[Abrir fuente verificable](https://www.nature.com/articles/s41562-018-0399-z)

Estudio de replicación; DOI: 10.1038/s41562-018-0399-z. No generalizar la tasa a toda la ciencia.

**[35]** Seshadri, P., Cahyawijaya, S., Odumakinde, A., Singh, S. y Goldfarb-Tarrant, S. (2026). Lost in Simulation: LLM-Simulated Users are Unreliable Proxies for Human Users in Agentic Evaluations.

[Abrir fuente verificable](https://arxiv.org/html/2601.17087v2)

Manuscrito v2 del 28/01/2026 consultado; registro de publicación corroborado en ACL 2026, artículo 2192.

**[36]** Zheng, L. y colaboradores (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. NeurIPS 2023, Datasets and Benchmarks.

[Abrir fuente verificable](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html)

Publicación primaria sobre evaluación con LLM. Transferencia a diseño documental es una hipótesis de ingeniería.

**[37]** Linardos, A., Kümmerer, M., Press, O. y Bethge, M. (2021). DeepGaze IIE: Calibrated Prediction in and Out-of-Domain for State-of-the-Art Saliency Modeling. ICCV, 12919-12928.

[Abrir fuente verificable](https://openaccess.thecvf.com/content/ICCV2021/html/Linardos_DeepGaze_IIE_Calibrated_Prediction_in_and_Out-of-Domain_for_State-of-the-Art_Saliency_ICCV_2021_paper.html)

Publicación primaria; saliencia visual no equivale a comprensión.

**[38]** Dmitriev, P., Gupta, S., Kim, D. W. y Vaz, G. (2017). A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls in Online Controlled Experiments. DOI: 10.1145/3097983.3098024.

[Abrir fuente verificable](https://www.microsoft.com/en-us/research/publication/a-dirty-dozen-twelve-common-metric-interpretation-pitfalls-in-online-controlled-experiments/)

Publicación de sus autores en Microsoft Research.

**[39]** Fabijan, A. y colaboradores (2019). Diagnosing Sample Ratio Mismatch in Online Controlled Experiments: A Taxonomy and Rules of Thumb for Practitioners.

[Abrir fuente verificable](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/)

Artículo original contrastado con explicación oficial de Microsoft Research (2020).

**[40]** W3C (2026). W3C Accessibility Guidelines (WCAG) 3.0. Working Draft de 10/09/2026.

[Abrir fuente verificable](https://www.w3.org/TR/2026/WD-wcag-3.0-20260910/)

Borrador consultado en la ruta vigente; no estándar final de conformidad.

Fecha de consulta: 26/09/2026. Los enlaces son clicables. "Consultado" no significa reanalizado ni reproducido experimentalmente. Las referencias privadas no constituyen prueba científica externa.

**[p.40]**

## REFERENCIAS • 6 — Fuentes y nivel de acceso

**[41]** Sweller, J. (1988). Cognitive Load During Problem Solving: Effects on Learning. Cognitive Science, 12, 257-285. DOI: 10.1207/s15516709cog1202_4.

[Abrir fuente verificable](https://doi.org/10.1207/s15516709cog1202_4)

Artículo original y resumen editorial; dominio original de aprendizaje.

**[42]** Autores del User Experience Questionnaire. UEQ y manual.

[Abrir fuente verificable](https://ueq-online.org/)

Instrumento y materiales de sus autores; consulta de dimensiones, versiones y documentación.

**[43]** Suchman, L. A. Conclusion to the 1st Edition. Human-Machine Reconfigurations. Cambridge Core.

[Abrir fuente verificable](https://www.cambridge.org/core/books/abs/humanmachine-reconfigurations/conclusion-to-the-1st-edition/8386E26332B53FF8314D54C5167BFCCF)

Resumen editorial de la conclusión de la primera edición, consultado para [11].

**[44]** Eduardo / sistema de propuestas (2026). Documento Maestro - Propuestas [el creador] v4 (2).pdf. Contenido identificado como v4.3, 25/09/2026.

Fuente privada del proyecto: texto de 27 páginas leído. Se analizó la especificación, sin ejecutar el kit ni verificar sus afirmaciones de desempeño.

Fecha de consulta: 26/09/2026. Los enlaces son clicables. "Consultado" no significa reanalizado ni reproducido experimentalmente. Las referencias privadas no constituyen prueba científica externa.
