# 06. Juicio de antojo de las fotos

Se usa solo en la personalidad URBANO, para ordenar el mural y la galería de la más provocativa a la menos (estilo.orden_fotos igual a "antojo"). En ELEGANTE no hace falta: omite el campo antojo.

Regla de oro: juzgas MIRANDO la foto. Si no puedes ver las imágenes, no inventes juicios: no pongas antojo en ninguna foto, no pongas orden_fotos y anótalo en Por confirmar. Las fotos se juzgan todas o ninguna: si una foto de comida o del local (menos logo y hero) lleva antojo y otra no, el verificador lo marca como error.

## Cómo se juzga cada foto

Para cada uno de los siete criterios pon un número: 0 si no, 1 si en parte, 2 si claramente sí. No infles: un 2 es un sí sin dudas, y la mayoría de las fotos de redes sociales tienen varios 0 y 1. Una foto con todo 2 es rarísima.

{{CRITERIOS}}

## Los campos de cada foto

- juicio: los siete criterios con su 0, 1 o 2, con estas claves exactas: textura, reconocible, accion, protagonista, luz, calor, mano.
- real: true si es una foto verdadera del plato o del local; false si es una ilustración, un render o una imagen generada.
- sin_marcas_ajenas: true si no hay logotipos de otras marcas, marcas de agua ni textos de terceros. El logo o la tabla con el nombre del propio restaurante NO es una marca ajena.
- nota: una frase con lo que ves y lo que resta puntos. Ejemplo: "Lomo con tocino ya cortado, con luz cálida lateral y la tabla con el nombre de la casa; se ve el interior jugoso."

Si una foto es real pero no es de comida (el local, el trailer, la fachada), también se juzga: lo normal es 0 o 1 en textura, acción, calor y mano, y quedará al final del orden. Una foto con real false o sin_marcas_ajenas false queda fuera del ranking y no debe usarse en ninguna parte de la web (ni galería ni carta): quítala de la ficha y anótalo en Por confirmar.

## Cómo se combina

El motor suma el 65 por ciento de tu juicio y el 35 por ciento de cuatro medidas técnicas que calcula solo (nitidez en la zona del plato, calidez de la luz, saturación y contraste). Tú no calculas nada técnico: solo miras y juzgas.

## Ejemplos de referencia

- Lomo con tocino ya cortado, luz lateral cálida, un solo protagonista, tabla con el nombre de la casa: textura 2, reconocible 2, accion 1, protagonista 2, luz 2, calor 1, mano 2.
- Picada larga de chorizos, pollo y cortes sobre una tabla con fondo de acero que enfría la luz: textura 2, reconocible 2, accion 0, protagonista 1, luz 1, calor 1, mano 2.
- Asador vertical con brochetas junto a las brasas, composición cargada y una barra metálica que estorba: textura 2, reconocible 1, accion 1, protagonista 1, luz 2, calor 2, mano 1.
- El trailer del restaurante con su logo y su teléfono (no es un plato): textura 0, reconocible 1, accion 0, protagonista 2, luz 2, calor 0, mano 1.
