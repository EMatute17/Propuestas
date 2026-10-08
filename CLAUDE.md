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
- Las fotos y vídeos deben tener licencia libre o ser del restaurante, con su procedencia registrada en el manifiesto de activos.

## Git

- Rama de desarrollo: claude/restaurant-web-engines-2t4cx7. No abrir pull requests salvo petición expresa.
- Mensajes de commit claros, en español, sin comillas angulares.
