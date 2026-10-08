"""Portadas del catálogo (la dimensión que más se nota, R-VAR-04). Cada función recibe la ficha (F) y el contexto de construcción (C) y devuelve el HTML
de la portada. Comparten con las clásicas los datos, los botones, el estado de apertura y la calificación de Google; cambian la composición.

  elegante: marco_editorial (papel, titular por palabras y foto en arco con sello giratorio) y cortina (foto a pantalla completa con marco fino y cortina que se abre).
  urbano:   collage_pegatinas (fotos como polaroids que caen sobre un fondo de puntos) y cartel_rotulo (cartel de color de marca con disco de foto y cinta que corre).
"""
from .imagenes import picture_html
from .piezas import (ICONO_PAUSA, ICONO_PLAY, _enlace_accion, acciones, e_, estado_y_valoracion, hero_picture, letras_titular, luz_html, nav_elegante,
                     paralaje_attr, particulas_html)
from . import piezas_urbano as U


def _botones(F, C):
    return "".join(_enlace_accion(a, "btn" if i == 0 else "btn suave") for i, a in enumerate(acciones(F, C)["hero"]))


def _pausa():
    return f'<button type="button" class="pausa" data-pausa aria-pressed="false">{ICONO_PAUSA}{ICONO_PLAY}<span data-pausa-texto>Pausar animación</span></button>'


def sello_circular(F, clase, idn, anillo_solo=False):
    """Sello con la cocina y la ciudad escritas en el borde, que gira despacio. Decorativo: el texto ya está en la portada."""
    N = F["negocio"]
    base = f'{N["cocina"].upper()} · {N["ciudad"].upper()} · '
    if len(base) > 54:
        base = f'{" ".join(N["cocina"].upper().split()[:3])} · {N["ciudad"].upper()} · '
    while len(base) < 34:
        base += base
    tam = max(9.0, min(15.0, 470 / (len(base) * 0.66)))
    return (f'<div class="{clase}" aria-hidden="true" data-decorativo><svg viewBox="0 0 200 200" focusable="false">'
            f'<defs><path id="anillo-{idn}" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>'
            f'<circle cx="100" cy="100" r="{85 if anillo_solo else 98}" class="s-fondo"/><circle cx="100" cy="100" r="55" class="s-centro"/>'
            f'<g class="s-giro"><text class="s-anillo" style="font-size:{tam:.1f}px"><textPath href="#anillo-{idn}" textLength="482" lengthAdjust="spacing">{e_(base)}</textPath></text></g>'
            f'<path class="s-estrella" d="M100 72 L108 92 L130 94 L113 108 L119 130 L100 118 L81 130 L87 108 L70 94 L92 92 Z"/></svg></div>')


# ------------------------------------------------------------------ elegante: marco_editorial
def portada_marco(F, C):
    N = F["negocio"]
    nombre = N["nombre"]
    palabras = nombre.split(" ")
    n = len(palabras)
    pic, foco, _ = hero_picture(C, paralaje_attr(C, 5))
    hs = "".join(f'<span class="mp"><span class="mp-i{" mp-ultima" if i == n - 1 else ""}" data-anim-titulo style="--i:{i}">{e_(w)}</span></span>' for i, w in enumerate(palabras))
    mas_larga = max(len(w) for w in palabras)
    return f'''<header class="hero hero-marco" id="inicio" style="--c:{mas_larga};--foco:{foco}">
<div class="hero-barra"><a class="marca" href="#inicio" aria-label="{e_(nombre)}, inicio">{e_(nombre)}</a><div class="barra-der">{nav_elegante()}{_pausa()}</div></div>
<div class="marco-cuerpo"><div class="marco-texto"><p class="marco-sobre"><span>{e_(N["cocina"])}</span><i aria-hidden="true"></i><span>{e_(N["ciudad"])}</span></p>
<h1><span class="sr-only">{e_(nombre)}</span><span aria-hidden="true" class="marco-h1">{hs}</span></h1>
<p class="lema">{e_(N["lema"])}</p>
<div class="acciones">{_botones(F, C)}</div>
{estado_y_valoracion(F, C, '<p class="estado" data-open><span data-open-text>Ver horario</span></p>')}</div>
<div class="marco-foto" aria-hidden="true"><div class="arco">{pic}{luz_html(C)}{particulas_html(C, "claro")}</div><span class="filete"></span>{sello_circular(F, "sello-marco", "marco")}</div></div>
</header>'''


# ------------------------------------------------------------------ elegante: cortina
def portada_cortina(F, C):
    N = F["negocio"]
    nombre = N["nombre"]
    letras, mas_larga = letras_titular(nombre)
    pic, foco, lqip = hero_picture(C, paralaje_attr(C))
    return f'''<header class="hero hero-cortina" id="inicio" style="--c:{mas_larga};--foco:{foco}">
<div class="hero-fondo" aria-hidden="true" style="--lqip:url({lqip})">{pic}<div class="velo"></div>{luz_html(C)}<div class="grano"></div>{particulas_html(C)}</div>
<span class="cortina-hoja izq" aria-hidden="true"></span><span class="cortina-hoja der" aria-hidden="true"></span>
<div class="hero-barra"><a class="marca" href="#inicio" aria-label="{e_(nombre)}, inicio">{e_(nombre)}</a><div class="barra-der">{nav_elegante()}{_pausa()}</div></div>
<div class="hero-cuerpo cortina-cuerpo"><p class="cortina-sobre"><span>{e_(N["cocina"])}</span><b aria-hidden="true"></b><span>{e_(N["ciudad"])}</span></p>
<h1><span class="sr-only">{e_(nombre)}</span><span aria-hidden="true">{letras}</span></h1>
<p class="lema">{e_(N["lema"])}</p>
<div class="acciones">{_botones(F, C)}</div>
{estado_y_valoracion(F, C, '<p class="estado" data-open><span data-open-text>Ver horario</span></p>')}</div>
</header>'''


# ------------------------------------------------------------------ urbano: collage_pegatinas
def _marca_urbana(F, C):
    nombre = F["negocio"]["nombre"]
    if C["logo"]:
        return (f'<a class="logo-enlace" href="#inicio" aria-label="{e_(nombre)}, inicio">'
                f'{picture_html(C["logo"], "", "(min-width:900px) 68px, 56px", lazy=False)}</a>')
    return f'<a class="marca" href="#inicio">{e_(nombre)}</a>'


def portada_collage(F, C):
    N = F["negocio"]
    nombre = N["nombre"]
    titular, mayor_linea = U._titular(nombre)
    claves = list(dict.fromkeys(g["foto"] for g in U._galeria(F, C)))[:5]
    pols = "".join(f'<figure class="pol" style="--i:{i}">{picture_html(C["fotos"][k]["datos"], "", "(min-width:1000px) 15rem, 9rem", lazy=False)}</figure>' for i, k in enumerate(claves))
    lema_en = f'<span class="lema-en" lang="en">{e_(N["lema_en"])}</span>' if N.get("lema_en") else ""
    return f'''<header class="hero hero-collage" id="inicio" style="--c:{mayor_linea};--ct:{len(nombre)}">
<div class="hero-fondo" aria-hidden="true"><div class="puntos"></div><div class="velo"></div><div class="grano"></div>{particulas_html(C)}</div>
<div class="hero-barra">{_marca_urbana(F, C)}<div class="barra-der"><nav aria-label="Secciones">{U._nav(F, C)}</nav>{_pausa()}</div></div>
<div class="collage" aria-hidden="true" data-decorativo>{pols}</div>
{U._pegatina(F, C)}
<div class="hero-cuerpo"><div class="hero-titulo"><p class="sobre">{e_(N["cocina"])} · {e_(N["ciudad"])}</p>
<h1>{titular}</h1></div>
<div class="hero-base"><p class="lema">{e_(N["lema"])}{lema_en}</p>
<div class="hero-lado"><div class="acciones">{_botones(F, C)}</div>
{estado_y_valoracion(F, C, U._estado_horario(F, C))}</div></div></div>
</header>'''


# ------------------------------------------------------------------ urbano: cartel_rotulo
def portada_cartel(F, C):
    N = F["negocio"]
    nombre = N["nombre"]
    titular, mayor_linea = U._titular(nombre)
    claves = list(dict.fromkeys(g["foto"] for g in U._galeria(F, C)))
    disco = ""
    if claves:
        disco = (f'<div class="cartel-disco" aria-hidden="true" data-decorativo><div class="disco-foto">{picture_html(C["fotos"][claves[0]]["datos"], "", "(min-width:900px) 17rem, 8rem", lazy=False)}</div>'
                 f'{sello_circular(F, "disco-anillo", "cartel", True)}</div>')
    palabras = F.get("textos", {}).get("marquesina") or [c["titulo"] for c in F["carta"]] + [N["cocina"], N["ciudad"]]
    una = "".join(f"<span>{e_(w)}</span>" for w in palabras)
    lema_en = f'<span class="lema-en" lang="en">{e_(N["lema_en"])}</span>' if N.get("lema_en") else ""
    return f'''<header class="hero hero-cartel" id="inicio" style="--c:{mayor_linea};--ct:{len(nombre)}">
<div class="hero-fondo" aria-hidden="true"><div class="puntos"></div>{particulas_html(C)}</div>
<div class="hero-barra">{_marca_urbana(F, C)}<div class="barra-der"><nav aria-label="Secciones">{U._nav(F, C)}</nav>{_pausa()}</div></div>
{disco}
<div class="hero-cuerpo"><div class="hero-titulo"><p class="sobre">{e_(N["cocina"])} · {e_(N["ciudad"])}</p>
<h1>{titular}</h1></div>
<div class="hero-base"><p class="lema">{e_(N["lema"])}{lema_en}</p>
<div class="hero-lado"><div class="acciones">{_botones(F, C)}</div>
{estado_y_valoracion(F, C, U._estado_horario(F, C))}</div></div></div>
<div class="cartel-cinta" aria-hidden="true" data-decorativo><div class="pista-m">{una}{una}</div></div>
</header>'''


ELEGANTE = {"marco_editorial": portada_marco, "cortina": portada_cortina}
URBANO = {"collage_pegatinas": portada_collage, "cartel_rotulo": portada_cartel}
