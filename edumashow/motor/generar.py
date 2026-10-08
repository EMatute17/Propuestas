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

from . import dinero, huella as _huella, imagenes, piezas, temas, tipografia

VERSION_GENERADOR = "0.1.0"
RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PLANTILLAS = os.path.join(RAIZ, "motor", "plantillas")
ORIGEN_ACTIVOS = os.path.join(RAIZ, "activos", "origen")
REGISTRO_HUELLAS = os.path.join(RAIZ, "gate", "registro_huellas.json")


class FichaIncompleta(Exception):
    """El motor se abstiene: faltan datos críticos (R-DAT-08)."""


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


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
    if not F.get("contacto", {}).get("mapa_consulta"):
        falta.append("contacto.mapa_consulta")
    if not any(F.get("horario", {}).values()):
        falta.append("horario (todos los días vacíos)")
    if not F.get("carta"):
        falta.append("carta")
    for c in F.get("carta", []):
        for p in c.get("platos", []):
            if not isinstance(p.get("precio"), (int, float)) or not p.get("nombre") or not p.get("descripcion"):
                falta.append(f"carta.{c.get('id')}.{p.get('id')} (nombre, descripción o precio)")
            if p.get("foto") and p["foto"] not in F.get("activos", {}):
                falta.append(f"activos.{p['foto']}")
    conf = F.get("confirmacion", {})
    if conf.get("estado") not in ("confirmado", "ejemplo") or not conf.get("fecha"):
        falta.append("confirmación (estado y fecha)")
    if F.get("modo") == "final" and conf.get("estado") != "confirmado":
        falta.append("confirmacion.estado debe ser confirmado en el modo final")
    if F.get("modo") == "final" and not F.get("contacto", {}).get("whatsapp"):
        falta.append("contacto.whatsapp (obligatorio en el modo final)")
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


def construir(ruta_ficha, salida_base, base_url=None):
    F = leer(ruta_ficha)
    cfg = leer(os.path.join(RAIZ, "config.json"))
    validar_ficha(F)
    N = F["negocio"]
    muestra = F["modo"] == "muestra"
    ejemplo = muestra and F.get("muestra", {}).get("ejemplo_ficticio", False)
    agencia = dict(cfg["agencia"])
    agencia["vigencia"] = F.get("muestra", {}).get("vigencia", "unas semanas")
    bid = hashlib.sha1((json.dumps(F, sort_keys=True) + VERSION_GENERADOR).encode()).hexdigest()[:8]
    carpeta = os.path.join(salida_base, F["id"])
    if os.path.isdir(carpeta):
        shutil.rmtree(carpeta)
    os.makedirs(carpeta)
    prefijo = f"assets/{bid}"

    # ---- tipografía
    est = F["estilo"]
    fuentes = tipografia.preparar_pareja(est["tipografia"], os.path.join(carpeta, prefijo, "fonts"), f"{prefijo}/fonts")
    par = fuentes["pareja"]
    textos_para_glifos = json.dumps(F, ensure_ascii=False)
    faltan = tipografia.glifos_faltantes(par["texto"][0][0], textos_para_glifos)
    if faltan:
        raise FichaIncompleta("La tipografía no tiene estos caracteres: " + "".join(faltan))

    # ---- imágenes
    A = imagenes.Activos(carpeta, f"{prefijo}/img")
    procedencia = F.get("procedencia_activos", {})
    abiertas = {}

    def abrir(clave):
        if clave not in abiertas:
            abiertas[clave] = imagenes.abrir(os.path.join(ORIGEN_ACTIVOS, F["activos"][clave]["archivo"]))
        return abiertas[clave]

    def prov(clave):
        p = dict(procedencia)
        p["archivo_origen"] = F["activos"][clave]["archivo"]
        return p

    h = F["activos"]["hero"]
    hero_im = abrir("hero")
    foco = tuple(h.get("foco", (0.5, 0.5)))
    ajustes = h.get("ajustes")
    hero = {
        "foco": foco,
        "escritorio": A.procesar("hero", hero_im, [800, 1280, 1920], prov("hero"), ajustes=ajustes, jpg_ancho=1280),
        "movil": A.procesar("hero-m", hero_im, [480, 768, 960], prov("hero"), recorte={"razon": 0.8, "foco": foco}, ajustes=ajustes, jpg_ancho=768),
    }
    fotos = {}
    for c in F["carta"]:
        for p in c["platos"]:
            k = p.get("foto")
            if k and k not in fotos:
                d = A.procesar(k, abrir(k), [210, 420], prov(k), jpg_ancho=420)
                fotos[k] = {"datos": d, "color": d["color"]}
    for g in F["galeria"]:
        k = g["foto"]
        if k not in fotos:
            im = abrir(k)
            anchos = sorted({min(480, im.width), im.width})
            d = A.procesar(k, im, anchos, prov(k), jpg_ancho=im.width)
            fotos[k] = {"datos": d, "color": d["color"]}

    # ---- contexto de construcción
    wa_destino = agencia["whatsapp"] if ejemplo else F["contacto"]["whatsapp"]
    prefijo_wa = f"(Prueba de la muestra de Edumashow para {N['nombre']}) " if ejemplo else ""
    C = {"muestra": muestra, "ejemplo": ejemplo, "agencia": agencia, "hero": hero, "fotos": fotos,
         "wa_destino": wa_destino, "prefijo_wa": prefijo_wa}

    # ---- CSS y JS
    paleta = est["paleta"]
    cinta_h = "3.25rem" if muestra else "0rem"
    css = temas.tokens_css(paleta, est["forma"], est["movimiento"], par, max(len(w) for w in N["nombre"].split()), cinta_h)
    css += f"body{{--grano:{temas.grano_datauri()}}}"
    css += fuentes["css"]
    for nombre in ("base.css", f"{est['personalidad']}.css"):
        with open(os.path.join(PLANTILLAS, nombre), encoding="utf-8") as f:
            css += "\n" + f.read()
    css += (".carta,.visita,.tarjeta,.panel-edu{--foco-anillo:var(--foco-anillo-papel)}"
            ".resumen{font-weight:600;min-height:1.6em}"
            "@media (prefers-reduced-motion:reduce){.hero-fondo img{animation:none}.grano{animation:none}}")
    css_min = rcssmin.cssmin(css)

    Fjs = {
        "nombre": N["nombre"], "wa": wa_destino, "prefijo_wa": prefijo_wa, "tz": N["zona_horaria"],
        "horario": F["horario"], "moneda": F["moneda"],
        "reservas": {"paso": F["reservas"]["paso_minutos"], "ultima": F["reservas"]["ultima_antes_del_cierre_min"],
                     "antelacion": F["reservas"]["antelacion_min"], "preferida": F["reservas"]["hora_preferida"],
                     "personas": F["reservas"]["personas_por_defecto"]},
        "fuentes_carga": [f"italic 400 1em '{par['familia_display']}'", f"400 1em '{par['familia_texto']}'"],
    }
    js = "window.__F=" + json.dumps(Fjs, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";\n"
    for nombre in ("base.js", f"{est['personalidad']}.js"):
        with open(os.path.join(PLANTILLAS, nombre), encoding="utf-8") as f:
            js += f.read() + "\n"
    js += "(function(){var f=document.getElementById('form-reserva');if(f)f.hidden=false;})();\n"
    js_min = rjsmin.jsmin(js)

    # ---- HTML
    secciones = {"idea": piezas.idea, "carta": piezas.carta, "ambiente": piezas.ambiente, "reserva": piezas.reserva,
                 "visita": piezas.visita, "cierre": piezas.cierre_muestra}
    main = "".join(secciones[s](F, C) for s in est["orden"] if s in secciones)
    titulo = f"{N['nombre']} · {N['cocina']} en {N['ciudad']}" + (" · Muestra de Edumashow" if muestra else "")
    meta = [f'<meta name="description" content="{piezas.e_(N["descripcion"])}">']
    if muestra:
        meta.append('<meta name="robots" content="noindex,nofollow">')
    meta += [f'<meta name="theme-color" content="{temas.PALETAS[paleta]["meta-color"]}">', '<meta name="color-scheme" content="dark light">',
             '<meta property="og:type" content="website">', f'<meta property="og:title" content="{piezas.e_(titulo)}">',
             f'<meta property="og:description" content="{piezas.e_(N["descripcion"])}">',
             f'<meta property="og:locale" content="{F["idioma"]}_{N["pais"]}">', '<meta name="twitter:card" content="summary_large_image">']
    if base_url:
        imagenes.imagen_og(hero_im, N["nombre"], N["cocina"], os.path.join(tipografia.CARPETA, par["display"][0][0]),
                           os.path.join(tipografia.CARPETA, par["texto"][0][0]), os.path.join(carpeta, "og.jpg"))
        meta.append(f'<meta property="og:image" content="{base_url.rstrip("/")}/og.jpg">')
        meta.append(f'<meta property="og:url" content="{base_url}">')
    precarga = "".join(f'<link rel="preload" href="{p["archivo"]}" as="font" type="font/woff2" crossorigin>'
                       for p in fuentes["precarga"] if (p["rol"] == "display" and p["estilo"] == "italic") or (p["rol"] == "texto" and p["peso"] == 400))
    icono = temas.favicon_datauri(N["nombre"][0].upper(), temas.PALETAS[paleta]["tinta"], temas.PALETAS[paleta]["brasa"])
    head = (f'<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            f'<title>{piezas.e_(titulo)}</title>{"".join(meta)}<link rel="icon" href="{icono}">{precarga}'
            f'<script>document.documentElement.className+=" js"</script><style>{css_min}</style></head>')
    body = (f'<body class="tema-{est["personalidad"]}"><a class="salto" href="#contenido">Saltar al contenido</a>'
            f'{piezas.cinta(F, C)}{piezas.portada(F, C)}<main id="contenido">{main}</main>{piezas.pie(F, C)}'
            f'{piezas.barra_movil(F, C)}{piezas.vista_plato(F, C)}{piezas.panel_edu(F, C)}<script>{js_min}</script></body>')
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
    hu = _huella.huella(F)
    pesos = {"html": os.path.getsize(os.path.join(carpeta, "index.html")), "css_min": len(css_min.encode()), "js_min": len(js_min.encode())}
    dir_fuentes = os.path.join(carpeta, prefijo, "fonts")
    dir_img = os.path.join(carpeta, prefijo, "img")
    pesos["fuentes"] = sum(os.path.getsize(os.path.join(dir_fuentes, x)) for x in os.listdir(dir_fuentes))
    pesos["imagenes"] = sum(os.path.getsize(os.path.join(dir_img, x)) for x in os.listdir(dir_img))
    enlaces = sorted({u for u in re.findall(r'href="(https?://[^"]+|mailto:[^"]+)"', html)})
    manifiesto = {
        "id": F["id"], "version_ficha": F["version"], "version_generador": VERSION_GENERADOR, "version_reglas": leer(os.path.join(RAIZ, "nucleo", "reglas.json"))["version"],
        "fecha": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "modo": F["modo"], "ejemplo_ficticio": ejemplo,
        "pais": N["pais"], "ciudad": N["ciudad"], "idioma": F["idioma"], "confirmacion": F["confirmacion"],
        "huella_diseno": hu, "id_de_ensamblado": bid,
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
