"""Versión de un solo archivo de un sitio generado, para verla o compartirla como una vista previa.

La versión buena para publicar es la carpeta (carga más rápido: las fotos van aparte y se cachean).
Esta incrusta las fuentes y una sola variante de cada foto dentro del HTML.

Uso: python3 -m edumashow.motor.unico muestras/lumbre muestras/lumbre.unico.html
"""
import base64
import mimetypes
import os
import re
import sys

PIXEL = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
mimetypes.add_type("image/avif", ".avif")
mimetypes.add_type("font/woff2", ".woff2")


def datauri(ruta):
    mime = mimetypes.guess_type(ruta)[0] or "application/octet-stream"
    with open(ruta, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def candidato_medio(srcset):
    c = [x.strip().rsplit(" ", 1) for x in srcset.split(",") if x.strip()]
    c = sorted(c, key=lambda p: int(p[1].rstrip("w")) if len(p) > 1 else 0)
    return c[len(c) // 2][0]


def construir(carpeta, salida):
    with open(os.path.join(carpeta, "index.html"), encoding="utf-8") as f:
        html = f.read()
    # el precargado de fuentes no hace falta cuando van incrustadas
    html = re.sub(r'<link rel="preload"[^>]*as="font"[^>]*>', "", html)
    # fuentes dentro del CSS
    html = re.sub(r"url\((assets/[^)]+\.woff2)\)", lambda m: f"url({datauri(os.path.join(carpeta, m.group(1)))})", html)

    def fuente(m):
        tag = m.group(0)
        s = re.search(r'srcset="([^"]+)"', tag)
        if not s:
            return tag
        uri = datauri(os.path.join(carpeta, candidato_medio(s.group(1))))
        tag = tag.replace(s.group(0), f'srcset="{uri}"')
        return re.sub(r'\s+sizes="[^"]*"', "", tag)

    html = re.sub(r"<source\b[^>]*>", fuente, html)
    html = re.sub(r'(<img\b[^>]*\bsrc=")(assets/[^"]+)(")', lambda m: m.group(1) + PIXEL + m.group(3), html)
    html = re.sub(r'data-vista="(assets/[^"]+)"', lambda m: f'data-vista="{datauri(os.path.join(carpeta, m.group(1)))}"', html)
    with open(salida, "w", encoding="utf-8") as f:
        f.write(html)
    return os.path.getsize(salida)


if __name__ == "__main__":
    n = construir(sys.argv[1], sys.argv[2])
    print(f"{sys.argv[2]}: {n // 1024} KB")
