# R02-01 — Auditoría Exhaustiva de Métricas y Recursos Visuales (`sections/results.tex`)

**Estado:** DIAGNÓSTICO — ningún archivo de `sections/`, `assets/` o `source/` fue modificado para producir este
informe. Es de solo lectura sobre el estado actual del repositorio.

**Alcance auditado:** `sections/results.tex` (974 líneas, texto completo) y las **~50 figuras/tablas** que
referencia dentro de `assets/`. No cubre `methodology.tex` salvo donde su nomenclatura ($N_0/N_1/N_2$, $X_i$, etc.)
es necesaria para verificar consistencia con las figuras de resultados.

**Método:** lectura íntegra del `.tex` fuente + inspección visual directa (píxel a píxel, no solo por el nombre
de archivo) de 17 figuras representativas de cada familia visual del documento, cruzando cada valor numérico
citado en prosa contra el valor real leído en el eje/leyenda de la figura o tabla que la prosa dice sustentar.

**Convención de referencia usada en este informe:** cada hallazgo tiene un ID `F-NN` (Figura/Fusión) o `M-NN`
(Métrica/Texto) para poder citarlo desde el checklist final y desde una futura fila de `PROGRESS.md` sin
ambigüedad.

---

## 1. Resumen Ejecutivo del Diagnóstico

`results.tex` es una sección extensa (974 líneas, ~50 figuras/tablas) que ya pasó por una ronda de depuración de
redundancia textual (R2-01, 12 ediciones aplicadas por Sebas, ver `PROGRESS.md`). Esa ronda fue efectiva
**reduciendo prosa redundante**, pero no auditó la **consistencia numérica entre el texto y los datos
efectivamente graficados**, ni la **coherencia visual/idiomática de las figuras mismas**. Esta auditoría llena
exactamente ese hueco y encuentra tres clases de problemas, en orden de severidad:

1. **Discrepancias numéricas graves entre texto y figura (severidad CRÍTICA, 3 casos, sección
   §2, hallazgos M-01/M-02/M-03).** En la subsección "Quantitative Performance in Variable Topographies"
   (`sssec:variable_topo_quant`) y en "Quantitative Validation" (simulación de estímulo único/múltiple), el texto
   afirma valores (latencia de decisión "≈47 ms constante", riesgo de volcamiento "μ≈0.42 con escalada monótona a
   0.58", clusters de roll/pitch "perfectamente no solapados" con medias de 1.36°/1.25° vs. 0.43°/6.95°) que **no
   coinciden con los datos trazados en las figuras que el propio texto cita como evidencia** (`FigA`, `FigB`,
   `FigC`, y los cuatro `fig1_*_macro.png`). Esto no es un problema de redacción — es una posible
   desincronización entre el dataset con el que se generaron las figuras y el dataset (o la generalización) con
   el que se redactó el texto. **Requiere verificación contra los logs crudos antes de tocar una sola palabra del
   texto**, porque no sabemos todavía cuál de los dos (texto o figura) es el que está desactualizado.
2. **Error de traducción sistemático en las figuras generadas por script (severidad ALTA, 1 causa raíz,
   ~8-10 figuras afectadas, hallazgo F-01).** Todos los rasters neuronales (`NEU_EST_*`, `NEU_IMU*`) rotulan un
   panel como **"March Decision Module"** — traducción literal incorrecta de "Módulo de Decisión de Marcha"
   (debería ser *"Gait Decision Module"*, coincidiendo con el término que usa el propio `methodology.tex`) — y
   otro panel como **"Auxiliar"** (español, debería ser *"Auxiliary"*). Como es el mismo script de graficación el
   que genera las ~10 figuras, es una única corrección de código que se propaga a todas.
3. **Redundancia visual estructural y oportunidades de fusión de paneles (severidad MEDIA, sección §3).**
   Cuatro pares de familias de figuras (macro-robustez de los 4 escenarios simulados; ECDF+dinámica+RMS de los 4
   escenarios físicos; comparación de clasificadores + costo computacional; timeline IMU sim/real) están
   estructuralmente duplicadas panel por panel y son candidatas naturales a rejillas consolidadas — exactamente
   el patrón que ya se aplicó una vez con éxito para las tablas `tab:consolidated_simulation_metrics` y
   `tab:consolidated_physical_metrics` (ver R2-01, patches 03 y 15), pero que nunca se extendió al arte gráfico
   mismo.
4. **Problemas menores de nomenclatura, ejes sin unidad y contenido de figura no discutido en prosa** (severidad
   BAJA/MEDIA, hallazgos F-04–F-08): un eje Y llamado literalmente "V A L U E" que mezcla dos magnitudes
   físicas distintas sin unidades; un panel completo de una figura (tamaño de modelo en `fig6`) que nunca se
   menciona en el texto; rótulos `Stuck/Flat/Inclined` en las figuras de terreno que no usan la notación
   $N_0/N_1/N_2$ que sí usa el texto.

**Balance volumen vs. síntesis:** el volumen de figuras es alto pero, a diferencia de lo que sugeriría una
primera lectura, **el problema dominante no es "hay demasiadas figuras"** — es que **el texto y las figuras que
ya existen no siempre dicen lo mismo**. Fusionar paneles sin resolver primero las discrepancias numéricas
correría el riesgo de consolidar un error en una figura más grande y más citada. Por eso este informe ordena las
acciones: primero verificar (§2), después fusionar (§3), y solo al final tocar prosa/redacción (§4/§5).

---

## 2. Discrepancias Numéricas Texto↔Figura — Verificar ANTES de editar nada

Estos son los hallazgos de mayor prioridad del informe. Para cada uno: la cita textual exacta, lo que la figura
citada realmente muestra, y por qué importa.

### M-01 — "Decision latency ≈47 ms" no coincide con el panel C de los 4 `fig1_*_macro.png`

- **Ubicación del texto:** `results.tex:77` (párrafo "Appetitive Targeting"): *"decision latency stays clamped
  at ≈47 ms"*; `results.tex:178` (caption de `tab:consolidated_simulation_metrics`): *"Latency remained constant
  at ≈47 ms"*; reforzado indirectamente en `results.tex:973` (Limitations, tras el patch R2-01 #16 de Sebas:
  *"decision latency remained invariant (see the simulation quantitative-validation results above)"*).
- **Lo que muestran las figuras citadas como evidencia** (`fig:appetitive_results` → `fig1_Appetitive_macro.png`,
  panel C "Decision Latency Profile"; y sus tres análogas `fig1_Aversive_macro.png`, `fig1_Obstacle_macro.png`):
  el eje Y está en **milisegundos** y las medias por nivel de ruido van de **~50 ms hasta ~2000 ms**, con
  desviaciones estándar que en varios puntos llegan a **±1500-2000 ms**. Ninguno de los tres escenarios (Appetitive,
  Aversive, Obstacle) muestra un valor "clamped" o "constante" cerca de 47 ms — solo el punto $\sigma=0$ de
  Appetitive está cerca de cero; el resto oscila entre cientos y miles de ms.
- **La única figura que sí es consistente con "~47 ms" es `fig1_Complex_macro.png`** (panel C ronda 30-140 ms) —
  pero el texto no atribuye el "47 ms" a Complex, lo atribuye a Appetitive y lo generaliza a los cuatro
  escenarios vía el caption de la tabla consolidada.
- **Agravante:** `tab:consolidated_simulation_metrics` (la tabla que el caption dice que sustenta "47 ms") **no
  tiene ninguna columna de latencia** — sus columnas son `Suite | Success % | T_sim (s) | Roll (deg) | Pitch
  (deg)`. El número "47 ms" vive únicamente en el caption, sin ninguna celda de la tabla que lo respalde.
- **Por qué importa:** un revisor con acceso a las figuras de alta resolución puede leer directamente "Decision
  Latency (ms)" en el eje Y del panel C y ver valores de miles de ms — una contradicción directa y fácil de
  detectar con la afirmación central de robustez del controlador ("decision latency stays clamped").
- **Hipótesis de causa (sin confirmar):** es posible que "~47 ms" se refiera a una medida distinta — el tiempo de
  cómputo puro de la red neuronal (inferencia), no el tiempo total desde estímulo hasta despacho del comando de
  modo (que sí incluye exploración visual, filtrado, etc., y por tanto sí sería del orden de cientos/miles de
  ms). Si esa es la intención, el texto necesita **desambiguar qué "decision latency" está citando** y dejar de
  citar a `tab:consolidated_simulation_metrics`/Fig. C como su evidencia, porque esas sí miden el pipeline
  completo.

### M-02 — El perfil de "Tipover Risk" (`FigA_Stability_Profile.png`) no muestra la escalada monótona ni los valores medios que describe el texto

- **Ubicación del texto:** `results.tex:276`, párrafo completo de `\paragraph{}`-menos "Tipover Risk": *"In the
  rugged terrain, the platform maintained a bounded risk profile with a mean of $\mu_{TR}\approx 0.42$ ... In the
  inclined slope, a severe monotonic risk escalation was recorded ... reaching a dangerous peak of $TR\approx
  0.58$ ... this produced an immediate drop ... back to a safe baseline of $TR\approx 0.42$."*
- **Lo que muestra la figura** (`fig:stability_profile` → `FigA_Stability_Profile.png`, dos paneles apilados,
  C1=Rugged Terrain arriba, C2=Inclined Slope abajo, confirmado por `FigB_Decision_Delay.png` que rotula
  explícitamente "C1 = Rugged Terrain" / "C2 = Inclined Slope"):
  - **Panel C1 (Rugged Terrain):** línea base plana en **TR ≈ 0.58–0.60** (no 0.42), con un **pico transitorio
    aislado hasta TR≈0.77** entre t=-1.3 s y t=-0.5 s (es decir, *antes* del instante de transición t=0, no
    después), volviendo a ~0.59 tras el cruce por t=0. No hay patrón de "oscilaciones tipo sierra" continuas —
    es un único bache.
  - **Panel C2 (Inclined Slope):** línea **completamente plana en TR≈0.59** en todo el rango mostrado
    (t=-5 s a t=+10 s). No hay ninguna escalada monótona, ningún pico hacia 0.58 (de hecho ya *está* en 0.59 desde
    el inicio de la ventana), y no hay ninguna caída visible en t=0.
- **Por qué importa:** el texto describe explícitamente una dinámica temporal (escalada → pico → caída
  sincronizada con el cambio de modo) que es, según la figura tal como está trazada hoy, la característica
  central que demuestra "eficacia física del controlador bio-inspirado" — y esa dinámica no aparece en absoluto
  en el panel que supuestamente la muestra. Es el hallazgo más citable de toda la subsección de topografías
  variables si un revisor decide verificarlo.
- **Nota de calibración:** no estoy afirmando que el experimento subyacente sea inválido — es muy posible que
  exista una versión anterior de esta figura (con otro rango de eje Y, u otra ventana temporal, o generada con
  datos de una ejecución distinta) que sí coincida con el texto, y que la `FigA_Stability_Profile.png` actual en
  `assets/` sea una regeneración posterior con un dataset o parámetro de recorte distinto. **Antes de reescribir
  el texto, hay que confirmar contra el script/notebook que generó esta figura cuál de las dos versiones (texto o
  PNG actual) refleja el run real.**

### M-03 — El "phase-space" de Roll/Pitch RMS (`FigC_Terrain_Adaptability.png`) muestra clusters solapados con medias muy distintas a las citadas

- **Ubicación del texto:** `results.tex:281`: *"the rugged terrain converged into a high-roll, low-pitch
  operational zone ($\mu_\phi\approx1.36°$, $\mu_\theta\approx1.25°$) ... the inclined slope clustered exclusively
  in a high-pitch, low-roll region ($\mu_\phi\approx0.43°$, $\mu_\theta\approx6.95°$) ... reducing parasitic roll
  disturbances by 68.3% ... zero cluster overlap across all 30 trials"*. También citado en el caption de
  `fig:terrain_adaptability` (subfigura C de `fig:variable_topo_metrics`): *"form two perfectly non-overlapping
  clusters"*.
- **Lo que muestra la figura:** eje X = "Transversal Variance – Roll RMS (deg)" de **1.25 a ~3.1**; eje Y =
  "Longitudinal Variance – Pitch RMS (deg)" de **~1.2 a ~3.25**.
  - **Rugged Terrain (círculos azules):** roll ≈ 1.3–1.6° (con 2 outliers en 1.5–3.05°), pitch en su mayoría
    1.2–1.8° salvo **dos puntos claramente en pitch≈3.05–3.1°** — muy por encima del "μ_θ≈1.25°" citado.
  - **Inclined Slope (equis naranjas):** roll ≈ **1.4–1.65°** (no "0.43°" — casi 4× el valor citado), pitch ≈
    **2.0–3.25°** (no "6.95°" — menos de la mitad del valor citado).
  - **Solapamiento:** en el eje X (roll), el rango de Inclined Slope (1.4–1.65°) está **completamente contenido
    dentro** del rango de Rugged Terrain (1.3–3.05°) — exactamente lo opuesto de "zero cluster overlap" /
    "perfectly non-overlapping".
- **Por qué importa:** de los tres hallazgos M-01/M-02/M-03, este es el más cuantitativamente extremo (medias
  citadas ~3-4× distintas de lo que se lee en los ejes) y el que más directamente contradice una frase explícita
  ("perfectly non-overlapping", "zero overlap") que un revisor puede falsificar con una regla sobre la figura.
- **Acción recomendada (para todos los M-01/M-02/M-03):** antes de escribir una sola palabra nueva, regenerar (o
  pedir a quien tenga el notebook/script original que confirme) estas tres figuras a partir del dataset que
  efectivamente respalda los números ya escritos en el texto — o, si el texto es el que está desactualizado,
  reescribirlo a partir de lo que las figuras actuales muestran. **No se puede resolver por inspección visual
  únicamente si el texto o la figura es la fuente de verdad** — eso requiere volver a los logs/CSVs crudos del
  experimento (`experiments/` no tiene actualmente ninguna carpeta para R3-01 relacionada; si existe un
  notebook fuera de este repo que generó estos PNG, referenciarlo desde `intake/SOURCES.md` ayudaría a futuras
  auditorías).

### M-04 (severidad menor) — "T_switch = 0.3 ms, perfect Heaviside step" no coincide con los paneles B/C de `FigB_Decision_Delay.png`

- **Ubicación del texto:** `results.tex:279`: *"Both ECDF distributions collapsed into a perfect Heaviside step
  function ... The mechanical transition latency was equally deterministic, remaining invariant at
  $T_{switch}=0.3$ ms for both terrain types ... confirmed that the controller achieved structurally deterministic
  switching behaviour, completely free from chattering effects."*
- **Lo que muestra la figura:** Panel A ($T_{response}$) sí es un escalón de Heaviside perfecto (0→1 en un único
  salto en t=0) — **esa parte del texto es correcta**. Pero:
  - **Panel B (C1, Rugged Terrain, $T_{switch}$):** NO es un escalón único — sube a 0.87 en t≈0 pero tiene una
    **cola larga hasta t=0.6 s** (600 ms, no 0.3 ms) antes de llegar a 1.0. Es una distribución de dos escalones,
    con ~13% de los ensayos tardando hasta 2000× más que el valor citado.
  - **Panel C (C2, Inclined Slope, $T_{switch}$):** tampoco es un escalón único — es una escalera de **5-6
    saltos discretos** distribuidos entre 0.8 ms y 1.9 ms (orden de magnitud correcto respecto a "0.3 ms", pero
    no es un valor "invariante" ni un "perfect Heaviside step": hay dispersión real entre 0.8 y 1.9 ms).
- **Por qué importa (menor que M-01/M-02/M-03 pero real):** la frase "completely free from chattering effects" es
  una afirmación de robustez fuerte que el panel B contradice directamente (la cola hasta 600 ms en 13% de los
  ensayos es, por definición, el tipo de comportamiento no determinista que "chattering-free" promete excluir).
- **Acción recomendada:** igual que M-01–M-03, verificar contra los datos crudos antes de editar. Si la cola de
  600 ms en Panel B es real, el texto debería mencionarla explícitamente (p. ej. como un caso límite en terreno
  rugoso) en vez de afirmar "invariante para ambos tipos de terreno".

### M-05 (control positivo — no es un problema) — La matriz de confusión sí es 100% consistente con el texto

Verificación cruzada, para que quede documentado que no todo el bloque de métricas tiene problemas: `results.tex:571`
cita accuracy=0.800, precision=0.747, recall=0.918 sobre n=120 para el clasificador MLP. La matriz de confusión en
`fig1_confusion_matrix.png` da TP=56, FN=5, FP=19, TN=40 (suma 120) →
accuracy=(56+40)/120=0.800, precision=56/75=0.747, recall=56/61=0.918 — **coincide exactamente, cifra a cifra**.
El bloque de evaluación del clasificador MLP (`fig1`–`fig6`, líneas 567–623) es, en general, la parte de
`results.tex` con mejor trazabilidad número↔figura de toda la sección.

---

## 3. Plan de Reestructuración y Guía de Regeneración de Imágenes

Cada bloque abajo sigue la estructura pedida: figura(s) actuales, diagnóstico, propuesta y especificación técnica
exacta para regenerar. **Estas fusiones son independientes de los hallazgos M-01–M-04** — se pueden ejecutar ya
sea antes o después de resolver las discrepancias numéricas (aunque lo lógico es corregir los datos primero, para
no fusionar un error en una figura más grande y más difícil de corregir después).

### F-01 (causa raíz, alta prioridad) — "March Decision Module" / "Auxiliar" en todos los rasters neuronales

- **Figuras afectadas:** `NEU_EST_UNIG.png`, `NEU_EST_UNIB.png`, `NEU_EST_MUL.png`, `NEU_EST_UNIG_real.png`,
  `NEU_EST_MUL_real.png`, y con alta probabilidad (mismo generador, no verificadas pixel-a-pixel en esta pasada
  pero comparten título/estructura de panel) `NEU_IMU.png`, `NEU_IMU2.png`, `NEU_IMU_real.png`, `NEU_IMU2_real.png`.
- **Diagnóstico:** panel inferior-derecho (subpanel "d)" o "c)" según la figura) titulado **"March Decision
  Module"** — traducción literal incorrecta de "Módulo de Decisión de Marcha". El texto de `methodology.tex` y
  `results.tex` llama consistentemente a este módulo **"gait-decision module"**. Además, dentro del panel de
  LiDAR (subpanel "b)"), el cuarto subplot dice **"Auxiliar"** — palabra en español, debería ser "Auxiliary"
  (coincide con la capa "auxiliary layer" que sí nombra el texto, `results.tex:133`).
- **Propuesta de corrección (no es una fusión, es una corrección de rótulo — pero se agrupa aquí porque es la
  misma pieza de código para las ~9 figuras):**
  - Título del subpanel: `"March Decision Module"` → **`"Gait Decision Module"`**.
  - Título del subplot dentro del panel LiDAR: `"Auxiliar"` → **`"Auxiliary"`**.
- **Instrucciones para regeneración:** localizar en el script/notebook de graficación (fuera de este repo,
  probablemente en `PETER_SIMULATION` o en un notebook de análisis no versionado aquí) la cadena literal
  `"March Decision Module"` (o su origen, probablemente una variable `titulo_modulo_marcha` o similar mal
  traducida) y `"Auxiliar"`, corregirlas una sola vez, y regenerar las ~9 figuras desde ese mismo script para que
  la corrección se propague de forma idéntica a todas — evita corregir cada PNG a mano y con riesgo de
  inconsistencia entre ellas.

### F-02 (media prioridad) — Fusión de los 4 `fig1_*_macro.png` (robustez ante ruido, simulación) en una rejilla única

- **Figuras actuales:** `fig1_Appetitive_macro.png`, `fig1_Aversive_macro.png`, `fig1_Obstacle_macro.png`,
  `fig1_Complex_macro.png` — cuatro figuras independientes, cada una con 3 subpaneles (A: tiempo/duración vs.
  ruido, B: Pitch RMS vs. ruido, C: latencia de decisión vs. ruido), estructuralmente idénticas entre sí salvo la
  variable "A" (nombre distinto por escenario: Mission Time / Evacuation Time / Evasion Time / Lifecycle Time).
- **Diagnóstico visual:** las cuatro figuras comparten ejes X idénticos (Sensory Noise Index σ∈[0,4]), mismo
  estilo de error bars, mismos colores por panel (azul/rosa/verde) — son, de hecho, ya casi una rejilla mental
  que el lector arma comparando 4 figuras separadas por varias páginas de texto entre sí. **Una vez resuelto
  M-01** (para que el panel C dependa de una definición de latencia consistente entre las 4), esta es una fusión
  de bajo riesgo y alto beneficio de lectura.
- **Propuesta de fusión:** rejilla **4×3** (una fila por escenario, una columna por métrica), o alternativamente
  **3×4** si se prefiere que cada métrica ocupe una fila y cada escenario una columna (recomendado: 4 filas × 3
  columnas, porque el lector ya sigue el orden Appetitive→Aversive→Obstacle→Complex fila por fila en el texto).
- **Instrucciones de regeneración:**
  - **Layout:** Grid 4×3, una figura `\figure*` a ancho completo de columna doble en LaTeX (reemplaza a las 4
    `\begin{figure*}` individuales de las líneas 58–75, 79–96, 100–117, 153–170).
  - **Filas (orden fijo):** Appetitive, Aversive, Obstacle, Complex.
  - **Columnas:** (1) Tiempo/duración de misión vs. σ — unificar el nombre de variable a un único término
    genérico **"Mission Time $T_{sim}$ (s)"** en las 4 filas en vez de 4 nombres distintos (Mission/Evacuation/
    Evasion/Lifecycle Time), delegando la semántica específica al texto/caption, no al eje. (2) **"Pitch RMS
    (deg)"** — ya es consistente entre las 4. (3) **"Decision Latency (ms)"** — pendiente de resolver M-01 antes
    de fusionar, para no fusionar 4 definiciones distintas de "latencia" bajo el mismo eje.
  - **Ejes y escalas:** usar el mismo rango de eje Y por columna en las 4 filas cuando sea físicamente razonable
    (p. ej. Pitch RMS: fijar 0–4° en las 4 filas) para que el lector compare escenarios de un vistazo, no solo
    dentro de cada fila.
  - **Nomenclatura:** eje X unificado **"Sensory Noise Index ($\sigma$)"** en las 12 subgráficas, tal como ya
    está hoy.
  - **Etiquetas de fila:** añadir el nombre del escenario como etiqueta de fila (fuera del área de plot, al estilo
    `\rotatebox{90}` en LaTeX o como texto de márgen si se compone en Python/matplotlib con `fig.text()`), en vez
    de repetirlo en cada título de columna.

### F-03 (media prioridad) — Fusión de `fig5_classifier_comparison.png` + `fig6_computational_cost.png`

- **Figuras actuales:** `fig5_classifier_comparison.png` (accuracy/precision/recall/F1 de 4 clasificadores) y
  `fig6_computational_cost.png` (ya es un panel 1×2: latencia por muestra + tamaño de modelo, para los mismos 4
  clasificadores).
- **Diagnóstico:** el texto (`results.tex:607` y `results.tex:616`) discute ambas figuras en dos párrafos
  consecutivos, para justificar la misma decisión de diseño (por qué MLP y no SVM-RBF/Random Forest pese a menor
  accuracy). El panel **"Model size"** dentro de `fig6` (parámetros/nodos de árbol, escala log) **no se menciona
  en ningún punto del texto** — es contenido de figura huérfano de discusión.
- **Propuesta de fusión:** panel único **1×3** — (a) métricas de clasificación (barras agrupadas, ya existe en
  fig5), (b) latencia de inferencia por muestra (ya existe en fig6-izquierda), (c) tamaño de modelo (ya existe en
  fig6-derecha, pero **debe ganar una frase de discusión en el texto** o, si no se considera relevante para el
  argumento del paper, eliminarse del todo en vez de dejarse sin comentar).
- **Instrucciones de regeneración:**
  - **Layout:** 1×3, incluso ancho, compartiendo la leyenda de clasificadores (colores) en una única leyenda
    superior en vez de repetirla (o de omitirla, como hace hoy fig6).
  - **Ejes:** (a) "Score (5-fold CV mean)" 0–1.0 lineal; (b) "Inference time (µs/sample)" log10, y (c)
    "Parameters / tree nodes" log10 — mantener las escalas actuales de fig6, que ya son correctas.
  - **Orden de clasificadores:** idéntico en los 3 paneles — Logistic Reg. / SVM (RBF) / Random Forest / MLP
    (150-80) — ya es consistente hoy entre fig5 y fig6, mantenerlo.
  - **Decisión editorial pendiente para el autor:** si se conserva el panel (c) "Model size", añadir 1 frase en
    `results.tex` tras la línea 616 conectándolo con el argumento de "resource-constrained embedded hardware" que
    ya usa el resto del párrafo (el tamaño de modelo es directamente relevante a ese argumento y hoy se
    desperdicia).

### F-04 (baja prioridad, cosmética pero real) — Ejes "V A L U E" sin unidades y con dos magnitudes mezcladas en `GRAPH_IMU*.png`

- **Figuras afectadas:** `GRAPH_IMU.png`, `GRAPH_IMU2.png` (versión de simulación; no se inspeccionaron
  `GRAPH_IMU_real`/`GRAPH_IMU2_real` para este defecto específico porque resultaron ser gráficas de estado
  categórico, no series continuas — ver más abajo).
- **Diagnóstico:**
  - Eje Y rotulado letra-por-letra en vertical **"V\nA\nL\nU\nE"** (sin unidad, sin significado físico claro):
    superpone dos series con magnitudes y unidades físicas distintas — "Standar dev accel z" (desviación estándar
    de aceleración en Z, m/s²) y "Pitch angle" (grados) — **en el mismo eje sin dualidad de ejes**, lo cual hace
    ambiguo leer cualquiera de las dos curvas con precisión cuantitativa.
  - Error tipográfico en la leyenda: **"Standar dev accel z"** → falta la "d" de "Standard", y "z" debería ir en
    mayúscula para consistencia con el resto del documento (**"Standard dev. accel. Z"**).
  - El texto (`results.tex:199`) menciona un umbral específico ("the graph highlights the instant when this value
    exceeds the 3.7 threshold") que **no está dibujado en la figura** — no hay línea de referencia en 3.7.
- **Propuesta de fusión/rediseño:** convertir a **doble eje Y** (Y1 izquierda, Y2 derecha) en vez de un único eje
  ambiguo.
- **Instrucciones de regeneración:**
  - **Layout:** figura única, doble eje Y, sin cambio de tamaño/posición respecto a la actual.
  - **Ejes:** Eje X: **"Time (s)"** (sin cambio). Eje Y1 (izquierda, color azul, igual que hoy): **"Std. dev.
    acceleration, Z axis (m/s²)"**. Eje Y2 (derecha, color naranja, igual que hoy): **"Pitch angle (deg)"**.
  - **Nomenclatura/leyenda:** cambiar la entrada de leyenda "Standar dev accel z" → **"$\sigma_{az}$ — Std. dev.
    accel. Z"** (alineado con la notación $\sigma_{az}$ que methodology.tex ya define, `methodology.tex:354`) y
    "Pitch angle" → **"Pitch (deg)"**.
  - **Elemento añadido:** línea horizontal punteada en Y1=3.7 con etiqueta **"$U_{\sigma_{az}}$ threshold"**
    (nombre de la variable de umbral que methodology.tex ya define, `methodology.tex:354`), para que la figura
    autocontenga el umbral que el texto dice que muestra.
  - **Título:** mantener "IMU activity" o, mejor, diferenciarlo por figura: **"IMU activity — Rugged Terrain
    (Simulation)"** / **"IMU activity — Inclined Slope (Simulation)"** en vez del genérico "IMU activity"
    idéntico en ambas, para que la figura sea autoexplicativa sin depender del caption externo.

### F-05 (baja prioridad) — Nomenclatura `Stuck/Flat/Inclined` vs. $N_0/N_1/N_2$ en `GRAPH_IMU_real.png` / `GRAPH_IMU2_real.png`

- **Diagnóstico:** las figuras de estado categórico (`GRAPH_IMU_real.png`, `GRAPH_IMU2_real.png`, timeline
  binario Stuck/Flat/Inclined) rotulan las filas con nombres en inglés llano ("Stuck", "Flat", "Inclined") que no
  se corresponden 1:1 con la notación matemática que el texto usa para las mismas tres salidas de la MLP:
  $N_0$ (probabilidad terreno plano), $N_1$ (probabilidad terreno inclinado), $N_2$ (indicador binario de
  estancamiento) — ver `results.tex:195`.
  - Además, el título repetido **"IMU (Stuck / Flat / Inclined)"** seguido de un subtítulo casi idéntico **"IMU
    States (0–1)"** es una redundancia de título/subtítulo dentro de la misma figura (no del texto — un defecto
    puramente de la imagen).
- **Propuesta:** añadir la notación matemática entre paréntesis junto a cada etiqueta de fila: **"Flat ($N_0$)"**,
  **"Inclined ($N_1$)"**, **"Stuck ($N_2$)"** — permite al lector mapear figura↔ecuación sin tener que memorizar
  el orden. Colapsar el título/subtítulo redundante en uno solo: **"MLP output states: Flat ($N_0$) / Inclined
  ($N_1$) / Stuck ($N_2$)"**.
- **Instrucciones de regeneración:** cambio de rótulo de eje Y únicamente (`yticklabels` en el script de
  matplotlib/seaborn que genera el heatmap binario) — no requiere volver a correr ningún experimento, es
  puramente cosmético sobre los mismos datos ya calculados.

### F-06 (baja prioridad, informativa) — `fig4_architecture_ablation.png`: diferencias visualmente imperceptibles para la afirmación que sustenta

- **Diagnóstico:** el texto (`results.tex:598`) afirma que la arquitectura (150,80) logra "the highest F1-score
  among all tested architectures (F1=0.771)" frente a (50: 0.747), (100: 0.766), (200,100,50: 0.766). El gráfico
  de barras agrupadas hace estas diferencias (0.747 vs. 0.766 vs. 0.771 vs. 0.766) **visualmente
  indistinguibles** — las 4 barras F1 (rojas) se ven prácticamente iguales a simple vista, porque el eje Y va de
  0.0 a 1.0 completo, comprimiendo un rango real de solo 0.024 puntos F1 en ~2% de la altura del gráfico.
- **Propuesta:** no es una fusión, es un ajuste de escala. Recortar el eje Y a un rango que amplifique la
  diferencia real (p. ej. 0.65–0.80, con una nota "\% axis truncated for legibility" o un inset/zoom), o
  reemplazar por una tabla numérica simple (ya casi redundante con la prosa que lista los 4 valores) si no se
  considera que el gráfico de barras aporte algo que la prosa ya no diga.
- **Instrucciones de regeneración:** `ax.set_ylim(0.65, 0.80)` (o el rango que el autor prefiera) en el script
  que genera `fig4_architecture_ablation.png`; mantener las 4 series (accuracy/precision/recall/f1) y colores
  actuales.

### F-07 (informativa, sin acción necesaria) — Fotografías de terreno/frames (D1-D6, E1-E6, Prueba_Terreno_Parte_1-6) sin problema de idioma

Se inspeccionó una muestra (`D1.png`) para verificar la instrucción de "control de traducción" del encargo: son
fotografías directas del robot físico sin overlays de texto ni HUD — **no hay mezcla de idioma que corregir en
esta familia de figuras**. Se documenta aquí explícitamente para que quede registrado que fueron revisadas y no
omitidas por descuido.

### F-08 (informativa) — `fig_stability_phases.png` es internamente consistente con `tab:crawl_stability`

Los cuatro paneles de fase de balanceo (A, C, D, F) muestran TR≈0.71–0.77, y los dos paneles de apoyo de 4 patas
(B, E) muestran "Static stance" (TR≈0, sin anotar numéricamente). Promediando aproximadamente estos dos regímenes
se obtiene un valor cercano a $TR_{mean}=0.439$ (tabla `tab:crawl_stability`) — **no hay contradicción aquí**,
a diferencia de M-02/M-03. Se documenta para dejar constancia de que esta figura sí fue verificada y aprobada.

---

## 4. Depuración de Redundancia Texto↔Tabla/Figura Restante (más allá de lo ya resuelto en R2-01)

La ronda R2-01 (Sebas) ya condensó la mayoría de la restatement numérica obvia. Quedan estos casos menores no
cubiertos por esa ronda:

| Ubicación | Problema | Propuesta |
|---|---|---|
| `results.tex:917-920`, tabla `tab:consolidated_physical_metrics`, fila "Complex" | El valor "peak $>30{,}000$" en la columna $Var(z)$ peak no tiene unidad ni escala de referencia — un lector no puede saber si eso es alto o bajo sin comparar manualmente contra las otras 3 filas (~1100, dual-peak sin número, sustained) | Normalizar la columna a una escala relativa común (p. ej. "×27 vs. baseline Obstacle" o un rango) o añadir una nota al pie con la unidad de "firing variance" |
| `results.tex:934`, párrafo de energía | Describe cualitativamente "invariant energetic cost" vs. "greater dispersion" para las dos direcciones de transición sin dar ningún número (ni siquiera aproximado) — es prosa puramente cualitativa sobre una figura (`FigReal_Morphological_Transition_Energy.png`) que sí tiene datos cuantificables | Añadir al menos el rango o media±SD de energía (J o Wh) por dirección de transición, igual que se hizo para las otras figuras de esta subsección |
| `results.tex:945-949` | Tres párrafos consecutivos describen los 4 paneles de `FigReal_Terrain_Latencies_4Panels.png` panel por panel — ya fue parcialmente condensado por R2-01 (patch 16), pero el primer párrafo (945) sigue siendo puramente descriptivo de metodología sin aportar interpretación nueva | Fusionable con el párrafo siguiente (947) sin pérdida de contenido — es candidato a una futura pasada de redundancia, no urgente |

---

## 5. Depuración Editorial, Gramática y Estilo

Revisión dirigida (no exhaustiva línea-por-línea, dado que el foco del encargo es métricas/figuras) — se listan
los casos encontrados al leer el archivo completo:

- **`results.tex:9`** — *"its scope and caveats as a symbolic, non-certified test arena are discussed in
  Section~\ref{ssec:Limitations}"*: "non-certified test arena" es una frase un poco abrupta/calcada; considerar
  *"a symbolic representation rather than a certified test arena"* para fluidez, sin cambiar el significado.
- **`results.tex:224`** — párrafo sobre la discretización STL del terreno inclinado en simulación es denso y
  técnicamente correcto, pero está aislado entre dos figuras sin conexión clara con el párrafo anterior o
  siguiente — candidato a moverse junto a la explicación del terreno inclinado en la línea 197, donde
  temáticamente encaja mejor.
- **`results.tex:497-500`** — dos párrafos consecutivos comparan repetidamente el comportamiento real vs.
  simulación para el estímulo apetitivo con estructura de frase casi idéntica ("unlike the simulation, where...",
  "In contrast, in the simulation...") — no es una redundancia de datos (cada uno aporta un ángulo neuronal
  distinto), pero podría fusionarse en un solo párrafo con mejor flujo.
- **`results.tex:954`** — el párrafo de Limitations es una sola oración larguísima (>150 palabras) con múltiples
  cláusulas subordinadas encadenadas con "yet", "rather than", "Instead" — buen contenido, pero se beneficiaría de
  dividirse en 2-3 oraciones para legibilidad, sin tocar el argumento.
- **Consistencia de mayúsculas en nombres de modo:** el documento alterna entre "Quadrupedal Walking",
  "quadrupedal mode", "Quadrupedal ($C$)" y similar para Differential Rolling/Omnidirectional — no es un error,
  pero no hay una convención única de capitalización aplicada consistentemente; se beneficiaría de una pasada de
  estandarización (p. ej. siempre Title Case cuando se usa como nombre propio de modo, minúscula cuando es
  adjetivo genérico).

### Consistencia de referencias cruzadas si se aplican las fusiones de §3

| Fusión propuesta | Referencias `\ref{}`/`\label{}` afectadas | Acción necesaria |
|---|---|---|
| F-02 (4× `fig1_*_macro` → rejilla única) | `fig:appetitive_results`, `fig:aversive_results`, `fig:obstacle_results`, `fig:complex_results` (4 labels) + sus 8 sub-labels (`fig:appetitive_macro`, `fig:appetitive_micro`, etc.) | Colapsar a un único `\label{fig:noise_robustness_grid}` con subfiguras `(a)`-`(l)`; actualizar las 4 llamadas `\ref{}` en los párrafos "Appetitive/Aversive/Obstacle/Complex Targeting" (líneas 77, 98, 119, 172) para apuntar a `fig:noise_robustness_grid` + letra de panel específica |
| F-03 (`fig5`+`fig6` → panel 1×3) | `fig:classifier_comparison`, `fig:computational_cost` (2 labels) | Colapsar a `\label{fig:classifier_tradeoff}`; actualizar `\ref{}` en líneas 607 y 616 (dos párrafos consecutivos, se pueden fusionar en uno solo si se fusiona la figura) |
| F-04 (doble eje en `GRAPH_IMU`/`GRAPH_IMU2`) | `fig:GRAPH_IMU`, `fig:GRAPH_IMU2` | Sin cambio de label — mismo `\ref{}`, solo cambia el contenido interno de la imagen |
| F-05 (rótulos `Stuck/Flat/Inclined`) | `fig:GRAPH_IMU_real`, `fig:GRAPH_IMU2_real` | Sin cambio de label |

---

## 6. Propuesta de Mapeo de Fusiones de Métricas

| Métrica(s) | Ubicación actual | Acción propuesta | Prioridad |
|---|---|---|---|
| Decision Latency (4 escenarios sim.) | `fig1_*_macro.png` panel C × 4 | **Verificar dato crudo (M-01) antes de fusionar**; después, fusionar a F-02 | Alta (verificación), Media (fusión) |
| Tipover Risk profile (rugged/slope) | `FigA_Stability_Profile.png` | **Verificar dato crudo (M-02)** — no fusionar hasta resolver | Alta |
| Roll/Pitch RMS phase-space (rugged/slope) | `FigC_Terrain_Adaptability.png` | **Verificar dato crudo (M-03)** — no fusionar hasta resolver | Alta |
| $T_{switch}$ ECDF (rugged/slope) | `FigB_Decision_Delay.png` paneles B/C | **Verificar cola de 600 ms (M-04)** | Media |
| Mission Time / Pitch RMS / Decision Latency (4 escenarios sim.) | 4× `fig1_*_macro.png` | Fusionar a rejilla 4×3 (F-02) | Media |
| Classifier accuracy + inference latency + model size | `fig5` + `fig6` | Fusionar a panel 1×3 (F-03); decidir si se conserva "model size" | Media |
| $Var(z)$ peak (4 escenarios físicos) | `tab:consolidated_physical_metrics`, columna 2 | Normalizar unidad/escala relativa (§4) | Baja |
| Energía de transición morfológica | `results.tex:934`, prosa sin números | Añadir cifras concretas desde `FigReal_Morphological_Transition_Energy.png` | Baja |
| Model size (parámetros MLP/SVM/RF) | `fig6_computational_cost.png` panel derecho | Conectar con 1 frase en prosa, o retirar del panel si no aporta | Baja |

---

## 7. Checklist de Próximos Pasos para el Autor

**Fase 1 — Verificación de datos (bloqueante, hacer primero):**
1. [ ] Localizar el script/notebook que generó `FigA_Stability_Profile.png`, `FigB_Decision_Delay.png`,
   `FigC_Terrain_Adaptability.png` y los 4 `fig1_*_macro.png`, y confirmar si el dataset usado coincide con el
   que se usó para redactar los números en `results.tex:77,174,178,276,281` (M-01, M-02, M-03).
2. [ ] Decidir, para cada uno de los 4 hallazgos M-01–M-04, si la corrección va en el **texto** (actualizar los
   números citados para que coincidan con las figuras actuales) o en la **figura** (regenerarla desde el dataset
   correcto que sí respalda el texto ya escrito). **No aplicar ninguna de las dos sin antes confirmar cuál es la
   fuente de verdad.**
3. [ ] Si se decide que el texto necesita corrección: reescribir los párrafos de `results.tex:77` (Appetitive),
   `:178` (caption tabla), `:276` (Tipover Risk), `:279` (T_switch/Heaviside), `:281` (phase-space) usando los
   valores reales leídos de las figuras vigentes, envuelto en `\revblue{}` por ser texto materialmente cambiado
   esta ronda (regla permanente del proyecto, ver `CLAUDE.md`).

**Fase 2 — Corrección de idioma/nomenclatura (no bloqueante, bajo riesgo):**
4. [ ] Corregir "March Decision Module" → "Gait Decision Module" y "Auxiliar" → "Auxiliary" en el script fuente
   que genera los rasters neuronales (F-01), y regenerar las ~9 figuras afectadas de una sola vez.
5. [ ] Añadir notación $N_0/N_1/N_2$ a los rótulos de `GRAPH_IMU_real.png`/`GRAPH_IMU2_real.png` (F-05).
6. [ ] Corregir "Standar dev accel z" → "Std. dev. accel. Z" y convertir a doble eje Y con unidades explícitas en
   `GRAPH_IMU.png`/`GRAPH_IMU2.png`, añadiendo la línea de umbral 3.7 que el texto ya menciona (F-04).

**Fase 3 — Fusión de paneles (después de Fase 1, para no fusionar un dato erróneo):**
7. [ ] Regenerar los 4 `fig1_*_macro.png` como una rejilla única 4×3 (F-02), unificando el nombre de la métrica
   de tiempo de misión entre escenarios y fijando escalas de eje Y comunes por columna.
8. [ ] Fusionar `fig5_classifier_comparison.png` + `fig6_computational_cost.png` en un panel 1×3 (F-03); decidir
   si se conserva y se discute el panel "Model size" o se retira.
9. [ ] Ajustar el rango del eje Y de `fig4_architecture_ablation.png` para hacer visualmente perceptible la
   diferencia de F1 que el texto usa para justificar la arquitectura elegida (F-06).

**Fase 4 — Actualización de referencias cruzadas y registro en el pipeline:**
10. [ ] Actualizar los `\label{}`/`\ref{}` afectados por las fusiones de la Fase 3 (tabla de §5).
11. [ ] Una vez resuelto, dar de alta en `PROGRESS.md` las filas correspondientes (`N-xx` para las fusiones de
    figura que son contenido nuevo/reestructurado, `C-xx` para las correcciones puntuales de texto/nomenclatura),
    siguiendo el flujo estándar de `intake/` descrito en `CLAUDE.md` — este documento, una vez las decisiones de
    la Fase 1 estén tomadas, sirve como el documento de entrada para ese triage.
12. [ ] Mover este archivo a `intake/processed/` solo cuando todas las filas que genere hayan alcanzado al menos
    estado `applied` en `PROGRESS.md` (regla del proyecto).
