/* Módulo marquesina: la banda que corre con lo que ofrece la casa (bajo la portada o dentro de la portada de cartel); el movimiento es CSS y aquí solo se comprueba que esté. */
EDU.modulo('marquesina', function () { return !!window.EDU.qs('.marq-caja, .cartel-cinta'); });
