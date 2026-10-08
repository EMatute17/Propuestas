# Reglas permanentes del proyecto Edumashow

Estas reglas mandan sobre cualquier costumbre. Se aplican a todo lo que se escribe en este repositorio y en el chat.

## Comillas (orden directa de Eduardo)

- Nunca uses las comillas angulares dobles del español (los caracteres U+00AB y U+00BB).
- Usa siempre la comilla recta doble (") o la simple (').
- Vale para: respuestas en el chat, textos de las webs, código, comentarios, JSON, documentos y mensajes de commit.
- El Gate la comprueba con la regla G-COMILLAS y bloquea la entrega si aparece alguna. El script `scripts/revisar_comillas.py` revisa todo el repositorio y debe pasar antes de cada commit.
- En el código, para buscar esos caracteres se construyen con chr(0xAB) y chr(0xBB), nunca se escriben literales (y nunca se usan secuencias de escape unicode en herramientas de edición, porque se convierten en el carácter real).

## Marca y entregables

- La marca comercial es Edumashow. Las webs de muestra y las finales llevan solo esa marca.
- Ningún entregable (HTML, CSS, JS, textos, manifiestos públicos) menciona herramientas de IA, nombres de modelos ni nada de Peetfoodie. El Gate lo comprueba (G-MARCA).
- No se copia al repositorio nada del kit de propuestas de Peetfoodie salvo lo genérico y con licencia libre (tipografías OFL y su texto de licencia).
- El idioma de trabajo y de las webs por defecto es el español.

## Cómo se trabaja

- Todo se hace en este chat: las muestras para prospectos (motor básico) y las webs finales de clientes (versión completa).
- El conocimiento vive en `edumashow/nucleo/` como reglas con prioridad, fuente, nivel de evidencia y prueba. No se pega como texto en ningún prompt.
- Ninguna web sale sin pasar el Gate (`edumashow/gate/`). Sin prueba no hay aprobación. El generador no puede aprobar su propia salida.
- No se promete ningún porcentaje de ventas, reservas o contratos. Solo se informan medidas reales (Lighthouse, cumplimiento de reglas, tareas probadas).
- No se inventan datos del restaurante, reseñas, premios, escasez ni urgencia. Lo ficticio se rotula como ejemplo.
- Las fotos y vídeos deben tener licencia libre o ser del restaurante, con su procedencia registrada en el manifiesto de activos (ver la sección Fotos).

## Fotos (orden de Eduardo, 2026-10-08)

- Todas las fotos de una web son de la máxima calidad: originales sin ampliar ni recomprimir. El mínimo que comprueba el Gate (G-FOTOS) es de 2400 px de lado largo en la portada, 1600 px en las demás fotos y 640 px en el logo.
- Está prohibido usar fotos de Instagram o de cualquier otra red social. La única excepción es el logo, que se puede tomar del perfil del restaurante y se sube en la mayor calidad disponible.
- Las fotos que no son el logo son originales enviados por el restaurante (como archivo, no como captura ni reenviados por una red) o de un banco libre con la licencia comprobada. Su procedencia consta en el manifiesto.
- Esta regla no admite excepciones en el Gate. Una foto que no llega se sustituye por una mejor.

## Calificación de Google (orden de Eduardo, 2026-10-08)

- Si el restaurante tiene en Google una calificación de 4,0 o más, la web la muestra (estrellas, nota y número de reseñas, con enlace a su ficha de Google Maps).
- Solo se muestra un dato real, con fuente, fecha de consulta y enlace. Nunca se inventa, se redondea hacia arriba ni se muestra una nota menor de 4,0. Sin dato real no hay calificación.
- No se copia ningún comentario de clientes, ni bueno ni malo: la nota ya los resume todos. Se prohíbe en especial mostrar comentarios negativos o inventados.

## Diseño: cada web distinta y premium (orden de Eduardo, 2026-10-08)

- Está prohibido hacer webs iguales. Cada restaurante recibe una composición propia (portada, carta, galería, ornamentos, navegación y animaciones) elegida según sus datos reales (cocina, nivel de precio, ambiente, servicio, fotos y logo), no solo otros colores y otra tipografía.
- Toda web incluye animaciones de firma de nivel premium, y el paquete de animaciones cambia de una web a otra. Todas respetan el movimiento reducido, tienen pausa y la página es completa sin ellas.
- La composición elegida y su motivo constan en el manifiesto. El Gate bloquea una web que repite la composición de otra ya registrada.
- Lo premium se prueba con medidas (Gate completo, Lighthouse, contraste, accesibilidad) y con revisión visual sobre el render real; no se declara premium sin esa prueba.

## Git

- Rama de desarrollo: claude/restaurant-web-engines-2t4cx7. No abrir pull requests salvo petición expresa.
- Mensajes de commit claros, en español, sin comillas angulares.
