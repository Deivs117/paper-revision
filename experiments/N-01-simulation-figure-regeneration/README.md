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

**Round 3 (2026-08-29, author audit `n01_audit_notes_2026-08-29.md`, plan `R02-01-04_simulacion_N01_grid_fusion_FigABC.md`):**
- `fig1_noise_robustness_grid.png` approved unchanged (layout final) and **promoted to `assets/`**
  (new asset, no prior name to replace). `sections/results.tex`'s 4 separate per-scenario
  robustness figures (`fig1_Appetitive/Aversive/Obstacle/Complex_macro.png`, each previously paired
  as subfigure (a) with its own `fig2_*_micro` trial as subfigure (b)) were replaced by this single
  figure; the 4 `fig2_*_micro` trial figures remain, now as standalone single-image figures instead
  of subfigure (b). The 4 old `fig1_*_macro.png` assets were `git rm`'d. Cross-reference remap: each
  scenario's `\label{fig:X_results}` combined-figure label is gone — Appetitive/Complex prose now
  points at `\label{fig:noise_robustness_grid}` (their claims are robustness/noise-sweep content),
  Aversive/Obstacle prose now points at their own `\label{fig:X_micro}` (their claims are
  single-trial temporal-dynamics content, not noise-sweep content). No literal panel letters
  (a)-(l) exist inside the fused grid image (the author's "gráficamente están perfectas" note meant
  don't touch the visual at all, so none were added) — the one prose mention that used to say
  "panel C of Figure~X" now says "the Decision Latency column, Appetitive row, of
  Figure~\ref{fig:noise_robustness_grid}" instead.
- `FigA_Stability_Profile.png`/`FigB_Decision_Delay.png`/`FigC_Terrain_Adaptability.png`: the 3
  audit adjustments from `R02-01-04` §1c implemented in `ecdf_phase_space.py` (FigA: dropped a
  redundant outer `fig.suptitle()` that was the actual cause of the "espacio perdido" title-spacing
  bug, not a margin-tuning issue; FigB: removed the $T_{\text{response}}$ ECDF panel, now 2 panels
  instead of 3, its 0.0s-for-all-trials result moved into `results.tex` prose instead; FigC: added
  a Pitch RMS boundary line + zone labels, criterion resolved directly from the figure's own
  existing caption text). All 3 re-promoted to `assets/` (`--force`, same filenames).
- `results.tex` validated (`validate_tex.sh`/`check_roundtrip.sh` both pass) after all of the above.

## Update 2026-09-02 (C-53: NEU_IMU/NEU_IMU2 — dropped the "Locomotion 2" panel)

- Per `redundancy_closing_audit_consolidation_2026-09-02.md`'s `[FIG-X17]` finding: `NEU_IMU.png`/
  `NEU_IMU2.png`'s "Locomotion 2" panel (neuron `X17`) was suspected inactive, but verified against
  `experiments/_plotting/vectorized/neu_imu.csv`/`neu_imu2.csv` to actually be tonically active
  near-constant (`activation_normalized` 0.502–1.0, mean 0.503, 731 samples) — not silent, just
  carrying no interpretable temporal variation for the reader.
- `experiments/_plotting/builders/imu_terrain_real.py::build_neu_imu()` gained an optional `panels`
  parameter (default unchanged, so `NEU_IMU_real`/`NEU_IMU2_real` in this same file's `__main__`
  are untouched); group-title/letter placement now derives its axes boundaries from the actual
  panel list instead of hardcoded indices, so it works for any panel subset.
- `regenerate_neu_panels.py`'s two `NEU_IMU`/`NEU_IMU2` call sites now pass
  `panels=["Locomotion_1", "Decision_1", "Decision_2"]`, dropping `Locomotion_2`. Re-ran the full
  script — the other 3 outputs (`NEU_EST_UNIB/UNIG/MUL.png`) regenerated byte-identical to the
  currently promoted assets (confirmed via `cmp`), confirming this change didn't touch them.
- Both new `output/NEU_IMU.png`/`NEU_IMU2.png` visually verified (3 panels, `a)`/`b)` letters and
  group titles still correctly positioned) before promoting to `assets/` with `--force`.
  `compile_pdf.sh` re-run clean; the rendered page (55) visually confirmed to match.
- No `results.tex` prose references `X17` or "Locomotion 2" by name (confirmed via `grep`), so no
  caption/prose rewording was needed beyond the image regeneration itself.
