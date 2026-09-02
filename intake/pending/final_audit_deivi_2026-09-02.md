# Auditoría final — Deivi (sesión Claude Code) — 2026-09-02

Ejecutada según `redundancy_closing_audit.md` §2/§3 (4 categorías, pasada completa,
sin editar `sections/*.tex`). Se leyeron las 6 secciones de principio a fin:
`introduction.tex`, `methodology.tex`, `results.tex` (980 líneas), `conclusions.tex`,
`preamble.tex`, `closing.tex`.

Baseline de `check_word_growth.sh` al inicio de esta sesión:
`results.tex` 12 451 palabras, `methodology.tex` 6 422, `introduction.tex` 1 534,
`conclusions.tex` 1 270, `preamble.tex` 539, `closing.tex` 82.

---

## 2.1 Inconsistencias de datos

### [2.1-A] ROC AUC: 0.866 en prosa y caption vs. 0.864 en la figura

**Ubicación:**
- `results.tex` línea ~682 (prosa): *"an ROC-AUC of 0.866"*
- `results.tex` línea ~698 (subcaption de subfigure b): *"ROC curve (AUC = 0.866)."*
- `results.tex` línea ~713 (caption del grid `fig:mlp_eval_grid`): *"(b) ROC curve (AUC = 0.866)."*
- Asset en `assets/fig2_roc_curve.png` (reconstruido por `C-21`): la leyenda muestra **0.864**

**Descripción:** `C-21` vectorizó la curva ROC y la reconstruyó con el estilo compartido; el
AUC trapezoidal recalculado desde los puntos extraídos dio 0.864 (Δ0.002 respecto al 0.866
original). La figura fue promovida con 0.864 en su leyenda "para consistencia interna", pero la
prosa y las tres referencias en el caption aún dicen 0.866. El lector ve 0.866 en el texto
y 0.864 en la figura — inconsistencia concreta y verificable.

**Sugerencia:** Actualizar prosa y subcaption a 0.864, que es el valor recalculado y el que
está en el asset. Si se prefiere mantener 0.866 (valor del experimento original), reconstruir
la figura con 0.866 en la leyenda. Lo importante es que sean iguales en texto y figura.

---

### [2.1-B] SR de Appetitive y Aversive difiere entre Tab:consolidated\_simulation\_metrics y Tab:fsm\_comparison

**Ubicación:**
- `results.tex` líneas ~132–147 (`tab:consolidated_simulation_metrics`):
  Appetitive SR = 100.0 %, Aversive SR = 100.0 %
- `results.tex` líneas ~505–511 (`tab:fsm_comparison`, columna Neural):
  Appetitive/Neural SR = 78.9 %, Aversive/Neural SR = 88.2 %
- `results.tex` línea ~543 (reconocimiento explícito): *"do not match
  Table~\ref{tab:consolidated_simulation_metrics}'s previously published figures…
  (a discrepancy already tracked, not introduced by this comparison)"*

**Descripción:** Para los cuatro escenarios comunes (Appetitive, Aversive, Obstacle, Complex),
los valores de `$T_{sim}$` y Roll RMS coinciden entre tablas, pero los SR de Appetitive (100 %
vs. 78.9 %) y Aversive (100 % vs. 88.2 %) difieren. El texto lo reconoce, pero publica los dos
valores contradictorios sin explicación de causa. Para un lector del journal esto levanta
preguntas de integridad de datos: el mismo sistema en el mismo escenario reporta tasas de éxito
distintas según la tabla que se mire. El paper actual no aclara si la diferencia viene del
conjunto de trials, del método de conteo, o del pipeline de análisis.

**Nota:** `C-22` reconcilió los valores de `$T_{sim}$` y Roll pero no explica la discrepancia
de SR. La causa posible más probable es que el pipeline de `tab:fsm_comparison` usó un
conjunto de trials distinto o una definición diferente de "éxito" que la usada para
`tab:consolidated_simulation_metrics`.

**Sugerencia:** Antes de enviar, confirmar con el equipo cuál conjunto de trials y definición
de éxito produjo cada tabla. Si los SR ahora coinciden con los datos crudos, actualizar el
texto de la línea 543 para retirar la nota de discrepancia y dejar solo la nota del outlier
excluido. Si aún difieren, añadir una nota de pie en una de las tablas explicando la razón
específica (diferente N de trials o diferente criterio de éxito por el pipeline de FSM vs. el
de la tabla consolidada).

---

### [2.1-C] SM=0.050 m / TR=0.000 "sin excepción" en los 979 muestras vs. valores en fig:transition\_phases

**Ubicación:**
- `results.tex` líneas ~453–459: *"the Normalised Stability Margin was maintained at its
  platform-geometry maximum ($SM = 0.050\,\text{m}$, $SM_{\mathrm{norm}} = 1.000$) and the
  Tipover Risk index remained at $TR = 0.000$ without exception, yielding a transition success
  rate of $6/6$ ($100\%$)."*
- `results.tex` líneas ~423–438 (caption de `fig:transition_phases`): *"$TR$ and $SM$ are
  reported as a min--max range across all instances of that mode observed across the original
  six directed transitions"*

**Descripción:** La prosa afirma TR=0.000 y SM=0.050 m para los **979 samples totales**. Sin
embargo, el caption de `fig:transition_phases` describe rangos de TR/SM por modo (min–max), lo
que implica valores no-nulos. El análisis de vectorización de N-09 (registrado en
`intake/processed/N-09_fusion_transition_phases_reversible.md`) reportó lecturas de TR en el
rango 0.003–0.079 en los 12 paneles del figura, ninguna en 0.000. No fue corregida porque
requería confirmación del autor (*"No corregido sin confirmación del autor"*).

**Interpretación más probable:** TR=0.000 aplica al instante específico de la transición
(4 patas en suelo → soporte máximo), mientras que los 979 samples incluyen también frames de
locomoción en modo establecido (3 patas en suelo → TR >0). Si ese es el caso, la prosa es
engañosa al decir "without exception" sobre todos los 979 samples.

**Sugerencia:** Restringir la afirmación de TR=0.000 explícitamente al intervalo de
reconfiguracion morfológica (*"during the morphological switching window itself"*), y señalar
que los samples de locomoción en modo establecido dentro del run de 979 muestran TR > 0.
Alternativamente, verificar con el autor si los 979 samples son solo los frames de
transición (no de locomoción estable), lo que resolvería la contradicción.

---

### [2.1-D] "direction-switching latencies below 600 ms" en conclusions.tex: trazabilidad abierta

**Ubicación:**
- `conclusions.tex` línea ~8: *"its predominant channel activation inhibiting competing
  channels and reducing the probability of erratic trajectory changes; this behavior yielded
  direction-switching latencies below 600~ms."*

**Descripción:** `C-24` lo marcó explícitamente como *"open traceability question (same class
of issue C-15 fixed for the old '47ms' claim)"*. Las latencias de hardware reportadas en
`results.tex` (`fig:FourPanelLatencies`) son 184 ms y 534 ms (Panel A y B), ambas por debajo
de 600 ms. La afirmación es técnicamente correcta pero no cita una fuente precisa — el "below
600 ms" no corresponde a ningún número reportado directamente en la tabla de resultados.

**Sugerencia:** Reemplazar por la cifra más conservadora ya reportada: *"yielding
direction-switching neural latencies of 184--534~ms (Fig.~\ref{fig:FourPanelLatencies})"*.
Esto cierra la trazabilidad y es más informativo que un bound suelto.

---

### [2.1-E] "distal end of the femur" vs. "tibia" — error de nomenclatura del limb

**Ubicación:**
- `methodology.tex` línea ~25: *"This motor is located at the distal end of the femur and is
  directly coupled to a mecanum wheel"*
- `preamble.tex` línea ~34 (abstract / descripción del robot): *"each incorporating an
  omnidirectional wheel at the distal segment (tibia)"*
- `conclusions.tex` línea ~6: describe el sistema sin repetir el término
- En `methodology.tex` la subsección `ssec:ServoCompensation` (línea ~472) dice: *"N20 motors
  rated at 104 RPM, responsible for driving the wheels located at the distal end of the tibia"*

**Descripción:** La línea 25 de `methodology.tex` dice que el motor de rueda está *"at the
distal end of the femur"*, pero el abstract (preamble.tex) y la sección de Physical Platform
Construction (metodología línea ~472) dicen *"tibia"*. El fémur es el segmento proximal (muslo)
y la tibia es el distal (espinilla) — el motor de la rueda va en el extremo distal, i.e., en la
tibia. "Femur" en la línea 25 parece ser un error de nomenclatura que sobrevivió a todas las
rondas de revisión.

**Sugerencia:** Cambiar `methodology.tex` línea ~25 de *"distal end of the femur"* a *"distal
end of the tibia"* para alinear con el abstract y con el resto de la sección de metodología.

---

## 2.2 Redundancia de datos / contenido duplicado

### [2.2-A] "builds no map, retains no spatial memory, and computes no global re-route" — casi verbatim en dos secciones

**Ubicación:**
- `methodology.tex` línea ~61 (C-20, párrafo de Gazebo Simulation sobre la tarea de inspección):
  *"it builds no map, retains no spatial memory, and computes no global re-route when
  blocked, relying instead on the same basal-ganglia/Winner-Take-All arbitration…"*
- `results.tex` línea ~552 (sssec:reactive\_inspection):
  *"The system does not implement deliberate path planning: it builds no map, retains no
  spatial memory, and does not compute a global re-route when blocked."*

**Descripción:** Las tres cláusulas ("no map", "no spatial memory", "no global re-route when
blocked") aparecen casi verbatim en ambos lugares. El patrón es idéntico al de los pares ya
condensados por R2-01. La metodología es el lugar natural para establecer el hecho;
results.tex debería cruzar-referenciar.

**Sugerencia:** Condensar la frase de results.tex línea ~552 a:
*"As described in Section~\ref{sec:methodology}, the system is purely reactive — no map,
no spatial memory, no deliberate re-routing — so the metrics used here reflect what the
reactive architecture can actually measure."*
(preservando el forward-pointer a Limitations que ya existe para coverage rate).

---

### [2.2-B] fig:mode\_timeline\_inspection y fig:mode\_timeline\_complex tienen mensaje casi idéntico

**Ubicación:**
- `results.tex` líneas ~534–538 (caption de `fig:mode_timeline_complex`): *"abrupt,
  timer-held FSM transitions vs. shorter, more graduated Neural mode occupancy"*
- `results.tex` líneas ~592–596 (caption de `fig:mode_timeline_inspection`): *"Both traces
  show the same qualitative difference as Figure~\ref{fig:mode_timeline_complex}: abrupt,
  timer-held FSM transitions vs. shorter, more graduated Neural mode occupancy."*

**Descripción:** El propio caption de `fig:mode_timeline_inspection` admite que el mensaje es
el mismo que el de `fig:mode_timeline_complex`. Dos figuras completas de una columna de ancho
que dicen lo mismo cualitativamente. El diferenciador es el escenario (Complex vs. Inspection),
no el mecanismo — que es idéntico.

**Sugerencia:** Evaluar si las dos figuras pueden fusionarse en un panel de dos filas (Neural
arriba, FSM abajo, con columnas para Complex y Inspection), similar a cómo se fusionaron otros
pares en C-29/C-30. Esto no eliminaría ningún dato y reduciría el recuento de floats. Si la
fusión no es viable por diferencias de escala temporal, al menos acortar el caption de
`fig:mode_timeline_inspection` eliminando la cláusula que repite la descripción ya en
`fig:mode_timeline_complex`.

---

## 2.3 Candidatos a acortar (tablas/figuras)

### [2.3-A] tab:fsm\_comparison — dos tablas coexistentes con SR contradictorios y sin reconciliación visual

**Ubicación:** `results.tex` líneas ~497–521 (`tab:fsm_comparison`) y líneas ~132–147
(`tab:consolidated_simulation_metrics`).

**Descripción:** Para los cuatro escenarios compartidos (Appetitive, Aversive, Obstacle,
Complex), `tab:fsm_comparison` duplica parcialmente `tab:consolidated_simulation_metrics`
(mismos $T_{sim}$ y Roll RMS para tres de las cuatro familias, pero SR diferente — ver
hallazgo 2.1-B). El lector debe reconciliar mentalmente dos tablas con datos solapados.
El texto de la línea 543 agrava el problema al reconocer la discrepancia explícitamente.

**Sugerencia de condensación:** Una vez resuelto el hallazgo 2.1-B (causa de la diferencia de
SR), podría añadirse una columna "Neural (Tab. X ref.)" en `tab:fsm_comparison` o una nota de
pie que ponga los dos SRs lado a lado con explicación. Esto no reduce el número de tablas pero
resuelve la ambigüedad sin que el lector tenga que saltar entre secciones. Alternativamente, si
los SRs coinciden tras la revisión, eliminar la nota de la línea 543 y dejar solo la nota del
outlier excluido.

---

### [2.3-B] Párrafo de cierre del ablation study (línea ~207) restata puntos ya establecidos

**Ubicación:** `results.tex` línea ~207: *"Taken together, these results support the
winner-take-all arbitration design on two separable grounds. First… Second…"*

**Descripción:** El párrafo de cierre del ablation study resume las conclusiones del estudio,
pero ambos "grounds" ya están establecidos con detalle en los dos párrafos anteriores (SR
collapse para R3-01; latency + stability degradation para R3-02). El párrafo añade pequeñas
matizaciones ("supported by latency and attitude metrics rather than success rate alone") pero
en su mayoría repite la estructura lógica ya presentada.

**Sugerencia:** Reducir el párrafo de cierre a 1-2 oraciones que solo añadan el hecho nuevo
que no está en los párrafos anteriores: la distinción entre los dos grounds (mechanism-level
vs. static-threshold comparison). Las oraciones que repiten los números o conclusiones ya
establecidas pueden eliminarse.

---

### [2.3-C] Tab:inspection\_metrics — columna de métricas con nombres de estilo-código

(Ver también hallazgo 2.4-B.) Esta tabla tiene 5 métricas: $d_{final}$,
$N_{lidar\_events}$, $N_{mode\_X\_events}$, $T_{acquisition}$, $T_{task}$. Dos de estas
($N_{lidar\_events}$, $N_{mode\_X\_events}$) tienen nombres con underscores propios de
variables de código. La tabla es de tamaño apropiado pero podría condensar las dos últimas
columnas ($T_{acquisition}$ / $T_{task}$) en una sola si el espacio lo permite, dado que
ambas son métricas de tiempo con definiciones distintas pero relacionadas.

**Sugerencia:** De menor prioridad — la tabla es compacta. El hallazgo principal es en 2.4-B.

---

## 2.4 Ortografía, convenciones académicas, y nombres filtrados del repositorio

### [2.4-A] "Experiment E" en caption de tab:inspection\_metrics — identificador de repositorio

**Ubicación:** `results.tex` línea ~560:
```latex
\caption{\revblue{Reactive Inspection Task --- Aggregate Performance Metrics
(Experiment E, 17/20 successful trials, …)}}
```

**Descripción:** La etiqueta "Experiment E" es el identificador interno de familia del
repositorio (`familia_e` en el código, "Familia E" en los documentos de análisis). El PROGRESS.md
de R3-05 documenta explícitamente que el autor quitó "(Experiment E)" de las dos apariciones en
el cuerpo de texto (*"título de párrafo y el que abre 'Regarding the Reactive Inspection Task'"*),
pero la caption de la tabla sobrevivió intacta. Es exactamente el tipo de identificador que
README §11.1 prohíbe filtrar al texto visible por el lector.

**Sugerencia:** Eliminar `(Experiment E, ` de la caption. La frase resultante —
*"Reactive Inspection Task --- Aggregate Performance Metrics (17/20 successful trials, obstacle
field with initially non-visible target)"* — es autoexplicativa sin el identificador interno.

---

### [2.4-B] $N_{lidar\_events}$ y $N_{mode\_X\_events}$ — nombres de métrica de estilo-código

**Ubicación:** `results.tex` líneas ~554 y ~566–569 (prosa y tabla):
*"$N_{lidar\_events}$ counts sensory-level obstacle-detection transitions"*;
*"$N_{mode\_X\_events}$ counts the resulting omnidirectional-mode switches"*

**Descripción:** Estos nombres de métrica usan la convención de snake_case typical de variables
de código (subíndices con underscores: `lidar_events`, `mode_X_events`). Las otras métricas de
la misma tabla ($d_{final}$, $T_{acquisition}$, $T_{task}$) usan la convención estándar de
publicación (inicial + subscript conciso, no snake_case). La regla README §11.1 menciona
"nombres de columna de CSV" como ejemplo de identificadores a no filtrar; estos nombres se
parecen más a columnas de CSV que a símbolos matemáticos estándar.

**Sugerencia:** Renombrar en prosa y tabla a símbolos más convencionales, p.ej.:
- $N_{lidar\_events}$ → $N_{ev}^{LiDAR}$ (LiDAR obstacle-detection event count) o simplemente
  $N_{obs}$ con definición en texto
- $N_{mode\_X\_events}$ → $N_{ev}^{X}$ (omnidirectional-mode-switch event count) o $N_{sw}$

Mantener la definición en prosa para que el lector no tenga que inferir el significado.

---

### [2.4-C] "Figure" vs. "Fig." — inconsistencia en referencias dentro de results.tex

**Ubicación:** `results.tex`:
- Línea ~99: `Fig.~\ref{fig:NEU_EST_MUL}` (abreviado)
- Líneas ~111, ~115: `Fig.~\ref{fig:NEU_EST_MUL}b`, `Fig.~\ref{fig:NEU_EST_MUL}a` (abreviado)
- Resto del archivo (~30 referencias): `Figure~\ref{…}` (escrito completo)

**Descripción:** La gran mayoría de referencias a figuras en todo el papel usa `Figure~\ref{}`,
pero tres ocurrencias en la subsección de "Response to Multiple Stimuli" usan `Fig.~\ref{}`. La
inconsistencia es localizada pero visible. `methodology.tex` y `conclusions.tex` usan
consistentemente la forma larga.

**Sugerencia:** Cambiar las tres ocurrencias de `Fig.~` a `Figure~` en `results.tex` (líneas
~99, ~111, ~115). Es un cambio de 3 caracteres × 3 = trivial.

---

### [2.4-D] "Winner-Take-All" (mayúsculas) vs. "winner-take-all" (minúsculas) — inconsistencia

**Ubicación:**
- `introduction.tex` línea ~30: *"a salience-driven winner-take-all (WTA) mechanism"*
  (minúsculas)
- `results.tex` línea ~552: *"the basal-ganglia/Winner-Take-All (BG/WTA) arbitration network"*
  (Title Case, en `\revblue{}`)
- `results.tex` línea ~586: *"the WTA arbitration"* (sigla, sin el término escrito)
- `methodology.tex` línea ~65: *"behavioral decision-making"* (no usa el término directamente)

**Descripción:** El mismo término se escribe como nombre propio capitalizado en results.tex
(parcial del texto nuevo de R3-05) y como descriptor en minúsculas en introduction.tex. La
convención estándar en la literatura de basal ganglia/robotics es usar "winner-take-all" en
minúsculas cuando se describe el mecanismo (no es un nombre propio).

**Sugerencia:** Estandarizar a minúsculas ("winner-take-all") en toda aparición que no sea
el sigla WTA o el nombre propio del módulo (Basal Ganglia Module). Cambio puntual en
`results.tex` línea ~552.

---

### [2.4-E] "Hunting Instinct" (mayúsculas, results.tex) vs. "hunting instinct" / "hunting drive" (metodología)

**Ubicación:**
- `results.tex` línea ~641: *"from the constant Hunting Instinct stimulus"* (capitalized)
- `methodology.tex` línea ~235: *"$HI$ denotes an intrinsic hunting drive"* (minúsculas,
  además nombre diferente: "drive" vs. "instinct")
- `methodology.tex` línea ~302: *"$HI = 3.0$ defines a baseline forward bias"* (minúsculas)

**Descripción:** El parámetro $HI$ se introduce en methodology como "hunting drive" o "hunting
instinct" en minúsculas, pero results.tex lo trata como nombre propio ("Hunting Instinct" con
mayúsculas). El nombre en sí también difiere: "drive" vs. "instinct" (menor, pero añade
ambigüedad). No es un término de la literatura de neurosci — es un nombre interno del modelo.

**Sugerencia:** Estandarizar a minúsculas en results.tex ("hunting instinct" o "hunting drive"
— elegir uno) y usar el mismo nombre que methodology.tex usa para el parámetro $HI$.

---

### [2.4-F] Comentario de desarrollo en closing.tex — artefacto de edición visible en fuente

**Ubicación:** `closing.tex` línea 2:
```latex
\bibliographystyle{elsarticle-num-names}
% [CHANGE: bibliography file renamed from persbiblio to references]
```

**Descripción:** El comentario `% [CHANGE: bibliography file renamed from persbiblio to
references]` es un artefacto de proceso interno (nota de edición del repositorio), no un
comentario LaTeX con función técnica. No afecta la compilación (es un comentario) pero
contamina el fuente del paper con terminología de desarrollo que no tendría sentido para
cualquier co-autor que lea el `.tex` directamente sin el contexto del repositorio. Por
convención del proyecto (README §11.1, C-17), este tipo de identificadores de
repositorio no debe quedar en el texto visible — aunque este está en un comentario LaTeX, por
limpieza debería eliminarse antes de la versión final que se sube a Overleaf.

**Sugerencia:** Eliminar la línea del comentario de `closing.tex`. Cambio de una línea.

---

## Resumen ejecutivo

| Cat. | ID | Severidad | Archivo | Descripción breve |
|---|---|---|---|---|
| 2.1 | A | Alta | results.tex | AUC 0.866 prosa vs. 0.864 figura (C-21 actualizó figura pero no texto) |
| 2.1 | B | Alta | results.tex | SR Appetitive 100% vs. 78.9% / Aversive 100% vs. 88.2% entre dos tablas |
| 2.1 | C | Media | results.tex | TR=0.000 "sin excepción" en 979 samples vs. valores no-nulos en fig:transition_phases |
| 2.1 | D | Baja | conclusions.tex | "below 600 ms" — trazabilidad abierta (C-24), reemplazar por 184–534 ms |
| 2.1 | E | Media | methodology.tex | "distal end of the femur" → debe ser "tibia" (inconsiste con preamble + resto de metodología) |
| 2.2 | A | Media | methodology/results | "builds no map…" casi verbatim en dos secciones — candidato a condensar |
| 2.2 | B | Baja | results.tex | fig:mode\_timeline\_inspection = mismo mensaje que fig:mode\_timeline\_complex |
| 2.3 | A | Media | results.tex | Dos tablas con datos solapados y SRs contradictorios sin reconciliación visible |
| 2.3 | B | Baja | results.tex | Párrafo de cierre del ablation study restata los dos grounds ya establecidos |
| 2.3 | C | Baja | results.tex | tab:inspection\_metrics — métricas con nombres de estilo-código (ver 2.4-B) |
| 2.4 | A | **Alta** | results.tex | "Experiment E" en caption de tab:inspection\_metrics — identificador de repo (§11.1) |
| 2.4 | B | Media | results.tex | $N_{lidar\_events}$/$N_{mode\_X\_events}$ — snake_case de código en notación matemática |
| 2.4 | C | Baja | results.tex | "Fig." vs. "Figure" — 3 ocurrencias inconsistentes (líneas ~99, ~111, ~115) |
| 2.4 | D | Baja | results.tex | "Winner-Take-All" mayúsculas vs. "winner-take-all" minúsculas |
| 2.4 | E | Baja | results.tex | "Hunting Instinct" mayúsculas + nombre inconsistente vs. "hunting drive" en metodología |
| 2.4 | F | Baja | closing.tex | Comentario de desarrollo `% [CHANGE: …]` — artefacto de edición en fuente |

**Hallazgos de alta prioridad antes de envío:** 2.1-A (AUC inconsistente), 2.1-B (SR
contradictorios entre tablas), 2.4-A (identificador de repo en caption de tabla).

**Hallazgos que requieren confirmación del autor antes de editar:** 2.1-C (TR=0.000 vs.
fig:transition\_phases), 2.1-D (600 ms vs. 184–534 ms).

**Hallazgos resueltos por pasadas anteriores (confirmados, sin acción nueva):**
- §6 del audit doc: C-23/C-24 ya aplicados, la redundancia cross-section de Limitations
  (Reactive Inspection Task) y de conclusions.tex (BG mechanism) está cerrada.
- Grupo B del figure-redundancy-audit (rasters NEU\_IMU sim vs. real): revisados en §6,
  confirmados como pares legítimos de validación sim→real — sin cambios.
- tab:action\_selection\_comparison vs. párrafo línea 9: confirmado por C-14, sin restatement.
- Sección "warehouse" (Gazebo depot): 3 menciones con función distinta — sin restatement.
