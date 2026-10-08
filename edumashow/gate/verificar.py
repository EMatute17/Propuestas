"""Gate de Edumashow: verifica un sitio generado y emite un informe con veredicto.

Uso:
    python3 -m edumashow.gate.verificar edumashow/fichas/lumbre.json --sitio muestras/lumbre [--rapido]

El generador no puede aprobar su propia salida: este módulo recalcula el hash del paquete, abre la web
en un navegador real en muchos dispositivos y juzga cada regla bloqueante (R-PRO-01 y R-PRO-02).
Gravedades: bloqueo (FAIL impide entregar), defecto (FAIL impide entregar salvo excepción documentada en
la ficha, que lo convierte en WARN), asesor (solo avisa).
"""
import argparse
import datetime as _dt
import json
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from urllib.parse import unquote

from edumashow.motor import dinero, huella as _huella, pedido as _pedido, piezas, tipografia
from edumashow.motor.generar import hash_paquete
from . import estatico

VERSION_GATE = "0.3.0"
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, ".."))


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


class Informe:
    def __init__(self, excepciones):
        self.items = []
        self.excepciones = excepciones

    def add(self, id, titulo, reglas, gravedad, resultado, evidencia, detalle=None):
        item = {"id": id, "titulo": titulo, "reglas": reglas, "gravedad": gravedad, "resultado": resultado,
                "evidencia": evidencia, "detalle": list(detalle or [])}
        if resultado == "FAIL":
            if gravedad == "asesor":
                item["resultado"] = "WARN"
            elif gravedad == "defecto" and id in self.excepciones:
                item["resultado"] = "WARN"
                item["excepcion"] = self.excepciones[id]
        self.items.append(item)

    def bloqueantes(self):
        return [i for i in self.items if i["resultado"] in ("FAIL", "UNAVAILABLE") and i["gravedad"] in ("bloqueo", "defecto")]


def luminancia(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


# ------------------------------------------------------------------ jueces de los datos del navegador
def juzgar_contraste(D, dir_informe):
    filas, fallos = [], []
    for rec in D["contraste"]:
        im = np.array(Image.open(os.path.join(dir_informe, rec["imagen"])).convert("RGB"))
        dpr = rec["dpr"]
        for f in rec["filas"]:
            trozos = []
            for x, y, w, h in f["rects"]:
                x0, y0, x1, y1 = int(x * dpr), int(y * dpr), int((x + w) * dpr) + 1, int((y + h) * dpr) + 1
                r = im[max(0, y0):min(im.shape[0], y1), max(0, x0):min(im.shape[1], x1)]
                if r.size:
                    trozos.append(r.reshape(-1, 3))
            if not trozos:
                continue
            px = np.concatenate(trozos).astype(np.float64)
            lb = luminancia(px)
            tc = np.array(f["color"], dtype=np.float64)
            a = f["alfa"]
            lt = luminancia(a * tc + (1 - a) * px) if a < 0.999 else luminancia(tc)
            ratio = (np.maximum(lt, lb) + 0.05) / (np.minimum(lt, lb) + 0.05)
            grande = f["px"] >= 24 or (f["px"] >= 18.66 and f["peso"] >= 700)
            umbral = 3.0 if grande else 4.5
            p5 = float(np.percentile(ratio, 5))
            fila = {"dispositivo": rec["dispositivo"], "zona": rec["etiqueta"], "elemento": f["sel"], "texto": f["texto"], "p5": round(p5, 2), "minimo": round(float(ratio.min()), 2), "umbral": umbral, "ok": p5 >= umbral}
            filas.append(fila)
            if not fila["ok"]:
                fallos.append(f"{rec['dispositivo']} {f['sel']} \"{f['texto']}\": {p5:.2f} (mínimo {umbral})")
    return filas, fallos


def hoja_contacto(dir_informe, dispositivos, salida):
    celdas = []
    try:   # tipografia libre del repositorio: la de Pillow por defecto no tiene tildes ni la o ordinal
        fuente = ImageFont.truetype(os.path.join(RAIZ, "fuentes", "Manrope-Medium.ttf"), 13)
    except OSError:
        fuente = ImageFont.load_default()
    ancho = 250
    for d in dispositivos:
        ruta = os.path.join(dir_informe, "capturas", d["id"] + ".jpg")
        if not os.path.exists(ruta):
            continue
        im = Image.open(ruta).convert("RGB")
        escala = ancho / im.width
        alto = min(int(im.height * escala), 470)
        im = im.resize((ancho, int(im.height * escala)), Image.LANCZOS).crop((0, 0, ancho, alto))
        celdas.append((im, f"{d['nombre']}", f"{d['w']}x{d['h']} @{d['dpr']}"))
    if not celdas:
        return None
    por_fila, margen, cab = 7, 12, 40
    filas = (len(celdas) + por_fila - 1) // por_fila
    alto_fila = 470 + cab + margen
    hoja = Image.new("RGB", (por_fila * (ancho + margen) + margen, filas * alto_fila + margen), (24, 28, 34))
    dr = ImageDraw.Draw(hoja)
    for i, (im, t1, t2) in enumerate(celdas):
        x = margen + (i % por_fila) * (ancho + margen)
        y = margen + (i // por_fila) * alto_fila
        hoja.paste(im, (x, y))
        dr.text((x, y + im.height + 6), t1, fill=(240, 240, 240), font=fuente)
        dr.text((x, y + im.height + 20), t2, fill=(150, 160, 170), font=fuente)
    hoja.save(salida, quality=88)
    return salida



def juzgar_pedido(ficha, cfg, datos, muestra):
    """Recalcula en Python lo que el ticket de la página tiene que decir y lo compara con lo que se vio en el navegador."""
    if not datos:
        return "UNAVAILABLE", "la prueba del pedido no se ejecutó", []
    faltan_disp = [d for d in ("iph-390", "pc-1440") if d not in datos.get("dispositivos", {})]
    if faltan_disp:
        return "UNAVAILABLE", f"la prueba del pedido no corrió en {faltan_disp}", []
    importe = dinero.importe_fn(ficha)
    T = _pedido.textos(ficha)
    platos = {pl["id"]: pl for c in ficha["carta"] for pl in c["platos"]}
    esperadas, total_cent, n = [], 0, 0
    for l in datos["lineas"]:
        id_, _, k = l["op"].partition("~")
        pl = platos[id_]
        base = pl["variantes"][int(k)]["precio"] if k != "" else pl["precio"]
        etiqueta = pl["variantes"][int(k)]["etiqueta"] if k != "" else None
        sups = [pl["suplementos"][i] for i in l.get("suplementos", [])]
        unit = round((base + sum(x["precio"] for x in sups)) * 100)
        detalle = ", ".join(([etiqueta] if etiqueta else []) + [x["etiqueta"].lower() for x in sups]) or None
        esperadas.append({"nombre": pl["nombre"], "detalle": detalle, "qty": str(l["cantidad"]), "precio": importe(unit * l["cantidad"] / 100), "unit": unit, "cantidad": l["cantidad"]})
        total_cent += unit * l["cantidad"]
        n += l["cantidad"]
    total_txt = importe(total_cent / 100)
    destino = cfg["agencia"]["whatsapp"] if muestra else ficha["contacto"].get("whatsapp")
    prefijo = f"(Prueba de la muestra de Edumashow para {ficha['negocio']['nombre']}) " if muestra else ""
    nbsp = chr(0xA0)
    norm = lambda t: (t or "").replace(nbsp, " ")
    fl = []
    for did, R_ in datos["dispositivos"].items():
        movil = did.startswith("iph")
        if R_.get("faltaOp"): fl.append(f"{did}: la página no tiene estas opciones del menú: {R_['faltaOp']}")
        a = R_["antes"]
        if a["barraVisible"] or a["lineas"]: fl.append(f"{did}: el ticket no empieza vacío (barra {a['barraVisible']}, líneas {len(a['lineas'])})")
        t = R_["tras"]
        esp = [{"nombre": e["nombre"], "detalle": e["detalle"], "qty": e["qty"], "precio": norm(e["precio"])} for e in esperadas]
        # en el teléfono las líneas se leen en la hoja; en la computadora, en el ticket lateral
        lineas_vistas = R_["hoja"]["lineas"] if movil and R_.get("hoja") else t["lineas"]
        obt = [{"nombre": x["nombre"], "detalle": x["detalle"], "qty": x["qty"], "precio": norm(x["precio"])} for x in lineas_vistas]
        if obt != esp: fl.append(f"{did}: las líneas del ticket son {obt} y se esperaban {esp}")
        fuente_total = R_["hoja"] if movil and R_.get("hoja") else t
        if norm(fuente_total["total"]) != norm(total_txt): fl.append(f"{did}: el total del ticket es {fuente_total['total']} y la ficha da {total_txt}")
        if fuente_total["n"] != str(n) or fuente_total["unidad"] != T["productos_varios"]: fl.append(f"{did}: el contador dice {fuente_total['n']} {fuente_total['unidad']} y son {n}")
        if movil:
            if not (t["barraVisible"] and t["barraN"] == str(n) and norm(t["barraTotal"]) == norm(total_txt)): fl.append(f"{did}: la barra del pedido dice {t['barraN']} y {t['barraTotal']}, y debía decir {n} y {total_txt}")
            h = R_.get("hoja") or {}
            if not (h.get("hojaAbierta") and "cerrar" in (h.get("foco") or "")): fl.append(f"{did}: la hoja del ticket no se abre con el foco en Cerrar ({h.get('foco')})")
            c = R_.get("cerrada") or {}
            if c.get("abierta") or "pb-ver" not in (c.get("foco") or ""): fl.append(f"{did}: Escape no cierra la hoja devolviendo el foco a la barra ({c})")
        else:
            if not t["ladoVisible"] or t["barraVisible"]: fl.append(f"{did}: con el ticket a la vista no debe haber barra del pedido (lateral {t['ladoVisible']}, barra {t['barraVisible']})")
            if not (R_.get("barraLejos") or {}).get("barraVisible"): fl.append(f"{did}: con el ticket fuera de pantalla debía aparecer la barra del pedido")
        primera = esperadas[0]
        mas = R_["masUno"]
        if norm(mas["total"]) != norm(importe((total_cent + primera["unit"]) / 100)): fl.append(f"{did}: al agregar uno desde el ticket el total es {mas['total']}")
        menos = R_["menosUno"]
        if norm(menos["total"]) != norm(total_txt): fl.append(f"{did}: al quitar uno desde el ticket el total es {menos['total']} y debía volver a {total_txt}")
        sn = R_["sinNombre"]
        if sn["envios"] != 0 or not sn["visible"] or sn["aviso"] != T["falta_nombre"] or sn["foco"] != "nombre": fl.append(f"{did}: enviar sin nombre debía avisar y no abrir WhatsApp ({sn})")
        envio = R_["envio"]
        if len(envio) != 1: fl.append(f"{did}: se esperaba un solo envío a WhatsApp y hubo {len(envio)}")
        else:
            url = envio[0]["url"]
            if not url.startswith(f"https://wa.me/{destino}?text="): fl.append(f"{did}: el pedido no va al WhatsApp esperado ({url[:40]})")
            texto = unquote(url.split("?text=", 1)[1]) if "?text=" in url else ""
            saludo = T["saludo"].replace("{negocio}", ficha["negocio"]["nombre"])
            if not texto.startswith(prefijo + saludo): fl.append(f"{did}: el mensaje no empieza con {prefijo + saludo!r}")
            for e in esperadas:
                nombre_l = e["nombre"] + (", " + e["detalle"] if e["detalle"] else "")
                linea = f"\u2022 {e['cantidad']} \u00d7 {nombre_l} \u2014 {e['precio']}"
                if norm(linea) not in norm(texto): fl.append(f"{did}: al mensaje le falta la línea {linea!r}")
            if f"{T['total']}: {total_txt}" not in norm(texto): fl.append(f"{did}: al mensaje le falta el total {total_txt}")
            if f"{T['a_nombre']}: Ana P\u00e9rez" not in texto: fl.append(f"{did}: al mensaje le falta el nombre")
            if f"{T['notas']}: Sin cebolla, por favor" not in texto: fl.append(f"{did}: al mensaje le falta la nota")
            nav = R_.get("navegacion") or []
            if len(nav) != 1 or unquote(nav[0]) != unquote(url): fl.append(f"{did}: el navegador no intentó abrir el mismo enlace que anunció la página ({[x[:60] for x in nav]})")
            na = R_.get("noAbrio") or {}
            # el navegador normaliza el enlace (un apóstrofo pasa a %27): se compara lo que dicen, no cómo está escrito
            if not na.get("visible") or unquote(na.get("href") or "") != unquote(url): fl.append(f"{did}: el aviso por si no se abrió WhatsApp no lleva el mismo enlace")
        for x in R_.get("anillos", []):   # aros de foco con el pedido en marcha
            if x.get("ausente"): continue
            if not x.get("enfocado"): fl.append(f"{did}: no se pudo enfocar con teclado {x['sel']} ({x['donde']})")
            if x.get("recortado"): fl.append(f"{did}: el aro de foco de {x['sel']} ({x['donde']}) queda recortado por {x['recortado']}")
            if x.get("contraste") is not None and x["contraste"] < 3: fl.append(f"{did}: el aro de foco de {x['sel']} ({x['donde']}) tiene {x['contraste']} a 1 de contraste (mínimo 3)")
        if not movil:
            pa = R_.get("pastilla")
            if not pa: fl.append(f"{did}: falta la prueba de pulsar Ver mi pedido con el ticket fuera de pantalla")
            else:
                if pa["hojaAbierta"] or pa["modal"]: fl.append(f"{did}: Ver mi pedido abre una hoja que no se dibuja y deja la página inerte ({pa})")
                if not pa["ticketEnPantalla"]: fl.append(f"{did}: Ver mi pedido no lleva al ticket ({pa})")
                if not pa["responde"]: fl.append(f"{did}: tras Ver mi pedido la página no responde a un clic")
        v = R_["vaciado"]
        if v["lineas"] or v["barraVisible"] or v["pasosActivos"]: fl.append(f"{did}: tras vaciar quedan líneas {len(v['lineas'])}, barra {v['barraVisible']}, contadores {v['pasosActivos']}")
        if v.get("foco") == "body": fl.append(f"{did}: al vaciar el ticket el foco se perdió (quedó en el body)")
        if v["almacenamiento"] or t["almacenamiento"]: fl.append(f"{did}: el pedido dejó cookies o almacenamiento")
        if R_.get("errores"): fl.append(f"{did}: errores de consola durante el pedido: {R_['errores']}")
    ok = "PASS" if not fl else "FAIL"
    return ok, f"{len(datos['lineas'])} líneas de prueba ({n} productos, total {total_txt}) en {len(datos['dispositivos'])} dispositivos; destino {'la agencia (prueba)' if muestra else 'el restaurante'}", fl

# ------------------------------------------------------------------ verificación completa
def verificar(ruta_ficha, sitio, rapido=False, con_navegador=True, con_rendimiento=True, dir_informe=None):
    ficha = leer(ruta_ficha)
    cfg = leer(os.path.join(RAIZ, "config.json"))
    reglas = leer(os.path.join(RAIZ, "nucleo", "reglas.json"))
    excep = ficha.get("excepciones_gate", {})
    I = Informe(excep)
    dir_informe = dir_informe or os.path.join(RAIZ, "informes", ficha["id"])
    os.makedirs(dir_informe, exist_ok=True)
    muestra = ficha["modo"] == "muestra"
    ejemplo = muestra and ficha.get("muestra", {}).get("ejemplo_ficticio", False)
    ficha["_wa_agencia"] = cfg["agencia"]["whatsapp"]
    ficha["_wa_destino"] = cfg["agencia"]["whatsapp"] if ejemplo else ficha["contacto"].get("whatsapp")
    man = leer(os.path.join(sitio, "manifiesto.json"))
    base_url = man.get("base_url")

    # ---- estáticas
    r = estatico.comillas(sitio, extra=[ruta_ficha, os.path.join(RAIZ, "nucleo", "reglas.json")])
    I.add("G-COMILLAS", "Sin comillas angulares", ["R-ETI-12"], "bloqueo", r["resultado"], r["evidencia"], r["detalle"])
    r = estatico.marca(sitio)
    I.add("G-MARCA", "Sin menciones a IA ni a Peetfoodie", ["R-ETI-11"], "bloqueo", r["resultado"], r["evidencia"], r["detalle"])
    r = estatico.datos(sitio, ficha, dinero.importe_fn(ficha), piezas.rango_horario)
    I.add("G-DATOS", "Datos del HTML iguales a la ficha, sin relleno", ["R-DAT-01", "R-DAT-02", "R-DAT-03", "R-DAT-08", "R-SIG-06"], "bloqueo", r["resultado"], r["evidencia"], r["detalle"])
    r = estatico.etica(sitio)
    I.add("G-ETICA", "Sin escasez, testimonios ni promesas inventadas", ["R-ETI-01", "R-ETI-02", "R-ETI-03", "R-ETI-05", "R-SIG-11"], "bloqueo", r["resultado"], r["evidencia"], r["detalle"])
    r = estatico.meta(sitio, ficha, base_url)
    I.add("G-META", "Metadatos, noindex y vista previa al compartir", ["R-MUE-01", "R-MUE-04"], "bloqueo", r["resultado"], r["evidencia"], r["detalle"])
    if muestra:
        r = estatico.muestra(sitio, ficha, cfg["agencia"]["whatsapp"])
        I.add("G-MUESTRA", "La muestra se rotula, deja pedir su retirada y tiene una sola acción de contratación", ["R-MUE-01", "R-MUE-02", "R-ETI-07", "R-MUE-05"], "bloqueo", r["resultado"], r["evidencia"], r["detalle"])
    r = estatico.fotos(sitio, ficha)
    I.add("G-FOTOS", "Procedencia y licencia de cada imagen", ["R-DAT-04"], "bloqueo", r["resultado"], r["evidencia"], r["detalle"])
    r = estatico.manifiesto(sitio, reglas["version"], hash_paquete)
    I.add("G-MANIFIESTO", "Manifiesto completo y hash del paquete", ["R-PRO-02", "R-PRO-06"], "bloqueo", r["resultado"], r["evidencia"], r["detalle"])
    h = man["huella_diseno"]
    registro = _huella.cargar_registro(os.path.join(AQUI, "registro_huellas.json"))
    otras, cumple = _huella.comparar(ficha["id"], h, registro)
    rot = _huella.rotacion(ficha["id"], h, registro)
    previas = _huella.anteriores(ficha["id"], registro)
    ev_rot = f"titular {h['display']} ({h['clase_tipografica']}); rotación frente a las {min(len(previas), _huella.ULTIMAS_FUENTE)} webs anteriores: " + ("sin repeticiones" if not rot else "; ".join(rot))
    if not otras:
        I.add("G-HUELLA", "Unicidad de diseño y rotación de la tipografía de titular", ["R-VAR-01", "R-VAR-03"], "bloqueo", "PASS" if not rot else "FAIL",
              "no hay otras webs registradas con las que comparar (primera del registro); " + ev_rot, rot)
    else:
        I.add("G-HUELLA", "Unicidad de diseño y rotación de la tipografía de titular", ["R-VAR-01", "R-VAR-03"], "bloqueo", "PASS" if (cumple and not rot) else "FAIL",
              f"distancia mínima {min(d for _, d in otras)} de 6 (se exigen {_huella.MINIMO_DISTINTAS}); " + ev_rot, [f"{k}: {d} dimensiones distintas" for k, d in otras] + rot)
    r = estatico.paleta(sitio)
    I.add("G-PALETA", "Pares de colores de lectura con contraste suficiente (4,5 a 1; 3 a 1 en anillos de foco)", ["R-LEG-01", "R-IDE-03", "R-IDE-06"], "bloqueo", r["resultado"], r["evidencia"], r["detalle"])
    r = estatico.antojo(sitio, ficha)
    if r is not None:
        I.add("G-ANTOJO", "Fotos ordenadas por antojo: juicio completo, fotos reales y orden visible igual al del ranking", ["R-IDE-07", "R-DAT-04"], "defecto", r["resultado"], r["evidencia"], r["detalle"])
    r = estatico.fuentes_glifos(sitio, tipografia.PAREJAS, h["tipografia"])   # la pareja ya resuelta por el director (la ficha puede decir "auto")
    I.add("G-FUENTES", "Todos los caracteres existen en las tipografías", ["R-LEG-04", "R-REN-03"], "bloqueo", r["resultado"], r["evidencia"], r["detalle"])
    r = estatico.red_estatica(sitio, ficha)
    estatica_red = r

    D = None
    if con_navegador:
        cmd = ["node", "dinamico.mjs", os.path.abspath(sitio), os.path.abspath(dir_informe), os.path.abspath(ruta_ficha)] + (["rapido"] if rapido else [])
        p = subprocess.run(cmd, cwd=AQUI, capture_output=True, text=True, timeout=1800)
        if p.returncode != 0:
            I.add("G-NAVEGADOR", "Pruebas en navegador real", ["R-PRO-05"], "bloqueo", "UNAVAILABLE", "el Gate dinámico no pudo ejecutarse", (p.stderr or p.stdout)[-600:].splitlines())
        else:
            D = leer(os.path.join(dir_informe, "dinamico.json"))
    else:
        I.add("G-NAVEGADOR", "Pruebas en navegador real", ["R-PRO-05"], "bloqueo", "UNAVAILABLE", "se omitió el navegador (--sin-navegador)")

    resumen_contraste = []
    if D:
        devs = D["dispositivos"]
        repr_ = [d for d in devs if "estructura" in d]
        # ---- red y consola
        ext = sorted({u for d in devs for u in d["externas"]})
        errs = [f"{d['id']}: {e}" for d in devs for e in d["errores"]]
        cookies = [d["id"] for d in devs if d["arriba"]["cookies"] or any(d["arriba"]["storage"])]
        n404 = D["red"]["peticiones404"]
        det = estatica_red["detalle"] + [f"petición externa intentada: {u}" for u in ext] + errs[:6] + [f"cookies o almacenamiento en {c}" for c in cookies] + [f"404: {u}" for u in n404]
        ok = estatica_red["resultado"] == "PASS" and not ext and not errs and not cookies and not n404
        I.add("G-RED", "Cero terceros, cookies y errores de consola", ["R-ETI-08", "R-REN-05"], "bloqueo", "PASS" if ok else "FAIL",
              f"{len(devs)} dispositivos: {len(ext)} peticiones externas, {len(errs)} errores de consola, {len(cookies)} con cookies o almacenamiento, {len(n404)} respuestas 404", det)
        # ética dinámica
        marc = [d["id"] for d in devs if d["arriba"]["checkboxMarcados"] or d["arriba"]["dialogosAbiertos"]]
        I.add("G-ETICA-VISTA", "Sin casillas premarcadas ni ventanas bloqueantes al cargar", ["R-ETI-04"], "bloqueo", "PASS" if not marc else "FAIL", f"{len(devs)} dispositivos revisados", marc)
        # ---- estructura
        e = repr_[0]["estructura"] if repr_ else {}
        fl = []
        if e.get("lang") != "es" and ficha["idioma"] == "es":
            fl.append(f"lang = {e.get('lang')}")
        if e.get("h1") != 1: fl.append(f"h1 = {e.get('h1')}")
        if e.get("saltosEncabezado"): fl.append(f"saltos de encabezado = {e['saltosEncabezado']}")
        lm = e.get("landmarks", {})
        if not (lm.get("header") and lm.get("main") == 1 and lm.get("footer")): fl.append(f"marcas de región: {lm}")
        if e.get("imgSinAlt"): fl.append(f"imágenes sin alt = {e['imgSinAlt']}")
        if e.get("sinNombre"): fl.append(f"controles sin nombre accesible = {e['sinNombre']}")
        if not (e.get("salto") and e["salto"]["existe"]): fl.append("enlace de salto roto o ausente")
        if e.get("anclasRotas"): fl.append(f"anclas rotas {e['anclasRotas']}")
        I.add("G-ESTRUCTURA", "Idioma, un h1, encabezados en orden, regiones, alt y nombres", ["R-LEG-05", "R-SIG-12"], "bloqueo", "PASS" if not fl else "FAIL",
              f"{len(e.get('encabezados', []))} encabezados, {e.get('imgTotal')} imágenes, {e.get('landmarks', {}).get('nav')} navegaciones", fl)
        # ---- axe
        graves, leves = [], []
        for did, vs in D["axe"].items():
            for v in vs:
                (graves if v["impacto"] in ("serious", "critical") else leves).append(f"{did}: {v['id']} ({v['impacto']}) x{v['nodos']} {v['ejemplo']} {v.get('datos', '')}".rstrip())
        I.add("G-AXE", "axe-core sin violaciones graves (WCAG 2.2 AA)", ["R-LEG-05", "R-LEG-08"], "bloqueo", "FAIL" if graves else ("WARN" if leves else "PASS"),
              f"{len(D['axe'])} pruebas (tamaños y, con pedido, la hoja y el ticket armados): {len(graves)} graves y {len(leves)} leves", graves + leves)
        # ---- contraste real
        filas, fc = juzgar_contraste(D, dir_informe)
        resumen_contraste = filas
        peor = min(filas, key=lambda f: f["p5"] / f["umbral"]) if filas else None
        I.add("G-CONTRASTE", "Contraste de texto sobre el fondo real (fotos y animaciones)", ["R-LEG-01", "R-IDE-03"], "bloqueo", "PASS" if not fc and filas else ("FAIL" if fc else "UNAVAILABLE"),
              f"{len(filas)} textos medidos sobre píxeles reales; el peor: {peor['elemento']} {peor['p5']}:1 (se exige {peor['umbral']}:1)" if peor else "sin datos", fc[:10])
        # ---- táctil, desborde, texto, primera pantalla
        mov = [d for d in devs if d["tipo"] != "escritorio"]
        t24 = [f"{d['id']}: {x}" for d in mov for x in d["pagina"]["tactil24"]]
        I.add("G-TACTIL24", "Objetivos de al menos 24 por 24 px", ["R-LEG-02"], "bloqueo", "PASS" if not t24 else "FAIL", f"{len(mov)} teléfonos y tablets", t24[:8])
        t44 = [f"{d['id']}: {x}" for d in mov for x in d["pagina"]["tactil44"] if not d.get("estres")]
        I.add("G-TACTIL44", "Acciones principales de al menos 44 por 44 px en móvil", ["R-LEG-02"], "defecto", "PASS" if not t44 else "FAIL", f"{len(mov)} teléfonos y tablets", t44[:8])
        des, sol, rec = [], [], []
        for d in devs:
            p = d["pagina"]
            tag = f"{d['id']} ({d['w']}x{d['h']})" + (" estrés" if d.get("estres") else "")
            if p["desborde"] > 0 or d["arriba"]["desborde"] > 0: des.append(f"{tag}: desborde {p['desborde']} px")
            sol += [f"{tag}: {s}" for s in p["solapes"]]
            rec += [f"{tag}: {s}" for s in p["recortes"]]
        zoom = [f"zoom 200% {k}: " + "; ".join([f"desborde {v['desborde']}"] * (v["desborde"] > 0) + v["solapes"][:2] + v["recortes"][:2]) for k, v in D["zoom"].items() if v["desborde"] > 0 or v["solapes"] or v["recortes"]]
        solo_estres = lambda lst: all("estrés" in x for x in lst) if lst else True
        res_d = "PASS" if not (des or sol or rec or zoom) else ("WARN" if solo_estres(des + sol + rec) and not zoom else "FAIL")
        I.add("G-DESBORDE", "Sin desborde, solapes ni texto recortado (320 px a 3440 px y zoom 200%)", ["R-LEG-03", "R-LEG-09"], "bloqueo", res_d,
              f"{len(devs)} dispositivos y {len(D['zoom'])} pruebas de zoom", des + sol + rec + zoom)
        txt = [f"{d['id']}: {d['pagina']['textoMin']['menores14']}" for d in devs if d["pagina"]["textoMin"]["menores14"] or (d["pagina"]["cuerpoPx"] or 16) < 16]
        minimo = min(d["pagina"]["textoMin"]["px"] for d in devs)
        I.add("G-TEXTO", "Texto de 16 px en cuerpo y de 14 px como mínimo", ["R-LEG-07"], "defecto", "PASS" if not txt else "FAIL", f"texto mínimo medido: {minimo} px", txt[:6])
        pr = []
        for d in devs:
            pm = d["arriba"]["primera"]
            if not (pm["h1"] and pm["h1"]["dentro"] and pm["cta"] and pm["cta"]["dentro"]):
                pr.append(f"{d['id']} ({d['w']}x{d['h']}): h1 {pm['h1']} cta {pm['cta']}" + (" [estrés]" if d.get("estres") else ""))
        res_p = "PASS" if not pr else ("WARN" if all("[estrés]" in x for x in pr) else "FAIL")
        I.add("G-PRIMERA", "Nombre y acción principal visibles en la primera pantalla", ["R-SIG-01", "R-SIG-07", "R-MUE-02"], "bloqueo", res_p, f"{len(devs)} dispositivos, incluidos horizontales y plegables", pr)
        # ---- enlaces y barra fija
        links = repr_[0]["estructura"]["enlaces"] if repr_ else []
        K = ficha.get("contacto", {})
        redes_ok = {r["url"] for r in K.values() if isinstance(r, dict) and r.get("url")}
        tel_ok = ("tel:" + K["telefono"]) if K.get("telefono") else None
        malos = []
        if tel_ok and tel_ok not in links: malos.append("la ficha tiene teléfono y la página no tiene un enlace para llamar")
        for l in links:
            if l.startswith("#") and len(l) == 1: malos.append("enlace # sin destino")
            elif l.startswith("tel:"):
                if l != tel_ok: malos.append(f"enlace tel: distinto del teléfono de la ficha: {l}")
            elif l in redes_ok: pass
            elif l.startswith("https://wa.me/"):
                if not re.match(r"^https://wa\.me/\d{8,15}(\?text=.+)?$", l): malos.append(f"wa.me mal formado: {l[:50]}")
                elif "?text=" not in l: malos.append(f"wa.me sin mensaje prellenado: {l}")
            elif l.startswith("https://www.google.com/maps/search/?api=1&query="): pass
            elif l.startswith("mailto:") or l.startswith("#"): pass
            else: malos.append(f"enlace inesperado: {l[:60]}")
        pm_ = [d for d in devs if d["tipo"] != "escritorio" and d["w"] < 900]
        sin_barra = [d["id"] for d in pm_ if not d["pagina"]["barra"] or d["pagina"]["barra"]["enlaces"] < 3 or d["pagina"]["barra"]["visibilidad"] != "visible"]
        I.add("G-SIGUIENTE", "Contactos con acción directa y barra fija en móvil", ["R-SIG-02", "R-SIG-03", "R-SIG-08"], "bloqueo", "PASS" if not malos and not sin_barra else "FAIL",
              f"{len(links)} enlaces revisados; barra fija en {len(pm_) - len(sin_barra)} de {len(pm_)} móviles", malos[:6] + [f"barra fija no visible en {x}" for x in sin_barra])
        # ---- funcional
        Fn = D["funcional"]
        hs = Fn.get("horario", [])
        malos_h = [f"{h['caso']}: esperado \"{h['esperado']}\" y obtenido \"{h['obtenido']}\"" for h in hs if not h["ok"]]
        if ficha.get("horario_estado") == "por_confirmar":
            ap = Fn.get("apertura", {})
            fl = [f"la página dice si está abierto o cerrado ({ap.get('textoEstado')}) y el horario está por confirmar"] if ap.get("elementos") else []
            I.add("G-HORARIO", "Sin horario confirmado la página no afirma que esté abierto ni cerrado", ["R-DAT-03", "R-DAT-08"], "bloqueo", "PASS" if ap and not fl else ("FAIL" if fl else "UNAVAILABLE"),
                  "horario por confirmar: se muestra el texto de la ficha y la página no afirma que esté abierto o cerrado", fl)
        else:
            I.add("G-HORARIO", "Abierto ahora con relojes simulados, otras zonas horarias y cierre pasada la medianoche", ["R-DAT-03", "R-SIG-02"], "bloqueo", "PASS" if hs and not malos_h else "FAIL", f"{len(hs)} casos simulados", malos_h)
        if ficha.get("reservas"):
            rv = Fn.get("reserva", {})
            fl = []
            a = rv.get("antes", {})
            if a.get("personas") != str(ficha["reservas"]["personas_por_defecto"]): fl.append(f"personas por defecto = {a.get('personas')}")
            if not a.get("hora") or a.get("hora") not in a.get("horas", []): fl.append("hora por defecto fuera de las opciones")
            if rv.get("sinNombre", {}).get("envios") != 0 or not rv.get("sinNombre", {}).get("visible"): fl.append("enviar sin nombre debía avisar y no abrir WhatsApp")
            envio = (rv.get("envio") or [{}])[0]
            url = envio.get("url", "")
            if not url.startswith(f"https://wa.me/{ficha['_wa_destino']}?text="): fl.append("el mensaje no va al WhatsApp esperado")
            tx = envio.get("texto", "")
            for esperado in ("Ana Pérez", "4 personas", "20:00", "Cumpleaños, una silla para bebé", "Hola " + ficha["negocio"]["nombre"]):
                if esperado not in tx: fl.append(f"el mensaje de WhatsApp no contiene: {esperado}")
            if ejemplo and "(Prueba de la muestra de Edumashow" not in tx: fl.append("el mensaje de la muestra no se identifica como prueba")
            if not (rv.get("cerrado", {}).get("deshabilitado") and "no hay mesas" in (rv.get("cerrado", {}).get("aviso") or "")): fl.append("un día cerrado debía deshabilitar la hora y avisar")
            if min(a.get("horas", ["99:99"]), default="99:99") <= "16:00" and a.get("fecha") == "2026-10-07": fl.append("se ofrecen horas pasadas o sin antelacion")
            I.add("G-FORMULARIO", "Reserva: valores por defecto, validación, mensaje y destino de WhatsApp", ["R-SIG-03", "R-SIG-04", "R-DAT-03"], "defecto", "PASS" if not fl else "FAIL", "5 campos; se probó envío vacío, envío completo y día cerrado", fl)
        else:
            I.add("G-FORMULARIO", "Reserva: valores por defecto, validación, mensaje y destino de WhatsApp", ["R-SIG-03", "R-SIG-04", "R-DAT-03"], "defecto", "NA", "no aplica: la ficha no tiene reservas y su acción principal es llamar")
        pe, dl, ch = Fn.get("pestanas"), Fn.get("dialogo", {}), Fn.get("filtros")
        fl, partes = [], []
        if pe:   # la carta con pestañas (personalidad elegante)
            ids = [c["id"] for c in ficha["carta"]]
            n = len(ids)
            if pe.get("t0", {}).get("sel") != ["true"] + ["false"] * (n - 1) or pe.get("t0", {}).get("visibles") != 1: fl.append("estado inicial de las pestañas")
            if pe.get("t1", {}).get("sel") != ["false", "true"] + ["false"] * (n - 2) or pe.get("t1", {}).get("visibles") != [f"panel-{ids[1]}"]: fl.append("la flecha derecha no cambia de pestaña")
            if pe.get("t2", {}).get("activo") != f"tab-{ids[-1]}": fl.append("la tecla Fin no va a la última pestaña")
            partes.append("flechas y Fin en las pestañas")
        if ch:   # el menú con filtros: una categoría a la vez, o todas (personalidad urbana)
            ids, ini = ch["ids"], ch["inicial"]
            if ini["presionados"] != [ids[0]] or ini["visibles"] != [ids[0]]: fl.append(f"estado inicial de los filtros: {ini['presionados']} y a la vista {ini['visibles']}")
            for p_ in ch["pasos"]:
                esperado = ini["todas"] if p_["id"] == "todo" else [p_["id"]]
                if p_["visibles"] != esperado: fl.append(f"al pulsar {p_['id']} se ven {p_['visibles']} y se esperaba {esperado}")
                if p_["presionados"] != [p_["id"]]: fl.append(f"al pulsar {p_['id']} el filtro marcado es {p_['presionados']}")
                if p_["tarjetaTop"] is not None and p_["tarjetaTop"] < p_["barraAbajo"] - 2: fl.append(f"con {p_['id']} la primera tarjeta queda tapada por la barra de filtros")
                if not p_["tarjetas"]: fl.append(f"con {p_['id']} no se ve ninguna tarjeta")
            if ch["enter"]["presionados"] != [ids[0]]: fl.append("Enter sobre un filtro no lo activa")
            if ch["espacio"]["presionados"] != [ids[min(2, len(ids) - 1)]]: fl.append("la barra espaciadora sobre un filtro no lo activa")
            partes.append(f"{len(ids) - 1} categorías y Ver todo: clic, Enter y espacio")
        if muestra:   # el diálogo de Edumashow solo existe en la muestra
            if not (dl.get("abierto", {}).get("abierto") and dl.get("abierto", {}).get("foco") == "cerrar"): fl.append("el diálogo no se abre con el foco en Cerrar")
            if dl.get("cerrado", {}).get("abierto") or dl.get("cerrado", {}).get("foco") != "Quiero mi web": fl.append("Escape no cierra el diálogo devolviendo el foco")
            partes.append("Escape y retorno del foco en el diálogo")
        if not (pe or ch): fl.append("la carta no tiene pestañas ni filtros que probar")
        I.add("G-INTERACCION", "Navegación de la carta con teclado" + (" y diálogo de la muestra" if muestra else ""), ["R-LEG-05"], "bloqueo", "PASS" if not fl else "FAIL", "; ".join(partes), fl)
        # ---- pedido: ticket en vivo, totales, mensaje y destino
        if ficha.get("pedido"):
            I.add("G-PEDIDO", "Pedido: totales del ticket, mensaje de WhatsApp, destino y vaciado", ["R-DAT-03", "R-SIG-03", "R-SIG-04", "R-MUE-02"], "bloqueo",
                  *juzgar_pedido(ficha, cfg, Fn.get("pedido"), muestra))
        else:
            I.add("G-PEDIDO", "Pedido: totales del ticket, mensaje de WhatsApp, destino y vaciado", ["R-DAT-03", "R-SIG-03", "R-SIG-04", "R-MUE-02"], "bloqueo", "NA", "no aplica: la ficha no tiene pedido en la página")
        # ---- logotipo
        logos = [(d["id"], d["pagina"]["logo"]) for d in devs if d["pagina"].get("logo")]
        if logos:
            fl = []
            for did, lg in logos:
                if not lg["cargada"]: fl.append(f"{did}: el logotipo no cargó")
                else:
                    rp, ra = lg["ancho"] / max(lg["alto"], 1), lg["nw"] / max(lg["nh"], 1)
                    if abs(rp / ra - 1) > 0.02: fl.append(f"{did}: el logotipo se deforma (en pantalla {rp:.2f} y en el archivo {ra:.2f})")
                if lg["ancho"] < 40: fl.append(f"{did}: el logotipo mide {lg['ancho']} px de ancho (mínimo 40)")
            I.add("G-LOGO", "El logotipo carga, no se deforma y se lee a su tamaño", ["R-IDE-04"], "defecto", "PASS" if not fl else "FAIL",
                  f"{len(logos)} dispositivos; el logotipo más pequeño mide {min(lg['ancho'] for _, lg in logos)} px", fl)
        # ---- foco
        fl, av = [], []
        for did, f in D["foco"].items():
            if f["primero"] != "a.salto": fl.append(f"{did}: el primer foco no es el enlace de salto ({f['primero']})")
            if f["sinAnillo"]: fl.append(f"{did}: sin indicador de foco: {f['sinAnillo']}")
            if f["noAlcanzados"]: fl.append(f"{did}: {f['noAlcanzados']} controles inalcanzables con Tab")
            if f["fueraDePantalla"]: fl.append(f"{did}: foco fuera de pantalla en {f['fueraDePantalla']}")
            if f.get("tapadoPorBarra"): fl.append(f"{did}: foco tapado por la barra fija en {f['tapadoPorBarra']}")
            if f.get("aroNoVisible"): fl.append(f"{did}: el aro de foco no se ve en pantalla en {f['aroNoVisible']}")
            if f.get("aroRecortado"): fl.append(f"{did}: el aro de foco queda recortado por un contenedor en {f['aroRecortado']}")
            if f.get("aroPocoContraste"): fl.append(f"{did}: el aro de foco tiene menos de 3 a 1 de contraste con su fondo en {f['aroPocoContraste']}")
            if f.get("tapadoParcial"): av.append(f"{did}: la barra fija tapa en parte el elemento enfocado: {f['tapadoParcial']}")
        I.add("G-FOCO", "Teclado: orden, alcance y foco siempre visible", ["R-LEG-05"], "bloqueo", "FAIL" if fl else ("WARN" if av else "PASS"), f"{len(D['foco'])} dispositivos recorridos con Tab", fl + av)
        # ---- movimiento
        m = D["movimiento"]
        fl = []
        # WCAG 2.2.2: lo que dura mas de 5 segundos o se repite tiene que poder pausarse; una transicion de revelado de un segundo no cuenta
        if m["pausado"]["infinitas"] or m["pausado"].get("largas", 0) or m["pausado"]["brasas"]: fl.append(f"tras pausar siguen: {m['pausado']}")
        if not (m["pausaEstado"]["aria"] == "true" and m["pausaEstado"]["clase"]): fl.append("el botón de pausa no actualiza su estado")
        if m["reducido"]["infinitas"] or m["reducido"]["brasas"] or not m["reducido"]["letras"]: fl.append(f"con movimiento reducido: {m['reducido']}")
        I.add("G-MOVIMIENTO", "Movimiento reducido y pausa de las animaciones", ["R-LEG-06", "R-REN-04", "R-IDE-05"], "bloqueo", "PASS" if not fl else "FAIL",
              f"animaciones infinitas normales {m['normal']['infinitas']}; con pausa {m['pausado']['infinitas']}; con movimiento reducido {m['reducido']['infinitas']}", fl)
        # ---- efectos ligados al scroll (la cifra que se llena)
        sc = D.get("scroll", {})
        if sc:
            fl, disp = [], [k for k in sc if k not in ("reducido", "sinJs")]
            for did in disp:
                pts = {x["fr"]: x for x in sc[did]["puntos"]}
                if pts[0.95]["p"] > 0.2: fl.append(f"{did}: el efecto ya va por {pts[0.95]['p']} cuando el elemento apenas asoma por abajo")
                if pts[0.4]["p"] < 0.95: fl.append(f"{did}: el efecto no se completa mientras el elemento se ve (con el elemento al 40 por ciento de la pantalla va por {pts[0.4]['p']})")
            for clave, texto in (("reducido", "con movimiento reducido"), ("sinJs", "sin JavaScript")):
                if clave in sc and abs(sc[clave]["p"] - 1) > 0.01: fl.append(f"{texto} el efecto no queda completo (avance {sc[clave]['p']})")
            I.add("G-AVANCE", "Los efectos ligados al scroll se completan mientras se ven y la página queda completa sin ellos", ["R-IDE-05"], "defecto", "PASS" if not fl else "FAIL",
                  f"{len(disp)} dispositivos; con movimiento reducido y sin JavaScript el efecto queda completo", fl)
        # ---- sin JavaScript (visores de teléfono, correo o mensajería que no lo ejecutan)
        sj = D.get("sinjs")
        if sj:
            fl = []
            if sj["desborde"] > 0: fl.append(f"desborde horizontal de {sj['desborde']} px")
            if sj["imagenesFallan"]: fl.append(f"fotos que no se ven: {sj['imagenesFallan']}")
            if sj["ocultos"]: fl.append(f"contenido invisible hasta que corra el JavaScript: {sj['ocultos']}")
            if (sj["infinitas"] or sj["largas"]) and not sj["pausaVisible"]: fl.append(f"animaciones de más de 5 segundos sin botón de pausa ({sj['infinitas']} en bucle, {sj['largas']} largas)")
            if sj["copiarVisible"]: fl.append(f"{sj['copiarVisible']} controles de copiar visibles que sin JavaScript no hacen nada")
            if muestra:
                pn = sj.get("panel")
                if not sj.get("enlacePanel") or sj["enlacePanel"]["tag"] != "a" or sj["enlacePanel"]["href"] != "#panel-edu": fl.append("el acceso a 'Quiero mi web' no es un enlace a #panel-edu que funcione sin JavaScript")
                elif not pn or pn["display"] == "none" or not pn["dentro"] or not pn["cabe"]: fl.append(f"el panel no se abre bien por enlace sin JavaScript: {pn}")
                elif not pn["cerrar"] or pn["cerrar"]["tag"] != "a" or not sj.get("panelCerrado"): fl.append("el panel no se puede cerrar sin JavaScript")
            I.add("G-SINJS", "Sin JavaScript la página se ve completa: fotos, textos, panel y sin movimiento sin pausa", ["R-LEG-06", "R-REN-04", "R-SIG-01"], "bloqueo", "PASS" if not fl else "FAIL",
                  f"{sj['imagenes']} fotos revisadas con el JavaScript apagado en un teléfono de 390 px" + ("; el panel de la muestra abre y cierra por enlace" if muestra else ""), fl)
        # ---- resolución de imágenes
        nat = {im["clave"]: im for im in man["imagenes"]}
        amp = []
        for d in repr_:
            for im in d["pagina"]["imagenes"]:
                n = nat.get(im["clave"])
                if not n: continue
                bw, bh = im["cajaW"] * d["dpr"], im["cajaH"] * d["dpr"]
                f = max(bw / n["ancho_nativo"], bh / n["alto_nativo"]) if im["cubre"] else bw / n["ancho_nativo"]
                if f > 1.25: amp.append((round(f, 2), f"{d['id']}: {im['clave']} necesita x{round(f, 2)} su resolución original ({n['ancho_nativo']}x{n['alto_nativo']})"))
        amp.sort(reverse=True)
        I.add("G-RESOLUCION", "Resolución de las fotos suficiente para cada pantalla", ["R-REN-02"], "defecto", "PASS" if not amp else "FAIL", f"{len(amp)} fotos mostradas ampliadas más de un 25 por ciento en {len(repr_)} dispositivos", [x for _, x in amp[:8]])
        # ---- visual
        hoja = hoja_contacto(dir_informe, devs, os.path.join(dir_informe, "hoja_dispositivos.jpg"))
        I.add("G-VISUAL", "Revisión visual sobre el render real", ["R-PRO-05", "R-MED-04"], "asesor", "REVISAR", f"{len(devs)} capturas en {os.path.relpath(hoja, RAIZ) if hoja else 'sin hoja'}; falta la revisión humana (Eduardo) y las pruebas con personas")

    perf = None
    if con_rendimiento:
        sal = os.path.join(dir_informe, "rendimiento.json")
        p = subprocess.run(["node", "rendimiento.mjs", os.path.abspath(sitio), sal, "3"], cwd=AQUI, capture_output=True, text=True, timeout=1800)
        if p.returncode != 0:
            I.add("G-REND", "Presupuesto de rendimiento en móvil lento", ["R-REN-01"], "bloqueo", "UNAVAILABLE", "Lighthouse no pudo ejecutarse", (p.stderr or p.stdout)[-400:].splitlines())
        else:
            perf = leer(sal)
            B = cfg["gate"]["presupuesto"]
            mv, es = perf["perfiles"]["movil"], perf["perfiles"]["escritorio"]
            fl = []
            if mv["puntuaciones"]["performance"] < B["lighthouse_rendimiento"]: fl.append(f"rendimiento móvil {mv['puntuaciones']['performance']} (se exigen {B['lighthouse_rendimiento']})")
            if mv["lcp_ms"] > B["lcp_ms"]: fl.append(f"LCP móvil {mv['lcp_ms']} ms (máximo {B['lcp_ms']})")
            if mv["cls"] > B["cls"]: fl.append(f"CLS móvil {mv['cls']} (máximo {B['cls']})")
            if mv["tbt_ms"] > B["tbt_ms"]: fl.append(f"TBT móvil {mv['tbt_ms']} ms (máximo {B['tbt_ms']})")
            if es["puntuaciones"]["performance"] < B["lighthouse_rendimiento"]: fl.append(f"rendimiento escritorio {es['puntuaciones']['performance']}")
            if D:
                pm = D["peso"].get("iph-390")
                if pm:
                    if pm["inicial"] / 1024 > B["inicial_kb"]: fl.append(f"peso inicial en móvil {pm['inicial'] // 1024} KB (máximo {B['inicial_kb']})")
                    if pm["total"] / 1024 > B["total_kb"]: fl.append(f"peso total en móvil {pm['total'] // 1024} KB (máximo {B['total_kb']})")
            I.add("G-REND", "Presupuesto de rendimiento en móvil lento simulado", ["R-REN-01", "R-REN-02", "R-REN-03", "R-REN-04"], "bloqueo", "PASS" if not fl else "FAIL",
                  f"Lighthouse móvil {mv['puntuaciones']['performance']}, LCP {mv['lcp_ms']} ms, CLS {mv['cls']}, TBT {mv['tbt_ms']} ms; escritorio {es['puntuaciones']['performance']}", fl)

    # ---- veredicto
    bl = I.bloqueantes()
    veredicto = "APTO" if not bl else "NO APTO"
    informe = {
        "gate": VERSION_GATE, "reglas": reglas["version"], "fecha": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "id": ficha["id"], "nombre": ficha["negocio"]["nombre"], "modo": ficha["modo"], "paquete_sha256": man["paquete_sha256"],
        "veredicto_tecnico": veredicto, "bloqueantes": [b["id"] for b in bl],
        "estados": {"tecnico": veredicto, "revision_visual": "pendiente: capturas generadas, falta la revisión de una persona", "aprobacion_de_eduardo": "pendiente", "entrega": "pendiente"},
        "decisiones_de_diseno": man.get("decisiones_de_diseno"),
        "resultados": I.items, "dispositivos": D["dispositivos"] if D else [], "contraste": resumen_contraste, "rendimiento": perf, "peso": D["peso"] if D else None,
        "no_verifica": [
            "Safari y Firefox reales: solo se probó Chromium con los tamaños, la densidad y el tacto de cada dispositivo emulados.",
            "Pruebas con personas reales (comprensión, confianza, facilidad): el Gate mide reglas, no personas.",
            "Que el restaurante conteste los mensajes de WhatsApp ni que los datos de la ficha sean ciertos.",
            "Rendimiento en el hosting real: se midió en un servidor local con compresión, sin CDN ni latencia de red real.",
            "Aspectos legales (RGPD, LSSI, alérgenos, permisos de uso de nombre y fotos): validar con asesoría legal.",
        ],
    }
    with open(os.path.join(dir_informe, "informe.json"), "w", encoding="utf-8") as f:
        json.dump(informe, f, ensure_ascii=False, indent=1)
    escribir_md(informe, ficha, os.path.join(dir_informe, "informe.md"))
    if veredicto == "APTO" and D and not rapido:
        _huella.registrar(ficha["id"], h, os.path.join(AQUI, "registro_huellas.json"))
    return informe


def escribir_md(inf, ficha, ruta):
    L = []
    L.append(f"# Informe del Gate: {inf['nombre']} ({inf['id']})\n")
    L.append(f"- **Veredicto técnico: {inf['veredicto_tecnico']}**" + (f" (bloquean: {', '.join(inf['bloqueantes'])})" if inf["bloqueantes"] else ""))
    L.append(f"- Fecha: {inf['fecha']} | Gate {inf['gate']} | Reglas {inf['reglas']}")
    L.append(f"- Paquete (SHA-256): `{inf['paquete_sha256']}`")
    L.append("- Estados: técnico = " + inf["estados"]["tecnico"] + "; revisión visual = " + inf["estados"]["revision_visual"] + "; aprobación de Eduardo = pendiente; entrega = pendiente\n")
    L.append("## Resultado por comprobación\n")
    L.append("| ID | Resultado | Gravedad | Reglas | Evidencia |\n|---|---|---|---|---|")
    for r in inf["resultados"]:
        ev = r["evidencia"].replace("|", "/")
        L.append(f"| {r['id']} | **{r['resultado']}** | {r['gravedad']} | {', '.join(r['reglas'])} | {ev} |")
    avisos = [r for r in inf["resultados"] if r["resultado"] in ("WARN", "FAIL", "REVISAR", "UNAVAILABLE")]
    if avisos:
        L.append("\n## Detalle de avisos, fallos y excepciones\n")
        for r in avisos:
            L.append(f"### {r['id']}: {r['titulo']} ({r['resultado']})")
            if r.get("excepcion"):
                L.append(f"- Excepción documentada en la ficha: {r['excepcion']}")
            for d in r["detalle"][:12]:
                L.append(f"- {d}")
            L.append("")
    dd = inf.get("decisiones_de_diseno")
    if dd:
        L += lineas_decisiones(dd)
    L.append("## Dispositivos probados\n")
    L.append("| Dispositivo | Tamaño | Desborde | h1 y botón principal en la primera pantalla | Solapes | Recortes |\n|---|---|---|---|---|---|")
    for d in inf["dispositivos"]:
        p = d["arriba"]["primera"]
        ok = "sí" if (p["h1"] and p["h1"]["dentro"] and p["cta"] and p["cta"]["dentro"]) else "NO"
        L.append(f"| {d['nombre']}{' (estrés)' if d.get('estres') else ''} | {d['w']}x{d['h']} @{d['dpr']} | {d['pagina']['desborde']} px | {ok} | {len(d['pagina']['solapes'])} | {len(d['pagina']['recortes'])} |")
    if inf.get("rendimiento"):
        L.append("\n## Rendimiento (Lighthouse, mediana de 3 pasadas, servidor local con brotli)\n")
        L.append("| Perfil | Rendimiento | Accesibilidad | Buenas prácticas | LCP | CLS | TBT | Peso |\n|---|---|---|---|---|---|---|---|")
        for k, v in inf["rendimiento"]["perfiles"].items():
            pu = v["puntuaciones"]
            L.append(f"| {NOMBRE_PERFIL.get(k, k)} | {pu['performance']} | {pu['accessibility']} | {pu['best-practices']} | {v['lcp_ms']} ms | {v['cls']} | {v['tbt_ms']} ms | {v['peso_KB']} KB |")
    if inf.get("peso"):
        L.append("\nPeso realmente descargado (con compresión): " + "; ".join(f"{k}: inicial {v['inicial'] // 1024} KB, total tras recorrer la página {v['total'] // 1024} KB" for k, v in inf["peso"].items()))
    if inf["contraste"]:
        L.append("\n## Contraste medido sobre píxeles reales (peores 8)\n")
        L.append("| Elemento | Dispositivo | Contraste (5.º percentil) | Se exige | |\n|---|---|---|---|---|")
        for f in sorted(inf["contraste"], key=lambda f: f["p5"] / f["umbral"])[:8]:
            L.append(f"| {f['elemento']} \"{f['texto']}\" | {f['dispositivo']} | {f['p5']}:1 | {f['umbral']}:1 | {'ok' if f['ok'] else 'FALLA'} |")
    L.append("\n## Lo que este Gate no verifica\n")
    L += [f"- {x}" for x in inf["no_verifica"]]
    open(ruta, "w", encoding="utf-8").write("\n".join(L) + "\n")


NOMBRE_PERFIL = {"movil": "móvil", "escritorio": "escritorio"}


def lineas_decisiones(dd):
    """Sección del informe con lo que decidió el director de estilo y por qué."""
    L = [f"## Decisiones de diseño (director de estilo {dd['version_director']})\n"]
    pa, ti, fo = dd["paleta"], dd["tipografia"], dd["fotos"]
    L.append(f"**Paleta: {pa['id']}.** {pa['origen']}.\n")
    rep = pa.get("informe")
    if rep:
        L.append(f"- Color de identidad sacado del logo: {rep['color_de_marca']}. Proporción: {rep['proporcion']}.")
        ac = rep.get("acento")
        if ac:
            L.append(f"- Acento de temporada ({ac['temporada']}, {ac['fuente']}): {ac['elegido']}, afinado hacia la marca a {ac['afinado']}. "
                     "Alternativas: " + "; ".join(f"{a['nombre']} (relación de tono {a['relacion']}, unidad {a['unidad']}, puntos {a['puntos']})" for a in ac["alternativas"]) + ".")
        L.append(f"- Fondos: claro desde {rep['fondos']['claro_desde']}; oscuro desde {rep['fondos']['oscuro_desde']}.")
        L.append("- Colores dominantes del logo: " + ", ".join(f"{d['hex']} ({round(d['peso'] * 100)} %{', neutro' if d['neutro'] else ''})" for d in rep["dominantes_del_logo"]) + ".")
    L.append("\n| Rol | Color |\n|---|---|")
    for k in ("tinta", "tinta-2", "tinta-3", "crema", "papel", "papel-2", "brasa", "brasa-2", "brasa-papel", "acento", "acento-papel"):
        if k in pa["tokens"]:
            L.append(f"| {k} | `{pa['tokens'][k]}` |")
    pares = pa["pares"]
    peor = min(pares, key=lambda f: f["contraste"] / f["minimo"])
    L.append(f"\n{len(pares)} pares de contraste medidos al generar; el más justo: {peor['texto']} sobre {peor['fondo']} {peor['contraste']}:1 (se exigen {peor['minimo']}:1).\n")
    el = ti["elegida"]
    L.append(f"**Tipografía del titular: {el['display']} ({el['clase']}), pareja {ti['clave']}.** {ti['origen']}. Tonos del restaurante: {', '.join(dd['tonos']['lista'])} ({dd['tonos']['origen']}).\n")
    L.append("| Pareja | Clase | Tonos que encajan | Puntos | Probada en el Gate | Rotación | Caracteres que faltan |\n|---|---|---|---|---|---|---|")
    for f in ti["ranking"]:
        L.append(f"| {f['clave']} | {f['clase']} | {', '.join(f['tonos_que_encajan']) or '-'} | {f['puntos']} | {'sí' if f['probada'] else 'no'} | {'; '.join(f['rotacion']) or 'sin repetición'} | {f['faltan_caracteres'] or '-'} |")
    if fo["registros"]:
        L.append(f"\n**Fotos por antojo** (juicio visual {int(fo['pesos']['juicio'] * 100)} % y medidas técnicas {int(fo['pesos']['tecnica'] * 100)} %; se usa el orden: {'sí' if fo['usa_el_orden'] else 'no'}).\n")
        L.append("| Foto | Puntos | Juicio visual | Técnica | Nota |\n|---|---|---|---|---|")
        for k in fo["orden_por_antojo"]:
            r = fo["registros"][k]
            L.append(f"| {k} | {r['puntos']} | {r['visual']} | {r['tecnica']} | {r['nota']} |")
    if dd.get("idea"):
        i = dd["idea"]
        L.append(f"\n**Idea dibujada: {i['pieza']}** ({i['categoria']}, en {i['unidad']}; medidas {i['medidas']}). Datos: {i['datos']}.")
    L.append("")
    return L


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gate de Edumashow")
    ap.add_argument("ficha")
    ap.add_argument("--sitio", required=True)
    ap.add_argument("--rapido", action="store_true", help="solo los dispositivos representativos")
    ap.add_argument("--sin-navegador", action="store_true")
    ap.add_argument("--sin-rendimiento", action="store_true")
    a = ap.parse_args(argv)
    inf = verificar(a.ficha, a.sitio, a.rapido, not a.sin_navegador, not a.sin_rendimiento)
    for r in inf["resultados"]:
        print(f"{r['resultado']:12s} {r['id']:16s} {r['evidencia'][:110]}")
    print("VEREDICTO TÉCNICO:", inf["veredicto_tecnico"], "| bloquean:", inf["bloqueantes"] or "ninguna")
    return 0 if inf["veredicto_tecnico"] == "APTO" else 1


if __name__ == "__main__":
    sys.exit(main())
