"""Pruebas rápidas del director de estilo (sin navegador): paleta, rotación tipográfica, cobertura de caracteres, antojo y determinismo.

Uso: python3 scripts/probar_director.py
Sale con código 0 si todo pasa.
"""
import copy
import json
import os
import sys
import tempfile

from PIL import Image

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, RAIZ)

from edumashow.motor import antojo, catalogo, color, estilo, huella, tipografia  # noqa: E402
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
    reg = {"lumbre": {"display": "Bodoni Moda", "clase_tipografica": "serif", "portada": "luz_brasas", "secuencia": 1},
           "alfuego": {"display": "Anton", "clase_tipografica": "condensada", "portada": "mural_columnas", "secuencia": 2}}
    # el director anota lo que elige en el registro: las pruebas usan uno propio, nunca el real
    ruta_reg = os.path.join(tempfile.mkdtemp(), "registro.json")
    with open(ruta_reg, "w", encoding="utf-8") as f:
        json.dump(reg, f)

    # 1) paleta: del logo, todos los pares de contraste cumplen y es determinista
    d1 = estilo.decidir(alf, ORIGEN_ACTIVOS, ruta_reg)
    d2 = estilo.decidir(alf, ORIGEN_ACTIVOS, ruta_reg)
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
    h = dict(h, familia="urbano")
    comprobar("la rotación detecta una repetición de fuente y de clase", len(huella.rotacion("otro", h, {"a": {"display": "Anton", "clase_tipografica": "condensada", "portada": "mural_columnas", "secuencia": 1},
                                                                                                          "b": {"display": "Anton", "clase_tipografica": "condensada", "portada": "mural_columnas", "secuencia": 2}})) == 2)
    comprobar("la rotación no salta si la fuente no se repite en la familia", huella.rotacion("otro", dict(h, display="Unbounded", clase_tipografica="expandida"), reg) == [])
    comprobar("la rotación de la familia urbana no cuenta las webs elegantes", huella.rotacion("otro", dict(h, display="Bodoni Moda", clase_tipografica="serif"), reg) == [])

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
    dl = estilo.decidir(lum, ORIGEN_ACTIVOS, ruta_reg)
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

    # 8) composición: cada dimensión sale de las opciones de su familia, con su motivo, y la ficha puede fijarla
    c = d1["composicion"]
    comprobar("la composición elige una opción de su familia en cada dimensión", all(c["elegidas"][d] in catalogo.OPCIONES[d]["urbano"] for d in catalogo.DIMENSIONES))
    comprobar("cada elección lleva su motivo", all(c["motivos"].get(d) for d in catalogo.DIMENSIONES))
    fijada = copy.deepcopy(alf); fijada["id"] = "fijada"; fijada["estilo"]["portada"] = "cartel_rotulo"; fijada["estilo"]["ornamento"] = "onda"
    df = estilo.decidir(fijada, ORIGEN_ACTIVOS, ruta_reg)
    comprobar("lo que la ficha fija manda", df["composicion"]["elegidas"]["portada"] == "cartel_rotulo" and df["composicion"]["elegidas"]["ornamento"] == "onda")
    df2 = estilo.decidir(fijada, ORIGEN_ACTIVOS, ruta_reg)
    comprobar("una web ya construida conserva su diseño al volver a construirse", df2["composicion"]["elegidas"] == df["composicion"]["elegidas"] and df2["tipografia"]["clave"] == df["tipografia"]["clave"])
    # variedad: 30 webs seguidas de la misma familia cumplen la distancia con las 12 anteriores y no repiten firma
    ruta30 = os.path.join(tempfile.mkdtemp(), "registro30.json")
    hs = []
    for i in range(30):
        f30 = copy.deepcopy(alf); f30["id"] = f"s{i:02d}"; f30["estilo"].pop("portada", None); f30["estilo"].pop("carta", None); f30["estilo"].pop("galeria", None); f30["estilo"]["tipografia"] = "auto"
        hs.append(estilo.decidir(f30, ORIGEN_ACTIVOS, ruta30)["huella"])
    minimos = [min(huella.distancia(h_, p_) for p_ in hs[max(0, i - 12):i]) for i, h_ in enumerate(hs) if i]
    comprobar("30 webs seguidas distan al menos el umbral de las 12 anteriores", min(minimos) >= huella.UMBRAL, f"mínimo {min(minimos)}")
    comprobar("30 webs seguidas no repiten ninguna huella completa", len({huella.firma(h_) for h_ in hs}) == 30)

    print("\nFALLAN:" if FALLOS else "\nTodo pasa.", FALLOS or "")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    sys.exit(main())
