# R02-01 — Índice de bloques atómicos

Los dos documentos originales de esta auditoría (`intake/pending/R02-01_metric_and_figure_audit.md` "Informe 1" y
`intake/pending/R02-01_data_traceability_and_plotting_plan.md` "Informe 2") se **atomizaron y eliminaron el
2026-08-27** — habían crecido hasta el punto de duplicarse/contradecirse entre sí sobre qué seguía pendiente
(ver, p. ej., la corrección de estado hecha ese mismo día en §7/§8 de Informe 1 antes de la atomización). Cada
bloque de abajo es ahora autocontenido (diagnóstico + método + estado, sin depender de leer otro archivo) y
cubre una familia de tareas que comparten builder/decisión/ejecución.

## Bloques cerrados (`intake/processed/`)

| Archivo | Cubre |
|---|---|
| `R02-01-01_simulacion_M01-M05_verificacion_redaccion.md` | M-01–M-05: discrepancias texto↔figura en simulación, verificación contra datos crudos y redacción de los 5 pasajes afectados |
| `R02-01-02_fisico_regeneracion_N02-N05.md` | F-01 (físico)/F-03/F-05/F-06, tipografía serif del proyecto, eliminación de `*_Real_Plot_2`, promoción de las 12 figuras físicas + fusión del clasificador |
| `R02-01_basal_ganglia_text_adaptation_plan.md` | Análisis específico de por qué la narrativa textual del ganglio basal no dependía de la figura eliminada (`*_Real_Plot_2`) |
| `R02-01-03_energia_transicion_y_modo_R2-04.md` | Energía de transición morfológica + tabla de consumo por modo (R2-04) — con nota de seguimiento sobre el placeholder Omnidireccional (no bloqueante) |

## Bloques pendientes (`intake/pending/`)

| Archivo | Cubre | Bloqueado por |
|---|---|---|
| `R02-01-04_simulacion_N01_grid_fusion_FigABC.md` | Rejilla 4×3 (F-02) + regeneración code-traceable de FigA/B/C — pipeline ya construido y ejecutado, solo falta promover | Decisión del autor sobre el hueco de latencia de Obstacle (§3 del archivo) |
| `R02-01-05_simulacion_grupo2_vectorizacion.md` | F-01 (instancias de simulación), F-04 (doble eje `GRAPH_IMU`), F-08 (`fig_stability_phases.png`) — requieren vectorización, ningún builder existe aún | Nada externo — listo para empezar cuando se priorice |
| `R02-01-06_limpieza_editorial_menor.md` | Redundancia residual + gramática/estilo, baja prioridad | Nada — se puede hacer en paralelo a cualquier otro bloque |

## Regla de mantenimiento

Cada bloque nuevo que se abra a partir de aquí (p. ej. si `R02-01-04`/`05` generan sub-tareas) debe seguir el
mismo patrón: un archivo por familia de tareas conjuntas, autocontenido, en `intake/pending/` hasta que todas sus
filas de `PROGRESS.md` lleguen a `applied`, momento en el que se mueve a `intake/processed/` — nunca se deja un
bloque pendiente compartiendo archivo con uno ya cerrado.
