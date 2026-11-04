# Auditoría final ronda 2: Diego (C-78), 2026-11-04

Fila `C-78`. Brief: `intake/pending/final_audit_round2_2026-11-02.md`. Pasada de **hallazgos**, no de corrección: no se
editó `sections/*.tex`. Líneas referidas a `main` en `7f57a9b` (2026-11-03); reconciliado al final con `main` en `0d6cdfe` (ver "Delta frente al consolidado"). Orden de lectura: `methodology.tex` →
`results.tex` → `introduction.tex` → `conclusions.tex` → `preamble.tex` → `closing.tex` (las seis, completas).

**Independencia.** No leí los hallazgos de Samuel ni de Sebas antes de escribir este documento. Sí vi, por otra razón
(responder "¿cuáles son mis tareas?" del dueño, el mismo día), la cabecera de ambos archivos, la sección "Sin poder
verificar" de Samuel (sus líneas 286-293: S-05, S-13, S-15, S-17; bandas del caption (b) de
`fig:noise_robustness_extra_combined`; iluminación 0.30 en los niveles 3 y 4; 8 volcaduras y 4 choques de 27 intentos),
sus verificaciones OK de esas líneas (F1 del MLP, `Ar`, estadísticos de Perlin, conteos de la ablación) y fragmentos de
sus líneas 129 y 139 (FSM a ruido 0, semilla). No reporto como hallazgo propio nada de esa lista; lo que la toca va
marcado **(no independiente)**. Ya con este documento terminado, al actualizar la fila `C-78` de `PROGRESS.md` leí el
resumen que lleva la fila `C-80` (Sebas): menciona A-1 (inspección que no se queda en H), A-3 (TR > 1 en 2 ensayos),
A-4 (flash y parámetros del ESP32), A-5 (mapeo de colores) y la subordinación de las frases de ruido a `C-75`. Mis D-01,
D-02, D-06 y D-11 estaban escritos y verificados antes de verlo; A-3 no lo pude verificar (ver "Sin poder verificar").
Si coinciden, la consolidación puede tratarlos como confirmados por dos autores.

**Cómo verifiqué.** Datos versionados recomputados con Python (`numpy`/`pandas`, sin `scipy`) desde `experiments/`;
los scripts y sus salidas están descritos en cada hallazgo. Código leído de `sammcar/PETER_SIMULATION` rama `main` @
`4ab2c1018c` (último commit 2026-06-09, vía `gh api`; las corridas de inspección son del 2026-08-29, así que es
probablemente la versión que corrió, pero **no lo puedo confirmar**). Compilé `main` (4 pasadas de pdflatex, 104
páginas, 0 errores) y miré las páginas y las 25 figuras regeneradas por C-70 a C-72 y C-75. Lo que cae en
`R3-04-noise-robustness/data/` o `R2-02-fsm-baseline/data/` va marcado *requiere verificación con datos no versionados*.

## Resumen

| Categoría | Alta | Media | Baja | Total |
|---|---|---|---|---|
| 1.1 Inconsistencias de datos | 7 | 13 | 9 | 29 |
| 1.2 Redundancia y contenido duplicado | 0 | 2 | 5 | 7 (+1 ya resuelto en el PR #38) |
| 1.3 Candidatos a acortar | 0 | 2 | 4 | 6 |
| 1.4 Ortografía y convenciones académicas | 0 | 2 | 15 | 17 |
| 1.5 Calcos del español e inglés no idiomático | 0 | 0 | 8 | 8 |
| 1.6 Texto tocado en las últimas 48 horas | 1 | 4 | 1 | 6 (C-76: sin hallazgos de puntuación) |
| **Total** | **8** | **23** | **42** | **73** |

**Las 8 de prioridad alta:**
- **D-01** colores Blue/Green de los canales de los ganglios basales: el texto contradice al código, a las figuras y a Resultados.
- **D-69** la Tabla 11 pierde sus seis últimas filas (Inspection, Rugged Terrain, Inclined Slope) en el PDF compilado.
- **D-02, D-03, D-04, D-05** cuatro afirmaciones de Resultados que los datos del repositorio contradicen: modo H en toda la inspección, "≈ 2.3× en cada ensayo sin excepción", "peor caso ≤ 5.06 J" (el máximo es 15.88 J) y la ventana `T_switch` del apetitivo físico.
- **D-07** los CPG que la Introducción y las Conclusiones dicen integrar y que la Metodología no describe.
- **D-06** (conocido, abierto: `C-75`) el ruido nunca estuvo activo en `experiments/simulation/`; aquí con dos registros independientes.

## Delta frente al consolidado del dueño

El consolidado (`final_audit_r2_consolidated_2026-11-03.md`, PR #39) y las decisiones del autor llegaron mientras yo terminaba
esta pasada, y piden de Diego "cerrar la fila o recibir un delta solo sobre `methodology.tex`". Lo leí **después** de redactar los
74 hallazgos de arriba y los crucé por ID y por palabras clave con los cinco informes de origen. `main` al cruzar: `0d6cdfe`
(PR #38 = C-82 fusionado; #40 = reparto C-83..C-89; #41 = figuras C-89). Las reglas del autor son: prima la consistencia del paper
consigo mismo, no con `experiments/`; se aplica solo lo de A y las decisiones; no se tocan las captions de `tab:fsm_comparison`.

**Ya cubiertos o decididos (no hace falta nada más de mi parte):**
- Confirmados por otros y en A.2: D-01 (= S-05 = A-5 = D-15), D-02 (= A-1 = D-01 de Deivi), D-04 (= S-01 = B-3 = D-05, con la decisión de no citar el máximo), D-08 (= M-6), D-10 (= S-24 = M-4), D-11 (= S-02 = A-4 = D-04; el % de flash va a C), D-15 (= S-23, quitar la cifra), D-19 (= N-1) y D-25 (= M-13).
- Con decisión del autor en B: D-05 (= B.1: texto a cuatro réplicas y celda 0.9-13 s; el 0.15 s de Complex ya lo vio Sam en S-09), D-07 (= B.2, CPG), D-12 (= B.4, λ_trial y λ_conflict), D-18 en lo de "energy-aware" (= B.16), D-20 y D-45 (= B.17b y B.17a) y, de D-09, solo `z_6` con `L_3` (= B.11).
- Aparcados en la sección C (no se tocan): D-03, D-06, D-21, D-22, D-23, D-24, D-28 y, de D-04 y D-11, el máximo de energía y el % de flash.
- Ya vistos por otros: D-13 (Deivi, redundancia l.220), D-14 y D-35 (D-18 de Deivi), D-26 (Samuel), D-27 (Deivi, redundancia), D-33 (M-17 = R-18) y D-36 (M-14).
- Resueltos: D-32 (C-82, en `main`) y D-71 (pie de la figura de energía, C-89).

**Nuevos respecto al consolidado** (no aparecen en ninguno de los cinco informes de origen):

| ID | Qué | Prioridad | Zona del reparto | Encaja con las reglas del autor |
|---|---|---|---|---|
| **D-69** | **La Tabla 11 pierde sus seis últimas filas en el PDF** (el consolidado solo recoge el desborde de la Tabla 1, L-11) | **Alta** | C-86 (`results.tex` l.478-502) | Sí: la variante de formato no toca el caption (probé con el caption completo y caben las 14 filas) y es del mismo tipo que L-11 ("Layout" de A.1) |
| D-17 | "no sufre bloqueos computacionales" quedó sin su respaldo tras C-66 | Media | C-85 (l.128) | Sí: contradicción interna (el respaldo se borró) |
| D-47 | "GPR" sin expandir en la Introducción (se lee como radar de penetración del suelo) | Media | C-84 (`introduction.tex` l.32) | Sí (A.1, siglas) |
| D-70 | El pie de la Fig. 43 queda pisado por el número de página (52 pt de más) | Media | C-87 (l.624-655) | Sí, layout |
| D-46 | "Figures 33 and Table 9" en el PDF | Baja | C-86 (l.455-457) | Sí (A.1) |
| D-29 | El resumen gráfico dice "outperforms" y la Tabla 11 es mixta | Baja | figura | Solo si el autor quiere tocarlo |
| D-72, D-73, D-74 | Etiquetas apretadas y "a)/b)" gigantes en `NEU_IMU`/`NEU_IMU2`; "R3-04 dataset" en el título de la Fig. 20; leyenda tapada y "base_link" en dos figuras | Media y Baja | C-89 (figuras) | Chocan con "solo se regeneran las que el paper contradice": quedan como constancia |
| D-09 (resto) | Las Ecs. (9), (Z_5), (Z_13), (Z_15), (Z_16) y `f_Imu` difieren del código leído; ningún informe compara con `red_neuronal.py` | Media | C-83 | Fuera del criterio (consistencia con el paper, no con el código): candidato a la sección C |
| D-16 | Tras B.3, `results.tex` l.666 (F1 = 0.771, 0.766, 0.747) también debe alinearse con `fig4_architecture_ablation.png`; con diferencias de 0.005 y SD de 0.033 "confirms ... most favorable" sobra | Media | C-87 | Sí, es consecuencia de B.3 |

**Mis propuestas que las reglas del autor impiden aplicar:** D-42 y D-43 (acortar las captions de `tab:fsm_comparison` y de la Fig. 28), D-38, D-39 y D-41 (fusionar o quitar tablas y figuras: B.8 y B.18) y la parte de D-04 que citaba el máximo.

**Delta solo de `methodology.tex`** (lo que pedía el consolidado): D-09 (resto), D-55 (la lista de etapas no remite a sección en el control neuronal) y D-56 (`θ_p` "initial heading" frente a su uso como variable); D-30 y D-31 (duplicados de `τ_Z`/`σ_Z` y de la justificación de `σ_M`/`σ_I`) pueden estar ya en R-04, R-12 o R-13 de la zona de C-83, que no leí a fondo. El resto de lo mío en ese archivo ya está en el consolidado.

## 1.1 Inconsistencias de datos

### Alta

#### D-01. Colores de los canales de los ganglios basales: el texto invierte Blue y Green (y el mapeo x/y/z)
- **Ubicación:** `methodology.tex` l.244, l.290 (`\revblue`, esta ronda) y l.337; contradichos por l.43, l.66, l.225, Ecs. (Z_13)/(Z_17) (l.240-241), `fig:estimulos`, `fig:Modos_Locomocion` y por el propio `results.tex` (l.45, l.128, subtítulos de Figs. de robot físico: "red/blue stimulus-presence shading").
- **Descripción:** el texto dice que `Gpe_B`, `Gpe_G`, `Gpe_R` son los canales "obstacle (Blue), appetitive (Green), aversive (Red)" (l.244) y que el canal aversivo pesa más "compared to the appetitive (green) channel" (l.290). En l.337 dice que `G_{pe,y}` es el canal apetitivo y `G_{pi,x}`, `G_{pi,z}` los de obstáculo y aversivo. Pero (a) `fig:estimulos` muestra el estímulo **apetitivo azul** y el **aversivo rojo**, l.43 dice "red and blue 3D models", y Resultados sombrea "red/blue" como aversivo/apetitivo; (b) l.225 dice que la neurona de parada `X_17` es la del acercamiento apetitivo y su ecuación (Z_17) usa `Gpe_B` con `Ar` = 28 % del campo visual de la cámara, lo que solo tiene sentido si Blue es el apetitivo; (c) l.66 asigna el obstáculo al modo omnidireccional (`X_14` en `fig:Modos_Locomocion`), y la Ec. (Z_14) lo alimenta con `100 G_{pe,y}`, así que `G_{pe,y}` es el canal de **obstáculo**; (d) Resultados l.45 dice que la activación GPe "asociada al obstáculo" dispara `X_4`, y la Ec. (Z_4) de la metodología pone `Gpe_G` ahí.
- **Cómo lo verifiqué:** leí `red_neuronal.py` (PETER_SIMULATION@4ab2c1018c): l.30-32 publica `/Gpe_Hostil` (R), `/Gpe_Obstaculo` (G), `/Gpe_Apetente` (B); l.316-317 comenta "Huye del depredador (Red)... Caza a la presa (Blue)... Evita al obstaculo (Green)"; l.348-358 indexa STN/Gpe como 0 = R, 1 = G, 2 = B; l.380 `z_3 ← Gpe[2]` (apetitivo) y l.395 `z_14 ← 100·Gpe[1]` (obstáculo). Miré `assets/estimulo_apetente.png` (esfera azul) y `estimulo_adversivo.png` (roja). Además se contradice solo con el manuscrito (l.43 y l.225 frente a l.244).
- **Corrección sugerida:** l.244: "...for the appetitive (Blue), obstacle (Green), and aversive (Red) behavioral channels"; l.290: "...compared to the appetitive (blue) channel"; l.337: `G_{pe,y}` es el canal de obstáculo y `G_{pi,x}`, `G_{pi,z}` los de aversivo y apetitivo (confirmar contra `fig:Modos_Locomocion`).

#### D-02. "El robot permaneció en modo H durante los 20 ensayos" es falso: entró en modo omnidireccional en los 20
- **Ubicación:** `results.tex` l.569 ("The robot remained in the wheeled/differential locomotion mode (H) throughout all 20 trials, so no gait-transition stability data applies"); contradice l.535 (`N_ev^X` "counts the resulting omnidirectional-mode switches"), la Tabla `tab:inspection_metrics` (`N_ev^X` mín 1) y el trazo Neural de `fig:mode_timeline_inspection` (X → H).
- **Descripción:** si `N_ev^X` ≥ 1 en todos los ensayos exitosos, el robot pasó por el modo X en todos ellos.
- **Cómo lo verifiqué:** `experiments/R3-05-inspection/data/test_*/inspection_summary.json`: `N_mode_X_events` ≥ 1 en **20 de 20** ensayos (17 exitosos: mín 1, máx 10, media 3.29; los 3 timeouts: 13, 12 y 7). No comprobé si el modo cuadrúpedo (C) se activó alguna vez.
- **Corrección sugerida:** "The robot alternated between the omnidirectional (X) and wheeled/differential (H) modes in every trial" y, si C nunca aparece en `metrics_raw.csv`, mantener la conclusión sobre estabilidad de transiciones solo para C.

#### D-03. "≈2.3× menos en cada uno de los 17 ensayos exitosos, sin excepción" es falso por ensayo
- **Ubicación:** `results.tex` l.567 (`\revblue`, esta ronda).
- **Descripción:** 2.3× es el cociente de medias (7.71 / 3.29). Por ensayo, `N_ev^LiDAR / N_ev^X` va de 1.0 a 5.0 (mediana 2.8). En el ensayo 014 hay 4 detecciones y 4 cambios de modo (ninguna reducción); en el 016, 7 frente a 4 (1.75×) y en el 019, 5 frente a 4 (1.25×). La frase "in every one of the 17 successful trials without exception" no se sostiene.
- **Cómo lo verifiqué:** mismo conjunto que D-02; recomputé `N_lidar_events` y `N_mode_X_events` por ensayo. Los estadísticos de la Tabla 10 sí coinciden (ver "Verificado sin hallazgos").
- **Corrección sugerida:** "on average ≈2.3× fewer (per-trial median 2.8×; in 3 of 17 trials the reduction is below 2×, in one of them there is none)".

#### D-04. "Peor caso ≤ 5.06 J" usa una media como cota superior
- **Ubicación:** `results.tex` l.990 ("its transition energy serves as an upper bound on the cost of any mode transition: in the worst case a transition consumes ≤ 5.06 J") y `fig:MorphologicalEnergy`.
- **Descripción:** 5.06 J es la **media** de Q→D (SD 2.93 J). La transición más cara medida es **15.88 J**; 6 de 35 transiciones superan 5.06 J. La barra de error de la propia figura llega a ≈ 7.9 J, por encima de la "cota". Además las transiciones con modo X (`c→x`, 1 evento, excluido) no se midieron, así que "cualquier transición" no está respaldado. La conclusión cualitativa (coste pequeño frente a ≈ 216 J de un segmento X) se mantiene incluso con 15.88 J.
- **Cómo lo verifiqué:** importé las funciones del builder (`experiments/_plotting/builders/energy_transition.py::find_transitions` e `integrate_energy`) sobre `experiments/real/Test_current_integrated_*/imu_ina.csv`: Q→D N = 16, media 5.06, SD muestral 2.93, mín 3.64, **máx 15.88**; D→Q N = 19, media 4.13, SD 1.19, máx 7.27; t de Welch con SD muestrales = 1.18 (coincide con el texto).
- **Corrección sugerida:** "mean 5.06 J (maximum observed 15.88 J)" y borrar "upper bound / worst case". Detalle menor: el texto usa SD muestral (2.93; 1.19) y las barras de la figura usan SD poblacional (`np.std`: 2.84; 1.16); declararlo o unificarlo (ver D-28).
- **Estado (consolidado):** el autor decidió reescribirlo como media **sin citar el máximo** (A.2, S-01 = B-3 = D-05) y el 15.88 J pasa a la sección C; mi sugerencia de citarlo no va.

#### D-05. Tabla 13: la ventana `T_switch` del apetitivo físico (3.0-9.0 s) no coincide con los datos ni con su ECDF
- **Ubicación:** `results.tex` l.973 (fila Appetitive de `tab:consolidated_physical_metrics`), l.894 y `fig:appetitive_ecdf_real`; subpuntos en las filas Complex y Obstacle (l.975-976).
- **Descripción:** la tabla dice "3.0-9.0 s (mechanically limited)". Los datos dan 0.876, 0.902, 1.349 y 13.200 s: ninguno cae en 3-9 s y la propia ECDF (en ms) abarca ≈ 0.9-13.2 s. El recuento de réplicas (3 o 4) es el tema abierto conocido y no lo reporto. Subpuntos: (i) Complex "≈ 1.0-1.2 s": las réplicas son 0.150, 1.051 y 1.200 s; la de 0.15 s no está en el rango (la ECDF arranca en 150 ms); (ii) Obstacle `Var(z)` "≈ 1100": los máximos por réplica son 1316.5, 683.7 y 687.8 (media 896), y "≈ 27× Obstacle baseline" depende de ese 1100 (picos de Complex: 23 487, 32 860 y 31 843); (iii) la columna se llama "Roll / Pitch RMS" pero contiene rangos de una señal oscilante ("3.0°-3.5° (cyclic)") y el caption dice "attitude range".
- **Cómo lo verifiqué:** apliqué la lógica del builder (`real_plot_suite.py::switching_delay_s`: máximo de `Tswitch` por réplica en `combined_metrics.csv`) a `experiments/real/StimuliB_t01..t04`, `StimuliR_t01..t03`, `StimuliG_t01..t03`, `MultiRGB_t01..t03` (las `MultiRB_*` llevan `DISCARDED.md`), y el máximo de `firing_variance` en `neural_metrics.csv`. Aversive (2.8, 2.4, 0.4 ms) y Obstacle (0.6, 0.4, 0.6 ms) sí coinciden con "≈ 0.0 s".
- **Corrección sugerida:** Appetitive "0.9-13.2 s" (o la mediana y el máximo), Complex "0.15-1.2 s", recalcular el "≈ 1100" y el "27×" desde los picos reales o citar el criterio, y renombrar la columna "Roll / Pitch attitude range".

#### D-06. (Conocido, abierto: `C-75`) El ruido nunca estuvo activo en `experiments/simulation/`
- **Ubicación:** `results.tex` l.152 ("which carried only proportional Gaussian sensor noise"), l.320 ("zero-mean Gaussian noise ... at five levels (σ = 0, 5, 10, 20, and 30%)" y "filtered out the injected sensor noise"), l.504 y el caption de `fig:attempts_vs_noise_level` (l.509, eje "Noise Level"), filas Neural de `tab:fsm_comparison` para Appetitive/Aversive/Obstacle, `methodology.tex` l.439 ("noise levels", "noise-injection model ... unchanged") y los captions de `fig:appetitive_micro`, `aversive_micro`, `obstacle_micro`, `complex_micro` ("three per perturbation level").
- **Descripción:** ya documentado en `intake/pending/C-75_fig20_restore_and_simulation_noise_audit_2026-11-01.md` (mecanismo en el código: los launch de `single_stimulus`/`multiple_stimuli` no declaran `noise_level_idx` y los de terreno no lo reenvían). Aquí lo dejo con evidencia de datos para que la consolidación lo vea: los niveles 0-4 son solo etiquetas.
- **Cómo lo verifiqué:** en los 96 ensayos de `experiments/simulation/`, `final_metrics.noise_idx` = 0 en **96/96**, y en `unified_metrics.csv` la columna `active_noise_level` vale 0.0 como máximo en las 12 961 filas de los ensayos etiquetados con niveles 0, 1, 2, 3 y 4 (`seed_info.noise_level_idx`: 19/18/19/21/19 ensayos). Los 20 ensayos de inspección también registran 0, coherente con "no noise injection" de su caption. El CSV maestro de la FSM anota que los ensayos FSM de terreno corrieron sin ruido ("FSM ignores noise entirely"), coherente con la prosa de l.522 (no independiente de S-15 de Samuel).
- **Corrección sugerida:** pendiente de decisión del dueño tras la comprobación de Sam (línea de arranque "[ROBUSTEZ] Nivel de ruido activo: σ = …%"): o se re-corren con ruido real, o se retiran/reescriben las frases de arriba y se declara el eje de `fig:attempts_vs_noise_level` como réplicas sin ruido. `fig:noise_robustness_grid` (R3-04) es otra tubería y no se ve afectada por lo comprobado aquí.

#### D-07. La Introducción y las Conclusiones dicen que la plataforma integra CPGs, y la Metodología no los describe
- **Ubicación:** `introduction.tex` l.32 ("the present platform integrates central pattern generators (CPGs)" y "BG arbitration above and CPG execution below forms a hierarchical neural stack"); `conclusions.tex` l.6 ("a central pattern generator modulated by stimulus type is sufficient to ensure stable and efficient displacement").
- **Descripción:** en todo el manuscrito las únicas menciones de CPG están en la Introducción (3, contando la Tabla 1) y las Conclusiones (1); Metodología y Resultados tienen 0. La Metodología describe cuatro módulos neuronales (sensorial, ganglios basales, locomoción, decisión de modo) y la ejecución de la marcha como "pre-configured open-loop control patterns" (`results.tex` l.1030) con calendario fijo de patas e interpolación acotada en el firmware (`methodology.tex` l.524-530). Eso no es una red de osciladores acoplados. El módulo de locomoción emite magnitud y dirección de velocidades, no un patrón rítmico.
- **Cómo lo verifiqué:** `grep -c "CPG|central pattern"` en `sections/*.tex` (introduction 3, conclusions 1, resto 0) y lectura de `methodology.tex` §2.3.3 y §2.4.
- **Corrección sugerida:** Introducción: "the quadrupedal gait is executed by a pre-configured open-loop scheduler (Section 2.4), the role CPGs play in other systems"; Conclusiones l.6: sustituir "a central pattern generator modulated by stimulus type" por "the locomotion module". Si los autores consideran que el calendario es un CPG, hay que describirlo en la Metodología.

### Media

#### D-08. Tabla 4 y l.290: las "ganancias de amplificación" son pesos inhibitorios y cinco parámetros de la tabla no están en ninguna ecuación
- **Ubicación:** `methodology.tex` l.259-264 (`table:Locom_NN`), l.290 (`\revblue`, esta ronda), Ecs. (Z_7)-(Z_10) (l.232-235).
- **Descripción:** l.290 dice que "the gains ω_{X4→X7} and ω_{X3→X8} provide sufficient command amplification to overcome robot inertia and produce quick evasive turns". En las ecuaciones esos pesos entran con **signo menos**: `z_7 = (z_5 + z_3 − w z_4)_+`, `z_8 = (z_5 + z_4 − w z_3)_+`, con `w = 10` (Tabla 4, l.268), el mismo valor que ω_{X4→X7} y ω_{X3→X8}. Es inhibición mutua entre canales, no amplificación. Además `ω_{X3→X7}`, `ω_{X4→X7}`, `ω_{X5→X7}`, `ω_{X3→X8}` y `ω_{Gpe→X1}` figuran en la tabla pero no aparecen en ninguna ecuación.
- **Cómo lo verifiqué:** comparé la Tabla 4 con las Ecs. (Z_3)-(Z_17) línea a línea; en el código (`red_neuronal.py` l.386-389) `z_7`...`z_10` usan `- self.w*self.z[...]`, también inhibitorios.
- **Corrección sugerida:** reescribir la tercera frase de l.290 ("the mutual-inhibition weight w = 10 between the stimulus channels (Eqs. Z_7-Z_10) lets the strongest channel suppress the others, which yields quick evasive turns") y quitar de la Tabla 4 esos cinco parámetros, o añadirlos a las ecuaciones.

#### D-09. Varias ecuaciones del manuscrito no coinciden con el código leído (requiere confirmar la revisión usada para los resultados)
- **Ubicación:** `methodology.tex` Ecs. (9), (Z_5)/(Z_6), (Z_13), (Z_15), (Z_16) y `f_{Imu}` (Ecs. Z_0-Z_2, Ec. Naka).
- **Descripción** (manuscrito frente a `red_neuronal.py` @4ab2c1018c):

| Ec. | Manuscrito | Código |
|---|---|---|
| (9) `L_4` | `τ_L` = 10 s, fuga 1 | `τ` = 1 s y fuga 1.1 (l.337); `L_0`-`L_3` sí usan 10 (l.327-330) |
| (Z_5), (Z_6) | `ω L_2 + L_4[θ_s − θ_p − 20]`, con `L_2` en las dos | `160·L_2 + 1[L_4 < 0.3]·(θ_s − θ_p − 20)` y `160·L_3 + 1[L_4 < 0.3]·(θ_p − θ_s − 20)` (l.383-384): `L_4` es un interruptor, no un factor, y Z_6 usa `L_3` |
| (Z_13) | `−w z_11 − w z_12 − w z_17 + HI + Gpe_B` | `−w·|cmd_ang|·z_11 − w·|cmd_ang|·z_12 − 2w·z_17 + cte + Gpe[2]` (l.393) |
| (Z_15) | `−G_{pe,y} − 0.5 HI + 2 z_3 + 20 z_0 − 1.5 w z_14 − w z_16` | `−100 Gpe[1] − cte + w z_4 + 2 z_0 − 1.5 w z_14 − w z_16` (l.396) |
| (Z_16) | `z_4 − w G_{pe,y} − 1.5 w z_14 − 1.5 w z_15 + 0.7 z_1 + 0.7 z_2 + HI` | `z_3 − 100 Gpe[1] − 1.5 w z_14 − 1.5 w z_15 + 5 z_1 + 5 z_2 + cte` (l.397) |
| `f_{Imu}` | `A x_+² / (σ_I² + x_+²)` | `A max(0,x)² / (σ_I² + (x − z_i)²)`: el denominador lleva el estado de la propia neurona (l.377-379). Para `f_{Mode}` sí coincide |

  La Ec. (Z_14) sí coincide. `A`, `w`, `σ_M`, `HI`, `Ar`, `j` y `τ` de las Tablas 2-4 coinciden con las constantes del código (l.116-132).
- **Cómo lo verifiqué:** lectura directa de `red_neuronal.py` l.327-337 y 377-399 frente a las ecuaciones. No sé qué revisión generó los resultados de simulación; el último commit de `main` es del 2026-06-09 y las corridas de inspección son del 2026-08-29.
- **Corrección sugerida:** que Sam o Deivi confirmen si ese `main` es la versión corrida; si lo es, corregir las ecuaciones del manuscrito (o declarar que son una forma simplificada) antes de que un revisor con acceso al código las compare.

#### D-10. Índices mal puestos en las Ecs. (6), (7) y (9), justo bajo un texto nuevo que los describe
- **Ubicación:** `methodology.tex` l.142, l.143, l.145 y el párrafo `\revblue` de l.148.
- **Descripción:** Ec. (6): `dI_n/dt = (−I_n + Z_i)/τ_IRA` usa `Z_i` con un índice libre (debería ser `Z_n`). Ec. (7): `Σ_i W^{(IR)}_{n,i}·A_i` multiplica a la capa auxiliar, pero `W^{(IR)}` es el peso input→response (en el código multiplica la actividad del anillo, l.334). Ec. (9): `Σ_{r=0}^{15} A_n` suma sobre `r` con sumando `A_n`; el párrafo azul de l.148 dice que "`r` in Equation (9) running over all auxiliary units", así que el sumando debe ser `A_r`.
- **Cómo lo verifiqué:** lectura de las ecuaciones y de l.148; código `red_neuronal.py` l.332-337.
- **Corrección sugerida:** `Z_n` en (6), `I_i` o `Z_i` en (7) (según se quiera describir el código) y `A_r` en (9).

#### D-11. Cifras de despliegue del MLP en el ESP32-S3: parámetros, denominador del flash y "casi todo es el modelo"
- **Ubicación:** `results.tex` l.701.
- **Descripción:** (a) "the ∼47k-parameter model": los pesos exportados suman **32 642** parámetros (135·150 + 150 + 150·80 + 80 + 80·2 + 2), y `classifier_fig6.csv` da 32 489 para el MLP; ≈ 46k es la entrada de la SVM-RBF. (b) "397,829 B flash (30.4% of the board's 4 MB partition...)": 397 829 B es el 30.4 % de la **partición de aplicación de 1 310 720 B (1.25 MB)** del informe de compilación, y solo el 9.5 % de los 4 MB. (c) "almost entirely the model itself": 32 642 floats son ≈ 130.6 KB, un tercio de los 397 829 B; el resto es firmware. (d) Mezcla de unidades en una frase: "8.81 ms (SD = 2.67 µs)" (los valores son correctos: 8814.009 µs y SD 2.672 µs).
- **Cómo lo verifiqué:** `experiments/R2-04-mlp-onboard-compute/output/mlp_weights.h` (tamaños de arrays `W1[20250]`, `BIAS1[150]`, `W2[12000]`, `BIAS2[80]`, `W3[160]`, `BIAS3[2]`) y `onboard_compute_results.txt` (informe de compilación y latencia). La nota original del archivo ("~47K float32, ~188KB... matching Section 3.1's ~47K-parameter count") arrastra la misma cifra.
- **Corrección sugerida:** "∼33k-parameter", "30.4% of the 1.25 MB application partition (4 MB flash)", borrar "almost entirely the model itself" y escribir "8.814 ms (SD 2.67 µs)" en una sola unidad.

#### D-12. El símbolo λ designa dos métricas distintas
- **Ubicación:** `results.tex` l.476 y columna λ de `tab:fsm_comparison`, frente a l.1052 (Limitaciones).
- **Descripción:** l.476 define λ como "a motor-command clarity ratio (commanded-velocity magnitude relative to neural activity norm)" y la Tabla 11 lo reporta para los dos controladores. l.1052 habla de "the conflict-efficiency metric λ" que "was excluded from the reported results because its current implementation only registers active conflict when two specific channels are simultaneously present". O es la misma métrica y Limitaciones contradice la Tabla 11, o son dos y comparten símbolo.
- **Cómo lo verifiqué:** lectura de ambos pasajes y de `table_master_comparison.csv`, que lleva `lambda_whole_trial_mean` (el que va en la tabla) y, aparte, `conflict_exposure_pct`/`conflict_exposure_s`.
- **Corrección sugerida:** renombrar una de las dos (por ejemplo `λ_cmd` y `λ_conf`) y aclarar en Limitaciones cuál se excluyó.

#### D-13. "Ningún sustituto más simple lo iguala" (l.217) frente a "aún no concluyente" (l.219)
- **Ubicación:** `results.tex` l.217 (texto base) y l.219 (`\revblue`, esta ronda).
- **Descripción:** l.217 concluye que "no simpler substitute, including the same static-threshold family..., matches it". l.219 dice que esa segunda conclusión "is not yet conclusive" (con 2 fallos de 12, `threshold only` no se distingue del circuito completo en éxito). El `threshold only` sí es más lento (p = 0.014) y tiene más Roll RMS (p = 0.017), pero con `n = 12` las dos frases se leen juntas con grados de certeza distintos.
- **Cómo lo verifiqué:** recomputé los p exactos de Fisher (dos colas) para 12/12 frente a 3/12, 4/12, 10/12 y 11/12: 0.0003, 0.0013, 0.4783 y 1.0000 (coinciden con los captions) y que hacen falta 5 fallos para p < 0.05.
- **Corrección sugerida:** en l.217, "...and the static-threshold substitute is slower and less attitude-stable, although its success rate is not statistically distinguishable at n = 12 (next paragraph)".

#### D-14. La Fig. 28 se cita como respaldo del resultado de Appetitive, pero su caption dice que ese resultado "no se muestra"
- **Ubicación:** `results.tex` l.194 (`\revblue`: "...in the Appetitive Targeting scenario (Figure~\ref{fig:ablation_combined})") frente a l.211 ("Under the no-conflict Appetitive Targeting scenario (not shown), all four variants perform statistically indistinguishably").
- **Descripción:** los paneles (a) y (b) de `fig:ablation_combined` son solo Complex Navigation.
- **Cómo lo verifiqué:** lectura del caption y de los dos subcaptions; vista de `assets/fig_ablation_complex_stability.png` (solo Complex).
- **Corrección sugerida:** quitar la referencia a la figura en l.194 o decir "(not shown)".

#### D-15. Tabla 12: el "≈ 5°" de re-engagement no está definido en ninguna parte y el robot físico no usa un umbral de pitch en grados
- **Ubicación:** `results.tex` l.809 ("pitch exceeds the threshold") y l.811 ("quadrupedal re-engagement threshold (≈ 5°)").
- **Descripción:** la Tabla 4 define `U_Pitch` = 15° para la simulación; en el robot físico `X_1` se alimenta de la salida `N_1` del MLP con umbral `U_{N_1}` = 7.8 (`methodology.tex` l.375, 389-392, Tabla 6), que no está en grados. El 5° no aparece en la Metodología ni en las tablas de parámetros.
- **Cómo lo verifiqué:** `grep` de umbrales en `methodology.tex`; lectura de Tablas 4 y 6.
- **Corrección sugerida:** citar el umbral real (`U_{N_1}` para el robot físico) o declarar de dónde sale el 5° y por qué difiere de los 15° de la Tabla 4.

#### D-16. "150-80 es el mejor compromiso" con diferencias de F1 de 0.005 y SD de CV de 0.033
- **Ubicación:** `results.tex` l.666.
- **Descripción:** 150-80 tiene F1 = 0.771; 100 y 200-100-50 tienen 0.766. La diferencia (0.005) es ≈ 0.15 SD de la validación cruzada (0.033). "confirms that 150-80 represents the most favorable trade-off" va más allá de lo que muestran los datos. Además, "simpler (50, 100) ... topologies" se lee como una red de dos capas 50-100, cuando son dos redes de una capa (50 y 100 unidades).
- **Cómo lo verifiqué:** lectura de l.664-666 (F1 = 0.771 ± 0.033 en CV); no tengo los F1 por pliegue.
- **Corrección sugerida:** "is statistically indistinguishable from the 100-unit and 200-100-50 variants (ΔF1 ≤ 0.005, within one SD) and was retained for its ...", y "single-layer 50- and 100-unit".

#### D-17. Tras C-66, "no sufre bloqueos computacionales" queda sin la frase que lo respaldaba
- **Ubicación:** `results.tex` l.128 (marcado `\revblue` solo en el sujeto "The arbitration network").
- **Descripción:** la versión anterior decía "Every retained trial across all five severity levels resolves this three-stimulus encounter successfully..., evidencing that...". Ahora queda la afirmación suelta. Y ese respaldo era débil: la batería retiene solo ensayos exitosos por construcción (l.57), así que no puede mostrar ausencia de bloqueos. El marcado azul parcial también es un residuo de la consolidación.
- **Cómo lo verifiqué:** `git log -S"evidencing that the arbitration network does not suffer" -- sections/results.tex` da el commit `e6a6b0e` (C-66, 2026-11-01) como el que quitó la frase; lectura de l.57 y l.180.
- **Corrección sugerida:** borrar la frase o limitarla a "in none of the retained trials did the network stall (attempts discarded before retention are analyzed in Section 3.1.5)", y marcar la frase entera como `\revblue`.

#### D-18. Afirmaciones de las Conclusiones y la Introducción sin ninguna medida que las respalde
- **Ubicación:** `conclusions.tex` l.6 (`\revblue`: "trajectories with minimal deviations from the optimal path, maintaining a consistent safety distance"), l.10 ("significantly reduced lateral and longitudinal oscillation amplitudes"), l.12 (`\revblue`: "the latter yields smoother transitions with fewer undesired oscillations"); `introduction.tex` l.34 ("(iii) autonomous energy-aware mode selection").
- **Descripción:** Resultados no reporta desviación de trayectoria óptima ni distancia de seguridad, ni compara amplitudes de oscilación con y sin cambio de modo, ni tiene una variante sin Naka-Rushton. El controlador no usa energía en sus ecuaciones (la energía no se registró en Gazebo, l.470, y l.1014 recomienda minimizar el modo X "a mission controller should"). Las Conclusiones (l.12) reformulan (iii) como "autonomous mode selection that exploits the efficiency of wheeled locomotion", sin "energy-aware", así que ni siquiera coinciden entre sí.
- **Cómo lo verifiqué:** `grep -i "optimal path|safety distance|oscillation amplitude|deviation from|path length|clearance"` en `results.tex`: 0 resultados; lectura completa de Resultados y de las Ecs. de la Metodología.
- **Corrección sugerida:** convertir en descripciones cualitativas ("the trajectories in Figures X-Y show...") o quitar el "significantly"/"minimal"/"energy-aware", y alinear (iii) entre Introducción y Conclusiones.

#### D-19. La Introducción describe un MLP que alimenta al circuito de ganglios basales; en la Metodología alimenta a la decisión de modo
- **Ubicación:** `introduction.tex` l.34 ("A multilayer perceptron (MLP) processes sensory data to detect terrain instability and compute per-channel salience inputs to the basal-ganglia network, which in turn executes mode selection via a WTA disinhibition mechanism").
- **Descripción:** en la Metodología el MLP produce `N_0`, `N_1`, `N_2` (plano/inclinado/atascado) que entran a `X_0`/`X_1` del módulo de decisión de modo (l.375-392); las entradas del circuito de ganglios basales son `Stimuli_i` de visión (y L_4 del LiDAR). El MLP no calcula saliencias por canal.
- **Cómo lo verifiqué:** lectura de `methodology.tex` §2.3.2 y §2.3.4 y `fig:Modos_LocomocionV2`.
- **Corrección sugerida:** "...an MLP processes inertial data to classify terrain (flat/inclined/stuck); its outputs drive the gait-decision units, while the basal-ganglia network arbitrates among the visual and LiDAR stimulus channels".

#### D-20. La declaración de uso de IA nombra solo ChatGPT y "refinamiento lingüístico", y la ronda se trabajó también con agentes de código (decisión de los autores)
- **Ubicación:** `conclusions.tex` l.38-40.
- **Descripción:** la declaración dice que se usó ChatGPT (OpenAI) "solely for linguistic and stylistic refinement" y no para "results, data, analyses, or conclusions". El repositorio documenta que los colaboradores dirigen agentes de IA (Claude Code, de Anthropic) para parchar `sections/*.tex`, redactar texto nuevo de esta ronda (los bloques `\revblue`), recomputar tablas desde los logs y auditar. No es un error del manuscrito, pero la política de la editorial pide que la declaración refleje el uso real.
- **Cómo lo verifiqué:** `CLAUDE.md` (flujo de colaboradores) y `git log --grep "Co-Authored-By: Claude"`: 241 commits con ese trailer (174 de Deivs117, 48 de Sebas, 17 de Sam, 1 de David Caicedo y 1 de Diego).
- **Corrección sugerida:** decisión de los autores. Si se mantiene la declaración, que alguien confirme que sigue siendo cierta; si se amplía, nombrar las herramientas y el alcance (redacción y revisión de texto, verificación numérica).

### Baja

#### D-21. "Sub-milisegundo en la gran mayoría de los ensayos" no vale para la pendiente
- **Ubicación:** `results.tex` l.320 ("likewise sub-millisecond in the vast majority of trials") y `fig:decision_delay` (B).
- **Descripción:** en terreno rugoso, 13 de 15 ensayos están en 0.2-0.7 ms y 2 tienen cola de ≈ 0.6 s. En la pendiente, `T_switch` = 0.9 (×3), 1.0 (×8), 1.1 (×2), 1.3 y 1.8 ms: solo 3 de 15 son < 1 ms. En total 16 de 30 (53 %) son sub-milisegundo.
- **Cómo lo verifiqué:** `experiments/simulation/familia_c1_terreno_rugoso` y `familia_c2_pendiente` (`trial_summary.json: final_metrics.tswitch`): los valores de arriba; `T_response` = 0.0 en los 30; medias de Roll/Pitch 1.586/1.666 (rugoso) y 1.469/2.290 (pendiente), todas coinciden con el texto.
- **Corrección sugerida:** "sub-millisecond in 16 of the 30 trials (13 of 15 on rugged terrain, 3 of 15 on the slope, where it spans 0.9-1.8 ms)".

#### D-22. La prosa de la Fig. 36 no coincide con el dato en dónde ocurren los reintentos
- **Ubicación:** `results.tex` l.504 ("up to 1.67× ... in Appetitive ... at the noisiest levels tested") y caption l.509 ("an occasional retry at intermediate/high noise").
- **Descripción:** los intentos por misión de Appetitive/Neural son 1.33, 1.0, 1.33, 1.67 y 1.0 en los niveles 0-4: el máximo está en el nivel 3 (no en el más ruidoso), y el nivel 0 (sin ruido) ya necesita reintentos. Aversive (1.0, 1.0, 1.0, 1.33, 1.33) sí encaja. Esto se suma a D-06: con `noise_idx` = 0 en todos los ensayos, las diferencias entre niveles son variación de muestreo, como el propio caption dice.
- **Cómo lo verifiqué:** contado desde `experiments/simulation/familia_a_*` (`seed_info.noise_level_idx` y veredicto): coinciden exactamente con la figura.
- **Corrección sugerida:** "Neural needs up to 1.67× as many attempts in Appetitive (level 3; 1.33× already at level 0) and 1.33× in Aversive (levels 3-4)".

#### D-23. "Unas 30 veces" es 27 veces
- **Ubicación:** `results.tex` l.513 ("≈ 0.2 s/trial ... against ≈ 6.1 s/trial, roughly 30× longer").
- **Descripción:** 6.134 / 0.2267 = 27.06. El 30 sale de dividir los valores ya redondeados (6.1 / 0.2).
- **Cómo lo verifiqué:** `table_master_comparison.csv` (`conflict_exposure_s`: 0.2267 Neural, 6.1335 FSM; `conflict_exposure_pct`: 1.67 % y 4.73 %, que los porcentajes del texto reproducen).
- **Corrección sugerida:** "roughly 27× longer".

#### D-24. "La gran mayoría" (Fig. 27) frente a "ella sola" (l.180) para las volcaduras y choques de Rugged Terrain
- **Ubicación:** `results.tex` l.176 ("accounts for the large majority of non-timeout failures (8 tipovers, 4 crashes out of 27 attempts)") y l.180 ("the Rugged Terrain suite alone accounts for the tipovers and crashes").
- **Descripción:** una frase admite fallos no-timeout en otras suites y la otra dice que Rugged Terrain es la única. Requiere verificación con datos no versionados (`R3-04-noise-robustness/data/`). Los 8 + 4 de 27 los vio también Samuel (no independiente).
- **Cómo lo verifiqué:** solo lectura cruzada de las dos frases.
- **Corrección sugerida:** igualar a "the large majority" o "alone", según el dato.

#### D-25. Las entradas del MLP se describen de dos maneras (l.339 frente a l.348)
- **Ubicación:** `methodology.tex` l.339 frente a l.348-373.
- **Descripción:** l.339 dice que el MLP procesa "variations in roll, pitch, and the standard deviation of the Z-axis acceleration"; l.348 dice que el vector son aceleraciones lineales x/y/z, angulares x/y, tres bits de dirección y un bit de modo (9 × 15 = 135). `σ_az` no es una entrada explícita.
- **Cómo lo verifiqué:** lectura de ambos párrafos, de `fig:DATOSMLP` y de `INPUT_SIZE 135` en `mlp_weights.h`.
- **Corrección sugerida:** en l.339 decir "raw inertial telemetry (linear and angular accelerations)" o aclarar que `σ_az` es una característica derivada.

#### D-26. La marcha "crawl" se remite a una sección que no la describe
- **Ubicación:** `methodology.tex` l.526 ("The crawl gait described in Section~\ref{ssec:Gait_Decision_Module}").
- **Descripción:** `ssec:Gait_Decision_Module` (§2.3.4) trata las neuronas de decisión de modo y el MLP; "crawl" aparece una sola vez en toda la Metodología (esa frase). La marcha de seis fases está en `sssec:transition_stability` (Resultados).
- **Cómo lo verifiqué:** `grep -c crawl` en `methodology.tex` (1) y lectura de §2.3.4; `results.tex` l.331-344 describe las seis fases.
- **Corrección sugerida:** apuntar a `sssec:transition_stability`.

#### D-27. "Ruido gaussiano ... ya usado en la formulación sensorial de obstáculos" no coincide con la Metodología
- **Ubicación:** `methodology.tex` l.417 ("Gaussian noise proportional to each sensor reading's measured range, already used elsewhere in this section's obstacle-sensory formulation").
- **Descripción:** el único gaussiano de §2.3.1 es la curva de sintonía de las neuronas del anillo (Ec. 1), no un modelo de ruido.
- **Cómo lo verifiqué:** lectura de §2.3.1 y de l.417.
- **Corrección sugerida:** borrar "already used elsewhere..." o citar dónde se usa ruido en el código.

#### D-28. Convención de SD sin declarar en la energía y en la Fig. 38
- **Ubicación:** `results.tex` l.986/990 (energía: texto ±2.93, ±1.19 = SD muestral; barras de la figura = SD poblacional 2.84, 1.16) y l.563 (`fig:inspection_dfinal_scatter`: 1.081 ± 0.042, 1.065 ± 0.022 son SD muestrales, sin decirlo).
- **Descripción:** C-74 declaró la convención de las Tablas 9, 10 y 11, pero no la de estos dos captions.
- **Cómo lo verifiqué:** recomputé ambas SD en cada caso (ver D-04 y D-02/D-03).
- **Corrección sugerida:** añadir "(sample SD)" a ambos captions y unificar las barras de la figura de energía.

#### D-29. El encabezado del resumen gráfico dice "outperforms" y los resultados son mixtos
- **Ubicación:** `assets/GRAPHICAL_ABSTRACT.pdf`, panel "FSM baseline & inspection": "Neural arbitration outperforms a priority-rule FSM baseline".
- **Descripción:** el panel solo muestra los dos casos donde gana Neural (conflicto de tres estímulos, inspección). La Tabla 11 da a la FSM más rápida en Aversive y Obstacle (8.32 frente a 9.98 s; 12.44 frente a 15.72 s), sin reintentos, y a Neural peor por intento en las suites de un estímulo (78.9 % y 88.2 % por intento). El abstract y los highlights están bien acotados; solo el encabezado generaliza. Los números del panel (100/0 %, 85/45 %, 25/33/83 %, p) coinciden con el texto.
- **Cómo lo verifiqué:** vista del PDF y comparación con `table_master_comparison.csv`.
- **Corrección sugerida:** "Neural arbitration outperforms the FSM under stimulus conflict and in inspection".

## 1.2 Redundancia y contenido duplicado

### D-30. `τ_Z` y `σ_Z` se explican dos veces, la segunda en texto nuevo de esta ronda — **Baja**
- **Ubicación:** `methodology.tex` l.109 y l.131-132.
- **Descripción:** l.109 ya define `τ_Z` y `σ_Z`. l.131 vuelve a decir "τ_Z (s) governs the ring neurons (Equation (1))" y l.132 (`\revblue`) "σ_Z is the tuning width defined with Equation (1)". Redundancia entre texto viejo y nuevo.
- **Corrección sugerida:** borrar esos dos fragmentos azules y dejar `τ_L`, `τ_IRA` y los pesos.

### D-31. La justificación de `σ_M`/`σ_I` está en l.292 y otra vez en l.316 — **Baja**
- **Ubicación:** `methodology.tex` l.292 (texto base) y l.316 (`\revblue`).
- **Descripción:** l.292: "σ_M provides rapid mode switching through a narrow saturation range, while σ_I affords greater noise tolerance in the IMU pathway"; l.316: "different half-saturation constants match the dynamic range of the IMU and mode-selection pathways". Dicen lo mismo, y l.286 (azul) ya remite a la Ec. (26).
- **Corrección sugerida:** dejar l.292 (tiene los valores) y acortar l.316 a la definición de `f_{Imu}` y `f_{Mode}`.

### D-32. La definición del rectificador `(·)_+` estaba repetida: **resuelto, C-82 ya está en `main` (PR #38)**, sin acción
- Se anota para que la consolidación no lo cuente como hallazgo nuevo: `methodology.tex` l.135, l.310 y l.314.

### D-33. Las cuatro filas Neural de la Tabla 11 repiten `T_sim` y Roll de la Tabla 9 — **Media**
- **Ubicación:** `results.tex` l.130-147 (`tab:consolidated_simulation_metrics`) y l.486-492 (`tab:fsm_comparison`).
- **Descripción:** para Appetitive, Aversive, Obstacle y Complex los valores de tiempo y Roll coinciden (38.52 ± 1.20 / 0.54 ± 0.01 frente a 38.52 ± 1.20 / 0.536 ± 0.009, etc.), y l.130 y l.524 ya lo dicen. Lo único propio de la Tabla 9 es la columna Pitch.
- **Cómo lo verifiqué:** recomputé ambas tablas desde `experiments/simulation/` y `table_master_comparison.csv`: las dos coinciden entre sí y con los datos.
- **Corrección sugerida:** ver D-40.

### D-34. Los dos últimos párrafos de l.215 repiten el caption (b) de la Fig. 28 — **Media**
- **Ubicación:** `results.tex` l.215 (desde "Roll RMS increases significantly for all three ablations..." hasta el final, `\revblue`) y l.211 caption (b).
- **Descripción:** el caption ya dice, con las cifras, que Roll RMS sube para las tres ablaciones y que Pitch RMS baja para dos "plausibly reflecting reduced net locomotor activity in trials that fail outright". El párrafo lo repite casi palabra por palabra sin cifras. C-60 recortó otros solapes, pero este quedó.
- **Corrección sugerida:** borrar esas dos frases del párrafo (la latencia, que no está en el caption, se queda).

### D-35. La Fig. 20 se cita dos veces en la misma oración — **Baja**
- **Ubicación:** `results.tex` l.73: "**Appetitive Targeting (see Figure 20):** ... (Section 2.3.5) (see Figure 20 for the per-level ...)".
- **Descripción:** además, `fig:appetitive_micro` (Fig. 21) no se cita en ningún párrafo (el xref automático lo confirma: 0 referencias), a diferencia de las micro-figuras de Aversive, Obstacle y Complex, que sí se citan en su párrafo.
- **Cómo lo verifiqué:** script de referencias cruzadas sobre `sections/*.tex` (157 etiquetas, 0 duplicadas, 0 referencias rotas; solo `fig:appetitive_micro` queda sin cita entre las figuras completas).
- **Corrección sugerida:** "(see Figures 20 and 21)" en l.73, sin la segunda cita.

### D-36. El aviso de inyección conjunta y de ruido blanco IMU = 0 está en ocho sitios — **Baja**
- **Ubicación:** `methodology.tex` l.417 y l.434; `results.tex` l.62 (Fig. 20), l.73, l.152, l.176 (Fig. 27) y l.1050 (dos veces).
- **Descripción:** R2b-02 y R3b-03 piden el aviso en el texto principal y en el caption, así que al menos Fig. 20 + l.73 + §2.3.5 son obligatorios. El de la Fig. 27 y el de Limitaciones son repeticiones del mismo aviso.
- **Corrección sugerida:** si hay que acortar, dejar Fig. 20, l.73, §2.3.5 y una sola frase en Limitaciones.

### D-37. Los tres subcaptions de la Fig. 31 repiten cifras del texto — **Baja**
- **Ubicación:** `results.tex` l.296, l.303, l.310 frente a l.317-322.
- **Descripción:** "No trial violated this limit across all 30 runs", "long tail to ≈ 0.6 s in 2/15", "Pitch RMS midpoint ≈ 1.98°" están en el subcaption y otra vez en la prosa.
- **Corrección sugerida:** recortar los subcaptions a una línea cada uno.

## 1.3 Candidatos a acortar

Propuestas concretas, sin perder validez estadística ni capacidad de comunicar:

| ID | Qué | Cómo | Ahorro estimado | Prioridad |
|---|---|---|---|---|
| D-38 | Tablas 2 y 3 (`table:LiDAR`, `table:Ganglia`; `methodology.tex` l.111-129, l.174-192) | Sustituir por dos frases: "τ_Z = 1, τ_L = 10, τ_IRA = 5 s; σ_Z = 0.06; all weights ω, W = 1.0" y "τ_Gpi = 1, τ_Gpe = τ_STN = τ_STR = 2 s; all ω = 1.0". 14 de sus 20 filas valen 1.0 | 2 flotantes, ≈ 25 líneas | Baja |
| D-39 | Tabla 5 (`table:DIR_BINARY`, l.350-364) | Una frase con los cinco códigos de 3 bits ("000 static, 001 forward, 010 left, 011 right, 100 backward") | 1 flotante | Baja |
| D-40 | Tabla 9 (`tab:consolidated_simulation_metrics`) | Quitarla y añadir la columna Pitch RMS (y la nota n = 15/14) a la Tabla 11 o a su caption; l.130, l.455-460 y l.524 se simplifican. Conserva toda la información (`T_sim` y Roll ya están en la Tabla 11) | 1 tabla, ≈ 3 frases | Media |
| D-41 | Figs. 21-24 (micro-dinámica de los cuatro escenarios, cada una a 0.75 de ancho de texto) | Una figura 2 × 2 con subcaptions de una línea y un caption común ("first trial by index of the suite's N = 15; Simulation data") | 3 captions, ≈ 1 página | Baja |
| D-42 | Caption de la Tabla 11 (≈ 330 palabras, l.480) | Mover a la prosa la definición de N y la explicación de la media Inclined Slope/Neural; dejar en el caption el aviso de equidad y la fuente. ver D-69 | ≈ 15 líneas | Media |
| D-43 | Caption de la Fig. 28 (≈ 290 palabras, l.211) | Quitar las cifras que ya están en el texto de l.194 y l.215 y los p repetidos | ≈ 8 líneas | Baja |

## 1.4 Ortografía y convenciones académicas

| ID | Ubicación | Problema | Corrección | Prioridad |
|---|---|---|---|---|
| D-44 | `preamble.tex` l.65-72 frente a `conclusions.tex` l.26-32 | Los nombres de los autores no coinciden: "Carlos-Rodríguez"/"Carlos Rodriguez", "Caro-Vaca"/"Caro Vaca", "Caicedo-Samboní"/"Caicedo Samboni", "Grajales-Pulgarín"/"Grajales Pulgarín", "Sebastián"/"Sebastian", "Ramírez-Moreno"/"Ramirez-Moreno", y el orden difiere (portada: Caicedo 3.º y Grajales 4.º; contribuciones al revés) | Un solo formato y un solo orden en los dos sitios | Media |
| D-45 | `results.tex` l.455-457 | "Figures 33 and Table 9" (se ve en el PDF): `\ref{fig:variable_topo_metrics}` es una figura | "Figure~\ref{...} and Table~\ref{...}" | Baja |
| D-46 | `introduction.tex` l.32 (tres veces) | "GPR" sin definir; en un artículo de inspección se lee como radar de penetración del suelo | Expandir en el primer uso ("Gurney-Prescott-Redgrave (GPR) model") | Media |
| D-47 | `methodology.tex` l.76, l.131, l.135; `results.tex` l.36 | Las mismas neuronas `L_0`-`L_4` se llaman "tank neurons", "directional integrator neurons" y "accumulator neuron", y Resultados dice "the sensory ring, whose unit L_4" (L_4 no es del anillo) | Un solo término ("integrator neurons", `L_4` "accumulator") | Baja |
| D-48 | `methodology.tex` l.231, l.244 frente a l.326, l.337 | Dos notaciones para lo mismo: `Gpe_{B,G,R}` y `G_{pe,y}`, `G_{pi,x}` | Unificar (ver D-01) | Baja |
| D-49 | `results.tex` l.192-219 y `fig_ablation_complex_stability.png` | La misma condición se llama "intact circuit" (10), "full circuit" (2), "full" y "Full (control)" en la figura | Un solo nombre | Baja |
| D-50 | `methodology.tex` l.248, l.402 | Captions "Arbitration of locomotion modes Networks parameters" y "...with MLP Network parameters" (mayúscula intermedia y gramática) frente a "LiDAR network hyperparameters" | "Parameters of the locomotion-mode arbitration network (with MLP)" | Baja |
| D-51 | `methodology.tex` l.198 | "Eqs.~" una vez frente a "Equations~" 16 veces | Unificar | Baja |
| D-52 | `methodology.tex` l.339; `results.tex` l.275 | "Z-axis" frente a "Z axis" | Unificar | Baja |
| D-53 | `results.tex` l.1025, l.1050 | "basal ganglia loop/module" sin guion frente a "basal-ganglia" (32 usos como adjetivo) | Guion | Baja |
| D-54 | `methodology.tex` l.4 | La lista de cuatro etapas remite a sección en tres y no en la del control neuronal | Añadir `(Section~\ref{...})` | Baja |
| D-55 | `methodology.tex` l.266 (Tabla 4) | `θ_p` = 90.0 se describe como "initial platform heading" pero en las Ecs. (Z_5)/(Z_6) y l.204 es la orientación instantánea | "initial value of θ_p" | Baja |
| D-56 | `assets/fig_classifier_tradeoff_fused.png` | Eje "Inference time (us/sample)" | µs | Baja |
| D-57 | `results.tex` l.713 | "1.2cm" sin espacio frente a "30 cm" | "1.2~cm" | Baja |
| D-58 | `assets/fig1_noise_robustness_grid.png` y Fig. 27 | Barras ±1σ con n = 3 que cruzan cero en cantidades no negativas (latencias): p. ej. `T_switch` de Appetitive llega a ≈ −50 ms | Barras mín-máx o recortar en 0 | Baja |
| D-59 | `results.tex` l.753 | "gait-decision network ... (Figure, Locomotion Module panel)": la detección de la pendiente está en el grupo de decisión de modo, no en el de locomoción | "Gait Decision Module group" | Baja |
| D-60 | `results.tex` l.558 | "close to one detection per capsule" con 4-7 detecciones para 3 cápsulas | "1.3-2.3 detections per capsule" | Baja |

Los highlights cumplen Elsevier (5 viñetas, 80-84 caracteres cada una), las citas cruzadas están completas (0 etiquetas duplicadas, 0 referencias rotas) y la numeración compilada coincide con la que citan el profe y los revisores (Ecs. (2)-(9) y (26), Tabla 4, Tablas 9 y 11).

## 1.5 Calcos del español e inglés no idiomático

| ID | Ubicación | Texto | Problema | Corrección |
|---|---|---|---|---|
| D-61 | `methodology.tex` l.76 | "used by the tank neurons of the integrator stage" | calco de "neuronas tanque" | "the integrator neurons" |
| D-62 | `methodology.tex` l.43 | "emulating the embedded knowledge required for detecting anomalies" | calco de "conocimiento embebido" | "emulating the prior knowledge..." |
| D-63 | `results.tex` l.522 | "the team that ran the FSM terrain trials identified three configuration differences" | proceso interno del equipo; en un artículo son "we" | "the FSM terrain trials revealed..." |
| D-64 | `results.tex` l.180 | "(counts in the Figure~\ref{...} caption)" | artículo + número ("el pie de la Figura") | "(counts in the caption of Figure~\ref{...})" |
| D-65 | `methodology.tex` l.225; `results.tex` l.240 | "It is important to emphasize that..." / "It is important to highlight the neural responses..." | muletilla ("es importante destacar") | borrar y empezar por el hecho |
| D-66 | `conclusions.tex` l.10 | "produces variant transient states" | "variante" por "variable" | "variable transient states" |
| D-67 | `methodology.tex` l.480 | "tests were performed in an enclosed facility under controlled lighting conditions, used to calibrate the color filters" | modificador colgante | "...conditions, which were also used to calibrate the color filters" |
| D-68 | `results.tex` l.666 | "simpler (50, 100) and deeper (200, 100, 50) topologies" | ambigüedad (ver D-16) | "single-layer 50- and 100-unit and deeper 200-100-50 topologies" |

Los falsos amigos habituales (`actually`, `eventually`, `realize`, `library`) aparecen en usos correctos ("what the task actually requires", "eventually complete", "software libraries"). No encontré `permit to`, `in base to`, `the same` como pronombre ni "presents a behavior".

## 1.6 Texto tocado en las últimas 48 horas

### D-69. La Tabla 11 pierde sus últimas filas en el PDF compilado — **Alta**
- **Ubicación:** `results.tex` l.478-502 (`tab:fsm_comparison`, página impresa 56).
- **Descripción:** la tabla no cabe en una página (LaTeX avisa "Float too large for page by 398 pt") y las seis filas de Inspection, Rugged Terrain e Inclined Slope **no aparecen en ningún lugar del PDF** (la de Complex/FSM queda en el borde de la página). Son las filas del aviso de equidad de R2.3 y del 85 % frente a 45 % del abstract. Ya desbordaba antes de R2.3 (290 pt en la compilación previa); con el caption de R2.3 fue 386 pt y con la frase de SD de C-74, 398 pt (tres compilaciones). No es un tema de colocación de figura: el contenido se pierde.
- **Cómo lo verifiqué:** compilé `main` (4 pasadas); `pdftotext` del PDF completo no contiene ninguno de los valores 51.61, 55.13, 54.94, 55.42, 77.02, 64.53, 6.751 ni 5.430, que sí aparecen en la fuente; la página impresa 56 termina en Complex/FSM con el número de página pisando la tabla. Probé en el scratchpad una variante solo de formato (`\small`, `\setlength{\tabcolsep}{4pt}`, `tabular{l l c c c c c}` en vez de `tabularx`) con las 14 filas y el caption completo: cabe en la página sin cambiar ningún valor ni texto.
- **Corrección sugerida:** esa variante de formato (una línea por fila) y, de paso, D-42 (acortar el caption). Debe hacerla el autor de la tabla o el dueño; no la apliqué por ser una auditoría.

### D-70. El pie de la Fig. 43 queda pisado por el número de página — **Media**
- **Ubicación:** `results.tex` l.624-655 (`fig:robot-6frames`).
- **Descripción:** "Float too large for page by 52 pt": el pie sale sobre el número de página ("...Four representative frames from the [93] real-robot experiment..."). Otros dos flotantes se pasan por poco (el resumen gráfico, 5 pt; `fig:transition_phases`, 1.7 pt).
- **Cómo lo verifiqué:** renderizado de la página 95 del PDF y aviso de LaTeX (52 pt).
- **Corrección sugerida:** reducir el ancho de las cuatro imágenes (p. ej. 0.45 de línea en lugar de 0.48) o dejar un 8 % menos de alto.

### D-71. El pie de la figura de energía (C-72) está recortado por los dos lados — **Media**
- **Estado:** **resuelto por C-89 (PR #41, `energy_transition.py`)**: la nota ahora va en dos líneas completas (lo comprobé en el PNG nuevo). Queda el registro por trazabilidad.
- **Ubicación:** `assets/FigReal_Morphological_Transition_Energy.png` (generado por `energy_transition.py`, `fig.text(0.5, 0.01, ..., fontsize=9)`).
- **Descripción:** la nota inferior se lee "...ver = |current| x 7.2 V (NiMH pack voltage); N = detected mode transitions, not an inferred p...": faltan el principio ("Po") y el final ("eak"). C-72 subió el cuerpo de 7 a 9 pt sin comprobar que la frase cabe en un lienzo de 6 pulgadas.
- **Cómo lo verifiqué:** recorté el borde inferior del PNG a resolución nativa (1800 × 1500).
- **Corrección sugerida:** partir la nota en dos líneas o acortarla ("Power = |current| × 7.2 V; N = detected transitions"); lo hace quien regenere con el builder.

### D-72. `NEU_IMU` y `NEU_IMU2` (simulación) siguen con etiquetas apretadas y "a)/b)" gigantes, y sus gemelas físicas no — **Media**
- **Ubicación:** `assets/NEU_IMU.png`, `assets/NEU_IMU2.png` frente a `NEU_IMU_real.png`, `NEU_IMU2_real.png` (`results.tex` l.233, l.244, l.766-772).
- **Descripción:** en las de simulación las marcas del eje y (`X3`...`X13`, `X0`...`X4`) se montan unas sobre otras y las letras "a)" y "b)" van en un cuerpo varias veces mayor que el resto, mientras las físicas tienen marcas legibles y sin letras (su caption dice "top group/bottom group"). C-70 unificó el tipo de letra pero no esto. A 0.4-0.5 del ancho de texto las marcas de las de simulación no se leerán.
- **Cómo lo verifiqué:** hoja de contacto de las 25 figuras regeneradas (C-70 a C-72 y C-75).
- **Corrección sugerida:** regenerar con la altura de eje de las físicas y quitar las letras (o ponerlas al cuerpo de la figura).

### D-73. La Fig. 20 restaurada (C-75) lleva "R3-04 dataset" en el título — **Media**
- **Ubicación:** `assets/fig1_noise_robustness_grid.png`, título: "Multisensor Noise-Robustness Battery — 4 Scenarios x 4 Metrics (simulation, **R3-04 dataset**, N=15 trials/scenario)".
- **Descripción:** es nomenclatura interna que C-68 quitó del texto visible ("it is our bookkeeping, not the paper's vocabulary"); la imagen restaurada la recuperó. Además usa "x" por "×".
- **Cómo lo verifiqué:** vista de la figura a resolución completa (3900 × 3300).
- **Corrección sugerida:** regenerar con `noise_sweep_grid.py` y un título sin "R3-04 dataset" (requiere los datos no versionados de R3-04, o sea, el dueño).

### D-74. Dos detalles de figuras regeneradas — **Baja**
- `assets/Complex_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png`: la curva de `Var(z)` cruza la leyenda ("Aversive stimulus in view") en el primer pico; C-72 declaraba arreglar "las últimas oclusiones".
- `assets/fig_stability_phases.png`: la leyenda dice "CoM (base_link)", un nombre de marco ROS, justo el tipo de jerga que C-72 sacó de otras imágenes.

### C-76 (63 em dashes): sin hallazgos de puntuación
- Escaneé las seis secciones: 0 `—` (U+2014), 0 `---` fuera de la plantilla, 0 puntuaciones dobles (`,,` `;;` `:.` `,.`), 0 espacios antes de coma o punto, 0 paréntesis vacíos y 0 oraciones que empiecen en minúscula tras un punto. Al leer `methodology.tex` y `results.tex` completos no encontré frases ambiguas ni con el sentido cambiado. Lo que sí quedó del tramo C-66/C-67 está en D-17 y D-34.

## Sin poder verificar

- **Ablación (R3-01):** `experiments/R3-01-basal-ganglia-ablation/` solo tiene README, así que no pude recomputar latencias (75.9, 81.7, 66.6, 109.1 ms y sus IC), Roll/Pitch RMS ni los p de Mann-Whitney. Verifiqué los p de Fisher desde los conteos (D-13).
- **Baterías R3-04** (`R3-04-noise-robustness/data/`, no versionado): los valores por nivel de `fig:noise_robustness_grid`, los de `fig:noise_robustness_extra_combined` (8 volcaduras y 4 choques de 27 intentos, bandas de Roll/Pitch: no independiente, ya en la lista de Samuel) y D-24.
- **Latencias de terreno reales (15 réplicas):** `terrain_latencies.csv` es una vectorización de la figura con 8-12 puntos por panel, así que no confirma N = 15; las medias (0.185, 0.535, 2.94 y 1.57 s) sí se acercan a los 0.184, 0.534, 2.92 y 1.56 s del texto.
- **Perfil TR de la Fig. 31A** (μ_TR 0.600 y 0.593, pico 0.77), la frase "No trial violated this limit across all 30 runs" (l.296) y los **estadísticos de la Tabla 10** (`tab:crawl_stability`, N = 268): los datos versionados de los 30 ensayos solo traen `final_metrics.tr` (0.0, 0.5797 y 0.6049), sin la serie por ensayo, así que no puedo recomputar el máximo de TR. La fila `C-80` menciona "TR > 1 en 2 ensayos" (A-3): no lo verifiqué. Para la Tabla 10 no localicé la fuente por ensayo; la identidad `TR = 1 − SM_norm` de esa tabla sí se cumple (0.439 = 1 − 0.561; máx 1.173 = 1 + 0.173).
- **Revisión del código** usada en los resultados (D-09) y **línea base del sketch vacío** del ESP32-S3 (D-11).
- **`Var(z)` "≈ 1100" y "27×"** de la Tabla 13 (D-05): no sé de qué réplica o criterio salen.

## Verificado sin hallazgos

- Tabla 9: las 24 cifras coinciden con los 90 ensayos exitosos de `experiments/simulation/` (SD poblacional; Obstacle con n = 14 sin `test_007`, Roll = 37.3°).
- Tabla 11: las 14 filas (N, SR, tiempo, Roll RMS, λ) coinciden con `table_master_comparison.csv`; exposición a conflicto 0.2267 s (1.67 %) y 6.134 s (4.73 %).
- Tabla 10 (inspección): las 5 filas, los grupos limpio/elevado (n = 12 y n = 5, `d_final` 1.081 ± 0.042 y 1.065 ± 0.022 con SD muestral), los timeouts (ensayos 7, 11 y 17 con N_LiDAR = 18, 27 y 33) y que todos los ensayos tienen `T_acquisition`.
- Batería de terreno variable: `T_response` = 0.0 en los 30, 13/15 en 0.2-0.7 ms y 2 con cola de 0.6 s en rugoso, escalera de 5 valores (0.9-1.8 ms) en pendiente, y las cuatro medias de Roll/Pitch.
- Tabla 14 (`mode_energy_stats.csv`): 2.73 ± 2.29 W (N = 20 segmentos, 1873 muestras), 1.13 ± 1.08 W (20; 3297) y 5.71 ± 0.73 W (1; 194); t de Welch 1.18; 5.71 × 38 s = 217 J.
- MLP en ESP32-S3: media 8814.009 µs, SD 2.672 µs, RAM 24 140 B (7.4 % de 320 KiB).
- Ablación: p de Fisher de los captions (0.0003, 0.0013, 0.4783, 1.0) y la frontera de 5 fallos.
- Fig. 36 (Neural): los intentos por misión de los tres paneles coinciden con los datos (ver D-22 para la prosa).
- Resumen gráfico, abstract y highlights frente a Tabla 11 y Fig. 28.
- Referencias cruzadas y numeración (ver 1.4).

## Descartado por el brief (sección 3), visto y no reportado

En dash `--`, nombres internos dentro de `\label`/`\ref`/`\includegraphics`, los 15 `---` de `preamble.tex`, el PDF de 36 MB, las dos baterías de terreno citadas por separado (C-69), la SD poblacional declarada (C-74) y el Appetitive físico con tres frente a cuatro réplicas (abierto; solo cito la cifra en D-05 por otro motivo). El desbordamiento de la Tabla 11 (D-69) no es "tamaño o ubicación de la figura": se pierden filas del PDF.
