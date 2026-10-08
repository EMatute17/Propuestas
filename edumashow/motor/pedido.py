"""Pedido por WhatsApp: las piezas que comparten las personalidades (filas de opciones con Agregar, suplementos,
barra del pedido, hoja del ticket y la sección Cómo pedir).

El carrito vive en plantillas/pedido.js y solo existe en el navegador de quien pide: no guarda nada (ni cookies ni
almacenamiento), no pide datos que no hagan falta y no promete lo que el restaurante no ha confirmado. Sin JavaScript la
carta se lee igual (sin los botones de agregar) y se ofrece llamar.

En una muestra el pedido siempre va al WhatsApp de la agencia, rotulado como prueba: nadie le manda un pedido de mentira
a un restaurante real (R-MUE-02)."""
from urllib.parse import quote

from .piezas import ICONO_TEL, ICONO_WA, e_

# Textos de la interfaz del pedido. La ficha puede cambiar cualquiera con pedido.textos.
TEXTOS = {
    "ticket_titulo": "Tu ticket",
    "vacio": "Todavía no hay nada. Toca Agregar en el menú y tu pedido va apareciendo aquí.",
    "total": "Total",
    "productos_uno": "producto",
    "productos_varios": "productos",
    "nombre": "Tu nombre",
    "nota": "Notas para tu pedido (opcional)",
    "nota_ejemplo": "Una indicación para la cocina",
    "enviar_wa": "Enviar pedido por WhatsApp",
    "enviar_prueba": "Enviar pedido de prueba por WhatsApp",
    "llamar": "Prefiero llamar",
    "copiar": "Copiar mi pedido",
    "copiado": "Pedido copiado",
    "vaciar": "Vaciar ticket",
    "ver": "Ver mi pedido",
    "cerrar": "Cerrar",
    "falta_nombre": "Escribe tu nombre para poder enviar el pedido.",
    "aviso_muestra": "Es una muestra: este pedido te llega a Edumashow como prueba, no al restaurante. Cuando la página sea tuya, llegará a tu WhatsApp.",
    "aviso_precios": "Los precios salen del menú público del restaurante y están por confirmar.",
    "no_abrio": "Si no se abrió WhatsApp,",
    "no_abrio_enlace": "tócalo aquí",
    "saludo": "Hola {negocio}, quiero hacer este pedido:",
    "a_nombre": "A nombre de",
    "notas": "Notas",
    "agregado": "Agregado",
    "quitado": "Quitado",
    "en_el_pedido": "en tu pedido",
    "vacio_aviso": "Tu ticket quedó vacío",
    "quitar_uno": "Quitar uno de",
    "agregar_uno": "Agregar uno más de",
    "agregar": "Agregar",
    "pedir_como_titulo": "Cómo pedir",
    "paso1_t": "Elige",
    "paso1_x": "Mira el menú y toca Agregar en lo que quieras.",
    "paso2_t": "Arma tu ticket",
    "paso2_x": "Tu pedido se va sumando solo, con el total siempre a la vista.",
    "paso3_t_wa": "Envíalo",
    "paso3_x_wa": "Con un toque lo mandas por WhatsApp.",
    "paso3_t_llamada": "Llámanos",
    "paso3_x_llamada": "Con tu ticket a la mano, pides en una llamada.",
    "paso3_x_muestra": "Con un toque lo mandas por WhatsApp. En esta muestra llega a Edumashow como prueba.",
    "sin_js": "Para armar el pedido aquí hace falta JavaScript. Mientras tanto puedes llamar",
    "sin_js_corto": "Para armar el pedido aquí hace falta JavaScript.",
}


def activo(F):
    return bool(F.get("pedido"))


def textos(F):
    t = dict(TEXTOS)
    t.update((F.get("pedido") or {}).get("textos", {}))
    return t


def destino_wa(F, C):
    """WhatsApp que recibe los pedidos: en una muestra, siempre el de la agencia."""
    return C["agencia"]["whatsapp"] if C["muestra"] else F["contacto"].get("whatsapp")


def canal(F, C):
    """whatsapp o llamada: lo que la ficha declara, y sin WhatsApp al que enviar, el pedido se canta por teléfono."""
    c = (F.get("pedido") or {}).get("canal", "whatsapp")
    if c == "whatsapp" and not destino_wa(F, C):
        return "llamada"
    return c


def config_js(F, C):
    """Lo que el JavaScript del ticket necesita saber. Los textos viajan aquí para que haya un solo lugar donde escribirlos."""
    P = F["pedido"]
    K = F["contacto"]
    t = textos(F)
    t["saludo"] = t["saludo"].replace("{negocio}", F["negocio"]["nombre"])
    return {
        "canal": canal(F, C), "muestra": bool(C["muestra"]), "precios_por_confirmar": F.get("confirmacion", {}).get("estado") == "por_confirmar",
        "wa": destino_wa(F, C), "prefijo": C["prefijo_wa_pedido"], "tel": K.get("telefono"), "tel_visible": K.get("telefono_visible"),
        "t": t, "ejemplo_nota": P.get("nota_ejemplo") or t["nota_ejemplo"],
    }


# ------------------------------------------------------------------ filas de opciones (cada una se puede agregar al ticket)
def _precio(C, valor):
    return f'<data class="pre" value="{valor}">{e_(C["importe"](valor))}</data>'


def _nombre_accion(p, etiqueta):
    return p["nombre"] + (f", {etiqueta}" if etiqueta else "")


def _controles(F, p, etiqueta):
    t = textos(F)
    n = _nombre_accion(p, etiqueta)
    return (f'<span class="ctl"><button type="button" class="add" data-add aria-label="{e_(t["agregar"])} {e_(n)}"><span class="mas" aria-hidden="true"></span><span class="add-txt">{e_(t["agregar"])}</span></button>'
            f'<span class="paso" hidden><button type="button" class="menos" data-menos aria-label="{e_(t["quitar_uno"])} {e_(n)}"><span aria-hidden="true"></span></button>'
            f'<output class="qty" data-q>0</output>'
            f'<button type="button" class="mas-uno" data-mas aria-label="{e_(t["agregar_uno"])} {e_(n)}"><span aria-hidden="true"></span></button></span></span>')


def opciones(F, C, p, pedir):
    """Lista de opciones de un plato: una fila por precio (una sola si no hay variantes). Con pedir, cada fila lleva su botón Agregar."""
    if p.get("variantes"):
        filas = "".join(f'<li class="op" data-op="{e_(p["id"])}~{k}"><span class="eti">{e_(v["etiqueta"])}</span>{_precio(C, v["precio"])}'
                        f'{_controles(F, p, v["etiqueta"]) if pedir else ""}</li>' for k, v in enumerate(p["variantes"]))
        return f'<ul class="ops">{filas}</ul>'
    return f'<div class="ops"><div class="op" data-op="{e_(p["id"])}">{_precio(C, p["precio"])}{_controles(F, p, None) if pedir else ""}</div></div>'


def suplementos(F, C, p, pedir):
    """Extras opcionales de un plato. Con pedir son interruptores (nacen apagados); sin pedir, una línea de texto."""
    if not p.get("suplementos"):
        return ""
    if not pedir:
        return "".join(f'<p class="sup">{e_(s["etiqueta"])} +{_precio(C, s["precio"])}</p>' for s in p["suplementos"])
    botones = "".join(f'<button type="button" class="sup-btn" data-sup="{k}" aria-pressed="false"><span class="chk" aria-hidden="true"></span>'
                      f'<span class="sup-et">{e_(s["etiqueta"])}</span><span class="sup-mas">+{_precio(C, s["precio"])}</span></button>' for k, s in enumerate(p["suplementos"]))
    return f'<div class="sups" role="group" aria-label="Extras de {e_(p["nombre"])}">{botones}</div>'


def molde(F, C):
    """Plantilla (inerte, no se muestra) del ticket. El JavaScript la copia una vez para el ticket lateral y otra para la hoja."""
    t = textos(F)
    K = F["contacto"]
    cn = canal(F, C)
    llamar_href = f'tel:{K["telefono"]}' if K.get("telefono") else ""
    avisos = []
    if C["muestra"]:
        avisos.append(f'<p class="tk-nota">{e_(t["aviso_muestra"])}</p>')
    if F.get("confirmacion", {}).get("estado") == "por_confirmar":
        avisos.append(f'<p class="tk-nota">{e_(t["aviso_precios"])}</p>')
    if cn == "whatsapp":
        enviar = t["enviar_prueba"] if C["muestra"] else t["enviar_wa"]
        # el enlace de respaldo ya apunta al WhatsApp correcto (el pedido completo lo pone el JavaScript al enviar): un enlace sin destino no sirve ni se rastrea
        aviso_href = "https://wa.me/" + destino_wa(F, C) + "?text=" + quote(C["prefijo_wa_pedido"] + t["saludo"].replace("{negocio}", F["negocio"]["nombre"]), safe="")
        campos = (f'<div class="campo"><label for="tk-nombre-{{v}}">{e_(t["nombre"])}</label><input id="tk-nombre-{{v}}" name="nombre" autocomplete="name" required></div>'
                  f'<div class="campo"><label for="tk-nota-{{v}}">{e_(t["nota"])}</label><textarea id="tk-nota-{{v}}" name="nota"></textarea></div>'
                  f'<p class="aviso" data-tk-error role="alert" hidden></p>')
        acciones = (f'<button type="submit" class="btn tk-enviar">{ICONO_WA} {e_(enviar)}</button>'
                    f'<p class="aviso-wa" data-tk-noabrio hidden>{e_(t["no_abrio"])} <a href="{aviso_href}" target="_blank" rel="noopener">{e_(t["no_abrio_enlace"])}</a>.</p>')
        if llamar_href:
            acciones += f'<a class="btn suave tk-llamar" href="{llamar_href}">{ICONO_TEL} {e_(t["llamar"])}</a>'
    else:
        campos = ""
        acciones = (f'<a class="btn tk-llamar" href="{llamar_href}">{ICONO_TEL} Llamar para pedir</a>'
                    f'<button type="button" class="btn suave tk-copiar">{e_(t["copiar"])}</button>'
                    f'<p class="aviso-wa" data-tk-copiado role="status" hidden>{e_(t["copiado"])}</p>')
    return (f'<template id="tk-molde"><div class="tk-cab"><p class="tk-tit" role="heading" aria-level="3" id="tk-tit-{{v}}">{e_(t["ticket_titulo"])}</p>'
            f'<p class="tk-cuenta"><b data-tk-n>0</b> <span data-tk-unidad>{e_(t["productos_varios"])}</span></p></div>'
            f'<p class="tk-vacio" data-tk-vacio>{e_(t["vacio"])}</p>'
            f'<div class="tk-cuerpo" data-tk-cuerpo hidden><ul class="tk-lineas" data-tk-lineas></ul>'
            f'<p class="tk-total"><span>{e_(t["total"])}</span><b data-tk-total></b></p>'
            f'<form class="tk-form" novalidate>{campos}{acciones}<button type="button" class="tk-vaciar" data-tk-vaciar>{e_(t["vaciar"])}</button>{"".join(avisos)}</form></div></template>')


# ------------------------------------------------------------------ barra, hoja y avisos
def extras(F, C):
    """Barra fija del pedido, hoja del ticket (diálogo) y zona de avisos para lectores de pantalla. Todo nace oculto y lo muestra el JavaScript."""
    if not activo(F):
        return ""
    t = textos(F)
    K = F["contacto"]
    llamar = ""
    if K.get("telefono"):
        etiqueta = f'Llamar al {K["telefono_visible"]}' if K.get("telefono_visible") else "Llamar"
        llamar = f'<a class="pb-llamar" href="tel:{K["telefono"]}" aria-label="{e_(etiqueta)}">{ICONO_TEL}</a>'
    barra = (f'<div class="pedido-barra" id="pedido-barra" hidden>{llamar}<button type="button" class="pb-ver" data-abrir-hoja aria-haspopup="dialog">'
             f'<span class="pb-n" data-barra-n>0</span><span class="pb-txt">{e_(t["ver"])}</span><b class="pb-total" data-barra-total></b></button></div>')
    hoja = (f'<dialog class="hoja-pedido" id="hoja-pedido" aria-labelledby="tk-tit-hoja"><button type="button" class="cerrar" data-cerrar-hoja aria-label="{e_(t["cerrar"])}"><span aria-hidden="true"></span></button>'
            f'<div class="tk" data-ticket="hoja"></div></dialog>')
    vivo = '<div class="sr-only" id="pedido-vivo" role="status" aria-live="polite" aria-atomic="true"></div>'
    return barra + hoja + vivo + molde(F, C)


def ticket_lateral(F, C):
    """Ticket fijo al lado del menú en pantallas anchas. Lo rellena el JavaScript."""
    if not activo(F):
        return ""
    return '<div class="ticket" data-ticket="lado" role="region" aria-label="Tu pedido"></div>'


def sin_js(F, C):
    """Aviso para quien no ejecuta JavaScript: se puede leer la carta y llamar."""
    if not activo(F):
        return ""
    t = textos(F)
    K = F["contacto"]
    if K.get("telefono"):
        etiqueta = K.get("telefono_visible") or K["telefono"]
        return f'<noscript><p class="aviso-js">{e_(t["sin_js"])} al <a href="tel:{K["telefono"]}">{e_(etiqueta)}</a>.</p></noscript>'
    return f'<noscript><p class="aviso-js">{e_(t["sin_js_corto"])}</p></noscript>'


# ------------------------------------------------------------------ cómo pedir
def como_pedir(F, C):
    if not activo(F):
        return ""
    t = textos(F)
    wa = canal(F, C) == "whatsapp"
    p3t = t["paso3_t_wa"] if wa else t["paso3_t_llamada"]
    p3x = (t["paso3_x_muestra"] if C["muestra"] else t["paso3_x_wa"]) if wa else t["paso3_x_llamada"]
    pasos = [(t["paso1_t"], t["paso1_x"]), (t["paso2_t"], t["paso2_x"]), (p3t, p3x)]
    lis = "".join(f'<li class="paso-c rv" data-superpuesto style="--d:{i * 110}ms;--giro:{(-1.6, 1.2, -0.8)[i]}deg"><span class="n" aria-hidden="true">{i + 1}</span><h3>{e_(a)}</h3><p>{e_(b)}</p></li>'
                  for i, (a, b) in enumerate(pasos))
    return (f'<section class="como" id="como-pedir" aria-labelledby="t-como"><div class="caja"><h2 id="t-como" class="rv">{e_(t["pedir_como_titulo"])}</h2>'
            f'<ol class="pasos-c">{lis}</ol></div></section>')


def validar(F, C_muestra):
    """Faltas de la ficha para que el pedido funcione. Devuelve una lista (vacía si todo bien)."""
    falta = []
    P = F.get("pedido")
    if not P:
        return falta
    K = F.get("contacto", {})
    if P.get("canal", "whatsapp") not in ("whatsapp", "llamada"):
        falta.append("pedido.canal (whatsapp o llamada)")
    if P.get("canal") == "llamada" and not K.get("telefono"):
        falta.append("pedido.canal llamada necesita contacto.telefono")
    if F.get("modo") == "final" and P.get("canal", "whatsapp") == "whatsapp" and not K.get("whatsapp"):
        falta.append("pedido por WhatsApp necesita contacto.whatsapp en el modo final")
    for c in F.get("carta", []):
        for p in c.get("platos", []):
            for s in p.get("suplementos", []):
                if not s.get("etiqueta") or not isinstance(s.get("precio"), (int, float)):
                    falta.append(f"carta.{c.get('id')}.{p.get('id')} (suplemento sin etiqueta o sin precio)")
    return falta
