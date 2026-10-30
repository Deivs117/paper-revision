# Auditoría final — Deivi (2026-09-01)

Ejecutada según `intake/pending/redundancy_closing_audit.md` (Secciones 2 y 3: 4 categorías, mismo
rigor que R2-01, sin editar `sections/*.tex` en esta pasada). Releídas de principio a fin las 6
secciones (`preamble.tex`, `introduction.tex`, `methodology.tex`, `results.tex`, `conclusions.tex`,
`closing.tex`), no solo diffs recientes. `scripts/check_word_growth.sh` corrido primero como guía de
priorización (confirma que `results.tex` es, con mucha diferencia, la sección que más creció desde
`R2-01`: 8645→13370 palabras; `methodology.tex` 5660→6407; `introduction.tex` 1193→1534; `conclusions.tex`
casi sin cambio, 1327→1337).

Cada hallazgo incluye ubicación exacta, categoría, descripción concreta y una sugerencia de
corrección — sin aplicarla. No se tocó ningún archivo en `sections/`.

---

## 2.1 — Inconsistencias de datos

### Hallazgo 1 (prioridad alta): SR contradictorio entre `tab:fsm_comparison` y `tab:consolidated_simulation_metrics` para Appetitive y Aversive

- **Ubicación:** `results.tex:143-150` (`tab:consolidated_simulation_metrics`) vs.
  `results.tex:493-501` (`tab:fsm_comparison`, filas "Appetitive"/"Aversive").
- **Descripción:** Ambas tablas reportan, para Appetitive y Aversive, exactamente el mismo
  $T_{sim}$ y Roll RMS (Appetitive: $38.52\pm1.20$~s / $0.54\text{–}0.536\pm0.01$°; Aversive:
  $9.98\pm2.07$~s / $1.36\text{–}1.357\pm0.11$°), lo que indica que provienen del mismo subconjunto
  de datos recalculado (post-`C-22`). Sin embargo, el **Success Rate difiere**: Appetitive
  100.0% (`tab:consolidated_simulation_metrics`) vs. 78.9% (`tab:fsm_comparison`, fila "Neural");
  Aversive 100.0% vs. 88.2%. Para Obstacle y Complex, en cambio, el SR coincide en ambas tablas
  (100.0%/100.0% en ambos casos), lo que hace más visible la anomalía en las otras dos filas.
  El párrafo aclaratorio existente en `results.tex:532` ("The Neural-side values recomputed here...
  do not match Table~\ref{tab:consolidated_simulation_metrics}'s previously published figures")
  ya no describe el estado actual con precisión: desde `C-22`, $T_{sim}$/Roll **sí coinciden**
  entre ambas tablas — la disonancia que persiste es específicamente el SR, no cubierta por esa
  nota.
- **Sugerencia:** Confirmar con el equipo si el SR de `tab:fsm_comparison` agrega intentos de
  niveles de ruido >0 (mientras que $T_{sim}$/Roll solo usan el subconjunto de ruido cero) — de
  ser así, aclararlo explícitamente en el texto o en la nota al pie de la tabla ("SR computed over
  all noise levels; timing/attitude statistics over the noise-free baseline only"). Si no es así,
  reconciliar los números como se hizo con `C-22` para Roll.

### Hallazgo 2 (prioridad media): "direction-switching latencies below 600 ms" no trazable

- **Ubicación:** `conclusions.tex:8`.
- **Descripción:** Afirma "This behavior yielded direction-switching latencies below 600~ms" sin
  cifra correspondiente en ningún lugar de `results.tex`. Es la misma clase de problema que
  `C-15` ya resolvió para el "~47 ms" en `methodology.tex` (dato no trazable, probablemente
  residual de una ronda anterior). Ya está identificado como abierto en `PROGRESS.md`, fila
  `C-12` ("file a C-xx for an unverified '600ms' claim in conclusions.tex... remain[s] open for a
  future round if wanted") — sigue sin resolver.
- **Sugerencia:** Igual patrón que `C-15`: sustituir por una cifra real y trazable (p. ej. alguno
  de los valores de $T_{switch}$ de `tab:consolidated_physical_metrics`, todos por debajo de
  600 ms salvo Appetitive) o eliminar la cifra específica y dejar la afirmación cualitativa.

### Hallazgo 3 (prioridad media): "1.70 m ahead" / "less than 80 s" en conclusions.tex sin respaldo actual

- **Ubicación:** `conclusions.tex:4`.
- **Descripción:** "the physical robot reaches an appetitive stimulus located 1.70 m ahead...
  in an average time of less than 80~s" — ninguna de estas dos cifras aparece en
  `tab:consolidated_physical_metrics` ni en ningún párrafo de `results.tex` actual (el settling
  time de Appetitive reportado es "$t>25$~s", y $d_{final}$ solo se reporta para el escenario de
  Reactive Inspection Task, con un valor distinto, $1.076\pm0.038$~m). Probable resto de una
  redacción anterior a varias rondas de reescritura de resultados (N-04/N-05/R2-02/etc.).
- **Sugerencia:** Verificar contra los datos crudos si "1.70 m"/"80 s" siguen siendo válidos para
  algún escenario específico y citarlos con esa referencia, o generalizar la frase sin cifras
  puntuales no trazables.

### Hallazgo 4 (prioridad baja, límite con 2.4): resto de "(Experiment E)" en el caption de `tab:inspection_metrics`

- **Ubicación:** `results.tex:548`.
- **Descripción:** El caption de la tabla todavía dice "(Experiment E, 17/20 successful trials...)".
  `PROGRESS.md`, fila `R3-05`, documenta que el autor pidió quitar "(Experiment E)" de **dos**
  apariciones en la subsección (2026-08-29, vía Overleaf) "ninguna otra suite del paper usa
  numeración tipo 'Experiment A/B/C/D'". Esta tercera aparición, en el caption de la tabla, quedó
  fuera de esa limpieza — inconsistente con la decisión ya tomada y registrada.
- **Sugerencia:** Quitar "(Experiment E, " del caption, dejando "Reactive Inspection Task ---
  Aggregate Performance Metrics (17/20 successful trials, obstacle field with initially
  non-visible target)."

---

## 2.2 — Redundancia de datos / contenido duplicado

### Hallazgo único: pares de rasters simulación/físico (Grupo B de `figure-redundancy-audit-triage.md`), revisado con criterio fresco

- **Ubicación:** `NEU_IMU`/`NEU_IMU2` (`results.tex:230,246`) vs. `NEU_IMU_real`/`NEU_IMU2_real`
  (`results.tex:759,782`); mismo patrón en `NEU_EST_UNIG`/`NEU_EST_MUL` (`results.tex:40,101`) vs.
  sus contrapartes `_real` (`results.tex:608,624`).
- **Descripción:** `intake/processed/figure-redundancy-audit-triage.md` (Grupo B) ya señaló que
  estos pares tienen layout casi idéntico y quedó como backlog explícito para "la próxima ronda".
  Esta es esa ronda. Confirmado con lectura fresca: los captions son prácticamente intercambiables
  ("Neural activations during locomotion over irregular/inclined terrain (simulation/physical
  robot). (a) Locomotion decision module; (b) Gait mode control module.") y, tras el trabajo de
  `N-06`/`N-08` (vectorización + letras de panel), ambos lados del par están hoy visualmente más
  pulidos y más parecidos entre sí que cuando se escribió el informe original — exactamente la
  situación que el propio documento de auditoría anticipa.
- **Evaluación:** No recomiendo fusionarlos ni eliminar ninguno. A diferencia de las curvas de
  estabilidad cuasi-idénticas que `R2-01` sí condensó (esas eran gráficos cuantitativos
  redundantes entre sección física y de simulación), estos rasters cumplen una función narrativa
  distinta: son el par sim→físico que valida que el mismo patrón neuronal ocurre en ambos
  dominios — es el mismo rol que cumplen, sin objeción del revisor, `RES_IMU`/`RES_IMU_real`,
  `GRAPH_IMU`/`GRAPH_IMU_real`, `NEU_EST_UNIG`/`NEU_EST_UNIG_real`, etc. Cortar uno de cada par
  rompería esa validación cruzada explícita, que es justamente lo que R2-01 preservó
  deliberadamente en el Grupo A del mismo informe (rechazado por la misma razón).
- **Sugerencia concreta (si se quiere acortar espacio, no contenido):** en vez de eliminar,
  fusionar cada par sim/físico en una única figura de dos paneles lado a lado (mismo patrón usado
  en `fig:mlp_eval_grid`, precedente de `C-19`) — mantiene ambas piezas de evidencia visual pero
  ocupa un solo float en vez de dos. Marcar como candidato opcional, no como corrección
  obligatoria; requiere decisión del autor porque toca 4 pares de figuras ya publicadas.

---

## 2.3 — Candidatos a acortar (tablas/figuras)

### Candidato 1: tabla `tab:action_selection_comparison` (R3-06) vs. línea 9 de `introduction.tex`

- **Ubicación:** `introduction.tex:10` (frase que introduce la tabla) y `introduction.tex:13-28`
  (la tabla misma).
- **Verificación:** Ya resuelto. `C-14` condensó explícitamente la línea 9 para que no reintroduzca
  en prosa lo que la tabla ya muestra; comparando el texto actual, la frase de introducción
  ("Table~\ref{table:action_selection_comparison} summarizes this landscape...") no repite
  columna alguna de la tabla, solo la enmarca. **Sin hallazgo aquí** — ya cerrado por `C-14`/`R3-06`.

### Candidato 2: sección de simulación del "warehouse"

- **Ubicación:** `results.tex:1,4,10`.
- **Verificación:** Sigue corta (4 líneas de introducción a la subsección "Simulation Results"),
  sin crecimiento de prosa nueva desde `R2-01`/`C-07` (que ya reformuló "non-certified test
  arena"). **Sin hallazgo aquí** — ninguna fila nueva le devolvió prosa.

### Candidato 3 (nuevo, prioridad media): las dos figuras de la ablación de ganglios basales podrían fusionarse

- **Ubicación:** `fig_ablation_success_rate.png` (`results.tex:195-200`) y
  `fig_ablation_complex_stability.png` (`results.tex:204-209`).
- **Descripción:** Ambas figuras cubren el mismo estudio (mismas 4 variantes de ablación, mismo
  escenario Complex Navigation, mismo $n=12$), una con SR y otra con Roll/Pitch RMS — son paneles
  complementarios de un mismo resultado, no contenido distinto.
- **Sugerencia concreta:** Fusionar en una única figura multi-panel (SR + Roll RMS + Pitch RMS,
  3 paneles) siguiendo el mismo patrón ya usado para la evaluación del MLP
  (`fig:mlp_eval_grid`, 4 paneles, precedente de `C-19`) — reduce de 2 floats a 1 sin perder
  ningún dato ni capacidad de comunicar el resultado.

### Candidato 4 (nuevo, prioridad baja/opcional): 3 figuras sueltas en `sssec:noise_robustness_extra`

- **Ubicación:** `fig_R1_failure_by_family.png`, `fig_R2_terrain_stability_vs_noise.png`,
  `fig_R3_camera_dropout_evidence.png` (`results.tex:158-181`).
- **Descripción:** Tres figuras de ancho completo, una tras otra, dentro de la misma
  subsubsección — mismo patrón estructural que `FigA_Stability_Profile`/`FigB_Decision_Delay`/
  `FigC_Terrain_Adaptability`, que sí están fusionadas en una sola `figure*` de 3 subfiguras
  (`fig:variable_topo_metrics`, `results.tex:268-292`).
- **Sugerencia concreta:** Aplicar el mismo patrón de fusión de 3 subfiguras que ya existe en el
  propio archivo para `fig:variable_topo_metrics`, dado que las tres figuras ya se leen y discuten
  en secuencia. Opcional — a diferencia del Candidato 3, estas tres cubren temas más distintos
  entre sí (fallos por familia, estabilidad vs. ruido, evidencia de camera dropout), así que la
  ganancia de espacio es menor y el autor podría preferir dejarlas separadas por claridad temática.

---

## 2.4 — Ortografía, convenciones académicas, y nombres filtrados del repositorio

### Hallazgo 1 (prioridad alta): `\texttt{ablation\_mode}` — identificador crudo de código en prosa

- **Ubicación:** `methodology.tex:205`.
- **Descripción:** "An \texttt{ablation\_mode} parameter was introduced into the simulated
  implementation with four variants..." — viola directamente la regla del README §11.1: es
  exactamente el patrón "Bad" documentado allí (`robot_cmd`, ya corregido por `C-17`), solo que
  esta instancia se introdujo después de la auditoría de `C-17` (2026-08-29) — la propia guía de
  README §11.1 pide re-correr este barrido "whenever a new intake doc full of code-level detail
  ... gets turned into manuscript prose", que es exactamente lo que pasó con la redacción del
  estudio de ablación de R3-01/R3-02. Confirmado con `grep -o '\texttt{[^}]*}' sections/*.tex`:
  es la **única** ocurrencia de `\texttt{}` en todo `sections/`, y es justo esta.
- **Sugerencia:** El propio párrafo ya nombra funcionalmente las cuatro variantes justo después
  (\emph{full}, \emph{no lateral inhibition}, \emph{no STN/STR}, \emph{threshold-only}) —
  simplemente quitar "\texttt{ablation\_mode} parameter" y decir algo como "Four ablation
  variants of the simulated circuit were introduced: the intact circuit (\emph{full}, control);
  ...", sin nombrar el parámetro de código.

### Hallazgo 2 (prioridad media): `noise_level_idx` / `NoiseSeed` como notación matemática

- **Ubicación:** `methodology.tex:442,446,459` (`$\mathit{noise\_level\_idx}$`, 3 apariciones) y
  `methodology.tex:459` (`$\mathit{NoiseSeed}=42$`).
- **Descripción:** Mismo problema de fondo que el Hallazgo 1, pero disfrazado de notación
  matemática en vez de `\texttt{}` — sigue siendo un identificador `snake_case` de código
  (probablemente una variable/columna de `experiments/R3-04-noise-robustness/`) expuesto
  directamente al lector. El propio texto ya usa, en otros lugares (leyendas de figuras,
  `results.tex`), la forma legible "Combined Perturbation Level (index 0–4)" — la notación cruda
  en `methodology.tex` es inconsistente con esa forma ya preferida en otras partes del paper.
- **Sugerencia:** Reemplazar `$\mathit{noise\_level\_idx}$` por un símbolo matemático limpio (p. ej.
  $\eta \in \{0,\dots,4\}$) y reservar "Combined Perturbation Level" como su nombre en prosa,
  igual que ya se hace en `results.tex`. Para `NoiseSeed=42`: es una decisión ya tomada por el
  autor ("kept out of the table per author request", según `PROGRESS.md` fila `R3-04`) — flag de
  baja confianza, no recomiendo tocarlo sin confirmar de nuevo con el autor si el nombre crudo
  del parámetro también debía cambiarse o solo mantenerse fuera de la tabla.

### Hallazgo 3 (prioridad media): mezcla de ortografía británica/americana

- **Ubicación (instancias británicas, todas en `results.tex` salvo indicación):**
  `:17` "organisation" (baseline, caption `fig:depot_simulation`), `:306` "behaviour" (baseline,
  intro a `sssec:transition_stability`), `:460` "characterise" (baseline), `:672` "minimises"
  (`\revblue`), `:674` "optimisation"/"generalisation"/"favourable" (`\revblue`, mismo párrafo),
  `:794` "characterised" (baseline), `:913` "prioritise" (`\revblue`), `:959` "colour" (`\revblue`),
  `:1044` "behaviour" (baseline).
- **Descripción:** El paper usa mayoritariamente ortografía americana como convención dominante
  (>40 instancias de "behavior"/"analyze"/"center"/"color"/"characterized"/"optimize"/"modeled"
  repartidas en las 6 secciones), pero sobreviven al menos 9 instancias británicas — no
  confinadas a una sola ronda: aparecen tanto en texto base (líneas sin `\revblue`, de rondas
  anteriores) como en prosa nueva de esta ronda (`\revblue`, principalmente en el párrafo de
  evaluación del MLP y en las secciones físicas de R2-01/R3-04). No es un problema nuevo
  introducido en esta ronda, pero sigue sin normalizar.
- **Sugerencia:** Pasada de normalización a ortografía americana (la convención dominante) en las
  9 instancias listadas: organization, behavior (x2), characterize/characterized (x2), minimizes,
  optimization, generalization, favorable, prioritize, color.

### Hallazgo 4 (prioridad baja): "Winner-Take-All" en mayúsculas vs. "winner-take-all" en minúsculas

- **Ubicación:** Mayúsculas en `methodology.tex:61`, `results.tex:540`, `results.tex:1049` (3
  instancias); minúsculas en `preamble.tex:97`, `introduction.tex:10,24,30`,
  `methodology.tex:159,203,464`, `results.tex:211`, `conclusions.tex:8` (9 instancias).
  ("WTA" como sigla, sin ambigüedad, no está afectado.)
- **Descripción:** Inconsistencia menor de Title Case vs. minúsculas para el mismo término técnico
  usado como sustantivo común a lo largo del paper.
- **Sugerencia:** Normalizar las 3 instancias en mayúsculas a minúsculas ("winner-take-all"), que
  es la convención mayoritaria ya establecida en el resto del documento.

---

## Resumen para la consolidación

| # | Categoría | Hallazgo | Prioridad |
|---|---|---|---|
| 1 | 2.1 | SR contradictorio Appetitive/Aversive entre `tab:fsm_comparison` y `tab:consolidated_simulation_metrics` | Alta |
| 2 | 2.1 | "600 ms" no trazable en `conclusions.tex` (ya abierto en `PROGRESS.md` C-12) | Media |
| 3 | 2.1 | "1.70 m"/"80 s" no trazables en `conclusions.tex` | Media |
| 4 | 2.1 | Resto de "(Experiment E)" en caption de `tab:inspection_metrics` | Baja |
| 5 | 2.2 | Pares raster sim/físico (Grupo B backlog) — revisados, **no fusionar**, opcional side-by-side | Informativo |
| 6 | 2.3 | Fusionar las 2 figuras de ablación BG en un multi-panel (precedente `fig:mlp_eval_grid`) | Media |
| 7 | 2.3 | Fusionar las 3 figuras de `sssec:noise_robustness_extra` (opcional) | Baja |
| 8 | 2.4 | `\texttt{ablation\_mode}` viola README §11.1 | Alta |
| 9 | 2.4 | `noise_level_idx`/`NoiseSeed` como notación cruda | Media |
| 10 | 2.4 | Mezcla ortografía británica/americana (9 instancias) | Media |
| 11 | 2.4 | "Winner-Take-All" vs. "winner-take-all" (3 vs. 9 instancias) | Baja |

Ningún archivo de `sections/*.tex` fue editado en esta pasada, conforme a lo pedido. Listo para
consolidación junto con los archivos `final_audit_diego_*.md`/`final_audit_sebas_*.md`/
`final_audit_samuel_*.md` cuando existan (Sección 5 de `redundancy_closing_audit.md`).
