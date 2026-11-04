# Auditoría final R2 — parte Deivi (C-77), enfoque 1.1 Datos y números (prefijo D-)

Fecha: 2026-11-03. Pasada de hallazgos: no se editó nada del repo.
Lectura: `results.tex` completo primero, después `methodology.tex`, `introduction.tex`, `conclusions.tex`, `closing.tex` y el abstract/highlights de `preamble.tex`. Las auditorías de Sam (`final_audit_r2_samuel_2026-11-03.md`, IDs S-xx) y de Sebas (`final_audit_r2_sebas_2026-11-03.md`, IDs A-/M-/B-/N-xx) las leí **después** de recomputar.

Los datos se leyeron con `python3 -I` o con `experiments/.venv_plotting/bin/python -I`, y los scripts auxiliares están en el scratchpad. En esta máquina **sí están** `experiments/R3-04-noise-robustness/data/` y `experiments/R2-02-fsm-baseline/data/`, así que también se recomputó lo que sale de ahí.

## Resumen

| Prioridad | Total | Nuevos | Coinciden con Sam/Sebas |
|---|---|---|---|
| Alta | 10 | 3 | 7 |
| Media | 9 | 5 | 4 |
| Baja | 5 | 3 | 2 |

**Nuevos de alta:** D-08 (Complex también tuvo vuelcos en la batería combinada), D-09 (FSM Inspection: son 9 de 20 los ensayos que nunca ven el objetivo, no 11) y D-10 (tiempos de la fila Obstacle de la tabla física).

---

## 1.1 Inconsistencias de datos

### D-01 · ALTA · `results.tex:569`: el robot no se quedó en modo H en la inspección
- **Cita:** "The robot remained in the wheeled/differential locomotion mode (H) throughout all 20 trials, so no gait-transition stability data applies to this experiment."
- **Verificación:** recorrí la columna `mode` de `experiments/R3-05-inspection/data/test_*/metrics_raw.csv`. En los 20 ensayos la ocupación es X = 40.6–86.1 %, H = 13.4–58.4 % y C = 0.4–1.1 %. Además, `N_mode_X_events` vale ≥ 1 en todos los ensayos, y el propio texto lo define en `:535` como "omnidirectional-mode switches", así que el paper se contradice. `test_017` termina en modo X.
- **Corrección sugerida:** "The robot alternated between differential rolling (H) and omnidirectional (X) evasion throughout (X occupancy 41–86 % of trial time); no quadrupedal gait-transition data applies." Revisar si "no gait-transition stability data applies" sigue en pie.
- **Coincide con Sebas A-1.**

### D-02 · ALTA · `results.tex:567`: "in every one of the 17 successful trials without exception" es falso
- **Verificación:** en `R3-05-inspection/data/test_014_SUCCESS/inspection_summary.json`, `N_lidar_events = 4` y `N_mode_X_events = 4` son iguales, así que ese ensayo no tiene "fewer". El cociente de medias, 7.71/3.29 = 2.34, sí cuadra. Por ensayo, el cociente va de 1.0 a 4.0, de modo que "≈2.3× fewer … in every one" también sugiere una regularidad por ensayo que no existe.
- **Corrección sugerida:** "on average ≈2.3× fewer … (fewer in 16 of the 17 successful trials, equal in the remaining one)".
- **Coincide con Sam S-12 y Sebas A-2.**

### D-03 · ALTA · `results.tex:296` (caption de `fig:stability_profile`): "No trial violated this limit across all 30 runs"
- **Verificación:** alineé cada `stability_log.csv` de `experiments/simulation/familia_c{1,2}_*/test_*` con `loaders.load_stability_log_aligned`, que es el mismo método que `ecdf_phase_space.py`.
  - Rugged: en `test_005` y `test_006` hay 22 muestras con TR ≥ 1 (máximo **1.862**), 11 de ellas dentro de la ventana dibujada [−5, 10] s, justo en t ≈ −1.25…−0.4 s. Ese es el "spike" de 0.77 de la media.
  - Slope: `test_002` y `test_015` superan TR = 1 (1.66 y 1.62) fuera de la ventana, a t ≈ +27 s.
  - Las medias de la prosa sí cuadran: 0.597 frente a 0.600 y 0.592 frente a 0.593, con pico medio 0.772 a t = −1.09 s.
- **Corrección sugerida:** "The mean profile stays below TR = 1.0; four of the 30 trials show brief per-sample excursions above it (up to 1.86, during leg lift, cf. Table~\ref{tab:crawl_stability}) without overturning." Reformular también el "isolated transient spike reaching TR ≈ 0.77" de `:317` como valor medio.
- **Coincide con Sebas A-3.**

### D-04 · ALTA · `results.tex:701`: parámetros del MLP y partición de flash
- **Cita:** "397{,}829~B flash (30.4\% of the board's 4~MB partition, almost entirely the $\sim$47k-parameter model itself)".
- **Verificación:**
  - Build report en `experiments/R2-04-mlp-onboard-compute/output/onboard_compute_results.txt`: "Flash … used 397829 bytes from **1310720** bytes". Eso es el 30.4 % de la partición de app de 1.25 MB. Sobre 4 MB sería el 9.5 %.
  - Los arrays de `output/mlp_weights.h` (W1[20250], B1[150], W2[12000], B2[80], W3[160], B3[2]) suman **32 642** parámetros. Eso son ≈ 131 KB en float32, un 33 % de la flash usada, así que "almost entirely the model" es falso.
  - La propia figura `fig:classifier_tradeoff`(c), según `_plotting/vectorized/classifier_fig6.csv`, muestra 32 489 parámetros para el MLP. El "~47k" se parece al tamaño del SVM (45 917).
- **Corrección sugerida:** "397,829 B flash (30.4 % of the 1.25 MB application partition, of which the ≈32.6k float32 weights take ≈131 KB)".
- **Coincide con Sam S-02 y Sebas A-4.**

### D-05 · ALTA · `results.tex:990`: "in the worst case a transition consumes ≤ 5.06 J"
- **Verificación:** recomputé con `energy_transition.find_transitions` e `integrate_energy` sobre `experiments/real/Test_current_integrated_*/imu_ina.csv`.

  | Dirección | N | Media | SD muestral | Máximo |
  |---|---|---|---|---|
  | Q→DR | 16 | 5.059 J | 2.932 | **15.88 J** |
  | DR→Q | 19 | 4.132 J | 1.195 | 7.27 J |

  Welch t = 1.184, que cuadra con el caption. 5.06 J es la media, no una cota. La SD de 2.93 J de Q→DR la produce casi entera ese único ensayo de 15.88 J: los otros 15 están entre 3.64 y 5.33 J. Eso podría reformular "the present dataset does not isolate a specific mechanical cause".
- **Corrección sugerida:** "…averages 5.06 J (maximum 15.9 J, a single outlier) over 16 detected transitions…". Quitar "upper bound … worst case".
- **Coincide con Sam S-01** y con Sebas B-3 en la parte de "any mode transition".

### D-06 · ALTA · `tab:consolidated_physical_metrics` (`results.tex:973`): ventana $T_{switch}$ del Appetitive
- **Cita:** "$3.0$--$9.0\,\text{s}$ (mechanically limited)".
- **Verificación:** el máximo de `Tswitch` en `experiments/real/StimuliB_t0{1..4}/combined_metrics.csv` da 0.876, 13.200, 1.349 y 0.902 s. Abrí `assets/Appetitive_Real_Plot_1_Switching_Delay_ECDF.png` y los escalones están en ≈0.9, 1.35 y 13.2 s. Ningún ensayo cae entre 3 y 9 s.
- **Corrección sugerida:** "0.9–1.35 s (one replicate at 13.2 s)". La cuestión de 3 o 4 réplicas sigue siendo decisión del autor y no se reabre aquí.
- **Coincide con Sam S-03.**

### D-07 · ALTA · `results.tex:504`: "this is the only sense in which 'success rate' is used anywhere in this paper"
- **Verificación:**
  - El caption de `tab:fsm_comparison` (`:480`) dice que Inspection, Rugged e Inclined son "individual attempts". Rugged/Neural da 3/6 = 50 % y Rugged/FSM 15/25 = 60 % en `R2-02-fsm-baseline/output/table_master_comparison.csv`.
  - En Inspection, 17/20 son intentos sin reintento (`R3-05-inspection/data`).
  - En la ablación, 3/12 y 4/12 son por ensayo (`R3-02-wta-vs-threshold/output/ablation_stats_summary.csv`).
  - Además, en Aversive los reintentos no siguen a un timeout, como dice la definición, sino a vuelcos. Ver D-13.
- **Corrección sugerida:** declarar las dos definiciones (mission-level para las 4 suites con reintento y per-attempt para el resto) y quitar "anywhere in this paper".
- **Coincide con Sam S-07.**

### D-08 · ALTA · `results.tex:180` (y `:176`): "the Rugged Terrain suite alone accounts for the tipovers and crashes, the only suite where the robot's structural stability … was compromised"
- **Cita:** `:180` "the Appetitive Targeting and Complex Navigation suites discarded a share of attempts to timeout … and the Rugged Terrain suite alone accounts for \revblue{the tipovers and crashes …}, the only suite where the robot's structural stability, not merely task completion time, was compromised under perturbation."
- **Verificación:**
  - `experiments/R3-04-noise-robustness/output/table_R1_failure_rate.csv` y los veredictos de `data/familia_b_compleja/`: Complex tuvo **3 FAILURE_TIMEOUT + 3 FAILURE_TIPOVER** (`test_003`, `test_004` y `test_005_FAILURE_TIPOVER`) en 21 intentos.
  - Rugged tuvo 8 tipovers y 4 crashes en 27 intentos, cifra que sí cuadra con `:176` y `:1050`.
  - Por tanto Rugged no es la única suite con vuelcos, y Complex no descartó solo por timeout. El caption (`:176`) dice "large majority of non-timeout failures", que es correcto (12/15), pero la prosa de `:180` lo convierte en "alone" y "only suite".
- **Corrección sugerida:** "…Appetitive Targeting discarded attempts to timeout, Complex Navigation to timeout (3) and tipover (3), and the Rugged Terrain suite accounts for most tipovers and all crashes (8 tipovers, 4 crashes out of 27 attempts)…". Quitar "the only suite where…".
- **NUEVO.** La sugerencia de Sam en `:184` menciona solo "Rugged Terrain tipovers", así que no lo detecta.

### D-09 · ALTA · `results.tex:571` y caption `:576`: FSM Inspection, "in 11 of 20 trials … occupying that mode 93–99% of trial time and never visually detecting the target at all"
- **Verificación:** recorrí `mode` y `blue_present` en `experiments/R2-02-fsm-baseline/data/familia_e_inspeccion_fsm/test_*/metrics_raw.csv`. Hay 11 timeouts, pero solo **9** ocupan X el 93.0–98.7 % y nunca detectan el objetivo (`test_004`, 006, 007, 010, 011, 015, 017, 018 y 020).
  - `test_016_FAILURE_TIMEOUT`: X 49 %, H 50 %, objetivo detectado (`blue_present` = 1).
  - `test_019_FAILURE_TIMEOUT`: X 21 %, H 78 %, objetivo detectado.
  - El caption de `:576` ("in its 11 failing trials the lower trace instead stays flat in avoidance for nearly the entire duration") también es falso para esos 2.
- **Corrección sugerida:** "in 9 of 20 trials the robot … never visually detecting the target at all; the other 2 FSM timeouts detect the target but fail to reach it". En `:576`: "in 9 of its 11 failing trials…".
- **NUEVO.**

### D-10 · ALTA · `tab:consolidated_physical_metrics`, fila Obstacle (`results.tex:976`): tiempos de $Var(z)$ y "Settles by"
- **Cita:** "${\approx}\,1100$, transient ($t < 7\,\text{s}$)" … "$t = 8\,\text{s}$".
- **Verificación:** en `experiments/real/StimuliG_t01/neural_metrics.csv`, que es el ensayo que dibuja la figura (`real_plot_suite.py` usa `dirs[0]`), el pico de firing variance es **1316 a t = 26.9 s**. El valor está por encima de 50 entre t = 22.5 y 39.1 s, y vuelve a 0 hacia los 40 s. Abrí `assets/Obstacle_Real_Plot_3_…png` y lo confirma: hay doble pico en 27 s (≈1310) y 34 s (≈1000), y la base es 0 desde ~40 s. Roll RMS llega a 4.2° a t ≈ 33 s y decae a 2.8°, no a 3.5°.
  - Las otras réplicas dan picos de 684 a t = 8.2 s (t02) y 688 a t = 16.4 s (t03). Ninguna combinación da "≈1100, t < 7 s, settles at t = 8 s".
  - Además, el texto de `:963` ("consistent across all three replicates") no encaja con picos de 684 a 1316.
- **Corrección sugerida:** recalcular la fila desde `StimuliG_t0*`, por ejemplo "peak ≈1300 (t01; 680–1320 across replicates), double-peaked, t ≈ 22–40 s | Roll ≤ 4.2° | settles by t ≈ 40 s", o declarar que la fila describe la réplica representativa.
- **NUEVO** en cuanto a los tiempos. Sam S-09 ya señala que la fila no resume las 3 réplicas (Roll y "≈1100") y **coincide parcialmente**.

### D-11 · MEDIA · `results.tex:1021`, `:1025`, `methodology.tex:196`, `conclusions.tex:45`: latencias físicas 184/534 ms, "15 hardware replicates"
- **Verificación:** `experiments/real/Imu_pitch_test_t01/pitch_latency.csv` es un banco de 25 ensayos que alterna un estímulo de pitch de 12°/0°, con 1 TIMEOUT.
  - Estímulo de 12°: 12 OK, media 0.18477 s.
  - Estímulo de 0°: 12 OK, media 0.53487 s.
  - Coincide al ms con los paneles A/B (μ = 0.184 / 0.534 s). `_plotting/vectorized/terrain_latencies.csv` tiene 8/11/12/10 escalones, no 15.
  - Si esa es la fuente, N = 12 por dirección y el disparador de DR→Q es el pitch que vuelve a 0°, no "wheel slippage on rugged terrain".
- **Corrección sugerida:** que el autor confirme la fuente. Si es el banco de pitch, ajustar N y la explicación del panel B.
- **Coincide con Sam S-04 y Sebas A-7.** Lo bajo a media porque depende de una confirmación del autor.

### D-12 · MEDIA · `fig:classifier_tradeoff`(a) frente a texto `results.tex:699`/`:664`: F1 del MLP y de la regresión logística
- **Verificación:** `_plotting/vectorized/classifier_fig5.csv` es la extracción del panel (a). Da F1: LR **0.659**, SVM 0.857, RF 0.947 y MLP **0.734** (accuracy 0.730). El texto dice LR = 0.692 y MLP (CV) = 0.771/0.767. SVM y RF coinciden con ±0.001, así que la extracción es fiable y las diferencias de 0.033–0.037 son reales. El caption dice que (a) es la media de la misma CV de 5 pliegues.
- **Corrección sugerida:** que el autor aclare de qué corrida sale el panel (a), y unificar caption o valores.
- **Coincide con Sam S-13.** Requiere datos originales del clasificador no versionados.

### D-13 · MEDIA · `results.tex:504` y caption de `fig:attempts_vs_noise_level` (`:509`): reintentos "at the noisiest levels", "intermediate/high noise" y "times out"
- **Verificación:** manifiestos `experiments/simulation/familia_a_{apetitivo,aversivo}/suite_execution_manifest.json`, agrupados por `noise_level_idx`:

  | Suite | Nivel 0 | Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 |
  |---|---|---|---|---|---|
  | Appetitive | **1.67** | 1.00 | 1.33 | 1.67 | 1.00 |
  | Aversive | 1.00 | 1.00 | 1.00 | 1.33 | 1.33 |

  - El máximo de Appetitive (1.67) aparece también a **nivel 0, sin ruido**, y el nivel más ruidoso (4) da 1.00. Así que "at the noisiest levels" y "retry at intermediate/high noise" son falsos para Appetitive.
  - El manifiesto registra **dos** timeouts de la misión 6 a nivel 0, pero en disco solo hay un directorio `test_006_FAILURE_*`. `build_attempts_vs_nl.py` cuenta directorios y por eso la figura pinta 1.33 a nivel 0, no 1.67, y la CSV maestra da 19 intentos frente a los 20 del manifiesto.
  - En Aversive los dos fallos previos son FAILURE_TIPOVER, no timeouts, mientras que el caption de la tabla y `:504` dicen "a mission that first times out is retried".
- **Corrección sugerida:** "Neural needs up to 1.67× as many attempts in Appetitive (including at the unperturbed level) and 1.33× in Aversive (levels 3–4), with no monotonic trend". En el caption: "retried after a timeout or tipover". Decidir si se cuenta el intento perdido del manifiesto.
- **Coincide con Sebas M-2** en la parte de "noisiest" y "intermediate/high". **NUEVO** en la discrepancia manifiesto/directorio y en lo de tipover frente a timeout. Ojo, también es cierta la dependencia que señala Sebas: `final_metrics.noise_idx` = 0 en los 96 intentos de `simulation/`, lo comprobé. Eso afecta a si hubo ruido en esta batería (C-75 §2, abierto).

### D-14 · MEDIA · `results.tex:182`: "postural stability does not visibly degrade with perturbation severity on either terrain"
- **Verificación:** medias de los éxitos por nivel en `R3-04-noise-robustness/data/familia_c1_terreno_rugoso` y `familia_c2_pendiente`:

  | Métrica | Nivel 0 | Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 |
  |---|---|---|---|---|---|
  | Rugged, Roll RMS | 1.83 | 1.74 | 1.70 | 1.82 | 1.82 |
  | Rugged, Pitch RMS | 1.33 | 1.22 | 1.36 | 1.72 | 2.33 |
  | Slope, Roll RMS | 6.75 ± 7.16 | 1.48 | 1.54 | 1.48 | 3.74 ± 3.11 |

  - El Roll de Rugged queda dentro de la banda 1.65–1.9 del caption con ±σ, y eso cuadra.
  - El Pitch de Rugged sube un 75 % del nivel 0 al 4, casi monótono a partir del nivel 1. El panel (b), según el caption, dibuja Roll y Pitch de ambas suites, así que "either terrain" queda contradicho por la curva de pitch en Rugged.
  - En Slope hay dos outliers de roll en los niveles 0 y 4.
  - El mismo patrón de pitch creciente aparece en las 4 suites de `fig:noise_robustness_grid` (Appetitive 1.07→2.11, Aversive 1.03→2.61). Es plausible que sea un artefacto del drift angular inyectado en el mismo canal de pitch con que se calcula Pitch RMS, y el texto no lo menciona. No lo verifiqué en el código (dudoso).
- **Corrección sugerida:** acotar la frase a "Roll RMS on Rugged Terrain and Pitch RMS on the Inclined Slope" y mencionar que el Pitch RMS medido sube con η en todas las suites, probablemente por el drift angular inyectado.
- **NUEVO.**

### D-15 · MEDIA · `methodology.tex:244`, `:290`, `:337`: mapeo color ↔ canal
- **Verificación:**
  - `experiments/simulation/experiments_config.yaml`: "FAMILIA A1 — Estímulo Apetitivo (Target Azul)" y "A2 — Estímulo Obstáculo (Target Verde)".
  - `trial_summary.json` de Appetitive: `bb_blue = 41700`.
  - `experiments/real/MANIFEST.md`: StimuliB = appetitive y StimuliG = obstacle.
  - En las ecuaciones, $z_{17} = (Gpe_B - Ar)_+$ es la parada de aproximación, así que B es el canal apetitivo.
  - Todo eso contradice "obstacle (Blue), appetitive (Green)".
- **Corrección sugerida:** "appetitive (Blue), obstacle (Green), aversive (Red)", revisar `:290` y explicitar la equivalencia x/y/z de `:337`.
- **Coincide con Sam S-05 y Sebas A-5.** Lo dejo en media porque está fuera de mi foco estricto, aunque ellos lo dan como alta.

### D-16 · MEDIA · `results.tex:476` frente a `:1052`: λ con dos definiciones
- **Verificación:** `R2-02-fsm-baseline/scripts/build_master_table.py` (`_lambda_whole_trial` y `CONFLICT_NOTE`). El λ de la tabla es la media de `lambda_efficiency` = cmd_mag/‖activity‖ sobre todos los timesteps. El propio script dice que esa fórmula "mixes incompatible scales … small by construction". La Limitations (`:1052`) llama a λ "conflict-efficiency metric" y lo excluye por instrumentación. En la ablación, `exp_lambda` vale 1.0 en todas las variantes (`ablation_stats_summary.csv`).
- **Corrección sugerida:** distinguir los símbolos (por ejemplo $\lambda_{trial}$ y $\lambda_{conflict}$) o quitar λ de la tabla FSM, dado que el propio pipeline duda de su escala.
- **Coincide con Sam S-16 y Sebas M-3.**

### D-17 · MEDIA · `tab:fsm_comparison`, filas de terreno Neural: origen de los datos sin nombrar
- **Verificación:** Rugged/Neural (N = 6, 50 %, 54.94 ± 2.72, Roll 1.827 ± 0.033) y Slope/Neural (N = 3, 77.02 ± 1.26, Roll 6.751 ± 7.160) coinciden exactamente con el **nivel η = 0 de la batería de perturbación combinada** R3-04 (`R3-04-noise-robustness/data/familia_c{1,2}_*`). Ese nivel tiene 6 intentos y 3 éxitos en C1, y 3 intentos en C2. El caption lo llama "an independent re-run of the two scenarios", y `:152` dice de esa misma batería que "is not directly comparable" con la de topografía.
- **Corrección sugerida:** sin reabrir C-69, nombrar la fuente: "the η = 0 subset of the combined-perturbation battery of Section~\ref{sssec:noise_robustness_extra}". Eso además explica la restricción a ruido cero (ver Sam S-15).
- **Coincide parcialmente con Sam S-15.** Lo NUEVO es la identificación exacta de la fuente.

### D-18 · MEDIA · `results.tex:194` frente al caption de `fig:ablation_combined` (`:211`)
- **Cita:** `:194` "all four variants perform statistically indistinguishably in the Appetitive Targeting scenario (Figure~\ref{fig:ablation_combined})". El caption dice "Under the no-conflict Appetitive Targeting scenario (not shown)".
- **Verificación:** texto. Las cifras sí cuadran con `ablation_stats_summary.csv`: success 0.9167 frente a 1.0, Fisher p = 1.0.
- **Corrección sugerida:** quitar la referencia a la figura o cambiarla por "(Figure~\ref{fig:ablation_combined} caption)".
- **NUEVO.**

### D-19 · MEDIA · `methodology.tex:198` y `results.tex:219`: no lo pude verificar, ver Límites
Sin hallazgo. Recomputé Fisher para 12/12 frente a 7/12 y 8/12: el umbral de "≥ 5 fallos" cuadra según Sebas (p = 0.037), y mis cifras de la CSV dan los mismos p. Lo listo solo para dejar constancia de que se revisó.

### D-20 · BAJA · `results.tex:513`: "roughly 30× longer in absolute time"
- **Verificación:** en `table_master_comparison.csv`, la exposición al conflicto es 6.1335 s para FSM y 0.2267 s para Neural, un cociente de **27.1×**. El "30×" sale de los valores redondeados 6.1/0.2.
- **Corrección sugerida:** "≈27×".
- **NUEVO.**

### D-21 · BAJA · `fig:MorphologicalEnergy` frente a prosa `:990`: tipo de SD
- **Verificación:** las barras del builder usan `np.std`, es decir SD poblacional (2.84 y 1.16). La prosa da la SD muestral (2.93 y 1.19), y el caption dice "±1 SD" sin especificar. Es la clase C-74 y se trata como recomendación, no como error nuevo.
- **Corrección sugerida:** igualar figura y texto, o declarar el tipo de SD.
- **Coincide con Sam** (§1.6, nota de la figura de energía).

### D-22 · BAJA · `results.tex:1003–1011`: el segmento Omnidireccional, "38.6 s" y "typical 38 s"
- **Verificación:** `R2-04-mode-energy/output/mode_energy_stats.csv` da X con N = 194 muestras y 1 segmento. 194 muestras a ≈5 Hz son ≈38.8 s, coherente. Pero `:990` dice "a typical 38 s Omnidirectional segment integrates to ≈216 J" cuando solo existe uno: 5.71 W × 38.6 s ≈ 220 J.
- **Corrección sugerida:** "the single recorded 38.6 s Omnidirectional segment integrates to ≈220 J".
- **Coincide con Sebas B-3.**

### D-23 · BAJA · `results.tex:975`: "peak ≈27× Obstacle baseline"
- **Verificación:** los picos de MultiRGB son 23 487, 32 860 y 31 843, y los de StimuliG 1316, 684 y 688. El cociente sale contra el pico de Obstacle (por ejemplo 31 843/1 100 ≈ 29), no contra su línea base, que vale ≈0.
- **Corrección sugerida:** "≈20–30× the Obstacle peak".
- **Coincide con Sam S-10 y Sebas B-1.**

### D-24 · BAJA · Referencias cruzadas
- **Verificación:** script sobre los `\label` y `\ref` de `sections/*.tex`. No hay ninguna referencia rota.
  - `fig:appetitive_micro` **nunca se referencia**: `:73` remite a `fig:noise_robustness_grid`, mientras que las otras tres suites sí remiten a su figura micro.
  - `methodology.tex:439` remite a "Section~\ref{sec:methodology}'s Basal Ganglia Module" desde dentro de la propia Methodology. Debería ser `\ref{sssec:Basal_Ganglia_Module}`.
  - `results.tex:1052` remite a "Section~\ref{sec:results}" para la ablación. Convendría ponerle una etiqueta a la subsección de ablación.
- **Corrección sugerida:** añadir "(Figure~\ref{fig:appetitive_micro})" en `:73` y concretar las otras dos referencias.
- **NUEVO.**

---

## Verificado sin hallazgo (para la consolidación)
- **`tab:consolidated_simulation_metrics`, 4 filas:** recomputadas desde `experiments/simulation/*/trial_summary.json` como media ± SD poblacional. Obstacle con n = 14, sin `test_007` (roll 37.3°): 15.72 ± 2.49, 1.55 ± 0.15 y 0.90 ± 0.31. Cuadran todas.
- **`tab:fsm_comparison`:** las 16 filas cuadran con `table_master_comparison.csv` (SR, tiempo, Roll y λ). También cuadran los veredictos FSM: Complex 14 timeouts + 1 tipover, Rugged 15 S/8 tipovers/2 crashes, Slope 15 S/6 tipovers e Inspection 9/20.
- **Topografía variable:** Roll y Pitch medios 1.59/1.67 y 1.47/2.29, y punto medio 1.98°. $T_{switch}$: 13/15 ensayos de Rugged entre 0.2 y 0.7 ms (2 a ≈0.6 s), y Slope entre 0.9 y 1.8 ms con 5 valores distintos. $T_{response}$ = 0 en los 30. TR medio 0.597/0.592 (el paper dice 0.600/0.593, diferencia despreciable).
- **Cotas de `:459`:** Roll ≤ 1.59° y Pitch ≤ 2.29° en las dos baterías.
- **Ablación:** todos los porcentajes, IC y p cuadran con `ablation_stats_summary.csv`. Roll +43.5 %/+46.0 %/+22.0 %, frente a +43.6/+45.9/+22.0 en el texto, son diferencias de redondeo menores de 0.1 pp. Pitch +6.4/−11.3/−5.7. Latencias 75.9/81.7/66.6/109.1 ms con sus IC.
- **Inspección:** `tab:inspection_metrics` con SD muestral, grupos clean/elevated (n = 12/5, rangos 4–7/11–28, $d_{final}$ 1.081 ± 0.042/1.065 ± 0.022), timeouts 7/11/17 con $N_{ev}^{LiDAR}$ = 18/27/33, y $T_{acquisition}$ no nulo.
- **R3-04:** 8 tipovers y 4 crashes en 27 intentos en Rugged. Aversive y Obstacle sin descartes. Tres éxitos por nivel en las 6 suites. Fracción de detección de 0.010 frente a 0.994 en el par `test_007` de Appetitive. Las figuras micro son `test_001` a η = 0.
- **MLP:** test 96/120 = 0.800, precisión 56/75 = 0.747, recall 56/61 = 0.918 y F1 0.824. Latencia 8.81 ms (SD 2.67 µs) y RAM 24 140 B = 7.4 % de 320 KiB. 14× y 25× frente a SVM/RF.
- **Potencia por modo:** 2.73 ± 2.29, 1.13 ± 1.08 y 5.71 ± 0.73 W, con N de 20/20/1 segmentos y 1873/3297/194 muestras. "five-fold" = 5.05.
- **Abstract y Highlights:** 25 %/33 %, 100 % frente a 0 % y 85 % frente a 45 % cuadran.

## Otras categorías
Mi enfoque es la 1.1 y en las demás no hice una pasada sistemática. Sam y Sebas las cubren, y lo poco que vi coincide con lo suyo (por ejemplo S-06 CPG y S-08 modo ante inestabilidad).
- **1.2:** sin hallazgos propios nuevos.
- **1.3:** sin hallazgos propios nuevos.
- **1.4:** sin hallazgos propios nuevos.
- **1.5:** sin hallazgos propios nuevos.
- **1.6:** sin hallazgos propios nuevos.

## Límites
- **No verificable desde datos:**
  - `tab:crawl_stability` (N = 268) y la corrida de 979 muestras de transiciones: no hay datos crudos (`_plotting/vectorized/README.md`). Solo comprobé la coherencia interna: TR = 1 − SM_norm cuadra en media, SD, mínimo y máximo.
  - CV del MLP (0.767/0.764/0.779/0.771), ablación de arquitecturas y ROC: solo existen como valores de figura o texto.
  - `tab:terrain_sequence` (15 ensayos físicos): no hay dataset en `experiments/real/`.
- **Datos no versionados:** `R3-04-noise-robustness/data/` y `R2-02-fsm-baseline/data/` estaban presentes en esta máquina y los usé (D-08, D-09, D-14, D-17 y el resto de verificaciones de FSM/R3-04). En otra máquina, esos hallazgos **requieren verificación con datos no versionados**.
- **Hipótesis sin comprobar en el código:** que el Pitch RMS creciente en todas las suites (D-14) venga del drift angular inyectado. No revisé `red_neuronal.py`.
- **Ruido en la batería de `simulation/`:** que tuviera ruido de verdad (σ = 0–30 % en `:320`) depende de C-75 §2. Confirmé que `final_metrics.noise_idx` = 0 en los 96 intentos, pero no lo resolví.
- **Figuras:** solo abrí `Obstacle_Real_Plot_3` y `Appetitive_Real_Plot_1`. No revisé legibilidad ni leyendas del resto (categoría 1.6).
- **Tabla física:** los valores de Roll/Pitch de `tab:consolidated_physical_metrics` dependen de una "active response window" que no está definida, así que no se pueden reproducir con exactitud.
