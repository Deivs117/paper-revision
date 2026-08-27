# N-02 — Physical-Section Figure Regeneration (Tarea 3)

**Goal:** regenerate every figure in the manuscript's physical/real-robot results subsection,
either from CSV (where `experiments/real/` has it, per the Tarea 2 `MANIFEST.md`) or by vectorizing
the currently-published PNG (where it doesn't) — validating each against the original before it's
ever promoted to `assets/`.

**Scope note:** the author explicitly included the MLP-classifier block (`fig1_confusion_matrix`,
`fig4_architecture_ablation`, `fig5_classifier_comparison`, `fig6_computational_cost`) in this
task's scope 2026-08-27, even though it isn't physical-specific — see this repo's chat log /
`intake/pending/R02-01_data_traceability_and_plotting_plan.md` for that decision.

**Promotion policy (decision D-14, same round):** everything below lands in `output/`, reviewed by
hand before `scripts/promote_figure.sh` touches `assets/` — nothing here has been promoted yet.

## Done this round

### CSV-based rebuilds (`experiments/_plotting/builders/real_plot_suite.py`, `energy_transition.py`)

- `{Appetitive,Aversive,Obstacle,Complex}_Real_Plot_{1,2,3}.png` (12 figures) — Switching Delay ECDF,
  Basal Ganglia Dynamics, Pitch/Roll RMS, from `StimuliB/R/G_t0N` + `MultiRGB_t0N` (Complex, per D-2).
- `NEU_EST_UNIG_real.png` / `NEU_EST_MUL_real.png` — **simplified aggregate substitutes**, not full
  reproductions (see caveat below), output as `*_AGGREGATE_SUBSTITUTE.png`.
- `FigReal_Morphological_Transition_Energy.png` — from `Test_current_integrated_t01/imu_ina.csv`
  (see data-quality caveat below).

### Vectorized (`experiments/_plotting/extract/extract_fig5.py`, `extract_fig6.py`)

- `fig5_classifier_comparison.png` + `fig6_computational_cost.png` → fused into
  `fig_classifier_tradeoff_fused.png` (F-03, confirmed D-3). See
  `experiments/_plotting/vectorized/README.md` for the extraction method and validation.
- `fig1_confusion_matrix.png` / `fig4_architecture_ablation.png` — **not** vectorized (F-Data-06:
  their values are already exact in `results.tex` prose), regenerated directly from those numbers.

## New findings this round (corrections to earlier diagnosis — document, don't silently fix)

1. **`combined_metrics.csv`'s `Tswitch` column semantics, reverse-engineered:** it's a step
   function — `0.0` placeholder before the mode switch, then a single plateaued value for the rest
   of the recording. "Switching delay" = `max(Tswitch.dropna())` per trial. Verified row-by-row on
   `StimuliB_t01` (5 rows at `0.0`, then 283 rows at a bit-identical `0.875503...`). Resulting
   per-scenario delays are physically sensible and match `results.tex`'s own qualitative claims
   (Aversive/Obstacle: few milliseconds, "near-zero computational tick" reflex; Appetitive/Complex:
   0.15–13 s, "extended settling window" from trajectory smoothing) — see
   `output/*_Switching_Delay_ECDF.png`.
2. **`Test_current_integrated_t01/imu_ina.csv`'s `power_W` column has an implausible magnitude**
   (~1e-4 W; `voltage_V`~0.00125 V is far too small for a robot battery rail — plausibly an
   uncalibrated raw ADC register, e.g. an INA219-style sensor's raw count never multiplied by its
   conversion factor). The regenerated `FigReal_Morphological_Transition_Energy.png` still locates
   a transition instant from the *relative* power-draw peak (t≈24.8s into the trial) but the
   absolute Joule figures should not be trusted until this is resolved. There's also an unused
   `robot_cmd` column (teleoperation key codes) that's a more direct candidate marker for the
   transition instant than an inferred power peak — not used here for lack of a key→action mapping
   anywhere in this repo.
3. **`NEU_EST_UNIG_real.png`/`NEU_EST_MUL_real.png` cannot be fully reproduced from
   `experiments/real/`** — Informe 2 originally marked these "✅ Completo", but that verdict only
   checked that *a* CSV exists (`neural_metrics.csv`), not that it has the *specific* columns the
   published figure needs. The published figures show individual per-neuron activations
   ($X_0$..$X_{16}$, gait-decision module, LiDAR "Auxiliary" subplot); `neural_metrics.csv` only has
   aggregate columns (`firing_variance`, `temporal_consistency`, `lambda_efficiency`, `mode`,
   `red_present`, `blue_present`). This is the same class of gap as F-Data-04/05 (simulation
   IMU-terrain rasters), just not previously caught for the physical versions. The
   `*_AGGREGATE_SUBSTITUTE.png` outputs are a stand-in built from what's actually available, not a
   drop-in replacement — full reproduction needs either the per-neuron log (if it exists
   unexported somewhere) or vectorization of the published PNGs, same as the terrain-IMU figures
   below.

## Vectorization tier — completed 2026-08-27 (round 2)

All 5 remaining figures are now vectorized, regenerated, and validated (re-plotted + compared
against the published PNG) — see `experiments/_plotting/vectorized/README.md` for the full method/
validation notes per figure, and `experiments/_plotting/builders/imu_terrain_real.py` for the
regeneration code. Summary:

1. **`GRAPH_IMU_real.png` / `GRAPH_IMU2_real.png`** — turned out to be categorical 3-row
   (Stuck/Flat/Inclined) binary state heatmaps, not continuous dual-axis series (Informe 1 already
   flagged this). Regenerated with F-05's `N0`/`N1`/`N2` notation applied to the row labels. Method:
   `extract_graph_imu_real.py`, fully automatic per-image calibration (no hardcoded pixel numbers).
2. **`NEU_IMU_real.png` / `NEU_IMU2_real.png`** — 4-subplot per-neuron grayscale rasters. Contrary
   to Informe 2's original "✅ Completo" verdict for the *simulation* versions of these figures,
   the per-neuron activation data turned out to be recoverable directly from the published PNG's
   pixel intensities (each row genuinely is one neuron's grayscale-coded activation) — no separate
   raw log was needed after all for the physical versions once vectorized. Reported as normalized
   0–1 activation per panel (magnitude isn't cited numerically anywhere in `results.tex` for these
   figures, only activation timing is). Method: `extract_neu_imu_real.py`.
3. **`FigReal_Terrain_Latencies_4Panels.png`** — step-ECDF, N=15 hardware replicates per panel;
   extraction locates each step-jump's x-position, calibrated per panel from its own gridlines.
   Method: `extract_terrain_latencies.py`. Caveat: replicate *multiplicity* per jump isn't
   preserved (shape-correct reconstruction, not guaranteed value-exact per replicate) — see
   `vectorized/README.md`.

**Outstanding, lower priority:** the terrain-latencies ECDF reconstruction could be made
value-exact (not just shape-correct) by extending `extract_terrain_latencies.py` to also read each
step's height (not just its x-position) and infer replicate multiplicity from it — not done this
round because the shape-correct version is already sufficient for the figure's qualitative role in
`results.tex`'s current prose (no exact per-replicate values are cited there).
