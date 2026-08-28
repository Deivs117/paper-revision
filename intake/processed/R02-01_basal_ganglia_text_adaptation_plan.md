# R02-01 — Plan de adaptación textual por eliminación de `*_Real_Plot_2_Basal_Ganglia_Dynamics.png`

**Fecha:** 2026-08-27
**Fase:** Estrategia de reescritura y adaptación argumentativa por eliminación de figuras (mecanismo del ganglio basal).

## 0. Hallazgo previo — esta tarea ya está resuelta en el manuscrito

Antes de proponer redacción nueva, se auditó `sections/results.tex` completo (`grep` de
`Real_Plot_2`, `Basal_Ganglia_Dynamics`, "basal ganglia") y el historial de commits. Resultado: **la
sustitución argumentativa que pide este informe ya fue ejecutada**, en dos capas distintas y en dos
momentos distintos:

1. **La narrativa textual ya existía desde una ronda de revisión anterior** (commit `9df8395`,
   *"consolidate physical multi-stimuli scenario metrics into a table"*) — los 4 párrafos
   `\textbf{Appetitive/Aversive/Complex/Obstacle (see Figure~...)}` en `results.tex` (líneas
   ~803–876) ya describían en prosa el patrón de `Var(z)` (pico único, doble pico, tres fases,
   etc.) y su interpretación fisiológica/mecánica **independientemente de la figura** — nunca
   dependieron solo de que el lector mirara el panel.
2. **La figura y sus captions se fusionaron/limpiaron en el commit `d93adbd`** (N-03, 2026-08-27):
   se eliminó el subfigure `*_Real_Plot_2_Basal_Ganglia_Dynamics.png` de los 4 bloques
   `figure*` físicos, y su contenido (evolución temporal de `Var(z)`) se fusionó verticalmente
   dentro del panel (b) ya existente (RMS de Roll/Pitch), añadiendo sombreado rojo/azul de
   presencia de estímulo. Los captions se reescribieron para describir el panel compuesto.
3. **La métrica agregada ya está en una tabla**: `Table~\ref{tab:consolidated_physical_metrics}`
   (línea 877+) tiene una columna `Var(z) peak` con el valor/patrón cualitativo-cuantitativo por
   escenario (p. ej. Obstacle: `≈1100, transient (t<7s)`; Complex: `Three-phase, peak >30,000`).

`grep -rln "Real_Plot_2" sections/ assets/ OUTLINE.md` no devuelve **ninguna** coincidencia — no
queda ninguna referencia colgante a la familia de figuras eliminada en ningún archivo del
manuscrito activo.

**Conclusión:** no hace falta redactar párrafos nuevos para "compensar" la eliminación — el
argumento científico nunca dependió solo de la figura y ya fue reforzado. Lo que sigue documenta
el mapeo de impacto y el before/after real, como registro de auditoría, y señala el único punto
opcional que queda abierto.

## 1. Mapeo de impacto

| Escenario | Bloque afectado | Qué cambió | Commit |
|---|---|---|---|
| Appetitive | `figure*` `fig:appetitive_real_compound`, caption | subfigure removido, panel (b) fusionado, caption reescrito | `d93adbd` |
| Aversive | `figure*` `fig:aversive_real_compound`, caption | ídem | `d93adbd` |
| Complex | `figure*` `fig:complex_real_compound`, caption | ídem | `d93adbd` |
| Obstacle | `figure*` `fig:obstacle_real_compound`, caption | ídem (nota: sin sombreado rojo/azul — estímulo no cromático) | `d93adbd` |
| Todos | `Table~\ref{tab:consolidated_physical_metrics}` | columna `Var(z) peak` ya agrega el pico/patrón por escenario | pre-existente, confirmada vigente |
| Todos | párrafos `\textbf{Escenario (see Figure~...)}`  | narrativa de `Var(z)` en prosa, no depende de la figura eliminada | `9df8395` (ronda anterior) |

Ningún párrafo de la sección de limitaciones (`results.tex` línea ~938) ni del abstract/intro
menciona la familia `*_Real_Plot_2` — no requieren cambio.

## 2. Estrategia argumentativa (ya aplicada)

- **Traducción visual → narrativa:** cada uno de los 4 párrafos ya narra el patrón de `Var(z)`
  (pico sostenido no-nulo tras completar misión en Appetitive; doble pico detección+retirada en
  Aversive; tres fases en Complex; pico masivo transitorio en Obstacle) y lo conecta con una causa
  mecánica/fisiológica concreta — esto es exactamente la "traducción de evidencia visual a
  narrativa analítica" que pide el objetivo, y ya estaba en el manuscrito antes de tocar la figura.
- **Métricas agregadas:** la columna `Var(z) peak` de `tab:consolidated_physical_metrics` cubre el
  pedido de "valores numéricos clave" sin necesitar una gráfica independiente.
  Nota: peak values son picos exactos leídos de las gráficas (extracción por vectorización, no
  inventados) — mismo estándar de trazabilidad que el resto del pipeline.
- **Referencias cruzadas:** el panel (b) fusionado ya cumple el rol de "otras figuras conservadas"
  — la dinámica del ganglio basal sigue siendo visible (como sub-panel superior), solo se retiró la
  figura *independiente* y redundante, no la evidencia visual en sí.

## 3. Before/After (registro real, no propuesta)

### Caption — Appetitive (`fig:appetitive_real_compound`)

**Antes:**
> Real-world Appetitive Stimulus Scenario (*Appetitive_Real* family, three hardware replicates).
> (a) ECDF of locomotion mode-switching latency $T_{switch}$. (b) Temporal evolution of the basal
> ganglia firing variance $Var(z)$. (c) Coupled Roll and Pitch RMS attitude profile throughout the
> trial.

**Después:**
> Real-world Appetitive Stimulus Scenario (*Appetitive_Real* family, three hardware replicates).
> (a) ECDF of locomotion mode-switching latency $T_{switch}$. **(b) Coupled neural and kinematic
> response: (top) temporal evolution of the basal ganglia firing variance $Var(z)$ with red/blue
> stimulus-presence shading; (bottom) Roll and Pitch RMS attitude profile throughout the trial.**

### Caption — Aversive (`fig:aversive_real_compound`)

**Antes:**
> (b) Neural firing variance $Var(z)$ displaying the dual-peak evasion signature. (c) Chassis
> attitude micro-dynamics during and after the evasive manoeuvre.

**Después:**
> **(b) Coupled neural and kinematic response: (top) neural firing variance $Var(z)$ displaying the
> dual-peak evasion signature, with red/blue stimulus-presence shading; (bottom) chassis attitude
> micro-dynamics during and after the evasive manoeuvre.**

### Caption — Obstacle (`fig:obstacle_real_compound`)

**Antes:**
> (b) Massive transient hyper-excitation peak in neural firing variance $Var(z)$ induced by
> volumetric geometric input. (c) Rhythmic Roll RMS expansion during active lateral flanking and
> post-avoidance stabilisation.

**Después:**
> **(b) Coupled neural and kinematic response: (top) massive transient hyper-excitation peak in
> neural firing variance $Var(z)$ induced by volumetric geometric input (no stimulus-presence
> shading — this scenario uses a non-chromatic obstacle cue); (bottom) rhythmic Roll RMS expansion
> during active lateral flanking and post-avoidance stabilisation.**

(Complex sigue el mismo patrón; caption completo visible en `results.tex` línea ~211.)

## 4. Único punto abierto (opcional, no bloqueante)

Los picos de `Var(z)` en `tab:consolidated_physical_metrics` están en unidades relativas de la
red (no normalizadas a un rango 0–1 ni con unidades físicas), lo que es correcto pero podría
generar una pregunta de un revisor ("¿pico de qué escala?"). Si el equipo quiere blindar esto,
la única adición pendiente sería una nota al pie de tabla aclarando que `Var(z)` es la varianza de
disparo interna de la red (adimensional, específica del modelo), no una medida física. **No se
recomienda ejecutar esto de oficio** — es una decisión de estilo, no una corrección de contenido;
queda para que el autor lo confirme si lo considera necesario.

## 5. Estado en `PROGRESS.md`

No se crea una fila nueva: este hallazgo confirma que el trabajo relevante ya está cubierto por la
fila `N-03` (`applied`, commit `d93adbd`). No hay entregable de escritura pendiente para el bot de
redacción derivado de esta tarea.
