"""Revisa fichas antes de construir: forma (esquema), reglas del motor, frases que el Gate rechazaría y detalles de oficio.

Uso:
    python3 scripts/validar_ficha.py FICHA.json [OTRA.json ...] [--completar] [--escribir] [--corregir] [--sin-fotos]

  --completar   añade las pruebas del Gate que no escribe quien redacta (el pedido de prueba) y lo muestra
  --escribir    con --completar, guarda el resultado en el mismo archivo
  --corregir    imprime el mensaje listo para pegar en el chat del modelo que escribió la ficha, con los errores
  --sin-fotos   no exige que los archivos de fotos existan (para revisar la forma antes de tener las fotos)

Sale con código 0 si ninguna ficha tiene errores, y 1 si alguna los tiene.
"""
import argparse
import json
import os
import sys

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, RAIZ)

from edumashow.motor import esquema_ficha  # noqa: E402


def revisar_archivo(ruta, completar=False, escribir=False, corregir=False, fotos=True):
    with open(ruta, encoding="utf-8") as f:
        crudo = f.read()
    try:
        F = json.loads(crudo)
    except json.JSONDecodeError as e:
        linea = crudo.splitlines()[e.lineno - 1] if 0 < e.lineno <= len(crudo.splitlines()) else ""
        err = [f"no es JSON válido: {e.msg} en la línea {e.lineno}, columna {e.colno}: {linea.strip()[:80]!r}"]
        print(f"\n{ruta}: ERRORES")
        for x in err:
            print("  -", x)
        if corregir:
            print("\n" + esquema_ficha.mensaje_para_corregir(err))
        return False
    if chr(0xAB) in crudo or chr(0xBB) in crudo:
        print(f"\n{ruta}: lleva comillas angulares; usa comillas rectas")
    if completar:
        hecho = esquema_ficha.completar(F)
        if hecho and escribir:
            with open(ruta, "w", encoding="utf-8") as g:
                json.dump(F, g, ensure_ascii=False, indent=1)
                g.write("\n")
    errores, avisos = esquema_ficha.revisar(F, ruta, comprobar_fotos=fotos)
    print(f"\n{ruta}: " + ("SIN ERRORES" if not errores else f"{len(errores)} ERRORES") + (f" y {len(avisos)} avisos" if avisos else ""))
    if completar:
        print("  completado:", ", ".join(hecho) if hecho else "nada que completar")
    for x in errores:
        print("  ERROR:", x)
    for x in avisos:
        print("  aviso:", x)
    if corregir and errores:
        print("\n--- Mensaje para pegar en el chat del modelo ---\n" + esquema_ficha.mensaje_para_corregir(errores))
    return not errores


def main(argv=None):
    ap = argparse.ArgumentParser(description="Revisa fichas de Edumashow antes de construir")
    ap.add_argument("fichas", nargs="+")
    ap.add_argument("--completar", action="store_true")
    ap.add_argument("--escribir", action="store_true")
    ap.add_argument("--corregir", action="store_true")
    ap.add_argument("--sin-fotos", action="store_true")
    a = ap.parse_args(argv)
    ok = True
    for r in a.fichas:
        ok = revisar_archivo(r, a.completar, a.escribir, a.corregir, not a.sin_fotos) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
