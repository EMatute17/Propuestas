# Cómo entregar fotos y videos de bancos libres

Regla de oro: el motor solo usa archivos que están dentro del repositorio y tienen su procedencia registrada.
No enlaza imágenes ni videos de otros sitios (por velocidad, por privacidad y porque así se puede probar y archivar la web exacta).

## Forma preferida (la que funciona hoy)

1. Descargar el archivo original, en la mayor resolución disponible, desde la página de la foto o del video.
2. Adjuntarlo en el chat (fotos en JPG, PNG, WebP o AVIF; videos en MP4 H.264 o WebM). Se pueden mandar varios a la vez o en un zip.
3. Adjuntar también la tabla de abajo, una fila por archivo, o pegarla en el mensaje.

Un enlace directo a una imagen no basta: el entorno donde se construye la web no tiene salida a esos bancos (ver la otra forma) y,
aunque la tuviera, el motor necesita el original para recortarlo, comprimirlo a AVIF y WebP y guardar su huella (sha256).

## Otra forma: abrir el acceso a los bancos

En el menú del entorno en la nube (barra de título de la sesión), Editar, Acceso a la red: agregar en dominios permitidos
`images.unsplash.com`, `unsplash.com`, `images.pexels.com`, `videos.pexels.com`, `pexels.com`, `cdn.pixabay.com` y `pixabay.com`
(dejando marcada la casilla de gestores de paquetes). Con eso solo hace falta pasar la URL de la página de cada foto o video;
el original se descarga, se comprueba la licencia en su página y se registra la procedencia.

## Tabla para cada archivo

| archivo | página de origen (URL de la foto, no del archivo) | autor | licencia | URL de la licencia | qué muestra | dónde usarla |
|---|---|---|---|---|---|---|
| brasas_01.jpg | https://www.pexels.com/photo/... | nombre del autor | Pexels License | https://www.pexels.com/license/ | brasas sobre una parrilla, sin personas | fondo de la portada |

Reglas de la tabla:
- No se inventa ningún autor ni licencia. Si no se ve en la página, la celda dice sin verificar y el archivo no se usa hasta confirmarlo.
- Las licencias de Unsplash, Pexels y Pixabay permiten uso comercial sin atribución obligatoria, pero no permiten usar marcas, logotipos
  ni personas reconocibles de forma que sugiera apoyo o relación con el restaurante. Por eso se prefieren fotos sin rostros ni marcas.
- Una foto de banco no se presenta como un plato ni un local reales de un restaurante. Sirve para ambiente (brasas, humo, madera, manos
  sin rostro) y para páginas de ejemplo claramente rotuladas. Los platos y el local reales son del restaurante y se usan con su permiso.

## Mensaje para el asistente que haga la búsqueda

> Busca en Unsplash, Pexels y Pixabay fotos y videos libres para una parrillada (brasas, llamas, humo, carne a la parrilla, madera, sin
> rostros ni marcas visibles). Para cada resultado dame: la URL de su página (no la del archivo), el autor tal como figura en la página,
> el nombre de la licencia y su URL, la resolución original, una descripción de lo que se ve y si aparecen personas o logotipos.
> No inventes datos: si algo no aparece en la página, escribe sin verificar. Prefiere resoluciones de 3000 px o más y videos de 10 a 20
> segundos, verticales y horizontales.

## Qué hace el motor con cada archivo

- Fotos: recorte opcional, AVIF y WebP con srcset, JPEG de respaldo, miniatura borrosa, color medio, sha256 del original, procedencia y
  licencia en `manifiesto.json` y en la página si son de referencia.
- Videos (aún no están construidos): portada con video mudo y en bucle, imagen fija previa para la carga, botón de pausa, y se detiene con
  movimiento reducido o ahorro de datos. Hasta que existan, un video entregado se guarda como activo y se usa su fotograma.
