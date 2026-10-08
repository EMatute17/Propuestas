"""Piezas HTML de la personalidad elegante. Cada función recibe la ficha (F) y el contexto de
construcción (C) y devuelve HTML. Todo texto de la ficha se escapa (R-DAT-07)."""
from html import escape
from urllib.parse import quote

from . import dinero
from .imagenes import picture_html

NBSP = chr(0xA0)
DIAS = [("lun", "Lunes"), ("mar", "Martes"), ("mie", "Miércoles"), ("jue", "Jueves"), ("vie", "Viernes"), ("sab", "Sábado"), ("dom", "Domingo")]

ICONO_WA = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.86 9.86 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.18-1.14l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.24-8.23 2.2 0 4.27.86 5.82 2.42a8.18 8.18 0 0 1 2.41 5.83c0 4.54-3.7 8.21-8.23 8.21Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.12-.17.25-.64.81-.78.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-2-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.15.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.23.25-.87.85-.87 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.14-1.18-.06-.1-.23-.16-.48-.29Z"/></svg>')
ICONO_PAUSA = '<svg class="ico-pausa" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>'
ICONO_PLAY = '<svg class="ico-play" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>'
ICONO_MAPA = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg>'


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


# ------------------------------------------------------------------ cinta y portada
def cinta(F, C):
    if not C["muestra"]:
        return ""
    n = e_(F["negocio"]["nombre"])
    largo = (f"Muestra de Edumashow para <b>{n}</b> · ejemplo ficticio con fotos de referencia" if C["ejemplo"]
             else f"Muestra de Edumashow preparada para <b>{n}</b>")
    corto = "Muestra de Edumashow"
    return (f'<div class="cinta" role="region" aria-label="Aviso de muestra"><p><span class="largo">{largo}</span>'
            f'<span class="corto">{corto}</span></p><button type="button" data-abrir-panel>Quiero mi web</button></div>')


def portada(F, C):
    N = F["negocio"]
    nombre = N["nombre"]
    h = C["hero"]
    palabras, idx, partes = nombre.split(" "), 0, []
    for w in palabras:
        ls = []
        for ch in w:
            ls.append(f'<span class="l" style="--i:{idx}">{e_(ch)}</span>')
            idx += 1
        idx += 1
        partes.append('<span class="pal">' + "".join(ls) + "</span>")
    letras = " ".join(partes)
    mas_larga = max(len(w) for w in palabras)
    srcset = lambda v: ", ".join(f"{u} {a}w" for u, a in v)
    movil, esc = h["movil"], h["escritorio"]
    fuentes = []
    for tipo, mime in (("avif", "image/avif"), ("webp", "image/webp")):
        fuentes.append(f'<source media="(max-width:700px)" type="{mime}" srcset="{srcset(movil["variantes"][tipo])}" sizes="100vw">')
    for tipo, mime in (("avif", "image/avif"), ("webp", "image/webp")):
        fuentes.append(f'<source type="{mime}" srcset="{srcset(esc["variantes"][tipo])}" sizes="100vw">')
    foco = f'{int(h["foco"][0] * 100)}% {int(h["foco"][1] * 100)}%'
    img = (f'<img src="{esc["jpg"]}" alt="" width="{esc["ancho"]}" height="{esc["alto"]}" fetchpriority="high" decoding="async">')
    cta = "Reservar mesa"
    nav = ('<nav aria-label="Secciones"><a href="#carta">Carta</a><a href="#ambiente">Ambiente</a>'
           '<a href="#reservar">Reservar</a><a href="#visitanos">Visítanos</a></nav>')
    return f'''<header class="hero" id="inicio" style="--c:{mas_larga};--foco:{foco}">
<div class="hero-fondo" aria-hidden="true" style="--lqip:url({esc["lqip"]})"><picture>{"".join(fuentes)}{img}</picture><div class="velo"></div><div class="luz"></div><div class="grano"></div><canvas class="brasas"></canvas></div>
<div class="hero-barra"><a class="marca" href="#inicio" aria-label="{e_(nombre)}, inicio">{e_(nombre)}</a><div class="barra-der">{nav}<button type="button" class="pausa" data-pausa aria-pressed="false">{ICONO_PAUSA}{ICONO_PLAY}<span data-pausa-texto>Pausar animación</span></button></div></div>
<div class="hero-cuerpo"><div class="hero-titulo"><p class="sobre">{e_(N["cocina"])} · {e_(N["ciudad"])}</p>
<h1><span class="sr-only">{e_(nombre)}</span><span aria-hidden="true">{letras}</span></h1></div>
<div class="hero-base"><p class="lema">{e_(N["lema"])}</p>
<div class="hero-lado"><div class="acciones"><a class="btn" href="#reservar">{cta}</a><a class="btn suave" href="#carta">Ver la carta</a></div>
<p class="estado" data-open><span data-open-text>Ver horario</span></p></div></div></div>
</header>'''


# ------------------------------------------------------------------ idea
def idea(F, C):
    H = F["historia"]
    pasos = "".join(f'<li><h3>{e_(p["titulo"])}</h3><p>{e_(p["texto"])}</p></li>' for p in H["pasos"])
    return f'''<section class="idea" id="idea" aria-labelledby="t-idea"><div class="caja idea-rejilla">
<div class="idea-cifra" aria-hidden="true"><span class="num">{e_(H["cifra"])}</span><span class="uni">{e_(H["unidad"])}</span></div>
<h2 class="sr-only" id="t-idea">{e_(H["cifra"])} {e_(H["unidad"])}</h2>
<div><p class="lead rv">{e_(H["texto"])}</p><ol class="pasos rv" style="--d:120ms">{pasos}</ol></div></div></section>'''


# ------------------------------------------------------------------ carta
def _plato(F, C, p):
    precio = dinero.formato_importe(p["precio"], F["negocio"]["pais"], F["moneda"])
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
        f'<h3 class="cat-titulo">{e_(c["titulo"])}</h3><ul class="lista">{"".join(_plato(F, C, p) for p in c["platos"])}</ul></div>'
        for i, c in enumerate(F["carta"])
    )
    return f'''<section class="carta" id="carta" aria-labelledby="t-carta"><div class="caja">
<div class="carta-cab"><p class="sobretitulo">{e_(T["carta_sobretitulo"])}</p><h2 id="t-carta">{e_(T["carta_titulo"])}</h2>
<div class="tabs" role="tablist" aria-label="Categorías de la carta">{tabs}<span class="tab-ind" aria-hidden="true"></span></div></div>
<div class="paneles">{paneles}</div></div></section>'''


# ------------------------------------------------------------------ ambiente
def ambiente(F, C):
    T = F["textos"]
    figs = []
    for i, g in enumerate(F["galeria"]):
        clase = "abcd"[i % 4]
        a = C["fotos"][g["foto"]]
        pic = picture_html(a["datos"], F["activos"][g["foto"]]["alt"], "(min-width:900px) 58vw, 78vw")
        figs.append(f'<figure class="{clase} rv" style="--c:{a["color"]};--d:{i * 90}ms"><div class="marco">{pic}</div><figcaption>{e_(g["pie"])}</figcaption></figure>')
    return f'''<section class="ambiente" id="ambiente" aria-labelledby="t-amb"><div class="caja"><h2 id="t-amb" class="rv">{e_(T["ambiente_titulo"])}</h2>
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
    pais = dinero.PAISES[N["pais"]][0].replace("Espana", "España").replace("Peru", "Perú").replace("Mexico", "México").replace("Canada", "Canadá").replace("Panama", "Panamá")
    pref = C["prefijo_wa"]
    wa = wa_url(C["wa_destino"], f'{pref}Hola {N["nombre"]}, tengo una consulta.')
    return f'''<section class="visita" id="visitanos" aria-labelledby="t-vis"><div class="caja rej-2">
<div class="rv"><h2 id="t-vis">{e_(T["visita_titulo"])}</h2><address>{e_(N["direccion"])}<br>{e_(N["ciudad"])}, {e_(pais)}</address>
<p class="estado" data-open><span data-open-text>Ver horario</span></p>
<div class="botones"><a class="btn" href="{como}" target="_blank" rel="noopener">{ICONO_MAPA} Cómo llegar</a><a class="btn suave" href="{wa}" target="_blank" rel="noopener">{ICONO_WA} Escribirnos</a></div></div>
<ul class="horas rv" style="--d:120ms" aria-label="Horario">{filas}</ul></div></section>'''


# ------------------------------------------------------------------ cierre, pie, barra y panel
def cierre_muestra(F, C):
    if not C["muestra"]:
        return ""
    n = F["negocio"]["nombre"]
    wa = wa_url(C["agencia"]["whatsapp"], f'Hola Edumashow, vi la muestra de la web de {n} y quiero una así para mi restaurante.')
    return f'''<section class="cierre-muestra" id="tu-web" aria-labelledby="t-cierre"><div class="caja"><h2 id="t-cierre" class="rv">Así se vería tu restaurante</h2>
<p class="rv">Si te gusta cómo queda, la dejamos lista con tu carta, tus fotos y tu horario.</p>
<div class="cierre-btns rv"><a class="btn" href="{wa}" target="_blank" rel="noopener">{ICONO_WA} Hablar por WhatsApp</a><button type="button" class="btn suave" data-abrir-panel>Ver qué incluye</button></div></div></section>'''


def pie(F, C):
    N = F["negocio"]
    pais = dinero.PAISES[N["pais"]][0].replace("Espana", "España").replace("Peru", "Perú").replace("Mexico", "México").replace("Canada", "Canadá").replace("Panama", "Panamá")
    extra = ""
    if C["muestra"]:
        retirar = f'mailto:{C["agencia"]["correo"]}?subject=' + quote(f'Retirar la muestra de {N["nombre"]}')
        extra = (f'<span>Página de muestra hecha por Edumashow.</span>'
                 + ('<span>Fotos de referencia, solo para esta muestra.</span>' if C["ejemplo"] else "")
                 + f'<a href="{retirar}">Pedir que retiren esta muestra</a>')
    return f'<footer class="pie"><div class="caja"><b>{e_(N["nombre"])}</b><span>{e_(N["ciudad"])} · {e_(pais)}</span>{extra}</div></footer>'


def barra_movil(F, C):
    como = mapa_url(F["contacto"]["mapa_consulta"])
    return (f'<nav class="barra-movil" aria-label="Acciones rápidas"><a class="principal" href="#reservar">Reservar</a>'
            f'<a href="#carta">Carta</a><a href="{como}" target="_blank" rel="noopener">Cómo llegar</a></nav>')


def vista_plato(F, C):
    return '<div class="vista" aria-hidden="true"><img alt="" width="420" height="525"></div>'


def panel_edu(F, C):
    if not C["muestra"]:
        return ""
    n = F["negocio"]["nombre"]
    ag = C["agencia"]
    wa = wa_url(ag["whatsapp"], f'Hola Edumashow, vi la muestra de la web de {n} y quiero una así para mi restaurante.')
    return f'''<dialog class="panel-edu" id="panel-edu" aria-labelledby="t-panel"><div class="hoja"><button type="button" class="cerrar" data-cerrar-panel aria-label="Cerrar">{chr(0xD7)}</button>
<h2 id="t-panel">Esta es una muestra de lo que Edumashow hace</h2>
<p>La página final es la misma experiencia, completa y hecha con los datos de tu restaurante:</p>
<ul><li>Tu carta, tus precios y tus fotos, con el diseño que le corresponde a tu estilo.</li>
<li>Reservas o pedidos que llegan directos a tu WhatsApp, y tu horario siempre al día.</li>
<li>Pensada para verse bien y cargar rápido en el móvil de tus clientes.</li></ul>
<p>Esta muestra es gratuita y no te compromete a nada. Estará publicada {e_(ag["vigencia"])}. Si te interesa, hablamos del precio y los plazos por WhatsApp.</p>
<div class="contacto"><a class="btn" href="{wa}" target="_blank" rel="noopener">{ICONO_WA} Escríbenos por WhatsApp</a>
<div class="correo"><span>{e_(ag["correo"])}</span><button type="button" data-copiar="{e_(ag["correo"])}">Copiar</button></div></div>
<p class="nota">Los textos, fotos y precios de esta muestra son de ejemplo.</p></div></dialog>'''
