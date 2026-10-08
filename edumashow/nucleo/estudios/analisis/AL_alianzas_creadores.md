# AL. Motor predictivo para propuestas y alianzas con creadores (análisis)

Análisis de Edumashow sobre el estudio de 55 páginas que Eduardo aportó. El texto completo y limpio está en `../texto/AL_alianzas_creadores.md`. Aquí van la lectura, los datos, las especificaciones y la interpretación. Las páginas (p.N) son las del pie del PDF; la portada es la p.1 y el capítulo n está en la p.n+1.

## 1. Ficha

| Campo | Dato |
|---|---|
| Título | Motor predictivo para propuestas y alianzas con creadores. Estudio científico y especificación ampliada de ingeniería. Versión 2 |
| Preparado para | Eduardo |
| Corte editorial | 3 de octubre de 2026. Las fuentes S33 a S50 se consultaron el 4 de octubre de 2026 UTC sin incluir hallazgos posteriores al corte |
| Naturaleza | Revisión dirigida de literatura (no es revisión sistemática PRISMA ni un metaanálisis nuevo) más una especificación de ingeniería propuesta por el propio estudio |
| Estructura | 54 capítulos. Cap. 1 a 6 evidencia, Microsoft, modelos y marketing. Cap. 7 a 24 objetivos, datos, países, incertidumbre, potencia y diseño conceptual. Cap. 25 a 47 auditoría, ingeniería operativa, validación, frontera y paquetes de construcción. Cap. 48 a 54 referencias (S01 a S50) con metadatos y enlaces |
| Lo que NO es | No hay software desplegado, ni predictor entrenado con resultados de Eduardo, ni precisión comercial medida (p.1, p.26). Los parámetros, ejemplos, esquemas y políticas son hipótesis de ingeniería reemplazables (p.26, p.48) |
| Tema web | No trata de webs de restaurante. Trata de un motor de decisión para propuestas de un creador a marcas (restaurantes incluidos como ejemplo) |

## 2. Tesis central y conclusiones

1. Es factible construir una plataforma que investigue marcas, compare ofertas, estime resultados con incertidumbre y aprenda qué decisiones producen alianzas rentables. No está demostrado que sea el mejor motor del mundo ni que exista una base perfecta (p.1, p.25, p.48).
2. Millones de patrones no garantizan acertar: un patrón puede ser real, accidental, transitorio o efecto de una variable oculta (p.3).
3. La ventaja defendible es acumulativa: datos de decisiones y resultados bien definidos, experimentos, preferencias explícitas, acceso legítimo a información pertinente y un sistema que aprende con menos sesgo y coste (p.46).
4. La primera versión debe mejorar investigación, encaje, claridad y control económico. La fiabilidad predictiva se gana registrando resultados y superando pruebas futuras (p.25).
5. Un sistema que sabe abstenerse cuando no puede justificar una probabilidad es más fiable aunque sea menos espectacular (p.26).
6. Pregunta que debe gobernar cada mejora: produce mejores decisiones comprobables, con menos errores y mejor rentabilidad, para este talento y estas marcas (p.25).
7. Tres hitos distintos: construido (flujo de extremo a extremo con datos autorizados), validado (pruebas en la población objetivo), superior (comparación justa). Entregar código no cumple los otros dos (p.47).

## 3. Mapa de capítulos

| Cap. | p. | Tema |
|---|---|---|
| 1 | 2 | Cómo se hizo y cómo interpretar la evidencia (jerarquía de evidencia) |
| 2 | 3 | Por qué millones de patrones no garantizan acertar (falsos positivos, no free lunch, seis cantidades) |
| 3 | 4 | Qué tienen realmente Microsoft y LaLiga (TrueSkill, Beyond Stats, Matchbox, LightGBM, DoWhy y EconML) |
| 4 | 5 | Candidatos actuales y cuál elegir (TabPFN, TabICL, TabArena, ensambles) |
| 5 | 6 | Marketing con creadores (dos metaanálisis) y regla de traducción científica |
| 6 | 7 | Personalización con evidencia y sus límites (metaanálisis, Perla, Matz, Salvi y su corrección) |
| 7 | 8 | Objetivo económico a optimizar (función de valor, ejemplo A/B/C) |
| 8 | 9 | Los pocos datos que aportaría el usuario y los que el sistema investiga |
| 9 | 10 | El historial que sirve para aprender (oportunidad como unidad, estados, fugas, sesgos) |
| 10 | 11 | Arrancar con pocos datos y usar datos externos |
| 11 | 12 | Adaptación por país y por negocio |
| 12 | 13 | Cómo investigar lo que la marca necesita (hecho, inferencia, supuesto, desconocido) |
| 13 | 14 | Texto y diseño que puedan entenderse (auditoría editorial) |
| 14 | 15 | Arquitectura del motor (10 módulos) |
| 15 | 16 | Núcleo probabilístico y ejemplo bayesiano |
| 16 | 17 | Qué cambios causan una mejora (primer experimento) |
| 17 | 18 | Potencia estadística y tamaño de muestra (tabla) |
| 18 | 19 | Calibración y comprobación de la precisión |
| 19 | 20 | Simulación, decisiones robustas, política de abstención |
| 20 | 21 | Tres ejemplos de aplicación adaptativa (España, Venezuela, marca de viajes) |
| 21 | 22 | Qué se puede automatizar y qué requiere control |
| 22 | 23 | Plan de construcción en cinco fases y prueba de superioridad |
| 23 | 24 | Especificación para quien implemente (diez requisitos obligatorios) |
| 24 | 25 | Riesgos que engañan incluso a un motor avanzado |
| 25 | 26 | Qué aporta la ampliación y qué falta para construir (auditoría del primer informe) |
| 26 | 27 | Cartera de métodos |
| 27 | 28 | Modelos relacionales |
| 28 | 29 | Qué puede aportar una IA sin gran historial propio |
| 29 | 30 | Contrato de resultados (qué predice exactamente) |
| 30 | 31 | Esquema relacional mínimo y metadatos obligatorios |
| 31 | 32 | Construcción temporal de variables y prevención de fugas |
| 32 | 33 | Libro de variables |
| 33 | 34 | Investigación de marca y generación de ofertas verificables |
| 34 | 35 | Núcleo probabilístico y política de incertidumbre |
| 35 | 36 | Algoritmo de entrenamiento, comparación y publicación |
| 36 | 37 | Interfaces (contrato de API) |
| 37 | 38 | Optimización económica, preferencias y restricciones |
| 38 | 39 | Valor de información |
| 39 | 40 | Evaluación causal y aprendizaje entre alternativas |
| 40 | 41 | Protocolo experimental y potencia |
| 41 | 42 | Cómo demostrar superioridad frente a otros motores |
| 42 | 43 | Arquitectura de software y operación reproducible |
| 43 | 44 | Pruebas de aceptación y puertas de publicación |
| 44 | 45 | Economía y países |
| 45 | 46 | Frontera de investigación y ventaja difícil de copiar |
| 46 | 47 | Paquetes de construcción y entregables |
| 47 | 48 | Decisión final y cuestiones sin resolver |
| 48 a 54 | 49 a 55 | Referencias S01 a S50 y estado de verificación |

## 4. Jerarquía de evidencia que fija el estudio (p.2)

| Evidencia | Qué permite concluir | Qué falta para el caso de Eduardo |
|---|---|---|
| Experimento propio aleatorizado | Efecto de una alternativa en el entorno probado | Replicación y transporte a otras marcas |
| Historial propio validado hacia el futuro | Capacidad predictiva dentro del contexto observado | Causalidad y rendimiento fuera del contexto |
| Metaanálisis pertinente | Patrones medios y heterogeneidad | Correspondencia con compradores B2B |
| Benchmark de modelos | Comparación en tareas y recursos definidos | Datos y objetivo comercial propios |
| Documentación o anuncio del proveedor | Funcionalidad o disponibilidad declarada | Reproducción independiente |
| Juicio de IA o de experto | Hipótesis y propuestas de diseño | Validación con resultados observados |

Reglas de lectura: los estudios de consumidores que ven publicaciones no estudian a un gerente que decide pagar una colaboración (distancia de aplicación). Dos metaanálisis no se suman: pueden compartir investigaciones y medir resultados distintos. Algunas fuentes se comprobaron solo por resumen o ficha institucional y la bibliografía lo indica.

## 5. Hallazgos y datos con su contexto

Nivel de evidencia: E1 fuente primaria o metaanálisis revisado por pares; E2 preprint, documentación o anuncio de proveedor, o fuente comprobada solo por resumen; E3 propuesta, criterio o cálculo ilustrativo del autor del estudio.

### 5.1 Estadística, modelos y benchmarks

| Id | p. | Hallazgo y cifra | Evid. | Límite que declara el estudio |
|---|---|---|---|---|
| H-AL-01 | 3 | Con 1.000.000 de hipótesis nulas verdaderas y nivel 0,05 se esperan 50.000 falsos positivos sin corrección. Bajo independencia, P(al menos un falso positivo) = 1 - 0,95^1.000.000, prácticamente 1 | E3 (cálculo) | Encontrar algo llamativo es fácil sin señal útil |
| H-AL-02 | 3 | Benjamini y Hochberg (1995) controlan la tasa de falsos descubrimientos bajo sus supuestos | E1 [S01] | Es herramienta de exploración; no se eligen ganadores en el mismo conjunto con el que se comprueban. Hacen falta datos reservados y replicación |
| H-AL-03 | 3 | Los teoremas de no free lunch tienen supuestos específicos (promediar sobre distribuciones amplias). No dicen que aprender sea inútil | E1 [S02] | Un algoritmo necesita supuestos y un dominio; la complejidad no garantiza superioridad |
| H-AL-04 | 3 | Seis cantidades distintas: exactitud, precisión (valor predictivo positivo), calibración, potencia, intervalo de incertidumbre, utilidad. Si el 95% de las marcas rechaza, un predictor que dice siempre no tiene 95% de exactitud y puede ser inútil | E3 | El objetivo debe combinar probabilidades fiables, selección de oportunidades y rentabilidad |
| H-AL-05 | 4 | En Halo 5, TrueSkill 2 acertó 68% frente a 52% de TrueSkill | E2 [S03] | Pertenece a esa evaluación, no a cierres comerciales. Lo trasladable es inferencia con incertidumbre; copiar porcentajes sería incorrecto |
| H-AL-06 | 4 | LaLiga describe más de 3,5 millones de puntos de datos por partido | E2 [S04] | Son mediciones repetidas de un entorno instrumentado, no millones de decisiones independientes. Azure es infraestructura, no un modelo estadístico |
| H-AL-07 | 4 | Tres piezas aprovechables: Matchbox (recomendación con metadatos más interacciones), LightGBM (árboles para datos estructurados), DoWhy y EconML (causalidad) | E1/E2 [S05, S06, S26] | Ninguna interpreta automáticamente lo que desea un comprador |
| H-AL-08 | 5 | TabPFN (Nature 2025): modelo fundacional tabular evaluado hasta 10.000 muestras y 500 variables | E1 [S07] | Sigue necesitando ejemplos y señales pertinentes de la tarea |
| H-AL-09 | 5 | TabICLv2 (preprint revisado en septiembre de 2026) y TabPFN 2.5 informan resultados competitivos; SAP anunció TabPFN 3.5 Plus (15 de septiembre de 2026) | E2 [S08, S09, S10] | Resultado de autores o del proveedor, sujeto a condiciones de comparación; no demuestra ser el mejor para propuestas de creadores |
| H-AL-10 | 5 | TabArena (NeurIPS 2025): la validación, el presupuesto de cómputo y los ensambles afectan las comparaciones; recomienda evaluar sistemas completos con condiciones comparables | E1 [S11] | Un modelo que domina un benchmark puede perder al cambiar prevalencia, calidad de datos o país |
| H-AL-11 | 28 | RelBench v2 (2026): 11 conjuntos, más de 22 millones de filas, 29 tablas; favorece métodos relacionales frente a referencias de tabla única. KumoRFM-2 (preprint abril 2026): 41 conjuntos de referencia | E2 [S33, S34] | No evalúa propuestas con creadores; documentación NVIDIA RFM es de proveedor |
| H-AL-12 | 27 | Dynamics 365 exige al menos 40 oportunidades ganadas y 40 perdidas para configurar su modelo | E2 [S42] | Umbral de producto; no demuestra suficiencia estadística |

### 5.2 Marketing con creadores y personalización

| Id | p. | Hallazgo y cifra | Evid. | Límite |
|---|---|---|---|---|
| H-AL-13 | 6 | Pan y colaboradores: 1.531 tamaños de efecto de 251 trabajos. Los factores relevantes cambian según el resultado (actitud, interacción, intención, compra, ventas). Elegir pruebas y entregables según el objetivo comercial, no usar seguidores como medida universal | E1 [S12] | Resultados medios sobre consumidores, no probabilidades de firma de una marca |
| H-AL-14 | 6 | Barari, Eisend y Jain: 71 trabajos, 135 estudios experimentales, 571 efectos. Eficacia distinta según resultado y contexto; efectos mediados por credibilidad y atractivo | E1 [S13] | Idem. El tamaño del creador no sirve igual para interacción que para intención de compra |
| H-AL-15 | 7 | Eisend, Niewiadomska y van Noort (junio de 2026): 1.536 efectos, 290 estudios, 229 trabajos. Beneficios medios de personalización y moderación por tipo de dato y nivel | E1 [S14] | Solo se comprobó el resumen editorial, no las tablas |
| H-AL-16 | 7 | Perla y colaboradores: 41 estudios sobre inferir personalidad desde huellas digitales y adaptar mensajes. Aproximadamente 5% de varianza explicada en personalidad; efectos conductuales insignificantes o muy pequeños; al controlar problemas metodológicos la eficacia de extremo a extremo se acerca a cero | E1 [S15] | Estudia una estrategia específica; no invalida toda personalización |
| H-AL-17 | 7 | Matz y colaboradores (2017): hasta 40% más clics y 50% más compras con mensajes alineados a personalidad en sus campañas | E1 [S16] | Máximos de condiciones particulares; no es efecto universal ni garantía para propuestas |
| H-AL-18 | 7 | Salvi y colaboradores: persuasión conversacional con GPT-4, experimento prerregistrado de 900 participantes. Corrección de septiembre de 2026: al comparar GPT-4 personalizado y sin personalizar, p corregido = 0,0678 (no 0,04) | E1 [S17, S18] | No mide cierres comerciales. No se puede establecer una ventaja adicional de personalizar; ausencia de significación tampoco demuestra igualdad |
| H-AL-19 | 25 | Microsoft documentó que menos de un tercio de las ideas probadas en experimentos controlados movían las métricas que pretendían mejorar | E2 [S31] | Argumento a favor de comprobar intuiciones, no una tasa aplicable a propuestas |
| H-AL-20 | 23 | Lewis y Rao: experimentos publicitarios con millones de personas dan intervalos muy amplios para el retorno; el intervalo mediano superaba cien puntos porcentuales | E1 [S32] | Aun con gran escala es difícil medir efectos económicos pequeños con mucho ruido |
| H-AL-21 | 14 | Morkes y Nielsen (1997): concisión, facilidad de escaneo y objetividad mejoraron la usabilidad medida; el conocido 124% describe ese experimento y esa métrica | E2 [S25] (experimento publicado por Nielsen Norman Group, no revisado por pares) | No equivale a 124% más ventas ni a una estructura obligatoria para PDF de creadores |
| H-AL-22 | 29 | Ashokkumar y colaboradores (Nature, 8 de julio de 2026): 70 experimentos de encuesta de EE. UU., 469 efectos, 119.330 participantes. Los pronósticos de GPT-4 se correlacionaron con los efectos observados (también en estudios no publicados antes del corte de entrenamiento) pero sobreestimaron sistemáticamente los tamaños de efecto. En otro archivo de 15 megaestudios y 606 efectos las correlaciones fueron menores | E1 [S43] | Correlacionar el orden de los efectos y acertar su magnitud son cosas distintas. No convierte personajes simulados en compradores reales |
| H-AL-23 | 29 | Packard y Berger: el lenguaje concreto mejoró satisfacción y disposición de compra en ciertos experimentos de atención al cliente | E1 [S48] | Apoya probar entregables y beneficios concretos; no fija un número de palabras |

### 5.3 Datos externos y tamaños de muestra

| Id | p. | Hallazgo y cifra | Evid. | Límite |
|---|---|---|---|---|
| H-AL-24 | 11 | No se halló una base pública verificada de millones de propuestas de colaboración con texto, oferta, aceptación o rechazo, contexto previo y resultado económico | E3 | No demuestra que no exista una privada; conseguirla exige acuerdos, licencias y comprobar comparabilidad |
| H-AL-25 | 11 | UCI Bank Marketing: 45.211 observaciones de campañas telefónicas de un banco portugués. La duración de la llamada no está disponible antes de llamar: usarla sería fuga de información | E2 [S19] | Sirve para enseñar métodos o probar una tubería, no valida el problema |
| H-AL-26 | 11 | No hay número mínimo universal de casos. Reglas fijas como diez eventos por variable son insuficientes (Riley y colaboradores) | E1 [S20] | La adaptación comercial conserva la lógica sin importar umbrales clínicos mecánicamente |
| H-AL-27 | 18 | Tamaño de muestra para comparar dos proporciones (alfa 0,05 bilateral, potencia 0,80, 1 a 1): 10% a 20% = 199 por grupo (398); 10% a 15% = 686 (1.372); 10% a 12% = 3.841 (7.682); 20% a 30% = 294 (588). Estimar una tasa con margen de 5 puntos al 95%: 139 observaciones si p = 0,10 y 385 si p = 0,50 | E3 (cálculo reproducible) | Pertenecen a este diseño; dependencia por marca, pérdidas, comparaciones múltiples o asignación desigual cambian el cálculo |
| H-AL-28 | 16 | Ejemplo bayesiano: 24 acuerdos en 100 oportunidades independientes y comparables, prior Beta(1,1), posterior Beta(25,77), media 24,51%, intervalo creíble central 95% de 16,70% a 33,26% | E3 | Es una tasa agrupada, no la probabilidad de un restaurante nuevo |
| H-AL-29 | 8 | Ejemplo económico: ofertas A, B, C a 350, 500 y 650 euros; coste si se acepta 150, 170, 200; margen 200, 330, 450; probabilidad supuesta 50%, 35%, 25%; preparación 10 euros; margen esperado por oportunidad 90, 105,50 y 102,50 euros | E3 | Supone cobro íntegro y costes fijos por caso. B gana, pero B menos C son solo 3 euros: con probabilidades inciertas no se finge ventaja concluyente |
| H-AL-30 | 39 | Valor de información: utilidades actuales A 600 y B 580; una consulta revela dos estados equiprobables (A 800 y B 400; A 400 y B 760). Elegir con el estado conocido vale 780, así que EVSI = 180 euros. Con investigación a 40 y demora a 20, valor neto 120 | E3 | Supuestos didácticos, no medidas |

## 6. Marco conceptual y modelos del estudio

### 6.1 Seis salidas que no deben mezclarse (p.16, p.35)

Compatibilidad editorial, probabilidad estimada, intervalo, tamaño de muestra relevante, resultados de calibración y distancia respecto al entrenamiento. Un 92 de 100 de afinidad nunca se convierte en 92% de aceptación; un 85 de 100 nunca pasa a 85% de aceptación por cambiar la etiqueta. El panel debe impedir esa confusión por diseño.

### 6.2 Tres modos de salida (p.11, p.35)

- Nivel inicial: diagnóstico de encaje y escenarios, sin porcentaje validado.
- Nivel intermedio: probabilidades provisionales con supuestos, tasa base e incertidumbre identificados.
- Nivel validado: probabilidades comprobadas en oportunidades posteriores y comparables.
- En la API: `calibrated`, `experimental`, `insufficient_evidence`. Solo `calibrated` presenta la probabilidad como validada para su población y horizonte.

### 6.3 Modelos y cartera (p.5, p.27)

Referencia permanente: tasa base y regresión logística regularizada. Candidatos: modelo bayesiano jerárquico (comparte información sin borrar diferencias), CatBoost o LightGBM, familia TabPFN o TabICL, AutoGluon (limitar tiempo, memoria y complejidad), modelos relacionales, ensamble, modelo de lenguaje con recuperación (extrae hechos y redacta alternativas, sus juicios no son probabilidades), supervivencia y modelos de estados (tiempo hasta respuesta, firma o cobro), inferencia causal y efectos heterogéneos, optimización multiobjetivo, bandits y evaluación de políticas, multicalibración y robustez. Decisión inicial: datos trazables, investigación de marca, generación estructurada, referencia logística, candidato jerárquico y un competidor tabular; modelo relacional solo si la estructura lo justifica; aprendizaje de políticas después de validar resultados y propensiones. No elegir un ganador mundial único.

### 6.4 Modelo probabilístico (p.16, p.35)

- logit(p) = intercepto + efecto país + efecto sector + efecto talento + efecto marca o grupo + efecto temporal + contribuciones de oferta y contexto.
- Forma jerárquica: logit(p_i) = beta0 + x_i beta + u_marca[i] + v_sector[i] + w_pais[i] + z_talento[i]; y_i ~ Bernoulli(p_i) con etiqueta madura.
- Priors iniciales a investigar, no óptimos: beta_j ~ Normal(0,1); efectos de grupo ~ Normal(0, sigma_grupo); sigma_grupo ~ HalfNormal(0; 0,5). Se necesitan comprobaciones predictivas previas y sensibilidad a escalas.
- Efectos regularizados: con pocos datos se acercan a la información compartida. Marcas nuevas con atributos y mayor incertidumbre. No cientos de coeficientes libres con pocas firmas. Comprobar convergencia y tamaño efectivo de muestra si hay muestreo.
- Retador no lineal: interacciones precio por formato, geografía por objetivo, relación previa por prueba elegida. Debe mejorar en datos futuros; no enumerar millones de interacciones y presentar el mejor ajuste como descubrimiento.
- Objetivo inicial: probabilidad de aceptación documentada en una ventana definida (por ejemplo 30 días) condicionada a lo disponible al enviar. No multiplicar probabilidades marginales de etapas como si fueran independientes.

### 6.5 Función de valor y economía (p.8, p.38)

- Valor de una acción = P(aceptación) x margen esperado si se acepta - coste de preparar y negociar - penalización de riesgo + valor futuro documentado (p.8).
- Versión operativa: V(a) = P(firma30 | x,a) x E(margen90 | firma30,x,a) - coste_preparación(a) - coste_contacto(a). Las condiciones de ambas cantidades deben coincidir; margen incluye cancelaciones e impago (p.38).
- El margen condicionado a aceptación incluye cobro esperado, producción, edición, traslados, comisiones, impuestos aplicables si están determinados, devoluciones y coste de oportunidad. La penalización de riesgo no duplica costes ya descontados. La renovación entra solo con evidencia o como escenario separado.
- Preferencias del talento: mínimos irrenunciables como restricciones; para lo demás, frontera de opciones no dominadas y análisis de sensibilidad. Nunca inventar cuánto vale su felicidad ni convertir una preferencia leve en prohibición.
- Riesgo: CVaR sobre la peor cola de escenarios (nivel de cola y aversión se eligen con el usuario). Beneficio de la marca: ventas incrementales, contenido reutilizable y posicionamiento, sin sumarlos dos veces.
- Cartera: calendario, exclusividad, esfuerzo, concentración por cliente o moneda; la mejor oferta aislada puede no ser la mejor cartera. Si ninguna alternativa supera el mínimo defendible: renegociar, investigar o no proponer.
- Métodos a comparar: optimización bayesiana multiobjetivo con restricciones (BoTorch, S37), Smart Predict-then-Optimize (S36).

### 6.6 Valor de la información (p.20, p.39)

EVSI(q) = E_respuesta[max_a E(U(a) | datos, respuesta_q)] - max_a E(U(a) | datos). Valor neto = EVSI menos coste de búsqueda, contacto y demora. Sin distribución plausible, se presenta sensibilidad por escenarios, no un importe exacto. Se deja de investigar cuando el dato no cambia la alternativa recomendada o cuesta más que su beneficio. Si dos propuestas están casi empatadas, una pregunta barata puede valer más que cientos de textos. Nunca se envía consulta a la marca sin permiso de contacto.

### 6.7 Causalidad y experimentos (p.17, p.40, p.41)

- Predecir (qué suele pasar en casos parecidos) no es decidir (qué cambiaría enviar A en vez de B). Las propuestas caras pueden cerrar más porque se reservan a marcas con más presupuesto.
- Primer experimento: apertura centrada en un objetivo observable de la marca frente a la habitual. Mantener precio, entregables, calidad visual, canal y política de seguimiento. Aleatorizar entre oportunidades elegibles, estratificar por país y tipo de negocio; si una cadena comparte decisor, aleatorizar por grupo (diseño por conglomerados, más muestra).
- Registrar antes: población elegible, unidad aleatorizada, comparación, métrica primaria, horizonte, efecto mínimo relevante, tamaño de muestra, exclusiones, regla de parada. Analizar según asignación inicial, documentando excepciones y pérdidas.
- Métrica primaria sugerida: margen neto por oportunidad elegible. Si se usa firma a 30 días, declararla resultado intermedio. Secundarias: respuesta, firma, cobro, horas, cancelación, satisfacción declarada.
- Parada: horizonte fijo o método secuencial válido (secuencias de confianza, S41). No parar al primer p menor que 0,05. No usar potencia calculada después con el efecto observado.
- Registrar resultados negativos: si sube la firma pero baja el margen o suben las cancelaciones, no ganó la prueba económica. Si el intervalo admite mejoras y daños relevantes, la conclusión es inconclusa.
- Con pocas oportunidades, priorizar diferencias estratégicas grandes sobre decenas de variaciones de palabras.
- Evaluación fuera de política (doubly robust): V_DR = promedio_i [ suma_a pi(a|x_i) m(x_i,a) + pi(a_i|x_i)/e(a_i|x_i) x (r_i - m(x_i,a_i)) ]. Exige guardar probabilidades de asignación originales, soporte suficiente y mecanismo de asignación defendible. Tamaño efectivo ESS = (suma w)^2 / suma(w^2). Recortar pesos reduce varianza y puede introducir sesgo. Intervalos agrupando por la unidad real de dependencia. La doble robustez no es inmunidad a sesgos.
- Bandit contextual solo entre acciones autorizadas y con resultados rastreables; la exploración nunca autoriza precios por debajo del límite, promesas no demostradas ni derechos no aprobados. Preservar un grupo comparador al usar aprendizaje adaptativo. Li y colaboradores informaron 12,5% más clics que un bandit sin contexto en recomendación de noticias (antecedente, no porcentaje transferible).
- Double/debiased machine learning (S38) estima efectos con modelos flexibles y no elimina los supuestos de identificación.

### 6.8 Calibración, validación y despliegue (p.19, p.36, p.44)

- Medidas: Brier y log loss (comparar con la tasa base y segmentar), curva y pendiente de calibración, PR AUC y precisión a un cupo, margen por oportunidad y por hora, cobro, cancelación y renovación, cobertura de intervalos.
- Calibrar y evaluar con los mismos resultados produce optimismo. Redes con buen rendimiento pueden estar mal calibradas (Guo, S29). Predicción conformal da cobertura marginal bajo intercambiabilidad, no probabilidad personal calibrada (S30).
- Diseño: entrenar con el pasado, ajustar con un periodo posterior y reservar un periodo final intacto. Agrupar versiones y oportunidades relacionadas. Medir por separado marcas conocidas y marcas nuevas; reservar países para evaluar mercados nuevos.
- Criterio para desplegar: superar una base simple con incertidumbre cuantificada; no deteriorar de forma material margen o calibración en segmentos importantes; comprobar seguimiento y datos; conservar reversión. Umbrales según el coste de equivocarse, no decorativos.
- Pseudocódigo (p.36): congelar definición de etiqueta, esquema de variables y protocolo; construir dataset punto en el tiempo; quedarse con etiquetas maduras; afirmar que no hay información futura; división cronológica; ajuste con validación móvil; calibrador; congelar paquete; métricas de prueba bloqueadas; finalista por regla registrada; evaluar en reserva futura independiente; si pasan todas las puertas, registrar versión y desplegar en sombra; si no, conservar el modelo actual y registrar el fallo. El test usado para elegir entre candidatos ya participó en la selección: confirmar en otro periodo o con evaluación anidada predefinida.
- Registro mínimo por ejecución: hash del conjunto y su definición, intervalo temporal, código, dependencias bloqueadas, semillas, candidatos, presupuesto de búsqueda, parámetros, calibración, métricas con intervalos y, para APIs externas, versión del servicio y evidencia de respuesta.
- Reentrenamiento por volumen de etiquetas maduras y deterioro observado (no a diario con tres resultados). Pesos de ensamble con predicciones fuera de muestra; promediar modelos parecidos no multiplica la información ni justifica intervalos más estrechos.
- Puertas de publicación: integridad de datos y restricciones deben pasar; calidad predictiva frente a la referencia en periodo independiente; utilidad comercial con mejora mínima relevante y límites de deterioro fijados de antemano con márgenes y costes reales. Calibración con gráficos y precisión suficiente, no solo ECE agregado. Si el intervalo de evaluación es ancho, declarar falta de precisión, no ausencia de diferencias. Un modelo puede pasar pruebas técnicas y no demostrar utilidad comercial: queda como candidato o herramienta de investigación.
- Despliegue (p.43): modo sombra, luego recomendaciones supervisadas, luego automatización limitada solo para acciones autorizadas; rollback al modelo anterior; bloquear una versión si falla integridad, permisos o definición de resultados.

### 6.9 Simulación y abstención (p.20)

Un millón de escenarios es factible pero solo calcula con precisión una respuesta basada en los supuestos. El error de Monte Carlo baja como 1 dividido entre la raíz del número de simulaciones y no corrige el modelo ni reduce la incertidumbre de los datos. Por alternativa: valor esperado, riesgo de margen negativo, percentiles, carga y sensibilidad; los percentiles son resultados de escenario si no hay validación empírica.

| Situación | Respuesta del sistema |
|---|---|
| Sin acuerdos observados comparables | Diagnóstico y escenarios, sin porcentaje validado |
| País o sector nuevo | Intervalos más amplios y validación de transporte |
| Dos ofertas con valores casi iguales | Mostrar empate práctico y criterio humano |
| Falta una condición de coste decisiva | Pedirla al usuario o mostrar sensibilidad |
| Probabilidad fuera del rango comprobado | No presentarla como calibrada |
| Datos contradictorios o vencidos | Resolver fuente o degradar certeza |

Una salida de calidad puede recomendar posponer, cambiar el objetivo o descartar una marca. Obligar al motor a encontrar siempre una propuesta ganadora incentiva la sobreconfianza. La explicación final muestra qué hechos sostienen la recomendación, cuáles son supuestos y qué observación podría revertirla.

## 7. Datos, etiquetas y fugas

### 7.1 Entradas mínimas (p.9)

| Entrada | Contenido mínimo | Frecuencia |
|---|---|---|
| Perfil de talento | Nicho, idiomas, formatos, mercados y ejemplos aprobados | Inicial y cuando cambie |
| Métricas autorizadas | Alcance, retención, geografía y resultados disponibles | Por periodo y campaña |
| Restricciones | Tarifa mínima, costes, derechos, exclusividad y carga aceptable | Inicial y por excepción |
| Encargo de marca | Nombre o URL, país o ciudad, producto o categoría | Cada oportunidad |
| Oferta autorizada | Precio o rango permitido, entregables y condiciones | Cada oportunidad |
| Contexto conocido | Relación previa e información recibida | Si existe |

- Investigable (con fuente y fecha): identidad y ubicaciones, carta o catálogo, rango de precios observable, posicionamiento, promociones actuales, canales de reserva, colaboraciones publicadas, estacionalidad, situación económica. Una colaboración visible no revela cuánto se pagó.
- No inventar: presupuesto interno, margen del restaurante, alcance por ciudad no publicado, tasa de conversión no medida, motivos del rechazo, autoridad del contacto, ofertas de la competencia. Las reseñas indican temas, no son muestra neutral ni prueban problemas financieros.
- Las etiquetas extraídas por IA conservan evidencia y marca de revisión. Las reglas aprobadas del sistema de propuestas se cargan como configuración, no se infieren ni se reescriben por un supuesto aumento de aceptación. El estudio no audita el kit vigente.

### 7.2 La oportunidad como unidad y los estados (p.10, p.30)

- Unidad: oportunidad comercial (una marca, un objetivo, una secuencia de negociación y sus versiones; en p.30, creador más marca más objetivo más ventana comercial). No contar cada PDF, recordatorio o captura como venta independiente. Cadenas con varios locales pueden compartir decisor.
- Estados separados: preparada; enviada; entrega fallida; respuesta; interés; negociación; aceptación documentada; rechazo explícito; pendiente; cobrada; ejecutada; renovada. El silencio no revela rechazo.
- Aceptación en 30 días: un caso con seguimiento completo y sin acuerdo cuenta como no aceptación en esa ventana; uno observado solo 8 días permanece censurado o pendiente. Una firma posterior vale cero para la etiqueta de 30 días pero se registra como éxito posterior. Si se pierde el seguimiento hay censura o etiqueta desconocida, no se fabrica un rechazo.
- Una oferta alternativa que no se envió no recibe el resultado de la elegida. Contactar, elegir paquete y redactar se registran por separado.
- No mezclar tareas: aceptación condicionada a contacto no equivale a decidir qué marca contactar; cobro entre contratos firmados no equivale al valor esperado de una oportunidad nueva. Cada probabilidad devuelta indica población, condición, horizonte y versión.
- Sin fuga: no usar descuento final, respuesta posterior ni métricas de campaña para predecir la aceptación inicial. Las fuentes económicas necesitan versión histórica.
- Sesgos a registrar: selección (enviar solo a marcas prometedoras), supervivencia (conservar solo aprobadas), seudorreplicación (contar propuestas repetidas), confundir cortesía con firma. Un registro pequeño y consistente suele valer más que un archivo enorme con esos errores.

### 7.3 Contrato de resultados (p.30). Plazos iniciales de diseño, no hallazgos

| Resultado | Definición operativa |
|---|---|
| Respuesta a 14 días | Respuesta humana sustantiva en 14 días del primer envío entregado; excluir automáticas |
| Firma a 30 días | Acuerdo documentado y aceptado por ambas partes en 30 días; definir antes qué documentos califican |
| Cobro a 90 días | Importe recibido en los 90 días posteriores a la firma; moneda convertida con la regla fijada |
| Margen neto | Cobros menos costes directos, comisiones y costes fiscales incluidos expresamente |
| Resultado de campaña | Métrica acordada con la marca, método y ventana; atribución no es incremento causal |
| Repetición a 180 días | Segundo acuerdo dentro de 180 días de la primera firma |
| Satisfacción del talento | Valoración declarada con escala y momento constantes; nunca inferir felicidad |

### 7.4 Esquema relacional y reglas de integridad (p.31)

Tablas: talent, brand, contact, audience_snapshot, opportunity, offer_version, decision, message_event, outcome_event, evidence, feature_snapshot, prediction, experiment_assignment, preference_version. Claves internas (no usar el nombre comercial); tenant_id en todas si hay varias organizaciones. Claves foráneas obligatorias; unicidad por oportunidad y versión; importes decimales con moneda ISO; porcentajes con escala explícita; horas en UTC y zona del negocio aparte; un evento importado dos veces no duplica una firma; las correcciones crean versión nueva. Cada evidencia guarda event_time, available_at e ingested_at. Valores faltantes con motivo: cero, desconocido y no aplicable no son equivalentes. Documentos originales aparte de las variables de entrenamiento, con hash y control de acceso.

### 7.5 Variables temporales y prevención de fugas (p.32, p.33)

- Regla de oro: reconstruir lo que el sistema podía saber al recomendar. Filtrar por fecha del evento no basta (una estadística de septiembre publicada en octubre no estaba disponible). Feast ofrece uniones punto en el tiempo (S46); se añade control de available_at e ingested_at.
- Dos evaluaciones: reproducir el producto histórico exige ingested_at menor o igual que t0; un modelo retrospectivo con fuentes públicas ya existentes se etiqueta como reconstruido y no se presenta como rendimiento real.
- Agregados: tasas previas de una marca solo con oportunidades resueltas antes de t0; codificaciones por objetivo dentro de cada partición de entrenamiento; los índices de recuperación no contienen cartas de rechazo, contratos ni notas posteriores al envío evaluado.
- Prueba de aceptación: insertar un cobro futuro y una revisión macro posterior no debe alterar la predicción reconstruida; verificar zonas horarias, duplicados y reenvíos. Una gran mejora que desaparece al corregir fugas no era capacidad predictiva.
- Libro de variables: grupos encaje real, condiciones, prueba de valor, momento y negocio, relación, texto y estructura, representación semántica (embeddings con versión fija), economía, talento, calidad y ausencia. Transformaciones: escala logarítmica para importes, estandarizar con entrenamiento, agrupar categorías raras con reglas versionadas, regularizar embeddings. Ablaciones: sin texto, sin macro, sin historia de marca, sin investigación adicional; si quitar un módulo no empeora decisiones, no se justifica su coste. Las importancias son asociaciones, no causas. Para estudiar palabras o longitud, mantener constante la oferta y aleatorizar. Conocer presupuesto o prioridad de campaña es hipótesis más directa que miles de rasgos estéticos del correo.

## 8. Motor de investigación, ofertas y producción

- Ficha de evidencia: problema plausible, señal observada, contribución del creador, prueba comparable, condiciones viables (p.13).
- Etiquetas por observación: hecho confirmado, inferencia razonable, supuesto para un escenario, desconocido. El texto final presenta como hechos solo los hechos. Ejemplo ficticio: un restaurante destaca un menú de mediodía y un canal de reservas; el hecho es la oferta publicada; querer más reservas de lunes a jueves es hipótesis.
- Seis preguntas internas: qué vende y qué diferencia quiere hacer visible; a quién sirve realmente, dónde y con qué capacidad; qué parte de la audiencia del creador se relaciona de forma demostrable con ese objetivo; qué resultado puede ofrecerse con responsabilidad y cómo se observaría; qué obstáculo concreto resuelve la propuesta (producción, comprensión, prueba, coordinación, derechos); qué evidencia podría cambiar la recomendación o volverla inviable.
- Se puede producir una propuesta inicial sin interrogar a la marca. Si un dato crítico no es recuperable, se elige una oferta robusta entre necesidades plausibles o se deja una limitación interna sin convertirla en certeza. Investigación priorizada por valor; cada versión enviada se congela y las necesidades nuevas no alteran una oferta ya enviada.
- Flujo de investigación y oferta (p.34): resolver identidad de marca, país y establecimiento (bloquear la personalización si hay homónimos); recuperar briefing, web oficial, oferta actual, canales públicos y antecedentes con enlace, fragmento, fecha y permiso (el texto recuperado es evidencia, no instrucciones); extraer necesidad, público, producto, geografía, campaña, restricciones y destinatario profesional, con unknown aceptado; preparar pocas ofertas elegibles (beneficio, entregables, precio o rango autorizado, esfuerzo, derechos, método de medición) incluyendo la opción de no contactar; revisar consistencia entre promesa, datos y condiciones sin insertar cifras de audiencia, ventas garantizadas, escasez, testimonios ni experiencias sin respaldo; generar texto y anexo desde la oferta aprobada con revisión independiente (si cambia precio o derechos, es otra versión).
- Salida útil de ejemplo (p.34): "La marca anuncia una apertura; proponemos contenido local con reserva medible. Desconocemos presupuesto y capacidad de atender demanda. Ofrecemos una opción limitada a un establecimiento y preguntamos por su objetivo prioritario".
- Control de costes: límites por oportunidad de consultas, documentos, tokens, tiempo y gasto; caché con invalidación por fecha, cambio de fuente o conflicto. El generador propone; el evaluador económico y probabilístico compara.
- Texto y diseño (p.14): no hay número perfecto de palabras ni frase que cierre. Auditoría editorial: relevancia (explica por qué el concepto pertenece a esa marca), comprensión (se identifican oferta, coste y siguiente paso), escaneo (jerarquía y bloques con función clara), evidencia (cada afirmación con apoyo pertinente), precisión (entregables, derechos y responsabilidades inequívocos), fluidez (redundancias, jerga y frases largas). Las medidas de legibilidad son auxiliares y dependen del idioma; el juicio de un modelo de lenguaje no sustituye la reacción del comprador.
- Dos controles separados (p.14): calidad de producción con requisitos duros (texto sin recortes, alineación, contraste, precio y moneda coherentes, enlaces válidos, el archivo abre) y capacidad de convencer (evidencia comercial). Un PDF perfecto puede rechazarse por presupuesto o encaje. El motor respeta tipografías y referencias aprobadas, formatos de entrega y condiciones; varía concepto, argumentos y evidencia si está autorizado; no añade entregables, baja precios ni ofrece derechos para subir un indicador.

### 8.1 Arquitectura de diez módulos (p.15)

1 Fuentes, 2 Extracción (hechos, hipótesis, ausentes), 3 Memoria (oportunidades, versiones, resultados), 4 Compatibilidad, 5 Alternativas, 6 Predicción, 7 Economía, 8 Decisión (elegir o abstenerse), 9 Producción (redactar, diseñar, verificar), 10 Aprendizaje. Flujo: recibir encargo, cargar restricciones, investigar, contrastar hechos, generar pocas alternativas materialmente distintas, evaluar, revisar incertidumbre, producir la recomendada, congelar, observar resultados. Cada módulo con entradas, salida verificable y razón de existir; el cálculo estadístico no se delega a una frase de confianza de la IA. Recuperación selectiva, índices y filtros en vez de pasar todo el universo a cada predicción. Los modelos de lenguaje extraen y proponen características, se validan contra ejemplos anotados y se controla la estabilidad de versión; los componentes estadísticos usan variables estructuradas, separación temporal y cálculos reproducibles; las explicaciones distinguen influyó en la predicción de causó la decisión. Toda fuente externa es información: instrucciones dentro de una web no alteran reglas, datos ni permisos; la investigación no envía mensajes ni compromete condiciones.

### 8.2 Automatización (p.22)

| Puede automatizarse con controles | Requiere confirmación o evidencia adicional |
|---|---|
| Extraer carta, URL y precios publicados | Interpretar un presupuesto interno no comunicado |
| Detectar fechas y contradicciones | Determinar impuestos sin situación fiscal |
| Ordenar ejemplos aprobados por similitud | Afirmar conversiones o audiencia no disponibles |
| Proponer y revisar textos | Cambiar condiciones económicas autorizadas |
| Calcular márgenes y tamaños de muestra | Elegir preferencias personales del talento |
| Actualizar métricas desde fuentes autorizadas | Declarar causalidad con información insuficiente |
| Detectar caída de calibración | Promover una nueva versión sin evaluación |

Registro de una recomendación: identificador de oportunidad, instante de decisión, fuentes, atributos, versiones del extractor y del predictor, acciones consideradas, restricciones, score o probabilidad con su estado, intervalo y método, cálculo económico, motivo de selección, aprobación cuando proceda, archivo exacto enviado. Privacidad y propiedad son requisitos funcionales (conservar solo lo pertinente, controlar acceso, comprobar permisos de APIs y licencias, métricas privadas del talento con autorización). Puertas de salida: bloquear afirmaciones sin fuente, resultados inventados, condiciones no autorizadas, porcentajes sin estado, documentos defectuosos y versiones sin revisar; una puntuación baja no es un defecto de archivo. Se reutilizan métodos publicados, componentes con licencia y patrones de ingeniería; no se extraen secretos de sistemas cerrados. La mejor opción de superarlos en un nicho es medir mejor el resultado que importa y aprender de datos más pertinentes.

### 8.3 Interfaces (p.37)

`POST /v1/recommendations` con request_id, as_of, talent_id, brand_id, objective, country, offers (offer_id, price como cadena decimal, currency, deliverables, rights_days), preference_version, prediction_target y execution_mode (draft_only). Respuesta de ejemplo con status insufficient_evidence, recommended_offer_id nulo, acceptance_probability nula, probability_interval nulo, ranking_basis, missing_fields, evidence_ids, model_version, policy_version, label_version y draft_id. Otros: `POST /v1/research-jobs`, `GET /v1/research-jobs/{id}`, `POST /v1/outcome-events`, `GET /v1/predictions/{id}/audit`. Clave de idempotencia e identidad autorizada en cada petición. Desconocido se representa como null con motivo. El escenario económico usa un campo distinto de la predicción. El endpoint de recomendación no envía mensajes, no firma contratos ni cambia precios aceptados.

### 8.4 Arquitectura de software (p.43)

PostgreSQL para entidades y eventos, almacenamiento de objetos para documentos y conjuntos congelados, servicio Python de recomendaciones, cola de tareas, registro de modelos (MLflow). Elecciones de referencia, no resultado de competir infraestructuras. Componentes: ingesta, evidencias, variables, modelos (interfaz predict(features, target, horizon) con soporte y versión), evaluador de ofertas, generación, orquestación, auditoría, observación. Escala: particionar por organización y tiempo, materializar agregados temporales, procesos por lotes, búsqueda híbrida (filtros por entidad y fecha más texto y semántica); no enviar millones de filas a un modelo de lenguaje. Si falla una fuente macro, usar el último dato con fecha y caducidad o abstenerse; si cae el modelo avanzado, usar la referencia validada señalando el cambio o devolver análisis sin probabilidad.

### 8.5 Pruebas de aceptación (p.44)

Evento duplicado no duplica; propuesta pendiente no se etiqueta como rechazo; alternativa no enviada no hereda resultado; evidencia futura no cambia la predicción en t0; marca homónima no mezcla entidades; monedas incompatibles no se suman sin conversión y fecha; coste desconocido no se informa como margen conocido; fuente contradictoria conserva el conflicto y su resolución; texto inventado se bloquea o elimina; oferta prohibida no aparece como recomendada aunque puntúe alto; marca o país sin soporte informa cobertura y puede abstenerse; probabilidad calibrada tiene objetivo, población, horizonte y evaluación; fallo de proveedor ejecuta la política de degradación; separación de clientes (tenants); reproducción de la decisión con versión y snapshot.

## 9. Adaptación por país y negocio (p.12, p.21, p.45)

| Contexto | Variables a comprobar | Decisión que pueden cambiar |
|---|---|---|
| Restaurante local | Radio de clientes, ticket, capacidad, reservas, audiencia local | Contenido, prueba, promesa y viabilidad del precio |
| Cadena o franquicia | Decisor, número de locales, ámbito del presupuesto | Escala de campaña y alcance del acuerdo |
| Marca de comercio electrónico | Países servidos, entrega, margen y conversión disponibles | Geografía útil, medición y formato |
| Servicio internacional | Mercados prioritarios, idiomas, uso durante viajes | Narrativa y distribución entre países |
| España | Ciudad, turismo, estacionalidad, costes y marco fiscal | Contexto y margen neto, sin generalizaciones culturales |
| Venezuela | Moneda contractual, referencia de conversión, fecha de pago y costes | Escenarios de cobro y rentabilidad real |

- Fuentes estructuradas propuestas: INE (España), FMI y Banco Mundial (contexto internacional), BCE (cambio). Las tasas de referencia no son necesariamente el tipo efectivo de una transacción; guardar fuente, hora, comisiones y supuestos.
- Contratos referidos al BCV: verificar la fuente oficial y la fecha de las condiciones pactadas. El estudio no fija cotización ni regla fiscal. Impuestos según residencia, entidad que factura, actividad y jurisdicción; si faltan, mostrar escenarios y señalar la variable pendiente sin tasa arbitraria.
- La macroeconomía aporta contexto, no la caja del negocio. No contar cientos de negocios del mismo país y mes como observaciones independientes. Cada dato con vigencia y política ante fallo de la fuente.
- Paquete de país versionado: idioma y formatos; monedas de presupuesto, coste y cobro; zona horaria; calendario comercial; fuentes estadísticas; métodos de pago; reglas fiscales verificadas; restricciones de derechos.
- Ejemplos hipotéticos (p.21): restaurante en España con oferta de 350 euros, comida cubierta, relación fría y audiencia local sin comprobar (si falta alcance pertinente no se promete llenar mesas; el precio no cambia por iniciativa del modelo); restaurante en Venezuela con 550 dólares referidos al BCV (se conserva exactamente moneda y condiciones; se calculan escenarios de margen según costes, fecha y forma de conversión; no se traslada la tasa de cierre de España); marca internacional de viajes con tres videos gastronómicos (verificar mercados servidos; derechos de reutilización, pauta o exclusividad por separado). Adaptativo significa responder a diferencias verificadas, no cambiar colores, nacionalismos o adjetivos. Salida interna común: recomendación, alternativa, encaje, razones, riesgos económicos, datos ausentes, estado de validación, siguiente acción; la propuesta a la marca mantiene un mensaje simple.
- Robustez: ninguna familia finita de desviaciones cubre todos los choques (S45). Predicción performativa (S40): al cambiar a quién contactamos y qué ofrecemos, el sistema cambia los datos que observa. Mantener métricas por cohorte de captación y versión de política, un comparador estable y fechas de cambios comerciales. Una subida de aceptación tras abandonar sectores difíciles no prueba mejor redacción. No se necesita un modelo independiente por país el primer día: compartir información con jerarquía y evaluar dónde deja de transferir; país nuevo fuera de lo validado: investigación, escenarios y fase de aprendizaje local antes de anunciar precisión.

## 10. Requisitos obligatorios para quien implemente (p.24)

1. Definir antes de entrenar qué se predice, cuándo y en qué ventana; separar aceptación, cobro, ejecución y resultado de campaña.
2. Una oportunidad por proceso comercial; conservar versiones y agrupar marcas relacionadas; no etiquetar el silencio como rechazo explícito ni simular resultados para aumentar la muestra.
3. Tres niveles de evidencia por campo (observado, inferido, supuesto) más desconocido; registrar fuente, fecha y versión histórica disponible al decidir.
4. Comparar tasa base, regresión regularizada, modelo jerárquico y candidatos tabulares pertinentes; añadir complejidad solo si supera la referencia en evaluación temporal y utilidad.
5. Mostrar por separado compatibilidad, probabilidad, incertidumbre y estado de validación; sin calibración comprobada no presentar el porcentaje como precisión demostrada.
6. Optimizar margen y calidad de alianza bajo límites de tarifa, derechos, carga y afinidad del talento; no maximizar firmas sacrificando rentabilidad.
7. Investigar prioridades comerciales con fuentes públicas y datos autorizados; no inventar presupuesto, deseos privados, personalidad ni motivos de rechazo.
8. Usar experimentos para evaluar cambios; registrar asignación y resultado; calcular potencia; limitar comparaciones; impedir fugas y conclusiones causales injustificadas.
9. Comprobar PDF, enlaces y formato de entrega independientemente de la evaluación comercial; congelar el archivo enviado y relacionarlo con la predicción.
10. Conservar auditoría, validación por mercado, monitorización y reversión; entregar un informe de pruebas con mejoras, incertidumbre y fallos, sin afirmar superioridad mundial no demostrada.

Criterio de aceptación del desarrollo: reconocer un dato ausente, abstenerse ante una predicción injustificada y detectar una oferta económicamente mala aunque parezca fácil de vender.

## 11. Riesgos que engañan incluso a un motor avanzado (p.25)

| Fallo | Ejemplo | Defensa |
|---|---|---|
| Fuga temporal | Usar el precio negociado para predecir el primer sí | Reconstruir lo conocido al enviar |
| Sesgo de selección | Aprender solo de marcas contactadas a mano | Registrar elegibilidad y criterio de selección |
| Confusión causal | Atribuir a un título lo que produjo una rebaja | Experimentos o supuestos explícitos |
| Optimización de sustitutos | Ganar respuestas amables sin acuerdos rentables | Métrica económica principal y resultados finales |
| Dependencia | Cincuenta locales con un único comprador | Agrupar y ajustar la inferencia |
| Cambio de distribución | Crisis, nueva plataforma, cambio de audiencia | Monitorizar, recalibrar, limitar uso |
| Transferencia negativa | Aplicar patrones de España a Venezuela | Validación local y efectos jerárquicos |
| Sobreajuste de búsqueda | Elegir la mejor entre miles de redacciones simuladas | Reservas reales y pruebas prospectivas |
| Autoconfirmación | Entrenar con las notas que la propia IA asignó | Etiquetas externas de resultados |
| Incertidumbre oculta | Publicar 87,43% sin soporte | Redondeo razonable, intervalos y abstención |

Hipótesis operativas del diseño (a verificar con el negocio): elegir bien las marcas elegibles puede aportar más que retocar el copy; la integridad de las etiquetas puede valer más que un algoritmo nuevo; el coste de exclusividad puede superar el beneficio del contrato; renovación y cobro pueden ser mejores señales que una respuesta entusiasta. No todo riesgo necesita otro modelo: lo prohibido se filtra, el precio fijo se respeta, la fuente inexistente se deja como desconocido.

## 12. Plan de construcción, comparación y entrega (p.23, p.42, p.47)

- Cinco fases: preparar el dominio (leer el kit, inventariar historial, deduplicar oportunidades, separar reglas editoriales de datos de resultados, definir éxito, ventana, costes y límites; entregable diccionario de datos y auditoría); asistente de decisión (investigación, evidencia, compatibilidad, escenarios, QA; propuestas trazables y registro de desenlaces desde el primer envío); comparar predictores con cortes temporales; experimentar pocas hipótesis con potencia y seguimiento definidos y aleatorización antes de sistemas adaptativos; ampliar con tareas de transporte validadas, adaptación continua con monitorización y reversión, y el modelo nuevo compite en sombra.
- Nueve paquetes: A contratos del negocio, B datos y trazabilidad, C investigación y propuestas, D referencias predictivas, E competición de candidatos, F decisión económica, G integración operativa, H validación prospectiva, I expansión. Contenido esperado del repositorio final: esquema y migraciones, validadores, construcción temporal de variables, entrenamiento y calibración, evaluación reproducible, optimizador, generador con verificación, contratos API, pruebas, configuración de despliegue, documentación operativa y tarjetas de datos y modelos (el estudio no afirma haberlos producido). Roles: responsable comercial, ingeniería de datos y producto, modelado estadístico con experiencia experimental, revisión de condiciones económicas locales; una persona puede cubrir varios.
- Qué significa el mejor: conjunto de oportunidades representativo, competidores definidos, presupuesto de cómputo comparable, datos finales reservados, métrica principal acordada (sugerida: beneficio neto por oportunidad elegible, con límites de riesgo y carga, más calibración y calidad del acuerdo). La superioridad se afirma solo para el dominio, periodo y condiciones evaluados. Afirmación defendible: mejor desempeño entre los sistemas evaluados, bajo este protocolo, para estas tareas y mercados.
- Comparadores mínimos: proceso habitual, regla por segmentos, regresión regularizada, modelo jerárquico, competidor tabular fuerte, modelo preentrenado tabular, modelo relacional si aplica, modelo de lenguaje con investigación y sin historial, sistema completo, y el CRM existente si es accesible. Misma información disponible al decidir y presupuesto de ajuste comparable (cómputo, datos, trabajo humano, coste de inferencia); frontera rendimiento-coste. Competidor mal configurado no prueba superioridad algorítmica. Dimensiones: predicción, negocio, generalización, fiabilidad, operación, talento y marca. Conservar casos difíciles y abstenciones; informar cobertura y valor sobre toda la población elegible. Auditoría externa y protocolo publicado; clasificación pública describe participantes y datos; ausencias no son derrotas. La prueba causal prospectiva pesa más que ganar una métrica retrospectiva.
- Tiempo y coste no se prometen. La instrumentación puede construirse antes de tener evidencia; la validación comercial espera resultados observables. Un calendario no crea muestra estadística.
- Frontera (p.46): multicalibración, omnipredictors con restricciones (el nombre no implica omnisciencia), aprendizaje federado (no resuelve privacidad, permisos ni etiquetas por sí solo), modelos relacionales con entrenamiento orientado a decisión. Destilación: puede aproximar comportamientos, no revela la inteligencia interna ni garantiza superarla. Una base compartida de propuestas aceptadas y rechazadas, con autorización y buena cobertura, valdría más que acumular textos exitosos sin denominadores.
- Cuestiones sin resolver (p.48): cuánto transfieren los modelos preentrenados, qué información adicional produce valor, qué estilos funcionan en cada contexto, cuánto duran las relaciones, qué grupos admiten calibración suficiente, cuánto del beneficio viene de seleccionar marcas frente a cambiar ofertas. Faltan por especificar con datos reales: negocio y población inicial, fuentes y permisos, ciclo de venta, costes del talento, condiciones de pago, preferencias, definición de firma, seguimiento de rechazos y pendientes, infraestructura, volumen y presupuesto.

## 13. Referencias (pp.49 a 55)

50 referencias S01 a S50 con tipo y nivel de acceso declarados. Clasificación:

- Artículos o actas revisados por pares: S01 (Benjamini y Hochberg, JRSS B), S02 (no free lunch, ICML), S05 y S06 (Matchbox en WWW y LightGBM en NeurIPS), S07 (TabPFN, Nature 2025), S11 (TabArena, NeurIPS 2025), S12 y S13 (metaanálisis de marketing con influencers en JAMS), S14 (personalización, Journal of Marketing, junio de 2026), S15 (Perla, Psychology and Marketing), S16 (Matz, PNAS 2017), S17 y S18 (Salvi y su corrección, Nature Human Behaviour), S20 (Riley, BMJ), S27 (Li y colaboradores, WWW), S28 (Dudík, ICML), S29 (Guo, ICML), S32 (Lewis y Rao, QJE), S36 (Elmachtoub y Grigas, Management Science), S38 (Chernozhukov, Econometrics Journal), S39 y S40 (ICML), S41 (Howard y colaboradores, Annals of Statistics), S43 (Ashokkumar, Nature 2026), S44 y S45 (ICML), S48 (Packard y Berger, Journal of Consumer Research), S49 (AISTATS), S50 (ICML).
- Preprints y tutoriales de autores sin revisión por pares: S08 (TabPFN-2.5), S09 (TabICLv2), S30 (tutorial de predicción conformal), S33 (RelBench v2, ficha ICLR 2026), S34 (KumoRFM-2).
- Documentación, informes de desarrollador o proveedor, artículos divulgativos y fuentes institucionales: S03 (TrueSkill 2, Microsoft Research), S04 (LaLiga), S10 (SAP), S19 (UCI), S21 a S24 (INE, FMI, Banco Mundial, BCE), S25 (Morkes y Nielsen, experimento de usabilidad publicado por Nielsen Norman Group en 1997), S26 (PyWhy), S31 (Bing), S35 (AutoGluon), S37 (BoTorch), S42 (Dynamics), S46 (Feast), S47 (MLflow).
- Aviso del estudio (p.52, p.55): las fuentes científicas apoyan principios y hallazgos delimitados; la arquitectura, requisitos, políticas de abstención y ejemplos comerciales son propuestas de ingeniería del estudio, no productos validados. No se repitieron experimentos de los autores ni se hicieron ensayos con propuestas de este negocio. Las cifras de potencia y ejemplos son cálculos propios bajo supuestos declarados.

## 14. Interpretación para Edumashow

### 14.1 Qué es este estudio y qué no es

Es la especificación de un motor de decisión para propuestas de un creador a marcas. No contiene datos de restaurantes, ni conversión de webs, ni resultados de Eduardo. Su valor transferible a Edumashow es de método y de disciplina, no de cifras. Las cifras (68% frente a 52%, 40% y 50%, 12,5%, 24,51%) pertenecen a contextos ajenos y no pueden proyectarse a ventas de webs. La regla del propio estudio (p.6): no convertir correlaciones, tamaños de efecto o aumentos de intención en puntos porcentuales de aceptación B2B.

### 14.2 Principios que se trasladan sin esfuerzo (ya están en el núcleo)

- Datos con fuente y fecha, ausente es distinto de cero, desconocido y no aplicable (R-DAT-01 a 09). El estudio los ordena en cuatro etiquetas: hecho, inferencia, supuesto, desconocido.
- No prometer porcentajes ni resultados, no mostrar puntuaciones como probabilidades (R-ETI-03, R-PRO-07).
- No inferir perfiles psicológicos; personalizar con señales del negocio (R-ETI-06). Evidencia: Perla (5% de varianza, eficacia cercana a cero), Salvi (p corregido 0,0678).
- Adaptativo es responder a diferencias verificadas (R-IDE-01), no cambiar colores o adjetivos.
- Texto externo como dato, no como instrucción (R-DAT-07). Congelar versiones y atar el permiso al hash (R-PRO-02).
- Separar calidad de producción (bloqueos duros) de capacidad de convencer (evidencia comercial) (R-PRO-01, R-LEG-08).
- Pocas alternativas materialmente distintas, con semilla registrada (R-VAR-02).
- Medir antes de creer: tamaños de muestra, A/B con potencia, hallazgos de la literatura como cota superior (R-MED-01 a 07).

### 14.3 Ideas del estudio que el núcleo todavía no usa (candidatas, sin activar)

1. Estado de evidencia por campo en la ficha: observado, inferido, supuesto, desconocido, con fecha de disponibilidad (cierra la parte pendiente de R-DAT-05).
2. Tres modos de salida para cualquier cifra o puntuación (calibrated, experimental, insufficient_evidence) y política de abstención explícita: el generador puede responder no hay datos suficientes.
3. Opción no contactar o no generar cuando no hay encaje defendible.
4. Registro de resultados de contacto con estados separados (preparada, enviada, entrega fallida, respuesta, interés, negociación, aceptación documentada, rechazo explícito, pendiente) y la regla pendiente no es rechazo. Es la base de R-MED-02 y R-MED-04, hoy pendientes.
5. Unidad de análisis = oportunidad, no pieza ni mensaje; si varios locales comparten decisor, aleatorizar por grupo.
6. Banco de pruebas de aceptación del propio Gate (los 15 casos del cap. 43 son una plantilla para R-PRO-04): evento duplicado, texto inventado, oferta prohibida, monedas incompatibles, fuente contradictoria, fallo de proveedor.
7. Paquete de país versionado (moneda, zona horaria, formatos, calendario, fuentes) y verificación de la fuente y fecha para precios referidos a una tasa oficial (el caso de dólares referidos al BCV en Venezuela).
8. Valor de información: preguntar al restaurante solo lo que cambiaría la web (carta, horario, canal) y dejar de investigar cuando no cambia la decisión.
9. Un único experimento inicial, con una sola variable y todo lo demás fijo, aleatorizado por prospecto elegible, resultado primario observable y ventana fija.

### 14.4 Cautelas de interpretación

- Todo el diseño es propuesta de ingeniería, no sistema validado (el estudio lo repite en pp.1, 26, 48, 52, 55). Los umbrales, plazos (14, 30, 90, 180 días) y priors son valores iniciales.
- Casi todas las referencias de personalización y persuasión son de consumidores, no de decisores que contratan un servicio. El estudio lo declara como distancia de aplicación.
- Varias fuentes se comprobaron solo por resumen (S07, S11, S14 y otras); el estudio lo indica en la bibliografía.
- Nada del estudio habla de movimiento, velocidad de carga, móvil de gama media, carta, WhatsApp o apetito: esos temas se cubren con normas técnicas y medidas propias del proyecto.
