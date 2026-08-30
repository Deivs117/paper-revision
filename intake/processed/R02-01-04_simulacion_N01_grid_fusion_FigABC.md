# R02-01-04 — Simulación N-01: rejilla 4×3 (F-02) + regeneración FigA/B/C — PENDIENTE

**Estado (actualizado 2026-08-29): ✅ CERRADO — todo el alcance de este documento aplicado.** FigA/FigB/FigC
(§1c) implementadas, regeneradas y promovidas. La rejilla 4×3 (§1a) fusionada en `results.tex`: los 4
`fig1_*_macro.png` reemplazados por un único `figure*` (`fig1_noise_robustness_grid.png`, `\label{fig:
noise_robustness_grid}`), las 4 referencias cruzadas de §4 remapeadas, los 4 `fig2_*_micro` conservados como
figuras individuales, los 4 PNG viejos `git rm`'d. `validate_tex.sh`/`check_roundtrip.sh` pasan. Ver fila `N-01`
en `PROGRESS.md` para el detalle completo por pieza. El dato del panel de latencia de Obstacle sigue condicionado
a la re-corrida de simulación pendiente (§3) — el pipeline ya soporta el swap automático vía `--simulation-root`
(D-12), no requiere trabajo adicional ahora ni bloquea mover este documento a `processed/`. Deadline: 2026-08-31.

**Origen:** `intake/pending/R02-01_metric_and_figure_audit.md` §3 (F-02, D-9) + `intake/pending/R02-01_data_traceability_and_plotting_plan.md`
§1.1/§3.4 Grupo 1 (ambos eliminados tras atomizarse, ver `intake/R02-01_INDEX.md`) + `PROGRESS.md` fila `N-01` +
`experiments/N-01-simulation-figure-regeneration/README.md` + `intake/processed/n01_audit_notes_2026-08-29.md`
(auditoría del autor sobre el output ya generado, ver §1c).

## 1. Qué falta hacer (dos piezas independientes, mismo pipeline)

### 1a. Rejilla 4×3 — fusión de los 4 `fig1_*_macro.png` (F-02, confirmado D-9)

Fusionar `fig1_Appetitive_macro.png`, `fig1_Aversive_macro.png`, `fig1_Obstacle_macro.png`,
`fig1_Complex_macro.png` (4 figuras, 3 subpaneles cada una: tiempo/duración, Pitch RMS, latencia — todas vs.
σ∈[0,4]) en una única rejilla 4×3 (filas=escenario en orden Appetitive→Aversive→Obstacle→Complex,
columnas=métrica).

- **Eje X unificado:** "Sensory Noise Index ($\sigma$)" en las 12 subgráficas (ya lo es hoy).
- **Columna 1:** unificar a **"Mission Time $T_{sim}$ (s)"** en las 4 filas (hoy son 4 nombres distintos:
  Mission/Evacuation/Evasion/Lifecycle Time) — delegar la semántica específica al texto/caption, no al eje.
- **Columna 2:** "Pitch RMS (deg)" — ya consistente. Fijar el mismo rango de eje Y (0–4°) en las 4 filas.
- **Columna 3:** "Decision Latency (ms)" — **ver el hueco de Obstacle en §3 antes de fijar esta columna.**
- **Etiquetas de fila:** nombre del escenario fuera del área de plot (`\rotatebox{90}` en LaTeX o `fig.text()` en
  matplotlib), no repetido en cada título de columna.

### 1b. Regeneración code-traceable de FigA/FigB/FigC (M-01–M-04, ya verificadas correctas)

`FigA_Stability_Profile.png`, `FigB_Decision_Delay.png`, `FigC_Terrain_Adaptability.png` — **estas figuras no
tienen ningún número incorrecto** (Informe 2 §0 ya confirmó que coinciden con el dato crudo). Esto no es una
corrección, es dejar una versión regenerada por código, trazable, en vez de un PNG histórico sin script conocido
detrás. Ya ejecutado una vez (ver §2), visualmente consistente con las versiones publicadas (spot-check: TR
plano ≈0.58–0.60 con pico transitorio t=-1.3 a -0.5s en rugoso; TR plano ≈0.59 en pendiente — coincide).

### 1c. Ajustes del autor sobre FigA/B/C, auditoría 2026-08-29 (nuevo, va MÁS ALLÁ de "regenerar trazable")

Notas crudas en `intake/processed/n01_audit_notes_2026-08-29.md`. A diferencia de §1b (que asumía cero cambios de
contenido, solo trazabilidad de código), estos 3 ajustes sí cambian lo que la figura muestra — hay que aplicarlos
sobre `ecdf_phase_space.py` antes de volver a promover ninguna de las 3.

- **`fig1_noise_robustness_grid.png`: aprobado sin cambios.** Nota del autor: "gráficamente están perfectas" —
  el layout de la rejilla 4×3 queda cerrado. Lo único pendiente para esta figura es lo ya descrito en §3 (dato
  de latencia Obstacle, condicional a la re-corrida de simulación) — no un ajuste de diseño nuevo.
- **`FigA_Stability_Profile.png` — Estado: ⚠ Ajustar antes de integrar.** El título superior queda con demasiado
  espacio en blanco perdido debajo de él (layout, no contenido) — corregir el `subplots_adjust`/`tight_layout`
  (o equivalente) que separa el título del área de plot en `ecdf_phase_space.py`.
- **`FigB_Decision_Delay.png` — Estado: ❌ Rechazar / re-hacer.** Eliminar el panel/gráfica de $T_{response}$ (que
  solo muestra ceros, sin aportar explicabilidad) y en su lugar **explicar ese resultado textualmente** en
  `results.tex` (no graficarlo). Esto reduce el número de subpaneles de `FigB` — confirmar con el autor el layout
  resultante (¿2 paneles en vez de 3?) antes de re-generar, y redactar la frase explicativa que reemplaza al
  panel eliminado (envuelta en `\revblue{}` al integrarse).
- **`FigC_Terrain_Adaptability.png` — Estado: ⚠ Ajustar antes de integrar.** Mantener las líneas divisorias
  actuales, pero hacer que "sean dicientes" — **criterio resuelto (2026-08-29), a partir de la prosa que ya
  acompaña esta figura en `results.tex:280`**: la separación real entre los dos clusters (Rugged Terrain vs.
  Inclined Slope) ocurre en el **eje Pitch RMS**, no en Roll RMS (los rangos de Roll RMS se solapan a propósito
  — el texto lo señala como evidencia de que la estabilización lateral es igual de efectiva en ambos terrenos,
  no una separación que deba marcarse). Los centros de cluster que el texto ya reporta:
  Rugged $\mu_\theta\approx1.67°$ (con $\mu_\phi\approx1.59°$), Inclined Slope $\mu_\theta\approx2.29°$ (con
  $\mu_\phi\approx1.47°$).
  - **Acción concreta:** dibujar una única línea divisoria horizontal (Pitch RMS = valor intermedio entre 1.67°
    y 2.29°, p. ej. el punto medio $\approx1.98°$ salvo que los datos crudos de `experiments/simulation/`
    sugieran un mejor punto de corte al graficarlo) que separe visualmente la banda baja (Rugged) de la banda
    alta (Inclined Slope), con una etiqueta corta a cada lado (p. ej. "Rugged Terrain zone" / "Inclined Slope
    zone") en vez de una división sin explicar.
  - **No agregar** ninguna línea divisoria en el eje Roll RMS — sería contradecir la propia prosa (`results.tex`
    dice explícitamente que el solape en Roll RMS es la evidencia de estabilización lateral comparable, no algo
    que deba separarse).
  - Ya no queda ninguna decisión de diseño pendiente del autor para este panel — implementable directo en
    `ecdf_phase_space.py`.

## 2. Estado del pipeline (ya construido, D-12–D-14)

- **Scripts:** `experiments/_plotting/builders/macro_robustness.py` (rejilla 4×3 + recompute de
  `tab:consolidated_simulation_metrics`), `experiments/_plotting/builders/ecdf_phase_space.py` (FigA/B/C),
  `experiments/_plotting/generate_all_simulation.py` (entry point).
- **D-12 (versionado):** una futura re-corrida del equipo de simulación (notificada 2026-08-27, solo batería
  simulada) aterriza en un directorio hermano nuevo, nunca sobreescribe `experiments/simulation/` actual — el
  pipeline toma `--simulation-root` como flag de CLI para esto.
- **D-13:** construido y ya ejecutado una vez contra los datos actuales de `experiments/simulation/`.
- **D-14:** el output queda en `output/` para revisión manual — **no se promueve automáticamente.**
  `scripts/promote_figure.sh` sigue siendo el único camino a `assets/`.
- **Output ya generado (`experiments/N-01-simulation-figure-regeneration/output/`):**
  `fig1_noise_robustness_grid.png`, `FigA_Stability_Profile.png`, `FigB_Decision_Delay.png`,
  `FigC_Terrain_Adaptability.png`, `tab_consolidated_simulation_metrics.csv`.

## 3. Hallazgo nuevo que bloquea cerrar la columna 3 de la rejilla — hueco de latencia en Obstacle

Al ejecutar el pipeline se confirmó (no se sospechaba, se verificó directo): **0 de 15 filas de
`familia_a_obstaculo` tienen un valor de latencia poblado**, ni en `trial_summary.json.exp_latency` ni en
`metrics_raw.csv.latency_s` (esto **corrige** la nota anterior de Informe 2 D-4, que asumía `metrics_raw.csv` sí
lo tenía — no es así). El panel C de `fig1_Obstacle_macro.png` **publicado actualmente** sí muestra valores de
latencia normales — no se puede reproducir desde `experiments/` tal como está.

`fig1_noise_robustness_grid.png` (ya generado) renderiza una anotación explícita **"No latency data recorded in
this run"** en ese panel en vez de graficar ceros o dejar el eje vacío silenciosamente.

**✅ Decisión confirmada por el autor (2026-08-27), condicional a un evento externo:**

- **Si la re-corrida de simulación NO llega antes del cierre de esta ronda (deadline 2026-08-31):**
  vectorizar el panel C de `fig1_Obstacle_macro.png` (el PNG ya publicado) con el mismo método de extracción de
  color de píxel ya probado en los Grupos B/D (`experiments/_plotting/extract/`, ver
  `experiments/_plotting/vectorized/README.md`) e insertar ese valor extraído en la rejilla fusionada en vez del
  hueco. **Con 4 días hasta el deadline, este es el camino elegido para esta ronda** — ver §5.
- **Si la re-corrida llega a tiempo:** no hace falta vectorizar nada — el pipeline ya soporta `--simulation-root`
  (D-12), así que apuntar a la carpeta nueva y volver a correr `generate_all_simulation.py` reemplaza el dato
  vectorizado por el real sin rehacer nada más. Si esto pasa después de haber vectorizado, el swap es una
  operación barata (re-generar y re-promover, mismo nombre de archivo).

El autor confirma que estos datos sí existieron en su momento pero no son reproducibles hoy (no recuerda el
método de captura ni conserva el dato crudo) — es exactamente el caso previsto por D-1 (vectorizar cuando no hay
CSV recuperable), no una excepción.

**Nota relacionada, no bloqueante para este bloque:** este y otros 9 hallazgos sobre huecos/ambigüedades de
`experiments/simulation/` (mapeo σ↔`noise_level_idx` no documentado, sin activaciones neuronales individuales,
sin aceleración/pitch cruda en C1/C2, corrida $N=268$ nunca archivada, etc.) están documentados para el equipo
de simulación en `experiments/simulation/SIMULATION_TEAM_ACTION_ITEMS.md` — relevante para la re-corrida
notificada 2026-08-27, no para este bloque en sí (salvo el ítem 1, que es exactamente el hueco de arriba).

## 4. Referencias cruzadas a actualizar al fusionar (Fase 4 original) — ✅ APLICADO 2026-08-29

**Nota:** la imagen fusionada NO lleva letras de panel (a)-(l) dibujadas — el autor pidió no tocar el layout
("gráficamente están perfectas"), así que el plan original de "subfiguras (a)-(l)" se resolvió con referencias
descriptivas (fila/columna) en vez de letras inventadas que no existen en la imagen.

| Antes | Después (aplicado) |
|---|---|
| `fig:appetitive_macro`/`_micro`/`_results`, ídem Aversive/Obstacle/Complex (12 labels) | Un único `\label{fig:noise_robustness_grid}` para la rejilla fusionada; los 4 `fig:X_micro` se conservan como figuras individuales (ya no subfiguras) |
| `\ref{}` en `results.tex` (párrafos Appetitive/Aversive/Obstacle/Complex Targeting) | Appetitive y Complex (contenido de robustez/noise-sweep) → `fig:noise_robustness_grid`; Aversive y Obstacle (contenido de dinámica de un solo trial) → su propio `fig:X_micro` |
| "panel C of Figure~\ref{fig:appetitive_results}" (latencia) | "the Decision Latency column, Appetitive row, of Figure~\ref{fig:noise_robustness_grid}" |

## 5. Pasos para ejecutar (orden confirmado, 2026-08-27 — PRIMERO de los dos bloques de simulación, ver también
`R02-01-05` §7 para el orden combinado)

1. **Implementar los 3 ajustes de §1c en `ecdf_phase_space.py`:** FigA (corregir espacio perdido bajo el
   título), FigB (quitar panel $T_{response}$, reducir a los paneles restantes), FigC (línea divisoria horizontal
   en Pitch RMS ≈1.98°, ya resuelto en §1c — no requiere decisión adicional). Redactar la frase que reemplaza al
   panel eliminado de FigB para `results.tex`.
3. **Vectorizar el panel C (latencia) de `fig1_Obstacle_macro.png`:** nuevo script
   `experiments/_plotting/extract/extract_fig1_obstacle_latency.py` (mismo patrón que
   `extract_fig5.py`/`extract_terrain_latencies.py` — calibración de ejes desde las gridlines propias del panel,
   aislar la serie por su color, documentar la calibración exacta en el docstring del script). 5 puntos (uno por
   nivel de ruido σ∈[0,4]) con su barra de error. Guardar en
   `experiments/_plotting/vectorized/fig1_obstacle_latency.csv` + fila nueva en
   `experiments/_plotting/vectorized/README.md` (fuente, script, nota de validación — mismo formato que las
   entradas existentes).
4. **Modificar `macro_robustness.py`** para que la columna de latencia de Obstacle lea ese CSV vectorizado en vez
   de renderizar la anotación "No latency data recorded in this run" — dejar el fallback a la anotación
   condicionado a que el CSV vectorizado no exista (defensivo, por si se vuelve a correr sin este archivo
   presente).
5. Re-correr `experiments/_plotting/generate_all_simulation.py` (mismo comando del `README.md` de
   `experiments/N-01-simulation-figure-regeneration/`) para regenerar `output/` con el panel de Obstacle ya
   completo y los ajustes de FigA/B/C aplicados.
6. Revisar el resultado contra las figuras actualmente publicadas (comparación visual del panel de Obstacle
   contra `fig1_Obstacle_macro.png` original + `tab_consolidated_simulation_metrics.csv` contra la tabla
   publicada, más los 3 ajustes de FigA/B/C contra las notas de §1c) — confirmar que el valor vectorizado se ve
   consistente con lo que mostraba la figura vieja antes de promover.
7. Promover: `scripts/promote_figure.sh experiments/N-01-simulation-figure-regeneration/output/fig1_noise_robustness_grid.png assets/fig1_noise_robustness_grid.png` (nombre nuevo, sin `--force`); `--force` para `FigA/B/C` (mismos nombres que ya existen en `assets/`).
8. `git rm` de los 4 `fig1_*_macro.png` antiguos una vez confirmado que ya no tienen referencia.
9. Actualizar `sections/results.tex`: nuevo bloque `figure*` único reemplazando los 4 actuales (líneas
   aproximadas 58–75, 79–96, 100–117, 153–170 — confirmar número exacto antes de editar), aplicar la tabla de
   referencias cruzadas de §4, insertar la frase textual que reemplaza al panel $T_{response}$ eliminado de FigB
   (redactada en el paso 1), y en el caption/prosa del panel de Obstacle **mencionar explícitamente que el
   valor de latencia es reconstruido por vectorización de la figura previamente publicada, no de una re-corrida**
   (misma disciplina de trazabilidad que el resto del proyecto — nunca presentar un dato vectorizado como si
   fuera CSV crudo). Envolver en `\revblue{}`.
10. Actualizar `PROGRESS.md`: fila `N-01` de `drafted` → `applied` una vez promovido y `results.tex` actualizado;
    anotar en la fila que el panel de Obstacle usa dato vectorizado (`Data source` ya apunta a
    `experiments/N-01-simulation-figure-regeneration/`, añadir nota "panel Obstacle: ver
    `experiments/_plotting/vectorized/README.md`") y que FigA/B/C incorporan los ajustes de §1c (auditoría
    2026-08-29).
11. `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh` antes de cualquier commit.

**Si la re-corrida de simulación llega antes de ejecutar esto:** el paso 1 (ajustes FigA/B/C) sigue haciendo
falta igual, es independiente del dato de Obstacle — saltar solo los pasos 3-4 (vectorización), apuntar
`generate_all_simulation.py --simulation-root <carpeta nueva>` y continuar desde el paso 5 con dato real.
**Si la re-corrida llega después de haber promovido con el dato vectorizado:** repetir desde el paso 5 con
`--simulation-root` apuntando a la carpeta nueva, re-promover con `--force`, actualizar la nota de `PROGRESS.md`
(quitar la mención de dato vectorizado) — no requiere una fila `N-xx` nueva, es una actualización de la misma.
