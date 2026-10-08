# Guía paso a paso: de la hoja de un restaurante a su web (sin gastar crédito de Claude)

Esta guía es para ti, no para ChatGPT. No la subas al Proyecto.

## Qué hace cada cosa

1. ChatGPT (con el kit) lee los datos de UN restaurante y escribe su ficha: un archivo de texto con los datos, la carta y los textos. No gasta nada de Claude.
2. El validador y el motor (este repositorio) convierten la ficha en la web y la prueban. Es código: no gasta crédito de Claude cuando lo ejecutas tú.
3. El Gate dice si la web puede salir o no. Una web que no pasa no se entrega.

## Parte 1. El Proyecto en ChatGPT (unos 10 minutos, una sola vez)

1. En ChatGPT crea un proyecto nuevo (por ejemplo: Fichas Edumashow).
2. En las instrucciones del proyecto pega todo el contenido de INSTRUCCIONES.md (está dentro de kit_proyecto.zip).
3. Descomprime kit_proyecto.zip y sube al proyecto los 10 archivos de la carpeta conocimiento (del 01 al 10). No subas nada más.
4. Para cada restaurante, abre un chat NUEVO dentro del proyecto, pega la hoja de entrada (plantilla en conocimiento/08_hoja_de_entrada.md) y adjunta sus fotos como archivos.
5. ChatGPT responde con tres partes: la ficha (un bloque de código), Por confirmar y Decisiones. Guarda la ficha como ficha.json.

Regla de oro: un restaurante por chat. Nunca dos en el mismo.

## Parte 2. Convertir las fichas en webs (en tu computadora)

Instalar una sola vez:

1. Python 3.12 o más nuevo (python.org; en Windows marca la casilla Add Python to PATH).
2. Node.js versión LTS (nodejs.org).
3. El repositorio: en GitHub, EMatute17/Propuestas, rama claude/restaurant-web-engines-2t4cx7, botón Code, Download ZIP. Descomprímelo.
4. Abre una terminal dentro de la carpeta descomprimida y ejecuta, una línea por vez:

        pip install -r requirements.txt
        cd edumashow/gate
        npm install
        npx playwright install chromium
        cd ../..

Por cada tanda de restaurantes:

1. Crea una carpeta (por ejemplo MIS_FICHAS) con una subcarpeta por restaurante. El nombre de la subcarpeta es el id de la ficha. Dentro van ficha.json y una carpeta fotos con los archivos originales y el logo:

        MIS_FICHAS/donchucho/ficha.json
        MIS_FICHAS/donchucho/fotos/picada.jpg

2. Primera revisión, en segundos (revisa las fichas y construye las webs sin abrir el navegador):

        python scripts/lote.py MIS_FICHAS --salida MIS_WEBS --nivel estatico

   Abre MIS_WEBS/_resumen.md. Las fichas con errores no se construyen: para cada una ejecuta

        python scripts/validar_ficha.py MIS_FICHAS/donchucho/ficha.json --corregir

   y pega en el mismo chat de ChatGPT el mensaje que imprime. ChatGPT devuelve la ficha corregida completa.

3. Prueba en navegador real (unos 3 a 5 minutos por web, de tres en tres):

        python scripts/lote.py MIS_FICHAS --salida MIS_WEBS --nivel rapido --paralelo 3

4. Para las que queden bien, el Gate de entrega (27 dispositivos, más lento; necesita Google Chrome instalado):

        python scripts/lote.py MIS_FICHAS --salida MIS_WEBS --nivel completo --solo donchucho,otro

5. Cada web queda en MIS_WEBS/id (carpeta lista para subir) y en MIS_WEBS/id.zip. Mira MIS_WEBS/_informes/id/informe.md y las capturas antes de enviar nada.

## Cómo leer el resultado

- APTO: pasó el nivel del Gate que corriste. Falta siempre que una persona la mire y, si el negocio es real, el permiso del dueño.
- NO APTO: dice qué regla bloquea. Si es de la ficha, se corrige en ChatGPT; si es del diseño, avísame con el nombre de la web y la regla.
- SOLO PRUEBA: las fotos no cumplen la regla de calidad (originales de al menos 2400 px la portada y 1600 px el resto, ninguna de Instagram salvo el logo). No se puede entregar.

## Lo que conviene hacer primero

Haz un lote de diez restaurantes antes de pensar en mil. Mira cuántas fichas pasan el validador a la primera, cuántas webs pasan el Gate rápido y qué errores se repiten. Si se repite el mismo error, es del kit o del motor: arréglalo una vez y rehaz esas webs.

## Lo que no puedo prometerte

- Que ChatGPT funcione igual de bien que el modelo con el que lo probé (un modelo pequeño de Claude): con ChatGPT no se pudo probar.
- Que todas las combinaciones de diseño pasen el Gate a la primera. El Gate está para eso: una web con un fallo no sale. Si alguna combinación falla de forma repetida, se corrige en el motor.
- Que los datos sean ciertos: el Gate compara la web con la ficha, no la ficha con la realidad. Los datos los confirma el dueño.
- Que haya fotos buenas: las pone cada restaurante. Sin ellas la web queda en SOLO PRUEBA.
- No lo probé en Windows ni en Mac, solo en Linux.

## Si te queda poco crédito de Claude

Úsalo solo para tareas cortas y concretas, con el nombre de la web y el mensaje exacto del Gate. Por ejemplo: arreglar una combinación de diseño que falla, o añadir una tipografía. Todo lo demás (escribir fichas, validar, construir, verificar) lo hacen ChatGPT y el código sin gastar crédito de Claude.
