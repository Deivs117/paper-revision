# R02-01-06 — Limpieza editorial menor (redundancia residual + gramática/estilo) — PENDIENTE, baja prioridad

**Estado: 🔲 Sin empezar, sin bloquear nada.** Ninguno de estos ítems depende de datos, figuras, ni de los otros
bloques de simulación — se pueden hacer en cualquier momento, incluso en paralelo. Se agrupan aquí porque son
puramente de redacción/estilo, no de contenido factual.

**Origen:** `intake/pending/R02-01_metric_and_figure_audit.md` §4 y §5 (eliminado tras atomizarse, ver
`intake/R02-01_INDEX.md`).

## 1. Redundancia texto↔tabla/figura residual (más allá de lo ya resuelto en R2-01/Sebas)

| Ubicación | Problema | Propuesta | Estado |
|---|---|---|---|
| `tab:consolidated_physical_metrics`, columna `Var(z) peak` (fila Complex: "peak >30,000") | Sin unidad ni escala de referencia — un lector no puede saber si es alto/bajo sin comparar a mano contra las otras 3 filas (~1100, dual-peak sin número, sustained) | Normalizar a escala relativa común (p. ej. "×27 vs. baseline Obstacle") o añadir nota al pie con la unidad de "firing variance" | **Decisión editorial pendiente del autor** — no depende de datos, es puramente de presentación |
| `results.tex:945-949` (3 párrafos sobre `FigReal_Terrain_Latencies_4Panels.png`) | Ya parcialmente condensado por R2-01 (patch 16), pero el primer párrafo (945) sigue siendo puramente descriptivo de metodología sin interpretación nueva | Fusionable con el párrafo siguiente (947) sin pérdida de contenido | No urgente, candidato a una futura pasada de redundancia. Independiente de la vectorización de esa figura (ya cerrada, ver `intake/processed/R02-01-02_fisico_regeneracion_N02-N05.md`) — se puede hacer en cualquier orden respecto a eso |

**Nota:** la fila original de esta tabla sobre "energía de transición sin números" ya se resolvió — ver
`intake/processed/R02-01-03_energia_transicion_y_modo_R2-04.md`. No repetir esa tarea.

## 2. Gramática y estilo (revisión dirigida, no exhaustiva línea-por-línea)

- **`results.tex:9`** — "its scope and caveats as a symbolic, non-certified test arena are discussed in
  Section~\ref{ssec:Limitations}": "non-certified test arena" es un poco abrupto/calcado; considerar "a symbolic
  representation rather than a certified test arena" — sin cambiar el significado.
- **`results.tex:224`** — párrafo sobre discretización STL del terreno inclinado en simulación, denso y
  técnicamente correcto pero aislado entre dos figuras sin conexión clara con el párrafo anterior/siguiente —
  candidato a moverse junto a la explicación del terreno inclinado en la línea 197, donde encaja temáticamente.
- **`results.tex:497-500`** — dos párrafos consecutivos comparan repetidamente real vs. simulación para el
  estímulo apetitivo con estructura de frase casi idéntica ("unlike the simulation, where...", "In contrast, in
  the simulation..."). No es redundancia de datos (cada uno aporta un ángulo neuronal distinto), pero podría
  fusionarse en un solo párrafo con mejor flujo.
- **`results.tex:954`** — párrafo de Limitations es una sola oración larguísima (>150 palabras) con múltiples
  cláusulas subordinadas encadenadas ("yet", "rather than", "Instead") — buen contenido, se beneficiaría de
  dividirse en 2-3 oraciones para legibilidad, sin tocar el argumento.
- **Consistencia de mayúsculas en nombres de modo:** el documento alterna entre "Quadrupedal Walking",
  "quadrupedal mode", "Quadrupedal ($C$)" y similar (también para Differential Rolling/Omnidirectional) — no es
  un error, pero no hay convención única aplicada consistentemente. Sugerencia: Title Case cuando se usa como
  nombre propio de modo, minúscula cuando es adjetivo genérico.

## 3. Al ejecutar (si el autor decide priorizar esto)

- Cambios de puro estilo/redundancia editorial (sin alterar cifras) — evaluar caso a caso si aplica `\revblue{}`
  (regla del proyecto: "pure typo fixes with zero meaning change can skip it; default to wrapping otherwise" —
  las fusiones de párrafo SÍ cambian estructura, envolver; los ajustes de una palabra suelta pueden omitirse).
- No requiere `Data source` en `PROGRESS.md` (sin experimento detrás) — dar de alta como fila `C-xx`
  (`scripts/next_id.sh C`), `Category: Escritura`.
- `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh` antes de cualquier commit.
