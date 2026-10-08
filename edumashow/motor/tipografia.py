"""Tipografías libres (OFL): registro de parejas, subconjunto WOFF2 y CSS @font-face.

Cada pareja tiene un papel de titular (display) y otro de texto. Se recortan a los caracteres que
una página en español, inglés, francés, italiano o portugués necesita. Las comillas angulares dobles
se dejan fuera a propósito (orden permanente de Eduardo).
"""
import io
import json
import os
import shutil

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
        "caracter": "elegante", "clase": "didona", "tonos": ["elegante", "premium", "autor", "calido", "brasa"], "personalidades": ["elegante"],
        "licencias": ["OFL_bodonimoda.txt", "OFL_playfairdisplay.txt", "OFL_manrope.txt"],
    },
    "playfair-inter": {
        "familia_display": "Playfair Display", "familia_texto": "Inter",
        "display": [("PlayfairDisplay-BoldItalic.ttf", 400, "italic"), ("PlayfairDisplay-Regular.ttf", 400, "normal")],
        "texto": [("Inter-Regular.ttf", 400, "normal"), ("Inter-SemiBold.ttf", 600, "normal")],
        "respaldo_display": "Georgia, 'Times New Roman', serif", "respaldo_texto": SANS,
        "caracter": "elegante", "clase": "didona", "tonos": ["elegante", "clasico", "premium", "brunch", "alta-cocina"], "personalidades": ["elegante"],
        "licencias": ["OFL_playfairdisplay.txt", "OFL_inter.txt"],
    },
    "instrument-inter": {
        "familia_display": "Instrument Serif", "familia_texto": "Inter",
        "display": [("InstrumentSerif-Italic.ttf", 400, "italic")],
        "familia_titulo": "Instrument Serif", "titulo": [("InstrumentSerif-Regular.ttf", 400, "normal")],
        "texto": [("Inter-Regular.ttf", 400, "normal"), ("Inter-SemiBold.ttf", 600, "normal"), ("Inter-Bold.ttf", 700, "normal")],
        "respaldo_display": "Georgia, 'Times New Roman', serif", "respaldo_texto": SANS,
        "caracter": "elegante", "clase": "editorial", "tonos": ["contemporaneo", "autor", "elegante", "minimal"], "personalidades": ["elegante"],
        "licencias": ["OFL_instrumentserif.txt", "OFL_inter.txt"],
    },
    "dmserif-inter": {
        "familia_display": "DM Serif Display", "familia_texto": "Inter",
        "display": [("DMSerifDisplay-Italic.ttf", 400, "italic")],
        "familia_titulo": "DM Serif Display", "titulo": [("DMSerifDisplay-Regular.ttf", 400, "normal")],
        "texto": [("Inter-Regular.ttf", 400, "normal"), ("Inter-SemiBold.ttf", 600, "normal"), ("Inter-Bold.ttf", 700, "normal")],
        "respaldo_display": "Georgia, 'Times New Roman', serif", "respaldo_texto": SANS,
        "caracter": "elegante", "clase": "suave", "tonos": ["clasico", "italiana", "trattoria", "calido", "tradicion"], "personalidades": ["elegante"],
        "licencias": ["OFL_dmserifdisplay.txt", "OFL_inter.txt"],
    },
    "fraunces-manrope": {
        "familia_display": "Fraunces", "familia_texto": "Manrope",
        "display": [("Fraunces-DisplayItalic.ttf", 400, "italic")],
        "familia_titulo": "Fraunces Soft", "titulo": [("Fraunces-DisplaySoft.ttf", 400, "normal")],
        "texto": [("Manrope-Regular.ttf", 400, "normal"), ("Manrope-SemiBold.ttf", 600, "normal"), ("Manrope-Bold.ttf", 700, "normal")],
        "respaldo_display": "Georgia, 'Times New Roman', serif", "respaldo_texto": SANS,
        "caracter": "elegante", "clase": "suave", "tonos": ["calido", "autor", "tradicion", "artesanal", "panaderia"], "personalidades": ["elegante"],
        "licencias": ["OFL_fraunces.txt", "OFL_manrope.txt"],
    },
    "bodoni-outfit": {
        "familia_display": "Bodoni Moda", "familia_texto": "Outfit",
        "display": [("BodoniModa-DisplayItalic.ttf", 400, "italic")],
        "familia_titulo": "Bodoni Moda Regular", "titulo": [("BodoniModa-DisplayRegular.ttf", 400, "normal")],
        "texto": [("Outfit-Regular.ttf", 400, "normal"), ("Outfit-SemiBold.ttf", 600, "normal"), ("Outfit-Bold.ttf", 700, "normal")],
        "respaldo_display": "Didot, 'Bodoni 72', 'Times New Roman', Georgia, serif", "respaldo_texto": SANS,
        "caracter": "elegante", "clase": "didona", "tonos": ["lujo", "dulce", "pasteleria", "premium", "elegante"], "personalidades": ["elegante"],
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

# ---------------------------------------------------------------- parejas traídas de Fontsource (archivos WOFF2 de edumashow/fuentes, sin modificar)
SERIF = "Georgia, 'Times New Roman', serif"
SANS_DURA = "Arial, 'Helvetica Neue', sans-serif"
CONDENSADA = "Impact, 'Arial Narrow Bold', sans-serif"


def _texto(familia, archivo, pesos=(400, 500, 700)):
    """Las caras de una fuente de texto de Fontsource: archivo Familia-Regular, -Medium y -Bold."""
    nombres = {400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold"}
    return [(f"{archivo}-{nombres[p]}.woff2", p, "normal") for p in pesos]


def _pareja(fd, ft, display, texto, clase, tonos, pers, lic, caracter=None, titulo=None, respaldo=SERIF):
    p = {"familia_display": fd, "familia_texto": ft, "display": display, "texto": texto, "respaldo_display": respaldo, "respaldo_texto": SANS,
         "caracter": caracter or ("elegante" if pers == "elegante" else "casual"), "clase": clase, "tonos": tonos, "personalidades": [pers], "licencias": lic}
    if titulo:
        p["familia_titulo"], p["titulo"] = titulo
    return p


# Elegante. Clases del titular (para la rotación): clasica (garaldas y romanas), didona (alto contraste), suave (serifas cálidas), editorial (de lectura y de revista).
PAREJAS.update({
    "cormorant-dmsans": _pareja("Cormorant Garamond", "DM Sans", [("CormorantGaramond-MediumItalic.woff2", 400, "italic"), ("CormorantGaramond-Medium.woff2", 400, "normal")],
                                _texto("DM Sans", "DmSans"), "clasica", ["clasico", "elegante", "premium", "autor", "tradicion", "italiana"], "elegante", ["OFL_cormorantgaramond.txt", "OFL_dmsans.txt"]),
    "caslon-karla": _pareja("Libre Caslon Display", "Karla", [("LibreCaslonDisplay-Regular.woff2", 400, "normal")],
                            _texto("Karla", "Karla"), "clasica", ["alta-cocina", "premium", "autor", "elegante", "lujo"], "elegante", ["OFL_librecaslondisplay.txt", "OFL_karla.txt"]),
    "gloock-worksans": _pareja("Gloock", "Work Sans", [("Gloock-Regular.woff2", 400, "normal")],
                               _texto("Work Sans", "WorkSans"), "didona", ["contemporaneo", "autor", "moderno", "premium", "elegante"], "elegante", ["OFL_gloock.txt", "OFL_worksans.txt"]),
    "youngserif-figtree": _pareja("Young Serif", "Figtree", [("YoungSerif-Regular.woff2", 400, "normal")],
                                  _texto("Figtree", "Figtree"), "suave", ["calido", "artesanal", "tradicion", "familiar", "amable", "panaderia"], "elegante", ["OFL_youngserif.txt", "OFL_figtree.txt"]),
    "newsreader-inter": _pareja("Newsreader", "Inter", [("Newsreader-RegularItalic.woff2", 400, "italic"), ("Newsreader-Regular.woff2", 400, "normal")],
                                [("Inter-Regular.ttf", 400, "normal"), ("Inter-SemiBold.ttf", 600, "normal"), ("Inter-Bold.ttf", 700, "normal")], "editorial",
                                ["contemporaneo", "autor", "calmado", "cafe", "minimal"], "elegante", ["OFL_newsreader.txt", "OFL_inter.txt"]),
    "lora-karla": _pareja("Lora", "Karla", [("Lora-RegularItalic.woff2", 400, "italic"), ("Lora-Regular.woff2", 400, "normal")],
                          _texto("Karla", "Karla"), "suave", ["calido", "familiar", "tradicion", "artesanal", "amable"], "elegante", ["OFL_lora.txt", "OFL_karla.txt"]),
    "baskerville-dmsans": _pareja("Libre Baskerville", "DM Sans", [("LibreBaskerville-RegularItalic.woff2", 400, "italic"), ("LibreBaskerville-Regular.woff2", 400, "normal")],
                                  _texto("DM Sans", "DmSans"), "clasica", ["clasico", "tradicion", "elegante", "premium", "italiana"], "elegante", ["OFL_librebaskerville.txt", "OFL_dmsans.txt"]),
    "garamond-manrope": _pareja("EB Garamond", "Manrope", [("EbGaramond-RegularItalic.woff2", 400, "italic"), ("EbGaramond-Regular.woff2", 400, "normal")],
                                [("Manrope-Regular.ttf", 400, "normal"), ("Manrope-SemiBold.ttf", 600, "normal"), ("Manrope-Bold.ttf", 700, "normal")], "clasica",
                                ["tradicion", "clasico", "italiana", "autor", "calido", "trattoria"], "elegante", ["OFL_ebgaramond.txt", "OFL_manrope.txt"]),
    "yeseva-outfit": _pareja("Yeseva One", "Outfit", [("YesevaOne-Regular.woff2", 400, "normal")],
                             [("Outfit-Regular.ttf", 400, "normal"), ("Outfit-SemiBold.ttf", 600, "normal"), ("Outfit-Bold.ttf", 700, "normal")], "didona",
                             ["dulce", "pasteleria", "lujo", "calido", "premium"], "elegante", ["OFL_yesevaone.txt", "OFL_outfit.txt"]),
    "prata-inter": _pareja("Prata", "Inter", [("Prata-Regular.woff2", 400, "normal")],
                           [("Inter-Regular.ttf", 400, "normal"), ("Inter-SemiBold.ttf", 600, "normal"), ("Inter-Bold.ttf", 700, "normal")], "didona",
                           ["lujo", "premium", "elegante", "alta-cocina", "autor"], "elegante", ["OFL_prata.txt", "OFL_inter.txt"]),
    "gilda-worksans": _pareja("Gilda Display", "Work Sans", [("GildaDisplay-Regular.woff2", 400, "normal")],
                              _texto("Work Sans", "WorkSans"), "clasica", ["marino", "luminoso", "elegante", "calmado", "premium"], "elegante", ["OFL_gildadisplay.txt", "OFL_worksans.txt"]),
    "marcellus-figtree": _pareja("Marcellus", "Figtree", [("Marcellus-Regular.woff2", 400, "normal")],
                                 _texto("Figtree", "Figtree"), "clasica", ["marino", "luminoso", "calmado", "minimal", "moderno"], "elegante", ["OFL_marcellus.txt", "OFL_figtree.txt"]),
    "spectral-dmsans": _pareja("Spectral", "DM Sans", [("Spectral-RegularItalic.woff2", 400, "italic"), ("Spectral-Regular.woff2", 400, "normal")],
                               _texto("DM Sans", "DmSans"), "editorial", ["contemporaneo", "autor", "cafe", "fresco", "calmado"], "elegante", ["OFL_spectral.txt", "OFL_dmsans.txt"]),
})

# Urbano. Clases: condensada, expandida, grotesca, geometrica (las que ya había) y pesada (rotundas de cartel), slab (con remates rectos), redondeada (amables y pop).
PAREJAS.update({
    "oswald-dmsans": _pareja("Oswald", "DM Sans", [("Oswald-Bold.woff2", 400, "normal")], _texto("DM Sans", "DmSans", (500, 700)), "condensada",
                             ["urbano", "potente", "callejero", "parrilla", "joven", "moderno"], "urbano", ["OFL_oswald.txt", "OFL_dmsans.txt"], respaldo=CONDENSADA),
    "leaguegothic-karla": _pareja("League Gothic", "Karla", [("LeagueGothic-Regular.woff2", 400, "normal")], _texto("Karla", "Karla", (500, 700)), "condensada",
                                  ["cartel", "potente", "urbano", "impacto", "nocturno", "social"], "urbano", ["OFL_leaguegothic.txt", "OFL_karla.txt"], respaldo=CONDENSADA),
    "bigshoulders-worksans": _pareja("Big Shoulders Display", "Work Sans", [("BigShouldersDisplay-Black.woff2", 400, "normal")], _texto("Work Sans", "WorkSans", (500, 700)), "condensada",
                                     ["parrilla", "potente", "urbano", "moderno", "callejero"], "urbano", ["OFL_bigshouldersdisplay.txt", "OFL_worksans.txt"], respaldo=CONDENSADA),
    "staatliches-figtree": _pareja("Staatliches", "Figtree", [("Staatliches-Regular.woff2", 400, "normal")], _texto("Figtree", "Figtree", (500, 700)), "condensada",
                                   ["cartel", "pop", "joven", "festivo", "callejero", "nocturno"], "urbano", ["OFL_staatliches.txt", "OFL_figtree.txt"], respaldo=CONDENSADA),
    "barlow-inter": _pareja("Barlow Condensed", "Inter", [("BarlowCondensed-ExtraBold.woff2", 400, "normal")],
                            [("Inter-Medium.ttf", 500, "normal"), ("Inter-Bold.ttf", 700, "normal")], "condensada",
                            ["urbano", "moderno", "potente", "tecnica", "social"], "urbano", ["OFL_barlowcondensed.txt", "OFL_inter.txt"], respaldo=CONDENSADA),
    "bowlby-dmsans": _pareja("Bowlby One", "DM Sans", [("BowlbyOne-Regular.woff2", 400, "normal")], _texto("DM Sans", "DmSans", (500, 700)), "pesada",
                             ["pop", "festivo", "joven", "expresivo", "callejero"], "urbano", ["OFL_bowlbyone.txt", "OFL_dmsans.txt"], respaldo=SANS_DURA),
    "passion-worksans": _pareja("Passion One", "Work Sans", [("PassionOne-Black.woff2", 400, "normal")], _texto("Work Sans", "WorkSans", (500, 700)), "pesada",
                                ["parrilla", "callejero", "festivo", "pop", "joven"], "urbano", ["OFL_passionone.txt", "OFL_worksans.txt"], respaldo=SANS_DURA),
    "alfaslab-karla": _pareja("Alfa Slab One", "Karla", [("AlfaSlabOne-Regular.woff2", 400, "normal")], _texto("Karla", "Karla", (500, 700)), "slab",
                              ["parrilla", "callejero", "tradicion", "potente", "familiar"], "urbano", ["OFL_alfaslabone.txt", "OFL_karla.txt"], respaldo=SERIF),
    "lilita-figtree": _pareja("Lilita One", "Figtree", [("LilitaOne-Regular.woff2", 400, "normal")], _texto("Figtree", "Figtree", (500, 700)), "redondeada",
                              ["amable", "familiar", "fresco", "pop", "joven", "dulce"], "urbano", ["OFL_lilitaone.txt", "OFL_figtree.txt"], respaldo=SANS_DURA),
    "paytone-dmsans": _pareja("Paytone One", "DM Sans", [("PaytoneOne-Regular.woff2", 400, "normal")], _texto("DM Sans", "DmSans", (500, 700)), "redondeada",
                              ["amable", "familiar", "fresco", "festivo", "dulce"], "urbano", ["OFL_paytoneone.txt", "OFL_dmsans.txt"], respaldo=SANS_DURA),
    "fredoka-figtree": _pareja("Fredoka", "Figtree", [("Fredoka-Bold.woff2", 400, "normal")], _texto("Figtree", "Figtree", (500, 700)), "redondeada",
                               ["amable", "familiar", "fresco", "joven", "dulce", "saludable"], "urbano", ["OFL_fredoka.txt", "OFL_figtree.txt"], respaldo=SANS_DURA),
    "righteous-karla": _pareja("Righteous", "Karla", [("Righteous-Regular.woff2", 400, "normal")], _texto("Karla", "Karla", (500, 700)), "redondeada",
                               ["festivo", "pop", "nocturno", "social", "joven"], "urbano", ["OFL_righteous.txt", "OFL_karla.txt"], respaldo=SANS_DURA),
    "rubik-rubik": _pareja("Rubik", "Rubik", [("Rubik-Black.woff2", 400, "normal")], [("Rubik-Regular.woff2", 400, "normal"), ("Rubik-SemiBold.woff2", 600, "normal")], "grotesca",
                           ["moderno", "joven", "fresco", "tecnica", "urbano"], "urbano", ["OFL_rubik.txt"], respaldo=SANS_DURA),
    "chivo-inter": _pareja("Chivo", "Inter", [("Chivo-Black.woff2", 400, "normal")], [("Inter-Medium.ttf", 500, "normal"), ("Inter-Bold.ttf", 700, "normal")], "grotesca",
                           ["moderno", "urbano", "potente", "tecnica", "social"], "urbano", ["OFL_chivo.txt", "OFL_inter.txt"], respaldo=SANS_DURA),
    "spacegrotesk-inter": _pareja("Space Grotesk", "Inter", [("SpaceGrotesk-Bold.woff2", 400, "normal")], [("Inter-Medium.ttf", 500, "normal"), ("Inter-Bold.ttf", 700, "normal")], "grotesca",
                                  ["tecnica", "moderno", "minimal", "nocturno", "social"], "urbano", ["OFL_spacegrotesk.txt", "OFL_inter.txt"], respaldo=SANS_DURA),
    "sora-figtree": _pareja("Sora", "Figtree", [("Sora-ExtraBold.woff2", 400, "normal")], _texto("Figtree", "Figtree", (500, 700)), "geometrica",
                            ["moderno", "fresco", "saludable", "amable", "luminoso"], "urbano", ["OFL_sora.txt", "OFL_figtree.txt"], respaldo=SANS_DURA),
    "syne-manrope": _pareja("Syne", "Manrope", [("Syne-ExtraBold.woff2", 400, "normal")], [("Manrope-Medium.ttf", 500, "normal"), ("Manrope-Bold.ttf", 700, "normal")], "expandida",
                            ["tendencia", "joven", "autor", "moderno", "minimal"], "urbano", ["OFL_syne.txt", "OFL_manrope.txt"], respaldo=SANS_DURA),
    "delagothic-dmsans": _pareja("Dela Gothic One", "DM Sans", [("DelaGothicOne-Regular.woff2", 400, "normal")], _texto("DM Sans", "DmSans", (500, 700)), "expandida",
                                 ["pop", "expresivo", "joven", "festivo", "tendencia"], "urbano", ["OFL_delagothicone.txt", "OFL_dmsans.txt"], respaldo=SANS_DURA),
    "shrikhand-dmsans": _pareja("Shrikhand", "DM Sans", [("Shrikhand-Regular.woff2", 400, "normal")], _texto("DM Sans", "DmSans", (500, 700)), "cursiva",
                                ["festivo", "pop", "dulce", "calido", "playero", "familiar"], "urbano", ["OFL_shrikhand.txt", "OFL_dmsans.txt"], respaldo=SERIF),
})

# clase tipográfica de cada fuente de titular (la rotación evita repetir la misma fuente y la misma clase entre webs seguidas de una familia)
CLASES = {
    "elegante": {"clasica": ("Cormorant Garamond", "EB Garamond", "Libre Baskerville", "Libre Caslon Display", "Gilda Display", "Marcellus"),
                 "didona": ("Bodoni Moda", "Playfair Display", "Prata", "Gloock", "Yeseva One"),
                 "suave": ("Fraunces", "DM Serif Display", "Young Serif", "Lora"),
                 "editorial": ("Instrument Serif", "Newsreader", "Spectral")},
    "urbano": {"condensada": ("Anton", "Bebas Neue", "Archivo Condensed", "Oswald", "League Gothic", "Big Shoulders Display", "Staatliches", "Barlow Condensed"),
               "expandida": ("Archivo Expanded", "Unbounded", "Syne", "Dela Gothic One"),
               "grotesca": ("Bricolage Grotesque", "Rubik", "Chivo", "Space Grotesk"), "geometrica": ("Outfit", "Sora"),
               "pesada": ("Bowlby One", "Passion One"), "slab": ("Alfa Slab One",), "redondeada": ("Lilita One", "Paytone One", "Fredoka", "Righteous"), "cursiva": ("Shrikhand",)},
}


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


def ancho_palabra(clave, palabra):
    """Ancho medio por letra (en em) de una palabra en las caras de titular de la pareja, escrita tal cual y en mayúsculas (se toma la mayor de las medidas).
    Hay tipografías cuyas minúsculas son más anchas que sus mayúsculas (Young Serif, por ejemplo): con el ancho de las mayúsculas el nombre se saldría de la pantalla."""
    p = PAREJAS[clave]
    mejor = 0.0
    for archivo, _, _ in list(p["display"]) + list(p.get("titulo", [])):
        t = TTFont(os.path.join(CARPETA, archivo))
        cm, hm, upm = t.getBestCmap(), t["hmtx"], t["head"].unitsPerEm
        for variante in {palabra, palabra.upper()}:
            ws = [hm[cm[ord(c)]][0] for c in variante if ord(c) in cm]
            if ws:
                mejor = max(mejor, sum(ws) / len(ws) / upm)
    return round(mejor, 3)


def ancho_titular(clave, nombre):
    """El ancho por letra con el que se dimensiona el titular: el de las mayúsculas o el de la palabra más ancha del nombre, el mayor de los dos."""
    return max(ancho_em(clave), max(ancho_palabra(clave, w) for w in nombre.split()))


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
    """Recorta una fuente a unicodes_base() y la guarda como WOFF2. Devuelve el tamaño en bytes.
    Un archivo que ya es WOFF2 (los de Fontsource, que ya son el recorte latino que publica Google Fonts) se sirve sin tocar: varias licencias OFL reservan
    el nombre de la fuente y solo permiten usarlo en la fuente sin modificar."""
    ruta = os.path.join(CARPETA, archivo_ttf)
    if archivo_ttf.endswith(".woff2"):
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        shutil.copyfile(ruta, destino)
        return os.path.getsize(destino)
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
    # una fuente TTF viaja recortada a unicodes_base(): lo que quede fuera se vería con la fuente del sistema; un WOFF2 de Fontsource viaja entero
    servidos = set(cmap) if archivo_ttf.endswith(".woff2") else set(unicodes_base())
    # el espacio de no separación (U+00A0) lo dibuja el navegador con el espacio de la fuente cuando ésta no lo trae: no cuenta como falta
    return sorted({c for c in texto if ord(c) > 0x20 and ord(c) != 0xA0 and (ord(c) not in cmap or ord(c) not in servidos)})
