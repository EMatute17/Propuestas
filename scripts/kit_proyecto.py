"""Genera el kit del Proyecto de fichas (ChatGPT o Claude): instrucciones, archivos de conocimiento, fichas de ejemplo y esquema JSON.

Uso:
    python3 scripts/kit_proyecto.py [--salida CARPETA]

Los textos fijos están en edumashow/kit_proyecto/_fuentes (plantillas con marcadores entre llaves dobles). Lo demás sale del propio repositorio, así que el kit se
regenera cuando cambia el motor: países y monedas, paletas, parejas tipográficas, criterios de antojo, opciones del catálogo de diseño, reglas del núcleo y
el esquema JSON. Al terminar hace comprobaciones (sin comillas angulares, instrucciones de menos de 8.000 caracteres, ejemplos válidos) y escribe
kit_proyecto.zip con INSTRUCCIONES.md, LEEME.md y la carpeta conocimiento.

El kit es solo para escribir fichas: lo que se puede comprobar con código (datos, ética, fotos, accesibilidad, rendimiento, variedad) lo comprueban el
validador de fichas y el Gate, no el modelo.
"""
import argparse
import copy
import json
import os
import re
import sys
import zipfile

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, RAIZ)

from edumashow.motor import antojo, calidad, catalogo, dinero, esquema_ficha, generar, temas, tipografia  # noqa: E402
from edumashow.gate import verificar as V  # noqa: E402

FUENTES = os.path.join(RAIZ, "edumashow", "kit_proyecto", "_fuentes")
SALIDA = os.path.join(RAIZ, "edumashow", "kit_proyecto")
NOMBRES_PAIS = {"Espana": "España", "Peru": "Perú", "Mexico": "México", "Canada": "Canadá", "Panama": "Panamá"}
ARCHIVOS_CONOCIMIENTO = [
    ("01_esquema_de_la_ficha.md", "Campo por campo: qué es cada dato de la ficha, cuál es obligatorio y los valores permitidos"),
    ("02_ejemplo_ficha_urbana.json", "Ficha completa de un restaurante ficticio URBANO (parrilla de pedido para llevar)"),
    ("03_ejemplo_ficha_elegante.json", "Ficha completa de un restaurante ficticio ELEGANTE (mantel, reservas)"),
    ("04_reglas_que_aplican.md", "Las reglas del núcleo que dependen de lo que escribes, con su puesto, su evidencia y qué haces tú"),
    ("05_guia_de_redaccion.md", "Cómo se redacta cada texto: principios, ejemplos, tono y lo que nunca se escribe"),
    ("06_juicio_de_antojo.md", "Cómo juzgar cada foto con los siete criterios (solo URBANO)"),
    ("07_elegir_estilo.md", "Cómo elegir la personalidad, el perfil del restaurante y qué decide el motor"),
    ("08_hoja_de_entrada.md", "La plantilla de lo que te pega el usuario, con dos ejemplos y las reglas de las fotos"),
    ("09_checklist_y_errores.md", "Lista de comprobación antes de responder y los errores más comunes del validador"),
    ("10_ficha.schema.json", "El esquema de la ficha en JSON Schema (la forma exacta que acepta el validador)"),
]

# lo que haces tú con cada regla que depende de tu redacción (el resto lo cumple el motor y lo prueba el verificador)
ACCION = {
    "R-DAT-01": "Cada dato visible sale de la hoja de entrada; nada se hereda de un ejemplo.",
    "R-DAT-02": "Si falta un dato, omite el campo o usa la forma por confirmar; nunca pongas 0, gratis ni sin alérgenos.",
    "R-DAT-03": "Escribe cada precio como número exacto de la carta; no añadas descuentos, depósitos ni condiciones.",
    "R-DAT-04": "Cada foto lleva procedencia y permiso; las de referencia o generadas solo valen en un ejemplo ficticio.",
    "R-DAT-05": "No escribas premios, antigüedad ni cifras sin fuente y fecha; la nota de Google va solo en valoracion.",
    "R-DAT-06": "Pon la fecha de hoy en confirmacion.fecha y di en la nota de dónde salen los datos.",
    "R-DAT-08": "Si falta la carta, el horario o un contacto, pídelos: el motor no construye sin ellos.",
    "R-ETI-01": "No escribas escasez ni urgencia (últimas mesas, solo hoy, quedan N).",
    "R-ETI-02": "No escribas testimonios, estrellas ni premios inventados; en un ejemplo ficticio se rotula como ejemplo.",
    "R-ETI-03": "No prometas ventas, reservas ni porcentajes.",
    "R-ETI-05": "No escribas ruletas, premios sorpresa ni frases que asusten por lo que se pierde.",
    "R-ETI-06": "No infieras el estado de ánimo, la salud ni el perfil psicológico de nadie.",
    "R-ETI-09": "No digas que la web está probada con usuarios ni que cumple WCAG sin decir el alcance.",
    "R-ETI-10": "No menciones alérgenos ni dietas salvo que consten en la hoja, tal cual.",
    "R-ETI-11": "No menciones herramientas de IA ni modelos; la marca es Edumashow.",
    "R-ETI-12": "Usa solo comillas rectas.",
    "R-FOT-01": "Ninguna foto de Instagram ni de otra red, salvo el logo. Las demás: archivos originales del restaurante o de banco libre con autor, licencia y enlace.",
    "R-FOT-02": "Usa solo fotos que lleguen a 2400 px (portada), 1600 px (resto) y 640 px (logo); si no llegan, no las uses y pide el original como archivo.",
    "R-VAL-01": "Escribe valoracion solo con la nota real de Google de 4,0 o más, con reseñas y fecha; sin dato, sin valoracion.",
    "R-VAL-02": "Nunca copies comentarios de clientes, buenos ni malos: la nota y el número de reseñas bastan.",
    "R-SIG-01": "Elige acciones que el restaurante atiende de verdad; la primera de hero es la principal.",
    "R-SIG-03": "Da el teléfono con código de país y el WhatsApp solo con dígitos: así los contactos abren la acción directa.",
    "R-SIG-05": "Etiqueta cada botón con un verbo que diga lo que pasa al pulsarlo.",
    "R-SIG-06": "El precio va junto al nombre del plato; no lo escondas en la descripción.",
    "R-SIG-10": "No ofrezcas lo que el restaurante no atiende (reserva sin WhatsApp, reparto sin confirmar).",
    "R-SIG-11": "Titulares literales y concretos, sin vacíos de curiosidad.",
    "R-SIG-12": "Cada sección con un encabezado que dice qué hay.",
    "R-IDE-01": "Usa las palabras, los platos, la zona y el lema del propio restaurante; nada genérico.",
    "R-IDE-04": "El logo, los colores y las fotos del restaurante son fijos: no los cambies.",
    "R-IDE-07": "Si ordenas por antojo, juzga mirando cada foto con los siete criterios y escribe el motivo.",
    "R-MUE-03": "Habla de las necesidades del restaurante como pregunta o hipótesis, nunca como hecho.",
    "R-MUE-05": "No uses nombre, logo, fotos ni carta de un negocio real sin permiso: permiso pendiente.",
    "R-PER-02": "La prueba social solo con dato real y fechado (la nota de Google).",
    "R-VAR-04": "No fijes la composición del diseño: aporta el perfil y los datos, y el motor varía la web.",
}
# reglas cuyo texto del núcleo nombra lo que no debe nombrarse fuera del repositorio: en el kit se dicen sin el nombre
TEXTO_PROPIO = {"R-ETI-11": "Los entregables no mencionan herramientas de IA, nombres de modelos ni de otras agencias. Solo llevan la marca Edumashow. Esto no autoriza presentar imágenes generadas como reales."}
TEMAS_ORDEN = [("datos", "Datos y honestidad"), ("etica", "Ética y marca"), ("fotos", "Fotos"), ("valoracion", "Calificación de Google"),
               ("siguiente_paso", "Siguiente paso y redacción"), ("identidad", "Identidad"), ("persuasion", "Persuasión"), ("variedad", "Variedad"), ("muestra", "Muestras")]


# ------------------------------------------------------------------ lo que sale del repositorio
def paises():
    filas = sorted(dinero.PAISES.items(), key=lambda kv: NOMBRES_PAIS.get(kv[1][0], kv[1][0]))
    return ", ".join(f"{k} ({NOMBRES_PAIS.get(v[0], v[0])})" for k, v in filas)


def monedas():
    por_moneda = {}
    for k, v in dinero.PAISES.items():
        por_moneda.setdefault(v[1], []).append(k)
    items = [f"{m} ({', '.join(sorted(por_moneda[m]))})" if m in por_moneda else m for m in sorted(dinero.MONEDAS)]
    return "una de " + ", ".join(items) + ". Entre paréntesis, los países que la usan; en un país puede usarse otra (en Venezuela y en Ecuador se paga en USD)"


def paletas():
    return ", ".join(f'"{k}"' for k in temas.PALETAS)


def parejas():
    L = []
    for fam in catalogo.FAMILIAS:
        ps = [k for k, p in tipografia.PAREJAS.items() if fam in p["personalidades"] and tipografia.esta_probada(k, fam)]
        L.append(f"- {fam.upper()} ({len(ps)}): " + "; ".join(f'{tipografia.PAREJAS[k]["familia_display"]} con {tipografia.PAREJAS[k]["familia_texto"]}' for k in ps) + ".")
    return "\n".join(L)


def criterios():
    return "\n".join(f"- {k} (pesa {peso} de 100): {desc}." for k, (desc, peso) in antojo.CRITERIOS.items())


def opciones():
    nombres = {"portada": "Portada", "carta": "Carta", "galeria": "Galería de fotos", "ornamento": "Borde entre secciones", "boton": "Estilo de los botones",
               "densidad": "Espaciado", "textura": "Textura", "animaciones": "Paquete de animaciones"}
    L = []
    for d in catalogo.DIMENSIONES:
        L.append(f"{nombres[d]}:")
        for fam in catalogo.FAMILIAS:
            ops = [o for o in catalogo.OPCIONES[d][fam] if (d, o) not in catalogo.PENDIENTES]
            L.append(f"- {fam.upper()}: " + "; ".join(f"{o} ({catalogo.DESCRIPCIONES[(d, o)]})" for o in ops) + ".")
    return "\n".join(L)


def capacidad():
    """Cuántas composiciones distintas puede dar cada familia con el catálogo actual (sin contar tipografía ni paleta) y con ellas."""
    out = {}
    for fam in catalogo.FAMILIAS:
        n = 1
        for d in catalogo.DIMENSIONES:
            n *= len([o for o in catalogo.OPCIONES[d][fam] if (d, o) not in catalogo.PENDIENTES])
        tipos = len([k for k, p in tipografia.PAREJAS.items() if fam in p["personalidades"] and tipografia.esta_probada(k, fam)])
        out[fam] = (n, n * tipos * 12)
    return out


def regla_texto(r):
    return f'- {r["id"]} ({r["tipo"]}, evidencia {r["evidencia"]}): {TEXTO_PROPIO.get(r["id"], r["regla"])} Tú: {ACCION[r["id"]]}'


def reglas_md(n_total):
    with open(os.path.join(RAIZ, "edumashow", "nucleo", "reglas.json"), encoding="utf-8") as f:
        N = json.load(f)
    incluidas = [r for r in N["reglas"] if r["id"] in ACCION]
    L = []
    for tema, titulo in TEMAS_ORDEN:
        rs = [r for r in incluidas if r["tema"] == tema]
        if not rs:
            continue
        L.append(f"## {titulo}\n")
        L += [regla_texto(r) for r in sorted(rs, key=lambda r: r["id"])]
        L.append("")
    choques = N["resolucion_de_choques"] + "\n\nLos puestos: " + "; ".join(f"{k}, {v.lower() if k != '0' else v.lower()}" for k, v in sorted(N["prioridades"].items())) + "."
    return "\n".join(L), choques, len(N["reglas"]) - len(incluidas), N["version"]


# ------------------------------------------------------------------ ejemplos
def ejemplo_elegante():
    with open(os.path.join(RAIZ, "edumashow", "fichas", "lumbre.json"), encoding="utf-8") as f:
        F = json.load(f)
    for k in ("firma", "gate_pruebas_horario", "gate_pruebas_pedido", "excepciones_gate"):
        F.pop(k, None)
    F["version"] = "1.0.0"   # una ficha nueva siempre empieza en 1.0.0
    F["estilo"] = {"personalidad": "elegante", "paleta": "brasa"}
    F["perfil"] = {"servicio": ["mesa"], "precio": 3, "ambiente": ["romantico", "tranquilo"]}
    F["valoracion"] = {"fuente": "google", "nota": 4.7, "resenas": 128, "fecha": "2026-10-08", "ejemplo": True}
    F["procedencia_activos"] = {"origen": "referencia", "descripcion": "Foto de ejemplo para enseñar la forma de la ficha; este restaurante es inventado.",
                                "licencia": "solo para ejemplos privados de Edumashow"}
    for a in F["activos"].values():
        a["archivo"] = re.sub(r"\.webp$", ".jpg", a["archivo"])
        a.pop("procedencia", None)
    return F


def escribir(ruta, texto):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Genera el kit del Proyecto de fichas")
    ap.add_argument("--salida", default=SALIDA)
    a = ap.parse_args(argv)
    sal = a.salida
    fallos = []

    reglas_txt, choques, otras, version_reglas = reglas_md(0)
    cap = capacidad()
    rel = lambda n: f"conocimiento/{n}"
    relleno = {
        "{{VERSION}}": f"{generar.VERSION_GENERADOR}, Gate {V.VERSION_GATE}, reglas {version_reglas}",
        "{{PAISES}}": paises(), "{{MONEDAS}}": monedas(), "{{PALETAS}}": paletas(), "{{PAREJAS}}": parejas(), "{{CRITERIOS}}": criterios(),
        "{{OPCIONES}}": opciones(), "{{REGLAS}}": reglas_txt, "{{CHOQUES}}": choques, "{{OTRAS}}": str(otras),
        "{{CAPACIDAD_ELEGANTE}}": f"{cap['elegante'][0]:,}".replace(",", "."), "{{CAPACIDAD_URBANO}}": f"{cap['urbano'][0]:,}".replace(",", "."),
        "{{COMBINACIONES_ELEGANTE}}": f"{cap['elegante'][1]:,}".replace(",", "."), "{{COMBINACIONES_URBANO}}": f"{cap['urbano'][1]:,}".replace(",", "."),
        "{{UMBRAL}}": str(catalogo._huella.UMBRAL), "{{VENTANA}}": str(catalogo._huella.VENTANA),
    }

    def rellenar(t):
        for k, v in relleno.items():
            t = t.replace(k, v)
        return t

    # textos
    textos = {}
    for n in sorted(os.listdir(FUENTES)):
        if n.endswith(".md"):
            with open(os.path.join(FUENTES, n), encoding="utf-8") as f:
                textos[n] = rellenar(f.read())
    # ejemplos y esquema
    with open(os.path.join(FUENTES, "ejemplo_urbano.json"), encoding="utf-8") as f:
        urbano = json.load(f)
    elegante = ejemplo_elegante()
    for nombre, F in (("urbano", urbano), ("elegante", elegante)):
        errores, avisos = esquema_ficha.revisar(F, comprobar_fotos=False)
        if errores:
            fallos.append(f"la ficha de ejemplo {nombre} no valida: {errores[:3]}")
        try:
            import jsonschema
            jsonschema.Draft7Validator(esquema_ficha.esquema()).validate(F)
        except ImportError:
            pass
        except Exception as e:
            fallos.append(f"la ficha de ejemplo {nombre} no cumple el esquema JSON: {str(e)[:120]}")
    archivos = {
        "02_ejemplo_ficha_urbana.json": json.dumps(urbano, ensure_ascii=False, indent=1) + "\n",
        "03_ejemplo_ficha_elegante.json": json.dumps(elegante, ensure_ascii=False, indent=1) + "\n",
        "10_ficha.schema.json": json.dumps(esquema_ficha.esquema(), ensure_ascii=False, indent=1) + "\n",
    }
    for n in ("01_esquema_de_la_ficha.md", "04_reglas_que_aplican.md", "05_guia_de_redaccion.md", "06_juicio_de_antojo.md", "07_elegir_estilo.md", "08_hoja_de_entrada.md", "09_checklist_y_errores.md"):
        archivos[n] = textos[n]
    lista = "\n".join(f"- {rel(n)} ({len(archivos[n].encode()) / 1024:.0f} KB): {d}" for n, d in ARCHIVOS_CONOCIMIENTO)
    leeme = textos["LEEME.md"].replace("{{ARCHIVOS}}", lista)
    instrucciones = textos["INSTRUCCIONES.md"]

    # comprobaciones
    todo = {"INSTRUCCIONES.md": instrucciones, "LEEME.md": leeme, **{rel(n): t for n, t in archivos.items()}}
    for n, t in todo.items():
        if chr(0xAB) in t or chr(0xBB) in t:
            fallos.append(f"{n}: lleva comillas angulares")
        if re.search(r"\{\{[A-Z_]+\}\}", t):
            fallos.append(f"{n}: quedó un marcador sin rellenar: {re.search(r'{{[A-Z_]+}}', t).group(0)}")
        if re.search(r"claude|chatgpt|openai|anthropic|peetfoodie", t, re.I) and n not in ("LEEME.md",):
            fallos.append(f"{n}: nombra una herramienta o una marca que no debe salir en los textos del proyecto")
    if len(instrucciones) >= 8000:
        fallos.append(f"INSTRUCCIONES.md mide {len(instrucciones)} caracteres y el campo de instrucciones admite menos de 8.000")
    grandes = [n for n, t in archivos.items() if len(t.encode()) > 24 * 1024]
    if grandes:
        fallos.append(f"archivos de conocimiento demasiado grandes (más de 24 KB, se recuperan peor): {grandes}")
    if fallos:
        print("EL KIT NO SE ESCRIBIÓ:\n- " + "\n- ".join(fallos))
        return 1

    escribir(os.path.join(sal, "INSTRUCCIONES.md"), instrucciones)
    escribir(os.path.join(sal, "LEEME.md"), leeme)
    for n, t in archivos.items():
        escribir(os.path.join(sal, "conocimiento", n), t)
    ruta_zip = os.path.join(sal, "kit_proyecto.zip")
    with zipfile.ZipFile(ruta_zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(sal, "INSTRUCCIONES.md"), "INSTRUCCIONES.md")
        z.write(os.path.join(sal, "LEEME.md"), "LEEME.md")
        for n in sorted(archivos):
            z.write(os.path.join(sal, "conocimiento", n), f"conocimiento/{n}")
    print(f"Kit escrito en {sal}")
    print(f"  INSTRUCCIONES.md: {len(instrucciones)} caracteres (límite 8.000)")
    for n, d in ARCHIVOS_CONOCIMIENTO:
        print(f"  conocimiento/{n}: {len(archivos[n].encode()) / 1024:.1f} KB")
    print(f"  kit_proyecto.zip: {os.path.getsize(ruta_zip) / 1024:.0f} KB")
    print(f"  capacidad del catálogo (composiciones por familia): elegante {cap['elegante'][0]}, urbano {cap['urbano'][0]}; con tipografía y tono de paleta: {cap['elegante'][1]} y {cap['urbano'][1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
