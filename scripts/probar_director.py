"""Pruebas rápidas del director de estilo (sin navegador): paleta, rotación tipográfica, cobertura de caracteres, antojo y determinismo.

Uso: python3 scripts/probar_director.py
Sale con código 0 si todo pasa.
"""
import copy
import json
import os
import sys

from PIL import Image

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, RAIZ)

from edumashow.motor import antojo, color, estilo, huella, tipografia  # noqa: E402
from edumashow.motor.generar import ORIGEN_ACTIVOS  # noqa: E402

FALLOS = []


def comprobar(nombre, condicion, detalle=""):
    print(("ok     " if condicion else "FALLA  ") + nombre + (f"  {detalle}" if detalle else ""))
    if not condicion:
        FALLOS.append(nombre)


def ficha(nombre):
    with open(os.path.join(RAIZ, "edumashow", "fichas", nombre + ".json"), encoding="utf-8") as f:
        return json.load(f)


def main():
    alf, lum = ficha("alfuego"), ficha("lumbre")
    reg = {"lumbre": {"display": "Bodoni Moda", "clase_tipografica": "serif", "secuencia": 1},
           "alfuego": {"display": "Anton", "clase_tipografica": "condensada", "secuencia": 2}}

    # 1) paleta: del logo, todos los pares de contraste cumplen y es determinista
    d1 = estilo.decidir(alf, ORIGEN_ACTIVOS, reg)
    d2 = estilo.decidir(alf, ORIGEN_ACTIVOS, reg)
    pares = d1["paleta"]["pares"]
    comprobar("la paleta de Al Fuego sale del logo", d1["paleta"]["id"].startswith("auto:"), d1["paleta"]["origen"])
    comprobar("todos los pares de contraste de la paleta cumplen", all(p["ok"] for p in pares), f"{len(pares)} pares")
    comprobar("la misma ficha da las mismas decisiones", json.dumps(d1["paleta"]["tokens"], sort_keys=True) == json.dumps(d2["paleta"]["tokens"], sort_keys=True)
              and d1["tipografia"]["clave"] == d2["tipografia"]["clave"] and d1["fotos"]["orden_por_antojo"] == d2["fotos"]["orden_por_antojo"])
    comprobar("el acento de temporada es de la temporada vigente en la fecha de la ficha", d1["paleta"]["informe"]["acento"]["temporada"] == "AW26/27")

    # 2) paletas hechas a mano: se validan con los mismos pares
    for n in ("brasa", "fuego"):
        from edumashow.motor import temas
        comprobar(f"la paleta a mano {n} cumple todos los pares", all(p["ok"] for p in color.pares_de_contraste(temas.PALETAS[n])))

    # 3) tipografía: la mejor probada, y nunca una que repita fuente o clase
    t = d1["tipografia"]
    comprobar("el director elige una pareja probada en el Gate", tipografia.esta_probada(t["clave"], "urbano"), t["clave"])
    reg3 = copy.deepcopy(reg)
    reg3["x1"] = {"display": "Bebas Neue", "clase_tipografica": "condensada", "secuencia": 3}
    reg3["x2"] = {"display": "Archivo Condensed", "clase_tipografica": "condensada", "secuencia": 4}
    nuevo = copy.deepcopy(alf)
    nuevo["id"] = "otro_urbano"
    try:
        t3 = estilo.elegir_tipografia(nuevo, json.dumps(nuevo, ensure_ascii=False), reg3, ["callejero", "potente", "urbano"])
        comprobar("con 3 titulares condensados ya registrados no se propone otro condensado", t3["elegida"]["clase"] != "condensada", t3["clave"])
    except Exception as e:   # sin parejas probadas de otra clase el motor se abstiene: también es correcto
        comprobar("con 3 titulares condensados ya registrados el motor se abstiene o cambia de clase", "rotación" in str(e) or "pareja" in str(e), str(e)[:80])
    # una pareja fijada a mano que rompe la rotación se ve en la huella
    h = {"display": "Anton", "clase_tipografica": "condensada"}
    comprobar("la rotación detecta una repetición", len(huella.rotacion("otro", h, {"a": {"display": "Anton", "clase_tipografica": "condensada", "secuencia": 1},
                                                                                   "b": {"display": "Anton", "clase_tipografica": "condensada", "secuencia": 2}})) == 2)
    comprobar("la rotación no salta con una sola repetición", huella.rotacion("otro", h, reg) == [])

    # 4) cobertura de caracteres: Instrument Serif no trae la media (U+00BD)
    comprobar("una pareja sin el carácter de la media libra se descarta", "½" in tipografia.faltantes("instrument-inter", "carne ½ lb"))
    comprobar("Anton y Archivo sí traen la media libra", tipografia.faltantes("anton-archivo", "carne ½ lb") == [])

    # 5) antojo: el ranking sigue los puntos y deja fuera lo descartado
    regs, orden = estilo.puntuar_fotos(alf, ORIGEN_ACTIVOS)
    puntos = [regs[k]["puntos"] for k in orden]
    comprobar("el ranking de antojo va de más a menos", puntos == sorted(puntos, reverse=True), str(list(zip(orden, puntos))))
    f2 = copy.deepcopy(alf)
    f2["activos"]["picada"]["antojo"]["sin_marcas_ajenas"] = False
    regs2, orden2 = estilo.puntuar_fotos(f2, ORIGEN_ACTIVOS)
    comprobar("una foto con marcas ajenas queda fuera del ranking", "picada" not in orden2 and regs2["picada"]["descartada"])
    try:
        antojo.juicio_visual({"textura": 2})
        comprobar("un juicio incompleto se rechaza", False)
    except ValueError:
        comprobar("un juicio incompleto se rechaza", True)
    im = Image.new("RGB", (40, 40), (120, 80, 40))
    comprobar("una foto diminuta y lisa no rompe las medidas", antojo.medidas_tecnicas(im)["puntos"] >= 0)

    # 6) Lumbre (paleta y pareja a mano): se valida sin cambiar nada
    dl = estilo.decidir(lum, ORIGEN_ACTIVOS, reg)
    comprobar("Lumbre mantiene su pareja fijada", dl["tipografia"]["clave"] == lum["estilo"]["tipografia"])
    comprobar("Lumbre mantiene su paleta a mano", dl["paleta"]["id"] == lum["estilo"]["paleta"])

    # 7) casos de borde: un logo de un solo color, una foto muy plana o con transparencia no rompen el cálculo
    from PIL import ImageDraw
    plano = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
    ImageDraw.Draw(plano).rectangle((10, 10, 110, 110), fill=(200, 60, 30, 255))
    dom = color.colores_dominantes(plano)
    comprobar("un logo de un solo color no rompe el cálculo de la paleta", len(dom) == 1 and dom[0]["peso"] == 1.0)
    dos = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
    ImageDraw.Draw(dos).rectangle((10, 10, 110, 110), fill=(200, 60, 30, 255))
    ImageDraw.Draw(dos).rectangle((40, 40, 80, 80), fill=(20, 20, 20, 255))
    comprobar("un logo de dos colores lisos da dos grupos", len(color.colores_dominantes(dos)) == 2)
    comprobar("una foto de 800 x 3 px no rompe las medidas", antojo.medidas_tecnicas(Image.new("RGB", (800, 3), (120, 80, 40)))["puntos"] >= 0)
    comprobar("una foto transparente se mide sobre gris y no rompe", antojo.medidas_tecnicas(Image.new("RGBA", (60, 60), (255, 0, 0, 0)))["puntos"] >= 0)

    print("\nFALLAN:" if FALLOS else "\nTodo pasa.", FALLOS or "")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    sys.exit(main())
