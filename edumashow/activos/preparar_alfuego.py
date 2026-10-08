"""Prepara los activos de Al Fuego Grill a partir de las capturas de pantalla que envió Eduardo.

Las capturas son del Instagram público del restaurante (@alfuego_grill) y de su menú. Este script
recorta, sin tocar el contenido de la foto, solo lo necesario y deja cada recorte en
edumashow/activos/origen/alfuego/ con su procedencia anotada. No inventa detalle: no escala ni retoca.

Uso: python3 edumashow/activos/preparar_alfuego.py CARPETA_CON_LAS_CAPTURAS
Las capturas se identifican por su nombre de archivo (ver CAPTURAS).
"""
import hashlib
import json
import os
import sys

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
DESTINO = os.path.join(AQUI, "origen", "alfuego")

CAPTURAS = {
    "logo": "a8de67ff-image.png",      # pantalla de carga de Instagram con el logo
    "perfil": "fab81f07-image.png",    # perfil con la cuadricula de fotos
    "cuadricula": "ece0c8f8-image.png",  # mas fotos de la cuadricula
    "volante": "89ee87ca-image.png",   # volante con logo, telefono y direccion
    "menu": "e9f05eca-image.jpg",      # menu impreso con precios
}

# columnas y filas de la cuadricula de Instagram, en pixeles de la captura original (1179 de ancho)
COLS = [(0, 391), (395, 783), (788, 1179)]
FILAS = {"perfil": [(1241, 1762), (1766, 2286)], "cuadricula": [(459, 979), (983, 1503), (1507, 2027), (2031, 2550)]}
INSET = 3  # recorta unos pixeles de borde para no arrastrar la separacion entre fotos
ARRIBA = 72  # las fotos de la cuadricula traen el icono de video de Instagram arriba a la derecha: se recorta, no se borra

# clave: (captura, fila, columna, descripcion para el alt)
FOTOS = {
    "picada": ("perfil", 0, 1, "Picada de carnes a la parrilla sobre una tabla de madera, con papas fritas"),
    "tostones": ("perfil", 0, 2, "Tostones con carne asada, cebolla, queso y salsa verde sobre una bandeja"),
    "sandwich": ("cuadricula", 0, 1, "Sándwich de churrasco con papas fritas en un envase para llevar"),
    "lomo": ("cuadricula", 3, 2, "Lomo de cerdo envuelto en tocino con chorizo sobre una tabla con el logo de Al Fuego Grill"),
    "asador": ("perfil", 1, 2, "Asador vertical con brochetas y cortes de carne sobre brasas"),
    "trailer": ("perfil", 1, 0, "El trailer de Al Fuego Grill con su logo y teléfono"),
}

# logo: circulo del emblema en la captura (centro y radio medidos sobre los pixeles saturados del aro de fuego)
LOGO_CENTRO = (590, 1100)
LOGO_RADIO = 388


def sha256(ruta):
    with open(ruta, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main(carpeta):
    os.makedirs(DESTINO, exist_ok=True)
    abiertas = {k: Image.open(os.path.join(carpeta, n)).convert("RGB") for k, n in CAPTURAS.items()}
    registro = {"capturas": {k: {"archivo": n, "sha256": sha256(os.path.join(carpeta, n))} for k, n in CAPTURAS.items()}, "recortes": {}}

    for clave, (cap, fila, col, _alt) in FOTOS.items():
        x0, x1 = COLS[col]
        y0, y1 = FILAS[cap][fila]
        caja = (x0 + INSET, y0 + ARRIBA, x1 - INSET, y1 - INSET)
        im = abiertas[cap].crop(caja)
        im.save(os.path.join(DESTINO, clave + ".webp"), "WEBP", lossless=True, method=6)
        registro["recortes"][clave] = {"captura": cap, "caja": list(caja), "tam": list(im.size)}

    # logo con transparencia: circulo con borde suave de dos pixeles
    cx, cy = LOGO_CENTRO
    R = LOGO_RADIO
    c = abiertas["logo"].crop((cx - R - 4, cy - R - 4, cx + R + 4, cy + R + 4))
    w, S = c.width, 4
    m = Image.new("L", (w * S, w * S), 0)
    ImageDraw.Draw(m).ellipse((4 * S, 4 * S, (w - 4) * S, (w - 4) * S), fill=255)
    m = m.resize((w, w), Image.LANCZOS)
    logo = c.convert("RGBA")
    logo.putalpha(m)
    logo.save(os.path.join(DESTINO, "logo.png"), optimize=True)
    registro["recortes"]["logo"] = {"captura": "logo", "centro": [cx, cy], "radio": R, "tam": list(logo.size)}

    with open(os.path.join(DESTINO, "recortes.json"), "w", encoding="utf-8") as f:
        json.dump(registro, f, ensure_ascii=False, indent=1)
    print("listo:", sorted(os.listdir(DESTINO)))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
