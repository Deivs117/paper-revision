# R3-01 / R3-02 — Análisis de la mejor forma de presentar los datos de ablación

**Fase:** Análisis previo a redacción. Este documento **no propone texto ni toca `sections/*.tex`
todavía** — responde solo a "¿cómo usamos mejor la información que ya tenemos?", como paso previo
al plan de redacción (que será un documento separado, una vez esto se discuta/decida).

**Insumo:** `intake/pending/R3-02_ablation_results_handoff.md` (handoff crudo) +
`experiments/R3-02-wta-vs-threshold/README.md` + `experiments/R3-01-basal-ganglia-ablation/README.md`
+ `output/ablation_stats_summary.{json,csv}` + lectura de `methodology.tex` (Basal Ganglia Module,
línea ~154-201) y `results.tex` (estructura de Simulation Results, tabla
`tab:consolidated_simulation_metrics`, subsección de ablación MLP como precedente de formato).

## 1. R3-01 y R3-02 se responden como una sola pieza, no dos

Ya está decidido en los propios READMEs de experimento (no hay que redecidirlo): un solo dataset
de 96 corridas (4 variantes × 2 escenarios × 12 réplicas) cubre ambos comentarios. La forma más
limpia de usarlo es **una sola subsección nueva** en el paper que presente las 4 variantes juntas,
con la lectura narrativa dividida en dos mitades que mapean 1:1 a los dos reviewers:

- **R3-01** ("ablation analysis on basal ganglia arbitration network") → `no_lateral_inhibition`
  (conexiones) + `no_stn_str` (capas) vs. `full`.
- **R3-02** ("removing... to justify WTA over threshold logic") → `threshold_only` vs. `full`,
  con el contraste adicional (ya señalado en `OUTLINE.md`) de que el propio Módulo de Locomoción
  ya usa lógica de umbral en otro punto del diseño (cono frontal 20°, `Ar=28.0`) — un gancho
  narrativo gratis, ya está en el paper, no hay que inventarlo.

Escribir dos subsecciones separadas duplicaría método, tabla y figura para el mismo dataset — el
mismo patrón de redundancia que R2-01 ya está corrigiendo en otras partes del paper. Evitarlo aquí
desde el diseño, no como limpieza posterior.

## 2. Dónde va cada pieza

- **`methodology.tex` (Basal Ganglia Module, ~línea 154-201):** un párrafo corto describiendo el
  método de ablación (las 4 variantes, qué desactiva cada una) — no los resultados. Candidato
  natural: justo antes o después del párrafo existente que cita a Gurney2001a/b y
  Prescott2006Robot como justificación puramente teórica del diseño WTA. Ese párrafo hoy afirma la
  superioridad del circuito solo por autoridad de cita; con la ablación lista, puede
  actualizarse para decir que la ventaja además **se mide** en este trabajo, con
  `\ref{}` a la subsección de resultados — mismo patrón que ya se usó en `C-15` (reemplazar la
  cifra "~47ms" no trazable por los dos números reales de latencia ya verificados). Es una edición
  a un párrafo existente, no una subsección nueva en methodology.
- **`results.tex` (Simulation Results):** una subsubsección nueva con tabla(s) + figura(s) — el
  lugar natural es después del párrafo de "Complex Navigation" (línea ~132, que ya reusa ese mismo
  escenario) y antes de "Quantitative Stability Analysis of Locomotion Mode Transitions", ya que
  esta última mide algo distinto (transiciones de modo, no ablación de arbitraje) y no debería
  interrumpirse. **Importante para no sobre-prometer alcance:** este dataset es solo de simulación
  — no hay ablación física — así que el texto debe dejarlo explícito (ninguna otra parte de
  Simulation/Physical Results mezcla ambas fuentes sin decirlo).

## 3. Qué tabla(s)/figura(s) usar (y cuáles no)

**Tabla de tasa de éxito** (la pieza central): 4 variantes × 2 escenarios + p de Fisher vs. `full`,
igual a la que ya está armada en el README del experimento. Es autocontenida y ya tiene el formato
correcto para convertirse en tabla LaTeX (estilo `tabularx` como `tab:consolidated_simulation_metrics`,
reutilizando el mismo patrón visual en vez de inventar uno nuevo).

**Tabla o panel de métricas continuas — solo para Complex Navigation**, no para Appetitive: en
Appetitive ninguna métrica difiere significativamente de `full` (es el resultado esperado — "la
ablación no rompe el caso simple" — y basta una frase, no una tabla completa). Meter Appetitive en
la misma tabla que Complex diluye la señal real; mejor una tabla y una mención de una línea para el
caso nulo.

**Figura recomendada:** un gráfico de barras agrupadas de tasa de éxito por variante × escenario
(paralelo directo a `fig4_architecture_ablation.png`, que ya usa exactamente este lenguaje visual
para la ablación de arquitectura del MLP — mismo tipo de comparación, mismo repo, ya hay precedente
de estilo que seguir). Un segundo panel (o figura separada) con `roll_rms`/`pitch_rms` por variante
en Complex Navigation, con asteriscos/anotación de significancia, cubre el argumento de estabilidad
sin necesitar una tabla numérica adicional en el cuerpo del texto (los números exactos van a pie de
figura o a la tabla, no repetidos en prosa).

**Qué NO mostrar como resultado propio:**
- **λ (`exp_lambda`):** sale 1.0 en las 96 corridas por una limitación conocida y documentada del
  instrumento de medición (`_compute_lambda_efficiency` no captura conflicto real en la ventana
  de muestreo), no porque el efecto no exista. Presentarlo en una tabla de resultados sin ese
  contexto se leería como "la ablación no afecta la eficiencia de conflicto", que es lo opuesto de
  lo que dicen las demás métricas. Recomendación: **omitir de toda tabla/figura de resultados**, y
  si se menciona, que sea una sola frase de limitación (ya hay dos párrafos de limitación
  documentando esto en el README — no hace falta traerlos al paper en detalle, la limitación en sí
  ya está justificada y aceptada como "no arreglar en esta pasada").
- **`firing_variance`/`temporal_consistency`:** no existen en el dataset (bug conocido de
  `test_manager.py`, deliberadamente no corregido 2026-08-31). No inventar ni aproximar estos
  números — la comparación `threshold_only` vs. `full` debe sostenerse solo en lo que sí está
  medido (latencia + roll/pitch RMS), no en lo que se especula que mostraría "oscilación cerca del
  umbral" si se tuviera el dato.

## 4. Rigor estadístico — el punto que más fácil se presta a sobreventa

El propio handoff ya marca esto dos veces como advertencia explícita para cuando se redacte, así
que conviene tratarlo como restricción de diseño, no solo de redacción:

- `threshold_only` en Complex Navigation: tasa de éxito 83.3% vs. 100%, **p=0.478 (no
  significativo)**. El argumento contra `threshold_only` **no puede apoyarse en la tasa de éxito**
  — se apoya en latencia (p=0.014) y `roll_rms`/`pitch_rms` (p=0.017 / p=0.0029), que sí son
  significativas. Cualquier redacción debe nombrar el p no significativo de éxito explícitamente
  en vez de omitirlo (omitir un p n.s. cuando se reportan los otros tres como significativos es
  exactamente el tipo de sobreventa que el handoff pide evitar).
- `no_lateral_inhibition` y `no_stn_str` sí tienen tasa de éxito significativa (p=0.00034 y
  p=0.00135) — para estas dos, la tasa de éxito **sí** es la métrica principal a destacar, con
  `roll_rms`/`pitch_rms` como refuerzo. Ninguna de las dos degrada la latencia de forma
  significativa (p=0.84 / n.s.) — esto también hay que decirlo, no silenciarlo, porque es parte de
  la lectura conjunta interesante: la arbitración tardía no es el modo de falla del circuito
  dañado, sí lo es del reemplazo por umbral.
- n=12 réplicas por celda es razonable para Fisher/Mann-Whitney pero modesto — no presentar los
  resultados con lenguaje que implique una muestra grande; los propios intervalos de confianza
  (ya calculados en el CSV) deberían acompañar las medias en vez de solo el p-valor, donde el
  espacio lo permita.

## 5. Puntos de "a triage" del handoff — recomendación de análisis, no decisión final

Estos quedan explícitamente para que el equipo decida, pero el análisis dice lo siguiente sobre
cada uno:

- **¿Arreglar `_compute_lambda_efficiency()` y re-correr?** No parece necesario para responder a
  R3-01/R3-02 — el argumento ya es sólido sin λ (tasa de éxito + latencia + roll/pitch RMS). Vale
  la pena solo si en algún momento se quiere reportar "eficiencia de conflicto" como métrica propia
  en otra parte del paper, no específicamente para esta comparación.
- **¿Capturar `firing_variance`/`temporal_consistency` y re-correr 48 corridas (~2h)?** Reforzaría
  específicamente el caso `threshold_only`, pero el argumento actual (latencia + estabilidad,
  ambos significativos) ya es suficiente para sostener la afirmación central del reviewer sin esa
  corrida adicional. Es una mejora de robustez, no un bloqueo — recomendación: dejarlo como
  limitación documentada (ya está redactado así en el README) y no re-correr, salvo que el equipo
  quiera un argumento más fuerte que "no significativo en esta métrica sola, significativo en
  estas otras dos".
- **¿Cuánto texto en `methodology.tex` vs. `results.tex`?** Ver §2 arriba — método breve en
  methodology (edición de un párrafo existente + referencia cruzada), resultados completos
  (tabla+figura+prosa) en results, siguiendo el mismo reparto que ya usa el paper en todos los
  demás pares método/resultado (p. ej. Gait Decision Module ↔ Evaluation of the MLP-based terrain
  classifier).

## 6. Siguiente paso

Con esto decidido/discutido, el plan de redacción concreto (qué frases, qué tabla LaTeX exacta, qué
script de figura en `experiments/R3-02-wta-vs-threshold/scripts/`, qué fila de `PROGRESS.md`) va en
un documento aparte — este análisis es insumo para ese plan, no el plan en sí.
