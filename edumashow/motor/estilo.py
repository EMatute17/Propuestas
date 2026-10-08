"""Director de estilo: convierte los datos reales de un restaurante en decisiones de diseño, y deja escrita la razón de cada una.

Qué decide (y de qué dato sale):
  - la paleta: del color de identidad del logo, con el acento de temporada y los fondos de WGSN x Coloro (color.py);
  - la tipografía del titular: la pareja que mejor encaja con el carácter de la cocina y que no repite fuente ni clase
    de las webs anteriores (rotación, huella.py);
  - el orden de las fotos del mural y de la galería: por antojo (antojo.py), con el juicio visual escrito en la ficha;
  - qué idea se dibuja: la regla de medidas, solo si la carta tiene medidas reales.

Nada se inventa: cada decisión se traza a un campo de la ficha o a una medida, y el resultado (con sus alternativas) va al
manifiesto y al informe del Gate. Una ficha puede fijar a mano cualquier decisión: lo fijado manda y solo se valida."""
import hashlib
import os
import re

from PIL import Image

from . import antojo, color, huella as _huella, temas, tipografia

VERSION = "0.1.0"

# carácter de cocina: palabras de la ficha (cocina, nombre, descripción) que sugieren un tono tipográfico
TONOS_COCINA = [
    (r"parrill|asad|churrasc|brasa|grill|carne|bbq|barbacoa", ["parrilla", "potente", "callejero", "urbano"]),
    (r"hamburgues|burger|pizz|alitas|wings|tacos|street|calle|fast", ["callejero", "joven", "urbano", "pop"]),
    (r"pasta|trattor|ital|risott", ["italiana", "clasico", "calido", "trattoria"]),
    (r"pasteler|reposter|dulce|postre|chocolat|helad", ["lujo", "dulce", "pasteleria"]),
    (r"vegan|saludable|ensalad|fresco|bowl", ["fresco", "saludable", "amable"]),
    (r"alta cocina|autor|degustaci|gourmet|fine", ["autor", "elegante", "premium", "contemporaneo"]),
    (r"panader|artesan|tradici|casero|abuela", ["tradicion", "artesanal", "calido"]),
    (r"sushi|nikkei|ramen|japon", ["minimal", "tecnica", "moderno"]),
    (r"mariscos|pescad|cevich|marin", ["fresco", "elegante", "calido"]),
]


def tonos_de(F):
    """Tonos del restaurante: los que fija la ficha o, si no, los que sugieren su cocina, su nombre y su descripción."""
    e = F.get("estilo", {})
    if e.get("tono"):
        return list(e["tono"]), "fijados en la ficha (estilo.tono)"
    N = F["negocio"]
    texto = " ".join([N.get("cocina", ""), N.get("nombre", ""), N.get("descripcion", "")]).lower()
    tonos = []
    for patron, ts in TONOS_COCINA:
        if re.search(patron, texto):
            tonos += [t for t in ts if t not in tonos]
    if e.get("personalidad") == "elegante":
        tonos += [t for t in ("elegante", "premium", "calido") if t not in tonos]
    return tonos, "sacados de la cocina, el nombre y la descripción"


# ------------------------------------------------------------------ paleta
def _tokens_con_acento(tokens):
    t = dict(tokens)
    t.setdefault("acento", t["brasa-2"])
    t.setdefault("acento-papel", t["brasa-papel"])
    return t


def resolver_paleta(F, origen_activos, fecha=None):
    """Tokens de color de la web. Con paleta 'auto' salen del logo; con el nombre de una paleta hecha a mano, de ella (solo se valida)."""
    est = F["estilo"]
    if est["paleta"] != "auto":
        tokens = _tokens_con_acento(temas.PALETAS[est["paleta"]])
        return {"id": est["paleta"], "origen": "paleta hecha a mano, validada con los mismos pares de contraste", "tokens": tokens,
                "pares": color.pares_de_contraste(tokens), "informe": None}
    if "logo" not in F.get("activos", {}):
        from .generar import FichaIncompleta
        raise FichaIncompleta("estilo.paleta auto necesita activos.logo: el color de identidad sale del logo")
    im = Image.open(os.path.join(origen_activos, F["activos"]["logo"]["archivo"]))
    dominantes = color.colores_dominantes(im, k=6)
    marca = color.color_de_marca(dominantes)
    if marca is None:
        from .generar import FichaIncompleta
        raise FichaIncompleta("no se pudo sacar un color de identidad del logo")
    tokens, rep = color.paleta_marca(marca["hex"], fecha, variante=est.get("variante_paleta", 0), con_acento=est.get("acento_temporada", True))
    rep["dominantes_del_logo"] = dominantes
    return {"id": "auto:" + tokens["brasa"].lstrip("#"), "origen": f'derivada del logo (color de identidad {marca["hex"]}, tono {marca["h"]:.0f})',
            "tokens": tokens, "pares": rep["pares"], "informe": rep}


# ------------------------------------------------------------------ tipografía
def elegir_tipografia(F, texto, registro, tonos):
    """Clasifica las parejas posibles de la personalidad y devuelve la mejor que cubre todos los caracteres y cumple la rotación."""
    est = F["estilo"]
    pers = est["personalidad"]
    clave_ficha = est["tipografia"]
    nombre = F["negocio"]["nombre"]
    filas = []
    for k, p in tipografia.PAREJAS.items():
        if pers not in p["personalidades"]:
            continue
        faltan = tipografia.faltantes(k, texto)
        rot = _huella.rotacion(F["id"], {"display": p["familia_display"], "clase_tipografica": p["clase"]}, registro)
        coincide = [t for t in p["tonos"] if t in tonos]
        puntos = len(coincide) / max(1, len(tonos)) if tonos else 0.0
        probada = tipografia.esta_probada(k, pers)
        puntos += 0.05 if probada else 0.0
        desempate = int(hashlib.sha1(f"{nombre}|{k}".encode()).hexdigest()[:6], 16) / 0xFFFFFF * 0.01   # la misma marca recibe siempre lo mismo
        filas.append({"clave": k, "display": p["familia_display"], "clase": p["clase"], "tonos_que_encajan": coincide, "puntos": round(puntos, 3),
                      "orden": puntos + desempate, "faltan_caracteres": "".join(faltan), "rotacion": rot, "probada": probada, "ancho_em": tipografia.ancho_em(k)})
    filas.sort(key=lambda f: -f["orden"])
    aptas = [f for f in filas if not f["faltan_caracteres"] and not f["rotacion"] and f["probada"]]
    if clave_ficha != "auto":
        elegida = next((f for f in filas if f["clave"] == clave_ficha), None)
        origen = "fijada en la ficha"
    else:
        elegida = aptas[0] if aptas else None
        origen = "elegida por el director: la mejor probada que cubre los caracteres y cumple la rotación"
    if elegida is None:
        from .generar import FichaIncompleta
        raise FichaIncompleta(f"no hay una pareja tipográfica probada para la personalidad {pers} que cubra el texto y cumpla la rotación")
    return {"clave": elegida["clave"], "origen": origen, "elegida": elegida, "ranking": [{k: v for k, v in f.items() if k != "orden"} for f in filas]}


# ------------------------------------------------------------------ fotos
def puntuar_fotos(F, origen_activos):
    """Registro de antojo de cada foto que declara su juicio en la ficha, y el orden de más a menos provocativa."""
    registros = {}
    for clave, a in F.get("activos", {}).items():
        if "antojo" not in a:
            continue
        im = Image.open(os.path.join(origen_activos, a["archivo"]))
        registros[clave] = antojo.puntuar(im, a["antojo"])
    return registros, antojo.ranking(registros)


# ------------------------------------------------------------------ todo junto
def _limpio(x):
    """Convierte lo que salga de numpy a tipos de JSON."""
    if isinstance(x, dict):
        return {str(k): _limpio(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_limpio(v) for v in x]
    if hasattr(x, "item"):
        return x.item()
    return x


def para_manifiesto(D):
    """Las decisiones, listas para guardarse en el manifiesto del sitio."""
    return _limpio(D)


def decidir(F, origen_activos, registro, fecha=None):
    """Decisiones de diseño de una ficha. Devuelve un diccionario serializable y completo (va al manifiesto)."""
    est = F["estilo"]
    fecha = fecha or F.get("confirmacion", {}).get("fecha")
    tonos, de_donde = tonos_de(F)
    import json
    texto = json.dumps(F, ensure_ascii=False)
    from . import pedido
    if pedido.activo(F):
        texto += json.dumps(pedido.textos(F), ensure_ascii=False)
    paleta = resolver_paleta(F, origen_activos, fecha)
    tipo = elegir_tipografia(F, texto, registro, tonos)
    registros, orden = puntuar_fotos(F, origen_activos)
    d = {
        "version_director": VERSION, "fecha_de_referencia": fecha, "tonos": {"lista": tonos, "origen": de_donde},
        "paleta": paleta, "tipografia": tipo,
        "fotos": {"registros": registros, "orden_por_antojo": orden, "usa_el_orden": est.get("orden_fotos") == "antojo",
                  "criterios": {k: {"descripcion": v[0], "peso": v[1]} for k, v in antojo.CRITERIOS.items()},
                  "pesos": {"juicio": antojo.PESO_JUICIO, "tecnica": antojo.PESO_TECNICA}},
        "estilo_resuelto": {"paleta": paleta["id"], "tipografia": tipo["clave"]},
    }
    # la idea que se dibuja: solo si la carta tiene medidas reales
    idea = F.get("idea")
    if idea:
        cat = next(c for c in F["carta"] if c["id"] == idea["categoria"])
        d["idea"] = {"pieza": "regla de medidas", "categoria": idea["categoria"], "unidad": idea["unidad"],
                     "medidas": [p["medida"] for p in cat["platos"] if p.get("medida")], "datos": "medida y precio de cada plato, de la carta de la ficha"}
    return d
