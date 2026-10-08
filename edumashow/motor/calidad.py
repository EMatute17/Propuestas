"""Calidad y procedencia de las fotos (R-FOT-01 y R-FOT-02, ordenes de Eduardo del 2026-10-08).

Dos revisiones:
  - `revisar_procedencia`: solo mira la ficha. Ninguna foto viene de una red social (salvo el logo), las fotos de banco
    libre traen autor, licencia y enlace, y las de referencia o generadas solo valen en un ejemplo ficticio.
  - `revisar_archivos`: mide los originales. Lado largo minimo (2400 px la portada, 1600 las demas, 640 el logo),
    calidad de compresion de los JPEG y, como aviso, si la foto parece ampliada o muy suavizada.

El mismo criterio lo aplica el validador de fichas (antes de construir) y el Gate (sobre el paquete). Esta regla no tiene excepciones.
"""
import os
import re

import numpy as np
from PIL import Image

MINIMOS = {"portada": 2400, "otras": 1600, "logo": 640}
DETALLE_AVISO = 0.12                      # por debajo, la foto parece ampliada o muy suavizada (solo aviso)
JPEG_MINIMA, JPEG_AVISO = 60, 80          # calidad estimada: por debajo de 60 es error; entre 60 y 79, aviso
ORIGENES = ("propia_del_restaurante", "banco_libre", "redes_del_restaurante", "referencia", "generada")
SOLO_EJEMPLO = ("referencia", "generada")
PISTAS_REDES = re.compile(r"instagram|cdninstagram|fbcdn|scontent|facebook|tiktok|pinterest|\bfb\.com", re.I)
# tabla de cuantizacion de luminancia de referencia (JPEG anexo K); solo su suma importa para estimar la calidad
_TABLA_BASE = [16, 11, 10, 16, 24, 40, 51, 61, 12, 12, 14, 19, 26, 58, 60, 55, 14, 13, 16, 24, 40, 57, 69, 56, 14, 17, 22, 29, 51, 87, 80, 62,
               18, 22, 37, 56, 68, 109, 103, 77, 24, 35, 55, 64, 81, 104, 113, 92, 49, 64, 78, 87, 103, 121, 120, 101, 72, 92, 95, 98, 112, 100, 103, 99]


def tipo_de(clave):
    return "portada" if clave == "hero" else ("logo" if clave == "logo" else "otras")


def minimo_de(clave):
    return MINIMOS[tipo_de(clave)]


def procedencia_de(F, clave):
    """Procedencia efectiva de un activo: la general de la ficha afinada por la suya."""
    p = dict(F.get("procedencia_activos") or {})
    p.update((F.get("activos", {}).get(clave) or {}).get("procedencia") or {})
    return p


# ------------------------------------------------------------------ procedencia (solo la ficha)
def revisar_procedencia(F):
    """Devuelve (errores, avisos) sobre el origen declarado de cada foto."""
    errores, avisos = [], []
    ficticio = bool((F.get("muestra") or {}).get("ejemplo_ficticio"))
    for clave, a in (F.get("activos") or {}).items():
        if not isinstance(a, dict):
            continue
        p = procedencia_de(F, clave)
        origen = p.get("origen")
        donde = f"activos.{clave}"
        es_logo = clave == "logo"
        if not origen:
            errores.append(f"{donde}.procedencia.origen: falta (propia_del_restaurante o banco_libre)")
            continue
        if origen not in ORIGENES:
            errores.append(f"{donde}.procedencia.origen: valor no permitido ({origen!r})")
            continue
        if origen == "redes_del_restaurante" and not es_logo:
            errores.append(f"{donde}: foto sacada de redes sociales. Solo el logo puede venir de una red (R-FOT-01); pide la foto original al restaurante como archivo, o usa un banco libre")
        if origen in SOLO_EJEMPLO and not ficticio:
            errores.append(f"{donde}: una foto {origen.replace('_', ' ')} solo se admite en un ejemplo ficticio rotulado; en un negocio real usa fotos propias del restaurante o de un banco libre")
        if origen == "banco_libre":
            for k, nombre in (("autor", "el autor"), ("licencia", "la licencia"), ("url", "el enlace a la página de la foto")):
                if not p.get(k):
                    errores.append(f"{donde}.procedencia.{k}: falta {nombre} (una foto de banco libre lleva autor, licencia y enlace)")
        if not es_logo and origen != "redes_del_restaurante":   # una foto de redes con otro origen declarado: se delata por su enlace, su descripcion o su nombre
            pistas = [str(p.get(k, "")) for k in ("url", "descripcion", "autor")] + [str(a.get("archivo", ""))]
            hit = next((PISTAS_REDES.search(t) for t in pistas if PISTAS_REDES.search(t)), None)
            if hit:
                errores.append(f"{donde}: la procedencia o el nombre del archivo menciona {hit.group(0)!r}; las fotos de redes sociales están prohibidas (R-FOT-01)")
    return errores, avisos


# ------------------------------------------------------------------ archivos (medidas)
def estimar_calidad_jpeg(im):
    """Calidad aproximada (1 a 100) de un JPEG a partir de su tabla de cuantizacion de luminancia. None si no se puede."""
    tablas = getattr(im, "quantization", None)
    if not tablas:
        return None
    t = tablas.get(0) or next(iter(tablas.values()))
    if len(t) != 64:
        return None
    escala = 100.0 * sum(t) / sum(_TABLA_BASE)
    q = 5000.0 / escala if escala > 100 else (200.0 - escala) / 2.0
    return int(round(max(1.0, min(100.0, q))))


def detalle_fino(im, lado=768):
    """Cociente entre la energia de las frecuencias altas y medias de la zona central, a resolucion nativa.
    En una foto nativa nitida ronda 0,2 a 0,7; una ampliada al doble ronda 0,06 a 0,10 y por debajo de 0,12 se avisa."""
    g = im.convert("L")
    w, h = g.size
    if min(w, h) < 128:
        return None
    cx, cy = w // 2, h // 2
    caja = (max(0, cx - lado // 2), max(0, cy - lado // 2), min(w, cx + lado // 2), min(h, cy + lado // 2))
    a = np.asarray(g.crop(caja), dtype=np.float64)
    a = a - a.mean()
    ven = np.hanning(a.shape[0])[:, None] * np.hanning(a.shape[1])[None, :]
    esp = np.abs(np.fft.fftshift(np.fft.fft2(a * ven))) ** 2
    yy, xx = np.indices(esp.shape)
    r = np.hypot((yy - esp.shape[0] / 2) / (esp.shape[0] / 2), (xx - esp.shape[1] / 2) / (esp.shape[1] / 2))
    media = esp[(r > 0.25) & (r <= 0.5)].sum()
    alta = esp[(r > 0.5) & (r <= 0.8)].sum()
    return float(alta / media) if media > 0 else None


def medir(ruta):
    """Medidas de un archivo de foto original."""
    with Image.open(ruta) as im:
        formato = (im.format or "").lower()
        d = {"ancho": im.width, "alto": im.height, "lado_largo": max(im.width, im.height), "formato": formato,
             "bytes": os.path.getsize(ruta), "calidad_jpeg": estimar_calidad_jpeg(im) if formato in ("jpeg", "mpo") else None}
        try:
            im.load()
            d["detalle_fino"] = detalle_fino(im)
        except Exception:
            d["detalle_fino"] = None
    return d


def juzgar(clave, medidas, ficticio_con_banco=False):
    """(errores, avisos) de una foto a partir de sus medidas. `medidas` es lo que devuelve `medir`."""
    errores, avisos = [], []
    minimo = minimo_de(clave)
    if medidas["lado_largo"] < minimo:
        errores.append(f"activos.{clave}: mide {medidas['ancho']} x {medidas['alto']} px y se exigen al menos {minimo} px de lado largo "
                       f"(foto {'de portada' if clave == 'hero' else ('del logo' if clave == 'logo' else 'de la web')}). Pide el original como archivo, sin reenviarlo por una red ni por una mensajería que lo comprima")
    q = medidas.get("calidad_jpeg")
    if q is not None:
        if q < JPEG_MINIMA:
            errores.append(f"activos.{clave}: JPEG muy comprimido (calidad estimada {q}); es una copia recomprimida, pide el original")
        elif q < JPEG_AVISO and clave != "logo":
            avisos.append(f"activos.{clave}: calidad JPEG estimada {q} (conviene un original de calidad 85 o más)")
    f = medidas.get("detalle_fino")
    if f is not None and f < DETALLE_AVISO and clave != "logo":
        avisos.append(f"activos.{clave}: parece ampliada o muy suavizada (detalle fino {f:.3f}); comprueba que sea el original")
    return errores, avisos


def revisar_archivos(F, origen_activos):
    """Mide los archivos de la ficha. Devuelve (errores, avisos, medidas por activo)."""
    errores, avisos, medidas = [], [], {}
    for clave, a in (F.get("activos") or {}).items():
        ruta = os.path.join(origen_activos, (a or {}).get("archivo", "?"))
        if not os.path.exists(ruta):
            continue   # que falte el archivo ya lo señala el motor
        try:
            m = medir(ruta)
        except Exception as e:
            errores.append(f"activos.{clave}: el archivo no se puede abrir como imagen ({type(e).__name__})")
            continue
        medidas[clave] = m
        e, av = juzgar(clave, m)
        errores += e
        avisos += av
    return errores, avisos, medidas


def revisar(F, origen_activos, con_archivos=True):
    """Procedencia y, si se pide, medidas. Devuelve (errores, avisos)."""
    errores, avisos = revisar_procedencia(F)
    if con_archivos:
        e, av, _ = revisar_archivos(F, origen_activos)
        errores += e
        avisos += av
    return errores, avisos
