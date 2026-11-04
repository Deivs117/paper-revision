# Consolidado y triage de la auditoría final de la ronda 2 (C-77 a C-81)

Fuentes integradas: **Sam** (`final_audit_r2_samuel_2026-11-03.md`, IDs `S-`), **Sebas** (`final_audit_r2_sebas_2026-11-03.md`,
IDs `A-`/`M-`/`B-`/`N-`) y **Deivi** (3 pasadas de agente con Opus: datos `D-`, redundancia `R-`, lenguaje `L-`; informes completos en
`final_audit_r2_deivi_{datos,redundancia,lenguaje}_2026-11-03.md`). Pendiente: Diego (C-78); no bloquea el envío.

Este documento **solo cruza, clasifica y prioriza**: el detalle, la verificación y la corrección sugerida de cada hallazgo están en el informe
de origen. No se ha editado `sections/`. Cuando varios IDs son el mismo hallazgo se escriben juntos (`S-02 = A-4 = D-04 = L-02`).
Recuento: 182 entradas brutas → **≈ 120 hallazgos únicos**; varias entradas agrupan micro-correcciones.

## Criterio de priorización (decidido por el autor, 2026-11-03)

**Prima la consistencia del paper consigo mismo** (texto contra texto, tablas, ecuaciones y figuras que ya están en el manuscrito), **no
la consistencia con `experiments/`**. No hay tiempo de volver a la raíz de los datos. Consecuencias:

- Lo que el paper ya afirma se mantiene: si menciona 3 ensayos, son 3; no se añade un cuarto porque exista en el repo.
- Un hallazgo que solo existe al contrastar con los datos crudos **no se corrige ahora**: se anota en la sección C como riesgo conocido.
- Se evita regenerar figuras salvo que el paper se contradiga a sí mismo (sección D).

Secciones: **A** corregir ahora · **B** decisión del autor (solo contradicciones internas) · **C** riesgos conocidos aparcados · **D** figuras.

---

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

## B. Decisión del autor (solo contradicciones internas del paper)

**Estado 2026-11-03: los 18 puntos están resueltos; ver "Decisiones tomadas por el autor". Pendientes solo de confirmación: texto del AI disclosure y nombres de autor.** Lo que sigue es el listado original.

Orden sugerido: primero 1–8 (afectan a lo que el revisor lee primero), luego el resto en bloque.

1. **Appetitive: la tabla dice 3.0–9.0 s y el ECDF del propio paper llega a 13.2 s** (S-03 = D-06, S-09). Se mantienen 3 réplicas. Decidir: ¿la celda pasa a "hasta ≈ 13 s" (sin recomputar) o se retira la ventana?
2. **"CPG" en Introducción y Conclusiones; el método no describe ninguno** (S-06). ¿Se cambia el texto o se describe el generador de marcha?
3. **F1 del MLP: texto 0.771 / LR 0.692 vs. figura 0.734 / 0.659** (S-13 = D-12). Opción barata: alinear el texto con la figura (sin regenerar).
4. **λ con dos definiciones** (S-16 = M-3 = D-16 = L-03): ¿renombrar (λ_trial / λ_conflict) o quitar λ de la tabla FSM?
5. **$X_{15}/X_{16}$ con dos significados** (S-21 = M-1).
6. **N-1, N-2, N-3** (`introduction.tex:34` función del MLP; `results.tex:608` figura equivocada y neuronas inactivas; `:597` "$L_4$ ≈35 s"): requieren que indiques la figura o el valor correcto.
7. **Aversive y Obstacle sin resultado** (`results.tex:82` y `:91`, L-35): ¿se escribe el resultado o se recorta la frase?
8. **Recortes de redundancia que tocan lo pedido por un revisor** (R-22): quitar `tab:mode_steady_state_energy` (S-31) dejaría sin objeto R3b-05; pasar `table:Locom_MLP` a prosa (B-6) va contra R3b-01. **Recomendación: conservar ambas.**
9. **Umbral $Ar$: % de ancho vs. "bounding-box area units"** (S-18 = L-04).
10. **Ecuaciones de Methodology**: índices de la red integradora (S-24 = M-4), $z_5$/$z_6$ ambos $L_2$ (M-5), $\omega$ "amplificación" (M-6), "no lateral inhibition" (M-7), $\sigma_Z$ "dimensionless" (M-12), entradas del MLP descritas de dos formas (M-13), M-10, L-23, "Normalized SM" en metros (L-09).
11. **Distancia de parada 1.08 m vs. 31 cm de diseño** (M-9).
12. **Ciclo de 6 fases vs. "two transfer sub-phases"** (S-20 = M-8) · **"instantaneous step response"** (S-22) · **"guaranteeing static stability" vs. SM negativo** (S-19) · **"≈5°" sin origen en el paper** (S-23).
13. **Terreno Neural "solo sin perturbación": dos explicaciones incompatibles** (S-15 = D-17) · **semilla fija vs. "different dropout realization"** (S-17).
14. **Afirmaciones de robustez/postura** (S-25: Conclusiones atribuye robustez por sensor; D-14: "postural stability does not degrade on either terrain" frente al Pitch RMS que sube en la propia figura).
15. **"Energy-aware" en la Introducción vs. Conclusiones** (S-38 = M-19).
16. **Sensor "onboard INA" en los captions de energía, ausente de `table:HardwareParams`** (L-01).
17. **Nombres de autor, portada vs. CRediT** (S-33 = M-18 = L-13) y **AI disclosure** (solo nombra ChatGPT; B-13).
18. **Recortes de redundancia con matiz**: caveat FSM ×6 (R-01 = S-28; las captions se quedan, solo la prosa de `:522`), caveat de perturbación conjunta ×7–9 (M-14; R2b-02 pide una mención breve), M-16 (ablación contada dos veces), M-17 = R-18, B-5 = R-11, R-07, R-08 = S-26, y **R-17 = S-30** (escenarios físicos, ≈ 250 palabras: hacerlo el último).

---

## C. Riesgos conocidos, aparcados (existen solo al contrastar con los datos; no se corrigen ahora)

**Nada de esta sección se menciona ni se matiza en el paper**: los datos sí se validaron en su momento; simplemente no hay tiempo de rastrear ahora dónde están. No se añade ninguna salvedad de 'no validado' a texto ni captions. El paper no se contradice a sí mismo aquí. Quedan anotados por si un revisor pide los datos. Detalle en los informes de origen.

| Tema | IDs | Qué dicen los datos |
|---|---|---|
| "Ningún ensayo violó TR = 1 en los 30" | A-3 = D-03 | 4 de 30 superan TR = 1 (máx. 1.86); la banda de la propia figura ya se sale del eje |
| "$N_{ev}^X < N_{ev}^{LiDAR}$ en los 17 ensayos sin excepción" | S-12 = A-2 = D-02 | `test_014` tiene cociente 1.0 |
| "Rugged alone accounts for tipovers/crashes" | D-08 | Complex tuvo 3 vuelcos |
| FSM inspección: "11 de 20 nunca ven el objetivo" | D-09 | Son 9; otros 2 timeouts sí lo detectan |
| Fila Obstacle: "≈1100, t < 7 s, settles t = 8 s" | D-10 | Picos 1316 / 684 / 688 en las 3 réplicas |
| Origen de las latencias 184/534 ms ("15 replicates") | S-04 = A-7 = D-11 | Coinciden al ms con un banco de pitch de 25 ensayos |
| Flash del MLP "30.4 % de 4 MB" | S-02 (parte) | Es el 30.4 % de la partición de app de 1.25 MB |
| `noise_idx` = 0 en los 96 intentos de simulación; "noisiest levels" | M-2 · D-13 · C-75 §2 | La batería no registra niveles de ruido |
| "Sub-millisecond in the vast majority of trials" | A-6 | Exagera |
| "Non-chromatic obstacle cue" | S-11 | Falso según Sam |
| "30× longer" | D-20 | 27× |
| Máximo de transiciones (15.88 J) y "typical 38 s" (un solo segmento) | S-01 (parte) = D-22 | |
| Tipo de SD en la figura de energía (poblacional vs. muestral; C-74 cerrada) | D-21 | |
| Fila "three replicates each" con valores de un solo ensayo | S-09 | |

---

## D. Figuras

Solo se regeneran las que el propio paper contradice. Cada una pasa por `experiments/` + `scripts/promote_figure.sh`.

| Figura | Cambio | Estado |
|---|---|---|
| `FigReal_Terrain_Latencies_4Panels.png` | Títulos "Differential Mobile" → "Rolling" (los de leyenda/escalones van a la sección C) | Regenerar (autorizado por el autor, 2026-11-03; cierra S-34) |
| `FigReal_Morphological_Transition_Energy.png` | Pie cortado por los dos bordes; etiquetas "Differential Mobile" | Regenerar (autorizado; pie ilegible + etiquetas) |
| ECDF físicos (título con em dash) | Cambiar título | Opcional, baja |
| `fig_mode_timeline_inspection.png` (eje en tiempo de pared) · `FigB_Decision_Delay.png` (eje log) · `FigA_Stability_Profile.png` (banda fuera del eje) | | Opcionales; el último pertenece a C |
| Panel (a) de `fig:classifier_tradeoff` | | **No regenerar**: se alinea el texto (B.3) |

---

## Orden sugerido
1. Aplicar **A.1** en una sola pasada y **A.2** tras tu lectura rápida.
2. Tú decides **B**, empezando por 1–8.
3. Figuras de **D** que decidas mantener.
4. Recortes de B.18 al final (R-17 solo cuando B.1 esté cerrada).
5. Ninguna de la sección **C** se toca; queda como constancia.

## Pendiente
- Diego (C-78): sin entregable; cerrar la fila o recibir un delta solo sobre `methodology.tex`.
- Cada fila nueva en `PROGRESS.md` necesita `Owner` y `Category`; la edición de `sections/` pasa por `sections/` + `PROGRESS.md` + `patches/`.

## Texto propuesto del AI disclosure (autor aprobó añadir Claude; redacción final al aplicar)

"During the writing of this manuscript and its revisions, we used AI-based tools, including ChatGPT (OpenAI) and Claude (Anthropic), as editorial support to improve grammar, clarity, tone and coherence, and Claude (Anthropic) as a coding assistant to maintain the manuscript source and to run the analysis and plotting scripts that regenerate figures and tables from the experimental data. These tools were not used to design the experiments, collect the data, or draw the scientific conclusions. The authors critically reviewed, edited and approved all content, verified the outputs of the scripts, and take full responsibility for the accuracy and integrity of the manuscript."

## Estado de la aplicación (2026-11-03)
**Ninguna corrección se ha aplicado a `sections/`.** El autor indicó que no se aplica nada hasta que lo ordene. El parche C-82 de Diego (PR #38) ya está en `main`; no interfiere con las ediciones planeadas.
