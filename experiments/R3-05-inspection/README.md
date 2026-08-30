# R3-05 — Reactive Inspection Task Metrics (Experiment E)

**Reviewer ask (#3.5, HIGH):** "The paper only mentions inspection as a target scenario but does
not design inspection-oriented task indicators such as target tracking accuracy, coverage rate, and
autonomous re-planning ability after obstacle blockage, lacking practical engineering demonstration."

Full diagnosis, code-level analysis, and per-metric argument for the referee live in
`intake/pending/R3-05_inspection_handoff.md` (kept as the authoritative narrative source — this
README only covers the data/regeneration side). The actual writing plan derived from this data is
`intake/pending/R3-05-inspection_writing_plan.md`.

## Goal

Produce the aggregate statistics table and the `d_final` vs `N_lidar_events` scatter figure for the
new "Reactive Inspection Task" subsection in `sections/results.tex` (Simulation Results, after
Complex Navigation / before Physical Implementation Results). `PROGRESS.md` row `R3-05`.

## Method

`scripts/aggregate_and_plot.py` reads all 20 trial folders in `data/`, reading each
`inspection_summary.json` (per-trial `success`, `d_final_m`, `N_lidar_events`, `N_mode_X_events`,
`T_acquisition_s`, `z17_peak`) and each `trial_summary.json` (`final_metrics.sim_time_s`). It:

1. Computes mean/SD/min/max of `d_final_m`, `N_lidar_events`, `N_mode_X_events`, `T_acquisition_s`,
   `sim_time_s` over the 17 `SUCCESS` trials → `output/inspection_summary_stats.csv`.
2. Computes SR = 17/20 = 85%.
3. Computes the same breakdown split by the "clean" vs "elevated" `N_lidar_events` pattern (see
   point 4) → `output/inspection_group_stats.csv`. Added after a caption-writing pass revealed the
   pooled SD alone hides an asymmetry between the two groups (see point 4) — kept as a committed,
   traceable number instead of leaving that claim resting on eyeballing the PNG.
4. Produces `output/fig_dfinal_vs_nlidar.png`: single-panel scatter, `N_lidar_events` (x) vs
   `d_final_m` (y), 17 points (successes only — failures have no `d_final_m`), marker color/shape
   split by the "clean" vs "elevated" `N_lidar_events` pattern described in the handoff §9.3
   (threshold: `N_lidar_events < 10` clean / `>= 10` elevated — chosen because it cleanly separates
   the two clusters in the data: clean trials sit at 4–7, elevated trials at 11+, no trial falls
   in between). Purpose: show that `d_final` does not degrade with path complexity.
   **Verified reading of the actual image + `inspection_group_stats.csv` (not assumed from the
   generation code):** the elevated group is in fact *tighter* around the stopping point
   (μ=1.065 m, σ=0.022 m, range 0.046 m, n=5) than the clean group (μ=1.081 m, σ=0.042 m, range
   0.139 m, n=12) — see `intake/pending/R3-05-inspection_writing_plan.md` §0bis for the mandatory
   verification protocol this triggered and why the pooled-SD-only framing was insufficient.

No inferential statistics (t-test, etc.) — this is a descriptive/illustrative figure for an n=17
observational dataset (n=5 in the elevated subgroup), not a hypothesis test; the writing plan
explicitly cautions against over-reading the tighter-elevated-group pattern given that sample size.

## Parameters / seed

Not a stochastic script — it's a deterministic aggregation over pre-existing trial data. No
`config.yaml` (deleted from the copied template): nothing here is worth tracking as a run parameter
other than the clean/elevated threshold, which is documented inline in the script and above.

## Data provenance

- **Not regenerable from this repo.** `data/` (20 trial folders + `suite_execution_manifest.json`)
  is the simulation output handed off directly by the author, produced by running
  `familia_e_inspeccion` (20 repetitions, `obstaculos.world`, 90s timeout, no random perturbation)
  via `test_manager.py` inside `PETER_SIMULATION`.
- **Pinned commit:** `PETER_SIMULATION`, branch `sam`, commit `6d5a2e6` ("feat(exp-e): implementar
  experimento de inspección reactiva (Reviewer #3.5)") — this is the *only* branch that has
  `inspection_recorder.py` and the `familia_e_inspeccion` suite; `main`/`dieguito`/`Deiv` do not.
  See `intake/SOURCES.md`.
- `data/` was moved here verbatim via `git mv` from the flat `experiments/R3-05_inspection_results/`
  drop (2026-08-29) — no file contents were changed, only the path, to match the repo's
  `experiments/<ID>-<slug>/{data,scripts,output}` convention (README.md §9.1).

## How to regenerate

```
cd experiments/R3-05-inspection
python3 scripts/aggregate_and_plot.py
```

Requires `pandas`+`matplotlib` (exempt from the stdlib-only rule per README.md §9.2, same as every
other `experiments/*/scripts/` script).

## Output files

| File in `output/` | Promoted to (`assets/...`) | Used in |
|---|---|---|
| `inspection_summary_stats.csv` | — (table is typed directly into `results.tex`, not included as an image) | `sections/results.tex`, new Reactive Inspection Task subsection |
| `inspection_group_stats.csv` | — (numbers typed into the figure caption, not included as an image) | `sections/results.tex`, `Fig.~\ref{fig:inspection_dfinal_scatter}` caption |
| `fig_dfinal_vs_nlidar.png` | `assets/fig_inspection_dfinal_vs_nlidar.png` | `sections/results.tex`, `Fig.~\ref{fig:inspection_dfinal_scatter}` |
