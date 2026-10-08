"""Archivo de los cinco estudios: genera MAPA_REGLAS.md y comprueba que el archivo está completo.

Uso: python3 edumashow/nucleo/estudios/archivo_fuente.py

Hace dos cosas:
  1. Lee ../reglas.json y escribe MAPA_REGLAS.md: para cada regla unificada, qué estudios la apoyan
     (con los ids y páginas de la primera extracción, que siguen valiendo porque las páginas son las del PDF).
  2. Valida el archivo: están los cinco textos completos y los cinco análisis, las marcas de página van de 1
     a N sin saltos, no hay comillas angulares ni el nombre del creador original, los ids H-XX-NN de cada
     análisis no se repiten y los enlaces relativos existen.
Sale con código 1 si algo falla. Los caracteres prohibidos se construyen con chr() para que este archivo
tampoco los contenga.
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
NUCLEO = os.path.normpath(os.path.join(AQUI, ".."))
PROHIBIDOS = (chr(0xAB), chr(0xBB))
CREADOR = re.compile("Peet" + "foodie", re.I)

ESTUDIOS = {
    "AL": ("AL_alianzas_creadores.md", 55, "Motor predictivo para propuestas y alianzas con creadores"),
    "PS": ("PS_psicologia_humana.md", 9, "Psicología humana histórica y actual"),
    "UX": ("UX_motor_predictivo_ux.md", 40, "Motor predictivo de UX para propuestas"),
    "CO": ("CO_ciencias_comportamiento.md", 11, "Ciencias del comportamiento y de la conducta"),
    "GR": ("GR_motor_grafico.md", 33, "Motor gráfico para propuestas comerciales"),
}


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()


def mapa_de_reglas():
    datos = json.loads(leer(os.path.join(NUCLEO, "reglas.json")))
    filas = []
    for r in datos["reglas"]:
        por_estudio = {k: [] for k in ESTUDIOS}
        otras = []
        for f in r["fuentes"]:
            m = re.match(r"^(AL|PS|UX|CO|GR)\b[- ]?(.*)$", f)
            if m:
                por_estudio[m.group(1)].append(f)
            else:
                otras.append(f)
        prio = "-" if r["prioridad"] is None else str(r["prioridad"])
        celdas = ["; ".join(por_estudio[k]) or "" for k in ESTUDIOS]
        filas.append("| " + " | ".join([r["id"], r["tema"], prio, r["tipo"], r["evidencia"]] + celdas + ["; ".join(otras)]) + " |")
    cab = ["Regla", "Tema", "Prio.", "Tipo", "Evid."] + list(ESTUDIOS) + ["Otras fuentes (norma, medida, orden)"]
    texto = [
        "# Mapa de las reglas unificadas a los cinco estudios",
        "",
        "Lo genera `archivo_fuente.py` a partir de `../reglas.json`; no se edita a mano. Sirve para saber qué estudio leer cuando una regla "
        "necesita su fuente. Los ids (AL-01, UX-33, CO-07 y similares) son los de la primera extracción de los estudios, que no se conservó; "
        "las páginas son las del PDF y siguen siendo válidas contra los textos completos de `texto/` y las lecturas de `analisis/`.",
        "",
        "Prioridad: 0 verdad, legalidad y ética; 1 accesibilidad y legibilidad; 2 tarea del visitante; 3 rendimiento; 4 identidad; "
        "5 persuasión (hipótesis); 6 variedad; guion = regla de proceso. Evidencia: N norma, M medida del proyecto, E1 a E4 según el estudio de origen.",
        "",
        f"Reglas: {len(datos['reglas'])}. Versión del núcleo: {datos['version']}.",
        "",
        "| " + " | ".join(cab) + " |",
        "|" + "---|" * len(cab),
    ] + filas
    return "\n".join(texto) + "\n"


def validar():
    errores = []
    base = os.path.join(AQUI)
    for clave, (nombre, paginas, _) in ESTUDIOS.items():
        ruta_t = os.path.join(base, "texto", nombre)
        ruta_a = os.path.join(base, "analisis", nombre)
        for ruta in (ruta_t, ruta_a):
            if not os.path.exists(ruta):
                errores.append(f"falta {os.path.relpath(ruta, NUCLEO)}")
        if not (os.path.exists(ruta_t) and os.path.exists(ruta_a)):
            continue
        t = leer(ruta_t)
        a = leer(ruta_a)
        marcas = [int(n) for n in re.findall(r"\*\*\[p\.(\d+)\]\*\*", t)]
        if marcas != list(range(1, paginas + 1)):
            errores.append(f"{nombre}: las marcas de página no van de 1 a {paginas} sin saltos ({len(marcas)} marcas)")
        for nombre_f, contenido in ((f"texto/{nombre}", t), (f"analisis/{nombre}", a)):
            for ch in PROHIBIDOS:
                if ch in contenido:
                    errores.append(f"{nombre_f}: comilla angular")
            if CREADOR.search(contenido):
                errores.append(f"{nombre_f}: nombre del creador original")
        ids = re.findall(r"^\| (H-" + clave + r"-\d{2}) \|", a, re.M)
        if len(ids) != len(set(ids)):
            errores.append(f"{nombre}: ids H-{clave}-NN repetidos")
        if not ids:
            errores.append(f"{nombre}: el análisis no tiene hallazgos con id H-{clave}-NN")
        for enlace in re.findall(r"`\.\./([a-z]+/[A-Za-z_]+\.md)`", a):
            if not os.path.exists(os.path.join(base, enlace)):
                errores.append(f"{nombre}: enlace roto a {enlace}")
    for nombre in ("LEEME.md", "SINTESIS.md"):
        if not os.path.exists(os.path.join(base, nombre)):
            errores.append(f"falta {nombre}")
    return errores


def main():
    errores = validar()
    destino = os.path.join(AQUI, "MAPA_REGLAS.md")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(mapa_de_reglas())
    if errores:
        print("\n".join(errores))
        sys.exit(1)
    print("archivo de estudios correcto: 5 textos completos, 5 análisis, mapa de reglas escrito en MAPA_REGLAS.md")


if __name__ == "__main__":
    main()
