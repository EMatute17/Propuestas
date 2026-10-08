"""Piezas HTML de la personalidad urbana (parrillas y comida de calle): mural de fotos, titular de cartel y menú
como tablero de precios. Cada función recibe la ficha (F) y el contexto de construcción (C) y devuelve HTML.
Todo texto de la ficha se escapa (R-DAT-07). Comparte con la elegante la cinta de muestra, el pie, la barra móvil y el panel."""
from . import temas
from .imagenes import picture_html
from .piezas import (ICONO_IG, ICONO_MAPA, ICONO_PAUSA, ICONO_PLAY, ICONO_TEL, ICONO_WA, _enlace_accion, acciones, e_, mapa_url,
                     nombre_pais, wa_url, DIAS, rango_horario, cierre_muestra)

ICONO_TIKTOK = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"><path d="M19.6 7.7a4.7 4.7 0 0 1-3.5-1.6A4.7 4.7 0 0 1 '
                '14.9 3h-3.2v12.6a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .8.1V9.8a5.9 5.9 0 0 0-.8-.1 5.8 5.8 0 1 0 5.8 5.8V9.2a7.9 7.9 0 0 0 4.7 1.5V7.7Z"/></svg>')
MURAL_COLUMNAS = 6
MURAL_SIZES = "(min-width:1000px) 17vw, (min-width:700px) 25vw, 34vw"


def _precio(C, valor):
    return f'<data class="pre" value="{valor}">{e_(C["importe"](valor))}</data>'


# ------------------------------------------------------------------ portada
def _tesela(C, clave, lazy):
    a = C["fotos"][clave]
    return f'<div class="tesela" style="--c:{a["color"]}">{picture_html(a["datos"], "", MURAL_SIZES, lazy=lazy)}</div>'


def _mural(F, C):
    claves = list(dict.fromkeys(g["foto"] for g in F["galeria"]))
    n = len(claves)
    paso = max(1, n // 3)   # cada columna arranca un tercio del juego mas alla de la anterior: las fotos vecinas no se repiten
    cols = []
    for c in range(MURAL_COLUMNAS):
        d = (c * paso) % n
        orden = claves[d:] + claves[:d]
        # la primera tanda se pide ya; la segunda solo cierra el bucle y se carga cuando haga falta (son los mismos archivos)
        pista = "".join(_tesela(C, k, False) for k in orden) + "".join(_tesela(C, k, True) for k in orden)
        cols.append(f'<div class="col"><div class="pista">{pista}</div></div>')
    return f'<div class="mural">{"".join(cols)}</div>'


def _titular(nombre):
    """H1 en lineas de cartel. La palabra mas larga lleva el color de la marca."""
    palabras = nombre.split()
    acento = max(range(len(palabras)), key=lambda i: len(palabras[i]))
    lineas, k = [], 0
    for ln in temas.lineas_titular(nombre):
        ws = []
        for w in ln.split(" "):
            ws.append(f'<span class="acento">{e_(w)}</span>' if k == acento else e_(w))
            k += 1
        lineas.append(f'<span class="linea" style="--i:{len(lineas)}"><span>{" ".join(ws)}</span></span>')
    return "".join(lineas), max(len(x) for x in temas.lineas_titular(nombre))


def _nav(F):
    T = F.get("textos", {})
    destinos = {"carta": ("#carta", T.get("nav_carta", "Menú")), "fotos": ("#fotos", T.get("nav_fotos", "Fotos")), "visita": ("#visitanos", "Visítanos")}
    return "".join(f'<a href="{h}">{e_(t)}</a>' for s in F["estilo"]["orden"] if s in destinos for h, t in [destinos[s]])


def _estado_horario(F, C):
    if C["horario_pendiente"]:
        return f'<p class="estado pendiente">Horario por confirmar: {e_(F["horario_texto"])}</p>'
    return '<p class="estado" data-open><span data-open-text>Ver horario</span></p>'


def portada(F, C):
    N = F["negocio"]
    nombre = N["nombre"]
    titular, mayor_linea = _titular(nombre)
    total = len(nombre)
    logo = C["logo"]
    if logo:
        marca = (f'<a class="logo-enlace" href="#inicio" aria-label="{e_(nombre)}, inicio">'
                 f'{picture_html(logo, "", "(min-width:900px) 68px, 56px", lazy=False)}</a>')
    else:
        marca = f'<a class="marca" href="#inicio">{e_(nombre)}</a>'
    botones = "".join(_enlace_accion(a, "btn" if i == 0 else "btn suave") for i, a in enumerate(acciones(F, C)["hero"]))
    lema_en = f'<span class="lema-en" lang="en">{e_(N["lema_en"])}</span>' if N.get("lema_en") else ""
    return f'''<header class="hero" id="inicio" style="--c:{mayor_linea};--ct:{total}">
<div class="hero-fondo" aria-hidden="true">{_mural(F, C)}<div class="velo"></div><div class="luz"></div><div class="grano"></div><canvas class="brasas"></canvas></div>
<div class="hero-barra">{marca}<div class="barra-der"><nav aria-label="Secciones">{_nav(F)}</nav><button type="button" class="pausa" data-pausa aria-pressed="false">{ICONO_PAUSA}{ICONO_PLAY}<span data-pausa-texto>Pausar animación</span></button></div></div>
<div class="hero-cuerpo"><div class="hero-titulo"><p class="sobre">{e_(N["cocina"])} · {e_(N["ciudad"])}</p>
<h1>{titular}</h1></div>
<div class="hero-base"><p class="lema">{e_(N["lema"])}{lema_en}</p>
<div class="hero-lado"><div class="acciones">{botones}</div>
{_estado_horario(F, C)}</div></div></div>
</header>'''


# ------------------------------------------------------------------ menu
def _item(F, C, p):
    lang = f' lang="{e_(p["lang"])}"' if p.get("lang") else ""
    en = f'<p class="nom-en" lang="en">{e_(p["nombre_en"])}</p>' if p.get("nombre_en") else ""
    des = f'<p class="des">{e_(p["descripcion"])}</p>' if p.get("descripcion") else ""
    if p.get("variantes"):
        precios = "".join(f'<span class="var"><span class="eti">{e_(v["etiqueta"])}</span>{_precio(C, v["precio"])}</span>' for v in p["variantes"])
    else:
        precios = f'<span class="var">{_precio(C, p["precio"])}</span>'
    sup = "".join(f'<p class="sup">{e_(s["etiqueta"])} +{_precio(C, s["precio"])}</p>' for s in p.get("suplementos", []))
    return (f'<li class="item" data-item="{e_(p["id"])}"><div class="item-txt"><p class="nom"{lang}>{e_(p["nombre"])}</p>{en}</div>'
            f'<div class="precios">{precios}</div>{des}{sup}</li>')


def _categoria(F, C, c):
    foto = ""
    if c.get("foto"):
        a = C["fotos"][c["foto"]]
        foto = f'<div class="cat-foto" style="--c:{a["color"]}">{picture_html(a["datos"], "", "(min-width:900px) 96px, 80px")}</div>'
    nota = f'<p class="cat-nota">{e_(c["nota"])}</p>' if c.get("nota") else ""
    clase = "cat lista" if c.get("presentacion") == "lista" else "cat"
    items = "".join(_item(F, C, p) for p in c["platos"])
    return (f'<section class="{clase}" id="cat-{e_(c["id"])}" aria-labelledby="h-{e_(c["id"])}">'
            f'<div class="cat-cab"><div><h3 id="h-{e_(c["id"])}">{e_(c["titulo"])}</h3>{nota}</div>{foto}</div><ul class="items">{items}</ul></section>')


def carta(F, C):
    T = F["textos"]
    chips = "".join(f'<li><a href="#cat-{e_(c["id"])}">{e_(c.get("chip") or c["titulo"])}</a></li>' for c in F["carta"])
    cats = "".join(_categoria(F, C, c) for c in F["carta"])
    nota = f'<p class="nota-precios">{e_(T["carta_nota"])}</p>' if T.get("carta_nota") else ""
    return f'''<section class="carta" id="carta" aria-labelledby="t-carta"><div class="caja carta-cab">
<p class="sobretitulo">{e_(T["carta_sobretitulo"])}</p><h2 id="t-carta">{e_(T["carta_titulo"])}</h2>{nota}</div>
<nav class="chips" aria-label="Categorías del menú"><div class="caja"><ul>{chips}</ul></div></nav>
<div class="caja cats">{cats}</div></section>'''


# ------------------------------------------------------------------ fotos
def fotos(F, C):
    T = F["textos"]
    figs = []
    for i, g in enumerate(F["galeria"]):
        a = C["fotos"][g["foto"]]
        pic = picture_html(a["datos"], F["activos"][g["foto"]]["alt"], "(min-width:900px) 17vw, 30vw")
        figs.append(f'<figure class="rv" style="--c:{a["color"]};--d:{i * 70}ms"><div class="marco">{pic}</div><figcaption>{e_(g["pie"])}</figcaption></figure>')
    ig = F["contacto"].get("instagram")
    boton = f'<a class="btn suave" href="{ig["url"]}" target="_blank" rel="noopener">{ICONO_IG} Ver más en Instagram</a>' if ig else ""
    return f'''<section class="fotos" id="fotos" aria-labelledby="t-fotos"><div class="caja">
<div class="fotos-txt"><p class="sobretitulo rv">{e_(T["fotos_sobretitulo"])}</p><h2 id="t-fotos" class="rv">{e_(T["fotos_titulo"])}</h2><p class="rv">{e_(T["fotos_texto"])}</p>{boton}</div>
<div class="galeria" role="group" aria-label="{e_(T["fotos_aria"])}">{"".join(figs)}</div></div></section>'''


# ------------------------------------------------------------------ visita
def visita(F, C):
    N, K, T = F["negocio"], F["contacto"], F["textos"]
    como = mapa_url(K["mapa_consulta"])
    # si la direccion ya nombra la ciudad (como en Estados Unidos), la segunda linea es solo el pais
    linea_pais = e_(nombre_pais(N)) if N["ciudad"].lower() in N["direccion"].lower() else f'{e_(N["ciudad"])}, {e_(nombre_pais(N))}'
    botones = [f'<a class="btn" href="{como}" target="_blank" rel="noopener">{ICONO_MAPA} Cómo llegar</a>']
    if K.get("telefono"):
        etiqueta = f'Llamar al {K["telefono_visible"]}' if K.get("telefono_visible") else "Llamar"
        botones.append(f'<a class="btn suave" href="tel:{K["telefono"]}">{ICONO_TEL} {e_(etiqueta)}</a>')
    if C["horario_pendiente"]:
        horas = (f'<div class="dato"><h3>Horario</h3><p class="horario-texto">{e_(F["horario_texto"])}</p>'
                 f'<p class="aviso-datos">{e_(T["horario_aviso"])}</p></div>')
    else:
        filas = "".join(f'<li data-dia="{k}"><span>{n}</span><span>{rango_horario(F["horario"].get(k, []))}</span></li>' for k, n in DIAS)
        horas = (f'<div class="dato"><h3>Horario</h3><p class="estado" data-open><span data-open-text>Ver horario</span></p>'
                 f'<ul class="horas" aria-label="Horario">{filas}</ul></div>')
    reparto = ""
    if K.get("reparto"):
        nombres = " y ".join(e_(r["nombre"]) for r in K["reparto"])
        texto = e_(T["reparto_texto"]).replace("{apps}", nombres)
        reparto = f'<div class="dato"><h3>Pedidos a domicilio</h3><p>{texto}</p></div>'
    redes = []
    for clave, icono, nombre in (("instagram", ICONO_IG, "Instagram"), ("tiktok", ICONO_TIKTOK, "TikTok")):
        r = K.get(clave)
        if r:
            redes.append(f'<a class="btn suave" href="{r["url"]}" target="_blank" rel="noopener">{icono} {nombre} @{e_(r["usuario"])}</a>')
    bloque_redes = f'<div class="dato"><h3>Redes</h3><div class="redes">{"".join(redes)}</div></div>' if redes else ""
    return f'''<section class="visita" id="visitanos" aria-labelledby="t-vis"><div class="caja">
<div class="rv"><h2 id="t-vis">{e_(T["visita_titulo"])}</h2><address>{e_(N["direccion"])}<br>{linea_pais}</address>
<div class="vis-botones">{"".join(botones)}</div></div>
<div class="datos rv" style="--d:120ms">{horas}{reparto}{bloque_redes}</div></div></section>'''


def _extras(F, C):
    return ""


PERSONALIDAD = {
    "portada": portada,
    "secciones": {"carta": carta, "fotos": fotos, "visita": visita, "cierre": cierre_muestra},
    "extras": _extras,
    "css_extra": (".carta,.panel-edu{--foco-anillo:var(--foco-anillo-papel)}.cinta{--foco-anillo:var(--foco-anillo-papel)}"
                  "@media (prefers-reduced-motion:reduce){.pista,.luz{animation:none}}"),
    "js_extra": "",
    "requiere_hero": False,
    "admite_variantes": True,
    "descripcion_opcional": True,
    "mide_apertura": False,
    "textos": ["carta_titulo", "carta_sobretitulo", "fotos_sobretitulo", "fotos_titulo", "fotos_texto", "fotos_aria", "visita_titulo"],
}
