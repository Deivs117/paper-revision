# R2-02 — FSM Gait Arbitration Baseline Comparison

**Reviewer ask:** *"Add finite state machine (FSM) gait arbitration baseline comparisons under
identical experimental conditions."* (R2-02).

**Estado de este directorio:** auditado (2026-09-01), datos verificados contra el código fuente y
las cifras del documento de referencia. Pipeline de tablas/figuras en construcción para las 5
familias con datos completos (A-Apetitivo, A-Aversivo, A-Obstáculo, B-Compleja, E-Inspección).
**Faltan C1-Terreno rugoso y C2-Pendiente** (FSM aún no ejecutado por el equipo de simulación —
ver `intake/pending/R2-02_fsm_baseline_reference.md` §9 para el instructivo de esas dos).

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
  - `experiments/simulation/familia_c1_terreno_rugoso|c2_pendiente` — mismo dataset detrás de
    `FigA/B/C_*.png` (R3-04). Sin par FSM todavía.

## Cómo regenerar

No regenerable desde cero (requiere una corrida real de Gazebo/ROS 2 por el equipo). Para
reprocesar lo ya entregado, una vez existan los scripts en `scripts/`:

```
cd experiments/R2-02-fsm-baseline
python3 scripts/build_master_table.py
python3 scripts/build_sr_vs_nl.py
python3 scripts/build_mode_timelines.py
```

## Hallazgo abierto — λ-eficiencia en conflicto (Familia B)

La fórmula de λ está bien documentada en código (`neural_recorder.py::_compute_lambda_efficiency`,
rama `fsm`): `λ=1.0` sin conflicto, `λ = |cmd_vel| / (‖actividad neuronal‖+ε)` con conflicto
(ambos rojo Y azul presentes). **Pero la cifra citada en el documento del equipo (0.982 Neural /
0.837 FSM) no se reprodujo exactamente** al recalcularla desde los CSV crudos — ver
`intake/pending/R2-02_audit_and_plan.md` Pregunta 3 para el detalle de los dos intentos de
agregación probados (ninguno calzó). Pendiente de confirmar el criterio exacto con el equipo antes
de citar esa cifra específica en el paper.

## Output files

| File in `output/` | Builder | Promoted to (`assets/...`) | Used in |
|---|---|---|---|
| *(pendiente — ver scripts/ en construcción)* | — | — | Nueva subsección `results.tex` (R2-02) + ampliación de la subsección `R3-05` existente (Familia E) |
