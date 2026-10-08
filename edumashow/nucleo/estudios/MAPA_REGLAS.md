# Mapa de las reglas unificadas a los cinco estudios

Lo genera `archivo_fuente.py` a partir de `../reglas.json`; no se edita a mano. Sirve para saber qué estudio leer cuando una regla necesita su fuente. Los ids (AL-01, UX-33, CO-07 y similares) son los de la primera extracción de los estudios, que no se conservó; las páginas son las del PDF y siguen siendo válidas contra los textos completos de `texto/` y las lecturas de `analisis/`.

Prioridad: 0 verdad, legalidad y ética; 1 accesibilidad y legibilidad; 2 tarea del visitante; 3 rendimiento; 4 identidad; 5 persuasión (hipótesis); 6 variedad; guion = regla de proceso. Evidencia: N norma, M medida del proyecto, E1 a E4 según el estudio de origen.

Reglas: 76. Versión del núcleo: 0.2.0.

| Regla | Tema | Prio. | Tipo | Evid. | AL | PS | UX | CO | GR | Otras fuentes (norma, medida, orden) |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DAT-01 | datos | 0 | bloqueo | E3 | AL-01 pp.9,13,34; AL-09 pp.13,20 |  | UX-01 pp.20,31 |  | GR-I01 p.24 |  |
| R-DAT-02 | datos | 0 | bloqueo | E3 | AL-03 pp.31,37; AL-02 p.24 |  | UX-08 p.22 |  |  |  |
| R-DAT-03 | datos | 0 | bloqueo | E3 | AL-04 pp.14,21; AL-05 p.12 |  | UX-02 p.20; UX-03 p.20 |  | GR-I02 p.24 |  |
| R-DAT-04 | datos | 0 | bloqueo | E3 |  | PS-16 p.7 | UX-06 pp.18,20,30 |  | GR-A01 p.24; GR-A02 p.25 |  |
| R-DAT-05 | datos | 0 | bloqueo | E3 | AL-12 p.34 | PS-16 p.7 | UX-05 pp.18,20 | CO-07 p.8 |  |  |
| R-DAT-06 | datos | 0 | defecto | E3 | AL-08 pp.12,34 |  | UX-07 pp.18,23 |  |  |  |
| R-DAT-07 | datos | 0 | bloqueo | E3 | AL-10 pp.15,34 |  | UX-33 p.24 |  |  |  |
| R-DAT-08 | datos | 0 | bloqueo | E3 | AL-09 p.13; AL-50 pp.20,34 |  | UX-08 pp.18,22,33 |  |  |  |
| R-DAT-09 | datos | 0 | bloqueo | E3 | AL-06 pp.12,31 |  |  |  | GR-I01 p.24 |  |
| R-ETI-01 | etica | 0 | prohibido | E3 | AL-12 p.34 | PS-18 p.7 |  | CO-09 p.9 |  |  |
| R-ETI-02 | etica | 0 | prohibido | E3 | AL-13 pp.9,14 | PS-17 p.7 |  | CO-07 p.8; CO-08 p.9 |  |  |
| R-ETI-03 | etica | 0 | prohibido | E3 | AL-14 p.16; AL-15 pp.6,23 | PS-19 p.7 | UX-52 pp.1,10,22 | CO-14 p.2 | GR p.7-8 |  |
| R-ETI-04 | etica | 0 | bloqueo | E3 |  | PS-20 p.7 |  | CO-06 p.9 |  |  |
| R-ETI-05 | etica | 0 | prohibido | E2 |  | PS-21 pp.3,7; PS-25 p.4 |  | CO-27 p.5 |  |  |
| R-ETI-06 | etica | 0 | prohibido | E1 | AL-27 pp.7,24,39 | PS-28 pp.1,3,4,7 |  |  |  |  |
| R-ETI-07 | etica | 0 | bloqueo | E3 | AL-48 pp.15,22,37 |  |  | CO-13 p.9 |  |  |
| R-ETI-08 | etica | 0 | bloqueo | E2 | AL-47 pp.7,22,31 |  | UX-09 pp.8,15,18,33 | CO sec.6 p.9 |  |  |
| R-ETI-09 | etica | 0 | bloqueo | E1 |  |  | UX-22 pp.12,15,21; UX-53 pp.8,12,13; UX p.29 |  |  |  |
| R-ETI-10 | etica | 0 | bloqueo | N | AL-03 p.31 | PS sec.6 |  |  |  |  |
| R-ETI-11 | etica | 0 | bloqueo | N |  |  |  |  |  | Orden de Eduardo |
| R-ETI-12 | etica | 0 | bloqueo | N |  |  |  |  |  | Orden de Eduardo |
| R-LEG-01 | legibilidad | 1 | bloqueo | N | AL-34 p.14 |  | UX-16 pp.12,21 |  | GR-G06 p.25 | WCAG 2.2 SC 1.4.3 |
| R-LEG-02 | legibilidad | 1 | bloqueo | N |  |  | UX-17 p.21 |  |  | WCAG 2.2 SC 2.5.8 |
| R-LEG-03 | legibilidad | 1 | bloqueo | N | AL-33 p.14 |  | UX-19 pp.21,24,31 |  | GR-G01 p.25 | WCAG 2.2 SC 1.4.10 y 1.4.4 |
| R-LEG-04 | legibilidad | 1 | bloqueo | E3 |  | PS-27 p.6 | UX-15 pp.21,24 |  | GR-T03 p.25 |  |
| R-LEG-05 | legibilidad | 1 | bloqueo | N |  |  | UX-21 pp.12,21,24 |  |  | WCAG 2.2 SC 3.1.1, 1.3.1, 2.4.1, 2.4.7, 2.1.1, 4.1.2 |
| R-LEG-06 | legibilidad | 1 | bloqueo | N | AL-42 pp.4,5,33 |  | UX p.7 (hueco) |  |  | WCAG 2.2 SC 2.2.2 y 2.3.1 |
| R-LEG-07 | legibilidad | 1 | defecto | E3 |  |  | UX-18 pp.21,30 |  | GR-V05 p.26 |  |
| R-LEG-08 | legibilidad | 1 | proceso | E1 |  |  | UX-58 p.10; UX-47 pp.10,15 |  | GR p.5 (Tuch 2012) |  |
| R-LEG-09 | legibilidad | 1 | defecto | E1 |  |  | UX-24 p.9; UX-25 pp.21,30 |  | GR-G05 p.25 |  |
| R-SIG-01 | siguiente_paso | 2 | bloqueo | E3 | AL-17 pp.14,21 | PS-11 p.7; PS-10 pp.2,7 | UX-59 p.11 | CO-01 pp.5,8 |  |  |
| R-SIG-02 | siguiente_paso | 2 | defecto | E2 | AL-23 p.14 | PS-08 pp.3,7; PS-12 p.7 | UX-13 pp.7,15 | CO-02 pp.5,8 |  |  |
| R-SIG-03 | siguiente_paso | 2 | bloqueo | E1 |  | PS-08 pp.3,7 | UX-10 pp.9,14,20 | CO-03 pp.5,7,8 |  |  |
| R-SIG-04 | siguiente_paso | 2 | defecto | E2 |  | PS-09 p.3; PS-14 p.2 |  | CO-04 p.5; CO-05 pp.5-7 |  |  |
| R-SIG-05 | siguiente_paso | 2 | defecto | E2 |  | PS-07 p.7 | UX-12 pp.7,9,14 |  |  |  |
| R-SIG-06 | siguiente_paso | 2 | defecto | E3 | AL-24 p.14 | PS-12 p.7 |  | CO-10 pp.5,8 |  |  |
| R-SIG-07 | siguiente_paso | 2 | defecto | E3 |  | PS-10 pp.2,7 | UX-23 p.21 |  |  |  |
| R-SIG-08 | siguiente_paso | 2 | bloqueo | E3 | AL-35 pp.14,24 |  | UX-10 pp.9,14,20; UX-11 pp.21,24 |  |  |  |
| R-SIG-09 | siguiente_paso | 2 | defecto | E2 |  | PS-23 p.7 |  |  |  |  |
| R-SIG-10 | siguiente_paso | 2 | proceso | E3 |  |  | UX-14 pp.8,14,15 | CO-16 pp.8,9 |  |  |
| R-SIG-11 | siguiente_paso | 2 | defecto | E2 | AL-19 pp.14,33,51; AL-20 pp.29,54 | PS-24 p.7 |  |  |  |  |
| R-SIG-12 | siguiente_paso | 2 | defecto | E1 | AL-18 pp.14,51 | PS-26 p.6 | UX-56 pp.6,9,11 |  |  |  |
| R-REN-01 | rendimiento | 3 | bloqueo | M | AL-42 pp.4,5,33 |  | UX-26 p.21 (el estudio no da cifra) |  |  | Core Web Vitals; Medida: Lumbre 61 a 95 al sacar fotos del HTML |
| R-REN-02 | rendimiento | 3 | defecto | M |  |  | UX-20 p.21; UX-26 p.21 |  | GR p.14 (densidad efectiva) |  |
| R-REN-03 | rendimiento | 3 | defecto | M |  |  | UX-15 p.21 |  | GR p.13 (fuentes embebidas) |  |
| R-REN-04 | rendimiento | 3 | defecto | E3 | AL-42 pp.4,5,33 |  | UX p.29 (ablación) |  |  |  |
| R-REN-05 | rendimiento | 3 | bloqueo | M | AL-47 p.22 |  | UX-09 p.8 |  |  |  |
| R-IDE-01 | identidad | 4 | defecto | E3 | AL-25 pp.21,45; AL-26 pp.7,9,13 |  | UX-27 pp.7,21,30 |  |  |  |
| R-IDE-02 | identidad | 4 | defecto | E3 |  | PS-15 p.4 | UX-27 p.21 |  |  |  |
| R-IDE-03 | identidad | 4 | defecto | E3 |  |  | UX-28 pp.13,30; UX-60 pp.6,11 |  |  |  |
| R-IDE-04 | identidad | 4 | defecto | E3 | AL-31 pp.9,14,24 |  |  |  | GR-A04 p.24 |  |
| R-IDE-05 | identidad | 4 | defecto | E3 | AL-42 pp.4,5,33 |  | UX-58 p.10 |  |  |  |
| R-PER-01 | persuasion | 5 | hipotesis | E1 |  | PS-01 pp.1,4,6,7 |  | CO-26 pp.5-6,8 |  |  |
| R-PER-02 | persuasion | 5 | hipotesis | E1 |  | PS-22 pp.4,6 |  | CO-26 pp.5-6,8; CO-07 p.8 |  |  |
| R-PER-03 | persuasion | 5 | hipotesis | E1 |  | PS-25 p.4 | UX-56 pp.6,9,11; UX-57 pp.6,9 | CO-27 p.5 |  |  |
| R-VAR-01 | variedad | 6 | bloqueo | E3 | AL-29 pp.15,17,25 |  | UX-27 pp.7,21,30 |  | GR-V03 p.26 |  |
| R-VAR-02 | variedad | 6 | defecto | E2 | AL-29 pp.15,17,25; AL-30 pp.17,31,40 |  | UX-38 pp.25,33 |  |  |  |
| R-MUE-01 | muestra | 0 | bloqueo | M |  | PS-17 p.7 | UX-62 pp.6,7,14 |  |  |  |
| R-MUE-02 | muestra | 2 | defecto | E1 |  | PS-13 p.7 | UX-04 pp.14,20; UX-62 pp.6,7,14 | CO-11 pp.5,9 |  |  |
| R-MUE-03 | muestra | 0 | bloqueo | E3 | AL-16 pp.6,9,13,34 |  |  |  |  |  |
| R-MUE-04 | muestra | 2 | defecto | M |  |  | UX-62 pp.6,7,14 |  |  | Medida: las 3 muestras actuales no tienen vista previa de enlace |
| R-MUE-05 | muestra | 0 | bloqueo | N | AL sec.6 (suplantación) | PS sec.6 |  |  |  |  |
| R-PRO-01 | proceso | - | proceso | E3 | AL-32 pp.14,22,24 |  | UX-29 pp.3,5,8,20,22,23 |  | GR sec.9 p.15 |  |
| R-PRO-02 | proceso | - | proceso | E3 | AL-49 pp.13,22,24 |  | UX-30 pp.21,22,23 |  | GR-D02 p.26 |  |
| R-PRO-03 | proceso | - | proceso | E3 |  |  | UX-31 pp.22,23,31 |  | GR sec.9 p.15; GR Anexo B p.28 |  |
| R-PRO-04 | proceso | - | proceso | E3 |  |  | UX-32 pp.13,24,29,33 |  | GR-L01 p.27 |  |
| R-PRO-05 | proceso | - | proceso | E3 |  |  | UX-34 pp.7,21,24 |  | GR-V01 p.26 |  |
| R-PRO-06 | proceso | - | proceso | E3 | AL-49 pp.13,22,24,29,31 |  | UX-36 p.18 |  |  |  |
| R-PRO-07 | proceso | - | proceso | E3 |  |  | UX-51 pp.13,19,22,26 |  | GR sec.4 p.7 |  |
| R-MED-01 | medicion | - | proceso | E1 |  | PS-02 p.1 | UX-46 pp.4,11,28 | CO-22 pp.7,8 |  |  |
| R-MED-02 | medicion | - | proceso | E3 | AL-39 pp.10,23,30 | PS-04 pp.3,4,7 | UX-54 pp.3,14,15,18,27 | CO-19 pp.2,7,9 |  |  |
| R-MED-03 | medicion | - | proceso | E1 | AL-37 pp.17,18 |  | UX-44 pp.27,28 |  | GR sec.13 p.21 |  |
| R-MED-04 | medicion | - | proceso | E2 |  |  | UX-40 pp.13,16; UX-41 p.16; UX-42 pp.6,16 |  |  |  |
| R-MED-05 | medicion | - | proceso | E3 |  | PS sec.6 | UX-55 p.15 | CO sec.5 p.9 |  |  |
| R-MED-06 | medicion | - | proceso | E1 | AL-43 pp.14,29 |  | UX-53 pp.8,12,13,17,19 | CO-25 p.8 |  |  |
| R-MED-07 | medicion | - | proceso | E1 |  |  | UX-47 pp.10,15 | CO-24 pp.5,8,9; CO-23 pp.2,9 |  |  |
