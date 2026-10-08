"""Anota como probadas las parejas tipográficas de las webs de un lote que pasaron el Gate sin ningún bloqueo.

El director de estilo solo propone parejas tipográficas que ya pasaron el Gate en su personalidad (gate/parejas_probadas.json). Una forma de probarlas todas es
repartirlas entre las fichas de cobertura del catálogo (`scripts/cobertura_catalogo.py --tipografias`), pasar el lote con `scripts/lote.py` y anotar aquí las que
salieron sin bloqueos. Una pareja que bloqueó en alguna web no se anota: se mira el informe de esa web para saber si falló la pareja o la composición.

Uso:
    python3 scripts/anotar_parejas_probadas.py SALIDA_DEL_LOTE [--nivel "rápido (4 dispositivos, cobertura del catálogo)"] [--simular]
"""
import argparse
import datetime
import json
import os
import sys

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, RAIZ)

from edumashow.gate import verificar as V  # noqa: E402
from edumashow.motor import tipografia  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Anota las parejas tipográficas probadas por un lote")
    ap.add_argument("salida", help="carpeta SALIDA del lote (la que tiene _informes/)")
    ap.add_argument("--nivel", default="rápido (4 dispositivos representativos, sin Lighthouse; cobertura del catálogo con fotos en modo prueba)")
    ap.add_argument("--simular", action="store_true", help="solo muestra qué se anotaría")
    a = ap.parse_args()
    base = os.path.join(a.salida, "_informes")
    if not os.path.isdir(base):
        print(f"no existe {base}")
        return 1
    pasan, fallan = {}, {}
    for id_ in sorted(os.listdir(base)):
        ruta = os.path.join(base, id_, "informe.json")
        if not os.path.exists(ruta):
            continue
        with open(ruta, encoding="utf-8") as f:
            inf = json.load(f)
        d = inf.get("decisiones_de_diseno") or {}
        clave = (d.get("tipografia") or {}).get("clave")
        fam = (d.get("estilo_resuelto") or {}).get("familia") or (d.get("composicion") or {}).get("familia")
        if not clave or clave not in tipografia.PAREJAS:
            continue
        pers = fam or tipografia.PAREJAS[clave]["personalidades"][0]
        if pers not in tipografia.PAREJAS[clave]["personalidades"]:
            continue
        bloqueantes = [b for b in inf.get("bloqueantes", []) if b != "G-HUELLA"]
        (pasan if not bloqueantes else fallan).setdefault((clave, pers), []).append((id_, bloqueantes))
    registro = tipografia.probadas()
    nuevas = 0
    for (clave, pers), webs in sorted(pasan.items()):
        if (clave, pers) in fallan:
            print(f"{clave} ({pers}): pasó en {[w[0] for w in webs]} pero bloqueó en {[(w[0], w[1]) for w in fallan[(clave, pers)]]}: no se anota")
            continue
        ya = pers in registro.get(clave, {})
        print(f"{clave} ({pers}): {'ya estaba probada' if ya else 'se anota'} con {', '.join(w[0] for w in webs)}")
        if not ya and not a.simular:
            registro.setdefault(clave, {})[pers] = {"fecha": datetime.date.today().isoformat(), "sitio": webs[0][0], "modo": a.nivel, "veredicto": "APTO", "gate": V.VERSION_GATE}
            nuevas += 1
    for (clave, pers), webs in sorted(fallan.items()):
        if (clave, pers) not in pasan:
            print(f"{clave} ({pers}): BLOQUEÓ en {[(w[0], w[1]) for w in webs]}")
    if nuevas and not a.simular:
        with open(tipografia.RUTA_PROBADAS, "w", encoding="utf-8") as g:
            json.dump(registro, g, ensure_ascii=False, indent=1, sort_keys=True)
            g.write("\n")
    print(f"{nuevas} parejas nuevas anotadas" if not a.simular else "simulación: no se escribió nada")
    return 0


if __name__ == "__main__":
    sys.exit(main())
