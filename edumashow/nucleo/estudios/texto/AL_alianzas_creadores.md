> Texto completo del PDF aportado por Eduardo (Estudio_motor_predictivo_alianzas_creadores.pdf, 55 páginas), convertido a Markdown por Edumashow para consulta. Las marcas **[p.N]** indican el cambio de página (numeración del pie del PDF). Se quitan cabeceras y pies repetidos, las comillas se normalizan a rectas, las tablas pasan a Markdown y se conservan los enlaces del PDF. 
> Archivo de consulta: el conocimiento ejecutable vive en reglas.json; este texto no se pega en prompts ni se entrega a clientes. Lectura analítica en ../analisis/.

**[p.1]**

# Motor predictivo para propuestas y alianzas con creadores

Estudio científico y especificación ampliada de ingeniería · Versión 2

Preparado para Eduardo · Corte editorial: 3 de octubre de 2026

### Conclusión ejecutiva

Es factible construir una plataforma que investigue marcas, compare ofertas, estime resultados con incertidumbre y aprenda qué decisiones producen alianzas rentables. Este estudio define una arquitectura ambiciosa y verificable para competir en ese dominio. No demuestra que ya sea el mejor motor mundial ni que exista una base perfecta que siempre encuentre la mejor opción.

### Qué cambia en esta versión

La ampliación añade métodos relacionales de frontera, evidencia de 2026 sobre pronósticos con modelos de lenguaje, contratos de resultados, esquema de datos, construcción temporal, algoritmos, interfaces, optimización, pruebas, operación y un protocolo de superioridad. Explica también las decisiones que necesitan datos reales antes de producción.

### Guía de lectura

Capítulos 1-6: evidencia, Microsoft, modelos y marketing. Capítulos 7-24: objetivos, datos, países, incertidumbre, potencia y diseño conceptual. Capítulos 25-47: auditoría, ingeniería operativa, validación, frontera de investigación y paquetes de construcción. Capítulos 48-54: 50 referencias con metadatos y enlaces.

### Qué está y qué no está construido

Hay una investigación documentada y una especificación para iniciar una implementación delimitada. No hay software desplegado, predictor entrenado con tus resultados ni precisión comercial medida. Los parámetros iniciales, ejemplos, esquemas y políticas propuestos deben comprobarse. La superioridad se determina con pruebas independientes, no contando algoritmos o variables.

Los ejemplos están identificados como hipotéticos. Los resultados científicos conservan su ámbito original; no se presentan como evidencia directa de aceptación de tus propuestas. Un resultado desconocido puede seguir siendo desconocido después de millones de cálculos.

**[p.2]**

## 01 Cómo se hizo y cómo interpretar la evidencia

Se realizó una revisión dirigida de publicaciones científicas, repositorios de sus autores, documentación técnica y fuentes institucionales, con corte al 3 de octubre de 2026. Se priorizaron artículos originales, metaanálisis, experimentos y documentación de los desarrolladores. Las referencias al final permiten comprobar los hallazgos. Esta revisión no equivale a una revisión sistemática exhaustiva con protocolo PRISMA ni a un nuevo metaanálisis.

Se buscaron seis grupos de evidencia: sistemas de Microsoft y LaLiga; aprendizaje con pocos datos; marketing con creadores; personalización y persuasión; incertidumbre y causalidad; y evaluación experimental. Se revisaron tanto resultados favorables como limitaciones y una corrección científica reciente. Los anuncios comerciales se identifican como tales y no se convierten en pruebas independientes de superioridad.

### Jerarquía práctica para tomar decisiones

| Evidencia | Qué permite concluir | Qué falta para tu caso |
|---|---|---|
| Experimento propio aleatorizado | Efecto de una alternativa en el entorno probado | Replicación y transporte a otras marcas |
| Historial propio validado en el futuro | Capacidad predictiva dentro del contexto observado | Causalidad y rendimiento fuera del contexto |
| Metaanálisis pertinente | Patrones medios y heterogeneidad de varios estudios | Correspondencia con compradores B2B |
| Benchmark de modelos | Comparación en tareas y recursos definidos | Datos y objetivo comercial propios |
| Documentación o anuncio del proveedor | Funcionalidad o disponibilidad declarada | Reproducción independiente |
| Juicio de IA o experto | Hipótesis y propuestas de diseño | Validación con resultados observados |

Las investigaciones sobre consumidores que ven publicaciones no estudian necesariamente a un gerente que decide pagar una colaboración. Esa distancia de aplicación es central. Tampoco pueden sumarse directamente estudios de dos metaanálisis: pueden compartir investigaciones y medir resultados distintos.

Acceso y alcance. Algunas fuentes se comprobaron a nivel de resumen o ficha institucional; se indica en la bibliografía. No se extrajeron bases privadas de millones de propuestas ni secretos empresariales. El estudio propone aprovechar métodos publicados y componentes autorizados, junto con datos propios que se puedan obtener legítimamente.

**[p.3]**

## 02 Por qué millones de patrones no garantizan acertar

Un patrón puede ser real, accidental, transitorio o consecuencia de una variable oculta. Que una relación describa bien el pasado no demuestra que vaya a funcionar al cambiar el precio, el país o la persona que decide. La evidencia relevante es su capacidad de predecir datos nuevos y, cuando se cambia una propuesta, el efecto de ese cambio.

Ejemplo matemático. Si se prueban 1.000.000 de hipótesis nulas verdaderas con pruebas válidas al nivel 0,05, el número esperado de falsos positivos es 50.000 sin corrección. Para esa esperanza no se necesita independencia. Bajo independencia, la probabilidad de obtener al menos un falso positivo sería 1 - 0,95 elevado a 1.000.000, prácticamente uno. Encontrar algo llamativo sería fácil aunque no hubiera señal útil.

Benjamini y Hochberg formalizaron en 1995 un procedimiento para controlar la tasa de falsos descubrimientos bajo sus supuestos. Es una herramienta de exploración, no una licencia para seleccionar ganadores en el mismo conjunto utilizado para comprobarlos. El diseño necesita también datos reservados y replicación. [S01]

Los teoremas de no free lunch tienen supuestos específicos, como promediar sobre distribuciones amplias de problemas. No significan que aprender sea inútil. Sí ayudan a entender que un algoritmo necesita supuestos y un dominio: no hay una garantía de superioridad universal por ser más complejo. [S02]

### Seis cantidades distintas

| Concepto | Significado correcto |
|---|---|
| Exactitud | Proporción de decisiones clasificadas correctamente |
| Precision o valor predictivo positivo | De los casos marcados como positivos, cuántos lo fueron |
| Calibración | Concordancia entre probabilidades y frecuencias en grupos comparables |
| Potencia estadística | Probabilidad de detectar un efecto específico si existe |
| Intervalo de incertidumbre | Rango ligado al modelo, datos y supuestos establecidos |
| Utilidad | Valor económico y estratégico de la decisión, incluidos sus costes |

Si el 95% de las marcas rechaza, un predictor que diga siempre "no" tendrá 95% de exactitud y puede ser inútil para vender. Tu objetivo debe combinar probabilidades fiables, selección de oportunidades y rentabilidad; no una cifra de exactitud aislada.

**[p.4]**

## 03 Qué tienen Microsoft y LaLiga realmente

Tu referencia parece combinar dos familias diferentes. TrueSkill se desarrolló para estimar habilidad en videojuegos. Beyond Stats utiliza datos futbolísticos y tecnología de Microsoft Azure junto con Mediacoach. No son el mismo motor ni hay evidencia de un único sistema omnisciente detrás de ambos.

| Sistema | Qué hace | Idea aprovechable para tus propuestas |
|---|---|---|
| TrueSkill y TrueSkill 2 | Inferencia bayesiana de habilidad a partir de partidas y señales adicionales | Actualizar estimaciones e incertidumbre tras cada resultado |
| Mediacoach y Beyond Stats | Captura, procesamiento y presentación de métricas de fútbol | Datos trazables, variables específicas y análisis contextual |
| Matchbox | Recomendación que combina metadatos e interacciones previas | Compatibilidad talento, marca y oferta; arranque con atributos |
| LightGBM | Aprendizaje con árboles para datos estructurados | Comparar patrones e interacciones de precios y condiciones |
| DoWhy y EconML | Modelado y estimación de relaciones causales | Investigar qué cambios pueden mejorar resultados |
| Experimentación y bandits | Comparación controlada y selección adaptativa de acciones | Aprender de variantes comerciales seguras |

En la evaluación descrita por Microsoft para Halo 5, TrueSkill 2 alcanzó 68% de acierto sobre resultados históricos frente a 52% de TrueSkill. Ese resultado pertenece a esa evaluación, no a cierres comerciales. Lo trasladable es la inferencia con incertidumbre; copiar sus porcentajes sería incorrecto. [S03]

LaLiga describe más de 3,5 millones de puntos de datos por partido para sus métricas. Son mediciones repetidas de un entorno instrumentado, no millones de decisiones independientes ni millones de variables causales. El equivalente comercial sería disponer de un registro consistente de todo el proceso de venta y ejecución. [S04]

Matchbox incorporó metadatos de usuarios y productos junto con comportamiento previo. Es una inspiración más directa para recomendar alianzas que un ranking de habilidad deportiva. LightGBM proporciona otra pieza de ingeniería, no una interpretación automática de lo que desea un comprador. [S05, S06]

Conclusión técnica. Azure puede ser infraestructura; no es por sí mismo un modelo estadístico. El valor viene de definir bien la tarea, capturar las señales adecuadas y verificar cada módulo.

**[p.5]**

## 04 Los candidatos actuales y cuál elegiría

No seleccionaría un ganador mundial sin medirlo sobre tus datos y tus costes. Mantendría una comparación entre una base sencilla y modelos más avanzados. Un modelo que domina un benchmark puede perder al cambiar la prevalencia de aceptación, la calidad de los datos o el país.

TabPFN es especialmente pertinente: el trabajo publicado en Nature en 2025 presentó un modelo fundacional tabular evaluado en conjuntos pequeños y medianos, de hasta 10.000 muestras y 500 variables. El preentrenamiento permite reutilizar estructura aprendida; sigue necesitando ejemplos y señales pertinentes para la tarea concreta. [S07]

La investigación posterior incluye TabPFN 2.5 y TabICLv2. El preprint de este último, revisado en septiembre de 2026, informa resultados competitivos en TabArena y TALENT y capacidad para conjuntos mucho mayores. Debe tratarse como resultado de sus autores, sujeto a condiciones de comparación y reproducción. [S08, S09]

También verifiqué una novedad de septiembre de 2026: SAP anunció TabPFN 3.5 Plus en SAP AI Core. Su superioridad declarada es una afirmación del proveedor basada en benchmarks; no demuestra que sea el mejor para propuestas de creadores. [S10]

| Candidato | Cuándo tiene sentido | Condición para conservarlo |
|---|---|---|
| Tasa base y regresión logística regularizada | Inicio y referencia permanente | Buena calibración y utilidad con poca complejidad |
| Modelo bayesiano jerárquico | Marcas, países y sectores con pocos casos cada uno | Compartir información sin borrar diferencias |
| CatBoost o LightGBM | Historial tabular suficiente y relaciones no lineales | Mejora temporal reproducible frente a la base |
| Familia TabPFN o TabICL | Evaluar transferencia de aprendizaje con pocos datos | Ganancia local que compense coste y restricciones |
| Ensamble | Modelos que cometen errores distintos | Beneficio fuera de muestra y calibración estable |
| Modelo de lenguaje | Leer fuentes, extraer atributos y redactar alternativas | Trazabilidad y revisión; no inventar probabilidades |

TabArena, publicado en NeurIPS 2025, muestra que la validación, el presupuesto de cómputo y los ensambles afectan las comparaciones. Recomienda evaluar sistemas completos con condiciones comparables. [S11]

Mi elección inicial sería una base jerárquica interpretable y un módulo de investigación. Añadiría candidatos tabulares como retadores, sin convertir una marca de software en requisito de éxito.

**[p.6]**

## 05 Qué sabemos sobre el marketing con creadores

Pan y colaboradores sintetizaron 1.531 tamaños de efecto de 251 trabajos. Distinguen características del contenido, del seguidor y del creador, además de mediadores y moderadores. Los factores relevantes cambian según el resultado: actitud, interacción, intención, conducta de compra o ventas. La implicación es elegir pruebas y entregables según el objetivo comercial, en lugar de usar seguidores como medida universal. [S12]

Barari, Eisend y Jain analizaron 71 trabajos con 135 estudios experimentales y 571 tamaños de efecto. Encontraron diferencias en la eficacia de los creadores según el resultado y el contexto, y efectos mediados por credibilidad y atractivo. El tamaño del creador tampoco tiene una utilidad idéntica para interacción e intención de compra. Son resultados medios sobre consumidores, no probabilidades de firma de una marca. [S13]

### Cómo traducirlo a una propuesta

| Necesidad plausible | Evidencia que conviene mostrar | Lo que no demuestra por sí sola |
|---|---|---|
| Visitas locales | Audiencia geográfica relevante y resultados locales verificables | Que cualquier seguidor se desplazará al local |
| Descubrimiento de producto | Retención, visualizaciones cualificadas y demostraciones comparables | Ventas incrementales garantizadas |
| Contenido para redes de marca | Calidad de piezas, formatos y derechos claramente delimitados | Que alcance orgánico equivalga a licencia de uso |
| Captación medible | Clics, códigos, reservas y medición acordada | Causalidad si no hay comparación apropiada |
| Posicionamiento | Encaje de estilo, valores y referencias del segmento | Facturación inmediata |

Una marca puede valorar varios objetivos. El motor debe mantenerlos separados hasta que haya evidencia suficiente para priorizar. Si solo conoce información pública, puede proponer una hipótesis de necesidad y una alternativa robusta, pero no afirmar que ha leído la intención interna del gerente.

La pregunta central para el encaje es concreta: "¿Qué resultado puede aportar este creador a este negocio, en este mercado, con este formato y estas condiciones?". Una propuesta puede estar bien escrita y no resolver esa pregunta.

Regla de traducción científica. No convertir una correlación, un tamaño de efecto estandarizado o un aumento de intención de compra en puntos porcentuales de aceptación B2B. El cierre, la ejecución y el resultado de la campaña requieren etiquetas y validaciones distintas.

**[p.7]**

## 06 Personalización con evidencia y sus límites

La personalización comercial puede ser útil, pero no equivale a adivinar la personalidad de una persona. Un metaanálisis de Eisend, Niewiadomska y van Noort, publicado en línea en junio de 2026, integra 1.536 efectos de 290 estudios en 229 trabajos. Su resumen informa beneficios medios de personalización y moderación según el tipo de datos y el nivel de personalización. Aquí se comprobó el resumen editorial, no sus tablas completas. [S14]

En contraste, Perla y colaboradores revisaron 41 estudios sobre inferir personalidad a partir de huellas digitales y adaptar mensajes a ella. Informan aproximadamente 5% de varianza explicada en personalidad y efectos conductuales insignificantes o muy pequeños; al controlar problemas metodológicos, la eficacia de extremo a extremo se aproxima a cero. Esto no invalida toda personalización: estudia una estrategia más específica. [S15]

El estudio histórico de Matz y colaboradores de 2017 informó, en sus campañas, hasta 40% más clics y 50% más compras con determinados mensajes alineados. Son máximos de condiciones particulares, no un efecto universal ni una garantía aplicable a propuestas. Deben interpretarse junto con la evidencia posterior. [S16]

### Una corrección que cambia la interpretación

Salvi y colaboradores estudiaron persuasión conversacional con GPT-4 en un experimento prerregistrado de 900 participantes. La comparación con humanos no mide cierres comerciales. En septiembre de 2026 apareció una corrección: al comparar directamente GPT-4 personalizado y sin personalizar, el valor p corregido es 0,0678, no 0,04. Esa comparación no permite establecer concluyentemente una ventaja adicional de personalizar. Ausencia de significación tampoco demuestra igualdad. [S17, S18]

### Recomendación derivada para este motor

Priorizar señales de negocio: carta, precios públicos, ubicación, productos protagonistas, canales, campañas, lenguaje de marca y audiencia servida. Usar información del decisor solo cuando esté disponible de forma pertinente y autorizada, como su función profesional o requisitos expresados. Evitar convertir estilo de Instagram, apariencia o supuestas emociones en un perfil psicológico factual.

El objetivo de "hacer clic" con la marca debe operacionalizarse como relevancia comprobable, comprensión, confianza en la ejecución y valor económico plausible. Ninguna de esas dimensiones autoriza inventar necesidades privadas ni fabricar evidencia social.

**[p.8]**

## 07 El objetivo económico que debe optimizar

Maximizar la tasa de aceptación puede producir ofertas demasiado baratas, agotamiento y derechos cedidos sin compensación. El motor debe optimizar una colaboración viable para ambas partes, con restricciones explícitas del talento y una evaluación separada del beneficio de la marca.

### Una función de decisión propuesta

Valor de una acción = probabilidad de aceptación × margen esperado si se acepta - coste de preparar y negociar - penalización de riesgo + valor futuro documentado.

El margen condicionado a aceptación debe contemplar cobro esperado, producción, edición, traslados, comisiones, impuestos aplicables cuando estén determinados, devoluciones y coste de oportunidad. La penalización de riesgo representa preferencias explícitas; no debe duplicar costes ya descontados. La renovación futura solo se incorpora si hay evidencia, o se presenta como escenario separado.

| Ejemplo hipotético | Oferta A | Oferta B | Oferta C |
|---|---|---|---|
| Precio | 350 € | 500 € | 650 € |
| Coste si se acepta | 150 € | 170 € | 200 € |
| Margen condicionado | 200 € | 330 € | 450 € |
| Probabilidad supuesta | 50% | 35% | 25% |
| Preparación y negociación | 10 € | 10 € | 10 € |
| Margen esperado por oportunidad | 90 € | 105,50 € | 102,50 € |

Este cálculo supone cobro íntegro, costes fijos por caso y ninguna diferencia de riesgo o renovación. Bajo esos supuestos, B tiene el mayor valor esperado aunque A se acepte más. La diferencia B-C es solo 3 €: con probabilidades inciertas no corresponde fingir una ventaja concluyente. La función real debe valorar tiempo y capacidad disponibles.

Bienestar y preferencias. El talento define límites de carga, viajes, afinidad con la marca, exposición reputacional, exclusividad y libertad creativa. Un modelo no puede deducir cuánto vale su felicidad. Puede mostrar opciones no dominadas: aquellas para las que mejorar una dimensión exige empeorar otra, y hacer análisis de sensibilidad a sus preferencias.

Para la marca, el beneficio esperado debe distinguir ventas incrementales, contenido reutilizable y posicionamiento sin sumarlos dos veces. Una negociación sostenible busca una zona de beneficio mutuo; no presume que todo comprador aceptará una oferta técnicamente atractiva.

**[p.9]**

## 08 Los pocos datos que tú aportarías

Es viable reducir tu carga manual. No es viable eliminar la información que permite distinguir una oportunidad de otra. Propongo dos entradas: un perfil permanente del talento y un breve encargo por marca. El resto lo investiga o calcula el sistema, conservando los desconocidos.

| Entrada | Contenido mínimo | Frecuencia |
|---|---|---|
| Perfil de talento | Nicho, idiomas, formatos, mercados y ejemplos aprobados | Inicial y cuando cambie |
| Métricas autorizadas | Alcance, retención, geografía y resultados disponibles | Por periodo y campaña |
| Restricciones | Tarifa mínima, costes, derechos, exclusividad y carga aceptable | Inicial y por excepción |
| Encargo de marca | Nombre o URL, país o ciudad, producto o categoría | Cada oportunidad |
| Oferta autorizada | Precio o rango permitido, entregables y condiciones | Cada oportunidad |
| Contexto conocido | Relación previa y cualquier información recibida | Si existe |

Datos que puede investigar: identidad y ubicaciones del negocio, carta o catálogo, rango de precios observable, posicionamiento, promociones actuales, canales de reserva, colaboraciones publicadas, estacionalidad y situación económica. Cada hallazgo debe llevar fuente y fecha. Una colaboración visible no revela necesariamente cuánto se pagó ni cómo se negoció.

Datos que no debe inventar: presupuesto interno, margen del restaurante, alcance por ciudad no publicado, tasa de conversión no medida, motivos del rechazo, autoridad del contacto y ofertas de la competencia. Las reseñas pueden indicar temas, pero no representan una muestra neutral de clientes ni prueban un problema financiero.

El aprendizaje posterior puede ser casi automático si el sistema recibe, con autorización, respuestas y resultados. Para cada caso bastaría confirmar la etapa, las condiciones finales, el cobro y la ejecución cuando no puedan extraerse de registros fiables. Las etiquetas extraídas por IA conservan evidencia y una marca de revisión.

Las reglas aprobadas de tu sistema de propuestas se cargan como configuración. No se infieren de preferencias genéricas ni se reescriben por un supuesto aumento de aceptación. Antes de integrar el motor habría que leer la versión vigente del kit; este estudio no audita sus archivos actuales.

**[p.10]**

## 09 El historial que verdaderamente sirve para aprender

Un archivo de propuestas enseña formato, oferta y decisiones editoriales. Un historial predictivo añade qué pasó después, cuándo pasó y qué información se conocía antes del envío. Tener cientos de PDFs sin resultados no equivale a tener cientos de ejemplos etiquetados de aceptación.

Unidad recomendada: oportunidad comercial. Una marca, un objetivo, una secuencia de negociación y sus versiones. No contar cada PDF, recordatorio o captura como una nueva venta independiente. Las cadenas con varios locales pueden compartir decisor; conviene registrar esa dependencia.

| Grupo de metadatos | Campos fundamentales |
|---|---|
| Identidad | opportunity_id, brand_id, grupo comercial, talento y mercado |
| Oferta | Texto exacto, versión, precio, moneda, entregables y derechos |
| Información disponible | Evidencia, fecha observada, fecha publicada y nivel de certeza |
| Envío | Fecha, canal, destinatario funcional y estado de entrega conocido |
| Negociación | Respuestas, objeciones expresadas, contrapropuestas y seguimiento |
| Resultado | Acuerdo, fecha, precio final, cobro, cancelación y ejecución |
| Campaña | Métricas acordadas, periodo, coste real, resultado y renovación |
| Modelo | Versión, predicción congelada, alternativas y decisión elegida |

Estados separados. Preparada; enviada; entrega fallida; respuesta; interés; negociación; aceptación documentada; rechazo explícito; pendiente; cobrada; ejecutada; renovada. El silencio no revela rechazo psicológico. Para "aceptación dentro de 30 días", un caso con seguimiento completo y sin acuerdo cuenta como no aceptación en esa ventana; uno observado solo 8 días permanece censurado o pendiente.

Sin fuga de información. No utilizar el descuento final, una respuesta posterior o métricas de la campaña para predecir la aceptación inicial. Sí pueden alimentar un modelo distinto que se ejecuta en una etapa posterior. Las fuentes económicas también necesitan una versión histórica: una revisión publicada después no era conocida al decidir.

Sesgos que hay que registrar. Solo enviar a marcas prometedoras produce selección. Conservar únicamente aprobadas produce supervivencia. Contar propuestas repetidas produce seudorreplicación. Confundir cortesía con firma cambia la etiqueta. Un registro pequeño pero consistente suele ser más útil que un archivo enorme con estos errores.

**[p.11]**

## 10 Arrancar con pocos datos y aprovechar datos externos

El arranque razonable tiene tres niveles de salida. Nivel inicial: diagnóstico de encaje y escenarios, sin porcentaje validado. Nivel intermedio: probabilidades provisionales con supuestos, tasa base e incertidumbre claramente identificados. Nivel validado: probabilidades cuyo comportamiento se comprobó en oportunidades posteriores y comparables.

Se puede transferir conocimiento sobre lenguaje, categorías, estructuras tabulares y mecanismos plausibles. No se transfiere automáticamente una tasa de cierre. El público, los precios, el canal y el proceso de compra pueden ser diferentes. Un millón de campañas de comercio electrónico no reemplaza resultados de negociaciones B2B de creadores.

En esta búsqueda no identifiqué una base pública verificada de millones de propuestas de colaboración con creadores que combine texto, oferta, aceptación o rechazo, contexto previo y resultado económico. Esto no demuestra que no exista alguna base privada. Conseguirla exigiría acuerdos, licencias y comprobar su comparabilidad; no basta con extraer páginas de Internet.

Como contraste, UCI Bank Marketing contiene 45.211 observaciones en su conjunto clásico de campañas telefónicas de banca portuguesa. Sirve para enseñar métodos o probar una tubería de datos, pero no valida tu problema. Además, la duración de la llamada no estaría disponible antes de llamar: incluirla para una predicción previa sería fuga de información. [S19]

### Tres formas útiles de usar información externa

1. Recuperar casos semejantes para inspirar la oferta y comprobar sus diferencias. Una referencia editorial no se convierte en una etiqueta de éxito si no hay resultado observable.

2. Compartir información entre sectores o países mediante un modelo jerárquico, con validación del transporte. Si empeora un mercado nuevo, reducir esa transferencia.

3. Utilizar preentrenamiento y datos sintéticos para representación, pruebas de software y situaciones de estrés. Las respuestas simuladas de marcas no cuentan como aceptaciones reales para calibrar.

No hay un número mínimo universal de casos. Depende de la frecuencia de acuerdos, complejidad, heterogeneidad y precisión exigida. Riley y colaboradores muestran por qué reglas fijas como "diez eventos por variable" son insuficientes para planificar modelos; la adaptación comercial debe conservar esa lógica, sin importar umbrales clínicos mecánicamente. [S20]

**[p.12]**

## 11 Adaptación por país y por negocio

Independencia de análisis no significa entrenar un modelo aislado para cada marca con dos observaciones. La solución propuesta combina información compartida, efectos por mercado y atributos específicos del negocio. Un establecimiento nuevo conserva más incertidumbre; no recibe una identidad estadística inventada.

| Contexto | Variables a comprobar | Decisión que pueden cambiar |
|---|---|---|
| Restaurante local | Radio de clientes, ticket, capacidad, reservas y audiencia local | Contenido, prueba, promesa y viabilidad del precio |
| Cadena o franquicia | Decisor, número de locales y ámbito del presupuesto | Escala de campaña y alcance del acuerdo |
| Marca de comercio electrónico | Países servidos, entrega, margen y conversión disponibles | Geografía útil, medición y formato |
| Servicio internacional | Mercados prioritarios, idiomas y uso durante viajes | Narrativa y distribución entre países |
| España | Ciudad, turismo, estacionalidad, costes y marco fiscal aplicable | Contexto y margen neto, sin generalizaciones culturales |
| Venezuela | Moneda contractual, referencia de conversión, fecha de pago y costes | Escenarios de cobro y rentabilidad real |

Fuentes estructuradas propuestas. INE para series españolas; FMI y Banco Mundial para contexto internacional; BCE para referencias de cambio pertinentes. Estas fuentes permiten automatizar consultas y preservar fecha y unidad. Los tipos de referencia no necesariamente son el tipo efectivo de una transacción. [S21, S22, S23, S24]

En contratos referidos al BCV, el sistema debe verificar la fuente oficial y la fecha que corresponda a las condiciones pactadas. Este informe no fija una cotización ni una regla fiscal. Los impuestos requieren residencia, entidad que factura, actividad y jurisdicción; si faltan, mostrar escenarios y señalar la variable pendiente, sin asignar una tasa arbitraria.

La macroeconomía aporta contexto, no lectura de la caja del negocio. Inflación, turismo o PIB pueden ser útiles si agregan poder predictivo comprobado, pero no prueban disposición a pagar de un restaurante particular. Evitar contar cientos de negocios del mismo país y mes como cientos de observaciones económicas independientes.

Actualización propuesta. Refrescar precios públicos y campañas antes de cada oferta; tasas cuando corresponda al cálculo; series macro al publicarse; métricas del talento por ventana comparable. Cada dato debe tener vigencia y una política para actuar si la fuente falla.

**[p.13]**

## 12 Cómo investigar lo que la marca necesita

El motor necesita una ficha de evidencia, no una descripción halagadora. Para cada marca construiría una secuencia de problema plausible, señal observada, contribución del creador, prueba comparable y condiciones que vuelven viable la alianza.

Ejemplo ficticio. Un restaurante destaca públicamente un menú de mediodía y un canal de reservas. El hecho es la oferta publicada. "Quiere aumentar reservas de lunes a jueves" es una hipótesis que necesita contexto adicional; la publicación por sí sola no demuestra mesas vacías. Un concepto centrado en explicar el menú puede ser pertinente sin afirmar una necesidad financiera.

Cada observación tendría una de cuatro etiquetas: hecho confirmado; inferencia razonable; supuesto para un escenario; o desconocido. El texto final solo presenta los hechos como hechos. Las inferencias pueden guiar la creatividad sin atribuir al comprador una confesión que nunca hizo.

### Preguntas internas del motor

1. ¿Qué vende el negocio y qué diferencia quiere hacer visible según sus propios canales?

2. ¿A quién puede servir realmente, en qué lugares y con qué capacidad?

3. ¿Qué parte de la audiencia y del formato del creador tiene relación demostrable con ese objetivo?

4. ¿Qué resultado puede ofrecerse de forma responsable y cómo se observaría?

5. ¿Qué obstáculos concretos puede resolver la propuesta: producción, comprensión, prueba, coordinación o derechos?

6. ¿Qué evidencia podría cambiar la recomendación o volverla inviable?

Si tú no tienes más información, el sistema puede continuar investigando fuentes públicas. No necesita interrogar a la marca para producir una propuesta inicial. Cuando un dato crítico no sea recuperable, elegirá una oferta robusta entre necesidades plausibles o dejará una limitación interna, sin convertirla en certeza.

La prioridad de investigación se decide por su valor. Confirmar que el creador alcanza al mercado servido puede cambiar la oferta completa; descubrir otra variación de adjetivo puede no justificar trabajo adicional. Se deja de investigar cuando el dato extra no parece capaz de cambiar la decisión o cuesta más que su posible beneficio.

El seguimiento de nuevas necesidades no debe alterar automáticamente una oferta ya enviada. Cada versión se congela para mantener trazabilidad y evitar contradicciones en la negociación.

**[p.14]**

## 13 Texto y diseño que puedan entenderse

No hay evidencia universal de un número perfecto de palabras o de una frase que cierre cualquier colaboración. La longitud debe evaluarse junto con la complejidad de la oferta, el dispositivo, el canal, el conocimiento previo y la información que el comprador necesita para decidir.

Morkes y Nielsen compararon estilos de escritura web en 1997. La combinación de concisión, facilidad de escaneo y objetividad mejoró la usabilidad medida frente a su control; el conocido 124% describe ese experimento y esa métrica. No equivale a 124% más ventas ni demuestra una estructura obligatoria para PDFs de creadores. [S25]

### Propuesta de auditoría editorial

| Dimensión | Comprobación observable | Cómo aprender si mejora cierres |
|---|---|---|
| Relevancia | Explica por qué el concepto pertenece a esa marca | Comparar conceptos con el resto estable |
| Comprensión | Se pueden identificar oferta, coste y siguiente paso | Medir comprensión y luego acuerdos |
| Escaneo | Jerarquía visible y bloques con función clara | Pruebas en móvil y tiempos de localización |
| Evidencia | Cada afirmación tiene apoyo pertinente | Comparar selección de casos, sin inventarlos |
| Precisión | Entregables, derechos y responsabilidades inequívocos | Medir dudas, renegociación y disputas |
| Fluidez | Redundancias, jerga y frases largas detectadas | Probar simplificación conservando información |

Las medidas de legibilidad son señales auxiliares: dependen del idioma y no comprueban por sí solas que el lector entendió el negocio. El juicio de un modelo de lenguaje tampoco sustituye la reacción del comprador. Puede detectar ambigüedades y generar variantes para revisión.

Separar dos controles. La calidad de producción sí admite requisitos duros: texto sin recortes, alineación, contraste, precio y moneda coherentes, enlaces válidos y archivo que abre. La capacidad de convencer exige evidencia comercial. Un PDF perfecto puede ser rechazado por presupuesto o encaje.

Para tu flujo, el motor deberá respetar tipografías y referencias aprobadas, formatos de entrega y condiciones del encargo. Variará concepto, argumentos y evidencia cuando esté autorizado. No añadirá entregables, reducirá precios ni ofrecerá derechos para subir un indicador sin comprobar el efecto sobre el talento.

**[p.15]**

## 14 Arquitectura del motor propuesto

Diseño recomendado, no sistema ya implementado. Cada módulo debe tener entradas, salida verificable y una razón para existir. El cálculo estadístico no se delega a una frase de confianza producida por la IA.

| Módulo | Trabajo | Salida que se conserva |
|---|---|---|
| 1 Fuentes | Recuperar web, catálogo, métricas y contexto autorizado | Documento, URL, fecha y procedencia |
| 2 Extracción | Convertir información a campos y detectar contradicciones | Hechos, hipótesis y datos ausentes |
| 3 Memoria | Unir oportunidades, versiones y resultados sin duplicar | Historial con tiempos y entidades |
| 4 Compatibilidad | Relacionar talento, necesidad y mercado servido | Diagnóstico y evidencia comparable |
| 5 Alternativas | Proponer conceptos y paquetes dentro de límites | Acciones candidatas y restricciones |
| 6 Predicción | Estimar acuerdos, cobro, tiempo y resultados posibles | Distribuciones y estado de validación |
| 7 Economía | Calcular margen, esfuerzo y escenarios de riesgo | Valor por oferta y sensibilidad |
| 8 Decisión | Elegir o abstenerse según evidencia y preferencias | Recomendación y motivos verificables |
| 9 Producción | Redactar, diseñar y verificar entregables | Archivo final y control de calidad |
| 10 Aprendizaje | Capturar desenlace y comparar con lo previsto | Evaluación y propuesta de actualización |

Flujo operativo. Recibir el encargo; cargar restricciones; investigar; contrastar hechos; generar pocas alternativas materialmente distintas; evaluar; revisar incertidumbre; producir la recomendada; congelar; observar resultados. Las revisiones relevantes generan nuevas versiones, sin borrar lo anterior.

La búsqueda en millones de documentos, si se dispone de acceso, se resuelve con recuperación selectiva, índices y filtros de pertinencia. No conviene pasar todo el universo a cada predicción. Primero se identifica evidencia útil y después se estima una decisión concreta.

Los modelos de lenguaje sirven para extracción y propuesta de características. Se validan contra ejemplos anotados y se controla su estabilidad de versión. Los componentes estadísticos usan variables estructuradas, separación temporal y cálculos reproducibles. Las explicaciones distinguen "influyó en la predicción" de "causó la decisión".

Toda fuente externa se trata como información, sin permitir que instrucciones dentro de una web alteren reglas, datos o permisos del sistema. La investigación no envía mensajes ni compromete condiciones por sí sola.

**[p.16]**

## 15 El núcleo probabilístico y la individualización

Objetivo inicial propuesto: probabilidad de aceptación documentada dentro de una ventana definida, por ejemplo 30 días, condicionada a la información disponible al enviar. Otros modelos estiman respuesta, tiempo hasta acuerdo, cobro y ejecución. No multiplicar probabilidades marginales como si esas etapas fueran independientes.

### Modelo conceptual

logit(p) = intercepto + efecto de país + efecto de sector + efecto de talento + efecto de marca o grupo + efecto temporal + contribuciones de la oferta y del contexto.

Los efectos por grupo se regularizan: cuando hay pocos datos se aproximan a la información compartida; cuando hay evidencia suficiente pueden diferenciarse. Las marcas nuevas se estiman con atributos y distribución de grupos, manteniendo mayor incertidumbre. La fórmula es una especificación inicial, no una afirmación de que todas las relaciones sean lineales.

Un retador no lineal puede añadir interacciones útiles, como precio × formato, geografía × objetivo o relación previa × prueba elegida. Debe demostrar mejora en datos futuros. No se deben enumerar millones de interacciones con pocos acuerdos y luego presentar el mejor ajuste como descubrimiento.

### Ejemplo bayesiano calculado

Suponiendo 24 acuerdos en 100 oportunidades independientes y comparables, y un prior uniforme Beta(1,1), el posterior sería Beta(25,77). La media es 24,51% y el intervalo creíble central del 95% es aproximadamente 16,70%-33,26%. Es una tasa agrupada bajo esos supuestos, no la probabilidad específica de un restaurante nuevo.

Esta cuenta muestra que incluso cien observaciones dejan incertidumbre. Un prior informativo puede estrechar el intervalo, pero si no representa el mercado también puede sesgarlo. El motor debe mostrar sensibilidad a los priors y evitar que información externa muy abundante ahogue el historial local más pertinente.

Salidas separadas. Compatibilidad editorial, probabilidad estimada, intervalo, tamaño de muestra relevante, resultados de calibración y distancia respecto al entrenamiento. Un "92 de 100" de afinidad no se transforma en 92% de aceptación. El panel debe impedir esa confusión desde el diseño.

**[p.17]**

## 16 Qué cambios causan una mejora

La predicción responde "¿qué suele pasar en casos parecidos?". La decisión de modificar una oferta requiere otra pregunta: "¿qué cambiaría si enviáramos A en vez de B?". Las propuestas más caras podrían cerrar más porque se reservan para marcas con mayor presupuesto; eso no demuestra que subir el precio cause más acuerdos.

DoWhy organiza el análisis alrededor de supuestos causales explícitos, identificación, estimación y comprobaciones. EconML permite estimar efectos heterogéneos con métodos de aprendizaje. Estas herramientas no descubren automáticamente causas verdaderas ni eliminan confusores no medidos. [S26]

### Diseño de un primer experimento

Hipótesis: una apertura centrada en un objetivo observable de la marca mejora acuerdos frente a la apertura habitual. Mantener precio, entregables, calidad visual, canal y política de seguimiento. Asignar versiones al azar entre oportunidades elegibles, estratificando por país y tipo de negocio cuando sea viable. Si una cadena comparte decisor, aleatorizar por grupo para reducir contaminación.

Definir antes el resultado principal, ventana, mejora mínima relevante, tamaño de muestra y reglas de análisis. Medir aceptación documentada y margen por oportunidad; usar comprensión y respuestas como resultados secundarios. Analizar según la asignación inicial, documentando excepciones y pérdidas.

Cuando haya volumen suficiente, un bandit contextual puede seleccionar variantes utilizando el contexto y una exploración limitada. El trabajo de Li y colaboradores en recomendación de noticias informó una mejora de clics del 12,5% frente a un bandit sin contexto en su evaluación. Es un antecedente del método, no un porcentaje comercial transferible. [S27]

La evaluación fuera de política mediante estimadores doubly robust combina modelos de resultados con probabilidades de asignación. Necesita registrar esas probabilidades, solapamiento suficiente y supuestos adecuados; no corrige por magia un historial determinista que nunca probó ciertas ofertas. [S28]

Comenzaría con experimentos sencillos y seguros. La exploración nunca autoriza precios por debajo del límite, promesas no demostradas o derechos no aprobados. Si hay pocas oportunidades, priorizar diferencias estratégicas grandes sobre decenas de variaciones de palabras que serían imposibles de distinguir con precisión.

**[p.18]**

## 17 Potencia estadística y tamaño de muestra

Potencia del 80% significa que un experimento detectaría un efecto del tamaño especificado en aproximadamente 80% de repeticiones bajo el modelo. No significa 80% de probabilidad de que una oferta funcione. Primero se define el efecto mínimo que vale la pena detectar y luego se calcula la muestra.

Cálculo ilustrativo reproducible: dos grupos independientes, asignación 1 a 1, contraste bilateral, nivel 0,05, potencia 0,80, observaciones completas y aproximación normal sin corrección de continuidad.

| Tasa base supuesta | Tasa alternativa | Diferencia absoluta | Casos por grupo | Total |
|---|---|---|---|---|
| 10% | 20% | 10 puntos | 199 | 398 |
| 10% | 15% | 5 puntos | 686 | 1.372 |
| 10% | 12% | 2 puntos | 3.841 | 7.682 |
| 20% | 30% | 10 puntos | 294 | 588 |

### Fórmula usada

n por grupo = [1,96 × raíz(2 × p media × (1 - p media)) + 0,8416 × raíz(p0 × (1 - p0) + p1 × (1 - p1))]² / (p1 - p0)².

Se calcularon los cuantiles normales con scipy.stats.norm y se redondeó hacia arriba. No son muestras mínimas para cualquier algoritmo: pertenecen a este diseño de comparación de proporciones. Dependencia por marca, pérdida de seguimiento, muchas comparaciones o asignación desigual modifican el cálculo.

Para estimar una tasa única con un margen aproximado de ±5 puntos al 95%, la fórmula normal z²p(1-p)/e² requiere 139 observaciones si p=0,10 y 385 si p=0,50. Estimar efectos por país o calibración en grupos estrechos exige otras muestras; no se hereda la precisión del total.

Implicación práctica. Con pocas decenas de propuestas no es razonable demostrar que cambiar dos palabras aumenta el cierre dos puntos. Sí puede detectarse un error grave de comprensión, aprender objeciones y acumular evidencia sobre hipótesis prioritarias.

No parar un test convencional en cuanto aparece p menor que 0,05. Si se desea monitorización continua, definir un método secuencial válido y su regla de decisión. No usar la potencia calculada después con el efecto observado para rescatar un resultado incierto; informar tamaño del efecto e intervalo.

**[p.19]**

## 18 Calibración y comprobación de la precisión

Un motor calibrado que asigna alrededor del 30% a muchos casos comparables debería observar una frecuencia cercana al 30% en ese grupo, dentro del error de muestreo. No significa que se pueda comprobar un "30% verdadero" observando la única decisión de una marca.

Guo y colaboradores mostraron que redes con buen rendimiento de clasificación pueden estar mal calibradas, y evaluaron métodos de recalibración. En tu aplicación habría que comparar ajustes sencillos con alternativas flexibles usando datos separados; calibrar y evaluar con los mismos resultados produce optimismo. [S29]

| Medida | Para qué sirve | Limitación |
|---|---|---|
| Brier y log loss | Evaluar probabilidades frente a resultados | Deben compararse con la tasa base y segmentarse |
| Curva y pendiente de calibración | Detectar exceso de confianza y sesgo | Requieren muestra y bandas de incertidumbre |
| PR AUC y precisión a un cupo | Evaluar selección cuando hay pocos positivos | No certifican probabilidades ni causalidad |
| Margen por oportunidad y por hora | Medir valor comercial realizado | Puede tener demora y alta variabilidad |
| Cobro, cancelación y renovación | Medir calidad posterior al sí | Deben conservar ventana y denominador |
| Cobertura de intervalos | Comprobar incertidumbre predictiva | No garantiza cada caso individual |

La predicción conformal puede crear conjuntos o intervalos con cobertura marginal bajo condiciones como intercambiabilidad. No convierte automáticamente un score en probabilidad personal calibrada y no garantiza cobertura condicional para cada marca. Un cambio de mercado puede invalidar garantías de métodos estándar. [S30]

Diseño de validación. Entrenar con pasado, ajustar con un periodo posterior y reservar un periodo final sin tocar. Agrupar versiones y oportunidades relacionadas para evitar fugas. Medir por separado repetición con marcas conocidas y generalización a marcas nuevas; reservar países cuando se evalúe entrada a mercados nuevos.

Criterio para desplegar. Superar una base simple con incertidumbre cuantificada en las métricas prioritarias; no deteriorar de forma material el margen o la calibración en segmentos importantes; comprobar seguimiento y datos; y conservar opción de volver a la versión anterior. Los umbrales concretos se fijan según el coste de equivocarse y la precisión disponible, no como números decorativos.

**[p.20]**

## 19 Simulación y decisiones robustas

Simular un millón de escenarios es técnicamente factible para modelos de coste moderado. Cada escenario debe proceder de distribuciones justificadas de aceptación, costes, cobro o rendimiento, preservando sus dependencias. Si los supuestos son débiles, más simulaciones solo calculan con mayor precisión una respuesta basada en supuestos débiles.

En un cálculo Monte Carlo ordinario, el error numérico de estimar una media suele reducirse en proporción a 1 dividido entre la raíz del número de simulaciones, bajo condiciones regulares. Eso no reduce automáticamente la incertidumbre de los datos ni corrige el modelo. Un millón de muestras simuladas no equivale a un millón de marcas observadas.

Para cada alternativa se mostrarían valor esperado, riesgo de margen negativo, percentiles de resultado, carga de trabajo y sensibilidad a supuestos. Los percentiles se etiquetan como resultados de escenario cuando no hay validación empírica de las distribuciones.

Valor de la información. Si conocer el alcance real en una ciudad cambiaría la elección entre dos propuestas, ese dato puede ser valioso. Si ninguna conclusión cambia al variar razonablemente una variable, investigar más esa variable tiene poco valor de decisión. Se prioriza información por su capacidad de reducir una pérdida relevante.

### Política de abstención propuesta

| Situación | Respuesta del sistema |
|---|---|
| Sin acuerdos observados comparables | Diagnóstico y escenarios; no porcentaje validado |
| País o sector nuevo | Intervalos más amplios y validación de transporte |
| Dos ofertas con valores casi iguales | Mostrar empate práctico y criterio humano |
| Falta una condición de coste decisiva | Solicitarla al usuario o mostrar sensibilidad |
| Probabilidad fuera del rango comprobado | No presentarla como calibrada |
| Datos contradictorios o vencidos | Resolver fuente o degradar certeza |

Una salida de calidad puede recomendar posponer, cambiar el objetivo o descartar una marca. Obligar al motor a encontrar siempre una propuesta ganadora incentiva sobreconfianza. La opción "no contactar en estas condiciones" también tiene valor económico.

La explicación final debe mostrar qué hechos sostienen la recomendación, cuáles son supuestos y qué observación podría revertirla. Esto permite tomar decisiones aun cuando el modelo no pueda ofrecer una cifra precisa.

**[p.21]**

## 20 Tres ejemplos de aplicación adaptativa

Son situaciones hipotéticas para ilustrar decisiones. No describen información investigada de marcas reales ni probabilidades estimadas con tu historial.

### Restaurante local en España

Datos: creador gastronómico, oferta de 350 €, comida cubierta, relación fría y audiencia local todavía sin comprobar. El motor verifica ciudad, carta, estilo, canales y evidencia geográfica del talento. Si falta alcance pertinente, no promete llenar mesas. Puede recomendar una propuesta centrada en una experiencia gastronómica y contenido claramente delimitado, si ese valor está respaldado, o descartar el objetivo de captación local. El precio no cambia por iniciativa del modelo si tú lo fijaste.

Texto conceptual: "Una pieza que muestre cómo se vive vuestra propuesta gastronómica y explique qué pedir, con un recorrido claro por los productos que os distinguen". Se concreta con hechos del local. La utilidad depende de que la marca valore ese resultado; la redacción por sí sola no sustituye la evidencia.

### Restaurante en Venezuela

Datos: 550 dólares referidos al BCV, comida cubierta, producción local y relación fría. El motor conserva exactamente moneda y condiciones autorizadas. Calcula escenarios de margen según costes, fecha y forma de conversión pactada, sin trasladar automáticamente una tasa de cierre de España. Investiga propuesta gastronómica y referencias comparables del creador. Si el mejor concepto exige más producción, verifica que siga dentro del margen y del alcance ofrecido.

### Marca internacional relacionada con viajes

Datos: tres videos gastronómicos en distintos países y una oferta monetaria autorizada. El motor verifica los mercados servidos y la relación funcional entre servicio y recorrido. Puede proponer integración durante acciones concretas, como consultar una ruta o reservar, cuando esa función sea real. Los derechos de reutilización, pauta o exclusividad se tratan por separado; no se añaden para hacer la oferta más atractiva sin aprobación.

En los tres casos la estructura de razonamiento es compartida, pero cambian necesidad, evidencia, coste y medición. "Adaptativo" significa responder a diferencias verificadas, no cambiar colores, nacionalismos o adjetivos para dar apariencia de personalización.

Salida interna común: recomendación; alternativa; encaje; razones; riesgos económicos; datos ausentes; estado de validación; y siguiente acción. La propuesta que recibe la marca mantiene un mensaje simple.

**[p.22]**

## 21 Qué se puede automatizar y qué requiere control

La automatización debería descargar trabajo repetitivo y conservar trazabilidad. El problema no se resuelve añadiendo un único prompt gigantesco que diga "cruza millones de variables". Necesita un registro de datos, un modelo de decisión y mediciones reales.

| Puede automatizarse con controles | Requiere confirmación o evidencia adicional |
|---|---|
| Extraer carta, URLs y precios publicados | Interpretar un presupuesto interno no comunicado |
| Detectar fechas y contradicciones | Determinar impuestos sin situación fiscal |
| Ordenar ejemplos aprobados por similitud | Afirmar conversiones o audiencia no disponibles |
| Proponer y revisar textos | Cambiar condiciones económicas autorizadas |
| Calcular márgenes y tamaños de muestra | Elegir preferencias personales del talento |
| Actualizar métricas desde fuentes autorizadas | Declarar causalidad con información insuficiente |
| Detectar caída de calibración | Promover una nueva versión sin evaluación |

Registro de una recomendación. Identificador de oportunidad; instante de decisión; fuentes; atributos; versiones del extractor y predictor; acciones consideradas; restricciones; score o probabilidad con su estado; intervalo y método; cálculo económico; motivo de selección; aprobación cuando proceda; y archivo exacto enviado.

Privacidad y propiedad como requisitos funcionales. Conservar solo información pertinente, controlar acceso y comprobar permisos de APIs y licencias de datos o modelos. Las métricas privadas del talento requieren autorización. Las restricciones comerciales de componentes deben revisarse al implementarlos. Este diseño no presupone permiso para copiar código propietario o bases privadas.

Puertas de salida. Bloquear afirmaciones sin fuente, resultados inventados, condiciones no autorizadas, porcentajes sin identificación de su estado, documentos defectuosos y versiones no revisadas. Una puntuación estadística baja, por sí sola, no equivale a un defecto de archivo: puede requerir cambiar la estrategia.

Lo que se puede reutilizar de otros motores son métodos publicados, componentes con licencia y patrones de ingeniería. No se pueden extraer los secretos de un sistema cerrado a partir de una descripción comercial. La mejor posibilidad de superarlos en tu nicho es medir mejor el resultado que te importa y aprender de datos más pertinentes.

**[p.23]**

## 22 Plan de construcción y prueba de superioridad

Fase 1 Preparar el dominio. Leer el kit vigente, inventariar historial, deduplicar oportunidades y separar reglas editoriales de datos de resultados. Definir éxito, ventana, costes y límites del talento. Entregable: diccionario de datos y auditoría de qué puede aprenderse realmente.

Fase 2 Construir el asistente de decisión. Automatizar investigación, evidencia, compatibilidad, escenarios económicos y QA. Puede aportar valor aunque todavía no publique probabilidades calibradas. Entregable: propuestas trazables y registro de desenlaces desde el primer envío.

Fase 3 Comparar predictores. Entrenar la base sencilla y candidatos tabulares con cortes temporales. Documentar intervalos, aprendizaje por tamaño de muestra y comportamiento por mercado. Entregable: informe de comparación y modelo autorizado para los contextos que supera.

Fase 4 Experimentar. Probar pocas hipótesis prioritarias, con potencia y política de seguimiento definidas. Usar asignación aleatoria antes de sistemas adaptativos complejos. Entregable: efecto sobre acuerdos y margen, con incertidumbre y registro de daños o costes.

Fase 5 Ampliar. Incorporar nuevos países, marcas y formatos como tareas de transporte que se validan. Añadir adaptación continua solo con monitorización y posibilidad de reversión. El modelo nuevo compite en sombra antes de reemplazar al vigente.

### Qué significa "el mejor" de forma comprobable

Se necesita un conjunto de oportunidades representativo, competidores definidos, presupuesto de cómputo comparable, datos finales reservados y una métrica principal acordada. Para tu negocio elegiría beneficio neto por oportunidad elegible, con límites de riesgo y carga, más calibración y calidad del acuerdo. La superioridad se afirma solo para el dominio, periodo y condiciones evaluados.

Microsoft documentó que menos de un tercio de las ideas examinadas en experimentos controlados movían las métricas que pretendían mejorar. Es un argumento a favor de comprobar las intuiciones, no una tasa aplicable a tus propuestas. [S31]

Lewis y Rao analizaron experimentos publicitarios con millones de personas y encontraron intervalos muy amplios para el retorno; el intervalo mediano superaba cien puntos porcentuales. Incluso con gran escala puede ser difícil medir efectos económicos pequeños frente a mucho ruido. [S32]

Tiempo y coste dependen de limpieza del historial, acceso a fuentes, integraciones, número de oportunidades y rigor exigido. La instrumentación puede construirse antes de tener evidencia suficiente; la validación comercial debe esperar a que existan resultados observables. Un calendario no crea muestra estadística.

**[p.24]**

## 23 Especificación para quien implemente el motor

### Mandato de construcción

Construir un sistema especializado en decisiones de colaboración entre marcas y creadores. Investigar cada oportunidad, generar alternativas dentro de las condiciones autorizadas, estimar resultados solo con respaldo suficiente, comparar utilidad económica y conservar trazabilidad. Mantener las reglas y activos aprobados del sistema vigente como configuración versionada.

### Requisitos obligatorios

1. Definir antes de entrenar qué se predice, en qué momento y durante qué ventana. Separar aceptación, cobro, ejecución y resultado de campaña.

2. Registrar una oportunidad por proceso comercial; conservar versiones y agrupar marcas relacionadas. No etiquetar silencio como rechazo explícito ni simular resultados para aumentar la muestra.

3. Mantener tres niveles de evidencia por campo: observado, inferido y supuesto, más el estado desconocido. Registrar fuente, fecha y versión histórica disponible al decidir.

4. Comparar tasa base, regresión regularizada, modelo jerárquico y candidatos tabulares pertinentes. Añadir complejidad solo cuando supere la referencia en evaluación temporal y utilidad.

5. Mostrar por separado compatibilidad, probabilidad, incertidumbre y estado de validación. Si no hay calibración comprobada, no presentar el porcentaje como precisión demostrada.

6. Optimizar margen y calidad de alianza bajo límites de tarifa, derechos, carga y afinidad definidos por el talento. No maximizar firmas sacrificando rentabilidad.

7. Investigar prioridades comerciales con fuentes públicas y datos autorizados. No inventar presupuesto, deseos privados, personalidad ni motivos de rechazo.

8. Usar experimentos para evaluar cambios. Registrar asignación y resultado; calcular potencia; limitar comparaciones; impedir fuga de información y conclusiones causales injustificadas.

9. Comprobar PDF, enlaces y formato de entrega independientemente de la evaluación comercial. Congelar el archivo enviado y relacionarlo con la predicción.

10. Conservar auditoría, validación por mercado, monitorización y reversión. Entregar al final un informe de pruebas que indique mejoras, incertidumbre y fallos, sin afirmar superioridad mundial no demostrada.

Criterio de aceptación del desarrollo. El sistema debe reconocer un dato ausente, abstenerse ante una predicción injustificada y detectar una oferta económicamente mala aunque parezca fácil de vender. Esas capacidades son parte de su inteligencia.

**[p.25]**

## 24 Riesgos que pueden engañar incluso a un motor avanzado

| Fallo | Ejemplo comercial | Defensa necesaria |
|---|---|---|
| Fuga temporal | Usar el precio negociado para predecir el primer sí | Reconstruir lo conocido al enviar |
| Sesgo de selección | Aprender solo de marcas contactadas a mano | Registrar elegibilidad y criterio de selección |
| Confusión causal | Atribuir a un título lo que produjo una rebaja | Experimentos o supuestos explícitos |
| Optimización de sustitutos | Ganar respuestas amables sin acuerdos rentables | Métrica principal económica y resultados finales |
| Dependencia | Cincuenta locales con un único comprador | Agrupar y ajustar inferencia |
| Cambio de distribución | Crisis, nueva plataforma o cambio de audiencia | Monitorizar, recalibrar y limitar uso |
| Transferencia negativa | Aplicar patrones de España a Venezuela | Validación local y efectos jerárquicos |
| Sobreajuste de búsqueda | Elegir la mejor entre miles de redacciones simuladas | Reservas reales y pruebas prospectivas |
| Autoconfirmación | Entrenar con las notas que la propia IA asignó | Etiquetas externas de resultados |
| Incertidumbre oculta | Publicar 87,43% sin soporte | Redondeo razonable, intervalos y abstención |

Lo que suele pasar desapercibido. La elección de marcas elegibles puede aportar más que retocar el copy. La integridad de las etiquetas puede valer más que un nuevo algoritmo. El coste de exclusividad puede superar el beneficio del contrato. La renovación y el cobro pueden ser mejores señales que una respuesta entusiasta. Son hipótesis operativas de este diseño, que deben verificarse con tu negocio.

No todo riesgo necesita otro modelo. Si una condición está prohibida por el talento, se filtra. Si un precio es fijo, se respeta. Si la fuente no existe, se conserva el desconocido. Reservar la estadística para la incertidumbre real evita usar complejidad para decisiones ya resueltas.

### Decisión recomendada

Construirlo es factible como sistema especializado, verificable y adaptativo. La primera versión debería mejorar investigación, encaje, claridad y control económico; la fiabilidad predictiva se gana al registrar resultados y superar pruebas futuras. No hay respaldo para garantizar aceptación, certeza universal o supremacía mundial desde el inicio.

La pregunta que debe gobernar cada mejora es: "¿Produce mejores decisiones comprobables para este talento y estas marcas, con menos errores y mejor rentabilidad?". Esa exigencia protege la ambición del proyecto de convertirse en una colección de porcentajes vistosos.

**[p.26]**

## 25 Qué aporta esta ampliación y qué falta para construir

El objetivo es competir por el mejor resultado comercial demostrado en alianzas con creadores. No basta con declarar que el motor es el más complejo, ni con que un proveedor gane un benchmark tabular. La comparación debe medir qué decisiones produce ante las mismas oportunidades, qué beneficio genera, cómo estima el riesgo y cuándo reconoce que faltan datos.

### Auditoría del primer informe

Los capítulos 1 a 24 aportan evidencia, criterios y una arquitectura conceptual. No bastaban por sí solos para implementar íntegramente un producto: faltaban contratos de datos, definición temporal de etiquetas, interfaces, selección operativa de modelos, manejo de fallos y pruebas de aceptación. Esta ampliación concreta esos componentes. Los capítulos iniciales siguen siendo necesarios para interpretar sus límites científicos.

| Nivel de resultado | Estado de este trabajo |
|---|---|
| Estudio científico y comparación de alternativas | Sí: fuentes identificadas, diferencias de calidad y alcance de los hallazgos. |
| Arquitectura y especificación de una implementación delimitada | Sí: decisiones de diseño, datos, flujo, modelos, interfaces y pruebas descritos. |
| Software completo, conectado a fuentes y desplegado | No: este entregable es un estudio, no un repositorio ejecutable ni una integración. |
| Predictor entrenado y calibrado para tus propuestas | No: requiere resultados reales, definiciones acordadas y evaluación temporal. |
| Superioridad frente a competidores | No medida: aquí se define el protocolo para demostrarla. |
| Base perfecta y mejor motor universal | No establecida; no es una propiedad que pueda demostrarse con esta investigación. |

### Qué significa "construible"

Un equipo puede usar esta especificación para implementar una primera versión funcional y contrastar que cumple su comportamiento esperado. Antes de producción debe resolver accesos, volúmenes, presupuesto técnico, identidades, jurisdicciones y preferencias económicas reales. Las elecciones iniciales indicadas son hipótesis de ingeniería reemplazables, no parámetros óptimos descubiertos.

La ambición aumenta de forma verificable: incorporar candidatos de frontera; probar su aportación individual; descartar los que empeoran las decisiones; mejorar cobertura por segmentos; y repetir una evaluación independiente. Un sistema que sabe abstenerse cuando no puede justificar una probabilidad puede ser más fiable, aunque resulte menos espectacular en una demostración.

No se ha localizado una base pública, representativa y autorizada con millones de colaboraciones aceptadas y rechazadas y sus condiciones completas. Tampoco se ha accedido a algoritmos privados ni a resultados internos de competidores. Esas ausencias son límites concretos de esta investigación.

**[p.27]**

## 26 Cartera de métodos: qué incorporar y qué poner a prueba

La arquitectura admite varios modelos sustituibles. Los siguientes compiten mediante el protocolo común de los capítulos posteriores; no se suman automáticamente. El modelo de referencia sencillo siempre permanece como control.

| Familia | Función y condición de uso |
|---|---|
| Regresión logística regularizada | Referencia interpretable para aceptación; comprueba si el resto aporta valor. |
| Modelo bayesiano jerárquico | Comparte información entre marcas y segmentos; expresa incertidumbre cuando hay pocos casos. |
| LightGBM y otros árboles potenciados | Candidato para relaciones no lineales en datos estructurados; requiere validación temporal. |
| AutoGluon | Compara y combina modelos tabulares; limitar tiempo, memoria y complejidad del ensamblaje. [S35] |
| TabPFN y TabICL | Candidatos preentrenados para tablas; probar disponibilidad, licencias, tamaño y transferencia al dominio. [S07, S08, S09, S10] |
| Modelos relacionales preentrenados | Usan conexiones entre tablas; candidatos cuando existe historial relacional suficiente. [S33, S34] |
| LLM con recuperación documental | Extrae hechos y redacta alternativas; sus juicios no son probabilidades comerciales calibradas. |
| Supervivencia y modelos de estados | Estiman tiempo hasta respuesta, firma o cobro, respetando observaciones aún pendientes. |
| Inferencia causal y efectos heterogéneos | Estiman mejoras atribuibles a cambios de oferta cuando el diseño permite identificarlas. [S26, S38] |
| Optimización multiobjetivo | Compara beneficio, restricciones, riesgo y preferencias del talento. [S36, S37] |
| Bandits y evaluación de políticas | Aprenden entre alternativas permitidas cuando hay seguimiento fiable y exploración autorizada. [S27, S28, S44] |
| Multicalibración y robustez | Investigan fiabilidad por grupos y sensibilidad a cambios plausibles de distribución. [S39, S45] |

### Decisión inicial

Para la primera versión: datos trazables, investigación de marca, generación estructurada, referencia logística, candidato jerárquico y un competidor tabular. Añadir un modelo relacional si la estructura de datos lo justifica. Activar aprendizaje de políticas después de validar resultados y propensiones. Es una secuencia para producir evidencia, no una renuncia a métodos avanzados.

No elegiría hoy un único producto como "el ganador mundial" para esta aplicación: no encontré una comparación pública que lo establezca. Dynamics y otros CRM son referencias comerciales útiles. Dynamics exige al menos 40 oportunidades ganadas y 40 perdidas en el periodo elegido para configurar su modelo; ese umbral de producto no demuestra suficiencia estadística. [S42]

**[p.28]**

## 27 Modelos relacionales: una alternativa especialmente pertinente

Una colaboración no vive en una sola fila. Conecta un creador, sus contenidos y audiencia, una marca, establecimientos, contactos, versiones de oferta, mensajes, contratos, facturas y campañas. Aplanarlo todo puede perder información o introducir duplicados. Por ello, el aprendizaje entre tablas relacionadas merece una prueba específica.

### Qué evidencia existe

RelBench v2, publicado en 2026 según la ficha de sus autores, reúne 11 conjuntos con más de 22 millones de filas y 29 tablas. Evalúa predicciones temporales en bases relacionales. Sus resultados favorecen métodos relacionales frente a determinadas referencias de tabla única; no evalúan este negocio de creadores. [S33]

KumoRFM-2, preprint de abril de 2026, combina aprendizaje en contexto y ajuste sobre bases relacionales. Sus autores lo evalúan en 41 conjuntos de referencia y reportan mejoras frente a otros enfoques. La documentación actual de NVIDIA RFM describe inferencias que aprovechan tablas conectadas y ejemplos históricos relevantes. Son un candidato de frontera y una capacidad documentada, respectivamente; no una validación independiente de aceptación de propuestas. [S34]

### Prueba concreta para este motor

Construir tres tareas: probabilidad de firma a 30 días; importe cobrado a 90 días desde firma; y probabilidad de una segunda colaboración dentro de 180 días. Cada tarea necesita su población, momento de observación y etiqueta. Los plazos son decisiones iniciales de producto y pueden cambiar según el ciclo comercial.

Comparar la misma población con: tabla agregada y regresión; tabla agregada y modelo tabular; modelo relacional usando las mismas fuentes disponibles antes de cada decisión. La división temporal debe excluir conexiones futuras. Si el grafo incluye una factura posterior a la propuesta, la aparente mejora puede ser fuga de información.

Evaluar por separado marcas conocidas, marcas nuevas con sector conocido y países nuevos. Una relación repetida con un cliente puede facilitar predicción, pero no prueba capacidad de captar otro cliente. El rendimiento global no debe ocultar esa diferencia.

### Condiciones de incorporación

Se adopta si mejora el objetivo predefinido con coste y latencia admisibles, mantiene calibración y permite procesar los datos bajo las condiciones contratadas. Si empata, se conserva el sistema más sencillo de mantener. La integración debe quedar detrás de una interfaz para poder reemplazar al proveedor.

Los modelos preentrenados reducen el esfuerzo de aprender desde cero; no generan el presupuesto privado de una marca, las propuestas que nunca registraste ni la preferencia real de su decisor. El preentrenamiento aporta regularidades previas, no observaciones nuevas de tu negocio.

**[p.29]**

## 28 Qué puede aportar una IA sin un gran historial propio

El hallazgo reciente más relevante es favorable, pero delimitado. Ashokkumar y colaboradores publicaron en Nature en julio de 2026 un archivo de 70 experimentos de encuesta estadounidenses, con 469 efectos y 119.330 participantes. Los pronósticos derivados de GPT-4 se correlacionaron con los efectos observados, también en estudios no publicados antes de su corte de entrenamiento. Sin embargo, sobreestimaron sistemáticamente los tamaños de efecto. En otro archivo de 15 megaestudios y 606 efectos, las correlaciones fueron menores. [S43]

Esta evidencia justifica investigar el uso de LLM para anticipar tendencias y seleccionar hipótesis prometedoras. No convierte a participantes simulados en compradores reales ni demuestra que el modelo conozca la decisión de una marca particular. Correlacionar bien el orden de efectos y acertar sus magnitudes son propiedades distintas.

### Uso propuesto de las simulaciones

Generar objeciones posibles, detectar ambigüedades, comparar comprensión del entregable y formular alternativas de valor. Cada resultado queda marcado como "simulado". El sistema puede decir que una versión merece probarse; no presentará un porcentaje de aceptación empírico porque cien personajes artificiales hayan contestado que sí.

### Diseño de la comprobación local

Archivar predicciones del LLM antes de conocer resultados. Compararlas con una regla sencilla, evaluadores humanos y el predictor tabular. Medir ordenación y error probabilístico por separado. Calibrar únicamente con datos históricos de entrenamiento; reservar un periodo posterior para evaluar. Documentar modelo, versión, prompt, documentos recuperados y fecha de corte.

Si una puntuación del LLM mejora fuera de muestra, puede incorporarse como una variable más. No se debe introducir el texto de una respuesta real de la marca en un predictor que pretende operar antes del envío. Tampoco usar varios jueces basados en el mismo modelo como si fueran experimentos independientes.

Otra pista útil: Packard y Berger estudiaron lenguaje concreto en atención al cliente y encontraron mejoras en satisfacción y disposición de compra en determinados experimentos. Esto apoya probar entregables y beneficios concretos en las propuestas; no fija una cantidad universal de palabras ni una fórmula comprobada para cerrar colaboraciones. [S48]

La conclusión operativa es combinar conocimiento previo, hechos actuales y aprendizaje propio. Con poca historia se puede ofrecer una buena investigación y decisiones condicionadas por escenarios. La afirmación de precisión comercial debe crecer al ritmo de la evidencia obtenida.

**[p.30]**

## 29 Contrato de resultados: qué predice exactamente

La unidad inicial será una oportunidad única: creador, marca, objetivo de colaboración y ventana comercial. Dentro de ella pueden existir varias versiones de oferta y mensajes. No se contarán como negocios independientes. El momento de decisión es t0; todas las entradas del pronóstico deben estar disponibles entonces.

| Resultado | Definición operativa propuesta |
|---|---|
| Respuesta a 14 días | Respuesta humana sustantiva dentro de 14 días del primer envío entregado; excluir respuestas automáticas. |
| Firma a 30 días | Acuerdo documentado y aceptado por ambas partes dentro de 30 días. Definir qué documentos califican antes de empezar. |
| Cobro a 90 días | Importe efectivamente recibido durante los 90 días posteriores a firma; convertir moneda con la regla fijada. |
| Margen neto | Cobros menos costes directos, comisiones y costes fiscales incluidos expresamente en el alcance. |
| Resultado de campaña | Métrica acordada con la marca, método de medición y ventana; atribución no equivale a incremento causal. |
| Repetición a 180 días | Segundo acuerdo dentro de 180 días de la primera firma. |
| Satisfacción del talento | Valoración declarada con escala y momento constantes; nunca inferir felicidad como un hecho. |

Los plazos anteriores son valores iniciales de diseño, no hallazgos científicos. Un país o sector con ciclos largos puede necesitar otros horizontes; se versiona la definición para no mezclar etiquetas incompatibles.

### Pendiente no significa rechazado

Para entrenar firma a 30 días se incluyen decisiones cuya ventana terminó y cuya observación es fiable. Antes del día 30, los casos sin firma permanecen pendientes. Una firma posterior vale cero para la etiqueta "firma dentro de 30 días", aunque se registra como éxito posterior. Si se pierde seguimiento, hay censura o etiqueta desconocida; no fabricar un rechazo.

Una oferta alternativa que no se envió no recibe la etiqueta del resultado de la oferta elegida. Ese error enseñaría al modelo resultados que nunca se observaron. Las decisiones de contactar, elegir paquete y redactar texto se registran separadamente para poder investigar sus efectos.

### No mezclar tareas

Predecir aceptación condicionada a contacto no equivale a estimar qué marca conviene contactar. Predecir cobro entre contratos firmados no equivale al valor esperado de una oportunidad nueva. El servicio debe indicar población, condición, horizonte y versión para cada probabilidad que devuelve.

**[p.31]**

## 30 Esquema relacional mínimo y metadatos obligatorios

Esta estructura conserva identidades y versiones para evitar que el motor aprenda con datos incompatibles. Las claves son internas; no se usa un nombre comercial como identificador estable. Todas las tablas incluyen tenant_id cuando exista más de una organización usuaria.

| Tabla y clave principal | Contenido y relaciones esenciales |
|---|---|
| talent / talent_id | País, disponibilidad, restricciones y perfil declarado; versiones de preferencias. |
| brand / brand_id | Identidad, sector, país y filiales; distinguir grupo empresarial y establecimiento. |
| contact / contact_id | Relación con brand_id, función profesional, canal y estado de contacto. |
| audience_snapshot / snapshot_id | talent_id, plataforma, periodo de métricas, geografía, fecha disponible y calidad de origen. |
| opportunity / opportunity_id | talent_id, brand_id, objetivo, t0, estado y política de seguimiento. |
| offer_version / offer_id | opportunity_id, versión, precio, moneda, entregables, derechos, plazo y hash del texto. |
| decision / decision_id | offer_id elegido, alternativas elegibles, política, propensiones y versiones del motor. |
| message_event / event_id | offer_id, canal, entrega, respuesta y marcas temporales; identificador externo para deduplicar. |
| outcome_event / outcome_id | opportunity_id, firma, cancelación, factura, cobro o campaña; importe y evidencia. |
| evidence / evidence_id | Entidad, hecho, valor, fuente, permisos, fechas y estado: observado, inferido o desconocido. |
| feature_snapshot / feature_id | decision_id, valores calculados, versión y referencias de evidencia. |
| prediction / prediction_id | decision_id, objetivo, horizonte, estimación, incertidumbre, cobertura y versión del modelo. |
| experiment_assignment / assignment_id | Unidad aleatorizada, brazo, probabilidad, semilla, fecha y protocolo. |
| preference_version / preference_id | talent_id, mínimos, pesos declarados, incompatibilidades y fecha de vigencia. |

### Reglas de integridad

Claves foráneas obligatorias; unicidad por oportunidad y número de versión; importes decimales con moneda ISO; porcentajes con escala explícita; horas en UTC y zona de negocio separada. Un evento importado dos veces no debe duplicar una firma. Las correcciones crean una nueva versión con referencia a la anterior.

Cada evidencia registra event_time, available_at e ingested_at: cuándo ocurrió, cuándo pudo conocerse y cuándo entró al sistema. Una fuente revisada conserva su versión previa. Para valores faltantes se guarda un motivo; cero, desconocido y no aplicable no son equivalentes.

Los documentos originales se guardan separados de las variables de entrenamiento, con control de acceso y su hash. Las relaciones por sí solas no autorizan a compartir contratos entre clientes ni a incorporar información privada a servicios externos.

**[p.32]**

## 31 Construcción temporal de variables y prevención de fugas

La regla de oro es reconstruir lo que el sistema podía saber al recomendar. No basta con filtrar por fecha del evento: una estadística de septiembre publicada en octubre no estaba disponible para una decisión de septiembre. Las uniones temporales de Feast son una referencia de implementación; la fecha de disponibilidad debe controlarse además en nuestro contrato. [S46]

### Ejemplo de consulta de evidencia disponible

```text
WITH ranked AS (
  SELECT d.decision_id, e.field_name, e.value_json,
         e.evidence_id,
         ROW_NUMBER() OVER (
           PARTITION BY d.decision_id, e.field_name
           ORDER BY e.available_at DESC, e.ingested_at DESC
         ) AS rn
  FROM decision d
  JOIN evidence e ON e.entity_id = d.brand_id
                 AND e.tenant_id = d.tenant_id
  WHERE e.event_time <= d.decided_at
    AND e.available_at <= d.decided_at
    AND e.ingested_at <= d.decided_at
)
SELECT decision_id, field_name, value_json, evidence_id
FROM ranked WHERE rn = 1;
```

Es SQL ilustrativo: decision puede obtener brand_id mediante opportunity y offer_version. El esquema físico debe mantener esa relación sin duplicar identidades. Las correcciones y retiradas se resuelven con su estado vigente en t0, nunca con el estado actual. La selección exige reglas por campo y fiabilidad; una fuente reciente no siempre reemplaza a una primaria mejor.

### Dos evaluaciones diferentes

Para reproducir el comportamiento histórico del producto se exige ingested_at menor o igual que t0. Para investigar un modelo retrospectivo con fuentes públicas que entonces existían pero aún no habíamos ingerido, se usa otro conjunto, expresamente etiquetado como reconstruido. Sus resultados no se presentan como rendimiento real en operación.

### Tratamiento de agregados

Las tasas previas de aceptación de una marca usan exclusivamente oportunidades resueltas y conocidas antes de t0. Las codificaciones por objetivo se calculan dentro de cada partición de entrenamiento. Los índices de recuperación no pueden contener cartas de rechazo, contratos o notas posteriores al envío evaluado.

La prueba de aceptación inserta deliberadamente un cobro futuro y una revisión macroeconómica posterior. Ninguno debe alterar la predicción reconstruida. También verifica zonas horarias, duplicados y mensajes reenviados. Una gran mejora que desaparece al corregir estas fugas no era capacidad predictiva aprovechable.

**[p.33]**

## 32 Libro de variables: información útil frente a combinaciones

La primera versión comienza con un conjunto manejable de variables estructuradas y representaciones de texto. El número exacto se decide por disponibilidad y evaluación, no por alcanzar millones. Millones de interacciones calculables no equivalen a millones de observaciones independientes.

| Grupo | Variables candidatas y precaución |
|---|---|
| Encaje real | Geografía de audiencia, temática, formato y objetivo declarado de marca; no confundir afinidad textual con necesidad comprobada. |
| Condiciones | Precio, moneda, entregables, revisiones, exclusividad, derechos, calendario y forma de pago. |
| Prueba de valor | Resultados anteriores verificables, comparabilidad de campaña y calidad de medición. |
| Momento y negocio | Apertura, campaña vigente, estacionalidad y capacidad operativa documentadas. |
| Relación | Contactos previos, acuerdos resueltos y función del destinatario, solo antes de la decisión. |
| Texto y estructura | Palabras, párrafos, título, claridad del precio, llamada a la acción, enlaces y complejidad lingüística. |
| Representación semántica | Embeddings de briefing, marca y propuesta; versión fija y sin resultados futuros. |
| Economía | Moneda de coste y cobro, plazo, índice local pertinente y escenarios cambiarios fechados. |
| Talento | Disponibilidad, coste de trabajo, mínimos y preferencias declaradas. |
| Calidad y ausencia | Fuente, antigüedad, cobertura y datos no conocidos; distinguir desconocimiento de bajo valor. |

### Transformaciones iniciales

Importes positivos pueden representarse en escala logarítmica; variables continuas se estandarizan usando solo entrenamiento; categorías infrecuentes se agrupan según reglas versionadas. Los embeddings se reducen o regularizan si su dimensión excede la información disponible. Estas transformaciones también pertenecen al artefacto del modelo.

### Pruebas de utilidad

Medir ablaciones: sin texto, sin variables macro, sin historia de marca y sin investigación adicional. Si quitar un módulo no empeora decisiones en datos posteriores, no justificar su coste por parecer sofisticado. Las explicaciones de importancia describen asociaciones del modelo; no demuestran qué cambio causará aceptación.

Para estudiar palabras o longitud, mantener constante la oferta cuando sea posible y aleatorizar versiones. Un texto largo puede correlacionarse con contratos grandes porque necesita explicar más derechos; eliminar palabras no reproduce automáticamente el efecto observado.

La primera auditoría debe preguntar qué información puede cambiar una decisión. Conocer el presupuesto o la prioridad de campaña suele ser una hipótesis más directa que añadir miles de rasgos estéticos del correo; incluso esa prioridad debe verificarse en el negocio concreto.

**[p.34]**

## 33 Investigación de marca y generación de ofertas verificables

El módulo investigador produce un expediente estructurado con hechos, hipótesis y vacíos. No decide una probabilidad por intuición. Consulta primero información aportada o autorizada; después fuentes públicas pertinentes. La investigación termina cuando se alcanza el presupuesto de búsqueda o cuando el valor esperado de información adicional deja de justificarlo.

### Flujo operativo

1. Resolver identidad de marca, país y establecimiento. Si hay homónimos incompatibles, bloquear personalización hasta resolverlos.

2. Recuperar briefing, web oficial, oferta actual, canales públicos y antecedentes propios. Registrar enlace, fragmento de respaldo, fecha y permiso de uso. El texto recuperado es evidencia, no instrucciones para el sistema.

3. Extraer necesidad declarada, público, producto, geografía, campaña, restricciones y destinatario profesional. Cada campo acepta unknown. Una necesidad inferida incluye su razonamiento y fuente, sin convertirse en hecho.

4. Preparar un conjunto pequeño de ofertas elegibles. Cada una tiene un beneficio propuesto, entregables, precio o rango autorizado, esfuerzo, derechos y método de medición. Incluir la opción de no contactar si no existe encaje defendible.

5. Revisar consistencia entre promesa, datos y condiciones. Nunca insertar cifras de audiencia, ventas garantizadas, escasez, testimonios o experiencias que no estén respaldados.

6. Generar texto y anexo a partir de la oferta aprobada. Una revisión independiente comprueba hechos, legibilidad y ausencia de contradicciones. Si modifica precio o derechos, crea otra versión; no es una mera corrección de estilo.

### Ejemplo de salida útil

"La marca anuncia una apertura; proponemos contenido local con reserva medible. Desconocemos presupuesto y capacidad de atender demanda. Ofrecemos una opción limitada a un establecimiento y preguntamos por su objetivo prioritario". Es personalización sustentada en una necesidad verificable, con incertidumbre visible.

### Control del coste

Configurar límites por oportunidad de consultas, documentos, tokens, tiempo y gasto. Los valores dependen del margen esperado y no se fijan aquí como universales. Reutilizar hechos vigentes mediante caché; invalidarlos por fecha, cambio de fuente o conflicto. Una investigación larga que no modifica la oferta puede ser económicamente peor.

El generador propone alternativas; el evaluador económico y probabilístico las compara. Mantener ese contrato evita que una explicación persuasiva sea confundida con una demostración de que la propuesta funcionará.

**[p.35]**

## 34 Núcleo probabilístico y política de incertidumbre

Para firma dentro de 30 días, una referencia jerárquica puede expresar:

logit(p_i) = beta0 + x_i beta + u_marca[i] + v_sector[i] + w_pais[i] + z_talento[i].

La observación y_i sigue Bernoulli(p_i) cuando su etiqueta está madura. Los efectos por entidad comparten distribuciones comunes; una marca sin historia recibe información del grupo y mayor incertidumbre. Si marcas y países están anidados, se modela esa estructura explícitamente para reducir problemas de identificación.

### Priors iniciales, no parámetros perfectos

Después de estandarizar variables, un punto de partida investigable es beta_j ~ Normal(0,1) y efectos de grupo ~ Normal(0,sigma_grupo), con sigma_grupo ~ HalfNormal(0,0.5). El intercepto puede centrarse en una tasa previa comparable documentada; si no existe, usar un prior amplio y comprobar sus implicaciones. Estos valores son decisiones propuestas: necesitan comprobaciones predictivas previas y sensibilidad a escalas alternativas.

No se introducirán cientos de coeficientes libres con unas pocas firmas. Se regulariza, se reduce dimensión y se comparan alternativas. Si se realiza inferencia bayesiana por muestreo, se comprueba convergencia y tamaño efectivo de muestra. Si se usa una aproximación, se declara y se revisa que no subestime incertidumbre.

### Qué devuelve la distribución

Puede dar una estimación de p y un intervalo posterior para esa probabilidad bajo el modelo. No es una garantía de que una marca individual aceptará, ni el intervalo de un resultado binario futuro. La incertidumbre estructural y el cambio de país pueden exceder la que representa el posterior.

### Calibración y abstención

Calibrar predicciones con una partición posterior al entrenamiento y anterior a la prueba final. Comparar un ajuste logístico de calibración con alternativas más flexibles solo si hay datos. Revisar curvas e intervalos por sectores amplios; investigar multicalibración en grupos con soporte suficiente. [S29, S39]

La salida tiene tres modos: calibrated, experimental o insufficient_evidence. Solo el primero presenta probabilidad como validada para su población y horizonte. Los otros permiten escenarios y priorización cualitativa, y explican qué falta. La marca puede ser nueva y aun así estar dentro de una población evaluada de marcas nuevas; la decisión no depende exclusivamente de cuántos ejemplos tenga esa marca.

El umbral de soporte se fija mediante precisión requerida y evaluación, no con una cifra universal de filas. Nunca se convierte una puntuación de 85 sobre 100 en "85 % de aceptación" por cambiarle la etiqueta.

**[p.36]**

## 35 Algoritmo de entrenamiento, comparación y publicación

El proceso produce un artefacto reproducible con datos, transformaciones, predictor y calibrador. No modifica el modelo en producción por cada respuesta recibida. Las incorporaciones se evalúan y publican como versiones identificables.

```text
freeze(label_definition, feature_schema, evaluation_protocol)
rows = build_point_in_time_dataset(cutoff)
rows = retain_observed_mature_labels(rows)
assert_no_future_information(rows)

train, calibration, test = chronological_split(rows)
# Todas las versiones de una oportunidad permanecen juntas.
# Definir además pruebas separadas de marcas/países nuevos.

for candidate in registered_candidates:
    config = tune_with_rolling_validation(train, candidate)
    model = fit(train, config)
    calibrator = fit_calibrator(model, calibration)
    package = freeze(model, calibrator, feature_pipeline)
    record_locked_test_metrics(package, test)

finalist = select_under_registered_rule()
evaluate_on_independent_future_holdout(finalist)
if all_release_gates_pass(finalist):
    register_version(finalist)
    deploy_shadow(finalist)
else:
    retain_current_model_and_record_failure()
```

### Separaciones necesarias

El test usado para seleccionar entre varios candidatos ya participa en la selección. Por eso el ganador debe confirmarse en otro periodo independiente, o mediante una evaluación anidada predefinida. Mirar repetidamente el mismo test y rediseñar hasta ganar sobreajusta la evaluación.

Si la meta es predecir futuras propuestas a marcas conocidas, estas pueden aparecer en entrenamiento con su historia previa. Si la meta es generalizar a marcas desconocidas, se requiere una prueba donde sus oportunidades estén fuera del entrenamiento. No mezclar las dos afirmaciones en una sola métrica.

### Registro mínimo por ejecución

Hash del conjunto y su definición, intervalo temporal, código, dependencias bloqueadas, semillas, candidatos, presupuesto de búsqueda, parámetros, calibración y métricas con intervalos. Para APIs externas, conservar versión del servicio y evidencias de respuesta; una dependencia sin versión puede impedir reproducir exactamente el resultado.

La frecuencia de reentrenamiento responde a volumen de nuevas etiquetas maduras y a deterioro observado. Reentrenar a diario con tres resultados nuevos puede aumentar variabilidad sin aportar evidencia. Los datos recientes no deben sustituir sin análisis a segmentos históricos que siguen vigentes.

Los pesos de un ensamblaje se aprenden usando predicciones fuera de muestra dentro del entrenamiento. Promediar modelos muy similares no multiplica la información disponible ni justifica estrechar intervalos como si fueran observaciones independientes.

**[p.37]**

## 36 Interfaces: un contrato que un equipo puede implementar

El servicio separa investigación, recomendación y registro de resultados. Cada petición incluye una clave de idempotencia y una identidad autorizada; el mismo envío repetido no crea otra oportunidad. Los ejemplos son ilustrativos, no datos reales del negocio.

```text
POST /v1/recommendations
{
  "request_id": "demo-001",
  "as_of": "2026-10-03T12:00:00Z",
  "talent_id": "talent-demo",
  "brand_id": "brand-demo",
  "objective": "qualified_local_bookings",
  "country": "ES",
  "offers": [
    {"offer_id": "a", "price": "1200.00", "currency": "EUR",
     "deliverables": ["one_video"], "rights_days": 30}
  ],
  "preference_version": "pref-demo-1",
  "prediction_target": "signed_within_30d",
  "execution_mode": "draft_only"
}

{
  "request_id": "demo-001",
  "status": "insufficient_evidence",
  "recommended_offer_id": null,
  "acceptance_probability": null,
  "probability_interval": null,
  "ranking_basis": "needs_budget_and_cost_scenarios",
  "missing_fields": ["talent_cost", "brand_budget_status"],
  "evidence_ids": ["evidence-demo-1"],
  "model_version": null,
  "policy_version": "policy-demo-1",
  "label_version": "signed30-v1",
  "draft_id": "draft-demo-1"
}
```

Una respuesta validada añade población de referencia, horizonte, intervalo y tipo de incertidumbre, fecha de evaluación, cobertura y explicación apoyada en hechos. Un escenario económico utiliza un campo distinto de la predicción para que no se confundan supuestos y estimaciones entrenadas.

Otros contratos: POST /v1/research-jobs devuelve una tarea consultable; GET /v1/research-jobs/{id} devuelve expediente y fuentes; POST /v1/outcome-events incorpora evidencia de un resultado; GET /v1/predictions/{id}/audit reconstruye versiones y entradas. Los valores desconocidos se representan como null acompañado de motivo.

El endpoint de recomendación no envía mensajes, firma contratos ni cambia precios aceptados. La ejecución de una acción comercial requiere su propio permiso y registro. Esto permite probar el motor con oportunidades reales sin confundir análisis con actuaciones ya realizadas.

**[p.38]**

## 37 Optimización económica, preferencias y restricciones

El sistema primero descarta alternativas incompatibles con derechos, disponibilidad, mínimos económicos o reglas del negocio. Después compara las restantes. "Que digan sí" es una métrica insuficiente: un descuento excesivo puede aumentar aceptación y empeorar la vida y rentabilidad del talento.

### Una función inicial de valor por oportunidad

V(a) = P(firma30 dado x,a) × E(margen90 dado firma30,x,a) − coste_preparacion(a) − coste_contacto(a).

Las condiciones de ambas cantidades deben coincidir. El margen incluye cancelaciones y falta de cobro según el horizonte fijado. Si se decide separar firma, cobro y cumplimiento en etapas, se usan probabilidades condicionales consistentes; no se multiplican marginales suponiendo independencia.

### Preferencias del talento

Mantener como restricciones los mínimos irrenunciables. Para los demás criterios, mostrar una frontera de opciones: mayor margen, menor carga, mejor encaje o menor riesgo. Si el talento desea una puntuación única, documentar pesos o equivalencias que él haya aceptado. Un algoritmo no debe inventar cuánto vale su felicidad ni transformar una preferencia leve en una prohibición.

### Riesgo y escenarios

Evaluar retrasos, costes, impago y cambios cambiarios plausibles. Una alternativa es penalizar la pérdida esperada en la peor cola de escenarios mediante CVaR, declarando nivel de cola y aversión al riesgo. Los parámetros se eligen con el usuario; no hay un valor universal científicamente perfecto. El resultado depende de escenarios y dependencias modelados.

### Ofertas nuevas

Cambiar precio, derechos o entregables puede situar la propuesta fuera de los datos conocidos. Una predicción observacional no demuestra cuánto causará ese cambio. Limitar inicialmente la búsqueda a alternativas comparables y verificar las nuevas con experimentos o negociación documentada.

### Métodos avanzados a comparar

La optimización bayesiana multiobjetivo con restricciones ofrece métodos para explorar opciones cuando evaluarlas cuesta; BoTorch documenta implementaciones. No sustituye la observación real del resultado. [S37] El enfoque Smart Predict-then-Optimize entrena atendiendo al coste de decisión, además del error predictivo; su utilidad aquí tendría que compararse experimentalmente. [S36]

Para una cartera de colaboraciones se agregan límites de calendario, exclusividad, esfuerzo y concentración por cliente o moneda. La mejor oferta aislada puede no ser la mejor cartera. Si ninguna alternativa supera el mínimo defendible, la recomendación será renegociar, investigar o no proponer.

**[p.39]**

## 38 Valor de información: cuándo conviene saber más

La automatización más útil no siempre consiste en calcular más, sino en descubrir qué dato cambiaría la decisión. La prioridad puede ser saber quién decide, si existe presupuesto, cuándo empieza la campaña o qué derechos se requieren. Se compara el beneficio esperado de conocerlo con su coste y demora.

### Definición operativa

EVSI(q) = E_respuesta[max_a E(U(a) dado datos, respuesta_q)] − max_a E(U(a) dado datos).

El valor neto resta coste de búsqueda, contacto y retraso. Esta expresión necesita una distribución plausible de respuestas y utilidades; sin ella se presenta una sensibilidad por escenarios, no un importe aparentemente exacto. No se envía una consulta a la marca automáticamente sin permiso de contacto.

### Ejemplo hipotético de cálculo

Con la información actual, A y B ofrecen utilidades esperadas de 600 y 580 euros. Una consulta puede revelar dos estados equiprobables. En el primero, A y B valen 800 y 400; en el segundo, 400 y 760. Las medias coinciden con la información actual. Conocer el estado permitiría elegir 800 o 760: valor esperado 780. EVSI es 180 euros. Si investigar cuesta 40 y demora cuesta 20, el valor neto sería 120. Son supuestos didácticos, no resultados medidos.

### Política de investigación

El motor enumera vacíos relevantes, calcula o aproxima sensibilidad y prioriza la siguiente pregunta. Si un dato no cambia la alternativa recomendada en escenarios razonables, deja de buscarlo. Si dos propuestas están prácticamente empatadas, una pregunta barata puede ser mejor inversión que generar cientos de textos adicionales.

### Distinguir incertidumbres

Más información puede reducir desconocimiento sobre presupuesto, costes o preferencias. No elimina la variabilidad de las decisiones humanas ni eventos futuros imprevisibles. Si la pregunta exige una inferencia no verificable sobre la personalidad privada del decisor, se sustituye por información profesional pertinente y preferencias expresadas.

La política debe evaluarse: cuántos vacíos resolvió, qué decisiones cambió y si el beneficio posterior compensó tiempo y coste. La tasa de documentos recuperados o el número de variables rellenadas no demuestra que investigó mejor.

Esta capa permite pedir pocos datos al usuario y enriquecerlos de forma selectiva. Es compatible con empezar pequeño, pero reconoce que ciertos datos privados solo pueden conocerse preguntando o negociando.

**[p.40]**

## 39 Evaluación causal y aprendizaje entre alternativas

Un modelo puede acertar qué marcas suelen aceptar sin saber qué cambio de propuesta aumenta su aceptación. La segunda pregunta es causal. Priorizar marcas predispuestas y mejorar una oferta son efectos distintos; deben medirse por separado.

La opción preferente es aleatorizar entre ofertas elegibles dentro de grupos comparables. Cuando solo hay datos observacionales, explicitar supuestos de ausencia de confusión no medida, comparabilidad y soporte. Double/debiased machine learning ayuda a estimar efectos con modelos flexibles y separación de muestras; no elimina esos supuestos. [S38]

### Evaluación fuera de política

Para acciones discretas y recompensa r, un estimador doblemente robusto del valor de una política pi puede escribirse:

V_DR = promedio_i [ suma_a pi(a dado x_i) m(x_i,a) + pi(a_i dado x_i)/e(a_i dado x_i) × (r_i − m(x_i,a_i)) ].

e es la probabilidad de la acción bajo la política que generó los datos; m estima su recompensa. La identificación exige soporte y un mecanismo de asignación defendible. La propiedad de doble robustez depende de que al menos uno de esos modelos esté correctamente especificado, junto con los supuestos restantes; no es inmunidad a sesgos. [S28]

### Requisitos prácticos

Guardar el conjunto de acciones elegibles, probabilidades originales, política, contexto y restricciones al decidir. Si históricamente todas las marcas recibían siempre la misma oferta, no hay soporte para evaluar cualquier otra. Estimar propensiones retrospectivamente puede ser frágil si no se registraron los factores de decisión.

Comprobar pesos extremos y tamaño efectivo aproximado, ESS = (suma w)^2 / suma(w^2). Recortar pesos reduce varianza y puede introducir sesgo: documentar sensibilidad. Calcular intervalos agrupando por la unidad real de dependencia. Usar ajustes de recompensa y propensión fuera de la muestra evaluada.

### Bandit contextual

Solo se activa entre acciones autorizadas, con límites de riesgo y resultados rastreables. Puede comenzar comparando paquetes discretos; precios continuos requieren otro tratamiento del soporte. Métodos conservadores intentan limitar deterioro frente a una referencia bajo supuestos concretos. No trasladar esa garantía matemática sin verificar las condiciones del negocio. [S44]

El aprendizaje adaptativo produce selección cambiante. Para medir su utilidad, preservar un grupo comparador o un diseño de evaluación válido y registrar la asignación. Optimizar sobre sus propios resultados sin corregir cómo los seleccionó puede producir una ilusión de mejora.

**[p.41]**

## 40 Protocolo experimental y potencia estadística

Antes de experimentar, registrar población elegible, unidad aleatorizada, comparación, métrica primaria, horizonte, efecto mínimo relevante, tamaño de muestra, exclusiones y regla de parada. Esto impide escoger después el segmento o indicador que casualmente salió favorable.

### Prueba inicial de utilidad

Comparar proceso habitual frente a propuesta asistida por el motor dentro de oportunidades elegibles. Si varios contactos pertenecen a la misma marca y pueden compartir mensajes, aleatorizar por marca o grupo comercial. No tratar sus respuestas correlacionadas como observaciones independientes. Un diseño por conglomerados puede requerir más muestra.

En la primera prueba, mantener iguales criterios de captación y seguimiento para aislar el efecto de la propuesta. Después probar una política completa de selección y oferta, cuya métrica incluya costes de investigación y oportunidades no contactadas. Son preguntas experimentales diferentes.

| Elemento | Decisión que debe quedar escrita |
|---|---|
| Métrica primaria | Por ejemplo, margen neto por oportunidad elegible a un horizonte suficiente; si se usa firma30, declararla como resultado intermedio. |
| Métricas secundarias | Respuesta, firma, cobro, horas invertidas, cancelación y satisfacción declarada. |
| Potencia | Calcular con tasa o variabilidad inicial, efecto mínimo y dependencia por marca; simular si el diseño es complejo. |
| Datos pendientes | Esperar maduración o aplicar un análisis de tiempo hasta evento previamente especificado. |
| Comparaciones múltiples | Limitar hipótesis primarias; ajustar el análisis de exploraciones y exigir confirmación. |
| Parada | Horizonte fijo o método secuencial válido; no detener al primer valor p favorable. |

El capítulo 17 contiene ejemplos reproducibles de potencia para dos proporciones. No son requisitos universales: sin una tasa de referencia y un cambio mínimo relevante no existe un tamaño de muestra único que garantice precisión.

Las secuencias de confianza permiten ciertos seguimientos continuos con cobertura temporal bajo condiciones explícitas. Son una opción metodológica para reglas secuenciales; no arreglan un experimento pequeño, confundido o con recompensas mal definidas. [S41]

Registrar también resultados negativos. Si el motor aumenta firmas pero reduce margen o multiplica cancelaciones, no ganó la prueba económica. Si el intervalo todavía admite mejoras y daños relevantes, la conclusión es inconclusa. El sistema puede seguir usándose como apoyo de investigación sin atribuirle una mejora causal no demostrada.

**[p.42]**

## 41 Cómo demostrar superioridad frente a otros motores

"El mejor" necesita una población, fecha y criterio. La afirmación defendible sería: "mejor desempeño entre los sistemas evaluados, bajo este protocolo, para estas tareas y mercados". Afirmar superioridad mundial exigiría una cobertura comparativa que hoy no tenemos, incluidas soluciones privadas que quizá no permitan ser evaluadas.

### Comparadores mínimos

Proceso comercial habitual; regla por segmentos; regresión regularizada; modelo jerárquico; competidor tabular fuerte; modelo preentrenado tabular; modelo relacional si aplica; LLM con investigación y sin historial; y el sistema completo. Cuando sea accesible, incorporar el CRM comercial existente. Todos reciben información equivalente disponible al decidir.

Un presupuesto de ajuste comparable debe incluir cómputo, datos, trabajo humano y coste de inferencia. Además del rendimiento a presupuesto fijo, puede mostrarse una frontera rendimiento-coste. Un competidor mal configurado o con menos fuentes no prueba superioridad algorítmica.

| Dimensión | Evidencia requerida |
|---|---|
| Predicción | Brier y log loss, curvas de calibración e intervalos; AUC/PR-AUC como métricas complementarias de ordenación. |
| Negocio | Margen por oportunidad elegible, cobro, coste de preparación y beneficio incremental del experimento. |
| Generalización | Periodo futuro; marcas nuevas; sectores y países evaluados por separado. |
| Fiabilidad | Errores por segmento, casos desconocidos, abstención y degradación bajo cambios. |
| Operación | Latencia, coste, fallos, completitud de fuentes y reproducibilidad. |
| Talento y marca | Restricciones satisfechas, cumplimiento y satisfacción declarada con medición estable. |

### Diseño de confirmación

Separar selección de modelos de prueba final; fijar métricas y comparaciones; informar incertidumbre de diferencias; y repetir en organizaciones o mercados externos cuando sea posible. La prueba causal prospectiva pesa más para decidir utilidad comercial que ganar una métrica retrospectiva.

La independencia de la evaluación puede mejorar mediante auditoría externa y un protocolo publicado que proteja datos confidenciales. Una clasificación pública exige describir qué competidores participaron y qué datos pudieron usar; no convertir ausencias en derrotas.

TabArena y RelBench aportan referencias metodológicas y conjuntos de comparación. Sus ganadores son candidatos para nuestra evaluación, no campeones automáticamente transferibles al mercado de creadores. [S11, S33]

El benchmark debe conservar los casos difíciles y las abstenciones. Comparar únicamente oportunidades que el motor decidió atender puede inflar su resultado; se informa cobertura y valor sobre la población elegible completa.

**[p.43]**

## 42 Arquitectura de software y operación reproducible

Una implementación inicial puede usar PostgreSQL para entidades y eventos, almacenamiento de objetos para documentos y conjuntos congelados, un servicio Python de recomendaciones, una cola de tareas para investigación y un registro de modelos. Son elecciones de referencia; no resultados de una competición entre infraestructuras.

| Componente | Responsabilidad y contrato |
|---|---|
| Ingesta | Validar origen, esquema, identidades y duplicados; registrar errores recuperables. |
| Evidencias | Conservar hechos y versiones con fechas y permisos; buscar por entidad y pregunta. |
| Variables | Construir snapshots temporales deterministas; reutilizar transformaciones de entrenamiento en inferencia. |
| Modelos | Interfaz común predict(features, target, horizon); devolver soporte y versión junto a la estimación. |
| Evaluador de ofertas | Aplicar restricciones, escenarios, preferencias y valor esperado sin modificar hechos. |
| Generación | Redactar desde una oferta estructurada; validar promesas y coherencia con datos. |
| Orquestación | Gestionar tareas, tiempos límite, reintentos idempotentes y fallos parciales. |
| Auditoría | Reconstruir entradas, fuentes, decisiones, versiones y permisos por recomendación. |
| Observación | Vigilar integridad, disponibilidad, coste, cambios de población y resultados maduros. |

El registro de modelos puede implementarse con MLflow: versiones y alias facilitan identificar el modelo activo. La disponibilidad de un registro no valida su calidad; los criterios de promoción son nuestros. [S47]

### Escalabilidad

Para millones de registros, particionar por organización y tiempo, materializar agregados temporales y ejecutar procesos por lotes. Para recuperar documentos, combinar filtros de entidad/fecha con búsqueda textual y semántica. No enviar millones de filas a un LLM por oportunidad. El predictor recibe variables o subgrafos pertinentes; el generador recibe evidencia seleccionada.

Cada módulo informa coste y tiempo. Si falla una fuente macroeconómica, usar el último dato vigente solo con su fecha y regla de caducidad; si resulta esencial y no está disponible, abstenerse. Si cae el modelo avanzado, se puede usar una referencia validada y señalar el cambio, o devolver análisis sin probabilidad.

### Despliegue

Comenzar en modo sombra: el motor calcula pero no ejecuta decisiones comerciales. Comparar entradas y salidas con el flujo real. Después habilitar recomendaciones supervisadas y, únicamente para acciones autorizadas, automatización limitada. Conservar rollback al modelo anterior y bloquear una versión cuando falla integridad, permisos o definición de resultados.

**[p.44]**

## 43 Pruebas de aceptación: condiciones para ponerlo en uso

La especificación se vuelve comprobable con pruebas vinculadas al riesgo que evitan. No es necesario escribir pruebas que solo repitan la implementación; sí cubrir errores capaces de fabricar evidencia o alterar decisiones económicas.

| Caso de prueba | Resultado que debe exigirse |
|---|---|
| Evento duplicado | Una importación repetida no duplica firma, respuesta ni cobro. |
| Propuesta pendiente | No se etiqueta rechazo antes de madurar su horizonte. |
| Alternativa no enviada | No hereda éxito ni fracaso de la propuesta seleccionada. |
| Evidencia futura | Insertarla no cambia una predicción reconstruida en t0. |
| Marca homónima | No se mezclan oportunidades ni documentos de entidades diferentes. |
| Monedas incompatibles | No se suman importes sin conversión y fecha documentadas. |
| Coste desconocido | No se informa un margen neto como si fuera conocido. |
| Fuente contradictoria | Se conserva conflicto y resolución trazable. |
| Texto inventado | Se bloquea una afirmación factual sin soporte o se elimina de la propuesta. |
| Oferta prohibida | No aparece como recomendada aunque su puntuación sea alta. |
| Marca/país sin soporte | Se informa la cobertura disponible; puede abstenerse. |
| Probabilidad calibrada | Tiene objetivo, población, horizonte y evaluación asociada. |
| Fallo de proveedor | Se ejecuta la política de degradación y no se inventa una respuesta. |
| Separación de clientes | Ninguna petición devuelve contratos o documentos de otro tenant. |
| Reproducción | La versión y snapshot conservados permiten reconstruir la decisión. |

### Puertas de publicación

Integridad de datos y restricciones deben pasar. Para calidad predictiva, comparar con la referencia en el periodo independiente usando métricas e incertidumbre. Para utilidad comercial, fijar de antemano una mejora mínima relevante y límites de deterioro aceptables. Esos valores necesitan márgenes y costes reales; establecerlos aquí con números arbitrarios fingiría conocimiento del negocio.

La calibración se evalúa con gráficos y precisión suficiente, no solo con un ECE agregado. Un ECE bajo puede ocultar subgrupos pequeños con errores grandes. Si el intervalo de evaluación es demasiado ancho, declarar falta de precisión en vez de afirmar que no hay diferencias.

Un modelo puede pasar pruebas técnicas y no demostrar utilidad comercial; en ese caso permanece como candidato o herramienta de investigación. Superar una revisión de código no equivale a superar una prueba de negocio.

**[p.45]**

## 44 Economía y países: adaptación sin generalizaciones falsas

País, moneda, legislación, idioma y sector cambian restricciones y datos; no determinan por sí solos lo que una marca quiere. La adaptación individual combina hechos de esa empresa con información compartida y declara qué parte es observada y cuál procede del grupo.

### Paquete de país versionado

Configurar idioma y formatos; monedas de presupuesto, costes y cobro; zona horaria; calendario comercial; fuentes estadísticas; métodos de pago; reglas fiscales aplicables verificadas; y restricciones de derechos. Un país puede necesitar más de una regla según residencia, tipo de entidad y transacción. Este informe no calcula impuestos concretos ni sustituye esa configuración profesional.

### Variables económicas

Usar inflación, tipo de cambio, actividad sectorial o renta únicamente cuando exista una hipótesis y una fecha de disponibilidad pertinente. Series nacionales con pocos cambios no se convierten en miles de observaciones independientes por repetirse en muchas propuestas. La incertidumbre debe respetar la dependencia temporal y territorial.

### Evaluación de cambios

Simular escenarios declarados de costes, demora y cobro; informar qué recomendación cambia. Las tasas oficiales de referencia no son necesariamente el tipo ejecutable de una operación. Conservar fuente, hora, comisiones y supuestos. Evitar optimizar impuestos con información incompleta o datos desactualizados.

### Robustez y comportamiento adaptativo

La optimización robusta puede evaluar una familia definida de desviaciones respecto a la distribución histórica. La literatura sobre políticas robustas proporciona métodos, pero ninguna familia finita cubre todos los shocks posibles. [S45] Además, al cambiar qué marcas contactamos y qué ofrecemos, el propio sistema altera los datos que después observa: es un problema de predicción performativa. [S40]

Por ello, conservar métricas por cohortes de captación y versión de política, un comparador estable cuando sea viable y fechas de cambios comerciales. Una subida de aceptación tras abandonar sectores difíciles no demuestra mejor redacción para esos sectores.

La revisión por país no requiere entrenar modelos completamente independientes desde el primer día. Se puede compartir información mediante una jerarquía y evaluar dónde deja de transferir. Si un país nuevo está fuera de lo validado, ofrecer investigación, escenarios y una fase de aprendizaje local antes de anunciar precisión.

**[p.46]**

## 45 Frontera de investigación y ventaja difícil de copiar

No hay un secreto documentado que transforme patrones arbitrarios en certezas. Sí hay una ventaja acumulativa defendible: datos de decisiones y resultados bien definidos; experimentos; preferencias explícitas; acceso legítimo a información relevante; y un sistema que aprende con menor sesgo y coste que sus alternativas.

### Líneas avanzadas que merecen investigación

Multicalibración: intentar que las probabilidades sean fiables en familias de subgrupos verificables, no solo en promedio. Exige datos y criterios para esos grupos; no garantiza calibración individual para cada marca con dos observaciones. [S39]

Omnipredictors con restricciones: teoría que estudia cómo un predictor puede servir a una clase especificada de funciones de pérdida y restricciones mediante procesamiento posterior. El nombre no significa omnisciencia. Sus garantías se refieren a clases y supuestos definidos, no a cualquier situación del mundo. Aquí es una dirección experimental, no una capacidad ya implementada. [S50]

Aprendizaje federado: podría permitir colaboración entre agencias sin centralizar todos sus registros. El trabajo original demuestra un método de entrenamiento distribuido; no resuelve automáticamente privacidad, permisos, heterogeneidad o diferencias de etiquetas. Solo tendría sentido tras acordar un esquema común y evaluar sus costes. [S49]

Modelos relacionales y entrenamiento orientado a decisiones: comprobar si las conexiones entre entidades y la pérdida económica mejoran decisiones frente a enfoques tabulares bien ajustados. No asumir que dos métodos prometedores producen una mejora al combinarlos. [S34, S36]

### Qué se puede reutilizar

Reimplementar métodos publicados, usar bibliotecas y modelos conforme a sus condiciones, contratar predicciones de un proveedor o ajustar pesos disponibles. La destilación de un modelo puede aproximar comportamientos observados cuando su acceso y condiciones lo permiten; no revela su inteligencia interna ni garantiza superarlo. El rendimiento debe medirse con resultados externos al profesor.

Una base compartida de propuestas rechazadas y aceptadas, si se construye con autorización y buena cobertura, sería más valiosa que acumular ejemplos de textos exitosos sin sus denominadores. Debe incluir ofertas no aceptadas, seguimiento, motivos desconocidos y cambios de política; el sesgo de supervivencia puede destruir su utilidad.

La estrategia más exigente es mantener una cartera de hipótesis de investigación, presupuesto y criterios de descarte. "Explorar todas las opciones" no es una tarea finita; este estudio cubre las familias pertinentes identificadas y define cómo incorporar y evaluar nuevas candidatas.

**[p.47]**

## 46 Paquetes de construcción y entregables verificables

No sería honesto prometer un calendario y coste exactos sin equipo, infraestructura y acceso a datos. Sí se puede dividir la construcción en paquetes con una salida verificable, de manera que el siguiente dependa de evidencia del anterior.

| Paquete | Entregable y condición de salida |
|---|---|
| A. Contratos del negocio | Objetivos, horizontes, costes, preferencias, restricciones y esquema aprobados por responsables. |
| B. Datos y trazabilidad | Ingesta, identidades, snapshots, registros de resultados y pruebas de fugas superadas. |
| C. Investigación y propuestas | Expedientes con fuentes, ofertas estructuradas y borradores coherentes; revisión de una muestra representativa. |
| D. Referencias predictivas | Modelos sencillos reproducibles y evaluación temporal; modo sin probabilidad si no hay evidencia suficiente. |
| E. Competición de candidatos | Tabular, jerárquico y relacional cuando aplique; selección registrada y prueba independiente. |
| F. Decisión económica | Restricciones y escenarios comprobados con casos calculables; preferencias del talento conservadas. |
| G. Integración operativa | API, auditoría, acceso, costes, observación, modo sombra y recuperación ante fallos. |
| H. Validación prospectiva | Experimento dimensionado, resultados maduros y estimación del beneficio incremental. |
| I. Expansión | Evaluación específica al añadir países, sectores, creadores o nuevas acciones. |

### Qué debe contener el repositorio final

Esquema y migraciones; validadores de entrada; construcción temporal de variables; entrenamiento y calibración; evaluación reproducible; optimizador; generador con verificación; contratos API; pruebas pertinentes; configuración de despliegue; documentación operativa y tarjetas de datos y modelos. Este estudio describe su contenido esperado, pero no afirma haber producido esos archivos.

### Roles necesarios

Responsable comercial que defina valor y restricciones; ingeniería de datos y producto; modelado estadístico con experiencia experimental; y revisión de condiciones económicas locales cuando aplique. Una persona puede cubrir varios roles si tiene capacidad suficiente; su número depende del alcance.

### Criterio de finalización

"Construido" exige que el flujo funcione de extremo a extremo con datos autorizados, errores controlados y resultados rastreables. "Validado" exige pruebas en la población objetivo. "Superior" exige comparación justa. Son tres hitos distintos; entregar código no cumple automáticamente los otros dos.

Puede existir una versión útil antes de contar con miles de contratos: investigación, comparación económica, estructura de propuestas y registro del aprendizaje. En esa fase no se anuncia una precisión de aceptación que todavía no se ha medido.

**[p.48]**

## 47 Decisión final y cuestiones que la evidencia no resuelve

Sí existe una base suficientemente concreta para iniciar la construcción de un sistema ambicioso y comprobable. La propuesta es una plataforma de decisión comercial con investigación trazable, modelos intercambiables, probabilidades calibradas, restricciones económicas, preferencias declaradas y experimentación. Su ingeniería debe permitir reemplazar módulos según resultados, no quedar ligada a una supuesta fórmula definitiva.

No he encontrado una ingeniería perfecta ni evidencia de que esta combinación supere ya a todos los motores existentes. No he entrenado el sistema, accedido a millones de negociaciones privadas, comparado su rentabilidad prospectiva ni comprobado su precisión por país. Una investigación no puede certificar resultados de experimentos aún no realizados.

### Qué falta especificar con datos reales

El negocio y población inicial; fuentes y permisos; ciclo de venta; costes del talento; condiciones de pago; preferencias; definición de firma; seguimiento de rechazos y pendientes; infraestructura; volumen y presupuesto. Con esas entradas se concretan umbrales, potencia, modelos y prioridades. No hace falta que el usuario proporcione millones de filas, pero sí información verdadera sobre su operación.

### Qué queda abierto científicamente

Cuánto transfieren los modelos preentrenados a estas propuestas; qué información adicional produce valor; qué estilos funcionan en cada contexto; cuánto duran esas relaciones; qué grupos admiten calibración suficiente; y qué parte del beneficio procede de seleccionar marcas frente a cambiar las ofertas. Las respuestas requieren aprendizaje empírico local.

### La promesa que sí es defendible

Construir un motor que use la mejor evidencia disponible, investigue cada caso, compare alternativas coherentes con los intereses de ambas partes, mida sus errores y mejore con resultados. Puede aspirar a liderar un dominio delimitado; la superioridad se gana mediante comparaciones repetibles y decisiones rentables, no por una etiqueta comercial.

### Cómo leer las fuentes nuevas

Las referencias S33 a S50 amplían la frontera metodológica y la implementación. Se distinguen trabajos revisados por pares, preprints, documentación y resultados comunicados por autores o proveedores. Las fórmulas operativas, esquemas, interfaces, valores iniciales y criterios de publicación de esta ampliación son propuestas de ingeniería propias, no sistemas comercialmente validados en los artículos.

El informe conserva los metaanálisis y hallazgos históricos de los primeros capítulos. No calcula un nuevo metaanálisis: no dispone de un conjunto armonizado de estudios de aceptación B2B comparable con esta tarea. Sus metadatos documentan origen y alcance de la evidencia, sin presentarlos como datos de entrenamiento de colaboraciones.

**[p.49]**

## 48 Referencias y metadatos de la evidencia

Fecha de consulta de las fuentes: 3 de octubre de 2026. Las cifras de los ejemplos y de potencia son cálculos propios bajo los supuestos declarados. Los enlaces identifican la fuente comprobada. "Resumen" indica que no se verificó el texto íntegro; "proveedor" identifica evidencia de disponibilidad o resultados declarados por sus autores comerciales.

[S01] Benjamini, Y. y Hochberg, Y. (1995). Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. JRSS B, 57, 289-300. Artículo metodológico; resumen editorial comprobado. DOI: 10.1111/j.2517-6161.1995.tb02031.x.

https://academic.oup.com/jrsssb/article/57/1/289/7035855

[S02] Goldblum, M. et al. (2024). Position: The No Free Lunch Theorem, Kolmogorov Complexity, and the Role of Inductive Biases in Machine Learning. ICML, PMLR 235, 15788-15808. Artículo teórico y de posición; resumen comprobado.

https://proceedings.mlr.press/v235/goldblum24a.html

[S03] Minka, T., Cleven, R. y Zaykov, Y. (2018). TrueSkill 2: An improved Bayesian skill rating system. Microsoft Research, MSR-TR-2018-8. Informe técnico del desarrollador; evaluación en Halo 5.

https://www.microsoft.com/en-us/research/publication/trueskill-2-improved-bayesian-skill-rating-system/

[S04] LaLiga (2021 y documentación del proyecto). Beyond Stats en colaboración con Microsoft y Mediacoach. Fuente institucional; describe infraestructura y métricas, no una validación comercial.

https://www.laliga.com/noticias/laliga-y-microsoft-presentan-beyond-stats-un-proyecto-de-analisis-futbolistico-avanzado-que-profundiza-en-el-juego-de-cada-equipo

https://iaas-public-front-pro.laliga.com/beyondstats

[S05] Stern, D., Herbrich, R. y Graepel, T. (2009). Matchbox: Large Scale Bayesian Recommendations. WWW. Publicación de Microsoft Research; ficha y resumen comprobados.

https://www.microsoft.com/en-us/research/?p=157042

[S06] Ke, G. et al. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. NeurIPS. Artículo técnico del desarrollador y repositorio oficial.

https://www.microsoft.com/en-us/research/?p=439545

https://github.com/lightgbm-org/LightGBM

[S07] Hollmann, N. et al. (2025). Accurate predictions on small data with a tabular foundation model. Nature, 637, 319-326. DOI: 10.1038/s41586-024-08328-6. Artículo revisado por pares; resumen y fragmentos editoriales indexados comprobados; acceso directo limitado.

https://www.nature.com/articles/s41586-024-08328-6

[S08] Grinsztajn, L. et al. (2025; revisión de febrero de 2026). TabPFN-2.5: Advancing the State of the Art in Tabular Foundation Models. arXiv:2511.08667. Informe de autores; resumen comprobado.

https://arxiv.org/abs/2511.08667

**[p.50]**

## 49 Referencias sobre modelos y persuasión

[S09] Qu, J., Holzmüller, D., Varoquaux, G. y Le Morvan, M. (2026; revisión del 16 de septiembre). TabICLv2: A better, faster, scalable, and open tabular foundation model. arXiv:2602.11139. Preprint; resumen comprobado.

https://arxiv.org/abs/2602.11139

[S10] SAP News (15 de septiembre de 2026). TabPFN-3.5 Plus Now Available in SAP AI Core for Instant Business Predictions. Anuncio del proveedor; confirma disponibilidad declarada, no desempeño en este dominio.

https://news.sap.com/2026/09/tabpfn-35-plus-now-available-sap-ai-core-instant-business-predictions/

[S11] Erickson, N. et al. (2025). TabArena: A Living Benchmark for Machine Learning on Tabular Data. NeurIPS, Datasets and Benchmarks. Resumen de actas comprobado; DOI: 10.52202/085713-0519.

https://proceedings.neurips.cc/paper_files/paper/2025/hash/1697e3fb412da11dc9488249f9e7bbc9-Abstract-Datasets_and_Benchmarks_Track.html

[S12] Pan, M., Blut, M., Ghiassaleh, A. y Lee, Z. W. Y. (en línea 2024; volumen 2025). Influencer marketing effectiveness: A meta-analytic review. JAMS, 53, 52-78. 251 trabajos, 1.531 efectos; texto editorial accesible. DOI: 10.1007/s11747-024-01052-7.

https://link.springer.com/article/10.1007/s11747-024-01052-7

[S13] Barari, M. M., Eisend, M. y Jain, S. P. (en línea 2025; volumen 2026). A meta-analysis of the effectiveness of social media influencers: Mechanisms and moderation. JAMS, 54, 28-48. 71 trabajos, 135 estudios experimentales, 571 efectos. Texto editorial accesible. DOI: 10.1007/s11747-025-01107-3.

https://link.springer.com/article/10.1007/s11747-025-01107-3

[S14] Eisend, M., Niewiadomska, D. y van Noort, G. (5 de junio de 2026). Personalization in Marketing Communication: A Meta-Analysis. Journal of Marketing, publicación EXPRESS. 229 trabajos, 290 estudios, 1.536 efectos; resumen editorial comprobado, tablas completas no revisadas. DOI: 10.1177/00222429261460888.

https://journals.sagepub.com/doi/10.1177/00222429261460888

[S15] Perla, R. et al. (volumen de marzo de 2026). The (In)Effectiveness of Psychological Targeting: A Meta-Analytic Review. Psychology & Marketing, 43, 575-590. 41 estudios; resumen institucional de autores comprobado. DOI: 10.1002/mar.70073.

https://pure.uj.ac.za/en/publications/the-ineffectiveness-of-psychological-targeting-a-meta-analytic-re/

[S16] Matz, S. C. et al. (2017). Psychological targeting as an effective approach to digital mass persuasion. PNAS, 114, 12714-12719. Campañas de campo; resumen de autores y ficha PMC comprobados. DOI: 10.1073/pnas.1710966114.

https://pmc.ncbi.nlm.nih.gov/articles/PMC5715760/

**[p.51]**

## 50 Referencias sobre datos y métodos

[S17] Salvi, F., Horta Ribeiro, M., Gallotti, R. y West, R. (2025). On the conversational persuasiveness of GPT-4. Nature Human Behaviour, 9, 1645-1653. Experimento prerregistrado, N=900; resumen comprobado. Interpretar con S18. DOI: 10.1038/s41562-025-02194-6.

https://pubmed.ncbi.nlm.nih.gov/40389594/

[S18] Salvi, F. et al. (septiembre de 2026). Author Correction: On the conversational persuasiveness of GPT-4. Nature Human Behaviour. Contenido de la corrección comprobado en el repositorio de Princeton. DOI: 10.1038/s41562-026-02588-0.

https://collaborate.princeton.edu/en/publications/author-correction-on-the-conversational-persuasiveness-of-gpt-4/

[S19] UCI Machine Learning Repository. Bank Marketing. Documentación del conjunto de datos y variables. El conjunto clásico tiene 45.211 observaciones; no es una base de colaboraciones con creadores.

https://archive.ics.uci.edu/dataset/222/bank

[S20] Riley, R. D. et al. (2020). Calculating the sample size required for developing a clinical prediction model. BMJ, 368:m441. Metodología de tamaño de muestra; recomendaciones y resumen comprobados. Su aplicación comercial aquí es una adaptación conceptual.

https://www.bmj.com/content/368/bmj.m441

[S21] Instituto Nacional de Estadística de España. Referencia de la API JSON. Documentación oficial para consultar datos y metadatos.

https://www.ine.es/dyngs/DAB/index.htm?cid=1100

[S22] Fondo Monetario Internacional (abril de 2026). World Economic Outlook y documentación de la base. Distinguir observaciones, estimaciones y proyecciones, además de la fecha de información disponible.

https://data.imf.org/Datasets/WEO

https://www.imf.org/en/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026

[S23] Banco Mundial. About the Indicators API Documentation. Documentación oficial de acceso programático a indicadores.

https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation

[S24] Banco Central Europeo. Exchange rates, ECB Data Portal. Documentación oficial de series y alcance de tasas de referencia.

https://data.ecb.europa.eu/key-figures/ecb-interest-rates-and-exchange-rates/exchange-rates

[S25] Morkes, J. y Nielsen, J. (1997). Concise, SCANNABLE, and Objective: How to Write for the Web. Nielsen Norman Group. Experimento de usabilidad y escritura; descripción original comprobada mediante contenido indexado. No mide cierres B2B.

https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/

**[p.52]**

## 51 Referencias de causalidad y evaluación

[S26] PyWhy. Tutorial on Causal Inference and its Connections to Machine Learning Using DoWhy and EconML. Documentación oficial. Modelos y comprobaciones dependen de supuestos de identificación.

https://www.pywhy.org/dowhy/main/example_notebooks/tutorial-causalinference-machinelearning-using-dowhy-econml.html

[S27] Li, L., Chu, W., Langford, J. y Schapire, R. E. (2010). A Contextual-Bandit Approach to Personalized News Article Recommendation. WWW; arXiv:1003.0146. Evaluación de recomendación de noticias; resumen comprobado. DOI: 10.1145/1772690.1772758.

https://arxiv.org/abs/1003.0146

[S28] Dudík, M., Langford, J. y Li, L. (2011). Doubly Robust Policy Evaluation and Learning. ICML. Ficha y resumen en Microsoft Research; metodología de evaluación fuera de política.

https://www.microsoft.com/en-us/research/publication/doubly-robust-policy-evaluation-and-learning-2/

[S29] Guo, C., Pleiss, G., Sun, Y. y Weinberger, K. Q. (2017). On Calibration of Modern Neural Networks. ICML, PMLR 70, 1321-1330. Resumen de actas comprobado; evidencia sobre clasificación, no evaluación de este motor.

https://proceedings.mlr.press/v70/guo17a.html

[S30] Angelopoulos, A. N. y Bates, S. (2021; revisión 2022). A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification. arXiv:2107.07511. Tutorial metodológico; ficha y resumen comprobados.

https://arxiv.org/abs/2107.07511

[S31] Microsoft Bing (2013). Large Scale Experimentation at Bing. Descripción institucional de experimentación y resultados agregados de ideas probadas.

https://blogs.bing.com/search-quality-insights/2013/8/Large-Scale-Experimentation-at-Bing/

[S32] Lewis, R. A. y Rao, J. M. (2015). The Unfavorable Economics of Measuring the Returns to Advertising. Quarterly Journal of Economics, 130, 1941-1973. Análisis de experimentos publicitarios; resumen editorial comprobado. DOI: 10.1093/qje/qjv023.

https://academic.oup.com/qje/article-abstract/130/4/1941/1914592

### Sobre la verificabilidad de este informe

Las fuentes científicas apoyan principios y hallazgos delimitados. La arquitectura, los requisitos, las políticas de abstención y los ejemplos comerciales son propuestas de ingeniería de este estudio, no productos validados experimentalmente. La demostración pendiente es compararlos con el proceso actual en oportunidades reales.

La bibliografía mezcla trabajos históricos, revisados por pares, preprints, documentación y un anuncio reciente. Cada tipo está identificado para que novedad no se confunda con solidez ni un proveedor se convierta en juez definitivo de su propio rendimiento.

**[p.53]**

## 52 Referencias ampliadas: modelos y decisiones

Fuentes consultadas para la ampliación el 4 de octubre de 2026 UTC. Se conserva el corte editorial del estudio del 3 de octubre; no se incluyen hallazgos publicados después de esa fecha. "Resumen comprobado" no implica lectura íntegra ni reproducción de sus experimentos.

[S33] Gu, J. et al. (2026, revisión del 9 de mayo). RelBench v2: A Large-Scale Benchmark and Repository for Relational Data. arXiv:2602.12606. Ficha de autores: ICLR 2026. Resumen comprobado; cifras declaradas: 11 conjuntos, más de 22 millones de filas y 29 tablas. No evalúa propuestas con creadores.

https://arxiv.org/abs/2602.12606

[S34] Hudovernik, V. et al. (14 de abril de 2026). KumoRFM-2: Scaling Foundation Models for Relational Learning. arXiv:2604.12596. Preprint de autores; resumen comprobado. La documentación NVIDIA RFM describe el servicio y su procesamiento relacional; documentación de proveedor, no comparación independiente en este dominio.

https://arxiv.org/abs/2604.12596

https://docs.nvidia.com/sdgm/rfm/overview

[S35] AutoGluon. Tabular Prediction: In-depth. Documentación oficial consultada; describe ensamblajes, bagging y stacking. Las versiones deben bloquearse al implementar; no se atribuye una superioridad comercial por defecto.

https://auto.gluon.ai/stable/tutorials/tabular/tabular-indepth.html

[S36] Elmachtoub, A. N. y Grigas, P. (2022; preprint inicial de 2017). Smart "Predict, then Optimize". Management Science, 68, 9-26. DOI: 10.1287/mnsc.2020.3922. Resumen de autores comprobado. Metodología de aprendizaje orientado al coste de decisión; aplicación aquí propuesta.

https://arxiv.org/abs/1710.08005

[S37] BoTorch. Constrained Multi-Objective Bayesian Optimization. Tutorial oficial, documentación v0.17.0 consultada. Métodos computacionales y ejemplo reproducible del proveedor; no ensayo de propuestas comerciales.

https://botorch.org/docs/v0.17.0/tutorials/constrained_multi_objective_bo

[S38] Chernozhukov, V. et al. (2018). Double/debiased machine learning for treatment and structural parameters. The Econometrics Journal, 21, C1-C68. DOI: 10.1111/ectj.12097. Ficha y resumen editorial comprobados; metodología bajo supuestos de identificación.

https://academic.oup.com/ectj/article/21/1/C1/5056401

**[p.54]**

## 53 Referencias ampliadas: fiabilidad y experimentación

[S39] Hébert-Johnson, U., Kim, M., Reingold, O. y Rothblum, G. (2018). Multicalibration: Calibration for the (Computationally-Identifiable) Masses. ICML, PMLR 80. Resumen de actas comprobado; garantías para familias de grupos definidas, no certeza individual.

https://proceedings.mlr.press/v80/hebert-johnson18a.html

[S40] Perdomo, J., Zrnic, T., Mendler-Dünner, C. y Hardt, M. (2020). Performative Prediction. ICML, PMLR 119. Resumen de actas comprobado; formaliza situaciones donde decisiones del predictor modifican la distribución observada.

https://proceedings.mlr.press/v119/perdomo20a.html

[S41] Howard, S. R., Ramdas, A., McAuliffe, J. y Sekhon, J. (2021; preprint inicial de 2018). Time-uniform, nonparametric, nonasymptotic confidence sequences. Annals of Statistics. DOI: 10.1214/20-AOS1991. Ficha y resumen de autores comprobados.

https://arxiv.org/abs/1810.08240

[S42] Microsoft Learn. Configure predictive opportunity scoring. Documentación oficial de Dynamics 365 Sales consultada. Incluye requisito de configuración de 40 oportunidades ganadas y 40 perdidas en un periodo elegido de tres meses a dos años; no es cálculo de potencia para este proyecto.

https://learn.microsoft.com/en-us/dynamics365/sales/configure-predictive-opportunity-scoring

[S43] Ashokkumar, A., Hewitt, L., Ghezae, I. y Willer, R. (publicado el 8 de julio de 2026). Large language models can predict the results of social science experiments. Nature, 656, 115-122. DOI: 10.1038/s41586-026-10742-x. Artículo revisado por pares; resumen original indexado en PubMed y metadatos editoriales comprobados; acceso directo editorial limitado. Archivo principal: 70 experimentos, 469 efectos y 119.330 participantes. No se usan las cifras de versiones preliminares anteriores.

https://www.nature.com/articles/s41586-026-10742-x

https://pubmed.ncbi.nlm.nih.gov/42420458/

[S44] Takemura, K. (2023). Contextual Conservative Interleaving Bandits. ICML, PMLR 202. Resumen de actas comprobado. Método conservador bajo supuestos específicos; su garantía no se declara transferida al motor propuesto.

https://proceedings.mlr.press/v202/takemura23a.html

**[p.55]**

## 54 Referencias ampliadas: operación y líneas de frontera

[S45] Si, N., Zhang, F., Zhou, Z. y Blanchet, J. (2020). Distributionally Robust Policy Evaluation and Learning in Offline Contextual Bandits. ICML, PMLR 119. Resumen de actas comprobado; robustez respecto a una familia modelada de desviaciones, no protección frente a todo cambio.

https://proceedings.mlr.press/v119/si20a.html

[S46] Feast. Point-in-time joins. Documentación oficial consultada. Referencia para unir variables temporales; este diseño añade control explícito de disponibilidad e ingestión según la finalidad de evaluación.

https://docs.feast.dev/getting-started/concepts/point-in-time-joins

[S47] MLflow. Model Registry y Model Registry Workflows. Documentación oficial consultada. Versiones y alias de modelos; infraestructura de trazabilidad, no validación de su precisión.

https://mlflow.org/docs/latest/ml/model-registry/workflow/

[S48] Packard, G. y Berger, J. (2021). How Concrete Language Shapes Customer Satisfaction. Journal of Consumer Research, 47, 787-806. DOI: 10.1093/jcr/ucaa038. Resumen y fragmentos editoriales comprobados; experimentos de atención al cliente, no aceptación de patrocinios.

https://academic.oup.com/jcr/article/47/5/787/5873524

[S49] McMahan, H. B. et al. (2017). Communication-Efficient Learning of Deep Networks from Decentralized Data. AISTATS, PMLR 54. Resumen de actas comprobado. Método de aprendizaje distribuido; no garantiza por sí solo privacidad ni compatibilidad entre agencias.

https://proceedings.mlr.press/v54/mcmahan17a.html

[S50] Hu, L., Livni Navon, I., Reingold, O. y Yang, C. (2023). Omnipredictors for Constrained Optimization. ICML, PMLR 202. Resumen de actas comprobado. Garantías relativas a clases de funciones, hipótesis y restricciones definidas; no predictor universal de resultados individuales.

https://proceedings.mlr.press/v202/hu23b.html

### Estado de verificación del estudio

Se han contrastado fuentes públicas y documentado su nivel de acceso. No se han repetido los experimentos de los autores ni realizado ensayos con propuestas de este negocio. Los ejemplos aritméticos son demostraciones bajo supuestos declarados. La arquitectura sigue pendiente de implementación y validación prospectiva.
