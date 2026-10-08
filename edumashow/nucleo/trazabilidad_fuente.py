"""Trazabilidad de los estudios: dónde se aplica cada regla y cada control del informe del motor gráfico.

Ejecutar este archivo escribe TRAZABILIDAD.md y lo valida:
  - cada una de las reglas de reglas.json tiene su fila
  - cada archivo citado existe y contiene el símbolo citado (función, clase, selector o identificador)
Así el documento no puede quedarse viejo sin que alguien se entere.

Estados
  Aplicada       está en el código o en el diseño y el Gate la comprueba
  Sin prueba     está aplicada, pero solo por construcción o revisión humana: el Gate no la mide
  Parcial        está hecha en parte; la nota dice que falta
  No aplica      no corresponde a este tipo de entrega (por ejemplo, controles propios de un PDF)
  Pendiente      todavía no está hecha
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, ".."))

# ---------------------------------------------------------------------------------------------
# Reglas unificadas (reglas.json): id -> (estado, [(archivo, símbolo)], nota)
# ---------------------------------------------------------------------------------------------
MOT = "motor/"
GAT = "gate/"
PLA = "motor/plantillas/"

REGLAS = {
    "R-DAT-01": ("Aplicada", [(MOT + "generar.py", "validar_ficha"), (GAT + "estatico.py", "PLACEHOLDERS"), (GAT + "estatico.py", "def datos")],
                 "Todo el texto sale de la ficha; si falta un dato el motor se abstiene. El Gate busca marcadores de relleno y compara con la ficha."),
    "R-DAT-02": ("Aplicada", [(MOT + "generar.py", "validar_ficha"), (GAT + "estatico.py", "patron_cero")],
                 "Un dato ausente no se rellena. El Gate busca ceros, gratis y similares que la ficha no tenga."),
    "R-DAT-03": ("Aplicada", [(MOT + "dinero.py", "def formato_importe"), (MOT + "dinero.py", "def importe_fn"), (GAT + "estatico.py", "def datos"), (GAT + "verificar.py", "G-FORMULARIO")],
                 "Un solo formato de moneda por país y por página (si algún precio lleva centavos, todos llevan dos decimales); cada importe de la página, sea de un plato, de una variante (media libra, una libra) o de un suplemento, y cada importe del mensaje de WhatsApp se compara con la ficha."),
    "R-DAT-04": ("Aplicada", [(MOT + "imagenes.py", "class Activos"), (MOT + "generar.py", "LICENCIAS.txt"), (GAT + "estatico.py", "def fotos")],
                 "Cada imagen lleva su procedencia, su permiso y el hash del archivo original en el manifiesto, y las tipografías en LICENCIAS.txt. Las fotos de referencia obligan a declararlo en la página."),
    "R-DAT-05": ("Parcial", [(GAT + "estatico.py", "ETICA")],
                 "El Gate bloquea premios, estrellas y porcentajes inventados, pero no hay un registro de afirmaciones con fuente y fecha por frase."),
    "R-DAT-06": ("Parcial", [(MOT + "generar.py", "confirmacion")],
                 "La ficha guarda estado y fecha de confirmación y el manifiesto la copia; revalidar los datos antes de cada entrega es un paso humano."),
    "R-DAT-07": ("Sin prueba", [(MOT + "piezas.py", "def e_"), (MOT + "generar.py", "replace(\"</\"")],
                 "Todo texto de la ficha se escapa y el JSON incrustado cierra las etiquetas. Falta el caso de prueba con texto malicioso (ver R-PRO-04)."),
    "R-DAT-08": ("Aplicada", [(MOT + "generar.py", "class FichaIncompleta"), (MOT + "generar.py", "def validar_ficha")],
                 "Si falta carta, horario, contacto o un precio, el motor se abstiene y dice que falta."),
    "R-DAT-09": ("Parcial", [(MOT + "generar.py", "confirmacion")],
                 "La identidad (nombre, dirección, contacto) la declara la ficha; el Gate no puede comprobar en el mundo real que sean del mismo local."),
    "R-ETI-01": ("Aplicada", [(GAT + "estatico.py", "escasez o urgencia")], "Patrones de escasez y urgencia inventadas bloquean la entrega."),
    "R-ETI-02": ("Aplicada", [(GAT + "estatico.py", "testimonios"), (MOT + "piezas.py", "def cinta")], "Sin testimonios ni estrellas; lo ficticio se rotula como ejemplo en la cinta."),
    "R-ETI-03": ("Aplicada", [(GAT + "estatico.py", "promesa de resultados")], "Sin promesas de ventas ni porcentajes con falsa precisión."),
    "R-ETI-04": ("Aplicada", [(GAT + "dinamico.mjs", "dialogosAbiertos"), (GAT + "verificar.py", "G-ETICA-VISTA")], "Al cargar no hay ventanas abiertas ni casillas premarcadas, en los 27 dispositivos."),
    "R-ETI-05": ("Aplicada", [(GAT + "estatico.py", "refuerzo variable")], "Sin ruletas ni premios sorpresa."),
    "R-ETI-06": ("Sin prueba", [(MOT + "temas.py", "PALETAS")], "Ningún código infiere perfiles de personas: el estilo lo elige la ficha a partir de datos del restaurante."),
    "R-ETI-07": ("Aplicada", [(MOT + "piezas.py", "def pie"), (MOT + "piezas.py", "def panel_edu"), (GAT + "estatico.py", "def muestra")],
                 "La muestra trae un enlace visible para pedir su retirada y el Gate lo exige. Que nunca se envie sola a un restaurante es una regla de proceso: la aprueba una persona."),
    "R-ETI-08": ("Aplicada", [(GAT + "estatico.py", "def red_estatica"), (MOT + "generar.py", "Content-Security-Policy"), (GAT + "verificar.py", "G-RED")],
                 "Sin cookies, sin scripts ni recursos de terceros; la cabecera de seguridad lo impone y el Gate lo mide en 27 dispositivos."),
    "R-ETI-09": ("Aplicada", [(GAT + "verificar.py", "Lo que este Gate no verifica")], "El informe dice que solo se probó Chromium emulado y que no hay pruebas con personas."),
    "R-ETI-10": ("No aplica", [], "Regla del modo final (alérgenos y dietas). Las muestras no los muestran. Queda pendiente su comprobación cuando haya una web final con alérgenos."),
    "R-ETI-11": ("Aplicada", [(GAT + "estatico.py", "def marca")], "Ninguna mención a herramientas de IA ni a Peetfoodie en lo que se entrega."),
    "R-ETI-12": ("Aplicada", [(GAT + "estatico.py", "def comillas"), ("../scripts/revisar_comillas.py", "PROHIBIDOS"), ("../CLAUDE.md", "Comillas")], "Cero comillas angulares en todo el repositorio y en cada paquete."),
    "R-FOT-01": ("Aplicada", [(MOT + "calidad.py", "def revisar_procedencia"), (GAT + "estatico.py", "def fotos"), ("../CLAUDE.md", "Fotos")],
                 "Ninguna foto de redes sociales salvo el logo: lo comprueba el validador de fichas antes de construir y el Gate sobre el manifiesto. Las de referencia o generadas solo valen en un ejemplo ficticio."),
    "R-FOT-02": ("Aplicada", [(MOT + "calidad.py", "MINIMOS"), (GAT + "estatico.py", "def fotos_calidad"), (GAT + "verificar.py", "G-FOTOS-CALIDAD")],
                 "El Gate mide el original (lado largo, calidad JPEG, detalle fino) y lo compara con su SHA-256; sin excepciones. Con la opción de prueba el resultado queda marcado como no entregable."),
    "R-VAL-01": ("Aplicada", [(MOT + "valoracion.py", "def validar"), (MOT + "valoracion.py", "def pieza"), (GAT + "estatico.py", "def valoracion"), (GAT + "verificar.py", "G-VALORACION")],
                 "La nota de Google solo sale de la ficha, con 4,0 o más, fecha de consulta y enlace; el Gate compara la pastilla de la portada y de la visita con la ficha."),
    "R-VAL-02": ("Aplicada", [(MOT + "valoracion.py", "ningun comentario"), (GAT + "estatico.py", "blockquote")],
                 "La ficha no admite campos de comentarios y el Gate bloquea bloques de reseñas y datos estructurados de reseñas."),
    "R-IDE-08": ("Aplicada", [(MOT + "catalogo.py", "PAQUETES"), (PLA + "a/particulas.js", "EDU.modulo"), (PLA + "base.js", "EDU.correrAnim"), (GAT + "verificar.py", "G-ANIMACION")],
                 "Seis paquetes de animaciones (brasa, bruma, editorial, minimal, cartel, festivo) hechos de módulos; la web declara el suyo en el manifiesto y el Gate comprueba en el navegador que cada módulo arrancó (mínimo tres). Todo respeta el movimiento reducido y la pausa."),
    "R-VAR-04": ("Aplicada", [(MOT + "catalogo.py", "def componer"), (MOT + "catalogo.py", "OPCIONES"), (MOT + "estilo.py", "def decidir"), (MOT + "ornamentos.py", "def intercalar"), (GAT + "verificar.py", "G-HUELLA")],
                 "El director elige cada dimensión de composición según los rasgos del restaurante y la rotación, prueba cientos de combinaciones y se queda con la de mayor encaje que cumple la distancia con las últimas webs. Cada elección y su motivo van al manifiesto y al informe."),
    "R-LEG-01": ("Aplicada", [(MOT + "temas.py", "PALETAS"), (GAT + "dinamico.mjs", "muestrearContraste"), (GAT + "verificar.py", "G-CONTRASTE")],
                 "El contraste se mide sobre los píxeles reales (texto oculto, captura, relación por pixel), no sobre colores nominales."),
    "R-LEG-02": ("Aplicada", [(PLA + "base.css", ".btn{"), (GAT + "verificar.py", "G-TACTIL44")], "Botones de 3,25 rem y controles de al menos 44 px en móvil."),
    "R-LEG-03": ("Aplicada", [(PLA + "base.css", "@container"), (PLA + "elegante.css", "minmax(0,1fr)"), (GAT + "verificar.py", "G-DESBORDE")],
                 "Reorganiza sin desbordar desde 280 px y con el texto al 200 por ciento; medido en 27 dispositivos."),
    "R-LEG-04": ("Aplicada", [(MOT + "tipografia.py", "def glifos_faltantes"), (GAT + "estatico.py", "def fuentes_glifos")], "Texto real y todos los glifos presentes; si falta uno, no se genera."),
    "R-LEG-05": ("Aplicada", [(MOT + "generar.py", "lang="), (MOT + "generar.py", "salto"), (PLA + "base.css", ":focus-visible"), (GAT + "verificar.py", "G-AXE")],
                 "Idioma, un h1, regiones, enlace de salto, foco visible y teclado; axe y recorrido con Tab lo comprueban."),
    "R-LEG-06": ("Aplicada", [(PLA + "base.js", "data-pausa"), (PLA + "base.css", "prefers-reduced-motion"), (GAT + "verificar.py", "G-MOVIMIENTO")], "Control de pausa visible y movimiento reducido respetado."),
    "R-LEG-07": ("Aplicada", [(GAT + "verificar.py", "G-TEXTO")], "Texto mínimo medido en pantalla: 14 px."),
    "R-LEG-08": ("Parcial", [(GAT + "verificar.py", "G-AXE")], "La estética no tapa los fallos de uso: axe y las pruebas funcionales corren siempre. La regla en si es un criterio de proceso."),
    "R-LEG-09": ("Aplicada", [(PLA + "elegante.css", ".fila"), (GAT + "dinamico.mjs", "solapes")], "Plato, descripción y precio comparten contenedor; el Gate detecta solapes y recortes."),
    "R-SIG-01": ("Aplicada", [(MOT + "piezas.py", "def portada"), (PLA + "elegante.css", "100svh"), (GAT + "verificar.py", "G-PRIMERA")], "Nombre y acción principal completos en la primera pantalla de los 27 dispositivos, incluidos horizontales."),
    "R-SIG-02": ("Aplicada", [(MOT + "piezas.py", "def barra_movil"), (PLA + "base.js", "IntersectionObserver"), (GAT + "verificar.py", "G-SIGUIENTE")], "Barra fija en móvil y menú en escritorio."),
    "R-SIG-03": ("Aplicada", [(MOT + "piezas.py", "def wa_url"), (MOT + "piezas.py", "def mapa_url"), (GAT + "verificar.py", "wa.me")], "WhatsApp con mensaje prellenado y mapa directo; el Gate valida el formato de cada enlace."),
    "R-SIG-04": ("Aplicada", [(MOT + "piezas.py", "def reserva"), (PLA + "elegante.js", "form-reserva"), (GAT + "verificar.py", "G-FORMULARIO")], "Cinco campos, valores por defecto (2 personas, hora cercana a las 20:00) y resumen antes de enviar."),
    "R-SIG-05": ("Sin prueba", [(MOT + "piezas.py", "Reservar mesa")], "Los botones dicen lo que hacen. El Gate valida los enlaces pero no lee las etiquetas."),
    "R-SIG-06": ("Parcial", [(MOT + "piezas.py", "def _plato"), (GAT + "estatico.py", "def datos")], "El precio va junto al nombre y se compara con la ficha; las condiciones de reserva o pedido no existen aun como datos."),
    "R-SIG-07": ("Sin prueba", [(PLA + "base.css", ".btn.suave")], "Un control primario y los demás subordinados; el Gate solo comprueba que el primario se vea."),
    "R-SIG-08": ("Aplicada", [(GAT + "verificar.py", "enlace # sin destino")], "Ningún enlace falso; Lighthouse además encontro uno sin destino y se corrigio."),
    "R-SIG-09": ("Parcial", [(MOT + "piezas.py", "def carta")], "La carta está a un toque y abierta por defecto, pero en Lumbre va después de la sección de historia."),
    "R-SIG-10": ("Parcial", [(MOT + "piezas.py", "def panel_edu")], "La muestra aclara a quién llega el mensaje. Que el restaurante conteste es algo que ningún Gate puede medir."),
    "R-SIG-11": ("Parcial", [(GAT + "estatico.py", "ETICA")], "Titulares literales; el Gate no detecta vacíos de curiosidad."),
    "R-SIG-12": ("Aplicada", [(GAT + "verificar.py", "G-ESTRUCTURA")], "Cada sección tiene un encabezado que dice su función (25 encabezados en Lumbre)."),
    "R-REN-01": ("Aplicada", [(GAT + "rendimiento.mjs", "lighthouse"), (GAT + "verificar.py", "G-REND"), ("config.json", "lcp_ms")], "Lighthouse en móvil lento simulado y peso real descargado contra el presupuesto."),
    "R-REN-02": ("Aplicada", [(MOT + "imagenes.py", "def picture_html"), (GAT + "verificar.py", "G-RESOLUCION")], "AVIF y WebP con srcset, JPEG de respaldo, tamaño declarado, miniatura borrosa y portada con prioridad."),
    "R-REN-03": ("Aplicada", [(MOT + "tipografia.py", "def subconjunto_woff2"), (GAT + "estatico.py", "def fuentes_glifos")], "Subconjuntos WOFF2 propios con font-display swap."),
    "R-REN-04": ("Sin prueba", [(PLA + "base.js", "ResizeObserver")], "JavaScript propio de unos 17 KB minificado. El tope de 30 KB lo imprime el generador pero el Gate no lo exige."),
    "R-REN-05": ("Aplicada", [(MOT + "generar.py", "_headers"), (GAT + "verificar.py", "G-RED")], "Un solo origen, cabeceras de caché inmutable y cero peticiones externas."),
    "R-IDE-01": ("Aplicada", [(MOT + "estilo.py", "def decidir"), (MOT + "estilo.py", "TONOS_COCINA"), (MOT + "huella.py", "def huella")],
                 "El director de estilo deduce paleta (del logo), tipografía (del carácter de la cocina) y orden de fotos (por antojo) de los datos de la ficha, y deja escrita la razón de cada decisión en el manifiesto y en el informe del Gate."),
    "R-IDE-02": ("Aplicada", [(MOT + "piezas.py", "def _plato"), (PLA + "elegante.js", "role=tab"), (MOT + "piezas_urbano.py", "def _item"), (PLA + "urbano.js", "chips")], "Precio junto al nombre, categorías de carta y botones de acción donde se esperan: pestañas en la personalidad elegante y barra de categorías pegada arriba, con la categoría actual marcada, en la urbana."),
    "R-IDE-03": ("Aplicada", [(MOT + "color.py", "def paleta_marca"), (MOT + "tipografia.py", "PAREJAS"), (GAT + "verificar.py", "G-CONTRASTE"), (GAT + "verificar.py", "G-PALETA")],
                 "Paleta y tipografía se eligen por contraste, marca y carácter, y se miden dos veces: los pares de colores sobre los tokens finales y el contraste real sobre los píxeles de la página."),
    "R-IDE-04": ("Parcial", [(MOT + "imagenes.py", "def procesar_logo"), (GAT + "verificar.py", "G-LOGO"), (MOT + "temas.py", "\"fuego\"")],
                 "El logo se usa íntegro: con su transparencia, sin recortar, recolorear ni deformar, y el Gate mide que cargue y que no cambie de proporción. La paleta fuego se tomó de los colores del logo; falta un campo de colores aprobados por el restaurante."),
    "R-IDE-05": ("Aplicada", [(MOT + "temas.py", "MOVIMIENTOS"), (PLA + "urbano.css", "mural"), (GAT + "verificar.py", "G-AVANCE"), (GAT + "verificar.py", "G-MOVIMIENTO")], "Movimiento lento para la personalidad elegante y rápido y grueso para la urbana (mural de fotos, brasas, titular que sube), las dos con pausa, sin efectos obligatorios y quietas con movimiento reducido."),
    "R-PER-01": ("No aplica", [], "Ninguna técnica de persuasión se activa por defecto: es la regla y se cumple por omisión."),
    "R-PER-02": ("No aplica", [], "No hay prueba social ni normas en las muestras."),
    "R-PER-03": ("No aplica", [], "No se usan anclajes ni encuadres como palanca."),
    "R-VAR-01": ("Aplicada", [(MOT + "huella.py", "def comparar"), (GAT + "verificar.py", "G-HUELLA")], "Huella de trece dimensiones con peso (familia, portada, carta, galería, paleta, tipografía, animaciones, ornamento, botones, densidad, textura, orden, forma y movimiento); el Gate exige 8 puntos de distancia con cada una de las últimas 12 webs y ninguna firma repetida en el registro."),
    "R-VAR-02": ("Parcial", [(MOT + "huella.py", "def huella"), (MOT + "piezas_urbano.py", "PERSONALIDAD"), (MOT + "estilo.py", "variante_paleta")],
                 "Hay dos personalidades materialmente distintas y el director propone la pareja tipográfica y el acento de temporada con alternativas, pero no asigna variantes al azar ni registra semillas: la misma ficha siempre da el mismo resultado."),
    "R-IDE-06": ("Aplicada", [(MOT + "color.py", "def paleta_marca"), (MOT + "color.py", "def colores_dominantes"), (MOT + "color.py", "def elegir_acento"), (GAT + "estatico.py", "def paleta"), (GAT + "verificar.py", "G-PALETA")],
                 "Color de identidad del logo (k-means en OKLab, sin neutros), acento de temporada con relación de tono y unidad, fondos teñidos hacia la marca y ajuste automático de luminosidad hasta cumplir cada par de contraste; el Gate recalcula los pares sobre los colores finales."),
    "R-IDE-07": ("Aplicada", [(MOT + "antojo.py", "CRITERIOS"), (MOT + "antojo.py", "def puntuar"), (MOT + "piezas_urbano.py", "def _galeria"), (GAT + "estatico.py", "def antojo"), (GAT + "verificar.py", "G-ANTOJO")],
                 "Siete criterios juzgados mirando cada foto (65 %) y cuatro medidas técnicas (35 %); el orden del mural y de la galería es el del ranking y el Gate comprueba que lo que se ve coincide con el ranking del manifiesto."),
    "R-VAR-03": ("Aplicada", [(MOT + "huella.py", "def rotacion"), (MOT + "tipografia.py", "CLASES"), (MOT + "estilo.py", "def elegir_tipografia"), (GAT + "verificar.py", "G-HUELLA")],
                 "Fuente y clase del titular quedan en la huella y en el registro con su secuencia; el director solo propone parejas que no repiten y el Gate bloquea una repetición."),
    "R-MUE-01": ("Aplicada", [(MOT + "piezas.py", "def cinta"), (MOT + "generar.py", "noindex"), (GAT + "estatico.py", "def muestra")], "Cinta, noindex, cabecera X-Robots-Tag y robots.txt; el Gate lo exige en toda muestra."),
    "R-MUE-02": ("Aplicada", [(MOT + "piezas.py", "def cierre_muestra"), (MOT + "piezas.py", "def panel_edu")], "Una sola acción de contratación: WhatsApp a Edumashow con mensaje prellenado."),
    "R-MUE-03": ("Aplicada", [(MOT + "piezas.py", "def cierre_muestra")], "El cierre habla en condicional y no menciona presupuesto ni margen."),
    "R-MUE-04": ("Aplicada", [(MOT + "generar.py", "og:title"), (GAT + "estatico.py", "def meta")], "Titulo, descripción y vista previa; la imagen social necesita el dominio final (aviso del Gate)."),
    "R-MUE-05": ("Parcial", [(GAT + "estatico.py", "def muestra")], "Para un negocio real la ficha debe declarar el permiso, de dónde salen los datos y el permiso de cada foto; la muestra lo dice en el pie, lleva cinta y noindex, y el Gate lo exige. Que se le enseñe primero al dueño es un paso humano."),
    "R-PRO-01": ("Aplicada", [(GAT + "verificar.py", "UNAVAILABLE")], "El Gate falla cerrado: sin navegador no hay veredicto. El generador no aprueba su propia salida."),
    "R-PRO-02": ("Aplicada", [(MOT + "generar.py", "def hash_paquete"), (GAT + "estatico.py", "def manifiesto")], "El permiso se liga al hash SHA-256 del paquete exacto; cualquier cambio lo invalida."),
    "R-PRO-03": ("Aplicada", [(GAT + "verificar.py", "class Informe")], "Cada comprobación tiene id, estado, gravedad, reglas, evidencia y detalle."),
    "R-PRO-04": ("Pendiente", [], "Falta el banco formal de casos válidos y defectuosos con el que el Gate se prueba a sí mismo."),
    "R-PRO-05": ("Aplicada", [(GAT + "verificar.py", "def hoja_contacto"), (GAT + "verificar.py", "G-VISUAL")], "Capturas reales de 27 dispositivos y revisión humana pendiente y visible."),
    "R-PRO-06": ("Aplicada", [(MOT + "generar.py", "manifiesto")], "El manifiesto trae versión, fecha, modo, país, ciudad, idioma, hash del paquete, id de ensamblado y huella de diseño."),
    "R-PRO-07": ("Aplicada", [(GAT + "verificar.py", "aprobacion_de_eduardo")], "El informe separa estado técnico, revisión visual, aprobación y entrega, y no promete ventas."),
    "R-MED-01": ("Pendiente", [], "Aun no hay experimentos con clientes: todo efecto de la literatura es una hipótesis."),
    "R-MED-02": ("Parcial", [], "La conducta objetivo existe como campo de la ficha (conducta), pero todavía no se mide."),
    "R-MED-03": ("Pendiente", [], "Se calcula el tamaño de muestra cuando haya un A/B que proponer."),
    "R-MED-04": ("Pendiente", [], "Pruebas de tarea con 5 a 8 personas: tu revisión es la primera de ellas."),
    "R-MED-05": ("Aplicada", [(GAT + "verificar.py", "G-RED")], "No hay ninguna medición: ni cookies ni analítica. Cuando se añada será agregada y sin identificadores."),
    "R-MED-06": ("Pendiente", [], "Ningún modelo estima efectos; las variantes e hipótesis las propone el motor sin predecir resultados."),
    "R-MED-07": ("Pendiente", [], "Análisis por mercado y subgrupo: cuando haya datos."),
}

# ---------------------------------------------------------------------------------------------
# Controles del informe del motor gráfico (Anexo A): id -> (nombre, estado, donde y nota)
# ---------------------------------------------------------------------------------------------
GRAFICO = {
    "I01": ("Identidad confirmada", "Aplicada", "validar_ficha y G-DATOS: sin marcadores pendientes ni datos heredados."),
    "I02": ("Contrato comercial tipado", "Aplicada", "dinero.py exige país y moneda conocidos; G-DATOS compara cada importe."),
    "I03": ("Visibilidad del encargo", "Parcial", "No hay un campo de visibilidad por dato; la muestra evita presupuesto y margen (R-MUE-03)."),
    "I04": ("Contacto verificado", "Aplicada", "El contacto sale de la ficha; G-SIGUIENTE valida el formato de wa.me, tel: y mapas, y que las redes sean solo las que declara la ficha."),
    "S01": ("Concepto específico", "Parcial", "La ficha declara sus acciones (reservar, llamar, mapa, redes) y la portada y la barra móvil las siguen; el motor aún no elige solo la acción a partir de la conducta."),
    "S02": ("Afirmaciones trazables", "Parcial", "Ver R-DAT-05."),
    "S03": ("Metricas originales", "No aplica", "La web no muestra metricas de audiencia."),
    "S04": ("Mercado documentado", "No aplica", "La web no atribuye audiencia geográfica."),
    "S05": ("Condiciones preservadas", "Aplicada", "Precios y horarios de la página son los de la ficha y el hash congela el paquete."),
    "A01": ("Procedencia del activo", "Aplicada", "Cada imagen lleva origen, licencia, permiso y el hash sha256 del archivo original en el manifiesto; los recortes de capturas dejan su caja y el hash de la captura en recortes.json."),
    "A02": ("Uso autorizado", "Parcial", "La ficha declara uso y permiso por foto; no hay perfil de fuentes admitidas por rol."),
    "A03": ("Original conservado", "Aplicada", "imagenes.py parte siempre del original y registra recortes y ajustes; no se inventa detalle."),
    "A04": ("Logo íntegro", "Aplicada", "procesar_logo no recorta ni recolorea y G-LOGO comprueba en cada dispositivo que carga, que su proporción en pantalla es la del archivo y que mide al menos 40 px."),
    "A05": ("Permiso documentado", "Parcial", "Campo de permiso por activo; la aprobación es un paso humano."),
    "A06": ("Evidencia protegida", "Parcial", "Punto de foco por imagen y recorte dirigido; sin prueba automática de que no se corte el sujeto."),
    "A07": ("Resolución efectiva", "Aplicada", "G-RESOLUCION mide cuanto se amplia cada foto en cada pantalla."),
    "A08": ("Variedad sin duplicados", "Aplicada", "Activos evita imágenes repetidas y G-HUELLA exige diseño distinto."),
    "T01": ("Fuente permitida", "Parcial", "Solo tipografías OFL del kit; no hay lista de vetos por marca."),
    "T02": ("Fuentes incorporadas", "Aplicada", "WOFF2 propias y G-RED comprueba que no se pide ninguna externa."),
    "T03": ("Glifos completos", "Aplicada", "glifos_faltantes impide generar y G-FUENTES lo repite sobre el paquete."),
    "T04": ("Sin deformación del cuerpo", "Sin prueba", "El CSS no escala el texto de forma anisotropa; no hay prueba automática."),
    "T05": ("Tinta sin recorte", "Aplicada", "G-DESBORDE detecta texto recortado por un contenedor."),
    "T06": ("Parrafos legibles", "Parcial", "Tamaño mínimo medido; interlineado y longitud de línea por CSS sin prueba."),
    "G01": ("Regiones respetadas", "Aplicada", "G-DESBORDE en 27 dispositivos y con texto al 200 por ciento."),
    "G02": ("Superposicion declarada", "Aplicada", "G-DESBORDE detecta solapes de texto y controles; las capas decorativas estan declaradas."),
    "G03": ("Zonas seguras", "Parcial", "Margenes y área segura inferior para la barra; sin prueba específica de muescas."),
    "G04": ("Precio alineado", "Parcial", "Espacio duro entre símbolo e importe y alineación de base; sin prueba de la línea base."),
    "G05": ("Separacion de líneas", "Sin prueba", "Separaciones por CSS; sin prueba automática."),
    "G06": ("Contraste suficiente", "Aplicada", "G-CONTRASTE sobre el fondo compuesto real."),
    "G07": ("Recorte de producto", "Parcial", "Foco por imagen; sin prueba automática del sujeto."),
    "G08": ("Color y transparencia", "Parcial", "El logo conserva su transparencia (AVIF y WebP con alfa y PNG de respaldo) y su borde se suavizó con máscara supermuestreada; no hay prueba automática de halos ni de perfil de color."),
    "V01": ("Todas las páginas revisadas", "Parcial", "Capturas de 27 dispositivos en una hoja; la revisión humana (la tuya) es el paso que falta para aprobar."),
    "V02": ("Nivel visual pertinente", "Parcial", "Comparación antes y después de Lumbre; sin referencias autorizadas más allá de ella."),
    "V03": ("Independencia creativa", "Aplicada", "La huella de diseño impide clonar una web cambiando solo la identidad."),
    "V04": ("Densidad con función", "No aplica", "Es un criterio de diseño que no se puede medir con un script."),
    "V05": ("Jerarquía móvil", "Aplicada", "G-PRIMERA: concepto y siguiente paso visibles en el primer tramo."),
    "V06": ("Detalle verificable", "Aplicada", "Pruebas con texto al 200 por ciento: nada se corta ni se solapa."),
    "P01": ("Apertura estructural (PDF)", "No aplica", "Es un control de PDF; el equivalente web es que el HTML se lea sin errores (el Gate lo analiza, no usa un validador externo)."),
    "P02": ("Contenido extraible (PDF)", "No aplica", "Equivalente web: todo el texto esencial es texto real."),
    "P03": ("Páginas e integridad (PDF)", "No aplica", "Equivalente web: manifiesto con todos los archivos y su hash."),
    "P04": ("Enlaces correctos (PDF)", "Parcial", "El formato de cada enlace se valida; que el destino siga vivo no se comprueba."),
    "P05": ("Compatibilidad contrastada (PDF)", "Parcial", "Solo Chromium emulando dispositivos; Safari y Firefox reales no estan probados."),
    "P06": ("Accesibilidad del perfil (PDF)", "Aplicada", "axe en tres tamaños y recorrido con teclado."),
    "D01": ("Paquete completo", "Aplicada", "Carpeta, zip, manifiesto y licencias."),
    "D02": ("Identidad del artefacto", "Aplicada", "El informe lleva el hash del paquete y el Gate lo recalcula."),
    "D03": ("Constancia auténtica", "Aplicada", "El informe lo escribe el Gate, no el generador."),
    "D04": ("Archivo almacenado", "Aplicada", "El paquete queda en el repositorio, en la rama de trabajo."),
    "D05": ("Lectura posterior", "Pendiente", "Hace falta un hosting para comprobar que lo publicado coincide con el hash."),
    "D06": ("Ruta de acceso valida", "Pendiente", "Idem: hasta que haya una URL pública no hay ruta que comprobar."),
    "D07": ("Sin cambio posterior", "Aplicada", "Cualquier cambio cambia el hash y obliga a pasar el Gate de nuevo."),
    "D08": ("Reintentos coherentes", "Parcial", "La generación es determinista por contenido; todavía no hay publicación que repetir."),
    "L01": ("Regresiones conservadas", "Parcial", "Cada defecto hallado se volvio una comprobación (desborde con texto grande, foco tapado, cifra que no avanza, enlace sin destino); falta el banco formal de casos."),
    "L02": ("Aprobaciones con autor", "Aplicada", "El informe separa técnico, revisión visual, aprobación de Eduardo y entrega."),
    "L03": ("Probabilidades justificadas", "Aplicada", "No se muestra ninguna probabilidad comercial."),
}

ORDEN_ESTADO = ["Aplicada", "Sin prueba", "Parcial", "Pendiente", "No aplica"]


def _existe(archivo, simbolo):
    ruta = os.path.normpath(os.path.join(RAIZ, archivo))
    if not os.path.exists(ruta):
        return f"no existe {archivo}"
    with open(ruta, encoding="utf-8") as f:
        if simbolo not in f.read():
            return f"{archivo} no contiene {simbolo!r}"
    return None


def validar(reglas_json):
    errores = []
    ids = {r["id"] for r in reglas_json}
    for i in ids - set(REGLAS):
        errores.append(f"falta la fila de {i}")
    for i in set(REGLAS) - ids:
        errores.append(f"{i} no esta en reglas.json")
    for i, (estado, donde, _nota) in REGLAS.items():
        if estado not in ORDEN_ESTADO:
            errores.append(f"{i}: estado desconocido {estado}")
        if estado in ("Aplicada", "Sin prueba") and not donde:
            errores.append(f"{i}: dice {estado} pero no cita donde")
        for archivo, simbolo in donde:
            e = _existe(archivo, simbolo)
            if e:
                errores.append(f"{i}: {e}")
    for i, (_n, estado, _nota) in GRAFICO.items():
        if estado not in ORDEN_ESTADO:
            errores.append(f"{i}: estado desconocido {estado}")
    return errores


def escribir(reglas_json, salida):
    por_id = {r["id"]: r for r in reglas_json}
    cuenta = {e: 0 for e in ORDEN_ESTADO}
    for e, _, _ in REGLAS.values():
        cuenta[e] += 1
    cuenta_g = {e: 0 for e in ORDEN_ESTADO}
    for _, e, _ in GRAFICO.values():
        cuenta_g[e] += 1
    L = []
    L.append("# Trazabilidad: dónde se aplican los estudios\n")
    L.append("Este documento lo genera `edumashow/nucleo/trazabilidad_fuente.py`, que además comprueba que cada archivo y cada función citados existen. Dice también lo que todavía no está hecho.\n")
    L.append("Estados: **Aplicada** (está en el código o el diseño y el Gate la comprueba), **Sin prueba** (aplicada, pero el Gate no la mide), **Parcial**, **Pendiente** y **No aplica**.\n")
    L.append("## Resumen\n")
    L.append(f"| Estado | Reglas unificadas ({len(REGLAS)}) | Controles del informe del motor gráfico (54) |\n|---|---|---|")
    for e in ORDEN_ESTADO:
        L.append(f"| {e} | {cuenta[e]} | {cuenta_g[e]} |")
    L.append("")
    L.append(f"Los cuatro estudios de conocimiento (alianzas, psicología, UX predictivo y conducta) y el informe del motor gráfico se unificaron, junto con el método de paleta, tipografía y fotos del Documento Maestro del kit, en {len(REGLAS)} reglas con prioridad, fuente, evidencia y prueba (`reglas.json`). Cada regla lleva un número de orden de importancia, como un podio: el 0 es lo más importante (verdad, legalidad y ética) y el 6 lo menos (variedad entre webs). Cuando dos reglas chocan gana la que tiene el número más bajo, porque número bajo quiere decir más importante. Ninguno de los cinco trata de webs de restaurante: las reglas web son traducciones y están marcadas como tales.\n")
    L.append(f"## Las {len(REGLAS)} reglas unificadas\n")
    L.append("| Regla | Estado | Fuente en los estudios | Dónde se aplica | Prueba del Gate | Nota |\n|---|---|---|---|---|---|")
    for rid in sorted(REGLAS, key=lambda x: (x.split("-")[1], x)):
        estado, donde, nota = REGLAS[rid]
        r = por_id[rid]
        fuentes = "; ".join(r["fuentes"][:4])
        sitios = "<br>".join(f"`{a}`: {s}" for a, s in donde) or "-"
        gate = ", ".join(r["gate"]) or "-"
        L.append(f"| {rid} | {estado} | {fuentes} | {sitios} | {gate} | {nota} |")
    L.append("")
    L.append("## Los 54 controles del informe del motor grafico\n")
    L.append("El informe esta pensado para propuestas en PDF. Aquí se traducen a la web los controles que tienen equivalente y se marcan como no aplicables los que son propios del PDF.\n")
    L.append("| Control | Nombre | Estado | Dónde y por qué |\n|---|---|---|---|")
    for cid, (nombre, estado, nota) in GRAFICO.items():
        L.append(f"| {cid} | {nombre} | {estado} | {nota} |")
    L.append("")
    with open(salida, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    return cuenta, cuenta_g


if __name__ == "__main__":
    with open(os.path.join(AQUI, "reglas.json"), encoding="utf-8") as f:
        datos = json.load(f)["reglas"]
    errores = validar(datos)
    if errores:
        print("TRAZABILIDAD CON ERRORES:")
        for e in errores:
            print(" -", e)
        sys.exit(1)
    cuenta, cuenta_g = escribir(datos, os.path.join(AQUI, "TRAZABILIDAD.md"))
    print("TRAZABILIDAD.md escrito | reglas:", cuenta, "| controles del motor gráfico:", cuenta_g)
