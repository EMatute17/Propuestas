"""Huella de diseño y distancia entre webs (Gate de unicidad, R-VAR-01) y rotación tipográfica (R-VAR-03).

Seis dimensiones: paleta, tipografía, portada, carta, orden de secciones, forma y movimiento.
Dos webs son suficientemente distintas si difieren en al menos 3 de las 6.

Rotación (Documento Maestro, 6.3): una misma tipografía de titular web tras web hace que todas se parezcan aunque cambien
los colores. Es FALLO que el titular nuevo use la misma fuente que 2 de las 6 webs anteriores, o la misma clase tipográfica
que 2 de las 4 anteriores. El orden de las webs lo da la secuencia con la que se registraron.
"""
import hashlib
import json
import os

from . import tipografia

DIMENSIONES = ("paleta", "tipografia", "portada", "carta", "orden", "forma_movimiento")
MINIMO_DISTINTAS = 3


ULTIMAS_FUENTE, MAX_FUENTE = 6, 2       # la misma fuente de titular en 2 de las 6 anteriores es fallo
ULTIMAS_CLASE, MAX_CLASE = 4, 2         # la misma clase en 2 de las 4 anteriores es fallo


def huella(ficha, estilo=None):
    """Huella de diseño. `estilo` es el estilo ya resuelto por el director (paleta y tipografía concretas); si no se da, el de la ficha."""
    e = estilo or ficha["estilo"]
    clave = e["tipografia"]
    return {
        "paleta": e["paleta"],
        "tipografia": clave,
        "display": tipografia.display_de(clave),
        "clase_tipografica": tipografia.clase(clave),
        "portada": e["portada"],
        "carta": e["carta"],
        "orden": hashlib.sha1("|".join(e["orden"]).encode()).hexdigest()[:8],
        "forma_movimiento": f'{e["forma"]}+{e["movimiento"]}',
    }


def distancia(a, b):
    """Número de dimensiones en las que difieren (la secuencia y los datos de rotación no cuentan)."""
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


def anteriores(ficha_id, registro):
    """Las demás webs del registro, de la más reciente a la más antigua."""
    return [v for _, _, v in sorted(((v.get("secuencia", 0), k, v) for k, v in registro.items() if k != ficha_id), reverse=True)]


def rotacion(ficha_id, h, registro):
    """Lista de problemas de rotación tipográfica de una huella frente a las webs registradas (vacía si cumple)."""
    previas = anteriores(ficha_id, registro)
    en_fuente = sum(1 for v in previas[:ULTIMAS_FUENTE] if v.get("display") == h["display"])
    en_clase = sum(1 for v in previas[:ULTIMAS_CLASE] if v.get("clase_tipografica") == h["clase_tipografica"])
    problemas = []
    if en_fuente >= MAX_FUENTE:
        problemas.append(f'la fuente de titular {h["display"]} ya está en {en_fuente} de las {min(ULTIMAS_FUENTE, len(previas))} webs anteriores')
    if en_clase >= MAX_CLASE:
        problemas.append(f'la clase tipográfica {h["clase_tipografica"]} ya está en {en_clase} de las {min(ULTIMAS_CLASE, len(previas))} webs anteriores')
    return problemas


def registrar(ficha_id, h, ruta):
    reg = cargar_registro(ruta)
    previo = reg.get(ficha_id, {})
    h = dict(h)
    h["secuencia"] = previo.get("secuencia") or (max([v.get("secuencia", 0) for v in reg.values()] or [0]) + 1)
    reg[ficha_id] = h
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
