"""Piezas HTML de la personalidad elegante. Cada función recibe la ficha (F) y el contexto de
construcción (C) y devuelve HTML. Todo texto de la ficha se escapa (R-DAT-07)."""
import unicodedata
from html import escape
from urllib.parse import quote

from . import dinero, valoracion
from .imagenes import picture_html

NBSP = chr(0xA0)
DIAS = [("lun", "Lunes"), ("mar", "Martes"), ("mie", "Miércoles"), ("jue", "Jueves"), ("vie", "Viernes"), ("sab", "Sábado"), ("dom", "Domingo")]

ICONO_WA = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.86 9.86 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.18-1.14l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.24-8.23 2.2 0 4.27.86 5.82 2.42a8.18 8.18 0 0 1 2.41 5.83c0 4.54-3.7 8.21-8.23 8.21Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.12-.17.25-.64.81-.78.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-2-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.15.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.23.25-.87.85-.87 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.14-1.18-.06-.1-.23-.16-.48-.29Z"/></svg>')
ICONO_PAUSA = '<svg class="ico-pausa" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>'
ICONO_PLAY = '<svg class="ico-play" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>'
ICONO_MAPA = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg>'
ICONO_TEL = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25c1.1.37 2.3.57 3.6.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1C10.6 21 3 13.4 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1l-2.22 2.2Z"/></svg>'
ICONO_IG = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"><path d="M7.5 2h9A5.5 5.5 0 0 1 22 7.5v9a5.5 5.5 0 0 1-5.5 5.5h-9A5.5 5.5 0 0 1 2 16.5v-9A5.5 5.5 0 0 1 7.5 2Zm0 2A3.5 3.5 0 0 0 4 7.5v9A3.5 3.5 0 0 0 7.5 20h9a3.5 3.5 0 0 0 3.5-3.5v-9A3.5 3.5 0 0 0 16.5 4h-9ZM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm0 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6Zm5.25-3.25a1.25 1.25 0 1 1 0 2.5 1.25 1.25 0 0 1 0-2.5Z"/></svg>'


def e_(t):
    return escape(str(t), quote=True)


def wa_url(numero, texto):
    return f"https://wa.me/{numero}?text={quote(texto, safe='')}"


def mapa_url(consulta):
    return "https://www.google.com/maps/search/?api=1&query=" + quote(consulta, safe="")


def rango_horario(tramos):
    if not tramos:
        return "Cerrado"
    return " y ".join(f"{a}–{b}" for a, b in tramos)


def nombre_pais(N):
    return dinero.PAISES[N["pais"]][0].replace("Espana", "España").replace("Peru", "Perú").replace("Mexico", "México").replace("Canada", "Canadá").replace("Panama", "Panamá")


def _plano(t):
    """Minúsculas y sin tildes, para comparar textos sin que importen las mayúsculas ni los acentos."""
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def direccion_html(N):
    """La dirección y, en otra línea, la ciudad y el país que la dirección aún no dice (muchas fichas ya traen la dirección completa, con ciudad y país)."""
    d = _plano(N["direccion"])
    resto = [x for x in (N["ciudad"], nombre_pais(N)) if _plano(x) not in d]
    return e_(N["direccion"]) + (f'<br>{e_(", ".join(resto))}' if resto else "")


# ------------------------------------------------------------------ acciones: lo que la ficha pide que se pueda hacer en un toque
# Cada tipo trae su texto en la portada y en la barra del móvil. La ficha puede cambiar el texto (etiqueta) o el orden.
ETIQUETAS_ACCION = {
    "reservar": ("Reservar mesa", "Reservar"),
    "carta": ("Ver la carta", "Carta"),
    "mapa": ("Cómo llegar", "Cómo llegar"),
    "llamar": ("Llamar", "Llamar"),
    "whatsapp": ("Escribir por WhatsApp", "WhatsApp"),
    "instagram": ("Ver el Instagram", "Instagram"),
}
ACCIONES_POR_DEFECTO = {"hero": ["reservar", "carta"], "barra": ["reservar", "carta", "mapa"]}


def _accion(tipo, donde, F, C, etiqueta=None):
    K = F["contacto"]
    nombre = F["negocio"]["nombre"]
    ext, icono = False, ""
    if tipo == "reservar":
        href = "#reservar"
    elif tipo == "carta":
        href = "#carta"
    elif tipo == "mapa":
        href, ext = mapa_url(K["mapa_consulta"]), True
    elif tipo == "llamar":
        href, icono = "tel:" + K["telefono"], ICONO_TEL
    elif tipo == "whatsapp":
        href, ext, icono = wa_url(C["wa_destino"], f'{C["prefijo_wa"]}Hola {nombre}, tengo una consulta.'), True, ICONO_WA
    elif tipo == "instagram":
        href, ext, icono = K["instagram"]["url"], True, ICONO_IG
    else:
        raise ValueError(f"tipo de acción desconocido: {tipo}")
    if etiqueta is None:
        etiqueta = ETIQUETAS_ACCION[tipo][0 if donde == "hero" else 1]
        if tipo == "llamar" and donde == "hero" and K.get("telefono_visible"):
            etiqueta = f'Llamar al {K["telefono_visible"]}'
    return {"tipo": tipo, "etiqueta": etiqueta, "href": href, "externo": ext, "icono": icono if donde == "hero" else ""}


def acciones(F, C):
    """Acciones de la portada y de la barra fija del móvil, ya resueltas con su enlace."""
    pedido = F.get("acciones") or {}
    out = {}
    for donde in ("hero", "barra"):
        lista = pedido.get(donde) or ACCIONES_POR_DEFECTO[donde]
        out[donde] = []
        for a in lista:
            if isinstance(a, str):
                a = {"tipo": a}
            out[donde].append(_accion(a["tipo"], donde, F, C, a.get("etiqueta")))
    return out


def _enlace_accion(a, clase=""):
    ext = ' target="_blank" rel="noopener"' if a["externo"] else ""
    ico = f'{a["icono"]} ' if a["icono"] else ""
    cl = f' class="{clase}"' if clase else ""
    return f'<a{cl} href="{a["href"]}"{ext}>{ico}{e_(a["etiqueta"])}</a>'


def estado_y_valoracion(F, C, estado_html):
    """El estado de apertura y, si la ficha trae calificacion de Google, la pastilla con las estrellas, en una misma fila."""
    v = valoracion.pieza(F, C)
    return f'<div class="hero-datos">{estado_html}{v}</div>' if v else estado_html


# ------------------------------------------------------------------ piezas que dependen del paquete de animaciones
def particulas_html(C, fondo="oscuro"):
    """El lienzo de partículas de la portada, del tipo que pide el paquete (vacío si el paquete no lleva partículas)."""
    tipo = C["paquete"].get("particulas")
    return f'<canvas class="particulas" data-tipo="{tipo}" data-fondo="{fondo}"></canvas>' if tipo else ""


def luz_html(C):
    return '<div class="luz"></div>' if "luz" in C["modulos"] else ""


def paralaje_attr(C, fuerza=6):
    return f' data-paralaje="{fuerza}"' if "paralaje" in C["modulos"] else ""


def banda_texto(F, C):
    """Banda de texto muy grande que se desliza con el scroll (módulo texto_corre). Solo repite el nombre, la cocina y la ciudad de la ficha."""
    if "texto_corre" not in C["modulos"]:
        return ""
    N = F["negocio"]
    una = "".join(f"<span>{e_(w)}</span>" for w in (N["nombre"], N["cocina"], N["ciudad"]))
    return f'<div class="banda-texto" aria-hidden="true" data-decorativo><div class="pista-t">{una * 4}</div></div>'


# ------------------------------------------------------------------ cinta y portada
def cinta(F, C):
    if not C["muestra"]:
        return ""
    n = e_(F["negocio"]["nombre"])
    largo = (f"Muestra de Edumashow para <b>{n}</b> · ejemplo ficticio con fotos de referencia" if C["ejemplo"]
             else f"Muestra de Edumashow preparada para <b>{n}</b>")
    corto = "Muestra de Edumashow"
    return (f'<div class="cinta" role="region" aria-label="Aviso de muestra"><p><span class="largo">{largo}</span>'
            f'<span class="corto">{corto}</span></p><a class="cinta-btn" href="#panel-edu" data-abrir-panel>Quiero mi web</a></div>')


def hero_picture(C, atributos=""):
    """La foto de portada como picture (AVIF y WebP con srcset, uno para móvil y otro para escritorio) y su punto de foco en porcentajes."""
    h = C["hero"]
    srcset = lambda v: ", ".join(f"{u} {a}w" for u, a in v)
    movil, esc = h["movil"], h["escritorio"]
    fuentes = []
    for tipo, mime in (("avif", "image/avif"), ("webp", "image/webp")):
        fuentes.append(f'<source media="(max-width:700px)" type="{mime}" srcset="{srcset(movil["variantes"][tipo])}" sizes="100vw">')
    for tipo, mime in (("avif", "image/avif"), ("webp", "image/webp")):
        fuentes.append(f'<source type="{mime}" srcset="{srcset(esc["variantes"][tipo])}" sizes="100vw">')
    foco = f'{int(h["foco"][0] * 100)}% {int(h["foco"][1] * 100)}%'
    img = (f'<img src="{esc["jpg"]}" alt="" width="{esc["ancho"]}" height="{esc["alto"]}" fetchpriority="high" decoding="async">')
    return f'<picture{atributos}>{"".join(fuentes)}{img}</picture>', foco, esc["lqip"]


def letras_titular(nombre):
    """El nombre letra a letra (cada letra entra con su retardo); las palabras no se parten."""
    palabras, idx, partes = nombre.split(" "), 0, []
    for w in palabras:
        ls = []
        for ch in w:
            ls.append(f'<span class="l" style="--i:{idx}">{e_(ch)}</span>')
            idx += 1
        idx += 1
        partes.append('<span class="pal">' + "".join(ls) + "</span>")
    return " ".join(partes), max(len(w) for w in palabras)


def lema_en_html(N):
    """La frase de marca en inglés (si la ficha la trae), debajo del lema."""
    return f'<span class="lema-en" lang="en">{e_(N["lema_en"])}</span>' if N.get("lema_en") else ""


def hero_pie_html(F):
    """Pie de la foto de portada (por ejemplo, que es una imagen de ejemplo de banco libre): texto visible junto a la portada."""
    t = (F.get("textos") or {}).get("hero_pie")
    return f'<p class="hero-pie">{e_(t)}</p>' if t else ""


def nota_precios_html(F):
    t = (F.get("textos") or {}).get("carta_nota")
    return f'<p class="nota-precios">{e_(t)}</p>' if t else ""


def marca_elegante(F, C):
    """La marca de la cabecera: el logotipo si la ficha lo trae y, si no, el nombre escrito. Un logotipo de un solo tono va en negativo sobre el fondo del tono contrario (CSS)."""
    nombre = F["negocio"]["nombre"]
    logo = C.get("logo")
    if not logo:
        return f'<a class="marca" href="#inicio" aria-label="{e_(nombre)}, inicio">{e_(nombre)}</a>'
    return (f'<a class="marca marca-logo" href="#inicio" aria-label="{e_(nombre)}, inicio" data-logo="{logo.get("tono", "color")}">'
            f'{picture_html(logo, "", "(min-width:900px) 120px, 96px", lazy=False)}</a>')


def nav_elegante(F):
    """Los enlaces de la cabecera llevan solo a las secciones que la ficha tiene (un enlace a una sección que no existe no lleva a ningún sitio)."""
    enlaces = ['<a href="#carta">Carta</a>']
    if F.get("galeria"):
        enlaces.append('<a href="#ambiente">Ambiente</a>')
    if F.get("reservas"):
        enlaces.append('<a href="#reservar">Reservar</a>')
    enlaces.append('<a href="#visitanos">Visítanos</a>')
    return '<nav aria-label="Secciones">' + "".join(enlaces) + '</nav>'


def portada(F, C):
    N = F["negocio"]
    nombre = N["nombre"]
    letras, mas_larga = letras_titular(nombre)
    pic, foco, lqip = hero_picture(C, paralaje_attr(C))
    hero_acc = acciones(F, C)["hero"]
    botones = "".join(_enlace_accion(a, "btn" if i == 0 else "btn suave") for i, a in enumerate(hero_acc))
    nav = nav_elegante(F)
    return f'''<header class="hero" id="inicio" style="--c:{mas_larga};--ln:{len(nombre.split())};--foco:{foco}">
<div class="hero-fondo" aria-hidden="true" style="--lqip:url({lqip})">{pic}<div class="velo"></div>{luz_html(C)}<div class="grano"></div>{particulas_html(C)}</div>
<div class="hero-barra">{marca_elegante(F, C)}<div class="barra-der">{nav}<button type="button" class="pausa" data-pausa aria-pressed="false">{ICONO_PAUSA}{ICONO_PLAY}<span data-pausa-texto>Pausar animación</span></button></div></div>
<div class="hero-cuerpo"><div class="hero-titulo"><p class="sobre">{e_(N["cocina"])} · {e_(N["ciudad"])}</p>
<h1><span class="sr-only">{e_(nombre)}</span><span aria-hidden="true">{letras}</span></h1></div>
<div class="hero-base"><p class="lema">{e_(N["lema"])}{lema_en_html(N)}</p>
<div class="hero-lado"><div class="acciones">{botones}</div>
{estado_y_valoracion(F, C, '<p class="estado" data-open><span data-open-text>Ver horario</span></p>')}</div></div>{hero_pie_html(F)}</div>
</header>'''


# ------------------------------------------------------------------ idea
def idea(F, C):
    H = F["historia"]
    pasos = "".join(f'<li><h3>{e_(p["titulo"])}</h3><p>{e_(p["texto"])}</p></li>' for p in H["pasos"])
    return f'''<section class="idea" id="idea" aria-labelledby="t-idea"><div class="caja idea-rejilla">
<div class="idea-cifra" aria-hidden="true"><span class="num" data-progreso data-superpuesto><span class="num-linea">{e_(H["cifra"])}</span><span class="num-brasa">{e_(H["cifra"])}</span></span><span class="uni">{e_(H["unidad"])}</span></div>
<h2 class="sr-only" id="t-idea">{e_(H["cifra"])} {e_(H["unidad"])}</h2>
<div><p class="lead rv">{e_(H["texto"])}</p><ol class="pasos rv" style="--d:120ms">{pasos}</ol></div></div></section>'''


# ------------------------------------------------------------------ carta
def _plato(F, C, p):
    precio = C["importe"](p["precio"])
    firma = '<span class="firma">de la casa</span>' if p.get("firma") else ""
    foto_html, vista, clase = "", "", ""
    if p.get("foto"):
        a = C["fotos"][p["foto"]]
        foto_html = ('<div class="plato-foto" style="--c:%s">%s</div>' % (
            a["color"], picture_html(a["datos"], F["activos"][p["foto"]]["alt"], "(min-width:900px) 100px, 76px")))
        vista = f' data-vista="{a["datos"]["variantes"]["webp"][-1][0]}"'
        clase = " con-foto"
    return (f'<li class="plato{clase}" data-item="{e_(p["id"])}"{vista}>{foto_html}<div class="plato-cuerpo">'
            f'<div class="fila"><h3 class="nom">{e_(p["nombre"])}{firma}</h3><span class="puntos" aria-hidden="true"></span>'
            f'<data class="pre" value="{p["precio"]}">{e_(precio)}</data></div><p class="des">{e_(p["descripcion"])}</p></div></li>')


def carta(F, C):
    T = F["textos"]
    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{c["id"]}" aria-controls="panel-{c["id"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e_(c["titulo"])}</button>'
        for i, c in enumerate(F["carta"])
    )
    paneles = "".join(
        f'<div class="panel-cat{" activo" if i == 0 else ""}" role="tabpanel" id="panel-{c["id"]}" aria-labelledby="tab-{c["id"]}">'
        f'<h3 class="cat-titulo">{e_(c["titulo"])}</h3>' + (f'<p class="cat-nota">{e_(c["nota"])}</p>' if c.get("nota") else "")
        + f'<ul class="lista">{"".join(_plato(F, C, p) for p in c["platos"])}</ul></div>'
        for i, c in enumerate(F["carta"])
    )
    return f'''<section class="carta" id="carta" aria-labelledby="t-carta"><div class="caja">
<div class="carta-cab"><p class="sobretitulo">{e_(T["carta_sobretitulo"])}</p><h2 id="t-carta">{e_(T["carta_titulo"])}</h2>{nota_precios_html(F)}
<div class="tabs" role="tablist" aria-label="Categorías de la carta">{tabs}<span class="tab-ind" aria-hidden="true"></span></div></div>
<div class="paneles">{paneles}</div></div></section>'''


def carta_indice(F, C):
    """Carta con todas las categorías a la vista, una tras otra, con un índice pegado al lado (escritorio) o arriba (móvil) que marca dónde se está."""
    T = F["textos"]
    indice = "".join(f'<li><a href="#cat-{e_(c["id"])}" data-cat-link="{e_(c["id"])}">{e_(c.get("chip") or c["titulo"])}</a></li>' for c in F["carta"])
    cats = "".join(
        f'<section class="cat-i" id="cat-{e_(c["id"])}" aria-labelledby="h-{e_(c["id"])}"><h3 class="cat-i-titulo" id="h-{e_(c["id"])}">{e_(c["titulo"])}</h3>'
        + (f'<p class="cat-i-nota">{e_(c["nota"])}</p>' if c.get("nota") else "")
        + f'<ul class="lista">{"".join(_plato(F, C, p) for p in c["platos"])}</ul></section>' for c in F["carta"])
    return f'''<section class="carta carta-indice" id="carta" aria-labelledby="t-carta"><div class="caja">
<div class="carta-lado"><div class="carta-cab"><p class="sobretitulo">{e_(T["carta_sobretitulo"])}</p><h2 id="t-carta">{e_(T["carta_titulo"])}</h2>{nota_precios_html(F)}</div>
<nav class="indice" aria-label="Categorías de la carta"><ol>{indice}</ol></nav></div>
<div class="carta-cuerpo-i">{cats}</div></div></section>'''


# ------------------------------------------------------------------ ambiente
def ambiente(F, C):
    T = F["textos"]
    figs = []
    # el mosaico de escritorio tiene cuatro huecos (a, b, c y d): con más fotos se solaparían, así que solo lleva las cuatro primeras
    fotos_galeria = F["galeria"][:4] if (C.get("comp") or {}).get("galeria", "mosaico") == "mosaico" else F["galeria"]
    for i, g in enumerate(fotos_galeria):
        clase = "abcd"[i % 4]
        a = C["fotos"][g["foto"]]
        pic = picture_html(a["datos"], F["activos"][g["foto"]]["alt"], "(min-width:900px) 58vw, 78vw").replace("<picture>", f"<picture{paralaje_attr(C, 3)}>", 1)
        figs.append(f'<figure class="{clase} rv" style="--c:{a["color"]};--d:{i * 90}ms"><div class="marco">{pic}</div><figcaption>{e_(g["pie"])}</figcaption></figure>')
    return f'''<section class="ambiente" id="ambiente" aria-labelledby="t-amb"><div class="caja"><h2 id="t-amb" class="rv">{e_(T["ambiente_titulo"])}</h2>{('<p class="amb-texto rv">' + e_(T["ambiente_texto"]) + '</p>') if T.get("ambiente_texto") else ""}
<div class="galeria" role="group" aria-label="Fotos del local" tabindex="0">{"".join(figs)}</div></div></section>'''


# ------------------------------------------------------------------ reserva
def reserva(F, C):
    T, R = F["textos"], F["reservas"]
    opciones_p = "".join(f'<option value="{n}"{" selected" if n == R["personas_por_defecto"] else ""}>{n}</option>' for n in range(1, R["maximo_personas"] + 1))
    todas = set()
    for tramos in F["horario"].values():
        for a, b in tramos:
            ha, hb = int(a[:2]) * 60 + int(a[3:]), int(b[:2]) * 60 + int(b[3:])
            if hb <= ha:
                hb += 1440
            for m in range(ha, hb - R["ultima_antes_del_cierre_min"] + 1, R["paso_minutos"]):
                todas.add(m % 1440)
    horas = "".join(f'<option value="{m // 60:02d}:{m % 60:02d}">{m // 60:02d}:{m % 60:02d}</option>' for m in sorted(todas))
    prefijo = C["prefijo_wa"]
    wa_sin_js = wa_url(C["wa_destino"], f'{prefijo}Hola {F["negocio"]["nombre"]}, quisiera reservar una mesa.')
    aviso_muestra = ('<p class="ficticio">Es una muestra: este mensaje te llega a Edumashow, no a un restaurante.</p>' if C["ejemplo"] else "")
    return f'''<section class="reserva" id="reservar" aria-labelledby="t-res"><div class="caja rej-2">
<div class="rv"><h2 id="t-res">{e_(T["reserva_titulo"])}</h2><p class="texto">{e_(T["reserva_texto"])}</p>
<p class="estado" data-open><span data-open-text>Ver horario</span></p></div>
<div class="tarjeta rv" style="--d:120ms">
<noscript><p><a class="btn" href="{wa_sin_js}" target="_blank" rel="noopener">{ICONO_WA} Pedir mesa por WhatsApp</a></p></noscript>
<form class="form form-js" id="form-reserva" novalidate hidden>
<div class="campo"><label for="r-nombre">Tu nombre</label><input id="r-nombre" name="nombre" autocomplete="name" required></div>
<div class="dos"><div class="campo"><label for="r-fecha">Día</label><input id="r-fecha" name="fecha" type="date" required></div>
<div class="campo"><label for="r-hora">Hora</label><select id="r-hora" name="hora" required>{horas}</select></div></div>
<div class="campo"><label for="r-pers">Personas</label><select id="r-pers" name="personas">{opciones_p}</select></div>
<div class="campo"><label for="r-nota">Algo que debamos saber (opcional)</label><textarea id="r-nota" name="nota" placeholder="Una celebración, una alergia…"></textarea></div>
<p class="resumen" data-r-resumen aria-live="polite"></p>
<p class="aviso" data-r-mensaje role="alert" hidden></p>
<button class="btn" type="submit">{ICONO_WA} Pedir mesa por WhatsApp</button>
<p class="aviso-wa" data-aviso-wa hidden>Si no se abrió WhatsApp, <a href="{wa_sin_js}" target="_blank" rel="noopener">tócalo aquí</a>.</p>
</form>{aviso_muestra}</div></div></section>'''


# ------------------------------------------------------------------ visita
def visita(F, C):
    N, T = F["negocio"], F["textos"]
    filas = "".join(f'<li data-dia="{k}"><span>{n}</span><span>{rango_horario(F["horario"].get(k, []))}</span></li>' for k, n in DIAS)
    como = mapa_url(F["contacto"]["mapa_consulta"])
    pref = C["prefijo_wa"]
    K = F["contacto"]
    # los contactos que la ficha trae, cada uno con su acción directa: sin WhatsApp no hay botón de escribir (un enlace sin número no lleva a ningún sitio)
    botones = [f'<a class="btn" href="{como}" target="_blank" rel="noopener">{ICONO_MAPA} Cómo llegar</a>']
    if C["wa_destino"]:
        wa = wa_url(C["wa_destino"], f'{pref}Hola {N["nombre"]}, tengo una consulta.')
        botones.append(f'<a class="btn suave" href="{wa}" target="_blank" rel="noopener">{ICONO_WA} Escribirnos</a>')
    if K.get("telefono"):
        botones.append(f'<a class="btn suave" href="tel:{K["telefono"]}">{ICONO_TEL} Llamar al {e_(K.get("telefono_visible") or K["telefono"])}</a>')
    if K.get("instagram"):
        botones.append(f'<a class="btn suave" href="{e_(K["instagram"]["url"])}" target="_blank" rel="noopener">{ICONO_IG} Instagram @{e_(K["instagram"]["usuario"])}</a>')
    return f'''<section class="visita" id="visitanos" aria-labelledby="t-vis"><div class="caja rej-2">
<div class="rv"><h2 id="t-vis">{e_(T["visita_titulo"])}</h2><address>{direccion_html(N)}</address>
<p class="estado" data-open><span data-open-text>Ver horario</span></p>{('<p class="aviso-datos">' + e_(T["horario_aviso"]) + '</p>') if T.get("horario_aviso") else ""}
{valoracion.pieza(F, C, "en-visita")}{valoracion.nota_fuente(F)}
<div class="botones">{"".join(botones)}</div></div>
<ul class="horas rv" style="--d:120ms" aria-label="Horario">{filas}</ul></div></section>'''


# ------------------------------------------------------------------ cierre, pie, barra y panel
def cierre_muestra(F, C):
    if not C["muestra"]:
        return ""
    n = F["negocio"]["nombre"]
    wa = wa_url(C["agencia"]["whatsapp"], f'Hola Edumashow, vi la muestra de la web de {n} y quiero una así para mi restaurante.')
    return f'''<section class="cierre-muestra" id="tu-web" aria-labelledby="t-cierre"><div class="caja"><h2 id="t-cierre" class="rv">Así se vería tu restaurante</h2>
<p class="rv">Si te gusta cómo queda, la dejamos lista con tu carta, tus fotos y tu horario.</p>
<div class="cierre-btns rv"><a class="btn" href="{wa}" target="_blank" rel="noopener">{ICONO_WA} Hablar por WhatsApp</a><a class="btn suave" href="#panel-edu" data-abrir-panel>Ver qué incluye</a></div></div></section>'''


def _origen_fotos(F):
    """De dónde salen las fotos de la muestra, dicho en el pie (R-MUE-05): las del restaurante, las de ejemplo de banco libre o ambas."""
    origenes = {(a.get("procedencia") or {}).get("origen") for k, a in F["activos"].items() if k != "logo"}
    propias = "propia_del_restaurante" in origenes
    ajenas = bool(origenes - {"propia_del_restaurante"})
    if propias and not ajenas:
        return "Fotos del restaurante, aportadas por el propio restaurante."
    if propias:
        return "Las fotos del restaurante son las que aportó el propio restaurante; el resto son de ejemplo, de banco libre."
    return "Las fotos son de ejemplo, de banco libre: no son las fotos del restaurante, que se pondrán cuando las aporte."


def pie(F, C):
    N = F["negocio"]
    pais = nombre_pais(N)
    extra = ""
    if C["muestra"]:
        retirar = f'mailto:{C["agencia"]["correo"]}?subject=' + quote(f'Retirar la muestra de {N["nombre"]}')
        if C["ejemplo"]:
            origen = '<span>Fotos de referencia, solo para esta muestra.</span>'
        else:   # negocio real: se dice de dónde salen los datos y las fotos (R-MUE-05)
            origen = f'<span>{e_(F["muestra"]["origen_datos"])}</span><span>{e_(_origen_fotos(F))}</span>'
        extra = (f'<span>Página de muestra hecha por Edumashow.</span>' + origen
                 + f'<a href="{retirar}" data-retirada>Pedir que retiren esta muestra</a>')
    logo = C.get("logo")
    sello = (f'<span class="pie-logo" data-logo="{logo.get("tono", "color")}" aria-hidden="true">{picture_html(logo, "", "120px")}</span>' if logo else "")
    return f'<footer class="pie"><div class="caja">{sello}<b>{e_(N["nombre"])}</b><span>{e_(N["ciudad"])} · {e_(pais)}</span>{extra}</div></footer>'


def barra_movil(F, C):
    barra = acciones(F, C)["barra"]
    enlaces = "".join(_enlace_accion(a, "principal" if i == 0 else "") for i, a in enumerate(barra))
    return f'<nav class="barra-movil" aria-label="Acciones rápidas">{enlaces}</nav>'


def vista_plato(F, C):
    return '<div class="vista" aria-hidden="true"><img alt="" width="420" height="525"></div>'


def panel_edu(F, C):
    if not C["muestra"]:
        return ""
    n = F["negocio"]["nombre"]
    ag = C["agencia"]
    wa = wa_url(ag["whatsapp"], f'Hola Edumashow, vi la muestra de la web de {n} y quiero una así para mi restaurante.')
    incluye = F.get("muestra", {}).get("incluye") or [
        "Tu carta, tus precios y tus fotos, con el diseño que le corresponde a tu estilo.",
        "Reservas o pedidos que llegan directos a tu WhatsApp, y tu horario siempre al día.",
        "Pensada para verse bien y cargar rápido en el móvil de tus clientes."]
    lista = "\n".join(f"<li>{e_(t)}</li>" for t in incluye)
    nota = ("Los textos, fotos y precios de esta muestra son de ejemplo." if C["ejemplo"]
            else F["muestra"]["nota_panel"])
    return f'''<dialog class="panel-edu" id="panel-edu" aria-labelledby="t-panel"><div class="hoja"><a class="cerrar" href="#contenido" data-cerrar-panel aria-label="Cerrar">{chr(0xD7)}</a>
<h2 id="t-panel">Esta es una muestra de lo que Edumashow hace</h2>
<p>La página final es la misma experiencia, completa y hecha con los datos de tu restaurante:</p>
<ul>{lista}</ul>
<p>Esta muestra es gratuita y no te compromete a nada. Estará publicada {e_(ag["vigencia"])}. Si te interesa, hablamos del precio y los plazos por WhatsApp.</p>
<div class="contacto"><a class="btn" href="{wa}" target="_blank" rel="noopener">{ICONO_WA} Escríbenos por WhatsApp</a>
<div class="correo"><span>{e_(ag["correo"])}</span><button type="button" data-copiar="{e_(ag["correo"])}">Copiar</button></div></div>
<p class="nota">{e_(nota)}</p></div></dialog>'''


# ------------------------------------------------------------------ registro de la personalidad elegante
CSS_EXTRA = (".carta,.visita,.tarjeta,.panel-edu,.cinta{--foco-anillo:var(--foco-anillo-papel)}"
             ".resumen{font-weight:600;min-height:1.6em}"
             "@media (prefers-reduced-motion:reduce){.hero-fondo img{animation:none}.grano{animation:none}}")
JS_EXTRA = "(function(){var f=document.getElementById('form-reserva');if(f)f.hidden=false;})();\n"


def _extras(F, C):
    return vista_plato(F, C)


PERSONALIDAD = {
    "portada": portada,
    "portadas": {"luz_brasas": portada},
    "cartas": {"pestanas_lista": carta, "indice_columnas": carta_indice},
    "tras_portada": banda_texto,
    "secciones": {"idea": idea, "carta": carta, "ambiente": ambiente, "reserva": reserva, "visita": visita, "cierre": cierre_muestra},
    "extras": _extras,
    "css_extra": CSS_EXTRA,
    "js_extra": JS_EXTRA,
    "requiere_hero": True,
    "admite_variantes": False,
    "mide_apertura": True,
    "textos": ["carta_titulo", "carta_sobretitulo", "ambiente_titulo", "reserva_titulo", "reserva_texto", "visita_titulo"],
}
