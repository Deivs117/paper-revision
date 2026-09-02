# Ticket de redacción — Falta la metodología de la Reactive Inspection Task

**Tipo:** corrección/gap de redacción (asignar ID `C-xx` con `scripts/next_id.sh C` cuando se
triage este documento a una fila de `PROGRESS.md`).

**Qué falta:** `sections/results.tex` tiene una subsección completa "Reactive Inspection Task"
(línea ~481 al momento de escribir esto) con métricas, tabla (`tab:inspection_metrics`), figura
(`fig:inspection_dfinal_scatter`) y una discusión detallada de resultados — todo eso ya está
redactado y `synced-to-overleaf` desde la fila `R3-05`. **Pero `sections/methodology.tex` no
describe en ningún lugar el diseño del experimento en sí** — confirmado por `grep` exhaustivo:
ninguna mención de la tarea de inspección más allá de dos referencias incidentales al umbral
$Ar=28.0$ (derivación geométrica de la cámara, sin relación con el escenario de inspección
específico). Un lector que llegue a la subsección de resultados no tiene, en ningún punto anterior
del paper, una descripción de qué es el "campo de obstáculos" (`\subsubsection{Reactive Inspection
Task}`), cuántos ensayos se corrieron, cuál era el timeout, o cuál era el criterio de éxito —
solo lo infiere retroactivamente de la prosa de resultados.

**Qué debe cubrir la redacción nueva** (metodología, no resultados — eso ya existe):
- Descripción funcional del escenario: un campo de obstáculos diseñado a propósito donde el
  objetivo visual **no** es visible desde la pose inicial del robot, y solo entra en el campo de
  visión tras superar tres obstáculos estáticos (cápsulas) — sin nombrar el archivo de mundo crudo
  (`obstaculos.world`), regla README §11.1, ya aplicada en la subsección de resultados y debe
  mantenerse aquí también.
- Parámetros del experimento: N=20 ensayos independientes, timeout de 90 s, sin inyección de ruido
  artificial (ya estos números están en `results.tex` línea 483, pero pertenecen conceptualmente a
  la metodología — decisión de estilo del equipo de redacción si se repiten o se mueven).
- Qué hace y qué NO hace el sistema en esta tarea (ya hay una frase de esto en resultados línea
  485 — "no implementa planeación deliberada... reactivo vía BG/WTA" — igual, candidato a vivir en
  metodología en vez de (o además de) resultados).
- Mantener breve — el propio usuario pidió que no sea extenso, solo que exista una descripción
  clara de qué se hizo.

**Fuentes disponibles para quien redacte** (no es necesario re-investigar desde cero):
- `experiments/R3-05-inspection/README.md` — proveniencia de datos: suite `familia_e_inspeccion`,
  N=20, `90s timeout`, sin perturbación aleatoria, vía `test_manager.py` en `PETER_SIMULATION`
  rama `sam`, commit `6d5a2e6` ("feat(exp-e): implementar experimento de inspección reactiva
  (Reviewer #3.5)").
- `intake/processed/R3-05_inspection_handoff.md` — diagnóstico técnico original y completo del
  escenario (ya triado y aplicado, pero conserva el detalle de diseño del experimento).
- `intake/processed/R3-05-inspection_writing_plan.md` — plan de redacción original que sí generó
  la parte de resultados; puede tener contexto de diseño no trasladado a metodología.

**Dónde insertar en `methodology.tex`:** cerca de la descripción de otros escenarios de
simulación/comportamiento (revisar `OUTLINE.md` para la ubicación exacta más coherente con el
resto de la estructura del documento) — coordinarlo para que no quede desconectado de dónde
`results.tex` ya lo referencia.

**Nota:** este documento es solo el hallazgo/ticket — no contiene la redacción en sí. Al triarlo,
sigue el flujo normal (§8.2 del README raíz): asignar `C-xx`, fila en `PROGRESS.md` con target
`sections/methodology.tex`, y mover este archivo a `intake/processed/` una vez aplicado.
