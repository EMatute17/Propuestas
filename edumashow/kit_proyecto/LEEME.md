# Kit del Proyecto de fichas de Edumashow

Sirve para que ChatGPT (o un Proyecto de Claude) escriba las FICHAS de los restaurantes con el mismo criterio con el que se escriben aquí. No sirve para que escriba webs: las webs las hace el motor de este repositorio (con diseño propio para cada restaurante y animaciones de nivel premium) y las verifica el Gate. Esa división es la que permite hacer muchas webs buenas, distintas y baratas.

## Qué hace cada pieza

1. El Proyecto (ChatGPT o Claude) recibe la hoja de entrada de UN restaurante y devuelve su ficha en JSON. Es la parte que necesita redactar, interpretar datos desordenados y mirar fotos.
2. El validador (scripts/validar_ficha.py) comprueba la ficha en segundos: forma, reglas del motor, frases prohibidas y, lo nuevo, el origen y el tamaño de cada foto y la nota de Google. Si falla, entrega un mensaje listo para pegar de vuelta en el chat con los errores.
3. El motor (python3 -m edumashow.motor.generar) convierte la ficha en la web. No gasta tokens: elige la paleta desde el logo, la tipografía con rotación y la composición entera (portada, carta, galería, bordes entre secciones, botones, espaciado, textura y paquete de animaciones) según el perfil y los datos del restaurante, y comprueba que no se parezca a las últimas webs hechas.
4. El Gate (python3 -m edumashow.gate.verificar) prueba la web en navegador real. Sin prueba no hay aprobación.
5. Para muchos restaurantes, scripts/lote.py hace los pasos 2 a 4 con todas las fichas de una carpeta, de varias en varias.

## Montar el Proyecto en ChatGPT

1. Crea un proyecto nuevo (por ejemplo: Fichas Edumashow).
2. En las instrucciones del proyecto pega el contenido de INSTRUCCIONES.md (mide menos de 8.000 caracteres).
3. Sube los archivos de la carpeta conocimiento (los 9 del 01 al 09 y el esquema JSON del 10). No hace falta subir los estudios originales: sus reglas ya están en el archivo 04, con su fuente y su nivel de evidencia, y más archivos solo dispersan al modelo.
4. Para cada restaurante abre un chat NUEVO dentro del proyecto, pega la hoja de entrada (plantilla en el archivo 08) y adjunta las fotos originales (como archivos, no capturas) en el orden que dice la hoja. Envía.
5. Copia el JSON de la respuesta a CARPETA_LOTE/ID/ficha.json y guarda las fotos en CARPETA_LOTE/ID/fotos/ con los mismos nombres que dijiste en la hoja.
6. Ejecuta el validador. Si hay errores, pega al chat el mensaje que imprime con la opción --corregir; el modelo devuelve la ficha corregida y repites.

Para Claude (claude.ai) es igual: un Proyecto con las instrucciones en el campo de instrucciones y los mismos archivos como conocimiento.

## Flujo para muchos restaurantes

1. Antes de abrir el chat, reúne por restaurante: los datos de la hoja de entrada, los archivos originales de sus fotos (pídelos como documento, no como foto de chat, que la comprime) y la nota de Google con su número de reseñas y el día en que la miraste.
2. Un chat nuevo por restaurante. Guarda la ficha y las fotos en CARPETA_LOTE/ID/.
3. python3 scripts/validar_ficha.py CARPETA_LOTE/*/ficha.json   (corrige lo que marque)
4. python3 scripts/lote.py CARPETA_LOTE --nivel rapido --paralelo 3   (construye y verifica de a tres; mira _resumen.md y las capturas)
5. Con los que quedan bien: python3 scripts/lote.py CARPETA_LOTE --nivel completo --solo id1,id2   (el Gate de entrega, con 27 dispositivos y Lighthouse; es el único que registra la web como aprobada)
6. Revisión visual de una persona sobre las capturas, y permiso del dueño si el negocio es real, antes de enviar nada.

## Dos restaurantes a la vez

Cada restaurante en su propio chat, con su propia ficha y su propia carpeta de fotos. Así no hay forma de que se mezclen datos. Las instrucciones le dicen al modelo que avise si le pegas datos de otro negocio en el mismo chat. Aun así, el Gate compara cada web con su ficha, y el validador no deja pasar una ficha con otro nombre de carpeta, así que un cruce se vería.

## Lo que se probó con un modelo barato

Se probó con dos restaurantes inventados a la vez (Casa Almendra, elegante, y La Esquina del Patacón, urbano), cada uno en su propio chat, con un modelo pequeño de Claude (Haiku) en lugar de ChatGPT, que no está disponible desde aquí: **ChatGPT no se probó**. Las hojas de entrada iban desordenadas a propósito y con trampas: un comentario de un cliente pegado para publicar, un "el mejor italiano de la ciudad", una petición de poner "solo quedan 10 porciones" y "la oferta termina en una hora", una nota de Google de 3,8, una foto bajada de Instagram, una foto con el rótulo de otra marca, festivos que la ficha no admite y un horario que cruza la medianoche.

- Gastó unos 236.000 y 218.000 tokens (la mayor parte es leer el manual de 110 KB y mirar las fotos) y tardó unos 8 minutos cada uno, en paralelo.
- Pasó el validador a la primera (Casa Almendra) y a la segunda (La Esquina del Patacón: escribió un permiso pendiente dentro del campo licencia).
- No cayó en ninguna trampa: no copió el comentario ni el superlativo, no puso escasez, no puso la nota de 3,8, dejó fuera las dos fotos prohibidas y lo anotó en Por confirmar.
- Entre los dos señalaron doce puntos confusos del manual (el antojo en ELEGANTE, las reservas, qué número de WhatsApp guardar, cuándo una hoja es real o de ejemplo, el horario que cruza la medianoche, las fotos de menos de seis, el origen de las fotos de un ejemplo...). Todos están corregidos en esta versión del kit.
- Al construir las webs con esas fichas salieron dos fallos del propio motor que el Gate de Lumbre y Al Fuego no veía: la web elegante no mostraba el teléfono, y el Gate se caía si las categorías de la carta no se llamaban c0, c1... También quedó al descubierto que el menú de la cabecera enlazaba secciones que la ficha no tiene. Ya están corregidos.

Conclusión honesta: un modelo pequeño escribe fichas válidas y respeta las reglas de verdad con este manual, pero la prueba fue de dos restaurantes, no de cien. Haz primero un lote de diez y mira cuántos pasan el validador a la primera.

## Qué NO garantiza este kit

- Que los datos de la ficha sean los del restaurante real. El Gate compara la web con la ficha, no la ficha con la realidad: eso lo confirma el dueño. Por eso las fichas de negocios reales salen con estado por confirmar y las muestras llevan una cinta que lo dice.
- Que un modelo barato juzgue las fotos como lo haría una persona. Sus juicios de antojo son una primera pasada.
- Que existan fotos buenas. El kit no las consigue: cada restaurante debe aportar originales de al menos 1600 px (2400 px la de portada, 640 px el logo), sin Instagram ni otras redes (salvo el logo). Sin ellas el validador y el Gate no dejan entregar la web, y no hay excepción. Con fotos de baja calidad solo se puede probar el sistema (opción --fotos-de-prueba), y el resultado queda marcado como no entregable.
- Que la nota de Google sea cierta: la escribe quien prepara la hoja mirando la ficha de Google Maps, y la web la cita con su enlace y la fecha. Sin dato real o con menos de 4,0 no se muestra.
- Que el permiso del dueño exista: la muestra es privada para su dueño y el permiso queda pendiente hasta que lo conceda.
- Variedad infinita. Con el catálogo actual el motor puede dibujar 23.040 composiciones distintas en la familia elegante y 23.040 en la urbana (1.658.880 y 1.658.880 con tipografía y tono de paleta). El Gate exige que cada web difiera al menos 8 puntos de las últimas 12 y que no haya dos huellas iguales. Si una racha de restaurantes muy parecidos agota el catálogo, el Gate lo dice y toca ampliar el catálogo (más portadas, tipografías y paquetes de animación): es trabajo del motor, no del modelo que escribe fichas.

## Una excepción a una regla del proyecto

CLAUDE.md dice que el conocimiento vive en edumashow/nucleo y no se pega como texto en ningún prompt. ChatGPT no puede ejecutar ese núcleo, así que este kit es la excepción que pidió Eduardo, limitada a escribir fichas: lo que se puede comprobar con código (datos, ética, fotos, accesibilidad, rendimiento, variedad) se sigue comprobando con el validador y el Gate, no con el modelo. Los archivos de conocimiento no llevan datos de ningún restaurante real: los ejemplos son inventados.

## Cómo se genera este kit

Con python3 scripts/kit_proyecto.py. Los textos fijos están en edumashow/kit_proyecto/_fuentes y lo demás (reglas, parejas, opciones del catálogo de diseño, ejemplos, esquema) sale del propio repositorio, así que el kit se regenera cuando cambia el motor.

Archivos del kit:
- conocimiento/01_esquema_de_la_ficha.md (17 KB): Campo por campo: qué es cada dato de la ficha, cuál es obligatorio y los valores permitidos
- conocimiento/02_ejemplo_ficha_urbana.json (9 KB): Ficha completa de un restaurante ficticio URBANO (parrilla de pedido para llevar)
- conocimiento/03_ejemplo_ficha_elegante.json (6 KB): Ficha completa de un restaurante ficticio ELEGANTE (mantel, reservas)
- conocimiento/04_reglas_que_aplican.md (13 KB): Las reglas del núcleo que dependen de lo que escribes, con su puesto, su evidencia y qué haces tú
- conocimiento/05_guia_de_redaccion.md (8 KB): Cómo se redacta cada texto: principios, ejemplos, tono y lo que nunca se escribe
- conocimiento/06_juicio_de_antojo.md (3 KB): Cómo juzgar cada foto con los siete criterios (solo URBANO)
- conocimiento/07_elegir_estilo.md (9 KB): Cómo elegir la personalidad, el perfil del restaurante y qué decide el motor
- conocimiento/08_hoja_de_entrada.md (6 KB): La plantilla de lo que te pega el usuario, con dos ejemplos y las reglas de las fotos
- conocimiento/09_checklist_y_errores.md (5 KB): Lista de comprobación antes de responder y los errores más comunes del validador
- conocimiento/10_ficha.schema.json (23 KB): El esquema de la ficha en JSON Schema (la forma exacta que acepta el validador)
