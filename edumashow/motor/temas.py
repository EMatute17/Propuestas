"""Paletas, formas y movimientos. Un tema es una combinación de estas piezas, elegida a partir de los
datos reales del restaurante (R-IDE-01). Cada paleta declara sus pares de contraste para que el Gate
los compruebe (R-LEG-01, R-IDE-03)."""
import urllib.parse

PALETAS = {
    # elegante, cocina de brasa: tinta azulada, brasa naranja y papel crema
    "brasa": {
        "tinta": "#0b141c", "tinta-2": "#0f1b25", "tinta-3": "#162532",
        "crema": "#f3e9d8", "crema-2": "#d8ccb7", "papel": "#f3e9d8", "papel-2": "#ebdfc9",
        "brasa": "#ff6b2c", "brasa-2": "#ff9a52", "brasa-papel": "#af3500",
        "bruma": "#9fb0bd", "bruma-papel": "#56616b", "texto-suave-papel": "#3d4a55",
        "sobre-brasa": "#0b141c", "foco-anillo": "#ffb27a", "foco-anillo-papel": "#8a2a05",
        "aviso": "#8a2a05", "fondo-campo": "#ffffff", "borde-campo": "rgba(11,20,28,.4)", "texto-campo": "#0b141c",
        "acento": "#ff9a52", "acento-papel": "#af3500",
        "meta-color": "#0b141c",
    },
    # urbano, parrilla y comida de calle: negro de carbon, naranja de llama y papel crema (todos los pares medidos, minimo 4.7 a 1)
    "fuego": {
        "tinta": "#0b0908", "tinta-2": "#12100e", "tinta-3": "#1b1713",
        "crema": "#f6efe6", "crema-2": "#d8cdbf", "papel": "#f6efe6", "papel-2": "#ece2d3",
        "brasa": "#ff7a1a", "brasa-2": "#ffb02e", "brasa-papel": "#b13a05",
        "bruma": "#a9a094", "bruma-papel": "#5c5349", "texto-suave-papel": "#40382f",
        "sobre-brasa": "#0b0908", "foco-anillo": "#ffc477", "foco-anillo-claro": "#ffc477", "foco-anillo-papel": "#8a2a05",
        "aviso": "#8a2a05", "fondo-campo": "#ffffff", "borde-campo": "rgba(11,9,8,.4)", "texto-campo": "#0b0908",
        "acento": "#ffb02e", "acento-papel": "#b13a05",
        "meta-color": "#0b0908",
    },
}

FORMAS = {
    "recta": {"r": "2px", "r-boton": "2px", "r-tarjeta": "4px"},
    "suave": {"r": "14px", "r-boton": "999px", "r-tarjeta": "22px"},
}

MOVIMIENTOS = {
    "lento": {"dur": ".35s", "ease": "cubic-bezier(.2,.7,.2,1)"},
    "rapido": {"dur": ".18s", "ease": "cubic-bezier(.3,1.4,.5,1)"},
}


def tokens_css(paleta, forma, movimiento, fuentes, num_letras, cinta_h, ancho_titular=0.47):
    """Bloque :root con todas las variables de diseño de la página. `paleta` es el diccionario de colores (o el nombre de una paleta hecha a mano).
    ancho_titular: ancho medio de una mayúscula del titular, en em; con él el nombre ocupa el ancho disponible sea cual sea la tipografía."""
    p, f, m = (PALETAS[paleta] if isinstance(paleta, str) else paleta), FORMAS[forma], MOVIMIENTOS[movimiento]
    linea = [f"--{k}:{v}" for k, v in p.items() if k != "meta-color"]
    linea += [f"--{k}:{v}" for k, v in f.items()]
    linea += [f"--{k}:{v}" for k, v in m.items()]
    linea += [
        f"--f-display:'{fuentes['familia_display']}',{fuentes['respaldo_display']}",
        f"--f-titulo:'{fuentes.get('familia_titulo', fuentes['familia_display'])}',{fuentes['respaldo_display']}",
        f"--f-texto:'{fuentes['familia_texto']}',{fuentes['respaldo_texto']}",
        "--max:78rem", "--pad:clamp(1.25rem,4.5vw,3.5rem)", f"--c:{num_letras}", f"--cinta-h:{cinta_h}", f"--w-d:{ancho_titular}",
    ]
    return ":root{" + ";".join(linea) + "}"


def grano_datauri():
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'>"
           "<feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/>"
           "<feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .6 0'/></filter>"
           "<rect width='100%' height='100%' filter='url(#n)'/></svg>")
    return "url(\"data:image/svg+xml," + urllib.parse.quote(svg, safe="/:=' ") + "\")"


def fibras_datauri():
    """Fibras de papel: ruido de baja frecuencia en dos capas, oscuro y transparente, para la textura papel de las secciones claras."""
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='f'>"
           "<feTurbulence type='fractalNoise' baseFrequency='.035 .6' numOctaves='3' seed='4' stitchTiles='stitch'/>"
           "<feColorMatrix values='0 0 0 0 .25 0 0 0 0 .18 0 0 0 0 .1 0 0 0 .32 0'/></filter>"
           "<rect width='100%' height='100%' filter='url(#f)'/></svg>")
    return "url(\"data:image/svg+xml," + urllib.parse.quote(svg, safe="/:=' ") + "\")"


def favicon_datauri(inicial, color_fondo, color_letra, estilo="elegante"):
    if estilo == "elegante":
        letra = "font-family='Georgia,serif' font-style='italic'"
    else:   # personalidad urbana: letra recia y sin serifas
        letra = "font-family='Impact,Arial Black,sans-serif' font-weight='900'"
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='{color_fondo}'/>"
           f"<text x='32' y='47' font-size='42' text-anchor='middle' {letra} fill='{color_letra}'>{inicial}</text></svg>")
    return "data:image/svg+xml," + urllib.parse.quote(svg, safe="/:=' ")


def lineas_titular(nombre, minimo=9):
    """Reparte las palabras del nombre en lineas de portada sin partir ninguna palabra.
    Cada linea cabe en max(minimo, la palabra mas larga) letras."""
    palabras = nombre.split()
    tope = max(minimo, max(len(w) for w in palabras))
    lineas, actual = [], ""
    for w in palabras:
        if actual and len(actual) + 1 + len(w) > tope:
            lineas.append(actual)
            actual = w
        else:
            actual = (actual + " " + w) if actual else w
    if actual:
        lineas.append(actual)
    return lineas
