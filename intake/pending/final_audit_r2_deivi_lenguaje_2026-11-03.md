# Auditoría final ronda 2: parte Deivi (C-77), auditor de lenguaje (prefijo L-), 2026-11-03

Enfoque: 1.4 (ortografía y convenciones), 1.5 (calcos del español), 1.6 (texto de las últimas 48 h,
sobre todo C-76). Leí entero `preamble.tex` (abstract y highlights), `introduction.tex`, `methodology.tex`,
`results.tex`, `conclusions.tex` y `closing.tex`, en ese orden y antes de abrir las auditorías de Sam
(`S-xx`) y Sebas (`A-/M-/B-/N-xx`). Después crucé cada hallazgo con ellas.

Método para 1.6: `git log --since=48.hours` → C-76 (`1b708f2`), C-74 (`a20680a`), C-66 (`e6a6b0e`),
R2b-03 (`af653fd`). Revisé los 63 reemplazos de C-76 uno por uno con
`git show 1b708f2 --word-diff=plain -- sections/`, además de `patches/c-76-remove-em-dashes.tex`. Para
"compila limpio" leí el log ya existente `build/tex-src/elsarticle-template-num-names.log` (1-nov 20:14,
posterior a C-76; su `.tex` es byte a byte igual a `source/main_monolithic.tex`). No compilé nada.

Resumen: **0 altas, 19 medias, 25 bajas** (44 en total; 30 NUEVOS, 14 que coinciden con Sam o Sebas).

---

## 1.1 Inconsistencias de datos (fuera de mi enfoque; solo lo que vi de paso)

### L-01 · MEDIA · NUEVO · `results.tex:986` y `:997`: el "onboard INA sensor" no figura en `table:HardwareParams`
- **Cita:** "current sampled at $\approx 5$\,Hz by the onboard INA sensor" (caption de
  `fig:MorphologicalEnergy` y de `tab:mode_steady_state_energy`).
- **Verificación:** `methodology.tex:473`, fila Sensors: "MPU-6050 IMU, HMC5883L magnetometer, LDROBOT
  STL-19P LiDAR, Logitech C270 camera". No hay sensor de corriente. `grep INA sections/*.tex` solo da
  esas dos líneas de results. Además "INA" nunca se expande ni lleva modelo.
- **Corrección sugerida:** añadir el sensor de corriente a la fila Sensors con su modelo (p. ej.
  "INA219 current sensor", según el hardware real) y usar ese nombre en los dos captions.

### L-02 · MEDIA · coincide con Sam S-02 / Sebas A-4 · `results.tex:701`: "~47k-parameter" y "30.4% of the board's 4 MB partition"
- **Verificación:** 135·150+150 + 150·80+80 + 80·2+2 = 32 642 parámetros. 397 829 / 4 194 304 = 9.5 %,
  y 397 829 / 1 310 720 (1.25 MiB) = 30.35 %. Lo confirmo con un cálculo propio. El SD de 2.67 µs
  frente a una media de 8.81 ms parece una errata de unidades pero no lo es:
  `experiments/R2-04-mlp-onboard-compute/output/onboard_compute_results.txt` dice "mean=8814.009 us,
  sd=2.672 us". **Ese dato está bien.**

### L-03 · MEDIA · coincide con Sam S-16 / Sebas M-3 · λ con dos definiciones (`results.tex:476` vs `:1052`)
Lo encontré por mi cuenta como problema de notación: un revisor leerá que λ "was excluded from the reported
results" y la verá como columna de `tab:fsm_comparison`.

### L-04 · MEDIA · coincide con Sam S-18 · `methodology.tex:288` vs `:429`: $Ar$ derivado como % de **ancho** y tabulado como "bounding-box **area** units"

Fuera de esto, 1.1 no lo revisé a fondo (es el enfoque de otros auditores).

## 1.2 Redundancia y 1.3 Candidatos a acortar
No eran mi enfoque y no los recorrí de forma sistemática. Lo único que anoto viene de C-66 (ver L-35):
dejó párrafos de resultados sin resultado.

---

## 1.4 Ortografía y convenciones académicas

### L-05 · MEDIA · NUEVO · `results.tex:504`: comillas rectas de ASCII
- **Cita:** `this is the only sense in which "success rate" is used anywhere in this paper`
- **Problema:** en LaTeX, `"` se imprime como dos comillas de cierre (”success rate”). Es la única
  aparición en todo `sections/` (`grep -n '"' sections/*.tex`, sin contar preamble).
- **Corrección:** ``` ``success rate'' ```. El contenido de la frase lo cuestiona Sam S-07, así que
  puede que la frase entera cambie.

### L-06 · MEDIA · NUEVO · `methodology.tex:417`: la lista de mecanismos queda colgada de "five discrete severity levels"
- **Cita:** "…the Combined Perturbation Level $\eta \in \{0,1,2,3,4\}$, applied jointly across five
  discrete severity levels: IMU drift, LiDAR range noise, and camera illumination distortion."
- **Problema:** tras los dos puntos vienen **tres** elementos, que se leen como si fueran los cinco
  niveles. La enumeración es de los "three sensor-level perturbation mechanisms" del principio de la
  frase. Es justo la definición que sostiene la cautela de perturbación conjunta de R2b-02.
- **Corrección:** "…three sensor-level perturbation mechanisms (IMU drift, LiDAR range noise, and
  camera illumination distortion) were combined into a single sweep index, the Combined Perturbation
  Level $\eta \in \{0,\dots,4\}$, applied jointly across five discrete severity levels."

### L-07 · MEDIA · NUEVO · Captions de tabla agramaticales y mayúsculas incoherentes (`methodology.tex:248`, `:402`, `:176`, `:113`)
- **Citas:** "Arbitration of locomotion modes Networks parameters." / "Arbitration of locomotion modes
  with MLP Network parameters." / "Basal Ganglia Network parameters." / "LiDAR network hyperparameters."
- **Corrección:** "Locomotion-mode arbitration network parameters." / "Parameters of the MLP-driven
  gait-decision network." / "Basal ganglia network parameters." Usar el mismo patrón (sentence case)
  en los cuatro.

### L-08 · MEDIA · NUEVO · `fig:variable_topo_metrics` (`results.tex:296`–313): rotulación de paneles contradictoria
- **Problema:** las subfiguras se numeran automáticamente (a)–(c), pero el caption general dice
  "(A)~tipover risk … (B)~ECDF … (C)~Roll RMS". Dentro del subcaption (b) los subpaneles internos
  también se llaman "(A)~Rugged Terrain, (B)~Inclined Slope", y el texto (`:320`) cita
  "Figure~\ref{fig:decision_delay}A", que se imprime como "Figure 23bA". En el subcaption (a) se dice
  "upper panel / lower panel". Son tres convenciones en una misma figura. `fig:FourPanelLatencies` usa
  además "Panel~A–D".
- **Corrección:** en el caption general, (a)–(c) en minúscula, igual que las subfiguras. Para los
  subpaneles internos, "top/bottom" o "left/right", y en el texto "Figure~\ref{fig:decision_delay}
  (left panel)".

### L-09 · MEDIA · NUEVO · `results.tex:328`, `:444`, `:317`: "Normalized Stability Margin ($SM$)" para una magnitud en metros
- **Problema:** `tab:crawl_stability` distingue $SM$ (m) de $SM_{\mathrm{norm}}$ (adimensional), pero
  la prosa llama "Normalized Stability Margin ($SM$)" a la que va en metros. Por eso `:444` dice "the
  Normalized Stability Margin reached … ($SM = 0.050$ m, $SM_{norm} = 1.000$)".
- **Corrección:** "stability margin $SM$ (m) and its normalized form $SM_{\mathrm{norm}} = SM/r_{in}$",
  y $TR = 1 - SM_{\mathrm{norm}}$.

### L-10 · MEDIA · NUEVO · Siglas en el abstract y los highlights sin definir, y STR nunca expandida
- `preamble.tex:85` y `:97`: "its STN/STR layers", "Ablating lateral inhibition or STN/STR". El
  abstract debe sostenerse solo. Además, en el cuerpo "STR" no se define como sigla en ninguna parte:
  `methodology.tex:172` dice "striatum" en la lista del *where*, sin "(STR)".
- **Corrección:** abstract: "removing the circuit's lateral inhibition or its subthalamic/striatal
  (STN/STR) layers". En `methodology.tex:153`, añadir "the striatum (STR)" a la lista de núcleos.

### L-11 · MEDIA · NUEVO · Tabla 1 (`table:action_selection_comparison`) desborda el margen 37.6 pt
- **Verificación:** log, "Overfull \hbox (37.6139pt too wide) in paragraph at lines 133--143" (línea
  133 del monolito = `\begin{tabular}{|p{2.1cm}|…|p{2.0cm}|}`). Hay tres overfull más en sus
  cabeceras: "Representative" 18 pt, "Interpretability" 9 pt, "Biological" 9 pt. Las columnas suman
  12.4 cm más 12 `\tabcolsep`, más que `\textwidth`. No es un tema de "tamaño de figura" (sección 3
  del brief): es una tabla nuestra que se sale de la caja.
- **Corrección:** `tabularx` con columnas X, o reducir `\tabcolsep`. Romper las cabeceras con
  `\newline`.

### L-12 · MEDIA · coincide con Sebas B-8 · GPe/GPi en prosa vs Gpe/Gpi en ecuaciones, tablas y en la misma frase
`methodology.tex:198` mezcla ambas en una sola frase: "(Gpe$\rightarrow$STN, STN$\rightarrow$Gpi)" y
"STN/GPi/GPe/STR". `:284` dice "GPe\_R" donde la ecuación dice $Gpe_R$. Mismo caso: $X_n$ en la prosa
frente a $z_n$ en las ecuaciones (`:204` "units $X_5$ and $X_6$" junto a `eq:Z_5`).

### L-13 · MEDIA · coincide con Sam S-33 / Sebas M-18 · Nombres de autor portada vs CRediT
Confirmado.

### L-14 · MEDIA · coincide con Sebas M-21 · "stimuli of different natures" (ver 1.5)

### L-15 · BAJA · NUEVO · Siglas definidas más de una vez o usadas antes de definirse
- **CPG** se define tres veces: `introduction.tex:10` "(CPGs)", la tabla en `:23` "(CPG)" y `:32`
  "central pattern generators (CPGs)".
- **ECDF**, dos: `results.tex:303` "Empirical Cumulative Distribution Functions (ECDF)" y `:320`
  "the Empirical Cumulative Distribution Function (ECDF)".
- **MPC** se usa en `introduction.tex:8` ("offline motion libraries and MPC") antes de definirse en la
  tabla (`:21`).
- **IMU** no se expande en ninguna parte (aparece 92 veces).
- **SR** aparece en la cabecera de `tab:fsm_comparison` (`:484`) antes de definirse en `:533`.
- **CoM** (`:359`, `:394`) nunca se define como sigla.
- **GPR** no se expande. Coincide con Sebas B-9, que además cubre MLP (definido tres veces) y BG.
- **Corrección:** cada sigla definida una vez, en su primer uso del cuerpo.

### L-16 · BAJA · NUEVO · Títulos de (sub)sección: mayúsculas incoherentes y plurales calcados
- `results.tex:659`: "Evaluation of the MLP-based terrain classifier" va en sentence case. Todas las
  demás van en Title Case → "Evaluation of the MLP-Based Terrain Classifier".
- `results.tex:56` "Single-Stimuli", `:868` "Multi-Stimuli", `:967` caption "Multi-Stimuli
  Scenarios" → "Single-Stimulus", "Multi-Stimulus". En un compuesto adjetival, el sustantivo va en
  singular.
- `results.tex:119` "Multi-Modal" vs "multimodal" en keywords, abstract y conclusiones →
  "Multimodal".

### L-17 · BAJA · NUEVO · Nombres de las variantes de ablación con y sin guion
`methodology.tex:198` y `results.tex:1052` dicen "\emph{threshold-only}". `results.tex` (8 veces)
dice "\emph{threshold only}". Hay que unificar. Sam S-36 ya cubre "full" vs "intact circuit".

### L-18 · BAJA · NUEVO · Guion en compuestos adjetivales
- "basal-ganglia inspired architecture" (`methodology.tex:132`) y "basal-ganglia inspired arbitration
  network" (`results.tex:1030`) → "basal-ganglia-inspired", como en el resto del texto.
- "continuously-converging" (`results.tex:215`): ya en Sebas B-12.
- "static-stable by construction" (`results.tex:334`) → "statically stable by construction".
- "tipover" (8 veces) frente a "tip-over events" (`:400`) → "tipover".

### L-19 · BAJA · NUEVO · Caracteres Unicode y tipografía mezclada en la fuente
Compila (el log no da errores de carácter), pero la fuente queda incoherente:
- `results.tex:223`: "three‐section" lleva **U+2010 HYPHEN**, no un guion ASCII. Si alguna vez se
  copia a otro motor, es candidato a romper. → "three-section".
- Apóstrofo curvo ’ en `methodology.tex:25, 27, 104, 202, 373` y `results.tex:225`. El resto usa `'`.
- "°" literal en `introduction.tex:8` ("180°") y `methodology.tex:497` ("20°"). El resto usa
  `$^\circ$`.
- "·" literal en `methodology.tex:469` ("kg·cm").
- Las en dash Unicode "–" ya las cubre Sebas B-10. Añado que `methodology.tex:131` dice
  "($L_0$–$L_4$)" para las neuronas **direccionales**, cuando `:148` dice $L_0$--$L_3$ y $L_4$ es el
  acumulador.

### L-20 · BAJA · NUEVO · Referencias cruzadas en minúscula, "Eqs." y autorreferencias vagas
- "subsection~\ref{ssec:Platform_Design}" (`methodology.tex:446`) y "subsection~\ref{ssec:Construction}"
  (`results.tex:584`) → "Section~\ref{…}", como en el resto.
- "Eqs.~\eqref" (`methodology.tex:198`): el resto del texto dice "Equations~". Hay que unificar.
- `methodology.tex:439`: "of Section~\ref{sec:methodology}'s Basal Ganglia Module" (dentro de la
  propia Methodology) → "of Section~\ref{sssec:Basal_Ganglia_Module}".
- "results are reported in Section~\ref{sec:results}" en `methodology.tex:62, 198, 434, 439`, y
  "(Section~\ref{sec:results})" en `conclusions.tex:12, 18`: apuntan a la sección entera de 60 páginas.
  Hay que apuntar a la subsubsección (Sam S-37 lo señala solo en `results.tex:1052`).

### L-21 · BAJA · NUEVO · Notación de tablas y celdas
- `tab:consolidated_simulation_metrics` (`results.tex:139`–144): la cabecera es "Success (\%)" y las
  celdas dicen "100.0\%". El signo de porcentaje sale dos veces. `tab:fsm_comparison` lo hace bien
  ("SR (\%)", "100.0").
- `results.tex:480`: el caption dice "undefined ($-$)" (un signo menos) pero la celda tiene `--` (en
  dash). → "undefined (--)".
- `methodology.tex:264`: $\omega_{Gpe \rightarrow X_1}$ está en `table:Locom_NN` pero no aparece en
  ninguna ecuación ni en el texto de notación (`:283`–286).
- `methodology.tex:283`: "$\tau$ … common time constant of the locomotion decision neurons
  (Equations~\eqref{eq:Z_5}--\eqref{eq:Z_6})". En realidad $\tau$ entra en todas las ecuaciones $z_n$,
  también en las del gait-decision.
- `methodology.tex:288`: $Z = 31$ cm reutiliza la letra de las neuronas del anillo $Z_j$ y del eje $Z$
  → $d_{stop}$.
- $Ar$ va en `\text{Ar}` en `eq:Z_17` y en cursiva ($Ar$) en tabla y prosa.

### L-22 · BAJA · NUEVO · Precisión de los p-valores
`results.tex:211`: "$p=0.0029$" (4 decimales) junto a "$p=0.017$", "$p=0.478$", "$p<0.005$" y
"$p=1.000$". → "$p=0.003$".

### L-23 · BAJA · NUEVO · Arquitecturas del MLP: notación ambigua (`results.tex:666`)
- **Cita:** "compared the proposed 150–80 configuration against simpler (50, 100) and deeper (200, 100,
  50) topologies … shallower (50: F1 = 0.747; 100: F1 = 0.766) and deeper (200-100-50: F1 = 0.766)".
- **Problema:** "(50, 100)" se lee como **una** red de dos capas, pero luego se tratan como dos redes de
  una capa. La notación cambia entre "150–80" (en dash) y "200-100-50" (guion). Y "topologies" es un
  calco por "architectures".
- **Corrección:** "against two single-hidden-layer networks (50 and 100 units) and a deeper
  200–100–50 network".

### L-24 · BAJA · NUEVO · `results.tex:73` (efecto de C-66): dos paréntesis seguidos y overfull de 31.9 pt
- **Cita:** "…across the full combined-perturbation sweep (Section~\ref{ssec:NoiseRobustnessEval}) (see
  Figure~\ref{fig:noise_robustness_grid} for the per-level … trends)".
- **Verificación:** C-66 (`e6a6b0e`) borró la cláusula que había entre los dos paréntesis. El log da
  "Overfull \hbox (31.93489pt too wide)" en la línea 759 del monolito, que es este párrafo.
- **Corrección:** "…sweep (Section~\ref{…}; per-level trends in Figure~\ref{…})".

### L-25 · BAJA · NUEVO · Resto de cajas sobrellenas (> 10 pt) en el log
En el monolito, las líneas 1162 (`results.tex:476`, 14.8 pt, junto a "$\lambda$"), 1700 (`:1014`,
14.8 pt), 570 (`methodology.tex:417`, 12.5 pt), 526 (`methodology.tex:373`, 17.2 pt), 1308
(`results.tex:622`, 11.0 pt), 870 (`results.tex:184`, 10.9 pt), 126/157 (intro y methodology,
13.4/12.9 pt) y el bloque de autores (11.3 pt). Las de 398–409 son de la `.bbl`. No hay errores ni
referencias indefinidas. El único warning de paquete es el de hyperref "Token not allowed in a PDF
string" ×20 en `\end{frontmatter}`, que es inocuo.

### L-26 · BAJA · coincide con Sam S-37 / Sebas B-11, B-12 · "artefact", "summarises", "1.2cm", "Figures~" con una sola referencia, el doble espacio de la Intro
Confirmados. Mi barrido con grep no encontró más británicos (`-ise/-our/-isation`).

### L-27 · BAJA · NUEVO · Nombres incoherentes del robot y de familias de plataformas
- "real robot" (6 veces), "physical robot" (10), "physical platform", "real-world" en captions: conviene
  fijar uno ("physical robot"). Sebas M-20 cubre los nombres de los modos, no los del robot.
- "ANYmal-on-wheels family" (`introduction.tex:8`) vs "ANYmal-wheels" (misma línea, al final).
- "neuronal" (4 veces) vs "neural" (cientos): usar "neural".

---

## 1.5 Calcos del español e inglés no idiomático

### L-28 · MEDIA · coincide con Sebas M-21 · "stimuli of different/diverse nature(s)"
`results.tex:93, 100, 107, 611, 618, 653` y `conclusions.tex:4`. Es *de diferente naturaleza*.
→ "multiple stimuli of different types".

### L-29 · BAJA · NUEVO · Preposiciones calcadas de "en"
- "Trajectory in an unstable terrain" (`results.tex:254`), "in a steeply sloping terrain" (`:281`),
  "In both terrains" (`:317`), "Trajectory in a terrain with elevation in real test" (`:758`) → "on …
  terrain". "Terrain" en este sentido es incontable: "on unstable terrain", "on sloping terrain".
- "during transport on an unstable terrain" (`:275`, *desplazamiento*) → "during locomotion over
  uneven terrain".
- "an obstacle was placed close on the robot's right side" (`:95`) → "close to the robot, on its right".

### L-30 · BAJA · NUEVO · Artículo omitido en "remove(s) basal-ganglia mechanism itself"
`results.tex:194` ("The two ablations that remove basal-ganglia mechanism itself"), `:211` (caption,
igual) y `:215` ("unaffected by removing basal-ganglia mechanism") → "the basal-ganglia mechanism
itself" / "removing basal-ganglia mechanisms".

### L-31 · BAJA · NUEVO · Calcos léxicos sueltos (no repetidos en Sam S-39 ni en Sebas B-14)
| Ubicación | Texto | Origen | Sugerencia |
|---|---|---|---|
| `introduction.tex:4` | "civil constructions" | *construcciones civiles* | "civil structures" |
| `introduction.tex:15` (caption Tabla 1) | "Horizontal comparison" | *comparación horizontal* | "Side-by-side comparison" |
| `methodology.tex:43` | "large-scale works" | *obras* | "large-scale civil works" / "construction sites" (si se mantiene la frase) |
| `results.tex:111` | "At the initial moment" | *en el momento inicial* | "Initially" / "At $t = 0$" |
| `results.tex:940` | "exciting the transversal axis" | *eje transversal* | "the lateral (roll) axis" |
| `results.tex:818` | "non-structured terrain conditions" | *no estructurado* | "unstructured" |
| `results.tex:1050` | "real, non-controlled conditions" | *no controladas* | "real, uncontrolled conditions" |
| `conclusions.tex:16` | "and, conditionally on the scenario, camera illumination distortion" | *condicionado al escenario* | "and, depending on the scenario, …" |
| `results.tex:328` | "This subsubsection quantifies" | metatexto | "This section quantifies" / "Below, we quantify" |
| `results.tex:522` | "the team that ran the FSM terrain trials identified" | registro informal, expone el proceso interno | "three configuration differences were identified between…" |
| `methodology.tex:290` | "to model higher priority urgency" | — | "to give avoidance higher priority" |
| `methodology.tex:216` | "defined in Table~\ref{table:Locom_NN}'s notation below" | — | "defined below Table~\ref{…}" |
| `methodology.tex:373` | "used as a notion of robot stagnation" | *como noción de* | "which flags robot stagnation" |

### L-32 · BAJA · coincide con Sam S-39 y Sebas B-14 · "around second 86", "before second 46", "Complementarily", "three main topologies", "It is important to emphasize/highlight that", "decisions can be taken", "emulating the embedded knowledge…", "tank neurons", "This distinction…"
Confirmados por lectura propia; no los repito.

### L-33 · BAJA · NUEVO · Formulación del caveat de equidad (R2b-03): "make … not comparable under strictly identical conditions"
- **Ubicación:** `methodology.tex:439`, `results.tex:480`, `:509`, `:518`, `:522`, `:576` (seis veces;
  Sam S-28 cubre la repetición).
- **Problema:** la expresión es ilógica en inglés. Las diferencias no hacen las métricas "no comparables
  en condiciones idénticas": hacen que **no se midieran** en condiciones idénticas.
- **Corrección (sin cambiar el alcance de la cautela):** "…make $T_{switch}$ and $T_{response}$ not
  comparable, since the two controllers were not run under strictly identical terrain-transition
  settings".

---

## 1.6 Texto tocado en las últimas 48 h

### Lo que verifiqué y quedó bien
- **Cautelas de revisores tras C-76:** R2b-02 en `results.tex:73` (paréntesis, mismas palabras),
  `methodology.tex:434` ("…simultaneously: no configuration isolates…"), `results.tex:1050` ("applied
  jointly: no configuration isolates…"), `results.tex:1052` (punto y coma; mantiene "not evidence that
  conflict efficiency is unaffected") y `results.tex:186` ("but, in the code that generated this
  dataset, does not reach the basal-ganglia arbitration…"). Las cinco conservan la fuerza original, y
  las comas de `:186` no alteran el sentido.
- No quedan em dash (`---`/`—`) en la prosa (`grep`). Las 46 en dash se respetan.
- Highlights (`preamble.tex:95`–99): 80–84 caracteres, por debajo del límite de 85 de Elsevier.

### L-34 · MEDIA · coincide con Sam S-40(23) / Sebas M-22 · `results.tex:176`: dos dos puntos en una frase (C-76)
"…under camera illumination distortion: a failed attempt (timeout) and its successful retry at the same
severity level: the failed attempt's…". Confirmado.

### L-35 · MEDIA · NUEVO · C-66 dejó dos párrafos de resultados sin resultado (`results.tex:82`, `:91`)
- **Citas:** "The defensive repulsion properties of the architecture were re-evaluated under the
  combined-perturbation sweep (Figure~\ref{fig:noise_robustness_grid})." / "Smooth capsule geometries
  for simulated obstacles prevent localized torque spikes during contact. Neural firing variance stays
  at a low baseline…".
- **Verificación:** `git show e6a6b0e --word-diff`. Se quitó "with every retained trial across all five
  severity levels resolving the threat successfully" y la frase "Every retained trial … completed
  evasion successfully". La consolidación en `:57` dice que se retuvieron tres ensayos exitosos por
  nivel. Los párrafos de Aversive y Obstacle quedan diciendo solo "se reevaluó", sin cómo salió, y un
  revisor puede leerlo como un resultado omitido.
- **Corrección:** cerrar la frase de `:82` con "(outcome per level in Figure~\ref{…}; retained-trial
  rule in the paragraph above)" o similar. No hay que restituir la redundancia.

### L-36 · MEDIA · coincide con Sam S-40(56) / Sebas M-23 · `results.tex:622`: "uninhibited by $X_{15}$, the no-motor-action state" (C-76)
Confirmado: la aposición se pega a $X_{15}$.

### L-37 · MEDIA · coincide con Sam S-40(09) · `introduction.tex:32`: "…distributed across the oscillator network, a property advantageous for diagnosing…" (C-76)
Confirmado. Además repite "property" dos veces en seis palabras ("an emergent property … a property
advantageous").

### L-38 · BAJA · NUEVO · `results.tex:426` (caption `fig:transition_phases`, C-76): "itself" colgante
- **Cita:** "…since all four readings of a given mode agree closely, itself the empirical evidence that
  both transition directions are equally stable."
- **Problema:** antes era un inciso entre rayas. Con coma, "itself" no tiene antecedente nominal (se
  refiere a toda la cláusula "that they agree").
- **Corrección:** "…agree closely; this agreement is itself the empirical evidence that…".

### L-39 · BAJA · NUEVO · `results.tex:509` (caption `fig:attempts_vs_noise_level`, C-76): coma de empalme y "that took" colgante
- **Cita:** "(not a success-rate metric: every mission in this dataset eventually succeeds, see
  Table~\ref{tab:fsm_comparison}; this counts how many attempts, including retries after a timeout,
  that took)". En la misma caption: "across all five evaluated noise levels, not a subset, so the
  dashed Neural line…".
- **Corrección:** "(not a success-rate metric: every mission eventually succeeds, Table~\ref{…}; it
  counts the attempts, including retries after a timeout, each mission needed)". Y "at all five noise
  levels, so the dashed Neural line…" (el "not a subset" sobra).

### L-40 · BAJA · NUEVO · Falta coma tras paréntesis que antes cerraba una raya (C-76)
- `results.tex:459`: "within those two datasets (the four scenario suites and the variable-topography
  battery of 15 trials per terrain) the mean Roll RMS stays…" → coma tras el paréntesis.
- `results.tex:713`: "a region with minimal irregularities (less than 1.2cm) which it overcomes…" → "(less
  than 1.2~cm), which it overcomes". El espacio ya está en Sam S-37; la coma es nueva.

### L-41 · BAJA · coincide con Sebas B-15 · `results.tex:310` "zones, deliberately not drawn on the Roll RMS axis" y `results.tex:587` "(approach, a, appetitive; evasion, b, obstacle; …)" (C-76)
Confirmados.

### L-42 · BAJA · coincide con Sam S-40(51, 52) · `results.tex:567` "…would exhibit, the mechanism underlying…" y `:569` "…once the obstacle clears, the system's re-acquisition-like behavior" (C-76)
Confirmados.

### L-43 · BAJA · NUEVO · `results.tex:1025` (C-76): una aposición presenta una hipótesis como hecho
- **Cita:** "settles at a markedly longer latency, a deliberate stability feature that filters transient
  high-frequency impact noise…".
- **Problema:** con la raya, era un comentario del autor. Con coma, se lee como descripción establecida
  del sistema, y Sam S-04 / Sebas A-7 cuestionan precisamente esa causa. **Esto lo suaviza el
  lenguaje, pero el contenido depende de S-04.**
- **Corrección:** "…a markedly longer latency, which we attribute to…" o eliminarla si S-04 confirma
  el banco de pitch.

### L-44 · BAJA · NUEVO · `conclusions.tex:18` (C-76): gerundio final
Coincide en el diagnóstico con Sam S-40(01). Añado una alternativa que no fuerza la finalidad: "…aligned
with current standards. Together, these steps would evolve the platform from a functional prototype
into a practical autonomous inspection tool."

---

## Límites
- **No compilé.** "Compila limpio" se basa en el log ya existente de `build/tex-src/` (1-nov 20:14).
  Comprobé que su `.tex` es idéntico a `source/main_monolithic.tex`, pero no si `sections/` cambió
  después. El último commit que toca `sections/` es C-76, anterior al log; no vi commits posteriores a
  `sections/`, aunque no lo verifiqué contra el remoto ni hice `git pull`.
- No revisé el PDF renderizado ni las **figuras** (texto rasterizado, leyendas, ejes). Lo de figuras
  de C-70–C-75 queda para Sam y Sebas.
- No revisé la bibliografía (`references.bib`): formato de citas, mayúsculas de títulos, DOIs.
- 1.1, 1.2 y 1.3 no se recorrieron sistemáticamente. Solo se anota lo que vi de paso (L-01 a L-04,
  L-35). Cualquier cifra de `R3-04-noise-robustness/data` o `R2-02-fsm-baseline/data` (las bandas
  1.65–1.9° / 2.3–5.7°, los 8/4/27 tipovers/crashes/intentos, los N de terreno del FSM) **requiere
  verificación con datos no versionados**. No la toqué.
- En L-01 no sé qué modelo de sensor de corriente lleva el robot. Hay que confirmarlo con el hardware
  o con `PETER_SIMULATION`, que no consulté.
- La detección de calcos es por lectura. Puede haber más casos sueltos en `results.tex` (es de 113 KB),
  sobre todo en los párrafos físicos de las líneas 894–963, que tienen mucha jerga ("hyper-excitation
  wave", "computational ticks").
