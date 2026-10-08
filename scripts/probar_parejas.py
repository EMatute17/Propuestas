"""Prueba parejas tipográficas en el Gate para que el director de estilo pueda proponerlas.

Para cada pareja genera la web de una ficha base con esa pareja y pasa el Gate en modo rápido (los 4 dispositivos
representativos, sin Lighthouse). Si no hay ningún bloqueo la anota en edumashow/gate/parejas_probadas.json. El director de
estilo solo propone parejas anotadas ahí. La web que se entrega pasa siempre el Gate completo, con la pareja que se haya elegido.

La web de prueba es una copia de otra a propósito (solo cambia la tipografía), así que no se le exige G-HUELLA: que una web
sea distinta de las demás no tiene sentido para una copia. Todo lo demás sí se exige, salvo el origen y la calidad de las fotos de las fichas base
(Lumbre y Al Fuego ya no cumplen la regla de fotos): esas dos comprobaciones corren en modo prueba y no bloquean. Con tantas parejas conviene usar
`scripts/cobertura_catalogo.py --tipografias`, que reparte las parejas entre las fichas de cobertura y las prueba junto con todas las composiciones.

Uso:
    python3 scripts/probar_parejas.py edumashow/fichas/alfuego.json pareja1,pareja2 [--trabajo CARPETA]
"""
import argparse
import copy
import datetime
import json
import os
import sys

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, RAIZ)

from edumashow.gate import verificar as V  # noqa: E402
from edumashow.motor import generar, tipografia  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ficha")
    ap.add_argument("parejas")
    ap.add_argument("--trabajo", default=os.path.join(RAIZ, "..", "pruebas_parejas"))
    a = ap.parse_args()
    base = json.load(open(a.ficha, encoding="utf-8"))
    pers = base["estilo"]["personalidad"]
    os.makedirs(a.trabajo, exist_ok=True)
    resultados = {}
    for clave in a.parejas.split(","):
        p = tipografia.PAREJAS[clave]
        if pers not in p["personalidades"]:
            print(f"{clave}: no es una pareja de la personalidad {pers}; se omite")
            continue
        f = copy.deepcopy(base)
        f["id"] = f"{base['id']}__{clave}"
        f["estilo"]["tipografia"] = clave
        ruta = os.path.join(a.trabajo, f["id"] + ".json")
        json.dump(f, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        try:
            r = generar.construir(ruta, a.trabajo)
        except generar.FichaIncompleta as e:
            print(f"{clave}: el motor se abstiene: {e}")
            resultados[clave] = ("SE ABSTIENE", [str(e)])
            continue
        inf = V.verificar(ruta, r["carpeta"], rapido=True, con_navegador=True, con_rendimiento=False, dir_informe=os.path.join(a.trabajo, "informe_" + f["id"]), fotos_de_prueba=True)
        bloq = [(b["id"], b["detalle"][:3]) for b in inf["resultados"] if b["id"] in inf["bloqueantes"] and b["id"] != "G-HUELLA"]
        veredicto = "APTO" if not bloq else "NO APTO"
        resultados[clave] = (veredicto, bloq)
        print(f"{clave}: {veredicto} {bloq if bloq else ''}", flush=True)
        if veredicto == "APTO":
            reg = tipografia.probadas()
            reg.setdefault(clave, {})[pers] = {"fecha": datetime.date.today().isoformat(), "sitio": base["id"],
                                               "modo": "rápido (4 dispositivos representativos, sin Lighthouse; sin G-HUELLA, que no aplica a una copia de prueba)", "veredicto": "APTO",
                                               "gate": V.VERSION_GATE}
            with open(tipografia.RUTA_PROBADAS, "w", encoding="utf-8") as g:
                json.dump(reg, g, ensure_ascii=False, indent=1, sort_keys=True)
                g.write("\n")
    print(json.dumps({k: v[0] for k, v in resultados.items()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
