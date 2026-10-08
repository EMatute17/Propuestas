"""Tipografías libres (OFL): registro de parejas, subconjunto WOFF2 y CSS @font-face.

Cada pareja tiene un papel de titular (display) y otro de texto. Se recortan a los caracteres que
una página en español, inglés, francés, italiano o portugués necesita. Las comillas angulares dobles
se dejan fuera a propósito (orden permanente de Eduardo).
"""
import io
import os

from fontTools import subset
from fontTools.ttLib import TTFont

AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.normpath(os.path.join(AQUI, "..", "fuentes"))

# Parejas disponibles. Cada fuente: (archivo, peso CSS, estilo CSS)
PAREJAS = {
    "bodoni-manrope": {
        "familia_display": "Bodoni Moda", "familia_texto": "Manrope",
        "display": [("BodoniModa-DisplayItalic.ttf", 400, "italic")],
        "familia_titulo": "Playfair Display",
        "titulo": [("PlayfairDisplay-Regular.ttf", 400, "normal")],
        "texto": [("Manrope-Regular.ttf", 400, "normal"), ("Manrope-SemiBold.ttf", 600, "normal"), ("Manrope-Bold.ttf", 700, "normal")],
        "respaldo_display": "Didot, 'Bodoni 72', 'Times New Roman', Georgia, serif",
        "respaldo_texto": "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
        "caracter": "elegante",
        "licencias": ["OFL_bodonimoda.txt", "OFL_playfairdisplay.txt", "OFL_manrope.txt"],
    },
    "playfair-inter": {
        "familia_display": "Playfair Display", "familia_texto": "Inter",
        "display": [("PlayfairDisplay-BoldItalic.ttf", 700, "italic"), ("PlayfairDisplay-Regular.ttf", 400, "normal")],
        "texto": [("Inter-Regular.ttf", 400, "normal"), ("Inter-SemiBold.ttf", 600, "normal")],
        "respaldo_display": "Georgia, 'Times New Roman', serif",
        "respaldo_texto": "system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif",
        "caracter": "elegante",
        "licencias": ["OFL_playfairdisplay.txt", "OFL_inter.txt"],
    },
    "anton-archivo": {
        "familia_display": "Anton", "familia_texto": "Archivo",
        "display": [("Anton-Regular.ttf", 400, "normal")],
        "texto": [("Archivo-Medium.ttf", 500, "normal"), ("Archivo-Bold.ttf", 700, "normal")],
        "respaldo_display": "Impact, 'Arial Narrow Bold', 'Haettenschweiler', sans-serif",
        "respaldo_texto": "system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif",
        "caracter": "casual",
        "licencias": ["OFL_anton.txt", "OFL_archivo.txt"],
    },
}


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
    return sorted({c for c in texto if ord(c) > 0x20 and ord(c) not in cmap})
