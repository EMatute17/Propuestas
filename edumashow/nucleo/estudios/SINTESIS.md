# Síntesis de los cinco estudios

Lectura integrada de los cinco documentos que Eduardo aportó. El detalle y las citas por página están en `analisis/` (lectura) y `texto/` (texto completo). Las páginas (p.N) son las del pie de cada PDF. Los ids H-XX-NN remiten a los hallazgos numerados de cada análisis.

## 1. Los cinco en una página

| Clave | Documento | Páginas | Corte | Qué es | Qué aporta | Qué no hace |
|---|---|---|---|---|---|---|
| PS | Psicología humana histórica y actual | 9 | 26 sep 2026 | Síntesis crítica de psicología con 48 referencias | El freno: ninguna palanca psicológica universal; casi todo efecto famoso se encoge al replicar o al corregir el sesgo de publicación; definir una conducta, medir acciones y no intenciones | No trata de webs, restaurantes ni propuestas. Selección narrativa de estudios, sin PRISMA ni GRADE |
| CO | Ciencias del comportamiento y de la conducta | 11 | 28 sep 2026 | Estudio crítico con 36 referencias | El método: niveles de evidencia, lectura de magnitudes, mecanismos (intención y acción, hábitos, defaults, recordatorios con enlace), controversia de los nudges, replicación, protocolo de seis pasos para investigar una conducta comercial | Los números vienen de salud, energía, ejercicio y encuestas, no de webs. El protocolo es una aplicación inferida |
| UX | Motor predictivo de UX para propuestas | 40 | 26 sep 2026 | Estudio de viabilidad y especificación, 44 referencias | La puerta de liberación que falla cerrada, 33 filtros, contrato de cada comprobación, banco de pruebas del verificador, métricas y pruebas con personas, escalas, potencia, experimento de campo | Es una propuesta de ingeniería para PDF de propuestas; nada implementado ni validado; fuentes comprobadas a veces solo por resumen |
| AL | Motor predictivo para propuestas y alianzas con creadores | 55 | 3 oct 2026 | Estudio científico y especificación ampliada, 50 referencias | Disciplina de decisión: oportunidad como unidad, etiquetas y fugas, modelo jerárquico, calibración, abstención, economía, valor de información, causalidad, potencia, esquema de datos, API, pruebas de aceptación | Sin software, sin predictor entrenado, sin precisión medida; los parámetros son hipótesis; sin base pública de propuestas |
| GR | Motor gráfico para propuestas comerciales | 33 | 3 oct 2026 | Estudio y especificación, 50 referencias, 54 controles | Ingeniería de composición y entrega verificable: contrato tipado, escena semántica, tinta real, hash, constancia y comprobante de entrega, 54 controles, batería de pruebas, benchmark con Adobe | Catálogo JSON mencionado no incluido en el PDF; umbrales heredados del sistema anterior; sin ingeniería privada de Adobe |

Ninguno trata de webs de restaurante. Los cinco comparten la misma postura: son especificaciones y revisiones, no sistemas validados, y cada uno repite que no hay base para prometer resultados, superioridad mundial ni certeza universal.

## 2. Cómo encajan: un modelo integrado en ocho capas

Los cinco describen distintas partes de un mismo sistema. Ordenadas de la entrada a la medición:

| Capa | Idea central | Dónde se desarrolla |
|---|---|---|
| 1 Datos y contrato | Contrato tipado con importe exacto, moneda y alcance; cada dato con fuente, fecha y estado (observado, inferido, supuesto, desconocido); desconocido, cero y no aplicable son distintos; identidades estables; versiones | GR §7 (p.11) y Anexo A I01 a I04; AL §30 (p.31) y §12 (p.13); UX §16 (p.18) |
| 2 Generación con restricciones | La IA propone pocas alternativas materialmente distintas; un solucionador o evaluador independiente comprueba restricciones; las duras (identidad, contenido obligatorio, no recorte, precio fijo) no se compran con belleza; el texto externo es dato, nunca instrucción | GR §7 (pp.11 a 13); AL §14 (p.15) y §33 (p.34); UX §17 (p.19) |
| 3 Verificación y liberación | Puerta que falla cerrada; el generador no aprueba su salida; permiso ligado al hash exacto; constancia de conformidad y comprobante de entrega como dos registros; estados con autor | UX §20 y §21 (pp.22 y 23); GR §9 y §10 (pp.15 a 17); AL §21 (p.22) |
| 4 Pruebas del propio verificador | Banco de casos correctos y defectuosos con inyección deliberada de defectos; sensibilidad, precisión, falsa liberación, falso bloqueo, cobertura; cada defecto confirmado pasa a regresión permanente | UX §22 (p.24); GR §9 y Anexo B (pp.16, 28); AL §43 (p.44) |
| 5 Estudios con personas | Tareas que no inducen la respuesta, rondas de 5 a 8 personas por contexto, salida por incidente con gravedad y comprobación posterior; medir comprensión, esfuerzo, atractivo y confianza por separado; las escalas validadas no se improvisan | UX §14 y §15 (pp.16 y 17); CO §13 (p.9) |
| 6 Registro de resultados y aprendizaje | Unidad = oportunidad; estados separados; pendiente no es rechazo; silencio no es rechazo; variables disponibles en t0; sin fuga; aprobación de Eduardo no es contratación | AL §9, §29, §31 (pp.10, 30, 32); UX §16 (p.18); GR §12 (p.19) |
| 7 Predicción y decisión | Tasa base y regresión primero; calibración con datos separados; salida en tres modos; abstención; margen por oportunidad como objetivo económico; valor de la información | AL §15 a §20, §34 a §38 (pp.16 a 21, 35 a 39); UX §23 y §24 (pp.25 y 26) |
| 8 Evaluación causal y afirmaciones | Aleatorizar antes de enviar, potencia y regla de parada fijadas de antemano, analizar según la asignación; todo efecto de la literatura es hipótesis local y cota superior; superioridad solo para un dominio, periodo y comparadores definidos | AL §16, §17, §39 a §41 (pp.17, 18, 40 a 42); UX §26 y §27 (pp.28 y 29); GR §13 (pp.19 a 21); CO §10 y §13 (pp.7, 9); PS §1 (p.1) |

## 3. Lo que los cinco dicen igual

| Principio | Quién lo dice y dónde |
|---|---|
| Datos con fuente y fecha; lo ausente no se rellena ni se convierte en cero | AL pp.9, 13, 31; UX pp.18, 20; GR pp.11, 18 (S02) |
| Una puntuación no es una probabilidad; sin modelo calibrado, no estimable de forma validada | AL pp.16, 35; UX pp.13, 19, 26; GR pp.7, 8, 19 |
| No prometer porcentajes ni resultados comerciales | AL p.25; UX pp.1, 34; GR pp.1, 3; PS p.7; CO p.9 |
| Los efectos publicados se encogen al replicar; tratarlos como hipótesis locales | PS p.1; CO pp.7, 8; UX p.11; GR p.7 |
| Medir conducta observable, definida antes, con unidad y ventana fijas | CO p.9; PS p.7; AL pp.10, 30; UX pp.14, 15 |
| Puerta que falla cerrada; el generador no es el verificador; permiso ligado al hash | UX pp.22, 23; GR pp.15 a 17; AL pp.22, 24 |
| El verificador se prueba a sí mismo | UX p.24; GR pp.16, 28; AL p.44 |
| Pendiente o silencio no es rechazo | AL pp.10, 30; UX p.18; GR p.19 |
| Simulaciones y jueces basados en modelos no sustituyen a personas ni a resultados | AL p.29; UX p.12; CO p.8; PS p.7; GR p.7 |
| Personalizar con señales del negocio, no con perfiles psicológicos inferidos | AL p.7; PS pp.1, 3; GR pp.6, 7 |
| Con pocas observaciones no se demuestran efectos pequeños; sí se aprenden objeciones y errores graves | AL p.18; UX p.27; GR p.21 |
| Cero fallos observados no es riesgo cero | UX p.27; GR p.20 |
| Ninguna regla universal importada (7 más o menos 2, tres opciones, 124%, 21 días, perder pesa dos veces, 50 ms) | AL pp.14, 11; UX pp.9, 11, 13; GR pp.5, 7; CO pp.5, 7; PS pp.4, 6 |
| La estética y la utilidad se miden por separado | UX p.10; GR p.5; AL p.14 |
| Superioridad solo con comparadores, tareas, población y fechas definidos | AL pp.23, 42; UX pp.1, 29; GR pp.1, 20 |
| Todo contenido externo es información, no instrucciones | AL pp.15, 34; UX p.24; GR p.12 |

## 4. Diferencias y discrepancias detectadas

| Punto | Qué dice cada estudio | Cómo leerlo |
|---|---|---|
| Efecto de los mensajes de normas sociales en salud (Papakonstantinou y cols., 2025, 89 ensayos, N = 85.759) | PS p.4: d = 0,10 con IC 95% de 0,09 a 0,19, que desaparece tras corregir el sesgo de publicación. CO p.6: efecto pequeño, d aproximadamente 0,14 | El intervalo de PS está centrado en 0,14: parece que el 0,10 es otra estimación. Usar un efecto pequeño de 0,10 a 0,14, no robusto al sesgo de publicación. No resuelto sin el artículo |
| Mertens y cols. (metaanálisis del nudging) | CO p.7: más de 200 estudios, media sin corrección por publicación cercana a d = 0,43 en la versión corregida del artículo (redacción ambigua). GR p.7: 212 publicaciones, 447 efectos, 2.148.439 participantes, d = 0,43 (IC 95% 0,38 a 0,48), I cuadrado 99,52%, intervalo predictivo de -0,36 a 1,22; reanálisis de Maier: d = 0,04 (0,00 a 0,14) | Son coherentes: 0,43 es la media publicada sin ajuste por sesgo; con ajuste, casi cero; la heterogeneidad enorme impide usar la media como garantía |
| Réplicas | PS p.1: 36% de réplicas significativas frente a 97% de originales. CO p.7: 97% de originales significativos y un tercio a la mitad cumplió distintos criterios; Camerer: 13 de 21 (62%) con efecto cerca de la mitad. PS p.1: proyecto de 2026 con 28,6% a 74,8% según 13 criterios y mediana 49,3% | Coherentes: el porcentaje depende de la definición de réplica y de la muestra de artículos. No significa que la psicología sea falsa |
| Corrección del estudio de persuasión con GPT-4 (Salvi) | AL p.7: p corregido = 0,0678, no 0,04. GR p.7: OR original 1,812 (IC 1,260 a 2,607); tras la corrección, personalizado frente a no personalizado OR = 1,487 (0,971 a 2,276), p = 0,0678 | Coherentes. Lección compartida: el registro de evidencia conserva y aplica las correcciones |
| Personalización | AL p.7: metaanálisis de 1.536 efectos con beneficios medios según tipo de dato; Perla: 5% de varianza explicada y eficacia de extremo a extremo cercana a cero; Matz: hasta 40% y 50% como máximos. GR p.6: d = 0,16 en 53 estudios de publicidad personalizada | Coherentes: la personalización con datos reales del negocio puede tener efectos pequeños en actitud e intención; la basada en perfiles psicológicos inferidos no tiene respaldo. Nada se convierte en ventas |
| Tamaño de muestra de piloto | UX p.16: rondas de 5 a 8 personas por contexto; AL p.11: no hay mínimo universal; GR p.20: 30 a 50 encargos para descubrir defectos; UX p.27: 15 resultados para iniciar un registro | No chocan: son tamaños para descubrir problemas, no para demostrar efectos |
| Estados de una comprobación | AL: calibrated, experimental, insufficient_evidence (predicción). UX: PASS, FAIL, REVIEW, MISSING, ERROR, NOT_APPLICABLE. GR: PASS, WARN, FAIL, UNAVAILABLE, N/A | Vocabularios distintos. El Gate de Edumashow usa el de GR (R-PRO-03) |
| Ventanas de tiempo | AL: 14, 30, 90 y 180 días. UX: 14, 30 y 90. CO: 7 días para la primera respuesta (ejemplo). GR: ventana definida antes de observar | Valores iniciales de diseño en todos; ninguno es un hallazgo científico |
| Numeración de páginas | AL y UX numeran capítulos y páginas de forma distinta (en AL el capítulo n está en la p.n+1). PS y GR cuentan la portada como p.1 | En todo el archivo, p.N es el número de página del pie del PDF |

## 5. Referencias compartidas: no son corroboración independiente

Varias fuentes aparecen en más de un estudio. Los estudios las usan para frases parecidas, así que contarlas dos veces daría una falsa sensación de acuerdo (el propio AL recuerda que dos metaanálisis pueden compartir estudios y que sus muestras no se suman).

| Fuente | Aparece en |
|---|---|
| Open Science Collaboration 2015; Many Labs 2 (2018) | PS [6, 7]; CO [21, 23] |
| Camerer y cols. 2018 (13 de 21) | CO [22]; UX [34] |
| Papakonstantinou y cols. 2025 (normas sociales en salud) | PS [9]; CO [28] |
| Polderman y cols. 2015 (heredabilidad) | PS [10]; CO [16] |
| Henrich, Heine y Norenzayan 2010 (WEIRD) | PS [5, 25]; CO [15] |
| Kahneman y Tversky 1979 (teoría de prospectos) | PS [20]; CO [9] |
| Ashokkumar y cols. 2026 (modelos de lenguaje predicen experimentos) | AL [S43]; CO [33] |
| Salvi y cols. 2025 y corrección de 2026 | AL [S17, S18]; GR [22, 23] |
| Guo y cols. 2017 (calibración) | AL [S29]; UX [31]; GR [48] |
| Angelopoulos y Bates (predicción conforme) | AL [S30]; UX [32]; GR [49] |
| Riley y cols. 2020 (tamaño de muestra de modelos) | AL [S20]; UX [30] |
| Scheibehenne y cols. 2010; Chernev y cols. 2015 (opciones) | UX [18, 19]; GR [17, 18] |
| Lindgaard y cols. 2006 (50 ms) | UX [21]; GR [4] |
| Mertens y cols. 2022; Maier y cols. 2022 (nudging) | CO [25, 26, 27]; GR [19, 20] |
| WCAG 2.2 (12 de diciembre de 2024) | UX [22]; GR [45] |

## 6. Cifras que conviene tener a mano

Cada cifra pertenece a su contexto original y ninguna se traslada a ventas de webs.

| Tema | Cifra | Dónde |
|---|---|---|
| Replicación | 36% de réplicas significativas frente a 97% de originales; mediana de r de 0,25 a 0,10; 13 de 21 replican con efecto cerca de la mitad | PS p.1; CO p.7 |
| Intención y acción | Cambios de intención d = 0,66 acompañan cambios de conducta d = 0,36 (47 pruebas) | CO p.5 |
| Defaults y recordatorios | Cerca de 80% se mantuvo con energía verde por defecto (más de 200.000 hogares); recordatorios con enlace en ensayos de 93.354 y 67.092 personas | CO p.5 |
| Comparación y normas sociales | g = 0,17 y 0,23 (79 ensayos); normas en salud d entre 0,10 y 0,14 y no robusto al sesgo | CO p.5; PS p.4; CO p.6 |
| Nudging | Media publicada d = 0,43; con ajuste de sesgo d = 0,04; DellaVigna y Linos 1,4 puntos porcentuales | GR p.7 |
| Opciones | Sobrecarga D = 0,02 (-0,09 a 0,12) | UX p.11; GR p.7 |
| Hábitos | 18 a 254 días; medianas de 59 a 66 días; rango 4 a 335 | CO pp.5, 6 |
| Personalización | 5% de varianza y eficacia casi nula (41 estudios); d = 0,16 (53 estudios) | AL p.7; GR p.6 |
| Estética, señalización, multimedia | g = 0,29; g = 0,53 y 0,33; g = 0,37 | UX p.10; GR p.5 |
| Facilidad frente a ejecución | Con mayor SUS, peor tiempo en 24% y peor error en 23% de los estudios | UX p.10 |
| Lectura | Velocidad 35% mayor con la mejor fuente por lector | GR p.4 |
| Tamaños de muestra por grupo | 10% a 20%: 199; 10% a 15%: 686; 10% a 12%: 3.841; 20% a 30%: 294; 20% a 25%: 1.094; 50% a 55%: 1.565; 80% a 90%: 199 | AL p.18; UX p.27 |
| Una tasa con margen de 5 puntos | 139 observaciones si p = 0,10; 385 si p = 0,50 | AL p.18 |
| Cero fallos observados | Límite superior de 95%: con 5 casos 45,1%; 30, 9,5%; 100, 3,0%; 300, 1,0%; con 3.000, 0,0998% | UX p.27; GR p.20 |
| Bayes con pocos casos | 24 de 100, Beta(25,77): 24,51% (16,70% a 33,26%) | AL p.16 |
| Falsos positivos | 1.000.000 de nulas verdaderas al 0,05 dan 50.000 falsos positivos | AL p.3 |
| Contraste y táctil | 4,5 a 1 y 3 a 1; objetivos de 24 por 24 píxeles CSS | UX p.21; GR p.14 |
| Imagen y pantalla | 200 PPI mínimo y 300 de referencia; A4 de 595 puntos a 390 píxeles: 11 puntos son unos 7,2 píxeles | GR pp.14, 15 |
| Pilotos y ventanas | 5 a 8 personas por contexto; 30 a 50 encargos; 15 resultados para iniciar un registro; ventanas de 14, 30, 90 y 180 días | UX pp.16, 27; GR p.20; AL p.30 |
| Umbral de un producto | Dynamics: 40 ganadas y 40 perdidas | AL p.27 |
| Experimentos en empresa | Menos de un tercio de las ideas probadas mueven su métrica; intervalo mediano del retorno publicitario de más de 100 puntos | AL p.23 |

## 7. Lo que ningún estudio cubre

Los cinco tratan de propuestas en PDF de un creador a marcas. No hay nada, o casi nada, sobre: animación y movimiento (la regla del núcleo viene de WCAG 2.2 y no de los estudios), velocidad de carga y presupuesto de bytes de una web (UX pide un presupuesto sin dar cifra), móvil de gama media, diseño de una carta, WhatsApp como canal, reservas, apetito y fotografía gastronómica (GR solo exige que una foto artificial no se presente como el plato real), tasas de conversión de webs de restaurante, SEO local, y normativa legal (alérgenos, cookies, comunicaciones comerciales, reseñas, derechos de imagen). En el núcleo esos huecos se cubren con normas externas (WCAG 2.2, Core Web Vitals) y con medidas propias del proyecto (ver ../README.md).

## 8. Candidatas a reglas nuevas, sin activar

Consolidación de las listas de cada análisis. Ninguna está en `reglas.json`; sirven para cuando el siguiente encargo lo pida.

| Id | Idea | Dónde | Relación con el núcleo |
|---|---|---|---|
| C-01 | Estado de evidencia por campo de la ficha (observado, inferido, supuesto, desconocido, con fecha de disponibilidad) y registro de afirmaciones con fuente exacta, fragmento, fecha, ámbito, responsable, confirmación y permiso | AL pp.13, 24, 31; UX p.18; GR pp.18, 24 (S02) | Cierra la parte parcial de R-DAT-05 |
| C-02 | Campo de visibilidad por dato, distinto del valor interno | GR I03 (p.24) | Hoy solo se evita presupuesto y margen en el cierre de la muestra (R-MUE-03) |
| C-03 | Banco de casos del Gate con inyección de defectos y cinco métricas (sensibilidad por gravedad, precisión, falsa liberación, falso bloqueo, cobertura) | UX p.24; GR pp.16, 28; AL p.44 | Es el contenido de R-PRO-04 (pendiente) |
| C-04 | Salida de cifras en tres modos (calibrated, experimental, insufficient_evidence) y política de abstención | AL pp.20, 35; UX p.19 | Refuerza R-PRO-07 y R-ETI-03 |
| C-05 | Registro de resultados de contacto con estados separados, unidad = oportunidad y aleatorización por grupo cuando varios locales comparten decisor | AL pp.10, 17, 30; UX p.18; GR p.19; CO p.9 | Base de R-MED-02, R-MED-03, R-MED-04 (pendientes) |
| C-06 | Pruebas de tarea con personas, tareas que no inducen, salida por incidente con gravedad | UX p.16; CO p.9 | R-MED-04 (pendiente) |
| C-07 | Dos políticas de entrega declaradas (con conformidad y revisión; con predicción validada) y cuatro estados con autor | UX p.22; GR p.17 | El informe del Gate ya separa estados; falta declarar la política |
| C-08 | Redactar el informe sin sobreprometer: cero fallos observados no es riesgo cero (límite 1 - 0,05 a la 1/N) | UX p.27; GR p.20 | Nuevo |
| C-09 | Clasificar cada corrección de Eduardo (regla comercial, defecto de implementación, criterio creativo, barrera UX o preferencia personal) y convertir lo verificable en caso de prueba; preferencias con ámbito | UX p.33; GR pp.18, 19 | Se apoya en L01 y L02 del informe gráfico |
| C-10 | Perfil de fuentes admitidas por rol y lista de vetos tipográficos con referencia visual negativa | GR T01, A02 | R-IDE-04 y T01 parciales |
| C-11 | Región protegida del sujeto por foto y revisión humana si baja la confianza del detector | GR A06, G07 | Hoy hay punto de foco por imagen sin prueba automática |
| C-12 | Paquete de país versionado (moneda, zona horaria, formatos, calendario, fuentes) y verificación de fuente y fecha para precios referidos a una tasa oficial | AL pp.12, 45; GR p.14 | Amplía R-DAT-03 |
| C-13 | Valor de información: preguntar al restaurante solo lo que cambiaría la web; parar cuando el dato no cambia la decisión | AL pp.13, 39 | Nuevo |
| C-14 | Un solo experimento inicial con una variable, resultado primario observable, ventana fija y subgrupos predefinidos confirmados en otro lote; medir efectos adversos y a largo plazo | CO p.9; AL p.41 | R-MED-01, R-MED-07 |
| C-15 | Ablaciones: cada módulo demuestra lo que aporta | AL p.33; UX p.29 | Encaja con R-REN-04 |
| C-16 | Señal de congestión visual solo como alerta para revisión hasta calibrarla | GR p.6 | Nuevo |
| C-17 | Formato de las incidencias del Gate: qué, dónde, cómo corregir, con antes y después | GR p.18 | Nuevo |
| C-18 | COM-B como lista de comprobación de barreras de una web (capacidad, oportunidad, motivación) | CO p.3 | Nuevo, marco de diagnóstico y no predictor |

## 9. Qué leer según el siguiente encargo

| Si el encargo trata de | Leer primero |
|---|---|
| Mejorar el motor de webs o el Gate | GR §7 a §10 y Anexo A; UX §17 a §22; CO §12 |
| Medir si una web o un mensaje funcionan | CO §13; AL §16, §17, §39 a §41; UX §25 y §26; GR §13 |
| Registrar resultados de contactos con restaurantes | AL §9, §10, §29 a §31; UX §16 |
| Predecir o priorizar prospectos | AL §15 a §20, §34 a §38; UX §23 y §24 |
| Redactar propuestas o mensajes a marcas | AL §5 a §8, §12, §13, §33; PS §12; CO §12 |
| Ética, persuasión y límites de lo que se puede afirmar | PS §7 a §12; CO §9, §10, §12, §13; AL §6 |
| Probar el Gate con casos defectuosos | UX §22; GR §9 y Anexo B; AL §43 |
| Pruebas con personas | UX §14 y §15; CO §13 |
| Países y monedas (España, Venezuela) | AL §11, §20, §44; CO §13; GR §8 (componente monetario) |

## 10. Cautelas de este archivo

- El texto completo de `texto/` se extrajo del PDF por programa y se comprobó por conjunto de palabras contra el texto del PDF: no falta ninguna palabra salvo cabeceras y pies repetidos y el nombre del creador original, que se sustituye por [el creador] por la regla de marca. Las tablas, los títulos y los enlaces se reconstruyeron por posición y pueden tener errores de forma. Ante una duda, el PDF manda.
- Los análisis de `analisis/` son lectura de Edumashow: resumen, clasificación de la evidencia e interpretación. Los números se comprobaron contra el texto completo. La interpretación y las candidatas son juicio propio y no del estudio; están marcadas como tales.
- Los ids AL-nn, PS-nn, UX-nn y CO-nn de `reglas.json` y de TRAZABILIDAD.md son de una primera extracción que no se conservó. No coinciden con los ids H-XX-NN de estos análisis. Las páginas sí coinciden.
- El catálogo JSON que menciona el informe gráfico no venía en el PDF. Los documentos privados del sistema de propuestas anterior que los estudios citan (documento maestro, estándar visual, especificación completa, archivo de continuidad) no se han visto ni se copian al repositorio.
- Los enlaces de las referencias se conservaron tal como están en los PDF; no se han vuelto a verificar en línea.
