"""Comprobaciones estáticas del Gate: leen el paquete generado sin abrir un navegador.

Cada función devuelve un dict {resultado, evidencia, detalle}. Los caracteres prohibidos se construyen
con chr() para que este archivo tampoco los contenga (orden permanente de Eduardo).
"""
import hashlib
import json
import os
import re
from html.parser import HTMLParser

from fontTools.ttLib import TTFont

PROHIBIDOS = (chr(0xAB), chr(0xBB))
EXT_TEXTO = (".html", ".css", ".js", ".json", ".txt", ".svg", ".xml", ".md")
MARCA_PROHIBIDA = re.compile(
    r"claude|chatgpt|gpt-?\d|openai|anthropic|peetfoodie|inteligencia artificial|generad[oa]\s+(con|por)\s+ia|modelo de lenguaje|\bIA\b",
    re.I)
PLACEHOLDERS = [r"lorem", r"ipsum", r"plato 1", r"tu texto", r"calculando", r"todo:", r"undefined", r"\bnan\b", r"\{\{", r"\}\}", r"\bxxx\b", r"por definir", r"pendiente de"]
ETICA = [
    ("escasez o urgencia", r"quedan\s+\d+|[uú]ltim[ao]s?\s+(mesas?|plazas?|unidades?)|solo\s+hoy|oferta\s+limitada|date\s+prisa|\bcorre\s|no\s+te\s+lo\s+pierdas|no\s+te\s+quedes\s+sin|cuenta\s+atr[aá]s"),
    ("testimonios, reseñas o estrellas", r"testimonio|rese[nñ]as?\s+de\s+clientes|\d[.,]\d\s*/\s*5|\b\d(?:[.,]\d)?\s*estrellas?\b|\bestrellas?\s+(?:de\s+)?(?:google|tripadvisor|yelp|rese[nñ]as?)\b|" + chr(0x2605) + "|" + chr(0x2B50)),
    ("promesa de resultados", r"\+\s*\d+\s*%|\d+\s*%\s*m[aá]s\s|aument(a|ar[aá])\s+(tus\s+)?(ventas|reservas|pedidos)|garantiz|llen(a|ar)\s+tus\s+mesas|\b(?:duplica|triplica)\s+(?:tus?|las?|los)\b"),
    ("porcentaje con falsa precisión", r"\d+[.,]\d+\s*%"),
    ("refuerzo variable", r"ruleta|rasca\s+y\s+gana|premio\s+sorpresa"),
]


def archivos_texto(carpeta):
    for dp, dn, fn in os.walk(carpeta):
        for f in sorted(fn):
            if f.lower().endswith(EXT_TEXTO):
                yield os.path.join(dp, f)


def sin_datos(txt):
    return re.sub(r"data:[a-z0-9/+.-]+[;,][^\"')\s]+", "data:", txt)


class _Texto(HTMLParser):
    """Extrae el texto visible (sin script, style ni noscript) y los metadatos de la cabecera."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.texto, self.pila, self.meta, self.title, self.datas, self.imgs, self.links, self.html_attrs = [], [], [], "", [], [], [], {}
        self._en_title = False
        self._data_actual = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.pila.append(tag)
        if tag == "html":
            self.html_attrs = a
        if tag == "meta":
            self.meta.append(a)
        if tag == "title":
            self._en_title = True
        if tag == "img":
            self.imgs.append(a)
        if tag == "a":
            self.links.append(a)
        if tag == "data":
            # eco: repite el precio real de un plato en otro lugar (la regla de medidas); calc: cifra derivada de la ficha con su cuenta
            self._data_actual = {"value": a.get("value"), "texto": "", "eco": "data-eco" in a, "calc": a.get("data-calc")}

    def handle_endtag(self, tag):
        if tag == "title":
            self._en_title = False
        if tag == "data" and self._data_actual is not None:
            self.datas.append(self._data_actual)
            self._data_actual = None
        if self.pila and self.pila[-1] == tag:
            self.pila.pop()

    def handle_data(self, d):
        if self._en_title:
            self.title += d
        if any(t in self.pila for t in ("script", "style", "noscript")):
            return
        if self._data_actual is not None:
            self._data_actual["texto"] += d
        self.texto.append(d)


def leer_html(carpeta):
    with open(os.path.join(carpeta, "index.html"), encoding="utf-8") as f:
        html = f.read()
    p = _Texto()
    p.feed(html)
    return html, p


def res(resultado, evidencia, detalle=None):
    return {"resultado": resultado, "evidencia": evidencia, "detalle": detalle or []}


# ------------------------------------------------------------------ comprobaciones
def comillas(carpeta, extra=()):
    malos = []
    rutas = list(archivos_texto(carpeta)) + [r for r in extra if os.path.exists(r)]
    for ruta in rutas:
        with open(ruta, encoding="utf-8", errors="replace") as f:
            for n, linea in enumerate(f.read().splitlines(), 1):
                if any(c in linea for c in PROHIBIDOS):
                    malos.append(f"{os.path.relpath(ruta, carpeta)}:{n}")
    return res("PASS" if not malos else "FAIL", f"{len(rutas)} archivos de texto revisados, {len(malos)} con comillas angulares", malos[:10])


def marca(carpeta):
    malos = []
    for ruta in archivos_texto(carpeta):
        with open(ruta, encoding="utf-8", errors="replace") as f:
            txt = sin_datos(f.read())
        for m in MARCA_PROHIBIDA.finditer(txt):
            malos.append(f"{os.path.relpath(ruta, carpeta)}: {m.group(0)}")
    return res("PASS" if not malos else "FAIL", f"{len(malos)} menciones a herramientas de IA o a Peetfoodie", malos[:10])


def datos(carpeta, ficha, importe, rango_horario):
    """Los datos de la página son los de la ficha, ni más ni menos: importes (con variantes y suplementos), horario,
    teléfono y WhatsApp. `importe` es la función de formato de la ficha (un monto da su texto)."""
    html, p = leer_html(carpeta)
    texto = re.sub(r"\s+", " ", " ".join(p.texto))
    fallos = []
    N, K = ficha["negocio"], ficha.get("contacto", {})
    ws = lambda t: re.sub(r"\s+", " ", t)    # los espacios duros y repetidos cuentan como uno, igual que en el texto de la pagina
    for k in ("nombre", "ciudad", "direccion"):
        if ws(N[k]) not in texto:
            fallos.append(f"falta en el texto visible: {k} = {N[k]}")
    # precios: cada importe de la carta (plato, variante o suplemento) con su texto exacto y ningún importe extra
    esperados = []
    for c in ficha["carta"]:
        for pl in c["platos"]:
            montos = ([pl["precio"]] if "precio" in pl else []) + [v["precio"] for v in pl.get("variantes", [])] + [s_["precio"] for s_ in pl.get("suplementos", [])]
            esperados += [(m, importe(m)) for m in montos]
    propios = [d for d in p.datas if not d.get("eco") and not d.get("calc")]
    obtenidos = [(d["value"], re.sub(r"\s+", " ", d["texto"]).strip()) for d in propios]
    nbsp = chr(0xA0)
    norm = lambda s_: s_.replace(nbsp, " ")
    clave_valor = lambda v: str(float(v)).rstrip("0").rstrip(".") if not str(v).isdigit() else str(v)
    esp_set = sorted((clave_valor(v), norm(t)) for v, t in esperados)
    obt_set = sorted((clave_valor(v), norm(t)) for v, t in obtenidos)
    if esp_set != obt_set:
        faltan = [x for x in esp_set if x not in obt_set]
        sobran = [x for x in obt_set if x not in esp_set]
        fallos.append(f"los importes del HTML no coinciden con la ficha: faltan {faltan[:4]} y sobran {sobran[:4]}")
    # ecos: el mismo precio real repetido en otro sitio de la pagina; cifras derivadas: el precio entre la medida, recalculado aqui
    for d in p.datas:
        if d.get("eco") and (clave_valor(d["value"]), norm(re.sub(r"\s+", " ", d["texto"]).strip())) not in esp_set:
            fallos.append(f"un precio repetido en la pagina no coincide con la carta: {d['value']} {d['texto']}")
    platos = {pl["id"]: pl for c in ficha["carta"] for pl in c["platos"]}
    derivados = []
    for d in p.datas:
        if not d.get("calc"):
            continue
        pl = platos.get(d["calc"])
        if not pl or not pl.get("medida") or not isinstance(pl.get("precio"), (int, float)):
            fallos.append(f"cifra derivada de un plato sin precio o sin medida: {d['calc']}")
            continue
        esperado = round(pl["precio"] / pl["medida"], 2)
        texto_d = norm(re.sub(r"\s+", " ", d["texto"]).strip())
        if abs(float(d["value"]) - esperado) > 0.005 or texto_d != norm(importe(esperado)):
            fallos.append(f"cifra derivada de {d['calc']}: la pagina dice {d['value']} ({texto_d}) y el calculo da {esperado}")
        derivados.append(texto_d)
    # importes sueltos en el texto que no pertenezcan a la carta (el patron sale del propio formato de la ficha)
    base = norm(importe(1))
    m = re.search(r"\d[\d.,]*", base)
    patron = re.escape(base[:m.start()]) + r"\d(?:[\d.,]*\d)?" + re.escape(base[m.end():])
    sueltos = [x for x in re.findall(patron, norm(texto)) if x not in [t for _, t in esp_set] and x not in derivados]
    if sueltos:
        fallos.append(f"importes en el texto que no estan en la carta: {sueltos[:5]}")
    # horario: por dias, o el texto que la ficha declara por confirmar (entonces la pagina no puede decir si esta abierto)
    n_horarios = 0
    if ficha.get("horario_estado") == "por_confirmar":
        if re.sub(r"\s+", " ", ficha["horario_texto"]) not in texto:
            fallos.append(f"falta el horario declarado en la ficha: {ficha['horario_texto']}")
        if "por confirmar" not in texto.lower():
            fallos.append("el horario esta por confirmar y la pagina no lo dice")
        marcado = re.sub(r"<(script|style)\b.*?</\1>", "", html, flags=re.S)   # el atributo en las etiquetas, no la palabra dentro del codigo
        if re.search(r"<[^>]*\sdata-open[\s>=]", marcado):
            fallos.append("el horario esta por confirmar y la pagina muestra un estado de abierto o cerrado")
        n_horarios = 1
    else:
        claves = [("lun", "Lunes"), ("mar", "Martes"), ("mie", "Miércoles"), ("jue", "Jueves"), ("vie", "Viernes"), ("sab", "Sábado"), ("dom", "Domingo")]
        for k, nombre in claves:
            esperado = f"{nombre} {rango_horario(ficha['horario'].get(k, []))}"
            if esperado not in texto:
                fallos.append(f"horario distinto del de la ficha: {esperado}")
        n_horarios = 7
    # marcadores de relleno y ceros engañosos
    bajo = texto.lower()
    for ph in PLACEHOLDERS:
        if re.search(ph, bajo):
            fallos.append(f"marcador de relleno: {ph}")
    for patron_cero in (r"\b0\s?(us\$|€|\$|bs)", r"\bgratis\b", r"sin al[eé]rgenos"):
        if re.search(patron_cero, bajo) and not re.search(patron_cero, json.dumps(ficha, ensure_ascii=False).lower()):
            fallos.append(f"valor engañoso sin respaldo en la ficha: {patron_cero}")
    # WhatsApp: solo el de la agencia (muestra) y el del restaurante si la ficha lo declara
    nums = set(re.findall(r"wa\.me/(\d+)", html))
    permitidos = {ficha.get("_wa_agencia")} | ({ficha["_wa_destino"]} if ficha.get("_wa_destino") else set())
    if not nums.issubset(permitidos):
        fallos.append(f"números de WhatsApp inesperados: {sorted(nums - permitidos)}")
    # teléfono: los enlaces tel: son el de la ficha y el número visible es el que la ficha declara
    tels = {l.get("href") for l in p.links if (l.get("href") or "").startswith("tel:")}
    if K.get("telefono"):
        if tels != {"tel:" + K["telefono"]}:
            fallos.append(f"enlaces tel: distintos del telefono de la ficha: {sorted(tels)}")
        if K.get("telefono_visible") and ws(K["telefono_visible"]) not in texto:
            fallos.append(f"falta el telefono visible: {K['telefono_visible']}")
    elif tels:
        fallos.append(f"enlaces tel: y la ficha no declara telefono: {sorted(tels)}")
    extra = f" (más {len([d for d in p.datas if d.get('eco')])} repetidos y {len(derivados)} cifras derivadas recalculadas)" if (derivados or any(d.get("eco") for d in p.datas)) else ""
    return res("PASS" if not fallos else "FAIL", f"{len(obtenidos)} importes{extra} y {n_horarios} {'horario' if n_horarios == 1 else 'horarios'} comparados con la ficha; {len(fallos)} discrepancias", fallos[:10])


def etica(carpeta):
    html, p = leer_html(carpeta)
    texto = re.sub(r"\s+", " ", " ".join(p.texto)).lower()
    malos = []
    for nombre, patron in ETICA:
        for m in re.finditer(patron, texto, re.I):
            malos.append(f"{nombre}: {m.group(0)}")
    # contadores y temporizadores de escasez en el código propio
    js = " ".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    if re.search(r"countdown|cuenta[_ ]?atras|setInterval\([^)]*(restan|quedan)", js, re.I):
        malos.append("temporizador de escasez en el JavaScript")
    return res("PASS" if not malos else "FAIL", f"{len(malos)} patrones de escasez, testimonios, promesas o refuerzo variable", malos[:10])


def meta(carpeta, ficha, base_url):
    html, p = leer_html(carpeta)
    m = {x.get("name") or x.get("property"): x.get("content") for x in p.meta if (x.get("name") or x.get("property"))}
    fallos, avisos = [], []
    if not p.html_attrs.get("lang"):
        fallos.append("falta lang")
    if not p.title.strip():
        fallos.append("falta title")
    d = m.get("description") or ""
    if not (50 <= len(d) <= 170):
        fallos.append(f"description fuera de 50 a 170 caracteres ({len(d)})")
    if "width=device-width" not in (m.get("viewport") or ""):
        fallos.append("viewport incorrecto")
    muestra = ficha["modo"] == "muestra"
    if muestra and "noindex" not in (m.get("robots") or ""):
        fallos.append("la muestra no lleva robots noindex")
    ruta_h = os.path.join(carpeta, "_headers")
    if muestra:
        h = open(ruta_h, encoding="utf-8").read() if os.path.exists(ruta_h) else ""
        if "X-Robots-Tag: noindex" not in h:
            fallos.append("falta la cabecera X-Robots-Tag noindex en _headers")
        r = open(os.path.join(carpeta, "robots.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(carpeta, "robots.txt")) else ""
        if "Disallow: /" not in r:
            fallos.append("robots.txt no bloquea la muestra")
    for k in ("og:title", "og:description", "og:type"):
        if not m.get(k):
            avisos.append(f"falta {k}")
    if not m.get("og:image"):
        avisos.append("sin imagen de vista previa al compartir el enlace (se genera con --base-url)")
    estado = "FAIL" if fallos else ("WARN" if avisos else "PASS")
    return res(estado, f"{len(fallos)} fallos y {len(avisos)} avisos de metadatos", fallos + avisos)


def muestra(carpeta, ficha, whatsapp_agencia):
    """R-MUE-01, R-MUE-02, R-ETI-07 y R-MUE-05: la muestra se rotula, deja pedir su retirada,
    tiene una sola acción de contratación y, si es de un negocio real, declara el permiso."""
    html, p = leer_html(carpeta)
    texto = " ".join(p.texto)
    fallos = []
    if 'class="cinta"' not in html or "Muestra de Edumashow" not in texto:
        fallos.append("falta la cinta que dice Muestra de Edumashow")
    if not any("data-retirada" in l and (l.get("href") or "").startswith(("mailto:", "https://wa.me/")) for l in p.links):
        fallos.append("falta el enlace para pedir que retiren la muestra")
    if "data-abrir-panel" not in html:
        fallos.append("falta el botón que abre el panel de contratación")
    destino = f"https://wa.me/{whatsapp_agencia}?text="
    if not any((l.get("href") or "").startswith(destino) for l in p.links):
        fallos.append("ningún enlace lleva a WhatsApp de Edumashow con mensaje prellenado")
    man = json.load(open(os.path.join(carpeta, "manifiesto.json"), encoding="utf-8"))
    real = not ficha.get("muestra", {}).get("ejemplo_ficticio", False)
    if real:
        permiso = ficha.get("muestra", {}).get("permiso")
        if permiso not in ("pendiente", "concedido"):
            fallos.append("negocio real: la ficha debe declarar muestra.permiso como pendiente o concedido")
        for im in man["imagenes"]:
            if not im.get("permiso"):
                fallos.append(f"negocio real: falta el permiso de la imagen {im['clave']}")
        if "redes" not in texto.lower() and "fotos del restaurante" not in texto.lower():
            fallos.append("negocio real: la página no dice de dónde salen las fotos y los datos")
        origen = ficha.get("muestra", {}).get("origen_datos", "")
        if not origen or re.sub(r"\s+", " ", origen) not in re.sub(r"\s+", " ", texto):
            fallos.append("negocio real: el origen de los datos que declara la ficha no aparece en la página")
    return res("PASS" if not fallos else "FAIL",
               ("negocio real con permiso declarado" if real else "ejemplo ficticio") + f"; {len(fallos)} fallos",
               fallos[:8])


def fotos(carpeta, ficha):
    html, p = leer_html(carpeta)
    man = json.load(open(os.path.join(carpeta, "manifiesto.json"), encoding="utf-8"))
    fallos = []
    for im in man["imagenes"]:
        for k in ("origen", "licencia"):
            if not im.get(k):
                fallos.append(f"{im['clave']}: falta {k} en el manifiesto")
    sin_alt = [i.get("src", "")[-30:] for i in p.imgs if "alt" not in i]
    if sin_alt:
        fallos.append(f"imágenes sin atributo alt: {sin_alt[:4]}")
    if any(i.get("origen") == "referencia" for i in man["imagenes"]):
        t = " ".join(p.texto).lower()
        if "referencia" not in t:
            fallos.append("hay fotos de referencia y la página no lo declara")
    return res("PASS" if not fallos else "FAIL", f"{len(man['imagenes'])} imágenes con origen y licencia registrados; {len(p.imgs)} etiquetas img con alt", fallos[:8])


def red_estatica(carpeta, ficha=None):
    html, p = leer_html(carpeta)
    css = html
    cargas = re.findall(r'(?:src|srcset)="(https?://[^"]+)"|url\((https?://[^)]+)\)|@import\s+["\']?(https?://[^"\')\s]+)', css)
    ext = [next(x for x in c if x) for c in cargas]
    enlaces = sorted({a.get("href") for a in p.links if a.get("href", "").startswith(("http", "mailto"))})
    permitidos = ("https://wa.me/", "https://www.google.com/maps/", "mailto:")
    redes = {r["url"] for r in (ficha or {}).get("contacto", {}).values() if isinstance(r, dict) and r.get("url")}   # solo las redes que declara la ficha
    raros = [e for e in enlaces if not e.startswith(permitidos) and e not in redes]
    fallos = [f"recurso externo en la carga: {u}" for u in ext] + [f"enlace externo no previsto: {u}" for u in raros]
    return res("PASS" if not fallos else "FAIL", f"{len(ext)} recursos externos en la carga; {len(enlaces)} enlaces de salida revisados", fallos[:8])


def fuentes_glifos(carpeta, parejas, clave):
    html, p = leer_html(carpeta)
    texto = "".join(p.texto) + p.title
    faltan = {}
    pareja = parejas[clave]
    roles = ["display", "texto"] + (["titulo"] if pareja.get("titulo") else [])
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fuentes")
    from edumashow.motor import tipografia as _tipo
    servidos = set(_tipo.unicodes_base())    # lo que viaja en el WOFF2: un caracter fuera de esto cae a la fuente del sistema aunque la fuente completa lo tenga
    for rol in roles:
        archivo = pareja[rol][0][0]
        cmap = TTFont(os.path.join(base, archivo)).getBestCmap()
        f = sorted({c for c in texto if ord(c) > 0x20 and (ord(c) not in cmap or ord(c) not in servidos)})
        if f:
            faltan[archivo] = f
    return res("PASS" if not faltan else "FAIL", f"{len(roles)} tipografías revisadas contra {len(set(texto))} caracteres distintos", [f"{a}: {''.join(f)}" for a, f in faltan.items()])


def paleta(carpeta):
    """G-PALETA: los colores finales de la página (los que lee el navegador, no los de la ficha) cumplen todos los pares de contraste
    de lectura: 4,5 a 1 en texto y 3 a 1 en anillos de foco y grandes superficies de marca."""
    from edumashow.motor import color
    html, _ = leer_html(carpeta)
    m = re.search(r":root\{([^}]*)\}", html)
    if not m:
        return res("FAIL", "no se encontraron los colores de diseño (:root) en la página")
    tokens = {}
    for par in m.group(1).split(";"):
        if par.startswith("--") and ":" in par:
            k, v = par[2:].split(":", 1)
            tokens[k.strip()] = v.strip()
    hexes = {k: v for k, v in tokens.items() if re.fullmatch(r"#[0-9a-fA-F]{6}", v)}
    filas = color.pares_de_contraste(hexes)
    fallos = [f"{f['texto']} sobre {f['fondo']}: {f['contraste']}:1 (se exige {f['minimo']}:1)" for f in filas if not f["ok"]]
    peor = min(filas, key=lambda f: f["contraste"] / f["minimo"]) if filas else None
    if not filas:
        return res("FAIL", "no se pudo medir ningún par de colores")
    return res("PASS" if not fallos else "FAIL",
               f"{len(filas)} pares de colores medidos sobre los colores finales; el más justo: {peor['texto']} sobre {peor['fondo']} {peor['contraste']}:1 (se exige {peor['minimo']}:1)", fallos[:10])


def antojo(carpeta, ficha):
    """G-ANTOJO: si la web ordena sus fotos por antojo, cada foto tiene su juicio completo (7 criterios), es real y sin marcas ajenas, y el
    orden que se ve en la portada y en la galería es el del ranking."""
    html, p = leer_html(carpeta)
    man = json.load(open(os.path.join(carpeta, "manifiesto.json"), encoding="utf-8"))
    D = (man.get("decisiones_de_diseno") or {}).get("fotos") or {}
    declaradas = [k for k, a in ficha.get("activos", {}).items() if "antojo" in a]
    if not declaradas:
        return None
    fallos = []
    reg = D.get("registros", {})
    comida = [k for k in ficha.get("activos", {}) if k != "logo" and k != "hero"]
    for k in comida:
        if k not in reg:
            fallos.append(f"la foto {k} no tiene juicio de antojo en la ficha")
    for k, r in reg.items():
        if sorted(r["juicio"]) != sorted(["textura", "reconocible", "accion", "protagonista", "luz", "calor", "mano"]) or any(v not in (0, 1, 2) for v in r["juicio"].values()):
            fallos.append(f"{k}: el juicio no tiene los 7 criterios con 0, 1 o 2")
        if r["descartada"]:
            fallos.append(f"{k} se descarta del ranking: {', '.join(r['descartada'])}")
    orden = D.get("orden_por_antojo", [])
    if ficha["estilo"].get("orden_fotos") == "antojo" and orden:
        def clave_de(src):
            return re.sub(r"-\d+\.(avif|webp|jpg|png)$", "", src.split("/")[-1])
        galeria_claves = [g["foto"] for g in ficha.get("galeria", [])]
        esperado = [k for k in orden if k in galeria_claves] + [k for k in galeria_claves if k not in orden]
        mural = re.search(r'<div class="mural">.*?<div class="tesela"[^>]*>.*?<img[^>]*src="([^"]+)"', html, re.S)
        if mural and clave_de(mural.group(1)) != esperado[0]:
            fallos.append(f"la primera foto del mural es {clave_de(mural.group(1))} y la mejor por antojo es {esperado[0]}")
        galeria = re.search(r'<div class="galeria".*', html, re.S)
        if galeria:
            vistas = [clave_de(x) for x in re.findall(r'<figure[^>]*>.*?<img[^>]*src="([^"]+)"', galeria.group(0), re.S)]
            if vistas != esperado:
                fallos.append(f"el orden de la galería es {vistas} y el del ranking es {esperado}")
    puntos = sorted(((r["puntos"], k) for k, r in reg.items()), reverse=True)
    resumen = ", ".join(f"{k} {pt}" for pt, k in puntos[:3])
    return res("PASS" if not fallos else "FAIL", f"{len(reg)} fotos juzgadas con los 7 criterios; las mejores: {resumen}", fallos[:8])


def manifiesto(carpeta, version_reglas, hash_fn):
    ruta = os.path.join(carpeta, "manifiesto.json")
    if not os.path.exists(ruta):
        return res("FAIL", "no hay manifiesto.json")
    man = json.load(open(ruta, encoding="utf-8"))
    fallos = []
    for k in ("id", "version_generador", "version_reglas", "fecha", "modo", "pais", "ciudad", "idioma", "huella_diseno", "decisiones_de_diseno", "imagenes", "tipografias", "pesos_bytes", "paquete_sha256"):
        if k not in man:
            fallos.append(f"falta {k}")
    actual = hash_fn(carpeta)
    if man.get("paquete_sha256") != actual:
        fallos.append(f"el hash del paquete no coincide: manifiesto {str(man.get('paquete_sha256'))[:12]} y actual {actual[:12]}")
    if man.get("version_reglas") != version_reglas:
        fallos.append("la versión de reglas del manifiesto no es la vigente")
    return res("PASS" if not fallos else "FAIL", f"manifiesto completo y hash {actual[:12]} verificado sobre {sum(len(fn) for _, _, fn in os.walk(carpeta))} archivos", fallos)
