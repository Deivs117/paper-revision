# Auditoría final ronda 2 — Samuel (C-79), 2026-11-03

Brief: `intake/pending/final_audit_round2_2026-11-02.md`. Pasada de **hallazgos**, no de corrección: no se
editó `sections/*.tex`. Líneas referidas a `main` en `adca90e` (2026-11-03). Orden de lectura: `results.tex`
(físico, energía, MLP) → resto de `results.tex` → `methodology.tex` → `introduction.tex` → `conclusions.tex` →
`preamble.tex`/`closing.tex`.

Todo lo de 1.1 se recomputó con `uv run --python 3.13 --with pandas --with numpy --with scipy`, desde los
ficheros versionados indicados en cada hallazgo. Lo que depende de `R3-04-noise-robustness/data/` o
`R2-02-fsm-baseline/data/` va marcado **"requiere verificación con datos no versionados"**.

No reabro (sección 3 del brief): en dash, `\label{}`, tamaño de figuras, las dos baterías de C-69, la SD
poblacional de C-74 ni el Appetitive físico 3 vs. 4 (abierto, decisión del autor; solo lo cito donde afecta
a otro hallazgo).

## Resumen

| Prioridad | N | IDs |
|---|---|---|
| Alta | 8 | S-01 … S-08 |
| Media | 22 | S-09 … S-26, S-30, S-33, S-34, S-40 (+ la parte "MLP → salience" de S-38) |
| Baja | 10 | S-27, S-28, S-29, S-31, S-32, S-35 … S-39 |

Cada hallazgo de la tabla es una entrada. S-37 y S-39 agrupan varias correcciones menores localizadas.

Lo que bloquea el envío, en una línea cada uno:
- **S-01** "en el peor caso una transición consume ≤ 5.06 J": 5.06 J es la **media**; el máximo medido es 15.88 J.
- **S-02** MLP: no son "~47k parámetros" sino 32 642, y el 30.4 % de flash es de la partición de app de 1.25 MB, no "de 4 MB".
- **S-03** Tabla física: la ventana de $T_{switch}$ del Appetitive dice 3.0–9.0 s; los ensayos dan 0.88–13.2 s (y la propia figura ECDF llega a 13.2 s).
- **S-04** Las latencias físicas de 184/534 ms (citadas en 4 sitios como "15 hardware replicates" de la misión multiterreno) coinciden al ms con `Imu_pitch_test_t01`, un banco de pitch de 25 ensayos (12 OK por dirección).
- **S-05** Mapeo de canales de color contradictorio: methodology dice Blue = obstáculo / Green = apetitivo; los datos, las figuras y las ecuaciones dicen Blue = apetitivo / Green = obstáculo.
- **S-06** Introducción y Conclusiones afirman que la marcha la generan **CPGs**; Methodology describe un patrón de crawl fijo en firmware, en lazo abierto. No hay CPG en el método.
- **S-07** "this is the only sense in which 'success rate' is used anywhere in this paper" es falso en la misma tabla (Inspection/terreno = por intento) y en la ablación.
- **S-08** Methodology: "engaging the quadrupedal mode whenever gait stability is compromised"; las ecuaciones, Results y Conclusiones dicen que en pendiente entra **differential rolling**.

---

## 1.1 Inconsistencias de datos

### S-01 — Alta — "upper bound … ≤ 5.06 J" usa la media como cota
- **Ubicación:** `results.tex:990` (párrafo de energía tras `fig:MorphologicalEnergy`).
- **Problema:** "its transition energy serves as an upper bound on the cost of any mode transition: in the worst case a transition consumes $\leq 5.06$ J". 5.06 J es la media ± 2.93 J. Hay transiciones individuales muy por encima.
- **Verificación:** recomputé las 35 transiciones con la lógica exacta de `experiments/_plotting/builders/energy_transition.py` (`find_transitions` + `integrate_energy`, sobre `experiments/real/Test_current_integrated_*/imu_ina.csv`). Q→DR: N = 16, media 5.059 J, SD muestral 2.932, **máx. 15.88 J**, 3/16 > 5.06 J. DR→Q: N = 19, media 4.132, SD 1.195, máx. 7.27 J. Welch t = 1.184 (p = 0.25) ✓ con el caption.
- **Además:** "upper bound on the cost of *any* mode transition" supone que las transiciones con Omnidireccional cuestan menos, pero solo hay 1 transición →X y no se integró (sin ventana calibrada, según el docstring del builder).
- **Corrección sugerida:** "…the Quadrupedal→Differential Rolling direction averages 5.06 J per transition (maximum 15.9 J over the 16 detected transitions), a small cost relative to continuous operation…". Quitar "upper bound on any mode transition" o acotarlo a "among the two measured directions".

### S-02 — Alta — Huella de memoria del MLP: parámetros y partición de flash mal descritos
- **Ubicación:** `results.tex:701`.
- **Problema:** "397,829 B flash (30.4% of the board's 4 MB partition, almost entirely the $\sim$47k-parameter model itself)". Tres errores:
  1. La arquitectura confirmada es `Linear(135,150) → Linear(150,80) → Linear(80,2)`, es decir, 20 250 + 150 + 12 000 + 80 + 160 + 2 = **32 642 parámetros**, no ~47k.
  2. 397 829 / 1 310 720 = 30.35 %: la base es la **partición de app de 1.25 MB** que reporta PlatformIO ("used 397829 bytes from 1310720 bytes"). Respecto a 4 MB serían 9.5 %.
  3. 32 642 floats × 4 B ≈ 131 KB, así que el modelo es un tercio de los 398 KB de flash, no "almost entirely".
- **Verificación:** tamaños de array en `experiments/R2-04-mlp-onboard-compute/output/mlp_weights.h` (`W1[20250]`, `BIAS1[150]`, `W2[12000]`, `BIAS2[80]`, `W3[160]`, `BIAS3[2]`, más `SCALER_MEAN/SCALE[135]`). Build report en `.../output/onboard_compute_results.txt`. El propio fichero dice "~32,600-FLOP" en otra línea, y la figura `fig_classifier_tradeoff_fused.png`(c) muestra ~32 489 parámetros para el MLP (`_plotting/vectorized/classifier_fig6.csv`). El "~47K" de la nota de resultados es el origen del error.
- **Corrección sugerida:** "…and 397,829 B flash (30.4% of the 1.25 MB application partition), of which the $\approx$32.6k float32 weights account for $\approx$131 KB."

### S-03 — Alta — `tab:consolidated_physical_metrics`: la ventana de $T_{switch}$ del Appetitive no cuadra con los datos ni con su figura
- **Ubicación:** `results.tex:973` (fila Appetitive, "3.0–9.0 s (mechanically limited)").
- **Verificación:** columna `Tswitch` de `experiments/real/StimuliB_t0{1..4}/combined_metrics.csv`, valores no nulos > 0: 0.876, **13.2**, 1.349, 0.902 s. El ECDF promovido (`assets/Appetitive_Real_Plot_1_Switching_Delay_ECDF.png`) llega a 13 200 ms (lo vi, y C-72 lo documenta: "0.4 ms (Obstacle) to 13.2 s (Appetitive)"). Ningún ensayo cae en 3–9 s.
- **Corrección sugerida:** recalcular la celda desde los CSV (p. ej. "0.9–1.3 s; one outlier at 13.2 s"). Si el autor decide 3 réplicas (pregunta abierta), indicar cuál se excluye. Revisar el párrafo `results.tex:894` ("extended switching-delay window") con el valor corregido.

### S-04 — Alta — Las latencias físicas 184/534 ms no vienen de la misión multiterreno de 15 réplicas
- **Ubicación:** caption de `fig:FourPanelLatencies` (`results.tex:1021`) y prosa `results.tex:1025`. Las mismas cifras se repiten en `methodology.tex:196` y `conclusions.tex` (párrafo 3), siempre como "15 hardware replicates" de un "continuous multi-terrain navigation mission", con la transición DR→Q "triggered by wheel slippage on rugged terrain".
- **Verificación:** `experiments/real/Imu_pitch_test_t01/pitch_latency.csv` es un banco de **25 ensayos alternando un estímulo de pitch 12.0°/0.0°** (MANIFEST.md: "Dedicated pitch-triggered switching-latency test"). Recomputé: 12.0° → OK = 12, media **0.1848 s** (SD 1.4 ms); 0.0° → OK = 12, media **0.5349 s**; 1 TIMEOUT. Coincide al ms con los paneles A/B (0.184 / 0.534 s). Por otra parte, la figura publicada es una **reconstrucción por vectorización** de la imagen original (`_plotting/vectorized/terrain_latencies.csv`: 8/11/12/10 escalones en A/B/C/D, no 15; la leyenda de la figura dice "Hardware Replicates (reconstructed)"), y el README de `vectorized/` advierte que no es exacta valor a valor.
- **Por qué es alta:** si la fuente es el banco de pitch, (i) N = 12 por dirección, no 15; (ii) DR→Q lo dispara el pitch que vuelve a 0°, no el deslizamiento de ruedas; (iii) el texto de `results.tex:1025` sobre "filters transient high-frequency impact noise on noisy surfaces" no tiene sustento. Necesita confirmación del autor (el MANIFEST lo dejó como "strong candidate").
- **Corrección sugerida:** el autor confirma la fuente. Si es el banco de pitch: "(N = 12 pitch-step trials per direction)" y reescribir la causa de B. Si los 15 son reales, documentar de dónde salen. En ambos casos, quitar "(reconstructed)" de la leyenda visible.

### S-05 — Alta — Mapeo color ↔ canal contradictorio entre Methodology, ecuaciones, Results y datos
- **Ubicación:** `methodology.tex:244` ("$Gpe_B$, $Gpe_G$, and $Gpe_R$ are … for the obstacle (Blue), appetitive (Green), and aversive (Red)"), `methodology.tex:290` ("appetitive (green) channel") y `methodology.tex:337` ($G_{pe,y}$ = apetitivo, $G_{pi,x}$ = obstáculo).
- **Verificación (texto + datos versionados):**
  - `experiments/real/MANIFEST.md`: StimuliB = **Appetitive (blue)** ("verified: blue_present sum>0"), StimuliG = **Obstacle (green)**.
  - Results: "blue-shaded interval marks sustained appetitive tracking" (`results.tex:128`), "red-shaded … aversive".
  - Ecuaciones: `eq:Z_17` (parada de aproximación) usa $Gpe_B - Ar$, y `eq:Z_13` (avance hacia el objetivo) suma $Gpe_B$: $B$ solo puede ser el apetitivo.
  - `eq:Z16`: $z_{14}$ (omnidireccional, el modo de evasión de obstáculos según `methodology.tex:66`) está excitado por $100\,G_{pe,y}$, que `methodology.tex:337` llama "apetitivo".
- **No verificado:** el código (`PETER_SIMULATION`) no está en esta máquina. **Requiere verificación contra el código** de qué letra es cada canal en las ecuaciones de gait-decision.
- **Corrección sugerida:** unificar con el código. Como mínimo, `methodology.tex:244` → "obstacle (Green), appetitive (Blue)" y `methodology.tex:290` → "compared to the obstacle (green) channel" (el peso $\omega_{Gpe_G\rightarrow X_4}$ es el del obstáculo, no del apetitivo). Revisar `methodology.tex:337` y explicitar la equivalencia x/y/z ↔ B/G/R.

### S-06 — Alta — "CPG" atribuido a la plataforma sin respaldo en el método
- **Ubicación:** `introduction.tex` (párrafo GPR: "For the rhythmic generation of the quadrupedal walking gait, the present platform integrates central pattern generators (CPGs)…"; "This combination of BG arbitration above and CPG execution below forms a hierarchical neural stack") y `conclusions.tex` párrafo 2 ("…integrating a directional sensory system with a central pattern generator modulated by stimulus type…").
- **Verificación:** `grep -i "CPG\|pattern generator"` en `methodology.tex` y `results.tex`: 0 coincidencias. `methodology.tex:526` describe la marcha como un crawl de secuencia diagonal **fija** en firmware, y `results.tex:1030` como "pre-configured open-loop control patterns". Ningún oscilador acoplado.
- **Por qué es alta:** un revisor que cruce la Tabla 1 (fila CPG) con el método verá una afirmación sin implementación. Además, la tabla de comparación horizontal sitúa el CPG como alternativa, no como parte del sistema.
- **Corrección sugerida:** Intro: "…the walking gait itself is executed by a fixed, firmware-level crawl pattern (Section~\ref{ssec:ServoCompensation}); feedback-modulated CPGs can arbitrate…, but the present design keeps that decision with the basal-ganglia stage…". Eliminar "CPG execution below". Conclusiones: "…with a stimulus-modulated locomotion network…".

### S-07 — Alta — Definición única de "success rate" contradicha en la misma tabla
- **Ubicación:** `results.tex:504`: "…and this is the only sense in which "success rate" is used anywhere in this paper" (misión con reintentos).
- **Verificación (texto):** el caption de `tab:fsm_comparison` (`results.tex:480`) dice que para Inspection, Rugged Terrain e Inclined Slope el N es de **intentos individuales**. La inspección es 17/20 intentos (`R3-05-inspection/data/*/inspection_summary.json`: 17 SUCCESS, 3 TIMEOUT, sin reintentos). La ablación es por ensayo (Fisher sobre 12 ensayos). El Abstract y los Highlights usan las dos definiciones juntas ("100% … in every three-stimulus conflict trial"; "85% vs 45%").
- **Corrección sugerida:** sustituir por "For the four scenario suites, success rate is mission-level (…); for Inspection, the terrain suites and the ablation study it is per attempt (Table caption)". Quitar "anywhere in this paper".

### S-08 — Alta — Qué modo se activa ante inestabilidad: Methodology se contradice con sus ecuaciones y con Results
- **Ubicación:** `methodology.tex:305`: "…additionally engaging the quadrupedal mode whenever gait stability is compromised, irrespective of stimulus".
- **Verificación (texto/ecuaciones):** `methodology.tex:68` ("on steeply inclined terrains the robot selects … differential rolling mode"). En `eq:Z16`, pitch y roll ($z_1$, $z_2$) excitan $z_{16}$ (differential), y solo $\sigma_{az}$ ($z_0$) excita $z_{15}$ (quadrupedal). `results.tex:225` y 240: en la pendiente se adopta differential rolling. Conclusiones, párrafo 4: "sustained tilt on the slope engaged differential rolling".
- **Corrección sugerida:** "…additionally overriding the stimulus-driven mode when terrain instability is detected: quadrupedal on rough terrain (high $\sigma_{az}$), differential rolling on steep tilt (pitch/roll above threshold)".

### S-09 — Media — `tab:consolidated_physical_metrics` dice "three hardware replicates each", pero varios valores corresponden a un único ensayo
- **Ubicación:** `results.tex:967`–976 (filas Obstacle y Complex).
- **Verificación:** `experiments/real/Stimuli{G}_t0*/combined_metrics.csv` y `MultiRGB_t0*`:
  - Obstacle Roll RMS máx. por ensayo: 4.2°, 9.9°, 12.0° (tabla: "Roll 3.5°"). Peak $Var(z)$: 1316, 684, 688 (tabla: "≈1100").
  - Complex $T_{switch}$: 0.15, 1.20, 1.05 s (tabla: "≈1.0–1.2 s", omite el 0.15).
  - Los valores encajan con el ensayo `t01`, que es el que dibujan las figuras (`real_plot_suite.py` toma `dirs[0]`).
  - La ventana "active response window" no está definida, así que Roll/Pitch no se pueden reproducir exactamente.
- **Corrección sugerida:** o la tabla resume las réplicas (rango entre réplicas), o el caption dice "representative replicate (first by index); ranges across the three replicates in parentheses". Lo mismo vale para el texto "consistent across all three replicates" (`results.tex:963`).

### S-10 — Media — Complex "peak ≈27× Obstacle **baseline**": es 27× el **pico** del Obstacle
- **Ubicación:** `results.tex:975`.
- **Verificación:** picos de `firing_variance` (`neural_metrics.csv`): MultiRGB 23 487 / 32 860 / 31 843; StimuliG 1 316 / 684 / 688. 31 843 / 1 100 ≈ 29 y 23 487 / 1 316 ≈ 18. El cociente sale contra el pico de Obstacle, no contra su línea base (mediana ≈ 0–130).
- **Corrección sugerida:** "peak ≈27× the Obstacle peak".

### S-11 — Media — Obstacle físico: "non-chromatic obstacle cue" es falso
- **Ubicación:** caption de `fig:obstacle_real_compound` (`results.tex:959`, texto tocado por C-76).
- **Verificación:** `experiments/real/MANIFEST.md`: el Obstacle físico es **StimuliG = estímulo verde** ("verified: red_present/blue_present near-zero"). El motivo real de que no haya sombreado es que solo se registran `red_present`/`blue_present` (docstring de `micro_dynamics.py`: "Obstacle, whose stimulus is green and doesn't fit the red/blue scheme").
- **Corrección sugerida:** "(no stimulus-presence shading: only red/blue presence is logged, and this scenario's cue is green)".

### S-12 — Media — "$N_{ev}^{X}$ … fewer than $N_{ev}^{LiDAR}$ … in every one of the 17 successful trials without exception": falso en 1 ensayo
- **Ubicación:** `results.tex:567`.
- **Verificación:** `experiments/R3-05-inspection/data/test_014_SUCCESS/inspection_summary.json`: `N_lidar_events = 4`, `N_mode_X_events = 4` (iguales, no menos). Los 16 restantes cumplen. El agregado 7.71 / 3.29 = 2.34 ✓.
- **Corrección sugerida:** "…in 16 of the 17 successful trials (equal in the remaining one)".

### S-13 — Media — F1 del MLP en la figura de comparación ≠ texto
- **Ubicación:** `results.tex:666`/699 y `fig:classifier_tradeoff`(a).
- **Verificación:** `_plotting/vectorized/classifier_fig5.csv` (extracción de la figura original, de donde se redibujó el panel (a)): MLP F1 = **0.734**, accuracy 0.730; Logistic F1 = **0.659**. El texto dice MLP F1 = 0.771 (CV) y LR = 0.692. SVM (0.857) y RF (0.947) coinciden a ±0.001, así que la extracción es fiable y la diferencia (~0.035) es real. El caption dice "mean of 5-fold stratified cross-validation".
- **Corrección sugerida:** el autor confirma de qué corrida sale el panel (a). Si es otra corrida, rehacer el panel con los valores de CV del texto o cambiar el caption. **Requiere los datos originales del clasificador**, que no están versionados.

### S-14 — Media — `tab:fsm_comparison`: "± … over each row's N trials" no es cierto en 6 filas
- **Ubicación:** caption, `results.tex:480`.
- **Verificación:** Task Time y Roll RMS solo existen para ensayos exitosos. Inspection/Neural: N = 20, pero 51.61 ± 11.96 es sobre los 17 exitosos (`R3-05-inspection/output/inspection_summary_stats.csv`: n = 17, SD muestral 12.33 = 11.96·√(17/16)). Obstacle/Neural: N = 15, pero estadísticos sobre 14 (exclusión). Rugged/Neural 50 % de 6 → 3; Rugged/FSM 60 % de 25 → 15; Slope/FSM 71.4 % de 21 → 15.
- **Corrección sugerida:** "…population standard deviations over each row's successful trials (N × SR; 14 for Obstacle/Neural after the exclusion)". No reabre C-74: solo corrige sobre qué n se calcula.

### S-15 — Media — Neural en terreno "solo sin perturbación": dos explicaciones incompatibles
- **Ubicación:** `results.tex:480` (caption: "the Neural controller was evaluated only without perturbation, hence its small N") vs. `results.tex:522` ("restricted to the zero-noise condition **to match the FSM runs**") vs. `methodology.tex:439` ("evaluated … under matching … noise levels").
- **Verificación:** requiere verificación con datos no versionados (`R2-02-fsm-baseline/data/`). En el texto, si el FSM también fuera solo a ruido 0, sus 25/21 intentos serían todos a nivel 0. Si no, "to match the FSM runs" es falso.
- **Corrección sugerida:** el autor dice qué niveles corrió el FSM en terreno, y se unifican las tres frases.

### S-16 — Media — λ denota dos métricas distintas
- **Ubicación:** `results.tex:476` (λ = "motor-command clarity ratio", columna de `tab:fsm_comparison`) vs. `results.tex:1052` (λ = "conflict-efficiency metric", excluida de la ablación por instrumentación).
- **Verificación:** texto. En los logs, `exp_lambda` (trial_summary) y `lambda_efficiency` (neural_metrics) son la misma columna. El paper le da dos definiciones.
- **Corrección sugerida:** una sola definición y un solo nombre. Si son la misma variable, explicar en Limitations por qué se reporta en la FSM y no en la ablación.

### S-17 — Media — Semilla fija vs. "a different dropout realization"
- **Ubicación:** `methodology.tex:434` ("All trials used a fixed base seed ($\mathit{NoiseSeed}=42$) to keep the injected noise realization reproducible across replicates and severity levels") vs. `results.tex:184` ("The retry at the identical severity level, drawing a different dropout realization…").
- **Verificación:** texto. Con una semilla idéntica, el reintento sacaría la misma realización. Requiere verificación con datos no versionados (R3-04) de cómo se deriva la semilla por ensayo.
- **Corrección sugerida:** "a fixed base seed, offset per trial index" (si es así), para que ambos pasajes sean compatibles.

### S-18 — Media — Umbral de parada $Ar$: % de ancho horizontal vs. "bounding-box area units"
- **Ubicación:** `methodology.tex:288` ($Ar$ = 28 = % del **ancho horizontal** de la imagen) vs. `table:PerturbationParams` (`methodology.tex:429`: "Approach-stop area threshold … 28, 24, 20, 18, 14 (bounding-box **area** units)").
- **Problema:** dos definiciones de la misma magnitud. Además, la tabla de perturbaciones baja el umbral del controlador con la severidad, es decir, cambia un parámetro del controlador y no del sensor, y eso no se explica.
- **Corrección sugerida:** unificar la unidad y añadir una frase: "the approach-stop threshold is lowered with severity to compensate the area bias, so that…".

### S-19 — Media — Estabilidad del crawl: "guaranteeing static stability throughout" vs. SM negativo en la tabla
- **Ubicación:** caption de `fig:stability_phases` (`results.tex:357`) y `results.tex:334`–337 vs. `tab:crawl_stability` ($SM_{min} = -0.015$ m, $TR_{max} = 1.173$).
- **Problema:** por definición, SM < 0 significa CoM fuera del polígono, o sea, estáticamente inestable en ese instante. La tabla lo admite ("transient"), pero el caption dice "guaranteeing static stability throughout the gait".
- **Corrección sugerida:** "…providing a non-degenerate support polygon at every instant; brief transfer-phase extremes (two samples) fall marginally outside it (Table~\ref{tab:crawl_stability}) without causing a tip-over".

### S-20 — Media — "two transfer sub-phases per limb" no cuadra con un ciclo de seis fases
- **Ubicación:** `results.tex:339`–341.
- **Problema:** 4 patas × 2 sub-fases de transferencia = 8 > 6. El caption habla de "the two phases marked body shift", así que quedan 4 de transferencia: una por pata.
- **Corrección sugerida:** "four transfer sub-phases (one per limb), interleaved with two body-shift sub-phases".

### S-21 — Media — "$X_{15}$/$X_{16}$" usados como neuronas de la capa de entrada en el físico
- **Ubicación:** `results.tex:597`, 606 y 622 ("input-layer neurons $X_{15}$/$X_{16}$ activate first, indicating the obstacle on the front-right").
- **Verificación:** `_plotting/vectorized/neu_est_unig_real.csv`: el panel "Input" tiene neuronas 1–16 (las 16 del anillo / capa de entrada $I_n$). En el resto del paper, $X_{15}$ es la unidad de modo cuadrúpedo y $X_{16}$ la de differential rolling (`results.tex:117`, `eq:Z16`).
- **Corrección sugerida:** "input-layer units $I_{15}$/$I_{16}$" (o la notación de `eq:InputL`).

### S-22 — Media — "Panel A achieves an instantaneous step response"
- **Ubicación:** `results.tex:1025`.
- **Problema:** el propio caption da μ = 0.184 s para el panel A. Llamarlo "instantaneous" al lado de un valor de 184 ms es una contradicción visible (el que es determinista es la *dispersión*: SD ≈ 1.4 ms en `pitch_latency.csv`).
- **Corrección sugerida:** "a tightly clustered response (≈184 ms, SD ≈ 1 ms)".

### S-23 — Media — "≈5°" de reenganche cuadrúpedo sin origen
- **Ubicación:** `tab:terrain_sequence`, fila 4 (`results.tex:811`): "Pitch disturbance stays below quadrupedal re-engagement threshold ($\approx 5^{\circ}$)".
- **Verificación:** no aparece ningún umbral de 5° en `methodology.tex` (`U_{Pitch} = U_{Roll} = 15°`, `table:Locom_NN`).
- **Corrección sugerida:** citar el umbral real de la tabla de parámetros, o quitar la cifra.

### S-24 — Media — Ecuaciones de la red integradora con índices inconsistentes
- **Ubicación:** `methodology.tex:142`–145.
- **Problema:**
  - `eq:InputL`: $dI_n/dt = (-I_n + Z_i)$ mezcla los índices $n$ e $i$.
  - `eq:ResL`: la respuesta suma $W^{(IR)}_{n,i}\,A_i$ (salida *auxiliar*), aunque el texto dice "cross-connections between the input and response layers"; debería ser $I_i$.
  - `eq:L4`: $\sum_{r=0}^{15} A_n$ suma sobre $r$ un término en $n$.
  - Los pesos de la tabla ($W_{Z\rightarrow I}$, $W_{I\rightarrow R}$, $W_{R\rightarrow A}$, $W_{A\rightarrow L_4}$) no son los de las ecuaciones ($W^{(IR)}$, $W^{(RR)}$, $W^{(RA)}$).
- **Corrección sugerida:** $Z_n$ en `eq:InputL`, $I_i$ en `eq:ResL`, $A_r$ en `eq:L4`, y un solo juego de nombres de matrices.

### S-25 — Media — Conclusiones atribuye la robustez por sensor cuando el paper dice que no se puede
- **Ubicación:** `conclusions.tex`, penúltimo párrafo: "retained task-level performance under combined IMU-drift and LiDAR-noise perturbation, and, conditionally on the scenario, camera illumination distortion…, evaluated jointly rather than as isolated single-sensor degradations".
- **Problema:** la frase reparte el resultado por sensor (IMU/LiDAR sí, cámara "condicionalmente") en la misma oración que reconoce que no se aislaron. Contradice las notas R2b-02/R3b-03 que pidieron los revisores.
- **Corrección sugerida:** "…retained task-level performance under the combined perturbation in most scenarios (failures concentrated in Appetitive timeouts and Rugged Terrain tipovers), evaluated jointly rather than per sensor".

## 1.2 Redundancia (texto viejo vs. nuevo)

### S-26 — Media — La misma misión física de 15 ensayos se describe dos veces sin referencia cruzada
- `results.tex:798`–818 (pista de 4 segmentos, "15 continuous repetitive trials") y `results.tex:1025` ("continuous multi-terrain navigation mission … across 15 hardware replicates", subida → rolling, terreno rugoso → cuadrúpedo). Ninguno remite al otro. **Sugerencia:** en 1025, "the 15-trial compound-terrain mission of Table~\ref{tab:terrain_sequence}". Ver también S-04: si los paneles A/B son del banco de pitch, no son "esta" misión.

### S-27 — Baja — Interpretación del Pitch RMS de la ablación, dos veces
- Caption (b) de `fig:ablation_combined` (`results.tex:211`) y prosa `results.tex:215`: la misma frase "plausibly reflecting reduced net locomotor activity in trials that fail outright rather than improved attitude control". C-60 quitó las cifras duplicadas, pero no esta frase. **Sugerencia:** dejarla solo en la prosa.

### S-28 — Baja — Caveat de equidad FSM: seis apariciones
- Caption de la tabla, 3 captions de figuras (pedido por R2b-03), `results.tex:522` (párrafo completo) y `methodology.tex:439`. Las cuatro de caption son las que pidió el revisor; el párrafo `results.tex:522` repite íntegro el caption de la tabla. **Sugerencia:** reducir 522 a "…$T_{switch}$/$T_{response}$ are omitted for the reasons given in the Table caption" y conservar solo la frase sobre el tamaño muestral.

### S-29 — Baja — "Neural values match Table consolidated" dicho dos veces
- `results.tex:130` ("these are the same trials as the corresponding four basal-ganglia rows of Table fsm") y `results.tex:524`. **Sugerencia:** borrar 524.

## 1.3 Candidatos a acortar

### S-30 — Media — `tab:consolidated_physical_metrics` + 4 párrafos + 4 captions dicen lo mismo
- Cada escenario físico tiene un caption de figura con la descripción cualitativa, un párrafo que la repite y una fila de tabla con lo mismo ("Dual-peak (detection + retreat-FOV)", "Three-phase"). **Propuesta:** dejar la tabla como único sitio de las cifras (corregidas por S-03/S-09), reducir cada caption a "(a) ECDF of $T_{switch}$; (b) $Var(z)$ and Roll/Pitch RMS; see Table~X", y dejar en la prosa solo la interpretación mecánica. Ahorro estimado: ~250 palabras. No se pierde información.

### S-31 — Baja — `tab:mode_steady_state_energy` (3 filas) cabe en una frase
- La fila Omnidireccional es N = 1. **Propuesta:** integrar en la prosa ("2.73 ± 2.29 W (C, 20 segments), 1.13 ± 1.08 W (H, 20), 5.71 ± 0.73 W (X, a single 38.6 s segment)") y quitar la tabla. Opcional: R2.4 pidió el dato, no la tabla.

### S-32 — Baja — Caption y prosa de `fig:FourPanelLatencies` repiten la descripción de los cuatro paneles
- `results.tex:1021` (caption con los 4 μ) y `results.tex:1025` (prosa que recorre A–D). **Propuesta:** dejar los μ solo en el caption y que la prosa interprete.

## 1.4 Ortografía y convenciones

### S-33 — Media — Nombres de autor inconsistentes entre la portada y CRediT
- Portada (`preamble.tex:64`–71): "Carlos-Rodríguez", "Caro-Vaca", "Caicedo-Samboní", "Grajales-Pulgarín", "Ramírez-Moreno". CRediT (`conclusions.tex`): "Carlos Rodriguez" (sin guion ni tilde), "Caro Vaca", "Caicedo Samboni", "Grajales Pulgarín", "Ramirez-Moreno". El orden también cambia (Grajales antes que Caicedo). **Sugerencia:** copiar exactamente la forma de la portada.

### S-34 — Media — "Differential Mobile" (en figuras) vs. "Differential Rolling" (texto)
- Visible en `FigReal_Terrain_Latencies_4Panels.png` (los cuatro títulos de panel) y `FigReal_Morphological_Transition_Energy.png` (etiquetas del eje x). El texto y las tablas dicen siempre "Differential Rolling". **Sugerencia:** regenerar ambas con "Differential Rolling" (es la misma familia que C-72).

### S-35 — Baja — Color azul fijo fuera de `\revblue{}`
- `methodology.tex:165` y `methodology.tex:231` (`\textcolor{blue}{…}` dentro de ecuaciones) y `methodology.tex:462` (`\color{blue}` en `table:HardwareParams`). `strip_revblue.py` no los convierte, así que quedarán azules en la ronda siguiente. **Sugerencia:** `\revblue{}`.

### S-36 — Baja — "intact circuit" vs. "full"
- `results.tex:215` ("for \emph{full}") y `methodology.tex:198` ("(\emph{full}, control)"); en el resto se usa "intact circuit". **Sugerencia:** "intact circuit" en todo el texto.

### S-37 — Baja — Tipografía menor
- `results.tex:455`: "Figures~\ref{fig:variable_topo_metrics}" con una sola referencia → "Figure".
- `results.tex:713`: "1.2cm" → "1.2~cm".
- `results.tex:296`: doble espacio y puntuación en "for  Rugged Terrain, upper panel and Inclined Slope, lower panel" → "for Rugged Terrain (upper panel) and Inclined Slope (lower panel)".
- `introduction.tex`: "\citet{Liu2024Max},  \citet" (doble espacio).
- Mezcla británico/estadounidense: "artefact" (`results.tex:396`) vs. "artifact" (`results.tex:219`); "summarises" (`results.tex:342`) vs. "summarizes". El resto del texto es estadounidense.
- `results.tex:1052`: "(Section~\ref{sec:results})" para referirse a la ablación → `\ref` a la subsubsección (no tiene `\label`; habría que añadirlo).
- `methodology.tex:526`: "The crawl gait described in Section~\ref{ssec:Gait_Decision_Module}": esa sección no describe el crawl → `ssec:ServoCompensation`/`sssec:transition_stability`.
- `results.tex:320`: "$0.2$–$0.7$ ms … (a single discrete update cycle of the ROS 2 Control loop operating at 3.3 kHz)": a 3.3 kHz un ciclo dura 0.3 ms, así que 0.7 ms son dos o tres ciclos. **Sugerencia:** "one to two update cycles".
- `results.tex:320`: "the threshold-based basal ganglia selection logic" choca con todo el argumento de la ablación (BG ≠ umbral). **Sugerencia:** "the basal-ganglia selection logic".

### S-38 — Baja — Intro (iii) "autonomous energy-aware mode selection" vs. Conclusiones
- La selección de modo no usa ninguna entrada energética. Las Conclusiones ya lo formulan bien ("autonomous mode selection that exploits the efficiency of wheeled locomotion… with the energy cost… measured"). **Sugerencia:** alinear la Intro con esa redacción. En la misma línea, la Intro dice "A multilayer perceptron (MLP) processes sensory data to … compute per-channel salience inputs to the basal-ganglia network", pero el MLP alimenta el gait-decision module ($X_0$/$X_1$, `methodology.tex:376`), no la saliencia de los ganglios basales, cuyas entradas son visuales (`methodology.tex:162`). Esto último lo subiría a media.

## 1.5 Calcos del español e inglés no idiomático

### S-39 — Baja — Lista localizada
| Ubicación | Texto | Sugerencia |
|---|---|---|
| `results.tex:713` | "around second 86" | "at $t \approx 86$ s" |
| `results.tex:753` | "before second 46" | "before $t \approx 46$ s" |
| `results.tex:584` | "Complementarily, the experiments…" (*complementariamente*) | "The physical experiments reproduced…" |
| `results.tex:587` | "(approach, a, appetitive; evasion, b, obstacle; and escape, c, aversive)" | "(a) approach to the appetitive stimulus, (b) obstacle evasion, (c) escape from the aversive stimulus" |
| `methodology.tex:43` | "emulating the embedded knowledge required for detecting anomalies" | "standing in for the anomaly and hazard cues an inspection task would target" |
| `methodology.tex:76` | "the tank neurons of the integrator stage" | "the integrator neurons" |
| `results.tex:225` | "according to the previously defined behaviors" (muletilla) | "per the stimulus-mode mapping" |
| `results.tex:917` | "high-speed backward flight", "near-zero computational ticks" | "rapid backward retreat"; eliminar "ticks" |
| `results.tex:1025` | "partitioned into a four-panel layout to preserve resolution against low statistical variance" | "shown in four panels so each narrow distribution remains readable" |
| `introduction.tex` (párrafo GPR) | "This distinction and its subsequent computational formulation" (no hay distinción previa) | "This computational formulation" |
| `conclusions.tex` (último párr. de resultados) | "decisions can be taken for such resource-constrained platforms" | "can be made for…" |
| `methodology.tex:162` | "guarantees the effective selection of one type of stimulus" | "selects a single stimulus channel" |

## 1.6 Texto tocado en las últimas 48 h (C-76, C-73, C-70–C-72)

Revisé uno por uno los 64 reemplazos de C-76 (`git show 1b708f2 --word-diff`). La gran mayoría quedó bien. Problemas:

### S-40 — Media — Frases de C-76 con puntuación doble o referente ambiguo
| # C-76 | Ubicación | Problema | Sugerencia |
|---|---|---|---|
| 23 | caption `fig:noise_robustness_extra_combined` (c), `results.tex:176` | **Dos dos puntos** en una frase: "…under camera illumination distortion: a failed attempt (timeout) and its successful retry at the same severity level: the failed attempt's…" | "…distortion (a failed attempt and its successful retry at the same level): the failed attempt's…" |
| 09 | `introduction.tex`, párrafo GPR | "…distributed across the oscillator network, a property advantageous for diagnosing…": "a property" parece referirse a la red distribuida, que es justo lo que se descarta | "…oscillator network; a single locus is advantageous for diagnosing…" |
| 56 | `results.tex:622` | "keeps $X_{16}$ active and uninhibited by $X_{15}$, the no-motor-action state shown in…": parece que $X_{15}$ es el estado | "…uninhibited by $X_{15}$, which produces the no-motor-action state shown in…" |
| 51 | `results.tex:567` | "…the mode-dithering a simple threshold-triggered controller would exhibit, the mechanism underlying the reactive re-routing": aposición colgante | "This conversion is the mechanism underlying…" (frase nueva) |
| 52 | `results.tex:569` | "…resuming automatically once the obstacle clears, the system's re-acquisition-like behavior." | "…clears; this resumption is the system's re-acquisition-like behavior." |
| 01 | `conclusions.tex` (última frase) | "…aligned with current standards, evolving the platform…": gerundio sin sujeto claro | "…standards, so as to evolve the platform…" |

**C-73:** las marcas "Simulation data." / "Physical-robot data." están bien. Solo tengo la duda de S-11 (el "non-chromatic" del Obstacle físico, que es texto de C-76 en un caption que C-73 no tocó).

**Figuras regeneradas (C-70–C-72, vistas en `assets/`):**
- `FigReal_Morphological_Transition_Energy.png`: la **nota al pie está cortada por los dos bordes** ("wer = |current| x 7.2 V … not an inferred pe"). Las barras de error son SD **poblacional** (2.84 / 1.16, `np.std` en el builder), mientras que el texto y el caption dan la muestral (2.93 / 1.19). Media: ajustar `rect`/ancho y usar `ddof=1`, o declarar el tipo de SD en el caption.
- `FigReal_Terrain_Latencies_4Panels.png`: la leyenda "Hardware Replicates (reconstructed)" deja a la vista un término interno, y cada panel muestra 8–12 escalones, no 15 (ver S-04). Además, "Differential Mobile" (S-34).
- `Appetitive_Real_Plot_1_Switching_Delay_ECDF.png`: el título lleva un **em dash** ("Appetitive—Switching Delay ECDF"), lo mismo que C-76 quitó de la prosa; probablemente afecta también a los otros tres ECDF físicos. Baja: "Appetitive: Switching Delay ECDF". Cuatro escalones = cuatro ensayos (el caption dice tres: pregunta abierta, no la reabro).

---

## Verificaciones que salieron bien (para la consolidación)
- `tab:consolidated_simulation_metrics`: las 12 celdas se reproducen desde `experiments/simulation/*/test_*SUCCESS/trial_summary.json` con SD poblacional (Appetitive 38.516 ± 1.203 / 0.536 ± 0.009 / 1.067 ± 0.003; Complex 24.962 ± 10.355 …).
- Variable topography: $T_{response}$ = 0.0 en los 30 ensayos ✓; rugged $T_{switch}$ 0.2–0.7 ms en 13/15 y 2 colas ≈0.6 s ✓; slope 0.9–1.8 ms ✓; μφ/μθ 1.586/1.666 y 1.469/2.290 ✓; punto medio 1.98° ✓.
- Conflicto Neural en Complex: 0.222 s/ensayo, 1.65 % (media de cocientes) ✓ con "≈0.2 s (1.7 %)".
- Inspección: SR 17/20, $d_{final}$, grupos 12/5, rangos 4–7 y 11–28, timeouts con 18/27/33 eventos ✓ (`R3-05-inspection/data` y `output/*.csv`).
- Energía: N = 16/19, medias, Welch t ≈ 1.18 ✓; estado estacionario 2.73/1.13/5.71 W, N segmentos 20/20/1 ✓ (`R2-04-mode-energy/output/mode_energy_stats.csv`); 5.71 W × 38 s ≈ 217 J ✓.
- MLP: F1 del test = 2PR/(P+R) = 0.824 ✓; los conteos implícitos de la matriz de confusión cuadran con accuracy 0.800 y n = 120; latencias 23.5/1.64 = 14× y 41.0/1.64 = 25× ✓.
- $Ar$ = 28: 554·10/31 = 178.7 px; 178.7/640 = 27.9 % ✓. Perlin: σ² = 5.469 ↔ σ = 2.339 ✓.
- Ablación: las 9 y 8 fallas de 12 (25 %, 33.3 %) y el umbral de Fisher (≥ 5 fallas) ✓.

## Sin poder verificar (datos no versionados o código ausente)
- S-05 (letras de canal en el código), S-13 (corrida del clasificador), S-15 (niveles de ruido del FSM en terreno), S-17 (derivación de la semilla).
- Las bandas del caption (b) de `fig:noise_robustness_extra_combined` (Roll 1.65–1.9°, Pitch 2.3–5.7°) y las 8 volcaduras / 4 choques de 27 intentos: `R3-04-noise-robustness/data/`.
- `table:PerturbationParams`: la severidad de iluminación es 0.30 en los niveles 3 **y** 4. Puede ser deliberado (el umbral de área sí cambia), pero conviene confirmarlo en el código.
