"""Color para la web: OKLCH, colores dominantes del logo y paleta de marca con acento de temporada.

Método (Documento Maestro, sección 6.2, traducido a una web y escrito de nuevo para este proyecto):
  1. El color de identidad de la marca manda: se saca del logo (los neutros no cuentan como identidad).
  2. De los colores clave de la temporada vigente (WGSN x Coloro) se separan neutros y cromáticos.
  3. El acento de temporada es el cromático con mejor relación de tono con la marca (análogo o complementario, nunca la
     zona de choque) y más unidad (luminosidad y croma parecidos); se afina un poco hacia la marca.
  4. Los fondos salen de los neutros de la temporada (claro: Wax Paper; oscuro: Cocoa Powder o Deep Green) teñidos hacia la marca.
  5. Proporción 60 / 30 / 10: fondo, color de marca, acento de temporada.
  6. Todo par de colores que se usa para leer cumple 4,5 a 1 (3 a 1 el texto grande y los anillos de foco): los tonos se
     ajustan solos hasta lograrlo, y el Gate lo comprueba otra vez sobre los colores finales (G-PALETA).

Los hex de WGSN son aproximaciones digitales no oficiales calculadas desde los códigos Coloro publicados."""
import datetime as _dt
import math

import numpy as np
from PIL import Image

# ------------------------------------------------------------------ espacios de color (fórmulas publicadas de OKLab y sRGB)
def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_hex(rgb):
    return "#" + "".join(f"{int(round(max(0, min(255, v)))):02x}" for v in rgb)


def _lin(c):
    c = np.asarray(c, dtype=np.float64)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _delin(c):
    c = np.asarray(c, dtype=np.float64)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(np.clip(c, 0, None), 1 / 2.4) - 0.055)


def rgb_oklab(rgb):
    """rgb en 0 a 255 (o un arreglo N x 3) a OKLab."""
    c = _lin(np.asarray(rgb, dtype=np.float64) / 255.0)
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    l = np.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    m = np.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    s = np.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)
    return np.stack([0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
                     1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
                     0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s], axis=-1)


def _oklab_lineal(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def oklch(color):
    """(L, C, h) de un hex o de un rgb. h en grados."""
    rgb = hex_rgb(color) if isinstance(color, str) else color
    L, a, b = rgb_oklab(rgb)
    return float(L), float(math.hypot(a, b)), float(math.degrees(math.atan2(b, a)) % 360)


def desde_oklch(L, C, h):
    """Hex de un color OKLCH. Si no cabe en sRGB se baja el croma hasta que quepa (la luminosidad y el tono se conservan)."""
    for k in range(48):
        c = C * (1 - k / 48)
        r, g, b = _oklab_lineal(L, c * math.cos(math.radians(h)), c * math.sin(math.radians(h)))
        if min(r, g, b) >= -1e-4 and max(r, g, b) <= 1 + 1e-4:
            return rgb_hex(_delin(np.array([r, g, b])) * 255)
    return rgb_hex(_delin(np.array(_oklab_lineal(L, 0, 0))) * 255)


def luminancia(color):
    c = _lin(np.asarray(hex_rgb(color) if isinstance(color, str) else color, dtype=np.float64) / 255.0)
    return float(0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def mezcla_tono(h1, h2, w2):
    """Tono intermedio entre h1 y h2 (por el camino corto); w2 es el peso de h2 de 0 a 1."""
    d = ((h2 - h1 + 180) % 360) - 180
    return (h1 + d * w2) % 360


def distancia_tono(h1, h2):
    d = abs(h1 - h2) % 360
    return min(d, 360 - d)


# ------------------------------------------------------------------ colores dominantes de un logo
def colores_dominantes(imagen, k=6, semilla=7):
    """K-means en OKLab sobre los píxeles opacos de un logo. Devuelve los grupos ordenados por peso:
    [{hex, peso, L, C, h, neutro}]. Es determinista (semilla fija)."""
    im = imagen.convert("RGBA") if isinstance(imagen, Image.Image) else Image.open(imagen).convert("RGBA")
    im.thumbnail((220, 220))
    a = np.asarray(im).reshape(-1, 4)
    a = a[a[:, 3] > 128][:, :3]
    if len(a) < 20:
        return []
    lab = rgb_oklab(a)
    rng = np.random.default_rng(semilla)
    k = min(k, len(lab))
    # k-means++: cada centro nuevo se elige lejos de los anteriores
    c = [lab[rng.integers(len(lab))]]
    for _ in range(1, k):
        d2 = np.min(((lab[:, None, :] - np.array(c)[None]) ** 2).sum(-1), axis=1)
        suma = d2.sum()
        if suma <= 1e-12:        # un logo de pocos colores: ya no quedan colores distintos de los elegidos
            break
        c.append(lab[rng.choice(len(lab), p=d2 / suma)])
    k = len(c)
    cent = np.array(c)
    for _ in range(30):
        asign = ((lab[:, None, :] - cent[None]) ** 2).sum(-1).argmin(1)
        nuevo = np.array([lab[asign == i].mean(0) if (asign == i).any() else cent[i] for i in range(k)])
        if np.allclose(nuevo, cent, atol=1e-5):
            break
        cent = nuevo
    pesos = np.bincount(asign, minlength=k) / len(lab)
    out = []
    for i in np.argsort(-pesos):
        L, A, B = cent[i]
        C, h = math.hypot(A, B), math.degrees(math.atan2(B, A)) % 360
        hexc = desde_oklch(float(L), float(C), float(h))
        out.append({"hex": hexc, "peso": round(float(pesos[i]), 4), "L": round(float(L), 3), "C": round(float(C), 3), "h": round(float(h), 1), "neutro": bool(C < 0.04)})
    return out


def color_de_marca(dominantes):
    """El color de identidad: el cromático con más presencia y viveza (peso por croma). Si el logo es todo neutro, el más claro u oscuro con peso."""
    # la identidad es un color vivo: ni un fondo casi negro, ni uno casi blanco, ni uno apagado
    vivos = [d for d in dominantes if not d["neutro"] and d["peso"] >= 0.02 and 0.30 <= d["L"] <= 0.92 and d["C"] >= 0.06]
    if vivos:
        return max(vivos, key=lambda d: d["peso"] * (0.4 + d["C"]))
    cromaticos = [d for d in dominantes if not d["neutro"] and d["peso"] >= 0.02]
    if cromaticos:
        return max(cromaticos, key=lambda d: d["peso"] * (0.4 + d["C"]))
    return dominantes[0] if dominantes else None


# ------------------------------------------------------------------ temporadas WGSN x Coloro (anuncios públicos; hex aproximados, no oficiales)
TEMPORADAS = {
    "AW26/27": {"desde": "2026-07-01", "hasta": "2026-12-31", "fuente": "WGSN x Coloro, 12-09-2024",
                "colores": [("Transformative Teal", "#016168"), ("Wax Paper", "#ECDCAF"), ("Fresh Purple", "#712892"),
                            ("Cocoa Powder", "#664C4D"), ("Green Glow", "#9EDE69")]},
    "SS27": {"desde": "2027-01-01", "hasta": "2027-06-30", "fuente": "WGSN x Coloro, 29-04-2025",
             "colores": [("Luminous Blue", "#044280"), ("Energy Orange", "#D86925"), ("Pop Pink", "#F097D0"),
                         ("Meadowland Green", "#839C59"), ("Clay", "#BE827A")]},
    "AW27/28": {"desde": "2027-07-01", "hasta": "2028-02-28", "fuente": "WGSN x Coloro, 17-09-2025",
                "colores": [("Russet", "#852225"), ("Peaceful Lilac", "#D0B9DE"), ("Maize", "#B89B49"), ("Deep Green", "#005049")]},
}
WAX_PAPER, COCOA_POWDER, DEEP_GREEN = "#ECDCAF", "#664C4D", "#005049"   # neutros de los que salen los fondos


def temporada_vigente(fecha=None):
    f = fecha or _dt.date.today().isoformat()
    for k, v in TEMPORADAS.items():
        if v["desde"] <= f <= v["hasta"]:
            return k
    return "AW26/27" if f < "2026-07-01" else max(TEMPORADAS, key=lambda k: TEMPORADAS[k]["hasta"])


def _relacion_tono(dh, croma_marca):
    """1 si el tono del acento es análogo o complementario del de la marca; casi 0 en la zona de choque (60 a 120 grados)."""
    if croma_marca < 0.04:
        return 0.8                      # marca sin color propio: cualquier tono convive
    if dh <= 40:
        return 1.0 - dh / 90
    if dh >= 150:
        return 1.0 - (180 - dh) / 70
    return 0.15


def elegir_acento(marca, fecha=None, variante=0, evitar=()):
    """Acento de temporada para una marca. Devuelve (color_afinado, reporte). `variante` 0, 1 o 2 da alternativas."""
    temporada = temporada_vigente(fecha)
    Lm, Cm, hm = oklch(marca)
    cromaticos, neutros = [], []
    for nombre, hexc in TEMPORADAS[temporada]["colores"]:
        L, C, h = oklch(hexc)
        (cromaticos if C >= 0.07 else neutros).append((nombre, hexc, L, C, h))
    puntos = []
    for nombre, hexc, L, C, h in cromaticos:
        dh = distancia_tono(h, hm)
        relacion = _relacion_tono(dh, Cm)
        unidad = 1.0 - min(1.0, abs(L - Lm) / 0.35) * 0.5 - min(1.0, abs(C - Cm) / 0.15) * 0.5
        redundante = 0.35 if (dh < 15 and abs(L - Lm) < 0.08) else 0.0
        repetido = 0.6 if any(distancia_tono(h, oklch(e)[2]) < 18 for e in evitar) else 0.0
        puntos.append({"nombre": nombre, "hex": hexc, "relacion": round(relacion, 2), "unidad": round(unidad, 2),
                       "puntos": round(0.55 * relacion + 0.45 * unidad - redundante - repetido, 3), "dh": round(dh, 1), "L": L, "C": C, "h": h})
    puntos.sort(key=lambda p: -p["puntos"])
    e = puntos[min(variante, len(puntos) - 1)]
    # se afina hacia la marca: un tercio del camino en luminosidad y croma, el tono no cambia
    afinado = desde_oklch(e["L"] + (Lm - e["L"]) * 0.35, e["C"] + (Cm - e["C"]) * 0.35, e["h"])
    rep = {"temporada": temporada, "fuente": TEMPORADAS[temporada]["fuente"], "elegido": f'{e["nombre"]} ({e["hex"]})', "afinado": afinado,
           "alternativas": [{k: p[k] for k in ("nombre", "hex", "relacion", "unidad", "puntos", "dh")} for p in puntos],
           "neutros_de_temporada": [f"{n} ({x})" for n, x, *_ in neutros]}
    return afinado, rep


# ------------------------------------------------------------------ ajuste de contraste
def _con_luminosidad(color, L):
    _, C, h = oklch(color)
    return desde_oklch(L, C, h)


def ajustar_contra(color, fondos, minimo, subir=None):
    """Mueve la luminosidad de `color` (tono y croma intactos) hasta que cumpla `minimo` contra todos los fondos.
    subir=True aclara, False oscurece; por defecto va hacia el lado contrario de la luminosidad de los fondos."""
    L, C, h = oklch(color)
    fondos = [fondos] if isinstance(fondos, str) else list(fondos)
    if subir is None:
        subir = np.mean([oklch(f)[0] for f in fondos]) < 0.5
    paso = 0.004 if subir else -0.004
    cur = desde_oklch(L, C, h)
    for _ in range(260):
        if all(contraste(cur, f) >= minimo for f in fondos):
            return cur
        L = min(1.0, max(0.0, L + paso))
        cur = desde_oklch(L, C, h)
    return cur


def tinta_sobre(fondo, claro, oscuro, minimo=4.5):
    """El texto (claro u oscuro) que se lee mejor sobre `fondo`; si ninguno llega al mínimo, el mejor de los dos."""
    return claro if contraste(claro, fondo) >= contraste(oscuro, fondo) else oscuro


# ------------------------------------------------------------------ paleta completa de una web
def paleta_marca(color_marca, fecha=None, variante=0, evitar=(), con_acento=True):
    """Todos los colores de diseño de una web a partir del color de identidad. Devuelve (tokens, reporte).
    Los tokens usan los mismos nombres que las paletas hechas a mano de temas.py, más `acento` y `acento-papel`."""
    Lm, Cm, hm = oklch(color_marca)
    cromatica = Cm >= 0.04
    wax, cocoa, deep = oklch(WAX_PAPER), oklch(COCOA_POWDER), oklch(DEEP_GREEN)
    # tono de los fondos: el de la marca si es cálido o neutro; si la marca es fría, el de la temporada (los fondos fríos restan apetito)
    fria = 150 <= hm <= 320
    h_claro = wax[2] if (not cromatica or fria) else mezcla_tono(wax[2], hm, 0.5)
    base_oscura = (deep[2] if 120 <= hm <= 260 else cocoa[2]) if cromatica else cocoa[2]
    h_oscuro = base_oscura if (not cromatica or fria) else mezcla_tono(base_oscura, hm, 0.5)
    t = {}
    # fondos oscuros (más oscuros que el 'oscuro WGSN': la web se lee de noche y sobre fotos) y claros
    t["tinta"] = desde_oklch(0.145, 0.014, h_oscuro)
    t["tinta-2"] = desde_oklch(0.178, 0.016, h_oscuro)
    t["tinta-3"] = desde_oklch(0.215, 0.018, h_oscuro)
    t["crema"] = desde_oklch(0.962, 0.014, h_claro)
    t["crema-2"] = ajustar_contra(desde_oklch(0.86, 0.02, h_claro), [t["tinta"], t["tinta-2"], t["tinta-3"]], 7.0, True)
    t["papel"] = desde_oklch(0.962, 0.016, h_claro)
    t["papel-2"] = desde_oklch(0.925, 0.024, h_claro)
    # el color de marca como superficie (botones, barras) y sus compañeros
    # el color de un logo es un promedio con sombras: en pantalla, sobre fondo oscuro, el color de marca tiene que leerse como luz,
    # así que se aclara un poco y se aviva su croma (el tono no cambia)
    Lb = min(0.80, max(0.68, Lm + 0.05))
    Cb = min(0.22, max(0.12, Cm * 1.2)) if cromatica else 0.0
    brasa = desde_oklch(Lb, Cb, hm)
    t["sobre-brasa"] = tinta_sobre(brasa, t["crema"], t["tinta"])
    if contraste(t["sobre-brasa"], brasa) < 4.5:                       # ningún texto llega: se mueve el color de marca
        brasa = ajustar_contra(brasa, t["sobre-brasa"], 4.6, t["sobre-brasa"] == t["tinta"])   # texto oscuro: se aclara la marca; texto claro: se oscurece
    t["brasa"] = brasa
    h2 = hm + (18 if 0 <= hm <= 100 or hm >= 340 else -18)
    t["brasa-2"] = ajustar_contra(desde_oklch(min(0.86, Lb + 0.06), max(0.08, Cb - 0.03), h2), [t["tinta"], t["tinta-2"], t["tinta-3"]], 7.0, True)
    t["brasa-papel"] = ajustar_contra(desde_oklch(0.5, max(0.1, Cb - 0.02), hm), [t["papel"], t["papel-2"]], 5.0, False)
    # textos apagados
    t["bruma"] = ajustar_contra(desde_oklch(0.7, 0.02, h_oscuro), [t["tinta"], t["tinta-2"], t["tinta-3"]], 6.0, True)
    t["bruma-papel"] = ajustar_contra(desde_oklch(0.46, 0.02, h_oscuro), [t["papel"], t["papel-2"]], 5.5, False)
    t["texto-suave-papel"] = ajustar_contra(desde_oklch(0.36, 0.02, h_oscuro), [t["papel"], t["papel-2"]], 8.0, False)
    t["aviso"] = ajustar_contra(desde_oklch(0.4, 0.14, 32), [t["papel"], t["papel-2"]], 6.5, False)
    # anillos de foco (3 a 1 como mínimo) y campos de formulario
    t["foco-anillo"] = t["brasa-2"]
    t["foco-anillo-claro"] = t["brasa-2"]
    t["foco-anillo-papel"] = ajustar_contra(desde_oklch(0.42, max(0.1, Cb - 0.05), hm), [t["papel"], t["papel-2"]], 6.0, False)
    t["fondo-campo"] = "#ffffff"
    r, g, b = hex_rgb(t["tinta"])
    t["borde-campo"] = f"rgba({r},{g},{b},.4)"
    t["texto-campo"] = t["tinta"]
    # acento de temporada (el 10 %): una versión para fondo oscuro y otra para papel
    rep_acento = None
    if con_acento:
        acento, rep_acento = elegir_acento(brasa, fecha, variante, evitar)
        _, Ca, ha = oklch(acento)
        t["acento"] = ajustar_contra(desde_oklch(0.78, max(0.08, Ca), ha), [t["tinta"], t["tinta-2"], t["tinta-3"]], 7.0, True)
        t["acento-papel"] = ajustar_contra(desde_oklch(0.42, max(0.08, Ca), ha), [t["papel"], t["papel-2"]], 6.0, False)
    else:
        t["acento"], t["acento-papel"] = t["brasa-2"], t["brasa-papel"]
    t["meta-color"] = t["tinta"]
    reporte = {
        "color_de_marca": color_marca, "marca_oklch": [round(Lm, 3), round(Cm, 3), round(hm, 1)], "marca_cromatica": cromatica,
        "fondos": {"claro_desde": f"Wax Paper ({WAX_PAPER}) teñido hacia el tono {h_claro:.0f}", "oscuro_desde": f"{'Deep Green' if 120 <= hm <= 260 and cromatica else 'Cocoa Powder'} teñido hacia el tono {h_oscuro:.0f}"},
        "proporcion": "60 % fondo, 30 % color de marca, 10 % acento de temporada",
        "acento": rep_acento, "variante": variante,
        "nota": "Los hex de WGSN son aproximaciones digitales no oficiales de los códigos Coloro publicados.",
    }
    reporte["pares"] = pares_de_contraste(t)
    return t, reporte


# pares (texto, fondo, mínimo) con los que la web lee. Se usan igual aquí y en el Gate (G-PALETA).
PARES = [
    ("crema", "tinta", 4.5), ("crema", "tinta-2", 4.5), ("crema", "tinta-3", 4.5), ("crema-2", "tinta", 4.5), ("crema-2", "tinta-2", 4.5), ("crema-2", "tinta-3", 4.5),
    ("bruma", "tinta", 4.5), ("bruma", "tinta-2", 4.5), ("bruma", "tinta-3", 4.5), ("brasa", "tinta", 3.0), ("brasa-2", "tinta", 4.5), ("brasa-2", "tinta-2", 4.5), ("brasa-2", "tinta-3", 4.5),
    ("sobre-brasa", "brasa", 4.5), ("sobre-brasa", "brasa-2", 4.5),
    ("tinta", "papel", 4.5), ("tinta", "papel-2", 4.5), ("brasa-papel", "papel", 4.5), ("brasa-papel", "papel-2", 4.5),
    ("texto-suave-papel", "papel", 4.5), ("texto-suave-papel", "papel-2", 4.5), ("bruma-papel", "papel", 4.5), ("bruma-papel", "papel-2", 4.5),
    ("aviso", "papel", 4.5), ("aviso", "papel-2", 4.5),
    ("foco-anillo", "tinta", 3.0), ("foco-anillo-papel", "papel", 3.0), ("foco-anillo-papel", "papel-2", 3.0),
    ("acento", "tinta", 4.5), ("acento", "tinta-2", 4.5), ("acento", "tinta-3", 4.5), ("acento-papel", "papel", 4.5), ("acento-papel", "papel-2", 4.5),
]


def pares_de_contraste(tokens):
    filas = []
    for fg, bg, minimo in PARES:
        if fg in tokens and bg in tokens:
            c = contraste(tokens[fg], tokens[bg])
            filas.append({"texto": fg, "fondo": bg, "contraste": round(c, 2), "minimo": minimo, "ok": c >= minimo})
    return filas
