# N-09 — Fusionar `fig_transition_phases_v9_part1/2` en una sola figura de transiciones reversibles — PENDIENTE

**Origen:** hallazgo del autor (2026-08-29) al revisar `fig_stability_phases.png` para `R02-01-05`/`R02-01-04`
(N-07) — mientras se re-auditaba esa figura se notó que `fig_transition_phases_v9_part1.png` y
`fig_transition_phases_v9_part2.png` (`results.tex` §"Mode-transition stability", líneas ~372–410,
`\label{fig:transition_part1}`/`\label{fig:transition_part2}`) son redundantes en su diseño actual. No forma
parte del alcance original de `R02-01-04`/`R02-01-05` (esas figuras no aparecen en ninguno de los dos) — bloque
nuevo e independiente, aunque comparte el mismo `experiments/N-01-simulation-figure-regeneration/` como área de
trabajo natural por cercanía temática (todas son figuras de estabilidad/transición de N-01).

## 1. Diagnóstico

Estructura actual: 6 filas (A–F) en total, una por cada transición **dirigida** entre los 3 modos de locomoción
(Quadrupedal $C$, Differential Rolling $H$, Omnidirectional $X$):

- Part 1: A = $C\to H$, B = $H\to X$, C = $X\to C$.
- Part 2: D = $C\to X$, E = $X\to H$, F = $H\to C$.

Cada fila tiene 3 columnas (snapshots): Onset ($t_0$), mid-reconfiguración ($t_0+1$s), final ($t_0+2$s).

**Confirmado por el autor:**
- Las dos filas de cada pareja no dirigida (p. ej. A=$C\to H$ y F=$H\to C$) muestran el mismo tipo de
  reconfiguración, solo invertida en el tiempo — no aportan información nueva mostradas por separado. Las 3
  parejas reales son $C\leftrightarrow H$, $H\leftrightarrow X$, $X\leftrightarrow C$.
- La columna del medio ($t_0+1$s, mid-reconfiguración) se elimina — queda cada fila con 2 columnas (Onset /
  Final) en vez de 3.

## 2. Rediseño (confirmado por el autor, 2026-08-29)

- **Fusionar en una sola figura de 3 filas** (una por pareja no dirigida), reemplazando las dos figuras actuales
  — ya no hace falta "Part 1 of 2"/"Part 2 of 2" con solo 3 filas totales.
- **Fila = pareja de modos**, con **doble flecha (⇄)** entre las dos cajas de modo (reemplaza la flecha simple
  hacia abajo) para simbolizar que la transición es reversible e igualmente estable en ambos sentidos.
- **2 columnas por fila** (se elimina el snapshot $t_0+1$s de cada fila): Onset y Final.
- **TR/SM numéricos:** cada pareja fusiona los datos de las 2 corridas originales (p. ej. A y F) — reportar
  **rango (mín–máx)** de TR y de SM por snapshot en vez de un solo número o dos series superpuestas. Ejemplo de
  formato esperado en la anotación: `TR=0.003–0.079` en vez de un único valor.
- **Título de la figura:** ya no aplica "Part 1 of 2"/"Part 2 of 2" — un solo título, p. ej. "Static Stability
  Analysis across Locomotion Mode Transitions — Generalised McGhee-Frank (1968) Support Polygon".

## 3. Referencias cruzadas a actualizar (mismo patrón que `R02-01-04` §4)

| Antes | Después |
|---|---|
| `\label{fig:transition_part1}`, `\label{fig:transition_part2}` (2 figuras, 6 filas rotuladas A–F) | Colapsar a un único `\label{fig:transition_phases}` con 3 filas (una por pareja, sin dirección) |
| Caption de `transition_part1` (líneas ~391–401): "Top: $C\to H$. Middle: $H\to X$. Bottom: $X\to C$." | Reescribir como 3 filas no dirigidas: "$C \leftrightarrow H$", "$H \leftrightarrow X$", "$X \leftrightarrow C$" — mencionar explícitamente que ambos sentidos fueron verificados como igualmente estables (rango TR/SM reportado) |
| Caption de `transition_part2` (líneas ~404–410) | Se elimina — su contenido queda absorbido en la nueva caption única |
| Prosa en `results.tex` ~línea 372–381 ("All six pairwise transitions... Figures~\ref{fig:transition_part1} and~\ref{fig:transition_part2} show three representative frames per transition...") | Reescribir: ya no son "seis transiciones" mostradas por separado sino 3 parejas reversibles, 2 frames (no 3) por fila — actualizar el conteo y la descripción del contenido |

## 4. Pasos para ejecutar

1. Localizar los datos crudos de las 6 corridas (A–F) usadas para generar `fig_transition_phases_v9_part1/2.png`
   — confirmar si están en `experiments/` (con script conocido) o si esta figura también es un PNG histórico sin
   pipeline detrás (a verificar; no confirmado en este documento).
   - Si no hay pipeline/CSV trazable: aplica el mismo criterio D-1 de `R02-01-05` (vectorizar desde el PNG
     publicado) — documentar en `experiments/_plotting/vectorized/README.md` igual que los demás casos.
   - Si sí hay pipeline: extender/crear un builder (`experiments/_plotting/builders/transition_phases.py`) que
     lea ambos sentidos de cada pareja y calcule el rango TR/SM min–max por snapshot.
2. Diseñar la fila fusionada: layout 2 columnas (Onset, Final) × 3 filas (parejas), con ⇄ entre las cajas de modo
   en vez de flecha simple. Reutilizar la leyenda existente (Support Polygon, Critical Edge, SM Arrow, CoM,
   Stance Feet, Inradius Circle) sin cambios.
3. Generar output en `experiments/N-01-simulation-figure-regeneration/output/` (o carpeta hermana si el pipeline
   es distinto al de N-01) — no promover automáticamente (D-14 ya vigente en el bloque N-01).
4. Revisión visual del autor contra las 6 filas originales antes de promover — confirmar que el rango TR/SM por
   pareja es consistente con ambos sentidos originales.
5. Promover a `assets/` con **nombre nuevo** (p. ej. `fig_transition_phases_v10.png`), sin `--force` — no
   reemplaza en el mismo nombre porque cambia de 2 figuras a 1.
6. `git rm` de `fig_transition_phases_v9_part1.png`/`_part2.png` una vez confirmado que ya no tienen referencia.
7. Actualizar `sections/results.tex`: un solo bloque `figure*`, aplicar la tabla de referencias cruzadas de §3,
   reescribir la prosa de apertura del párrafo "Mode-transition stability" (líneas ~372–381) para reflejar 3
   parejas reversibles en vez de 6 transiciones dirigidas. Envolver todo lo nuevo/cambiado en `\revblue{}`.
8. Dar de alta la fila `N-09` en `PROGRESS.md` (ya reservado, `scripts/next_id.sh N` → `N-09`), `Category:
   Métricas`, `Data source` apuntando a la carpeta de experimento usada en el paso 3.
9. `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh` antes de cualquier commit.

## 5. Relación con el resto del bloque de simulación

No bloquea ni es bloqueado por `R02-01-04`/`R02-01-05` — comparte solo el área de trabajo
(`experiments/N-01-simulation-figure-regeneration/` o similar) y el mismo deadline de ronda (2026-08-31). Puede
ejecutarse en paralelo a cualquiera de los otros dos bloques. Si el tiempo no alcanza para los tres antes del
31, es candidato a quedar documentado como pendiente explícito para la siguiente ronda, igual que el criterio ya
usado en `R02-01-05` §7 (nota de priorización).
