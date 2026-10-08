"""País, moneda y formato de importes.

Los datos de formato (separadores y plantillas) se portan del kit de propuestas, que ya los tenía
validados. El país y la moneda los da siempre el ficha del restaurante: nunca se suponen.
"""
NBSP = chr(0xA0)  # espacio duro: une símbolo y número para que no queden en líneas distintas

# código: (nombre, moneda habitual, separador de miles, separador decimal, habla española)
PAISES = {
    "ES": ("Espana", "EUR", ".", ",", True),
    "VE": ("Venezuela", "USD", ".", ",", True),
    "CO": ("Colombia", "COP", ".", ",", True),
    "MX": ("Mexico", "MXN", ",", ".", True),
    "PE": ("Peru", "PEN", ",", ".", True),
    "CL": ("Chile", "CLP", ".", ",", True),
    "AR": ("Argentina", "ARS", ".", ",", True),
    "EC": ("Ecuador", "USD", ".", ",", True),
    "PA": ("Panama", "USD", ",", ".", True),
    "DO": ("República Dominicana", "DOP", ",", ".", True),
    "UY": ("Uruguay", "UYU", ".", ",", True),
    "PY": ("Paraguay", "PYG", ".", ",", True),
    "BO": ("Bolivia", "BOB", ".", ",", True),
    "CR": ("Costa Rica", "CRC", ".", ",", True),
    "GT": ("Guatemala", "GTQ", ",", ".", True),
    "SV": ("El Salvador", "USD", ",", ".", True),
    "HN": ("Honduras", "HNL", ",", ".", True),
    "NI": ("Nicaragua", "NIO", ",", ".", True),
    "PR": ("Puerto Rico", "USD", ",", ".", True),
    "US": ("Estados Unidos", "USD", ",", ".", False),
    "CA": ("Canada", "CAD", ",", ".", False),
    "BR": ("Brasil", "BRL", ".", ",", False),
    "PT": ("Portugal", "EUR", ".", ",", False),
    "FR": ("Francia", "EUR", ".", ",", False),
    "IT": ("Italia", "EUR", ".", ",", False),
    "DE": ("Alemania", "EUR", ".", ",", False),
    "GB": ("Reino Unido", "GBP", ",", ".", False),
}

EURO = chr(0x20AC)
LIBRA = chr(0xA3)

# moneda -> plantilla ({n} es el número ya formateado)
MONEDAS = {
    "EUR": "{n}" + NBSP + EURO,
    "USD": "US$" + NBSP + "{n}",
    "VES": "Bs." + NBSP + "{n}",
    "COP": "$" + NBSP + "{n}" + NBSP + "COP",
    "MXN": "$" + NBSP + "{n}" + NBSP + "MXN",
    "PEN": "S/" + NBSP + "{n}",
    "CLP": "$" + NBSP + "{n}" + NBSP + "CLP",
    "ARS": "$" + NBSP + "{n}" + NBSP + "ARS",
    "DOP": "RD$" + NBSP + "{n}",
    "UYU": "$U" + NBSP + "{n}",
    "PYG": "Gs." + NBSP + "{n}",
    "BOB": "Bs" + NBSP + "{n}" + NBSP + "BOB",
    "CRC": "CRC" + NBSP + "{n}",
    "GTQ": "Q" + NBSP + "{n}",
    "HNL": "L" + NBSP + "{n}",
    "NIO": "C$" + NBSP + "{n}",
    "GBP": LIBRA + "{n}",
    "CHF": "CHF" + NBSP + "{n}",
    "BRL": "R$" + NBSP + "{n}",
    "CAD": "CA$" + NBSP + "{n}",
}


# plantilla propia del país cuando la costumbre local difiere de la general (en Estados Unidos el dólar se escribe $15.00)
PLANTILLAS_PAIS = {("US", "USD"): "${n}"}


def separadores(pais):
    if pais not in PAISES:
        raise ValueError(f"País desconocido: {pais}. El país lo da la ficha; no se supone.")
    return PAISES[pais][2], PAISES[pais][3]


def formato_numero(monto, pais, fijos=False):
    """Número con los separadores del país. En España, los enteros de 4 cifras van sin separador. Con fijos=True siempre lleva dos decimales."""
    miles, dec = separadores(pais)
    neg = monto < 0
    ent_s, dec_s = f"{abs(float(monto)):.2f}".split(".")
    entero = int(ent_s)
    if pais in ("ES", "AD") and entero < 10000:
        txt = str(entero)
    else:
        txt = f"{entero:,}".replace(",", miles)
    if dec_s != "00" or fijos:
        txt += dec + dec_s
    return ("-" if neg else "") + txt


def formato_importe(monto, pais, moneda, fijos=False):
    """Importe listo para mostrar, por ejemplo formato_importe(18, 'VE', 'USD') da 'US$ 18'."""
    if moneda not in MONEDAS:
        raise ValueError(f"Moneda desconocida: {moneda}. La moneda la da la ficha; no se supone.")
    plantilla = PLANTILLAS_PAIS.get((pais, moneda), MONEDAS[moneda])
    return plantilla.format(n=formato_numero(monto, pais, fijos))


def precios_de_carta(F):
    """Todos los precios de la carta, incluidos los de cada variante (media libra, una libra...)."""
    out = []
    for c in F.get("carta", []):
        for p in c.get("platos", []):
            if isinstance(p.get("precio"), (int, float)):
                out.append(p["precio"])
            for v in p.get("variantes", []):
                out.append(v["precio"])
    return out


def importe_fn(F):
    """Función de formato de la ficha: un solo formato por página (R-DAT-03). Si algún precio tiene centavos, todos llevan dos decimales."""
    fijos = any(float(m) != int(m) for m in precios_de_carta(F))
    pais, moneda = F["negocio"]["pais"], F["moneda"]
    return lambda monto: formato_importe(monto, pais, moneda, fijos)


def config_js(pais, moneda):
    """Datos de formato para el JavaScript del navegador (misma lógica que formato_importe)."""
    miles, dec = separadores(pais)
    return {"pla": MONEDAS[moneda].replace("{n}", "{n}"), "miles": miles, "dec": dec, "es4": pais in ("ES", "AD")}
