"""Trae tipografías libres (OFL) del paquete Fontsource de npm a edumashow/fuentes/ con su texto de licencia.

Cada fuente se pide como  id:pesos  donde los pesos van separados por comas y una i detrás marca la cursiva. Ejemplos:

    python3 scripts/traer_fuentes.py cormorant-garamond:500i,600 oswald:700 dm-sans:400,500,700

Para cada una descarga el paquete con `npm pack` en una carpeta temporal, lee solo los archivos latin WOFF2 de los pesos pedidos y el texto de la licencia
(sin extraer nada más del paquete), comprueba que cada archivo es una fuente válida y que su licencia es la OFL, y los guarda como
Nombre-PesoEstilo.woff2 y licencias/OFL_nombre.txt. Anota de dónde viene cada archivo en edumashow/fuentes/ORIGEN.md.
"""
import argparse
import io
import os
import re
import subprocess
import sys
import tarfile
import tempfile

from fontTools.ttLib import TTFont

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FUENTES = os.path.join(RAIZ, "edumashow", "fuentes")
NOMBRES_PESO = {100: "Thin", 200: "ExtraLight", 300: "Light", 400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold", 800: "ExtraBold", 900: "Black"}


def nombre_de_familia(id_):
    return "".join(p.capitalize() for p in id_.split("-"))


def pedir(id_, pesos, trabajo):
    """Descarga el paquete y devuelve ({(peso, estilo): bytes}, licencia, version)."""
    r = subprocess.run(["npm", "pack", f"@fontsource/{id_}", "--silent"], cwd=trabajo, capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        raise RuntimeError(f"npm pack @fontsource/{id_} falló: {r.stderr.strip()[:200]}")
    tgz = os.path.join(trabajo, r.stdout.strip().splitlines()[-1])
    version = re.search(r"-(\d+\.\d+\.\d+)\.tgz$", tgz)
    out, licencia = {}, None
    with tarfile.open(tgz) as t:
        nombres = {m.name for m in t.getmembers()}
        for peso, estilo in pesos:
            n = f"package/files/{id_}-latin-{peso}-{estilo}.woff2"
            if n not in nombres:
                raise RuntimeError(f"{id_}: el paquete no tiene el peso {peso} {estilo} (hay: {sorted(x.split('/')[-1] for x in nombres if x.endswith('-latin-400-normal.woff2') or '-latin-' in x)[:12]}...)")
            out[(peso, estilo)] = t.extractfile(n).read()
        if "package/LICENSE" in nombres:
            licencia = t.extractfile("package/LICENSE").read().decode("utf-8", "replace")
    return out, licencia, (version.group(1) if version else "?")


def main():
    ap = argparse.ArgumentParser(description="Trae tipografías OFL de Fontsource")
    ap.add_argument("fuentes", nargs="+", help="id:pesos (por ejemplo oswald:700 o lora:400,400i)")
    a = ap.parse_args()
    ok = True
    for pedido in a.fuentes:
        id_, _, pesos_txt = pedido.partition(":")
        pesos = []
        for p in pesos_txt.split(","):
            m = re.fullmatch(r"(\d{3})(i?)", p.strip())
            if not m:
                print(f"{pedido}: peso no válido {p!r}")
                ok = False
                continue
            pesos.append((int(m.group(1)), "italic" if m.group(2) else "normal"))
        if not pesos:
            continue
        try:
            with tempfile.TemporaryDirectory(prefix="fontsource_") as trabajo:
                archivos, licencia, version = pedir(id_, pesos, trabajo)
        except Exception as e:  # noqa: BLE001
            print(f"{id_}: {e}")
            ok = False
            continue
        if not licencia or "SIL OPEN FONT LICENSE" not in licencia.upper():
            print(f"{id_}: el paquete no trae la licencia OFL; no se guarda")
            ok = False
            continue
        familia = nombre_de_familia(id_)
        guardados = []
        for (peso, estilo), datos in archivos.items():
            f = TTFont(io.BytesIO(datos))   # que sea una fuente de verdad (lanza si el archivo está dañado)
            if f.flavor != "woff2" or "cmap" not in f:
                raise RuntimeError(f"{id_} {peso} {estilo}: no es una fuente WOFF2 válida")
            nombre = f"{familia}-{NOMBRES_PESO[peso]}{'Italic' if estilo == 'italic' else ''}.woff2"
            with open(os.path.join(FUENTES, nombre), "wb") as g:
                g.write(datos)
            guardados.append(nombre)
        with open(os.path.join(FUENTES, "licencias", f"OFL_{id_.replace('-', '')}.txt"), "w", encoding="utf-8") as g:
            g.write(licencia.strip() + "\n")
        with open(os.path.join(FUENTES, "ORIGEN.md"), "a", encoding="utf-8") as g:
            g.write(f"- {', '.join(guardados)}: paquete @fontsource/{id_} {version} de npm (subconjunto latin, licencia SIL OFL 1.1 en licencias/OFL_{id_.replace('-', '')}.txt)\n")
        print(f"{id_} {version}: {', '.join(guardados)}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
