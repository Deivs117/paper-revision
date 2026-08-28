# R02-01-05 — Simulación N-01, Grupo 2: rasters neuronales (F-01) + IMU doble eje (F-04) + walk sequence (F-08) — PENDIENTE

**Estado: 🔲 Sin empezar.** Ninguno de los builders necesarios existe todavía (`experiments/_plotting/builders/`
solo tiene `classifier_suite.py`, `ecdf_phase_space.py`, `energy_transition.py`, `imu_terrain_real.py`,
`macro_robustness.py`, `real_plot_suite.py` — no hay `neural_raster.py` ni `imu_dual_axis.py`). Es el bloque
grande de simulación que sigue sin tocar; requiere vectorización previa (WebPlotDigitizer o extracción de
píxel), no CSV crudo.

**Origen:** `intake/pending/R02-01_metric_and_figure_audit.md` §3 (F-01, F-04, F-08) + `intake/pending/R02-01_data_traceability_and_plotting_plan.md`
§2 (D-1, D-8, D-11, F-Data-03/04/05) + §3.4 Grupo 2 (ambos eliminados tras atomizarse, ver
`intake/R02-01_INDEX.md`).

## 0. Por qué estas 3 tareas van juntas

Las tres comparten la misma causa técnica (sin CSV crudo recuperable, D-1 ya descartó preguntar al equipo como
método) y el mismo método de recuperación (vectorización), agrupadas en 2 de los 4 grupos de calibración
compartida de Informe 2 (Grupo A y Grupo C — los Grupos B y D ya se cerraron, ver
`intake/processed/R02-01-02_fisico_regeneracion_N02-N05.md`).

## 1. F-01 (instancias de simulación) — "March Decision Module"/"Auxiliar" mal traducidos

**Figuras:** `NEU_EST_UNIB.png`, `NEU_EST_UNIG.png`, `NEU_EST_MUL.png` (CSV real disponible — Grupo 1 de
Informe 2, implementable sin vectorizar) + `NEU_IMU.png`, `NEU_IMU2.png` (sin CSV — Grupo 2, vectorizar).

- **Corrección:** título del subpanel `"March Decision Module"` → `"Gait Decision Module"` (coincide con
  `methodology.tex` y `results.tex`); título del subplot LiDAR `"Auxiliar"` → `"Auxiliary"`.
- **`NEU_EST_UNIB/UNIG/MUL`:** CSV en `familia_a_apetitivo`/`familia_a_obstaculo`/`familia_b_compleja`, cualquier
  `test_0XX_SUCCESS/metrics_raw.csv` (columnas `sim_time_s`, `mode`, `red_present`, `blue_present`,
  `firing_variance`, `temporal_consistency`, `lambda_efficiency`, resolución 0.2s). **No requiere vectorizar** —
  implementable ya, mismo builder `neural_raster.py` que las versiones `_real` que ya están cerradas.
- **`NEU_IMU/NEU_IMU2`:** sin activaciones $X_i$ en ningún CSV de `familia_c1_terreno_rugoso`/`familia_c2_pendiente`
  — **requiere vectorizar la figura completa** (serie temporal íntegra, no solo eventos puntuales — decisión D-8:
  se prioriza cobertura completa sobre precisión puntual de picos).

## 2. F-04 — Ejes "V A L U E" sin unidades, dos magnitudes mezcladas en `GRAPH_IMU.png`/`GRAPH_IMU2.png`

**Diagnóstico:** eje Y rotulado letra-por-letra "V\nA\nL\nU\nE" superpone "Standar dev accel z" (m/s², con typo:
falta la "d" de "Standard") y "Pitch angle" (grados) en el mismo eje sin dualidad — ambiguo de leer. El texto
(`results.tex:199`) menciona un umbral de 3.7 que la figura actual no dibuja.

**Rediseño (aplicar sobre el dato vectorizado, no sobre una re-corrida):**
- Doble eje Y: Y1 izquierda (azul) = "Std. dev. acceleration, Z axis (m/s²)"; Y2 derecha (naranja) = "Pitch angle
  (deg)".
- Leyenda: "Standar dev accel z" → "$\sigma_{az}$ — Std. dev. accel. Z" (notación que `methodology.tex:354` ya
  define); "Pitch angle" → "Pitch (deg)".
- Añadir línea horizontal punteada en Y1=3.7 con etiqueta "$U_{\sigma_{az}}$ threshold" (variable que
  `methodology.tex:354` ya define).
- Título diferenciado por figura: "IMU activity — Rugged Terrain (Simulation)" / "IMU activity — Inclined Slope
  (Simulation)" (hoy ambas dicen el genérico "IMU activity").

**Nota:** la versión **física** (`GRAPH_IMU_real`/`GRAPH_IMU2_real`) resultó ser un caso distinto (heatmap
categórico, no serie continua) — ese caso (F-05) ya está cerrado, ver
`intake/processed/R02-01-02_fisico_regeneracion_N02-N05.md`. No confundir los dos.

## 3. F-08 / F-Data-03 — `fig_stability_phases.png` ($N=268$) sin carpeta de origen

**Diagnóstico:** el texto (`results.tex:313-315`) es explícito: "one complete representative walk sequence" — una
corrida distinta y más corta que las 15 réplicas de C1/C2, exclusiva para documentar el ciclo de marcha de 6
fases del modo Cuadrúpedo. Ninguna carpeta actual tiene 268 filas en `stability_log.csv` (rango real: 296–1240).
**Confirmado también por el pipeline N-01 (§4 de este documento, ítem 5 de la lista para el equipo de
simulación): esta corrida nunca se archivó.**

**Consistencia interna ya verificada (no requiere corrección de contenido, solo regenerar la imagen):** los 4
paneles de fase de balanceo (A,C,D,F) muestran TR≈0.71–0.77, los 2 de apoyo de 4 patas (B,E) muestran "Static
stance" (TR≈0) — promediando ambos regímenes da ≈0.439, que coincide con `tab:crawl_stability`
($TR_{mean}=0.439$). **La tabla `tab:crawl_stability` NO se vectoriza** (decisión D-6, ya vigente) — sus números
son la fuente de verdad; solo la figura se redibuja para combinar visualmente con esos números.

**Método:** vectorizar con WebPlotDigitizer — pocos puntos de inflexión discretos, caso simple, 1 sola
calibración (Grupo A, figura única sin más miembros en su grupo).

## 4. Método de vectorización (D-1, D-8, D-11) — aplica a las 3 tareas de arriba

- **D-1 (alcance):** nunca preguntar al equipo/operadores como método de recuperación — todo dato no verificable
  por CSV/JSON ya existente se resuelve por vectorización desde imagen o inferencia automatizada.
- **D-11 (herramienta):** WebPlotDigitizer como motor de extracción (modo automático por color para series
  continuas, manual por click para scatter/discreto) — o extracción directa de color de píxel en Python si el
  caso lo amerita (refinamiento encontrado en la práctica al cerrar los Grupos B/D, ver
  `experiments/_plotting/vectorized/README.md`).
- **Agrupar por template compartido, calibrar una sola vez por grupo** (el cuello de botella real es la
  calibración manual de ejes, no el algoritmo de extracción):

| Grupo | Figuras de este bloque | Calibraciones estimadas |
|---|---|---|
| A — walk sequence | `fig_stability_phases.png` (§3) | 1 |
| C — IMU terreno, simulación | `NEU_IMU`/`GRAPH_IMU`/`RES_IMU` (rugoso) + `NEU_IMU2`/`GRAPH_IMU2`/`RES_IMU2.0` (pendiente) — 6 figuras (§1 parcial + §2 completo) | 2–6 (verificar primero si comparten layout entre tipos de plot) |

**Paso 0 obligatorio antes de calibrar nada:** abrir las figuras de cada grupo lado a lado y confirmar
visualmente si comparten posición de ejes en píxeles — determina si el grupo necesita 1 calibración o varias.
Documentar el resultado en `experiments/_plotting/vectorized/README.md` antes de exportar el primer CSV.

**Cuándo sí se justifica un script propio (OpenCV) — la excepción:** solo como post-procesado puntual cuando el
modo automático falla en un caso concreto y verificable (series que se cruzan/superponen — posible en
`GRAPH_IMU`/`GRAPH_IMU2`, que ya mezclan dos magnitudes en el mismo eje; una línea de referencia como el umbral
3.7 confundida con la serie real por color/grosor similar). Documentar cualquier post-procesado junto con el
export que corrige.

## 5. Arquitectura de builders a crear

- `neural_raster.py` — raster neuronal 2-3 paneles, usado por `NEU_EST_UNIB/UNIG/MUL` (CSV real, §1) y
  `NEU_IMU/NEU_IMU2` (vectorizado, §1) — una sola definición de rótulos correctos resuelve F-01 para todas las
  instancias de simulación de una vez.
- `imu_dual_axis.py` — `GRAPH_IMU`/`GRAPH_IMU2` con doble eje Y (§2, vectorizado).
- Builder dedicado simple para `fig_stability_phases.png` (§3, vectorizado, acompaña a `tab:crawl_stability` que
  no se toca).
- `loaders.py` lee `vectorized/*.csv` con la misma función que CSV real — no hace falta un parser aparte (D-11).

## 6. Orden sugerido

1. Paso 0 de calibración compartida (arriba).
2. Grupo A → `fig_stability_phases.png` (baja complejidad, 1 calibración).
3. Grupo C → las 6 figuras IMU de terreno en simulación (2-6 calibraciones según el paso 0).
4. Implementar `neural_raster.py` completo (rama CSV real primero — `NEU_EST_UNIB/UNIG/MUL`, sin esperar a que el
   Grupo C esté vectorizado — luego la rama vectorizada `NEU_IMU/NEU_IMU2` una vez lista).
5. Implementar `imu_dual_axis.py` sobre el Grupo C ya vectorizado.
6. Documentar cada CSV en `experiments/_plotting/vectorized/README.md` al momento de vectorizarlo, no después.
7. Dar de alta en `PROGRESS.md` las filas `N-xx` correspondientes (`scripts/next_id.sh N`), `Category: Métricas`
   o `Escritura` según corresponda, `Data source: experiments/N-01-simulation-figure-regeneration/` (y
   `experiments/_plotting/vectorized/` en la columna de notas cuando aplique).
8. Promover con `scripts/promote_figure.sh --force` (mismos nombres que las figuras actuales en `assets/`) y
   actualizar `sections/results.tex` si algún `\label{}`/`\ref{}` cambia (F-01/F-04/F-08 no cambian labels, solo
   contenido de imagen — ver tabla de Fase 4 original, sin filas para este bloque).
9. `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh` antes de cualquier commit.
