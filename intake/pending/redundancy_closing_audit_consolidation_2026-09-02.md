# Consolidación final — redundancy_closing_audit (2026-09-02)

Ejecuta la Sección 5 de `intake/pending/redundancy_closing_audit.md`: cruza los 4 audits finales
(uno por autor, todos completos y en `intake/pending/`) y produce el plan de corrección definitivo.

**Fuentes cruzadas:**
- `final_audit_deivi_2026-09-01.md` (Deivi)
- `final_audit_samuel_2026-09-02.md` (Samuel — renombrado en esta misma sesión; se había commiteado
  como `final_audit_deivi_2026-09-02.md` por error de nombre, ver nota al inicio de ese archivo)
- `final_audit_sebas_2026-09-02.md` (Sebas)
- `final_audit_diego_2026-09-02.md` (Diego)

**No se editó ningún `sections/*.tex` en esta sesión.** Este documento es el plan de acción; la
ejecución (patches + filas `C-xx` en `PROGRESS.md`, wrapped en `\revblue{}` donde corresponda) queda
para la sesión de redacción que lo tome como entrada, siguiendo §5 pasos 2-4 del audit doc madre.

**Criterio de alcance:** por instrucción explícita del autor de esta sesión, se incluye *todo*
hallazgo real de los 4 documentos, sin importar tamaño — incluidos los puramente estéticos (mayúsculas,
guiones, ortografía de una palabra). Los IDs de trabajo abajo (`P-01`...`P-29`) son solo para referencia
interna de este documento; la sesión de ejecución debe pedir el ID real de cada `C-xx` a
`scripts/next_id.sh C` en el momento de escribir cada patch — **no reutilizar los números `P-xx` como
`C-xx`**.

Convención de columna "Fuentes": cuántos de los 4 autores reportaron el mismo hallazgo de forma
independiente (mayor conteo = mayor confianza en que es real, no un falso positivo de un solo lector).

---

## Resumen ejecutivo — orden de ejecución recomendado

| Tier | Qué agrupa | # de items |
|---|---|---|
| **P0 — Crítico** | Inconsistencias de datos visibles al lector + identificadores de repo filtrados (viola §11.1) | 4 |
| **P1 — Alto** | Datos no trazables / requieren decisión editorial clara | 6 |
| **P2 — Medio** | Redundancia de contenido y candidatos a fusión de tablas/figuras | 7 |
| **P3 — Bajo/estético** | Ortografía, capitalización, convenciones — "todo, todo" | 8 |
| **Confirmado sin acción** | Ya revisado por 2+ autores, decisión: no tocar | 4 |

Total: 29 ítems (25 accionables + 4 confirmados-cerrados).

---

## Decisiones tomadas en sesión (2026-09-02, segunda pasada) — todos los ítems que requerían confirmación humana

Se investigó cada ítem marcado "requiere confirmación" contra el código fuente real
(`PETER_SIMULATION`, `experiments/`) antes de preguntar — varias causas quedaron confirmadas con
evidencia dura, no solo hipótesis. Decisiones tomadas con el autor (Deivi):

- **[P-02] SR contradictorio — causa raíz confirmada en código, no es un bug:**
  `experiments/R2-02-fsm-baseline/scripts/build_master_table.py:127-140` (`collect()`) cuenta
  `n_attempted` como el número crudo de carpetas `test_NNN_<VERDICT>` (reintentos fallidos cuentan
  como intentos fracasados propios) — documentado explícitamente en el comentario de la línea 134
  como convención deliberada, heredada de `R2-02_fsm_baseline_reference.md`. En cambio,
  `experiments/_plotting/builders/macro_robustness.py:198` (`build_consolidated_table()`) deduplica
  por `trial_index` (si la misión eventualmente tuvo éxito, cuenta como éxito sin penalizar
  reintentos previos). Dos definiciones de "Success Rate" distintas y legítimas, no un error de
  cálculo. **Decisión: estandarizar `tab:fsm_comparison` a la convención de
  `tab:consolidated_simulation_metrics`** (dedupe por trial_index — es la tabla que el lector ve
  primero). Requiere recalcular el SR de `tab:fsm_comparison` para las filas Neural (Appetitive,
  Aversive; Obstacle/Complex ya coinciden) usando `collect()` con dedupe por trial_index en vez del
  conteo crudo de carpetas, y actualizar/retirar la nota de `results.tex:~543` una vez reconciliado.
  **Nota para ejecución:** esto es un recálculo de datos, no solo un ajuste de texto — sigue el flujo
  normal de `experiments/` (script + `Data source` en la fila `C-xx`), no editar el CSV a mano.

- **[P-17] σ_Z LiDAR — confirmado: no es un ángulo en grados.** Verificado en el código de
  producción `PETER_SIMULATION` (`ros2_ws/src/peter_robot/src/red_neuronal.py:174,283`): `sigma =
  0.06` es el ancho de un kernel gaussiano de similitud coseno,
  `exp((dot(theta,omega)-1)/(2*sigma**2))` — un parámetro adimensional, no una diferencia angular en
  grados. La etiqueta "(deg)" en `methodology.tex` es objetivamente incorrecta. **Decisión: describir
  σ_Z como parámetro adimensional del kernel** (quitar "(deg)", explicar brevemente la forma
  coseno-gaussiana en vez de la angular-gaussiana implícita en el texto actual).

- **[P-07] "1.70 m" / "80 s" — sin respaldo en `experiments/`, confirmado por búsqueda directa.**
  Ningún archivo en `experiments/` contiene esas cifras asociadas a un escenario físico. **Decisión:
  generalizar la frase en `conclusions.tex:4` sin cifras puntuales no trazables.**

- **[P-08] TR=0.000/SM=0.050 "sin excepción" en 979 muestras — confirmado sin datos crudos
  archivados.** `intake/processed/N-09_fusion_transition_phases_reversible.md` §4 ya documenta que
  los 979 datos crudos no existen en ningún lugar del repo. **Decisión: acotar la afirmación
  explícitamente a la ventana de conmutación morfológica puntual** (4 patas en suelo, soporte
  máximo), no a las 979 muestras completas — la interpretación ya documentada como más probable en
  N-09.

- **[P-10] `noise_level_idx` → símbolo limpio, `NoiseSeed` intacto.** Confirmado: renombrar solo el
  símbolo matemático ($\eta \in \{0,\dots,4\}$ o similar); no tocar dónde aparece/se excluye
  `NoiseSeed=42` (decisión de autor ya registrada en `R3-04`).

- **[P-24] "mecanum wheel" → "omnidirectional wheel".** Confirmado: usar "omnidirectional wheel"
  también en `methodology.tex:25` para consistencia total con el resto del paper (14+ instancias).

- **[P-13] Fusionar/recortar `fig:mode_timeline_complex` + `fig:mode_timeline_inspection`.**
  Confirmado ejecutar — intentar fusión en panel 2×2 (Neural/FSM × Complex/Inspection); si no es
  viable por diferencias de escala temporal, al menos recortar el caption duplicado de
  `fig:mode_timeline_inspection`.

- **[P-14] Fusionar las 2 figuras de ablación BG en un multi-panel.** Confirmado ejecutar —
  `fig_ablation_success_rate` + `fig_ablation_complex_stability` → 1 figura de 2-3 paneles, mismo
  patrón que `fig:mlp_eval_grid` (`C-19`).

- **Fusión de las 3 figuras de `sssec:noise_robustness_extra` (R1/R2/R3): NO seleccionada.** El
  autor no la eligió entre las opciones de fusión — se deja el ítem [P-16-bis, antes candidato de
  Tier P2] **sin ejecutar en esta ronda**, disponible para retomar en una ronda futura si se desea.

---

## Anexo — `figure_regeneration_candidates.md` (2026-08-31, handoff de figuras no cubierto por los 4 audits)

Documento aparte, no escrito por ninguno de los 4 auditores — lista de candidatos de fusión de
figuras que el autor había dejado como *handoff* para el equipo. Se decide aquí junto con el resto
del plan porque comparte alcance con [P-13]/[P-14]/[P-26]. Decisiones tomadas en sesión
(2026-09-02, tercera pasada):

### Grupo 1 — sin regenerar imágenes (fusión pura en `sections/*.tex`)

- **[FIG-1a] `fig:robot` + `fig:pata`** (`methodology.tex:11-22`) — dos renders CAD consecutivos,
  cada uno citado una sola vez, sin letras internas. **DECIDIDO: FIX-NOW**, fusionar en 2
  subfiguras (mismo patrón que `C-29`).
- **[FIG-1b] `fig:appetitive_micro`+`fig:aversive_micro`+`fig:obstacle_micro`+`fig:complex_micro`**
  (`results.tex:~66-125`) — el propio doc lo marcaba "coin-flip" (precedente
  `fig:noise_robustness_grid` a favor de fusionar; cada figura pegada a su propio párrafo de
  escenario, en contra). **DECIDIDO: NO fusionar** — se mantienen las 4 figuras separadas, cada
  una junto a su párrafo.
- **[FIG-1c] `fig:MLP` + `fig:DATOSMLP`** (`methodology.tex:~360-390`) — requiere mover
  `table:DIR_BINARY` (hoy físicamente entre ambas figuras) antes o después del par. **DECIDIDO:
  FIX-NOW**, fusionar y reordenar la tabla.

### Grupo 2 — requiere regenerar imagen (letras horneadas en el PNG)

- **[FIG-2a] `NEU_IMU` + `NEU_IMU2`** (simulación) — los 4 auditores habían dicho "NO fusionar"
  (ver [P-26]) por las letras horneadas, pero este doc sí tiene el procedimiento completo para
  regenerar sin letras y fusionar. **DECIDIDO: NO fusionar** — el autor confirmó, tras ver las
  imágenes actuales, que la fusión no reduce longitud de texto de forma significativa; no vale el
  riesgo/esfuerzo de regenerar + reescribir prosa. **[P-26] se mantiene cerrado tal cual estaba.**
  **Pero ver [FIG-X17] abajo — se sí regeneran ambos PNGs, por una razón distinta (quitar un panel,
  no fusionar dos figuras).**
- **[FIG-2b] `NEU_EST_UNIB` + `NEU_EST_UNIG`** (simulación, `results.tex:~38-53`) — **DECIDIDO:
  FIX-NOW**, regenerar sin `group_letters`, promover, fusionar en 2 subfiguras, reescribir la única
  cita con letra (línea ~45). Alinea la estructura de simulación con la del lado físico
  (`NEU_EST_UNIG_real`, ya fusionado por `C-18`).
- **[FIG-2c] `NEU_EST_MUL` (simulación) + `NEU_EST_MUL_real` (físico)** — fusión cruzada
  sim×físico, 4 letras horneadas por imagen, 2 subsecciones de `results.tex`, 7 citas con letra a
  reescribir (varias ya ajustadas cuidadosamente por `C-28`). **DECIDIDO: NO ejecutar esta ronda**
  — queda para una ronda futura, siguiendo la propia recomendación del documento origen.
- **Grupo 3 (`Modos_Locomocion`/`V2`):** ya venía "no recomendado" en el documento origen
  (riesgo de ilegibilidad de diagramas de circuito al encogerlos). **Sin acción, no se re-abre.**

### [FIG-X17] Hallazgo nuevo (fuera de los 4 audits y de `figure_regeneration_candidates.md`): panel "Locomotion 2" (neurona X17) de `NEU_IMU`/`NEU_IMU2` — verificado contra datos, actividad tónica constante sin variación temporal útil

- **Origen:** observación directa del autor al revisar las imágenes enviadas para decidir [FIG-2a].
- **Verificación:** confirmado contra `experiments/_plotting/vectorized/neu_imu.csv` y
  `neu_imu2.csv` — el panel "Locomotion_2" contiene únicamente la neurona `X17` en ambos archivos,
  con `activation_normalized` en el rango 0.502–1.0 (media 0.503, solo 3 valores distintos
  observados en 731 muestras). **Corrección a la premisa inicial:** X17 no está inactiva — está
  activa de forma tónica y casi constante todo el trial. Confirmado que no hay ninguna cita a
  `X17`/"Locomotion 2" en `results.tex` (`grep` sin resultados) — quitar el panel no requiere
  reescribir prosa.
- **Decisión:** quitar el panel "Locomotion 2" (X17) de ambas imágenes `NEU_IMU.png` y
  `NEU_IMU2.png`, ya que no aporta variación temporal interpretable para el lector (aunque
  técnicamente hay actividad, no es un error de datos ni algo a "corregir" en el sentido de las
  otras categorías — es una simplificación visual deliberada).
- **Cómo ejecutarlo (para la sesión de redacción):** `experiments/_plotting/builders/
  imu_terrain_real.py::build_neu_imu()` tiene la lista de paneles hardcodeada (`panels =
  ["Locomotion_1", "Locomotion_2", "Decision_1", "Decision_2"]`, línea ~70) — añadir un parámetro
  opcional `panels` (default a la lista actual, para no romper `NEU_IMU_real`/`NEU_IMU2_real`, que
  no deben tocarse) y pasar `["Locomotion_1", "Decision_1", "Decision_2"]` en las 2 llamadas de
  `regenerate_neu_panels.py` para `NEU_IMU`/`NEU_IMU2` únicamente. Regenerar, verificar visualmente,
  `scripts/promote_figure.sh --force` ambos PNGs. La estructura de "Locomotion Module" (grupo con
  letra "a") pasaría a tener un solo panel en vez de dos — revisar que `_place_group_title_above`/
  `_place_group_letter` sigan posicionándose bien con 3 paneles en vez de 4 (probable ajuste menor
  de `figsize`/`h_pad`).

---

## TIER P0 — Crítico (antes de cualquier otra cosa)

### [P-01] AUC 0.866 (prosa + 2 captions) vs. 0.864 (leyenda del propio asset)

- **Fuentes:** Samuel (2.1-A), Diego (2.1-A, verificó la imagen directamente) — 2/4, ambos con
  verificación visual del PNG, no solo lectura del texto.
- **Ubicación:** `results.tex` línea ~682 (prosa, dos menciones: "an ROC-AUC of 0.866" y "yielding
  an AUC of 0.866"), línea ~697 (subcaption "(b) ROC curve (AUC = 0.866)"), línea ~713 (caption del
  grid `fig:mlp_eval_grid`) — todas dicen 0.866, contra `assets/fig2_roc_curve.png` que imprime
  **"MLP (AUC = 0.864)"** en su propia leyenda.
- **Decisión:** FIX-NOW. `C-21`/`C-22` ya reconstruyeron y aprobaron la figura con 0.864 "for
  internal consistency" — el texto simplemente no se actualizó a esa cifra. No hay ambigüedad sobre
  cuál valor es el correcto (el ya publicado en el asset).
- **Corrección exacta:** cambiar las 3 ocurrencias de "0.866" en `results.tex` (líneas ~682, ~697,
  ~713) a "0.864".

### [P-02] Success Rate contradictorio: Appetitive/Aversive 100% vs. 78.9%/88.2% entre dos tablas

- **Fuentes:** Deivi, Samuel, Sebas, Diego — **4/4**, el hallazgo con más confirmación independiente
  de todo el audit.
- **Ubicación:** `results.tex:143-150` (`tab:consolidated_simulation_metrics`: Appetitive 100.0%,
  Aversive 100.0%) vs. `results.tex:493-511` (`tab:fsm_comparison`, fila "Neural": Appetitive 78.9%,
  Aversive 88.2%). $T_{sim}$ y Roll RMS ya coinciden entre ambas tablas (post-`C-22`) — la única
  discrepancia real es el SR. Nota de texto en `results.tex:~543` ("do not match... previously
  published figures") ya no describe el estado actual con precisión: da a entender una discrepancia
  general que ya no existe para $T_{sim}$/Roll, solo para SR.
- **Decisión:** FIX-CON-CONFIRMACIÓN. La causa (¿`tab:fsm_comparison` agrega intentos con ruido >0
  mientras la otra tabla usa solo el subconjunto sin ruido?) debe confirmarse con el equipo antes de
  reconciliar los números — pero el texto de la línea ~543 sí puede corregirse ya (reescribir para
  que diga específicamente qué coincide y qué no, en vez de una negación general desactualizada).
- **Acción concreta:**
  1. Preguntar al equipo/autor cuál conjunto de trials o definición de éxito produjo cada SR.
  2. Si se confirma causa → reconciliar (mismo enfoque de `C-22`) o añadir nota al pie explicando la
     causa específica en una de las dos tablas.
  3. Reescribir `results.tex:~543` para que sea precisa: qué coincide (tiempo/actitud) y qué no (SR),
     no una afirmación general de no-coincidencia.
- **Relacionado:** ver también [P-15] (reconciliación visual de las dos tablas, ángulo de tamaño/
  redundancia del mismo problema).

### [P-03] `\texttt{ablation_mode}` — identificador crudo de código en prosa (viola README §11.1)

- **Fuentes:** Deivi, Samuel, Sebas, Diego — **4/4**, unánime.
- **Ubicación:** `methodology.tex` línea ~205-206, subsección Basal Ganglia Module: *"An
  \texttt{ablation\_mode} parameter was introduced into the simulated implementation with four
  variants..."*. Confirmado (Diego, Deivi) vía `grep -o '\texttt{[^}]*}' sections/*.tex`: es la
  **única** ocurrencia de `\texttt{}` en todo `sections/`.
- **Decisión:** FIX-NOW. Mismo patrón exacto que `robot_cmd` (ya corregido por `C-17`) — el propio
  párrafo ya nombra funcionalmente las cuatro variantes justo después.
- **Corrección exacta:** *"An \texttt{ablation\_mode} parameter was introduced..."* →
  *"Four ablation variants of the simulated basal-ganglia circuit were introduced: the intact
  circuit (\emph{full}, control); ..."* (conservar el resto de la enumeración de variantes tal cual
  ya está redactada).

### [P-04] "Experiment E" en caption de `tab:inspection_metrics` — identificador de repositorio filtrado

- **Fuentes:** Deivi, Samuel, Diego — 3/4 (Sebas no lo reportó).
- **Ubicación:** `results.tex` línea ~548-560: `\caption{...Aggregate Performance Metrics
  (Experiment E, 17/20 successful trials, ...)}`. `PROGRESS.md` fila `R3-05` documenta que el autor
  ya pidió quitar "(Experiment E)" de las **dos** apariciones en el cuerpo de texto de esta
  subsección (2026-08-29) — esta tercera aparición, en el caption de la tabla, sobrevivió esa
  limpieza.
- **Decisión:** FIX-NOW. Es la continuación directa de una decisión de autor ya tomada y aplicada
  parcialmente; no hay ambigüedad.
- **Corrección exacta:** quitar `(Experiment E, ` del caption, dejando: *"Reactive Inspection Task
  --- Aggregate Performance Metrics (17/20 successful trials, obstacle field with initially
  non-visible target)."*

---

## TIER P1 — Alto (datos no trazables / decisión editorial clara)

### [P-05] "distal end of the femur" → debe ser "tibia"

- **Fuentes:** Samuel (2.1-E), Sebas (Hallazgo 9, categorizado en 2.4), Diego (2.1-E) — 3/4.
- **Ubicación:** `methodology.tex` línea ~25 dice "femur"; `preamble.tex` línea ~34 y
  `methodology.tex` línea ~472 dicen "tibia"; `introduction.tex` línea ~34 también dice "tibia".
  2 de 3 (más el abstract) coinciden en "tibia" — el fémur es el segmento proximal, la tibia el
  distal, y la rueda va en el extremo distal.
- **Decisión:** FIX-NOW. Consenso 3/4 + coherencia anatómica interna (fémur=proximal no encaja con
  "distal end").
- **Corrección exacta:** `methodology.tex:~25` — "distal end of the femur" → "distal end of the
  tibia".

### [P-06] "direction-switching latencies below 600 ms" (conclusions.tex) sin cifra trazable

- **Fuentes:** Deivi, Samuel, Sebas, Diego — **4/4**. Ya abierto en `PROGRESS.md` como `C-12`/`C-24`
  (mismo patrón que `C-15` ya resolvió para el antiguo "~47 ms").
- **Ubicación:** `conclusions.tex` línea ~8.
- **Decisión:** FIX-NOW (no requiere confirmación adicional — el rango de reemplazo ya está
  publicado y trazable en `results.tex`).
- **Corrección exacta:** reemplazar por *"yielding direction-switching neural latencies of
  184–534~ms (Fig.~\ref{fig:FourPanelLatencies})"*.

### [P-07] "1.70 m ahead" / "less than 80 s" (conclusions.tex) sin respaldo en results.tex

- **Fuentes:** Deivi, Sebas, Diego — 3/4 (Samuel no lo reportó).
- **Ubicación:** `conclusions.tex` línea ~4. Ninguna cifra aparece en
  `tab:consolidated_physical_metrics` (Appetitive settling reportado como "$t>25$s") ni en ningún
  otro lugar de `results.tex`. El único $d_{final}$ publicado es el de Reactive Inspection Task
  ($1.076\pm0.038$m), escenario distinto.
- **Decisión:** FIX-CON-CONFIRMACIÓN. A diferencia de [P-06], aquí no hay un valor de reemplazo
  obvio ya publicado — necesita verificación contra datos crudos antes de sustituir.
- **Acción concreta:** verificar con el equipo si "1.70 m"/"80 s" siguen siendo válidos para algún
  escenario físico concreto (y citarlos con esa referencia explícita), o generalizar la frase sin
  cifras puntuales no trazables si no se puede confirmar la fuente.

### [P-08] "TR = 0.000 sin excepción" (979 muestras) vs. rango 0.003–0.079 en fig:transition_phases

- **Fuentes:** Samuel, Diego — 2/4. Ya documentado como abierto en `PROGRESS.md` fila `N-09`
  ("No corregido sin confirmación del autor").
- **Ubicación:** `results.tex:~453-459` (prosa) vs. `results.tex:~423-438` (caption de
  `fig:transition_phases`, rangos min–max no nulos).
- **Decisión:** NO AUTO-CORREGIR — requiere confirmación explícita del autor. Interpretación más
  probable (compartida por ambos reportes): TR=0.000 aplica solo al instante puntual de la
  transición (4 patas en suelo), mientras que los 979 samples incluyen también locomoción en modo
  establecido (TR>0).
- **Acción concreta:** confirmar con el autor si los 979 samples son exclusivamente frames de
  transición. Si no, acotar la afirmación a *"during the morphological switching window itself"* y
  señalar que los samples de locomoción estable dentro del run muestran TR>0.

### [P-09] $N_{lidar\_events}$ / $N_{mode\_X\_events}$ — snake_case de código en notación matemática

- **Fuentes:** Samuel (2.4-B, cross-referenciado también en su 2.3-C), Diego (2.4-G) — 2/4.
- **Ubicación:** `results.tex:~554,566-569` (prosa y `tab:inspection_metrics`).
- **Decisión:** FIX-NOW. Las otras métricas de la misma tabla ($d_{final}$, $T_{acquisition}$,
  $T_{task}$) ya usan convención estándar; estos dos nombres son los únicos con subíndices
  snake_case.
- **Corrección sugerida:** $N_{lidar\_events}$ → $N_{ev}^{LiDAR}$ (o $N_{obs}$); $N_{mode\_X\_events}$
  → $N_{ev}^{X}$ (o $N_{sw}$). Mantener la definición completa en prosa para no perder claridad.

### [P-10] `noise_level_idx` / `NoiseSeed` como notación matemática

- **Fuentes:** Deivi (2.4 H2), Diego (2.4-B) — 2/4.
- **Ubicación:** `methodology.tex:~441-460` (`$\mathit{noise\_level\_idx}$`, 3 apariciones) y
  `$\mathit{NoiseSeed}=42$`.
- **Decisión:** FIX-NOW para `noise_level_idx` (mismo patrón que P-09, el propio texto ya usa "Combined
  Perturbation Level (index 0–4)" en otros lugares). **NO TOCAR `NoiseSeed`** sin reconfirmar con el
  autor: `PROGRESS.md` fila `R3-04` documenta que su exclusión de la tabla fue decisión explícita del
  autor — el hallazgo es solo sobre el estilo del nombre, no sobre dónde aparece.
- **Corrección sugerida:** `$\mathit{noise\_level\_idx}$` → $\eta \in \{0,\dots,4\}$, reservando
  "Combined Perturbation Level" como nombre en prosa (consistente con `results.tex`).

---

## TIER P2 — Medio (redundancia de contenido, fusión de tablas/figuras)

### [P-11] "builds no map, retains no spatial memory, and computes no global re-route" casi verbatim

- **Fuentes:** Samuel (2.2-A), Diego (2.2-A, confirmado independientemente) — 2/4.
- **Ubicación:** `methodology.tex:~61` (párrafo `C-20`, Gazebo Simulation) vs. `results.tex:~552`
  (Reactive Inspection Task) — las tres cláusulas se repiten casi palabra por palabra.
- **Decisión:** FIX-NOW. Mismo patrón que `R2-01` ya condensó en otros pares cross-section.
  `methodology.tex` es el lugar de establecimiento; `results.tex` debe cruzar-referenciar.
- **Corrección sugerida:** condensar `results.tex:~552` a: *"As described in
  Section~\ref{sec:methodology}, the system is purely reactive — no map, no spatial memory, no
  deliberate re-routing..."*, preservando el resto del párrafo (mecanismo BG/WTA de evasión lateral,
  que sí aporta información nueva).

### [P-12] Duplicación local del párrafo "industrial warehouse" (results.tex líneas ~4 y ~10)

- **Fuentes:** Sebas (Hallazgo 4) — 1/4, nuevo, no reportado por los otros tres.
- **Ubicación:** `results.tex:4` (apertura de Results) y `results.tex:10` (intro a
  `fig:depot_simulation`), separados por 6 líneas — restatement inmediato y local, no cruzado entre
  secciones distantes (que es el patrón que `R2-01` ya persiguió), por eso más fácil de perder en
  lectura rápida.
- **Decisión:** FIX-NOW. Concreto y de bajo riesgo — solo 2 oraciones a fusionar.
- **Nota:** no confundir con el candidato de "warehouse" ya cerrado sin acción en `final_audit_deivi_
  2026-09-01.md` (ese verificaba otra cosa: si la sección había crecido de más desde `R2-01`/`C-07`;
  éste es un hallazgo distinto y nuevo, restatement local entre dos párrafos consecutivos).
- **Corrección sugerida:** dejar el párrafo de apertura (línea 4) genérico ("simulations... were
  performed in the Gazebo environment") y que el párrafo de la línea 10 (que ya tiene la figura y la
  referencia a Limitations) sea la única mención específica de "industrial warehouse".

### [P-13] `fig:mode_timeline_complex` / `fig:mode_timeline_inspection` — mismo mensaje, admitido en el propio caption

- **Fuentes:** Samuel (2.2-B), Diego (2.2-C) — 2/4.
- **Ubicación:** `results.tex:~534-538` y `~592-596` — el segundo caption dice textualmente *"Both
  traces show the same qualitative difference as Figure~\ref{fig:mode_timeline_complex}"*.
- **Decisión:** FIX-NOW (al menos el recorte de caption; la fusión en panel 2×2 es opcional).
- **Corrección sugerida:** evaluar fusión en un panel de 2 filas (Neural/FSM) × 2 columnas
  (Complex/Inspection). Si no es viable por diferencias de escala temporal, al menos recortar el
  caption de `fig:mode_timeline_inspection` para no restablecer la explicación mecanicista completa
  — basta la referencia cruzada sin repetir "abrupt, timer-held... graduated".

### [P-14] Fusionar las 2 figuras de ablación de ganglios basales en un panel multi-figura

- **Fuentes:** Deivi (Candidato 3), Sebas (Hallazgo 5), Diego (2.3-A) — 3/4.
- **Ubicación:** `fig_ablation_success_rate.png` (`results.tex:~191-196`) y
  `fig_ablation_complex_stability.png` (`results.tex:~200-205`) — mismo estudio ($n=12$, 4 variantes,
  escenario Complex Navigation), un float por métrica (SR vs. Roll/Pitch RMS).
- **Decisión:** FIX-NOW. Mismo patrón exacto que el precedente `fig:mlp_eval_grid` (`C-19`).
- **Corrección sugerida:** fusionar en una figura de 2-3 paneles (SR + Roll RMS [+ Pitch RMS]),
  reduce de 2 floats a 1 sin perder ningún dato.

### [P-15] `tab:fsm_comparison` vs. `tab:consolidated_simulation_metrics` — solapamiento sin reconciliar visualmente

- **Fuentes:** Samuel (2.3-A), Diego (2.3-B) — 2/4; directamente ligado a [P-02] (mismo dato, ángulo
  de tamaño de tabla en vez de inconsistencia numérica).
- **Decisión:** BLOQUEADO POR [P-02]. Una vez resuelta la causa del SR, evaluar si $T_{sim}$/Roll
  pueden citarse en `tab:fsm_comparison` por referencia a la tabla consolidada en vez de repetirse
  numéricamente, o añadir una columna/nota que ponga los dos SR lado a lado con explicación.

### [P-16] Párrafo de cierre del ablation study (results.tex ~207) restata puntos ya establecidos

- **Fuentes:** Samuel (2.3-B), Diego (2.3-C) — 2/4.
- **Ubicación:** `results.tex:~207`: *"Taken together, these results support the winner-take-all
  arbitration design on two separable grounds. First… Second…"* — ambos "grounds" ya están
  desarrollados en los dos párrafos inmediatamente anteriores.
- **Decisión:** FIX-NOW.
- **Corrección sugerida:** reducir a 1-2 oraciones que solo aporten lo que no está ya dicho arriba
  (la distinción entre "mechanism-level" y "static-threshold comparison"); eliminar cláusulas que
  solo repiten números/conclusiones ya presentadas.

### [P-17] $\sigma_Z = 0.06$ (deg) en tabla LiDAR — posible error de unidad

- **Fuentes:** Sebas (Hallazgo 3) — 1/4, nuevo.
- **Ubicación:** `methodology.tex:~123,133` (Tabla LiDAR, $\sigma_Z=0.06$; texto dice "(deg)").
- **Descripción:** con $\sigma_Z=0.06°$ la curva de sintonía de cada neurona del anillo (16
  neuronas, espaciadas 22.5°) sería casi un impulso — inconsistente con la descripción funcional de
  activaciones superpuestas (Fig. lidar-combined). Podría ser radianes o una fracción distinta.
- **Decisión:** NO AUTO-CORREGIR — no verificable solo desde el texto del paper, requiere revisar el
  generador real en `PETER_SIMULATION` o el script que produjo ese valor (lectura, nunca edición,
  per `intake/SOURCES.md`).
- **Acción concreta:** verificar contra la implementación real si $0.06$ está en la unidad correcta
  antes de tocar el texto/tabla.

---

## TIER P3 — Bajo / estético ("todo, todo" — nada se omite)

### [P-18] "Fig." vs. "Figure" — normalizar todas las ocurrencias a "Figure"

- **Fuentes:** Samuel (2.4-C, reportó 3 ocurrencias) — **ampliado por Diego (2.4-C) a 21
  ocurrencias reales** (`grep -o 'Fig\.~'` sobre las 6 secciones): 1 en `methodology.tex:153`, 20 en
  `results.tex` (líneas 111,113,117,305,308,310,616,627,632,641,676,1004,1008,1014,1043, algunas con
  más de una ocurrencia por línea). El conteo de Diego es el autoritativo — verificó con grep directo
  y confirmó que ninguna está dentro de una cita textual o nombre propio.
- **Decisión:** FIX-NOW. Normalizar las 21 ocurrencias de "Fig.~" a "Figure~" en `methodology.tex` y
  `results.tex` (única forma larga usada en el resto del documento — 19+61 instancias ya en esa
  forma).

### [P-19] "Winner-Take-All" (mayúsculas) vs. "winner-take-all" (minúsculas)

- **Fuentes:** Deivi, Samuel, Diego — 3/4 (Sebas no lo reportó). Diego tiene el conteo más preciso:
  mayúsculas en `methodology.tex:61`, `results.tex:552`, `results.tex:1069` (3 instancias);
  minúsculas en 9 instancias repartidas en las otras 5 secciones.
- **Decisión:** FIX-NOW.
- **Corrección exacta:** normalizar las 3 instancias en mayúsculas a "winner-take-all" (convención
  mayoritaria 9 vs. 3; estándar en la literatura de ganglios basales/robótica para un mecanismo, no
  un nombre propio). La sigla WTA no está afectada.

### [P-20] "Hunting Instinct" (mayúsculas) vs. "hunting drive"/"hunting-instinct" (minúsculas) + nombre inconsistente

- **Fuentes:** Samuel (2.4-E), Diego (2.4-E) — 2/4.
- **Ubicación:** `results.tex:~641` ("Hunting Instinct", mayúsculas) vs. `methodology.tex:~235,292`
  ("hunting drive" / "hunting-instinct", minúsculas, dos nombres distintos entre sí).
- **Decisión:** FIX-NOW.
- **Corrección sugerida:** estandarizar a minúsculas en `results.tex` y unificar el nombre entre
  ambos archivos (elegir "hunting drive" o "hunting instinct", no ambos).

### [P-21] Mezcla de ortografía británica/americana — pasada de normalización dedicada

- **Fuentes:** Deivi (2.4 H3, 9 instancias listadas) — **ampliado por Diego (2.4-H) a >25 instancias
  en al menos 18 líneas**: además de las 9 de Deivi (organisation L17, behaviour L306/L672/L1044,
  characterise/characterised L460/L794, minimises L672, optimisation/generalisation/favourable L674,
  prioritise L913, colour L959), Diego encontró: analysed (L308), normalised (L393),
  synthesises/terrain-specialised/stabilisation (L298, 3 en la misma oración),
  specialisation/specialised/stabilisation (L310, 3 más), randomised (L305/L317), minimising (L935),
  "Centre of Mass" (L305) vs. "center of mass" en `methodology.tex:27` (mismo concepto, grafía
  distinta según sección).
- **Decisión:** FIX-NOW, pero — siguiendo la recomendación explícita de Diego — **como una pasada de
  normalización dedicada con grep/sed verificado manualmente**, no como 25+ filas `C-xx`
  individuales. Registrar como una sola fila `C-xx` que cubra la pasada completa, referenciando la
  lista de instancias de este documento.
- **Alcance:** normalizar a ortografía americana (convención dominante, >40 instancias ya
  americanas) en `results.tex` y `methodology.tex:27` ("Centre of Mass"→"Center of Mass").

### [P-22] "bioinspired" (sin guion, 1 instancia) vs. "bio-inspired" (14 instancias)

- **Fuentes:** Sebas (Hallazgo 11) — 1/4, nuevo.
- **Ubicación:** `conclusions.tex:4`.
- **Decisión:** FIX-NOW — fold dentro de la misma pasada de [P-21] (es la misma categoría de
  normalización ortográfica, aunque no sea británico/americano sino guionado).
- **Corrección exacta:** "bioinspired" → "bio-inspired".

### [P-23] Guion/puntuación faltante: "differential rolling mode-this mode remains active"

- **Fuentes:** Sebas (Hallazgo 8) — 1/4, nuevo.
- **Ubicación:** `results.tex:~771`.
- **Decisión:** FIX-NOW, trivial.
- **Corrección sugerida:** "...differential rolling mode; this mode remains active..." (o em-dash:
  "...rolling mode---this mode remains active...").

### [P-24] "mecanum wheel" (1 instancia) vs. "omnidirectional wheel" (14+ instancias) — terminología

- **Fuentes:** Sebas (Hallazgo 10) — 1/4, nuevo, ligado a [P-05] (misma oración de
  `methodology.tex:25`).
- **Decisión:** FIX-CON-DECISIÓN-EDITORIAL — no es necesariamente un error (una rueda mecanum es un
  tipo de rueda omnidireccional), pero introduce un término técnico distinto sin aclarar la
  relación.
- **Acción concreta:** decidir entre (a) usar "omnidirectional wheel" también aquí para consistencia
  total, o (b) aclarar explícitamente la primera vez que se usa "omnidirectional wheel" que se trata
  de una rueda tipo mecanum. Resolver junto con [P-05] ya que es la misma oración.

### [P-25] Comentario de desarrollo en `closing.tex` — artefacto de edición visible en el fuente

- **Fuentes:** Samuel (2.4-F), Diego (2.4-I) — 2/4.
- **Ubicación:** `closing.tex` línea 2: `% [CHANGE: bibliography file renamed from persbiblio to
  references]`.
- **Decisión:** FIX-NOW, trivial (no afecta compilación pero es un artefacto de proceso interno del
  repositorio sin sentido para un coautor que abra el `.tex` sin contexto — espíritu de README §11.1
  aunque técnicamente esté en comentario, no en texto renderizado).
- **Corrección exacta:** eliminar la línea del comentario.

---

## Confirmado sin acción (ya revisado por 2+ autores — no re-abrir)

### [P-26] Pares raster sim/físico — `NEU_IMU`/`NEU_IMU2` (Grupo B de figure-redundancy-audit-triage.md)

- **Fuentes:** Deivi, Samuel, Sebas, Diego — **4/4**, unánime: **NO fusionar**. Diego y Sebas
  verificaron directamente el PNG: las letras "(a)"/"(b)" están horneadas en la imagen, fusionar
  introduciría doble etiquetado ambiguo. Deivi había dejado abierta una fusión opcional de espacio
  (side-by-side sin cortar contenido) — dado el consenso 4/4 en no tocarlo y la razón técnica dura
  (letras horneadas), se descarta también esa opción.
- **Decisión:** CERRADO, sin acción.

### [P-27] `tab:action_selection_comparison` (R3-06) vs. `introduction.tex` línea ~9

- **Fuentes:** Deivi (verificó explícitamente) — ya resuelto por `C-14`: la línea 9 es solo
  fact + forward-pointer, no reintroduce columnas de la tabla.
- **Decisión:** CERRADO, sin acción.

### [P-28] Sección "warehouse" (Gazebo depot) mencionada 3 veces (intro/caption/Limitations)

- **Fuentes:** Deivi (verificó explícitamente) — cada mención tiene función distinta (forward-
  pointer, caption, caveat detallado), no hay restatement de prosa entre esas tres.
  **No confundir con [P-12]**, que es un hallazgo distinto (duplicación local entre líneas 4 y 10,
  no las 3 menciones de función distinta que aquí se confirman correctas).
- **Decisión:** CERRADO, sin acción.

### [P-29] QuantReal (4 escenarios físicos) vs. Simulation Results (4 escenarios sim) — paralelismo estructural

- **Fuentes:** documentado en §6 del audit doc madre (corrida angosta 2026-08-31) — paralelismo
  intencional, ya condensado agresivamente por `R2-01`/`C-14`.
- **Decisión:** CERRADO, sin acción.

---

## Notas para la sesión de ejecución (el "bot de redacción")

1. **Orden sugerido:** P0 → P1 → P2 → P3, en el orden en que aparecen arriba dentro de cada tier.
   [P-02]/[P-15] y [P-05]/[P-24] están explícitamente ligados — resolverlos juntos.
2. **Ítems que requerían respuesta humana — ya resueltos, ver sección "Decisiones tomadas en
   sesión" arriba:** [P-02] (estandarizar a convención de `tab:consolidated_simulation_metrics`,
   requiere recálculo de datos), [P-07] (generalizar sin cifras), [P-08] (acotar a ventana de
   transición), [P-10] (renombrar solo `noise_level_idx`, no tocar `NoiseSeed`), [P-17] (describir
   como parámetro adimensional), [P-24] (usar "omnidirectional wheel"). También decididas las
   fusiones de figuras: [P-13] y [P-14] sí se ejecutan; la fusión de las 3 figuras de
   `noise_robustness_extra` NO se ejecuta esta ronda.
3. Cada patch aplicado sigue el flujo normal: `sections/` + fila `C-xx` en `PROGRESS.md`
   (`scripts/next_id.sh C`, `Category: Escritura`, referenciando los 4 documentos de origen +
   este documento de consolidación) + `patches/<id>-<slug>.tex` + `\revblue{}` si cambia contenido
   (fusión de párrafos sí cuenta; ajuste de una palabra/mayúscula no, según CLAUDE.md).
4. [P-21] (ortografía UK/US) se registra como una sola fila `C-xx` que cubra toda la pasada, no 25+
   filas — sigue explícitamente la recomendación de Diego.
5. `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh` antes de cualquier commit que toque
   `sections/`.
6. Los 4 `final_audit_*.md` (más este documento de consolidación) se mueven a `intake/processed/`
   solo cuando **todas** las filas `C-xx` resultantes lleguen a `applied` — no antes (§5 paso 5 del
   audit doc madre).
7. `intake/pending/figure_regeneration_candidates.md` queda con las decisiones del Anexo arriba
   (FIG-1a/1c/2b ejecutar; FIG-1b/2a/2c/Grupo 3 no ejecutar esta ronda) — se mueve a
   `intake/processed/` junto con los demás solo cuando FIG-1a/1c/2b lleguen a `applied` (FIG-2c y
   FIG-1b quedan como candidatos abiertos para una ronda futura, no bloquean el movimiento del
   archivo si se documenta esa exclusión en su fila `C-xx`).
