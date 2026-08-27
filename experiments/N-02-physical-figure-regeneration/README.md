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

## Round 2 (2026-08-27) — author audit via `n02_audit_notes_2026-08-27.md`

The author reviewed all 22 figures from round 1 through a local audit tool
(`~/Documents/Paper/audit_tool_N02.html`, not committed) and exported notes. Actions taken this
round, in the order decided:

1. **Style overhaul.** Imported the `matplotlib` and `scientific-visualization` Claude Code skills
   from https://github.com/K-Dense-AI/scientific-agent-skills into `.claude/skills/` (mirrored
   `SKILL.md` + `assets/publication.mplstyle` only, not the full 163-skill/163-reference tree — see
   each skill's own "not mirrored" note for how to fetch more on demand). `experiments/_plotting/style.py`
   now loads that `.mplstyle` (Okabe-Ito colorblind-safe 5-color palette, `axes.grid: False` by
   default, clean sans-serif, 300dpi). This alone fixed the "quitar grilla" requests on
   `GRAPH_IMU_real/2` and `NEU_IMU_real/2` — the grid was never intentional, it came from this
   pipeline's *first*-round `style.py` forcing `axes.grid: True` globally.
2. **Removed internal jargon from figures.** `fig4_architecture_ablation.png`'s title no longer
   says "F-06" (kept the *disclosure* itself — "y-axis truncated for legibility" — as a small
   in-panel annotation, since the `scientific-visualization` skill's guardrails require disclosing
   nonzero-baseline axis choices; only the internal task-ID reference was removed).
   `NEU_IMU_real/2_real.png`'s suptitle no longer references
   `experiments/_plotting/vectorized/README.md`.
3. **Removed circular markers** from the 4 scenario ECDF plots (`*_Real_Plot_1`).
4. **`*_Real_Plot_2_Basal_Ganglia_Dynamics.png` removed from the pipeline entirely** (12 figures:
   4 scenarios × sim/physical was never the count — it's 4 physical scenarios × this one plot type).
   Per the author: this answers the reviewer's "cut repetitive descriptions, duplicated neural
   raster plots and identical stability curves between simulation and physical tests" request.
   `*_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png` is kept and now shades its background
   red/blue wherever the aversive/appetitive stimulus was in the camera's view (resampled from the
   companion `neural_metrics.csv`), folding in what the removed figure used to show. **The
   `results.tex` rewrite that formally answers the reviewer comment is a separate, later pass** —
   not done this round, per the author's explicit instruction; this round only stopped generating
   the `_2` figure and added the shading. `build_bg_dynamics()` is kept (unused) in
   `real_plot_suite.py` as a data-source reference for that later pass.
5. **`NEU_EST_UNIG_real.png`/`NEU_EST_MUL_real.png` vectorized** (previously rejected
   "aggregate substitute" approach abandoned entirely, per the author: "no representan lo mismo...
   no rehacer"). Same pixel-intensity technique as `NEU_IMU_real/2`, generalized in
   `extract/extract_neu_est_real.py` — these two figures are structurally bigger (8 and 12 panels
   in a multi-column layout, vs. `NEU_IMU_real`'s single column of 4), which required a real fix to
   `extract_neu_imu_real.find_panel_boxes()`: side-by-side panel columns can share row-spans by
   coincidence, and a colorbar's own left+right border sitting between two real panel spines was
   getting mismatched as if it were a spine itself. Fixed by (a) filtering spine-candidate clusters
   by pixel *density* (a real spine, even several px thick, has every column present across its
   span; a colorbar's doublet border does not) and (b) a greedy nearest-distant-partner pairing
   instead of naive even/odd pairing. Also caught and fixed: `NEU_EST_UNIG_real.png`'s time axis
   labels every **10s**, not every 20s like every other figure processed so far — an early pass
   silently produced a time axis running to ~130s against the true ~65s range before this was
   caught by re-comparing the regenerated figure to the original.
6. **Morphological Transition Energy — rejected, redesign proposed, not yet built.** The author
   wants the figure to answer R2-04's reviewer requirement directly (long-term average energy
   consumption across locomotion modes, framed for onboard-deployment feasibility) by showing
   consumption *during* a mode transition and across *one* transition, not where the current peak
   happened to occur. Three design alternatives proposed for the author to pick from (none built
   yet — waiting on that choice, and on resolving the `power_W` calibration caveat from round 1
   first, since any of the three inherits that problem unless it's fixed):
   - **(a) Bar chart, energy per transition direction.** One bar for Quadrupedal→Differential
     Mobile, one for Differential→Quadrupedal, total Joules (or Wh) integrated over each
     transition's actual duration window (not the full trial) ± range across the available trials.
     Closest to what a reviewer asking about "long-term average energy consumption... for onboard
     deployment" would expect to see at a glance — directly comparable numbers, no time-series
     reading required.
   - **(b) Time series cropped to the transition window only**, one small panel per direction,
     x-axis re-zeroed to transition onset (not full-trial elapsed time) — keeps the shape
     information (does power ramp, spike, or step during the transition) that a bar chart discards,
     at the cost of being less immediately quotable as a single number.
   - **(c) Text/table only, no new figure** — a small table in `results.tex` (mean energy per
     transition direction, ± range, transition duration) if the author judges that a graph doesn't
     earn its space here versus the classifier fusion/latency figures already carrying the
     quantitative load of this subsection.
   Recommendation if forced to pick one: **(a)**, because it answers the reviewer's actual wording
   ("long-term average... consumption") most directly, and pairs naturally with (b) as a
   supplementary inset only if the shape genuinely matters to the argument — but this is the
   author's call, not decided here.

## Round 3 (2026-08-27, same day) — typography + `_Real_Plot_3` structural correction

Two fixes from the round-2 audit's second export (`n02_audit_notes_2026-08-27.md`, later revision):

1. **Serif typography is now the project's house default**, not a one-off override — confirmed by
   comparing against `assets/fig1_Obstacle_macro.png` (already serif) and applied to
   `.claude/skills/scientific-visualization/assets/publication.mplstyle`:
   `font.family: serif`, sizes 10/11/12/10/10/10 (general/axes-labels/axes-titles/xtick/ytick/legend)
   per the author's exact spec. This propagates to **any figure regenerated from here on**,
   including the not-yet-reviewed N-01 simulation figures. **Already-approved N-02 output PNGs were
   deliberately NOT re-regenerated** (would have silently changed accepted work) — they were
   restored via `git checkout` after an initial batch run touched them by accident. Only the
   still-pending figures (4 ECDF, 4 `_Real_Plot_3`, `FigReal_Terrain_Latencies_4Panels`) carry the
   new font.
2. **`_Real_Plot_3` structural bug found and fixed.** The round-2 rebuild incorrectly assumed this
   was always a single-panel RMS plot — verified against the published originals
   (`assets/Appetitive_Real_Plot_3_..._.png`, `assets/Aversive_Real_Plot_3_..._.png`) that it is
   and always was **two stacked panels**: A) Basal Ganglia Neural Response Dynamics (firing
   variance, fixed orange `#D55E00`) and B) Chasis Kinematic Attitude Stabilization Space
   (Pitch/Roll RMS, fixed purple/lavender, not scenario-colored). `build_rms_dynamics()` in
   `real_plot_suite.py` now restores both panels with their correct fixed colors; the red/blue
   stimulus-presence shading (round 2) moved from panel B to panel A, and only applies to
   Appetitive/Aversive/Complex — **not Obstacle**, whose stimulus is green and doesn't fit the
   red/blue scheme (confirmed explicitly by the author: "NO COLOREAR ESTÍMULOS A LA VISTA" for
   that scenario). Verified visually against all 4 regenerated outputs.
