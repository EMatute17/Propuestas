# Edumashow: motor de webs para restaurantes

Un solo motor con dos modos:

- **Muestra**: una web de prueba, gratuita, que se prepara para un restaurante interesado. Lleva una cinta que dice Muestra de Edumashow, no se indexa en buscadores y avisa de qué datos son de ejemplo.
- **Final**: la web completa del restaurante que contrata, con sus datos y fotos reales.

El mismo motor, el mismo Gate y el mismo conocimiento sirven a los dos. Todo se hace en este repositorio.

## Estructura

| Carpeta | Qué hay |
|---|---|
| `edumashow/nucleo/` | El conocimiento unificado de los cinco estudios: reglas con prioridad, fuente, evidencia y prueba. Ver su README. |
| `edumashow/motor/` | El generador (ficha a sitio), las piezas de cada personalidad (elegante y urbana), el pedido con ticket en vivo (`pedido.py`, `pedido.js`), el director de estilo (`estilo.py`: paleta desde el logo en `color.py`, tipografía con rotación en `tipografia.py` y `huella.py`, fotos por antojo en `antojo.py`), los temas y el procesado de imágenes. |
| `edumashow/gate/` | El verificador: comprobaciones estáticas y pruebas en navegador real en 27 dispositivos (incluye el pedido, los filtros del menú, la página con el JavaScript apagado, los pares de colores, la rotación tipográfica y el aro de foco con el pedido en marcha). |
| `edumashow/fichas/` | Una ficha JSON por restaurante: datos, carta, horario, textos y estilo. |
| `edumashow/activos/origen/` | Fotos de origen: las de referencia de la muestra de ejemplo (Lumbre) y los recortes de las redes de Al Fuego Grill, con su `recortes.json`. La guía para pasar fotos y videos de bancos libres está en `edumashow/activos/GUIA_RECURSOS.md`. |
| `edumashow/fuentes/` | Tipografías libres (OFL) con su texto de licencia en `licencias/`. Las traídas de Fontsource van sin modificar y su origen está en `ORIGEN.md`. |
| `edumashow/kit_proyecto/` | El kit para que un Proyecto de ChatGPT o de Claude escriba las fichas (instrucciones, manual de 10 archivos y un LEEME con el paso a paso). Se regenera con `scripts/kit_proyecto.py`. |
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

Las dos muestras que hay hoy: `lumbre` (restaurante de ejemplo, personalidad elegante, con reservas por WhatsApp) y `alfuego` (negocio real, personalidad urbana, con llamada en un toque, menú con filtros, tarjetas con Agregar y ticket en vivo que sale por WhatsApp; sus datos y fotos salen de sus redes públicas y están por confirmar). Las dos se hicieron antes de las reglas de fotos del 8 de octubre (originales de la máxima calidad y nada de Instagram salvo el logo): hoy el Gate no las deja entregar y solo valen para probar el sistema. Para entregarlas hacen falta los originales del restaurante o fotos de un banco libre.

Muchos restaurantes (la ficha la escribe un modelo barato, el motor y el Gate hacen el resto):

    python3 scripts/validar_ficha.py CARPETA/*/ficha.json           # forma, reglas, fotos y nota de Google, en segundos
    python3 scripts/lote.py CARPETA --nivel rapido --paralelo 3     # construye y verifica de a tres; deja un resumen
    python3 scripts/lote.py CARPETA --nivel completo --solo id1,id2 # el Gate de entrega (27 dispositivos y Lighthouse)

La carpeta del lote tiene una subcarpeta por restaurante con su `ficha.json` y sus fotos. El paso a paso, con el kit para ChatGPT, está en `edumashow/kit_proyecto/LEEME.md`. Con `--fotos-de-prueba` se puede probar el sistema con fotos que no cumplen la regla de calidad; esas webs salen marcadas SOLO PRUEBA y no se pueden entregar.

Cada web elige su composición (portada, carta, galería, bordes, botones, densidad, textura y paquete de animaciones) entre las opciones del catálogo. Para comprobar con el Gate todos los pares de opciones y todas las tipografías:

    python3 scripts/cobertura_catalogo.py CARPETA --tipografias
    python3 scripts/lote.py CARPETA --salida SALIDA --nivel rapido --paralelo 3 --fotos-de-prueba
    python3 scripts/anotar_parejas_probadas.py SALIDA

Las parejas tipográficas que ya pasaron el Gate están en `edumashow/gate/parejas_probadas.json`; el director de estilo solo propone esas. Para traer más tipografías libres: `python3 scripts/traer_fuentes.py oswald:700 lora:400i,400` (comprueba la licencia OFL y anota el origen), y después se declaran en `edumashow/motor/tipografia.py` y se prueban como arriba. Para probar solo unas pocas con una ficha base: `python3 scripts/probar_parejas.py edumashow/fichas/alfuego.json bebas-manrope`.

La explicación de cómo se construyen estas webs y qué estudios se aplican en cada capa está en `edumashow/COMO_LO_HIZO.md`.

Subir a un hosting: sube la carpeta `muestras/lumbre` (o el zip). Trae `_headers` (seguridad, noindex y caché) y `robots.txt`, que funcionan en Netlify y Cloudflare Pages.

## Reglas de trabajo

Están en `CLAUDE.md`. Las principales: nunca comillas angulares, solo la marca Edumashow en los entregables, ninguna web sale sin pasar el Gate, no se promete ningún porcentaje de ventas, las fotos son originales de la máxima calidad y no vienen de redes sociales (solo el logo puede), la calificación de Google solo se muestra si es real y de 4,0 o más y sin comentarios, y cada web tiene su propia composición.

## Qué no cubre este Gate

Safari y Firefox reales (se prueba en Chromium emulando cada dispositivo), pruebas con personas, el rendimiento en el hosting real, que el restaurante conteste los mensajes y los aspectos legales. El informe de cada web lo recuerda.
