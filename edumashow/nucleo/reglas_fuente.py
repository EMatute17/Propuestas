"""Fuente del núcleo de conocimiento de Edumashow.

Aquí se escriben, una sola vez, las reglas unificadas que salen de los cinco estudios de Eduardo
(alianzas, psicología, UX, conducta y motor gráfico) más las normas técnicas y las medidas hechas
en este proyecto. Ejecutar este archivo regenera reglas.json y lo valida.

Convenciones
- prioridad: 0 verdad, legalidad y ética | 1 accesibilidad y legibilidad | 2 tarea del visitante |
  3 rendimiento en móvil lento | 4 identidad y estética | 5 persuasión (hipótesis) | 6 variedad |
  None = regla de proceso (como se construye, se prueba y se mide).
- tipo: bloqueo (impide entregar) | defecto (se aplica salvo razón documentada) | hipótesis (solo se
  activa si hay prueba propia) | prohibido (nunca) | proceso.
- evidencia: N norma o requisito técnico | M medida hecha en este proyecto | E1..E4 según el estudio de
  origen (E1 fuente primaria o metaanálisis, E2 fuente citada sin detalle, E3 criterio del autor,
  E4 sin respaldo). Ninguna E1 de los estudios es evidencia sobre webs de restaurante.
- fuentes: ID de la regla en el análisis de cada estudio (AL alianzas, PS psicología, UX motor
  predictivo UX, CO conducta, GR informe del motor gráfico) y páginas del estudio.
- gate: comprobaciones del Gate que la verifican (ver edumashow/gate).
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
PROHIBIDOS = (chr(0xAB), chr(0xBB))

PRIORIDADES = {
    0: "Verdad, legalidad y ética",
    1: "Accesibilidad y legibilidad",
    2: "Tarea del visitante: un siguiente paso claro y poca fricción",
    3: "Rendimiento en móvil lento",
    4: "Identidad y estética del restaurante",
    5: "Persuasión (solo como hipótesis a probar)",
    6: "Variedad entre webs (Gate de unicidad)",
}

REGLAS = []


def R(id, tema, regla, prio, tipo, publico, evid, fuentes, gate, notas="", modos=("muestra", "final")):
    REGLAS.append({
        "id": id, "tema": tema, "regla": regla, "prioridad": prio, "tipo": tipo, "publico": publico,
        "modos": list(modos), "evidencia": evid, "fuentes": fuentes, "gate": gate, "notas": notas,
    })


# ------------------------------------------------------------------ DATOS Y HONESTIDAD (prioridad 0)
R("R-DAT-01", "datos", "Todo dato factual visible (nombre, dirección, teléfono, horario, plato, precio, promoción, alérgeno) consta en la ficha confirmada con su fuente y fecha. Cero valores heredados de otra muestra o plantilla y cero marcadores de relleno.",
  0, "bloqueo", "ambos", "E3", ["UX-01 pp.20,31", "AL-01 pp.9,13,34", "AL-09 pp.13,20", "GR-I01 p.24"], ["G-DATOS", "G-ETICA"])
R("R-DAT-02", "datos", "Un dato ausente se omite o se muestra como por confirmar. Nunca aparece como 0, gratis o sin alérgenos por falta de dato: cero, desconocido y no aplicable no son lo mismo.",
  0, "bloqueo", "B", "E3", ["AL-03 pp.31,37", "UX-08 p.22", "AL-02 p.24"], ["G-DATOS"])
R("R-DAT-03", "datos", "Cada importe del HTML, de los metadatos y del mensaje de WhatsApp coincide uno a uno con la ficha. Un solo formato de moneda y decimales por página. La web no añade condiciones, depósitos ni descuentos que la ficha no tenga.",
  0, "bloqueo", "ambos", "E3", ["AL-04 pp.14,21", "AL-05 p.12", "UX-02 p.20", "UX-03 p.20", "GR-I02 p.24"], ["G-DATOS", "G-FORMULARIO"])
R("R-DAT-04", "datos", "Cada imagen y video declara su procedencia (propia del restaurante, licenciada de banco libre, de referencia o generada) y su licencia en el manifiesto de activos. Una imagen de referencia, de banco o generada no se presenta como el plato o el local reales: se rotula como imagen de ejemplo.",
  0, "bloqueo", "ambos", "E3", ["UX-06 pp.18,20,30", "GR-A01 p.24", "GR-A02 p.25", "PS-16 p.7"], ["G-FOTOS"])
R("R-DAT-05", "datos", "Toda afirmación factual (premios, antigüedad, superlativos, valoraciones, cifras) lleva fuente y fecha en la ficha. Sin fuente no se publica.",
  0, "bloqueo", "ambos", "E3", ["UX-05 pp.18,20", "AL-12 p.34", "PS-16 p.7", "CO-07 p.8"], ["G-ETICA", "G-DATOS"])
R("R-DAT-06", "datos", "Los datos volátiles (carta, precios, horarios, promociones) llevan fecha de última confirmación y se revalidan antes de cada entrega. Una promoción vencida no se muestra.",
  0, "defecto", "ambos", "E3", ["UX-07 pp.18,23", "AL-08 pp.12,34"], ["G-DATOS", "G-MANIFIESTO"])
R("R-DAT-07", "datos", "El texto que llega de webs, reseñas, redes o PDF del restaurante se trata como dato: se escapa y no puede alterar reglas, plantillas, enlaces ni el veredicto del Gate.",
  0, "bloqueo", "ambos", "E3", ["AL-10 pp.15,34", "UX-33 p.24"], ["G-DATOS"])
R("R-DAT-08", "datos", "Si falta un dato crítico (carta, horario o contacto) el motor omite el bloque y lo declara como limitación, o se abstiene de generar. No rellena con texto verosímil, ni platos de ejemplo, ni lorem ipsum.",
  0, "bloqueo", "ambos", "E3", ["UX-08 pp.18,22,33", "AL-09 p.13", "AL-50 pp.20,34"], ["G-DATOS", "G-MANIFIESTO"])
R("R-DAT-09", "datos", "Nombre, dirección y contacto corresponden al mismo establecimiento (identidad confirmada). Grupo y local son entidades distintas.",
  0, "bloqueo", "A", "E3", ["AL-06 pp.12,31", "GR-I01 p.24"], ["G-DATOS"])

# ------------------------------------------------------------------ ETICA, LEGALIDAD Y PRIVACIDAD (prioridad 0)
R("R-ETI-01", "etica", "Prohibida la escasez o urgencia inventada: cuentas atrás, quedan N mesas, últimas mesas, solo hoy. Solo se admite si se alimenta de un dato real, vigente y verificable del restaurante.",
  0, "prohibido", "ambos", "E3", ["CO-09 p.9", "PS-18 p.7", "AL-12 p.34"], ["G-ETICA"],
  "Normativa europea de prácticas comerciales desleales (Directiva 2005/29/CE): validar con asesoría legal.")
R("R-ETI-02", "etica", "Prohibidos los testimonios, reseñas, valoraciones, cifras de clientes o premios inventados. Los ejemplos ficticios de una muestra se rotulan como ejemplo. Una valoración real cita plataforma y fecha.",
  0, "prohibido", "ambos", "E3", ["CO-07 p.8", "CO-08 p.9", "PS-17 p.7", "AL-13 pp.9,14"], ["G-ETICA"],
  "Reseñas falsas: Directiva (UE) 2019/2161. Validar con asesoría legal.")
R("R-ETI-03", "etica", "Prohibido prometer resultados cuantificados (más reservas, más ventas, un porcentaje de mejora) y mostrar porcentajes con falsa precisión. Una nota de calidad nunca se presenta como probabilidad de éxito.",
  0, "prohibido", "ambos", "E3", ["UX-52 pp.1,10,22", "AL-14 p.16", "AL-15 pp.6,23", "CO-14 p.2", "PS-19 p.7", "GR p.7-8"], ["G-ETICA"])
R("R-ETI-04", "etica", "Decisión libre: sin ventanas bloqueantes al cargar, sin casillas premarcadas con coste o cesión de datos, y con salida o cierre visible en cada paso.",
  0, "bloqueo", "ambos", "E3", ["CO-06 p.9", "PS-20 p.7"], ["G-ETICA"])
R("R-ETI-05", "etica", "Sin refuerzo variable (ruletas, rasca y gana, premios sorpresa) ni copy encuadrado en pérdida por defecto (no te quedes sin mesa). Ninguna constante universal de aversión a la pérdida.",
  0, "prohibido", "ambos", "E2", ["PS-21 pp.3,7", "PS-25 p.4", "CO-27 p.5"], ["G-ETICA"])
R("R-ETI-06", "etica", "No se infiere ni se usa un perfil psicológico, estado emocional, salud o vulnerabilidad del dueño o del comensal para decidir diseño o texto. La personalización parte de necesidades observadas (sala, recoger, envío, grupo, idioma, hora).",
  0, "prohibido", "ambos", "E1", ["AL-27 pp.7,24,39", "PS-28 pp.1,3,4,7"], ["G-ETICA"])
R("R-ETI-07", "etica", "La muestra ofrece una vía visible y sencilla para declinar o pedir su retirada. Ninguna muestra se envía ni contacta automáticamente: la aprueba una persona antes.",
  0, "bloqueo", "A", "E3", ["CO-13 p.9", "AL-48 pp.15,22,37"], ["G-MUESTRA"], modos=("muestra",))
R("R-ETI-08", "etica", "Sin rastreo oculto: ninguna cookie, ningún script ni recurso de terceros en la carga. Los formularios piden solo los datos necesarios. Cualquier medición es agregada y declarada, o con consentimiento.",
  0, "bloqueo", "ambos", "E2", ["UX-09 pp.8,15,18,33", "AL-47 pp.7,22,31", "CO sec.6 p.9"], ["G-RED"],
  "RGPD y LSSI (art. 22.2) para analítica y cookies: validar con asesoría legal.")
R("R-ETI-09", "etica", "No se declara probado con usuarios lo que fue simulación, ni accesible o conforme a WCAG sin su alcance, ni el mejor sin un comparador y tareas definidos.",
  0, "bloqueo", "ambos", "E1", ["UX-22 pp.12,15,21", "UX-53 pp.8,12,13", "UX p.29"], ["G-ETICA"])
R("R-ETI-10", "etica", "Alérgenos, dietas y precios finales se muestran como texto real y solo si constan en la ficha. Ausencia de dato no es ausencia de alérgeno.",
  0, "bloqueo", "B", "N", ["AL-03 p.31", "PS sec.6"], ["G-DATOS"],
  "Reglamento (UE) 1169/2011 sobre información de alérgenos: validar con asesoría legal.", modos=("final",))
R("R-ETI-11", "etica", "Preferencia de marca de Eduardo: los entregables no mencionan herramientas de IA, nombres de modelos ni nada de Peetfoodie. Solo llevan la marca Edumashow. Esto no autoriza presentar imágenes generadas como reales (ver R-DAT-04).",
  0, "bloqueo", "ambos", "N", ["Orden de Eduardo"], ["G-MARCA"])
R("R-ETI-12", "etica", "Comillas: nunca se usan las comillas angulares dobles; siempre comillas rectas. Orden permanente de Eduardo.",
  0, "bloqueo", "ambos", "N", ["Orden de Eduardo"], ["G-COMILLAS"])

# ------------------------------------------------------------------ ACCESIBILIDAD Y LEGIBILIDAD (prioridad 1)
R("R-LEG-01", "legibilidad", "Contraste de texto de al menos 4,5:1 (3:1 en texto grande) medido sobre el fondo real bajo el texto, también sobre fotos, degradados y animaciones, no sobre un color nominal.",
  1, "bloqueo", "ambos", "N", ["UX-16 pp.12,21", "AL-34 p.14", "GR-G06 p.25", "WCAG 2.2 SC 1.4.3"], ["G-CONTRASTE", "G-AXE"])
R("R-LEG-02", "legibilidad", "Objetivos táctiles de al menos 24 por 24 px CSS (WCAG 2.2, bloqueo) y de 44 por 44 px en las acciones principales de móvil (defecto).",
  1, "bloqueo", "ambos", "N", ["UX-17 p.21", "WCAG 2.2 SC 2.5.8"], ["G-TACTIL"], "El umbral de 44 px es criterio de buenas prácticas móvil, no del estudio.")
R("R-LEG-03", "legibilidad", "Sin scroll horizontal, texto recortado ni elementos solapados desde 320 px de ancho (reflow) y con el texto ampliado al 200 por ciento.",
  1, "bloqueo", "ambos", "N", ["AL-33 p.14", "UX-19 pp.21,24,31", "GR-G01 p.25", "WCAG 2.2 SC 1.4.10 y 1.4.4"], ["G-DESBORDE"])
R("R-LEG-04", "legibilidad", "El texto esencial (nombre, precio, horario, CTA) es texto real, no imagen ni video. Todos los glifos necesarios (tildes, eñe, símbolos de moneda) existen en la fuente embebida o en una de respaldo legible.",
  1, "bloqueo", "ambos", "E3", ["UX-15 pp.21,24", "PS-27 p.6", "GR-T03 p.25"], ["G-FUENTES", "G-DATOS"])
R("R-LEG-05", "legibilidad", "Estructura accesible: idioma declarado, un solo h1, encabezados en orden, marcas de región (cabecera, principal, pie), texto alternativo, nombres accesibles, enlace de salto, foco visible y todo operable con teclado.",
  1, "bloqueo", "ambos", "N", ["UX-21 pp.12,21,24", "WCAG 2.2 SC 3.1.1, 1.3.1, 2.4.1, 2.4.7, 2.1.1, 4.1.2"], ["G-ESTRUCTURA", "G-AXE", "G-FOCO"])
R("R-LEG-06", "legibilidad", "Movimiento: se respeta prefers-reduced-motion, y todo movimiento automático de más de 5 segundos (canvas, bucles, desplazamientos) se puede pausar con un control visible y accesible. Sin destellos.",
  1, "bloqueo", "ambos", "N", ["WCAG 2.2 SC 2.2.2 y 2.3.1", "UX p.7 (hueco)", "AL-42 pp.4,5,33"], ["G-MOVIMIENTO"],
  "Ningún estudio cubre el movimiento; la regla viene de WCAG.")
R("R-LEG-07", "legibilidad", "Tamaño efectivo legible: texto de cuerpo de al menos 16 px y secundario de al menos 14 px en móvil, medidos sobre el render. Los conflictos de espacio no se resuelven encogiendo precio, horario o CTA.",
  1, "defecto", "ambos", "E3", ["UX-18 pp.21,30", "GR-V05 p.26"], ["G-TEXTO"], "Los mínimos en px son criterio propio del motor, no de los estudios.")
R("R-LEG-08", "legibilidad", "La estética no compensa fallos de lectura o de uso: una portada agradable no resuelve un contacto ausente, un precio incomprensible ni un archivo inaccesible. Atractivo y utilidad se miden por separado.",
  1, "proceso", "ambos", "E1", ["UX-58 p.10", "GR p.5 (Tuch 2012)", "UX-47 pp.10,15"], ["G-AXE"])
R("R-LEG-09", "legibilidad", "Proximidad y alineación: plato, descripción y precio comparten contenedor y alineación. Sin huecos accidentales ni líneas que crucen contenido.",
  1, "defecto", "ambos", "E1", ["UX-24 p.9", "UX-25 pp.21,30", "GR-G05 p.25"], ["G-DESBORDE"])

# ------------------------------------------------------------------ TAREA DEL VISITANTE (prioridad 2)
R("R-SIG-01", "siguiente_paso", "En el primer viewport de móvil (de 320 a 430 px de ancho) hay un h1 con el nombre, la cocina o la zona, y un CTA primario a un canal real (WhatsApp, teléfono o mapa) completamente visible, sin scroll ni menú previo.",
  2, "bloqueo", "ambos", "E3", ["CO-01 pp.5,8", "UX-59 p.11", "AL-17 pp.14,21", "PS-11 p.7", "PS-10 pp.2,7"], ["G-PRIMERA"],
  "El umbral de pantalla es operacionalización propia; los estudios piden que se vea oferta, coste y siguiente paso.")
R("R-SIG-02", "siguiente_paso", "Horario, dirección y contacto se alcanzan con un toque desde cualquier punto de la página (barra fija en móvil, cabecera o pie).",
  2, "defecto", "B", "E2", ["CO-02 pp.5,8", "PS-08 pp.3,7", "PS-12 p.7", "UX-13 pp.7,15", "AL-23 p.14"], ["G-SIGUIENTE"])
R("R-SIG-03", "siguiente_paso", "Los contactos abren la acción directamente: tel: para llamar y wa.me con el mensaje prellenado (restaurante y acción) para WhatsApp, sin páginas intermedias ni registro.",
  2, "bloqueo", "B", "E1", ["CO-03 pp.5,7,8", "PS-08 pp.3,7", "UX-10 pp.9,14,20"], ["G-SIGUIENTE", "G-FORMULARIO"],
  "La evidencia E1 es de recordatorios de salud; la traslación a web es inferencia.")
R("R-SIG-04", "siguiente_paso", "Formularios de reserva o pedido con solo los campos imprescindibles (no más de cinco), sin cuenta ni registro, con valores por defecto sensatos (dos personas, próxima franja disponible) y un resumen antes del envío.",
  2, "defecto", "B", "E2", ["CO-04 p.5", "CO-05 pp.5-7", "PS-09 p.3", "PS-14 p.2"], ["G-FORMULARIO"])
R("R-SIG-05", "siguiente_paso", "Cada botón dice lo que ocurre al pulsarlo (Reservar mesa, Pedir por WhatsApp, Cómo llegar), nunca Haz clic aquí, y su activación produce una respuesta visible. El rótulo coincide con la conducta objetivo declarada en la ficha.",
  2, "defecto", "ambos", "E2", ["UX-12 pp.7,9,14", "PS-07 p.7"], ["G-SIGUIENTE"])
R("R-SIG-06", "siguiente_paso", "El precio de cada plato es visible junto a su nombre y las condiciones de reserva o pedido (cancelación, mínimo, zona y coste de envío, plazos) se ven antes del paso final.",
  2, "defecto", "B", "E3", ["CO-10 pp.5,8", "AL-24 p.14", "PS-12 p.7"], ["G-DATOS"])
R("R-SIG-07", "siguiente_paso", "En cada tramo de pantalla hay un único control primario con más área y contraste que los demás. Los secundarios quedan subordinados.",
  2, "defecto", "ambos", "E3", ["PS-10 pp.2,7", "UX-23 p.21"], ["G-PRIMERA"])
R("R-SIG-08", "siguiente_paso", "Ningún enlace ficticio (#, javascript:void, example.com). Toda ancla existe y todo enlace tiene formato válido y lleva a lo que anuncia.",
  2, "bloqueo", "ambos", "E3", ["UX-10 pp.9,14,20", "UX-11 pp.21,24", "AL-35 pp.14,24"], ["G-SIGUIENTE"])
R("R-SIG-09", "siguiente_paso", "La carta, el precio y el horario no quedan detrás de la historia del local ni dentro de acordeones cerrados por defecto. La narrativa no se presume superior al dato.",
  2, "defecto", "ambos", "E2", ["PS-23 p.7"], ["G-SIGUIENTE"])
R("R-SIG-10", "siguiente_paso", "La web no promete lo que el restaurante no atiende (reserva por WhatsApp sin respuesta, reparto sin confirmar). El restaurante confirma cada promesa operativa antes de publicar.",
  2, "proceso", "ambos", "E3", ["UX-14 pp.8,14,15", "CO-16 pp.8,9"], ["G-MANIFIESTO"])
R("R-SIG-11", "siguiente_paso", "Titulares y CTA literales, sin vacíos de curiosidad (No imaginaras que lleva este plato). Los textos son concretos (ingredientes, técnica, origen) y concisos, sin superlativos sin respaldo.",
  2, "defecto", "ambos", "E2", ["PS-24 p.7", "AL-19 pp.14,33,51", "AL-20 pp.29,54"], ["G-ETICA"])
R("R-SIG-12", "siguiente_paso", "Escaneo: cada sección tiene un encabezado que declara su función (Carta, Reservar, Visítanos) y jerarquía tipográfica visible, sin muros de texto. No se fija un número mágico de platos o secciones: se prueba por tarea.",
  2, "defecto", "B", "E1", ["AL-18 pp.14,51", "UX-56 pp.6,9,11", "PS-26 p.6"], ["G-ESTRUCTURA"],
  "La sobrecarga de opciones tiene efecto medio cercano a cero (D 0,02): no hay base para límites fijos.")

# ------------------------------------------------------------------ RENDIMIENTO (prioridad 3)
R("R-REN-01", "rendimiento", "Presupuesto de carga en móvil lento simulado: transferencia inicial de 450 KB o menos, total de 1,5 MB o menos, LCP de 2,5 s o menos, CLS de 0,1 o menos y TBT de 200 ms o menos. Lighthouse móvil de 90 o más en rendimiento.",
  3, "bloqueo", "ambos", "M", ["UX-26 p.21 (el estudio no da cifra)", "AL-42 pp.4,5,33", "Core Web Vitals", "Medida: Lumbre 61 a 95 al sacar fotos del HTML"], ["G-REND"],
  "Cifras fijadas con medidas propias; el estudio de UX pide un presupuesto de bytes sin dar valor.")
R("R-REN-02", "rendimiento", "Imágenes: dimensiones declaradas (sin saltos de diseño), formatos AVIF y WebP con srcset, la imagen principal con prioridad alta y el resto diferido, sin duplicados, con píxeles nativos suficientes para su tamaño de colocación.",
  3, "defecto", "ambos", "M", ["UX-20 p.21", "UX-26 p.21", "GR p.14 (densidad efectiva)"], ["G-REND", "G-FOTOS"])
R("R-REN-03", "rendimiento", "Fuentes en subconjunto WOFF2 con font-display swap, como máximo dos precargadas y todas servidas desde el mismo origen.",
  3, "defecto", "ambos", "M", ["GR p.13 (fuentes embebidas)", "UX-15 p.21"], ["G-FUENTES", "G-REND"])
R("R-REN-04", "rendimiento", "Cada módulo costoso (animación, canvas, librería) justifica su coste. JavaScript propio de 30 KB o menos y adaptación a la capacidad del dispositivo (memoria, núcleos, ahorro de datos, movimiento reducido).",
  3, "defecto", "ambos", "E3", ["AL-42 pp.4,5,33", "UX p.29 (ablación)"], ["G-REND", "G-MOVIMIENTO"])
R("R-REN-05", "rendimiento", "Todos los recursos se sirven desde el mismo origen, con compresión y cabeceras de caché inmutables para los recursos con hash. Cero peticiones a terceros durante la carga.",
  3, "bloqueo", "ambos", "M", ["AL-47 p.22", "UX-09 p.8"], ["G-RED"])

# ------------------------------------------------------------------ IDENTIDAD Y ESTETICA (prioridad 4)
R("R-IDE-01", "identidad", "Cada web tiene identidad propia a partir de datos reales del restaurante (cocina, rango de precios, ciudad, marca, fotos). Toda variación se traza a un campo de la ficha; cambiar colores o adjetivos al azar no cuenta como adaptación.",
  4, "defecto", "ambos", "E3", ["AL-25 pp.21,45", "AL-26 pp.7,9,13", "UX-27 pp.7,21,30"], ["G-HUELLA"],
  "El estudio de alianzas define adaptativo como responder a diferencias verificadas.")
R("R-IDE-02", "identidad", "Las convenciones de la tarea se conservan (precio junto al nombre, categorías de carta, botón de acción reconocible en posición estable). Varia el estilo, no la tarea.",
  4, "defecto", "ambos", "E3", ["PS-15 p.4", "UX-27 p.21"], ["G-SIGUIENTE"])
R("R-IDE-03", "identidad", "Paleta, tipografía y proporciones se eligen por contraste, marca y población, no por prestigio de tendencia. El 60/30/10 y las paletas de moda son punto de partida, no ensayos de conversión.",
  4, "defecto", "ambos", "E3", ["UX-28 pp.13,30", "UX-60 pp.6,11"], ["G-CONTRASTE"])
R("R-IDE-04", "identidad", "Los activos de marca aprobados por el restaurante (logo, colores, tipografías, fotos) son restricciones fijas. La variación solo actúa sobre lo no fijado.",
  4, "defecto", "ambos", "E3", ["AL-31 pp.9,14,24", "GR-A04 p.24"], ["G-HUELLA"])
R("R-IDE-05", "identidad", "El movimiento tiene personalidad (elegante: lento y con aire; casual: rápido y grueso) y siempre respeta las reglas de legibilidad y rendimiento. Los efectos inmersivos son aditivos: la página es completa sin ellos.",
  4, "defecto", "ambos", "E3", ["AL-42 pp.4,5,33", "UX-58 p.10"], ["G-MOVIMIENTO", "G-REND"])

# ------------------------------------------------------------------ PERSUASION (prioridad 5, solo hipótesis)
R("R-PER-01", "persuasion", "Ninguna técnica de persuasión se activa por defecto en todas las webs. Cada módulo persuasivo lleva evidencia y estado (probada en este contexto o hipótesis), y las hipótesis no se activan sin prueba propia.",
  5, "hipotesis", "ambos", "E1", ["PS-01 pp.1,4,6,7", "CO-26 pp.5-6,8"], ["G-MANIFIESTO"])
R("R-PER-02", "persuasion", "La prueba social y las normas (el más pedido) solo se usan con dato real y fechado, y se les asigna un efecto esperado pequeño. No sustituyen a la reducción de fricción.",
  5, "hipotesis", "B", "E1", ["PS-22 pp.4,6", "CO-26 pp.5-6,8", "CO-07 p.8"], ["G-ETICA"],
  "Efecto de normas sociales: d 0,10 que desaparece al corregir sesgo de publicación (89 ensayos, N 85.759, salud).")
R("R-PER-03", "persuasion", "Anclaje, encuadre y otras heurísticas son descripciones de tareas concretas, no palancas con efecto garantizado. No se codifican constantes universales ni números mágicos de opciones.",
  5, "hipotesis", "ambos", "E1", ["CO-27 p.5", "PS-25 p.4", "UX-56 pp.6,9,11", "UX-57 pp.6,9"], ["G-MANIFIESTO"])

# ------------------------------------------------------------------ VARIEDAD (prioridad 6)
R("R-VAR-01", "variedad", "Gate de unicidad: la huella de diseño (paleta, tipografías, portada, carta, orden de secciones, forma y movimiento) difiere en al menos 3 de 6 dimensiones respecto de cada web ya registrada.",
  6, "bloqueo", "ambos", "E3", ["UX-27 pp.7,21,30", "GR-V03 p.26", "AL-29 pp.15,17,25"], ["G-HUELLA"],
  "Los estudios no definen familia de diseño ni distancia; la métrica de 6 dimensiones viene del kit de propuestas.")
R("R-VAR-02", "variedad", "Se generan pocas alternativas materialmente distintas, no decenas de variantes superficiales. Si la asignación de variante es aleatoria se registran semilla y probabilidad para poder evaluarla después.",
  6, "defecto", "ambos", "E2", ["AL-29 pp.15,17,25", "AL-30 pp.17,31,40", "UX-38 pp.25,33"], ["G-MANIFIESTO"])

# ------------------------------------------------------------------ MUESTRA (modo A)
R("R-MUE-01", "muestra", "La muestra se rotula (cinta Muestra de Edumashow para el restaurante), lleva noindex y la cabecera X-Robots-Tag, y distingue los datos de ejemplo de los reales.",
  0, "bloqueo", "A", "M", ["UX-62 pp.6,7,14", "PS-17 p.7"], ["G-META", "G-MUESTRA"], modos=("muestra",))
R("R-MUE-02", "muestra", "Una única acción de contratación visible en la primera pantalla y a un toque (WhatsApp con mensaje prellenado), con la oferta declarada: qué incluye, qué cuesta si procede, cuánto dura la prueba y qué ocurre al terminar.",
  2, "defecto", "A", "E1", ["CO-11 pp.5,9", "PS-13 p.7", "UX-04 pp.14,20", "UX-62 pp.6,7,14"], ["G-MUESTRA", "G-PRIMERA"], modos=("muestra",))
R("R-MUE-03", "muestra", "Las necesidades del restaurante se formulan como hipótesis o pregunta, nunca como hecho, y sin aludir a presupuesto, margen ni motivos privados.",
  0, "bloqueo", "A", "E3", ["AL-16 pp.6,9,13,34"], ["G-ETICA"], modos=("muestra",))
R("R-MUE-04", "muestra", "La muestra es compartible y explicable sin el autor: título con el nombre correcto, vista previa del enlace (Open Graph) y una URL estable que abre en móvil sin login.",
  2, "defecto", "A", "M", ["UX-62 pp.6,7,14", "Medida: las 3 muestras actuales no tienen vista previa de enlace"], ["G-META"], modos=("muestra",))
R("R-MUE-05", "muestra", "No se usan nombre, logo, fotos ni carta de un negocio real sin su permiso. La muestra para un prospecto real se enseña primero a su dueño. La cinta visible y el noindex evitan que se confunda con el sitio oficial.",
  0, "bloqueo", "A", "N", ["AL sec.6 (suplantación)", "PS sec.6"], ["G-MUESTRA"],
  "Propiedad intelectual y comunicaciones comerciales (LSSI art. 21): validar con asesoría legal.", modos=("muestra",))

# ------------------------------------------------------------------ PROCESO: GATE Y CONSTRUCCION
R("R-PRO-01", "proceso", "Puerta de liberación que falla cerrada: la ausencia de prueba es bloqueo, el generador no es el verificador, y ninguna nota de belleza, velocidad o persuasión compensa un fallo bloqueante. Un verificador caído nunca cuenta como aprobado.",
  None, "proceso", "ambos", "E3", ["UX-29 pp.3,5,8,20,22,23", "GR sec.9 p.15", "AL-32 pp.14,22,24"], ["G-MANIFIESTO"])
R("R-PRO-02", "proceso", "El permiso de entrega se liga al hash SHA-256 del paquete exacto que pasó el Gate. Cualquier edición posterior lo invalida.",
  None, "proceso", "ambos", "E3", ["UX-30 pp.21,22,23", "AL-49 pp.13,22,24", "GR-D02 p.26"], ["G-MANIFIESTO"])
R("R-PRO-03", "proceso", "Cada comprobación tiene identificador, método, estado (PASS, WARN, FAIL, UNAVAILABLE, N/A), evidencia y versión. N/A exige razón verificable. UNAVAILABLE bloquea una obligación.",
  None, "proceso", "ambos", "E3", ["UX-31 pp.22,23,31", "GR sec.9 p.15", "GR Anexo B p.28"], ["G-MANIFIESTO"])
R("R-PRO-04", "proceso", "El Gate se prueba a si mismo con un banco de casos válidos y defectuosos. Cada defecto confirmado pasa a caso de regresión permanente y no se reutiliza como muestra comercial.",
  None, "proceso", "ambos", "E3", ["UX-32 pp.13,24,29,33", "GR-L01 p.27"], ["G-MANIFIESTO"])
R("R-PRO-05", "proceso", "La revisión visual se hace sobre el render real en varios dispositivos y anchos, no solo sobre texto o coordenadas. Las notas de un modelo no validan por si solas la calidad visual.",
  None, "proceso", "ambos", "E3", ["UX-34 pp.7,21,24", "GR-V01 p.26"], ["G-VISUAL"])
R("R-PRO-06", "proceso", "Cada web emite un manifiesto con versión, fecha, país, ciudad, idioma, hash, plantilla y huella de diseño, tipografías, imágenes con su origen y licencia, enlaces, pesos y versión del generador.",
  None, "proceso", "ambos", "E3", ["UX-36 p.18", "AL-49 pp.13,22,24,29,31"], ["G-MANIFIESTO"])
R("R-PRO-07", "proceso", "Una puntuación no es una probabilidad. El informe separa conformidad, perfil de calidad y estimación comercial. Sin modelo calibrado, la estimación comercial dice no estimable de forma validada.",
  None, "proceso", "ambos", "E3", ["UX-51 pp.13,19,22,26", "GR sec.4 p.7"], ["G-MANIFIESTO"])

# ------------------------------------------------------------------ MEDICION
R("R-MED-01", "medicion", "Todo efecto tomado de la literatura es una hipótesis local y una cota superior: en las replicaciones el efecto fue aproximadamente la mitad (13 de 21 replicaron). Nunca se proyecta una ganancia con la cifra original.",
  None, "proceso", "ambos", "E1", ["CO-22 pp.7,8", "PS-02 p.1", "UX-46 pp.4,11,28"], ["G-MANIFIESTO"])
R("R-MED-02", "medicion", "El resultado primario es una conducta observable definida antes (clic a WhatsApp, reserva enviada, contratación), con unidad igual al restaurante y ventana fija. No se usan aperturas, elogios ni intención declarada.",
  None, "proceso", "ambos", "E3", ["CO-19 pp.2,7,9", "PS-04 pp.3,4,7", "UX-54 pp.3,14,15,18,27", "AL-39 pp.10,23,30"], ["G-MANIFIESTO"])
R("R-MED-03", "medicion", "Antes de proponer un A/B se calcula el tamaño necesario. Pasar de 10 a 12 por ciento exige unas 3.841 visitas por variante y de 20 a 30 por ciento unas 294 por grupo. Si el tráfico no alcanza no se hace el test ni se afirma mejora.",
  None, "proceso", "ambos", "E1", ["AL-37 pp.17,18", "UX-44 pp.27,28", "GR sec.13 p.21"], ["G-MANIFIESTO"])
R("R-MED-04", "medicion", "Con poco volumen se valida con pruebas de tarea de 5 a 8 personas representativas (dueños para la muestra, comensales con móvil de gama media y red lenta para la web final), con tareas que no inducen la respuesta.",
  None, "proceso", "ambos", "E2", ["UX-40 pp.13,16", "UX-41 p.16", "UX-42 pp.6,16"], ["G-VISUAL"])
R("R-MED-05", "medicion", "La medición es agregada y sin identificadores (conteo de clics a WhatsApp o llamada), o con consentimiento. Se filtran bots y previsualizadores de enlace antes de contar aperturas.",
  None, "proceso", "ambos", "E3", ["UX-55 p.15", "CO sec.5 p.9", "PS sec.6"], ["G-RED"])
R("R-MED-06", "medicion", "Un modelo de lenguaje propone variantes e hipótesis pero no estima efectos: sobrestima los tamaños de efecto. Los usuarios simulados no prueban comprensión, deseo ni confianza.",
  None, "proceso", "ambos", "E1", ["CO-25 p.8", "UX-53 pp.8,12,13,17,19", "AL-43 pp.14,29"], ["G-MANIFIESTO"])
R("R-MED-07", "medicion", "Los resultados se analizan por mercado y subgrupo fijados de antemano, se miden también efectos adversos (cancelaciones, quejas, no-shows) y todo hallazgo se replica en otro lote antes de promoverlo a regla.",
  None, "proceso", "ambos", "E1", ["CO-24 pp.5,8,9", "CO-23 pp.2,9", "UX-47 pp.10,15"], ["G-MANIFIESTO"])


def validar():
    errores = []
    ids = set()
    for r in REGLAS:
        if r["id"] in ids:
            errores.append(f"id repetido: {r['id']}")
        ids.add(r["id"])
        if not re.match(r"^R-[A-Z]{3}-\d{2}$", r["id"]):
            errores.append(f"id con formato raro: {r['id']}")
        if r["prioridad"] is not None and r["prioridad"] not in PRIORIDADES:
            errores.append(f"prioridad invalida en {r['id']}")
        if r["tipo"] not in ("bloqueo", "defecto", "hipotesis", "prohibido", "proceso"):
            errores.append(f"tipo inválido en {r['id']}")
        if r["publico"] not in ("A", "B", "ambos"):
            errores.append(f"publico inválido en {r['id']}")
        if r["evidencia"] not in ("N", "M", "E1", "E2", "E3", "E4"):
            errores.append(f"evidencia invalida en {r['id']}")
        if not r["fuentes"] or not r["gate"]:
            errores.append(f"faltan fuentes o gate en {r['id']}")
        texto = json.dumps(r, ensure_ascii=False)
        for ch in PROHIBIDOS:
            if ch in texto:
                errores.append(f"comilla angular en {r['id']}")
    return errores


def main():
    errores = validar()
    if errores:
        print("\n".join(errores))
        sys.exit(1)
    por_tema = {}
    for r in REGLAS:
        por_tema[r["tema"]] = por_tema.get(r["tema"], 0) + 1
    salida = {
        "version": "0.1.0",
        "descripcion": "Núcleo de conocimiento unificado de Edumashow. Reglas con prioridad, fuente, evidencia y prueba.",
        "prioridades": {str(k): v for k, v in PRIORIDADES.items()},
        "resolucion_de_choques": "Gana la regla de menor número de prioridad. A igual prioridad, el bloqueo gana al defecto y el defecto a la hipótesis. Una regla de prioridad mayor nunca se cumple a costa de una de prioridad menor.",
        "estudios_de_origen": {
            "AL": "Estudio motor predictivo para propuestas y alianzas con creadores (55 pp.)",
            "PS": "Estudio de psicología humana histórica y actual (9 pp.)",
            "UX": "Estudio motor predictivo de UX para propuestas (40 pp.)",
            "CO": "Estudio de ciencias del comportamiento y de la conducta (11 pp.)",
            "GR": "Informe motor gráfico para propuestas comerciales (33 pp.)",
        },
        "aviso": "Ninguno de los estudios trata de webs de restaurante: las reglas web son traducciones, y los umbrales numéricos de legibilidad, táctil y rendimiento son criterios propios o normas externas (WCAG 2.2, Core Web Vitals) o medidas de este proyecto.",
        "reglas": REGLAS,
    }
    destino = os.path.join(AQUI, "reglas.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"{len(REGLAS)} reglas escritas en reglas.json | por tema: {por_tema}")


if __name__ == "__main__":
    main()
