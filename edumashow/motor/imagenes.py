"""Procesado de imágenes: recortes, escalado, AVIF, WebP, JPEG de respaldo, miniatura borrosa y color medio.

Reglas que implementa (ver nucleo/reglas.json): R-REN-02 (formatos modernos con srcset, sin duplicados,
dimensiones declaradas) y R-DAT-04 (procedencia y licencia registradas en el manifiesto de activos).
"""
import base64
import hashlib
import io
import os

from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

try:  # el complemento AVIF se registra solo al importarlo
    import pillow_avif  # noqa: F401
    HAY_AVIF = True
except Exception:  # pragma: no cover
    HAY_AVIF = False

CALIDAD = {"avif": 46, "webp": 72, "jpg": 78}


def abrir(ruta):
    im = Image.open(ruta)
    im.load()
    if im.mode in ("RGBA", "LA", "P"):
        fondo = Image.new("RGB", im.size, (255, 255, 255))
        im = im.convert("RGBA")
        fondo.paste(im, mask=im.split()[-1])
        return fondo
    return im.convert("RGB")


def abrir_rgba(ruta):
    """Abre una imagen conservando la transparencia (para logotipos)."""
    im = Image.open(ruta)
    im.load()
    return im.convert("RGBA")


def ajustar(im, contraste=1.0, color=1.0, brillo=1.0):
    if contraste != 1.0:
        im = ImageEnhance.Contrast(im).enhance(contraste)
    if color != 1.0:
        im = ImageEnhance.Color(im).enhance(color)
    if brillo != 1.0:
        im = ImageEnhance.Brightness(im).enhance(brillo)
    return im


def recorte_relativo(im, razon_ancho_alto, foco=(0.5, 0.5)):
    """Recorta a una proporción dada (ancho/alto) centrando en el foco relativo (x, y entre 0 y 1)."""
    w, h = im.size
    if w / h > razon_ancho_alto:  # imagen más ancha: se recorta a los lados
        nw = round(h * razon_ancho_alto)
        x0 = min(max(round(foco[0] * w - nw / 2), 0), w - nw)
        return im.crop((x0, 0, x0 + nw, h))
    nh = round(w / razon_ancho_alto)
    y0 = min(max(round(foco[1] * h - nh / 2), 0), h - nh)
    return im.crop((0, y0, w, y0 + nh))


def escalar_a_ancho(im, ancho):
    if im.width == ancho:
        return im
    alto = max(1, round(im.height * ancho / im.width))
    r = im.resize((ancho, alto), Image.LANCZOS)
    if ancho > im.width:  # al ampliar, un afinado ligero compensa la suavidad
        r = r.filter(ImageFilter.UnsharpMask(radius=1.1, percent=45, threshold=2))
    return r


def color_medio(im):
    px = im.resize((1, 1), Image.BOX).getpixel((0, 0))
    return "#%02x%02x%02x" % px[:3]


def lqip_datauri(im, ancho=24):
    """Miniatura borrosa diminuta (unos 300 bytes) para pintar color antes de que llegue la imagen."""
    alto = max(1, round(im.height * ancho / im.width))
    p = im.resize((ancho, alto), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.6))
    b = io.BytesIO()
    p.save(b, "JPEG", quality=40, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def guardar(im, ruta_sin_ext, formato, calidad=None):
    ext = {"avif": "avif", "webp": "webp", "jpg": "jpg", "png": "png"}[formato]
    ruta = f"{ruta_sin_ext}.{ext}"
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    if formato == "avif":
        im.save(ruta, "AVIF", quality=calidad or CALIDAD["avif"], speed=6)
    elif formato == "webp":
        extra = {"alpha_quality": 100} if im.mode == "RGBA" else {}
        im.save(ruta, "WEBP", quality=calidad or CALIDAD["webp"], method=5, **extra)
    elif formato == "png":
        im.save(ruta, "PNG", optimize=True)
    else:
        im.save(ruta, "JPEG", quality=calidad or CALIDAD["jpg"], optimize=True, progressive=True)
    return ruta


class Activos:
    """Gestiona las imágenes de una web: las procesa, evita duplicados y escribe el registro."""

    def __init__(self, carpeta_sitio, prefijo="assets/img"):
        self.carpeta = carpeta_sitio
        self.prefijo = prefijo
        self.registro = []   # una entrada por imagen única
        self._por_hash = {}

    def _hash(self, im):
        return hashlib.sha1(im.tobytes()).hexdigest()[:10]

    def procesar(self, clave, im_origen, anchos, procedencia, recorte=None, ajustes=None,
                 jpg_ancho=None, formatos=("avif", "webp")):
        """Genera las variantes de una imagen. Devuelve los datos para construir un picture."""
        im = im_origen
        if recorte:
            im = recorte_relativo(im, recorte["razon"], recorte.get("foco", (0.5, 0.5)))
        if ajustes:
            im = ajustar(im, **ajustes)
        h = self._hash(im)
        if h in self._por_hash:  # misma imagen ya procesada: se reutilizan los archivos
            return self._por_hash[h]
        nativo = im.width
        anchos = sorted(set(anchos))
        variantes = {f: [] for f in formatos}
        for a in anchos:
            r = escalar_a_ancho(im, a)
            base = os.path.join(self.carpeta, self.prefijo, f"{clave}-{a}")
            for f in formatos:
                if f == "avif" and not HAY_AVIF:
                    continue
                guardar(r, base, f)
                variantes[f].append((f"{self.prefijo}/{clave}-{a}.{f}", a))
        # JPEG de respaldo: del ancho pedido o del mayor que no pase de 1280
        ja = jpg_ancho or max([a for a in anchos if a <= 1280] or [anchos[0]])
        rj = escalar_a_ancho(im, ja)
        guardar(rj, os.path.join(self.carpeta, self.prefijo, f"{clave}-{ja}"), "jpg")
        datos = {
            "clave": clave, "ancho": im.width, "alto": im.height, "nativo": nativo,
            "variantes": variantes, "jpg": f"{self.prefijo}/{clave}-{ja}.jpg", "jpg_ancho": ja,
            "lqip": lqip_datauri(im), "color": color_medio(im),
            "proporcion": f"{im.width} / {im.height}",
        }
        reg = dict(procedencia)
        reg.update({"clave": clave, "ancho_origen": im_origen.width, "alto_origen": im_origen.height,
                    "ancho_nativo": im.width, "alto_nativo": im.height,
                    "anchos_generados": anchos, "ampliada": max(anchos) > nativo})
        self.registro.append(reg)
        self._por_hash[h] = datos
        return datos

    def procesar_logo(self, clave, im_rgba, anchos, procedencia):
        """Logotipo con transparencia: AVIF y WebP con alfa y un PNG de respaldo. Nunca se amplía ni se recorta."""
        anchos = sorted({a for a in anchos if a <= im_rgba.width}) or [im_rgba.width]
        variantes = {"avif": [], "webp": []}
        for a in anchos:
            r = escalar_a_ancho(im_rgba, a)
            base = os.path.join(self.carpeta, self.prefijo, f"{clave}-{a}")
            if HAY_AVIF:
                guardar(r, base, "avif", calidad=60)
                variantes["avif"].append((f"{self.prefijo}/{clave}-{a}.avif", a))
            guardar(r, base, "webp", calidad=86)
            variantes["webp"].append((f"{self.prefijo}/{clave}-{a}.webp", a))
        pa = anchos[len(anchos) // 2]
        guardar(escalar_a_ancho(im_rgba, pa), os.path.join(self.carpeta, self.prefijo, f"{clave}-{pa}"), "png")
        mayor = anchos[-1]
        alto = max(1, round(im_rgba.height * mayor / im_rgba.width))
        datos = {"clave": clave, "ancho": mayor, "alto": alto, "nativo": im_rgba.width, "variantes": variantes,
                 "fallback": f"{self.prefijo}/{clave}-{pa}.png", "proporcion": f"{im_rgba.width} / {im_rgba.height}"}
        reg = dict(procedencia)
        reg.update({"clave": clave, "ancho_origen": im_rgba.width, "alto_origen": im_rgba.height,
                    "ancho_nativo": im_rgba.width, "alto_nativo": im_rgba.height,
                    "anchos_generados": anchos, "ampliada": False, "con_transparencia": True})
        self.registro.append(reg)
        return datos


def picture_html(datos, alt, sizes, clases="", extra_attrs="", prioridad=False, ancho_img=None, alto_img=None, lazy=True):
    """Construye un picture con AVIF y WebP y un JPEG de respaldo. Las dimensiones evitan saltos de diseño."""
    from html import escape
    partes = ['<picture>']
    for f, tipo in (("avif", "image/avif"), ("webp", "image/webp")):
        v = datos["variantes"].get(f)
        if v:
            srcset = ", ".join(f"{u} {a}w" for u, a in v)
            partes.append(f'<source type="{tipo}" srcset="{srcset}" sizes="{sizes}">')
    w = ancho_img or datos["ancho"]
    h = alto_img or datos["alto"]
    carga = 'fetchpriority="high" decoding="async"' if prioridad else ('loading="lazy" decoding="async"' if lazy else 'decoding="async"')
    cl = f' class="{clases}"' if clases else ""
    partes.append(f'<img{cl} src="{datos.get("fallback") or datos["jpg"]}" alt="{escape(alt, quote=True)}" width="{w}" height="{h}" {carga} {extra_attrs}>'.replace("  ", " ").replace(" >", ">"))
    partes.append("</picture>")
    return "".join(partes)


def imagen_og(hero_im, nombre, lema, ttf_display, ttf_texto, destino, color_fondo=(11, 20, 28)):
    """Imagen de vista previa para compartir el enlace (1200 por 630): foto oscurecida, nombre y lema."""
    W, H = 1200, 630
    base = recorte_relativo(hero_im, W / H, (0.5, 0.45))
    base = base.resize((W, H), Image.LANCZOS)
    velo = Image.new("RGB", (W, H), color_fondo)
    degradado = Image.linear_gradient("L").resize((W, H))      # negro arriba, blanco abajo
    mascara = degradado.point(lambda v: int(60 + v * 0.62))
    base = Image.composite(velo, base, mascara)
    d = ImageDraw.Draw(base)
    f1 = ImageFont.truetype(ttf_display, 168)
    f2 = ImageFont.truetype(ttf_texto, 34)
    d.text((72, 300), nombre, font=f1, fill=(243, 233, 216))
    d.text((78, 520), lema, font=f2, fill=(243, 233, 216))
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    base.save(destino, "JPEG", quality=82, optimize=True, progressive=True)
    return os.path.getsize(destino)


def imagen_og_logo(logo_rgba, lineas, lema, ttf_display, ttf_texto, destino,
                   color_fondo=(11, 9, 8), color_texto=(246, 239, 230), color_acento=(255, 122, 26)):
    """Vista previa para compartir el enlace cuando no hay foto de portada: fondo oscuro con brillo de brasa,
    el logotipo a su tamaño y el nombre en letras de titular (1200 por 630). No inventa ninguna imagen."""
    W, H = 1200, 630
    base = Image.new("RGB", (W, H), color_fondo)
    radial = Image.radial_gradient("L").resize((1000, 1000), Image.LANCZOS)   # negro en el centro, blanco en el borde
    luz = radial.point(lambda v: int(max(0, 255 - v) * 0.42))
    base.paste(Image.new("RGB", (1000, 1000), color_acento), (-260, 330), luz)
    lado = 430
    logo = logo_rgba.resize((lado, lado), Image.LANCZOS)
    base.paste(logo, (86, (H - lado) // 2 - 6), logo)
    d = ImageDraw.Draw(base)
    n = len(lineas)
    tam = 168 if n <= 2 else 124
    f1 = ImageFont.truetype(ttf_display, tam)
    f2 = ImageFont.truetype(ttf_texto, 34)
    alto_bloque = n * int(tam * 0.98)
    y = (H - alto_bloque) // 2 - 40
    for i, t in enumerate(lineas):
        d.text((580, y), t.upper(), font=f1, fill=color_acento if (n > 1 and i == n - 1) else color_texto)
        y += int(tam * 0.98)
    d.text((584, y + 18), lema, font=f2, fill=color_texto)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    base.save(destino, "JPEG", quality=84, optimize=True, progressive=True)
    return os.path.getsize(destino)
