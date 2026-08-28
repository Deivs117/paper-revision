# R02-01-04 — Simulación N-01: rejilla 4×3 (F-02) + regeneración FigA/B/C — PENDIENTE

**Estado: 🟡 Pipeline ya construido y ejecutado una vez, output en `experiments/N-01-simulation-figure-regeneration/output/`,
NO promovido a `assets/`. Su bloqueador original (decisión de redacción M-01–M-04) ya se resolvió — ver
`intake/processed/R02-01-01_simulacion_M01-M05_verificacion_redaccion.md`. Falta: revisión del autor + decisión
sobre el hueco de Obstacle (§3) + promoción + registro.**

**Origen:** `intake/pending/R02-01_metric_and_figure_audit.md` §3 (F-02, D-9) + `intake/pending/R02-01_data_traceability_and_plotting_plan.md`
§1.1/§3.4 Grupo 1 (ambos eliminados tras atomizarse, ver `intake/R02-01_INDEX.md`) + `PROGRESS.md` fila `N-01` +
`experiments/N-01-simulation-figure-regeneration/README.md`.

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

**Decisión pendiente del autor, dos caminos:**
1. **Aceptar el hueco** — publicar la rejilla con la anotación explícita en el panel de Obstacle, documentando
   la limitación en el caption/prosa.
2. **Preservar el valor histórico** — tratar el panel C de Obstacle como candidato de vectorización (extraer del
   `fig1_Obstacle_macro.png` publicado actualmente, método D-11/D-1) e insertarlo en la rejilla fusionada en vez
   del hueco.

No ejecutar la fusión final (promoción) sin que esta decisión esté tomada — cambia qué imagen se promueve.

**Nota relacionada, no bloqueante para este bloque:** este y otros 9 hallazgos sobre huecos/ambigüedades de
`experiments/simulation/` (mapeo σ↔`noise_level_idx` no documentado, sin activaciones neuronales individuales,
sin aceleración/pitch cruda en C1/C2, corrida $N=268$ nunca archivada, etc.) están documentados para el equipo
de simulación en `experiments/simulation/SIMULATION_TEAM_ACTION_ITEMS.md` — relevante para la re-corrida
notificada 2026-08-27, no para este bloque en sí (salvo el ítem 1, que es exactamente el hueco de arriba).

## 4. Referencias cruzadas a actualizar al fusionar (Fase 4 original)

| Antes | Después |
|---|---|
| `fig:appetitive_results`, `fig:aversive_results`, `fig:obstacle_results`, `fig:complex_results` (4 labels) + 8 sub-labels | Colapsar a `\label{fig:noise_robustness_grid}` con subfiguras (a)-(l) |
| `\ref{}` en `results.tex:77,98,119,172` (párrafos Appetitive/Aversive/Obstacle/Complex Targeting) | Apuntar a `fig:noise_robustness_grid` + letra de panel específica |

## 5. Pasos para ejecutar (cuando la decisión de §3 esté tomada)

1. Resolver la decisión de §3 con el autor.
2. Si se elige vectorizar el panel de Obstacle: hacerlo antes de fusionar (ver método en
   `intake/pending/R02-01-05_simulacion_grupo2_vectorizacion.md` §1, mismo procedimiento).
3. Revisar `experiments/N-01-simulation-figure-regeneration/output/` contra las figuras actualmente publicadas
   (comparación visual + `tab_consolidated_simulation_metrics.csv` contra la tabla publicada).
4. Promover: `scripts/promote_figure.sh experiments/N-01-simulation-figure-regeneration/output/fig1_noise_robustness_grid.png assets/fig1_noise_robustness_grid.png` (nombre nuevo, sin `--force`); `--force` para `FigA/B/C` (mismos nombres que ya existen en `assets/`).
5. `git rm` de los 4 `fig1_*_macro.png` antiguos una vez confirmado que ya no tienen referencia.
6. Actualizar `sections/results.tex`: nuevo bloque `figure*` único reemplazando los 4 actuales (líneas
   aproximadas 58–75, 79–96, 100–117, 153–170 — confirmar número exacto antes de editar), aplicar la tabla de
   referencias cruzadas de §4, envolver en `\revblue{}`.
7. Actualizar `PROGRESS.md`: fila `N-01` de `drafted` → `applied` una vez promovido y `results.tex` actualizado.
8. `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh` antes de cualquier commit.
