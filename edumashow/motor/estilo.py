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

from . import antojo, catalogo, color, huella as _huella, temas, tipografia

VERSION = "0.2.0"

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
    (r"mariscos|pescad|cevich|marin|peruan", ["fresco", "marino", "elegante", "luminoso"]),
    (r"caf[eé]|cafeter|brunch|desayun|bakery", ["fresco", "luminoso", "calmado", "moderno", "cafe"]),
    (r"\bbar\b|c[oó]ctel|cocktail|cerveza|taproom|\bpub\b|lounge", ["nocturno", "social", "joven", "festivo"]),
    (r"arepa|empanada|cachapa|criolla|callejer", ["callejero", "calido", "familiar"]),
    (r"taco|mexican|antojit|taquer|burrito", ["callejero", "festivo", "pop", "calido"]),
    (r"familiar|casa de comidas|menu del dia|men[uú] del d[ií]a", ["familiar", "calido", "tradicion", "amable"]),
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


# Restaurante sin logo: el color de marca lo propone el director según el tono de su cocina. Rangos de matiz (grados OKLCH) que van con cada tono.
MATICES_POR_TONO = [
    (("parrilla", "potente", "callejero"), [(28, 48), (52, 68)]),
    (("pop", "festivo", "joven", "social", "nocturno"), [(335, 358), (295, 325), (195, 215), (88, 104)]),
    (("italiana", "clasico", "trattoria", "tradicion", "artesanal", "calido", "familiar"), [(28, 42), (62, 80), (118, 134)]),
    (("dulce", "pasteleria", "lujo"), [(340, 358), (300, 328), (12, 28)]),
    (("fresco", "saludable", "amable", "luminoso", "cafe"), [(132, 158), (98, 120), (176, 198)]),
    (("marino",), [(214, 244), (190, 212)]),
    (("autor", "elegante", "premium", "contemporaneo", "minimal", "moderno", "tecnica"), [(10, 24), (150, 168), (240, 268), (302, 322)]),
]


def _paleta_sin_logo(F, fecha, tonos, registro):
    """Paleta de un restaurante sin logo: el color de marca sale del tono de su cocina y se aparta de los matices de las últimas webs, para que los restaurantes
    sin logo no acaben todos con las mismas dos paletas hechas a mano. Es una propuesta de diseño, no un dato del restaurante: se confirma con el dueño."""
    from .generar import FichaIncompleta
    est = F["estilo"]
    # los dos primeros tonos con matices propios mandan (los de la cocina van antes que los genéricos de la personalidad)
    grupos = []
    for t in tonos:
        for i, (palabras, _) in enumerate(MATICES_POR_TONO):
            if t in palabras and i not in grupos:
                grupos.append(i)
        if len(grupos) >= 2:
            break
    rangos = [r for i in grupos for r in MATICES_POR_TONO[i][1]]
    grupo = ", ".join(t for t in tonos[:3]) or "sin tono"
    if not rangos:
        rangos, grupo = [(0, 359)], "ningún tono concreto"
    matices = sorted({h % 360 for a, b in rangos for h in range(a, b + 1, 6)})
    if est.get("matiz") is not None:   # el dueño o quien arma la ficha fija el matiz (grados OKLCH); el director solo comprueba que el contraste se cumpla
        matices, grupo = [int(est["matiz"]) % 360], "matiz fijado en la ficha (estilo.matiz)"
    recientes = [_huella.normalizar(v).get("paleta") for _, v in _huella.vecinas(F["id"], registro, 8)]
    semilla = hashlib.sha1(F["id"].encode()).hexdigest()
    # primero los matices cuyo cubo de tono no está en las últimas webs; entre ellos, un orden fijo por el id de la ficha
    def clave(h):
        cubo = _huella.cubo_de_tono(color.desde_oklch(0.74, 0.17, h))
        return (recientes.count(cubo), hashlib.sha1(f"{semilla}|{h}".encode()).hexdigest())
    ultimo_error = ""
    for h in sorted(matices, key=clave)[:12]:
        marca = color.desde_oklch(0.62, 0.17, h)
        tokens, rep = color.paleta_marca(marca, fecha, variante=est.get("variante_paleta", 0), con_acento=est.get("acento_temporada", True))
        malos = [f'{p["texto"]} sobre {p["fondo"]} ({p["contraste"]}:1)' for p in rep["pares"] if not p["ok"]]
        if malos:
            ultimo_error = "; ".join(malos)
            continue
        rep["dominantes_del_logo"] = []
        return {"id": "auto:" + tokens["brasa"].lstrip("#"),
                "origen": f"propuesta del director (sin logo): color de marca {marca}, matiz {h} grados, del tono de la cocina ({grupo}); confirmar el color con el restaurante",
                "tokens": tokens, "pares": rep["pares"], "informe": rep}
    raise FichaIncompleta("ningún color de marca propuesto para un restaurante sin logo llega al contraste exigido (" + ultimo_error + "). Fija una paleta hecha a mano en estilo.paleta")


def resolver_paleta(F, origen_activos, fecha=None, tonos=(), registro=None):
    """Tokens de color de la web. Con paleta 'auto' salen del logo (o, sin logo, del tono de la cocina); con el nombre de una paleta hecha a mano, de ella (solo se valida)."""
    est = F["estilo"]
    if est.get("paleta", "auto") != "auto":
        tokens = _tokens_con_acento(temas.PALETAS[est["paleta"]])
        return {"id": est["paleta"], "origen": "paleta hecha a mano, validada con los mismos pares de contraste", "tokens": tokens,
                "pares": color.pares_de_contraste(tokens), "informe": None}
    if "logo" not in F.get("activos", {}):
        return _paleta_sin_logo(F, fecha, list(tonos), registro or {})
    im = Image.open(os.path.join(origen_activos, F["activos"]["logo"]["archivo"]))
    dominantes = color.colores_dominantes(im, k=6)
    marca = color.color_de_marca(dominantes)
    if marca is None:
        from .generar import FichaIncompleta
        raise FichaIncompleta("no se pudo sacar un color de identidad del logo")
    if marca.get("neutro"):
        # logotipo de un solo tono (negro, blanco o grises): no trae color de marca, y un gris como color de marca dejaría los botones apagados.
        # El director propone el color como si no hubiera logo (el logo se muestra tal cual, en negro o blanco) y el dueño lo confirma
        p = _paleta_sin_logo(F, fecha, list(tonos), registro or {})
        p["origen"] = p["origen"].replace("propuesta del director (sin logo)", "propuesta del director (el logo es de un solo tono, sin color de marca)")
        p["informe"]["dominantes_del_logo"] = dominantes
        return p
    tokens, rep = color.paleta_marca(marca["hex"], fecha, variante=est.get("variante_paleta", 0), con_acento=est.get("acento_temporada", True))
    rep["dominantes_del_logo"] = dominantes
    malos = [f'{p["texto"]} sobre {p["fondo"]} ({p["contraste"]}:1, mínimo {p["minimo"]})' for p in rep["pares"] if not p["ok"]]
    if malos:   # el director no entrega una paleta que no cumple: se abstiene y pide una a mano
        from .generar import FichaIncompleta
        raise FichaIncompleta("la paleta derivada del logo no llega al contraste exigido en " + "; ".join(malos) + ". Fija una paleta hecha a mano en estilo.paleta")
    return {"id": "auto:" + tokens["brasa"].lstrip("#"), "origen": f'derivada del logo (color de identidad {marca["hex"]}, tono {marca["h"]:.0f})',
            "tokens": tokens, "pares": rep["pares"], "informe": rep}


# ------------------------------------------------------------------ tipografía
def elegir_tipografia(F, texto, registro, tonos, conservar=None):
    """Clasifica las parejas posibles de la personalidad y devuelve la mejor que cubre todos los caracteres y cumple la rotación."""
    est = F["estilo"]
    pers = est["personalidad"]
    clave_ficha = est.get("tipografia", "auto")
    nombre = F["negocio"]["nombre"]
    filas = []
    for k, p in tipografia.PAREJAS.items():
        if pers not in p["personalidades"]:
            continue
        faltan = tipografia.faltantes(k, texto)
        rot = _huella.rotacion(F["id"], {"display": p["familia_display"], "clase_tipografica": p["clase"]}, registro, familia=pers)
        coincide = [t for t in p["tonos"] if t in tonos]
        puntos = len(coincide) / max(1, len(tonos)) if tonos else 0.0
        probada = tipografia.esta_probada(k, pers)
        puntos += 0.05 if probada else 0.0
        desempate = int(hashlib.sha1(f"{nombre}|{k}".encode()).hexdigest()[:6], 16) / 0xFFFFFF * 0.01   # la misma marca recibe siempre lo mismo
        filas.append({"clave": k, "display": p["familia_display"], "clase": p["clase"], "tonos_que_encajan": coincide, "puntos": round(puntos, 3),
                      "orden": puntos + desempate, "faltan_caracteres": "".join(faltan), "rotacion": rot, "probada": probada, "ancho_em": tipografia.ancho_em(k)})
    filas.sort(key=lambda f: -f["orden"])
    aptas = [f for f in filas if not f["faltan_caracteres"] and not f["rotacion"] and f["probada"]]
    previa = next((f for f in filas if f["clave"] == conservar and not f["faltan_caracteres"] and f["probada"]), None) if conservar else None
    if clave_ficha != "auto":
        elegida = next((f for f in filas if f["clave"] == clave_ficha), None)
        origen = "fijada en la ficha"
    elif previa is not None:
        elegida = previa
        origen = "conservada de la construcción anterior de esta misma web (el diseño no cambia al corregir un texto)"
    else:
        elegida = aptas[0] if aptas else None
        origen = "elegida por el director: la mejor probada que cubre los caracteres y cumple la rotación"
        if elegida is None:   # el catálogo de tipografías de la familia se agotó para esta racha: se elige la que menos repite y el Gate lo señala
            posibles = sorted((f for f in filas if not f["faltan_caracteres"] and f["probada"]), key=lambda f: (len(f["rotacion"]), -f["orden"]))
            elegida = posibles[0] if posibles else None
            origen = "no hay pareja que cumpla la rotación: se elige la que menos repite; faltan tipografías en el catálogo para esta racha de webs"
    if elegida is None:
        from .generar import FichaIncompleta
        raise FichaIncompleta(f"no hay una pareja tipográfica probada para la personalidad {pers} que cubra el texto y cumpla la rotación")
    # solo cuando la elección es del director (ni fijada en la ficha ni conservada) la composición puede afinarla entre las que cumplen
    candidatas = None
    if clave_ficha == "auto" and previa is None:
        candidatas = aptas if aptas else [f for f in sorted((f for f in filas if not f["faltan_caracteres"] and f["probada"]), key=lambda f: (len(f["rotacion"]), -f["orden"]))][:3]
    return {"clave": elegida["clave"], "origen": origen, "elegida": elegida, "ranking": [{k: v for k, v in f.items() if k != "orden"} for f in filas], "candidatas": candidatas}


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


def decidir(F, origen_activos, ruta_registro, fecha=None, redisenar=False):
    """Decisiones de diseño de una ficha. Devuelve un diccionario serializable y completo (va al manifiesto).
    La tipografía y la composición se eligen y se anotan como reservadas bajo un candado, para que varias webs construyéndose a la vez no repitan.
    Si la web ya estaba en el registro, conserva su diseño (corregir un texto no cambia el diseño aprobado) salvo que se pida rediseñar."""
    import json
    from . import pedido
    est = F["estilo"]
    fam = est["personalidad"]
    fecha = fecha or F.get("confirmacion", {}).get("fecha")
    tonos, de_donde = tonos_de(F)
    texto = json.dumps(F, ensure_ascii=False)
    if pedido.activo(F):
        texto += json.dumps(pedido.textos(F), ensure_ascii=False)
    paleta = resolver_paleta(F, origen_activos, fecha, tonos, _huella.cargar_registro(ruta_registro))
    registros, orden = puntuar_fotos(F, origen_activos)
    cubo = _huella.cubo_de_tono(paleta["tokens"]["brasa"]) if est.get("paleta", "auto") == "auto" else est["paleta"]

    def elegir(registro):
        previo = None if redisenar else registro.get(F["id"])
        tipo = elegir_tipografia(F, texto, registro, tonos, conservar=(previo or {}).get("tipografia"))
        fijados, origen_fijados = {}, {}
        for d in catalogo.DIMENSIONES:
            if est.get(d) not in (None, "auto"):
                fijados[d], origen_fijados[d] = est[d], "fijada en la ficha"
            elif previo and previo.get(d) in catalogo.OPCIONES[d][fam] and catalogo.viable(d, previo[d], F):
                fijados[d], origen_fijados[d] = previo[d], "conservada de la construcción anterior de esta misma web"
        orden_s = est.get("orden") or catalogo.orden_por_defecto(F)
        comp = catalogo.componer(F, registro, tonos, fijados, origen_fijados, tipos=tipo.get("candidatas"), paleta_cubo=cubo, orden=orden_s)
        if tipo.get("candidatas"):
            elegida = next(f for f in tipo["candidatas"] if f["clave"] == comp["elegidas"]["tipografia"])
            tipo = dict(tipo, clave=elegida["clave"], elegida=elegida, origen=tipo["origen"] + "; afinada junto con la composición para distinguirse de las últimas webs")
        el = {d: comp["elegidas"][d] for d in catalogo.DIMENSIONES}
        pack = catalogo.PAQUETES[el["animaciones"]]
        forma = est.get("forma") if est.get("forma") not in (None, "auto") else catalogo.forma_de(comp["rasgos"])
        mov = est.get("movimiento") if est.get("movimiento") not in (None, "auto") else pack["movimiento"]
        est_r = dict(est, familia=fam, paleta=paleta["id"], paleta_cubo=cubo, tipografia=tipo["clave"], forma=forma, movimiento=mov, orden=orden_s, **el)
        return _huella.huella(F, est_r), {"tipo": tipo, "comp": comp, "est_r": est_r, "forma_de": "fijada en la ficha" if est.get("forma") not in (None, "auto") else "por los rasgos del restaurante"}

    h, extra = _huella.reservar(F["id"], ruta_registro, elegir)
    tipo, comp, est_r = extra["tipo"], extra["comp"], extra["est_r"]
    tipo = {k: v for k, v in tipo.items() if k != "candidatas"}
    d = {
        "version_director": VERSION, "fecha_de_referencia": fecha, "tonos": {"lista": tonos, "origen": de_donde},
        "paleta": paleta, "tipografia": tipo,
        "composicion": {"elegidas": {d: comp["elegidas"][d] for d in catalogo.DIMENSIONES}, "motivos": comp["motivos"], "rasgos": comp["rasgos"], "ajustes_por_variedad": comp["ajustes_por_variedad"],
                        "distancia_minima": comp["distancia_minima"], "variedad_limitada": comp["variedad_limitada"],
                        "forma": est_r["forma"], "movimiento": est_r["movimiento"], "orden": est_r["orden"],
                        "animaciones_modulos": catalogo.animaciones_de(comp["elegidas"]["animaciones"]),
                        "paquete": {"nombre": comp["elegidas"]["animaciones"], **{k: v for k, v in catalogo.PAQUETES[comp["elegidas"]["animaciones"]].items() if k != "modulos"}},
                        "ranking": {dim: filas[:4] for dim, filas in comp["ranking"].items() if dim != "tipografia"}},
        "fotos": {"registros": registros, "orden_por_antojo": orden, "usa_el_orden": est.get("orden_fotos") == "antojo",
                  "criterios": {k: {"descripcion": v[0], "peso": v[1]} for k, v in antojo.CRITERIOS.items()},
                  "pesos": {"juicio": antojo.PESO_JUICIO, "tecnica": antojo.PESO_TECNICA}},
        "estilo_resuelto": {k: est_r[k] for k in ("familia", "paleta", "paleta_cubo", "tipografia", "portada", "carta", "galeria", "ornamento", "boton", "densidad", "textura",
                                                   "animaciones", "forma", "movimiento", "orden")},
        "huella": h,
    }
    # la idea que se dibuja: solo si la carta tiene medidas reales
    idea = F.get("idea")
    if idea:
        cat = next(c for c in F["carta"] if c["id"] == idea["categoria"])
        d["idea"] = {"pieza": "regla de medidas", "categoria": idea["categoria"], "unidad": idea["unidad"],
                     "medidas": [p["medida"] for p in cat["platos"] if p.get("medida")], "datos": "medida y precio de cada plato, de la carta de la ficha"}
    return d
