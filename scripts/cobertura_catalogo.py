"""Genera fichas de prueba que cubren todos los pares de opciones del catálogo de composiciones.

Cada web elige su composición entre las opciones de portada, carta, galería, ornamento, botones, densidad, textura y animaciones. Cualquier opción
puede tocarle a cualquier restaurante, así que cada una tiene que pasar el Gate junto con cada una de las demás. Probar las 23.040 combinaciones de una
familia no es posible; probar todos los PARES sí: este programa arma, con un algoritmo voraz, el menor conjunto de fichas en el que cada opción aparece con
cada opción de las otras dimensiones al menos una vez (unas 25 fichas por familia), y deja una carpeta lista para `scripts/lote.py`.

Con --tipografias, además, cada ficha fija una pareja tipográfica distinta (se recorren todas las de la familia, también las que aún no están probadas), de modo que
una misma pasada del Gate prueba las composiciones y las tipografías; con `scripts/anotar_parejas_probadas.py` las que pasan quedan anotadas como probadas.

Uso:
    python3 scripts/cobertura_catalogo.py CARPETA [--familia elegante|urbano|ambas] [--semilla N] [--tipografias]
    python3 scripts/lote.py CARPETA --salida SALIDA --nivel rapido --paralelo 3 --fotos-de-prueba

Las fichas parten de Lumbre (elegante) y de Al Fuego Grill (urbano), con una calificación de Google de ejemplo y sus opciones fijadas. Son solo para probar el
sistema: sus fotos no cumplen la regla de calidad y por eso el lote las marca SOLO PRUEBA.
"""
import argparse
import copy
import itertools
import json
import os
import random
import sys

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, RAIZ)

from edumashow.motor import catalogo  # noqa: E402

BASES = {"elegante": "lumbre", "urbano": "alfuego"}
PREFIJO = {"elegante": "ce", "urbano": "cu"}


def _ficha_base(familia):
    with open(os.path.join(RAIZ, "edumashow", "fichas", BASES[familia] + ".json"), encoding="utf-8") as f:
        F = json.load(f)
    if familia == "elegante" and len(F["galeria"]) < 6:
        # la galería bento pide cinco fotos o más: se completan con dos platos que la ficha ya tiene como activos
        F["galeria"] = F["galeria"] + [{"foto": "plato_ravioli", "pie": "Ravioli"}, {"foto": "plato_chuleton", "pie": "Chuletón"}]
    return F


def opciones_viables(familia, base):
    """Las opciones de cada dimensión que la ficha base puede dibujar (por ejemplo, la galería bento pide cinco fotos)."""
    return {d: [o for o in catalogo.OPCIONES[d][familia] if catalogo.viable(d, o, base)] for d in catalogo.DIMENSIONES}


def cubrir_pares(opciones, semilla=7, muestras=900):
    """Conjunto de combinaciones que cubre todos los pares (dimension, opcion) x (otra dimension, otra opcion)."""
    dims = list(opciones)
    pendientes = set()
    for a, b in itertools.combinations(dims, 2):
        for x in opciones[a]:
            for y in opciones[b]:
                pendientes.add(((a, x), (b, y)))
    rng = random.Random(semilla)
    elegidas = []
    while pendientes:
        mejor, mejor_n = None, -1
        # candidatos: combinaciones al azar y las que completan algún par pendiente
        candidatos = []
        for _ in range(muestras):
            candidatos.append({d: rng.choice(opciones[d]) for d in dims})
        for par in rng.sample(sorted(pendientes), min(len(pendientes), 60)):
            c = {d: rng.choice(opciones[d]) for d in dims}
            c[par[0][0]], c[par[1][0]] = par[0][1], par[1][1]
            candidatos.append(c)
        for c in candidatos:
            n = sum(1 for a, b in itertools.combinations(dims, 2) if ((a, c[a]), (b, c[b])) in pendientes)
            if n > mejor_n:
                mejor, mejor_n = c, n
        elegidas.append(mejor)
        for a, b in itertools.combinations(dims, 2):
            pendientes.discard(((a, mejor[a]), (b, mejor[b])))
    return elegidas


def construir(familia, combinacion, i, base, pareja=None):
    F = copy.deepcopy(base)
    F["id"] = f"{PREFIJO[familia]}{i:02d}"
    est = F["estilo"]
    est["personalidad"] = familia
    est.update({d: combinacion[d] for d in catalogo.DIMENSIONES})
    est["tipografia"] = pareja or "auto"
    est["paleta"] = "auto" if familia == "urbano" else "brasa"
    if familia == "urbano":
        est.setdefault("orden_fotos", "antojo")
    # calificación de Google de ejemplo (solo para probar la pieza): con enlace, fecha y sin comentarios
    F["valoracion"] = {"fuente": "google", "nota": round(4.1 + (i % 9) / 10, 1), "resenas": 80 + 37 * i, "fecha": "2026-10-08", "url": "https://maps.app.goo.gl/ejemplo" + F["id"]}
    if familia == "elegante":
        F["valoracion"]["ejemplo"] = True
    return F


def main():
    ap = argparse.ArgumentParser(description="Fichas de prueba que cubren todos los pares de opciones del catálogo")
    ap.add_argument("carpeta")
    ap.add_argument("--familia", choices=["elegante", "urbano", "ambas"], default="ambas")
    ap.add_argument("--semilla", type=int, default=7)
    ap.add_argument("--tipografias", action="store_true", help="fija en cada ficha una pareja tipográfica distinta, recorriendo todas las de la familia")
    a = ap.parse_args()
    familias = ["elegante", "urbano"] if a.familia == "ambas" else [a.familia]
    total = 0
    for fam in familias:
        base = _ficha_base(fam)
        ops = opciones_viables(fam, base)
        combos = cubrir_pares(ops, a.semilla)
        parejas = []
        if a.tipografias:
            from edumashow.motor import tipografia
            parejas = sorted(k for k, p in tipografia.PAREJAS.items() if fam in p["personalidades"])
            random.Random(a.semilla + 1).shuffle(parejas)
        for i, c in enumerate(combos, 1):
            F = construir(fam, c, i, base, parejas[(i - 1) % len(parejas)] if parejas else None)
            d = os.path.join(a.carpeta, F["id"])
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "ficha.json"), "w", encoding="utf-8") as f:
                json.dump(F, f, ensure_ascii=False, indent=1)
                f.write("\n")
        pares = sum(len(ops[x]) * len(ops[y]) for x, y in itertools.combinations(ops, 2))
        print(f"{fam}: {len(combos)} fichas cubren los {pares} pares de opciones ({', '.join(f'{d} {len(o)}' for d, o in ops.items())})")
        total += len(combos)
    print(f"{total} fichas en {a.carpeta}")


if __name__ == "__main__":
    main()
