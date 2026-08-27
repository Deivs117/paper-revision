# R02-01 — Trazabilidad de Datos de Origen y Plan de Regeneración de Gráficos

**Estado:** DIAGNÓSTICO + DECISIONES CONFIRMADAS — ningún archivo de `sections/`, `assets/` o `source/` fue
modificado para producir este informe. Es de solo lectura sobre `experiments/simulation/`, `experiments/real/` y
las figuras ya auditadas en `R02-01_metric_and_figure_audit.md` (documento previo, en adelante "el Informe 1").
Este documento ya no tiene decisiones abiertas de alcance — todas las preguntas planteadas en la ronda de revisión
del 2026-08-27 fueron respondidas por el autor (ver §0.1) y quedan incorporadas en el resto del informe.

**Continuación de:** `intake/pending/R02-01_metric_and_figure_audit.md`. Ese informe identificó **qué** está mal
(M-01–M-04, F-01–F-08) sin decidir si el texto o la figura tenía razón. Este informe responde la pregunta previa
y necesaria: **¿existe realmente el dato crudo detrás de cada figura, y de dónde sale?** — y, allí donde la
respuesta es "no completamente", ya fija (con el autor) cómo recuperarlo o resintetizarlo.

**Método:** lectura íntegra de la estructura de `experiments/simulation/` (6 familias × ~15 réplicas, 4 tipos de
archivo por réplica: `metrics_raw.csv`, `unified_metrics.csv`, `trial_summary.json`, y `stability_log.csv` en las
familias C1/C2) y de `experiments/real/` (14 carpetas de ensayo físico, con `combined_metrics.csv`,
`neural_metrics.csv`, y en algunos casos `imu_ina_*.csv`/`pitch_latency_*.csv`). Para cada figura/tabla citada en
el Informe 1, se identificó su carpeta de origen probable y **se recalcularon directamente con Python las
estadísticas que el texto y la figura afirman**, comparándolas entre sí — no solo se listó "el archivo existe",
se verificó que sus números efectivamente reproducen (o no) lo que está publicado.

---

## 0.1 Decisiones Confirmadas por el Autor (2026-08-27)

Estas respuestas resuelven **todas** las ambigüedades detectadas en la primera versión de este informe. Se listan
aquí como referencia única antes de entrar al detalle, y se repiten en línea en §1/§2/§3 donde corresponde.

| # | Pregunta | Decisión confirmada |
|---|---|---|
| D-1 | Alcance del criterio "no se puede recuperar dato crudo, hay que vectorizar" | **Aplica a TODO el informe, sin excepción.** Nunca preguntar al equipo/operadores (Sam, Diego, u otros) como método de recuperación — se elimina esa opción de todos los hallazgos, incluidos los que antes la sugerían como "más barata" (F-Data-03, F-Data-04/05, F-Data-06, F-Data-08, F-Data-09/10). Todo dato no verificable directamente por CSV/JSON ya presente en `experiments/` se resuelve por vectorización desde imagen o por inferencia estrictamente automatizada (script sobre datos ya existentes) — nunca por consulta humana externa a este repositorio. |
| D-2 | Escenario físico "Complex" (`Complex_Real_Plot_*.png`) — ¿`MultiRB` o `MultiRGB`? | **`MultiRGB_t01..t03` es la fuente confirmada.** `MultiRB_t01..t03` queda descartada — no se usa para ninguna figura, se documenta como carpeta obsoleta/no canónica (ver §1.2, fila `Complex_Real_Plot_*`). |
| D-3 | F-03 (fusión `fig5_classifier_comparison` + `fig6_computational_cost` → panel 1×3) | **Se ejecuta la fusión.** Como no existe el notebook de entrenamiento original, esto implica vectorizar los valores de `fig5`/`fig6` que no están ya citados textualmente (ver §2, F-Data-06 actualizado). |
| D-4 | F-Data-01 (`exp_latency=-1.0` en `familia_a_obstaculo`) | **Confirmado: usar `metrics_raw.csv` (columna `latency_s`)** en vez de `trial_summary.json.exp_latency` para este escenario. Es un dato CSV real ya existente — no requiere vectorización. |
| D-5 | F-Data-02 (re-alinear `FigA_Stability_Profile.png` a $t=0$) | **Confirmado: unir `metrics_raw.csv` (para localizar $t_{switch}$ por cambio de columna `mode`) con `stability_log.csv` (para la serie de $TR$)** — unión de tablas ya existentes, no vectorización. |
| D-6 | `tab:crawl_stability` (números $SM$/$TR$/inradio, $N=268$) | **Confirmado: se tratan como válidos, no se vectorizan.** Son valores numéricos ya escritos en LaTeX, no una imagen — solo la figura acompañante (`fig_stability_phases.png`) se vectoriza (por D-1) para que combine visualmente con esos números. |
| D-7 | F-Data-09/10 (nomenclatura `floor`/`ramp`/`static` de las carpetas físicas de terreno) | **Confirmado: no confiar en el nombre de carpeta — vectorizar las figuras (`GRAPH_IMU_real`, `GRAPH_IMU2_real`, `NEU_IMU_real`, `NEU_IMU2_real`, `FigReal_Terrain_Latencies_4Panels`) directamente desde el PNG publicado**, en vez de asumir la asociación por nombre o clasificar por firma de señal. |
| D-8 | Fidelidad de vectorización de las 4 figuras IMU de terreno en simulación (`NEU_IMU`, `GRAPH_IMU`, `NEU_IMU2`, `GRAPH_IMU2`) | **Confirmado: vectorizar la serie completa**, no solo los puntos/eventos puntuales citados en prosa — se acepta la menor precisión de digitalizar una serie densa a cambio de cobertura completa. |
| D-9 | F-02 (fusión de los 4 `fig1_*_macro.png` en rejilla 4×3) | **Se ejecuta directamente**, sin pasar primero por una regeneración de las 4 figuras separadas — se aprovecha que de todas formas hay que regenerarlas. |
| D-10 | F-Data-07 (solo 3–4 réplicas físicas por escenario, contra 15 en simulación) | **Se acepta la muestra tal cual, pero se anota la limitación** — se añade una nota breve en el caption o en la prosa de la subsección física (ámbito académico: con $N=3$–$4$ cualquier banda de error/consistencia debe declararse como preliminar; evita observaciones de revisor sobre poder estadístico). |
| D-11 | Herramienta de vectorización — ¿usar WebPlotDigitizer (WPD) tal cual, o construir un extractor propio (OpenCV)? | **Usar WebPlotDigitizer directamente como motor de extracción para las 13 figuras**, sin reimplementar su algoritmo. Además: **agrupar las figuras por template de generador compartido y calibrar los ejes una sola vez por grupo**, reutilizando esa calibración (proyecto/JSON de WPD) para el resto de figuras del mismo grupo en vez de recalibrar cada una — ver §2 (Método General de Vectorización, actualizado) para el detalle de agrupación y la excepción en la que sí se justifica un script propio. |

**Efecto agregado de D-1:** el "Paso 4" original del checklist ("preguntar al equipo por un rosbag2/log no
versionado") **queda eliminado del plan de acción** — ver §5 actualizado. Todo lo que antes dependía de esa
pregunta ahora tiene una ruta de vectorización explícita y es lo primero que hay que planear en términos de
esfuerzo, no lo último.

---

## 0. Hallazgo Principal — antes de la matriz

El supuesto de partida de la tarea ("dudo que esté toda la información que se necesitó para graficar") **era
parcialmente incorrecto para las figuras cuantitativas más importantes**. `experiments/simulation/` contiene el
dataset crudo detrás de `FigA_Stability_Profile.png`, `FigB_Decision_Delay.png`, `FigC_Terrain_Adaptability.png`
y los cuatro `fig1_*_macro.png` — es decir, exactamente las cinco figuras detrás de los hallazgos críticos
M-01/M-02/M-03/M-04 del Informe 1. Se recalcularon sus estadísticas y **el resultado resuelve la pregunta abierta
del Informe 1 ("¿el texto o la figura es la fuente de verdad?") con evidencia cuantitativa directa, no solo
inspección visual**:

| Hallazgo | Texto afirma | Figura muestra (Informe 1, inspección visual) | Dato crudo recalculado (`experiments/`) | Veredicto |
|---|---|---|---|---|
| M-01 (latencia) | "≈47 ms, constante" | 50–2000+ ms, variable con ruido | `exp_latency` en `trial_summary.json`, familia_a_apetitivo: rango 0.015 s–3.07 s; a $\sigma=0$ (sin ruido) media≈60 ms, subiendo a media≈1.6–2.0 s en $\sigma=1$–4 | **Figura y dato crudo coinciden. El texto está desactualizado o mide otra cosa.** |
| M-02 (Tipover Risk) | $\mu_{TR}\approx0.42$ rugoso, escalada a $TR\approx0.58$ en pendiente | plano en TR≈0.58–0.60 en ambos terrenos, sin escalada | `stability_log.csv`, columna `TR`, las 15 réplicas de C1 y C2: media global rugoso=0.600 (rango 0.549–0.605 salvo 2 picos transitorios a 1.86), media global pendiente=0.593 (rango 0.580–0.605 salvo 2 picos a 1.66) | **Figura y dato crudo coinciden (~0.59–0.60 plano). El texto (0.42/0.58, con escalada) no corresponde a ningún archivo existente.** |
| M-03 (phase-space Roll/Pitch RMS) | rugoso $\mu_\phi{=}1.36°,\mu_\theta{=}1.25°$; pendiente $\mu_\phi{=}0.43°,\mu_\theta{=}6.95°$; "zero overlap" | rugoso roll≈1.3–1.6° (2 outliers a 3.05°), pitch≈1.2–1.8° (2 outliers a 3.1°); pendiente roll≈1.4–1.65°, pitch≈2.0–3.25°; rangos de roll solapados | `trial_summary.json`, `roll_rms`/`pitch_rms` finales de las 15 réplicas: rugoso media roll=1.586°, pitch=1.667°; pendiente media roll=1.469°, pitch=2.290° | **Figura y dato crudo coinciden casi exactamente (1.59/1.67 vs. 1.3–1.6/1.2–1.8 leído en figura; 1.47/2.29 vs. 1.4–1.65/2.0–3.25). El texto (1.36/1.25 vs. 0.43/6.95, "zero overlap") no corresponde a ningún archivo existente — y los rangos reales muestran justo el solapamiento en roll que el texto niega.** |
| M-04 ($T_{switch}$) | "invariante, 0.3 ms, Heaviside perfecto, sin chattering" | rugoso: escalón con cola hasta 600 ms en ~13% de ensayos; pendiente: escalera de 5–6 saltos entre 0.8–1.9 ms | `trial_summary.json`, campo `tswitch`, 15 réplicas: rugoso = 0.0002–0.0007 s en 13/15 ensayos, **pero 2/15 (13.3%) en 0.5999 s y 0.6006 s** (≈600 ms); pendiente = 0.0009–0.0018 s (0.9–1.8 ms), 15 valores distintos sin agruparse en un único escalón | **Figura y dato crudo coinciden con precisión sorprendente (el 13% con cola a 600 ms del Informe 1 es exactamente 2/15). El texto (0.3 ms invariante) no corresponde a ningún archivo existente.** |

**Conclusión de la Fase 1 del Informe 1, ya resuelta:** en los cuatro casos, **la figura actualmente en `assets/`
es la que está sincronizada con el dataset crudo disponible; el texto de `results.tex` es el que quedó
desactualizado** (probablemente escrito contra una corrida anterior, un borrador de resultados preliminares, o una
generalización optimista hecha a mano sin volver a leer las figuras finales). Esto **no** es una conclusión sobre
si el experimento en sí es válido — es una conclusión sobre qué documento (texto vs. figura) refleja el dataset
que hoy vive en el repositorio. La recomendación es corregir el **texto** citado por M-01–M-04 para que describa
lo que las figuras (y ahora también los CSVs) efectivamente muestran, en vez de regenerar las figuras — pero esa
decisión de redacción queda fuera del alcance de este informe (es tarea de la Fase 1.3 del Informe 1, ya
desbloqueada por esta verificación).

Este hallazgo cambia el enfoque práctico del resto de la tarea: el problema dominante **no es falta de datos**
para las figuras más citadas — es la ausencia de los **scripts de ploteo originales**, que si existieran
permitirían regenerar `FigA/B/C` y los `fig1_*_macro` con un one-liner ya que el CSV fuente está completo. Para el
resto de las figuras (terreno IMU en simulación y en físico, clasificador MLP, walk sequence $N=268$), D-1 ya fijó
que la vía de recuperación es vectorización, no reconstrucción desde log — la sección 3 cubre ambos casos.

---

## 1. Mapa de Trazabilidad Data ↔ Gráfico

Convención de `Estado`: **✅ Completo** (todas las variables/columnas necesarias existen y se verificaron
numéricamente contra la figura, o el método de recuperación ya está confirmado y no requiere vectorizar) ·
**🖼️ Vectorizar** (decisión confirmada: no hay dato crudo recuperable, se extrae desde el PNG publicado) ·
**🟡 Parcial** (queda una duda menor no cubierta por las decisiones D-1–D-10, ver nota en la fila).

### 1.1 Simulación

| Figura/Tabla (`assets/`) | Sección `results.tex` | Carpeta(s) de origen (`experiments/simulation/`) | Variables/columnas implicadas | Estado |
|---|---|---|---|---|
| `fig1_Appetitive_macro.png` | `fig:appetitive_results` (Appetitive Targeting) | `familia_a_apetitivo/test_00{1..15}*` | `trial_summary.json`: `sim_time_s` (panel A), `pitch_rms` (panel B), `exp_latency` (panel C), agrupado por `seed_info.noise_level_idx` (eje X, $\sigma\in\{0..4\}$) | ✅ Completo (19 carpetas: 15 `SUCCESS` + 4 reintentos `FAILURE_TIMEOUT*` con mismo `trial_index`) — **se regenera fusionada en la rejilla 4×3 (D-9)**, no como figura individual |
| `fig1_Aversive_macro.png` | `fig:aversive_results` | `familia_a_aversivo/test_00{1..15}*` | ídem | ✅ Completo (17 carpetas: 15 `SUCCESS` + 2 `FAILURE_TIPOVER`) — ídem, fusionada por D-9 |
| `fig1_Obstacle_macro.png` | `fig:obstacle_results` | `familia_a_obstaculo/test_00{1..15}*` | panel A/B ídem; panel C (latencia) usa **`metrics_raw.csv`/`latency_s`, no `trial_summary.json.exp_latency`** (D-4) | ✅ Completo (D-4 resuelto sin vectorización) — fusionada por D-9 |
| `fig1_Complex_macro.png` | `fig:complex_results` | `familia_b_compleja/test_00{1..15}` | ídem (`sim_time_s`≈17–33 s, `exp_latency`≈0.03–0.08 s — el único escenario cuyo `exp_latency` sí ronda decenas de ms, consistente con el Informe 1) | ✅ Completo — fusionada por D-9 |
| `FigA_Stability_Profile.png` | `fig:stability_profile` (§Quantitative Performance in Variable Topographies) | `familia_c1_terreno_rugoso/test_00{1..15}_SUCCESS` (panel superior) + `familia_c2_pendiente/test_00{1..15}_SUCCESS` (panel inferior) | `stability_log.csv`: `timestamp`, `TR`, re-alineado a $t_{switch}$ **mediante unión con `metrics_raw.csv`/`mode`** (D-5) | ✅ Completo (D-5 resuelto sin vectorización) |
| `FigB_Decision_Delay.png` | `fig:decision_delay` | mismas carpetas que `FigA` | ECDF de $T_{response}$: `trial_summary.json.final_metrics.tresponse` (15+15 valores); ECDF de $T_{switch}$: `trial_summary.json.final_metrics.tswitch` (15+15 valores) | ✅ Completo (ambos campos existen y ya están agregados a nivel de réplica, no requieren reconstrucción desde series de tiempo) |
| `FigC_Terrain_Adaptability.png` | `fig:terrain_adaptability` | mismas carpetas | `trial_summary.json.final_metrics.roll_rms` / `pitch_rms`, 15+15 puntos (uno por réplica exitosa) | ✅ Completo |
| `fig_stability_phases.png` | `fig:stability_phases` (Quadrupedal Walking, $N=268$) | ninguna carpeta actual coincide (rango real de `stability_log.csv` en C1/C2: 296–1240 filas, ninguna es 268) | figura de 6 fases discretas, pocos puntos de inflexión | 🖼️ Vectorizar (D-1; método concreto en §2, F-Data-03) |
| `tab:crawl_stability` | misma subsección, tabla numérica ($SM$, $TR$, inradio, $N=268$) | mismo run que `fig_stability_phases.png` — pero son valores ya escritos en LaTeX, no un PNG | — | ✅ Válida tal cual (D-6) — **no se vectoriza**, se mantiene como fuente de verdad |
| `tab:consolidated_simulation_metrics` | `sssec:...` (tabla resumen 4 escenarios: Success %, $T_{sim}$, Roll, Pitch) | `familia_a_apetitivo/aversivo/obstaculo`, `familia_b_compleja` | `trial_summary.json`: `verdict` (Success %), `sim_time_s`, `roll_rms`, `pitch_rms` agregados por familia | ✅ Completo — recalculable de inmediato con el mismo script que `macro_robustness.py` |
| `NEU_EST_UNIB.png`/`NEU_EST_UNIG.png` (raster neuronal, single-stimulus, simulación) | Appetitive/Obstacle prose | `familia_a_apetitivo` / `familia_a_obstaculo`, cualquier `test_0XX_SUCCESS/metrics_raw.csv` | `metrics_raw.csv`: `sim_time_s`, `mode`, `red_present`, `blue_present`, `firing_variance`, `temporal_consistency`, `lambda_efficiency` (serie temporal completa a 0.2 s de resolución) | ✅ Completo — **el propio F-01 (traducción "March Decision Module") se corrige en el script que consume estas mismas columnas** |
| `NEU_EST_MUL.png` (multi-stimulus, simulación) | Complex scenario prose | `familia_b_compleja/test_0XX_SUCCESS/metrics_raw.csv` | ídem | ✅ Completo |
| `NEU_IMU.png` / `GRAPH_IMU.png` / `RES_IMU.png` (terreno rugoso, simulación) | `fig:NEU_IMU`/`fig:GRAPH_IMU`/`fig:RES_IMU` | `familia_c1_terreno_rugoso/` — no trae activaciones $X_i$ ni aceleración/pitch cruda | — | 🖼️ Vectorizar, serie completa (D-1 + D-8; ver F-Data-04/05) |
| `NEU_IMU2.png` / `GRAPH_IMU2.png` / `RES_IMU2.0.png` (pendiente, simulación) | análogas a las anteriores | `familia_c2_pendiente/` — mismo problema | — | 🖼️ Vectorizar, serie completa (D-1 + D-8) |
| `fig1_confusion_matrix.png` (clasificador MLP) | §MLP classifier | sin carpeta en `experiments/` (notebook de ML offline) — **pero sus 4 valores (TP=56, FN=5, FP=19, TN=40) ya están confirmados exactos por el Informe 1, M-05** | — | ✅ No requiere vectorizar — regenerar directamente desde los 4 valores ya conocidos |
| `fig4_architecture_ablation.png` | §MLP classifier, F-06 del Informe 1 | sin carpeta — **pero los 4 valores de F1 (0.747/0.766/0.771/0.766) ya están citados textualmente en `results.tex:598`** | — | ✅ No requiere vectorizar — regenerar con esos 4 valores y el nuevo rango de eje Y de F-06 (0.65–0.80) |
| `fig5_classifier_comparison.png` | §MLP classifier | sin carpeta — accuracy/precision/recall/F1 de **los otros 3 clasificadores (LogReg, SVM-RBF, RF) no están citados en prosa**, solo los de MLP | — | 🖼️ Vectorizar (D-1 + D-3, por la fusión F-03) |
| `fig6_computational_cost.png` | §MLP classifier | sin carpeta — latencia de inferencia y tamaño de modelo de los 4 clasificadores no están en prosa | — | 🖼️ Vectorizar (D-1 + D-3) |

### 1.2 Físico (robot real)

| Figura/Tabla (`assets/`) | Sección `results.tex` | Carpeta(s) de origen (`experiments/real/`) | Variables/columnas implicadas | Estado |
|---|---|---|---|---|
| `Appetitive_Real_Plot_1_Switching_Delay_ECDF.png` | `fig:appetitive_ecdf_real` | `StimuliB_t01`…`t04` (blue=apetitivo, confirmado: `blue_present` con suma>0 y `red_present=0` en `neural_metrics.csv`) | `combined_metrics.csv`: `Tswitch` | ✅ Completo — $N=4$; **anotar limitación de muestra en caption/prosa (D-10)** |
| `Appetitive_Real_Plot_2_Basal_Ganglia_Dynamics.png` | `fig:appetitive_bg_real` | ídem | `neural_metrics.csv`: `firing_variance`, `mode` vs. `sim_time_s` | ✅ Completo ($N=4$, D-10) |
| `Appetitive_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png` | `fig:appetitive_rms_real` | ídem | `combined_metrics.csv`: `roll_rms`, `pitch_rms` | ✅ Completo ($N=4$, D-10) |
| `Aversive_Real_Plot_{1,2,3}...png` | `fig:aversive_*_real` | `StimuliR_t01`…`t03` (red=aversivo, confirmado: `red_present` domina) | mismas columnas | ✅ Completo ($N=3$, D-10) |
| `Obstacle_Real_Plot_{1,2,3}...png` | `fig:obstacle_*_real` | `StimuliG_t01`…`t03` (green=obstáculo; `red_present`/`blue_present` casi nulos en las 3 carpetas) | mismas columnas | ✅ Completo ($N=3$, D-10) |
| `Complex_Real_Plot_{1,2,3}...png` | `fig:complex_*_real` | **`MultiRGB_t01..t03` — confirmado (D-2).** `MultiRB_t01..t03` descartada, no usar. | mismas columnas | ✅ Completo ($N=3$, D-10) |
| `NEU_EST_UNIG_real.png` (obstáculo, físico) | `fig:NEU_EST_UNIG_real` | `StimuliG_t01`…`t03` | `neural_metrics.csv` completo (misma estructura que la versión simulada) | ✅ Completo |
| `NEU_EST_MUL_real.png` (multi-estímulo, físico) | `fig:NEU_EST_MUL_real` | `MultiRGB_t01..t03` (D-2) | `neural_metrics.csv` | ✅ Completo |
| `GRAPH_IMU_real.png` / `NEU_IMU_real.png` (terreno rugoso, físico) | `fig:GRAPH_IMU_real`/`fig:NEU_IMU_real` | no se usa ninguna carpeta `Test_current_integrated_*` como fuente (D-7: no confiar en el nombre) | — | 🖼️ Vectorizar directamente desde el PNG publicado (D-1 + D-7) |
| `GRAPH_IMU2_real.png` / `NEU_IMU2_real.png` (pendiente, físico) | `fig:GRAPH_IMU2_real`/`fig:NEU_IMU2_real` | ídem | — | 🖼️ Vectorizar (D-1 + D-7) |
| `FigReal_Terrain_Latencies_4Panels.png` | `results.tex:940` | ídem — no se usa `pitch_latency_*.csv` como fuente pese a ser un candidato fuerte, por D-7 | — | 🖼️ Vectorizar (D-1 + D-7) |
| `FigReal_Morphological_Transition_Energy.png` | `results.tex:929` | `Test_current_integrated_t01` (y variantes `_floor`/`_ramp`/`_static`) | `imu_ina_*.csv`: `current_A × voltage_V = power_W` integrado en el tiempo (energía) | ✅ Completo — **no cubierto por D-7** (esa decisión aplicó solo a las 5 figuras de terreno IMU listadas explícitamente en F-Data-09/10, no a esta); el instante de "transición morfológica" se ubica por el propio pico de `power_W` en la serie, sin necesitar confirmación externa |
| `fig1_confusion_matrix.png`…`fig6_computational_cost.png` (físico) | §MLP classifier | mismo caso que en simulación — es un único clasificador offline, no hay versión "física" separada | — | ✅/🖼️ mismo tratamiento que en §1.1 (fig1/fig4 sin vectorizar, fig5/fig6 vectorizar por D-3) |
| `D1.png`…`D6.png`, `E1.png`…, `Prueba_Terreno_Parte_*` (fotos) | Figuras fotográficas, sin overlay de texto (F-07 del Informe 1) | no aplica — son fotografías directas, no datos graficados | — | N/A (no requieren CSV de origen) |

---

## 2. Matriz de Vacíos y Datos Faltantes (actualizada con decisiones confirmadas)

Cada fila es un hallazgo con ID propio (`F-Data-NN`). Los que ya tienen una decisión confirmada (D-1–D-10) se
marcan **[RESUELTO]** e incluyen el método exacto a implementar; no quedan hallazgos abiertos en esta sección.

### F-Data-01 [RESUELTO por D-4] — `exp_latency = -1.0` en las 15 réplicas de `familia_a_obstaculo`
El campo de latencia nunca se pobló para el escenario Obstacle (siempre exactamente `-1.0`, un valor centinela).
**Método confirmado:** recalcular la latencia directamente desde `metrics_raw.csv` (columna `latency_s`, con
resolución de 0.2 s) en vez de depender de `trial_summary.json.exp_latency` para este escenario específico —
`metrics_raw.csv` sí tiene la serie completa y no usa el centinela `-1.0`. No requiere vectorización.

### F-Data-02 [RESUELTO por D-5] — Falta el evento "instante de cambio de modo" para re-alinear `stability_log.csv`
`FigA_Stability_Profile.png` grafica $TR$ **alineado a $t=0$ = instante del cambio de modo neuronal**, pero
`stability_log.csv` solo trae `timestamp` absoluto de simulación. **Método confirmado:** hacer un `merge` por
trial entre `metrics_raw.csv` (para localizar $t_{switch}$ = primer timestamp donde `mode` cambia) y
`stability_log.csv` (para la serie de $TR$), y restar $t_{switch}$ al `timestamp` de este último antes de
graficar. No requiere vectorización — es unión de tablas ya existentes.

### F-Data-03 [RESUELTO por D-1] — `fig_stability_phases.png` ($N=268$) no tiene carpeta propia
El texto (`results.tex:313-315`) es explícito: *"one complete representative walk sequence"* — una corrida
distinta y más corta que las 15 réplicas de C1/C2, exclusiva para documentar el ciclo de marcha de 6 fases del
modo Cuadrúpedo ($C$). Ninguna carpeta actual tiene 268 filas en `stability_log.csv` (rango real: 296–1240).
**Método confirmado:** vectorizar `fig_stability_phases.png` con `WebPlotDigitizer` (ver método general, §2 final)
— es un scatter/línea de 6 fases discretas con pocos puntos de inflexión, el caso ideal para este flujo. **La
tabla `tab:crawl_stability` NO se vectoriza** (D-6) — sus números siguen siendo la fuente de verdad; solo la
figura se redibuja para combinar visualmente con esos números ya publicados.

### F-Data-04 / F-Data-05 [RESUELTO por D-1 + D-8] — Sin activaciones neuronales ($X_i$) ni aceleración/pitch en las carpetas de terreno C1/C2
`NEU_IMU.png`, `NEU_IMU2.png`, `GRAPH_IMU.png`, `GRAPH_IMU2.png`, `RES_IMU.png`, `RES_IMU2.0.png` necesitan
activaciones individuales $X_0$…$X_{15}$ y series de aceleración Z/pitch que no existen en ningún CSV de
`familia_c1_terreno_rugoso`/`familia_c2_pendiente`. **Método confirmado:** vectorizar las 6 figuras **completas**
(serie temporal íntegra, no solo eventos puntuales) — D-1 excluye tanto volver a correr el experimento como
preguntar al equipo por un log no versionado; D-8 confirma que se prioriza cobertura completa sobre precisión
puntual. Usar detección de color por trazo (OpenCV) en vez de solo `WebPlotDigitizer` manual, dado el volumen (6
figuras, series densas) — ver método general.

### F-Data-06 [RESUELTO por D-1 + D-3] — Bloque del clasificador MLP (`fig1_confusion_matrix`…`fig6`)
Estas 6 figuras provienen de un experimento de *machine learning offline* sin carpeta en `experiments/`. **Método
confirmado, diferenciado por figura:**
- `fig1_confusion_matrix.png`: **no vectorizar** — los 4 valores (TP=56, FN=5, FP=19, TN=40) ya están confirmados
  exactos contra el texto por el Informe 1 (M-05); se regenera directamente desde esos números.
- `fig4_architecture_ablation.png`: **no vectorizar** — los 4 valores de F1 por arquitectura (0.747/0.766/0.771/
  0.766) ya están citados en `results.tex:598`; se regenera con esos valores y el nuevo rango de eje Y 0.65–0.80
  (F-06 del Informe 1).
- `fig5_classifier_comparison.png` / `fig6_computational_cost.png`: **sí vectorizar** — por D-3 (se ejecuta la
  fusión F-03) y porque los valores de los 3 clasificadores no-MLP (LogReg, SVM-RBF, RF) no están citados en
  prosa en ningún punto de `results.tex`, así que no hay otra fuente que el PNG publicado.

### F-Data-07 [RESUELTO por D-10] — Físico tiene 3-4 réplicas donde simulación tiene 15
Cada escenario físico (`StimuliB/G/R`, `MultiRGB`) tiene solo 3-4 carpetas `_t0N`, contra 15 en simulación. El
texto nunca afirma "15 trials" para el robot real (ver caption de `fig:stability_profile`, que lo limita
explícitamente a C1/C2 en simulación), así que **no es un error** — pero sí es una muestra estadísticamente chica
si alguna figura muestra bandas de $\pm 1\sigma$. **Método confirmado:** aceptar la muestra ($N=3$–$4$) para
regenerar las figuras físicas, y **añadir una nota breve** (en el caption o en la prosa de la subsección física)
declarando el tamaño de muestra — evita que un revisor señale poder estadístico insuficiente sin aviso.

### F-Data-08 [RESUELTO por D-2] — Ambigüedad `MultiRB` vs. `MultiRGB` para el escenario "Complex" físico
**Confirmado: `MultiRGB_t01..t03` es la fuente para `Complex_Real_Plot_*.png` y `NEU_EST_MUL_real.png`.**
`MultiRB_t01..t03` no se usa para ninguna figura publicada — se documenta como carpeta obsoleta/de referencia,
sin eliminarla del repositorio (podría corresponder a un ensayo preliminar de 2 estímulos, mantenerla como
histórico no rompe nada).

### F-Data-09 / F-Data-10 [RESUELTO por D-1 + D-7] — Asociación carpeta↔figura no confirmada para las figuras de terreno físico
`GRAPH_IMU_real`/`GRAPH_IMU2_real`/`NEU_IMU_real`/`NEU_IMU2_real`/`FigReal_Terrain_Latencies_4Panels` tenían
candidatos razonables por nomenclatura (`floor`/`ramp`/`pitch_latency`), pero sin confirmación por contenido.
**Método confirmado:** no usar `Test_current_integrated_*`/`Imu_pitch_test_t01` como fuente para estas 5 figuras
— se vectorizan directamente desde el PNG publicado, tratando la asociación por nombre de carpeta como no
confiable. (Nota: esta decisión **no** se extiende a `FigReal_Morphological_Transition_Energy.png`, que sí sigue
usando `Test_current_integrated_*`/`imu_ina_*.csv` como fuente — ver §1.2 — porque esa figura no formaba parte del
conjunto ambiguo original de F-Data-09/10, solo se apoyaba en las mismas carpetas por un motivo distinto y no
disputado.)

### Método General de Vectorización [actualizado por D-11] — WebPlotDigitizer como motor único, agrupado por template compartido

**Decisión de herramienta (D-11):** se usa **WebPlotDigitizer (WPD)** directamente — modo "Automatic Extraction"
por segmentación de color para líneas/series continuas, modo manual por click para scatter/barras discretas — en
vez de reimplementar su lógica en un script propio de OpenCV. Razón: WPD ya resuelve los casos difíciles de
extracción (anti-aliasing, grosor de línea variable, ejes log) porque es el estándar de facto para extracción de
datos de figuras científicas; reescribir eso desde cero para una recuperación histórica puntual de 13 figuras (no
un pipeline recurrente) es esfuerzo de ingeniería que no se recupera. Además, WPD exporta CSV directo
(par de columnas por serie) — ese export **entra tal cual** al esquema que ya esperan los `builders/` de §3.2, sin
necesitar una capa de parsing intermedia.

**Optimización real de eficiencia — agrupar por template de figura, calibrar una sola vez por grupo:**
el cuello de botella de la vectorización no es el algoritmo de extracción, es la **calibración manual de ejes por
imagen** (fijar 2-4 puntos de referencia antes de poder extraer). El Informe 1 (F-01) ya estableció que varias
familias de figuras comparten un mismo script generador (mismo layout de panel, mismo rango de eje, mismo error de
traducción repetido en las ~9 figuras de raster neuronal) — eso implica que, dentro de cada grupo, la posición en
píxeles de los ejes es probablemente idéntica entre figuras. Antes de vectorizar, agrupar así y **verificar
visualmente que el layout de ejes coincide dentro de cada grupo** (comparando 2 imágenes del grupo lado a lado);
si coincide, calibrar una sola vez y reutilizar el proyecto/calibración de WPD para el resto del grupo:

| Grupo | Figuras | Calibraciones necesarias (estimado) |
|---|---|---|
| A — walk sequence | `fig_stability_phases.png` (F-Data-03) | 1 (figura única, sin grupo) |
| B — clasificador MLP | `fig5_classifier_comparison.png`, `fig6_computational_cost.png` (F-Data-06) | 1-2 (fig6 tiene 2 subpaneles con escalas propias — verificar si comparten eje) |
| C — IMU terreno, simulación | `NEU_IMU`/`GRAPH_IMU`/`RES_IMU` (rugoso) + `NEU_IMU2`/`GRAPH_IMU2`/`RES_IMU2.0` (pendiente) — 6 figuras | 2 (una por terreno, si rugoso/pendiente comparten layout entre sí — a verificar; probablemente NO entre `NEU_*`/`GRAPH_*`/`RES_*` porque son tipos de plot distintos, así que en el peor caso serían 3 calibraciones × 2 terrenos = 6, en el mejor 2) |
| D — IMU terreno, físico | `GRAPH_IMU_real`, `GRAPH_IMU2_real`, `NEU_IMU_real`, `NEU_IMU2_real`, `FigReal_Terrain_Latencies_4Panels` — 5 figuras | 2-3 (mismo criterio que grupo C) |

Esto reduce el trabajo de calibración manual de "13 calibraciones independientes" a un rango realista de 6-10,
dependiendo de cuánto layout comparta cada grupo — confirmar la agrupación real es el primer paso de la
implementación (§3.4, Grupo 2), no una suposición a ciegas.

**Cuándo SÍ se justifica un script propio (OpenCV) — la excepción, no la regla:** únicamente como
**post-procesado puntual sobre la exportación de WPD**, nunca como reemplazo del extractor completo, y solo
cuando el modo automático de WPD falla en un caso concreto y verificable:
- Dos series se cruzan o se superponen en un tramo y WPD confunde el trazo de una con el de otra al seguir color
  (posible en `GRAPH_IMU`/`GRAPH_IMU2`, que ya mezclan dos magnitudes en el mismo eje — F-04 del Informe 1).
- Una línea de referencia (p. ej. el umbral punteado en 3.7 que el texto menciona pero la figura actual no
  dibuja, F-04) se confunde con la serie de datos real por similitud de color/grosor.
- Un panel tiene demasiados puntos superpuestos para extracción manual razonable y el modo automático de WPD no
  logra separar la densidad (poco probable dado el volumen de estas 13 figuras, pero posible en las series más
  densas del Grupo C/D).
En cualquiera de estos casos, el script correctivo debe ser pequeño y dirigido al caso específico (aislar un
color, recortar una región), no un extractor genérico — y debe documentarse en
`experiments/_plotting/vectorized/README.md` junto con la exportación de WPD que corrige, exactamente igual que
cualquier otro dato vectorizado.

**OCR de ejes/leyenda** (`pytesseract` o similar) sigue siendo útil de forma independiente — no para extraer
valores de datos, sino para confirmar/extraer texto de rótulos y rangos de eje al mismo tiempo que se vectoriza
cada figura (relevante para corregir F-01/F-04/F-05 del Informe 1 de paso).

Ninguno de estos métodos es necesario para M-01–M-04 (ya resueltos con CSV real, §0), para las 4 `fig1_*_macro`
fusionadas (D-9, CSV real), para `FigA`/`FigB`/`FigC` (D-5, CSV real), ni para `fig1_confusion_matrix`/
`fig4_architecture_ablation` (F-Data-06, valores ya en prosa) — esas siguen siendo generables sin vectorizar.

---

## 3. Estrategia y Arquitectura para los Nuevos Scripts de Ploteo

### 3.1 Diagnóstico del problema real
El problema tiene ahora dos partes de tamaño comparable, no una dominante: (a) **13 figuras confirmadas para
vectorización** (D-1, D-7, D-8) necesitan pasar por WebPlotDigitizer (D-11) antes de poder graficarse de nuevo, y
(b) el resto (~20 figuras con CSV verificado) solo necesita el **código que convierte el CSV existente en
figura**, que nunca se escribió/versionó. Ambas partes comparten la misma librería de "constructores de figura"
de la sección 3.2 — la vectorización solo cambia **de dónde viene el DataFrame** que entra al builder (`loaders.py`
lee CSV real para (b); para (a) el export CSV de WPD se guarda directamente en `vectorized/` con el mismo esquema
de columnas y `loaders.py` lo lee igual que cualquier otro CSV — no hace falta una capa de parsing/extracción
propia, D-11 elimina esa pieza de la arquitectura).

### 3.2 Arquitectura propuesta

```
experiments/
  _plotting/                      # nueva carpeta, compartida por simulation/ y real/
    __init__.py
    style.py                      # paleta de colores única (azul/naranja/rosa/verde ya
                                   # usados en el documento), fuente, tamaño, grosor de línea,
                                   # DPI de exportación — UNA sola fuente de verdad de estilo
    loaders.py                    # funciones puras: load_trial_summary(), load_metrics_raw(),
                                   # load_stability_log() [con el merge de F-Data-02 ya
                                   # incorporado], load_real_combined() — y también lee
                                   # vectorized/*.csv con la MISMA función, porque el export de
                                   # WPD (D-11) ya tiene el esquema de columnas esperado; no hace
                                   # falta un loader/parser distinto para dato vectorizado
    vectorized/                   # NUEVO — exports de WebPlotDigitizer (D-1/D-7/D-8/D-11),
                                   # organizados por grupo de calibración compartida (ver §2)
      README.md                   # documenta, por cada CSV, de qué PNG salió, qué grupo de
                                   # calibración compartida usó (A/B/C/D, ver §2), y si tuvo
                                   # post-procesado puntual de OpenCV (excepción de D-11) —
                                   # trazabilidad inversa obligatoria dado que este dato NO
                                   # viene de una corrida real
      wpd_projects/                # proyectos .json de WPD guardados por grupo de calibración
                                   # (uno por grupo A-D, reutilizados entre figuras del mismo
                                   # grupo en vez de recalibrar cada imagen — la optimización de
                                   # D-11) — versionados para que la calibración sea auditable,
                                   # no solo el resultado final
      stability_phases_N268.csv           # F-Data-03 (grupo A)
      classifier_fig5.csv, classifier_fig6.csv                            # F-Data-06 (grupo B)
      neu_imu_rugged.csv, graph_imu_rugged.csv, res_imu_rugged.csv       # F-Data-04/05 (grupo C)
      neu_imu_slope.csv, graph_imu_slope.csv, res_imu_slope.csv          # F-Data-04/05 (grupo C)
      graph_imu_real_*.csv, neu_imu_real_*.csv, terrain_latencies_real.csv  # F-Data-09/10 (grupo D)
    builders/
      macro_robustness.py         # rejilla 4×3 única (D-9) — usado hoy por los 4 fig1_*_macro.png
      neural_raster.py            # raster neuronal 2-3 paneles — usado por NEU_EST_*, NEU_IMU*
                                   # (sim y real); UNA sola definición de rótulos en inglés
                                   # correcto ("Gait Decision Module", "Auxiliary") resuelve F-01
                                   # para las ~9 figuras de una vez, sin importar si el dato de
                                   # entrada viene de una corrida real o de vectorized/
      ecdf_phase_space.py         # FigA (TR alineado a t=0 vía F-Data-02) / FigB / FigC
      imu_dual_axis.py            # GRAPH_IMU/GRAPH_IMU2 (sim, vectorizado) y sus versiones
                                   # _real (también vectorizadas) con doble eje Y (F-04)
      classifier_suite.py         # fig1/fig4 desde valores ya en prosa; fig5/fig6 desde
                                   # vectorized/ (F-Data-06)
    generate_all.py               # script único de entrada: recorre experiments/simulation/*,
                                   # experiments/real/* y experiments/_plotting/vectorized/,
                                   # llama al builder correspondiente, escribe a
                                   # experiments/<id>/output/, y opcionalmente invoca
                                   # scripts/promote_figure.sh (nunca escribe a assets/ directo,
                                   # por la regla del CLAUDE.md de este repo)
```

### 3.3 Principios de diseño

1. **Separación loader/builder/estilo se mantiene, sin loader adicional para dato vectorizado (D-11).** Un
   builder nunca sabe (ni necesita saber) si sus datos vienen de una corrida real o de un export de WPD, porque
   `loaders.py` lee ambos con la misma función siempre que el CSV en `vectorized/` respete el esquema de columnas
   esperado — eso simplifica la arquitectura respecto a la v1 de este informe (que proponía un
   `vectorized_loaders.py`/pipeline OpenCV separado).
2. **`vectorized/README.md` + `wpd_projects/` son obligatorios, no opcionales.** Es la única forma de que una
   figura regenerada por vectorización siga siendo auditable en el futuro — sin esa trazabilidad inversa (qué PNG,
   qué grupo de calibración, qué proyecto de WPD), un lector de código no podría distinguir un CSV de una corrida
   real de uno digitalizado a mano, lo cual sería peor que el problema que este informe está resolviendo.
3. **Un builder = una familia visual, no una figura** (sin cambios respecto a la v1 de este informe).
4. **`generate_all.py` es determinista y sin estado oculto** (sin cambios).
5. **Reutiliza la infraestructura ya existente del proyecto** (sin cambios): `experiments/<id>/output/` →
   `scripts/promote_figure.sh` → `assets/`.
6. **Matplotlib puro, sin dependencias pesadas** para los builders (sin cambios); la vectorización en sí se hace
   fuera del repo, en la interfaz de WebPlotDigitizer — no se añade `opencv-python`/`pytesseract` como dependencia
   permanente del proyecto salvo que se dé el caso excepcional de post-procesado puntual descrito en §2.

### 3.4 Orden de implementación sugerido (actualizado — separa "listo hoy" de "requiere vectorizar primero")

**Grupo 1 — CSV real, sin vectorización, implementable de inmediato (4 builders):**
1. `ecdf_phase_space.py` — `FigA`/`FigB`/`FigC`, con F-Data-02 (merge) ya resuelto por D-5.
2. `macro_robustness.py` — rejilla 4×3 fusionada directamente (D-9), con F-Data-01 (latencia Obstacle) resuelto
   por D-4.
3. `neural_raster.py` (rama simulación: `NEU_EST_UNIB`/`NEU_EST_UNIG`/`NEU_EST_MUL`) — CSV completo, resuelve F-01
   de una vez para estas 3.
4. `classifier_suite.py` (rama `fig1_confusion_matrix`/`fig4_architecture_ablation` únicamente) — valores ya en
   prosa, sin vectorizar.

**Grupo 2 — requiere vectorización previa vía WebPlotDigitizer (D-11), hacer en paralelo al Grupo 1 por ser el
cuello de botella real del plan. Orden por grupo de calibración compartida (§2), no figura por figura:**
5. **Paso 0 obligatorio antes de calibrar nada:** abrir las figuras de cada grupo (A/B/C/D, tabla de §2) lado a
   lado y confirmar visualmente si comparten posición de ejes en píxeles — determina si el grupo necesita 1
   calibración o varias. Documentar el resultado en `vectorized/README.md` antes de exportar el primer CSV.
6. Grupo A — vectorizar `fig_stability_phases.png` (F-Data-03, WPD, baja complejidad — pocos puntos de inflexión,
   1 calibración) → alimenta un builder dedicado simple (la figura acompaña a `tab:crawl_stability`, que D-6 ya
   fijó como válida sin vectorizar).
7. Grupo B — vectorizar `fig5_classifier_comparison.png`/`fig6_computational_cost.png` (F-Data-06, WPD, baja
   complejidad, 1-2 calibraciones) → alimenta `classifier_suite.py` (rama fusión F-03, D-3).
8. Grupo C — vectorizar las 6 figuras IMU de terreno en simulación (F-Data-04/05, WPD modo automático por color,
   2-6 calibraciones según el paso 0) → alimenta `imu_dual_axis.py` + `neural_raster.py` (rama terreno).
9. Grupo D — vectorizar las 5 figuras IMU de terreno físico (F-Data-09/10, mismo método, 2-3 calibraciones según
   el paso 0) → alimenta las versiones `_real` de los mismos dos builders.
10. `neural_raster.py` (rama física: `NEU_EST_UNIG_real`/`NEU_EST_MUL_real`, con `MultiRGB` confirmado por D-2) y
    los 5 builders `Real_Plot_*` (Appetitive/Aversive/Obstacle/Complex) — CSV real, sin vectorizar, pero se coloca
    después del Grupo 1 solo por orden de familia, no por dependencia técnica; puede adelantarse si conviene.

**Razón del reordenamiento:** en la v1 de este informe, la vectorización era el último recurso (3 figuras en el
peor caso). Con D-1 aplicado a todo, son **13 figuras** las que dependen de vectorización — es ahora el cuello de
botella real de calendario del plan completo, así que conviene iniciar el Grupo 2 en paralelo al Grupo 1 en vez de
secuencialmente después. El paso 0 (agrupar por calibración compartida, D-11) es lo que decide si ese cuello de
botella termina siendo 13 calibraciones manuales o 6-10 — confirmarlo primero cambia la estimación de esfuerzo de
todo el Grupo 2.

---

## 4. Recomendación del Mejor Proceder

1. **No hay que "salvar" la mayoría de las métricas — ya están salvadas.** Para 20+ figuras (todo el Grupo 1 de
   §3.4 más las 5 `Real_Plot_*` físicas) el trabajo restante es ingeniería de reproducibilidad pura sobre CSV ya
   verificado — cero incertidumbre de datos.
2. **Cerrar primero la decisión de redacción de M-01–M-04** usando la tabla de §0 — sigue siendo la acción de
   mayor apalancamiento, ahora sin ninguna pregunta abierta que la bloquee.
3. **Empezar el Grupo 2 de vectorización (§3.4) en paralelo al Grupo 1, no después.** Es el cambio de
   recomendación más importante de esta actualización: con el criterio D-1 aplicado a todo, la vectorización pasó
   de ser una salida de emergencia a ser el ~40% del volumen total de figuras (13 de ~33 figuras cuantitativas) —
   arrancarla tarde extendería el cronograma sin necesidad.
4. **Documentar cada CSV vectorizado en `experiments/_plotting/vectorized/README.md` desde el primer archivo**,
   no al final — es la única salvaguarda de trazabilidad para datos que, por definición, no vienen de una corrida
   real y no pueden re-verificarse contra un log.
5. **Ya no hay ninguna pregunta pendiente de "para quién" (Sam/Diego/operador de ensayos) en este plan** — D-1
   cerró esa vía por completo; toda ambigüedad restante (F-Data-08, F-Data-09/10) ya tiene una decisión (D-2, D-7)
   en vez de una acción de "preguntar".
6. **Registrar este informe en `PROGRESS.md` solo después de que las decisiones de redacción de M-01–M-04 estén
   tomadas** (sin cambios respecto a la v1). Cuando se implementen los builders de §3.4, cada uno debería
   registrarse como una fila `N-xx` con `Data source` apuntando a `experiments/_plotting/` (y, para el Grupo 2, con
   una nota explícita "figura basada en datos vectorizados, ver `vectorized/README.md`" en la columna de
   `Requirement`/notas de `PROGRESS.md` — la trazabilidad de origen debe llegar hasta el dashboard, no quedarse
   solo en este documento).

---

## 5. Checklist de Próximos Pasos (actualizado, sin pasos de "preguntar al equipo")

1. [ ] Decidir la redacción de M-01–M-04 usando la tabla de §0 (texto → alinear con figura/CSV; envuelto en
   `\revblue{}`).
2. [ ] Implementar Grupo 1 completo (§3.4, pasos 1-4): `ecdf_phase_space.py`, `macro_robustness.py`,
   `neural_raster.py` (rama simulación), `classifier_suite.py` (rama fig1/fig4) — sin dependencias de
   vectorización, listo para arrancar de inmediato.
3. [ ] En paralelo al paso 2, iniciar el Grupo 2 (§3.4, pasos 5-8): vectorizar, en este orden de complejidad
   creciente, `fig_stability_phases.png` → `fig5`/`fig6` del clasificador → las 6 figuras IMU de terreno en
   simulación → las 5 figuras IMU de terreno físico. Documentar cada una en
   `experiments/_plotting/vectorized/README.md` al momento de vectorizarla, no después.
4. [ ] Implementar `neural_raster.py` (rama física, `MultiRGB` confirmado por D-2) y los builders `Real_Plot_*`
   (Appetitive/Aversive/Obstacle/Complex), añadiendo la nota de tamaño de muestra $N=3$–$4$ (D-10) al caption o a
   la prosa correspondiente.
5. [ ] Confirmar/computar el instante de "transición morfológica" en `FigReal_Morphological_Transition_Energy.png`
   por el pico de `power_W` en `imu_ina_*.csv` (sin vectorizar, sin preguntar — método ya definido en §1.2).
6. [ ] Una vez implementados los builders de los pasos 2-4, dar de alta las filas `N-xx` correspondientes en
   `PROGRESS.md` con `Data source` apuntando a `experiments/_plotting/` (y a `vectorized/` cuando aplique),
   siguiendo el flujo estándar de `intake/`.
7. [ ] Mover este archivo a `intake/processed/` **junto con `R02-01_metric_and_figure_audit.md`** (ver su §7), solo
   cuando todas las filas que genere alcancen al menos estado `applied` en `PROGRESS.md` (regla del proyecto) —
   se mueven a la vez para no romper la trazabilidad cruzada entre los dos documentos.

---

## Relación con `R02-01_metric_and_figure_audit.md` ("Informe 1")

Este documento y el Informe 1 se usan juntos, no en secuencia estricta: **Informe 1 responde "qué está mal y por
qué importa"** (catálogo de hallazgos M-01–M-05/F-01–F-08, con severidad y evidencia textual); **este documento
responde "de dónde sale el dato y cómo se ejecuta la corrección"** (mapa de trazabilidad, decisiones D-1–D-11,
arquitectura de builders). El checklist de la Fase 1-4 del Informe 1 (§7) queda como registro de *qué decisión se
tomó y por qué*, apuntando aquí para el *cómo*; el checklist de este documento (arriba) es la única lista de
pasos de ejecución vigente — evitar mantener una tercera copia de la secuencia de trabajo en ningún otro lugar.

---

## Adenda de Implementación (2026-08-27) — Tareas 1-3 ejecutadas, correcciones encontradas

Se construyó `experiments/_plotting/` (Tarea 1) y se ejecutó contra los datos actuales (`experiments/N-01-*`);
se estandarizó `experiments/real/` (Tarea 2, ver su `MANIFEST.md`); se regeneró/vectorizó el bloque físico +
clasificador (Tarea 3, ver `experiments/N-02-*`). Tres correcciones a este informe surgieron al ejecutar el
código, documentadas en detalle en los README de N-01/N-02 — resumen aquí para quien lea solo este documento:

- **F-Data-01 estaba mal diagnosticado.** No es que `metrics_raw.csv` tuviera el fallback de latencia para
  `familia_a_obstaculo` — **no existe ninguna fuente de latencia poblada para ese escenario en todo
  `experiments/`**, ni en `trial_summary.json` ni en `metrics_raw.csv` (0/15 filas en ambos). El panel C de
  `fig1_Obstacle_macro.png` publicado no se puede reproducir desde este repositorio tal como está.
- **La columna `Tswitch` de `combined_metrics.csv` (físico) es un escalón, no un reloj corriendo** — mantiene
  `0.0` antes del cambio de modo y luego un único valor fijo el resto de la grabación; "retraso de conmutación"
  = `max(Tswitch.dropna())` por ensayo. Confirmado fila por fila, no asumido.
- **`NEU_EST_UNIG_real.png`/`NEU_EST_MUL_real.png` no tienen los datos por-neurona ($X_i$) que muestran** —
  el veredicto original "✅ Completo" solo verificó que existiera un CSV, no que tuviera las columnas exactas
  que la figura necesita. Mismo tipo de vacío que F-Data-04/05, ahora también aplicable a estas dos.
- **D-11 se refinó en la práctica:** para las 2 figuras ya vectorizadas (`fig5`/`fig6`), se usó extracción
  directa de color de píxel en Python (no WebPlotDigitizer por navegador) — ver
  `experiments/_plotting/vectorized/README.md` para el razonamiento y la validación numérica de cada una.

Estado de figuras físicas de vectorización pendiente (5 de 7): `GRAPH_IMU_real`, `GRAPH_IMU2_real`,
`NEU_IMU_real`, `NEU_IMU2_real`, `FigReal_Terrain_Latencies_4Panels` — ver
`experiments/N-02-physical-figure-regeneration/README.md` §"Remaining work" para el plan concreto.

**Actualización 2026-08-27 (cierre de N-02):** las 5 figuras de arriba, más `NEU_EST_UNIG_real`/`NEU_EST_MUL_real`
y la fusión F-03, ya se completaron y pasaron 4 rondas de auditoría del autor — **12 de 19 figuras físicas
aprobadas, listas para promover a `assets/`.** El detalle completo de estado por hallazgo y el checklist de
tareas de escritura sistemáticas para ejecutar hoy ya NO vive aquí — ver
`R02-01_metric_and_figure_audit.md` §8 (estado) y §9 (tareas), para no mantener dos copias del mismo checklist.
Este documento (Informe 2) sigue siendo la referencia para el *método* de vectorización/extracción; Informe 1 es
la referencia para *qué hacer ahora* con el resultado.
