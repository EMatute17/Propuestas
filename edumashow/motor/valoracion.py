"""Calificacion de Google en la web (R-VAL-01 y R-VAL-02, orden de Eduardo del 2026-10-08).

La web muestra la calificacion que el restaurante tiene en Google cuando es de 4,0 o mas: estrellas, nota y numero de resenas, con
enlace a su ficha de Google Maps y la fecha en que se consulto. Solo es un dato real que la ficha trae con su fuente y su fecha.
No se copia ningun comentario de clientes (ni bueno ni malo): la nota ya los resume todos. No se publica como dato estructurado
(los buscadores no aceptan una calificacion propia): es una cita visible con su enlace.

Ficha:
    "valoracion": {"fuente": "google", "nota": 4.6, "resenas": 312, "fecha": "2026-10-08", "url": "https://maps.app.goo.gl/..."}
`url` es opcional (sin ella el enlace busca el local en Google Maps con `contacto.mapa_consulta`). `ejemplo: true` solo vale en un
restaurante ficticio y rotula la calificacion como ejemplo.
"""
import datetime as _dt
import re
from html import escape
from urllib.parse import quote

from . import dinero

NOTA_MINIMA = 4.0
RESENAS_AVISO = 20   # con menos resenas la nota aun no dice mucho: aviso, no error
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
URL_GOOGLE = re.compile(r"^https://((www\.)?google\.[a-z.]+/maps|maps\.google\.[a-z.]+/|maps\.app\.goo\.gl/|goo\.gl/maps/|g\.page/|share\.google/)", re.I)
PREFIJOS_ENLACE = ("https://www.google.com/maps/", "https://maps.app.goo.gl/", "https://goo.gl/maps/", "https://g.page/", "https://share.google/")


def e_(t):
    return escape(str(t), quote=True)


def validar(F):
    """Devuelve (errores, avisos) sobre el bloque valoracion de la ficha. Sin bloque, ([], [])."""
    V = F.get("valoracion")
    if V is None:
        return [], []
    errores, avisos = [], []
    if not isinstance(V, dict):
        return ["valoracion: debe ser un bloque con campos"], []
    ficticio = bool((F.get("muestra") or {}).get("ejemplo_ficticio"))
    if V.get("fuente") != "google":
        errores.append("valoracion.fuente: solo se admite google")
    nota = V.get("nota")
    if isinstance(nota, bool) or not isinstance(nota, (int, float)):
        errores.append("valoracion.nota: debe ser un número, por ejemplo 4.6")
    else:
        if nota < NOTA_MINIMA:
            errores.append(f"valoracion.nota: {nota} es menor de {NOTA_MINIMA:g}; con esa nota la web no muestra la calificación. Quita el bloque valoracion")
        if nota > 5:
            errores.append("valoracion.nota: no puede pasar de 5")
        if round(nota, 1) != nota:
            errores.append("valoracion.nota: Google muestra un solo decimal (4.6); copia la nota tal cual, sin redondear hacia arriba")
    n = V.get("resenas")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        errores.append("valoracion.resenas: debe ser el número de reseñas, un entero de 1 o más")
    elif n < RESENAS_AVISO:
        avisos.append(f"valoracion.resenas: solo {n} reseñas; con tan pocas la nota aún dice poco, decide si conviene mostrarla")
    try:
        _dt.date.fromisoformat(str(V.get("fecha")))
    except ValueError:
        errores.append("valoracion.fecha: falta o no es una fecha AAAA-MM-DD (el día en que se miró la nota en Google)")
    if V.get("url") and not URL_GOOGLE.match(str(V["url"])):
        errores.append("valoracion.url: debe ser un enlace de Google Maps (google.com/maps, maps.app.goo.gl, g.page); quítalo para usar la búsqueda del local")
    if V.get("ejemplo") is True and not ficticio:
        errores.append("valoracion.ejemplo solo se admite en un restaurante ficticio")
    if ficticio and V.get("ejemplo") is not True:
        errores.append("valoracion: un restaurante ficticio no tiene calificación real en Google; si se muestra, valoracion.ejemplo debe ser true")
    extra = sorted(set(V) - {"fuente", "nota", "resenas", "fecha", "url", "ejemplo"})
    if extra:
        errores.append(f"valoracion: campos no admitidos {extra} (la web no copia comentarios de clientes)")
    return errores, avisos


# ------------------------------------------------------------------ texto
def _seps(F):
    p = dinero.PAISES[F["negocio"]["pais"]]
    return p[2], p[3]


def nota_txt(F):
    miles, dec = _seps(F)
    return f"{F['valoracion']['nota']:.1f}".replace(".", dec)


def resenas_txt(F):
    miles, dec = _seps(F)
    return f"{F['valoracion']['resenas']:,}".replace(",", miles)


def fecha_txt(V):
    d = _dt.date.fromisoformat(V["fecha"])
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def enlace(F):
    V = F["valoracion"]
    if V.get("ejemplo"):
        return None
    return V.get("url") or ("https://www.google.com/maps/search/?api=1&query=" + quote(F["contacto"]["mapa_consulta"], safe=""))


ESTRELLA = "M10 1.4l2.6 5.5 6 .8-4.4 4.2 1.1 6-5.3-2.9-5.3 2.9 1.1-6L1.4 7.7l6-.8z"


def _estrellas(nota):
    fila = "".join(f'<path d="{ESTRELLA}" transform="translate({20 * i} 0)"/>' for i in range(5))
    p = round(nota / 5 * 100, 1)
    return (f'<span class="val-estrellas" aria-hidden="true" style="--p:{p}%"><svg viewBox="0 0 100 20" focusable="false" class="val-base">{fila}</svg>'
            f'<svg viewBox="0 0 100 20" focusable="false" class="val-llena">{fila}</svg></span>')


def pieza(F, C, clase=""):
    """La calificacion como una pastilla con enlace (portada). Vacia si la ficha no la trae."""
    V = F.get("valoracion")
    if not V:
        return ""
    href = enlace(F)
    ejemplo = V.get("ejemplo")
    nota, n = nota_txt(F), resenas_txt(F)
    resenas = "reseña" if V["resenas"] == 1 else "reseñas"
    cuerpo = (f'{_estrellas(V["nota"])}<span class="val-nota">{e_(nota)}</span><span class="sr-only"> de 5 estrellas</span>'
              f'<span class="val-texto">{e_(n)} {resenas} en Google</span>' + ('<span class="val-ejemplo">Ejemplo</span>' if ejemplo else ""))
    cl = f'valoracion {clase}'.strip()
    datos = f'data-valoracion data-nota="{V["nota"]:.1f}" data-resenas="{V["resenas"]}"'
    if href:
        return (f'<a class="{cl}" href="{e_(href)}" target="_blank" rel="noopener" {datos}>{cuerpo}'
                f'<span class="sr-only"> (se abre Google Maps en una pestaña nueva)</span></a>')
    return f'<p class="{cl}" {datos}>{cuerpo}</p>'


def nota_fuente(F):
    """Frase de la visita: de donde sale el dato y cuando se miro."""
    V = F.get("valoracion")
    if not V:
        return ""
    if V.get("ejemplo"):
        return f'<p class="val-fuente" data-valoracion-fecha="{e_(V["fecha"])}">Calificación de ejemplo: este restaurante es ficticio y no tiene una ficha real en Google.</p>'
    return (f'<p class="val-fuente" data-valoracion-fecha="{e_(V["fecha"])}">Calificación de Google Maps consultada el {e_(fecha_txt(V))}. '
            f'Puede haber cambiado desde entonces.</p>')
