"""Huella de diseño y distancia entre webs (Gate de unicidad, R-VAR-01).

Seis dimensiones: paleta, tipografía, portada, carta, orden de secciones, forma y movimiento.
Dos webs son suficientemente distintas si difieren en al menos 3 de las 6.
"""
import hashlib
import json
import os

DIMENSIONES = ("paleta", "tipografia", "portada", "carta", "orden", "forma_movimiento")
MINIMO_DISTINTAS = 3


def huella(ficha):
    e = ficha["estilo"]
    return {
        "paleta": e["paleta"],
        "tipografia": e["tipografia"],
        "portada": e["portada"],
        "carta": e["carta"],
        "orden": hashlib.sha1("|".join(e["orden"]).encode()).hexdigest()[:8],
        "forma_movimiento": f'{e["forma"]}+{e["movimiento"]}',
    }


def distancia(a, b):
    """Número de dimensiones en las que difieren."""
    return sum(1 for d in DIMENSIONES if a.get(d) != b.get(d))


def cargar_registro(ruta):
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    return {}


def comparar(ficha_id, h, registro):
    """Devuelve la lista de (otra_web, distancia) y si cumple el mínimo frente a todas las demás."""
    otras = [(k, distancia(h, v)) for k, v in registro.items() if k != ficha_id]
    cumple = all(d >= MINIMO_DISTINTAS for _, d in otras)
    return otras, cumple


def registrar(ficha_id, h, ruta):
    reg = cargar_registro(ruta)
    reg[ficha_id] = h
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
