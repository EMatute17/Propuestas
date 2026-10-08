"""Construye y verifica muchas webs de una vez, a partir de una carpeta de fichas.

Uso:
    python3 scripts/lote.py CARPETA [--salida SALIDA] [--nivel estatico|rapido|completo] [--paralelo N] [--max N] [--solo id1,id2] [--rehacer]

La carpeta del lote tiene una subcarpeta por restaurante:

    CARPETA/<id>/ficha.json     la ficha (la que escribe el Proyecto de ChatGPT o de Claude)
    CARPETA/<id>/fotos/         las fotos y el logo con los nombres que usa la ficha (se copian a edumashow/activos/origen/<id>/)

Niveles del Gate:
    estatico   comprobaciones del paquete sin navegador (comillas, marca, datos, ética, paleta, fuentes, fotos): segundos por web.
    rapido     lo anterior más pruebas en navegador real en 4 dispositivos representativos, sin Lighthouse: de 3 a 5 minutos por web.
    completo   27 dispositivos, texto al 200 por ciento y Lighthouse (el Gate de las webs que se entregan): de 7 a 14 minutos por web.

Para cada restaurante hace, en este orden: completa las pruebas que no escribe el redactor, revisa la ficha (esquema y reglas), construye la web y
pasa el Gate del nivel pedido. Si la ficha tiene errores no construye y lo anota. Al terminar deja:

    SALIDA/<id>/               la web lista para subir
    SALIDA/<id>.zip            el paquete
    SALIDA/_informes/<id>/     el informe del Gate (informe.md)
    SALIDA/_resumen.md y .csv  una fila por restaurante: veredicto, qué bloquea, estilo elegido y tiempo

El nivel rapido y el estatico NO registran la huella de diseño de la web (solo la registra un Gate completo con veredicto apto), así que no comprueban la
variedad entre las webs del lote. Esa comprobación y la rotación tipográfica hay que decidirlas aparte cuando el lote es grande.
"""
import argparse
import concurrent.futures
import csv
import json
import os
import shutil
import sys
import time
import traceback

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, RAIZ)

from edumashow.motor import esquema_ficha, generar  # noqa: E402
from edumashow.gate import verificar as V  # noqa: E402

COLUMNAS = ["id", "nombre", "estado", "veredicto", "bloquean", "personalidad", "tipografia", "paleta", "avisos", "segundos", "informe", "paquete"]


def _copiar_fotos(origen, destino):
    os.makedirs(destino, exist_ok=True)
    for n in sorted(os.listdir(origen)):
        s = os.path.join(origen, n)
        if os.path.isfile(s):
            d = os.path.join(destino, n)
            if not os.path.exists(d) or os.path.getmtime(s) > os.path.getmtime(d):
                shutil.copy2(s, d)


def procesar(carpeta, id_, salida, nivel, fotos_de_prueba=False):
    """Una web de principio a fin. Devuelve la fila del resumen; nunca lanza (un fallo de una web no para el lote)."""
    t0 = time.time()
    fila = {c: "" for c in COLUMNAS}
    fila["id"] = id_
    try:
        ruta = os.path.join(carpeta, id_, "ficha.json")
        with open(ruta, encoding="utf-8") as f:
            F = json.load(f)
        fila["nombre"] = (F.get("negocio") or {}).get("nombre", "")
        fotos = os.path.join(carpeta, id_, "fotos")
        if os.path.isdir(fotos):
            _copiar_fotos(fotos, os.path.join(generar.ORIGEN_ACTIVOS, F.get("id", id_)))
        if esquema_ficha.completar(F):
            with open(ruta, "w", encoding="utf-8") as g:
                json.dump(F, g, ensure_ascii=False, indent=1)
                g.write("\n")
        errores, avisos = esquema_ficha.revisar(F, ruta, fotos_de_prueba=fotos_de_prueba)
        fila["avisos"] = " | ".join(avisos)
        if errores:
            fila["estado"], fila["veredicto"] = "FICHA CON ERRORES", "NO SE CONSTRUYO"
            fila["bloquean"] = " ; ".join(errores)
            return fila
        r = generar.construir(ruta, salida)
        man = r["manifiesto"]
        d = (man.get("decisiones_de_diseno") or {})
        fila["personalidad"] = (F.get("estilo") or {}).get("personalidad", "")
        fila["tipografia"] = (d.get("tipografia") or {}).get("clave", "")
        fila["paleta"] = (d.get("paleta") or {}).get("id", "")
        fila["paquete"] = os.path.relpath(r["zip"], salida)
        informe_dir = os.path.join(salida, "_informes", F["id"])
        completo = nivel == "completo"
        # fuera del nivel completo la variedad entre webs pasa a aviso: no se puede juzgar web a web en un lote (ver el resumen)
        inf = V.verificar(ruta, r["carpeta"], rapido=not completo, con_navegador=nivel != "estatico", con_rendimiento=completo, dir_informe=informe_dir,
                          variedad_bloquea=completo, fotos_de_prueba=fotos_de_prueba)
        bloquean = [b for b in inf["bloqueantes"] if not (nivel == "estatico" and b == "G-NAVEGADOR")]
        if nivel == "estatico":
            fila["veredicto"] = "ESTATICO OK" if not bloquean else "ESTATICO NO"
        else:
            fila["veredicto"] = inf["veredicto_tecnico"]   # APTO, NO APTO o SOLO PRUEBA (las fotos no cumplen la regla de calidad: no es entregable)
        fila["estado"] = "VERIFICADA" if not bloquean else "NO PASA EL GATE"
        if inf.get("solo_prueba"):
            fila["estado"] = "SOLO PRUEBA (NO ENTREGABLE)"
        fila["bloquean"] = ", ".join(bloquean)
        fila["informe"] = os.path.relpath(os.path.join(informe_dir, "informe.md"), salida)
    except generar.FichaIncompleta as e:
        fila["estado"], fila["veredicto"], fila["bloquean"] = "EL MOTOR SE ABSTIENE", "NO SE CONSTRUYO", str(e)
    except Exception as e:   # un fallo inesperado de una web no debe parar las demás
        fila["estado"], fila["veredicto"] = "FALLO INESPERADO", "NO SE VERIFICO"
        fila["bloquean"] = f"{type(e).__name__}: {e}"
        fila["avisos"] = traceback.format_exc().splitlines()[-3:][0][:200]
    finally:
        fila["segundos"] = round(time.time() - t0)
    return fila


def escribir_resumen(salida, filas, nivel):
    ordenadas = sorted(filas, key=lambda f: f["id"])
    with open(os.path.join(salida, "_resumen.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(ordenadas)
    ok = [f for f in ordenadas if f["veredicto"] in ("APTO", "ESTATICO OK")]
    prueba = [f for f in ordenadas if f["veredicto"] == "SOLO PRUEBA"]
    L = [f"# Resumen del lote (nivel {nivel})", "", f"- Restaurantes: {len(ordenadas)}", f"- Pasan: {len(ok)}",
         f"- No pasan o no se construyeron: {len(ordenadas) - len(ok) - len(prueba)}", f"- Solo prueba (las fotos no cumplen la regla de calidad; no se pueden entregar): {len(prueba)}", f"- Tiempo total de trabajo: {sum(int(f['segundos'] or 0) for f in ordenadas) // 60} min (suma de todos)", "",
         "| Restaurante | Estado | Veredicto | Qué bloquea | Estilo | Tiempo |", "|---|---|---|---|---|---|"]
    for f in ordenadas:
        estilo = " / ".join(x for x in (f["personalidad"], f["tipografia"]) if x)
        L.append(f"| {f['nombre'] or f['id']} ({f['id']}) | {f['estado']} | {f['veredicto']} | {(f['bloquean'] or '')[:160]} | {estilo} | {f['segundos']} s |")
    # la variedad del lote entera, a la vista: cuántas webs hay de cada estilo
    from collections import Counter
    L += ["", "## Variedad del lote", "",
          "Personalidad: " + ", ".join(f"{k} {v}" for k, v in Counter(f["personalidad"] for f in ordenadas if f["personalidad"]).most_common()),
          "", "Tipografía de titular: " + ", ".join(f"{k} {v}" for k, v in Counter(f["tipografia"] for f in ordenadas if f["tipografia"]).most_common()), ""]
    L += ["Una web con veredicto apto ha pasado el nivel del Gate indicado. Falta siempre la revisión visual de una persona y, en un negocio real, el permiso del dueño."]
    with open(os.path.join(salida, "_resumen.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Construye y verifica un lote de webs")
    ap.add_argument("carpeta")
    ap.add_argument("--salida", default=os.path.join(os.path.dirname(RAIZ), "muestras"))
    ap.add_argument("--nivel", choices=["estatico", "rapido", "completo"], default="rapido")
    ap.add_argument("--paralelo", type=int, default=2, help="webs a la vez (cada una abre su navegador; con 4 núcleos, 2 o 3)")
    ap.add_argument("--max", type=int, default=0, help="procesar como máximo N restaurantes")
    ap.add_argument("--solo", default="", help="ids separados por coma")
    ap.add_argument("--rehacer", action="store_true", help="volver a hacer los que ya tienen informe")
    ap.add_argument("--fotos-de-prueba", action="store_true", help="solo para probar el sistema: la calidad de las fotos no bloquea y el resultado queda como SOLO PRUEBA, no entregable")
    a = ap.parse_args(argv)
    ids = sorted(d for d in os.listdir(a.carpeta) if os.path.isfile(os.path.join(a.carpeta, d, "ficha.json")))
    if a.solo:
        pedidos = {x.strip() for x in a.solo.split(",") if x.strip()}
        ids = [i for i in ids if i in pedidos]
    if not a.rehacer:
        hechos = {i for i in ids if os.path.exists(os.path.join(a.salida, "_informes", i, "informe.json"))
                  and os.path.getmtime(os.path.join(a.salida, "_informes", i, "informe.json")) > os.path.getmtime(os.path.join(a.carpeta, i, "ficha.json"))}
        if hechos:
            print(f"Ya hechos y sin cambios en su ficha ({len(hechos)}): se omiten. Usa --rehacer para repetirlos.")
        ids = [i for i in ids if i not in hechos]
    if a.max:
        ids = ids[:a.max]
    if not ids:
        print("Nada que procesar.")
        return 0
    os.makedirs(a.salida, exist_ok=True)
    print(f"{len(ids)} restaurantes, nivel {a.nivel}, {a.paralelo} a la vez. Salida: {a.salida}")
    filas = []
    # las filas que ya estaban en el resumen anterior se conservan, para que el resumen sea del lote entero
    anterior = os.path.join(a.salida, "_resumen.csv")
    if os.path.exists(anterior):
        with open(anterior, encoding="utf-8", newline="") as f:
            filas = [r for r in csv.DictReader(f) if r["id"] not in ids]
    t0 = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=max(1, a.paralelo)) as ex:
        futuros = {ex.submit(procesar, a.carpeta, i, a.salida, a.nivel, a.fotos_de_prueba): i for i in ids}
        for k, fu in enumerate(concurrent.futures.as_completed(futuros), 1):
            fila = fu.result()
            filas.append(fila)
            print(f"[{k}/{len(ids)}] {fila['id']}: {fila['estado']} {fila['veredicto']} ({fila['segundos']} s)" + (f"  -> {fila['bloquean'][:120]}" if fila["bloquean"] else ""), flush=True)
            escribir_resumen(a.salida, filas, a.nivel)
    print(f"Listo en {round((time.time() - t0) / 60, 1)} min. Resumen: {os.path.join(a.salida, '_resumen.md')}")
    return 0 if all(f["veredicto"] in ("APTO", "ESTATICO OK") for f in filas) else 1


if __name__ == "__main__":
    sys.exit(main())
