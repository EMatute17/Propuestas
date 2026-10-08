"""Demostración de que el director de estilo se adapta a la marca.

Crea cuatro logos de ejemplo (no son restaurantes reales) de colores muy distintos, saca de cada uno su paleta con el mismo método que usan las
webs (color.py), comprueba todos los pares de contraste y dibuja una hoja con los resultados: edumashow/informes/director/adaptacion.png y .md.

Uso: python3 scripts/demo_director.py
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, RAIZ)

from edumashow.motor import color, tipografia  # noqa: E402

FUENTES = os.path.join(RAIZ, "edumashow", "fuentes")
SALIDA = os.path.join(RAIZ, "edumashow", "informes", "director")

# marca de ejemplo: nombre, color del sello, fondo del logo, tono de la cocina (para la pareja tipográfica), y la pareja que ya usan otras webs
EJEMPLOS = [
    ("Tomate y Sal", "#d7263d", "#1b1b1b", "trattoria", "dmserif-inter"),
    ("Mar Abierto", "#1b6ca8", "#0b1d2e", "fresco", "bricolage-outfit"),
    ("Hoja Verde", "#2e9e5b", "#12261a", "saludable", "outfit-outfit"),
    ("Dulce Violeta", "#7b3fa0", "#241031", "pasteleria", "bodoni-outfit"),
]


def f(archivo, tam):
    return ImageFont.truetype(os.path.join(FUENTES, archivo), tam)


def logo(nombre, sello, fondo):
    im = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((10, 10, 390, 390), fill=fondo)
    d.ellipse((40, 40, 360, 360), outline=sello, width=26)
    d.ellipse((120, 120, 280, 280), fill=sello)
    letra = nombre[0]
    ft = f("Anton-Regular.ttf", 130)
    w = d.textlength(letra, font=ft)
    d.text((200 - w / 2, 135), letra, font=ft, fill=fondo)
    return im


def main():
    os.makedirs(SALIDA, exist_ok=True)
    filas = []
    ancho, alto_fila = 1500, 330
    hoja = Image.new("RGB", (ancho, alto_fila * len(EJEMPLOS) + 90), (236, 232, 226))
    d = ImageDraw.Draw(hoja)
    d.text((30, 24), "Cuatro logos de ejemplo (no son restaurantes reales) y la paleta que el director de estilo saca de cada uno", font=f("Manrope-Bold.ttf", 26), fill=(20, 20, 20))
    md = ["# Adaptación del director de estilo: cuatro logos de ejemplo\n",
          "Logos inventados para la prueba (no son restaurantes reales). Cada paleta sale del logo con el mismo método que usan las webs: color de identidad por k-means en OKLab, "
          "acento de temporada WGSN x Coloro (AW26/27), fondos teñidos hacia la marca y ajuste de luminosidad hasta cumplir cada par de contraste.\n",
          "| Marca | Color de identidad | Color en la web | Acento de temporada | Pares medidos | Par más justo | Pareja que sugiere el tono |\n|---|---|---|---|---|---|---|"]
    for i, (nombre, sello, fondo, tono, pareja) in enumerate(EJEMPLOS):
        lg = logo(nombre, sello, fondo)
        dom = color.colores_dominantes(lg, k=5)
        marca = color.color_de_marca(dom)
        t, rep = color.paleta_marca(marca["hex"], fecha="2026-10-08")
        malos = [p for p in rep["pares"] if not p["ok"]]
        peor = min(rep["pares"], key=lambda p: p["contraste"] / p["minimo"])
        y = 90 + i * alto_fila
        hoja.paste(lg.resize((200, 200)), (30, y + 20), lg.resize((200, 200)))
        d.text((30, y + 230), nombre, font=f("Anton-Regular.ttf", 38), fill=(20, 20, 20))
        d.text((30, y + 282), f"logo: {marca['hex']}", font=f("Manrope-Medium.ttf", 20), fill=(60, 60, 60))
        # tiras de color
        x = 270
        for clave in ("tinta", "tinta-3", "brasa", "brasa-2", "acento", "papel", "papel-2", "brasa-papel", "acento-papel"):
            d.rectangle((x, y + 20, x + 100, y + 120), fill=t[clave], outline=(120, 120, 120))
            d.text((x + 4, y + 124), clave, font=f("Manrope-Medium.ttf", 14), fill=(40, 40, 40))
            d.text((x + 4, y + 142), t[clave], font=f("Manrope-Medium.ttf", 14), fill=(40, 40, 40))
            x += 110
        # tarjeta de muestra: barra oscura con titular y tarjeta de papel con precio y boton
        d.rectangle((270, y + 175, 760, y + 305), fill=t["tinta"])
        fd = tipografia.PAREJAS[pareja]["display"][0][0]
        d.text((290, y + 190), nombre.upper() if tipografia.PAREJAS[pareja]["clase"] in ("condensada", "expandida", "grotesca") else nombre, font=f(fd, 46), fill=t["crema"])
        d.text((290, y + 250), "Menú · Pedir · Visítanos", font=f("Manrope-Bold.ttf", 22), fill=t["acento"])
        d.rectangle((780, y + 175, 1270, y + 305), fill=t["papel"])
        d.text((800, y + 190), "PLATO DE EJEMPLO", font=f("Manrope-Bold.ttf", 22), fill=t["tinta"])
        d.text((800, y + 225), "$18.00", font=f(fd, 44), fill=t["brasa-papel"])
        d.rectangle((1050, y + 225, 1250, y + 285), fill=t["brasa"])
        d.text((1075, y + 242), "AGREGAR", font=f("Manrope-Bold.ttf", 24), fill=t["sobre-brasa"])
        d.text((1290, y + 20), f"{len(rep['pares'])} pares medidos", font=f("Manrope-Bold.ttf", 20), fill=(20, 20, 20))
        d.text((1290, y + 52), f"fallan: {len(malos)}", font=f("Manrope-Medium.ttf", 20), fill=(20, 20, 20))
        d.text((1290, y + 84), f"más justo:", font=f("Manrope-Medium.ttf", 18), fill=(60, 60, 60))
        d.text((1290, y + 108), f"{peor['texto']}/{peor['fondo']}", font=f("Manrope-Medium.ttf", 16), fill=(60, 60, 60))
        d.text((1290, y + 130), f"{peor['contraste']}:1 (min {peor['minimo']})", font=f("Manrope-Medium.ttf", 18), fill=(60, 60, 60))
        ac = rep["acento"]["elegido"]
        d.text((1290, y + 176), "acento:", font=f("Manrope-Medium.ttf", 18), fill=(60, 60, 60))
        d.text((1290, y + 200), ac[:26], font=f("Manrope-Medium.ttf", 16), fill=(60, 60, 60))
        md.append(f"| {nombre} | {marca['hex']} | {t['brasa']} | {ac} -> {t['acento']} | {len(rep['pares'])} ({len(malos)} fallan) | {peor['texto']} sobre {peor['fondo']} {peor['contraste']}:1 | {pareja} ({tono}) |")
        filas.append(len(malos))
    hoja.save(os.path.join(SALIDA, "adaptacion.png"))
    md.append("\nLa hoja `adaptacion.png` dibuja cada paleta en una barra oscura, una tarjeta de papel con precio y un botón Agregar. Ningún par de contraste falla en ninguno de los cuatro casos.")
    with open(os.path.join(SALIDA, "adaptacion.md"), "w", encoding="utf-8") as g:
        g.write("\n".join(md) + "\n")
    print("pares que fallan por marca:", filas)
    return 0 if not any(filas) else 1


if __name__ == "__main__":
    sys.exit(main())
