"""Catálogo de composiciones: lo que hace que dos webs de Edumashow no sean la misma web con otros colores (R-VAR-01 y R-VAR-04).

Una web es la combinación de una familia (la personalidad: elegante o urbano) y de una opción en cada dimensión de composición:
portada, carta, galería, ornamento (el borde entre secciones), botones, densidad, textura y paquete de animaciones. A eso se suman
la paleta (sale del logo), la tipografía de titular (rotación) y el orden de las secciones.

El director elige cada opción según los datos reales del restaurante (cocina, nivel de precio, ambiente, servicio, fotos y logo), con
rotación frente a las webs ya hechas, y deja escrito el motivo. Una ficha puede fijar a mano cualquier dimensión: lo fijado manda y solo se valida.

Añadir una opción nueva es añadir su nombre aquí, su afinidad, y su marcado o su CSS en plantillas; el esquema, el kit del proyecto y el Gate
se actualizan solos porque leen este módulo.
"""
import hashlib
import math
import random
import re

from . import huella as _huella

FAMILIAS = ("elegante", "urbano")

# ------------------------------------------------------------------ opciones por dimensión (la primera de cada familia es la clásica de siempre)
OPCIONES = {
    "portada": {"elegante": ["luz_brasas", "marco_editorial", "cortina"], "urbano": ["mural_columnas", "collage_pegatinas", "cartel_rotulo"]},
    "carta": {"elegante": ["pestanas_lista", "indice_columnas"], "urbano": ["chips_tablero", "lista_cartel"]},
    "galeria": {"elegante": ["mosaico", "cinta", "polaroid", "bento"], "urbano": ["cuadricula_ig", "cinta", "polaroid", "bento"]},
    "ornamento": {"elegante": ["recto", "onda", "diente", "arco", "rasgado"], "urbano": ["recto", "onda", "diente", "arco", "rasgado"]},
    "boton": {"elegante": ["solido", "contorno", "subrayado", "sello"], "urbano": ["solido", "contorno", "subrayado", "sello"]},
    "densidad": {"elegante": ["media", "aire", "compacta"], "urbano": ["media", "aire", "compacta"]},
    "textura": {"elegante": ["grano", "papel", "rayas", "limpia"], "urbano": ["grano", "papel", "rayas", "limpia"]},
    "animaciones": {"elegante": ["brasa", "bruma", "editorial", "minimal"], "urbano": ["cartel", "festivo", "bruma", "editorial"]},
}
DIMENSIONES = tuple(OPCIONES)          # el orden en que se eligen
CLASICAS = {f: {d: OPCIONES[d][f][0] for d in OPCIONES} for f in FAMILIAS}
FORMAS = ("recta", "suave")

# opciones del catálogo que aún no tienen su marcado o su CSS: el director no las elige (se quitan de aquí al implementarlas)
PENDIENTES = set()
# Pares de opciones que el Gate no deja pasar juntas todavía (cada par: ((dimension, opcion), (dimension, opcion))). El director no los combina; una ficha que fije
# a mano los dos sí puede. Se llena con lo que muestra `scripts/cobertura_catalogo.py` y se vacía al arreglar la causa.
PARES_NO_VIABLES = set()

# ------------------------------------------------------------------ paquetes de animaciones
# Cada paquete es un conjunto de módulos (plantillas/anim) y un estilo de revelado; el Gate comprueba en el navegador que cada módulo arrancó.
PAQUETES = {
    "brasa": {"modulos": ["revelado", "particulas", "luz", "paralaje", "magnetico"], "particulas": "brasas", "revelado": "fade", "movimiento": "lento",
              "descripcion": "brasas que suben, luz que sigue al puntero, paralaje suave y botones magnéticos"},
    "bruma": {"modulos": ["revelado", "particulas", "paralaje", "subrayado", "progreso"], "particulas": "vapor", "revelado": "desenfoque", "movimiento": "lento",
              "descripcion": "vapor que se disuelve, revelado con desenfoque, subrayados dibujados y barra de avance"},
    "editorial": {"modulos": ["revelado", "particulas", "texto_corre", "subrayado", "magnetico", "progreso"], "particulas": "polvo", "revelado": "mascara", "movimiento": "lento",
                  "descripcion": "motas de luz, titulares que se descubren con máscara, texto grande que corre con el scroll y subrayados dibujados"},
    "minimal": {"modulos": ["revelado", "luz", "subrayado", "progreso"], "particulas": None, "revelado": "mascara", "movimiento": "lento",
                "descripcion": "luz que sigue al puntero, revelado con máscara y subrayados dibujados; sin partículas"},
    "cartel": {"modulos": ["revelado", "particulas", "inclinacion", "marquesina", "magnetico"], "particulas": "chispas", "revelado": "escalera", "movimiento": "rapido",
               "descripcion": "chispas, marquesina, tarjetas que se inclinan y entradas escalonadas"},
    "festivo": {"modulos": ["revelado", "particulas", "inclinacion", "marquesina", "magnetico"], "particulas": "burbujas", "revelado": "escalera", "movimiento": "rapido",
                "descripcion": "burbujas, marquesina, tarjetas que se inclinan y botones magnéticos"},
}

# qué es cada opción, en una frase (el kit del proyecto y el informe del Gate las usan)
DESCRIPCIONES = {
    ("portada", "luz_brasas"): "foto de portada a pantalla completa, luz de brasa que sigue al puntero y titular que entra letra a letra",
    ("portada", "marco_editorial"): "portada de papel claro, titular por palabras y la foto en un arco con un sello giratorio",
    ("portada", "cortina"): "foto a pantalla completa con marco fino, titular centrado y una cortina que se abre",
    ("portada", "mural_columnas"): "mural de fotos en columnas que suben y bajan y titular de cartel",
    ("portada", "collage_pegatinas"): "fotos como polaroids pegadas con cinta que caen sobre un fondo de puntos",
    ("portada", "cartel_rotulo"): "cartel del color de la marca con titular enorme, disco con foto y una cinta que corre",
    ("carta", "pestanas_lista"): "pestañas por categoría y lista con puntos guía y fotos pequeñas",
    ("carta", "indice_columnas"): "todas las categorías seguidas, con un índice que marca dónde se está leyendo",
    ("carta", "chips_tablero"): "filtros por categoría y tarjetas con precios grandes y botón de agregar",
    ("carta", "lista_cartel"): "menú como cartel de precios, en renglones y sin tarjetas",
    ("galeria", "mosaico"): "mosaico de fotos de distinto tamaño con parallax suave",
    ("galeria", "cuadricula_ig"): "cuadrícula de fotos ligeramente torcidas con pie en mayúsculas",
    ("galeria", "cinta"): "tira horizontal de fotos grandes numeradas, con el pie debajo",
    ("galeria", "polaroid"): "fotos con marco blanco, un poco torcidas, como pegadas en un tablero",
    ("galeria", "bento"): "mosaico de recuadros de distinto tamaño que encajan entre sí (necesita 5 fotos o más)",
    ("ornamento", "recto"): "secciones con borde recto",
    ("ornamento", "onda"): "borde en onda entre secciones",
    ("ornamento", "diente"): "borde en diente de sierra",
    ("ornamento", "arco"): "borde en arco amplio",
    ("ornamento", "rasgado"): "borde de papel rasgado, distinto en cada web",
    ("boton", "solido"): "botón relleno con el color de la marca",
    ("boton", "contorno"): "botón de contorno que se rellena al pasar el puntero",
    ("boton", "subrayado"): "botón de texto subrayado con una flecha",
    ("boton", "sello"): "botón con borde grueso y sombra dura que se hunde al pulsar",
    ("densidad", "media"): "espaciado habitual",
    ("densidad", "aire"): "secciones muy espaciadas",
    ("densidad", "compacta"): "secciones juntas, más contenido por pantalla",
    ("textura", "grano"): "grano de película en la portada",
    ("textura", "papel"): "fibras de papel en las secciones claras",
    ("textura", "rayas"): "diagonales finas en las secciones oscuras",
    ("textura", "limpia"): "sin textura",
}
for _p, _d in PAQUETES.items():
    DESCRIPCIONES[("animaciones", _p)] = _d["descripcion"]

# ------------------------------------------------------------------ afinidades: qué rasgos del restaurante piden cada opción
A = {
    ("portada", "luz_brasas"): ["brasa", "parrilla", "calido", "romantico", "nocturno", "autor", "premium", "lujo", "elegante"],
    ("portada", "marco_editorial"): ["moderno", "minimal", "luminoso", "fresco", "tradicion", "artesanal", "saludable", "calmado", "cafe", "panaderia", "dulce"],
    ("portada", "cortina"): ["lujo", "premium", "romantico", "nocturno", "autor", "elegante", "minimal", "marino"],
    ("portada", "mural_columnas"): ["parrilla", "callejero", "potente", "urbano", "rapido", "llevar", "brasa"],
    ("portada", "collage_pegatinas"): ["joven", "pop", "festivo", "fresco", "familiar", "dulce", "amable", "social"],
    ("portada", "cartel_rotulo"): ["potente", "callejero", "impacto", "economico", "rapido", "cartel", "urbano"],
    ("carta", "pestanas_lista"): ["elegante", "premium", "autor", "calmado", "lujo", "romantico"],
    ("carta", "indice_columnas"): ["tradicion", "moderno", "trattoria", "calido", "artesanal", "familiar", "marino"],
    ("carta", "chips_tablero"): ["urbano", "callejero", "joven", "rapido", "pop", "llevar"],
    ("carta", "lista_cartel"): ["tradicion", "economico", "cartel", "familiar", "potente", "parrilla"],
    ("galeria", "mosaico"): ["elegante", "premium", "autor", "calmado", "lujo"],
    ("galeria", "cuadricula_ig"): ["urbano", "callejero", "joven", "pop", "social"],
    ("galeria", "cinta"): ["moderno", "minimal", "marino", "luminoso", "autor", "cafe"],
    ("galeria", "polaroid"): ["familiar", "artesanal", "tradicion", "amable", "dulce", "romantico", "festivo"],
    ("galeria", "bento"): ["moderno", "pop", "joven", "social", "potente"],
    ("ornamento", "recto"): ["moderno", "minimal", "lujo", "premium", "autor"],
    ("ornamento", "onda"): ["fresco", "marino", "playero", "luminoso", "amable", "saludable", "cafe"],
    ("ornamento", "diente"): ["pop", "callejero", "festivo", "joven", "potente"],
    ("ornamento", "arco"): ["tradicion", "calido", "romantico", "familiar", "trattoria", "panaderia"],
    ("ornamento", "rasgado"): ["artesanal", "rustico", "tradicion", "callejero", "parrilla", "familiar"],
    ("boton", "solido"): ["potente", "callejero", "familiar", "economico", "urbano"],
    ("boton", "contorno"): ["elegante", "premium", "minimal", "moderno", "lujo", "autor"],
    ("boton", "subrayado"): ["minimal", "calmado", "autor", "cafe", "moderno", "luminoso"],
    ("boton", "sello"): ["pop", "joven", "festivo", "callejero", "dulce", "social"],
    ("densidad", "media"): [],
    ("densidad", "aire"): ["lujo", "premium", "minimal", "calmado", "autor", "elegante"],
    ("densidad", "compacta"): ["economico", "rapido", "callejero", "potente", "llevar"],
    ("textura", "grano"): ["nocturno", "brasa", "parrilla", "calido", "potente"],
    ("textura", "papel"): ["tradicion", "artesanal", "panaderia", "familiar", "rustico", "cafe", "trattoria"],
    ("textura", "rayas"): ["pop", "joven", "festivo", "social", "urbano"],
    ("textura", "limpia"): ["minimal", "moderno", "luminoso", "saludable", "lujo"],
    ("animaciones", "brasa"): ["brasa", "parrilla", "calido", "nocturno", "romantico", "potente"],
    ("animaciones", "bruma"): ["fresco", "saludable", "marino", "calmado", "cafe", "luminoso", "amable"],
    ("animaciones", "editorial"): ["moderno", "minimal", "autor", "premium", "luminoso", "artesanal"],
    ("animaciones", "minimal"): ["calmado", "minimal", "lujo", "elegante", "autor"],
    ("animaciones", "cartel"): ["callejero", "urbano", "pop", "rapido", "potente", "parrilla", "economico"],
    ("animaciones", "festivo"): ["festivo", "joven", "dulce", "playero", "pop", "social", "familiar"],
}

# rasgos que dan los datos de perfil de la ficha (servicio, precio y ambiente) además de la cocina
RASGOS_SERVICIO = {"mesa": ["calmado"], "llevar": ["rapido", "callejero", "llevar"], "barra": ["social", "nocturno"], "reparto": ["rapido", "llevar"]}
RASGOS_PRECIO = {1: ["economico", "callejero"], 2: [], 3: ["autor", "elegante"], 4: ["lujo", "premium", "elegante"]}
RASGOS_AMBIENTE = {
    "familiar": ["familiar", "calido", "amable"], "romantico": ["romantico", "calido", "elegante"], "juvenil": ["joven", "pop", "social"],
    "nocturno": ["nocturno", "social"], "tradicional": ["tradicion", "calido", "rustico"], "moderno": ["moderno", "minimal"],
    "terraza": ["fresco", "luminoso"], "playero": ["playero", "fresco", "luminoso", "festivo"], "festivo": ["festivo", "pop"], "tranquilo": ["calmado", "minimal"],
}
SERVICIOS = tuple(RASGOS_SERVICIO)
AMBIENTES = tuple(RASGOS_AMBIENTE)

UMBRAL_AFINIDAD_MAXIMA = 3     # coincidencias que cuentan como máximo por opción


# ------------------------------------------------------------------ rasgos del restaurante
def rasgos(F, tonos):
    """Lista de rasgos del restaurante y de dónde sale cada uno: la cocina (tonos), el servicio, el precio y el ambiente de la ficha."""
    out = {}
    for t in tonos:
        out.setdefault(t, "cocina, nombre o descripción")
    P = F.get("perfil") or {}
    for s in P.get("servicio", []):
        for t in RASGOS_SERVICIO.get(s, []):
            out.setdefault(t, f"perfil.servicio {s}")
    if P.get("precio") in RASGOS_PRECIO:
        for t in RASGOS_PRECIO[P["precio"]]:
            out.setdefault(t, f"perfil.precio {P['precio']}")
    for a in P.get("ambiente", []):
        for t in RASGOS_AMBIENTE.get(a, []):
            out.setdefault(t, f"perfil.ambiente {a}")
    pers = (F.get("estilo") or {}).get("personalidad")
    out.setdefault(pers, "personalidad de la ficha")
    return out


def afinidad(dim, opcion, tags):
    coinciden = [t for t in A.get((dim, opcion), []) if t in tags]
    return min(len(coinciden), UMBRAL_AFINIDAD_MAXIMA), coinciden


# ------------------------------------------------------------------ viabilidad: qué datos necesita cada opción
def viable(dim, opcion, F):
    if (dim, opcion) in PENDIENTES:
        return False
    n_gal = len(F.get("galeria") or [])
    hero = "hero" in (F.get("activos") or {})
    if dim == "portada":
        if opcion in ("luz_brasas", "marco_editorial", "cortina"):
            return hero
        if opcion in ("mural_columnas", "collage_pegatinas"):
            return n_gal >= 4
        if opcion == "cartel_rotulo":
            return n_gal >= 1 or "logo" in (F.get("activos") or {})
    if dim == "galeria":
        minimo = {"mosaico": 1, "cuadricula_ig": 1, "cinta": 2, "polaroid": 3, "bento": 5}.get(opcion, 1)
        return n_gal >= minimo
    return True


# ------------------------------------------------------------------ elección
def _desempate(ficha_id, dim, opcion):
    return int(hashlib.sha1(f"{ficha_id}|{dim}|{opcion}".encode()).hexdigest()[:6], 16) / 0xFFFFFF * 0.05   # la misma ficha recibe siempre lo mismo


def _novedad(dim, opcion, previas):
    """Premio por no repetir lo que usaron las webs recientes y castigo por repetirlo."""
    usos4 = sum(1 for v in previas[:4] if v.get(dim) == opcion)
    usos12 = sum(1 for v in previas[:_huella.VENTANA] if v.get(dim) == opcion)
    if usos12 == 0:
        return 0.35
    return -0.8 * usos4 - 0.15 * (usos12 - usos4)


MUESTRAS = 600        # composiciones que se prueban para cada web (el espacio tiene decenas de miles)
TEMPERATURA = 0.7     # cuánto se deja de lado la afinidad a favor de la variedad al muestrear


def componer(F, registro, tonos, fijados=None, origen_fijados=None, tipos=None, paleta_cubo=None, orden=None):
    """Elige la composición de una web. `registro` es el registro de huellas (para la rotación). Devuelve un diccionario serializable:
    la elección de cada dimensión, su motivo (rasgos que coinciden, novedad) y las alternativas puntuadas.

    Cada dimensión tiene un orden de preferencia (afinidad con los rasgos del restaurante y novedad frente a las últimas webs). Se prueban cientos de
    combinaciones (la mejor de cada dimensión primero, el resto muestreadas con más probabilidad cuanto mejor encajan, con una semilla fija por web) y se
    queda la de mayor encaje que cumple la variedad: distancia ponderada de al menos UMBRAL con cada una de las últimas VENTANA webs y ninguna huella igual
    en todo el registro. `tipos` son las parejas tipográficas posibles ya filtradas (cubren el texto, están probadas y cumplen la rotación)."""
    ficha_id = F["id"]
    est = F.get("estilo") or {}
    fam = est["personalidad"]
    tags = rasgos(F, tonos)
    fijados = dict(fijados or {})
    previas = [v for _, v in _huella.vecinas(ficha_id, registro, _huella.VENTANA)]
    ranking, motivos = {}, {}
    for dim in DIMENSIONES:
        cands = [o for o in OPCIONES[dim][fam] if viable(dim, o, F)]
        filas = []
        for o in cands:
            n, coinciden = afinidad(dim, o, tags)
            nov = _novedad(dim, o, previas)
            filas.append({"opcion": o, "afinidad": n, "coinciden": coinciden, "novedad": round(nov, 2), "puntos": round(n + nov + _desempate(ficha_id, dim, o), 3)})
        filas.sort(key=lambda f: -f["puntos"])
        ranking[dim] = filas
    if tipos:
        ranking["tipografia"] = [{"opcion": f["clave"], "afinidad": f["puntos"], "coinciden": f["tonos_que_encajan"], "novedad": 0.0, "puntos": round(f["puntos"] * 3 + _desempate(ficha_id, "tipografia", f["clave"]), 3)} for f in tipos]
    dims = list(ranking)
    opciones_fijas = {d: v for d, v in fijados.items() if d in ranking}

    def huella_de(el):
        pack = PAQUETES[el["animaciones"]]
        forma = est.get("forma") if est.get("forma") not in (None, "auto") else forma_de(tags)
        mov = est.get("movimiento") if est.get("movimiento") not in (None, "auto") else pack["movimiento"]
        clave = el.get("tipografia")
        e = {"familia": fam, "paleta_cubo": paleta_cubo or est.get("paleta", "auto"), "paleta": paleta_cubo or est.get("paleta", "auto"), "tipografia": clave or "-", "forma": forma, "movimiento": mov,
             "orden": orden or ["portada"], **{d: el[d] for d in DIMENSIONES}}
        h = _huella.huella(F, e) if clave else {**{k: e[k] for k in ("paleta",)}, "familia": fam, **{d: el[d] for d in DIMENSIONES}, "orden": "-", "forma_movimiento": f"{forma}+{mov}"}
        return h

    rng = random.Random(int(hashlib.sha1(f"{ficha_id}|{len(registro)}".encode()).hexdigest()[:12], 16))
    vecinas = _huella.vecinas(ficha_id, registro, _huella.VENTANA)
    firmas = {_huella.firma(v) for k, v in registro.items() if k != ficha_id}
    mejor_fila = {d: ranking[d][0]["opcion"] for d in dims}
    for d, v in opciones_fijas.items():
        mejor_fila[d] = v

    def candidato(rnd):
        el = {}
        for d in dims:
            if d in opciones_fijas:
                el[d] = opciones_fijas[d]
            elif rnd is None:
                el[d] = mejor_fila[d]
            else:
                filas = ranking[d]
                m = max(f["puntos"] for f in filas)
                pesos = [math.exp((f["puntos"] - m) / TEMPERATURA) for f in filas]
                el[d] = rnd.choices([f["opcion"] for f in filas], weights=pesos)[0]
        return el

    def puntos(el):
        return sum(next((f["puntos"] for f in ranking[d] if f["opcion"] == el[d]), 0.0) for d in dims)

    def con_par_no_viable(el):
        return any(((d1, el[d1]), (d2, el[d2])) in PARES_NO_VIABLES or ((d2, el[d2]), (d1, el[d1])) in PARES_NO_VIABLES
                   for i, d1 in enumerate(dims) for d2 in dims[i + 1:] if d1 in el and d2 in el)

    evaluados = []
    for i in range(MUESTRAS):
        el = candidato(None if i == 0 else rng)
        h = huella_de(el)
        d_min = min([_huella.distancia(h, v) for _, v in vecinas] or [99])
        evaluados.append((el, d_min, _huella.firma(h) in firmas, puntos(el), con_par_no_viable(el)))
    evaluados = [e for e in evaluados if not e[4]] or evaluados   # sin pares que el Gate no deja pasar (salvo que no quede otra: lo fijado en la ficha manda)
    buenos = [e for e in evaluados if e[1] >= _huella.UMBRAL and not e[2]]
    if buenos:
        el, d_min = max(buenos, key=lambda e: e[3])[:2]
        limitada = False
    else:
        sin_copia = [e for e in evaluados if not e[2]] or evaluados
        el, d_min = max(sin_copia, key=lambda e: (e[1], e[3]))[:2]
        limitada = True
    for d in dims:
        fila = next((f for f in ranking[d] if f["opcion"] == el[d]), None)
        if d in fijados:
            motivos[d] = (origen_fijados or {}).get(d, "fijada en la ficha")
        elif fila and fila["coinciden"]:
            motivos[d] = "encaja con " + ", ".join(fila["coinciden"]) + ("; no la usó ninguna de las últimas webs" if fila["novedad"] > 0 else "")
        else:
            motivos[d] = "elegida por la rotación para distinguirse de las últimas webs" if fila and fila["novedad"] > 0 else "sin rasgos que la pidan; la elige la rotación"
    return {"familia": fam, "elegidas": el, "motivos": motivos, "rasgos": tags, "ranking": ranking, "distancia_minima": d_min, "variedad_limitada": limitada,
            "ajustes_por_variedad": ([f"se probaron {MUESTRAS} combinaciones: la mejor llega a {d_min} puntos de {_huella.UMBRAL} frente a las últimas webs"] if limitada else [])}


def forma_de(tags):
    """Esquinas suaves para un restaurante amable, dulce o familiar; rectas para el resto."""
    return "suave" if any(t in tags for t in ("amable", "dulce", "playero", "festivo", "pop", "familiar")) else "recta"


def _huella_provisional(F, elegidas):
    """Solo las dimensiones de composición (sirve para medir la distancia mientras se elige)."""
    h = {"familia": F["estilo"]["personalidad"]}
    h.update(elegidas)
    return h


# ------------------------------------------------------------------ orden de las secciones por defecto
def orden_por_defecto(F):
    fam = F["estilo"]["personalidad"]
    if fam == "elegante":
        o = ["portada"] + (["idea"] if F.get("historia") else []) + ["carta"] + (["ambiente"] if F.get("galeria") else []) + (["reserva"] if F.get("reservas") else []) + ["visita", "cierre"]
    else:
        o = (["portada"] + (["regla"] if F.get("idea") else []) + (["como"] if F.get("pedido") else []) + ["carta"] + (["fotos"] if F.get("galeria") else []) + ["visita", "cierre"])
    return o


def animaciones_de(paquete):
    return list(PAQUETES[paquete]["modulos"])
