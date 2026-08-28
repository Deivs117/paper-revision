# R02-01 — Auditoría Exhaustiva de Métricas y Recursos Visuales (`sections/results.tex`)

**Estado:** DIAGNÓSTICO, con verificación de datos y decisiones de implementación ya cerradas en el documento
complementario — ningún archivo de `sections/`, `assets/` o `source/` fue modificado para producir este informe.
Es de solo lectura sobre el estado actual del repositorio.

**Relación con `intake/pending/R02-01_data_traceability_and_plotting_plan.md` ("Informe 2"):** este documento
("Informe 1") identifica **qué** está mal y **por qué importa** — es el catálogo de diagnóstico. Informe 2
responde, para cada hallazgo de aquí, **de dónde sale el dato real y cómo se recupera/regenera**, y ya tiene
**11 decisiones confirmadas por el autor (D-1–D-11)** que resuelven toda la Fase 1 de verificación de este
documento (§7 más abajo) y fijan el plan de implementación completo. Los dos documentos están pensados para
usarse juntos: **este informe para entender el problema y su severidad, Informe 2 para ejecutar la corrección**
— cada hallazgo `M-NN`/`F-NN` de aquí abajo tiene ahora una anotación **"Estado (2026-08-27)"** que apunta a la
sección exacta de Informe 2 donde se resolvió.

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
   **✅ RESUELTO (2026-08-27, Informe 2 §0):** se recalcularon estas cuatro cifras directamente contra
   `experiments/simulation/` (CSV/JSON crudos, no solo inspección visual) — **en los cuatro casos la figura
   coincide con el dato crudo y el texto es el que está desactualizado.** La verificación bloqueante de la Fase 1
   (§7) ya está hecha; lo único pendiente es la decisión de redacción en sí (reescribir los 5 párrafos citados
   usando los valores reales), que sigue sin tomarse.
2. **Error de traducción sistemático en las figuras generadas por script (severidad ALTA, 1 causa raíz,
   ~8-10 figuras afectadas, hallazgo F-01).** Todos los rasters neuronales (`NEU_EST_*`, `NEU_IMU*`) rotulan un
   panel como **"March Decision Module"** — traducción literal incorrecta de "Módulo de Decisión de Marcha"
   (debería ser *"Gait Decision Module"*, coincidiendo con el término que usa el propio `methodology.tex`) — y
   otro panel como **"Auxiliar"** (español, debería ser *"Auxiliary"*). Como es el mismo script de graficación el
   que genera las ~10 figuras, es una única corrección de código que se propaga a todas.
   **Estado (2026-08-27, Informe 2 §3.2/§3.4):** la corrección se centraliza en un único builder
   (`neural_raster.py`) reutilizado por todas las variantes — para `NEU_EST_UNIB`/`NEU_EST_UNIG`/`NEU_EST_MUL`
   (sim y físico) hay CSV real y el builder es implementable de inmediato (Grupo 1); para `NEU_IMU`/`NEU_IMU2`
   (sim y físico) el mismo builder consume datos vectorizados (D-1/D-8, Grupo 2 de Informe 2), porque esas 4
   figuras no tienen CSV crudo disponible (ver F-Data-04/05 de Informe 2).
3. **Redundancia visual estructural y oportunidades de fusión de paneles (severidad MEDIA, sección §3).**
   Cuatro pares de familias de figuras (macro-robustez de los 4 escenarios simulados; ECDF+dinámica+RMS de los 4
   escenarios físicos; comparación de clasificadores + costo computacional; timeline IMU sim/real) están
   estructuralmente duplicadas panel por panel y son candidatas naturales a rejillas consolidadas — exactamente
   el patrón que ya se aplicó una vez con éxito para las tablas `tab:consolidated_simulation_metrics` y
   `tab:consolidated_physical_metrics` (ver R2-01, patches 03 y 15), pero que nunca se extendió al arte gráfico
   mismo.
   **✅ Decidido (2026-08-27, Informe 2 D-9/D-3):** ambas fusiones propuestas en §3 más abajo (F-02: rejilla 4×3
   de `fig1_*_macro.png`; F-03: panel 1×3 de `fig5`+`fig6`) están **confirmadas para ejecutarse**, no solo
   propuestas — ver Informe 2 §3.4 para el orden de implementación exacto.
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
- **✅ Estado (2026-08-27, Informe 2 §0):** verificado contra `trial_summary.json.exp_latency` de las 15 réplicas
  de `familia_a_apetitivo` — rango real 0.015 s–3.07 s, media≈60 ms solo en $\sigma=0$ (sin ruido), subiendo a
  1.6–2.0 s en $\sigma\geq1$. **La figura y el dato crudo coinciden entre sí; la hipótesis de causa de arriba
  (medida de inferencia pura vs. pipeline completo) queda descartada como explicación** — el dato crudo *es* el
  pipeline completo (mismo campo que alimenta la figura) y de todas formas varía con el ruido. La única acción
  pendiente es de redacción: reescribir "≈47 ms, constante" en `results.tex:77,178,973`.

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
- **✅ Estado (2026-08-27, Informe 2 §0):** verificado contra `stability_log.csv`/columna `TR` de las 15 réplicas
  de `familia_c1_terreno_rugoso` y las 15 de `familia_c2_pendiente` — media global rugoso=0.600, media global
  pendiente=0.593, ambas planas en el rango 0.58–0.60 salvo picos transitorios aislados. **Coincide con la
  figura, no con el texto** — no existe ningún archivo en el repositorio consistente con "$\mu_{TR}\approx0.42$"
  ni con una escalada monótona. La nota de calibración de arriba queda resuelta: no hace falta buscar una versión
  anterior de la figura, el dataset actual y la figura actual ya están sincronizados entre sí.

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
- **✅ Estado (2026-08-27, Informe 2 §0):** `experiments/simulation/` sí tenía el dato (la nota de arriba estaba
  equivocada en ese punto específico — no era R3-01, era `familia_c1_terreno_rugoso`/`familia_c2_pendiente`, ya
  documentadas en `experiments/` desde antes de esta auditoría). Verificado contra `trial_summary.json.roll_rms`/
  `pitch_rms` de las 30 réplicas: rugoso media roll=1.586°, pitch=1.667°; pendiente media roll=1.469°,
  pitch=2.290°. **Coincide con la figura (no con el texto)** casi exactamente, y confirma en particular que el
  solapamiento en roll que la figura muestra es real — el texto ("zero cluster overlap", 1.36/1.25 vs.
  0.43/6.95) no corresponde a ningún archivo del repositorio.

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
- **✅ Estado (2026-08-27, Informe 2 §0):** verificado contra `trial_summary.json.tswitch` de las 30 réplicas —
  **la cola de 600 ms en Panel B es real y coincide con precisión exacta**: 2 de 15 réplicas de terreno rugoso
  (13.3%) caen en 0.5999 s/0.6006 s, el resto en 0.0002–0.0007 s; terreno pendiente muestra 15 valores distintos
  entre 0.0009–0.0018 s, consistente con la "escalera de 5-6 saltos" que describe la figura. **El texto ("0.3 ms
  invariante para ambos terrenos") no corresponde a ningún archivo existente** — misma conclusión que M-01–M-03.

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
- **Estado (2026-08-27, Informe 2 §3.2/§3.4):** el script de graficación original no se encontró en el repo — la
  corrección se hace en un builder nuevo (`neural_raster.py`, Informe 2) que centraliza el rótulo correcto para
  todas las variantes. `NEU_EST_UNIB`/`NEU_EST_UNIG`/`NEU_EST_MUL` (sim y físico) tienen CSV real y son
  implementables ya (Informe 2, Grupo 1); `NEU_IMU`/`NEU_IMU2` (sim y físico, 4 figuras) no tienen CSV crudo
  disponible (Informe 2, F-Data-04/05) y se resuelven vectorizando el PNG actual con WebPlotDigitizer antes de
  poder aplicar la corrección — ver Informe 2 §2/§3.4, Grupo 2.

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
- **✅ Estado (2026-08-27, Informe 2 D-9):** fusión **confirmada, se ejecuta directamente** (no se regeneran antes
  las 4 figuras individuales) — las 15 réplicas por escenario ya tienen CSV verificado (Informe 2 §0), incluida la
  corrección de F-Data-01 (latencia de Obstacle, que usaba un centinela `-1.0`). Implementable ya en
  `macro_robustness.py`, Informe 2 §3.4 Grupo 1.

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
- **✅ Estado (2026-08-27, Informe 2 D-3/D-11):** fusión **confirmada, se ejecuta**. No existe el notebook de
  entrenamiento original (Informe 2, F-Data-06), así que `fig5`/`fig6` se vectorizan con WebPlotDigitizer (los
  valores de los 3 clasificadores no-MLP no están citados en prosa en ningún punto de `results.tex`) — ver
  Informe 2 §2, Grupo B de calibración compartida, y §3.4 Grupo 2.

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
- **Estado (2026-08-27, Informe 2 F-Data-04/05):** sin CSV crudo disponible en `experiments/` para
  `familia_c1_terreno_rugoso`/`familia_c2_pendiente` (ni activaciones $X_i$ ni aceleración/pitch continuos) — se
  vectoriza `GRAPH_IMU.png`/`GRAPH_IMU2.png` completas con WebPlotDigitizer, y el rediseño de doble eje Y +
  umbral en 3.7 propuesto arriba se aplica sobre el dato vectorizado, no sobre una re-corrida. Ver Informe 2 §2,
  Grupo C de calibración compartida.

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
- **Estado (2026-08-27, Informe 2 D-7/F-Data-09/10):** la nota de "puramente cosmético sobre los mismos datos ya
  calculados" arriba asumía que había un CSV editable — **no lo hay** para estas dos figuras específicas; se
  descartó la asociación con `Test_current_integrated_*` por nombre de carpeta no confiable (D-7) y se vectorizan
  ambas figuras completas desde el PNG publicado, aplicando el cambio de rótulo sobre el dato ya extraído. Ver
  Informe 2 §2, Grupo D de calibración compartida (comparte grupo con `FigReal_Terrain_Latencies_4Panels.png`).

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
- **✅ Estado (2026-08-27, Informe 2 F-Data-06):** **no requiere vectorizar** — los 4 valores de F1 por
  arquitectura ya están citados en `results.tex:598`, así que se regenera directamente desde esos valores con el
  nuevo `ylim`. Es, junto con `fig1_confusion_matrix.png`, la única figura del bloque de clasificador que queda
  fuera del alcance de vectorización (Informe 2 D-1) por tener ya su dato completo en prosa.

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

**Estado (2026-08-27, Informe 2 F-Data-03/D-6):** el run que generó esta figura ($N=268$ muestras) no tiene
carpeta propia en `experiments/` (ninguna de las 30 réplicas de C1/C2 coincide en conteo de filas) — se vectoriza
la figura con WebPlotDigitizer (pocos puntos de inflexión discretos, caso simple). **Los números de
`tab:crawl_stability` NO se vectorizan** — se mantienen como fuente de verdad ya publicada en LaTeX (D-6); solo la
figura se redibuja para seguir combinando visualmente con esos números. Ver Informe 2 §2, Grupo A.

---

## 4. Depuración de Redundancia Texto↔Tabla/Figura Restante (más allá de lo ya resuelto en R2-01)

La ronda R2-01 (Sebas) ya condensó la mayoría de la restatement numérica obvia. Quedan estos casos menores no
cubiertos por esa ronda:

| Ubicación | Problema | Propuesta |
|---|---|---|
| `results.tex:917-920`, tabla `tab:consolidated_physical_metrics`, fila "Complex" | El valor "peak $>30{,}000$" en la columna $Var(z)$ peak no tiene unidad ni escala de referencia — un lector no puede saber si eso es alto o bajo sin comparar manualmente contra las otras 3 filas (~1100, dual-peak sin número, sustained) | Normalizar la columna a una escala relativa común (p. ej. "×27 vs. baseline Obstacle" o un rango) o añadir una nota al pie con la unidad de "firing variance" |
| `results.tex:934`, párrafo de energía | Describe cualitativamente "invariant energetic cost" vs. "greater dispersion" para las dos direcciones de transición sin dar ningún número (ni siquiera aproximado) — es prosa puramente cualitativa sobre una figura (`FigReal_Morphological_Transition_Energy.png`) que sí tiene datos cuantificables | Añadir al menos el rango o media±SD de energía (J o Wh) por dirección de transición, igual que se hizo para las otras figuras de esta subsección. **Fuente confirmada (Informe 2 §1.2):** `experiments/real/Test_current_integrated_*/imu_ina_*.csv` (`current_A`×`voltage_V`=`power_W`, integrado en el tiempo) — dato real disponible, no requiere vectorizar. |
| `results.tex:945-949` | Tres párrafos consecutivos describen los 4 paneles de `FigReal_Terrain_Latencies_4Panels.png` panel por panel — ya fue parcialmente condensado por R2-01 (patch 16), pero el primer párrafo (945) sigue siendo puramente descriptivo de metodología sin aportar interpretación nueva | Fusionable con el párrafo siguiente (947) sin pérdida de contenido — es candidato a una futura pasada de redundancia, no urgente. **Nota (Informe 2 D-7):** la figura misma se regenera por vectorización (Grupo D), no desde `experiments/real/`, así que esta fusión de prosa es independiente de esa regeneración y puede hacerse en cualquier orden respecto a ella. |

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

**Actualizado 2026-08-27** — las verificaciones de M-01–M-04 ya se hicieron (Informe 2 §0) y las fusiones F-02/F-03
ya están confirmadas (Informe 2 D-9/D-3), así que esta tabla ya no tiene entradas "pendientes de verificar": lo
que queda es redacción y ejecución de builders, ambas cubiertas por Informe 2 §3.4/§5.

| Métrica(s) | Ubicación actual | Acción propuesta | Prioridad | Estado |
|---|---|---|---|---|
| Decision Latency (4 escenarios sim.) | `fig1_*_macro.png` panel C × 4 | Reescribir texto (M-01 resuelto: figura correcta); fusionar a F-02 | Alta (redacción), Media (fusión) | ✅ Verificado — falta redacción + Informe 2 Grupo 1 |
| Tipover Risk profile (rugged/slope) | `FigA_Stability_Profile.png` | Reescribir texto (M-02 resuelto: figura correcta) | Alta | ✅ Verificado — falta redacción |
| Roll/Pitch RMS phase-space (rugged/slope) | `FigC_Terrain_Adaptability.png` | Reescribir texto (M-03 resuelto: figura correcta) | Alta | ✅ Verificado — falta redacción |
| $T_{switch}$ ECDF (rugged/slope) | `FigB_Decision_Delay.png` paneles B/C | Reescribir texto (M-04 resuelto: cola de 600 ms confirmada real) | Media | ✅ Verificado — falta redacción |
| Mission Time / Pitch RMS / Decision Latency (4 escenarios sim.) | 4× `fig1_*_macro.png` | Fusionar a rejilla 4×3 (F-02) | Media | ✅ Confirmado (D-9) — Informe 2 Grupo 1 |
| Classifier accuracy + inference latency + model size | `fig5` + `fig6` | Fusionar a panel 1×3 (F-03); decidir si se conserva "model size" | Media | ✅ Confirmado (D-3) — requiere vectorizar (Informe 2 Grupo 2) |
| $Var(z)$ peak (4 escenarios físicos) | `tab:consolidated_physical_metrics`, columna 2 | Normalizar unidad/escala relativa (§4) | Baja | Sin decisión aún — puramente editorial, no depende de datos |
| Energía de transición morfológica | `results.tex:934`, prosa sin números | Añadir cifras concretas desde `FigReal_Morphological_Transition_Energy.png` | Baja | ✅ Fuente confirmada (`imu_ina_*.csv`), no requiere vectorizar |
| Model size (parámetros MLP/SVM/RF) | `fig6_computational_cost.png` panel derecho | Conectar con 1 frase en prosa, o retirar del panel si no aporta | Baja | Decisión editorial pendiente del autor |

---

## 7. Checklist de Próximos Pasos para el Autor

**Este checklist queda reemplazado como plan de ejecución por `intake/pending/R02-01_data_traceability_and_plotting_plan.md`
§3.4/§5 (Informe 2)** — se conserva aquí solo con anotación de estado, para no mantener dos listas de pasos en
paralelo que puedan desincronizarse. Usar Informe 2 para saber **qué hacer y en qué orden**; usar este documento
para entender **por qué** cada paso existe.

**Fase 1 — Verificación de datos — ✅ COMPLETA (2026-08-27, Informe 2 §0):**
1. [x] Localizar el dataset que generó `FigA_Stability_Profile.png`, `FigB_Decision_Delay.png`,
   `FigC_Terrain_Adaptability.png` y los 4 `fig1_*_macro.png`, y confirmar si coincide con los números en
   `results.tex:77,174,178,276,281` (M-01, M-02, M-03). **Hecho: `experiments/simulation/` sí lo tenía; en los 4
   casos la figura coincide con el dato crudo, el texto no.**
2. [x] Decidir si la corrección va en el texto o en la figura. **Decidido: en el texto — las figuras actuales
   están sincronizadas con el dataset disponible en `experiments/`.**
3. [ ] Reescribir los párrafos de `results.tex:77` (Appetitive), `:178` (caption tabla), `:276` (Tipover Risk),
   `:279` (T_switch/Heaviside), `:281` (phase-space) usando los valores reales de la tabla de §0 de este informe
   (o §0 de Informe 2, misma tabla), envuelto en `\revblue{}` (regla permanente del proyecto, `CLAUDE.md`). **Único
   paso de Fase 1 que sigue sin ejecutarse** — es de redacción pura, no requiere más verificación de datos.

**Fase 2 — Corrección de idioma/nomenclatura → ver Informe 2 §3.4 Grupo 1 (builders listos, sin vectorizar) y
Grupo 2 (requieren vectorizar primero):**
4. [ ] Corregir "March Decision Module" → "Gait Decision Module" y "Auxiliar" → "Auxiliary" (F-01) en el nuevo
   builder `neural_raster.py` — parcialmente Grupo 1 (`NEU_EST_*`, CSV real) y parcialmente Grupo 2 (`NEU_IMU*`,
   requiere vectorizar, Informe 2 F-Data-04/05).
5. [ ] Añadir notación $N_0/N_1/N_2$ a `GRAPH_IMU_real.png`/`GRAPH_IMU2_real.png` (F-05) — Grupo 2, requiere
   vectorizar primero (Informe 2 D-7, no se confía en `Test_current_integrated_*` por nombre de carpeta).
6. [ ] Corregir "Standar dev accel z" y convertir a doble eje Y con umbral 3.7 en `GRAPH_IMU.png`/`GRAPH_IMU2.png`
   (F-04) — Grupo 2, requiere vectorizar primero (Informe 2 F-Data-04/05).

**Fase 3 — Fusión de paneles → ver Informe 2 §3.4 (ambas fusiones ya confirmadas, D-9/D-3, no pendientes de
decisión):**
7. [ ] Regenerar los 4 `fig1_*_macro.png` como rejilla 4×3 (F-02, **confirmado D-9**) — Grupo 1 de Informe 2, CSV
   real completo, implementable en cuanto se cierre el paso 3 de Fase 1 (redacción de M-01).
8. [ ] Fusionar `fig5_classifier_comparison.png` + `fig6_computational_cost.png` en panel 1×3 (F-03, **confirmado
   D-3**) — Grupo 2 de Informe 2, requiere vectorizar (no hay notebook de entrenamiento original).
9. [ ] Ajustar el rango del eje Y de `fig4_architecture_ablation.png` (F-06) — **no requiere vectorizar**, los 4
   valores de F1 ya están en prosa (`results.tex:598`); es el único paso de esta fase implementable de inmediato.

**Fase 4 — Actualización de referencias cruzadas y registro en el pipeline:**
10. [ ] Actualizar los `\label{}`/`\ref{}` afectados por las fusiones de la Fase 3 (tabla de §5).
11. [ ] Dar de alta en `PROGRESS.md` las filas correspondientes (`N-xx`/`C-xx`), con `Data source` apuntando a
    `experiments/_plotting/` (y a `experiments/_plotting/vectorized/` cuando la figura venga de vectorización —
    ver Informe 2 §3.2), siguiendo el flujo estándar de `intake/` descrito en `CLAUDE.md`.
12. [ ] Mover este archivo y `R02-01_data_traceability_and_plotting_plan.md` a `intake/processed/` juntos, solo
    cuando todas las filas que generen entre los dos hayan alcanzado al menos estado `applied` en `PROGRESS.md`
    (regla del proyecto) — se mueven a la vez porque están cruzados y dejar uno en `pending/` sin el otro
    rompería la trazabilidad entre "por qué" y "cómo".

---

## 8. Estado Actualizado — Ronda N-02, físico (2026-08-27, 4 sub-rondas de auditoría + ejecución §9)

Entre la publicación de este informe y hoy, `experiments/N-02-physical-figure-regeneration/` pasó por 4 rondas
de regeneración + auditoría manual del autor (ver `experiments/N-02-physical-figure-regeneration/README.md` y
`experiments/_plotting/vectorized/README.md` para el detalle técnico completo de cada una), y el checklist de
tareas de escritura de §9 ya se ejecutó por completo (commit `d93adbd`, filas `N-03`/`N-04` en `PROGRESS.md`,
estado `applied`). **Las 12 figuras físicas + la fusión F-03 ya están promovidas a `assets/`, no solo
aprobadas.** Este apartado solo resume el estado final por hallazgo de este informe — el detalle de *cómo* se
llegó a cada resultado vive en los README ya citados; el detalle de *qué patch lo aplicó* vive en
`patches/n-03-physical-figure-promotion-classifier-fusion.tex` y `patches/n-04-m01-m04-text-redaction.tex`.

| Hallazgo de este informe | Estado final (2026-08-27, actualizado tras N-03/N-04) |
|---|---|
| F-01 (traducción "March Decision Module"/"Auxiliar") — instancias **físicas** (`NEU_EST_UNIG_real`, `NEU_EST_MUL_real`, `NEU_IMU_real`, `NEU_IMU2_real`) | ✅ **Resuelto, aprobado y promovido a `assets/`.** Las 4 figuras se vectorizaron por intensidad de píxel (mismo método, generalizado a layouts multi-columna de 4/8/12 paneles) y ya usan "Gait Decision Module"/"Auxiliary" correctamente. |
| F-01 — instancias **de simulación** (`NEU_EST_UNIB`, `NEU_EST_UNIG`, `NEU_EST_MUL`, `NEU_IMU`, `NEU_IMU2`) | 🔲 Sin empezar — pertenece a `experiments/N-01-simulation-figure-regeneration/` (Grupo 1/2 del Informe 2 §3.4), no a N-02/N-03/N-04. No confundir con lo de arriba. |
| F-02 (rejilla 4×3 de `fig1_*_macro.png`, simulación) | 🔲 Sin empezar — mismo caso, pertenece a N-01. |
| F-03 (fusión `fig5`+`fig6` → panel 1×3) | ✅ **Resuelto, aprobado y promovido** (`fig_classifier_tradeoff_fused.png`, vectorizado). La verificación numérica que este informe dejaba pendiente en §9.3 ya se cerró: el autor confirmó (2026-08-27) que los valores vectorizados son los correctos, y `results.tex:607` se corrigió de SVM-RBF/RF F1=0.900/0.995 (prosa desactualizada) a F1=0.857/0.947 (`patches/n-03-...`). |
| F-04 (doble eje + umbral 3.7 en `GRAPH_IMU`/`GRAPH_IMU2`, **simulación**) | 🔲 Sin empezar — pertenece a N-01. La versión **física** (`GRAPH_IMU_real`/`GRAPH_IMU2_real`) resultó ser un caso distinto (ver F-05), y esa sí está promovida. |
| F-05 (notación $N_0/N_1/N_2$ en `GRAPH_IMU_real`/`GRAPH_IMU2_real`) | ✅ **Resuelto, aprobado y promovido a `assets/`.** Vectorizadas (resultaron ser heatmaps categóricos, no series continuas) con la notación ya incorporada en la imagen. |
| F-06 (reescalar eje Y de `fig4_architecture_ablation.png`) | ✅ **Resuelto, aprobado y promovido a `assets/`.** Regenerada desde los valores ya citados en prosa (`results.tex:598`), sin necesidad de vectorizar. Sin ninguna referencia al ID interno "F-06" en la imagen. |
| — (hallazgo nuevo, no estaba en este informe) | **`*_Real_Plot_2_Basal_Ganglia_Dynamics.png` (12 figuras: 4 escenarios × esta figura) eliminada por decisión del autor**, respondiendo al comentario del revisor "cut repetitive descriptions, duplicated neural raster plots and identical stability curves". Su contenido (firing variance) se fusionó como panel A dentro de `*_Real_Plot_3` (que ahora es un compuesto A+B de 2 paneles, con sombreado rojo/azul de presencia de estímulo en el panel A para Appetitive/Aversive/Complex — NO para Obstacle). ✅ **Las 4 `*_Real_Plot_3` regeneradas están aprobadas y promovidas, y la actualización de `results.tex` (subfigura eliminada de los 4 bloques `figure*`, captions reescritos) ya está aplicada** (`patches/n-03-...`) — ya no es una tarea pendiente. |
| — (hallazgo nuevo) | `FigReal_Morphological_Transition_Energy.png` — **✅ APROBADA (2026-08-27), plan de ejecución listo pero SIN EJECUTAR todavía** — ver §9.7 (nueva). Se descartó la Opción A original (pico inferido de `power_W`) por un hallazgo crítico: la columna `mode` de `Test_current_integrated_*` nunca cambia (siempre `'C'`), así que no ubica transiciones reales. El autor aportó la lógica original de detección (`robot_cmd` filtrado a `{c,z,x}`, ventanas precalibradas 2.92s/1.56s ya publicadas en `FigReal_Terrain_Latencies_4Panels`) — con eso se hallaron **35 transiciones reales** (16 Quad→Diff, 19 Diff→Quad, 1 Quad→Omni descartada por N insuficiente). El autor también confirmó que `current_A` es fiable pero `voltage_V`/`power_W` no — la potencia real se deriva como `\|current_A\| × 7.2V` (paquete NiMH fijo), dando **5.06±2.93 J (N=16) vs. 4.13±1.19 J (N=19)**, diferencia no significativa (Welch t≈1.18). |
| — (hallazgo nuevo, relacionado pero DISTINTO) | **R2-04 del reviewer ("long-term average energy consumption of THREE locomotion modes") — ✅ borrador listo, plan en §9.9, NO EJECUTAR TODAVÍA.** Es distinto de la figura de arriba (esa mide energía de **transición**, esta mide consumo **en estado estable** por modo). Con `Test_current_integrated_*` + `robot_cmd` se calculó: Quadrupedal 1.94±1.77W (N=20 segmentos), Differential Mobile 1.36±0.98W (N=20), Omnidireccional 5.71W (**N=1, placeholder — el equipo confirmó 2026-08-27 que viene una campaña de pruebas dedicada para este modo**). **Decisión del autor: tabla, no gráfica** (más barata de actualizar cuando llegue el dato real de X). Ver `experiments/R2-04-mode-energy/README.md`. |
| M-01–M-04 (discrepancias texto↔figura, §2) | ✅ **Resuelto.** Los 5 pasajes de `results.tex` (Appetitive Targeting, caption `tab:consolidated_simulation_metrics`, Limitations, Tipover Risk, $T_{switch}$/Heaviside + su caption, phase-space + su caption) se reescribieron con los valores reales verificados en Informe 2 §0, envueltos en `\revblue{}` (`patches/n-04-m01-m04-text-redaction.tex`). Ya no es una tarea de redacción pendiente. |
| Tipografía de figuras | Serif (10/11/12pt según elemento) es ahora el estilo **por defecto del proyecto** (`.claude/skills/scientific-visualization/assets/publication.mplstyle`), confirmado contra `assets/fig1_Obstacle_macro.png`. Aplica automáticamente a cualquier figura futura, incluidas las de N-01 cuando se generen. |

**Lo único que sigue abierto de este informe:** F-01/F-02/F-04 en su variante de **simulación** (pertenecen a
`N-01-simulation-figure-regeneration/`, sin empezar), `FigReal_Morphological_Transition_Energy.png` (aprobada,
plan en §9.7, **sin ejecutar por instrucción explícita del autor** — "haz el plan... pero no lo ejecutes aún"),
y la tabla de R2-04 (borrador listo en §9.9, con la fila de Omnidireccional marcada como placeholder N=1 hasta
que llegue la campaña de pruebas dedicada). Todo lo demás listado en este §8 y en el checklist de §9.1–§9.6 está
cerrado.

---

## 9. Tareas de Escritura Sistemáticas (2026-08-27) — para ejecutar HOY

**Estado (2026-08-27): §9.1–§9.5 ya se ejecutaron** (commit `d93adbd`, filas `N-03`/`N-04` en `PROGRESS.md`).
**§9.7 (energía de transición) tiene plan listo pero está bloqueada — el autor pidió explícitamente no
ejecutarla todavía. §9.9 (tabla de consumo por modo, R2-04) tiene plan listo y SÍ puede ejecutarse — con la
fila de Omnidireccional marcada como placeholder N=1 hasta que llegue la campaña de pruebas dedicada
(confirmada por el equipo, en camino).** No incluyen: la reescritura de `*_Real_Plot_2` como texto/estadística
de repetibilidad (sigue sin decidir), ni nada de `experiments/N-01-...` (simulación, no ha empezado). Seguir el
flujo normal del repo: `sections/` + fila de `PROGRESS.md` + `patches/` — nunca editar
`source/main_monolithic.tex` a mano, y correr `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh` antes de
cualquier commit que toque `sections/`.

### 9.1 Promover las 12 figuras aprobadas a `assets/`

Usar `scripts/promote_figure.sh <origen> <destino> [--force]`. Las primeras 9 reemplazan un archivo existente en
`assets/` con el mismo nombre → necesitan `--force`. `fig_classifier_tradeoff_fused.png` es un nombre nuevo → sin
`--force`.

```
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/fig1_confusion_matrix.png assets/fig1_confusion_matrix.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/fig4_architecture_ablation.png assets/fig4_architecture_ablation.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/GRAPH_IMU_real.png assets/GRAPH_IMU_real.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/GRAPH_IMU2_real.png assets/GRAPH_IMU2_real.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/NEU_EST_UNIG_real.png assets/NEU_EST_UNIG_real.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/NEU_EST_MUL_real.png assets/NEU_EST_MUL_real.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/NEU_IMU_real.png assets/NEU_IMU_real.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/NEU_IMU2_real.png assets/NEU_IMU2_real.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/FigReal_Terrain_Latencies_4Panels.png assets/FigReal_Terrain_Latencies_4Panels.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/Appetitive_Real_Plot_1_Switching_Delay_ECDF.png assets/Appetitive_Real_Plot_1_Switching_Delay_ECDF.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/Aversive_Real_Plot_1_Switching_Delay_ECDF.png assets/Aversive_Real_Plot_1_Switching_Delay_ECDF.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/Complex_Real_Plot_1_Switching_Delay_ECDF.png assets/Complex_Real_Plot_1_Switching_Delay_ECDF.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/Obstacle_Real_Plot_1_Switching_Delay_ECDF.png assets/Obstacle_Real_Plot_1_Switching_Delay_ECDF.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/Appetitive_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png assets/Appetitive_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/Aversive_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png assets/Aversive_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/Complex_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png assets/Complex_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/Obstacle_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png assets/Obstacle_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png --force
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/fig_classifier_tradeoff_fused.png assets/fig_classifier_tradeoff_fused.png
```

Después: `git rm assets/Appetitive_Real_Plot_2_Basal_Ganglia_Dynamics.png assets/Aversive_Real_Plot_2_Basal_Ganglia_Dynamics.png assets/Complex_Real_Plot_2_Basal_Ganglia_Dynamics.png assets/Obstacle_Real_Plot_2_Basal_Ganglia_Dynamics.png` (las 4 quedan sin ninguna referencia en `results.tex` una vez aplicado 9.2 — confirmado por grep, `fig:*_bg_real` no se cita en ningún otro punto de la prosa).

### 9.2 `sections/results.tex` — eliminar el panel `_Real_Plot_2` de los 4 bloques `figure*`

Los 4 bloques están en `results.tex` (aprox. líneas 791-905 al momento de este informe — confirmar número exacto
antes de editar, puede haber corrido). Cada uno es un `figure*` con 3 `subfigure` (a, b, c) + una `\caption{}`
externa que narra los 3 paneles a mano. Para cada uno de los 4 (Appetitive, Aversive, Complex, Obstacle):

1. **Borrar por completo** el bloque `\begin{subfigure}...\end{subfigure}` que incluye
   `*_Real_Plot_2_Basal_Ganglia_Dynamics.png` (subfigura "b", con su propio `\caption{Basal ganglia neural
   dynamics.}` y `\label{fig:*_bg_real}`) — y el `\hfill` que lo separaba de la subfigura siguiente.
2. Las 2 subfiguras restantes se re-letran solas (el paquete `subcaption` las numera por posición, no hace falta
   tocar sus captions cortos "Switching delay ECDF."/"Pitch/Roll RMS attitude dynamics.").
3. **Editar el `\caption{}` externo del `figure*`** (la descripción larga "(a)...(b)...(c)..." escrita a mano) —
   quitar la frase "(b) ..." y renombrar "(c)" a "(b)", describiendo que el panel ahora contiene AMBOS: la
   dinámica neuronal (arriba) y la cinemática (abajo). Texto sugerido por escenario (ajustar redacción si no
   fluye, pero mantener el contenido factual exacto):
   - **Appetitive** (`\label{fig:appetitive_real_compound}`): `"(b) Coupled neural and kinematic response: (top) temporal evolution of the basal ganglia firing variance $Var(z)$ with red/blue stimulus-presence shading; (bottom) Roll and Pitch RMS attitude profile throughout the trial."`
   - **Aversive** (`\label{fig:aversive_real_compound}`): `"(b) Coupled neural and kinematic response: (top) neural firing variance $Var(z)$ displaying the dual-peak evasion signature, with red/blue stimulus-presence shading; (bottom) chassis attitude micro-dynamics during and after the evasive manoeuvre."`
   - **Complex** (`\label{fig:complex_real_compound}`): `"(b) Coupled neural and kinematic response: (top) three-phase neural variance profile mapping obstacle avoidance, aversive escape, and appetitive convergence phases, with red/blue stimulus-presence shading; (bottom) step-like attitude excursions during transitions and final stabilisation at ${\approx}\,4^{\circ}$."`
   - **Obstacle** (`\label{fig:obstacle_real_compound}`): `"(b) Coupled neural and kinematic response: (top) massive transient hyper-excitation peak in neural firing variance $Var(z)$ induced by volumetric geometric input (no stimulus-presence shading — this scenario uses a non-chromatic obstacle cue); (bottom) rhythmic Roll RMS expansion during active lateral flanking and post-avoidance stabilisation."`
4. **No tocar** los 4 párrafos `\revblue{\textbf{Appetitive/Aversive/Complex/Obstacle (see Figure~...}}` que
   siguen a cada figura — siguen siendo válidos tal cual, ya narran el contenido combinado sin depender del
   subfigure eliminado. Confirmado por lectura completa de los 4 (líneas ~817, ~847, ~877, ~907).
5. Envolver cada `\caption{}` editado en `\revblue{}` si no lo está ya (regla permanente del proyecto — texto
   materialmente cambiado esta ronda).

### 9.3 `sections/results.tex` — fusión F-03 (clasificador)

Reemplazar los dos bloques `figure` (~líneas 609-614 `fig5_classifier_comparison.png` y ~618-623
`fig6_computational_cost.png`) por uno solo apuntando a `fig_classifier_tradeoff_fused.png`, con
`\label{fig:classifier_tradeoff}`. Actualizar las dos referencias:
- `results.tex:607` `Figure~\ref{fig:classifier_comparison}` → `Figure~\ref{fig:classifier_tradeoff}`
- `results.tex:616` `Figure~\ref{fig:computational_cost}` → `Figure~\ref{fig:classifier_tradeoff}`

⚠️ **No fusionar los dos párrafos de prosa** (F-03 original lo sugería como posible, pero no es sistemático —
requiere criterio editorial). Dejarlos como dos párrafos separados citando la misma figura fusionada.

✅ **Verificación numérica resuelta (2026-08-27).** La prosa original (`results.tex:607`) citaba SVM-RBF F1=0.900
y Random Forest F1=0.995; la extracción por vectorización de `fig5_classifier_comparison.png`
(`experiments/_plotting/vectorized/classifier_fig5.csv`) daba SVM-RBF F1≈0.857 y Random Forest F1≈0.947 — una
diferencia de ~4-5 puntos porcentuales, mayor que el error esperable de una extracción de píxeles bien calibrada.
Las cifras de latencia (`results.tex:616`) sí coincidían casi exactamente con la extracción (1.64 vs. 1.63 µs,
23.5 vs. 23.4 µs, 41.0 vs. 40.7 µs, 0.54 vs. 0.53 µs), lo que ya apuntaba a que solo el panel (a) tenía el
problema. **El autor confirmó que la extracción vectorizada es la correcta y la prosa era la desactualizada**
(mismo patrón que M-01–M-04) — `results.tex:607` ya se corrigió a F1=0.857/0.947, envuelto en `\revblue{}`
(`patches/n-03-physical-figure-promotion-classifier-fusion.tex`, fila `N-03` en `PROGRESS.md`).

### 9.4 `sections/results.tex` — redacción M-01–M-04 (ya verificado, Informe 2 §0)

Reescribir, envuelto en `\revblue{}`, usando exactamente los valores de la tabla en
`intake/pending/R02-01_data_traceability_and_plotting_plan.md` §0 (ya verificados contra `experiments/` — esto
NO requiere más verificación, solo redacción):
- `results.tex:77` (párrafo Appetitive Targeting): quitar "decision latency stays clamped at ≈47 ms", reemplazar
  por una descripción que refleje que la latencia varía con el ruido sensorial (rango real 15 ms–3.07 s, mínimo en
  $\sigma=0$).
- `results.tex:178` (caption `tab:consolidated_simulation_metrics`): quitar "Latency remained constant at ≈47 ms"
  (la tabla no tiene columna de latencia — o se agrega la columna con los valores reales, o se quita la frase).
- `results.tex:276` (párrafo Tipover Risk): reemplazar "$\mu_{TR}\approx 0.42$ ... severe monotonic risk
  escalation ... peak of $TR\approx 0.58$" por el perfil real: plano en TR≈0.58–0.60 en ambos terrenos, sin
  escalada, con un pico transitorio aislado en terreno rugoso (t=-1.3 a -0.5s, hasta TR≈0.77).
- `results.tex:279` (párrafo $T_{switch}$/Heaviside): quitar "invariant at $T_{switch}=0.3$ ms ... completely free
  from chattering" — el terreno rugoso tiene una cola real hasta 600 ms en 13% de los ensayos (2/15); el terreno
  con pendiente tiene una escalera de 5-6 saltos entre 0.8-1.9 ms, no un valor único.
- `results.tex:281` (párrafo phase-space): reemplazar $\mu_\phi/\mu_\theta$ citados y "zero cluster overlap" por
  los valores reales (rugoso: roll≈1.59°, pitch≈1.67°; pendiente: roll≈1.47°, pitch≈2.29°) y reconocer el
  solapamiento real en roll entre ambos terrenos.

### 9.5 Registro en `PROGRESS.md`

Dar de alta filas `N-xx`/`C-xx` (usar `scripts/next_id.sh N` / `scripts/next_id.sh C`, nunca a mano) para: (a) la
promoción de las 12 figuras físicas aprobadas + fusión F-03, `Category: Escritura`, `Data source:
experiments/N-02-physical-figure-regeneration/`; (b) la redacción M-01–M-04, `Category: Escritura`, `Data
source: —` (es solo texto, ya verificado). Actualizar el estado de la fila `N-02` existente a `applied` una vez
promovidas las imágenes y actualizado `results.tex`. Correr `scripts/validate_tex.sh` y
`scripts/check_roundtrip.sh` antes de cualquier commit, como siempre.

### 9.7 `FigReal_Morphological_Transition_Energy.png` — plan de ajuste y redacción

**⚠️ APROBADA por el autor (2026-08-27) — este es el plan de ejecución. NO EJECUTAR TODAVÍA — instrucción
explícita: "haz el plan de ajuste y redacción pero no lo ejecutes aún".** Cuando se autorice ejecutar, es una
tarea sistemática igual que 9.1–9.5 (los números y el método ya están decididos, sin ambigüedad de contenido).

**Qué cambió respecto a la versión rechazada:** el método pasó de "un pico de potencia inferido, sin verificar
contra ningún evento real" a "35 transiciones de modo reales, detectadas por comando estructural
(`robot_cmd` ∈ {`c`,`z`,`x`}, filtrando las teclas direccionales), integradas en la ventana mecánica ya
precalibrada y publicada (2.92s para `z`=Diferencial, 1.56s para `c`=Cuadrúpedo)". La potencia se deriva de
`current_A` (confirmado fiable por el equipo de hardware) × 7.2V (voltaje nominal fijo del paquete NiMH
3300mAh) — **no** de las columnas `power_W`/`voltage_V` originales (esas sí están rotas, magnitud implausible
~1e-4 W). Código: `experiments/_plotting/builders/energy_transition.py` (reescrito, no es un ajuste menor del
anterior). Figura ya regenerada en
`experiments/N-02-physical-figure-regeneration/output/FigReal_Morphological_Transition_Energy.png` — misma
ruta/nombre que la actual en `assets/`, así que la promoción es un simple `--force`.

**Resultados finales (N reales, no inferidos):**

| Dirección | N | Energía (media ± SD) |
|---|---|---|
| Quadrupedal → Differential Mobile (ventana 2.92s) | 16 | 5.06 ± 2.93 J |
| Differential Mobile → Quadrupedal (ventana 1.56s) | 19 | 4.13 ± 1.19 J |

Diferencia entre direcciones **no estadísticamente significativa** (Welch t≈1.18, dos muestras independientes,
varianzas desiguales) — importante para la redacción: no afirmar que una dirección "cuesta más" sin matizarlo.

**1. Promover la figura (mismo nombre, `--force`):**
```
scripts/promote_figure.sh experiments/N-02-physical-figure-regeneration/output/FigReal_Morphological_Transition_Energy.png assets/FigReal_Morphological_Transition_Energy.png --force
```

**2. Reescribir el caption (`results.tex:930`).** Texto actual: *"Energetic footprint of physical
morphological transitions. Integrated INA power telemetry during the Quadrupedal → Differential Mobile and
Differential Mobile → Quadrupedal electromechanical coupling windows, across all hardware replicates."*
Reemplazar por algo que refleje: (a) N reales por dirección, no "all hardware replicates" genérico — ahora son
transiciones individuales detectadas por comando, no una réplica = un punto; (b) el método de derivación de
potencia (`current_A`×7.2V nominal); (c) que la diferencia entre direcciones no es significativa. Ejemplo:
*"Morphological transition energy per direction, derived from `\|`current`\|`$\times$7.2V (fixed NiMH pack
voltage) integrated over the pre-calibrated electromechanical coupling window (2.92s/1.56s, matching
Fig.~\ref{fig:FourPanelLatencies}), across N=16 (Quadrupedal→Differential Mobile) and N=19 (Differential
Mobile→Quadrupedal) individually detected structural-command transitions. Error bars: ±1 SD; the
between-direction difference is not statistically significant (Welch's t≈1.18)."* Envolver en `\revblue{}`.

**3. Reescribir el párrafo (`results.tex:934`).** Texto actual afirma "invariant energetic cost" para
Quad→Diff y "greater dispersion" para Diff→Quad, con una explicación causal (terreno tipo "river-pebble",
deslizamiento de ruedas) escrita para la figura anterior (rechazada). **Con los datos reales, la SD es MAYOR
en Quad→Diff (2.93 J) que en Diff→Quad (1.19 J) — lo opuesto de lo que la prosa actual afirma.** No hay
manera sistemática de conservar la narrativa causal actual sin contradecir el dato — hace falta redactar de
nuevo. Contenido factual mínimo a incluir (dejar la prosa exacta a criterio editorial del agente de
escritura, pero sin inventar una causa mecánica no verificada):
   - $5.06 \pm 2.93$ J para Quadrupedal→Differential Mobile (N=16), $4.13 \pm 1.19$ J para Differential
     Mobile→Quadrupedal (N=19).
   - La diferencia entre direcciones no es estadísticamente significativa — no afirmar que una dirección es
     más costosa/más determinista que la otra como conclusión firme.
   - Método: transiciones reales detectadas por comando estructural de teleoperación (no inferidas de un pico
     de potencia), integradas sobre la ventana de acoplamiento electromecánico ya calibrada.
   - Si se quiere comentar la mayor dispersión en Quad→Diff, hacerlo como observación (p. ej. "greater
     trial-to-trial variability was observed in the Quadrupedal→Differential Mobile direction") sin atribuir
     una causa mecánica específica que no esté verificada contra el terreno/condición real de cada ensayo.

**4. `PROGRESS.md`:** nueva fila `N-xx` (`scripts/next_id.sh N`), `Category: Escritura`, `Data source:
experiments/N-02-physical-figure-regeneration/`, referenciando este §9.7 y
`experiments/_plotting/builders/energy_transition.py`. Actualizar `results.tex(934)` en `Target section(s)`.

**5. Explícitamente fuera de este plan (no hacer al ejecutar esto):** no intentar responder R2-04 (consumo en
estado estable de los 3 modos) como parte de esta tarea — es un gap distinto, ver la fila de §8 arriba.

### 9.9 R2-04 — tabla de consumo por modo (NO gráfica) — plan de integración

**Decisión del autor (2026-08-27):** para el consumo *en estado estable* de los 3 modos (distinto de la energía
de *transición* de §9.7), usar **tabla, no figura** — un bar chart de 3 categorías (una de ellas N=1 y
temporal) no es muy diciente, y una tabla es mucho más barata de actualizar cuando lleguen los datos reales de
Omnidireccional (una fila, no una regeneración de figura). Ver `experiments/R2-04-mode-energy/README.md` para
el método completo y las advertencias.

**⚠️ Dato de Omnidireccional (X) es un placeholder de N=1, con reemplazo confirmado en camino.** El equipo de
hardware confirmó (2026-08-27, verbalmente, tras una reunión) que se van a tomar muestras dedicadas de energía
para el modo Omnidireccional. **Cuando lleguen:** re-correr
`experiments/R2-04-mode-energy/scripts/build_mode_energy.py` contra la(s) carpeta(s) nueva(s) de
`experiments/real/`, la fila de X en la tabla de abajo se actualiza (media±SD/N), nada más del plan cambia. Este
informe/tarea NO debe tratarse como cerrado hasta que esa fila dejede ser N=1.

**Resultado actual (2026-08-27), listo para tabla:**

| Modo | N segmentos | Potencia media ± SD |
|---|---|---|
| Quadrupedal (C) | 20 | 1.94 ± 1.77 W |
| Differential Mobile (H) | 20 | 1.36 ± 0.98 W |
| Omnidireccional (X) | 1 (preliminar, sin réplica — ver advertencia arriba) | 5.71 W |

**1. Nueva tabla en `sections/results.tex`**, cerca de `FigReal_Morphological_Transition_Energy.png` (misma
subsección "ENERGY CONSUMPTION", después del párrafo de esa figura una vez aplicado §9.7), siguiendo el mismo
estilo que `tab:consolidated_physical_metrics` (`tabularx`, mismo formato de `\toprule`/`\midrule`/`\bottomrule`):

```latex
\begin{table}[htbp]
\centering
\caption{Long-term average steady-state power consumption per locomotion mode (three hardware
replicates' worth of instrumented segments; transition windows excluded per segment, see
Fig.~\ref{fig:MorphologicalEnergy}). Power derived as $|I|\times7.2\,\text{V}$ (fixed NiMH pack
voltage). \textbf{Omnidirectional is a single-segment preliminary estimate (N=1), pending a dedicated
test battery.}}
\label{tab:mode_steady_state_energy}
\begin{tabularx}{\textwidth}{l >{\centering\arraybackslash}X >{\centering\arraybackslash}X}
\toprule
\textbf{Locomotion Mode} & \textbf{N (segments)} & \textbf{Mean Power $\pm$ SD (W)} \\
\midrule
Quadrupedal ($C$) & 20 & $1.94 \pm 1.77$ \\
Differential Mobile ($H$) & 20 & $1.36 \pm 0.98$ \\
Omnidirectional ($X$)\textsuperscript{*} & 1 & $5.71$ (no SD, single segment) \\
\bottomrule
\end{tabularx}
\\[2pt]
\footnotesize{\textsuperscript{*}Preliminary — a dedicated Omnidirectional-mode energy test battery is
planned; this row will be updated once that data is available.}
\end{table}
```

Envolver en `\revblue{}` (tabla nueva).

**2. Una frase en el párrafo de energía (`results.tex:934`, después de §9.7)** conectando la tabla con el
pedido del reviewer explícitamente, p. ej.: *"To directly address the reviewer's request for long-term
average energy consumption across locomotion modes, Table~\ref{tab:mode_steady_state_energy} reports the
mean steady-state power draw for each of the three modes, computed by excluding the electromechanical
coupling window from each `robot\_cmd`-detected mode segment; the Omnidirectional estimate is preliminary
pending a dedicated test battery."* No afirmar diferencias significativas entre C y H (Welch t≈1.26, no
significativo).

**3. `PROGRESS.md`:** actualizar la fila `R2-04` existente (no crear una nueva — ya existe, `Owner: Sam`,
`Status: pending`) con: `Data source: experiments/R2-04-mode-energy/`, nota de que Quadrupedal/Differential ya
tienen N=20 cada uno pero Omnidireccional sigue con N=1 pendiente de reemplazo, `Status` sube a `drafted` (no
`applied` — no dar por cerrado mientras X sea un placeholder).

**4. Cuando lleguen los datos reales de Omnidireccional:** actualizar la fila X de la tabla (mean±SD/N),
quitar la nota "preliminary"/el `\textsuperscript{*}` si ya no aplica, subir `R2-04` a `applied` en
`PROGRESS.md`. Registrar como una fila `C-xx` (corrección puntual) en vez de un nuevo `N-xx`, ya que la tabla
y el párrafo ya existirán — solo se actualiza un valor.

### 9.10 Explícitamente FUERA de alcance para hoy (no tocar)

- Contenido de reemplazo en prosa para lo que mostraba `*_Real_Plot_2` como figura independiente — la fusión
  visual en 9.2 ya lo resuelve a nivel de figura; **no inventar además una nueva sección/tabla de
  "repeatability statistics"** sin que el autor lo pida — sigue siendo una decisión de escritura sin tomar (ver
  §8 arriba).
- `FigReal_Morphological_Transition_Energy.png` — plan listo en §9.7, pero **no ejecutar sin autorización
  explícita del autor** (instrucción directa: "no lo ejecutes aún").
- Cualquier cosa de `experiments/N-01-simulation-figure-regeneration/` — no ha empezado la revisión de esas
  figuras todavía.
