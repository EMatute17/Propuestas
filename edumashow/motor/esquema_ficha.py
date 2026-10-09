"""Esquema de la ficha y revisión previa a construir.

La ficha es lo único que el motor lee. Este módulo hace dos cosas que sirven antes de gastar tiempo en construir una web:
1. Un esquema JSON (jsonschema, borrador 7) con la forma de la ficha: tipos, valores permitidos y campos obligatorios.
2. `revisar`, que junta el esquema, las reglas del propio motor (`generar.validar_ficha`) y otras comprobaciones (zona horaria, horario,
   frases que el Gate rechazaría, juicios de antojo completos...) y devuelve dos listas en español: errores (la ficha no se puede construir
   o el Gate la rechazaría) y avisos (conviene mirarlos).

El mismo esquema se entrega a quien escribe fichas (kit del proyecto), para que el modelo vea la forma exacta.
"""
import json
import os
import re

from . import calidad, catalogo, dinero, tipografia, valoracion

# monedas en las que los precios normales pasan de cinco mil (para no avisar de un precio raro sin motivo)
MONEDAS_GRANDES = {"COP", "CLP", "PYG", "ARS", "CRC", "VES", "UYU"}
HORA = {"type": "string", "pattern": r"^([01]\d|2[0-3]):[0-5]\d$"}
TRAMO = {"type": "array", "minItems": 2, "maxItems": 2, "items": HORA}
DIA = {"type": "array", "items": TRAMO}
PRECIO = {"type": "number", "exclusiveMinimum": 0}
TEXTO = {"type": "string", "minLength": 1}
FECHA = {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"}
ID_PLATO = {"type": "string", "pattern": r"^[A-Za-z0-9_-]+$"}
ID_CORTO = {"type": "string", "pattern": r"^[a-z0-9_]+$"}
RED = {"type": "object", "required": ["usuario", "url"], "additionalProperties": False,
       "properties": {"usuario": TEXTO, "url": {"type": "string", "pattern": r"^https://"}}}
JUICIO = {"type": "object", "additionalProperties": False, "required": ["textura", "reconocible", "accion", "protagonista", "luz", "calor", "mano"],
          "properties": {k: {"type": "integer", "enum": [0, 1, 2]} for k in ("textura", "reconocible", "accion", "protagonista", "luz", "calor", "mano")}}
ANTOJO = {"type": "object", "required": ["juicio", "real", "sin_marcas_ajenas"], "additionalProperties": False,
          "properties": {"juicio": JUICIO, "real": {"type": "boolean"}, "sin_marcas_ajenas": {"type": "boolean"}, "nota": {"type": "string"}}}
PROCEDENCIA = {"type": "object", "properties": {"origen": {"type": "string", "enum": ["propia_del_restaurante", "redes_del_restaurante", "banco_libre", "referencia", "generada"]},
                                                 "descripcion": TEXTO, "licencia": TEXTO, "permiso": {"type": "string", "enum": ["pendiente", "concedido"]},
                                                 "autor": {"type": "string"}, "url": {"type": "string"}, "recorte": {"type": "string"}}}


def esquema():
    """El esquema de la ficha como un diccionario (JSON Schema, borrador 7)."""
    cats = {
        "type": "object", "required": ["id", "titulo", "platos"], "additionalProperties": False,
        "properties": {
            "id": ID_CORTO, "titulo": TEXTO, "chip": TEXTO, "nota": TEXTO, "foto": ID_CORTO, "presentacion": {"type": "string", "enum": ["lista"]},
            "platos": {"type": "array", "minItems": 1, "items": {
                "type": "object", "required": ["id", "nombre"], "additionalProperties": False,
                "properties": {
                    "id": ID_PLATO, "nombre": TEXTO, "nombre_en": TEXTO, "lang": {"type": "string", "enum": ["en", "it", "fr", "pt", "es", "de"]}, "descripcion": TEXTO,
                    "precio": PRECIO, "foto": ID_CORTO, "medida": {"type": "number", "exclusiveMinimum": 0}, "firma": {"type": "boolean"},   # firma: marca antigua, el motor la ignora
                    "variantes": {"type": "array", "minItems": 2, "items": {"type": "object", "required": ["etiqueta", "precio"], "additionalProperties": False,
                                                                           "properties": {"etiqueta": TEXTO, "precio": PRECIO}}},
                    "suplementos": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["etiqueta", "precio"], "additionalProperties": False,
                                                                             "properties": {"etiqueta": TEXTO, "precio": PRECIO}}},
                },
            }},
        },
    }
    accion = {"type": "object", "required": ["tipo"], "additionalProperties": False,
              "properties": {"tipo": {"type": "string", "enum": ["reservar", "carta", "mapa", "llamar", "whatsapp", "instagram"]}, "etiqueta": TEXTO}}
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Ficha de restaurante de Edumashow",
        "type": "object",
        "required": ["id", "version", "modo", "idioma", "confirmacion", "negocio", "contacto", "moneda", "carta", "textos", "activos", "estilo", "muestra"],
        "additionalProperties": False,
        "properties": {
            "id": ID_CORTO,
            "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
            "modo": {"type": "string", "enum": ["muestra", "final"]},
            "idioma": {"type": "string", "enum": ["es"]},
            "confirmacion": {"type": "object", "required": ["estado", "fecha"], "additionalProperties": False,
                             "properties": {"estado": {"type": "string", "enum": ["ejemplo", "por_confirmar", "confirmado"]}, "fecha": FECHA, "nota": {"type": "string"}}},
            "negocio": {"type": "object", "additionalProperties": False,
                        "required": ["nombre", "cocina", "ciudad", "pais", "direccion", "zona_horaria", "lema", "descripcion"],
                        "properties": {"nombre": TEXTO, "cocina": TEXTO, "ciudad": TEXTO, "pais": {"type": "string", "enum": sorted(dinero.PAISES)}, "direccion": TEXTO,
                                       "zona_horaria": {"type": "string", "pattern": r"^[A-Za-z_]+(/[A-Za-z_\-]+){1,2}$"}, "lema": TEXTO, "lema_en": TEXTO, "descripcion": TEXTO}},
            "contacto": {"type": "object", "required": ["mapa_consulta"], "additionalProperties": False,
                         "properties": {"mapa_consulta": TEXTO, "telefono": {"type": ["string", "null"], "pattern": r"^\+\d{8,15}$"}, "telefono_visible": {"type": ["string", "null"]},
                                        "whatsapp": {"type": ["string", "null"], "pattern": r"^\d{8,15}$"}, "instagram": RED, "tiktok": RED,
                                        "reparto": {"type": "array", "items": {"type": "object", "required": ["nombre"], "additionalProperties": False, "properties": {"nombre": TEXTO}}}}},
            "conducta": {"type": "object", "additionalProperties": False,
                         "properties": {"objetivo": {"type": "string", "enum": ["reservar", "llamar", "pedir"]}, "canal": {"type": "string", "enum": ["whatsapp", "telefono"]}}},
            "acciones": {"type": "object", "additionalProperties": False,
                         "properties": {"hero": {"type": "array", "minItems": 1, "maxItems": 2, "items": accion}, "barra": {"type": "array", "minItems": 1, "maxItems": 3, "items": accion}}},
            "moneda": {"type": "string", "enum": sorted(dinero.MONEDAS)},
            "carta_sin_precios": {"type": "boolean"},   # el restaurante no publica precios: ningun plato lleva precio y la pagina lo dice (textos.carta_nota)
            "horario_estado": {"type": "string", "enum": ["por_confirmar"]},
            "horario_texto": TEXTO,
            "horario": {"type": "object", "additionalProperties": False, "required": ["lun", "mar", "mie", "jue", "vie", "sab", "dom"],
                        "properties": {d: DIA for d in ("lun", "mar", "mie", "jue", "vie", "sab", "dom")}},
            "reservas": {"type": "object", "additionalProperties": False,
                         "required": ["maximo_personas", "personas_por_defecto", "paso_minutos", "ultima_antes_del_cierre_min", "antelacion_min", "hora_preferida"],
                         "properties": {"maximo_personas": {"type": "integer", "minimum": 2}, "personas_por_defecto": {"type": "integer", "minimum": 1},
                                        "paso_minutos": {"type": "integer", "enum": [15, 30, 60]}, "ultima_antes_del_cierre_min": {"type": "integer", "minimum": 0},
                                        "antelacion_min": {"type": "integer", "minimum": 0}, "hora_preferida": HORA}},
            "historia": {"type": "object", "required": ["cifra", "unidad", "texto", "pasos"], "additionalProperties": False,
                         "properties": {"cifra": {"type": "number"}, "unidad": TEXTO, "texto": TEXTO,
                                        "pasos": {"type": "array", "minItems": 2, "maxItems": 4, "items": {"type": "object", "required": ["titulo", "texto"], "additionalProperties": False,
                                                                                                          "properties": {"titulo": TEXTO, "texto": TEXTO}}}}},
            "valoracion": {"type": "object", "required": ["fuente", "nota", "resenas", "fecha"], "additionalProperties": False,
                           "properties": {"fuente": {"type": "string", "enum": ["google"]}, "nota": {"type": "number", "minimum": 1, "maximum": 5},
                                          "resenas": {"type": "integer", "minimum": 1}, "fecha": FECHA, "url": {"type": "string", "pattern": r"^https://"}, "ejemplo": {"type": "boolean"}}},
            "carta": {"type": "array", "minItems": 1, "items": cats},
            "galeria": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["foto", "pie"], "additionalProperties": False, "properties": {"foto": ID_CORTO, "pie": TEXTO}}},
            "textos": {"type": "object", "additionalProperties": {"type": "string", "minLength": 1}},
            "activos": {"type": "object", "minProperties": 1, "additionalProperties": {
                "type": "object", "required": ["archivo", "alt"], "additionalProperties": False,
                "properties": {"archivo": {"type": "string", "pattern": r"^[A-Za-z0-9_\-]+/[A-Za-z0-9_\-\.]+\.(jpg|jpeg|png|webp|avif)$"}, "alt": {"type": "string"}, "procedencia": PROCEDENCIA,
                               "antojo": ANTOJO, "foco": {"type": "array", "minItems": 2, "maxItems": 2, "items": {"type": "number", "minimum": 0, "maximum": 1}},
                               "ajustes": {"type": "object"}}}},
            "procedencia_activos": PROCEDENCIA,
            "estilo": {"type": "object", "additionalProperties": False, "required": ["personalidad"],
                       "properties": dict(
                           {"personalidad": {"type": "string", "enum": ["elegante", "urbano"]}, "paleta": {"type": "string", "enum": ["auto", "brasa", "fuego"]},
                            "tipografia": {"type": "string", "enum": ["auto"] + sorted(tipografia.PAREJAS)},
                            "forma": {"type": "string", "enum": ["auto", "recta", "suave"]}, "movimiento": {"type": "string", "enum": ["auto", "lento", "rapido"]},
                            "orden": {"type": "array", "minItems": 3, "items": {"type": "string", "enum": ["portada", "idea", "carta", "ambiente", "reserva", "visita", "cierre", "regla", "como", "fotos"]}},
                            "orden_fotos": {"type": "string", "enum": ["antojo", "ficha"]}, "variante_paleta": {"type": "integer"}, "acento_temporada": {"type": "boolean"},
                            "matiz": {"type": "integer", "minimum": 0, "maximum": 359},
                            "tono": {"type": "array", "items": TEXTO}},
                           **{d: {"type": "string", "enum": ["auto"] + sorted({o for f in catalogo.FAMILIAS for o in catalogo.OPCIONES[d][f]})} for d in catalogo.DIMENSIONES})},
            "perfil": {"type": "object", "additionalProperties": False,
                       "properties": {"servicio": {"type": "array", "items": {"type": "string", "enum": list(catalogo.SERVICIOS)}},
                                      "precio": {"type": "integer", "minimum": 1, "maximum": 4},
                                      "ambiente": {"type": "array", "maxItems": 3, "items": {"type": "string", "enum": list(catalogo.AMBIENTES)}}}},
            "pedido": {"type": "object", "additionalProperties": False,
                       "properties": {"canal": {"type": "string", "enum": ["whatsapp", "llamada"]}, "nota_ejemplo": TEXTO, "textos": {"type": "object"}}},
            "idea": {"type": "object", "additionalProperties": False, "required": ["tipo", "categoria", "unidad", "por", "sobretitulo", "titulo", "texto", "mejor", "nota"],
                     "properties": {"tipo": {"type": "string", "enum": ["medida"]}, "categoria": ID_CORTO, "unidad": TEXTO, "por": TEXTO, "sobretitulo": TEXTO, "titulo": TEXTO,
                                    "texto": TEXTO, "texto_js": TEXTO, "mejor": TEXTO, "nota": TEXTO}},
            "muestra": {"type": "object", "additionalProperties": False, "required": ["ejemplo_ficticio"],
                        "properties": {"ejemplo_ficticio": {"type": "boolean"}, "permiso": {"type": "string", "enum": ["pendiente", "concedido"]}, "origen_datos": TEXTO,
                                       "nota_panel": TEXTO, "incluye": {"type": "array", "minItems": 1, "maxItems": 4, "items": TEXTO}, "base_url": {"type": ["string", "null"]}}},
            "gate_pruebas_pedido": {"type": "object"},
            "gate_pruebas_horario": {"type": "array"},
            "excepciones_gate": {"type": "object"},
        },
    }


# ------------------------------------------------------------------ mensajes en español para los errores del esquema
_TIPOS = {"string": "un texto", "number": "un número", "integer": "un número entero", "boolean": "verdadero o falso", "array": "una lista", "object": "un bloque con campos", "null": "null"}
_PISTAS = {
    "telefono": 'formato internacional: signo más y de 8 a 15 dígitos, sin espacios ni guiones (ejemplo "+17867282934")',
    "whatsapp": 'solo dígitos con el código de país, sin signo ni espacios (ejemplo "584127705633"), o null',
    "zona_horaria": 'nombre IANA de la ciudad (ejemplo "America/Caracas")',
    "fecha": "formato AAAA-MM-DD", "id": "solo minúsculas, números y guion bajo, sin tildes ni espacios",
    "archivo": 'ruta "id_del_restaurante/nombre.ext" con jpg, jpeg, png, webp o avif',
    "hora_preferida": "hora HH:MM en 24 h", "version": 'formato "1.0.0"', "url": "debe empezar por https://",
}


def _ruta(e, F=None):
    """Ruta del error con el id de cada categoría y de cada plato en vez de su posición (carta[picadas].platos[picadas-2].precio)."""
    partes, nodo = [], F
    for p in e.absolute_path:
        if isinstance(p, int):
            ident = nodo[p].get("id") if isinstance(nodo, list) and p < len(nodo) and isinstance(nodo[p], dict) else None
            partes.append(f"[{ident if ident else p}]")
        else:
            partes.append(("." if partes else "") + str(p))
        try:
            nodo = nodo[p]
        except (KeyError, IndexError, TypeError):
            nodo = None
    return "".join(partes) or "(raíz)"


def _traducir(e, F=None):
    ruta = _ruta(e, F)
    v = e.validator
    ultimo = str(e.absolute_path[-1]) if e.absolute_path else ""
    if v == "required":
        faltan = [x for x in e.validator_value if x not in (e.instance if isinstance(e.instance, dict) else {})]
        return f"{ruta}: " + (f"falta el campo obligatorio {faltan[0]}" if len(faltan) == 1 else f"faltan los campos obligatorios {', '.join(faltan)}")
    if v == "enum":
        return f"{ruta}: valor no permitido ({e.instance!r}). Permitidos: {', '.join(str(x) for x in e.validator_value)}"
    if v == "type":
        esperado = e.validator_value if isinstance(e.validator_value, list) else [e.validator_value]
        return f"{ruta}: debe ser {' o '.join(_TIPOS.get(t, t) for t in esperado)} (se encontró {type(e.instance).__name__})"
    if v == "pattern":
        return f"{ruta}: formato no válido ({e.instance!r}); {_PISTAS.get(ultimo, 'revisa el formato en el esquema 01')}"
    if v == "additionalProperties":
        extra = re.findall(r"'([^']+)'", e.message)
        return f"{ruta}: campo desconocido {', '.join(extra)} (¿error de escritura o un campo que no existe en el esquema?)"
    if v in ("exclusiveMinimum", "minimum"):
        return f"{ruta}: el valor {e.instance!r} no es válido (debe ser mayor que {e.validator_value})" if v == "exclusiveMinimum" else f"{ruta}: debe ser al menos {e.validator_value}"
    if v == "minItems":
        return f"{ruta}: la lista necesita al menos {e.validator_value} elementos"
    if v == "maxItems":
        return f"{ruta}: la lista admite como máximo {e.validator_value} elementos"
    if v == "minLength":
        return f"{ruta}: no puede estar vacío"
    if v in ("oneOf", "not"):
        return f"{ruta}: el plato debe tener precio o variantes con precio, no las dos cosas ni ninguna"
    return f"{ruta}: {e.message}"


# faltas del motor (generar.validar_ficha) que dicen lo mismo que el esquema, con peor mensaje
_REDUNDANTES = [r"^negocio\.\w+( \(desconocido\))?$", r"^moneda$", r"^estilo\.(paleta|forma|movimiento|tipografia) \(", r"^contacto\.telefono \(formato",
                r"^contacto\.whatsapp \(solo", r"^carta\.[^ ]+ \(debe tener un precio o variantes", r"^carta\.[^ ]+ \(id y nombre\)", r"\(variante sin etiqueta o sin precio\)",
                r"^confirmación \(estado y fecha\)", r"^carta$", r"^carta\.[^ ]+ \(id, título y platos\)"]


def errores_de_esquema(F):
    try:
        import jsonschema
    except ImportError:
        return ["falta la librería jsonschema (pip install jsonschema) para comprobar la forma de la ficha"]
    val = jsonschema.Draft7Validator(esquema())
    out = []
    for e in sorted(val.iter_errors(F), key=lambda x: [str(p) for p in x.absolute_path]):
        t = _traducir(e, F)   # oneOf anida sus motivos: el mensaje propio ya los resume
        if t not in out:
            out.append(t)
    return out


# ------------------------------------------------------------------ completar lo que no es del redactor: las pruebas del Gate
def completar(F):
    """Añade a la ficha las pruebas que el Gate necesita y que no escribe quien redacta (el pedido de prueba). Devuelve lo que añadió."""
    hecho = []
    if F.get("pedido") and not F.get("gate_pruebas_pedido"):
        cats = [c for c in F.get("carta", []) if c.get("platos")]
        if cats:
            def op(p, i=0):
                return f"{p['id']}~{i}" if p.get("variantes") else p["id"]
            lineas = []
            primera = cats[0]["platos"]
            p1 = primera[1] if len(primera) > 1 else primera[0]
            lineas.append({"op": op(p1), "cantidad": 3})
            con_sup = next((p for c in cats for p in c["platos"] if p.get("suplementos")), None)
            if con_sup is not None:
                lineas.append({"op": op(con_sup, 1 if con_sup.get("variantes") and len(con_sup["variantes"]) > 1 else 0), "cantidad": 1, "suplementos": [0]})
            elif len(cats) > 1:
                lineas.append({"op": op(cats[1]["platos"][0]), "cantidad": 1})
            ultima = cats[-1]["platos"][0]
            if all(l["op"] != op(ultima) for l in lineas):
                lineas.append({"op": op(ultima), "cantidad": 2})
            F["gate_pruebas_pedido"] = {"lineas": lineas}
            hecho.append("gate_pruebas_pedido")
    return hecho


# ------------------------------------------------------------------ revisión completa
def _textos(x, ruta=""):
    """Todos los textos de la ficha con su ruta (para buscar frases que el Gate rechaza)."""
    if isinstance(x, str):
        yield ruta, x
    elif isinstance(x, dict):
        for k, v in x.items():
            if k in ("gate_pruebas_pedido", "gate_pruebas_horario", "excepciones_gate") or (ruta == "confirmacion" and k == "nota"):
                continue   # lo que no se publica en la página no se revisa como frase de la página
            yield from _textos(v, f"{ruta}.{k}" if ruta else k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from _textos(v, f"{ruta}[{i}]")


def revisar(F, ruta=None, comprobar_fotos=True, fotos_de_prueba=False):
    """Devuelve (errores, avisos). Un error impide construir o haría fallar el Gate; un aviso conviene mirarlo."""
    from ..gate import estatico
    from . import generar
    errores, avisos = [], []
    del_esquema = errores_de_esquema(F)
    errores += del_esquema
    try:
        generar.validar_ficha(F)
    except generar.FichaIncompleta as e:
        faltas = str(e).split(": ", 1)[-1].split("; ")
        for f in faltas:
            if not comprobar_fotos and "archivo (no existe" in f:
                continue
            # una falta del motor que el esquema ya señaló con un mensaje más claro no se repite
            if del_esquema and any(re.search(r_, f) for r_ in _REDUNDANTES):
                continue
            if f not in errores:
                errores.append(f)
    except Exception as e:   # una ficha rota por dentro (clave que falta) ya la señaló el esquema; aquí solo se evita el traceback
        if not errores:
            errores.append(f"la ficha no se pudo revisar: {type(e).__name__}: {e}")
    # fotos: procedencia y calidad de los originales (R-FOT-01 y R-FOT-02); calificacion de Google (R-VAL-01 y R-VAL-02)
    e_f, a_f = calidad.revisar(F, generar.ORIGEN_ACTIVOS, con_archivos=comprobar_fotos)
    if fotos_de_prueba:   # solo para probar el sistema: las faltas de las fotos pasan a avisos y la web resultante no es entregable
        avisos += [f"(PRUEBA) {x}" for x in e_f if x not in errores] + a_f
    else:
        errores += [x for x in e_f if x not in errores]
        avisos += a_f
    a_v = valoracion.validar(F)[1]
    avisos += a_v
    # zona horaria real
    tz = (F.get("negocio") or {}).get("zona_horaria")
    if tz:
        try:
            from zoneinfo import ZoneInfo
            ZoneInfo(tz)
        except Exception:
            errores.append(f"negocio.zona_horaria: {tz!r} no es una zona horaria que exista (ejemplo America/Caracas)")
    # horario
    for d, tramos in (F.get("horario") or {}).items():
        for t in tramos if isinstance(tramos, list) else []:
            if isinstance(t, list) and len(t) == 2 and t[0] == t[1]:
                errores.append(f"horario.{d}: apertura y cierre iguales ({t[0]})")
    # coherencia entre estado de los datos y muestra
    est = (F.get("confirmacion") or {}).get("estado")
    fict = (F.get("muestra") or {}).get("ejemplo_ficticio")
    if est == "ejemplo" and fict is False:
        errores.append("confirmacion.estado es ejemplo pero muestra.ejemplo_ficticio es false (un ejemplo es un restaurante inventado)")
    if est in ("por_confirmar", "confirmado") and fict is True:
        errores.append("muestra.ejemplo_ficticio es true pero confirmacion.estado no es ejemplo")
    if est == "por_confirmar" and fict is False:
        m = F.get("muestra") or {}
        for k in ("permiso", "origen_datos", "nota_panel"):
            if not m.get(k):
                errores.append(f"muestra.{k}: es un negocio real y falta este campo")
    # antojo: todas o ninguna (menos logo y hero) y orden_fotos
    activos = F.get("activos") or {}
    con = [k for k, a in activos.items() if isinstance(a, dict) and "antojo" in a]
    comida = [k for k in activos if k not in ("logo", "hero")]
    if con:
        sin = [k for k in comida if k not in con]
        if sin:
            errores.append(f"antojo: las fotos {sin} no tienen juicio y otras sí; se juzgan todas o ninguna")
    if (F.get("estilo") or {}).get("orden_fotos") == "antojo" and not con:
        errores.append("estilo.orden_fotos es antojo pero ninguna foto tiene juicio de antojo")
    # secciones y datos que necesitan
    orden = (F.get("estilo") or {}).get("orden") or []
    pers = (F.get("estilo") or {}).get("personalidad")
    if "idea" in orden and pers == "elegante" and not F.get("historia"):
        errores.append("estilo.orden lleva idea pero la ficha no tiene historia")
    if "regla" in orden and not F.get("idea"):
        errores.append("estilo.orden lleva regla pero la ficha no tiene idea")
    if "como" in orden and not F.get("pedido"):
        errores.append("estilo.orden lleva como pero la ficha no tiene pedido")
    if "reserva" in orden and not F.get("reservas"):
        errores.append("estilo.orden lleva reserva pero la ficha no tiene reservas")
    # frases que el Gate rechaza (se avisan aquí, antes de construir)
    for ruta_t, t in _textos(F):
        if estatico.MARCA_PROHIBIDA.search(t):
            errores.append(f"{ruta_t}: menciona herramientas de IA, modelos o una marca que no se puede nombrar ({estatico.MARCA_PROHIBIDA.search(t).group(0)!r})")
        for nombre, patron in estatico.ETICA:
            m = re.search(patron, t.lower())
            if m:
                errores.append(f"{ruta_t}: {nombre} ({m.group(0).strip()!r}); reescribe con un dato concreto")
        for ph in estatico.PLACEHOLDERS:
            if re.search(ph, t.lower()):
                errores.append(f"{ruta_t}: marcador de relleno ({ph})")
        if chr(0xAB) in t or chr(0xBB) in t:
            errores.append(f"{ruta_t}: lleva comillas angulares; usa comillas rectas")
    # longitudes y detalles de oficio (avisos)
    N = F.get("negocio") or {}
    if N.get("descripcion") and not 80 <= len(N["descripcion"]) <= 175:
        avisos.append(f"negocio.descripcion mide {len(N['descripcion'])} caracteres (lo habitual es de 100 a 160)")
    if N.get("lema") and not 2 <= len(N["lema"].split()) <= 14:
        avisos.append(f"negocio.lema tiene {len(N['lema'].split())} palabras (lo habitual es de 3 a 12)")
    for c in F.get("carta") or []:
        nombres = [p.get("nombre") for p in c.get("platos", [])]
        if len(set(nombres)) != len(nombres):
            avisos.append(f"carta.{c.get('id')}: hay nombres de plato repetidos")
        for p in c.get("platos", []):
            if p.get("descripcion") and len(p["descripcion"]) > 130:
                avisos.append(f"carta.{c.get('id')}.{p.get('id')}: la descripción mide {len(p['descripcion'])} caracteres (mejor hasta 110)")
            tope = 2_000_000 if F.get("moneda") in MONEDAS_GRANDES else 5000
            for precio in [p.get("precio")] + [v.get("precio") for v in p.get("variantes", [])] + [s.get("precio") for s in p.get("suplementos", [])]:
                if isinstance(precio, (int, float)) and (precio > tope or round(precio, 2) != precio):
                    avisos.append(f"carta.{c.get('id')}.{p.get('id')}: precio raro ({precio})")
    for k, a in activos.items():
        if isinstance(a, dict) and len(a.get("alt", "")) > 140:
            avisos.append(f"activos.{k}.alt mide {len(a['alt'])} caracteres (mejor hasta 125)")
        if isinstance(a, dict) and re.match(r"^(foto|imagen) de", (a.get("alt") or "").lower()):
            avisos.append(f"activos.{k}.alt empieza con foto de o imagen de; describe directamente lo que se ve")
    if pers == "urbano" and len(F.get("galeria") or []) < 6:
        avisos.append("la galería tiene menos de 6 fotos: el mural de la portada se verá repetitivo")
    if ruta:
        base = os.path.splitext(os.path.basename(ruta))[0]
        if F.get("id") and base not in (F["id"], "ficha"):
            avisos.append(f"el nombre del archivo ({base}) no coincide con el id ({F['id']})")
    return errores, avisos


def mensaje_para_corregir(errores):
    """Texto listo para pegar en el chat del modelo que escribió la ficha."""
    lineas = "\n".join(f"- {e}" for e in errores)
    return ("El validador encontró estos errores en tu ficha. Devuélveme la ficha COMPLETA corregida (en un bloque JSON), sin cambiar lo que ya estaba bien, "
            "y dime en una línea qué corregiste:\n" + lineas)
