# R2-02 — FSM Gait Arbitration Baseline Comparison

**Reviewer ask:** *"Add finite state machine (FSM) gait arbitration baseline comparisons under
identical experimental conditions."* (R2-02).

**Estado de este directorio:** auditado (2026-09-01/02), datos verificados contra el código fuente
y las cifras del documento de referencia. Pipeline de tablas/figuras completo para las **7**
familias, incluyendo **C1-Terreno rugoso y C2-Pendiente** (FSM ejecutado y entregado 2026-09-01/02
por el equipo de simulación, con análisis propio en
`data/familia_c_fsm/experiment_c_terrain.md` — ver advertencia metodológica más abajo antes de
usar esos dos números en el paper). Ronda 2 de auditoría (`r202_audit_notes_2026-09-01.md`):
tabla maestra rehecha, gráfica SR-vs-NL ajustada — ver `intake/pending/R2-02_audit_and_plan.md`
§8 para el detalle de ambas rondas.

Todo el análisis narrativo (arquitecturas, interpretación mecanicista por familia, síntesis,
párrafo de respuesta al referee) ya vive en
`intake/pending/R2-02_fsm_baseline_reference.md` — **no se duplica aquí**. Esta carpeta es
exclusivamente la reorganización de datos + el pipeline reproducible que faltaba (tablas/figuras
que antes solo existían como Markdown manual). Auditoría de calidad de datos y hallazgos en
`intake/pending/R2-02_audit_and_plan.md`.

## Goal

Producir, de forma reproducible (no manual): la tabla maestra comparativa Neural-vs-FSM, una
gráfica de tasa de éxito vs. nivel de ruido (Familia A), y figuras de timeline modal (Familia B y
Familia E) — las piezas que `R2-02_fsm_baseline_reference.md` §8.1 pide para la sección nueva de
`results.tex` y para ampliar la subsección `R3-05` existente (Familia E).

## Método

La FSM (`fsm_gait_arbitration.py`) hereda el pipeline sensorial y de navegación completo de la red
neuronal de ganglios basales (`red_neuronal.py`) — mismo lidar, cámara, IMU, inyección de ruido,
infraestructura de pruebas. La única diferencia es el bloque de selección de modo: la red usa
inhibición lateral competitiva continua (WTA dinámica); la FSM usa una jerarquía de prioridad fija
con temporizadores de persistencia. Ver `intake/pending/R2-02_fsm_baseline_reference.md` §1 para
el detalle arquitectónico completo (verificado línea por línea contra el código fuente real en
esta auditoría).

## Parámetros / seed

Ver `config.yaml` — incluye el mapeo explícito de qué carpeta "Neural" corresponde a cada familia
FSM (varias reutilizan datasets de otros experimentos ya existentes en este repo, no duplicados).

## Data provenance

- **FSM:** ejecución real en Gazebo/ROS 2 por el equipo de simulación, entregada como
  `familia_*_fsm/` (5 familias, 80 trials). Commit pinneado:
  `10e8aac9c480a31ac21003a411e7382717b595bb` (`PETER_SIMULATION`, rama `fsm`, "docs(fsm): documento
  de referencia FSM unificado y ajustes de infraestructura") — verificado que el bloque de
  arbitraje de modo en este commit coincide exactamente con lo descrito en el documento de
  referencia del equipo.
- **Neural (comparación):** NO son datos nuevos de este experimento — se reutilizan tres fuentes ya
  existentes en el repo (ver `config.yaml`):
  - `experiments/simulation/familia_a_apetitivo|aversivo|obstaculo|compleja` — el dataset "viejo"
    de ruido genérico (mismo que alimentaba `fig1_noise_robustness_grid.png` antes de R3-04).
  - `experiments/R3-05-inspection/data/` — **el mismo dataset ya publicado y `synced-to-overleaf`
    por la fila `R3-05`**. La comparación FSM de la Familia E debe presentarse como una AMPLIACIÓN
    de esa subsección existente en `results.tex`, no como contenido nuevo separado (decisión del
    autor, 2026-09-01) — evita duplicar `fig_dfinal_vs_nlidar.png`.
  - `experiments/R3-04-noise-robustness/data/familia_c1_terreno_rugoso|c2_pendiente` — **no**
    `experiments/simulation/` (que guarda una copia más chica/desactualizada de la misma familia,
    15/15 trials vs. los 27/15 reales — confirmado por conteo cruzado contra
    `experiment_c_terrain.md`). Filtrado a `noise_level_idx=0` únicamente al comparar contra FSM
    (ver advertencia metodológica abajo).
- **FSM C1/C2 (terreno):** entregado 2026-09-01/02 por el equipo de simulación como
  `data/familia_c_fsm/{familia_c1_terreno_rugoso_fsm,familia_c2_pendiente_fsm}/` (25 y 21 trials).
  El equipo incluyó su propio análisis exhaustivo en
  `data/familia_c_fsm/experiment_c_terrain.md` — **léelo antes de citar `Tswitch`/`Tresponse`**:
  encontraron 3 diferencias de configuración entre el código BG/WTA y el código FSM (umbral
  `Upitch` 0.9 vs. 1.30; offset `tchange` +98s vs. +80s; fórmula `Tswitch` con/sin +1s de margen)
  que invalidan una comparación directa de esas dos métricas "bajo condiciones idénticas" tal como
  pide el reviewer, a menos que se re-ejecute con los parámetros igualados o se documente
  explícitamente la limitación en el paper. `success_rate`/`sim_time`/`roll_rms` sí son
  comparables (no dependen de esos tres parámetros) — incluidos en la tabla maestra con una nota
  de precaución sobre el tamaño de muestra reducido del lado Neural (N=6 en C1, N=3 en C2, por
  estar restringido a `noise_level_idx=0`).

No regenerable desde cero (requiere una corrida real de Gazebo/ROS 2 por el equipo) — los comandos
de "Output files" abajo solo reprocesan lo ya entregado en `data/`.

## Hallazgo RESUELTO — λ-eficiencia en conflicto (Familia B) reemplazada por "Conflict Exposure"

**2026-09-02, confirmado por el equipo:** la cifra "0.982 Neural / 0.837 FSM" citada en
`R2-02_fsm_baseline_reference.md` §5.2 fue un **error de documentación de una sesión anterior**,
no reproducible con ninguna agregación (valor final, pooled/per-trial de todo el trial,
pooled/per-trial solo-conflicto). Además, el promedio λ solo-en-conflicto **no es una métrica
válida** — su fórmula (`cmd_mag / ‖actividad neuronal‖`) mezcla escalas incompatibles (m/s contra
la norma de un vector de activación crudo) y da valores pequeños por diseño, no porque el sistema
decida peor. **Ambos números fueron eliminados de la tabla y del paper.**

La métrica correcta, reproducible y ya verificada por el equipo es **exposición al conflicto**:
cuánto tiempo permanece cada sistema en conflicto simultáneo real (rojo Y azul presentes) antes de
resolverlo. Para Familia B: Neural ~0.2s/trial (1.1-1.7% del tiempo del trial, según definición
del denominador) vs. FSM ~6.1s/trial (4.3-4.7%) — **el fallo de la FSM es que permanece sin
resolver ~30 veces más tiempo, no que decida peor mientras está en conflicto.** Recalculado en esta
sesión desde `sim_time_s` exacto (no una cadencia de fila asumida) — los segundos/trial coinciden
exactamente con la estimación propia del equipo; el % difiere levemente por la definición del
denominador (ver `_conflict_exposure()` en `build_master_table.py`).

**Ronda 3 (author feedback):** esta métrica se calcula y verifica en el pipeline (`CONFLICT_NOTE`
en `build_master_table.py`) pero **NO va en la tabla LaTeX-facing** (`table_master_comparison_
display.csv`) — solo 1 de 7 familias (Complex) tiene conflicto real, así que dos columnas en 0.0
para el resto del cuadro son ruido visual/ineficiente en una tabla. Los dos números (Neural
~0.2s/trial, FSM ~6.1s/trial) deben mencionarse en prosa en la sección de resultados, no como
columnas de tabla.

## Output files

| File in `output/` | Builder | Estado (ronda 2) | Used in |
|---|---|---|---|
| `table_master_comparison.csv` | `build_master_table.py` | Datos crudos (traza, no promover tal cual) | Fuente de `table_master_comparison_display.csv` |
| `table_master_comparison_display.csv` | `build_master_table.py::build_display_table` | ✅ Ronda 3: sin columna Nota (caveats van en prosa); λ-conflict-only y Conflict Exposure **ambas fuera de la tabla** (ver hallazgo resuelto abajo — los 2 valores de exposición al conflicto van en prosa, no como columnas, por ser ruido visual en 6 de 7 familias) | Nueva subsección `results.tex` (R2-02), tabla comparativa |
| `fig_sr_vs_noise_level.png` | `build_sr_vs_nl.py` | ❌ **Retirado 2026-09-02 (`C-55`)** — reemplazado por `fig_attempts_vs_noise_level.png` (ver fila abajo); `git rm`'d de `assets/`, el script se deja intacto en `scripts/` como referencia histórica pero ya no se ejecuta en el flujo normal | — |
| `fig_attempts_vs_noise_level.png` | `build_attempts_vs_nl.py` | ✅ Nuevo 2026-09-02 (`C-55`, `redundancy_closing_audit_consolidation_2026-09-02.md` P-02 homogenización) — mismo dato subyacente que `fig_sr_vs_noise_level.png` pero reportado como "intentos necesarios por misión completada" (no como % de éxito), para que "Success Rate" signifique una sola cosa (nivel de misión) en todo el paper; el hallazgo de sensibilidad al ruido (Neural necesita más reintentos, FSM nunca) queda intacto bajo su propio nombre | Subsección `results.tex` (R2-02) |
| `fig_mode_timeline_complex.png` | `build_mode_timelines.py` | ✅ Aprobado ronda 1 (nota: redacción debe explicar las fluctuaciones repentinas del modo FSM) | Nueva subsección `results.tex` (R2-02) |
| `fig_mode_timeline_inspection.png` | `build_mode_timelines.py` | ✅ Aprobado ronda 1 (misma nota que arriba) | Ampliación de la subsección `R3-05` existente |

Comandos:

```
cd experiments/R2-02-fsm-baseline
python3 scripts/build_master_table.py    # escribe la tabla cruda + la _display.csv
python3 scripts/build_attempts_vs_nl.py  # reemplaza a build_sr_vs_nl.py desde C-55
python3 scripts/build_mode_timelines.py
```
