# Informe del Gate: Al Fuego Grill (alfuego)

- **Veredicto técnico: APTO**
- Fecha: 2026-10-08T14:15:54Z | Gate 0.3.0 | Reglas 0.2.0
- Paquete (SHA-256): `3cf436c7fc3c4cede483d4580a2e6e663f35304ad5fa606b0677fbfacc703c70`
- Estados: técnico = APTO; revisión visual = pendiente: capturas generadas, falta la revisión de una persona; aprobación de Eduardo = pendiente; entrega = pendiente

## Resultado por comprobación

| ID | Resultado | Gravedad | Reglas | Evidencia |
|---|---|---|---|---|
| G-COMILLAS | **PASS** | bloqueo | R-ETI-12 | 6 archivos de texto revisados, 0 con comillas angulares |
| G-MARCA | **PASS** | bloqueo | R-ETI-11 | 0 menciones a herramientas de IA o a Peetfoodie |
| G-DATOS | **PASS** | bloqueo | R-DAT-01, R-DAT-02, R-DAT-03, R-DAT-08, R-SIG-06 | 74 importes (más 6 repetidos y 4 cifras derivadas recalculadas) y 1 horario comparados con la ficha; 0 discrepancias |
| G-ETICA | **PASS** | bloqueo | R-ETI-01, R-ETI-02, R-ETI-03, R-ETI-05, R-SIG-11 | 0 patrones de escasez, testimonios, promesas o refuerzo variable |
| G-META | **WARN** | bloqueo | R-MUE-01, R-MUE-04 | 0 fallos y 1 avisos de metadatos |
| G-MUESTRA | **PASS** | bloqueo | R-MUE-01, R-MUE-02, R-ETI-07, R-MUE-05 | negocio real con permiso declarado; 0 fallos |
| G-FOTOS | **PASS** | bloqueo | R-DAT-04 | 7 imágenes con origen y licencia registrados; 82 etiquetas img con alt |
| G-MANIFIESTO | **PASS** | bloqueo | R-PRO-02, R-PRO-06 | manifiesto completo y hash 3cf436c7fc3c verificado sobre 33 archivos |
| G-HUELLA | **PASS** | bloqueo | R-VAR-01, R-VAR-03 | distancia mínima 6 de 6 (se exigen 3); titular Anton (condensada); rotación frente a las 1 webs anteriores: sin repeticiones |
| G-PALETA | **PASS** | bloqueo | R-LEG-01, R-IDE-03, R-IDE-06 | 33 pares de colores medidos sobre los colores finales; el más justo: brasa-papel sobre papel-2 5.05:1 (se exige 4.5:1) |
| G-ANTOJO | **PASS** | defecto | R-IDE-07, R-DAT-04 | 6 fotos juzgadas con los 7 criterios; las mejores: lomo 89.0, sandwich 82.5, asador 81.7 |
| G-FUENTES | **PASS** | bloqueo | R-LEG-04, R-REN-03 | 2 tipografías revisadas contra 84 caracteres distintos |
| G-RED | **PASS** | bloqueo | R-ETI-08, R-REN-05 | 27 dispositivos: 0 peticiones externas, 0 errores de consola, 0 con cookies o almacenamiento, 0 respuestas 404 |
| G-ETICA-VISTA | **PASS** | bloqueo | R-ETI-04 | 27 dispositivos revisados |
| G-ESTRUCTURA | **PASS** | bloqueo | R-LEG-05, R-SIG-12 | 83 encabezados, 82 imágenes, 3 navegaciones |
| G-AXE | **PASS** | bloqueo | R-LEG-05, R-LEG-08 | 5 pruebas (tamaños y, con pedido, la hoja y el ticket armados): 0 graves y 0 leves |
| G-CONTRASTE | **PASS** | bloqueo | R-LEG-01, R-IDE-03 | 249 textos medidos sobre píxeles reales; el peor: .regla-nota 7.01:1 (se exige 4.5:1) |
| G-TACTIL24 | **PASS** | bloqueo | R-LEG-02 | 20 teléfonos y tablets |
| G-TACTIL44 | **PASS** | defecto | R-LEG-02 | 20 teléfonos y tablets |
| G-DESBORDE | **PASS** | bloqueo | R-LEG-03, R-LEG-09 | 27 dispositivos y 2 pruebas de zoom |
| G-TEXTO | **PASS** | defecto | R-LEG-07 | texto mínimo medido: 14 px |
| G-PRIMERA | **PASS** | bloqueo | R-SIG-01, R-SIG-07, R-MUE-02 | 27 dispositivos, incluidos horizontales y plegables |
| G-SIGUIENTE | **PASS** | bloqueo | R-SIG-02, R-SIG-03, R-SIG-08 | 34 enlaces revisados; barra fija en 16 de 16 móviles |
| G-HORARIO | **PASS** | bloqueo | R-DAT-03, R-DAT-08 | horario por confirmar: se muestra el texto de la ficha y la página no afirma que esté abierto o cerrado |
| G-FORMULARIO | **NA** | defecto | R-SIG-03, R-SIG-04, R-DAT-03 | no aplica: la ficha no tiene reservas y su acción principal es llamar |
| G-INTERACCION | **PASS** | bloqueo | R-LEG-05 | 7 categorías y Ver todo: clic, Enter y espacio; Escape y retorno del foco en el diálogo |
| G-PEDIDO | **PASS** | bloqueo | R-DAT-03, R-SIG-03, R-SIG-04, R-MUE-02 | 3 líneas de prueba (6 productos, total $176.00) en 2 dispositivos; destino la agencia (prueba) |
| G-LOGO | **PASS** | defecto | R-IDE-04 | 27 dispositivos; el logotipo más pequeño mide 48 px |
| G-FOCO | **PASS** | bloqueo | R-LEG-05 | 4 dispositivos recorridos con Tab |
| G-MOVIMIENTO | **PASS** | bloqueo | R-LEG-06, R-REN-04, R-IDE-05 | animaciones infinitas normales 8; con pausa 0; con movimiento reducido 0 |
| G-SINJS | **PASS** | bloqueo | R-LEG-06, R-REN-04, R-SIG-01 | 82 fotos revisadas con el JavaScript apagado en un teléfono de 390 px; el panel de la muestra abre y cierra por enlace |
| G-RESOLUCION | **PASS** | defecto | R-REN-02 | 0 fotos mostradas ampliadas más de un 25 por ciento en 4 dispositivos |
| G-VISUAL | **REVISAR** | asesor | R-PRO-05, R-MED-04 | 27 capturas en informes/alfuego/hoja_dispositivos.jpg; falta la revisión humana (Eduardo) y las pruebas con personas |
| G-REND | **PASS** | bloqueo | R-REN-01, R-REN-02, R-REN-03, R-REN-04 | Lighthouse móvil 99, LCP 1808 ms, CLS 0, TBT 50 ms; escritorio 100 |

## Detalle de avisos, fallos y excepciones

### G-META: Metadatos, noindex y vista previa al compartir (WARN)
- sin imagen de vista previa al compartir el enlace (se genera con --base-url)

### G-VISUAL: Revisión visual sobre el render real (REVISAR)

## Decisiones de diseño (director de estilo 0.1.0)

**Paleta: auto:fd751c.** derivada del logo (color de identidad #de7031, tono 47).

- Color de identidad sacado del logo: #de7031. Proporción: 60 % fondo, 30 % color de marca, 10 % acento de temporada.
- Acento de temporada (AW26/27, WGSN x Coloro, 12-09-2024): Transformative Teal (#016168), afinado hacia la marca a #057e87. Alternativas: Transformative Teal (relación de tono 0.66, unidad 0.25, puntos 0.476); Green Glow (relación de tono 0.15, unidad 0.75, puntos 0.418); Fresh Purple (relación de tono 0.15, unidad 0.55, puntos 0.328).
- Fondos: claro desde Wax Paper (#ECDCAF) teñido hacia el tono 69; oscuro desde Cocoa Powder teñido hacia el tono 32.
- Colores dominantes del logo: #010101 (47 %, neutro), #de7031 (12 %), #854131 (11 %), #d9d3ca (11 %, neutro), #331611 (10 %), #9b9391 (9 %, neutro).

| Rol | Color |
|---|---|
| tinta | `#0f0807` |
| tinta-2 | `#180f0d` |
| tinta-3 | `#211614` |
| crema | `#f9f1e9` |
| papel | `#faf1e7` |
| papel-2 | `#f1e4d6` |
| brasa | `#fd751c` |
| brasa-2 | `#f99e31` |
| brasa-papel | `#9f4503` |
| acento | `#69c9d2` |
| acento-papel | `#04585e` |

33 pares de contraste medidos al generar; el más justo: brasa-papel sobre papel-2 5.05:1 (se exigen 4.5:1).

**Tipografía del titular: Anton (condensada), pareja anton-archivo.** elegida por el director: la mejor probada que cubre los caracteres y cumple la rotación. Tonos del restaurante: parrilla, potente, callejero, urbano (sacados de la cocina, el nombre y la descripción).

| Pareja | Clase | Tonos que encajan | Puntos | Probada en el Gate | Rotación | Caracteres que faltan |
|---|---|---|---|---|---|---|
| anton-archivo | condensada | callejero, potente, parrilla, urbano | 1.05 | sí | sin repetición | - |
| bebas-manrope | condensada | potente, callejero, urbano | 0.8 | sí | sin repetición | - |
| archivo-condensado-inter | condensada | urbano, potente, parrilla | 0.8 | sí | sin repetición | - |
| archivo-expandido | expandida | urbano | 0.3 | sí | sin repetición | - |
| unbounded-manrope | expandida | - | 0.05 | sí | sin repetición | - |
| bricolage-outfit | grotesca | - | 0.05 | sí | sin repetición | - |
| outfit-outfit | geometrica | - | 0.0 | no | sin repetición | - |

**Fotos por antojo** (juicio visual 65 % y medidas técnicas 35 %; se usa el orden: sí).

| Foto | Puntos | Juicio visual | Técnica | Nota |
|---|---|---|---|---|
| lomo | 89.0 | 87.0 | 92.7 | Lomo con tocino ya cortado, con luz cálida lateral y la tabla con el nombre de la casa; se ve el interior jugoso. |
| sandwich | 82.5 | 81.0 | 85.2 | Carne en rebanadas con papas, plano cerrado y un solo plato; la carne apilada invita a morder. |
| asador | 81.7 | 73.0 | 97.8 | Asador vertical con brochetas junto a las brasas: calor y fuego a la vista, pero la composición está cargada y una barra metálica estorba. |
| tostones | 71.0 | 67.0 | 78.3 | Tostones con carne asada, queso y hierbas; el acero y el vasito de salsa le restan protagonismo. |
| picada | 70.5 | 67.0 | 77.1 | Chorizos, pollo y cortes a la parrilla sobre una tabla; el fondo de acero enfría la luz y la tabla es larga, no un solo plato. |
| trailer | 65.4 | 49.0 | 96.0 | Foto del lugar (el trailer con su logo), no de un plato: sirve para reconocer la marca, no para dar antojo. |

**Idea dibujada: regla de medidas** (picadas, en lb; medidas [1, 2, 3, 5]). Datos: medida y precio de cada plato, de la carta de la ficha.

## Dispositivos probados

| Dispositivo | Tamaño | Desborde | h1 y botón principal en la primera pantalla | Solapes | Recortes |
|---|---|---|---|---|---|
| iPhone SE (1.ª gen) | 320x568 @2 | 0 px | sí | 0 | 0 |
| Galaxy Z Fold plegado (estrés) | 280x653 @3 | 0 px | sí | 0 | 0 |
| iPhone SE (2.ª y 3.ª gen) | 375x667 @2 | 0 px | sí | 0 | 0 |
| iPhone 12 mini | 360x780 @3 | 0 px | sí | 0 | 0 |
| Galaxy S8 | 360x740 @4 | 0 px | sí | 0 | 0 |
| iPhone 12, 13 y 14 | 390x844 @3 | 0 px | sí | 0 | 0 |
| iPhone 14 Pro | 393x852 @3 | 0 px | sí | 0 | 0 |
| Pixel 7 | 412x915 @2.6 | 0 px | sí | 0 | 0 |
| Galaxy S20 Ultra | 412x915 @3.5 | 0 px | sí | 0 | 0 |
| iPhone 14 Pro Max | 430x932 @3 | 0 px | sí | 0 | 0 |
| iPhone SE horizontal | 667x375 @2 | 0 px | sí | 0 | 0 |
| iPhone 14 horizontal | 844x390 @3 | 0 px | sí | 0 | 0 |
| Pixel 7 horizontal | 915x412 @2.6 | 0 px | sí | 0 | 0 |
| Galaxy Z Fold desplegado | 673x841 @2.6 | 0 px | sí | 0 | 0 |
| iPad mini | 768x1024 @2 | 0 px | sí | 0 | 0 |
| iPad | 810x1080 @2 | 0 px | sí | 0 | 0 |
| iPad Pro 11 | 834x1194 @2 | 0 px | sí | 0 | 0 |
| iPad Pro 12.9 | 1024x1366 @2 | 0 px | sí | 0 | 0 |
| iPad horizontal | 1024x768 @2 | 0 px | sí | 0 | 0 |
| iPad Pro 11 horizontal | 1194x834 @2 | 0 px | sí | 0 | 0 |
| Portátil 1280 | 1280x720 @1 | 0 px | sí | 0 | 0 |
| Portátil 1366 | 1366x768 @1 | 0 px | sí | 0 | 0 |
| Escritorio 1440 | 1440x900 @1 | 0 px | sí | 0 | 0 |
| Portátil 1536 | 1536x864 @1.25 | 0 px | sí | 0 | 0 |
| Escritorio Full HD | 1920x1080 @1 | 0 px | sí | 0 | 0 |
| Escritorio 2K | 2560x1440 @1 | 0 px | sí | 0 | 0 |
| Ultrapanorámico | 3440x1440 @1 | 0 px | sí | 0 | 0 |

## Rendimiento (Lighthouse, mediana de 3 pasadas, servidor local con brotli)

| Perfil | Rendimiento | Accesibilidad | Buenas prácticas | LCP | CLS | TBT | Peso |
|---|---|---|---|---|---|---|---|
| móvil | 99 | 100 | 100 | 1808 ms | 0 | 50 ms | 146 KB |
| escritorio | 100 | 100 | 100 | 413 ms | 0.001 | 24 ms | 146 KB |

Peso realmente descargado (con compresión): iph-390: inicial 150 KB, total tras recorrer la página 150 KB; pc-1440: inicial 143 KB, total tras recorrer la página 143 KB

## Contraste medido sobre píxeles reales (peores 8)

| Elemento | Dispositivo | Contraste (5.º percentil) | Se exige | |
|---|---|---|---|---|
| .regla-nota "El precio por libra es el de c" | mini-768 | 7.01:1 | 4.5:1 | ok |
| .sobre "Churrascaria · Miami" | iph-390 | 7.31:1 | 4.5:1 | ok |
| .hero .btn "Llamar al 786 728 2934" | iph-390 | 7.31:1 | 4.5:1 | ok |
| .add "Agregar" | iph-390 | 7.31:1 | 4.5:1 | ok |
| .add "Agregar" | iph-390 | 7.31:1 | 4.5:1 | ok |
| .add "Agregar" | iph-390 | 7.31:1 | 4.5:1 | ok |
| .regla .add "Agregar" | iph-390 | 7.31:1 | 4.5:1 | ok |
| .regla .add "Agregar" | iph-390 | 7.31:1 | 4.5:1 | ok |

## Lo que este Gate no verifica

- Safari y Firefox reales: solo se probó Chromium con los tamaños, la densidad y el tacto de cada dispositivo emulados.
- Pruebas con personas reales (comprensión, confianza, facilidad): el Gate mide reglas, no personas.
- Que el restaurante conteste los mensajes de WhatsApp ni que los datos de la ficha sean ciertos.
- Rendimiento en el hosting real: se midió en un servidor local con compresión, sin CDN ni latencia de red real.
- Aspectos legales (RGPD, LSSI, alérgenos, permisos de uso de nombre y fotos): validar con asesoría legal.
