# C-22 — Investigación y reconciliación: `tab:consolidated_simulation_metrics` vs. datos recalculados

**Origen:** hallazgo abierto en la fila `N-01` de `PROGRESS.md` ("new finding, out of scope for
this row"), reaparecido de forma independiente en `R2-02` al recalcular las mismas cuatro familias
para la comparación FSM-vs-Neural. El autor pidió investigar la causa raíz antes de reconciliar, y
decidió (2026-09-02) quedarse con los valores recalculados desde los datos crudos, no con los ya
publicados.

## 1. Qué se investigó

Recalculando Roll RMS desde `trial_summary.json` para las 4 familias de `experiments/simulation/`
(mismo dataset que alimentó la Tabla 6 original), 3 de 4 no coincidían con lo publicado:

| Familia | Roll publicado | Roll recalculado (sin excluir nada) |
|---|---|---|
| Appetitive | 0.54 ± 0.01 | 0.536 ± 0.009 — **coincide** |
| Aversive | 0.62 ± 0.04 | 1.357 ± 0.106 — no coincide |
| Obstacle | 0.55 ± 0.02 | 3.931 ± 8.925 — no coincide, SD mayor que la media |
| Complex | 0.58 ± 0.03 | 1.034 ± 0.349 — no coincide |

## 2. Hallazgo — anomalía real de datos en un trial de Obstacle

`familia_a_obstaculo/test_007_SUCCESS` tiene `roll_rms = 37.32°`, mientras los otros 14 trials de
la misma familia están todos en el rango 1.05°–1.77°. Su propia serie por-timestep
(`unified_metrics.csv`) llega hasta **108° de RMS** — físicamente implausible para un ángulo de
roll estable (el robot no da vueltas completas repetidas en este escenario). Es casi seguro un
trial con inestabilidad real no capturada por su veredicto `SUCCESS`, no un bug de cálculo del
script. **Decisión del autor: excluir este trial de cualquier estadística recalculada** (su
veredicto de éxito/fallo no se toca, solo sus lecturas de roll/pitch/tiempo).

Excluyéndolo, Obstacle Roll baja de 3.93±8.92° a **1.55±0.15°** — mucho más consistente
internamente, pero **todavía ~2.8x más alto** que el 0.55° publicado.

## 3. Por qué Aversive/Complex NO tienen un outlier — y aun así no coinciden

Revisé los 15 trials de `familia_a_aversivo` y `familia_b_compleja` uno por uno: **ningún trial
es anómalo**, la dispersión es genuina y consistente en ambas familias (Aversive: 1.16°–1.50°;
Complex: 0.56°–1.81°). Es decir, el recálculo de estas dos familias no tiene ningún dato corrupto
que excluir — el promedio de 15 trials limpios simplemente es ~2x más alto que lo publicado, en
ambas familias, de forma sistemática.

**Patrón observado:** Appetitive (la única familia sin maniobra evasiva/transición de marcha
brusca) es la única donde recálculo y publicado casi coinciden. Esto sugiere que el número
publicado pudo haberse calculado sobre una ventana de estado estable (excluyendo el pico
transitorio de un cambio de marcha), mientras que el recálculo usa el trial completo. **No se
pudo confirmar esta hipótesis con evidencia dura** — no sobrevive ningún script o nota que
documente el método exacto usado para generar la Tabla 6 original, y el historial de git de
`experiments/simulation/` no ayuda: la carpeta estuvo *sin versionar* desde el inicio del repo
hasta el commit `a96ce32` (2026-08-27), que la trackeó por primera vez sin indicar si los archivos
en disco habían cambiado antes de ese punto. No hay forma de probar, con lo disponible en este
repo, si la Tabla 6 original vino de un run distinto o de un método de cálculo distinto.

## 4. Decisión aplicada

Por instrucción explícita del autor: **`tab:consolidated_simulation_metrics` se reemplaza
íntegramente por los valores recalculados** (Success/T_sim/Roll/Pitch, las 4 familias), con
`test_007_SUCCESS` excluido de las estadísticas de Obstacle. No se intentó reproducir el método
exacto de la tabla original (opción de la Pregunta 1 no elegida) — se documenta la investigación
como evidencia de que la discrepancia es real y no un error de este pipeline, pero se prioriza
tener un número reproducible desde código sobre reconstruir un método que ya no es recuperable.

**Mismo criterio aplicado a la Tabla `tab:fsm_comparison` (R2-02):** la fila Obstacle/Neural
usaba el mismo dataset con el mismo trial anómalo (con nota-†, "outlier no excluido"). Actualizada
para excluirlo también — `results.tex` ambas tablas quedan mutuamente consistentes.

**Efecto adicional encontrado:** el mismo trial también distorsionaba visiblemente un punto de
`fig1_noise_robustness_grid.png` (panel Pitch RMS, familia Obstacle, nivel de ruido 1 — barra de
error subía a ~3.2° por 1 de solo 3 trials en ese punto). Corregido con la misma exclusión.

## 5. Archivos tocados

- `experiments/_plotting/builders/macro_robustness.py`: `EXCLUDED_TRIALS` (nuevo), aplicado en
  `build_consolidated_table()` y `collect_scenario()` (así que también corrige
  `fig1_noise_robustness_grid.png`).
- `experiments/R2-02-fsm-baseline/scripts/build_master_table.py`: mismo `EXCLUDED_TRIALS`,
  aplicado en `collect()`.
- `sections/results.tex`: `tab:consolidated_simulation_metrics` (4 filas reemplazadas + nota en
  el párrafo previo), `tab:fsm_comparison` (fila Obstacle/Neural + caption, sin el †).
- `assets/fig1_noise_robustness_grid.png` re-promovida.
- `reassemble.py`/`validate_tex.sh`/`check_roundtrip.sh`/`compile_pdf.sh` — todos pasan.

## 6. Lo que sigue sin explicación (documentado, no bloqueante)

Por qué el número publicado original de Aversive/Complex/Obstacle era sistemáticamente más bajo y
más ajustado que el recálculo del trial completo — sin outlier de por medio en 2 de las 3
familias — queda sin causa raíz confirmada. Se documenta aquí como el estado final de la
investigación, no como un hallazgo pendiente adicional.
