# Auditoría final ronda 2: Deivi (C-77), agente de redundancia (1.2) y acortamiento (1.3), 2026-11-03

Prefijo `R-`. Es una pasada de hallazgos: no se editó nada en el repo. Primero leí entero el paper actual (`results.tex`
completo y luego methodology, introduction, conclusions, closing y preamble/abstract). Después contrasté con
`intake/pending/round2_decision_letter_2026-10-25.md` (texto literal), PROGRESS.md (R2-01, R3b-01, R2b-02/03, C-57,
C-60, C-64, C-66, C-67, C-69), `second_pass_simplification_debate.md` (P-24 REJECT, P-25, P-26) y el `git log -S` de
los pasajes duplicados. Las auditorías de Sam y Sebas las leí **después** de mi primera lista.

Las palabras ahorradas se cuentan sobre el texto fuente, sin `\revblue{`/`\emph{` y con `split()` de Python. Es una
estimación del orden de magnitud, no el `wc -w` de `check_word_growth.sh`.

## 0. ¿Se reintrodujo verbosidad después de R2-01?

`scripts/check_word_growth.sh` (línea base 51c07b4, 2026-08-26): results 8645 → 12858 (+4213), introduction +271,
methodology +250, conclusions −139. Casi todo el crecimiento de `results.tex` es contenido nuevo pedido por los revisores
(FSM, ablación, inspección, ruido, estabilidad de transiciones, MLP on-device). **Sí hay verbosidad reintroducida**, pero
se concentra en un patrón: **las salvedades (caveats) que pidieron los revisores se añadieron a captions y texto sin
quitar la versión que ya existía en la prosa**. Los casos, por commit:

- `af653fd` (2026-11-02, R2b-03): salvedad de equidad del FSM completa en el caption de `tab:fsm_comparison` (94 palabras).
  Duplica casi palabra por palabra la prosa de `results.tex:522` (`1204e1a`, R2-02) y `methodology.tex:439` → R-01.
- `112b808` (2026-10-29, R2b-02/R3b-03): la salvedad de ruido conjunto se escribió entera en `:73` y otra vez en `:152` → R-03.
- `2c8d755` (2026-10-31, C-69): la explicación de "las filas de terreno vienen de otra re-ejecución" está en la prosa
  (`:463–466`) y en el caption de `tab:fsm_comparison` → R-07.
- `9a872a6` (C-32) + C-75: "los valores Neural coinciden con `tab:consolidated_simulation_metrics`" en `:130` y `:524` → R-05.

Recortando solo lo de bajo riesgo (sección 3), el ahorro estimado es de **≈ 480 palabras**. S-30 (escenarios físicos)
podría sumar ≈ 250 más, pero tiene más riesgo.

**Aviso de calendario:** el deadline es mañana (2026-11-04). Todo lo que sigue es media/baja. Ninguno de estos
hallazgos bloquea el envío. Los de 1.1 de Sam/Sebas (S-03, S-04, S-09) tocan los mismos párrafos que S-30/R-08 y van
primero.

---

## 1.2 Redundancia y contenido duplicado

### R-01 · MEDIA · Salvedad de equidad de timing FSM: la prosa repite el caption de la tabla
- **Ubicación:** `results.tex:522` (prosa, "but $T_{switch}$/$T_{response}$ are deliberately omitted: the team that ran
  the FSM terrain trials identified three configuration differences …"), `results.tex:480` (caption de
  `tab:fsm_comparison`, "Fairness caveat on timing metrics: … three configuration differences … (the pitch-instability
  threshold, a transition timing offset, and the switching-time formula's margin term) …") y `methodology.tex:439`
  ("except for three configuration differences in the terrain-transition logic (the pitch-instability threshold, a
  transition timing offset, and the switching-time formula's margin term)").
- **Cita literal (prosa :522):** "that make those two specific metrics not comparable under strictly identical
  conditions without re-running both controllers with matched parameters, which was out of scope for this comparison."
  El caption de :480 dice exactamente lo mismo: "make those two specific metrics not comparable under strictly identical
  conditions without re-running both controllers with matched parameters, which was out of scope for this comparison".
- **Cómo lo verifiqué:** comparé el texto (son idénticas 23 palabras seguidas) y conté palabras: caption 94, prosa 63,
  methodology 87. Con las tres captions de figura (43 cada una, `:509`, `:518`, `:576`) son seis apariciones.
  `git log -S`: el caption completo de la tabla entró en `af653fd` (2026-11-02).
- **Contraste con el revisor (R2b-03, literal):** "This important fairness caveat is currently only in the main text
  prose. Please duplicate this note inside the 'figure caption of FSM comparison plots'". El revisor pide *duplicar*:
  las captions se quedan (decisión ya cerrada en R2b-03; Sebas descartó M-15 por eso). La prosa también debe conservar
  la salvedad, pero no hace falta que sea la versión larga.
- **Corrección sugerida (sin aplicar):** dejar la versión larga solo en Methodology (que define el FSM) y en el caption
  de la tabla, y reducir `:522` a "On the two terrain suites, $T_{switch}$/$T_{response}$ are omitted for the reason
  given in Section~\ref{ssec:FSMBaseline} and the caption of Table~\ref{tab:fsm_comparison}." Se mantiene intacta la
  segunda frase de `:522`, la del desequilibrio muestral (6/3 vs 25/21 y las vuelcas 0 vs 6/21), que no está en ningún
  caption con esas cifras. **Ahorro ≈ 45 palabras.**
- **Coincide con Sam S-28** (misma propuesta para `:522`).

### R-02 · BAJA · Ablación: la interpretación de Pitch/Roll aparece en el caption (b) y en la prosa; además hay una tautología
- **Ubicación:** caption de `fig:ablation_combined`, `results.tex:211`, "Pitch RMS shows a different pattern: … plausibly
  reflecting reduced net locomotor activity in trials that fail outright rather than improved attitude control"
  (48 palabras), frente a `results.tex:215`, "Pitch RMS instead diverges by ablation type: … plausibly a symptom of
  reduced net locomotor activity in the majority of trials that fail outright under these two ablations rather than
  improved attitude control" (51 palabras). Tautología en `results.tex:194`: "\emph{no lateral inhibition} (inhibitory
  connections) and \emph{no STN/STR} (neural layers), collapse the success rate significantly, which quantifies the
  consequence of removing inhibitory connections or key neural layers" (la subordinada repite el paréntesis).
- **Cómo lo verifiqué:** lectura y conteo. El patch `patches/c-60-ablation-prose-trim.tex` confirma que C-60 solo quitó
  las **cifras** duplicadas y dejó la interpretación en los dos sitios.
- **Contraste con el revisor (R3b-02):** "Add brief explanations for four circuit variants and sample size in figure
  captions". Lo obligatorio en el caption son las variantes y el n. La interpretación mecánica no lo es.
- **Corrección sugerida:** en el caption (b), quedarse con las cifras y cortar en "… both $p<0.005$)." (≈ −12 palabras).
  En `:194`, borrar ", which quantifies the consequence of removing inhibitory connections or key neural layers"
  (−13 palabras). Ojo: la regla de C-64 era "cut the PROSE, never a caption", pero esa regla protegía lo pedido por
  R3b-02/R2b-05, y esta cláusula no es nada de eso. **Ahorro ≈ 25 palabras.**
- **Coincide con Sam S-27 y Sebas M-16** (los dos proponen dejar la interpretación solo en la prosa). La tautología de
  `:194` es **NUEVA**.

### R-03 · BAJA · Salvedad de ruido conjunto: `:152` repite entero lo que `:73` ya extiende a "all four scenarios"
- **Ubicación:** `results.tex:73` ("so the trends in Figure~\ref{fig:noise_robustness_grid}, across all four scenarios,
  cannot be attributed to any single sensing modality. Moreover, the IMU channel is perturbed only through cumulative
  random-walk drift …", 80 palabras) y `results.tex:152` ("As in those four scenarios, the three perturbation sources
  are injected jointly at every non-zero severity level rather than in isolation, … the IMU channel, as before, is
  perturbed only through cumulative random-walk drift, with additive white noise held at zero throughout", 55 palabras).
  En el mismo párrafo `:73`, `fig:noise_robustness_grid` se cita tres veces (cabecera, "(see Figure … for the per-level
  $T_{sim}$/Pitch RMS/Decision Latency/$T_{switch}$ trends)" y la salvedad).
- **Cómo lo verifiqué:** lectura y conteo. Recuento total de la salvedad: methodology `:417`, `:421` (caption de tabla),
  `:434`; results `:62` (caption), `:73`, `:152`, `:176` (caption), `:1050` (Limitations); conclusions `:16`. Son nueve
  apariciones.
- **Contraste con el revisor (R2b-02, literal):** "should also be briefly noted within the main text results section for
  this experiment". `:152` introduce un experimento distinto (los dos suites de terreno, `fig:noise_robustness_extra_combined`),
  así que ahí conviene una mención *breve*, no una segunda versión completa. El caption de esa figura (`:176`) ya lleva
  la salvedad completa (R3b-03).
- **Corrección sugerida:** sustituir la frase revblue de `:152` desde "As in those four scenarios…" por "\revblue{The
  joint-injection and drift-only caveats stated above for the four scenarios apply here unchanged.}" (≈ 15 palabras).
  En `:73`, quitar el paréntesis "(see Figure~\ref{fig:noise_robustness_grid} for the per-level … trends)", porque la
  cabecera del párrafo ya cita la figura. **Ahorro ≈ 50 palabras.** Las cinco apariciones pedidas (la de resultados y
  las de los captions) no se tocan.
- **Coincide parcialmente con Sebas M-14.** Sebas solo propone consolidar dentro de Methodology (ver R-04). Lo de `:152`
  y la cita triple de `:73` es **NUEVO**.

### R-04 · BAJA · Methodology dice dos veces "no configuration isolates a single sensor"
- **Ubicación:** `methodology.tex:417` ("three sensor-level perturbation mechanisms were combined into a single sweep
  index … applied jointly") y `methodology.tex:434` ("every level above 0 already combines all three simultaneously: no
  configuration isolates a single sensor's contribution from the others"). Además, `results.tex:1050` (Limitations) usa
  casi la misma frase: "applied jointly: no configuration isolates a single sensor's degradation".
- **Cómo lo verifiqué:** lectura.
- **Corrección sugerida:** en `:434`, dejar "At $\eta=0$ all three mechanisms are inactive, providing the unperturbed
  baseline." y borrar la segunda mitad, porque `:417` y el caption de `table:PerturbationParams` ("swept jointly (not in
  isolation)") ya lo dicen. **Ahorro ≈ 15 palabras.** Limitations se queda como está (allí es una limitación explícita;
  P-25 ya la dejó en una sola mención).
- **Coincide con Sebas M-14.**

### R-05 · BAJA · "Los valores Neural coinciden con `tab:consolidated_simulation_metrics`" se dice dos veces
- **Ubicación:** `results.tex:130` ("these are the same trials as the corresponding four basal-ganglia rows of
  Table~\ref{tab:fsm_comparison}") y `results.tex:524` ("The Neural-side values for the Appetitive, Aversive, Obstacle,
  and Complex suites are recomputed from the raw trial logs and match Table~\ref{tab:consolidated_simulation_metrics} on
  every reported statistic, under the single success-rate definition given above.").
- **Cómo lo verifiqué:** comparé fila a fila las dos tablas en el fuente. Appetitive 38.52±1.20 / 0.536 ↔ 0.54, Aversive
  9.98±2.07 / 1.357 ↔ 1.36, Obstacle 15.72±2.49 / 1.547 ↔ 1.55, Complex 24.96±10.36 / 1.034 ↔ 1.03: coinciden. No
  recomputé los JSON porque eso es trabajo del agente D-.
- **Corrección sugerida:** borrar `:524` entero (32 palabras). Así desaparece también "under the single success-rate
  definition given above", que Sam (S-07) mostró que es falso. **Ahorro ≈ 32 palabras.**
- **Coincide con Sam S-29.**

### R-06 · BAJA · La exclusión del ensayo Obstacle anómalo se explica tres veces (dos en el mismo párrafo)
- **Ubicación:** `results.tex:130` (dentro del revblue: "15 successful trials per scenario, 14 in Obstacle Evasion after
  the exclusion noted below", y dos frases después: "(one Obstacle trial with an anomalous, physically implausible roll
  reading was excluded, as in Table~\ref{tab:fsm_comparison})"), el caption de `tab:consolidated_simulation_metrics`
  (`:134`, "after the exclusion noted above") y el caption de `tab:fsm_comparison` (`:480`, "One Obstacle/Neural trial
  with an anomalous roll reading (physically implausible per-timestep values …) was excluded …").
- **Cómo lo verifiqué:** lectura. El "noted below" apunta a una frase del mismo párrafo.
- **Corrección sugerida:** en `:130`, juntar las dos menciones: "…(15 successful trials per scenario; 14 in Obstacle
  Evasion, where one trial with a physically implausible roll reading was excluded, as in Table~\ref{tab:fsm_comparison})…",
  y dejar la última frase en "Values are recomputed directly from the archived per-trial simulation logs." Los dos
  captions se quedan, porque tienen que ser autocontenidos. **Ahorro ≈ 15 palabras.**
- **NUEVO.**

### R-07 · BAJA · "Las filas de terreno de `tab:fsm_comparison` vienen de otra re-ejecución": en la prosa y en el caption
- **Ubicación:** `results.tex:463–466` ("The two terrain rows of Table~\ref{tab:fsm_comparison} come from an independent
  re-run of those scenarios rather than from this battery, and are not bounded by these values; see that table's
  caption.", 32 palabras) y el caption `:480` ("Those two terrain rows come from an independent re-run of the two scenarios, not from
  the variable-topography battery …, so their Roll RMS is not comparable with the bounds reported there.", 32 palabras).
- **Cómo lo verifiqué:** lectura y `git log -S`. Los dos textos entraron juntos en `2c8d755` (C-69, 2026-10-31).
- **No reabro C-69:** citar las dos baterías por separado es deliberado (brief §3). Lo único redundante es que la
  explicación esté dos veces.
- **Corrección sugerida:** en `:463–466`, dejar solo "\revblue{(The terrain rows of Table~\ref{tab:fsm_comparison} come
  from a separate re-run; see its caption.)}". **Ahorro ≈ 15 palabras.** Prioridad mínima: se puede dejar como está
  si se prefiere no tocar texto de C-69 a un día del envío.
- **NUEVO.**

### R-08 · MEDIA · La misión física de 15 ensayos multiterreno se describe dos veces, sin referencia cruzada
- **Ubicación:** `results.tex:798` ("a dedicated testing suite of 15 continuous repetitive trials was conducted over an
  experimental track whose structural layout systematically combines four topographic segments …") y `results.tex:1025`
  ("a continuous multi-terrain navigation mission was executed across 15 hardware replicates. The track forced the robot
  from Quadrupedal to Differential Rolling Mode to climb a steep incline, then back to Quadrupedal Mode on unstructured
  terrain …"). La misma frase de `:1025` tiene relleno: "the resulting temporal dynamics are partitioned into a
  four-panel layout to preserve resolution against low statistical variance".
- **Cómo lo verifiqué:** lectura y comparación con `tab:terrain_sequence`: misma secuencia (rampa → rolling, rugoso →
  cuadrúpedo, 15 ensayos). No pude confirmar con datos que sean los mismos 15 ensayos.
- **Corrección sugerida:** en `:1025`, "Over the 15-trial compound-terrain mission of Table~\ref{tab:terrain_sequence},
  the basal ganglia loop's decision latency shows …", borrando la redescripción de la pista y la frase sobre el layout de
  cuatro paneles. **Ahorro ≈ 40 palabras.** **Depende de S-04/A-7:** si los paneles A/B salen del banco de pitch
  (`Imu_pitch_test_t01`, N=12 por dirección), entonces **no** son esta misión y lo que hay que corregir es la atribución,
  no la redundancia.
- **Coincide con Sam S-26.** El relleno del layout es **NUEVO** y se puede sumar a S-32.

### R-09 · BAJA · Inspección: "17/20, three timeouts (trials 7, 11, 17)" tres veces en media página
- **Ubicación:** prosa `results.tex:537` ("Twenty trials yielded SR $= 85\%$ (17/20), with three timeouts (trials 7, 11,
  17) discussed below"), el caption de `tab:inspection_metrics` `:541` ("(17/20 successful trials …)") y la nota al pie
  de la tabla `:555` ("Success rate: 17/20 (85\%); three timeouts at 90~s (trials 7, 11, 17), analyzed below."). La fila
  Inspection de `tab:fsm_comparison` lo da una cuarta vez.
- **Cómo lo verifiqué:** lectura.
- **Contraste con el revisor (R3b-05):** "statistical rules for experimental samples" en el caption. Eso lo cubre la
  frase "Sampling rule: 20 independent trials, 90 s timeout, no noise injection; mean ± sample SD …" del caption, que
  no se toca.
- **Corrección sugerida:** borrar la nota al pie `:554–555` (`\\[2pt]` + footnotesize). El caption ya dice 17/20 y el
  timeout de 90 s. **Ahorro ≈ 15 palabras** y una línea de la tabla.
- **NUEVO.**

### R-10 · BAJA · `fig:inspection_dfinal_scatter` citada tres veces en dos frases seguidas
- **Ubicación:** `results.tex:558`: "(…close to one detection per capsule\revblue{; $d_{final}$ in
  Figure~\ref{fig:inspection_dfinal_scatter}}) … (…before finding a route toward the target\revblue{; $d_{final}$ in
  Figure~\ref{fig:inspection_dfinal_scatter}}). Despite the substantially messier routes, … as the clean group
  (Figure~\ref{fig:inspection_dfinal_scatter})".
- **Cómo lo verifiqué:** `grep -o "ref{fig:inspection_dfinal_scatter}"`: las tres únicas citas del paper están en esa
  línea. Si se quitan las dos revblue, la figura sigue citada una vez.
- **Corrección sugerida:** quitar los dos "\revblue{; $d_{final}$ in Figure~\ref{…}}". **Ahorro ≈ 10 palabras.**
- **NUEVO.**

### R-11 · BAJA · "Circuitos ejecutados en el portátil externo": cinco o seis menciones
- **Ubicación:** `methodology.tex:196` ("with the circuits executed on an external computer (Section~\ref{ssec:HardwareSpec})"),
  `methodology.tex:458` (Hardware Spec), `table:HardwareParams` (fila Off-board), `results.tex:701` ("the external laptop
  described in Section~\ref{ssec:HardwareSpec}"), `results.tex:1033` (Limitations) y `conclusions.tex:16` ("with the
  neural circuits executed on an external computer").
- **Contraste con el revisor:** P-26 ya recortó dos menciones y decidió conservar Hardware Spec y Limitations explícitas,
  porque el revisor de R2b-04 no tenía claro dónde se computaba. La de `:701` es necesaria (aclara de dónde sale la
  latencia del host).
- **Corrección sugerida (opcional):** en `conclusions.tex:16`, borrar ", with the neural circuits executed on an
  external computer", porque la misma frase termina con "onboard feasibility was assessed only for the MLP terrain
  classifier on the ESP32-S3 … not for the full neural pipeline", que ya lo implica. **Ahorro ≈ 10 palabras.**
- **Coincide con Sebas B-5.**

### R-12 · BAJA (nota, no recorte) · Latencias 75.9 ms y 184/534 ms en Methodology, Results y Conclusions
- **Ubicación:** `methodology.tex:196`, `results.tex:215` (75.9 ms con IC), caption `results.tex:1021` (184/534 ms) y
  `conclusions.tex:8` (las dos cifras, con IC).
- **No reabro P-24** (REJECT, porque C-15 puso a propósito cifras trazables en Methodology). Lo dejo solo como aviso para
  la consolidación: **si S-04/A-7 obliga a cambiar el N o la atribución de 184/534 ms, hay que editar cuatro sitios**.
  Ese es el único argumento nuevo para reducir `methodology.tex:196` a un puntero ("measured in
  Sections~\ref{sssec:fsm_baseline_comparison}… and~\ref{ssec:QuantReal}"). Ahorro potencial ≈ 45 palabras.
- **Relacionado con Sam S-04 y Sebas A-7** (trazabilidad). Como observación de redundancia es **NUEVO**.

### R-13 · BAJA · "The same static-threshold family already used elsewhere in this architecture's Locomotion Module", dos veces
- **Ubicación:** `methodology.tex:198` ("the same threshold-logic family already used elsewhere in this architecture's own
  Locomotion Module") y `results.tex:217` ("including the same static-threshold family already used elsewhere in this
  architecture's Locomotion Module").
- **Corrección sugerida:** en `:217`, "…and no simpler substitute, including static threshold logic, matches it once
  continuous, real-time arbitration is what the task actually requires." **Ahorro ≈ 10 palabras.**
- **NUEVO.**

### R-14 · BAJA · La definición de success rate y la nota de muestra pequeña, repetidas entre `:504` y el caption `:509`
- **Ubicación:** `results.tex:504` ("i.e. a trial that first times out and is then retried still counts as a success …",
  y ", non-monotonically given the small per-level sample") y el caption de `fig:attempts_vs_noise_level` `:509` ("not a
  success-rate metric: every mission in this dataset eventually succeeds …"; "non-monotonically (each point averages
  only 3 trials …)"). La definición está también en el caption de `tab:fsm_comparison`.
- **Corrección sugerida:** primero arreglar la frase como pide S-07 (es falsa). Luego quitar de `:504` ",
  non-monotonically given the small per-level sample", porque el caption lo explica con más detalle. **Ahorro ≈ 7 palabras.**
- **Coincide parcialmente con Sam S-07** (allí el problema es la veracidad, no la repetición). La repetición es **NUEVA**.

### R-15 · BAJA · Introducción: "developed at ETH Zürich" dos veces; la arbitración por CPG se menciona en `:10` y en `:32`
- **Ubicación:** `introduction.tex:6` y `:8` (ETH Zürich). La arbitración por CPG con feedback aparece en `:10`
  ("including feedback-modulated variants that trigger gait transitions from vestibular or load feedback"), en la tabla
  (fila CPG) y en `:32`.
- **Corrección sugerida:** quitar el segundo "developed at ETH Zürich". Lo del CPG no lo tocaría por redundancia: C-14 ya
  lo condensó y, si se aplica S-06 (no hay CPG en el método), `:32` se reescribe de todos modos. En esa reescritura,
  conviene que `:10` y `:32` no vuelvan a decir lo mismo. **Ahorro ≈ 4 palabras.**
- **Coincide con Sebas B-4.** La nota del CPG depende de Sam S-06.

### R-16 · BAJA · Limitations termina con una frase que solo dice "esto no se repite aquí"
- **Ubicación:** `results.tex:1054`: "The Reactive Inspection Task's scope constraints (absence of deliberate path planning
  or mapping, the resulting inapplicability of a formal coverage-rate metric, and the first- rather than re-acquisition
  semantics of $T_{acquisition}$) are established alongside that experiment's own results in
  Section~\ref{sssec:reactive_inspection} above and are not restated here." (45 palabras)
- **Cómo lo verifiqué:** `git log -S`: la puso `177475c` (C-20/C-21) al sustituir el párrafo duplicado. La frase enumera
  justo lo que dice no repetir.
- **Corrección sugerida:** reducirla a "\revblue{The Reactive Inspection Task's scope constraints are stated with its
  results (Section~\ref{sssec:reactive_inspection}).}" (≈ 12 palabras). Si se prefiere no tener ninguna mención en
  Limitations, se puede borrar entera. **Ahorro ≈ 33–45 palabras.**
- **NUEVO.**

---

## 1.3 Candidatos a acortar

### R-17 · MEDIA · Escenarios físicos: la tabla, cuatro párrafos y cuatro captions dicen lo mismo
- **Ubicación:** `results.tex:871–979` (`tab:consolidated_physical_metrics` y los párrafos `:894`, `:917`, `:940`, `:963`,
  con sus captions `:890`, `:913`, `:936`, `:959`).
- **Cómo lo verifiqué:** lectura. Las celdas de la tabla ("Dual-peak (detection + retreat-FOV)", "Three-phase") son las
  frases de los captions resumidas, y los párrafos las vuelven a contar.
- **Corrección sugerida:** la de Sam S-30: la tabla queda como único sitio de las cifras; los captions se reducen a
  "(a) ECDF of $T_{switch}$; (b) $Var(z)$ and Roll/Pitch RMS"; en la prosa queda solo el mecanismo. **Ahorro ≈ 250
  palabras.** No se pierde ningún dato: R2-01 fue quien creó la tabla consolidada para esto. **Ojo, orden:** antes hay
  que corregir S-03/S-09/S-10/S-11, porque tocan las mismas celdas y captions, y además está abierta la pregunta de
  3 vs 4 réplicas del Appetitive (no la reabro). A un día del envío, solo lo haría si esas correcciones se aplican de
  todos modos.
- **Coincide con Sam S-30.**

### R-18 · BAJA · `tab:consolidated_simulation_metrics`: la columna Success vale 100 % en las cuatro filas
- **Ubicación:** `results.tex:139–144`.
- **Corrección sugerida:** como alternativa menos invasiva que M-17 (fusionar la tabla con `tab:fsm_comparison`), quitar
  solo la columna Success (el SR ya está en `tab:fsm_comparison`) y añadir "All four suites: 100% mission-level success
  (Table~\ref{tab:fsm_comparison})." al caption. La tabla se queda, porque es la "consolidated table" que piden R2-01 y
  R3b-01 ("refer to consolidated tables instead of restating parameters"), y la columna Pitch solo está en ella.
- **Coincide parcialmente con Sebas M-17.** La propuesta concreta es **NUEVA**.

### R-19 · BAJA · Batería de perturbación extra: dos frases finales que reafirman lo ya dicho
- **Ubicación:** `results.tex:182`: "Read together with Figure~\ref{fig:failure_by_family}, this indicates that Rugged
  Terrain's elevated tipover/crash count is concentrated in the trials discarded before completion rather than reflected
  as progressive attitude degradation in the trials that do complete, a distinction relevant to how this suite's
  robustness should be characterized (Section~\ref{ssec:Limitations})." (45 palabras). Y `results.tex:184`: "This is
  precisely the pipeline-level (not sensor-level-only) evidence the combined-perturbation evaluation is designed to
  surface: the failure mode originates in the camera-illumination stage but only becomes visible as a robustness concern
  once its consequence for task completion is measured, not from the sensor-level distortion metric alone." (46 palabras)
- **Cómo lo verifiqué:** `:182` repite la primera frase del mismo párrafo y el caption (b). `:184` reformula dos veces la
  idea "sensor → tarea" que la frase anterior ya cuenta con el caso concreto. Las dos son de R3-04 (`6a79328`) y no tocan
  ninguna petición de la ronda 2.
- **Corrección sugerida:** `:182`, "Rugged Terrain's tipovers and crashes are therefore confined to discarded trials,
  not reflected as progressive attitude degradation (Section~\ref{ssec:Limitations})." (≈ 20). `:184`, "This is the
  pipeline-level evidence the combined-perturbation evaluation is designed to surface." (≈ 11). **Ahorro ≈ 60 palabras.**
- **NUEVO.**

### R-20 · BAJA · Topografía variable: un arranque de párrafo de 50 palabras de relleno
- **Ubicación:** `results.tex:320`: "To quantify the computational efficiency and temporal determinism of the proposed
  bio-inspired control architecture under stochastic conditions, the neural response latency ($T_{\text{response}}$) and
  the Empirical Cumulative Distribution Function (ECDF) of the mechanical state-switching delay ($T_{\text{switch}}$) were
  analyzed across 15 randomized trials for both experimental terrains, the latter illustrated in Figure~\ref{fig:decision_delay}."
- **Corrección sugerida:** "\revblue{$T_{\text{response}}$ and the ECDF of $T_{\text{switch}}$
  (Figure~\ref{fig:decision_delay}) were analyzed over the same 15 trials per terrain.}" Los 15 ensayos y la definición
  de ECDF ya están en el subcaption (b). **Ahorro ≈ 25 palabras.** Este párrafo también tiene hallazgos de datos (S-37
  ciclo 3.3 kHz, A-6, C-75 §2 sobre los niveles de ruido), así que conviene editarlo todo de una vez.
- **NUEVO.**

### R-21 · BAJA · Caption de `fig:transition_phases` (≈ 150 palabras): repite la justificación de la prosa `:410`
- **Ubicación:** caption `results.tex:416–428`, "rather than as a single value per direction, since all four readings of a given
  mode agree closely, itself the empirical evidence that both transition directions are equally stable", frente a la
  prosa `:410`, "Both directions of each mode pair converge to statistically indistinguishable support-polygon geometries
  and $TR$ values, so Figure~\ref{fig:transition_phases} shows each undirected pair … once". También el cierre de
  `:444–450` ("this instantaneous reading does not describe the full $N_{total}=979$-sample window …", 39 palabras)
  matiza algo que el caption ya da como rango por modo.
- **Corrección sugerida:** en el caption, dejar "$TR$ and $SM$ are reported as a min--max range across all instances of
  each mode in the six directed transitions (e.g. …)." y quitar la cláusula "rather than … equally stable". **Ahorro
  ≈ 25 palabras.** El `$N_{total}=979$` del caption se queda (R2b-05).
- **NUEVO.**

### R-22 · (aviso sobre propuestas de otros) Hay recortes de tablas que chocan con el texto literal de los revisores
- **Sam S-31** (pasar `tab:mode_steady_state_energy` a una frase): **en contra.** R3b-05 dice literalmente "Supplement
  key background information in captions for the **power-consumption table** … including battery specification". El
  revisor nombra esa tabla y su caption, y el caption ya lleva la especificación de batería. Si se quita la tabla, la
  respuesta a R3b-05 se queda sin objeto.
- **Sebas B-6** (pasar `table:Locom_MLP` a una frase): **en contra** para esa tabla. R3b-01 pide "refer to consolidated
  tables instead of restating parameters", así que una tabla de parámetros es justo lo que el revisor prefiere.
  `table:DIR_BINARY` no es de parámetros: ahí el recorte es neutral.

### R-23 · BAJA · Energía: la descripción de la medida está en el caption de la figura y en el de la tabla
- **Ubicación:** caption de `fig:MorphologicalEnergy` `:986` ("(current sampled at $\approx 5$\,Hz by the onboard INA
  sensor; fixed nominal voltage of the NiMH battery, Table~\ref{table:HardwareParams})") y caption de
  `tab:mode_steady_state_energy` `:997` (la misma información con más detalle).
- **Corrección sugerida:** el caption de la tabla se queda entero (R3b-05, ver R-22). En el de la figura se puede dejar
  "$|I_{\text{current}}|\times 7.2$\,V (measurement details in Table~\ref{tab:mode_steady_state_energy})". **Ahorro ≈ 12
  palabras.** Prioridad mínima: la figura también es un dato energético y se puede leer sola.
- **NUEVO.**

### R-24 · BAJA · Caption y prosa de `fig:FourPanelLatencies`
- `results.tex:1021` y `:1025`: la prosa recorre los paneles A–D, pero de forma cualitativa (las μ solo están en el
  caption). Así que la redundancia es menor de lo que parece. Lo único recortable es la frase del layout de cuatro
  paneles (ya incluida en R-08).
- **Coincide con Sam S-32**, con menos ahorro del que él estima.

### Revisado sin hallazgo (para que conste que se miró)
- **Abstract, Highlights y Results:** las cifras 25/33 %, 100/0 % y 85/45 % se repiten por diseño (R2b-06 pide
  alinearlos). No es redundancia.
- **Las tres propiedades diferenciadoras (Intro `:34`, Conclusiones `:12`):** el eco entre secciones es esperable. El
  problema de redacción ("energy-aware") ya lo tienen S-38/M-19.
- **Leyendas de hiperparámetros de Methodology (`:131–133`, `:283–286`):** ya condensadas por R3b-01/C-64, sin
  duplicados.
- **Variantes de la ablación en Methodology `:198` y en el caption `:211`:** el caption es obligatorio (R3b-02) y
  Methodology las define. Ninguna de las dos sobra.
- **Inspección, "no map / no spatial memory" (methodology `:62`, results `:533`):** C-41 ya dejó en results solo un
  puntero breve. Nada más que recortar.
- **Closing (`closing.tex`):** solo bibliografía y comentarios de plantilla.

---

## 2. Recuento

| Prioridad | IDs | Nº |
|---|---|---|
| Alta | — | 0 |
| Media | R-01, R-08, R-17 | 3 |
| Baja | R-02–R-07, R-09–R-16, R-18–R-21, R-23, R-24 | 20 |
| Aviso, sin recorte | R-12, R-22 | (incluidos arriba como baja/aviso) |

Coinciden con Sam/Sebas: R-01 (S-28), R-02 (S-27/M-16), R-03 (parcial M-14), R-04 (M-14), R-05 (S-29), R-08 (S-26),
R-11 (B-5), R-15 (B-4), R-17 (S-30), R-18 (parcial M-17), R-24 (S-32). NUEVOS: R-06, R-07, R-09, R-10, R-12 (como
redundancia), R-13, R-14 (la repetición), R-16, R-19, R-20, R-21, R-22 (aviso en contra de S-31/B-6), R-23.

Ahorro estimado si se aplican R-01–R-11, R-13, R-14, R-16 y R-19–R-21 (todo de bajo riesgo): **≈ 480 palabras**.
R-17 sumaría ≈ 250 más.

## 3. Límites
- **No verifiqué con datos crudos** ninguna cifra (no es mi categoría). Mis comprobaciones son de texto contra texto,
  conteos de palabras y `git log -S`. La coincidencia fila a fila de R-05 la hice entre las dos tablas del fuente, no
  contra los `trial_summary.json`.
- **R-08:** no pude confirmar con datos que `:798` y `:1025` sean los mismos 15 ensayos. Si los paneles A/B de
  `fig:FourPanelLatencies` salen de `Imu_pitch_test_t01` (S-04), el problema es de atribución. Lo de la batería de
  terreno/FSM (R-07) **requiere verificación con datos no versionados** (`R2-02-fsm-baseline/data/`) si alguien quiere
  confirmar algo más que el texto.
- **No miré las figuras (PNG).** Las redundancias entre figuras casi idénticas de simulación y físico, y lo que repiten
  las leyendas, quedan sin revisar.
- **Los conteos de palabras son aproximados** (split sobre el fuente sin macros). No equivalen al `wc -w` de
  `check_word_growth.sh`, que cuenta también el markup.
- Leí `final_audit_r2_consolidated_2026-11-03.md` solo por encima (cabecera), después de escribir mis hallazgos. No lo
  he cruzado entero.
