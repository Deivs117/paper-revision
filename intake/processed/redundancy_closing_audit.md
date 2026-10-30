# Auditoría final multi-autor — antes de compilar/enviar (reestructurada 2026-09-02)

**Estado: 🟢 Lista para ejecutar.** Las 6 filas que bloqueaban esta tarea (`R2-02`/`R3-01`/`R3-02`/
`R3-04`/`R3-05`/`R3-06`) ya están en `synced-to-overleaf` — la condición que originalmente la
pausaba ya se cumplió. Este es el ÚLTIMO paso antes de la compilación/envío final.

**Nota (2026-09-02, al mergear):** la versión *original* y más angosta de este mismo documento
(solo redundancia, no las 4 categorías de abajo) ya se ejecutó de forma independiente el
2026-08-31 — ver §6 para ese resultado (`C-23`/`C-24`, ambos `applied`). Las 4 sesiones de esta
reestructuración no necesitan repetir esos dos hallazgos puntuales, pero sí deben releer las 6
secciones completas igual: el alcance de esta pasada es más amplio (4 categorías, no solo
redundancia) que el de la corrida original.

**Reestructurada 2026-09-02** (instrucción directa del autor) — cambios respecto a la versión
original de este documento:
1. **Ejecución multi-sesión, un autor por máquina/sesión de Claude Code en la nube**: Diego,
   Sebas, Samuel y Deivi corren esta MISMA tarea, cada uno de forma independiente, en su propia
   sesión. No es una tarea de un solo autor.
2. **Alcance ampliado** — ya no es solo redundancia. Cada sesión escanea el paper completo
   buscando las 4 categorías de la Sección 2 (inconsistencias de datos, redundancia de datos,
   candidatos a acortar, ortografía/convenciones académicas).
3. **Esta pasada es de HALLAZGOS, no de corrección directa.** Cada sesión produce su propio
   archivo Markdown nuevo en `intake/pending/` (no edita `sections/*.tex` en esta pasada) — ver
   Sección 4 para el nombre exacto. Los 4 archivos se consolidan después, en una sesión aparte,
   antes de convertir cualquier hallazgo real en filas `C-xx` y patches.

## 0. Comentario textual del Revisor 2 (ancla, igual que R2-01 lo usó)

> "However the paper is overly verbose with repeated content, and several minor supplements are needed: Stream
> the whole manuscript heavily: Cut repetitive descriptions, duplicated neural raster plots and identical
> stability curves between simulation and physical tests; merge unified metric definitions to avoid restating
> multiple times, and shorten the symbolic warehouse simulation section."

`R2-01` (Sebas) ya lo resolvió una vez de forma completa y documentada (`PROGRESS.md`, 4 rondas de pasada
completa sobre las 6 secciones, `results.tex` 9668→8524 palabras). Esta auditoría no repite ese trabajo desde
cero — pero como el alcance ahora es el paper completo (no solo lo añadido después de `R2-01`), cada sesión sí
debe releer todo, no solo los cambios recientes: una restatement puede existir entre texto viejo y texto nuevo,
no solo dentro de lo nuevo.

## 1. Contexto — todo lo que se añadió desde que R2-01 cerró (commit `51c07b4`)

Cada fila fue individualmente justificada, pero el efecto acumulado es exactamente el tipo de crecimiento que
hay que vigilar — y es la superficie más probable donde aparezcan los hallazgos de la Sección 2:

| Fila | Qué añadió |
|---|---|
| `N-01` | Caption + prosa nueva para la rejilla fusionada de simulación, con disclosure de vectorización del panel Obstacle |
| `N-04` | Reescritura de 5 párrafos (M-01–M-04) |
| `N-05` | Párrafo + tabla nueva de energía de transición + consumo por modo (R2-04) |
| `N-06`/`N-07`/`N-08` | Correcciones de imagen (sin prosa nueva significativa, pero confirmar) |
| `C-07` | Limpieza editorial — en teoría reduce, confirmar que no añadió neto |
| `R3-06` | Tabla comparativa nueva + reformulación de prosa en `introduction.tex` — el más grande, alto riesgo si no se coordinó bien con el párrafo ya existente de la línea 9 |
| `R2-02` | Subsección nueva completa (metodología + resultados FSM), tabla de 7 familias, 4 figuras nuevas |
| `R3-01`/`R3-02` | Estudio de ablación de ganglios basales (subsección + 2 tablas + 2 figuras) |
| `R3-04` | Batería de robustez a ruido combinado (rejilla 4×4, 4 figuras de micro-dinámica, tabla de fallos, evidencia de camera dropout) |
| `R3-05` | Subsección Reactive Inspection Task, ampliada por `R2-02`'s Familia E |
| `C-20` | Párrafo nuevo de metodología para la tarea de inspección |
| `C-21`/`C-22` | Correcciones de figuras (oclusión de texto) y reconciliación de `tab:consolidated_simulation_metrics` — cambios de números/imágenes, no de prosa nueva, pero confirmar que no dejaron ninguna cifra vieja huérfana en otro lado del paper |
| `C-23`/`C-24` | Redundancy-closing audit original (angosta), ya ejecutada — ver §6 |
| `C-25`–`C-30` | Reviewer-simulation trim audit + figure-merge audit, ya ejecutadas (caption trims, fusión de párrafos de cierre, fusión de figuras) |

`scripts/check_word_growth.sh` (wired en `scripts/push_to_overleaf.sh`) da visibilidad continua del conteo de
palabras por sección en cada push — no reemplaza esta auditoría, solo ayuda a priorizar qué sección releer
primero si creció mucho más de lo esperado.

## 2. Las 4 categorías a buscar (todas las sesiones cubren las 4)

### 2.1 Inconsistencias de datos
Números, porcentajes, o afirmaciones que se contradicen entre sí en distintas partes del paper, o que
contradicen los datos fuente en `experiments/`. Ejemplo del tipo de problema ya resuelto una vez en esta ronda:
`C-22` (números de `tab:consolidated_simulation_metrics` que no coincidían con los recalculados desde datos
crudos). Buscar el mismo patrón en cualquier otra cifra citada más de una vez.

### 2.2 Redundancia de datos / contenido duplicado
Mismo hallazgo que `R2-01` ya perseguía, pero sobre el paper completo actual: definiciones de métricas
restablecidas en más de un lugar, descripciones repetidas, curvas de estabilidad casi idénticas entre
simulación y físico. **Hallazgo ya identificado que hay que re-visitar con criterio fresco:** Grupo B del
informe `figure-redundancy-audit.pdf` (ver `intake/processed/figure-redundancy-audit-triage.md`) señaló que
los pares de rasters `NEU_IMU`/`NEU_IMU2` (simulación) vs. sus versiones `_real` (físico) tienen layout casi
idéntico. Esto es más relevante ahora que cuando se escribió el backlog original — `R02-01-05` vectorizó y
pulió las versiones de simulación desde entonces, así que hoy ambos lados del par están más pulidos y más
parecidos visualmente entre sí de lo que estaban antes. Decidir si siguen siendo pares legítimos de validación
sim→real o si conviene fusionar/condensar alguno. **Nota:** `C-29`/`C-30` (figure-merge audit) ya revisaron y
fusionaron el par físico `NEU_IMU_real`/`NEU_IMU2_real`; el par de simulación se mantuvo sin fusionar
(letras "(a)"/"(b)" ya horneadas en el PNG) — confirmar con ojos frescos si esa decisión sigue siendo correcta.

### 2.3 Candidatos a acortar (tablas/figuras)
Tablas o figuras que se podrían condensar, fusionar, o presentar de forma más compacta **sin perder validez
estadística ni capacidad de comunicar el resultado**. Para cada candidato, proponer concretamente CÓMO
acortarlo (fusionar dos tablas, convertir una tabla dispersa en una figura, resumir columnas redundantes), no
solo señalar que "es largo". Revisar en particular:
- La tabla nueva de `R3-06` (`tab:action_selection_comparison`) — confirmar que no reintroduce en tabla lo que
  la línea 9 de `introduction.tex` ya dice en prosa (el plan de `R3-06` ya advertía esto explícitamente).
- La sección de simulación del "warehouse" (nombrada explícitamente por el Revisor 2, ya acortada por `R2-01`)
  — confirmar que ninguna fila nueva desde entonces le devolvió prosa.

### 2.4 Ortografía, convenciones académicas, y nombres filtrados del repositorio
- Ortografía y gramática en inglés académico (el paper es en inglés) — errores tipográficos, concordancia,
  puntuación, consistencia de términos técnicos (mismo término para el mismo concepto en todo el documento).
- Convenciones de formato académico: uso consistente de mayúsculas en títulos de sección/figura/tabla,
  formato de citas, notación matemática consistente, capitalización de nombres propios del sistema.
- **Nombres crudos del repositorio filtrados a texto legible por el lector** (regla README.md §11.1, ya
  aplicada proactivamente en rondas anteriores pero vale la pena una pasada final dedicada): nombres de
  carpeta (`familia_a_apetitivo`, `test_NNN_SUCCESS`), nombres de columna de CSV, rutas de archivo, nombres de
  script — cualquier identificador que solo tiene sentido dentro del repositorio de desarrollo, no en el paper
  publicado. Buscar especialmente en captions de figuras/tablas añadidas en las filas nuevas listadas en la
  Sección 1 — son las más recientes y las que menos rondas de revisión han tenido.

**Explícitamente FUERA de esta pasada:** una revisión de estilo de escritura línea por línea más profunda
(fraseo, tono, nivel de formalidad más allá de errores concretos) queda para una sesión aparte — esta pasada
busca errores concretos y localizables, no una reescritura editorial.

## 3. Método (mismo rigor que R2-01, no un vistazo rápido)

1. Releer las 6 secciones completas (`introduction.tex`, `methodology.tex`, `results.tex`, `conclusions.tex`,
   `preamble.tex`, `closing.tex`) de principio a fin — no solo diffs recientes.
2. Para cada afirmación/definición de métrica que aparece en más de un lugar, aplicar el mismo criterio que
   `R2-01` ya estableció (ver su fila en `PROGRESS.md` para el patrón: mención de establecimiento + referencia
   cruzada de las repeticiones, no restatement completo).
3. Correr `scripts/check_word_growth.sh` como punto de partida para priorizar qué secciones releer primero, no
   como sustituto de la relectura completa.
4. Documentar cada hallazgo con: ubicación exacta (archivo + línea o `\label{}` cercano), categoría (2.1–2.4),
   descripción concreta del problema, y una sugerencia de corrección (sin aplicarla todavía).

## 4. Entregable de cada sesión

**No editar `sections/*.tex` en esta pasada.** Cada autor escribe sus hallazgos en un archivo Markdown nuevo,
propio, en `intake/pending/`:

```
intake/pending/final_audit_<autor>_2026-09-XX.md
```

donde `<autor>` es uno de `diego`, `sebas`, `samuel`, `deivi` (usar la fecha real de ejecución). Estructura
sugerida dentro de cada archivo: una sección por categoría (2.1–2.4), cada hallazgo como una entrada con
ubicación + descripción + sugerencia. Si una sesión no encuentra nada en una categoría, decirlo explícitamente
("2.1 — sin hallazgos") en vez de omitir la sección, para que la consolidación sepa que sí se revisó.

## 5. Consolidación (sesión aparte, después de que existan los 4 archivos)

Una vez estén los 4 archivos `final_audit_*.md`, una sesión de consolidación:
1. Cruza los 4 documentos, agrupa hallazgos duplicados (varios autores probablemente van a encontrar lo mismo).
2. Para cada hallazgo real confirmado, un patch — un patch por hallazgo, wrapped en `\revblue{}` solo si cambia
   contenido (una fusión de párrafos sí cuenta, un ajuste de una palabra no).
3. Registrar como fila(s) `C-xx` en `PROGRESS.md` (`scripts/next_id.sh C`), `Category: Escritura`,
   referenciando los 4 documentos de origen.
4. `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh` antes de cualquier commit.
5. Mover los 4 `final_audit_*.md` a `intake/processed/` solo cuando esas filas `C-xx` lleguen a `applied` — no
   antes.

## 6. Resultado de la ejecución de la versión original y angosta (2026-08-31)

**Este §6 documenta la corrida angosta (solo redundancia) que ya se ejecutó antes de la reestructuración
multi-autor de arriba — sirve como antecedente, no como sustituto de la pasada de las 4 categorías.**

Se leyeron completas las 6 secciones (introduction/methodology/results/conclusions/preamble/closing)
con ojos frescos, no solo el diff desde `R2-01`. Baseline de páginas para esta corrida:
`51c07b4` (cierre de R2-01) compiló a **86 páginas**; el estado actual (post `R2-01`..`C-19`,
antes de este audit) compiló a **91 páginas** (+5).

**Hallazgos reales de redundancia (fijados):**

1. **`C-23`** — results.tex, subsección Limitations: el párrafo "Regarding the Reactive Inspection
   Task..." (añadido por `R3-05`) restablecía casi palabra por palabra 4 hechos ya establecidos en
   los propios párrafos de resultados de esa tarea (sin path planning/mapa; coverage rate no
   reportado + por qué; visual pursuit condicionado a ausencia de obstáculo frontal;
   $T_{acquisition}$ es primera adquisición no re-adquisición). Condensado a mención + referencia
   cruzada, mismo patrón que `R2-01` ya estableció.
2. **`C-24`** — conclusions.tex, párrafo de basal ganglia: re-explicaba el mecanismo STN/GPe/GPi/STR
   winner-take-all ya descrito en methodology.tex's Basal Ganglia Module. Este par ya se había
   identificado durante `C-12` (ofrecido como opción, no elegida esa ronda) — ejecutado ahora.
   Condensado a referencia cruzada + el contenido específico de resultados (latencia de 600ms,
   hipótesis de cierre) intacto.

**Puntos del método (§3) revisados, sin acción necesaria:**

- **§2 / Grupo B (rasters `NEU_IMU`/`NEU_IMU2` sim vs. `_real`):** releídos con ojos frescos. Las
  narrativas describen eventos distintos (tiempos, disparadores — sim: superar umbral $\sigma_{az}$
  directamente; físico: señal de estancamiento sostenida) contadas con un paralelismo estructural
  intencional (par de validación sim→real), no restatement verbatim. Se mantienen como pares
  legítimos, sin fusionar — confirma la lectura original del backlog, revisada explícitamente en
  vez de asumida.
- **Tabla `R3-06` (`table:action_selection_comparison`) vs. párrafo de la línea 9:** confirmado que
  no reintroduce contenido — la línea 9 es fact + forward pointer ("the rationale ... is given
  below"), el párrafo CPG (línea ~32) da la razón. Estructura correcta, ya arreglada por `C-14`.
- **Sección "warehouse" (Gazebo depot):** mencionada 3 veces (intro de resultados, caption de la
  figura, párrafo de Limitations) pero cada mención tiene función distinta (forward-pointer,
  caption, caveat detallado) — no hay restatement de prosa. Sin cambios.
- **QuantReal (4 escenarios físicos) vs. Simulation Results (4 escenarios sim):** el paralelismo
  estructural es intencional (mismo protocolo, sim vs. hardware) y ya fue condensado agresivamente
  por `R2-01`/`C-14` (plantilla de 3 párrafos → 1 párrafo por escenario, "Quantitative metrics are
  consolidated in..." des-duplicado 4x → 1x). No se encontró restatement adicional.

**Por qué el conteo de páginas no bajó (91 páginas antes y después de `C-23`/`C-24`):** los ~140
palabras cortadas entre ambos hallazgos no cruzan un salto de página en una sección tan dominada por
figuras/tablas flotantes como `results.tex`. El crecimiento real de páginas desde `R2-01` (+5,
86→91) viene abrumadoramente de **contenido nuevo genuino** (N-01/04/05/06/07/08/09, R3-05, R3-06),
no de redundancia de prosa — `C-19` ya consolidó lo más obvio a nivel de figura (4 floats MLP → 1
grid `figure*`). Bajar páginas de forma medible ahora requeriría decisiones editoriales más grandes
(consolidar más figuras/tablas, o recortar contenido) que exceden el alcance de una auditoría de
redundancia y necesitan una decisión explícita del autor sección por sección.

**Pendiente para cuando lleguen R2-02/R3-01/R3-02/R3-04:** esta auditoría no repite entonces — solo
hay que revisar que la integración de esas filas no *cree* redundancia nueva con lo que ya existe
(mismo riesgo que este documento señaló desde el principio en la tabla de §1). **Actualización:** esas
4 filas ya llegaron a `synced-to-overleaf` — de ahí la reestructuración multi-autor de la cabecera de
este documento, que retoma esa revisión pendiente con alcance ampliado.
