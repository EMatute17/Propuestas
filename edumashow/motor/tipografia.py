"""Tipografías libres (OFL): registro de parejas, subconjunto WOFF2 y CSS @font-face.

Cada pareja tiene un papel de titular (display) y otro de texto. Se recortan a los caracteres que
una página en español, inglés, francés, italiano o portugués necesita. Las comillas angulares dobles
se dejan fuera a propósito (orden permanente de Eduardo).
"""
import io
import json
import os

from fontTools import subset
from fontTools.ttLib import TTFont

AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.normpath(os.path.join(AQUI, "..", "fuentes"))

# Parejas disponibles. Cada fuente: (archivo, peso CSS, estilo CSS). El titular (display) se declara siempre con peso 400:
# la web lo pide así, y así el navegador nunca le inventa una negrita. El texto lleva sus pesos reales.
# clase: la clase tipográfica del titular (expandida, condensada, serif, grotesca o geometrica), la que cuenta la rotación.
# tonos: para qué carácter de restaurante encaja. personalidades: en cuáles se puede usar. Que una pareja esté probada
# (ya pasó el Gate en esa personalidad) lo dice gate/parejas_probadas.json, que escribe el propio Gate: el director de estilo
# solo propone parejas probadas.
SANS = "system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif"
PAREJAS = {
    "bodoni-manrope": {
        "familia_display": "Bodoni Moda", "familia_texto": "Manrope",
        "display": [("BodoniModa-DisplayItalic.ttf", 400, "italic")],
        "familia_titulo": "Playfair Display",
        "titulo": [("PlayfairDisplay-Regular.ttf", 400, "normal")],
        "texto": [("Manrope-Regular.ttf", 400, "normal"), ("Manrope-SemiBold.ttf", 600, "normal"), ("Manrope-Bold.ttf", 700, "normal")],
        "respaldo_display": "Didot, 'Bodoni 72', 'Times New Roman', Georgia, serif", "respaldo_texto": SANS,
        "caracter": "elegante", "clase": "serif", "tonos": ["elegante", "premium", "autor", "calido", "brasa"], "personalidades": ["elegante"],
        "licencias": ["OFL_bodonimoda.txt", "OFL_playfairdisplay.txt", "OFL_manrope.txt"],
    },
    "playfair-inter": {
        "familia_display": "Playfair Display", "familia_texto": "Inter",
        "display": [("PlayfairDisplay-BoldItalic.ttf", 400, "italic"), ("PlayfairDisplay-Regular.ttf", 400, "normal")],
        "texto": [("Inter-Regular.ttf", 400, "normal"), ("Inter-SemiBold.ttf", 600, "normal")],
        "respaldo_display": "Georgia, 'Times New Roman', serif", "respaldo_texto": SANS,
        "caracter": "elegante", "clase": "serif", "tonos": ["elegante", "clasico", "premium", "brunch", "alta-cocina"], "personalidades": ["elegante"],
        "licencias": ["OFL_playfairdisplay.txt", "OFL_inter.txt"],
    },
    "instrument-inter": {
        "familia_display": "Instrument Serif", "familia_texto": "Inter",
        "display": [("InstrumentSerif-Italic.ttf", 400, "italic")],
        "familia_titulo": "Instrument Serif", "titulo": [("InstrumentSerif-Regular.ttf", 400, "normal")],
        "texto": [("Inter-Regular.ttf", 400, "normal"), ("Inter-SemiBold.ttf", 600, "normal"), ("Inter-Bold.ttf", 700, "normal")],
        "respaldo_display": "Georgia, 'Times New Roman', serif", "respaldo_texto": SANS,
        "caracter": "elegante", "clase": "serif", "tonos": ["contemporaneo", "autor", "elegante", "minimal"], "personalidades": ["elegante"],
        "licencias": ["OFL_instrumentserif.txt", "OFL_inter.txt"],
    },
    "dmserif-inter": {
        "familia_display": "DM Serif Display", "familia_texto": "Inter",
        "display": [("DMSerifDisplay-Italic.ttf", 400, "italic")],
        "familia_titulo": "DM Serif Display", "titulo": [("DMSerifDisplay-Regular.ttf", 400, "normal")],
        "texto": [("Inter-Regular.ttf", 400, "normal"), ("Inter-SemiBold.ttf", 600, "normal"), ("Inter-Bold.ttf", 700, "normal")],
        "respaldo_display": "Georgia, 'Times New Roman', serif", "respaldo_texto": SANS,
        "caracter": "elegante", "clase": "serif", "tonos": ["clasico", "italiana", "trattoria", "calido", "tradicion"], "personalidades": ["elegante"],
        "licencias": ["OFL_dmserifdisplay.txt", "OFL_inter.txt"],
    },
    "fraunces-manrope": {
        "familia_display": "Fraunces", "familia_texto": "Manrope",
        "display": [("Fraunces-DisplayItalic.ttf", 400, "italic")],
        "familia_titulo": "Fraunces Soft", "titulo": [("Fraunces-DisplaySoft.ttf", 400, "normal")],
        "texto": [("Manrope-Regular.ttf", 400, "normal"), ("Manrope-SemiBold.ttf", 600, "normal"), ("Manrope-Bold.ttf", 700, "normal")],
        "respaldo_display": "Georgia, 'Times New Roman', serif", "respaldo_texto": SANS,
        "caracter": "elegante", "clase": "serif", "tonos": ["calido", "autor", "tradicion", "artesanal", "panaderia"], "personalidades": ["elegante"],
        "licencias": ["OFL_fraunces.txt", "OFL_manrope.txt"],
    },
    "bodoni-outfit": {
        "familia_display": "Bodoni Moda", "familia_texto": "Outfit",
        "display": [("BodoniModa-DisplayItalic.ttf", 400, "italic")],
        "familia_titulo": "Bodoni Moda Regular", "titulo": [("BodoniModa-DisplayRegular.ttf", 400, "normal")],
        "texto": [("Outfit-Regular.ttf", 400, "normal"), ("Outfit-SemiBold.ttf", 600, "normal"), ("Outfit-Bold.ttf", 700, "normal")],
        "respaldo_display": "Didot, 'Bodoni 72', 'Times New Roman', Georgia, serif", "respaldo_texto": SANS,
        "caracter": "elegante", "clase": "serif", "tonos": ["lujo", "dulce", "pasteleria", "premium", "elegante"], "personalidades": ["elegante"],
        "licencias": ["OFL_bodonimoda.txt", "OFL_outfit.txt"],
    },
    "anton-archivo": {
        "familia_display": "Anton", "familia_texto": "Archivo",
        "display": [("Anton-Regular.ttf", 400, "normal")],
        "texto": [("Archivo-Medium.ttf", 500, "normal"), ("Archivo-Bold.ttf", 700, "normal")],
        "respaldo_display": "Impact, 'Arial Narrow Bold', 'Haettenschweiler', sans-serif", "respaldo_texto": SANS,
        "caracter": "casual", "clase": "condensada", "tonos": ["callejero", "potente", "parrilla", "urbano", "hamburguesa"], "personalidades": ["urbano"],
        "licencias": ["OFL_anton.txt", "OFL_archivo.txt"],
    },
    "archivo-condensado-inter": {
        "familia_display": "Archivo Condensed", "familia_texto": "Inter",
        "display": [("Archivo-CondensedBlack.ttf", 400, "normal")],
        "texto": [("Inter-Medium.ttf", 500, "normal"), ("Inter-Bold.ttf", 700, "normal")],
        "respaldo_display": "'Arial Narrow', Impact, sans-serif", "respaldo_texto": SANS,
        "caracter": "casual", "clase": "condensada", "tonos": ["urbano", "joven", "moderno", "potente", "parrilla"], "personalidades": ["urbano"],
        "licencias": ["OFL_archivo.txt", "OFL_inter.txt"],
    },
    "bebas-manrope": {
        "familia_display": "Bebas Neue", "familia_texto": "Manrope",
        "display": [("BebasNeue-Regular.ttf", 400, "normal")],
        "texto": [("Manrope-Medium.ttf", 500, "normal"), ("Manrope-Bold.ttf", 700, "normal")],
        "respaldo_display": "Impact, 'Arial Narrow Bold', sans-serif", "respaldo_texto": SANS,
        "caracter": "casual", "clase": "condensada", "tonos": ["cartel", "potente", "callejero", "urbano", "impacto"], "personalidades": ["urbano"],
        "licencias": ["OFL_bebasneue.txt", "OFL_manrope.txt"],
    },
    "archivo-expandido": {
        "familia_display": "Archivo Expanded", "familia_texto": "Archivo",
        "display": [("Archivo-ExpandedBlack.ttf", 400, "normal")],
        "texto": [("Archivo-Medium.ttf", 500, "normal"), ("Archivo-Bold.ttf", 700, "normal")],
        "respaldo_display": "Arial, 'Helvetica Neue', sans-serif", "respaldo_texto": SANS,
        "caracter": "casual", "clase": "expandida", "tonos": ["expresivo", "pop", "joven", "urbano", "festivo"], "personalidades": ["urbano"],
        "licencias": ["OFL_archivo.txt"],
    },
    "unbounded-manrope": {
        "familia_display": "Unbounded", "familia_texto": "Manrope",
        "display": [("Unbounded-Black.ttf", 400, "normal")],
        "texto": [("Manrope-Medium.ttf", 500, "normal"), ("Manrope-Bold.ttf", 700, "normal")],
        "respaldo_display": "Arial, 'Helvetica Neue', sans-serif", "respaldo_texto": SANS,
        "caracter": "casual", "clase": "expandida", "tonos": ["tendencia", "joven", "pop", "festivo"], "personalidades": ["urbano"],
        "licencias": ["OFL_unbounded.txt", "OFL_manrope.txt"],
    },
    "bricolage-outfit": {
        "familia_display": "Bricolage Grotesque", "familia_texto": "Outfit",
        "display": [("Bricolage-DisplayExtraBold.ttf", 400, "normal")],
        "texto": [("Outfit-Regular.ttf", 400, "normal"), ("Outfit-SemiBold.ttf", 600, "normal"), ("Outfit-Bold.ttf", 700, "normal")],
        "respaldo_display": "Arial, 'Helvetica Neue', sans-serif", "respaldo_texto": SANS,
        "caracter": "casual", "clase": "grotesca", "tonos": ["fresco", "saludable", "moderno", "amable", "joven"], "personalidades": ["urbano"],
        "licencias": ["OFL_bricolagegrotesque.txt", "OFL_outfit.txt"],
    },
    "outfit-outfit": {
        "familia_display": "Outfit", "familia_texto": "Outfit",
        "display": [("Outfit-Black.ttf", 400, "normal")],
        "texto": [("Outfit-Regular.ttf", 400, "normal"), ("Outfit-SemiBold.ttf", 600, "normal"), ("Outfit-Bold.ttf", 700, "normal")],
        "respaldo_display": "Arial, 'Helvetica Neue', sans-serif", "respaldo_texto": SANS,
        "caracter": "casual", "clase": "geometrica", "tonos": ["amable", "familiar", "fresco", "casual"], "personalidades": ["urbano"],
        "licencias": ["OFL_outfit.txt"],
    },
}

# clase tipográfica de cada fuente de titular que el kit reconoce (para la rotación)
CLASES = {"expandida": ("Syne", "Archivo Expanded", "Unbounded"), "condensada": ("Anton", "Bebas Neue", "Archivo Condensed", "Bricolage Condensed"),
          "serif": ("Bodoni Moda", "Playfair Display", "Fraunces", "DM Serif Display", "Instrument Serif"),
          "grotesca": ("Archivo Black", "Inter Display", "Space Grotesk", "Bricolage Grotesque"), "geometrica": ("Outfit", "Manrope")}


RUTA_PROBADAS = os.path.normpath(os.path.join(AQUI, "..", "gate", "parejas_probadas.json"))


def probadas():
    """Parejas que ya pasaron el Gate: {clave: {personalidad: {fecha, sitio, modo, veredicto}}}."""
    if os.path.exists(RUTA_PROBADAS):
        with open(RUTA_PROBADAS, encoding="utf-8") as f:
            return json.load(f)
    return {}


def esta_probada(clave, personalidad):
    return personalidad in probadas().get(clave, {})


def clase(clave):
    return PAREJAS[clave]["clase"]


def display_de(clave):
    return PAREJAS[clave]["familia_display"]


_ANCHOS = {}


def ancho_em(clave):
    """Ancho medio de una mayúscula del titular, en em (las mayúsculas deciden cuánto cabe en una línea de cartel)."""
    if clave not in _ANCHOS:
        t = TTFont(os.path.join(CARPETA, PAREJAS[clave]["display"][0][0]))
        cm, hm, upm = t.getBestCmap(), t["hmtx"], t["head"].unitsPerEm
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        _ANCHOS[clave] = round(sum(hm[cm[ord(c)]][0] for c in letras) / len(letras) / upm, 3)
    return _ANCHOS[clave]


def faltantes(clave, texto):
    """Caracteres del texto que alguna de las fuentes de la pareja no tiene."""
    p = PAREJAS[clave]
    falta = set()
    for rol in ("display", "titulo", "texto"):
        for archivo, _, _ in p.get(rol, []):
            falta |= set(glifos_faltantes(archivo, texto))
    return sorted(falta)


def unicodes_base():
    """Conjunto de caracteres recortado. Se construye con números, sin escribir las comillas angulares."""
    u = set(range(0x20, 0x7F))
    u |= set(range(0xA0, 0x100))
    u |= set(range(0x100, 0x180))
    u -= {0xAB, 0xBB}
    u |= {0x2013, 0x2014, 0x2018, 0x2019, 0x201A, 0x201C, 0x201D, 0x201E, 0x2022, 0x2026,
          0x20AC, 0x2192, 0x2212, 0x00D7}
    return sorted(u)


def subconjunto_woff2(archivo_ttf, destino):
    """Recorta una fuente a unicodes_base() y la guarda como WOFF2. Devuelve el tamaño en bytes."""
    ruta = os.path.join(CARPETA, archivo_ttf)
    opt = subset.Options()
    opt.flavor = "woff2"
    opt.layout_features = ["kern", "liga", "calt", "ccmp", "locl", "mark", "mkmk", "tnum", "lnum", "onum", "case"]
    opt.hinting = False
    opt.desubroutinize = True
    opt.name_IDs = [1, 2, 3, 4, 6]
    opt.notdef_outline = True
    opt.drop_tables += ["DSIG"]
    fuente = subset.load_font(ruta, opt)
    sub = subset.Subsetter(opt)
    sub.populate(unicodes=unicodes_base())
    sub.subset(fuente)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    subset.save_font(fuente, destino, opt)
    return os.path.getsize(destino)


def preparar_pareja(clave, carpeta_fuentes, ruta_relativa="assets/fonts"):
    """Genera los WOFF2 de una pareja y devuelve el CSS @font-face y los datos para precargar."""
    p = PAREJAS[clave]
    css = []
    precarga = []
    lic = []
    roles = [("display", p["familia_display"])]
    if p.get("titulo"):
        roles.append(("titulo", p["familia_titulo"]))
    roles.append(("texto", p["familia_texto"]))
    for rol, familia in roles:
        for archivo, peso, estilo in p[rol]:
            nombre = archivo.replace(".ttf", ".woff2").lower()
            subconjunto_woff2(archivo, os.path.join(carpeta_fuentes, nombre))
            css.append(
                f"@font-face{{font-family:'{familia}';font-style:{estilo};font-weight:{peso};font-display:swap;"
                f"src:url({ruta_relativa}/{nombre}) format('woff2')}}"
            )
            precarga.append({"rol": rol, "archivo": f"{ruta_relativa}/{nombre}", "peso": peso, "estilo": estilo})
    for t in p["licencias"]:
        origen = os.path.join(CARPETA, "licencias", t)
        if os.path.exists(origen):
            lic.append(t)
    return {"css": "\n".join(css), "precarga": precarga, "licencias": lic, "pareja": p}


def glifos_faltantes(archivo_ttf, texto):
    """Caracteres del texto que la fuente no tiene (comprobación previa a la entrega)."""
    f = TTFont(os.path.join(CARPETA, archivo_ttf))
    cmap = f.getBestCmap()
    servidos = set(unicodes_base())    # la fuente se recorta a este conjunto: lo que quede fuera se vería con la fuente del sistema
    return sorted({c for c in texto if ord(c) > 0x20 and (ord(c) not in cmap or ord(c) not in servidos)})
