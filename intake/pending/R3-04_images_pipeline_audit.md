# Auditoría del pipeline de generación de imágenes — compatibilidad con los datos nuevos de R3-04

**Estado:** análisis/planificación únicamente (rama separada, ligada a
`intake/pending/R3-04_audit_and_plan.md` pero con su propio alcance: qué imágenes existen, cómo se
generan, y cuáles hay que regenerar/crear para R3-04). **No se generó ninguna figura nueva ni se
modificó ningún script en esta sesión** — solo se auditó lo que ya existe (inspección de código +
inspección visual "pixel a pixel" de las figuras publicadas, con el visor de imágenes).

---

## 1. Dónde está el pipeline (respuesta directa a "no sé dónde se encuentra")

```
experiments/_plotting/                       # librería compartida — TODO el pipeline de figuras vive aquí
├── loaders.py                                # parsing puro de CSV/JSON (family_dir/test_NNN[_VERDICT]/*)
├── style.py                                   # colores/DPI compartidos (SCENARIO_COLORS, TERRAIN_COLORS)
├── generate_all_simulation.py                 # entry point — llama a macro_robustness + ecdf_phase_space
├── builders/                                   # un módulo por figura o familia de figuras
│   ├── macro_robustness.py                     # fig1_noise_robustness_grid.png (4 escenarios x 3 métricas)
│   ├── ecdf_phase_space.py                     # FigA/FigB/FigC (terreno rugoso + pendiente)
│   ├── classifier_suite.py, energy_transition.py, imu_dual_axis.py, imu_terrain_real.py,
│   │   real_plot_suite.py, stability_phases.py, transition_phases.py   # otras figuras (ver §4 — no
│   │                                                                     dependen de datos de ruido)
├── extract/                                    # scripts de vectorización pixel-a-pixel de figuras ya publicadas
├── vectorized/                                  # CSVs producidos por extract/, con README de trazabilidad
└── .venv_plotting/  (gitignored)                # venv desechable: numpy/matplotlib/pandas/pillow

experiments/N-01-simulation-figure-regeneration/  # el "experimento" que envuelve el pipeline de arriba
├── README.md                                     # historial completo de decisiones (D-1 a D-14, 3 rondas)
├── output/                                       # las figuras ya regeneradas y promovidas (ver PROGRESS.md N-01/N-06/N-08/N-09)
└── scripts/regenerate_neu_panels.py

experiments/simulation/                          # el dataset VIEJO (ruido genérico único, sin drift/illum) que alimentó todo lo anterior
```

**Hallazgo clave (responde directamente a "si el pipeline existente es completo"):** el pipeline
**ya fue diseñado, el 2026-08-27, para este momento exacto**. El README de N-01 documenta una
decisión explícita, **D-12**: *"a future re-run lands in a new sibling directory... this pipeline
takes `--simulation-root` as a CLI flag for exactly this reason — no code change needed to point
it at the new batch, only the root path."* Es decir: apuntar el pipeline a
`experiments/R3-04-noise-robustness/data/` en vez de `experiments/simulation/` es, en el diseño
original, un cambio de un solo flag — **no un pipeline por construir desde cero.** Pero (ver §3) no
es tan simple en la práctica: dos de los tres builders relevantes tienen dependencias de datos que
los datos nuevos no satisfacen igual de bien que los viejos.

---

## 2. Qué genera hoy — inventario completo, verificado visualmente

Inspeccioné con el visor de imágenes (no solo el código) `fig1_noise_robustness_grid.png`,
`FigA_Stability_Profile.png`, `FigB_Decision_Delay.png`, `FigC_Terrain_Adaptability.png` y
`fig2_Appetitive_micro_test_005_SUCCESS.png` — los cinco archivos en `assets/` tal como se ven hoy
en el paper. Contenido confirmado pixel a pixel (no solo por el nombre del archivo o el docstring):

| Figura (`assets/`) | Builder | Datos que consume hoy | Confirmado visualmente |
|---|---|---|---|
| `fig1_noise_robustness_grid.png` | `macro_robustness.py` | `experiments/simulation/` (4 familias: apetitivo, aversivo, obstáculo, compleja) | Grid 4×3, eje X **"Sensory Noise Index (σ)"** (genérico, NO menciona IMU/LiDAR/cámara) — confirma la ambigüedad que `PROGRESS.md` ya señalaba para R3-04. |
| `FigA_Stability_Profile.png` | `ecdf_phase_space.build_fig_a` | `stability_log.csv` (serie `TR`) de `experiments/simulation/familia_c1_terreno_rugoso`/`familia_c2_pendiente` | Curvas densas y suaves (cientos de muestras por trial) — confirma que en el dataset VIEJO `stability_log.csv` sí estaba bien poblado. |
| `FigB_Decision_Delay.png` | `ecdf_phase_space.build_fig_b` | `trial_summary.json.tswitch`, mismas 2 familias | ECDF de 2 paneles, coincide con la prosa actual de `results.tex` (0.2–0.7 ms rugoso con cola a 0.6 s; escalera 0.9–1.8 ms pendiente). |
| `FigC_Terrain_Adaptability.png` | `ecdf_phase_space.build_fig_c` | `roll_rms`/`pitch_rms` de esas 2 familias, **N=30, sin desglose por nivel de ruido** | Scatter simple, sin codificar `noise_level_idx` en color/forma — nunca mostró efecto de ruido, solo separación por terreno. |
| `fig2_Appetitive_micro_test_005_SUCCESS.png` (+ Aversive/Obstacle/Complex) | **Ninguno — sin script en todo el repo** | — | Panel A (firing variance) + Panel B (roll/pitch RMS) de UN solo trial (`test_005`) por escenario. Confirmado por `grep` exhaustivo: no existe ningún `.py` que produzca "Firing Variance Response Profile" ni "Kinematic Stability Footprint". |

**`tab_consolidated_simulation_metrics.csv`** (recompute de `macro_robustness.build_consolidated_table`):
tiene un mismatch histórico sin resolver contra la tabla publicada (p. ej. Obstacle Roll: 3.93±8.92°
recomputado vs. 0.55±0.02° publicado — anotado en `PROGRESS.md` fila N-01, nunca investigado). Esto
es anterior a R3-04 y no lo introduce esta auditoría, pero **hay que resolverlo o el nuevo recompute
con datos R3-04 heredará la misma sospecha de inconsistencia.**

---

## 3. Compatibilidad con `experiments/R3-04-noise-robustness/data/` — builder por builder

### 3a. `macro_robustness.py` (fig1 grid) — **compatible con cambios menores, requiere decisión de framing**
- El layout de carpetas es idéntico (`familia_a_apetitivo/test_NNN_VERDICT/trial_summary.json` con
  `seed_info.noise_level_idx`) → apuntar `--simulation-root` a los datos nuevos funciona sin tocar
  `loaders.py`.
- **Pero** el eje sigue siendo un índice genérico "σ" — no cumple la petición explícita del
  reviewer de nombrar IMU drift / LiDAR noise / camera illumination. Esto es justo lo que
  `PROGRESS.md` ya preguntaba para R3-04. Con los datos nuevos, `noise_level_idx` sí tiene semántica
  por sensor documentada (`config.yaml` de R3-04), así que el builder (o una versión nueva) debería
  anotar el eje / la leyenda con esa tabla, no solo relabelear "σ" a otra palabra genérica.
- El `SCENARIOS` hardcodeado (4 familias) no incluye `familia_c1_terreno_rugoso`/`familia_c2_pendiente`
  — correcto, esas dos siempre vivieron en `ecdf_phase_space.py`, no en este grid.
- **No traza `Tswitch`** (la métrica que el propio equipo propuso como Figura R1 en
  `robustez_transferencia_tecnica.md` §11) — el grid actual solo tiene T_sim/Pitch RMS/Latencia.
  Añadir Tswitch es una columna nueva, no una simple sustitución de datos.
- La lógica de fallback de latencia para `familia_a_obstaculo` (vectorizado desde el PNG viejo)
  queda obsoleta si el dataset nuevo sí tiene latencia poblada — **hay que verificar si
  `data/familia_a_obstaculo/*/trial_summary.json.exp_latency` está poblado esta vez** (no lo verifiqué
  en esta pasada; ver Pregunta 4 abajo).

### 3b. `ecdf_phase_space.py` (FigA/B/C) — **FigA está bloqueada por un hueco real de datos**
- **FigA (Stability Profile) depende exclusivamente de `stability_log.csv`.** La auditoría de
  `R3-04_audit_and_plan.md` §3c ya estableció que, en los datos nuevos, `stability_log.csv` está
  vacío (solo cabecera) en la mayoría de los 27 trials de `familia_c1_terreno_rugoso` y en 8/15 de
  `familia_c2_pendiente` — solo 7/15 trials de c2 tienen filas reales. **Apuntar `build_fig_a()`
  directamente a `data/` con el código actual producirá una figura vacía o con una sola curva
  parcial (c2) y ninguna para c1.** Esto no es un problema de compatibilidad de formato, es que el
  dato en sí no está — el builder no tiene nada que arreglar por su cuenta.
  - **Camino alternativo ya identificado:** usar el campo `tr` de `trial_summary.json` (bien
    poblado en ambos datasets) — pero `tr` es **un escalar final por trial**, no una serie temporal
    alineada al instante de cambio de modo como pide FigA. No puede reconstruir la misma figura;
    como mucho permite un gráfico distinto (p. ej. `tr` final vs. `noise_level_idx`, un boxplot o
    scatter, no una curva TR(t) alineada). Ver Pregunta 1 abajo — es una decisión de diseño de
    figura, no solo de código.
- **FigB (Decision Delay ECDF)** solo necesita `trial_summary.json.tswitch` — bien poblado en ambas
  familias del dataset nuevo (confirmado en la auditoría de datos). Compatible sin cambios, más
  allá de añadir el desglose por `noise_level_idx` si se quiere mostrar el efecto del ruido (hoy
  agrupa los 15 trials de cada familia en una sola ECDF, sin separar por nivel).
- **FigC (Terrain Adaptability)** usa `roll_rms`/`pitch_rms` — poblado en ambas familias nuevas.
  Compatible, pero (igual que hoy) no muestra el nivel de ruido — sería la Figura R2 propuesta por
  el equipo (`robustez_transferencia_tecnica.md` §11) si se le añade color/forma por
  `noise_level_idx`, algo que el builder actual no hace.

### 3c. `fig2_*_micro` (4 figuras) — **sin builder, hay que construirlo desde cero**
No hay nada que "re-apuntar" — nunca existió un generador reproducible, ni para el dataset viejo ni
para cualquier otro. Si se quiere una versión de estas 4 figuras con un trial representativo del
dataset R3-04 (p. ej. de nuevo `test_005`, si existe con ese índice y verdict `SUCCESS`), hay que
escribir un builder nuevo que lea `metrics_raw.csv` de un trial puntual — trivial en términos de
datos (las columnas `firing_variance`/`roll_rms`/`pitch_rms` ya existen en el dataset nuevo), pero
es trabajo no existente, no una reutilización.

---

## 4. Figuras del pipeline que NO dependen del dataset de ruido — fuera de alcance de R3-04

Confirmado por lectura de cada builder: `classifier_suite.py` (MLP/clasificador, ligado a R2-04),
`energy_transition.py` y `real_plot_suite.py` (hardware físico, `experiments/real/`),
`imu_dual_axis.py`, `imu_terrain_real.py`, `stability_phases.py`, `transition_phases.py` — todos
estos consumen CSVs **vectorizados a mano** desde figuras ya publicadas (`NEU_EST_*`, `NEU_IMU*`,
`GRAPH_IMU*`, `fig_stability_phases.png`, `fig_transition_phases_v10.png`), no la carpeta
`family_dir/test_NNN` cruda. `PROGRESS.md` (filas N-06/N-08/N-09) confirma que **ni siquiera el
dataset viejo tenía CSV crudo para estas** — son reconstrucciones pixel-a-pixel del PNG ya
publicado, sin dato fuente regenerable en ningún punto de la historia de este repo. **No se ven
afectadas por la llegada de R3-04** a menos que el equipo decida específicamente rehacer esas
corridas puntuales también (serían experimentos nuevos, no una extensión de este).

---

## 5. Qué falta construir/modificar — resumen accionable

| Ítem | Estado del pipeline hoy | Acción necesaria |
|---|---|---|
| Fig R1 (`Tswitch` vs. nivel de ruido, 4 familias comportamentales) | Parcialmente cubierto por `macro_robustness.py` (tiene T_sim/Pitch/Latency, no Tswitch) | Extender el builder con una columna/figura nueva para `Tswitch` |
| Reencuadre "σ genérico" → IMU drift/LiDAR/iluminación | No existe | Anotar ejes/leyenda o caption citando `config.yaml`; decisión de diseño, no solo de datos (ver Pregunta 2) |
| Fig R2 (`roll_rms`/`pitch_rms` vs. nivel de ruido, terreno rugoso + pendiente) | No existe tal cual — `FigC` es lo más cercano pero sin eje de ruido | Nuevo builder o extensión de `ecdf_phase_space.build_fig_c` |
| Fig R3 (dropout de cámara, serie `blue_present` del par de trials `familia_a_apetitivo` #7) | No existe | Nuevo builder, trivial en datos (columna ya está en `metrics_raw.csv`) |
| FigA (Stability Profile) con datos nuevos | **Bloqueado** — dato fuente (`stability_log.csv`) insuficiente en el dataset nuevo | Decisión de diseño + posiblemente pedir al equipo que instrumente `stability_log.csv` en una futura corrida (ver Pregunta 1) |
| FigB/FigC con datos nuevos (sin desglose de ruido) | Compatible tal cual | Repuntar `--simulation-root`; opcionalmente añadir desglose por nivel |
| `fig2_*_micro` con datos nuevos | Sin builder (nunca existió) | Construir desde cero si se decide mantener esta figura |
| Tabla R1 (tasa de fallo por familia) | No existe como script | Trivial — conteo directo de manifiestos, ya tabulado a mano en `robustez_transferencia_tecnica.md` §10 |
| Tabla R2 (parámetros de perturbación por sensor) | No existe como script | Trivial — ya está en `config.yaml`/`robustez_transferencia_tecnica.md` §3, solo falta formatear como tabla LaTeX |
| `tab_consolidated_simulation_metrics.csv` mismatch histórico | Sin resolver, anterior a R3-04 | Investigar antes de recomputar con datos nuevos, para no arrastrar la misma duda |
| Latencia de `familia_a_obstaculo` (vectorizada por falta de dato real en el dataset viejo) | Fallback vectorizado activo | Verificar si el dataset NUEVO sí tiene `exp_latency` poblado — si sí, el fallback deja de ser necesario para R3-04 (aunque seguiría existiendo para el dataset viejo) |

---

## Preguntas — resueltas 2026-08-31

1. **FigA_Stability_Profile — RESUELTO: se deja tal como está.** Decisión del autor: la figura
   registrada/generada anteriormente (dataset viejo, `experiments/simulation/`) se mantiene sin
   cambios, y por lo tanto **el texto de `results.tex` que la describe (`fig:stability_profile`,
   §3.1) tampoco se toca** — no hay número ni afirmación que corregir ahí para esta ronda de R3-04.
   Sin acción pendiente sobre esta figura.

2. **`fig1_noise_robustness_grid.png` (grid 4×3, eje "σ" genérico) — RESUELTO: se reemplaza por
   completo.** Nuevo módulo `noise_sweep_grid.py` (NO se editó `macro_robustness.py`, que sigue
   siendo válido para el dataset viejo) — ver §7 abajo.

3. **`fig2_*_micro` — RESUELTO: SÍ se regenera, siguiendo el mismo criterio de precisión que
   `experiments/N-02-physical-figure-regeneration` usó para las figuras reales equivalentes
   (`{Escenario}_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png`).** Implementado y ejecutado en
   esta sesión — ver §6 abajo.

**Además, resuelto en la misma ronda:** Fig R2 (postural stability vs. ruido, terreno/pendiente),
Fig R3 (evidencia de dropout de cámara) y Tablas R1/R2 (tasa de fallo, parámetros de perturbación)
— el autor pidió construir las 5 piezas restantes ahora en vez de esperar a la sesión de escritura.
Ver §7.

4. ~~Verificación pendiente~~ **Ya verificado:** `exp_latency` **sí está poblado** en los 15/15
   trials `SUCCESS` de `data/familia_a_obstaculo/` del dataset nuevo (valores reales
   0.0001–0.465 s, no el centinela `-1.0` del dataset viejo, que tenía 0/15). Esto significa que,
   para la parte de R3-04, el fallback vectorizado de `macro_robustness.py`
   (`vectorized/fig1_obstacle_latency.csv`, reconstrucción del PNG viejo) **ya no es necesario** —
   el builder puede leer la latencia real directamente de `trial_summary.json.exp_latency`, sin
   activar la cadena de fallback. El fallback debe seguirse conservando solo por si en algún
   momento se vuelve a graficar el dataset viejo (`experiments/simulation/`), no se debe borrar el
   CSV vectorizado.

---

## 6. `fig2_*_micro` — construido esta sesión

Nuevo builder `experiments/_plotting/builders/micro_dynamics.py` (+ 2 helpers nuevos en
`loaders.py`: `load_unified_metrics`, `find_trial_by_noise_level`), calcado de
`real_plot_suite.py::build_rms_dynamics()` (N-02):

- Mismo layout 2 paneles: **A. Basal Ganglia Neural Response Dynamics** (firing variance, naranja
  fijo `#D55E00`) / **B. Chasis Kinematic Attitude Stabilization Space** (Pitch/Roll RMS, púrpura
  `#4B0082`/lavanda `#B8A9D9` fijos) — títulos igualados palabra por palabra con la versión real,
  por decisión del autor.
- Mismo sombreado rojo/azul de "estímulo a la vista" en el panel A, para Appetitive/Aversive/Complex
  — **no** Obstacle (estímulo verde, sin columna `green_present` en los datos, igual que en la
  versión real). Fuente: `metrics_raw.csv.red_present`/`blue_present` (equivalente simulación de
  `neural_metrics.csv` en la versión física) — sin necesidad de resamplear/interpolar, a diferencia
  de la versión real, porque en simulación ambas series viven en el mismo archivo con el mismo
  grid temporal.
- Panel B lee `unified_metrics.csv.pitch_rms`/`roll_rms` (equivalente de `combined_metrics.csv`).
- Trial representativo: `noise_level_idx=0` por familia (no `dirs[0]` como en la versión física —
  ver Pregunta 1 original, resuelta a favor de la baseline sin ruido).
- Guard defensivo de alineación de ejes X (mismo fix que N-02 aplicó para Obstacle-real en su
  Ronda 4, por si algún trial nuevo tiene el mismo patrón de NaN inicial).
- Nombre de archivo conservado: `fig2_{Escenario}_micro_{trial_dir}.png` (con el dataset nuevo,
  `trial_dir` resultó ser `test_001_SUCCESS` en las 4 familias — coincidencia de los datos, no
  hardcodeado).

**Ejecutado y verificado visualmente** (`experiments/.venv_plotting/bin/python
experiments/_plotting/builders/micro_dynamics.py --simulation-root
experiments/R3-04-noise-robustness/data --output-dir experiments/R3-04-noise-robustness/output`):
4 figuras en `experiments/R3-04-noise-robustness/output/`. Inspeccionadas con el visor de
imágenes (Appetitive: sombreado azul correcto y continuo; Obstacle: sin sombreado, panel B más
corto por ser un trial de ~3.3 s — coherente con la duración típica de este escenario, no un bug;
Complex: ambos sombreados alternando correctamente, coincide con que este escenario combina
estímulo apetitivo y aversivo). **No promovidas a `assets/` ni referenciadas desde `results.tex`**
— quedan en `output/` para revisión del autor, mismo gate que usaron N-01/N-02 antes de
`scripts/promote_figure.sh`.

---

## 7. Las 5 piezas restantes — construidas esta sesión

Todas en `experiments/R3-04-noise-robustness/output/`, ejecutadas y verificadas visualmente
(imagen completa, no solo el código). Ninguna promovida a `assets/` ni referenciada desde
`results.tex` todavía — mismo gate de revisión de autor que el resto.

| Pieza | Script | Notas de la verificación visual |
|---|---|---|
| `fig1_noise_robustness_grid.png` (reemplazo) | `experiments/_plotting/builders/noise_sweep_grid.py` (nuevo módulo, no toca `macro_robustness.py`) | Grid 4×4 (se añadió una 4ª columna, `Tswitch`, la métrica que el equipo llamaba "Figura R1"); eje X ahora dice "Combined Perturbation Level (index)" con una nota al pie explicando qué escala (IMU drift + LiDAR + iluminación, combinados). Primer intento tuvo un bug de solapamiento de texto en la fila inferior (etiqueta de 2 líneas repetida en cada columna) — corregido a una etiqueta corta + nota única al pie de la figura completa. |
| `fig_R2_terrain_stability_vs_noise.png` (Figura R2) | `experiments/_plotting/builders/terrain_noise_sweep.py` (nuevo) | Roll/Pitch RMS vs. nivel de ruido, terreno rugoso + pendiente. Mismo fix de etiqueta que el grid. Valores consistentes con los rangos ya auditados (roll rugoso 1.65–1.9°, pitch pendiente 2.3–5.7°). |
| `fig_R3_camera_dropout_evidence.png` (Figura R3) | `experiments/R3-04-noise-robustness/scripts/build_camera_dropout_evidence.py` (nuevo, específico de R3-04) | Serie `blue_present` del par `familia_a_apetitivo` trial_index=7. Confirma exactamente lo que documentaba `robustez_transferencia_tecnica.md`: `blue_present_frac ≈ 0.01` en el intento fallido vs. `≈ 0.99` en el reintento exitoso. |
| `table_R1_failure_rate.csv` (Tabla R1) | `experiments/R3-04-noise-robustness/scripts/build_tables.py` | Conteo por familia/verdict, recalculado directo de los nombres de carpeta (con los 3 `.zip` de c1 excluidos explícitamente). Coincide exactamente con la tabla manual del documento del equipo, incluyendo el caso especial de c1 (27 carpetas conservadas vs. 63 en el manifiesto). |
| `table_R2_perturbation_params.csv` (Tabla R2) | ídem | Parámetros por sensor, valores extraídos literalmente de `config.yaml`/`initctes()` (PyYAML no está en el venv de plotting, así que se hardcodeó desde la misma fuente en vez de parsear el YAML — documentado en el script). |

**Estado:** las 4 figuras/2 tablas de la sección 6 del plan original (`R3-04_audit_and_plan.md`)
ahora tienen builder y salida generada. Falta: decidir con el equipo el diseño final de caption/
prosa (fuera de alcance de esta sesión — solo diseño/planificación de imágenes, no redacción), y
la promoción a `assets/` una vez el autor las revise.

---

## 8. Ronda de auditoría con `audit_tool_R304.html` — 2026-09-01

El autor revisó las 7 figuras + 2 tablas con `~/Documents/Paper/audit_tool_R304.html` (herramienta
local, mismo formato que `audit_tool_N01.html`/`audit_tool_N02.html`, no versionada) y exportó
`intake/pending/r304_audit_notes_2026-09-01.md` con veredicto por pieza. Cambios aplicados:

| Pieza | Veredicto | Cambio aplicado |
|---|---|---|
| `fig1_noise_robustness_grid.png` | ⚠ Ajustar | Columna Pitch RMS: escala compartida-pero-ajustada (techo = máximo real entre las 4 filas × 1.1, no el 0–4° fijo anterior) — muestra la variación en las filas "planas" sin perder comparabilidad de magnitud entre escenarios. Nota al pie añadida: cada punto promedia solo 3 trials (no se inventó una causa mecánica para los "picos" en Obstacle — investigado y descartado, ver Pregunta resuelta abajo). Ticks del eje X forzados a enteros. |
| `fig2_*_micro` (×4) | ⚠ Ajustar | Nota superior (`fig.suptitle`) eliminada — exponía identificadores crudos (`test_001_SUCCESS`, `noise_level_idx=0`) que README.md §11.1 ya prohíbe en material orientado al lector. La nota de "reescribir el análisis de Complex" es de redacción — fuera de alcance de esta sesión, queda para quien escriba la prosa. |
| `fig_R2_terrain_stability_vs_noise.png` | ⚠ Ajustar | Ticks enteros (sin decimales). Espaciado título-contenido corregido (el `rect` de `tight_layout` estaba distribuyendo su margen superior como espacio en blanco en vez de ceñirse a los títulos — se resolvió empaquetando primero sin `rect` y fijando los márgenes después con `subplots_adjust`, no con `rect`). Índice mantenido como entero 0–4 (no convertido a %, decisión del autor: no existe un porcentaje único que represente a los 3 sensores con unidades distintas). |
| `fig_R3_camera_dropout_evidence.png` | ❌ Rechazado, rehecho | Un solo panel con ambas series superpuestas (antes 2 paneles apilados) + leyenda. Etiquetas humanas ("Successful retry"/"Failed attempt (timeout)") en vez de nombres de carpeta crudos. Título pegado al contenido. |
| Tabla R1 | ❌ Rechazada, reemplazada | Gráfico de barras horizontales apiladas (`fig_R1_failure_by_family.png`) en vez de tabla — decisión del autor fue reemplazar, no generar ambas. Nombres de escenario legibles (Appetitive/Rugged Terrain/...) en vez de `familia_*` crudo — corregido proactivamente por el mismo criterio de README.md §11.1, sin que el autor lo pidiera explícitamente para esta pieza. El CSV plano se conserva en `output/` como dato crudo de respaldo, no como la pieza a promover. |
| Tabla R2 | ⚠ Ajustar | Columna `Default` eliminada (redundante con "Values"). Fila `NoiseSeed` eliminada (una constante fija es un hecho de una línea de prosa, no un parámetro de perturbación por sensor). |

**Pregunta que se resolvió sin necesitar al autor:** si `results.tex` ya mencionaba
"Mode-Switch Latency"/`Tswitch` para las 4 familias comportamentales antes de esta ronda (el autor
recordaba haberlo visto y preguntó si "desapareció"). Verificado por grep completo: **no** — para
estas 4 familias en simulación, `Tswitch` nunca estuvo en el texto; sí está extensamente para las
versiones físicas (`_Real`) y para terreno rugoso/pendiente en simulación. La 4ª columna del grid
es contenido genuinamente nuevo, no una restauración de algo perdido.

**Pendiente aún (fuera de alcance de imágenes/datos, para la sesión de escritura):** explicar Tabla
R2 en la metodología; reescribir el análisis de `fig2_Complex_micro` relatando el encuentro con los
tres estímulos; explicar en prosa la interpretación de Fig R3; mencionar `NoiseSeed=42` en el
texto.

---

## 9. Ronda 2 de auditoría — cierre (2026-09-01)

Segunda pasada con `audit_tool_R304.html` (título de la herramienta actualizado a "Ronda 2 —
cierre", `STORE_KEY` re-versionado a `v2` para no arrastrar veredictos de la Ronda 1 sobre
contenido ya cambiado), notas exportadas a `r304_audit_notes_2026-09-01.md` (sobrescribió el mismo
nombre de archivo — mismo día, timestamp interno 8:21:28 PM).

**7 de 8 piezas ✅ aprobadas sin más cambios:** grid, las 4 `fig2_*_micro`, Fig R2, Fig R1
(gráfico de barras). Listas para promover a `assets/` cuando el autor lo confirme (`scripts/
promote_figure.sh`, todavía no ejecutado en esta sesión) — Tabla R2 igual.

**1 pieza con ajuste (⚠), ya corregido:** Fig R3 — la leyenda vivía dentro del rango de datos
(y∈[0,1]) y pisaba el relleno azul de "Successful retry". Fix: se reservó una franja de encabezado
vacía por encima de los datos (`ax.set_ylim` extendido a 1.9, sin tocar los ticks 0/1 que sí
importan) y la leyenda se ancla ahí (`loc="upper center"`, sin marco) — espacio en blanco
garantizado sin importar en qué tramo de x caigan los datos, no una reubicación manual que podría
volver a chocar si el par de trials cambia. Regenerado y verificado visualmente: la leyenda ya no
solapa ni el relleno ni la línea de "Failed attempt".

**Cierre de la fase de imágenes/planificación:** con este ajuste, las 8 piezas de R3-04 quedan
aprobadas. Lo que sigue es responsabilidad de la sesión de escritura: promover a `assets/`,
escribir/editar `sections/methodology.tex` y `sections/results.tex`, y resolver los 4 pendientes de
prosa listados arriba (Tabla R2 en metodología, análisis de `Complex`, interpretación de Fig R3,
mención de `NoiseSeed`).
