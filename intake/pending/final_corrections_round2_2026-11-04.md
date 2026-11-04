# Correcciones finales de la ronda 2 — brief para quien las tome (2026-11-04)

Deadline de la ronda: **2026-11-04**. Este brief es **autocontenido**: no hace falta preguntar a Deivi qué hacer. Si algo no está claro, no lo toques y escríbelo en el PR.

Origen: auditoría final multi-autor (C-77..C-80) consolidada en `intake/pending/final_audit_r2_consolidated_2026-11-03.md`. El detalle de cada
hallazgo (ubicación exacta, verificación, corrección sugerida) está en los informes de origen, buscando `### <ID>`:
`final_audit_r2_samuel_2026-11-03.md` (IDs `S-`), `final_audit_r2_sebas_2026-11-03.md` (`A-`, `M-`, `B-`, `N-`),
`final_audit_r2_deivi_datos_2026-11-03.md` (`D-`), `final_audit_r2_deivi_redundancia_2026-11-03.md` (`R-`),
`final_audit_r2_deivi_lenguaje_2026-11-03.md` (`L-`). Cuando varios IDs son el mismo hallazgo (`S-02 = A-4 = D-04`), basta uno.

## Quién toma qué (modelo de pool)

Las filas C-83, C-84, C-85, C-86, C-87, C-88, C-89 las puede tomar **cualquiera de Sam, Sebas o Diego**. Están repartidas por archivo/rango de líneas para que
dos personas no editen las mismas líneas. Para tomar una:
1. `git pull origin main`, `python3 scripts/my_tasks.py <tu nombre>` y elige la primera fila que **no esté ya en un PR abierto**: `gh pr list --state open`.
2. Abre rápido una rama `fix/<ID>-<slug>` y un PR borrador (draft) con el ID de la fila en el título; eso es el "voy a hacerla". Si ves un PR abierto con ese ID, elige otra fila.
3. Edita **solo** tu archivo/rango. Texto nuevo o cambiado de significado va en `\revblue{...}`; erratas sin cambio de significado, no.
4. Pasa por `reassemble.py`, `validate_tex.sh`, `check_roundtrip.sh`; deja la fila en `applied` con su `patches/<id>-<slug>.tex`. Nunca `push_to_overleaf.sh`.
5. Si tu PR choca con `main` en `source/main_monolithic.tex`, `docs/data.json` o `PROGRESS.md`: `git merge origin/main`, **regenera** (`scripts/reassemble.py`, `scripts/build_dashboard.py`), no resuelvas a mano. En `PROGRESS.md` conserva todas las filas de ambos lados.

## Reglas (decididas por el autor)

- **Prima la consistencia del paper consigo mismo**, no con `experiments/`. No abras datos crudos; no hay tiempo.
- **No toques la sección C del consolidado** (riesgos conocidos aparcados) ni escribas nada sobre "datos no validados": los datos sí se validaron.
- Lo que el paper ya afirma se mantiene (p. ej. si menciona N ensayos, son N).
- Aplica **solo** lo de las tablas de abajo (A y decisiones). Si un hallazgo no está ahí, no lo apliques.
- Si una corrección choca con un revisor (`intake/pending/round2_decision_letter_2026-10-25.md`), no la apliques y avísalo en el PR.
- Las captions de `tab:fsm_comparison` y las tablas `tab:mode_steady_state_energy` y `table:Locom_MLP` **no se tocan ni se quitan**.

## Reparto

| Fila | Archivo / rango | Pistas (IDs con ubicación en tu zona; **orientativas**, manda la ubicación del informe) |
|---|---|---|
| C-83 | `sections/methodology.tex` (entero) | A-5, A-8, B-10, B-14, B-8, B-9, D-15, D-24, L-01, L-06, L-07, L-10, L-12, L-17, L-18, L-19, L-20, L-21, L-25, L-31, L-33, M-13, M-4, M-5, M-6, M-7, N-1, R-04, R-12, R-13, S-05, S-08, S-17, S-23, S-35, S-36, S-37, S-38, S-39 |
| C-84 | `sections/introduction.tex`, `conclusions.tex`, `preamble.tex`, `closing.tex` | A-8, B-10, B-13, B-14, B-15, B-4, B-9, L-10, L-15, L-19, L-20, L-27, L-28, L-31, L-37, L-44, M-18, M-19, M-21, N-1, R-12, R-15, S-25, S-33, S-37, S-39, S-40 |
| C-85 | `sections/results.tex` líneas 1–323 (Simulation Results hasta Variable Topographies) | A-5, A-8, B-12, B-14, B-15, D-14, D-18, L-08, L-15, L-16, L-18, L-19, L-21, L-24, L-25, L-28, L-29, L-30, L-31, L-34, L-35, L-41, M-20, M-21, M-22, R-02, R-03, R-05, R-06, R-12, R-13, R-19, R-20, S-05, S-08, S-17, S-27, S-29, S-36, S-37, S-39, S-40 |
| C-86 | `sections/results.tex` líneas 324–581 (estabilidad de transiciones, FSM baseline, inspección) | A-1, B-11, D-01, D-07, L-05, L-09, L-18, L-21, L-25, L-31, L-33, L-38, L-39, L-40, L-42, M-8, R-05, R-09, R-10, R-14, R-21, S-07, S-14, S-19, S-20, S-29, S-37, S-40 |
| C-87 | `sections/results.tex` líneas 582–867 (resultados físicos, MLP, topografías físicas) | A-4, B-10, B-14, B-15, D-04, L-02, L-16, L-20, L-23, L-25, L-31, L-36, L-40, L-41, M-23, N-2, N-3, S-02, S-23, S-37, S-39, S-40 |
| C-88 | `sections/results.tex` líneas 868–1055 (desempeño físico cuantitativo, energía, Limitations) | B-1, B-3, D-05, D-24, L-01, L-17, L-18, L-20, L-31, L-43, R-04, R-12, R-16, R-24, S-01, S-09, S-10, S-22, S-32, S-37, S-39 |
| C-89 | Figuras (`experiments/` + `scripts/promote_figure.sh`, nunca a mano en `assets/`) | S-34 = M-20 ("Differential Mobile" → "Differential Rolling" en `FigReal_Terrain_Latencies_4Panels.png` y `FigReal_Morphological_Transition_Energy.png`); pie cortado en la figura de energía. Opcionales de baja: título con em dash en los ECDF físicos, eje de `fig_mode_timeline_inspection.png`, eje de `FigB_Decision_Delay.png`. **No** regenerar el panel (a) de `fig:classifier_tradeoff` ni la leyenda "(reconstructed)" de latencias salvo lo que aquí se dice |

Pistas globales (aparecen en varias zonas, aplica en la tuya): `stimuli of different natures` → una sola forma (`M-21 = L-14 = L-28`); GPe/Gpe, siglas, guiones, en dash Unicode, comillas rectas, calcos (`B-8`, `B-9`, `B-10`, `B-11`, `B-12`, `B-14 = S-39 = L-32`, `L-15..L-21`, `L-26`, `L-29..L-33`); puntuación heredada de C-76 (`S-40 = M-22 = M-23`, `L-34..L-44`); redundancia de bajo riesgo de la lista A.1.

## Decisiones tomadas por el autor (2026-11-03)

| Punto | Decisión | Qué se hace |
|---|---|---|
| B.1 Appetitive 3 vs. 4 | **Texto a 4** (el ECDF del paper ya dibuja 4) | Caption y prosa a "four"; celda de la tabla a ≈ 0.9–13 s leída del propio ECDF. No se regenera nada |
| B.2 CPG | **Cambiar Introducción y Conclusiones** | "CPG" → patrón de marcha fijo (crawl) en lazo abierto, como ya dice Methodology |
| B.3 F1 del MLP | **Alinear el texto con la figura** | Texto a 0.734 / 0.659 (results.tex:664 y :699). No se regenera el panel |
| B.4 λ | **Renombrar** | λ_trial en la tabla, λ_conflict en Limitations |
| B.5 X15/X16 | **Notación propia de la capa de entrada** | `results.tex:597/606` usan I_15/I_16 (como el panel de la figura); ecuaciones y modos intactos |
| B.6 N-2 | **Quitar la afirmación sobre X_5/X_7** | Se borra la frase y la referencia a `fig:NEU_EST_UNIG_real`b en `results.tex:608` |
| B.7 L-35 | **Puntero a la figura** | Cerrar `results.tex:82` y `:91` con "(outcome per level in Figure~\ref{fig:noise_robustness_grid}; retained-trial rule in the paragraph above)" |
| B.8 R-22 | **Conservar las dos tablas** | `tab:mode_steady_state_energy` y `table:Locom_MLP` se quedan |
| B.9 Umbral $Ar$ | **% del ancho horizontal** | `table:PerturbationParams` (`methodology.tex:429`) pasa a "percent of image width"; añadir frase: el umbral baja con la severidad para compensar el sesgo de área |
| B.10 Distancia de parada 1.08 m vs. 31 cm (M-9) | **Dejarlo como está** | Sin cambio; pasa a la sección C como riesgo conocido |
| B.11 $z_5$/$z_6$ ambos $L_2$ (M-5) | **Errata confirmada con el grafo** (X5 recibe L2+L4; X6 recibe L3+L4) | `eq:Z_6` usa $L_3$ y la frase "where $L_2$ and $L_4$ denote…" (`methodology.tex:215`) menciona también $L_3$ |
| B.12 $\sigma_Z$ "dimensionless" (M-12) | **Dejarlo como está** | Sin cambio; pasa a C |
| Pasan a A.2 por defecto (corrección sale del propio texto) | S-20 = M-8, S-19, M-4, M-6, M-7, M-13 | Cuatro sub-fases de transferencia (una por pata) · suavizar "guaranteeing static stability" · índices de `eq:InputL`/`eq:ResL`/`eq:L4` · pesos $\omega_{X_4\to X_7}$ como inhibición · "no lateral inhibition" matizado · entradas del MLP igual en `:339` y `:348` ("angular rates") |
| B.13 Neural en terreno "sin perturbación" (S-15 = D-17) | **Sin cambio (retirado)** | `results.tex:480` y `:522` ya dicen lo mismo (cero ruido); `methodology.tex:439` no dice "matching noise levels" (era paráfrasis de Sam). No es contradicción interna |
| B.14 Semilla fija vs. "different dropout realization" (S-17) | **Quitar la afirmación de realización distinta** | `results.tex:184`: el reintento "at the identical severity level succeeded", sin decir que cambia la realización |
| B.15 Robustez por sensor (S-25) + postura (D-14) | **Reescribir las dos, afirmando menos** | Conclusiones: "retained task-level performance under the combined perturbation in most scenarios (failures concentrated in Appetitive timeouts and Rugged Terrain tipovers), evaluated jointly rather than per sensor". `results.tex:182`: acotar a Roll RMS en Rugged y Pitch RMS en Slope, y decir que el Pitch RMS sube con la severidad |
| B.16 "Energy-aware" en la Introducción (S-38 = M-19) | **Alinear la Introducción con Conclusiones** | Quitar "energy-aware" de la contribución (iii) |
| S-22 "instantaneous step response" | Pasa a A.2 | "a tightly clustered response (≈184 ms)" |
| B.17a Nombres de autor (S-33 = M-18 = L-13) | **Forma de la portada** (guiones y tildes, mismo orden); estándar Elsevier: debe coincidir con el registro del sistema de envío | CRediT (`conclusions.tex:26–31`) corrige apellidos y orden; conserva los nombres de pila completos. **Confirmado por el autor (2026-11-03): usar la forma de la portada** |
| B.17b AI disclosure (B-13) | **Reflejar lo que se usó de verdad** | Añadir Claude (Anthropic) y reescribir "not used to generate … analyses". **Aprobado por el autor (2026-11-03): añadir Claude**; texto en la sección "Texto propuesto del AI disclosure" (ajustable al aplicar) |
| B.17c Sensor "onboard INA" (L-01) | **INA219** | Fila "Current sensor: INA219" en `table:HardwareParams`; captions de `results.tex:986`/`:997` dicen "onboard INA219 current sensor" |
| B.18 Recortes de redundancia | **Solo lo que no toca captions pedidos** | Recortar la prosa de `results.tex:522` (repite el caption de `tab:fsm_comparison`) y `:152` (repite `:73`); captions y tablas de B.8 se quedan; R-17 no se hace |
| Por defecto en A.2/A.1 | M-10, L-09, L-23 | L-09: quitar "Normalized" a $SM$ (es una magnitud en metros) · L-23: notación de las arquitecturas del MLP · M-10 (valor 0.30 repetido en los niveles 3–4): sin cambio, pasa a C |
| S-23 "≈5°" de reenganche (`results.tex:811`) | **Quitar la cifra** (sin respaldo en el paper) | La celda queda "Pitch disturbance stays below the quadrupedal re-engagement threshold" |
| S-09 "three hardware replicates each" | Consecuencia de B.1 | "three" → N real por escenario (Appetitive: four) |
| Cambios añadidos a la sección A | N-1 (`introduction.tex:34`, función del MLP) y N-3 (`results.tex:597`, "$L_4$ activa ≈35 s, pico ≈44 s") | Se aplican: contradicen a Methodology y a la figura del propio paper |
| S-34 | Autorizado regenerar figuras | Corregir "Differential Mobile" → "Rolling" en las dos figuras de la sección D |


## A. Corregir ahora (sin decisión del autor)

### A.1 Pasada mecánica (erratas, tipografía, estilo)
| Grupo | IDs |
|---|---|
| Puntuación y sintaxis heredadas de C-76 | S-40 = M-22 = M-23 = L-34 = L-36 = L-37 · B-15 = L-41 = L-42 · L-38 · L-39 · L-40 · L-44 · L-24 |
| Ortografía y convenciones | B-10 (13 en dash Unicode) · B-11 · B-12 · S-37 · L-26 · L-19 · L-18 · L-17 · L-16 · L-20 · L-21 · L-05 (comillas rectas) |
| Captions de tabla agramaticales | L-07 |
| Siglas y notación | B-8 = L-12 (GPe/Gpe) · B-9 · L-15 · L-10 (STN/STR sin definir) · S-36 |
| Calcos del español / inglés no idiomático | S-39 = B-14 = L-32 · L-29 · L-30 · L-31 · M-21 = L-14 = L-28 · L-33 |
| Nombres incoherentes (robot, familias) | L-27 |
| Duplicados triviales | B-4 = R-15 · R-13 · R-16 · R-20 |
| Layout | L-11 (Tabla 1 desborda 37.6 pt) · L-25 (cajas sobrellenas) |
| Referencias cruzadas | D-24 · D-18 |
| Color | S-35 (azul fijo fuera de `\revblue{}`) |
| Redundancia de bajo riesgo, sin tocar captions pedidos por un revisor | R-02 = S-27 · R-03 · R-04 · R-05 = S-29 · R-06 · R-09 · R-10 · R-14 · R-19 · R-21 · R-23 · R-24 = S-32 (≈ 480 palabras) |

### A.2 Contradicciones internas donde el propio paper fija la corrección
| Tema | IDs | Corrección (sin mirar datos) |
|---|---|---|
| Qué canal es cada color | S-05 = A-5 = D-15 | Ecuaciones, Results y figuras coinciden entre sí: corregir `methodology.tex:244/290/337` |
| Qué inestabilidad dispara qué modo | S-08 = A-8 | Methodology contradice sus ecuaciones, Results y Conclusiones: alinear Methodology |
| "Differential Mobile" vs. "Differential Rolling" | S-34 = M-20 | El texto usa "Rolling" siempre; unificar (las figuras, en sección D) |
| "Se quedó en H los 20 ensayos" | A-1 = D-01 | Choca con la propia `tab:inspection_metrics` ($N_{ev}^X$ = 1–10) |
| "Solo hay un sentido de success rate" | S-07 = D-07 | Lo contradice la misma tabla (Inspection, por intento) |
| "≤ 5.06 J peor caso" / "upper bound" | S-01 = B-3 = D-05 | El paper da 5.06 ± 2.93: es una media. Reescribir como media, sin citar el máximo |
| "~47k parámetros" | S-02 = A-4 = D-04 = L-02 | La propia figura de comparación muestra ≈32.5k; alinear (el % de flash va a la sección C) |
| "± … over each row's N trials" | S-14 | Falso en 6 filas de la propia tabla |
| "27× Obstacle baseline" | S-10 = B-1 = D-23 | Cambiar "baseline" por "peak" (solo la palabra) |
| Lista colgada de "five discrete severity levels" | L-06 | Reestructurar la frase (sostiene la cautela de R2b-02) |
| Rotulación de paneles contradictoria en `fig:variable_topo_metrics` | L-08 | Un solo esquema |
| Aposición que presenta una hipótesis como hecho | L-43 | Reformular |
| Estructura de recortes que no choca con un revisor | R-12 (nota) | Nada que hacer, solo consta |

---


## Texto propuesto del AI disclosure (autor aprobó añadir Claude; redacción final al aplicar)

"During the writing of this manuscript and its revisions, we used AI-based tools, including ChatGPT (OpenAI) and Claude (Anthropic), as editorial support to improve grammar, clarity, tone and coherence, and Claude (Anthropic) as a coding assistant to maintain the manuscript source and to run the analysis and plotting scripts that regenerate figures and tables from the experimental data. These tools were not used to design the experiments, collect the data, or draw the scientific conclusions. The authors critically reviewed, edited and approved all content, verified the outputs of the scripts, and take full responsibility for the accuracy and integrity of the manuscript."

