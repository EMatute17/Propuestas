"""Revisa que ningún archivo de texto del repositorio contenga comillas angulares dobles.

Uso: python3 scripts/revisar_comillas.py [ruta ...]
Sin argumentos revisa todo el repositorio (excepto .git y node_modules).
Sale con código 1 si encuentra alguna. Los caracteres se escriben por su código
para que este archivo tampoco los contenga.
"""
import os
import sys

PROHIBIDOS = {chr(0xAB): "U+00AB", chr(0xBB): "U+00BB"}
SALTAR = {".git", "node_modules", "__pycache__"}
BINARIOS = (".png", ".jpg", ".jpeg", ".webp", ".avif", ".woff2", ".woff", ".ttf", ".zip", ".mp4", ".webm", ".ico", ".pdf")


def archivos(raiz):
    if os.path.isfile(raiz):
        yield raiz
        return
    for dp, dn, fn in os.walk(raiz):
        dn[:] = [d for d in dn if d not in SALTAR]
        for f in fn:
            if not f.lower().endswith(BINARIOS):
                yield os.path.join(dp, f)


def main(rutas):
    malos = []
    for r in rutas:
        for p in archivos(r):
            try:
                txt = open(p, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            for n, linea in enumerate(txt.splitlines(), 1):
                for ch, cod in PROHIBIDOS.items():
                    if ch in linea:
                        malos.append((p, n, cod))
    for p, n, cod in malos:
        print(f"{p}:{n}: comilla angular {cod}")
    print("comillas angulares encontradas:", len(malos))
    return 1 if malos else 0


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.exit(main(sys.argv[1:] or [base]))
