"""Versión de un solo archivo de un sitio generado, para verla o compartirla como una vista previa.

La versión buena para publicar es la carpeta (carga más rápido: las fotos van aparte y se cachean).
Esta incrusta las fuentes y una sola variante de cada foto dentro del HTML.

No necesita JavaScript para mostrar nada: hay visores de teléfono (los de mensajería, correo o nube) que no lo
ejecutan, y una vista previa que depende de él se vería sin fotos. Por eso:
  - cada foto con significado va como etiqueta img con su imagen WebP incrustada (sin picture ni srcset);
  - el mural de la portada repite sus fotos muchas veces, así que cada foto se guarda una sola vez como una
    clase de CSS con la foto de fondo y las teselas solo la nombran.

Uso: python3 -m edumashow.motor.unico muestras/lumbre muestras/lumbre.unico.html
"""
import base64
import mimetypes
import os
import re
import sys

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


def _webp_de(picture):
    """Ruta relativa del WebP de un picture (el candidato de tamaño medio), o None si no tiene."""
    for tag in re.findall(r"<source\b[^>]*>", picture):
        if 'type="image/webp"' in tag:
            s = re.search(r'srcset="([^"]+)"', tag)
            if s:
                return candidato_medio(s.group(1))
    return None


def construir(carpeta, salida):
    with open(os.path.join(carpeta, "index.html"), encoding="utf-8") as f:
        html = f.read()
    # el precargado de fuentes no hace falta cuando van incrustadas
    html = re.sub(r'<link rel="preload"[^>]*as="font"[^>]*>', "", html)
    # fuentes dentro del CSS
    html = re.sub(r"url\((assets/[^)]+\.woff2)\)", lambda m: f"url({datauri(os.path.join(carpeta, m.group(1)))})", html)

    # 1) teselas del mural: una clase de CSS por foto, y la tesela solo la nombra
    clases, reglas = {}, []

    def tesela(m):
        webp = _webp_de(m.group(2))
        if not webp:
            return m.group(0)
        if webp not in clases:
            clases[webp] = f"fz{len(clases)}"
            reglas.append(f".tesela.{clases[webp]}{{background-image:url({datauri(os.path.join(carpeta, webp))})}}")
        return f'<div class="tesela {clases[webp]}" style="{m.group(1)}"></div>'

    html = re.sub(r'<div class="tesela" style="([^"]*)">(<picture>.*?</picture>)</div>', tesela, html, flags=re.S)
    if reglas:
        base = ".tesela{background-size:cover;background-position:50% 50%;background-repeat:no-repeat}"
        html = html.replace("</head>", "<style>" + base + "".join(reglas) + "</style></head>", 1)

    # 2) el resto de las fotos: img con el WebP incrustado
    def foto(m):
        pic = m.group(0)
        webp = _webp_de(pic)
        img = re.search(r"<img\b[^>]*>", pic)
        if not img:
            return pic
        tag = img.group(0)
        ruta = webp or (re.search(r'\bsrc="(assets/[^"]+)"', tag) or [None, None])[1]
        if not ruta:
            return pic
        tag = re.sub(r'\bsrc="[^"]*"', lambda _: f'src="{datauri(os.path.join(carpeta, ruta))}"', tag, count=1)
        return "<picture>" + tag + "</picture>"

    html = re.sub(r"<picture>.*?</picture>", foto, html, flags=re.S)
    html = re.sub(r'data-vista="(assets/[^"]+)"', lambda m: f'data-vista="{datauri(os.path.join(carpeta, m.group(1)))}"', html)
    with open(salida, "w", encoding="utf-8") as f:
        f.write(html)
    return os.path.getsize(salida)


if __name__ == "__main__":
    n = construir(sys.argv[1], sys.argv[2])
    print(f"{sys.argv[2]}: {n // 1024} KB")
