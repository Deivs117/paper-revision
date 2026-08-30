# R02-01-05 — Simulación N-01, Grupo 2: rasters neuronales (F-01) + IMU doble eje (F-04) + walk sequence (F-08) — PENDIENTE

**Estado (actualizado 2026-08-29, revisión frame-by-frame): ⚠ Parcialmente promovido, bloqueado por letras de
panel faltantes.** `N-07` (`fig_stability_phases.png`) y la mitad de `N-08` (`GRAPH_IMU.png`/`GRAPH_IMU2.png`)
ya están **promovidos a `assets/`** tras verificación visual — coinciden exactamente con el original (N-07:
paneles A–F, valores TR; N-08 parcial: doble eje, notación $\sigma_{az}$, línea de umbral 3.7, títulos por
terreno). **Bloqueado:** `N-06` completo (`NEU_EST_UNIB/UNIG/MUL`) y la otra mitad de `N-08`
(`NEU_IMU.png`/`NEU_IMU2.png`) — el builder `neural_raster.py` regenera correctamente el contenido de cada
subplot pero **omite por completo las letras de panel `a)`/`b)`/`c)`/`d)`** que el original dibuja como texto
dentro de la imagen. Ver §0ter abajo para el detalle completo por figura — es más grave de lo que anticipaba
§0bis: no es solo `NEU_EST_UNIG`/`NEU_EST_MUL` (ya identificadas ahí), sino que **`NEU_IMU2` tiene la misma
restricción y §0bis no la había detectado** (`\ref{fig:NEU_IMU2}a`/`b`, `results.tex:223/225`).

**No promover `N-06`/`NEU_IMU2` ni tocar `results.tex` hasta que el autor decida** cómo resolver las letras
faltantes (§0ter tiene el detalle de qué builder necesita el fix y si hay además un reordenamiento de contenido,
no solo letras ausentes, en el caso de `NEU_EST_MUL`).

**Origen:** `intake/pending/R02-01_metric_and_figure_audit.md` §3 (F-01, F-04, F-08) + `intake/pending/R02-01_data_traceability_and_plotting_plan.md`
§2 (D-1, D-8, D-11, F-Data-03/04/05) + §3.4 Grupo 2 (ambos eliminados tras atomizarse, ver
`intake/R02-01_INDEX.md`).

## 0. Por qué estas 3 tareas van juntas

Las tres comparten la misma causa técnica (sin CSV crudo recuperable, D-1 ya descartó preguntar al equipo como
método) y el mismo método de recuperación (vectorización), agrupadas en 2 de los 4 grupos de calibración
compartida de Informe 2 (Grupo A y Grupo C — los Grupos B y D ya se cerraron, ver
`intake/processed/R02-01-02_fisico_regeneracion_N02-N05.md`).

## 0bis. Confirmación de alcance (autor, 2026-08-29) + restricción nueva de numeración de paneles

El autor confirmó que "vectorizar y arreglar todas las imágenes NEU_\* y rasterogramas similares" **es
exactamente el alcance ya descrito en este documento** (§1 y §5: `NEU_EST_UNIB/UNIG/MUL` rama CSV real,
`NEU_IMU/NEU_IMU2` rama vectorizada, más `GRAPH_IMU/GRAPH_IMU2`/`RES_IMU/RES_IMU2.0` del Grupo C en §4) — no
agrega figuras nuevas al bloque.

**Restricción nueva, bloqueante para `neural_raster.py`:** en la auditoría del 2026-08-29 el autor señaló que
`NEU_EST_UNIG.png` y `NEU_EST_MUL.png` "perdieron los índices" al pensar en su regeneración — aclarado: se
refiere a la **numeración de sub-panel (a/b/c/d) que `results.tex` cita por letra**, no a ticks de eje ni a
columnas del CSV. `results.tex` ya depende de una lectura fija de panel por letra:

- `\ref{fig:NEU_EST_UNIG}` (sensory network) y `\ref{fig:NEU_EST_UNIG}b` (locomotor decision network) — línea 36/45.
- `\ref{fig:NEU_EST_MUL}a` (basal ganglia, línea 144), `b` (evasive sensory, línea 142), `c` (locomotion control,
  línea 142/144), `d` (terrain-instability units $X_1$/$X_2$, línea 150).

`neural_raster.py` debe **preservar exactamente ese orden y esas letras de panel** para `NEU_EST_UNIG`/
`NEU_EST_MUL` al regenerar desde CSV real. Si el nuevo builder reordena o renombra paneles por cualquier razón
de diseño, es obligatorio actualizar las referencias `\ref{fig:NEU_EST_MUL}a-d` / `\ref{fig:NEU_EST_UNIG}b` en
`results.tex` en el mismo commit (misma disciplina que la tabla de referencias cruzadas de
`R02-01-04` §4) — nunca dejar que la letra en la figura y la letra citada en el texto diverjan. Verificar esto
como paso explícito antes de promover estas dos figuras.

## 0ter. Verificación del 2026-08-29 — letras de panel ausentes en el output regenerado

Se comparó cada imagen de `experiments/N-01-simulation-figure-regeneration/output/` contra su versión actual en
`assets/`, panel por panel (visualmente, no solo por nombre de archivo), tal como pedía §0bis. Resultado:

| Figura | Letras en `assets/` (actual) | Letras en el output regenerado | Contenido por letra | Veredicto |
|---|---|---|---|---|
| `NEU_EST_UNIB.png` | a) Locomotion Module, b) March Decision Module | **ninguna** | mismo contenido, mismo orden | No bloqueada por `\ref` (`results.tex` la cita sin letra) — **promovible igual, pero pierde las letras visualmente** |
| `NEU_EST_UNIG.png` | a) sensory (LiDAR/Input/Response/Auxiliar), b) Locomotion Module, c) March Decision Module | **ninguna** | mismo agrupamiento por módulo, mismo orden (a=sensorial, b=Locomotion, c=Decision) | **Bloqueada** — `\ref{fig:NEU_EST_UNIG}b` (línea 36/45) no tiene letra que apuntar |
| `NEU_EST_MUL.png` | a) Basal Ganglia, b) LiDAR Net, c) Locomotion, d) March Decision (grilla 2×2) | **ninguna** | **orden cambiado**: Basal Ganglia, luego Locomotion, luego LiDAR Net, luego Gait Decision (columna única) — b/c intercambiados respecto al original | **Bloqueada, más grave que las otras dos** — no es solo falta de letras, el contenido que "b" y "c" señalarían en texto (línea 142/144/150) quedaría cruzado si alguien agrega letras a/b/c/d en el orden de lectura actual del nuevo layout |
| `NEU_IMU.png` | a) Locomotion Module, b) March Decision Module | **ninguna** | mismo contenido, mismo orden | No bloqueada por `\ref` — **mismo caso que `NEU_EST_UNIB`** |
| `NEU_IMU2.png` | a) Locomotion Module, b) March Decision Module | **ninguna** | mismo contenido, mismo orden (a=Locomotion, b=Decision, coincide) | **Bloqueada — hallazgo nuevo, §0bis no la había listado**: `\ref{fig:NEU_IMU2}a` (línea 223) y `\ref{fig:NEU_IMU2}b` (línea 225) sí dependen de la letra |
| `GRAPH_IMU.png` / `GRAPH_IMU2.png` | sin letras en el original | sin letras (no aplica) | — | Sin restricción — **promovidas** (verificación de contenido: doble eje, notación $\sigma_{az}$, línea de umbral 3.7, título por terreno, todo correcto) |
| `fig_stability_phases.png` | A–F (no citadas por letra en `results.tex`) | A–F preservadas, coinciden panel por panel | — | Sin restricción de `\ref`, letras además sí se preservaron — **promovida** |

**Causa técnica probable:** las 4 figuras afectadas (`NEU_EST_UNIB/UNIG/MUL`, `NEU_IMU`, `NEU_IMU2`) salen todas
del mismo builder nuevo `neural_raster.py` (§5) — el defecto de letras ausentes es del builder, no de una figura
puntual. `NEU_EST_MUL` además sufre un reordenamiento real del layout (2×2 → columna única), no solo la letra.

**Qué se promovió ya (2026-08-29):** `fig_stability_phases.png`, `GRAPH_IMU.png`, `GRAPH_IMU2.png` — ver
`PROGRESS.md` (`N-07` → `applied`, `N-08` con nota de promoción parcial). **Qué queda bloqueado, sin tocar
`results.tex` ni promover:** `NEU_EST_UNIB/UNIG/MUL` (`N-06` completo) y `NEU_IMU/NEU_IMU2` (mitad de `N-08`).

**Decisión pendiente del autor** — opciones, sin asumir ninguna:
1. Arreglar `neural_raster.py` para que vuelva a dibujar las letras `a)/b)/c)/(d)` en el mismo orden de lectura
   que el layout actual de `assets/` (para `NEU_EST_UNIB`/`NEU_IMU`/`NEU_IMU2`, el contenido por módulo ya
   coincide en ese orden — sería solo re-agregar el texto). Para `NEU_EST_MUL`, además hay que decidir si se
   revierte el layout a la grilla 2×2 original (más simple, preserva letras/orden sin tocar `results.tex`) o si
   se acepta el nuevo layout en columna y se actualiza `\ref{fig:NEU_EST_MUL}a-d` en `results.tex` para que
   apunte a los módulos correctos en su nuevo orden.
2. Promover igual `NEU_EST_UNIB`/`NEU_IMU` (no bloqueadas por `\ref`, solo pierden la anotación visual de letra)
   y dejar bloqueadas únicamente `NEU_EST_UNIG`/`NEU_EST_MUL`/`NEU_IMU2` — parcializa aún más `N-06`/`N-08` pero
   avanza lo que sí es seguro.
3. Dejar las 4 figuras de `neural_raster.py` sin promover hasta corregir el builder de una vez, evitando una
   promoción fragmentada de `N-06`.

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

## 6. Orden interno de este bloque

1. Paso 0 de calibración compartida (arriba).
2. Grupo A → `fig_stability_phases.png` (baja complejidad, 1 calibración).
3. Grupo C → las 6 figuras IMU de terreno en simulación: `NEU_IMU.png`, `NEU_IMU2.png`, `GRAPH_IMU.png`,
   `GRAPH_IMU2.png`, `RES_IMU.png`, `RES_IMU2.0.png` (2-6 calibraciones según el paso 0).
4. Implementar `neural_raster.py` completo (rama CSV real primero — `NEU_EST_UNIB/UNIG/MUL`, sin esperar a que el
   Grupo C esté vectorizado — luego la rama vectorizada `NEU_IMU/NEU_IMU2` una vez lista).
5. Implementar `imu_dual_axis.py` sobre el Grupo C ya vectorizado.
6. Documentar cada CSV en `experiments/_plotting/vectorized/README.md` al momento de vectorizarlo, no después.
7. Dar de alta en `PROGRESS.md` las filas `N-xx` correspondientes (`scripts/next_id.sh N`), `Category: Métricas`
   o `Escritura` según corresponda, `Data source: experiments/N-01-simulation-figure-regeneration/` (y
   `experiments/_plotting/vectorized/` en la columna de notas cuando aplique).

## 7. Orden combinado con `R02-01-04` (confirmado 2026-08-27 — deadline 2026-08-31, ambos bloques priorizados por igual)

Los dos bloques comparten infraestructura (mismo motor de extracción de píxel, mismo `experiments/_plotting/`,
mismo `PROGRESS.md` fila `N-01`) — este es el orden real de ejecución, intercalando por dependencia técnica, no
por documento:

1. **`R02-01-04` pasos 1-2** (vectorizar panel de Obstacle + parchear `macro_robustness.py`) — desbloquea la
   pieza más avanzada primero.
2. **En paralelo:** `neural_raster.py`, rama CSV real (`NEU_EST_UNIB/UNIG/MUL`, §1 de este documento, §4 paso 4
   parcial) — no depende de ninguna vectorización, se puede hacer mientras se vectoriza Obstacle.
3. **`R02-01-04` pasos 3-9** (regenerar, revisar, promover rejilla + FigA/B/C, actualizar `results.tex`/
   `PROGRESS.md`) — cierra el bloque más cercano a terminar.
4. **Paso 0 de calibración compartida** de este documento (§4) — mientras el paso 3 corre validaciones, se puede
   adelantar la inspección visual de los Grupos A y C.
5. **Grupo A** (`fig_stability_phases.png`, §3) — más simple, 1 calibración, cierra F-08 rápido.
6. **Grupo C** (6 figuras IMU, §1 parcial + §2) — el más largo del bloque combinado; si el tiempo aprieta antes
   del 31, es el candidato a recortar primero (ver nota de priorización abajo).
7. **`neural_raster.py` rama vectorizada** (`NEU_IMU`/`NEU_IMU2`) + **`imu_dual_axis.py`** (`GRAPH_IMU`/
   `GRAPH_IMU2`) sobre el Grupo C ya vectorizado.
8. Promoción final de todo lo de este documento (`--force`, mismos nombres que hoy en `assets/` — F-01/F-04/F-08
   no cambian ningún `\label{}`/`\ref{}` en `results.tex`, solo contenido de imagen), filas `N-xx` en
   `PROGRESS.md`, `validate_tex.sh`/`check_roundtrip.sh`.

**Nota de priorización si el tiempo no alcanza para todo antes del 31:** dentro de este bloque, F-01 en
`NEU_EST_UNIB/UNIG/MUL` (paso 2, CSV real, sin vectorizar) es el de mayor relación beneficio/esfuerzo — corrige
la traducción incorrecta en 3 figuras sin ningún trabajo de vectorización. El Grupo C (paso 6, 6 figuras,
2-6 calibraciones) es el de mayor esfuerzo y el candidato más razonable a quedar para la siguiente ronda de
revisión si hace falta recortar, dejando F-01/F-04 de simulación documentados como pendientes explícitos en vez
de forzar una vectorización apurada.
8. Promover con `scripts/promote_figure.sh --force` (mismos nombres que las figuras actuales en `assets/`) y
   actualizar `sections/results.tex` si algún `\label{}`/`\ref{}` cambia (F-01/F-04/F-08 no cambian labels, solo
   contenido de imagen — ver tabla de Fase 4 original, sin filas para este bloque).
9. `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh` antes de cualquier commit.
