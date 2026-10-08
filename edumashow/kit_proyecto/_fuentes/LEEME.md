# Kit del Proyecto de fichas de Edumashow

Sirve para que ChatGPT (o un Proyecto de Claude) escriba las FICHAS de los restaurantes con el mismo criterio con el que se escriben aquí. No sirve para que escriba webs: las webs las hace el motor de este repositorio, y las verifica el Gate. Esa división es la que permite hacer muchas webs buenas y baratas.

## Qué hace cada pieza

1. El Proyecto (ChatGPT o Claude) recibe la hoja de entrada de UN restaurante y devuelve su ficha en JSON. Es la parte que necesita redactar, interpretar datos desordenados y mirar fotos.
2. El validador (scripts/validar_ficha.py) comprueba la ficha en segundos y, si falla, entrega un mensaje listo para pegar de vuelta en el chat con los errores.
3. El motor (python3 -m edumashow.motor.generar) convierte la ficha en la web. No gasta tokens: elige paleta desde el logo, tipografía con rotación, orden de fotos por antojo y dibuja la idea de la casa.
4. El Gate (python3 -m edumashow.gate.verificar) prueba la web en navegador real. Sin prueba no hay aprobación.
5. Para muchos restaurantes, scripts/lote.py hace los pasos 2 a 4 con todas las fichas de una carpeta, de varias en varias.

## Montar el Proyecto en ChatGPT

1. Crea un proyecto nuevo (por ejemplo: Fichas Edumashow).
2. En las instrucciones del proyecto pega el contenido de INSTRUCCIONES.md (mide menos de 8.000 caracteres).
3. Sube los archivos de la carpeta conocimiento (los 9 del 01 al 09 y el esquema JSON). No hace falta subir los estudios originales: sus reglas ya están en el archivo 04, con su fuente y su nivel de evidencia, y más archivos solo dispersan al modelo.
4. Para cada restaurante abre un chat NUEVO dentro del proyecto, pega la hoja de entrada (plantilla en el archivo 08), adjunta las fotos en el orden que dice la hoja y envía.
5. Copia el JSON de la respuesta a CARPETA_LOTE/ID/ficha.json y las fotos a CARPETA_LOTE/ID/fotos/ con los mismos nombres que dijiste en la hoja.
6. Ejecuta el validador. Si hay errores, pega al chat el mensaje que imprime con la opción --corregir; el modelo devuelve la ficha corregida y repites.

Para Claude (claude.ai) es igual: un Proyecto con las instrucciones en el campo de instrucciones y los mismos archivos como conocimiento.

## Dos restaurantes a la vez

Cada restaurante en su propio chat, con su propia ficha y su propia carpeta de fotos. Así no hay forma de que se mezclen datos. Las instrucciones le dicen al modelo que avise si le pegas datos de otro negocio en el mismo chat. Aun así, el Gate compara cada web con su ficha, y el validador no deja pasar una ficha con otro nombre de carpeta, así que un cruce se vería.

## Qué NO garantiza este kit

- Que los datos de la ficha sean los del restaurante real. El Gate compara la web con la ficha, no la ficha con la realidad: eso lo confirma el dueño. Por eso las fichas de negocios reales salen con estado por confirmar y las muestras llevan una cinta que lo dice.
- Que un modelo barato juzgue las fotos como lo haría una persona. Sus juicios de antojo son una primera pasada.
- Que las fotos de un negocio real se puedan usar. La muestra es privada para su dueño y el permiso queda pendiente hasta que lo conceda.
- Variedad entre mil webs. Con dos personalidades y trece parejas tipográficas, mil webs se parecerán entre sí; ver la recomendación aparte.

## Una excepción a una regla del proyecto

CLAUDE.md dice que el conocimiento vive en edumashow/nucleo y no se pega como texto en ningún prompt. ChatGPT no puede ejecutar ese núcleo, así que este kit es la excepción que pidió Eduardo, limitada a escribir fichas: lo que se puede comprobar con código (datos, ética, accesibilidad, rendimiento, variedad) se sigue comprobando con el validador y el Gate, no con el modelo.

## Cómo se genera este kit

Con python3 scripts/kit_proyecto.py. Los textos fijos están en edumashow/kit_proyecto/_fuentes y lo demás (reglas, parejas, ejemplos, esquema) sale del propio repositorio, así que el kit se regenera cuando cambia el motor.

Archivos del kit:
{{ARCHIVOS}}
