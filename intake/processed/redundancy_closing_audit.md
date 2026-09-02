# Auditoría de redundancia final — antes de compilar/enviar (2026-08-31) — EJECUTADA

**Estado: ✅ Ejecutada 2026-08-31, author-requested antes de que todas las filas `Pruebas` (R2-02/
R3-01/R3-02/R3-04) hubieran aterrizado** — el autor pidió correrla de una vez en vez de esperar,
explícitamente para bajar el conteo de páginas si era posible. Resultado: 2 hallazgos reales de
redundancia (`C-23`, `C-24`, ambos `applied`), el resto de los puntos del método (§2–§5 abajo)
revisados con ojos frescos y confirmados sin acción necesaria. Ver §6 (nuevo) para el resultado y
qué queda pendiente para R2-02/R3-01/R3-02/R3-04 cuando lleguen.

**Origen:** pregunta directa del autor — "hay forma de seguir auditando estas correcciones para que no sean
contraproducentes en nuestra labor de sintetizar el paper", citando el comentario original del Revisor 2 que
`R2-01` ya resolvió una vez.

## 0. Comentario textual del Revisor 2 (ancla, igual que R2-01 lo usó)

> "However the paper is overly verbose with repeated content, and several minor supplements are needed: Stream
> the whole manuscript heavily: Cut repetitive descriptions, duplicated neural raster plots and identical
> stability curves between simulation and physical tests; merge unified metric definitions to avoid restating
> multiple times, and shorten the symbolic warehouse simulation section."

`R2-01` (Sebas) ya lo resolvió una vez de forma completa y documentada (`PROGRESS.md`, 4 rondas de pasada
completa sobre las 6 secciones, `results.tex` 9668→8524 palabras). **Este documento no repite ese trabajo** —
audita específicamente si algo de lo añadido *después* de que `R2-01` cerró (commit `51c07b4`) reintrodujo el
mismo problema.

## 1. Por qué esto es un riesgo real, no solo precaución

Desde que `R2-01` cerró, se añadió contenido nuevo en cada una de estas filas — cada una individualmente
justificada, pero el efecto acumulado es exactamente el tipo de crecimiento que hay que vigilar:

| Fila | Qué añadió |
|---|---|
| `N-01` | Caption + prosa nueva para la rejilla fusionada de simulación, con disclosure de vectorización del panel Obstacle |
| `N-04` | Reescritura de 5 párrafos (M-01–M-04) |
| `N-05` | Párrafo + tabla nueva de energía de transición + consumo por modo (R2-04) |
| `N-06`/`N-07`/`N-08` | Correcciones de imagen (sin prosa nueva significativa, pero confirmar) |
| `C-07` | Limpieza editorial — en teoría reduce, confirmar que no añadió neto |
| `R3-06` (en curso) | **Tabla comparativa nueva + reformulación de prosa en `introduction.tex`** — el más grande de los pendientes, alto riesgo si no se coordina bien con el párrafo ya existente de la línea 9 |
| `R2-02`/`R3-01`/`R3-02`/`R3-04`/`R3-05` (por integrar, datos llegan el domingo) | Contenido completamente nuevo — no existía antes, no hay redundancia previa que auditar, pero sí hay que revisar que la integración no *cree* redundancia con lo ya existente |

`scripts/check_word_growth.sh` (nuevo, wired en `scripts/push_to_overleaf.sh`) da visibilidad continua del
conteo de palabras por sección en cada push — **no reemplaza esta auditoría**, solo la hace más fácil de
priorizar (si una sección creció mucho más de lo esperado para el contenido que se supone que se le añadió, es
la primera candidata a releer aquí).

## 2. Hallazgo ya identificado que esta auditoría debe re-visitar explícitamente

**Grupo B del informe `figure-redundancy-audit.pdf`** (ver `intake/processed/figure-redundancy-audit-triage.md`)
ya señaló esto y se dejó como backlog explícito: los pares de rasters `NEU_IMU`/`NEU_IMU2` (simulación) vs. sus
versiones `_real` (físico) tienen layout casi idéntico. **Esto ahora es más relevante que cuando se escribió el
backlog** — desde entonces, `R02-01-05` vectorizó y pulió las versiones de simulación (`N-06`/`N-08`), así que
hoy ambos lados del par están más pulidos y visualmente más parecidos entre sí de lo que estaban antes. El
Revisor 2 nombra literalmente "duplicated neural raster plots... between simulation and physical tests" — esta
auditoría debe decidir con criterio fresco si, ahora que ambos lados están terminados, siguen siendo pares
legítimos de validación sim→real (la lectura original) o si conviene fusionar/condensar alguno, en vez de asumir
la conclusión de hace varios días sin revisarla.

## 3. Método (mismo rigor que R2-01, no un vistazo rápido)

1. Releer las 6 secciones completas (`introduction.tex`, `methodology.tex`, `results.tex`, `conclusions.tex`,
   `preamble.tex`, `closing.tex`) — no solo los diffs desde `R2-01`, porque una restatement puede ocurrir entre
   texto viejo y texto nuevo, no solo dentro de lo nuevo.
2. Para cada afirmación/definición de métrica que aparece en más de un lugar, aplicar el mismo criterio que
   `R2-01` ya estableció (ver su fila en `PROGRESS.md` para el patrón: mención de establecimiento + referencia
   cruzada de las repeticiones, no restatement completo).
3. Revisar específicamente el §2 de este documento (rasters sim/físico) con ojos frescos.
4. Revisar que la tabla nueva de `R3-06` (`tab:action_selection_comparison`) no reintroduzca en tabla lo que el
   párrafo de la línea 9 de `introduction.tex` ya dice en prosa — deben complementarse, no decir lo mismo dos
   veces (el plan de `R3-06` ya lo advierte explícitamente, confirmar que se ejecutó así).
5. Revisar la sección de simulación del "warehouse" (Referee 2 la nombra explícitamente, ya acortada por
   `R2-01`) — confirmar que ninguna fila nueva le añadió prosa de vuelta.
6. Correr `scripts/check_word_growth.sh` como punto de partida para priorizar qué secciones releer primero, no
   como sustituto de la relectura.

## 4. Al ejecutar

- Cualquier condensación encontrada sigue el mismo patrón que `R2-01`: un patch por hallazgo, wrapped en
  `\revblue{}` solo si cambia contenido (una fusión de párrafos sí cuenta, un ajuste de una palabra no).
- Registrar como fila(s) `C-xx` en `PROGRESS.md` (`scripts/next_id.sh C`), `Category: Escritura`, referenciando
  este documento.
- `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh` antes de cualquier commit.
- Mover este documento a `intake/processed/` solo cuando esas filas `C-xx` lleguen a `applied` — no antes.

## 6. Resultado de la ejecución (2026-08-31)

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
(mismo riesgo que este documento señaló desde el principio en la tabla de §1).
