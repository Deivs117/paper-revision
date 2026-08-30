# N-09 — Fusionar `fig_transition_phases_v9_part1/2` en una sola figura de transiciones reversibles — ✅ APLICADO 2026-08-29

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

1. ✅ **Confirmado (2026-08-29):** no hay pipeline/CSV detrás de `fig_transition_phases_v9_part1/2.png`. Búsqueda
   en todo el repo (`grep -rl "979"` sobre `.py`/`.md`, y comparación contra las 6 carpetas de
   `experiments/simulation/`, que solo cubren las 4 familias de la batería de ruido + `familia_c1`/`familia_c2`
   de terreno) no encuentra la corrida de $N_{\mathrm{total}}=979$ muestras (las 6 transiciones direccionadas en
   una sola corrida continua, `results.tex` línea ~336) en ningún lado — mismo caso exacto que la corrida
   $N=268$ de `fig_stability_phases.png` (N-07), nunca archivada. Aplica D-1: vectorizar desde el PNG publicado,
   mismo método ya probado en N-07 (`extract_stability_phases.py`/`stability_phases.py` — geometría real de
   polígono de soporte, pie de apoyo/vuelo, TR/SM leídos como texto plano de la figura, calibración por las
   gridlines compartidas ±0.4m de cada panel). Documentar en `experiments/_plotting/vectorized/README.md` igual
   que los demás casos.
   - Nuevo builder: `experiments/_plotting/builders/transition_phases.py`, reutilizando el patrón de
     `stability_phases.py` (mismo tipo de panel: polígono de soporte + CoM + flecha SM + círculo inradio +
     etiqueta TR). Diferencia clave: hay que vectorizar **12 paneles** (6 filas × 2 snapshots tras eliminar la
     columna media) en vez de leer un CSV, y fusionar cada pareja de filas (p. ej. A+F) calculando el rango
     TR/SM min–max en vez de un solo valor por snapshot.
2. ✅ Diseñado (con 2 iteraciones de feedback del autor, 2026-08-29): layout final = columna lateral con los 2
   cuadros de modo apilados (mismo estilo del original: caja de color redondeada, texto ceñido, sin relleno de
   color vacío) + flecha vertical **bidireccional** entre ellos (no una flecha horizontal entre los paneles, que
   se solapaba con los datos — corregido tras feedback). Leyenda completa restaurada al pie de la figura
   (Support Polygon, Critical Edge, SM Arrow, Polygon Centre, CoM, Stance Feet, Inradius Circle, colores de
   modo) — **sin "Swing Foot"**, deliberado: los 6 paneles son todos estados asentados de 4 patas, no hay pie en
   vuelo que legendar. Etiqueta "SM=" reubicada centrada justo arriba del eje X en cada panel (posición fija,
   no sigue la flecha — evita el solape que tenía en la primera iteración). Tipografía: serif obligatorio,
   10/11/12pt (general/ejes/títulos) vía `experiments/_plotting/style.py` (ya coincidía exactamente con la
   especificación pedida).
3. ✅ Output en `experiments/N-01-simulation-figure-regeneration/output/fig_transition_phases_v10.png`.
4. ✅ Revisión visual del autor (2 rondas de ajuste) — aprobado 2026-08-29.
5. ✅ Promovido a `assets/fig_transition_phases_v10.png` (nombre nuevo, sin `--force`).
6. ✅ `git rm` de `fig_transition_phases_v9_part1.png`/`_part2.png`.
7. ✅ `sections/results.tex` actualizado: un solo `\begin{figure}` (no `figure*`, cabe en una columna), tabla de
   referencias cruzadas de §3 aplicada, prosa de apertura reescrita para reflejar 3 parejas reversibles (ya no
   "seis transiciones" mostradas por separado). Todo envuelto en `\revblue{}`.
8. ✅ Fila `N-09` en `PROGRESS.md` actualizada a `applied`.
9. `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh`/`scripts/compile_pdf.sh` — pendiente de correr en el
   mismo commit que cierra este bloque (ver PROGRESS.md).

**Hallazgo nuevo, fuera de alcance de este bloque:** el párrafo de `results.tex` inmediatamente después de esta
figura ("Across all six pairwise transitions... the Normalised Stability Margin was maintained at its
platform-geometry maximum ($SM=0.050$m)... Tipover Risk index remained at $TR=0.000$ without exception") afirma
un agregado constante sobre los $N=979$ muestras crudas — pero esos datos crudos **no existen archivados en
ningún lado** (confirmado en el paso 1 de este documento). Los 12 valores TR/SM que sí pude leer del PNG
publicado (0.003–0.079, nunca 0.000; 10.5–20.8cm, nunca 0.050m) son inconsistentes con esa afirmación agregada.
No se tocó ese párrafo — mismo criterio que el mismatch de `tab:consolidated_simulation_metrics` en `N-01`
(flagged, no corregido sin confirmación del autor). Requiere decisión: ¿de dónde salió originalmente el
$SM=0.050$/$TR=0.000$ si no hay CSV crudo? ¿Es una cifra fabricada, una interpretación distinta de "SM/TR
durante la transición" (excluyendo los snapshots mostrados), o un error a corregir?

## 5. Relación con el resto del bloque de simulación

No bloquea ni es bloqueado por `R02-01-04`/`R02-01-05` — comparte solo el área de trabajo
(`experiments/N-01-simulation-figure-regeneration/` o similar) y el mismo deadline de ronda (2026-08-31). Puede
ejecutarse en paralelo a cualquiera de los otros dos bloques. Si el tiempo no alcanza para los tres antes del
31, es candidato a quedar documentado como pendiente explícito para la siguiente ronda, igual que el criterio ya
usado en `R02-01-05` §7 (nota de priorización).
