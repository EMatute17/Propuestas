# Trazabilidad: dónde se aplican los estudios

Este documento lo genera `edumashow/nucleo/trazabilidad_fuente.py`, que además comprueba que cada archivo y cada función citados existen. Dice también lo que todavía no está hecho.

Estados: **Aplicada** (está en el código o el diseño y el Gate la comprueba), **Sin prueba** (aplicada, pero el Gate no la mide), **Parcial**, **Pendiente** y **No aplica**.

## Resumen

| Estado | Reglas unificadas (85) | Controles del informe del motor gráfico (54) |
|---|---|---|
| Aplicada | 58 | 26 |
| Sin prueba | 5 | 2 |
| Parcial | 12 | 18 |
| Pendiente | 6 | 2 |
| No aplica | 4 | 6 |

Los cuatro estudios de conocimiento (alianzas, psicología, UX predictivo y conducta) y el informe del motor gráfico se unificaron, junto con el método de paleta, tipografía y fotos del Documento Maestro del kit, en 85 reglas con prioridad, fuente, evidencia y prueba (`reglas.json`). Cada regla lleva un número de orden de importancia, como un podio: el 0 es lo más importante (verdad, legalidad y ética) y el 6 lo menos (variedad entre webs). Cuando dos reglas chocan gana la que tiene el número más bajo, porque número bajo quiere decir más importante. Ninguno de los cinco trata de webs de restaurante: las reglas web son traducciones y están marcadas como tales.

## Las 85 reglas unificadas

| Regla | Estado | Fuente en los estudios | Dónde se aplica | Prueba del Gate | Nota |
|---|---|---|---|---|---|
| R-DAT-01 | Aplicada | UX-01 pp.20,31; AL-01 pp.9,13,34; AL-09 pp.13,20; GR-I01 p.24 | `motor/generar.py`: validar_ficha<br>`gate/estatico.py`: PLACEHOLDERS<br>`gate/estatico.py`: def datos | G-DATOS, G-ETICA | Todo el texto sale de la ficha; si falta un dato el motor se abstiene. El Gate busca marcadores de relleno y compara con la ficha. |
| R-DAT-02 | Aplicada | AL-03 pp.31,37; UX-08 p.22; AL-02 p.24 | `motor/generar.py`: validar_ficha<br>`gate/estatico.py`: patron_cero | G-DATOS | Un dato ausente no se rellena. El Gate busca ceros, gratis y similares que la ficha no tenga. |
| R-DAT-03 | Aplicada | AL-04 pp.14,21; AL-05 p.12; UX-02 p.20; UX-03 p.20 | `motor/dinero.py`: def formato_importe<br>`motor/dinero.py`: def importe_fn<br>`gate/estatico.py`: def datos<br>`gate/verificar.py`: G-FORMULARIO | G-DATOS, G-FORMULARIO | Un solo formato de moneda por país y por página (si algún precio lleva centavos, todos llevan dos decimales); cada importe de la página, sea de un plato, de una variante (media libra, una libra) o de un suplemento, y cada importe del mensaje de WhatsApp se compara con la ficha. |
| R-DAT-04 | Aplicada | UX-06 pp.18,20,30; GR-A01 p.24; GR-A02 p.25; PS-16 p.7 | `motor/imagenes.py`: class Activos<br>`motor/generar.py`: LICENCIAS.txt<br>`gate/estatico.py`: def fotos | G-FOTOS | Cada imagen lleva su procedencia, su permiso y el hash del archivo original en el manifiesto, y las tipografías en LICENCIAS.txt. Las fotos de referencia obligan a declararlo en la página. |
| R-DAT-05 | Parcial | UX-05 pp.18,20; AL-12 p.34; PS-16 p.7; CO-07 p.8 | `gate/estatico.py`: ETICA | G-ETICA, G-DATOS | El Gate bloquea premios, estrellas y porcentajes inventados, pero no hay un registro de afirmaciones con fuente y fecha por frase. |
| R-DAT-06 | Parcial | UX-07 pp.18,23; AL-08 pp.12,34 | `motor/generar.py`: confirmacion | G-DATOS, G-MANIFIESTO | La ficha guarda estado y fecha de confirmación y el manifiesto la copia; revalidar los datos antes de cada entrega es un paso humano. |
| R-DAT-07 | Sin prueba | AL-10 pp.15,34; UX-33 p.24 | `motor/piezas.py`: def e_<br>`motor/generar.py`: replace("</" | G-DATOS | Todo texto de la ficha se escapa y el JSON incrustado cierra las etiquetas. Falta el caso de prueba con texto malicioso (ver R-PRO-04). |
| R-DAT-08 | Aplicada | UX-08 pp.18,22,33; AL-09 p.13; AL-50 pp.20,34 | `motor/generar.py`: class FichaIncompleta<br>`motor/generar.py`: def validar_ficha | G-DATOS, G-MANIFIESTO | Si falta carta, horario, contacto o un precio, el motor se abstiene y dice que falta. |
| R-DAT-09 | Parcial | AL-06 pp.12,31; GR-I01 p.24 | `motor/generar.py`: confirmacion | G-DATOS | La identidad (nombre, dirección, contacto) la declara la ficha; el Gate no puede comprobar en el mundo real que sean del mismo local. |
| R-ETI-01 | Aplicada | CO-09 p.9; PS-18 p.7; AL-12 p.34 | `gate/estatico.py`: escasez o urgencia | G-ETICA | Patrones de escasez y urgencia inventadas bloquean la entrega. |
| R-ETI-02 | Aplicada | CO-07 p.8; CO-08 p.9; PS-17 p.7; AL-13 pp.9,14 | `gate/estatico.py`: testimonios<br>`motor/piezas.py`: def cinta | G-ETICA | Sin testimonios ni estrellas; lo ficticio se rotula como ejemplo en la cinta. |
| R-ETI-03 | Aplicada | UX-52 pp.1,10,22; AL-14 p.16; AL-15 pp.6,23; CO-14 p.2 | `gate/estatico.py`: promesa de resultados | G-ETICA | Sin promesas de ventas ni porcentajes con falsa precisión. |
| R-ETI-04 | Aplicada | CO-06 p.9; PS-20 p.7 | `gate/dinamico.mjs`: dialogosAbiertos<br>`gate/verificar.py`: G-ETICA-VISTA | G-ETICA | Al cargar no hay ventanas abiertas ni casillas premarcadas, en los 27 dispositivos. |
| R-ETI-05 | Aplicada | PS-21 pp.3,7; PS-25 p.4; CO-27 p.5 | `gate/estatico.py`: refuerzo variable | G-ETICA | Sin ruletas ni premios sorpresa. |
| R-ETI-06 | Sin prueba | AL-27 pp.7,24,39; PS-28 pp.1,3,4,7 | `motor/temas.py`: PALETAS | G-ETICA | Ningún código infiere perfiles de personas: el estilo lo elige la ficha a partir de datos del restaurante. |
| R-ETI-07 | Aplicada | CO-13 p.9; AL-48 pp.15,22,37 | `motor/piezas.py`: def pie<br>`motor/piezas.py`: def panel_edu<br>`gate/estatico.py`: def muestra | G-MUESTRA | La muestra trae un enlace visible para pedir su retirada y el Gate lo exige. Que nunca se envie sola a un restaurante es una regla de proceso: la aprueba una persona. |
| R-ETI-08 | Aplicada | UX-09 pp.8,15,18,33; AL-47 pp.7,22,31; CO sec.6 p.9 | `gate/estatico.py`: def red_estatica<br>`motor/generar.py`: Content-Security-Policy<br>`gate/verificar.py`: G-RED | G-RED | Sin cookies, sin scripts ni recursos de terceros; la cabecera de seguridad lo impone y el Gate lo mide en 27 dispositivos. |
| R-ETI-09 | Aplicada | UX-22 pp.12,15,21; UX-53 pp.8,12,13; UX p.29 | `gate/verificar.py`: Lo que este Gate no verifica | G-ETICA | El informe dice que solo se probó Chromium emulado y que no hay pruebas con personas. |
| R-ETI-10 | No aplica | AL-03 p.31; PS sec.6 | - | G-DATOS | Regla del modo final (alérgenos y dietas). Las muestras no los muestran. Queda pendiente su comprobación cuando haya una web final con alérgenos. |
| R-ETI-11 | Aplicada | Orden de Eduardo | `gate/estatico.py`: def marca | G-MARCA | Ninguna mención a herramientas de IA ni a Peetfoodie en lo que se entrega. |
| R-ETI-12 | Aplicada | Orden de Eduardo | `gate/estatico.py`: def comillas<br>`../scripts/revisar_comillas.py`: PROHIBIDOS<br>`../CLAUDE.md`: Comillas | G-COMILLAS | Cero comillas angulares en todo el repositorio y en cada paquete. |
| R-FOT-01 | Aplicada | Orden de Eduardo 2026-10-08; R-DAT-04 | `motor/calidad.py`: def revisar_procedencia<br>`gate/estatico.py`: def fotos<br>`../CLAUDE.md`: Fotos | G-FOTOS | Ninguna foto de redes sociales salvo el logo: lo comprueba el validador de fichas antes de construir y el Gate sobre el manifiesto. Las de referencia o generadas solo valen en un ejemplo ficticio. |
| R-FOT-02 | Aplicada | Orden de Eduardo 2026-10-08; R-REN-02 | `motor/calidad.py`: MINIMOS<br>`gate/estatico.py`: def fotos_calidad<br>`gate/verificar.py`: G-FOTOS-CALIDAD | G-FOTOS, G-RESOLUCION | El Gate mide el original (lado largo, calidad JPEG, detalle fino) y lo compara con su SHA-256; sin excepciones. Con la opción de prueba el resultado queda marcado como no entregable. |
| R-IDE-01 | Aplicada | AL-25 pp.21,45; AL-26 pp.7,9,13; UX-27 pp.7,21,30 | `motor/estilo.py`: def decidir<br>`motor/estilo.py`: TONOS_COCINA<br>`motor/huella.py`: def huella | G-HUELLA | El director de estilo deduce paleta (del logo), tipografía (del carácter de la cocina) y orden de fotos (por antojo) de los datos de la ficha, y deja escrita la razón de cada decisión en el manifiesto y en el informe del Gate. |
| R-IDE-02 | Aplicada | PS-15 p.4; UX-27 p.21 | `motor/piezas.py`: def _plato<br>`motor/plantillas/elegante.js`: role=tab<br>`motor/piezas_urbano.py`: def _item<br>`motor/plantillas/urbano.js`: chips | G-SIGUIENTE, G-INTERACCION | Precio junto al nombre, categorías de carta y botones de acción donde se esperan: pestañas en la personalidad elegante y barra de categorías pegada arriba, con la categoría actual marcada, en la urbana. |
| R-IDE-03 | Aplicada | UX-28 pp.13,30; UX-60 pp.6,11 | `motor/color.py`: def paleta_marca<br>`motor/tipografia.py`: PAREJAS<br>`gate/verificar.py`: G-CONTRASTE<br>`gate/verificar.py`: G-PALETA | G-CONTRASTE | Paleta y tipografía se eligen por contraste, marca y carácter, y se miden dos veces: los pares de colores sobre los tokens finales y el contraste real sobre los píxeles de la página. |
| R-IDE-04 | Parcial | AL-31 pp.9,14,24; GR-A04 p.24 | `motor/imagenes.py`: def procesar_logo<br>`gate/verificar.py`: G-LOGO<br>`motor/temas.py`: "fuego" | G-HUELLA, G-LOGO | El logo se usa íntegro: con su transparencia, sin recortar, recolorear ni deformar, y el Gate mide que cargue y que no cambie de proporción. La paleta fuego se tomó de los colores del logo; falta un campo de colores aprobados por el restaurante. |
| R-IDE-05 | Aplicada | AL-42 pp.4,5,33; UX-58 p.10 | `motor/temas.py`: MOVIMIENTOS<br>`motor/plantillas/urbano.css`: mural<br>`gate/verificar.py`: G-AVANCE<br>`gate/verificar.py`: G-MOVIMIENTO | G-MOVIMIENTO, G-AVANCE, G-REND | Movimiento lento para la personalidad elegante y rápido y grueso para la urbana (mural de fotos, brasas, titular que sube), las dos con pausa, sin efectos obligatorios y quietas con movimiento reducido. |
| R-IDE-06 | Aplicada | DM 6.2; GR-A04 p.24; UX-28 pp.13,30 | `motor/color.py`: def paleta_marca<br>`motor/color.py`: def colores_dominantes<br>`motor/color.py`: def elegir_acento<br>`gate/estatico.py`: def paleta<br>`gate/verificar.py`: G-PALETA | G-PALETA, G-CONTRASTE | Color de identidad del logo (k-means en OKLab, sin neutros), acento de temporada con relación de tono y unidad, fondos teñidos hacia la marca y ajuste automático de luminosidad hasta cumplir cada par de contraste; el Gate recalcula los pares sobre los colores finales. |
| R-IDE-07 | Aplicada | DM 5.4; DM 6.5 | `motor/antojo.py`: CRITERIOS<br>`motor/antojo.py`: def puntuar<br>`motor/piezas_urbano.py`: def _galeria<br>`gate/estatico.py`: def antojo<br>`gate/verificar.py`: G-ANTOJO | G-ANTOJO, G-FOTOS | Siete criterios juzgados mirando cada foto (65 %) y cuatro medidas técnicas (35 %); el orden del mural y de la galería es el del ranking y el Gate comprueba que lo que se ve coincide con el ranking del manifiesto. |
| R-IDE-08 | Aplicada | Orden de Eduardo 2026-10-08; R-IDE-05; R-LEG-06; R-REN-04 | `motor/catalogo.py`: PAQUETES<br>`motor/plantillas/a/particulas.js`: EDU.modulo<br>`motor/plantillas/base.js`: EDU.correrAnim<br>`gate/verificar.py`: G-ANIMACION | G-ANIMACION, G-MOVIMIENTO | Seis paquetes de animaciones (brasa, bruma, editorial, minimal, cartel, festivo) hechos de módulos; la web declara el suyo en el manifiesto y el Gate comprueba en el navegador que cada módulo arrancó (mínimo tres). Todo respeta el movimiento reducido y la pausa. |
| R-LEG-01 | Aplicada | UX-16 pp.12,21; AL-34 p.14; GR-G06 p.25; WCAG 2.2 SC 1.4.3 | `motor/temas.py`: PALETAS<br>`gate/dinamico.mjs`: muestrearContraste<br>`gate/verificar.py`: G-CONTRASTE | G-CONTRASTE, G-AXE | El contraste se mide sobre los píxeles reales (texto oculto, captura, relación por pixel), no sobre colores nominales. |
| R-LEG-02 | Aplicada | UX-17 p.21; WCAG 2.2 SC 2.5.8 | `motor/plantillas/base.css`: .btn{<br>`gate/verificar.py`: G-TACTIL44 | G-TACTIL | Botones de 3,25 rem y controles de al menos 44 px en móvil. |
| R-LEG-03 | Aplicada | AL-33 p.14; UX-19 pp.21,24,31; GR-G01 p.25; WCAG 2.2 SC 1.4.10 y 1.4.4 | `motor/plantillas/base.css`: @container<br>`motor/plantillas/elegante.css`: minmax(0,1fr)<br>`gate/verificar.py`: G-DESBORDE | G-DESBORDE | Reorganiza sin desbordar desde 280 px y con el texto al 200 por ciento; medido en 27 dispositivos. |
| R-LEG-04 | Aplicada | UX-15 pp.21,24; PS-27 p.6; GR-T03 p.25 | `motor/tipografia.py`: def glifos_faltantes<br>`gate/estatico.py`: def fuentes_glifos | G-FUENTES, G-DATOS | Texto real y todos los glifos presentes; si falta uno, no se genera. |
| R-LEG-05 | Aplicada | UX-21 pp.12,21,24; WCAG 2.2 SC 3.1.1, 1.3.1, 2.4.1, 2.4.7, 2.1.1, 4.1.2 | `motor/generar.py`: lang=<br>`motor/generar.py`: salto<br>`motor/plantillas/base.css`: :focus-visible<br>`gate/verificar.py`: G-AXE | G-ESTRUCTURA, G-AXE, G-FOCO | Idioma, un h1, regiones, enlace de salto, foco visible y teclado; axe y recorrido con Tab lo comprueban. |
| R-LEG-06 | Aplicada | WCAG 2.2 SC 2.2.2 y 2.3.1; UX p.7 (hueco); AL-42 pp.4,5,33 | `motor/plantillas/base.js`: data-pausa<br>`motor/plantillas/base.css`: prefers-reduced-motion<br>`gate/verificar.py`: G-MOVIMIENTO | G-MOVIMIENTO | Control de pausa visible y movimiento reducido respetado. |
| R-LEG-07 | Aplicada | UX-18 pp.21,30; GR-V05 p.26 | `gate/verificar.py`: G-TEXTO | G-TEXTO | Texto mínimo medido en pantalla: 14 px. |
| R-LEG-08 | Parcial | UX-58 p.10; GR p.5 (Tuch 2012); UX-47 pp.10,15 | `gate/verificar.py`: G-AXE | G-AXE | La estética no tapa los fallos de uso: axe y las pruebas funcionales corren siempre. La regla en si es un criterio de proceso. |
| R-LEG-09 | Aplicada | UX-24 p.9; UX-25 pp.21,30; GR-G05 p.25 | `motor/plantillas/elegante.css`: .fila<br>`gate/dinamico.mjs`: solapes | G-DESBORDE | Plato, descripción y precio comparten contenedor; el Gate detecta solapes y recortes. |
| R-MED-01 | Pendiente | CO-22 pp.7,8; PS-02 p.1; UX-46 pp.4,11,28 | - | G-MANIFIESTO | Aun no hay experimentos con clientes: todo efecto de la literatura es una hipótesis. |
| R-MED-02 | Parcial | CO-19 pp.2,7,9; PS-04 pp.3,4,7; UX-54 pp.3,14,15,18,27; AL-39 pp.10,23,30 | - | G-MANIFIESTO | La conducta objetivo existe como campo de la ficha (conducta), pero todavía no se mide. |
| R-MED-03 | Pendiente | AL-37 pp.17,18; UX-44 pp.27,28; GR sec.13 p.21 | - | G-MANIFIESTO | Se calcula el tamaño de muestra cuando haya un A/B que proponer. |
| R-MED-04 | Pendiente | UX-40 pp.13,16; UX-41 p.16; UX-42 pp.6,16 | - | G-VISUAL | Pruebas de tarea con 5 a 8 personas: tu revisión es la primera de ellas. |
| R-MED-05 | Aplicada | UX-55 p.15; CO sec.5 p.9; PS sec.6 | `gate/verificar.py`: G-RED | G-RED | No hay ninguna medición: ni cookies ni analítica. Cuando se añada será agregada y sin identificadores. |
| R-MED-06 | Pendiente | CO-25 p.8; UX-53 pp.8,12,13,17,19; AL-43 pp.14,29 | - | G-MANIFIESTO | Ningún modelo estima efectos; las variantes e hipótesis las propone el motor sin predecir resultados. |
| R-MED-07 | Pendiente | CO-24 pp.5,8,9; CO-23 pp.2,9; UX-47 pp.10,15 | - | G-MANIFIESTO | Análisis por mercado y subgrupo: cuando haya datos. |
| R-MUE-01 | Aplicada | UX-62 pp.6,7,14; PS-17 p.7 | `motor/piezas.py`: def cinta<br>`motor/generar.py`: noindex<br>`gate/estatico.py`: def muestra | G-META, G-MUESTRA | Cinta, noindex, cabecera X-Robots-Tag y robots.txt; el Gate lo exige en toda muestra. |
| R-MUE-02 | Aplicada | CO-11 pp.5,9; PS-13 p.7; UX-04 pp.14,20; UX-62 pp.6,7,14 | `motor/piezas.py`: def cierre_muestra<br>`motor/piezas.py`: def panel_edu | G-MUESTRA, G-PRIMERA | Una sola acción de contratación: WhatsApp a Edumashow con mensaje prellenado. |
| R-MUE-03 | Aplicada | AL-16 pp.6,9,13,34 | `motor/piezas.py`: def cierre_muestra | G-ETICA | El cierre habla en condicional y no menciona presupuesto ni margen. |
| R-MUE-04 | Aplicada | UX-62 pp.6,7,14; Medida: las 3 muestras actuales no tienen vista previa de enlace | `motor/generar.py`: og:title<br>`gate/estatico.py`: def meta | G-META | Titulo, descripción y vista previa; la imagen social necesita el dominio final (aviso del Gate). |
| R-MUE-05 | Parcial | AL sec.6 (suplantación); PS sec.6 | `gate/estatico.py`: def muestra | G-MUESTRA | Para un negocio real la ficha debe declarar el permiso, de dónde salen los datos y el permiso de cada foto; la muestra lo dice en el pie, lleva cinta y noindex, y el Gate lo exige. Que se le enseñe primero al dueño es un paso humano. |
| R-PER-01 | No aplica | PS-01 pp.1,4,6,7; CO-26 pp.5-6,8 | - | G-MANIFIESTO | Ninguna técnica de persuasión se activa por defecto: es la regla y se cumple por omisión. |
| R-PER-02 | No aplica | PS-22 pp.4,6; CO-26 pp.5-6,8; CO-07 p.8 | - | G-ETICA | No hay prueba social ni normas en las muestras. |
| R-PER-03 | No aplica | CO-27 p.5; PS-25 p.4; UX-56 pp.6,9,11; UX-57 pp.6,9 | - | G-MANIFIESTO | No se usan anclajes ni encuadres como palanca. |
| R-PRO-01 | Aplicada | UX-29 pp.3,5,8,20,22,23; GR sec.9 p.15; AL-32 pp.14,22,24 | `gate/verificar.py`: UNAVAILABLE | G-MANIFIESTO | El Gate falla cerrado: sin navegador no hay veredicto. El generador no aprueba su propia salida. |
| R-PRO-02 | Aplicada | UX-30 pp.21,22,23; AL-49 pp.13,22,24; GR-D02 p.26 | `motor/generar.py`: def hash_paquete<br>`gate/estatico.py`: def manifiesto | G-MANIFIESTO | El permiso se liga al hash SHA-256 del paquete exacto; cualquier cambio lo invalida. |
| R-PRO-03 | Aplicada | UX-31 pp.22,23,31; GR sec.9 p.15; GR Anexo B p.28 | `gate/verificar.py`: class Informe | G-MANIFIESTO | Cada comprobación tiene id, estado, gravedad, reglas, evidencia y detalle. |
| R-PRO-04 | Pendiente | UX-32 pp.13,24,29,33; GR-L01 p.27 | - | G-MANIFIESTO | Falta el banco formal de casos válidos y defectuosos con el que el Gate se prueba a sí mismo. |
| R-PRO-05 | Aplicada | UX-34 pp.7,21,24; GR-V01 p.26 | `gate/verificar.py`: def hoja_contacto<br>`gate/verificar.py`: G-VISUAL | G-VISUAL | Capturas reales de 27 dispositivos y revisión humana pendiente y visible. |
| R-PRO-06 | Aplicada | UX-36 p.18; AL-49 pp.13,22,24,29,31 | `motor/generar.py`: manifiesto | G-MANIFIESTO | El manifiesto trae versión, fecha, modo, país, ciudad, idioma, hash del paquete, id de ensamblado y huella de diseño. |
| R-PRO-07 | Aplicada | UX-51 pp.13,19,22,26; GR sec.4 p.7 | `gate/verificar.py`: aprobacion_de_eduardo | G-MANIFIESTO | El informe separa estado técnico, revisión visual, aprobación y entrega, y no promete ventas. |
| R-REN-01 | Aplicada | UX-26 p.21 (el estudio no da cifra); AL-42 pp.4,5,33; Core Web Vitals; Medida: Lumbre 61 a 95 al sacar fotos del HTML | `gate/rendimiento.mjs`: lighthouse<br>`gate/verificar.py`: G-REND<br>`config.json`: lcp_ms | G-REND | Lighthouse en móvil lento simulado y peso real descargado contra el presupuesto. |
| R-REN-02 | Aplicada | UX-20 p.21; UX-26 p.21; GR p.14 (densidad efectiva) | `motor/imagenes.py`: def picture_html<br>`gate/verificar.py`: G-RESOLUCION | G-REND, G-FOTOS | AVIF y WebP con srcset, JPEG de respaldo, tamaño declarado, miniatura borrosa y portada con prioridad. |
| R-REN-03 | Aplicada | GR p.13 (fuentes embebidas); UX-15 p.21 | `motor/tipografia.py`: def subconjunto_woff2<br>`gate/estatico.py`: def fuentes_glifos | G-FUENTES, G-REND | Subconjuntos WOFF2 propios con font-display swap. |
| R-REN-04 | Sin prueba | AL-42 pp.4,5,33; UX p.29 (ablación) | `motor/plantillas/base.js`: ResizeObserver | G-REND, G-MOVIMIENTO | JavaScript propio de unos 17 KB minificado. El tope de 30 KB lo imprime el generador pero el Gate no lo exige. |
| R-REN-05 | Aplicada | AL-47 p.22; UX-09 p.8 | `motor/generar.py`: _headers<br>`gate/verificar.py`: G-RED | G-RED | Un solo origen, cabeceras de caché inmutable y cero peticiones externas. |
| R-SIG-01 | Aplicada | CO-01 pp.5,8; UX-59 p.11; AL-17 pp.14,21; PS-11 p.7 | `motor/piezas.py`: def portada<br>`motor/plantillas/elegante.css`: 100svh<br>`gate/verificar.py`: G-PRIMERA | G-PRIMERA | Nombre y acción principal completos en la primera pantalla de los 27 dispositivos, incluidos horizontales. |
| R-SIG-02 | Aplicada | CO-02 pp.5,8; PS-08 pp.3,7; PS-12 p.7; UX-13 pp.7,15 | `motor/piezas.py`: def barra_movil<br>`motor/plantillas/base.js`: IntersectionObserver<br>`gate/verificar.py`: G-SIGUIENTE | G-SIGUIENTE | Barra fija en móvil y menú en escritorio. |
| R-SIG-03 | Aplicada | CO-03 pp.5,7,8; PS-08 pp.3,7; UX-10 pp.9,14,20 | `motor/piezas.py`: def wa_url<br>`motor/piezas.py`: def mapa_url<br>`gate/verificar.py`: wa.me | G-SIGUIENTE, G-FORMULARIO | WhatsApp con mensaje prellenado y mapa directo; el Gate valida el formato de cada enlace. |
| R-SIG-04 | Aplicada | CO-04 p.5; CO-05 pp.5-7; PS-09 p.3; PS-14 p.2 | `motor/piezas.py`: def reserva<br>`motor/plantillas/elegante.js`: form-reserva<br>`gate/verificar.py`: G-FORMULARIO | G-FORMULARIO | Cinco campos, valores por defecto (2 personas, hora cercana a las 20:00) y resumen antes de enviar. |
| R-SIG-05 | Sin prueba | UX-12 pp.7,9,14; PS-07 p.7 | `motor/piezas.py`: Reservar mesa | G-SIGUIENTE | Los botones dicen lo que hacen. El Gate valida los enlaces pero no lee las etiquetas. |
| R-SIG-06 | Parcial | CO-10 pp.5,8; AL-24 p.14; PS-12 p.7 | `motor/piezas.py`: def _plato<br>`gate/estatico.py`: def datos | G-DATOS | El precio va junto al nombre y se compara con la ficha; las condiciones de reserva o pedido no existen aun como datos. |
| R-SIG-07 | Sin prueba | PS-10 pp.2,7; UX-23 p.21 | `motor/plantillas/base.css`: .btn.suave | G-PRIMERA | Un control primario y los demás subordinados; el Gate solo comprueba que el primario se vea. |
| R-SIG-08 | Aplicada | UX-10 pp.9,14,20; UX-11 pp.21,24; AL-35 pp.14,24 | `gate/verificar.py`: enlace # sin destino | G-SIGUIENTE | Ningún enlace falso; Lighthouse además encontro uno sin destino y se corrigio. |
| R-SIG-09 | Parcial | PS-23 p.7 | `motor/piezas.py`: def carta | G-SIGUIENTE | La carta está a un toque y abierta por defecto, pero en Lumbre va después de la sección de historia. |
| R-SIG-10 | Parcial | UX-14 pp.8,14,15; CO-16 pp.8,9 | `motor/piezas.py`: def panel_edu | G-MANIFIESTO | La muestra aclara a quién llega el mensaje. Que el restaurante conteste es algo que ningún Gate puede medir. |
| R-SIG-11 | Parcial | PS-24 p.7; AL-19 pp.14,33,51; AL-20 pp.29,54 | `gate/estatico.py`: ETICA | G-ETICA | Titulares literales; el Gate no detecta vacíos de curiosidad. |
| R-SIG-12 | Aplicada | AL-18 pp.14,51; UX-56 pp.6,9,11; PS-26 p.6 | `gate/verificar.py`: G-ESTRUCTURA | G-ESTRUCTURA | Cada sección tiene un encabezado que dice su función (25 encabezados en Lumbre). |
| R-VAL-01 | Aplicada | Orden de Eduardo 2026-10-08; R-DAT-05; R-ETI-02 | `motor/valoracion.py`: def validar<br>`motor/valoracion.py`: def pieza<br>`gate/estatico.py`: def valoracion<br>`gate/verificar.py`: G-VALORACION | G-VALORACION, G-ETICA | La nota de Google solo sale de la ficha, con 4,0 o más, fecha de consulta y enlace; el Gate compara la pastilla de la portada y de la visita con la ficha. |
| R-VAL-02 | Aplicada | Orden de Eduardo 2026-10-08; R-ETI-02; R-DAT-05 | `motor/valoracion.py`: ningun comentario<br>`gate/estatico.py`: blockquote | G-VALORACION, G-ETICA | La ficha no admite campos de comentarios y el Gate bloquea bloques de reseñas y datos estructurados de reseñas. |
| R-VAR-01 | Aplicada | UX-27 pp.7,21,30; GR-V03 p.26; AL-29 pp.15,17,25; Orden de Eduardo 2026-10-08 | `motor/huella.py`: def comparar<br>`gate/verificar.py`: G-HUELLA | G-HUELLA | Huella de trece dimensiones con peso (familia, portada, carta, galería, paleta, tipografía, animaciones, ornamento, botones, densidad, textura, orden, forma y movimiento); el Gate exige 8 puntos de distancia con cada una de las últimas 12 webs y ninguna firma repetida en el registro. |
| R-VAR-02 | Parcial | AL-29 pp.15,17,25; AL-30 pp.17,31,40; UX-38 pp.25,33 | `motor/huella.py`: def huella<br>`motor/piezas_urbano.py`: PERSONALIDAD<br>`motor/estilo.py`: variante_paleta | G-MANIFIESTO | Hay dos personalidades materialmente distintas y el director propone la pareja tipográfica y el acento de temporada con alternativas, pero no asigna variantes al azar ni registra semillas: la misma ficha siempre da el mismo resultado. |
| R-VAR-03 | Aplicada | DM 6.3; Orden de Eduardo 2026-10-08 | `motor/huella.py`: def rotacion<br>`motor/tipografia.py`: CLASES<br>`motor/estilo.py`: def elegir_tipografia<br>`gate/verificar.py`: G-HUELLA | G-HUELLA | Fuente y clase del titular quedan en la huella y en el registro con su secuencia; el director solo propone parejas que no repiten y el Gate bloquea una repetición. |
| R-VAR-04 | Aplicada | Orden de Eduardo 2026-10-08; R-IDE-01 | `motor/catalogo.py`: def componer<br>`motor/catalogo.py`: OPCIONES<br>`motor/estilo.py`: def decidir<br>`motor/ornamentos.py`: def intercalar<br>`gate/verificar.py`: G-HUELLA | G-HUELLA | El director elige cada dimensión de composición según los rasgos del restaurante y la rotación, prueba cientos de combinaciones y se queda con la de mayor encaje que cumple la distancia con las últimas webs. Cada elección y su motivo van al manifiesto y al informe. |

## Los 54 controles del informe del motor grafico

El informe esta pensado para propuestas en PDF. Aquí se traducen a la web los controles que tienen equivalente y se marcan como no aplicables los que son propios del PDF.

| Control | Nombre | Estado | Dónde y por qué |
|---|---|---|---|
| I01 | Identidad confirmada | Aplicada | validar_ficha y G-DATOS: sin marcadores pendientes ni datos heredados. |
| I02 | Contrato comercial tipado | Aplicada | dinero.py exige país y moneda conocidos; G-DATOS compara cada importe. |
| I03 | Visibilidad del encargo | Parcial | No hay un campo de visibilidad por dato; la muestra evita presupuesto y margen (R-MUE-03). |
| I04 | Contacto verificado | Aplicada | El contacto sale de la ficha; G-SIGUIENTE valida el formato de wa.me, tel: y mapas, y que las redes sean solo las que declara la ficha. |
| S01 | Concepto específico | Parcial | La ficha declara sus acciones (reservar, llamar, mapa, redes) y la portada y la barra móvil las siguen; el motor aún no elige solo la acción a partir de la conducta. |
| S02 | Afirmaciones trazables | Parcial | Ver R-DAT-05. |
| S03 | Metricas originales | No aplica | La web no muestra metricas de audiencia. |
| S04 | Mercado documentado | No aplica | La web no atribuye audiencia geográfica. |
| S05 | Condiciones preservadas | Aplicada | Precios y horarios de la página son los de la ficha y el hash congela el paquete. |
| A01 | Procedencia del activo | Aplicada | Cada imagen lleva origen, licencia, permiso y el hash sha256 del archivo original en el manifiesto; los recortes de capturas dejan su caja y el hash de la captura en recortes.json. |
| A02 | Uso autorizado | Parcial | La ficha declara uso y permiso por foto; no hay perfil de fuentes admitidas por rol. |
| A03 | Original conservado | Aplicada | imagenes.py parte siempre del original y registra recortes y ajustes; no se inventa detalle. |
| A04 | Logo íntegro | Aplicada | procesar_logo no recorta ni recolorea y G-LOGO comprueba en cada dispositivo que carga, que su proporción en pantalla es la del archivo y que mide al menos 40 px. |
| A05 | Permiso documentado | Parcial | Campo de permiso por activo; la aprobación es un paso humano. |
| A06 | Evidencia protegida | Parcial | Punto de foco por imagen y recorte dirigido; sin prueba automática de que no se corte el sujeto. |
| A07 | Resolución efectiva | Aplicada | G-RESOLUCION mide cuanto se amplia cada foto en cada pantalla. |
| A08 | Variedad sin duplicados | Aplicada | Activos evita imágenes repetidas y G-HUELLA exige diseño distinto. |
| T01 | Fuente permitida | Parcial | Solo tipografías OFL del kit; no hay lista de vetos por marca. |
| T02 | Fuentes incorporadas | Aplicada | WOFF2 propias y G-RED comprueba que no se pide ninguna externa. |
| T03 | Glifos completos | Aplicada | glifos_faltantes impide generar y G-FUENTES lo repite sobre el paquete. |
| T04 | Sin deformación del cuerpo | Sin prueba | El CSS no escala el texto de forma anisotropa; no hay prueba automática. |
| T05 | Tinta sin recorte | Aplicada | G-DESBORDE detecta texto recortado por un contenedor. |
| T06 | Parrafos legibles | Parcial | Tamaño mínimo medido; interlineado y longitud de línea por CSS sin prueba. |
| G01 | Regiones respetadas | Aplicada | G-DESBORDE en 27 dispositivos y con texto al 200 por ciento. |
| G02 | Superposicion declarada | Aplicada | G-DESBORDE detecta solapes de texto y controles; las capas decorativas estan declaradas. |
| G03 | Zonas seguras | Parcial | Margenes y área segura inferior para la barra; sin prueba específica de muescas. |
| G04 | Precio alineado | Parcial | Espacio duro entre símbolo e importe y alineación de base; sin prueba de la línea base. |
| G05 | Separacion de líneas | Sin prueba | Separaciones por CSS; sin prueba automática. |
| G06 | Contraste suficiente | Aplicada | G-CONTRASTE sobre el fondo compuesto real. |
| G07 | Recorte de producto | Parcial | Foco por imagen; sin prueba automática del sujeto. |
| G08 | Color y transparencia | Parcial | El logo conserva su transparencia (AVIF y WebP con alfa y PNG de respaldo) y su borde se suavizó con máscara supermuestreada; no hay prueba automática de halos ni de perfil de color. |
| V01 | Todas las páginas revisadas | Parcial | Capturas de 27 dispositivos en una hoja; la revisión humana (la tuya) es el paso que falta para aprobar. |
| V02 | Nivel visual pertinente | Parcial | Comparación antes y después de Lumbre; sin referencias autorizadas más allá de ella. |
| V03 | Independencia creativa | Aplicada | La huella de diseño impide clonar una web cambiando solo la identidad. |
| V04 | Densidad con función | No aplica | Es un criterio de diseño que no se puede medir con un script. |
| V05 | Jerarquía móvil | Aplicada | G-PRIMERA: concepto y siguiente paso visibles en el primer tramo. |
| V06 | Detalle verificable | Aplicada | Pruebas con texto al 200 por ciento: nada se corta ni se solapa. |
| P01 | Apertura estructural (PDF) | No aplica | Es un control de PDF; el equivalente web es que el HTML se lea sin errores (el Gate lo analiza, no usa un validador externo). |
| P02 | Contenido extraible (PDF) | No aplica | Equivalente web: todo el texto esencial es texto real. |
| P03 | Páginas e integridad (PDF) | No aplica | Equivalente web: manifiesto con todos los archivos y su hash. |
| P04 | Enlaces correctos (PDF) | Parcial | El formato de cada enlace se valida; que el destino siga vivo no se comprueba. |
| P05 | Compatibilidad contrastada (PDF) | Parcial | Solo Chromium emulando dispositivos; Safari y Firefox reales no estan probados. |
| P06 | Accesibilidad del perfil (PDF) | Aplicada | axe en tres tamaños y recorrido con teclado. |
| D01 | Paquete completo | Aplicada | Carpeta, zip, manifiesto y licencias. |
| D02 | Identidad del artefacto | Aplicada | El informe lleva el hash del paquete y el Gate lo recalcula. |
| D03 | Constancia auténtica | Aplicada | El informe lo escribe el Gate, no el generador. |
| D04 | Archivo almacenado | Aplicada | El paquete queda en el repositorio, en la rama de trabajo. |
| D05 | Lectura posterior | Pendiente | Hace falta un hosting para comprobar que lo publicado coincide con el hash. |
| D06 | Ruta de acceso valida | Pendiente | Idem: hasta que haya una URL pública no hay ruta que comprobar. |
| D07 | Sin cambio posterior | Aplicada | Cualquier cambio cambia el hash y obliga a pasar el Gate de nuevo. |
| D08 | Reintentos coherentes | Parcial | La generación es determinista por contenido; todavía no hay publicación que repetir. |
| L01 | Regresiones conservadas | Parcial | Cada defecto hallado se volvio una comprobación (desborde con texto grande, foco tapado, cifra que no avanza, enlace sin destino); falta el banco formal de casos. |
| L02 | Aprobaciones con autor | Aplicada | El informe separa técnico, revisión visual, aprobación de Eduardo y entrega. |
| L03 | Probabilidades justificadas | Aplicada | No se muestra ninguna probabilidad comercial. |

