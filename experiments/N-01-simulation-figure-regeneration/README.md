# N-01 — Simulation Figure Regeneration Pipeline (Tarea 1)

**Goal:** a reusable pipeline that turns a simulation results folder (the same layout as
`experiments/simulation/familia_*/test_NNN[_VERDICT]/*.csv|json`) into the noise-robustness grid,
`FigA/FigB/FigC`, and `tab:consolidated_simulation_metrics` — so that when the team re-runs the
simulated tests (notified 2026-08-27, only the simulated battery), regenerating every affected
figure is one command, not a manual re-derivation.

**Provenance:** built from the shared library `experiments/_plotting/` (loaders/builders/style),
following the architecture and the 11 confirmed decisions (D-1–D-11), now documented in
`intake/pending/R02-01-05_simulacion_grupo2_vectorizacion.md` (§4) and `intake/processed/R02-01-02_fisico_regeneracion_N02-N05.md`
(§2) — see `intake/R02-01_INDEX.md` for the full block index. Council decisions specific to this
experiment, made 2026-08-27 in the follow-up planning round:

- **D-12 (versioning):** a future re-run lands in a **new sibling directory** next to the current
  `experiments/simulation/familia_*` folders (e.g. `experiments/simulation_2026XXXX/` or
  `familia_a_apetitivo_v2/` — exact naming TBD when the run actually lands), never overwriting the
  current ones. This pipeline takes `--simulation-root` as a CLI flag for exactly this reason — no
  code change needed to point it at the new batch, only the root path.
- **D-13 (execution scope):** built AND already executed once against the current
  `experiments/simulation/` data (this round), producing the files in `output/` below, to prove the
  pipeline end-to-end and leave a byte-fresh, code-traceable version of the already-published
  figures on hand.
- **D-14 (promotion):** output stays in `output/` for manual review — **not** promoted to `assets/`
  automatically. `scripts/promote_figure.sh` remains the only path into `assets/`, run by hand once
  the author has compared `output/` against the current published figures and (for M-01–M-04)
  decided the text redaction in `results.tex`.

## Scripts

- `experiments/_plotting/builders/macro_robustness.py` — the fused 4x3 noise-robustness grid
  (Informe 1 F-02, confirmed D-9) + `tab:consolidated_simulation_metrics` recompute.
- `experiments/_plotting/builders/ecdf_phase_space.py` — `FigA_Stability_Profile`,
  `FigB_Decision_Delay`, `FigC_Terrain_Adaptability` (the M-01–M-04 figures, already verified
  correct against this exact data in Informe 2 §0 — this regenerates a fresh, code-traceable copy,
  it does not change any number).
- `experiments/_plotting/generate_all_simulation.py` — entry point, calls both builders.

Run (from repo root, using the project's own throwaway venv — `experiments/.venv_plotting/`,
gitignored, created with `python3 -m venv experiments/.venv_plotting && experiments/.venv_plotting/bin/pip install numpy matplotlib pandas pillow`):

```bash
experiments/.venv_plotting/bin/python experiments/_plotting/generate_all_simulation.py \
  --simulation-root experiments/simulation \
  --output-dir experiments/N-01-simulation-figure-regeneration/output
```

## New finding this round — correction to Informe 2's F-Data-01

Running the pipeline against `familia_a_obstaculo` surfaced a mistake in Informe 2's original
diagnosis of F-Data-01: it assumed `metrics_raw.csv`'s `latency_s` column was populated for this
scenario (as a fallback for `trial_summary.json`'s `-1.0` sentinel). **It is not** — verified
directly: **0 of the 15 `familia_a_obstaculo` trials have a single non-empty `latency_s` value in
either file.** There is currently no recorded latency source for the Obstacle scenario anywhere in
`experiments/simulation/`. The regenerated grid (`output/fig1_noise_robustness_grid.png`) renders
an explicit "No latency data recorded in this run" annotation in that panel instead of silently
plotting zeros or an empty axis (as the very first draft of this pipeline accidentally did before
this was caught).

**Action item, folds naturally into the upcoming re-run (Task notified 2026-08-27):** when the
simulated battery is re-run, confirm the Obstacle scenario's latency instrumentation is actually
wired up before archiving the new `familia_a_obstaculo/` folder — otherwise this gap repeats. Until
then, `fig1_Obstacle_macro.png`'s currently-published panel C (which per Informe 1 shows normal
latency values) cannot be reproduced from anything in this repository; if that figure needs to
stay in the paper as-is, it should be treated as a vectorization candidate (Informe 2 §2 method),
not a CSV rebuild.

**Full list for the simulation team:** this is one of 10 items (4 blocking, 6 minor) found while
building this pipeline — see `experiments/simulation/SIMULATION_TEAM_ACTION_ITEMS.md` for the
complete, evidence-backed list to hand off before the re-run.

## Output

- `output/fig1_noise_robustness_grid.png` — fused 4x3 grid replacing the 4 `fig1_*_macro.png`.
- `output/FigA_Stability_Profile.png`, `output/FigB_Decision_Delay.png`,
  `output/FigC_Terrain_Adaptability.png` — regenerated from `experiments/simulation/familia_c1_terreno_rugoso`
  / `familia_c2_pendiente`, visually consistent with the currently published versions (spot-checked
  against Informe 1's own pixel-level description: flat TR≈0.58–0.60 with a transient bump around
  t=-1.3s to -0.5s in Rugged Terrain, flat TR≈0.59 in Inclined Slope — matches).
- `output/tab_consolidated_simulation_metrics.csv` — recomputed `tab:consolidated_simulation_metrics`
  values, for cross-checking against the currently published table before promoting.

## Update 2026-08-27 (R02-01-04/05 generated, staged for author review — NOT promoted)

Everything flagged above as pending has been regenerated into `output/`, but **none of it has been
promoted to `assets/` yet** — the author needs to review each figure individually first (same gate
as N-02's physical figures went through before their own promotion). An earlier pass in this round
promoted these to `assets/` and updated `results.tex` before that review happened; it was reverted
(assets restored to their prior published versions, `results.tex` reverted to reference the
original figures, `PROGRESS.md`'s N-01/N-06/N-07/N-08 rows moved back to `drafted`) so the review
can happen against the correct baseline. The generation code and CSVs below are unaffected by that
revert and remain ready to be promoted once confirmed.

- **Obstacle latency gap:** addressed by vectorizing the currently-published `fig1_Obstacle_macro.png`
  panel C (`experiments/_plotting/extract/extract_fig1_obstacle_latency.py` →
  `vectorized/fig1_obstacle_latency.csv`), since the simulation re-run did not land before the
  2026-08-31 deadline. `macro_robustness.py` now reads this file with a fallback chain (vectorized
  → real CSV → "no data" annotation), so pointing `--simulation-root` at the eventual re-run and
  removing this CSV switches back to real data with no code change. Output (grid + FigA/B/C) is in
  `output/`, awaiting review.
- **F-01 (simulation NEU_EST/NEU_IMU mistranslation):** all 5 figures (`NEU_EST_UNIB/UNIG/MUL`,
  `NEU_IMU`, `NEU_IMU2`) vectorized and re-plotted with the corrected "Gait Decision Module"/
  "Auxiliary" labels — output in `output/`, awaiting review.
- **F-04 (`GRAPH_IMU`/`GRAPH_IMU2` mixed single axis):** vectorized and re-plotted with a double
  Y-axis, corrected legend, and the `$U_{\sigma_{az}}$=3.7` threshold line — output in `output/`,
  awaiting review.
- **F-08 (`fig_stability_phases.png`, N=268 walk cycle):** vectorized and re-plotted, real
  geometry — output in `output/`, awaiting review.
- **`RES_IMU.png`/`RES_IMU2.0.png`:** confirmed to be Gazebo screenshot composites (no chart
  data) — no action needed, same category as F-07.

New scripts added this round: `experiments/_plotting/extract/extract_neu_est_sim.py`,
`extract_stability_phases.py`, `extract_graph_imu_sim.py`; `experiments/_plotting/builders/
stability_phases.py`, `imu_dual_axis.py` (reused the existing `imu_terrain_real.build_neu_est()`/
`build_neu_imu()` for the NEU_EST/NEU_IMU re-plots, no new builder needed there).

**Still open, out of scope for this round:** re-running `macro_robustness.py`'s
`build_consolidated_table()` produces `Success%`/`T_sim`/`Roll`/`Pitch` numbers that do not match
`tab:consolidated_simulation_metrics` as currently published (e.g. Obstacle Roll: 3.93±8.92
recomputed vs. 0.55±0.02 published) — flagged in `PROGRESS.md`'s `N-01` row, not investigated or
acted on here.
