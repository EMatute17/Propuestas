# UX. Motor predictivo de UX para propuestas de colaboración (análisis)

Análisis de Edumashow sobre el estudio de 40 páginas que Eduardo aportó. El texto completo y limpio está en `../texto/UX_motor_predictivo_ux.md`. Las páginas (p.N) son las del pie del PDF (n / 40). El estudio nombra al creador original de las propuestas; aquí se le llama el creador, según la regla de marca del proyecto.

## 1. Ficha

| Campo | Dato |
|---|---|
| Título | Un motor predictivo de UX para propuestas de colaboración. Base científica, filtros de entrega y protocolo para demostrar mejoras. Estudio de viabilidad y especificación |
| Fecha y corte | 26 de septiembre de 2026 (fecha de consulta de las fuentes: 26/09/2026) |
| Preparado para | Eduardo. Aplicación inicial: propuestas comerciales del creador, desde la recepción hasta la decisión y la ejecución de la colaboración |
| Naturaleza | Revisión integrativa dirigida (búsqueda web y contraste en artículos, repositorios de autores, normas y publicaciones de sus creadores). No es revisión sistemática exhaustiva ni un metaanálisis nuevo (p.4) |
| Estado real | Estudio y arquitectura propuestos. No se entrenó ni desplegó ningún motor, ni se ejecutó un experimento con marcas, ni se certificó el kit, ni se demostró una mejora de conversión (p.1). Los cálculos y escenarios propios se identifican como tales |
| Estructura | 32 secciones numeradas más 6 páginas de referencias [1] a [44]. Guía de lectura en la p.2: viabilidad pp.3 a 5; especialistas pp.6 a 8; historia y estudios recientes pp.9 a 13; a quién estudiar y qué medir pp.14 a 18; arquitectura y filtros pp.19 a 24; modelos, muestras y experimentos pp.25 a 29; incorporación al sistema del creador pp.30 a 34; fuentes pp.35 a 40 |
| Tema web | No trata de webs de restaurante. Trata de PDF de propuestas; sus filtros se tradujeron a web en el núcleo (ver SINTESIS) |

## 2. Tesis central (p.1, p.3, p.34)

- Es viable desarrollar un motor avanzado y especializado. Su excelencia tendría que demostrarse con comparaciones independientes, datos relevantes y resultados fuera de la muestra. La garantía defendible es sobre un proceso y sus controles definidos, nunca sobre una experiencia humana absoluta (p.1).
- Qué sí se puede construir: un control obligatorio que impida liberar archivos cuando falten pruebas exigidas o fallen reglas verificables; un sistema que compare diseños y estime resultados dentro de poblaciones y condiciones validadas; un proceso que aprenda de usuarios, resultados comerciales y errores documentados.
- Qué la evidencia no permite prometer: conocer el 100% de la experiencia de todas las personas, detectar todos los errores posibles o garantizar cada aceptación; ser el mejor motor del mundo por complejidad, número de variables, cantidad de agentes o una autoevaluación de 10 sobre 10; que observar patrones pruebe causalidad o que millones de simulaciones equivalgan a millones de usuarios reales.
- Garantía razonable (p.34): esta versión cumplió todas las reglas aplicables y las revisiones exigidas, con estas pruebas y estos límites. Meta científica: el sistema mejora de forma reproducible una experiencia y unos resultados definidos. Ambas son exigentes, útiles y comprobables.
- Primer resultado de ingeniería que conviene exigir (p.34): un prototipo de verificador que reciba el brief y el PDF final, produzca un informe por regla y bloquee de verdad los casos defectuosos conocidos. Después, demostrar que los documentos admitidos son comprensibles para destinatarios reales. El predictor comercial se incorpora cuando haya evidencia para calibrarlo.

## 3. Veredicto sobre el objetivo de Eduardo (sección 1, p.3)

| Objetivo | Veredicto | Condición |
|---|---|---|
| Bloquear propuestas que incumplen parámetros | Sí, dentro del sistema | Todos los caminos de entrega deben pasar por el verificador; la ausencia de prueba equivale a bloqueo |
| Detectar problemas de UX antes de enviar | Sí, parcialmente | Combinar controles automáticos, revisión experta y evidencia con personas representativas |
| Elegir entre alternativas | Sí, condicionado | Definir para quién, qué tarea, qué objetivo y qué perjuicios no se aceptan |
| Dar probabilidades fiables | Posible, por demostrar | Resultados etiquetados, validación externa, calibración, incertidumbre y vigilancia de cambios |
| Optimizar todos los objetivos a la vez | No en general | Hay conflictos: novedad frente a familiaridad, detalle frente a esfuerzo, velocidad frente a deliberación |
| Dominar UX al 100% o ganar siempre | No justificable | La experiencia depende de contexto, expectativas, capacidades, organización y tiempo |
| Ser el mejor en un dominio concreto | Meta evaluable | Superioridad replicada frente a competidores definidos, en tareas y poblaciones publicadas |

Tres salidas distintas que no se sustituyen entre sí: un resultado apto para entrega significa que se cumplieron las reglas y revisiones aplicables de una versión concreta; un resultado preferido indica por qué ganó una alternativa; una probabilidad de aceptación requiere otra evidencia. Aceptación y UX se relacionan pero no son la misma variable: una empresa puede entender perfectamente una propuesta y rechazarla por presupuesto, o aceptar una confusa porque ya conoce al creador.

## 4. Método del estudio y tipos de evidencia (sección 2, p.4)

| Tipo de evidencia | Uso correcto |
|---|---|
| Metaanálisis y revisiones | Resultados agregados, heterogeneidad, problemas de medición y límites de transferencia |
| Experimentos y estudios originales | Cómo se midió el efecto, quién participó y en qué tarea |
| Estándares y guías oficiales | Definir requisitos o métodos de evaluación; no atribuirles efectos causales sobre ventas |
| Fuentes profesionales de sus autores | Heurísticas y métodos prácticos; el prestigio no reemplaza una prueba empírica |
| Documento Maestro v4.3 (especificación privada del kit anterior) | Identificar requisitos propios; no es evidencia externa de eficacia |
| Diseño y cálculos del informe | Propuestas de ingeniería y ejemplos explícitos; no resultados observados |

Criterios: fuentes con autor, fecha, método y vínculo verificable; estudios que distinguen percepción y desempeño; resultados recientes pertinentes; trabajos históricos que aún orientan hipótesis medibles. Se descartó usar como prueba una lista comercial de leyes UX, una promesa de neuromarketing o cifras sin trazabilidad. Cuando el editor bloqueó el texto completo se contrastó el resumen en el repositorio institucional o de los autores (nivel de acceso indicado en las referencias). No se reanalizaron datos crudos. Los tamaños muestrales de distintos metaanálisis no se suman (pueden compartir estudios y participantes).

## 5. El tridente y el mapa de 30 funciones (secciones 3 a 6, pp.5 a 8)

- El tridente (investigador UX, diseñador UX/UI, analista de producto) es útil pero no contiene toda la UX. No existe un dueño de la verdad que domine la mente o la matemática al 100%. La división no es ley científica: una persona puede combinar competencias y un equipo grande puede equivocarse de forma coordinada (p.5).
- Aporte y límite de cada una: investigación de usuarios (necesidades, tareas, contexto, barreras y causas plausibles; no prueba que las entrevistas representen al mercado ni que lo declarado prediga la compra); diseño de interacción y visual (alternativas, jerarquía, navegación, legibilidad, respuesta del sistema; no prueba que una apariencia premium produzca comprensión); analítica y experimentación (medición del comportamiento, incertidumbre, experimentos; no prueba que una correlación explique por qué ocurre un problema).
- Quién decide: los usuarios aportan experiencia real; el negocio define objetivos y restricciones; investigadores y especialistas interpretan evidencia; ingeniería garantiza la ejecución; una persona responsable asume la decisión de liberar. NN/g es una referencia profesional reconocida pero no una biblia; sus guías dicen que la evaluación heurística no reemplaza las pruebas con usuarios. Material Design es un sistema de diseño de su creador, no prueba de superioridad (p.5).
- El mapa de 30 funciones es una taxonomía práctica propuesta, no un censo ni una recomendación de contratar a 30 personas. Pueden combinarse funciones; la independencia de la verificación debe preservarse. Los destinatarios reales, las personas con discapacidad, los equipos de marketing, los socios y los responsables de operación son colaboradores esenciales aunque no tengan cargo UX. La responsabilidad última de liberar no se diluye en una votación entre modelos (p.8).

| # | Función | Aplicación al motor |
|---|---|---|
| 1 | UXR cualitativo | Detectar vocabulario confuso y condiciones que el destinatario no entiende |
| 2 | UXR cuantitativo | Estimar comprensión y esfuerzo por población y dispositivo |
| 3 | Psicología cognitiva | Hipótesis de jerarquía y agrupación; medición por tarea |
| 4 | Ciencia de la percepción | Detectar interferencias y probar dónde se encuentra la información |
| 5 | Ergonomía y factores humanos | Revisar lectura, manipulación, fatiga y restricciones de trabajo |
| 6 | Antropología y etnografía | Entender cómo un dueño comparte la propuesta con su socio |
| 7 | Sociología e investigación cultural | Evitar usar el país como sustituto de preferencias individuales |
| 8 | Economía conductual y decisión | Probar cantidad y presentación de opciones; no asumir un número mágico |
| 9 | Psicometría | Impedir que preguntas inventadas se vendan como escalas validadas |
| 10 | ResearchOps y ciencia de encuestas | Panel pertinente y registro reutilizable de hallazgos |
| 11 | Arquitectura de información | Que se encuentren inversión, entregables, pruebas y siguiente paso |
| 12 | Diseño de interacción | Comprobar apertura de enlaces, regreso al documento y respuesta al CTA |
| 13 | Diseño visual y editorial | Revisar el render, no solo el texto o las coordenadas |
| 14 | UX writing y lingüística | Evitar ambigüedad entre precio, consumo, producción y plataformas |
| 15 | Estrategia de contenido | Vincular cada afirmación con una fuente y una necesidad de decisión |
| 16 | Accesibilidad y diseño inclusivo | Orden de lectura, alternativas textuales y tareas con usuarios diversos |
| 17 | Diseño de servicios y CX | Evaluar correo, propuesta, negociación, producción y renovación |
| 18 | Localización y comunicación intercultural | Adaptar expresiones y condiciones según información confirmada |
| 19 | Marca y dirección de arte | Usar referencias aprobadas como nivel, con una idea propia y coherente |
| 20 | Diseño afectivo | Examinar atractivo y confianza sin confundirlos con éxito de tarea |
| 21 | Product analyst y CRO | Distinguir entrega, respuesta, negociación, aceptación y renovación |
| 22 | Estadística y ciencia experimental | Separar señales de ruido y resultados exploratorios de confirmatorios |
| 23 | Ciencia causal y econometría | Estudiar si cambiar el diseño mejora resultados con comparación válida |
| 24 | ML y modelado predictivo | Predicciones con límites por país, marca, tipo de oferta y periodo |
| 25 | Visión artificial y document AI | Identificar posibles defectos y asistir la revisión; no leer emociones como hechos |
| 26 | Ingeniería de datos | Conectar un resultado con el archivo exacto; evitar duplicados y fuga de datos |
| 27 | Software, QA y accesibilidad técnica | Crear una vía de entrega que realmente falle de forma cerrada |
| 28 | MLOps y fiabilidad | Impedir que un cambio de modelo invalide en silencio la evaluación anterior |
| 29 | Privacidad, seguridad y ética | Proteger evidencias; evitar rastreo oculto y afirmaciones engañosas |
| 30 | Producto, ventas y especialistas del negocio | Definir qué mejora importa y comprobar que la colaboración puede ejecutarse |

Advertencia (p.6): un panel formado solo por amigos, diseñadores o seguidores del creador no representa a quienes aprueban presupuestos. Advertencia (p.7): copiar una lista de parámetros de una aplicación interactiva puede introducir filtros irrelevantes en una propuesta documental.

## 6. Fundamentos históricos (sección 7, p.9)

| Origen | Aporte | Traducción correcta |
|---|---|---|
| Gestalt, siglo XX; revisión 2012 [9] | Agrupación y organización figura-fondo | Usar proximidad y alineación para relacionar elementos; no deducir conversión de una retícula |
| Hick, 1952 [5] | Información y tiempo de elección en tareas experimentales | Probar la complejidad de las decisiones; no concluir que toda propuesta debe tener exactamente tres opciones |
| Fitts, 1954 [6] | Movimiento, distancia y tamaño del objetivo | Enlaces utilizables; no convertir la ley en una ecuación de aceptación comercial |
| Miller, 1956; Cowan, 2001 [7, 8] | Capacidad y agrupación de información bajo condiciones definidas | Reducir la necesidad de recordar; 7 más o menos 2 o 4 no son límites universales de páginas o bullets |
| Card, Moran y Newell, 1983 [10] | Modelos de tareas y desempeño humano-computadora | Descomponer acciones observables; un flujo de lectura persuasiva requiere validación adicional |
| Suchman, 1987 [11] | Acción situada y límites de los planes | Observar entorno y relaciones: la lectura real puede interrumpirse o delegarse |
| Norman, 1988 [12] | Comprensibilidad del diseño; intención, acción y respuesta | Que el siguiente paso y sus consecuencias sean claros |
| Sweller, 1988 [41] | Carga cognitiva en aprendizaje y resolución de problemas | Hipótesis de reducción de esfuerzo; transferencia a venta B2B por probar |
| Nielsen y Molich, 1990; Brooke, 1996 [4, 26] | Inspección heurística y usabilidad percibida | Métodos complementarios; ninguno certifica perfección |
| Desmet y Hekkert, 2007; HEART, 2010 [13, 27] | Experiencia afectiva y métricas centradas en objetivos | Separar sensación, significado, tareas y resultados en un conjunto de medidas |

La antigüedad no invalida un hallazgo y la novedad no lo hace superior; los principios conservan su ámbito de aplicación y se revisan frente a tareas, dispositivos y expectativas actuales.

## 7. Evidencia reciente y complementaria

Nivel: E1 metaanálisis, revisión o estudio primario; N norma; E2 manuscrito de autores o fuente comprobada solo por resumen.

| Id | p. | Hallazgo y cifra | Evid. | Límite |
|---|---|---|---|---|
| H-UX-01 | 10 | Schlamann, Nestler y Thielsch (2026), metaanálisis preregistrado: 31 estudios, 234 tamaños de efecto, 18.794 participantes; efecto positivo agregado g = 0,29 de la estética sobre el desempeño, con heterogeneidad alta no explicada. La selección exigía una manipulación estética detectada en las valoraciones | E1 [14] | g no equivale a 29% más ventas; no da una probabilidad de aceptación para un PDF. Solo se comprobó el resumen editorial y el repositorio de datos y código |
| H-UX-02 | 10 | Hertzum (2025), metaanálisis de 144 estudios: la preferencia se relaciona más con menor carga percibida que con tiempo o errores. Solo en 2% de los estudios un sistema preferido imponía una carga significativamente mayor | E1 [15] | Predominan tareas utilitarias; no identifica un diseño ganador para las marcas |
| H-UX-03 | 10 | Hertzum (2026), SUS, metaanálisis de 105 estudios: el sistema con mayor SUS tenía peor desempeño temporal en 24% de los estudios y peor desempeño en errores en 23%; en 10% imponía mayor carga | E1 [17] | Porcentajes de estudios, no de destinatarios comerciales; una valoración de facilidad puede mejorar sin que todas las medidas objetivas mejoren |
| H-UX-04 | 10 | Perrig y colaboradores (2024), revisión de CHI 2019 a 2022: 153 artículos examinados, 60 elegibles, 85 escalas y 172 constructos. Solo 20% justificó completamente la selección de escalas y 36,67% informó alguna evaluación de su calidad | E1 [16] | La popularidad de una escala no corrige un uso inadecuado |
| H-UX-05 | 11 | Scheibehenne, Greifeneder y Todd (2010): 63 condiciones de 50 experimentos, N = 5.036; efecto medio de sobrecarga de opciones prácticamente nulo, D = 0,02 (IC 95% de -0,09 a 0,12) con variación entre estudios. Chernev, Böckenholt y Goodman (2015): 99 observaciones, N = 7.202; moderadores: complejidad, dificultad, incertidumbre de preferencias y objetivo | E1 [18, 19] | No hay una cantidad universalmente óptima de planes |
| H-UX-06 | 11 | Reinecke y Gajos (2014): 2,4 millones de valoraciones de atractivo de sitios de casi 40.000 participantes; diferencias ligadas a antecedentes de los participantes | E1 [20] | Justifica estudiar heterogeneidad; no permite deducir el gusto de una persona por su nacionalidad |
| H-UX-07 | 11 | Lindgaard y colaboradores (2006): juicios de atractivo de páginas web con exposiciones de 50 milisegundos | E1 [21] | Una impresión rápida no demuestra comprensión del precio, memoria posterior ni intención de contratar. La portada debe atraer y dar paso a una tarea completable |
| H-UX-08 | 11 | Camerer y colaboradores (2018): 21 experimentos de ciencias sociales de Nature y Science, 13 con efecto significativo en la dirección original; el efecto de réplica fue aproximadamente la mitad del original | E1 [34] | No representa toda la psicología pero obliga a tratar con cuidado promesas basadas en un estudio famoso |
| H-UX-09 | 12 | Seshadri y colaboradores (2026): simulación frente a participantes de EE. UU., India, Kenia y Nigeria en tareas de agentes de atención comercial. Cambiar el modelo simulador alteró el éxito hasta 9 puntos porcentuales; hubo diferencias de calibración y de patrones de error frente a humanos | E2 [35] (manuscrito v2; registro en ACL 2026) | Entorno de agentes, no de propuestas; justifica limitar la transferencia |
| H-UX-10 | 12 | Zheng y colaboradores: fortalezas y sesgos de usar modelos como evaluadores. Uso propuesto: revisar afirmaciones o localizar problemas con rúbrica y ejemplos de referencia | E1 [36] | No convertir el acuerdo entre modelos en validación humana independiente |
| H-UX-11 | 12 | DeepGaze IIE: modelado de saliencia con calibración dentro y fuera del dominio | E1 [37] | Una predicción de fijaciones no mide comprensión, deseo, confianza, emoción ni compra. Los mapas de calor del cursor no son eye tracking |
| H-UX-12 | 12 | Normas verificadas: ISO 9241-210:2019 (confirmada en 2025); WCAG 2.2 (recomendación de diciembre de 2024); WCAG 3.0 (Working Draft de 10 de septiembre de 2026); PDF/UA-2, ISO 14289-2:2024 | N [1, 22, 40, 25] | WCAG 3.0 es borrador, no estándar final. Un escáner no verifica todo. La accesibilidad del PDF exige estructura semántica |

Implicación de diseño (p.10): mantener un perfil de medidas separado. Un diseño atractivo no compensa un precio incomprensible; una lectura rápida no compensa condiciones mal entendidas; una puntuación de facilidad no prueba eficacia comercial. Cómo debe usar el motor un hallazgo (p.11): registrar qué se manipuló, qué se midió, en qué población, el tamaño del efecto y la incertidumbre; formular una hipótesis local; diseñar una prueba; actualizar la decisión con su resultado. Evidencia sobre supermercados, pacientes o sitios web puede orientar una hipótesis sobre propuestas B2B, pero no da su efecto.

## 8. Hallazgos menos obvios (sección 11, p.13)

| Idea tentadora | Criterio defendible |
|---|---|
| Más tiempo de lectura siempre es mejor | Puede ser interés o confusión: interpretarlo junto con comprensión y tarea completada |
| La propuesta con más clics tiene mejor UX | Los clics pueden venir de curiosidad, errores o búsqueda fallida; medir si acercan a una decisión informada |
| Un score de 95 implica 95% de éxito | Una rúbrica y una probabilidad son objetos distintos; prohibir esa conversión sin modelo validado |
| Cinco usuarios garantizan encontrar casi todo | Las rondas pequeñas sirven para descubrir; no certifican ausencia de fallos ni precisión poblacional [3] |
| La ciencia dice qué color vende más | El color opera en un contexto de marca, contraste y población; las tendencias no son ensayos de conversión [20] |
| Si la IA imita a un dueño, ya fue probado | La simulación es fuente de hipótesis y pruebas de software, no una muestra humana [35] |
| La unanimidad de expertos elimina la incertidumbre | Pueden compartir sesgos; registrar discrepancias y contrastar con tareas reales [4] |
| Cuantos más filtros, mejor | Un filtro inválido puede bloquear buenos diseños; medir falsos bloqueos y defectos que escapan |
| Pasó QA, no tiene errores | Pasó lo que QA pudo comprobar en esas condiciones; deben constar cobertura, versión y límites [24] |
| Millones de variables revelan todos los patrones | Sin resultados pertinentes aumentan las posibilidades de sobreajuste; la validación decide qué complejidad aporta [29] |

El avance competitivo más defendible es reunir mejores evidencias propias y ejecutar decisiones trazables, incluso cuando la conclusión sea todavía no sabemos.

## 9. Definir la experiencia, métricas y pruebas con personas (secciones 12 a 15, pp.14 a 17)

### 9.1 Unidad de análisis y recorrido (p.14)

La unidad de análisis es una persona haciendo una tarea. Usuario primario: quien evalúa o aprueba una colaboración (dueño, gerente, responsable de marketing, agencia o socio). Los espectadores del contenido son otra población; los datos de retención de un Reel no miden la facilidad con que una marca entiende la propuesta.

| Momento | Tarea observable | Fallo relevante |
|---|---|---|
| Recepción | Reconocer quién escribe y decidir abrir | Remitente o asunto confuso; archivo que no se puede abrir |
| Orientación | Entender qué idea se propone y para qué marca | Promesa genérica o producto equivocado |
| Evaluación | Encontrar entregables y comprobar evidencias | Contenido ambiguo o enlaces que llevan a otra pieza |
| Decisión | Identificar inversión, responsabilidades y siguiente paso | Confundir tarifa con consumo o no saber cómo responder |
| Consulta interna | Compartir y explicar el acuerdo a otra persona | Condiciones dispersas o dependencia del autor para entenderlo |
| Ejecución y continuidad | Cumplir lo acordado y evaluar renovación | Aceptación inicial que termina en cambios, decepción o conflicto |

Objetivos propuestos, en orden: 1 requisitos mínimos (veracidad, coherencia comercial, acceso al contenido, ausencia de defectos bloqueantes); 2 resultado UX (decisión informada con esfuerzo razonable y comprensión correcta); 3 resultado comercial (colaboración viable, margen y continuidad). Los pesos entre objetivos deben ser explícitos y revisables. Ventanas de registro de 14, 30 y 90 días para respuesta, contratación y ejecución o renovación: decisiones iniciales de diseño, no plazos científicos.

### 9.2 Métricas (p.15)

| Dimensión | Medida propuesta | Límite |
|---|---|---|
| Comprensión | Respuestas correctas sobre entregables, importe, moneda, consumo y siguiente paso | Criterio primario de tarea; definir la respuesta correcta antes del estudio |
| Encontrabilidad | Tiempo hasta localizar precio, evidencia o contacto; éxito con o sin ayuda | Comparar tareas equivalentes; no penalizar la deliberación razonada |
| Esfuerzo | Valoración posterior a la tarea y, si procede, NASA-TLX | Autoinforme; no es lectura objetiva de la mente |
| Atractivo | Preferencia entre variantes y valoración visual separada | Contrabalancear orden y ocultar autoría cuando sea viable |
| Confianza informada | Qué evidencia considera creíble y qué dudas quedan | Una puntuación sola no sustituye explicación ni comprobación de hechos |
| Accesibilidad | Tareas con lector de pantalla, zoom y acceso a enlaces | Complementar inspección semántica y revisión manual |
| Conversión | Aceptaciones definidas dividido entre oportunidades asignadas elegibles | No confundir con apertura, respuesta o aceptación del diseño por Eduardo |
| Calidad posterior | Cambios de condiciones, cancelaciones, entrega, renovación y margen | Una conversión temprana puede ocultar una experiencia posterior negativa |
| Calidad del filtro | Defectos omitidos, falsos bloqueos, cobertura y tiempo de revisión | El verificador se evalúa como un producto propio |

En un PDF por correo o mensajería normalmente no se observa de forma fiable cuánto se leyó ni el recorrido entre páginas: no inventar telemetría. Si se usa un visor instrumentado, validar eventos, permisos y limitaciones; los accesos de bots o previsualizadores no prueban lectura humana. HEART parte de objetivos, luego señales y métricas; no forzar métricas de adopción o retención diaria propias de aplicaciones en una propuesta de contacto único.

### 9.3 Pruebas con personas (p.16)

- Reclutamiento: perfiles que realmente revisen presupuestos de colaboración; cubrir los contextos iniciales de España y Venezuela, la familiaridad con creadores, distintos tamaños de negocio y las condiciones de lectura prioritarias. No usar país ni edad para asignar preferencias sin observarlas.
- Descubrimiento: rondas de 5 a 8 personas por contexto prioritario, corregir y volver a probar. Es una decisión de trabajo, no una garantía de cobertura ni tamaño suficiente para un A/B comercial [3].
- Tareas sin inducir la respuesta, ejemplos del estudio: explícame qué se está proponiendo; qué recibiría tu negocio; cuánto pagaría y qué más aportaría; comprueba un ejemplo; si quisieras avanzar, qué harías. Evitar: ves qué clara y premium está.
- Observación: éxito, errores, petición de ayuda, dudas, tiempo, lectura del precio y navegación. Si se mide tiempo natural, separarlo del pensamiento en voz alta, que puede modificar la ejecución.
- Comparación: dos variantes con contenido comercial equivalente; contrabalancear el orden, controlar aprendizaje, mismo dispositivo o asignado por diseño; preguntar preferencia después de las tareas.
- Salida de cada ronda: incidentes con ubicación, evidencia, gravedad, población afectada, hipótesis de causa, corrección propuesta y comprobación posterior. Un resumen como gustó mucho no es evidencia suficiente.
- Objetivos iniciales del piloto (a validar): cero errores críticos observados de precio, moneda o entregables; comprensión correcta de las cinco condiciones centrales; capacidad de completar el siguiente paso sin ayuda. Los tamaños de muestra e intervalos determinan cuánto se puede generalizar.
- No hace falta un panel nuevo por cada cambio de nombre o foto: las pruebas cubren familias de diseños y contextos con vigencia y alcance declarados. Cambios sustanciales de estructura, oferta, idioma o audiencia activan una nueva evaluación.

### 9.4 Escalas y validez (p.17)

SUS: 10 ítems, puntuación de 0 a 100, no es un porcentaje de éxito; se administra tras interactuar; cambiar palabras no basta para declarar que conserva validez; un umbral como 80 sería una meta interna [26]. UEQ: distingue atractivo y dimensiones pragmáticas y hedónicas; usar versión lingüística documentada; si ciertos ítems no encajan con un documento estático, justificar otro instrumento o validar la adaptación; no rellenar respuestas como si el modelo fuera un humano [42]. NASA-TLX: carga subjetiva en seis dimensiones; registrar si se usa el procedimiento ponderado o sin ponderar; puede ser excesivo para una tarea breve [28].

Controles psicométricos: constructo (qué significa comprensión, confianza o atractivo y qué queda fuera); instrumento (origen, idioma, versión, ítems, escala, regla de puntuación); adaptación (cambios y evidencia de que miden lo previsto); fiabilidad (un alfa alto no demuestra validez); validez (relación con tareas y criterios externos, estructura, sesgo de respuesta); comparación entre grupos (comparabilidad antes de atribuir diferencias a país o público); carga de investigación (pocas medidas relevantes). Las preguntas propias sobre precio y entregables son pruebas de comprensión de contenido específico y deben llamarse así [16].

## 10. Datos y metadatos (sección 16, p.18)

| Entidad | Campos esenciales propuestos |
|---|---|
| Propuesta | proposal_id, versión, fecha, marca, país, ciudad, idioma, objetivo, precio, moneda, responsabilidades, oferta confirmada |
| Archivo y diseño | Hash del PDF final, plantilla o familia, estructura, fuentes, imágenes y origen, enlaces, tamaño, renderer y versión del generador |
| Afirmaciones | Texto o identificador, fuente, fecha consultada, ubicación, permiso de uso si procede, tipo: dato, inferencia o supuesto |
| Estudio UX | study_id, protocolo, tareas, reclutamiento, dispositivo, contexto, consentimiento, criterios, desviaciones, evidencia anonimizada |
| Observación | Participante seudónimo, variante asignada, orden, respuestas, errores, tiempos, medidas, datos ausentes |
| Oportunidad comercial | Empresa o grupo decisor, relación previa, canal, fechas, asignación, cambios de oferta, seguimiento |
| Resultado | Respuesta, aceptación al precio original, negociación, rechazo, pendiente, fecha, motivo conocido, resultado de ejecución |
| Evaluación | rule_id, versión, estado, evidencia, gravedad, evaluador, fecha, hash inspeccionado, motivo de no aplicabilidad |
| Modelo | Versión de datos, variables disponibles al decidir, particiones, algoritmo, calibración, métricas, ámbito de validez |

Reglas de calidad del dato: una fila de resultado representa una oportunidad definida, no cada página, lectura o mensaje de seguimiento; varias personas de la misma empresa requieren agrupar la dependencia; un aprobado de Eduardo valida su preferencia interna, no la contratación de la marca. Distinguir sin respuesta a 30 días de rechazo explícito y de expediente pendiente con solo tres días de observación; los resultados tardíos exigen actualizar el estado o análisis de tiempo hasta evento; nunca completar razones desconocidas con intuiciones del modelo. Metadatos son datos sobre origen, contexto y procesamiento; metaanálisis es síntesis estadística de estudios; ninguno crea por sí mismo observaciones de los destinatarios. No se incorporó una base verificada de 742.137 propuestas ni de millones de marcas.

## 11. Arquitectura y control de liberación (secciones 17 y 21, pp.19 y 23)

Diez capas: 1 especificación versionada (reglas del usuario, requisitos del caso, catálogo de comprobaciones aplicables); 2 registro de evidencia; 3 generación de alternativas (no puede modificar la política que lo evaluará); 4 verificación determinista (campos, reglas exactas, integridad de archivo, enlaces, geometría); 5 inspección multimodal (páginas renderizadas, OCR, contradicciones texto-imagen); 6 evaluación experta y humana; 7 predicción calibrada; 8 selección de alternativa (solo entre candidatos admisibles); 9 control de liberación (permiso ligado al archivo exacto); 10 seguimiento y aprendizaje.

Tres salidas centrales: estado de conformidad, perfil UX y estimación comercial. Si falta evidencia predictiva, la tercera dice no estimable de forma validada; las dos primeras siguen siendo útiles sin fabricar probabilidades. La recuperación de evidencia con embeddings no convierte similitud en causalidad. Las evaluaciones generadas por IA se guardan como juicios asistidos, separadas de observaciones humanas. NIST AI RMF aporta estructura de gobierno y medición de riesgos [33]; no certifica esta arquitectura.

Control obligatorio (p.23): una instrucción textual como revisa todo antes de entregar ayuda pero no impone control de acceso. El generador escribe solo en borradores y un componente independiente autoriza el envío del archivo cuyo hash se evaluó. Contrato mínimo de cada comprobación: identidad (rule_id, policy_version), aplicabilidad, método, estado (PASS, FAIL, REVIEW, MISSING, ERROR, NOT_APPLICABLE), evidencia (brief, página, fragmento, hash, versión del verificador), responsable, validez (solo para el hash y la política registrados; evidencias externas con vigencia definida). Lógica de liberación: congelar brief, reglas y archivo candidato; calcular qué pruebas corresponden; ejecutarlas y comprobar que sus evidencias existen; resolver revisiones requeridas; bloquear si falta algo o queda un fallo; emitir un permiso verificable ligado al hash del PDF y de la política; la vía de entrega compara ambos antes de dejar salir. El generador no puede alterar resultados ni fabricar firmas; los fallos de verificador, timeout, OCR o renderer nunca cuentan como aprobado; trazabilidad del responsable y protección contra reutilizar un informe anterior para un archivo modificado. Límites: no impide que alguien descargue un borrador y lo envíe por una vía externa; no elimina errores desconocidos del propio verificador.

## 12. Catálogo de 33 filtros (secciones 18 a 20, pp.20 a 22)

Tipos: B bloquea ante incumplimiento o falta de prueba crítica; R exige revisión documentada. Toda regla necesita responsable y una forma de comprobarse. Es un catálogo inicial de familias de comprobación: al implementarlo deben desglosarse y vincularse con cada requisito aplicable; una regla sin implementación o evidencia permanece pendiente.

### 12.1 Filtros A: contenido, hechos y condiciones comerciales (p.20)

| ID | Tipo | Criterio | Prueba exigida |
|---|---|---|---|
| C01 | B | Marca, país, precio y moneda confirmados | Comparar la solicitud autoritativa con los datos y el PDF final; cero valores heredados sin confirmación |
| C02 | B | Responsabilidades y entregables coherentes | Según el encargo y las reglas vigentes |
| C03 | B | Inversión localizada correctamente | Tarifa solo en el módulo de inversión; distinguir precios de carta y cifras de evidencia |
| C04 | B | Afirmaciones y cifras trazables | Fuente y fecha para visualizaciones, premios, sede, producto o cualquier afirmación factual |
| C05 | B | Tres evidencias del grupo correcto | Identidad de cada vídeo, imagen y cifra; enlace correspondiente y set autorizado |
| C06 | B | No atribuir a la marca un producto ajeno | Procedencia de la imagen y relación con el texto; no presentar una referencia como plato exacto |
| C07 | B | Condiciones económicas sin contradicción | Importe, divisa, netos o BCV según el caso; no inferir obligaciones nuevas |
| C08 | B | CTA realizable y claro | Canal real, acción identificable, ausencia de enlaces ficticios |
| C09 | B | Ausencia de contenido prohibido por encargo | Sin QR ni fotos generadas o de Instagram para producto; excepciones expresas como logo |
| C10 | R | Idea y argumento comercial pertinentes | Activo real de la marca, beneficio concreto y relación con la ejecución propuesta |

La puntuación comercial nunca compensa C01 a C09. Si el CTA lleva a un recurso que exige iniciar sesión o que no se puede comprobar, queda como revisión pendiente: una respuesta HTTP por sí sola no demuestra que el destino funciona para el receptor. Cada afirmación de derechos, acceso o procedencia se apoya en evidencia; una etiqueta automática real=True no resuelve la incertidumbre; la ausencia de créditos se logra eligiendo activos compatibles con ese uso, no suponiendo permisos.

### 12.2 Filtros B: calidad del archivo y acceso al contenido (p.21)

| ID | Tipo | Criterio | Prueba sobre la versión final |
|---|---|---|---|
| V01 | B | Archivo íntegro y texto disponible | Abrir, renderizar y extraer contenido; verificar glifos, números y fuentes |
| V02 | B | Cero solapamientos dañinos | Texto con texto, caja, imagen, líneas y bordes: geometría más lectura del render |
| V03 | B | Contraste suficiente | Normal 4,5 a 1 y grande 3 a 1 según condiciones aplicables; revisar el fondo real bajo el texto [22] |
| V04 | B | Legibilidad en el contexto de lectura | Prueba en visores y teléfonos previstos; el tamaño tipográfico del archivo no basta |
| V05 | B | Imágenes y logos conformes al encargo | Píxeles nativos, tamaño de colocación, recorte y fidelidad visual; ampliar no crea detalle nativo |
| V06 | B | Enlaces correctos y utilizables | Destino real, rectángulo clicable, orden y acceso en dispositivos previstos |
| V07 | R | Jerarquía y orden coherentes | Título, evidencia y precio se encuentran sin competir; lectura comprobada |
| V08 | R | Espacios y divisores funcionales | Respiración deliberada y retícula consistente; cero huecos accidentales ni líneas que crucen contenido |
| V09 | B | Estructura accesible cuando se exige | Etiquetas, orden semántico, idioma, alternativas y validación manual; declarar alcance [23 a 25] |
| V10 | R | Identidad propia con patrón comprensible | Evaluar concepto y tratamiento; no penalizar por compartir convenciones útiles |
| V11 | B | El archivo entregado es el revisado | Hash idéntico al evaluado; cualquier edición posterior invalida el permiso |
| V12 | R | Peso compatible con canal y contexto | Presupuesto de bytes fijado antes de exportar; revisar compresión y apertura real |

Nota (p.21): para una web el mínimo WCAG 2.2 de ciertos objetivos de puntero es 24 por 24 píxeles CSS con excepciones; no se convierte automáticamente a 24 puntos en un PDF (tamaño de página, zoom y visor cambian el área efectiva).

### 12.3 Filtros C: evidencia y liberación (p.22)

| ID | Tipo | Condición | Tratamiento del incumplimiento |
|---|---|---|---|
| E01 | B | Protocolo UX aplicable vigente | Bloquear si una nueva familia de diseño o población exige prueba y todavía no existe |
| E02 | B | Sin incidentes críticos abiertos | Corregir y revalidar; una firma no transforma un error material en cumplimiento |
| E03 | R | Comprensión y esfuerzo dentro de objetivos | Comparar con la línea base y mostrar tamaño de muestra e incertidumbre |
| E04 | B | Medidas y etiquetas consistentes | Invalidar conclusiones que mezclan entrevistas, simulación o aceptación de Eduardo con contratación |
| P01 | B para predecir | Modelo validado para el uso | Retirar la probabilidad; se puede evaluar por reglas si la política permite modo sin predicción |
| P02 | B para predecir | Entrada dentro del ámbito aceptable | Abstenerse ante datos faltantes relevantes o cambio importante de contexto |
| P03 | B para predecir | Probabilidades calibradas y evaluadas fuera de muestra | No publicar porcentaje de éxito a partir de una puntuación experta |
| P04 | R | Comparación robusta de alternativas | Si la elección cambia con supuestos plausibles, declarar incertidumbre y priorizar prueba |
| L01 | B | Todas las reglas aplicables satisfechas | FAIL, ERROR, MISSING o REVIEW pendiente impiden liberar |
| L02 | B | Evidencia vigente y ligada a archivo y política | El cambio de archivo o de requisitos anula la evaluación anterior |
| L03 | B | Vía de entrega bajo control | No permitir exportación al cliente por rutas que omitan el permiso de liberación |

Cómo evitar un bloqueo eterno por no tener predictor: definir desde el inicio dos políticas explícitas: entrega con conformidad y revisión UX, y entrega con predicción validada adicional. P01 a P03 son obligatorios para afirmar probabilidades, no para fingir que no se puede mejorar nada hasta reunir miles de resultados. El modo seleccionado aparece en la auditoría interna. Cambiar una regla exige versionar la política y revalidar. NOT_APPLICABLE necesita una razón comprobable y no sustituye una prueba pendiente.

## 13. Probar el verificador (sección 22, p.24)

Antes de usarlo como barrera de salida se necesita un banco de casos correctos y defectuosos anotados por revisores competentes, con errores históricos del creador y casos que obliguen a distinguir un defecto de una decisión visual válida.

| Familia de prueba | Ejemplos que debe resolver |
|---|---|
| Semántica comercial | Moneda equivocada; precio contradictorio; confundir visualizaciones con tarifa; consumo sin definir |
| Geometría y renderizado | Texto tapado por caja; acento cortado; línea sobre postre; tipografía sustituida; capas invisibles |
| Evidencia y vínculos | Miniatura correcta con vídeo equivocado; enlace roto; cifras de fechas distintas; captura alterada |
| Integración | Archivo cambiado después del PASS; auditoría ausente; regla nueva; renderer caído; datos incompletos |
| Accesibilidad | Orden de lectura incorrecto pese a buena apariencia; CTA visual sin vínculo; imagen esencial sin alternativa |
| Falsos positivos | Espacio intencional; foto de referencia usada correctamente; cifra de menú igual a la tarifa; nombre propio exento |
| Contenido no confiable | Texto en una web o documento que instruye al evaluador a ignorar reglas o a inventar un PASS |

Métricas internas a publicar: sensibilidad por gravedad (fracción de defectos conocidos que detecta), precisión (cuántos bloqueos son errores reales), falsa liberación (proporción de documentos defectuosos que pasan), falso bloqueo (correctos retenidos), cobertura (pruebas aplicables completadas con su calidad de evidencia). Objetivo inicial: bloquear todos los defectos críticos del banco de aceptación y no dejar revisiones pendientes; alcanzarlo significa superar ese banco, no cero defectos en el mundo. El conjunto de prueba final permanece separado de los ejemplos usados para ajustar el motor. La revisión visual automática no se evalúa con etiquetas creadas solo por el mismo modelo: incluir desacuerdos entre personas, adjudicación y evidencia renderizada [4, 24].

## 14. Modelos, predicción y estadística (secciones 23 a 25, pp.25 a 27)

### 14.1 Modelos candidatos (p.25)

| Familia | Uso razonable | Límite principal |
|---|---|---|
| Reglas deterministas | Cumplimiento exacto, integridad y validación comercial | No predicen experiencia humana ni detectan toda ambigüedad |
| Tasas base y beta-binomial | Referencia simple y actualización por resultados | Pocos casos dan intervalos amplios; agrupaciones pequeñas son inestables |
| Regresión regularizada | Relación interpretable entre pocas variables y el resultado | Forma funcional limitada; correlación no implica efecto de cambiar una variable |
| Modelo bayesiano jerárquico | Compartir información entre países, tipos de negocio o formatos | Los supuestos y priors importan; no rescata datos sin pertinencia |
| Gradient boosting tabular | Relaciones no lineales con volumen y variedad suficientes | Sobreajuste, cambio de distribución, necesidad de calibración |
| Supervivencia y riesgos competitivos | Tiempo hasta respuesta, aceptación o rechazo y expedientes incompletos | Requiere fechas, seguimiento y supuestos adecuados sobre censura |
| Texto, visión y embeddings | Representar contenido y diseño, recuperar comparables, detectar anomalías | Alta dimensión, sesgos, similitud engañosa |
| Modelos causales y uplift | Efecto diferencial de variantes con datos de intervención adecuados | Necesitan identificación causal; no basta historial seleccionado |
| Bandits y optimización bayesiana | Aprender entre alternativas admisibles y gestionar exploración | La asignación adaptativa complica la inferencia; exige registrar probabilidades y resultados |
| Predicción conforme | Conjuntos o intervalos con cobertura bajo supuestos | Cobertura marginal no es certeza individual; los cambios de distribución pueden invalidarla [32] |

Para empezar: comparar reglas y tasas base con un modelo pequeño regularizado o jerárquico; la complejidad entra solo si mejora validación, estabilidad y coste de decisión. No hace falta entrenar un modelo fundacional propio.

### 14.2 Predicción y decisión (p.26)

- Estimando definido, por ejemplo: probabilidad de aceptación al precio original en 30 días, para una nueva oportunidad elegible de un contexto especificado, usando solo información disponible antes del envío. Cambiar plazo, definición de aceptación o población cambia el problema.
- Modelo ilustrativo no entrenado: logit(p) = intercepto + efecto de contexto + efecto de tipo de negocio + coeficientes de características disponibles antes del envío. Los coeficientes se estiman con resultados y regularización; no se inventan.
- No incorporar como predictor una negociación posterior, el número de seguimientos futuro ni otra señal que revele el resultado.
- Evaluación: probabilidad de aceptación con Brier o log loss, comparación con la tasa base y gráfico de calibración (la AUC mide discriminación, no calibración); intervalo explicando si cubre parámetros, una tasa poblacional o un resultado futuro; elección entre variantes comparando objetivos bajo restricciones, incertidumbre y coste; el efecto de modificar el diseño exige experimento o identificación causal válida.
- La calibración se aprende con datos separados del ajuste y se revisa por contexto; la validación final no se reutiliza para escoger continuamente al ganador [29, 31]. La decisión puede ser A y B son indistinguibles con la evidencia actual; elegir A por menor coste o riesgo es una decisión explícita, no una superioridad estadística inventada.

### 14.3 Potencia y muestra (p.27)

Dos proporciones independientes, 1 a 1, bilateral, alfa 0,05, potencia 80%, fórmula normal. No son tasas actuales del creador.

| Escenario hipotético | Mejora absoluta | Muestra por variante | Total |
|---|---|---|---|
| Aceptación 20% a 25% | 5 puntos | 1.094 | 2.188 |
| Aceptación 20% a 30% | 10 puntos | 294 | 588 |
| Aceptación 50% a 55% | 5 puntos | 1.565 | 3.130 |
| Comprensión 80% a 90% | 10 puntos | 199 | 398 |

Fórmula: n aproximado = [z(0,975) raíz(2 pbar (1 - pbar)) + z(0,80) raíz(p0 (1 - p0) + p1 (1 - p1))] al cuadrado dividido entre (p1 - p0) al cuadrado, con pbar = (p0 + p1) / 2; redondeo hacia arriba. Omite pérdidas, agrupación por empresa, multiplicidad y desviaciones de ejecución, que pueden aumentar la muestra.

Cero fallos observados no significa riesgo cero: bajo ensayos Bernoulli independientes y representativos, con 0 fallos en n casos, el límite superior unilateral exacto de 95% para la tasa de fallo es 1 - 0,05 elevado a 1/n. Con 5 casos es aproximadamente 45,1%; con 30, 9,5%; con 100, 3,0%; con 300, 1,0%. Un banco de errores construido artificialmente no representa la prevalencia real.

Tres tamaños distintos: descubrir problemas, estimar una tasa con precisión y detectar una mejora entre variantes requieren diseños distintos; desarrollar un predictor añade otro problema (parámetros, prevalencia, rendimiento esperado; Riley y colaboradores [30], sin importar umbrales clínicos). Quince resultados permiten iniciar un registro y actualizar una tasa con incertidumbre, pero no demostrar probabilidades personalizadas fiables por país, producto y precio; contar páginas, visitas o simulaciones como oportunidades independientes daría una precisión ficticia.

## 15. Experimento de campo y criterio de liderazgo (secciones 26 y 27, pp.28 a 29)

Experimento (p.28): línea base = proceso vigente y sus mejores propuestas aprobadas; tratamiento = mismo encargo atendido con los filtros y la selección propuestos; mantener oferta, precio y seguimiento equivalentes cuando se quiera atribuir el efecto al diseño, o declarar que se evalúa el paquete completo. Aleatorizar por oportunidad o empresa, antes del envío; evitar que una empresa reciba variantes rivales o que cada equipo elija los clientes más favorables; estratificar sin crear decenas de grupos vacíos. Preregistrar hipótesis, resultado principal, diferencia mínima relevante, horizonte, muestra, exclusiones, métricas de protección y regla de parada; no detener al primer p menor de 0,05 (usar diseño secuencial válido si se mira repetidamente). Verificar ejecución: asignación, duplicados, entregabilidad, desbalances; Microsoft documenta cómo los errores de métricas y el Sample Ratio Mismatch invalidan conclusiones convincentes [38, 39]. Analizar como se asignó; evitar analizar solo a quienes abrieron o respondieron (selección posterior al tratamiento). Reportar utilidad práctica: diferencia absoluta y relativa, intervalo, costes, margen, comprensión, cancelaciones y resultados por contexto; un resultado no significativo no demuestra igualdad. Si el volumen no permite detectar mejoras pequeñas: estudios de comprensión para eliminar fricciones claras, hipótesis comerciales prudentes y acumular evidencia; el control de calidad sigue aportando valor. Antes de generalizar a nuevos países o tipos de negocio, repetir la validación externa: una mejora en propuestas de restaurantes españoles no prueba que funcione igual en automoción venezolana.

| Dimensión | Prueba propuesta para llamarlo superior (p.29) |
|---|---|
| Cumplimiento | Mismo banco ciego de propuestas correctas y defectuosas, jueces independientes y gravedad fijada |
| Experiencia | Mismas tareas y participantes comparables; comprensión, esfuerzo, acceso y preferencia por separado |
| Predicción | Prueba temporal intacta y empresas fuera de entrenamiento; tasas base y modelos sencillos como referencias |
| Resultado comercial | Experimento prospectivo frente al sistema vigente y otros métodos relevantes |
| Generalización | Resultados por contexto, dispositivo, idioma y tipo de oferta; no ocultar segmentos donde falla |
| Eficiencia | Tiempo humano, coste por propuesta, latencia, falsos bloqueos y mantenimiento |
| Transparencia | Protocolo, versiones, exclusiones, incertidumbre y documentación para reproducir |

Controles contra una evaluación complaciente: separar datos por empresa, periodo y familias de propuestas; no poner casi duplicados en entrenamiento y prueba; mantener un conjunto prospectivo que no haya influido en reglas, prompts ni selección de modelos (Cawley y Talbot [29]). Evaluación externa útil: motor completo frente al proceso actual, una revisión humana experta, reglas automáticas sencillas y un modelo genérico con recursos comparables; ablaciones para medir lo que aporta cada componente (más módulos no implica más mejora). Afirmación defendible: superó a los sistemas A y B en estas tareas, poblaciones, métricas y fechas; no es defendible transformarla en domina toda la UX o es el mejor del mundo sin ámbito definido.

## 16. Aplicación al sistema del creador y ejemplo de funcionamiento (secciones 28 y 29, pp.30 a 31)

El estudio revisó el texto del Documento Maestro del kit anterior (identificado como v4.3 del 25/09/2026, 27 páginas): analizó la especificación, no ejecutó ni auditó su implementación. Tratamiento recomendado, en genérico (descripción de segunda mano; el kit no se copia al repositorio):

| Elemento del kit | Tratamiento recomendado por el estudio |
|---|---|
| Barrera de cero fallos con QA geométrico y revisión visual | Conservar como barrera; añadir evidencia por regla y validación del archivo final; no llamarlo ausencia absoluta de defectos |
| Precio solo en el módulo de inversión, país y moneda del encargo | Conservar como requisitos comerciales propios; no presentarlos como leyes universales de conversión |
| Fotos reales, tres evidencias y enlaces correctos | Conservar la trazabilidad; identidad y procedencia no se verifican con un booleano autodeclarado |
| Aprendizaje segmentado con 15 resultados | Tratarlo como comienzo de actualización exploratoria; exigir validación y calibración antes de afirmar precisión |
| Pesos fijos de juicio y técnica para puntuar el antojo | Son una regla de diseño del kit; no equivalen a coeficientes científicos ni a medición de deseo humano |
| Paleta de tendencia, 60/30/10 y tipografías | Conservar si son requisitos creativos vigentes; el beneficio comercial local debe medirse; no atribuir eficacia al prestigio de una tendencia |
| Texto mínimo de 8 pt y revisión al 50% | No basta para legibilidad móvil; probar tamaño efectivo en el visor y comprensión; resolver conflictos de espacio sin encoger información crítica |
| Puerta de independencia creativa | Mantener identidad propia; distinguir copia de concepto de convenciones útiles de lectura; no variar por variar a costa de la comprensión |
| Sin huecos y divisores con respiración | Conservar la intención visual; diferenciar hueco accidental de espacio que ayuda a agrupar y leer |
| Analogías con motores de grandes empresas | Exigir comparación real; usar la misma familia matemática no implica igual eficacia, datos ni infraestructura |

Estas recomendaciones no reescriben las reglas aprobadas: proponen una capa adicional de evidencia y controles y señalan qué afirmaciones técnicas necesitan demostración antes de ser garantías.

Ejemplo (p.31), escenario ficticio: restaurante de España, tarifa confirmada de 350 euros, consumo a cargo del restaurante, entregables definidos y grupo europeo de tres evidencias. Diseño A muestra 350 dólares aunque el brief dice euros: FAIL C01 y C07, bloqueo, corregir moneda y revalidar el archivo completo. Diseño B corrige la moneda pero el tercer enlace pertenece a otro vídeo: FAIL C05, bloqueo, identificar la pieza y comprobar el destino. Diseño C resuelve los enlaces pero una caja tapa parcialmente la cifra: FAIL V02, bloqueo aunque el texto extraído siga mostrando la tarifa. Diseño D corrige lo anterior pero usa una estructura nueva sin evidencia UX aplicable: MISSING E01, hacer la revisión o estudio exigido por la política de esa familia. Versión final cumple controles y revisiones, predictor comercial no validado: APTO en modo sin predicción; entregar si la política elegida lo permite; no adjuntar una probabilidad inventada. Si dos variantes admisibles compiten, se comparan comprensión, facilidad, atractivo y coste; la que gusta más no gana automáticamente si induce más errores de condiciones; sin diferencia concluyente se conserva la incertidumbre y puede elegirse la más sencilla de producir o la más consistente con la marca. Salida interna mínima: archivo y hash, versión de política, modo, pruebas realizadas, fallos abiertos, revisiones, alcance de la evidencia humana, predicción disponible o no, motivo de elección y próximos datos necesarios; ninguna nota global sustituye ese registro.

## 17. Puesta en marcha y mantenimiento (secciones 30 y 31, pp.32 a 33)

| Fase | Trabajo | Se avanza cuando |
|---|---|---|
| 1 Contrato y línea base | Consolidar reglas v4.3, ejemplos aprobados, defectos históricos y definiciones de resultado | Cada requisito tiene origen, prueba, responsable y aplicabilidad |
| 2 Control técnico | Validadores, renderizado, informe de evidencia y permiso de entrega ligado al hash | Pasa el banco de aceptación y se demuestra que las rutas inválidas quedan bloqueadas |
| 3 Investigación inicial | Probar comprensión, precio, entregables y CTA en contextos prioritarios | Se corrigen incidentes críticos y se documenta qué familias de diseño cubre la evidencia |
| 4 Registro prospectivo | Guardar oportunidades, asignaciones, seguimiento y resultados reales | Hay etiquetas consistentes y se distinguen rechazo, negociación y pendientes |
| 5 Predicción en observación | Comparar modelos pequeños y bases sin que decidan envíos | Superan referencias con calibración y utilidad suficientes en datos separados |
| 6 Experimento comercial | Comparar proceso nuevo y vigente con diseño y muestra adecuados | Se sostiene mejora útil sin deterioro de comprensión, operación o margen |
| 7 Escala y vigilancia | Nuevos contextos, deriva, incidentes y reversión | Cada expansión conserva evidencia y posibilidad de retirar predicciones no fiables |

Equipo mínimo por competencias: dirección de investigación, diseño editorial y de contenido, ingeniería de validación y datos y experimentos, con revisión de accesibilidad y de negocio; quien genera no debe ser la única fuente de validación. No se fija precio ni calendario: el coste se presupuesta como horas de investigación y revisión, captación de participantes, ingeniería, infraestructura y mantenimiento; el cómputo puede costar menos que conseguir resultados fiables.

Mantenimiento: versiones controladas (congelar reglas, rúbricas, modelos, prompts, datos y renderizador de cada entrega; reentrenar no autoriza a promover); incidentes como evidencia (clasificar cada corrección de Eduardo como regla comercial, defecto de implementación, criterio creativo, barrera UX o preferencia personal; convertir lo verificable en caso de prueba sin transformar cada preferencia aislada en ley psicológica); vigencia de la evidencia (revisar fuentes, enlaces, ofertas y documentos según su volatilidad; revisar mediciones y calibración al cambiar cliente, formato, idioma, precio, canal o proporción de resultados); abstención y reversión (suspender predicciones si faltan variables clave, se deteriora la calibración o hay entradas sin precedentes; conservar un proceso válido de reglas y revisión); aprendizaje seguro (explorar solo entre alternativas que ya cumplen el mínimo; registrar probabilidades de asignación en un bandit; evaluación independiente); privacidad proporcional (solo los datos necesarios; seudonimizar, limitar acceso y retención, documentar permisos de grabación o instrumentación; revisión por jurisdicción para obligaciones legales). La mejora continua se demuestra con una serie de resultados, no con el número de reglas añadidas; un modelo más sencillo con menos datos sensibles, menos falsos bloqueos o menos esfuerzo humano puede ser mejor.

Qué queda sin demostrar (p.34): la capacidad real del kit actual para aplicar cada regla, la tasa de defectos que deja pasar, la experiencia de los destinatarios, la calidad de un predictor de contratación y el aumento de aceptación frente al proceso actual; no se ejecutaron pruebas con personas ni se hizo una nueva síntesis estadística de datos crudos.

## 18. Referencias (pp.35 a 40)

44 fuentes con nivel de acceso declarado (fecha de consulta 26/09/2026; consultado no significa reanalizado ni reproducido). Resumen: [1] ISO 9241-210:2019. [2] International Ergonomics Association. [3] Nielsen (2000), por qué basta probar con 5 usuarios. [4] Moran y Gordon (2023), evaluación heurística (NN/g). [5] Hick (1952). [6] Fitts (1954). [7] Miller (1956). [8] Cowan (2001). [9] Wagemans y cols. (2012), un siglo de psicología Gestalt. [10] Card, Moran y Newell (1983). [11] Suchman (1987). [12] Norman (1988). [13] Desmet y Hekkert (2007). [14] Schlamann, Nestler y Thielsch (2026). [15] Hertzum (2025), International Journal of Human-Computer Studies 195, 103408 (el DOI contiene 2024). [16] Perrig y cols. (2024), Frontiers in Computer Science 6. [17] Hertzum (2026), System Usability Scale (texto editorial bloqueado, resumen institucional). [18] Scheibehenne, Greifeneder y Todd (2010). [19] Chernev, Böckenholt y Goodman (2015). [20] Reinecke y Gajos (2014), CHI. [21] Lindgaard y cols. (2006). [22] W3C WCAG 2.2 (12/12/2024). [23] WCAG2ICT. [24] W3C WAI, evaluación de accesibilidad web. [25] PDF Association, ISO 14289-2 (PDF/UA-2, 2024). [26] Brooke (1996), SUS. [27] Rodden, Hutchinson y Fu (2010), HEART (Google Research). [28] NASA-TLX. [29] Cawley y Talbot (2010), JMLR 11. [30] Riley y cols. (2020), BMJ. [31] Guo y cols. (2017), ICML. [32] Angelopoulos y Bates (2021, versión 2022), arXiv. [33] NIST AI RMF 1.0 (2023) y perfil de IA generativa (2024). [34] Camerer y cols. (2018). [35] Seshadri y cols. (2026), manuscrito v2 del 28/01/2026 (ACL 2026, artículo 2192). [36] Zheng y cols. (2023), NeurIPS Datasets and Benchmarks. [37] Linardos y cols. (2021), ICCV. [38] Dmitriev y cols. (2017), A Dirty Dozen (Microsoft Research). [39] Fabijan y cols. (2019), Sample Ratio Mismatch. [40] W3C WCAG 3.0, Working Draft del 10/09/2026. [41] Sweller (1988). [42] UEQ y manual. [43] Suchman, conclusión de la primera edición (Cambridge Core). [44] Documento Maestro del kit del creador, v4.3 del 25/09/2026, texto de 27 páginas (fuente privada: se analizó la especificación sin ejecutar el kit ni verificar sus afirmaciones de desempeño).

Aviso del estudio: las referencias privadas no constituyen prueba científica externa; los umbrales y decisiones de ingeniería no derivados de una norma se presentan como propuestas que requieren validación (p.34).

## 19. Interpretación para Edumashow

### 19.1 Qué aporta

Es el estudio que más se parece a lo que el Gate de Edumashow ya hace: un verificador que falla cerrado, ligado al hash del paquete, con un contrato por comprobación (id, método, estado, evidencia, versión) y salidas separadas (conformidad, perfil de calidad, estimación comercial no estimable). Fue la base de R-PRO-01 a R-PRO-07, de R-DAT-01 a 08 y de buena parte de los filtros de legibilidad y enlaces (R-LEG, R-SIG-08). Las traducciones de PDF a web las hizo el núcleo: contraste, glifos, solapes, enlaces reales, hash del archivo entregado, huella de diseño, texto mínimo medido en pantalla, peso por canal.

### 19.2 Principios ya aplicados

- Falla cerrada; sin prueba no hay aprobación; el generador no aprueba su propia salida (L01 a L03, p.23).
- El permiso se liga al hash exacto (V11, L02).
- Una comprobación con estado explícito y evidencia (p.23). El núcleo usa PASS, WARN, FAIL, UNAVAILABLE y N/A; el estudio usa PASS, FAIL, REVIEW, MISSING, ERROR y NOT_APPLICABLE.
- Conformidad, perfil de calidad y estimación comercial no se mezclan; sin modelo validado, la estimación dice no estimable (p.19).
- Un score no es una probabilidad (p.13).
- La estética no tapa los fallos de uso (H-UX-01 a H-UX-03).
- El texto de la web o del documento es dato, no instrucción para el evaluador (contenido no confiable, p.24).

### 19.3 Ideas que el núcleo aún no explota (candidatas, sin activar)

1. Mide el propio verificador: banco de casos correctos y defectuosos, y las cinco métricas (sensibilidad por gravedad, precisión, falsa liberación, falso bloqueo, cobertura). Es el contenido de R-PRO-04, hoy pendiente. Familias de prueba propias de la web: moneda y precio contradictorios, texto tapado, acentos cortados, enlace al destino equivocado, archivo cambiado tras el PASS, regla nueva, renderer caído, orden de lectura, CTA sin vínculo, falso positivo de espacio intencional, texto que instruye al evaluador.
2. Dos políticas de entrega declaradas desde el inicio: con conformidad y revisión UX, y con predicción validada adicional (p.22). Edumashow solo usa la primera; conviene dejarlo escrito en el informe.
3. Cero fallos observados no es riesgo cero: límite superior 1 - 0,05 a la 1/n (45,1% con 5 casos; 9,5% con 30; 3,0% con 100; 1,0% con 300). Útil para redactar el informe del Gate sin sobreprometer (p.27).
4. Pruebas de tarea con personas (p.16): rondas de 5 a 8 personas, tareas que no inducen la respuesta, salida por incidente con gravedad y comprobación posterior. Para una web de restaurante, tareas del tipo encuentra el horario, cuánto cuesta este plato, reserva para dos, cómo llegas. Objetivos piloto: cero errores críticos de precio, moneda o carta; comprensión de las condiciones centrales; completar el siguiente paso sin ayuda. Es R-MED-04, hoy pendiente.
5. Clasificar cada corrección de Eduardo (regla comercial, defecto de implementación, criterio creativo, barrera UX o preferencia personal) y convertir lo verificable en caso de prueba sin elevar las preferencias aisladas a ley (p.33).
6. Registro de afirmaciones con tipo dato, inferencia o supuesto, fuente, fecha consultada y ubicación (p.18). Completaría R-DAT-05 (parcial).
7. Aleatorizar por oportunidad o por empresa antes del envío; no analizar solo a quienes abrieron; revisar la proporción de muestra por si la asignación se rompió (Sample Ratio Mismatch) (p.28).
8. Ablaciones: cada módulo demuestra lo que aporta; más módulos no implican más mejora (p.29). Encaja con el presupuesto de movimiento y JavaScript.
9. Unidad de análisis: la persona haciendo una tarea, y el recorrido de seis momentos (recepción, orientación, evaluación, decisión, consulta interna, ejecución) para razonar la web como un recorrido de visitante (llegar, orientarse, evaluar la carta, decidir, compartir con el grupo, volver).
10. Tres hitos de ambición verificable: construido, validado, superior; no confundirlos en el lenguaje del informe.

### 19.4 Cautelas

- Todo el catálogo de 33 filtros es propuesta del estudio para PDF de propuestas. Los umbrales (4,5 a 1, 3 a 1, 24 píxeles, 5 a 8 personas, ventanas de 14, 30 y 90 días, 15 resultados) son valores iniciales, no resultados.
- Las cifras de potencia pertenecen a escenarios hipotéticos; no son tasas del creador ni de Edumashow.
- Varias fuentes se comprobaron solo por resumen (por ejemplo [14], [15], [17]); el estudio lo declara.
- El estudio no habla de webs, movimiento, velocidad de carga ni móvil de gama media; el núcleo los cubre con normas y medidas propias.
- La sección 28 es un comentario de segunda mano sobre reglas privadas del kit anterior; no se reproduce ese kit.
