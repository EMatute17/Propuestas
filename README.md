# Edumashow: motor de webs para restaurantes

Un solo motor con dos modos:

- **Muestra**: una web de prueba, gratuita, que se prepara para un restaurante interesado. Lleva una cinta que dice Muestra de Edumashow, no se indexa en buscadores y avisa de qué datos son de ejemplo.
- **Final**: la web completa del restaurante que contrata, con sus datos y fotos reales.

El mismo motor, el mismo Gate y el mismo conocimiento sirven a los dos. Todo se hace en este repositorio.

## Estructura

| Carpeta | Qué hay |
|---|---|
| `edumashow/nucleo/` | El conocimiento unificado de los cinco estudios: reglas con prioridad, fuente, evidencia y prueba. Ver su README. |
| `edumashow/motor/` | El generador (ficha a sitio), las piezas, los temas, las tipografías y el procesado de imágenes. |
| `edumashow/gate/` | El verificador: comprobaciones estáticas y pruebas en navegador real en 27 dispositivos. |
| `edumashow/fichas/` | Una ficha JSON por restaurante: datos, carta, horario, textos y estilo. |
| `edumashow/activos/origen/` | Fotos de origen (hoy, fotos de referencia para las muestras de ejemplo). |
| `edumashow/informes/` | Informes del Gate por restaurante. |
| `muestras/` | Sitios generados, listos para subir (carpeta y zip). |

## Uso

Preparar el Gate (una vez):

    cd edumashow/gate && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install

Generar un sitio desde su ficha:

    python3 -m edumashow.motor.generar edumashow/fichas/lumbre.json --salida muestras
    python3 -m edumashow.motor.generar edumashow/fichas/lumbre.json --salida muestras --base-url https://TU-DOMINIO/lumbre/

La segunda forma añade la imagen de vista previa para cuando el enlace se comparte por WhatsApp (necesita la URL pública final).

Verificar el paquete exacto que se va a entregar:

    python3 -m edumashow.gate.verificar edumashow/fichas/lumbre.json --sitio muestras/lumbre
    python3 -m edumashow.gate.verificar edumashow/fichas/lumbre.json --sitio muestras/lumbre --rapido   # solo dispositivos representativos

Versión de un solo archivo para verla o enviarla como vista previa:

    python3 -m edumashow.motor.unico muestras/lumbre muestras/lumbre.unico.html

Subir a un hosting: sube la carpeta `muestras/lumbre` (o el zip). Trae `_headers` (seguridad, noindex y caché) y `robots.txt`, que funcionan en Netlify y Cloudflare Pages.

## Reglas de trabajo

Están en `CLAUDE.md`. Las principales: nunca comillas angulares, solo la marca Edumashow en los entregables, ninguna web sale sin pasar el Gate y no se promete ningún porcentaje de ventas.

## Qué no cubre este Gate

Safari y Firefox reales (se prueba en Chromium emulando cada dispositivo), pruebas con personas, el rendimiento en el hosting real, que el restaurante conteste los mensajes y los aspectos legales. El informe de cada web lo recuerda.
