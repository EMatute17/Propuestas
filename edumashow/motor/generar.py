"""Generador de sitios Edumashow: ficha -> carpeta lista para subir a Netlify o Cloudflare Pages.

Uso:
    python3 -m edumashow.motor.generar edumashow/fichas/lumbre.json --salida muestras [--base-url URL]

El generador nunca aprueba su propia salida: la aprueba el Gate (edumashow/gate), que comprueba el
paquete exacto por su hash (R-PRO-01 y R-PRO-02).
"""
import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import shutil
import sys
import zipfile

import rcssmin
import rjsmin

from . import color, dinero, estilo as _estilo, huella as _huella, imagenes, pedido, piezas, temas, tipografia

VERSION_GENERADOR = "0.2.0"
RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PLANTILLAS = os.path.join(RAIZ, "motor", "plantillas")
ORIGEN_ACTIVOS = os.path.join(RAIZ, "activos", "origen")
REGISTRO_HUELLAS = os.path.join(RAIZ, "gate", "registro_huellas.json")

ESTADOS_CONFIRMACION = ("confirmado", "ejemplo", "por_confirmar")
PERSONALIDADES_CONOCIDAS = ("elegante", "urbano")


class FichaIncompleta(Exception):
    """El motor se abstiene: faltan datos críticos (R-DAT-08)."""


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def personalidad(nombre):
    """Módulo de piezas de una personalidad (cada una trae su portada, sus secciones y sus estilos)."""
    if nombre == "elegante":
        return piezas.PERSONALIDAD
    if nombre == "urbano":
        from . import piezas_urbano
        return piezas_urbano.PERSONALIDAD
    raise FichaIncompleta(f"estilo.personalidad desconocida: {nombre}")


def validar_ficha(F):
    falta = []
    N = F.get("negocio", {})
    for k in ("nombre", "cocina", "ciudad", "pais", "direccion", "zona_horaria", "lema", "descripcion"):
        if not N.get(k):
            falta.append(f"negocio.{k}")
    if N.get("pais") and N["pais"] not in dinero.PAISES:
        falta.append("negocio.pais (desconocido)")
    if F.get("moneda") not in dinero.MONEDAS:
        falta.append("moneda")
    K = F.get("contacto", {})
    if not K.get("mapa_consulta"):
        falta.append("contacto.mapa_consulta")
    horario_pendiente = F.get("horario_estado") == "por_confirmar"
    if horario_pendiente:
        if not F.get("horario_texto"):
            falta.append("horario_texto (el horario está por confirmar y falta el texto que se muestra)")
    elif not any(F.get("horario", {}).values()):
        falta.append("horario (todos los días vacíos)")

    est = F.get("estilo", {})
    pers = est.get("personalidad")
    P = personalidad(pers) if pers in PERSONALIDADES_CONOCIDAS else None
    if P is None:
        falta.append("estilo.personalidad (desconocida)")
    else:
        if est.get("paleta") not in temas.PALETAS and est.get("paleta") != "auto":
            falta.append("estilo.paleta (desconocida)")
        if est.get("forma") not in temas.FORMAS:
            falta.append("estilo.forma (desconocida)")
        if est.get("movimiento") not in temas.MOVIMIENTOS:
            falta.append("estilo.movimiento (desconocido)")
        if est.get("tipografia") not in tipografia.PAREJAS and est.get("tipografia") != "auto":
            falta.append("estilo.tipografia (desconocida)")
        for s in est.get("orden", []):
            if s != "portada" and s not in P["secciones"]:
                falta.append(f"estilo.orden: la sección {s} no existe en la personalidad {pers}")
        if "reserva" in est.get("orden", []) and not F.get("reservas"):
            falta.append("reservas (la sección reserva está en el orden)")
        if "idea" in est.get("orden", []) and not F.get("historia"):
            falta.append("historia (la sección idea está en el orden)")
        if P["requiere_hero"] and "hero" not in F.get("activos", {}):
            falta.append("activos.hero")
        for k in P["textos"]:
            if not F.get("textos", {}).get(k):
                falta.append(f"textos.{k}")
        if horario_pendiente and est.get("personalidad") == "urbano" and not F.get("textos", {}).get("horario_aviso"):
            falta.append("textos.horario_aviso (el horario está por confirmar)")
        if F.get("contacto", {}).get("reparto") and est.get("personalidad") == "urbano" and "{apps}" not in F.get("textos", {}).get("reparto_texto", ""):
            falta.append("textos.reparto_texto (debe llevar {apps})")
        if est.get("personalidad") == "urbano" and not F.get("galeria"):
            falta.append("galeria (el mural de la portada usa las fotos de la galería)")
        if "como" in est.get("orden", []) and not pedido.activo(F):
            falta.append("pedido (la sección como está en el orden)")
        if "regla" in est.get("orden", []):
            I = F.get("idea") or {}
            for k in ("categoria", "unidad", "por", "sobretitulo", "titulo", "texto", "mejor", "nota"):
                if not I.get(k):
                    falta.append(f"idea.{k} (la sección regla está en el orden)")
            cat = next((c for c in F.get("carta", []) if c.get("id") == I.get("categoria")), None)
            if cat is None:
                falta.append("idea.categoria no es una categoría de la carta")
            else:
                con_medida = [p_ for p_ in cat.get("platos", []) if p_.get("medida")]
                if len(con_medida) < 2 or any(not isinstance(p_.get("precio"), (int, float)) for p_ in con_medida):
                    falta.append("idea: la categoría necesita al menos dos platos con medida y un precio único cada uno")
    falta += pedido.validar(F, F.get("modo") == "muestra")

    if not F.get("carta"):
        falta.append("carta")
    for c in F.get("carta", []):
        if not c.get("id") or not c.get("titulo") or not c.get("platos"):
            falta.append(f"carta.{c.get('id')} (id, título y platos)")
        if c.get("foto") and c["foto"] not in F.get("activos", {}):
            falta.append(f"activos.{c['foto']}")
        for p in c.get("platos", []):
            tiene_precio = isinstance(p.get("precio"), (int, float)) and not isinstance(p.get("precio"), bool)
            variantes = p.get("variantes")
            if not p.get("id") or not p.get("nombre"):
                falta.append(f"carta.{c.get('id')}.{p.get('id')} (id y nombre)")
            if tiene_precio == bool(variantes):
                falta.append(f"carta.{c.get('id')}.{p.get('id')} (debe tener un precio o variantes con precio, no las dos cosas ni ninguna)")
            if variantes:
                if P is not None and not P["admite_variantes"]:
                    falta.append(f"carta.{c.get('id')}.{p.get('id')} (la personalidad {pers} no muestra variantes)")
                for v in variantes:
                    if not v.get("etiqueta") or not isinstance(v.get("precio"), (int, float)):
                        falta.append(f"carta.{c.get('id')}.{p.get('id')} (variante sin etiqueta o sin precio)")
            if P is not None and not P.get("descripcion_opcional") and not p.get("descripcion"):
                falta.append(f"carta.{c.get('id')}.{p.get('id')} (la personalidad {pers} exige descripción)")
            if p.get("foto") and p["foto"] not in F.get("activos", {}):
                falta.append(f"activos.{p['foto']}")
    for g in F.get("galeria", []):
        if g.get("foto") not in F.get("activos", {}):
            falta.append(f"activos.{g.get('foto')} (galería)")
    for clave, a in F.get("activos", {}).items():
        if not os.path.exists(os.path.join(ORIGEN_ACTIVOS, a.get("archivo", "?"))):
            falta.append(f"activos.{clave}.archivo (no existe {a.get('archivo')})")

    conf = F.get("confirmacion", {})
    if conf.get("estado") not in ESTADOS_CONFIRMACION or not conf.get("fecha"):
        falta.append("confirmación (estado y fecha)")
    if conf.get("estado") == "por_confirmar" and F.get("modo") != "muestra":
        falta.append("confirmacion.estado por_confirmar solo se admite en una muestra")
    if F.get("modo") == "final" and conf.get("estado") != "confirmado":
        falta.append("confirmacion.estado debe ser confirmado en el modo final")
    if F.get("modo") == "final" and horario_pendiente:
        falta.append("el horario no puede estar por confirmar en el modo final")
    if F.get("modo") == "final" and not (K.get("whatsapp") or K.get("telefono")):
        falta.append("contacto.whatsapp o contacto.telefono (obligatorio en el modo final)")
    if K.get("telefono") and not re.fullmatch(r"\+\d{8,15}", K["telefono"]):
        falta.append("contacto.telefono (formato internacional, por ejemplo +17867282934)")

    # una muestra de un negocio real declara de dónde salen los datos y las fotos y si hay permiso (R-MUE-05)
    M = F.get("muestra", {})
    if F.get("modo") == "muestra" and not M.get("ejemplo_ficticio", False):
        if M.get("permiso") not in ("pendiente", "concedido"):
            falta.append("muestra.permiso (pendiente o concedido, es un negocio real)")
        for k in ("origen_datos", "nota_panel"):
            if not M.get(k):
                falta.append(f"muestra.{k} (es un negocio real)")
        for clave, a in F.get("activos", {}).items():
            if not a.get("procedencia", {}).get("permiso"):
                falta.append(f"activos.{clave}.procedencia.permiso (es un negocio real)")

    # acciones pedidas: cada una necesita el dato con el que funciona
    A = F.get("acciones") or {}
    for donde in ("hero", "barra"):
        for a in A.get(donde, []):
            tipo = a if isinstance(a, str) else a.get("tipo")
            if tipo not in piezas.ETIQUETAS_ACCION:
                falta.append(f"acciones.{donde}: tipo desconocido {tipo}")
            elif tipo == "llamar" and not K.get("telefono"):
                falta.append(f"acciones.{donde}: llamar necesita contacto.telefono")
            elif tipo == "instagram" and not K.get("instagram", {}).get("url"):
                falta.append(f"acciones.{donde}: instagram necesita contacto.instagram.url")
            elif tipo == "reservar" and (not F.get("reservas") or "reserva" not in est.get("orden", [])):
                falta.append(f"acciones.{donde}: reservar necesita reservas y la sección reserva")
            elif tipo == "whatsapp" and not (K.get("whatsapp") or F.get("muestra", {}).get("ejemplo_ficticio")):
                falta.append(f"acciones.{donde}: whatsapp necesita contacto.whatsapp")
    if len(A.get("barra", [])) > 3:
        falta.append("acciones.barra: la barra del móvil admite tres acciones como máximo")
    if not A and not F.get("reservas"):
        falta.append("acciones (sin reservas, la ficha debe declarar sus acciones)")
    if falta:
        raise FichaIncompleta("Faltan o son inválidos: " + "; ".join(falta))


def sha256_archivo(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 16), b""):
            h.update(bloque)
    return h.hexdigest()


def hash_paquete(carpeta):
    """SHA-256 del paquete: de las rutas y los hashes de todos sus archivos salvo el manifiesto."""
    filas = []
    for dp, dn, fn in os.walk(carpeta):
        for f in sorted(fn):
            ruta = os.path.join(dp, f)
            rel = os.path.relpath(ruta, carpeta).replace(os.sep, "/")
            if rel == "manifiesto.json":
                continue
            filas.append(f"{rel}:{sha256_archivo(ruta)}")
    return hashlib.sha256("\n".join(sorted(filas)).encode()).hexdigest()


def _carga_fuente(familia, peso, estilo):
    """Texto para document.fonts.load: estilo, peso, tamaño y familia."""
    return f"{'' if estilo == 'normal' else estilo + ' '}{peso} 1em '{familia}'"


def construir(ruta_ficha, salida_base, base_url=None):
    F = leer(ruta_ficha)
    cfg = leer(os.path.join(RAIZ, "config.json"))
    validar_ficha(F)
    N = F["negocio"]
    est = F["estilo"]
    P = personalidad(est["personalidad"])
    muestra = F["modo"] == "muestra"
    ejemplo = muestra and F.get("muestra", {}).get("ejemplo_ficticio", False)
    horario_pendiente = F.get("horario_estado") == "por_confirmar"
    agencia = dict(cfg["agencia"])
    agencia["vigencia"] = F.get("muestra", {}).get("vigencia", "unas semanas")
    bid = hashlib.sha1((json.dumps(F, sort_keys=True) + VERSION_GENERADOR).encode()).hexdigest()[:8]
    carpeta = os.path.join(salida_base, F["id"])
    if os.path.isdir(carpeta):
        shutil.rmtree(carpeta)
    os.makedirs(carpeta)
    prefijo = f"assets/{bid}"

    # ---- director de estilo: paleta, tipografía y orden de fotos, cada una con su razón (se guardan en el manifiesto)
    registro_huellas = _huella.cargar_registro(REGISTRO_HUELLAS)
    D = _estilo.decidir(F, ORIGEN_ACTIVOS, registro_huellas)
    est_r = dict(est, paleta=D["paleta"]["id"], tipografia=D["tipografia"]["clave"])   # el estilo ya resuelto
    tokens_paleta = D["paleta"]["tokens"]

    # ---- tipografía
    fuentes = tipografia.preparar_pareja(est_r["tipografia"], os.path.join(carpeta, prefijo, "fonts"), f"{prefijo}/fonts")
    par = fuentes["pareja"]
    textos_para_glifos = json.dumps(F, ensure_ascii=False) + (json.dumps(pedido.textos(F), ensure_ascii=False) if pedido.activo(F) else "")
    faltan = tipografia.glifos_faltantes(par["texto"][0][0], textos_para_glifos)
    if faltan:
        raise FichaIncompleta("La tipografía no tiene estos caracteres: " + "".join(faltan))

    # ---- imágenes
    A = imagenes.Activos(carpeta, f"{prefijo}/img")
    procedencia = F.get("procedencia_activos", {})
    abiertas = {}

    def ruta_origen(clave):
        return os.path.join(ORIGEN_ACTIVOS, F["activos"][clave]["archivo"])

    def abrir(clave):
        if clave not in abiertas:
            abiertas[clave] = imagenes.abrir(ruta_origen(clave))
        return abiertas[clave]

    def prov(clave):
        """Procedencia de una imagen: la general de la ficha, afinada por la propia de ese activo, con el hash del archivo original."""
        p = dict(procedencia)
        p.update(F["activos"][clave].get("procedencia", {}))
        p["archivo_origen"] = F["activos"][clave]["archivo"]
        p["sha256_origen"] = sha256_archivo(ruta_origen(clave))
        return p

    hero, hero_im = None, None
    if "hero" in F["activos"]:
        h = F["activos"]["hero"]
        hero_im = abrir("hero")
        foco = tuple(h.get("foco", (0.5, 0.5)))
        ajustes = h.get("ajustes")
        hero = {
            "foco": foco,
            "escritorio": A.procesar("hero", hero_im, [800, 1280, 1920], prov("hero"), ajustes=ajustes, jpg_ancho=1280),
            "movil": A.procesar("hero-m", hero_im, [480, 768, 960], prov("hero"), recorte={"razon": 0.8, "foco": foco}, ajustes=ajustes, jpg_ancho=768),
        }
    logo = None
    if "logo" in F["activos"]:
        logo = A.procesar_logo("logo", imagenes.abrir_rgba(ruta_origen("logo")), [128, 256, 512], prov("logo"))
    fotos = {}

    def foto_general(k):
        """Foto sin recorte: hasta 480 px de ancho y el ancho original (no se amplía nada)."""
        if k not in fotos:
            im = abrir(k)
            anchos = sorted({min(480, im.width), im.width})
            d = A.procesar(k, im, anchos, prov(k), jpg_ancho=im.width)
            fotos[k] = {"datos": d, "color": d["color"]}

    for c in F["carta"]:
        for p in c["platos"]:
            k = p.get("foto")
            if k and k not in fotos:
                d = A.procesar(k, abrir(k), [210, 420], prov(k), jpg_ancho=420)
                fotos[k] = {"datos": d, "color": d["color"]}
    for c in F["carta"]:
        if c.get("foto"):
            foto_general(c["foto"])
    for g in F.get("galeria", []):
        foto_general(g["foto"])

    # ---- contexto de construcción
    wa_destino = agencia["whatsapp"] if ejemplo else F["contacto"].get("whatsapp")
    prefijo_wa = f"(Prueba de la muestra de Edumashow para {N['nombre']}) " if ejemplo else ""
    # un pedido de una muestra siempre va a la agencia y se rotula como prueba: nadie le manda un pedido de mentira a un restaurante real
    prefijo_wa_pedido = f"(Prueba de la muestra de Edumashow para {N['nombre']}) " if muestra else ""
    orden_fotos = D["fotos"]["orden_por_antojo"] if D["fotos"]["usa_el_orden"] else None
    C = {"muestra": muestra, "ejemplo": ejemplo, "agencia": agencia, "hero": hero, "logo": logo, "fotos": fotos, "orden_fotos": orden_fotos,
         "wa_destino": wa_destino, "prefijo_wa": prefijo_wa, "prefijo_wa_pedido": prefijo_wa_pedido, "importe": dinero.importe_fn(F), "horario_pendiente": horario_pendiente}

    # ---- CSS y JS
    cinta_h = "3.25rem" if muestra else "0rem"
    css = temas.tokens_css(tokens_paleta, est["forma"], est["movimiento"], par, max(len(w) for w in N["nombre"].split()), cinta_h, tipografia.ancho_em(est_r["tipografia"]))
    css += f"body{{--grano:{temas.grano_datauri()}}}"
    css += fuentes["css"]
    for nombre in ["base.css"] + (["pedido.css"] if pedido.activo(F) else []) + [f"{est['personalidad']}.css"]:
        with open(os.path.join(PLANTILLAS, nombre), encoding="utf-8") as f:
            css += "\n" + f.read()
    css += P["css_extra"]
    css_min = rcssmin.cssmin(css)

    disp = next(p for p in fuentes["precarga"] if p["rol"] == "display")
    txt_min = min(p["peso"] for p in fuentes["precarga"] if p["rol"] == "texto")
    Fjs = {
        "nombre": N["nombre"], "wa": wa_destino, "prefijo_wa": prefijo_wa, "tz": N["zona_horaria"],
        "horario": None if horario_pendiente else F["horario"], "moneda": F["moneda"],
    }
    if F.get("reservas"):
        R_ = F["reservas"]
        Fjs["reservas"] = {"paso": R_["paso_minutos"], "ultima": R_["ultima_antes_del_cierre_min"],
                           "antelacion": R_["antelacion_min"], "preferida": R_["hora_preferida"], "personas": R_["personas_por_defecto"]}
    Fjs["fmt"] = dinero.config_js(F)
    if pedido.activo(F):
        Fjs["pedido"] = pedido.config_js(F, C)
    Fjs["fuentes_carga"] = [_carga_fuente(par["familia_display"], disp["peso"], disp["estilo"]), _carga_fuente(par["familia_texto"], txt_min, "normal")]
    js = "window.__F=" + json.dumps(Fjs, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";\n"
    for nombre in ["base.js"] + (["pedido.js"] if pedido.activo(F) else []) + [f"{est['personalidad']}.js"]:
        with open(os.path.join(PLANTILLAS, nombre), encoding="utf-8") as f:
            js += f.read() + "\n"
    js += P["js_extra"]
    js_min = rjsmin.jsmin(js)

    # ---- HTML
    secciones = P["secciones"]
    main = "".join(secciones[s](F, C) for s in est["orden"] if s in secciones)
    titulo = f"{N['nombre']} · {N['cocina']} en {N['ciudad']}" + (" · Muestra de Edumashow" if muestra else "")
    meta = [f'<meta name="description" content="{piezas.e_(N["descripcion"])}">']
    if muestra:
        meta.append('<meta name="robots" content="noindex,nofollow">')
    meta += [f'<meta name="theme-color" content="{tokens_paleta["meta-color"]}">', '<meta name="color-scheme" content="dark light">',
             '<meta property="og:type" content="website">', f'<meta property="og:title" content="{piezas.e_(titulo)}">',
             f'<meta property="og:description" content="{piezas.e_(N["descripcion"])}">',
             f'<meta property="og:locale" content="{F["idioma"]}_{N["pais"]}">', '<meta name="twitter:card" content="summary_large_image">']
    if base_url:
        ttf_display = os.path.join(tipografia.CARPETA, par["display"][0][0])
        ttf_texto = os.path.join(tipografia.CARPETA, par["texto"][0][0])
        if hero_im is not None:
            imagenes.imagen_og(hero_im, N["nombre"], N["cocina"], ttf_display, ttf_texto, os.path.join(carpeta, "og.jpg"))
        else:   # sin foto de portada: fondo oscuro con el logotipo y el nombre
            rgb = lambda k: color.hex_rgb(tokens_paleta[k])
            imagenes.imagen_og_logo(imagenes.abrir_rgba(ruta_origen("logo")), temas.lineas_titular(N["nombre"]), N["lema"], ttf_display, ttf_texto,
                                    os.path.join(carpeta, "og.jpg"), color_fondo=rgb("tinta"), color_texto=rgb("crema"), color_acento=rgb("brasa"))
        meta.append(f'<meta property="og:image" content="{base_url.rstrip("/")}/og.jpg">')
        meta.append(f'<meta property="og:url" content="{base_url}">')
    precarga = "".join(f'<link rel="preload" href="{p["archivo"]}" as="font" type="font/woff2" crossorigin>'
                       for p in fuentes["precarga"] if p is disp or (p["rol"] == "texto" and p["peso"] == txt_min))
    icono = temas.favicon_datauri(N["nombre"][0].upper(), tokens_paleta["tinta"], tokens_paleta["brasa"], est["personalidad"])
    head = (f'<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            f'<title>{piezas.e_(titulo)}</title>{"".join(meta)}<link rel="icon" href="{icono}">{precarga}'
            f'<script>document.documentElement.className+=" js"</script><style>{css_min}</style></head>')
    body = (f'<body class="tema-{est["personalidad"]}"><a class="salto" href="#contenido">Saltar al contenido</a>'
            f'{piezas.cinta(F, C)}{P["portada"](F, C)}{P.get("tras_portada", lambda F_, C_: "")(F, C)}<main id="contenido">{main}</main>{piezas.pie(F, C)}'
            f'{piezas.barra_movil(F, C)}{P["extras"](F, C)}{piezas.panel_edu(F, C)}<script>{js_min}</script></body>')
    html = f'<!doctype html><html lang="{F["idioma"]}">{head}{body}</html>'
    with open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # ---- archivos de apoyo
    robots = "User-agent: *\nDisallow: /\n" if muestra else "User-agent: *\nAllow: /\n"
    with open(os.path.join(carpeta, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)
    cabeceras = ["/*", "  X-Content-Type-Options: nosniff", "  Referrer-Policy: strict-origin-when-cross-origin",
                 "  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()"]
    if muestra:
        cabeceras.append("  X-Robots-Tag: noindex, nofollow")
    cabeceras += ["  Content-Security-Policy: default-src 'self'; img-src 'self' data:; font-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'none'; object-src 'none'; base-uri 'self'; form-action 'none'",
                  "", "/assets/*", "  Cache-Control: public, max-age=31536000, immutable"]
    with open(os.path.join(carpeta, "_headers"), "w", encoding="utf-8") as f:
        f.write("\n".join(cabeceras) + "\n")
    with open(os.path.join(carpeta, "LICENCIAS.txt"), "w", encoding="utf-8") as f:
        f.write("Tipografías con licencia SIL Open Font License 1.1:\n\n")
        for t in fuentes["licencias"]:
            with open(os.path.join(tipografia.CARPETA, "licencias", t), encoding="utf-8") as g:
                f.write(f"--- {t} ---\n{g.read()}\n\n")

    # ---- huella, manifiesto y zip
    hu = _huella.huella(F, est_r)
    pesos = {"html": os.path.getsize(os.path.join(carpeta, "index.html")), "css_min": len(css_min.encode()), "js_min": len(js_min.encode())}
    dir_fuentes = os.path.join(carpeta, prefijo, "fonts")
    dir_img = os.path.join(carpeta, prefijo, "img")
    pesos["fuentes"] = sum(os.path.getsize(os.path.join(dir_fuentes, x)) for x in os.listdir(dir_fuentes))
    pesos["imagenes"] = sum(os.path.getsize(os.path.join(dir_img, x)) for x in os.listdir(dir_img))
    enlaces = sorted({u for u in re.findall(r'href="(https?://[^"]+|mailto:[^"]+|tel:[^"]+)"', html)})
    manifiesto = {
        "id": F["id"], "version_ficha": F["version"], "version_generador": VERSION_GENERADOR, "version_reglas": leer(os.path.join(RAIZ, "nucleo", "reglas.json"))["version"],
        "fecha": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "modo": F["modo"], "ejemplo_ficticio": ejemplo,
        "pais": N["pais"], "ciudad": N["ciudad"], "idioma": F["idioma"], "confirmacion": F["confirmacion"],
        "huella_diseno": hu, "decisiones_de_diseno": _estilo.para_manifiesto(D), "id_de_ensamblado": bid,
        "tipografias": [{"familia": par["familia_display"] if p["rol"] == "display" else par["familia_texto"], "archivo": p["archivo"],
                         "peso": p["peso"], "estilo": p["estilo"], "licencia": "OFL-1.1"} for p in fuentes["precarga"]],
        "imagenes": A.registro, "enlaces_externos": enlaces, "pesos_bytes": pesos,
        "base_url": base_url,
    }
    # el hash del paquete se calcula al final sobre todos los archivos salvo el propio manifiesto
    with open(os.path.join(carpeta, "manifiesto.json"), "w", encoding="utf-8") as f:
        json.dump(manifiesto, f, ensure_ascii=False, indent=1)
    manifiesto["paquete_sha256"] = hash_paquete(carpeta)
    with open(os.path.join(carpeta, "manifiesto.json"), "w", encoding="utf-8") as f:
        json.dump(manifiesto, f, ensure_ascii=False, indent=1)
    ruta_zip = os.path.join(salida_base, F["id"] + ".zip")
    with zipfile.ZipFile(ruta_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, dn, fn in os.walk(carpeta):
            for f in sorted(fn):
                ruta = os.path.join(dp, f)
                z.write(ruta, os.path.relpath(ruta, carpeta))
    return {"carpeta": carpeta, "zip": ruta_zip, "manifiesto": manifiesto}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Genera un sitio Edumashow desde una ficha.")
    ap.add_argument("ficha")
    ap.add_argument("--salida", default=os.path.join(os.path.dirname(RAIZ), "muestras"))
    ap.add_argument("--base-url", default=None, help="URL publica final (necesaria para la imagen de vista previa al compartir)")
    a = ap.parse_args(argv)
    try:
        r = construir(a.ficha, a.salida, a.base_url)
    except FichaIncompleta as err:
        print("EL MOTOR SE ABSTIENE:", err)
        return 2
    m = r["manifiesto"]
    kb = lambda b: f"{b / 1024:.0f} KB"
    p = m["pesos_bytes"]
    print(f"Sitio generado en {r['carpeta']}\n  zip: {r['zip']}\n  hash del paquete: {m['paquete_sha256'][:16]}...")
    print(f"  html {kb(p['html'])} | fuentes {kb(p['fuentes'])} | imágenes {kb(p['imagenes'])} (css {kb(p['css_min'])}, js {kb(p['js_min'])} dentro del html)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
