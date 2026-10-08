"""Huella de diseño y distancia entre webs (Gate de unicidad, R-VAR-01 y R-VAR-04) y rotación tipográfica (R-VAR-03).

La huella de una web reúne su familia (elegante o urbano), la paleta (el cubo de tono de su color de marca), la tipografía de titular y las
opciones de composición: portada, carta, galería, ornamento, botones, densidad, textura y paquete de animaciones, además del orden de las secciones
y la forma y el movimiento. Cada dimensión pesa según lo que se nota a primera vista (la familia y la portada pesan más que los botones).

Dos webs son suficientemente distintas si la suma de los pesos de las dimensiones en que difieren llega al umbral frente a cada una de las últimas
VENTANA webs registradas, y no hay dos huellas completas iguales en todo el registro. Con cientos de webs no se puede exigir que cada una difiera de todas
las demás: la ventana mide lo que se nota al ver webs seguidas, y la firma completa evita las copias.

Rotación (Documento Maestro, 6.3, adaptada a cientos de webs): una misma tipografía de titular web tras web hace que todas se parezcan aunque cambien los
colores. Es FALLO que el titular nuevo use la misma fuente que alguna de las 3 webs anteriores de su familia, o la misma clase tipográfica que 2 de las 4
anteriores de su familia cuando la familia tiene más de una clase. Con una sola clase en la familia (las serifas de la elegante) solo cuenta la fuente. El
orden lo da la secuencia con la que se registraron. Se cuenta dentro de la familia porque la elegante y la urbana no compiten por las mismas fuentes.

Un registro puede ser consultado y escrito por varias webs construyéndose a la vez: la elección de composición y su anotación como reservada ocurren
juntas bajo un candado (`reservar`), y el Gate la marca aprobada cuando la web pasa el Gate completo (`registrar`).
"""
import colorsys
import contextlib
import hashlib
import json
import os

from . import tipografia

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
REGISTRO_POR_DEFECTO = os.path.join(RAIZ, "gate", "registro_huellas.json")


def ruta_registro():
    """El registro de huellas de las webs aprobadas. Las pruebas usan otro con la variable EDUMASHOW_REGISTRO, para no ensuciar el real."""
    return os.environ.get("EDUMASHOW_REGISTRO") or REGISTRO_POR_DEFECTO


PESOS = {"familia": 3, "portada": 3, "carta": 2, "galeria": 2, "paleta": 2, "tipografia": 2, "animaciones": 2,
         "ornamento": 1, "boton": 1, "densidad": 1, "textura": 1, "orden": 1, "forma_movimiento": 1}
DIMENSIONES = tuple(PESOS)
UMBRAL = 8            # suma mínima de pesos de las dimensiones que difieren (de 23 posibles)
VENTANA = 12          # con cuántas de las últimas webs se compara

ULTIMAS_FUENTE, MAX_FUENTE = 3, 1       # la misma fuente de titular que alguna de las 3 anteriores de la familia es fallo
ULTIMAS_CLASE, MAX_CLASE = 4, 2         # la misma clase en 2 de las 4 anteriores de la familia es fallo (si la familia tiene más de una clase)

# lo que dibujaban las webs registradas antes de que existiera el catálogo: sirve para comparar con ellas
_LEGADO = {"elegante": {"galeria": "mosaico", "ornamento": "recto", "boton": "solido", "densidad": "media", "textura": "grano", "animaciones": "brasa"},
           "urbano": {"galeria": "cuadricula_ig", "ornamento": "recto", "boton": "solido", "densidad": "media", "textura": "grano", "animaciones": "cartel"}}


def cubo_de_tono(hex_):
    """Cubo de 30 grados del tono de un color (12 cubos). Dos marcas de un naranja parecido caen en el mismo cubo."""
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    tono, _, _ = colorsys.rgb_to_hls(r, g, b)
    return f"h{int(tono * 360 // 30) % 12:02d}"


def huella(ficha, estilo=None):
    """Huella de diseño. `estilo` es el estilo ya resuelto por el director (todas sus decisiones concretas); si no se da, el de la ficha."""
    e = estilo or ficha["estilo"]
    clave = e["tipografia"]
    fam = e.get("familia") or e["personalidad"]
    h = {
        "familia": fam,
        "paleta": e.get("paleta_cubo") or e["paleta"],
        "tipografia": clave,
        "display": tipografia.display_de(clave),
        "clase_tipografica": tipografia.clase(clave),
        "portada": e["portada"],
        "carta": e["carta"],
        "galeria": e.get("galeria") or _LEGADO[fam]["galeria"],
        "orden": hashlib.sha1("|".join(e["orden"]).encode()).hexdigest()[:8],
        "forma_movimiento": f'{e["forma"]}+{e["movimiento"]}',
    }
    for d in ("ornamento", "boton", "densidad", "textura", "animaciones"):
        h[d] = e.get(d) or _LEGADO[fam][d]
    return h


def normalizar(v):
    """Una huella del registro, completada con lo que dibujaba la web cuando se registró (las webs anteriores al catálogo)."""
    v = dict(v)
    if "familia" not in v:
        v["familia"] = "elegante" if v.get("portada") == "luz_brasas" else "urbano"
    for d, valor in _LEGADO[v["familia"]].items():
        v.setdefault(d, valor)
    return v


def distancia(a, b):
    """Suma de los pesos de las dimensiones en que difieren (la secuencia y los datos de rotación no cuentan)."""
    a, b = normalizar(a), normalizar(b)
    return sum(p for d, p in PESOS.items() if a.get(d) != b.get(d))


def firma(h):
    """Identificador de la huella completa: dos webs con la misma firma son la misma web con otro nombre."""
    h = normalizar(h)
    return hashlib.sha1(json.dumps({d: h.get(d) for d in DIMENSIONES}, sort_keys=True).encode()).hexdigest()[:12]


def cargar_registro(ruta):
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    return {}


def vecinas(ficha_id, registro, n=VENTANA):
    """Las últimas n webs del registro (sin la propia), de la más reciente a la más antigua: [(id, huella)]."""
    filas = sorted(((v.get("secuencia", 0), k, v) for k, v in registro.items() if k != ficha_id), reverse=True)
    return [(k, v) for _, k, v in filas[:n]]


def anteriores(ficha_id, registro):
    """Las demás webs del registro, de la más reciente a la más antigua."""
    return [v for _, v in vecinas(ficha_id, registro, len(registro))]


def comparar(ficha_id, h, registro):
    """Compara la huella con las últimas VENTANA webs. Devuelve ([(otra_web, distancia)], cumple, [copias exactas en todo el registro])."""
    otras = [(k, distancia(h, v)) for k, v in vecinas(ficha_id, registro, VENTANA)]
    f = firma(h)
    copias = [k for k, v in registro.items() if k != ficha_id and firma(v) == f]
    cumple = all(d >= UMBRAL for _, d in otras) and not copias
    return otras, cumple, copias


def _clases_de_familia(familia):
    return {tipografia.clase(k) for k, p in tipografia.PAREJAS.items() if familia in p["personalidades"]}


def rotacion(ficha_id, h, registro, familia=None):
    """Lista de problemas de rotación tipográfica de una huella frente a las webs registradas de su familia (vacía si cumple)."""
    familia = familia or h.get("familia")
    previas = [v for v in anteriores(ficha_id, registro) if normalizar(v)["familia"] == familia] if familia else anteriores(ficha_id, registro)
    en_fuente = sum(1 for v in previas[:ULTIMAS_FUENTE] if v.get("display") == h["display"])
    en_clase = sum(1 for v in previas[:ULTIMAS_CLASE] if v.get("clase_tipografica") == h["clase_tipografica"])
    problemas = []
    if en_fuente >= MAX_FUENTE:
        problemas.append(f'la fuente de titular {h["display"]} ya está en {en_fuente} de las {min(ULTIMAS_FUENTE, len(previas))} webs anteriores de la familia {familia}')
    if en_clase >= MAX_CLASE and len(_clases_de_familia(familia)) > 1:
        problemas.append(f'la clase tipográfica {h["clase_tipografica"]} ya está en {en_clase} de las {min(ULTIMAS_CLASE, len(previas))} webs anteriores de la familia {familia}')
    return problemas


# ------------------------------------------------------------------ escritura con candado
@contextlib.contextmanager
def _candado(ruta):
    """Con varias webs verificándose o construyéndose a la vez, un candado impide que dos escrituras se pisen."""
    try:
        import fcntl
    except ImportError:   # Windows: sin candado (se trabaja de una en una)
        fcntl = None
    os.makedirs(os.path.dirname(os.path.abspath(ruta)), exist_ok=True)
    with open(ruta + ".lock", "w") as cerrojo:
        if fcntl:
            fcntl.flock(cerrojo, fcntl.LOCK_EX)
        yield


def _escribir(ruta, reg):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")


def _secuencia(reg, ficha_id):
    previo = reg.get(ficha_id, {})
    return previo.get("secuencia") or (max([v.get("secuencia", 0) for v in reg.values()] or [0]) + 1)


def reservar(ficha_id, ruta, elegir):
    """Elige y anota, bajo el candado, la huella de una web que se está construyendo. `elegir(registro)` devuelve (huella, lo_que_se_devuelve).
    La huella queda como reservada: las webs que se construyan después (también en paralelo) la ven y no la repiten."""
    with _candado(ruta):
        reg = cargar_registro(ruta)
        h, extra = elegir(reg)
        h = dict(h)
        h["secuencia"] = _secuencia(reg, ficha_id)
        previo = reg.get(ficha_id) or {}
        h["estado"] = "aprobada" if previo.get("estado") == "aprobada" and firma(previo) == firma(h) else "reservada"
        reg[ficha_id] = h
        _escribir(ruta, reg)
        return h, extra


def registrar(ficha_id, h, ruta):
    """Anota la huella de una web que pasó el Gate completo (aprobada)."""
    with _candado(ruta):
        reg = cargar_registro(ruta)
        h = dict(h)
        h["secuencia"] = _secuencia(reg, ficha_id)
        h["estado"] = "aprobada"
        reg[ficha_id] = h
        _escribir(ruta, reg)
