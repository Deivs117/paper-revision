# Auditoría final ronda 2 — Sebas (2026-11-03)

Fila `C-80`. Brief: `intake/pending/final_audit_round2_2026-11-02.md`. Pasada de **hallazgos**, sin
editar `sections/*.tex`. Orden de lectura: `introduction.tex` + `conclusions.tex`, luego preámbulo,
`methodology.tex`, `results.tex` completos. Base: `main` @ `adca90e`.

Recomputado con Python stdlib (sin venv) desde `experiments/simulation/`, `experiments/real/`,
`experiments/R3-05-inspection/data/`, `experiments/R2-04-mlp-onboard-compute/output/`. Lo que cae en
`R3-04-noise-robustness/data/` o `R2-02-fsm-baseline/data/` va marcado como *requiere verificación
con datos no versionados*.

**Revisión adversarial aplicada.** Un segundo revisor independiente intentó refutar cada hallazgo:
releyó el `.tex`, recalculó los datos y cruzó cada punto con `PROGRESS.md` e `intake/`. Este
documento recoge solo lo que sobrevivió, con sus enmiendas, más 3 hallazgos nuevos que el revisor
verificó (N-1 a N-3). Lo descartado y el motivo están al final.

Las líneas citadas se refieren a `sections/<archivo>.tex` en `adca90e`.

**Resumen:** 9 de prioridad alta, 21 media, 21 baja. 3 descartados. Lo más urgente es A-1 a A-5,
N-1 y N-2: el `.tex` o los datos versionados los contradicen directamente.

**Dependencia abierta:** en los 96 intentos de `experiments/simulation/`, `final_metrics.noise_idx`
vale 0. Esto ya está documentado como hallazgo abierto en
`intake/pending/C-75_fig20_restore_and_simulation_noise_audit_2026-11-01.md` §2. Lo que dependa de
que esa batería tuviera ruido por niveles (M-2 y la frase "σ = 0, 5, 10, 20, 30%" de
`results.tex:320`) queda subordinado a que se resuelva C-75 §2.

---

## 1.1 Inconsistencias de datos

### A-1 · ALTA · `results.tex:569` (`sssec:reactive_inspection`): "el robot se quedó en H los 20 ensayos" es falso
- **Problema:** dice *"The robot remained in the wheeled/differential locomotion mode (H) throughout
  all 20 trials"*. Contradice la propia tabla `tab:inspection_metrics`, que cuenta
  $N_{ev}^{X}$ = 1–10 cambios a modo omnidireccional por ensayo.
- **Verificación:** columna `mode` de `metrics_raw.csv` en los 20 ensayos de
  `R3-05-inspection/data/`. Los 20 registran modo X: entre 390 y 1874 muestras, el **41–87 %** del
  total. También registran ~10 muestras de C al arranque (índices 0–11). Ningún ensayo está solo en
  H. El campo `trial_summary.json → mode` es el modo **final** (H en 19/20). Lo más probable es que
  la frase saliera de leer ese campo.
- **Corrección sugerida:** *"The robot alternated between differential rolling (H) and
  omnidirectional (X) modes in every trial (Table~\ref{tab:inspection_metrics}, $N_{ev}^{X}$), with
  only a brief quadrupedal start-up stance; no static-stability (TR) logs were recorded for this
  task."* Los 20 `stability_log.csv` de esta tarea solo tienen cabecera, así que la consecuencia
  "no stability data" es cierta, pero por esa razón y no porque el robot no cambiara de modo.

### A-2 · ALTA · `results.tex:567`: "$N_{ev}^{X} < N_{ev}^{LiDAR}$ in every one of the 17 successful trials without exception" es falso
- **Verificación:** en `inspection_summary.json`, `test_014_SUCCESS` tiene `N_lidar_events = 4` y
  `N_mode_X_events = 4` (cociente 1.0). En los otros 16 el cociente va de 1.25 a 5.0. La media
  7.71/3.29 = 2.34 sí cuadra con el "≈2.3×".
- **Problema adicional (argumento):** `results.tex:535` dice que $N_{ev}^{X}$ va *"gated by a 3 s
  dwell-time hysteresis"*. `N_mode_X_events` coincide exactamente, ensayo a ensayo, con las entradas
  a X del flujo `mode` registrado. La histéresis es la del **controlador** (`min_dwell_time`), no un
  filtro de la métrica. Aun así, parte de la reducción la impone ese tiempo mínimo y no solo la
  arbitración WTA, que es a quien el párrafo se la atribuye.
- **Corrección sugerida:** "in 16 of the 17 successful trials (equal in the remaining one)", más:
  "…the reduction partly reflects the controller's 3 s minimum dwell time, not only the WTA
  arbitration."

### A-3 · ALTA · `results.tex:296` (caption de `fig:stability_profile`): "No trial violated this limit across all 30 runs" es falso por ensayo
- **Verificación:** alineé cada `stability_log.csv` al primer cambio de `mode` en `metrics_raw.csv`
  (mismo criterio que `_plotting/loaders.py::load_stability_log_aligned`), con la ventana que
  grafica la figura (−5 a +10 s). Terreno rugoso, `test_005_SUCCESS` y `test_006_SUCCESS`: 11
  muestras cada uno con TR > 1 (unas 6 seguidas a 1.86, ≈0.3 s, más 5 a ~1.01), máximo **1.862**.
  Todas son anteriores a t = 0, en modo C y con `leg_in_air`. Fuera de la ventana también hay TR > 1
  en pendiente: 1.662 (`test_002`) y 1.622 (`test_015`). La media sí queda por debajo de 1. En el PNG
  regenerado, la banda ±1σ de rugoso se sale del eje (ylim ≈ 1.15) justo en ese pico.
- **Contradicción interna relacionada:** `results.tex:317` define TR = 1 como *"the critical
  overturning threshold"* y el caption lo llama *"physical overturning boundary"*. En cambio,
  `tab:crawl_stability` reporta TR máx. = 1.173 en marcha normal y `results.tex:396` dice que pasar
  de TR = 1 es *"an artefact"* que *"do[es] not result in physical instability"*.
- **Corrección sugerida:** "The mean profile stays below this limit; two rugged-terrain trials
  briefly exceed it (TR ≤ 1.86 for ≈0.5 s, before the switch, during foot-lift phases of the
  quadrupedal gait) without tipping over." Cambiar "physical overturning boundary" por "nominal
  static-stability limit". Opcional: subir el ylim para que la banda no se corte.

### A-4 · ALTA · `results.tex:701`: memoria del ESP32-S3 mal referida (30.4 % "of the board's 4 MB partition", "~47k-parameter")
- **Verificación:**
  - `R2-04-mlp-onboard-compute/output/onboard_compute_results.txt:85`:
    `Flash: 30.4% (used 397829 bytes from 1310720 bytes)`. El 30.4 % es de la partición de
    aplicación de 1.25 MB; sobre 4 MB sería el **9.5 %**.
  - Los arrays de `mlp_weights.h` suman **32,642 parámetros** (W1 20250 + 150 + W2 12000 + 80 +
    W3 160 + 2). La propia Fig. `classifier_tradeoff`(c) da 32,489
    (`_plotting/vectorized/classifier_fig6.csv:9`). Los "~47k" parecen salir de la fila SVM (45,916).
  - Son ~130 KB en float32. El resto de los 398 KB es sobre todo el framework Arduino/ESP-IDF, así
    que "almost entirely the model itself" es falso.
  - El error viene del propio txt de resultados (líneas 106–117).
- **Corrección sugerida:** "397,829 B flash (30.4% of the 1.25 MB application partition; the
  ≈32.6k-parameter model accounts for ≈130 KB of it)". Corregir también el txt de `experiments/`.

### A-5 · ALTA · `methodology.tex:244` + `:290` + `:337`: mapeo color ↔ canal contradice las ecuaciones y los datos
- **Problema:** `:244` dice *"$Gpe_B$, $Gpe_G$, $Gpe_R$ … obstacle (Blue), appetitive (Green),
  aversive (Red)"*, y `:290` lo repite (*"aversive (red) … appetitive (green) channel"*).
- **Verificación:**
  - **Las ecuaciones:** $z_{17} = (Gpe_B - Ar)_+$ es la parada de aproximación y $z_{13}$ recibe
    $+Gpe_B$, así que **B = apetitivo**. $z_4 = Gpe_G + 2Gpe_R$, junto con `results.tex:45`
    (*"obstacle-associated GPe activation triggers unit $X_4$"*), da **G = obstáculo**.
  - **Los datos:** `simulation/familia_a_apetitivo/test_001_SUCCESS/trial_summary.json` da
    `bb_blue = 41700`, `bb_green = 0`. En `experiments/real/MANIFEST.md`, `StimuliB` = Appetitive y
    `StimuliG` = Obstacle.
- **Corrección sugerida:** `:244` → "…for the appetitive (Blue), obstacle (Green), and aversive (Red)
  behavioral channels". `:290` → "compared to the obstacle (green) channel" (o el que corresponda:
  confirmar con el autor). Revisar también $G_{pe,y}$, $G_{pi,x}$, $G_{pi,z}$ (`:337`).
- **Advertencia:** aun corrigiendo esto, $z_{15}$ (+2$z_3$, apetitivo) y $z_{14}$ (100 $G_{pe,y}$)
  no encajan con "appetitive → rolling". Ver M-1; hace falta el autor de las ecuaciones.

### A-8 · ALTA · `methodology.tex:305` vs `:68` + ecuaciones: qué inestabilidad dispara qué modo
- **Problema:** `:305` dice que el módulo *"additionally engag[es] the quadrupedal mode whenever gait
  stability is compromised, irrespective of stimulus"*. Pero `:68`, `results.tex:240` y
  `conclusions.tex:10` dicen que la inclinación sostenida activa la **rodadura diferencial**.
- **Verificación:** en las ecuaciones solo $z_0$ ($\sigma_{az}$) entra en $z_{15}$ (cuadrúpedo,
  $+20z_0$). $z_1$ y $z_2$ (pitch/roll) entran en $z_{16}$ (rodadura, $+0.7z_1 + 0.7z_2$).
- **Corrección sugerida:** "...engaging the quadrupedal mode when vertical-acceleration variability
  ($\sigma_{az}$) exceeds its threshold, and differential rolling when sustained pitch/roll does,
  irrespective of stimulus."

### A-9 · ALTA · `results.tex:894`: Apetitivo físico atribuido a la marcha cuadrúpeda
- **Problema:** *"The cyclic Roll/Pitch oscillations stem from body-shaking during the rhythmic
  weight-shifting quadrupedal gait"*. El apetitivo usa rodadura diferencial por diseño
  (`methodology.tex:66`).
- **Verificación:** columna `mode` de `real/StimuliB_t01..t04/neural_metrics.csv`: H en el 92–96 %
  de las muestras; C solo 8–19 muestras al arranque.
- **Corrección sugerida:** atribuir las oscilaciones a la rodadura diferencial sobre el suelo (o a
  la fase de arranque en C).

### N-1 · ALTA · `introduction.tex:34`: función del MLP mal descrita *(hallazgo del revisor)*
- **Problema:** *"A multilayer perceptron (MLP) processes sensory data to detect terrain instability
  and compute per-channel salience inputs to the basal-ganglia network"*.
- **Verificación:** contradice `methodology.tex:4` ("MLP terrain-instability detector"), `:172`
  ($\text{Stimuli}_i$ = "sensory drive from visual processing") y `:375` (el MLP solo alimenta
  $X_0$/$X_1$ del gait-decision, y solo en hardware). El MLP no calcula saliencias para los ganglios
  basales.
- **Corrección sugerida:** "A multilayer perceptron (MLP) classifies terrain from inertial data on
  the physical platform and feeds the gait-decision module, while the basal-ganglia network
  arbitrates among camera- and LiDAR-driven behavioral channels."

### N-2 · ALTA · `results.tex:608`: figura equivocada y neuronas inactivas *(hallazgo del revisor)*
- **Problema:** *"at ≈23 s, neurons $X_5$/$X_7$ (Figure~\ref{fig:NEU_EST_UNIG_real}b) drive a
  leftward orientation correction via $X_{11}$"*.
- **Verificación:** lectura del PNG. `NEU_EST_UNIG_real` es el ensayo de **obstáculo** (caption:
  "single obstacle stimulus"). En su panel b, $X_5$/$X_7$ no tienen actividad y no pasa nada a
  ~23 s: la actividad empieza en ~39 s, en X4/X6/X8/X9/X11/X12. En `assets/` no hay ningún raster
  del apetitivo real.
- **Corrección sugerida:** el autor indica la figura correcta, o se quitan la referencia y la
  afirmación sobre $X_5$/$X_7$.

### A-6 · MEDIA · `results.tex:320`: "sub-millisecond in the vast majority of trials" exagera
- **Verificación:** `tswitch` en `trial_summary.json`. Rugoso: 13/15 entre 0.2 y 0.7 ms, 2 en
  ~0.6 s. Pendiente: [0.9 ×3, 1.0 ×8, 1.1 ×2, 1.3, 1.8] ms, o sea **12/15 ≥ 1.0 ms**. En total,
  16/30 por debajo de 1 ms. El caption (`:303`) ya dice "majority" y el párrafo da los rangos, así
  que es una sobreafirmación y no un dato falso.
- "A single discrete update cycle ... at 3.3 kHz" da ≈0.3 ms por ciclo, así que el rango 0.2–0.7 ms
  abarca hasta ~2 ciclos.
- **Corrección sugerida:** "sub-millisecond on rugged terrain in 13 of 15 trials and 0.9–1.8 ms on
  the inclined slope".

### A-7 · MEDIA (confirmación del autor) · `results.tex:1021`, `:1025`, `methodology.tex:196`: trazabilidad de las latencias físicas 184/534 ms
- **Verificación:** `real/Imu_pitch_test_t01/pitch_latency.csv` (prueba de banco, pitch alternado
  12°/0°) da 184.8 ms (SD 1.4) y 534.9 ms (SD 0.3) con N = 12 + 12 válidos. Pero
  `_plotting/vectorized/README.md:34` dice que la figura original tenía N = 15 por panel, y los
  paneles C/D (2.92 s / 1.56 s) no tienen equivalente en ese fichero. Por eso **no está probado que
  el texto sea falso**: la fuente real puede ser otra que no está en el repo.
- **Lo que hay que confirmar:** si la fuente es la prueba de banco, entonces sobran "15 hardware
  replicates" y "triggered by wheel slippage" (en el fichero la dispara el pitch volviendo a 0°).
  Si es una misión de 15 réplicas, archivar sus datos. Detalle menor: 184.8 redondea a 185.

### M-1 · MEDIA · `results.tex:597`, `:606`, `:622` vs `:45`, `:117`: $X_{15}$/$X_{16}$ con dos significados
- En `:45`/`:117` y en las ecuaciones son unidades de modo. En `:597`/`:606`, *"input-layer neurons
  $X_{15}$/$X_{16}$ activate first"*, son neuronas de la capa de entrada LiDAR. El panel "Input" de
  `NEU_EST_UNIG_real` las rotula 15/16 sin "X". `:622` vuelve al sentido de modo.
- Con las ecuaciones como están, la correspondencia unidad ↔ modo ↔ canal de `:117` no se puede
  reconstruir. Ligado a A-5.
- **Corrección sugerida:** en `:597`/`:606`, usar la notación propia de la capa de entrada ($I_n$).
  Revisar las ecuaciones junto con A-5.

### M-2 · MEDIA · `results.tex:504` + caption `:509`: "at the noisiest levels" / "retry at intermediate/high noise"
- **Verificación:** intentos por misión por `noise_level_idx` (mismo cálculo que
  `build_attempts_vs_nl.py`). Apetitivo: {0: 1.33, 1: 1.00, 2: 1.33, 3: 1.67, 4: 1.00}. Aversivo:
  {0–2: 1.00, 3: 1.33, 4: 1.33}. El nivel más ruidoso no tiene el máximo y el nivel 0 necesita un
  reintento.
- **Pero:** `final_metrics.noise_idx` = 0 en todos los intentos (ver "Dependencia abierta"). Puede
  que ningún nivel tuviera ruido. **No proponer texto nuevo** hasta resolver C-75 §2, que ya cita
  esta misma frase.

### M-3 · MEDIA · `results.tex:1052` vs `:476`: el símbolo λ tiene dos definiciones
- `:476` la define como *"motor-command clarity ratio (commanded-velocity magnitude relative to
  neural activity norm)"* y `tab:fsm_comparison` la reporta (0.73–1.00). `:1052` la define como
  *"conflict-efficiency metric ... only registers active conflict when two specific channels are
  simultaneously present ... rarely met"* y la excluye de la ablación.
- **Corrección sugerida:** unificar la definición o usar símbolos distintos, y explicar por qué es
  válida en una tabla y no en la otra.

### M-4 · MEDIA · `methodology.tex:142–145`: índices incorrectos en la red integradora
- `eq:InputL`: $(-I_n + Z_i)$ debería ser $Z_n$.
- `eq:ResL`: $W^{(IR)}_{n,i} A_i$ debería ser $I_i$ (input→response).
- `eq:L4`: $\sum_{r} A_n$ debería ser $A_r$; el texto de `:148` ya lo dice.

### M-5 · MEDIA · `methodology.tex:212–213`: $z_5$ y $z_6$ usan ambos $L_2$
- Por simetría (izquierda/derecha) y por `:216`, $z_6$ probablemente debería usar $L_3$. Confirmar
  con el código.

### M-6 · MEDIA · `methodology.tex:290`: $\omega_{X_4\rightarrow X_7}$, $\omega_{X_3\rightarrow X_8}$ descritas como "amplificación"
- *"provide sufficient command amplification to overcome robot inertia"*, pero en las ecuaciones de
  $z_7$/$z_8$ esos pesos (=10 = $w$) son **inhibitorios** ($-w z_4$, $-w z_3$).
- **Corrección sugerida:** describirlos como inhibición cruzada fuerte, o corregir tabla/ecuaciones.

### M-7 · MEDIA · `methodology.tex:198`: "no lateral inhibition" zeroes "cross-channel inhibitory terms (Gpe→STN, STN→Gpi)"
- Gpe→STN ($-\sum_j Gpe[j] + Gpe[i]$) es inhibitorio. STN→Gpi ($+\sum_j STN[j] - STN[i]$) es
  **excitatorio** difuso.
- **Corrección sugerida:** "zeroes the cross-channel terms (inhibitory Gpe→STN and diffuse
  excitatory STN→Gpi)".

### M-8 · MEDIA · `results.tex:339–341` vs caption `:352–361`: estructura del ciclo de 6 fases
- `:339` dice *"two transfer sub-phases per limb"*. Con 4 patas serían 8 + desplazamientos, no 6. El
  caption, con *"two phases marked body shift"*, implica 4 + 2.
- `:336` dice *"non-degenerate support polygon"*, pero `tab:crawl_stability` da un inradio mínimo
  "≈0".
- **Corrección sugerida:** "one transfer sub-phase per limb (four), interleaved with two body-shift
  sub-phases". Matizar "non-degenerate".

### M-9 · MEDIA · `results.tex:537` vs `methodology.tex:288`: distancia de parada 1.08 m vs 31 cm de diseño
- $Ar = 28$ se deriva para *"a designated safe stopping distance of Z = 31 cm"*. En la inspección
  simulada, $d_{final}$ = 1.076 ± 0.038 m (verificado). Nadie explica la diferencia.
- **Corrección sugerida:** una frase que la explique (otro blanco, otra cámara simulada, distancia
  entre centros).

### M-12 · MEDIA · `methodology.tex:104/109` (`table:LiDAR`): $\sigma_Z = 0.06$ "dimensionless"
- $\sigma_Z$ divide una diferencia de ángulos, así que tiene unidades de ángulo. Con 16 unidades a
  22.5° (0.39 rad), 0.06 rad casi no solapa unidades vecinas.
- **Corrección sugerida:** declarar la unidad de $\theta$ y la de $\sigma_Z$.

### M-13 · MEDIA · `methodology.tex:339` vs `:348`: entradas del MLP descritas de dos formas
- `:339` habla de *"variations in roll, pitch, and the standard deviation of the Z-axis
  acceleration"*; `:348`, de *"linear accelerations in x, y, z, and angular accelerations in x and
  y"*. El MPU-6050 da velocidad angular, no aceleración angular.
- **Corrección sugerida:** describir la entrada igual en ambos sitios y usar "angular rates".

### M-10 · BAJA · `methodology.tex:428` (`table:PerturbationParams`): "Illumination severity" 0.30 en los niveles 3 y 4
- **Verificación:** `R3-04-noise-robustness/config.yaml:29` →
  `illum_levels: [0.0, 0.10, 0.20, 0.30, 0.30] # nota: índices 3 y 4 comparten valor`. Es el valor
  real del código, no una errata.
- **Corrección sugerida:** aclararlo en el caption: "(severity capped at 0.30 at levels 3–4; the
  approach-stop area threshold continues to decrease)".

### B-1 · BAJA · `results.tex:975` (`tab:consolidated_physical_metrics`): "peak ≈27× Obstacle baseline"
- **Verificación:** picos de `firing_var` en `real/*/combined_metrics.csv`: MultiRGB 23.5k–32.9k,
  StimuliG 684–1317, B/R 23–74. Medianas de Obstacle: 0/104/134. El 27× es pico contra pico. Además,
  `:963` ("an order of magnitude above the color-cue scenarios") solo vale para los escenarios de un
  color.
- **Corrección sugerida:** "≈27× the Obstacle peak" y "above the single color-cue scenarios".

### B-2 · BAJA · `results.tex:107` vs `:117`: snapshots "until 3 min" con la meta alcanzada a los 92 s.

### B-3 · BAJA · `results.tex:990`: "a typical 38 s Omnidirectional segment" cuando solo existe uno (N = 1, `tab:mode_steady_state_energy`). Mejor "the single recorded 38.6 s segment". Además, "upper bound on the cost of any mode transition" es una suposición (las transiciones con X no se midieron).

### N-3 · BAJA · `results.tex:597`: "$L_4$ reaches maximum activity after ≈35 s" *(hallazgo del revisor)*
- **Verificación:** en el panel a de `NEU_EST_UNIG_real`, $L_4$ se activa a ~35 s y llega al máximo a
  ~43–45 s.
- **Corrección sugerida:** "$L_4$ activates at ≈35 s and peaks at ≈44 s".

### Verificado sin hallazgo (para la consolidación)
- `tab:consolidated_simulation_metrics`: las 4 filas cuadran con `trial_summary.json` (media ± SD
  poblacional; Obstacle n = 14 sin el ensayo de roll 37.3°).
- Filas Neural de `tab:fsm_comparison` (Appetitive–Complex): cuadran.
- Fisher de la ablación: 3/12 → p = 0.0003, 4/12 → 0.0013, 10/12 → 0.478; el umbral "≥ 5 fallos"
  da p = 0.037 ✓. 25 % / 33 % del abstract ✓.
- Roll/Pitch RMS de terreno (1.59/1.67, 1.47/2.29) y punto medio 1.98° ✓.
- $Ar$: 554·10/31 = 179 px, que es el 28.0 % ✓. F1 del MLP coherente (0.771; 0.824) ✓. Latencias
  14×/25× ✓. RAM 7.4 % ✓.
- Exposición al conflicto Complex/Neural (`results.tex:513`): 0.23 s/ensayo y 1.62 % (media de
  fracciones por ensayo, desde `familia_b_compleja/*/metrics_raw.csv`) ✓.
- "Success 100 %" con reintentos: ya resuelto en `C-55`.

---

## 1.2 Redundancia

### M-16 · MEDIA · Resultados de la ablación contados dos veces casi palabra por palabra
El panel (b) del caption de `fig:ablation_combined` (`results.tex:211`) y `:215` repiten la misma
interpretación de Roll/Pitch ("plausibly reflecting reduced net locomotor activity..."). Dejar las
cifras en el caption y la interpretación solo en la prosa.

### M-14 · BAJA · El caveat de "perturbación conjunta / IMU solo drift" aparece 7 veces
5 de las 7 apariciones las pidieron los revisores (R2b-02 en el texto de resultados, R3b-03 en los
captions), así que no se tocan. Solo se podría consolidar dentro de Metodología (`:417` y `:434`
dicen casi lo mismo).

### B-4 · BAJA · `introduction.tex:6` y `:8`: "developed at ETH Zürich" dos veces. Quitar el segundo.

### B-5 · BAJA · "Circuits executed on the external laptop" en `methodology.tex:196`, `:458`, `conclusions.tex:16` y `results.tex:1033`. Basta con Hardware Spec + Limitations.

---

## 1.3 Candidatos a acortar

### M-17 · BAJA · `tab:consolidated_simulation_metrics` duplica las 4 filas Neural de `tab:fsm_comparison`
El propio texto lo dice (`results.tex:130`, `:524`) y la columna Success es constante. Propuesta:
fusionarla en `tab:fsm_comparison` (añadiendo Pitch RMS). Prioridad baja: C-75 acaba de reencuadrar
esta tabla a propósito, y eliminarla a un día del envío no corrige ningún error.

### B-6 · BAJA · `table:Locom_MLP` (2 filas) y `table:DIR_BINARY` (5 filas) caben en una frase cada una.

---

## 1.4 Ortografía y convenciones académicas

### M-18 · MEDIA · Nombres de los autores distintos entre la portada y CRediT
La portada (`preamble.tex:65–72`, `\author{…}`) dice Carlos-Rodríguez, Caro-Vaca, Caicedo-Samboní,
Grajales-Pulgarín, Ramírez-Moreno. El CRediT (`conclusions.tex:26–31`) dice "Samuel F. Carlos
Rodriguez", "Diego A. Caro Vaca", "Sebastian Grajales Pulgarín", "David Caicedo Samboni", "David F.
Ramirez-Moreno": faltan guiones y tildes, y el orden Caicedo/Grajales está invertido.
**Corrección:** copiar la forma exacta de la portada.

### M-19 · MEDIA · `introduction.tex:34` vs `conclusions.tex:12`: "energy-aware" sigue en la Introducción
Sigue abierto en `C-64_point13_contributions_alignment_proposal.md:38`. Las Conclusiones lo evitan y
la Introducción no. Ninguna entrada del circuito es energía. **Decisión del autor.**

### M-20 · MEDIA · Nombres de los modos inconsistentes
"Quadrupedal Walking" / "quadrupedal mode" / "articulated mode"; "Differential Rolling" /
"differential-drive" / "wheeled/differential"; "Omnidirectional" con y sin mayúscula; "the Hybrid
morphological transformation" (`results.tex:322`). Fijar un nombre por modo.

### B-8 · BAJA · GPe/GPi en el texto vs Gpe/Gpi en ecuaciones y tablas; $X_n$ en la prosa vs $z_n$ en las ecuaciones (`methodology.tex:204`, `:307`).

### B-9 · BAJA · MLP se define tres veces con grafías distintas (`introduction.tex:34`, `methodology.tex:4`, `:339`). GPR nunca se expande (`introduction.tex:32`). BG se define después del primer uso de "basal ganglia".

### B-10 · BAJA · En dash Unicode "–" en lugar de `--` en 13 sitios: `methodology.tex:83, 90, 131, 135, 244, 336, 352`; `results.tex:653, 662, 666, 701, 745`; `conclusions.tex:10`.

### B-11 · BAJA · Ortografía británica ("artefact" `results.tex:396`, "summarises" `:342`) en un texto americano.

### B-12 · BAJA · "continuously-converging" (`results.tex:215`); "1.2cm" sin espacio (`:713`).

### B-13 · BAJA · `conclusions.tex:40` (AI disclosure): solo nombra ChatGPT, y la revisión se hizo en gran parte con Claude (Anthropic). Además dice "not used to generate ... analyses", cuando agentes de IA ejecutaron scripts de `experiments/`. **Decisión de los autores**; se marca para que se decida a propósito.

---

## 1.5 Calcos del español e inglés no idiomático

### M-21 · MEDIA · "stimuli of different natures" / "of diverse nature"
En títulos de subsección (`results.tex:93`, `:611`), captions (`:100`, `:106`, `:618`, `:653`) y
`conclusions.tex:4`. Sugerencia: "multiple stimuli of different types".

### B-14 · BAJA · Calcos concretos
| Ubicación | Texto | Sugerencia |
|---|---|---|
| `conclusions.tex:10` | "it is noted that" | eliminar |
| `conclusions.tex:10` | "produces variant transient states" | "produces fluctuating transient states" |
| `conclusions.tex:6` | "non-relevant obstacles" | "task-irrelevant obstacles" |
| `conclusions.tex:16` | "decisions can be taken for such ... platforms" | "decisions can be made on such platforms" |
| `methodology.tex:225`, `results.tex:240` | "It is important to emphasize/highlight that" | eliminar |
| `methodology.tex:34` | "thanks to its mechanical structure" | "owing to" |
| `methodology.tex:34`, `results.tex:4` | "three main topologies" / "three-topology terrain map" | "terrain sections" |
| `results.tex:584` | "Complementarily," | "In addition," |
| `methodology.tex:9` | "Based on the previously established criteria" | no se estableció ninguno antes; eliminar |
| `methodology.tex:43` | "emulating the embedded knowledge required for detecting anomalies" | "standing in for the anomaly and hazard cues an inspection robot would detect" |
| `results.tex:180` | "(respectively, before three successful replicates ... were retained)" | "until three successful replicates per level had been retained" |
| `introduction.tex:32` | "This distinction and its subsequent computational formulation" | no hay ninguna "distinction" antes; "This model and its computational formulation" |

---

## 1.6 Texto tocado en las últimas 48 h

### M-22 · MEDIA · `results.tex:176` (C-76): dos dos puntos en una misma oración
*"...distortion: a failed attempt (timeout) and its successful retry at the same severity level: the
failed attempt's..."*. Sugerencia: "...distortion (a failed attempt, timeout, and its successful
retry at the same severity level). The failed attempt's...".

### M-23 · MEDIA · `results.tex:622` (C-76): aposición ambigua
*"keeps $X_{16}$ active and uninhibited by $X_{15}$, the no-motor-action state shown in..."* se lee
como si $X_{15}$ fuera el estado. Sugerencia: "...by $X_{15}$; this is the no-motor-action state
shown in...".

### B-15 · BAJA · Restos de C-76 que se leen raro
- `results.tex:587`: "(approach, a, appetitive; evasion, b, obstacle; and escape, c, aversive)" →
  "((a) appetitive approach; (b) obstacle evasion; (c) aversive escape)".
- `results.tex:310`: "zones, deliberately not drawn on the Roll RMS axis" → "zones; the line is
  deliberately not drawn on the Roll RMS axis".
- `introduction.tex:34`: la lista (i)–(iii) mezcla coma y dos puntos como separador.

### Figuras regeneradas (C-70–C-75)
- **MEDIA** · `fig_mode_timeline_inspection.png`: en esta suite el eje está en **tiempo de pared**,
  porque `metrics_raw.sim_time_s` es epoch. En `test_001`, el eje llega a 196.4 s frente a 42.8 s
  de simulación y 90 s de timeout. Solo pasa en esta suite. Hay que reescalar a tiempo de
  simulación o rotular el eje como wall-clock.
- **BAJA** · `FigA_Stability_Profile.png`: la banda de rugoso se corta por arriba (ver A-3).
- **BAJA** · `FigB_Decision_Delay.png`: el panel A (0–600 ms) aplasta el grupo sub-ms contra el
  eje. Ayudaría un eje log o un inset.
- **BAJA** · `tab:crawl_stability` no dice en el caption que es simulación. El resto de captions sin
  marca es coherente con el alcance de C-73.

---

## Descartados tras la revisión adversarial

| ID original | Motivo |
|---|---|
| M-11 (exposición al conflicto 1.7 % vs 0.8 %) | Recalculado desde `familia_b_compleja/*/metrics_raw.csv`: 0.23 s/ensayo y 1.62 % (media de fracciones por ensayo). Las cifras del paper son correctas; mi 0.8 % usaba otro denominador. |
| M-15 (caveat FSM repetido en 3 captions de figura) | Decidido en `R2b-03`: el revisor pidió literalmente "figure caption of FSM comparison plots" y la fila lo puso a propósito en las 3 figuras. |
| B-7 (acortar esos captions) | Dependía de M-15. |

Enmiendas respecto a la versión anterior de este informe:
- **A-1:** rango 41–87 %; quité los "~85 s" (eran tiempo de pared).
- **A-2:** la histéresis es del controlador, no de la métrica.
- **A-3:** nueva corrección sugerida.
- **A-4:** más evidencia (la Fig. c da 32,489 parámetros).
- **A-5:** añadida `:290`; mapeo resuelto desde las ecuaciones.
- **M-2:** subordinado a C-75 §2.
- **M-10:** confirmado en `config.yaml` (baja).
- **M-18:** líneas corregidas.
- **Cambios de prioridad:** A-6 y A-7 de alta a media; M-14 y M-17 de media a baja.
