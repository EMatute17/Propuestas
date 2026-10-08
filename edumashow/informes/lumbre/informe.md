# Informe del Gate: Lumbre (lumbre)

- **Veredicto técnico: NO APTO** (bloquean: G-FOCO)
- Fecha: 2026-10-08T02:28:16Z | Gate 0.1.0 | Reglas 0.1.0
- Paquete (SHA-256): `1c3006fec8411c7a05b4c90a43c99694940725c06c88091685dd6951170a2c29`
- Estados: técnico = NO APTO; revisión visual = pendiente: capturas generadas, falta la revisión de una persona; aprobación de Eduardo = pendiente; entrega = pendiente

## Resultado por comprobacion

| ID | Resultado | Gravedad | Reglas | Evidencia |
|---|---|---|---|---|
| G-COMILLAS | **PASS** | bloqueo | R-ETI-12 | 6 archivos de texto revisados, 0 con comillas angulares |
| G-MARCA | **PASS** | bloqueo | R-ETI-11 | 0 menciones a herramientas de IA o a Peetfoodie |
| G-DATOS | **PASS** | bloqueo | R-DAT-01, R-DAT-02, R-DAT-03, R-DAT-08, R-SIG-06 | 10 importes y 7 horarios comparados con la ficha; 0 discrepancias |
| G-ETICA | **PASS** | bloqueo | R-ETI-01, R-ETI-02, R-ETI-03, R-ETI-05, R-SIG-11 | 0 patrones de escasez, testimonios, promesas o refuerzo variable |
| G-META | **WARN** | bloqueo | R-MUE-01, R-MUE-04 | 0 fallos y 1 avisos de metadatos |
| G-FOTOS | **PASS** | bloqueo | R-DAT-04 | 11 imágenes con origen y licencia registrados; 11 etiquetas img con alt |
| G-MANIFIESTO | **PASS** | bloqueo | R-PRO-02, R-PRO-06 | manifiesto completo y hash 1c3006fec841 verificado sobre 69 archivos |
| G-HUELLA | **PASS** | bloqueo | R-VAR-01 | no hay otras webs registradas con las que comparar (primera del registro) |
| G-FUENTES | **PASS** | bloqueo | R-LEG-04, R-REN-03 | 3 tipografías revisadas contra 73 caracteres distintos |
| G-RED | **PASS** | bloqueo | R-ETI-08, R-REN-05 | 27 dispositivos: 0 peticiones externas, 0 errores de consola, 0 con cookies o almacenamiento, 0 respuestas 404 |
| G-ETICA-VISTA | **PASS** | bloqueo | R-ETI-04 | 27 dispositivos revisados |
| G-ESTRUCTURA | **PASS** | bloqueo | R-LEG-05, R-SIG-12 | 25 encabezados, 11 imágenes, 2 navegaciones |
| G-AXE | **PASS** | bloqueo | R-LEG-05, R-LEG-08 | 3 tamaños: 0 graves y 0 leves |
| G-CONTRASTE | **PASS** | bloqueo | R-LEG-01, R-IDE-03 | 63 textos medidos sobre píxeles reales; el peor: .galeria figcaption 5.89:1 (se exige 4.5:1) |
| G-TACTIL24 | **PASS** | bloqueo | R-LEG-02 | 20 teléfonos y tablets |
| G-TACTIL44 | **PASS** | defecto | R-LEG-02 | 20 teléfonos y tablets |
| G-DESBORDE | **PASS** | bloqueo | R-LEG-03, R-LEG-09 | 27 dispositivos y 2 pruebas de zoom |
| G-TEXTO | **PASS** | defecto | R-LEG-07 | texto mínimo medido: 14 px |
| G-PRIMERA | **PASS** | bloqueo | R-SIG-01, R-SIG-07, R-MUE-02 | 27 dispositivos, incluidos horizontales y plegables |
| G-SIGUIENTE | **PASS** | bloqueo | R-SIG-02, R-SIG-03, R-SIG-08 | 16 enlaces revisados; barra fija en 16 de 16 móviles |
| G-HORARIO | **PASS** | bloqueo | R-DAT-03, R-SIG-02 | 11 casos simulados |
| G-FORMULARIO | **PASS** | defecto | R-SIG-03, R-SIG-04, R-DAT-03 | 5 campos; se probó envío vacío, envío completo y día cerrado |
| G-INTERACCION | **PASS** | bloqueo | R-LEG-05 | flechas, Fin, Escape y retorno del foco |
| G-FOCO | **FAIL** | bloqueo | R-LEG-05 | 4 dispositivos recorridos con Tab |
| G-MOVIMIENTO | **PASS** | bloqueo | R-LEG-06, R-REN-04, R-IDE-05 | animaciones infinitas normales 2; con pausa 0; con movimiento reducido 0 |
| G-RESOLUCION | **WARN** | defecto | R-REN-02 | 6 fotos mostradas ampliadas más de un 25 por ciento en 4 dispositivos |
| G-VISUAL | **REVISAR** | asesor | R-PRO-05, R-MED-04 | 27 capturas en informes/lumbre/hoja_dispositivos.jpg; falta la revisión humana (Eduardo) y las pruebas con personas |
| G-REND | **PASS** | bloqueo | R-REN-01, R-REN-02, R-REN-03, R-REN-04 | Lighthouse móvil 99, LCP 2180 ms, CLS 0, TBT 0 ms; escritorio 100 |

## Detalle de avisos, fallos y excepciones

### G-META: Metadatos, noindex y vista previa al compartir (WARN)
- sin imagen de vista previa al compartir el enlace (se genera con --base-url)

### G-FOCO: Teclado: orden, alcance y foco siempre visible (FAIL)
- se-horiz-667: foco tapado por la barra fija en ['div.galeria']

### G-RESOLUCION: Resolución de las fotos suficiente para cada pantalla (WARN)
- Excepción documentada en la ficha: Las fotos son de referencia y de baja resolución (la portada original mide 1398 px de ancho). Se sustituyen por fotos propias del restaurante o de banco libre en la versión final.
- iph-390: hero-m necesita x2.48 su resolución original (770x962)
- mini-768: hero necesita x2.03 su resolución original (1398x962)
- se-horiz-667: hero-m necesita x1.75 su resolución original (770x962)
- se-horiz-667: sala_azul necesita x1.44 su resolución original (1280x720)
- mini-768: sala_azul necesita x1.44 su resolución original (1280x720)
- iph-390: sala_azul necesita x1.42 su resolución original (1280x720)

### G-VISUAL: Revisión visual sobre el render real (REVISAR)

## Dispositivos probados

| Dispositivo | Tamaño | Desborde | h1 y botón principal en la primera pantalla | Solapes | Recortes |
|---|---|---|---|---|---|
| iPhone SE (1.a gen) | 320x568 @2 | 0 px | si | 0 | 0 |
| Galaxy Z Fold plegado (estres) | 280x653 @3 | 0 px | si | 0 | 0 |
| iPhone SE (2.a y 3.a gen) | 375x667 @2 | 0 px | si | 0 | 0 |
| iPhone 12 mini | 360x780 @3 | 0 px | si | 0 | 0 |
| Galaxy S8 | 360x740 @4 | 0 px | si | 0 | 0 |
| iPhone 12, 13 y 14 | 390x844 @3 | 0 px | si | 0 | 0 |
| iPhone 14 Pro | 393x852 @3 | 0 px | si | 0 | 0 |
| Pixel 7 | 412x915 @2.6 | 0 px | si | 0 | 0 |
| Galaxy S20 Ultra | 412x915 @3.5 | 0 px | si | 0 | 0 |
| iPhone 14 Pro Max | 430x932 @3 | 0 px | si | 0 | 0 |
| iPhone SE horizontal | 667x375 @2 | 0 px | si | 0 | 0 |
| iPhone 14 horizontal | 844x390 @3 | 0 px | si | 0 | 0 |
| Pixel 7 horizontal | 915x412 @2.6 | 0 px | si | 0 | 0 |
| Galaxy Z Fold desplegado | 673x841 @2.6 | 0 px | si | 0 | 0 |
| iPad mini | 768x1024 @2 | 0 px | si | 0 | 0 |
| iPad | 810x1080 @2 | 0 px | si | 0 | 0 |
| iPad Pro 11 | 834x1194 @2 | 0 px | si | 0 | 0 |
| iPad Pro 12.9 | 1024x1366 @2 | 0 px | si | 0 | 0 |
| iPad horizontal | 1024x768 @2 | 0 px | si | 0 | 0 |
| iPad Pro 11 horizontal | 1194x834 @2 | 0 px | si | 0 | 0 |
| Portatil 1280 | 1280x720 @1 | 0 px | si | 0 | 0 |
| Portatil 1366 | 1366x768 @1 | 0 px | si | 0 | 0 |
| Escritorio 1440 | 1440x900 @1 | 0 px | si | 0 | 0 |
| Portatil 1536 | 1536x864 @1.25 | 0 px | si | 0 | 0 |
| Escritorio Full HD | 1920x1080 @1 | 0 px | si | 0 | 0 |
| Escritorio 2K | 2560x1440 @1 | 0 px | si | 0 | 0 |
| Ultrapanoramico | 3440x1440 @1 | 0 px | si | 0 | 0 |

## Rendimiento (Lighthouse, mediana de 3 pasadas, servidor local con brotli)

| Perfil | Rendimiento | Accesibilidad | Buenas prácticas | LCP | CLS | TBT | Peso |
|---|---|---|---|---|---|---|---|
| movil | 99 | 100 | 100 | 2180 ms | 0 | 0 ms | 179 KB |
| escritorio | 100 | 100 | 100 | 605 ms | 0 | 0 ms | 310 KB |

Peso realmente descargado (con compresión): iph-390: inicial 293 KB, total tras recorrer la página 293 KB; pc-1440: inicial 420 KB, total tras recorrer la página 420 KB

## Contraste medido sobre píxeles reales (peores 8)

| Elemento | Dispositivo | Contraste (5.o percentil) | Se exige | |
|---|---|---|---|---|
| .galeria figcaption "El rincón rojo" | iph-390 | 5.89:1 | 4.5:1 | ok |
| .hero h1 "LumbreLumbre" | pc-1440 | 4.08:1 | 3.0:1 | ok |
| .hero .btn "Reservar mesa" | iph-390 | 6.53:1 | 4.5:1 | ok |
| .barra-movil a "Reservar" | iph-390 | 6.53:1 | 4.5:1 | ok |
| .hero .btn "Reservar mesa" | se-horiz-667 | 6.53:1 | 4.5:1 | ok |
| .barra-movil a "Reservar" | se-horiz-667 | 6.53:1 | 4.5:1 | ok |
| .hero .btn "Reservar mesa" | mini-768 | 6.53:1 | 4.5:1 | ok |
| .hero-barra nav a "Carta" | pc-1440 | 6.53:1 | 4.5:1 | ok |

## Lo que este Gate no verifica

- Safari y Firefox reales: solo se probó Chromium con los tamaños, la densidad y el tacto de cada dispositivo emulados.
- Pruebas con personas reales (comprensión, confianza, facilidad): el Gate mide reglas, no personas.
- Que el restaurante conteste los mensajes de WhatsApp ni que los datos de la ficha sean ciertos.
- Rendimiento en el hosting real: se midió en un servidor local con compresión, sin CDN ni latencia de red real.
- Aspectos legales (RGPD, LSSI, alérgenos, permisos de uso de nombre y fotos): validar con asesoría legal.
