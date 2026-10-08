"""Ranking de antojo: ordena las fotos de un restaurante por lo que provocan.

Criterios (Documento Maestro, 5.4 y 6.5, escritos de nuevo para esta web). Cada foto se juzga mirándola, con 0 (no),
1 (en parte) o 2 (claramente sí), y el juicio pesa el 65 %. El otro 35 % son medidas técnicas objetivas sobre la zona
que más atrae la mirada: nitidez, calidez de la luz, saturación y contraste. Los pesos y los umbrales son criterios de
diseño, no medidas calibradas con clientes: ningún cálculo mide el deseo de comer; lo que hace esto es aplicar, foto por
foto, las señales que la evidencia asocia con él, y dejar por escrito por qué una foto va antes que otra.

Solo cuentan las fotos reales (no ilustraciones ni generadas) y sin logotipos ni marcas de agua de otras marcas."""
import math

import numpy as np
from PIL import Image, ImageFilter

CRITERIOS = {
    "textura": ("Primer plano con textura visible: costra, brillo, fundido, glaseado", 22),
    "reconocible": ("Reconocible como el plato que el texto nombra", 18),
    "accion": ("Momento de acción: corte, salsa cayendo, mordisco, vapor", 14),
    "protagonista": ("Un solo protagonista sobre un fondo que contrasta", 14),
    "luz": ("Luz lateral cálida, sin dominante azulada", 12),
    "calor": ("Señal de calor o frescura: vapor, fundido, gotas de frío", 12),
    "mano": ("Mano o cubierto hacia la derecha, o nada que estorbe", 8),
}
PESO_JUICIO, PESO_TECNICA = 0.65, 0.35
LADO_TRABAJO = 384          # todas las fotos se miden a este tamaño para que se puedan comparar


def _mapa_saliencia(rgb):
    """Dónde mira el ojo: residuo espectral (Hou y Zhang, 2007) mezclado con la saturación. Valores de 0 a 1."""
    a = np.asarray(rgb, dtype=np.float64) / 255.0
    g = a.mean(2)
    F = np.fft.fft2(g)
    logamp = np.log(np.abs(F) + 1e-8)
    pad = np.pad(logamp, 1, mode="wrap")
    media = sum(pad[i:i + logamp.shape[0], j:j + logamp.shape[1]] / 9.0 for i in range(3) for j in range(3))
    sal = np.abs(np.fft.ifft2(np.exp(logamp - media + 1j * np.angle(F)))) ** 2
    mx, mn = a.max(2), a.min(2)
    sat = (mx - mn) / (mx + 1e-6)
    s = sal / (sal.max() + 1e-9) * 0.6 + sat / (sat.max() + 1e-9) * 0.4
    img = Image.fromarray((np.clip(s, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))
    return np.asarray(img, dtype=np.float64) / 255.0, a


def _laplaciano(g):
    return g[1:-1, 1:-1] * -4 + g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:]


def _nitidez_plato(a):
    """Varianza del laplaciano en las zonas más nítidas (percentil 90 de una rejilla de 6 por 6): en una foto de comida lo enfocado es
    el plato, y un fondo desenfocado no penaliza; una foto borrosa entera, sí."""
    g = a.mean(2) * 255.0
    lap = _laplaciano(g)
    H, W = lap.shape
    v = []
    for i in range(6):
        for j in range(6):
            t = lap[i * H // 6:(i + 1) * H // 6, j * W // 6:(j + 1) * W // 6]
            if t.size:
                v.append(float(t.var()))
    return float(np.percentile(v, 90)) if v else 0.0     # una foto de tres píxeles o menos no tiene zonas que medir


def medidas_tecnicas(imagen):
    """Medidas objetivas de una foto y su puntuación técnica de 0 a 100."""
    if imagen.mode in ("RGBA", "LA") or (imagen.mode == "P" and "transparency" in imagen.info):
        fondo = Image.new("RGBA", imagen.size, (128, 128, 128, 255))   # lo transparente se mide sobre gris medio, no sobre el RGB que quede oculto
        fondo.alpha_composite(imagen.convert("RGBA"))
        imagen = fondo
    im = imagen.convert("RGB")
    px = im.size
    t = im.copy()
    t.thumbnail((LADO_TRABAJO, LADO_TRABAJO))
    if max(t.size) < LADO_TRABAJO:                       # una foto pequeña se mide igual que una grande: a la misma escala
        k = LADO_TRABAJO / max(t.size)
        t = t.resize((round(t.width * k), round(t.height * k)), Image.LANCZOS)
    s, a = _mapa_saliencia(t)
    mx, mn = a.max(2), a.min(2)
    sat = (mx - mn) / (mx + 1e-6)
    w = s ** 2
    w = w / (w.sum() + 1e-9)
    R, B = a[..., 0], a[..., 2]
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    calidez = float(((R - B) * w).sum())
    saturacion = float((sat * w).sum())
    contraste = float(lum.std())
    nitidez = max(_nitidez_plato(a), 1e-3)
    p_nit = float(np.clip((math.log10(nitidez) - math.log10(50)) / (math.log10(2500) - math.log10(50)), 0, 1))   # de 50 (blanda) a 2500 (muy nitida) a 384 px
    p_cal = float(np.clip((calidez + 0.05) / 0.25, 0, 1))
    p_sat = float(np.clip((saturacion - 0.10) / 0.25, 0, 1) if saturacion < 0.35 else (1.0 if saturacion <= 0.85 else max(0.6, 1 - (saturacion - 0.85) * 3)))
    p_con = float(np.clip((contraste - 0.10) / 0.10, 0, 1) if contraste < 0.20 else (1.0 if contraste <= 0.35 else max(0.6, 1 - (contraste - 0.35) * 3)))
    puntos = 100 * (0.40 * p_nit + 0.25 * p_cal + 0.20 * p_sat + 0.15 * p_con)
    return {"px": list(px), "nitidez_plato": round(nitidez, 1), "calidez": round(calidez, 3), "saturacion": round(saturacion, 3),
            "contraste": round(contraste, 3), "puntos": round(puntos, 1)}


def juicio_visual(juicio):
    """Puntos de 0 a 100 del juicio (0, 1 o 2 por criterio, ponderados)."""
    faltan = [k for k in CRITERIOS if k not in juicio]
    malos = [k for k, v in juicio.items() if k in CRITERIOS and v not in (0, 1, 2)]
    if faltan or malos:
        raise ValueError(f"el juicio de antojo necesita los 7 criterios con 0, 1 o 2. Faltan: {faltan}; no válidos: {malos}")
    return sum(CRITERIOS[k][1] * juicio[k] / 2.0 for k in CRITERIOS)


def puntuar(imagen, antojo):
    """Puntúa una foto. `antojo` trae el juicio, real, sin_marcas_ajenas y una nota. Devuelve el registro completo."""
    visual = juicio_visual(antojo["juicio"])
    med = medidas_tecnicas(imagen)
    total = round(PESO_JUICIO * visual + PESO_TECNICA * med["puntos"], 1)
    motivos = []
    if not antojo.get("real", False):
        motivos.append("no es una foto real")
    if not antojo.get("sin_marcas_ajenas", False):
        motivos.append("lleva logos de otra marca o marca de agua")
    return {"puntos": total, "visual": round(visual, 1), "tecnica": med["puntos"], "medidas": med, "juicio": dict(antojo["juicio"]),
            "real": bool(antojo.get("real", False)), "sin_marcas_ajenas": bool(antojo.get("sin_marcas_ajenas", False)),
            "nota": antojo.get("nota", ""), "descartada": motivos}


def ranking(registros):
    """registros: {clave: registro de puntuar}. Devuelve las claves de más a menos provocativa; las descartadas no entran."""
    validas = [(k, r) for k, r in registros.items() if not r["descartada"]]
    validas.sort(key=lambda kr: (-kr[1]["puntos"], kr[0]))
    return [k for k, _ in validas]
