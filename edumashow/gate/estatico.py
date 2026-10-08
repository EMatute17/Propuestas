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
PLACEHOLDERS = ["lorem", "ipsum", "plato 1", "tu texto", "calculando", "todo:", "undefined", "nan", "{{", "}}", "xxx", "por definir", "pendiente de"]
ETICA = [
    ("escasez o urgencia", r"quedan\s+\d+|[uú]ltim[ao]s?\s+(mesas?|plazas?|unidades?)|solo\s+hoy|oferta\s+limitada|date\s+prisa|corre\s|no\s+te\s+lo\s+pierdas|no\s+te\s+quedes\s+sin|cuenta\s+atr[aá]s"),
    ("testimonios, reseñas o estrellas", r"testimonio|rese[nñ]as?\s+de\s+clientes|\d[.,]\d\s*/\s*5|\bestrellas?\b|" + chr(0x2605) + "|" + chr(0x2B50)),
    ("promesa de resultados", r"\+\s*\d+\s*%|\d+\s*%\s*m[aá]s\s|aument(a|ar[aá])\s+(tus\s+)?(ventas|reservas|pedidos)|garantiz|llen(a|ar)\s+tus\s+mesas|duplica|triplica"),
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
            self._data_actual = {"value": a.get("value"), "texto": ""}

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


def datos(carpeta, ficha, formato_importe, rango_horario):
    html, p = leer_html(carpeta)
    texto = re.sub(r"\s+", " ", " ".join(p.texto))
    fallos = []
    N = ficha["negocio"]
    for k in ("nombre", "ciudad", "direccion"):
        if N[k] not in texto:
            fallos.append(f"falta en el texto visible: {k} = {N[k]}")
    # precios: cada plato con su importe exacto y ningún importe extra
    esperados = []
    for c in ficha["carta"]:
        for pl in c["platos"]:
            esperados.append((pl["precio"], formato_importe(pl["precio"], N["pais"], ficha["moneda"])))
    obtenidos = [(d["value"], re.sub(r"\s+", " ", d["texto"]).strip()) for d in p.datas]
    nbsp = chr(0xA0)
    norm = lambda s: s.replace(nbsp, " ")
    esp_set = sorted((str(float(v)).rstrip("0").rstrip(".") if not str(v).isdigit() else str(v), norm(t)) for v, t in esperados)
    obt_set = sorted((str(float(v)).rstrip("0").rstrip(".") if not str(v).isdigit() else str(v), norm(t)) for v, t in obtenidos)
    if esp_set != obt_set:
        fallos.append(f"los importes del HTML no coinciden con la ficha: esperados {esp_set} y obtenidos {obt_set}")
    # importes sueltos en el texto que no pertenezcan a la carta
    simbolo = norm(formato_importe(1, N["pais"], ficha["moneda"]))
    patron = re.escape(simbolo).replace("1", r"\d[\d.,]*")
    sueltos = [m for m in re.findall(patron, norm(texto)) if m not in [t for _, t in esp_set]]
    if sueltos:
        fallos.append(f"importes en el texto que no estan en la carta: {sueltos[:5]}")
    # horario
    claves = [("lun", "Lunes"), ("mar", "Martes"), ("mie", "Miércoles"), ("jue", "Jueves"), ("vie", "Viernes"), ("sab", "Sábado"), ("dom", "Domingo")]
    for k, nombre in claves:
        esperado = f"{nombre} {rango_horario(ficha['horario'].get(k, []))}"
        if esperado not in texto:
            fallos.append(f"horario distinto del de la ficha: {esperado}")
    # marcadores de relleno y ceros engañosos
    bajo = texto.lower()
    for ph in PLACEHOLDERS:
        if ph in bajo:
            fallos.append(f"marcador de relleno: {ph}")
    for patron_cero in (r"\b0\s?(us\$|€|\$|bs)", r"\bgratis\b", r"sin al[eé]rgenos"):
        if re.search(patron_cero, bajo) and not re.search(patron_cero, json.dumps(ficha, ensure_ascii=False).lower()):
            fallos.append(f"valor engañoso sin respaldo en la ficha: {patron_cero}")
    # número de WhatsApp coherente con la ficha
    nums = set(re.findall(r"wa\.me/(\d+)", html))
    permitidos = {ficha.get("_wa_destino")} if ficha.get("_wa_destino") else set()
    if permitidos and not nums.issubset(permitidos | {ficha.get("_wa_agencia")}):
        fallos.append(f"números de WhatsApp inesperados: {sorted(nums - permitidos)}")
    return res("PASS" if not fallos else "FAIL", f"{len(obtenidos)} importes y 7 horarios comparados con la ficha; {len(fallos)} discrepancias", fallos[:10])


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


def red_estatica(carpeta):
    html, p = leer_html(carpeta)
    css = html
    cargas = re.findall(r'(?:src|srcset)="(https?://[^"]+)"|url\((https?://[^)]+)\)|@import\s+["\']?(https?://[^"\')\s]+)', css)
    ext = [next(x for x in c if x) for c in cargas]
    enlaces = sorted({a.get("href") for a in p.links if a.get("href", "").startswith(("http", "mailto"))})
    permitidos = ("https://wa.me/", "https://www.google.com/maps/", "mailto:")
    raros = [e for e in enlaces if not e.startswith(permitidos)]
    fallos = [f"recurso externo en la carga: {u}" for u in ext] + [f"enlace externo no previsto: {u}" for u in raros]
    return res("PASS" if not fallos else "FAIL", f"{len(ext)} recursos externos en la carga; {len(enlaces)} enlaces de salida revisados", fallos[:8])


def fuentes_glifos(carpeta, parejas, clave):
    html, p = leer_html(carpeta)
    texto = "".join(p.texto) + p.title
    faltan = {}
    pareja = parejas[clave]
    roles = ["display", "texto"] + (["titulo"] if pareja.get("titulo") else [])
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fuentes")
    for rol in roles:
        archivo = pareja[rol][0][0]
        cmap = TTFont(os.path.join(base, archivo)).getBestCmap()
        f = sorted({c for c in texto if ord(c) > 0x20 and ord(c) not in cmap})
        if f:
            faltan[archivo] = f
    return res("PASS" if not faltan else "FAIL", f"{len(roles)} tipografías revisadas contra {len(set(texto))} caracteres distintos", [f"{a}: {''.join(f)}" for a, f in faltan.items()])


def manifiesto(carpeta, version_reglas, hash_fn):
    ruta = os.path.join(carpeta, "manifiesto.json")
    if not os.path.exists(ruta):
        return res("FAIL", "no hay manifiesto.json")
    man = json.load(open(ruta, encoding="utf-8"))
    fallos = []
    for k in ("id", "version_generador", "version_reglas", "fecha", "modo", "pais", "ciudad", "idioma", "huella_diseno", "imagenes", "tipografias", "pesos_bytes", "paquete_sha256"):
        if k not in man:
            fallos.append(f"falta {k}")
    actual = hash_fn(carpeta)
    if man.get("paquete_sha256") != actual:
        fallos.append(f"el hash del paquete no coincide: manifiesto {str(man.get('paquete_sha256'))[:12]} y actual {actual[:12]}")
    if man.get("version_reglas") != version_reglas:
        fallos.append("la versión de reglas del manifiesto no es la vigente")
    return res("PASS" if not fallos else "FAIL", f"manifiesto completo y hash {actual[:12]} verificado sobre {sum(len(fn) for _, _, fn in os.walk(carpeta))} archivos", fallos)
