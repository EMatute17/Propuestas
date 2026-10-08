"""Ornamento: el borde entre secciones de color distinto (una de las dimensiones del catálogo, R-VAR-04).

Cada opción dibuja una forma distinta (onda, diente de sierra, arco, papel rasgado) en el límite entre una sección y la siguiente, con los colores reales de las
dos secciones, de modo que la página no sea una pila de bloques rectos. La forma rasgada se dibuja con la semilla de la web: cada restaurante tiene el suyo.
Son adornos: van ocultos a los lectores de pantalla y no ocupan más que unas decenas de píxeles.
"""
import hashlib
import math
import random

# color de fondo de cada sección (el token de color que usa su CSS); lo que no está aquí no lleva borde propio
FONDOS = {
    "elegante": {"idea": "tinta", "carta": "papel", "ambiente": "tinta-2", "reserva": "tinta", "visita": "papel", "cierre": "tinta-3"},
    "urbano": {"como": "papel", "carta": "papel", "regla": "tinta-2", "fotos": "tinta-2", "visita": "tinta", "cierre": "tinta-3"},
}
FONDO_PORTADA = {"luz_brasas": "tinta", "marco_editorial": "papel", "cortina": "tinta", "mural_columnas": "tinta", "collage_pegatinas": "tinta", "cartel_rotulo": "brasa"}
FONDO_BANDA = "tinta"
ANCHO, ALTO = 1440, 80


def _ruta_onda(rng):
    fase = rng.random() * math.tau
    ptos = [(x, 38 + 20 * math.sin(fase + x / 1440 * math.tau * 2.0) + 8 * math.sin(fase * 2 + x / 1440 * math.tau * 5.0)) for x in range(0, ANCHO + 1, 40)]
    return _poligono(ptos)


def _ruta_diente(rng):
    n = 36
    ptos = [(i * ANCHO / n, 12 if i % 2 == 0 else 58) for i in range(n + 1)]
    return _poligono(ptos)


def _ruta_arco(rng):
    return f"M0,{ALTO} L0,60 Q{ANCHO / 2},-34 {ANCHO},60 L{ANCHO},{ALTO} Z"


def _ruta_rasgado(rng):
    ptos, y, x = [], 34.0, 0.0
    while x < ANCHO:
        ptos.append((x, y))
        x += rng.uniform(14, 46)
        y = min(62, max(10, y + rng.uniform(-18, 18)))
    ptos.append((ANCHO, y))
    return _poligono(ptos)


def _poligono(ptos):
    """Cierra una línea de puntos hacia abajo: el área bajo la línea es la sección que viene."""
    d = "M0," + str(ALTO) + " " + " ".join(f"L{x:.0f},{y:.0f}" for x, y in ptos) + f" L{ANCHO},{ALTO} Z"
    return d


FORMAS = {"onda": _ruta_onda, "diente": _ruta_diente, "arco": _ruta_arco, "rasgado": _ruta_rasgado}


def divisor(forma, de, a, semilla, indice=0):
    """El borde entre dos secciones: `de` es el color de la que termina y `a` el de la que empieza (nombres de token)."""
    rng = random.Random(hashlib.sha1(f"{semilla}|{forma}|{indice}".encode()).hexdigest())
    d = FORMAS[forma](rng)
    return (f'<div class="divisor divisor-{forma}" aria-hidden="true" style="--de:var(--{de});--a:var(--{a})">'
            f'<svg viewBox="0 0 {ANCHO} {ALTO}" preserveAspectRatio="none" focusable="false"><path d="{d}"/></svg></div>')


def intercalar(partes, familia, est_r, banda=False, semilla=""):
    """Une las secciones ya dibujadas [(nombre, html)] poniendo el borde de la opción elegida donde cambia el color de fondo.
    Con `recto` no se añade nada. El primer borde va entre la portada (o su banda) y la primera sección."""
    forma = est_r.get("ornamento", "recto")
    if forma == "recto" or forma not in FORMAS:
        return "".join(h for _, h in partes)
    fondos = FONDOS[familia]
    anterior = FONDO_BANDA if banda else FONDO_PORTADA.get(est_r.get("portada"), "tinta")
    out = []
    for i, (nombre, h) in enumerate(partes):
        actual = fondos.get(nombre)
        if actual and anterior and actual != anterior:
            out.append(divisor(forma, anterior, actual, semilla, i))
        out.append(h)
        if actual:
            anterior = actual
    return "".join(out)
