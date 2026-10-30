# Auditoría final — Sebas (2026-09-02)

Ejecutada según `intake/pending/redundancy_closing_audit.md` (Secciones 2 y 3: 4 categorías, mismo
rigor que R2-01, sin editar `sections/*.tex` en esta pasada). Releídas de principio a fin las 6
secciones (`preamble.tex`, `introduction.tex`, `methodology.tex`, `results.tex`, `conclusions.tex`,
`closing.tex`), no solo diffs recientes. `scripts/check_word_growth.sh` corrido primero como guía de
priorización — confirma `results.tex` como la sección de mayor crecimiento desde `R2-01`
(8645→12451 palabras); también corridos `scripts/check_hardcoded_refs.sh` (limpio) y un grep dirigido
para nombres crudos de implementación (README §11.1).

Cada hallazgo incluye ubicación exacta, categoría, descripción concreta y una sugerencia de
corrección — sin aplicarla. No se tocó ningún archivo en `sections/`.

Nota de consolidación: varios hallazgos de abajo coinciden con los ya reportados en
`intake/pending/final_audit_deivi_2026-09-01.md` (Deivi corrió esta misma auditoría un día antes).
Los marco explícitamente como "confirmado independientemente" donde aplica — la sesión de
consolidación (§5 del documento madre) debería tratarlos como un solo hallazgo, no dos.

---

## 2.1 — Inconsistencias de datos

### Hallazgo 1 (prioridad alta, confirmado independientemente de `final_audit_deivi_2026-09-01.md`): SR contradictorio entre `tab:consolidated_simulation_metrics` y `tab:fsm_comparison`

- **Ubicación:** `results.tex:141-144` (`tab:consolidated_simulation_metrics`) vs. `results.tex:505-511`
  (`tab:fsm_comparison`, filas "Appetitive"/"Aversive"/Neural).
- **Descripción:** Confirmé de forma independiente el mismo patrón que Deivi reportó: $T_{sim}$ y
  Roll ya coinciden entre ambas tablas para las cuatro suites (p. ej. Appetitive: $38.52\pm1.20$~s /
  $0.54$ vs. $0.536\pm0.009$°; Complex: $24.96\pm10.36$~s idéntico en ambas), pero el **Success Rate
  sigue divergiendo** para Appetitive (100.0\% vs. 78.9\%) y Aversive (100.0\% vs. 88.2\%), mientras
  que Obstacle/Complex coinciden en 100.0\%/100.0\% en ambas tablas. Adicionalmente, encontré que la
  nota aclaratoria en `results.tex:543` ("The Neural-side values recomputed here ... do not match
  Table~\ref{tab:consolidated_simulation_metrics}'s previously published figures for the same four
  suites") está **desactualizada** respecto al propio contenido de las tablas que describe: desde
  `C-22`, $T_{sim}$/Roll **sí coinciden** — la única discrepancia real que persiste es el SR, no lo
  que la nota da a entender ("do not match", sin calificar).
- **Sugerencia:** Además de reconciliar el SR (mismo enfoque de `C-22`, o documentar explícitamente
  por qué difiere — p. ej. si `tab:fsm_comparison` agrega intentos con ruido >0), reescribir la nota
  de `results.tex:543` para que diga específicamente qué coincide (tiempo/actitud) y qué no (SR), en
  vez de una afirmación general de no-coincidencia que ya no es precisa.

### Hallazgo 2 (prioridad media, confirmado independientemente): claims sin respaldo trazable en `conclusions.tex` — "1.70 m", "80 s", "600 ms"

- **Ubicación:** `conclusions.tex:4` ("1.70 m ahead", "less than 80~s") y `conclusions.tex:8`
  ("direction-switching latencies below 600~ms").
- **Descripción:** Grep dirigido (`1.70`, `80~s`, `600~ms`) sobre `sections/*.tex` confirma que las
  tres cifras **aparecen únicamente en `conclusions.tex`** — no existen en ningún lugar de
  `results.tex` ni de `methodology.tex`. El valor más cercano a "80 s" en
  `tab:consolidated_physical_metrics`'s columna "Settles by" es Appetitive/Complex $t>25$~s, Aversive
  $t>10$~s, Obstacle $t=8$~s — ninguno coincide, ni individualmente ni como suma obvia. Para "1.70 m",
  la única distancia final reportada actualmente es la del Reactive Inspection Task,
  $d_{final}=1.076\pm0.038$~m (`results.tex:566`) — un escenario distinto, con un valor distinto. Para
  "600 ms", el número trazable más cercano es la latencia de procesamiento neural física ya citada en
  `methodology.tex:204`, $184$–$534$~ms — "600 ms" podría ser un redondeo laxo de ese rango, pero no es
  una cita exacta. Mismo patrón de dato-no-trazable que `C-15` ya corrigió para el "~47 ms"; ya está
  abierto como `C-12` en `PROGRESS.md`.
- **Sugerencia:** Reemplazar las tres cifras por valores reales y trazables — p. ej. el $d_{final}$ del
  Reactive Inspection Task (si es el escenario que se quiere describir) o el rango 184–534 ms para la
  latencia de conmutación, citando explícitamente su procedencia; o, si no hay una fuente exacta,
  suavizar a una afirmación cualitativa sin cifra específica.

### Hallazgo 3 (prioridad baja, nuevo — no en el reporte de Deivi): unidad/valor de $\sigma_Z$ en la tabla LiDAR

- **Ubicación:** `methodology.tex:123` (Tabla~\ref{table:LiDAR}, fila $\sigma_Z = 0.06$) y
  `methodology.tex:133` (texto: "$\sigma_{Z}$ (deg) is the Gaussian tuning width").
- **Descripción:** La activación gaussiana del anillo sensorial (Ec.~\eqref{eq:ring}) usa
  $\exp(-(\theta_j-\theta_{Obstacle})^2 / (2\sigma_Z^2))$. Con $\sigma_Z = 0.06$ **grados**, la curva de
  sintonía de cada una de las 16 neuronas del anillo (espaciadas cada $22.5°$) sería casi un impulso —
  cada unidad respondería solo cuando el obstáculo estuviera casi exactamente en su ángulo preferido,
  lo cual es inconsistente con la descripción funcional del módulo (activaciones superpuestas que
  permiten codificación direccional suave, ver Fig.~\ref{fig:lidar-combined}). No puedo confirmar si
  es un error de unidad (¿radianes?, ¿fracción de $2\pi$?) o un error de valor sin acceso al código
  fuente del generador.
- **Sugerencia:** Verificar contra la implementación real (`PETER_SIMULATION` o el script que generó
  este valor) si $\sigma_Z=0.06$ está en la unidad correcta; si el valor real es, p. ej., $0.06$
  radianes ($\approx3.4°$) o una fracción distinta, corregir la unidad indicada en el texto/tabla para
  que sea consistente con el comportamiento descrito.

---

## 2.2 — Redundancia de datos / contenido duplicado

### Hallazgo 4 (prioridad media, nuevo): descripción del escenario "warehouse" repetida en dos párrafos consecutivos

- **Ubicación:** `results.tex:4` (párrafo de apertura de la Sección Results) y `results.tex:10`
  (párrafo introductorio de la Fig.~\ref{fig:depot_simulation}), separados por solo 6 líneas.
- **Descripción:** Ambos párrafos afirman esencialmente el mismo hecho — que la simulación en Gazebo
  está inspirada en un almacén industrial — con redacción distinta pero contenido solapado: línea 4
  dice *"simulations of the platform were performed in the Gazebo environment within a
  three-dimensional space inspired by an industrial warehouse"*; línea 10 dice *"a Gazebo environment
  inspired by the spatial layout of an industrial warehouse was constructed"*. Es restatement
  inmediato de la misma información, no una repetición cruzada entre secciones distantes (el patrón
  que `R2-01` ya persiguió), sino local y consecutiva — más fácil de perder en una lectura rápida
  porque cada oración individualmente suena razonable.
- **Sugerencia:** Fusionar en una sola mención: el párrafo de apertura (línea 4) puede quedar genérico
  ("simulations... were performed in the Gazebo environment") y dejar que el párrafo de la línea 10 —
  que ya tiene la figura y la referencia a Limitations — sea la única mención específica de
  "industrial warehouse", o viceversa.

### Punto revisado, sin acción necesaria: par de rasters `NEU_IMU`/`NEU_IMU2` (simulación) vs. `_real`

- Releído con ojos frescos según pide §2.2 del documento madre. Confirmo la lectura de `C-29`/`C-30`
  (figure-merge audit): el par de simulación mantiene letras "(a)"/"(b)" horneadas en el PNG (verificado
  contra el generador citado en `PROGRESS.md` C-29/C-30), por lo que fusionarlo introduciría doble
  lettering ambiguo — correctamente dejado sin fusionar. El par físico ya fue fusionado por `C-30`. Sin
  cambios sugeridos.

---

## 2.3 — Candidatos a acortar (tablas/figuras)

### Hallazgo 5 (prioridad media, nuevo): figuras de ablación de ganglios basales fusionables

- **Ubicación:** `results.tex:191-196` (`fig:ablation_success_rate`,
  `fig_ablation_success_rate.png`, ancho $0.6\textwidth$) y `results.tex:200-205`
  (`fig:ablation_complex_stability`, `fig_ablation_complex_stability.png`, ancho completo), ambas en
  la subsubsección "Basal Ganglia Ablation Study", separadas por un solo párrafo de prosa.
- **Descripción:** Ambas figuras documentan el mismo experimento ($n=12$ trials/variant, escenario
  Complex Navigation, mismas 4 variantes de ablación) desde dos ángulos complementarios (tasa de éxito
  vs. estabilidad de actitud). Es exactamente el mismo patrón que ya se fusionó en `C-19` (los 4 floats
  de evaluación MLP → `fig:mlp_eval_grid`, un `figure*` de 2$\times$2) y en `C-26` (fusiones de
  `GRAPH_IMU`/`RES_IMU`).
- **Sugerencia:** Fusionar en una figura de 2 paneles (a: success rate; b: Roll/Pitch RMS), mismo
  patrón que `fig:mlp_eval_grid` — reduce de 2 floats a 1 sin perder ningún dato, y agrupa visualmente
  lo que la prosa ya presenta como un solo análisis.

### Hallazgo 6 (prioridad baja, candidato más débil): figuras R1/R2 de la batería de robustez combinada

- **Ubicación:** `results.tex:154-159` (`fig:failure_by_family`, `fig_R1_failure_by_family.png`) y
  `results.tex:163-168` (`fig:terrain_stability_vs_noise`, `fig_R2_terrain_stability_vs_noise.png`),
  consecutivas en `sssec:noise_robustness_extra`.
- **Descripción:** Ambas figuras documentan la misma batería combinada de perturbación (Rugged
  Terrain + Inclined Slope) desde ángulos distintos (conteo de fallos por causa vs. estabilidad
  postural vs. nivel de ruido). A diferencia del Hallazgo 5, son tipos de gráfico distintos (barras vs.
  líneas) y cada una ya tiene su propio párrafo de análisis extenso — la fusión es posible pero menos
  clara que en el Hallazgo 5.
- **Sugerencia:** Evaluar si fusionar en subfiguras (a)/(b) ahorra espacio suficiente para justificarlo;
  si no, dejar como están. Marco como candidato de menor confianza, a decisión del autor.

---

## 2.4 — Ortografía, convenciones académicas, y nombres filtrados del repositorio

### Hallazgo 7 (prioridad alta): identificador de implementación crudo filtrado a prosa — `\texttt{ablation\_mode}`

- **Ubicación:** `methodology.tex:206` (subsección Basal Ganglia Module, párrafo del ablation study).
- **Descripción:** *"An \texttt{ablation\_mode} parameter was introduced into the simulated
  implementation with four variants..."* — nombra directamente el parámetro de código
  `ablation_mode`, envuelto en `\texttt{}`, exactamente el patrón que README §11.1 prohíbe (mismo tipo
  de caso que `obstaculos.world` y `robot_cmd`, ya corregidos en rondas anteriores). El lector no
  necesita saber el nombre de la variable de código para entender el experimento — las cuatro
  variantes ya están bien descritas funcionalmente inmediatamente después (`\emph{full}`, `\emph{no
  lateral inhibition}`, etc.).
- **Sugerencia:** Reescribir sin el identificador crudo, p. ej.: *"Four ablation variants of the
  simulated basal-ganglia implementation were introduced: the intact circuit (\emph{full},
  control); ..."* — elimina `\texttt{ablation\_mode}` sin perder información para el lector.

### Hallazgo 8 (prioridad baja): typo de puntuación — guion faltante

- **Ubicación:** `results.tex:771`.
- **Descripción:** *"...which commands the robot to climb the ramp using the differential rolling
  mode-this mode remains active..."* — falta espacio/guion largo entre "mode" y "this"; se lee como un
  error de tecleo (posiblemente un em-dash perdido en la edición).
- **Sugerencia:** Corregir a "...differential rolling mode; this mode remains active..." o "...rolling
  mode---this mode remains active...".

### Hallazgo 9 (prioridad baja): inconsistencia anatómica — ubicación de la rueda (fémur vs. tibia)

- **Ubicación:** `introduction.tex:34` ("distal segment (tibia)"), `methodology.tex:25` ("distal end
  of the femur"), `methodology.tex:472` ("distal end of the tibia").
- **Descripción:** Tres menciones de dónde va montada la rueda omnidireccional en cada extremidad: dos
  dicen "tibia" (introducción y la sección de construcción física) y una dice "femur" (Platform
  Design). Dado que dos de tres coinciden en "tibia", "femur" en `methodology.tex:25` es la lectura
  más probable de ser el error, pero no puedo confirmar sin el diseño CAD real.
- **Sugerencia:** Confirmar con el equipo de diseño cuál es el segmento anatómico correcto y unificar
  las tres menciones al mismo término.

### Hallazgo 10 (prioridad baja): terminología de rueda — "mecanum" mencionado una sola vez

- **Ubicación:** `methodology.tex:25` ("directly coupled to a mecanum wheel").
- **Descripción:** El resto del paper usa consistentemente "omnidirectional wheel"/"omnidirectional
  mode" (14+ apariciones); "mecanum" aparece exactamente una vez, en la misma oración que el Hallazgo
  9. No es necesariamente incorrecto (una rueda mecanum es un tipo de rueda omnidireccional), pero
  introduce un término técnico distinto sin aclarar la relación, lo que puede confundir a un lector
  que compare ambos términos.
- **Sugerencia:** O bien usar "omnidirectional wheel" también aquí para consistencia terminológica, o
  aclarar explícitamente la primera vez que se usa "omnidirectional wheel" que se trata de una rueda
  tipo mecanum.

### Hallazgo 11 (prioridad muy baja): ortografía — "bioinspired" sin guion (1 instancia) vs. "bio-inspired" (14 instancias)

- **Ubicación:** `conclusions.tex:4` — mismo párrafo del Hallazgo 2.
- **Descripción:** El paper usa "bio-inspired" (con guion) 14 veces; "bioinspired" (sin guion) aparece
  una sola vez, en `conclusions.tex:4`.
- **Sugerencia:** Cambiar a "bio-inspired" para consistencia.

---

## Resumen para consolidación

- **Confirmados independientemente con `final_audit_deivi_2026-09-01.md`:** Hallazgo 1 (SR
  contradictorio) y Hallazgo 2 (cifras no trazables en conclusions.tex) — mismo hallazgo, ambos
  autores llegaron a él por separado.
- **Nuevos, no reportados por Deivi:** Hallazgo 3 ($\sigma_Z$), Hallazgo 4 (warehouse duplicado),
  Hallazgos 5–6 (figuras fusionables), Hallazgos 7–11 (categoría 2.4 completa).
- Ningún archivo en `sections/` fue modificado en esta pasada.
