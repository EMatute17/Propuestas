# Informe del Gate: Al Fuego Grill (alfuego)

- **Veredicto técnico: APTO**
- Fecha: 2026-10-08T05:18:38Z | Gate 0.2.0 | Reglas 0.2.0
- Paquete (SHA-256): `7f71a00bc6273784136774997d317e1b9d8867e5852c5da71388b7a7cad485b0`
- Estados: técnico = APTO; revisión visual = pendiente: capturas generadas, falta la revisión de una persona; aprobación de Eduardo = pendiente; entrega = pendiente

## Resultado por comprobación

| ID | Resultado | Gravedad | Reglas | Evidencia |
|---|---|---|---|---|
| G-COMILLAS | **PASS** | bloqueo | R-ETI-12 | 6 archivos de texto revisados, 0 con comillas angulares |
| G-MARCA | **PASS** | bloqueo | R-ETI-11 | 0 menciones a herramientas de IA o a Peetfoodie |
| G-DATOS | **PASS** | bloqueo | R-DAT-01, R-DAT-02, R-DAT-03, R-DAT-08, R-SIG-06 | 74 importes y 1 horario comparados con la ficha; 0 discrepancias |
| G-ETICA | **PASS** | bloqueo | R-ETI-01, R-ETI-02, R-ETI-03, R-ETI-05, R-SIG-11 | 0 patrones de escasez, testimonios, promesas o refuerzo variable |
| G-META | **WARN** | bloqueo | R-MUE-01, R-MUE-04 | 0 fallos y 1 avisos de metadatos |
| G-MUESTRA | **PASS** | bloqueo | R-MUE-01, R-MUE-02, R-ETI-07, R-MUE-05 | negocio real con permiso declarado; 0 fallos |
| G-FOTOS | **PASS** | bloqueo | R-DAT-04 | 7 imágenes con origen y licencia registrados; 82 etiquetas img con alt |
| G-MANIFIESTO | **PASS** | bloqueo | R-PRO-02, R-PRO-06 | manifiesto completo y hash 7f71a00bc627 verificado sobre 33 archivos |
| G-HUELLA | **PASS** | bloqueo | R-VAR-01 | distancia mínima 6 de 6 (se exigen 3) |
| G-FUENTES | **PASS** | bloqueo | R-LEG-04, R-REN-03 | 2 tipografías revisadas contra 81 caracteres distintos |
| G-RED | **PASS** | bloqueo | R-ETI-08, R-REN-05 | 27 dispositivos: 0 peticiones externas, 0 errores de consola, 0 con cookies o almacenamiento, 0 respuestas 404 |
| G-ETICA-VISTA | **PASS** | bloqueo | R-ETI-04 | 27 dispositivos revisados |
| G-ESTRUCTURA | **PASS** | bloqueo | R-LEG-05, R-SIG-12 | 16 encabezados, 82 imágenes, 3 navegaciones |
| G-AXE | **PASS** | bloqueo | R-LEG-05, R-LEG-08 | 3 tamaños: 0 graves y 0 leves |
| G-CONTRASTE | **PASS** | bloqueo | R-LEG-01, R-IDE-03 | 259 textos medidos sobre píxeles reales; el peor: .cat-nota 5.29:1 (se exige 4.5:1) |
| G-TACTIL24 | **PASS** | bloqueo | R-LEG-02 | 20 teléfonos y tablets |
| G-TACTIL44 | **PASS** | defecto | R-LEG-02 | 20 teléfonos y tablets |
| G-DESBORDE | **PASS** | bloqueo | R-LEG-03, R-LEG-09 | 27 dispositivos y 2 pruebas de zoom |
| G-TEXTO | **PASS** | defecto | R-LEG-07 | texto mínimo medido: 14 px |
| G-PRIMERA | **PASS** | bloqueo | R-SIG-01, R-SIG-07, R-MUE-02 | 27 dispositivos, incluidos horizontales y plegables |
| G-SIGUIENTE | **PASS** | bloqueo | R-SIG-02, R-SIG-03, R-SIG-08 | 25 enlaces revisados; barra fija en 16 de 16 móviles |
| G-HORARIO | **PASS** | bloqueo | R-DAT-03, R-DAT-08 | horario por confirmar: se muestra el texto de la ficha y la página no afirma que esté abierto o cerrado |
| G-FORMULARIO | **NA** | defecto | R-SIG-03, R-SIG-04, R-DAT-03 | no aplica: la ficha no tiene reservas y su acción principal es llamar |
| G-INTERACCION | **PASS** | bloqueo | R-LEG-05 | 7 categorías: clic, teclado y barra pegada; Escape y retorno del foco en el diálogo |
| G-LOGO | **PASS** | defecto | R-IDE-04 | 27 dispositivos; el logotipo más pequeño mide 48 px |
| G-FOCO | **PASS** | bloqueo | R-LEG-05 | 4 dispositivos recorridos con Tab |
| G-MOVIMIENTO | **PASS** | bloqueo | R-LEG-06, R-REN-04, R-IDE-05 | animaciones infinitas normales 4; con pausa 0; con movimiento reducido 0 |
| G-RESOLUCION | **PASS** | defecto | R-REN-02 | 0 fotos mostradas ampliadas más de un 25 por ciento en 4 dispositivos |
| G-VISUAL | **REVISAR** | asesor | R-PRO-05, R-MED-04 | 27 capturas en informes/alfuego/hoja_dispositivos.jpg; falta la revisión humana (Eduardo) y las pruebas con personas |
| G-REND | **PASS** | bloqueo | R-REN-01, R-REN-02, R-REN-03, R-REN-04 | Lighthouse móvil 99, LCP 1812 ms, CLS 0, TBT 71 ms; escritorio 100 |

## Detalle de avisos, fallos y excepciones

### G-META: Metadatos, noindex y vista previa al compartir (WARN)
- sin imagen de vista previa al compartir el enlace (se genera con --base-url)

### G-VISUAL: Revisión visual sobre el render real (REVISAR)

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
| móvil | 99 | 100 | 100 | 1812 ms | 0 | 71 ms | 134 KB |
| escritorio | 100 | 100 | 100 | 408 ms | 0 | 8 ms | 134 KB |

Peso realmente descargado (con compresión): iph-390: inicial 138 KB, total tras recorrer la página 138 KB; pc-1440: inicial 131 KB, total tras recorrer la página 131 KB

## Contraste medido sobre píxeles reales (peores 8)

| Elemento | Dispositivo | Contraste (5.º percentil) | Se exige | |
|---|---|---|---|---|
| .cat-nota "Por media libra o por libra" | iph-390 | 5.29:1 | 4.5:1 | ok |
| .cat-nota "Por media libra o por libra" | se-horiz-667 | 5.29:1 | 4.5:1 | ok |
| .cat-nota "Por media libra o por libra" | mini-768 | 5.29:1 | 4.5:1 | ok |
| .cat-nota "Por media libra o por libra" | pc-1440 | 5.29:1 | 4.5:1 | ok |
| .nom-en "Picanha" | iph-390 | 5.88:1 | 4.5:1 | ok |
| .nom-en "Flap meat" | iph-390 | 5.88:1 | 4.5:1 | ok |
| .nom-en "Lamb chops" | iph-390 | 5.88:1 | 4.5:1 | ok |
| .nom-en "Filet mignon" | iph-390 | 5.88:1 | 4.5:1 | ok |

## Lo que este Gate no verifica

- Safari y Firefox reales: solo se probó Chromium con los tamaños, la densidad y el tacto de cada dispositivo emulados.
- Pruebas con personas reales (comprensión, confianza, facilidad): el Gate mide reglas, no personas.
- Que el restaurante conteste los mensajes de WhatsApp ni que los datos de la ficha sean ciertos.
- Rendimiento en el hosting real: se midió en un servidor local con compresión, sin CDN ni latencia de red real.
- Aspectos legales (RGPD, LSSI, alérgenos, permisos de uso de nombre y fotos): validar con asesoría legal.
