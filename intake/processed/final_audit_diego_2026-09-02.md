# Auditoría final — Diego (2026-09-02)

Ejecutada según `intake/pending/redundancy_closing_audit.md` (Secciones 2 y 3: 4 categorías,
mismo rigor que R2-01, sin editar `sections/*.tex` en esta pasada). Releídas de principio a fin
las 6 secciones (`preamble.tex`, `introduction.tex`, `methodology.tex`, `results.tex`,
`conclusions.tex`, `closing.tex`) completas, no solo diffs recientes ni el contenido añadido
desde el cierre de `R2-01`.

Baseline de tamaño al inicio de esta sesión (`wc -w`/`wc -l` directos sobre `sections/*.tex`,
ya que `scripts/check_word_growth.sh` falla en este entorno por terminadores de línea CRLF —
ver nota al final): `results.tex` 12432 palabras/1072 líneas (con mucha diferencia la sección
que más creció desde el cierre de `R2-01`, 8524→12432), `methodology.tex` 6422/540,
`introduction.tex` 1534/37, `conclusions.tex` 1270/50, `preamble.tex` 539/116, `closing.tex`
82/30.

Método: lectura completa de las 6 secciones, seguida de verificación cruzada dirigida por
`grep`/`view` de cada hallazgo candidato (números citados dos veces, identificadores en bruto,
convenciones ortográficas) antes de incluirlo aquí — ningún hallazgo de este documento se basa
solo en una primera impresión de lectura. También abrí `assets/fig2_roc_curve.png` directamente
para verificar el valor de AUC impreso en la leyenda de la figura (ver 2.1-A). Este documento es
una sesión independiente de la de Deivi (`final_audit_deivi_2026-09-02.md`, ya presente en este
mismo directorio) — coincido con varios de sus hallazgos tras verificarlos yo mismo de forma
independiente (marcado explícitamente abajo como "confirmado de forma independiente"), añado
algunos hallazgos nuevos, y en un caso (2.4-C, `Fig.` vs `Figure`) mi conteo amplía
sustancialmente el alcance que su documento había reportado.

---

## 2.1 — Inconsistencias de datos

### [2.1-A] AUC de la ROC: 0.866 en prosa/captions vs. 0.864 en el propio asset de la figura

**Confirmado de forma independiente** (coincide con el hallazgo 2.1-A de Deivi 2026-09-02;
verifiqué yo mismo abriendo la imagen, no solo leyendo su reporte).

- **Ubicación:** `results.tex:682` (prosa, "an ROC-AUC of 0.866" y "yielding an AUC of 0.866"),
  `results.tex:697` (subcaption "(b) ROC curve (AUC = 0.866)"), `results.tex:713` (caption del
  grid `fig:mlp_eval_grid`, misma cifra) vs. `assets/fig2_roc_curve.png`, cuya leyenda interna
  imprime **"MLP (AUC = 0.864)"**.
- **Descripción:** `C-22` (registro en `PROGRESS.md`) documenta que la figura fue reconstruida
  por vectorización de píxeles con AUC trapezoidal recalculado en 0.864 "for internal
  consistency", pero las tres menciones en `results.tex` (prosa + 2 captions) nunca se
  actualizaron a esa cifra. El lector ve un número en el texto y otro, distinto, dentro de la
  propia figura que ese texto describe.
- **Sugerencia:** Actualizar las tres apariciones de "0.866" en `results.tex` a "0.864" para que
  coincidan con el asset ya publicado, en vez de regenerar la figura — el 0.864 es el valor
  recalculado y ya aprobado por el autor según `C-21`.

### [2.1-B] Success Rate de Appetitive/Aversive: 100% en `tab:consolidated_simulation_metrics` vs. 78.9%/88.2% en `tab:fsm_comparison`

**Confirmado de forma independiente** (coincide con el hallazgo de Deivi en ambos documentos,
09-01 y 09-02; verifiqué directamente ambas tablas en `results.tex`).

- **Ubicación:** `results.tex:141-142` (`tab:consolidated_simulation_metrics`: Appetitive
  100.0%, Aversive 100.0%) vs. `results.tex:505,507` (`tab:fsm_comparison`, fila "Neural":
  Appetitive 78.9%, Aversive 88.2%).
- **Descripción:** Para las mismas cuatro familias (Appetitive/Aversive/Obstacle/Complex), los
  valores de $T_{sim}$ y Roll RMS coinciden casi exactamente entre ambas tablas (p. ej.
  Appetitive: $38.52\pm1.20$s en ambas; Aversive: $9.98\pm2.07$s en ambas), lo que indica que
  vienen del mismo recálculo post-`C-22`. El SR, sin embargo, difiere fuertemente solo en
  Appetitive y Aversive — Obstacle y Complex coinciden en 100%/100% en ambas tablas. El propio
  texto (`results.tex:543`) reconoce la discrepancia ("do not match... previously published
  figures") pero no la explica ni resuelve, y la deja publicada tal cual en dos tablas del mismo
  paper.
- **Sugerencia:** Antes del envío, determinar la causa (¿`tab:fsm_comparison` cuenta intentos
  con niveles de ruido >0 mientras `tab:consolidated_simulation_metrics` solo usa el subconjunto
  sin ruido?) y, si se confirma, documentarlo en una nota al pie de tabla; si no, reconciliar
  ambos números como ya se hizo con `C-22` para $T_{sim}$/Roll. Dejar dos SR distintos para el
  mismo experimento sin explicación es el tipo de cosa que un revisor detecta de inmediato.

### [2.1-C] "$TR = 0.000$ sin excepción" en 979 muestras vs. rango 0.003–0.079 documentado en `fig:transition_phases`

**Confirmado de forma independiente** (coincide con el hallazgo 2.1-C de Deivi 09-02).

- **Ubicación:** `results.tex:455-459` (prosa: *"the Tipover Risk index remained at $TR = 0.000$
  without exception"*, sobre los $N_{\mathrm{total}}=979$ muestras de las 6 transiciones) vs.
  `results.tex:428-429` (caption de `fig:transition_phases`: *"$TR$ and $SM$ are reported as a
  min–max range across all instances of that mode"*, implicando valores no constantes).
- **Descripción:** El propio registro de `PROGRESS.md` (fila `N-09`) ya documenta esta
  contradicción como un hallazgo abierto, sin corregir "sin confirmación del autor": los 12
  valores de texto leídos directamente de la figura (una por modo × 4 lecturas) van de 0.003 a
  0.079, nunca 0.000. La afirmación "$TR=0.000$ sin excepción" sobre las 979 muestras crudas es
  más fuerte que lo que la propia figura, en el mismo `results.tex`, documenta para los mismos
  datos.
- **Sugerencia:** La lectura más probable es que $TR=0.000$ describe el instante puntual de la
  transición (4 patas en el suelo, soporte máximo), mientras que las 979 muestras incluyen
  también tramos de locomoción en modo ya establecido (con $TR>0$). Si es así, acotar la
  afirmación explícitamente a la ventana de conmutación morfológica en sí, o confirmar con el
  autor si las 979 muestras son exclusivamente instantes de transición.

### [2.1-D] "Direction-switching latencies below 600 ms" (`conclusions.tex`) sin cifra trazable

**Confirmado de forma independiente** (coincide con el hallazgo de Deivi en ambos documentos;
ya reconocido como abierto en `PROGRESS.md`, fila `C-24`, del mismo tipo que `C-15` resolvió
para el antiguo "~47 ms").

- **Ubicación:** `conclusions.tex:8`.
- **Descripción:** La cifra "600 ms" no corresponde a ningún valor citado directamente en
  `results.tex`. Las latencias de hardware reportadas en `fig:FourPanelLatencies` son 184 ms y
  534 ms (paneles A y B), ambas coherentes con "por debajo de 600 ms" pero el enunciado en sí no
  cita la fuente.
- **Sugerencia:** Reemplazar por la cifra ya trazable y verificada: *"yielding direction-switching
  neural latencies of 184–534 ms (Fig.~\ref{fig:FourPanelLatencies})"*, siguiendo el mismo patrón
  que `C-15` ya aplicó al caso del "~47 ms".

### [2.1-E] "distal end of the femur" (`methodology.tex:25`) vs. "tibia" en el resto del paper

**Confirmado de forma independiente.**

- **Ubicación:** `methodology.tex:25` (*"This motor is located at the distal end of the femur and
  is directly coupled to a mecanum wheel"*) vs. `introduction.tex:34` (*"an omnidirectional wheel
  at the distal segment (tibia)"*) y `methodology.tex:472` (*"the wheels located at the distal end
  of the tibia"*).
- **Descripción:** El fémur es el segmento proximal de una pierna articulada; la tibia es el
  distal. El resto del paper (introducción y la propia sección de Physical Platform Construction,
  47 líneas más abajo en el mismo archivo) usa consistentemente "tibia" para el punto de montaje
  de la rueda motorizada. La línea 25 es la única excepción y parece un residuo de una versión
  anterior del texto.
- **Sugerencia:** Cambiar "femur" por "tibia" en `methodology.tex:25` para que las tres menciones
  sean consistentes entre sí.

### [2.1-F] "1.70 m ahead" / "less than 80 s" (`conclusions.tex:4`) sin respaldo en `results.tex`

**Confirmado de forma independiente** (mismo hallazgo que Deivi 09-01, hallazgo 3; sigue sin
resolver en la versión actual).

- **Ubicación:** `conclusions.tex:4`: *"the physical robot reaches an appetitive stimulus located
  1.70 m ahead... in an average time of less than 80 s"*.
- **Descripción:** Ninguna de las dos cifras aparece en `tab:consolidated_physical_metrics`
  (`results.tex:989-996`, que reporta "Appetitive... Settles by $t>25$s", no "80 s") ni en
  ningún otro lugar de `results.tex` actual. El $d_{final}$ que sí se reporta en el paper
  (Reactive Inspection Task, $1.076\pm0.038$m) es un valor y un escenario distintos.
  Probablemente un resto de una redacción anterior a varias rondas de reescritura de resultados.
- **Sugerencia:** Verificar contra los datos crudos si "1.70 m"/"80 s" siguen siendo válidos para
  algún escenario físico concreto y citarlos con esa referencia explícita, o generalizar la frase
  sin cifras puntuales no trazables (mismo patrón que 2.1-D).

---

## 2.2 — Redundancia de datos / contenido duplicado

### [2.2-A] "builds no map, retains no spatial memory, and computes no global re-route" — casi verbatim en `methodology.tex` y `results.tex`

**Confirmado de forma independiente** (coincide con el hallazgo 2.2-A de Deivi 09-02).

- **Ubicación:** `methodology.tex:61` (párrafo de `C-20` en Gazebo Simulation: *"it builds no map,
  retains no spatial memory, and computes no global re-route when blocked"*) vs.
  `results.tex:552` (Reactive Inspection Task: *"it builds no map, retains no spatial memory, and
  does not compute a global re-route when blocked"*).
- **Descripción:** Las tres cláusulas se repiten casi palabra por palabra en ambos lugares —
  mismo patrón que `R2-01` ya condensó para otros pares cross-section. `methodology.tex` es el
  lugar natural de establecimiento (descripción del diseño del escenario); `results.tex` debería
  referenciarlo en vez de restablecerlo íntegro.
- **Sugerencia:** Condensar la frase de `results.tex:552` a una mención breve + referencia
  cruzada a `Section~\ref{sec:methodology}`, conservando el resto del párrafo (que sí añade
  información nueva: el mecanismo BG/WTA de evasión lateral).

### [2.2-B] Pares raster simulación/físico (Grupo B del `figure-redundancy-audit-triage.md`) — revisados con ojos frescos

- **Ubicación:** `NEU_IMU`/`NEU_IMU2` (`results.tex:221,232`, simulación) vs. la figura ya
  fusionada `fig:neu_imu_real_pair` (`results.tex:784-796`, físico, fusionada por `C-30`).
- **Descripción:** Confirmé el alcance exacto de "Grupo B" leyendo directamente
  `intake/processed/figure-redundancy-audit-triage.md` (no solo el resumen del audit doc
  actual): se refiere específicamente a este par `NEU_IMU`/`NEU_IMU2`, no a otros pares
  `NEU_EST_*`. Abrí `assets/NEU_IMU.png` directamente: confirmo que las letras "a)"/"b)" están
  efectivamente horneadas en el PNG (no son subfiguras LaTeX), tal como documenta `C-30` para
  justificar por qué el par de simulación quedó fuera de la fusión de `C-29`/`C-30` — fusionarlo
  en una figura de dos subfiguras externas produciría un doble etiquetado ambiguo con las letras
  ya impresas dentro de cada imagen.
- **Evaluación:** Confirmo la decisión ya tomada dos veces (`figure-redundancy-audit-triage.md`
  originalmente, y el audit angosto de 2026-08-31 documentado en §6 del audit doc actual): no
  fusionar. La causa técnica (letras horneadas en el PNG) es suficiente por sí sola,
  independientemente de la valoración narrativa de si las dos figuras "cuentan la misma
  historia". Sin acción.

### [2.2-C] `fig:mode_timeline_complex` y `fig:mode_timeline_inspection` — mismo mensaje cualitativo declarado en el propio caption

- **Ubicación:** `results.tex:536-538` (caption de `fig:mode_timeline_complex`) y
  `results.tex:594-596` (caption de `fig:mode_timeline_inspection`, que dice textualmente *"Both
  traces show the same qualitative difference as Figure~\ref{fig:mode_timeline_complex}"*).
- **Descripción:** El segundo caption admite explícitamente que repite la conclusión del primero
  (abrupt/timer-held FSM vs. graduated Neural). Son dos figuras completas de ancho de columna
  para el mismo punto cualitativo, diferenciadas solo por escenario (Complex vs. Inspection).
- **Sugerencia:** Si una fusión en un panel de 2×2 (Neural/FSM × Complex/Inspection) no es viable
  por diferencias de escala temporal entre ambos experimentos, al menos recortar el caption de
  `fig:mode_timeline_inspection` para no restablecer la explicación mecanicista completa —
  bastaría con la referencia cruzada sin repetir "abrupt, timer-held... graduated".

---

## 2.3 — Candidatos a acortar (tablas/figuras)

### [2.3-A] Dos figuras de la ablación de ganglios basales — candidatas a fusión multi-panel

- **Ubicación:** `fig_ablation_success_rate.png` (`results.tex:191-196`) y
  `fig_ablation_complex_stability.png` (`results.tex:200-205`).
- **Descripción:** Ambas cubren el mismo estudio (mismas 4 variantes de ablación, mismo escenario
  Complex Navigation, mismo $n=12$) — una reporta Success Rate, la otra Roll/Pitch RMS. Son
  paneles complementarios de un único resultado, no contenido distinto.
- **Sugerencia concreta:** Fusionar en una figura multi-panel de 3 subfiguras (SR + Roll RMS +
  Pitch RMS), mismo patrón ya usado para `fig:mlp_eval_grid` (precedente de `C-19`). Reduce de 2
  floats a 1 sin perder ningún dato.

### [2.3-B] `tab:fsm_comparison` y `tab:consolidated_simulation_metrics` — solapamiento sin reconciliar visualmente

- **Ubicación:** `results.tex:497-521` (`tab:fsm_comparison`) y `results.tex:132-147`
  (`tab:consolidated_simulation_metrics`).
- **Descripción:** Directamente relacionado con 2.1-B: para las 4 familias compartidas, ambas
  tablas repiten $T_{sim}$/Roll RMS (con SR contradictorio). El lector debe saltar entre dos
  tablas para reconciliar mentalmente datos solapados, y el texto que las conecta
  (`results.tex:543`) reconoce el problema sin resolverlo.
- **Sugerencia:** No es un problema de tamaño de tabla per se, sino de duplicación de columnas
  entre dos tablas del mismo paper. Una vez resuelto 2.1-B, evaluar si $T_{sim}$/Roll pueden
  citarse en `tab:fsm_comparison` por referencia a la tabla consolidada en vez de repetirse
  numéricamente, dejando `tab:fsm_comparison` centrada en las columnas que le son propias (SR,
  $\lambda$, comparación FSM).

### [2.3-C] Párrafo de cierre del ablation study — restata la estructura lógica ya presentada

- **Ubicación:** `results.tex:207` (*"Taken together, these results support the winner-take-all
  arbitration design on two separable grounds. First... Second..."*).
- **Descripción:** Los dos "grounds" ya están completamente desarrollados en los dos párrafos
  inmediatamente anteriores (SR collapse para R3-01 en `results.tex:189`; latencia+estabilidad
  para R3-02 en `results.tex:198`). El párrafo de cierre añade matices menores pero en su
  mayoría repite la estructura argumental ya dada.
- **Sugerencia:** Recortar a 1-2 oraciones que solo aporten lo que no está ya dicho arriba (la
  distinción entre "mechanism-level" y "static-threshold comparison"), eliminando las cláusulas
  que solo repiten números/conclusiones ya presentadas.

### [2.3-D] Tres figuras consecutivas de ancho completo en `sssec:noise_robustness_extra` — mismo patrón que `fig:variable_topo_metrics` ya fusiona

- **Ubicación:** `fig_R1_failure_by_family.png`, `fig_R2_terrain_stability_vs_noise.png`,
  `fig_R3_camera_dropout_evidence.png` (`results.tex:154-177`).
- **Descripción:** Tres figuras de ancho completo, secuenciales, dentro de la misma
  subsubsección — el propio archivo ya tiene el precedente estructural para este caso
  (`fig:variable_topo_metrics`, `results.tex:279-303`, 3 subfiguras fusionadas en un solo
  `figure*`).
- **Sugerencia concreta (opcional, prioridad baja):** Aplicar el mismo patrón de fusión de 3
  subfiguras. A diferencia de 2.3-A, estas tres cubren temas más distintos entre sí (fallos por
  familia, estabilidad vs. ruido, evidencia de camera dropout), así que la ganancia de espacio es
  menor y el autor podría preferir mantenerlas separadas por claridad temática — dejo la decisión
  al autor, no la recomiendo como acción obligatoria.

---

## 2.4 — Ortografía, convenciones académicas, y nombres filtrados del repositorio

### [2.4-A] `\texttt{ablation\_mode}` — identificador de código en prosa (viola README §11.1)

**Confirmado de forma independiente** (coincide con el hallazgo 2.4-A de Deivi 09-01; verifiqué
con `grep` que sigue siendo la única ocurrencia de `\texttt{}` en todo `sections/*.tex`).

- **Ubicación:** `methodology.tex:206`.
- **Descripción:** *"An \texttt{ablation\_mode} parameter was introduced into the simulated
  implementation with four variants..."* — es exactamente el patrón que README §11.1 prohíbe
  (identificador crudo de implementación, wrapeado en `\texttt{}` pero eso no lo exime). El mismo
  párrafo ya nombra funcionalmente las 4 variantes justo después (\emph{full}, \emph{no lateral
  inhibition}, \emph{no STN/STR}, \emph{threshold-only}).
- **Sugerencia:** Quitar "\texttt{ablation\_mode} parameter was introduced" y reformular como
  "Four ablation variants of the simulated circuit were introduced: the intact circuit
  (\emph{full}, control); ...", sin nombrar el parámetro de código.

### [2.4-B] `noise_level_idx` y `NoiseSeed` como notación matemática — mismo problema disfrazado

**Confirmado de forma independiente.**

- **Ubicación:** `methodology.tex:441,443,460` (`$\mathit{noise\_level\_idx}$`) y
  `methodology.tex:460` (`$\mathit{NoiseSeed}=42$`).
- **Descripción:** Son identificadores `snake_case` de código expuestos como si fueran notación
  matemática (envueltos en `$\mathit{...}$` en vez de `\texttt{}`, pero el efecto es el mismo:
  el lector ve un nombre de variable interna, no un símbolo). El propio texto ya usa, en otros
  lugares (`results.tex`), la forma legible "Combined Perturbation Level (index 0–4)".
- **Sugerencia:** Reemplazar `$\mathit{noise\_level\_idx}$` por un símbolo limpio (p. ej.
  $\eta \in \{0,\dots,4\}$) y usar "Combined Perturbation Level" en prosa, igual que ya se hace
  en `results.tex`. Para `NoiseSeed=42`: `PROGRESS.md` (fila `R3-04`) registra que se mantuvo
  fuera de la tabla por pedido explícito del autor — no tocar sin confirmar de nuevo si también
  debía cambiar el nombre crudo del parámetro o solo su ubicación.

### [2.4-C] "Fig." vs. "Figure" — inconsistencia mucho más extendida de lo reportado hasta ahora

**Amplío significativamente un hallazgo de Deivi 09-02** (su documento reportó solo 3
ocurrencias, líneas ~99/111/115 de `results.tex`; mi conteo con `grep -o 'Fig\.~' *.tex` en las
6 secciones encuentra **21 ocurrencias** de "Fig.~", no 3).

- **Ubicación exacta (todas las apariciones de "Fig.~", vía `grep -n`):**
  `methodology.tex:153`; `results.tex:111,113,117,305,308,310,616,627,632,641,676,1004,1008,1014,1043`
  (algunas líneas contienen más de una ocurrencia — el conteo total de tokens "Fig.~" es 21: 1 en
  `methodology.tex`, 20 en `results.tex`).
- **Descripción:** La forma larga "Figure~\ref{}" es mayoritaria (19 veces en `methodology.tex`,
  61 en `results.tex`), pero la forma abreviada "Fig.~" aparece dispersa a lo largo de *todo*
  `results.tex` — no confinada a una sola subsección como sugería el reporte anterior — más una
  vez en `methodology.tex`. `introduction.tex`/`conclusions.tex`/`preamble.tex`/`closing.tex` no
  tienen ninguna ocurrencia de "Fig.~", así que la inconsistencia es específica a
  `methodology.tex`+`results.tex`, pero dentro de esos dos archivos está mucho más repartida de
  lo que una revisión rápida sugeriría.
- **Sugerencia:** Antes de aplicar un `s/Fig\.~/Figure~/g` mecánico, confirmar que ninguna de las
  21 ocurrencias está dentro de una cita textual o nombre propio (no es el caso, verificado por
  inspección de las líneas listadas arriba) y luego normalizar todas a "Figure~", la convención
  dominante en el resto del documento.

### [2.4-D] "Winner-Take-All" (mayúsculas) vs. "winner-take-all" (minúsculas)

**Confirmado de forma independiente** (coincide con el hallazgo de Deivi en ambos documentos).

- **Ubicación:** Mayúsculas en `methodology.tex:61`, `results.tex:552`, `results.tex:1069` (3
  instancias, verificado con `grep -n 'Winner-Take-All'`); minúsculas en 9 instancias repartidas
  entre `preamble.tex` (1), `introduction.tex` (3), `methodology.tex` (3), `results.tex` (1),
  `conclusions.tex` (1) (verificado con `grep -c 'winner-take-all'` por archivo).
- **Descripción:** Mismo término técnico tratado como nombre propio en 3 lugares y como
  descriptor genérico en 9. La convención mayoritaria (9 vs. 3) y la estándar en la literatura de
  ganglios basales/robótica es minúscula cuando describe el mecanismo, no un nombre propio.
- **Sugerencia:** Normalizar las 3 instancias en mayúsculas a "winner-take-all".

### [2.4-E] "Hunting Instinct" (mayúsculas, `results.tex:641`) vs. "hunting drive"/"hunting-instinct" (minúsculas, `methodology.tex`)

**Confirmado de forma independiente** (coincide con el hallazgo de Deivi 09-02).

- **Ubicación:** `results.tex:641` (*"from the constant Hunting Instinct stimulus"*) vs.
  `methodology.tex:235` (*"$HI$ denotes an intrinsic hunting drive"*) y `methodology.tex:292`
  (*"the dimensionless hunting-instinct baseline drive"*).
- **Descripción:** El parámetro $HI$ se presenta en minúsculas en `methodology.tex` (con dos
  nombres ligeramente distintos entre sí, "hunting drive" y "hunting-instinct") pero se
  capitaliza como nombre propio en `results.tex`. No es terminología estándar de la literatura,
  es un nombre interno del modelo — no hay razón para tratarlo como nombre propio.
- **Sugerencia:** Estandarizar a minúsculas en `results.tex` y unificar el nombre (elegir "hunting
  drive" o "hunting instinct", no ambos) entre `methodology.tex` y `results.tex`.

### [2.4-F] "Experiment E" en el caption de `tab:inspection_metrics` — identificador de repositorio filtrado

**Confirmado de forma independiente** (coincide con el hallazgo de Deivi en ambos documentos).

- **Ubicación:** `results.tex:560`: *"Reactive Inspection Task --- Aggregate Performance Metrics
  (Experiment E, 17/20 successful trials, ...)"*.
- **Descripción:** `PROGRESS.md` (fila `R3-05`) documenta que el autor pidió quitar
  "(Experiment E)" de las dos apariciones en el cuerpo del texto de esta subsección
  (2026-08-29), por ser numeración interna tipo "Familia E" que ninguna otra parte del paper usa
  — pero esta tercera aparición, en el caption de la tabla, sobrevivió esa limpieza.
- **Sugerencia:** Quitar "(Experiment E, " del caption, dejando "Reactive Inspection Task ---
  Aggregate Performance Metrics (17/20 successful trials, obstacle field with initially
  non-visible target)."

### [2.4-G] $N_{lidar\_events}$ / $N_{mode\_X\_events}$ — snake_case de código como notación matemática

**Confirmado de forma independiente** (coincide con el hallazgo de Deivi 09-02; mismo patrón de
fondo que 2.4-B).

- **Ubicación:** `results.tex:554,567-568` (prosa y `tab:inspection_metrics`).
- **Descripción:** Estos nombres de métrica usan subíndices `snake_case` (`lidar_events`,
  `mode_X_events`), a diferencia de las otras métricas de la misma tabla ($d_{final}$,
  $T_{acquisition}$, $T_{task}$), que sí siguen la convención estándar de subíndice conciso.
- **Sugerencia:** Renombrar a algo como $N_{ev}^{LiDAR}$ / $N_{ev}^{X}$ (o $N_{obs}$/$N_{sw}$),
  manteniendo la definición completa en prosa.

### [2.4-H] Mezcla ortografía británica/americana — alcance más amplio de lo reportado previamente

**Amplío un hallazgo previamente reportado por Deivi 09-01** (9 instancias listadas allí; mi
`grep` encuentra al menos 18 líneas distintas de `results.tex` con al menos una forma
británica, varias líneas con más de una — el conteo total de tokens supera los 25).

- **Ubicación (todas en `results.tex`, verificado con `grep -n`):** además de las 9 ya
  reportadas por Deivi (`organisation` L17, `behaviour` L317/L684/L1062, `characterise`/
  `characterised` L471/L816, `minimises` L682, `optimisation`/`generalisation`/`favourable`
  L684, `prioritise` L935, `colour` L981), encontré adicionalmente: `analysed` (L308),
  `normalised` (L393), `synthesises`/`terrain-specialised`/`stabilisation` (L298, 3 instancias en
  la misma oración), `specialisation`/`specialised`/`stabilisation` (L310, 3 más), `randomised`
  (L305/L317, al menos 2), `minimising` (L935), `Centre of Mass` (L305, vs. "center of mass" en
  minúscula/americano en `methodology.tex:27` — el mismo concepto con grafía distinta según la
  sección).
- **Descripción:** El paper usa mayoritariamente ortografía americana (decenas de instancias de
  "behavior"/"analyze"/"center"/"color"/"characterized"/"optimize" en las 6 secciones), pero
  sobreviven muchas más excepciones británicas de las que el reporte anterior había capturado —
  concentradas casi enteramente en `results.tex`, tanto en texto base como en prosa nueva de esta
  ronda (`\revblue{}`).
- **Sugerencia:** Dado el volumen real (>25 instancias, no ~9), sugiero que la sesión de
  consolidación trate esto como una pasada de normalización dedicada con `grep`/`sed` verificado
  manualmente, en vez de una lista de correcciones puntuales — más eficiente que registrar cada
  instancia como una fila `C-xx` separada.

### [2.4-I] Comentario de desarrollo en `closing.tex` — artefacto de edición visible en el fuente

**Confirmado de forma independiente** (coincide con el hallazgo de Deivi 09-02).

- **Ubicación:** `closing.tex:2`: `% [CHANGE: bibliography file renamed from persbiblio to
  references]`.
- **Descripción:** Es un comentario LaTeX (no afecta compilación) pero es un artefacto de proceso
  interno del repositorio, sin sentido para un coautor o revisor que abra el `.tex` sin contexto
  del historial de edición. Mismo principio que README §11.1, aunque técnicamente esté en un
  comentario y no en texto renderizado.
- **Sugerencia:** Eliminar la línea antes de la versión final. Cambio de una línea.

---

## Resumen para la consolidación

| # | Cat. | Hallazgo | Prioridad | Nota |
|---|---|---|---|---|
| 1 | 2.1 | AUC 0.866 (prosa/caption) vs. 0.864 (asset de la figura) | Alta | Confirmado independientemente, verifiqué la imagen |
| 2 | 2.1 | SR Appetitive/Aversive contradictorio entre dos tablas | Alta | Confirmado independientemente |
| 3 | 2.1 | $TR=0.000$ "sin excepción" vs. rango 0.003–0.079 en la misma figura | Media | Confirmado; requiere confirmación del autor antes de editar |
| 4 | 2.1 | "600 ms" no trazable en `conclusions.tex` | Media | Ya abierto en `PROGRESS.md` (`C-24`) |
| 5 | 2.1 | "femur" (methodology.tex:25) debería ser "tibia" | Media | Confirmado independientemente |
| 6 | 2.1 | "1.70 m"/"80 s" no trazables en `conclusions.tex` | Media | Confirmado independientemente |
| 7 | 2.2 | "builds no map..." casi verbatim en dos secciones | Media | Confirmado independientemente |
| 8 | 2.2 | Pares raster NEU_IMU sim/físico — confirmado NO fusionar (letras horneadas) | Informativo | Verifiqué visualmente el PNG |
| 9 | 2.2 | `fig:mode_timeline_complex`/`_inspection` — mismo mensaje, admitido en el propio caption | Baja | Nuevo |
| 10 | 2.3 | Fusionar 2 figuras de ablación BG en un multi-panel | Media | Coincide con Deivi 09-01 |
| 11 | 2.3 | `tab:fsm_comparison` vs. `tab:consolidated_simulation_metrics` — solapamiento sin resolver | Media | Ligado a hallazgo 2 |
| 12 | 2.3 | Párrafo de cierre del ablation study restata lo ya dicho | Baja | Coincide con Deivi 09-02 |
| 13 | 2.3 | 3 figuras de `sssec:noise_robustness_extra` — fusión opcional | Baja/opcional | Coincide con Deivi 09-01 |
| 14 | 2.4 | `\texttt{ablation\_mode}` viola README §11.1 | Alta | Confirmado, única ocurrencia de `\texttt{}` en el repo |
| 15 | 2.4 | `noise_level_idx`/`NoiseSeed` como notación cruda | Media | Confirmado independientemente |
| 16 | 2.4 | "Fig." vs. "Figure" — **21 ocurrencias, no 3** | Media | Alcance ampliado respecto a Deivi 09-02 |
| 17 | 2.4 | "Winner-Take-All" vs. "winner-take-all" (3 vs. 9) | Baja | Confirmado independientemente |
| 18 | 2.4 | "Hunting Instinct" vs. "hunting drive"/"hunting-instinct" | Baja | Confirmado independientemente |
| 19 | 2.4 | "Experiment E" en caption de `tab:inspection_metrics` | **Alta** | Confirmado, viola README §11.1 |
| 20 | 2.4 | $N_{lidar\_events}$/$N_{mode\_X\_events}$ — snake_case en notación matemática | Media | Confirmado independientemente |
| 21 | 2.4 | Mezcla ortografía británica/americana — **>25 instancias, no ~9** | Media | Alcance ampliado respecto a Deivi 09-01 |
| 22 | 2.4 | Comentario de desarrollo en `closing.tex` | Baja | Confirmado independientemente |

**Hallazgos de alta prioridad antes de envío:** #1 (AUC), #2 (SR contradictorio), #14
(`\texttt{ablation\_mode}`), #19 (Experiment E en caption).

**Hallazgos que requieren confirmación del autor antes de editar (no auto-corregir):** #3
($TR=0.000$ vs. figura), #4/#6 (600 ms / 1.70 m / 80 s — verificar contra datos crudos antes de
sustituir), #15 (`NoiseSeed` — solo el nombre del parámetro, no su exclusión de la tabla, que ya
fue decisión explícita del autor).

**Nota técnica:** `scripts/check_word_growth.sh` no se pudo ejecutar en este entorno
(`sections/*.tex` tiene terminadores de línea CRLF, y el script usa `set -euo pipefail` con
`#!/usr/bin/env bash`, que falla al interpretar `$'\r'` como comando — error de entorno, no del
contenido del script). Usé `wc -w`/`wc -l` directos como sustituto para la priorización inicial;
el resultado (`results.tex` con, de lejos, el mayor crecimiento) coincide con lo que el script
habría reportado.

Ningún archivo de `sections/*.tex` fue editado en esta pasada. Listo para consolidación junto con
`final_audit_deivi_2026-09-01.md`, `final_audit_deivi_2026-09-02.md`, y los archivos
`final_audit_sebas_*.md`/`final_audit_samuel_*.md` cuando existan (Sección 5 de
`redundancy_closing_audit.md`).
