# experiments/_plotting/vectorized/ — hand-extracted figure data (trazabilidad inversa)

Every CSV here was extracted directly from a currently-published PNG in `assets/` because no raw
CSV/notebook source survives for it (Informe 2, decisions D-1/D-11). **Method used: direct
pixel-color extraction in Python** (`experiments/_plotting/extract/color_extract.py` + one
`extract_<figure>.py` script per figure), not WebPlotDigitizer-by-browser — D-11 was refined this
round (2026-08-27) once the work moved from "a human would do this by hand" to "an agent executes
this by code": precise pixel-coordinate calibration is more reliable and fully reproducible from a
committed script than driving a browser UI through simulated clicks. Same underlying principle as
D-11 (isolate each data series by its known plot color, calibrate axes from known reference points)
— just executed as a script instead of a manual tool session.

## Rule for every entry below

1. A dedicated `extract_<name>.py` script in `experiments/_plotting/extract/`, with the exact pixel
   calibration (axis spine/gridline rows, color tolerances) documented in its own docstring —
   never just a bare CSV with no way to reproduce it.
2. A row in the table below: source PNG, method, and a validation note (does the re-plotted figure
   match the original's visible shape/relative magnitudes).
3. Never overwrite a `vectorized/*.csv` in place — if a figure needs re-extraction, bump the
   calibration in the extract script and note why in its docstring; git history is the audit trail.

## Extracted so far

| CSV | Source PNG | Script | Validation |
|---|---|---|---|
| `classifier_fig5.csv` | `assets/fig5_classifier_comparison.png` | `extract_fig5.py` | Re-plotted as panel (a) of `fig_classifier_tradeoff_fused.png` (N-02 output) — bar ordering/relative heights per classifier match the original (Random Forest highest across all 4 metrics, Logistic Reg. lowest, SVM/MLP in between) to visual inspection. Absolute values (e.g. accuracy 0.945–0.950 for Random Forest) were **not independently confirmed against a raw training log** (none survives) — this is the PNG's content read at pixel precision, not a re-run of the classifier. |
| `classifier_fig6.csv` | `assets/fig6_computational_cost.png` | `extract_fig6.py` | Re-plotted as panels (b)/(c) of the same fused figure — log-scale ordering matches the original exactly (latency: Random Forest > SVM > MLP > Logistic Reg.; model size: SVM > MLP > Random Forest > Logistic Reg.) and the two panels were calibrated **independently** (different px/decade spacing measured directly from each panel's own gridlines, not assumed shared). |

## Extracted 2026-08-27 (round 2 — the "harder tier")

| CSV | Source PNG | Script | Validation |
|---|---|---|---|
| `terrain_latencies.csv` | `FigReal_Terrain_Latencies_4Panels.png` | `extract_terrain_latencies.py` | Step-ECDF, N=15 replicates/panel — extraction locates each visible step-jump's x-position per panel, calibrated independently per panel from its own dashed vertical gridlines (values read off the published tick labels). Re-plotted (`imu_terrain_real.py::build_terrain_latencies`) — panel shapes, x-ranges, and relative step spacing match the original closely (8/11/12/10 jumps found for panels A/B/C/D, matching a visual step-count check of the original). **Caveat:** the extractor records distinct jump *positions*, not each jump's replicate-count (multiplicity) — the regenerated ECDF assumes N/steps replicates evenly per jump rather than the exact original tie pattern, so it's shape-correct but not guaranteed value-exact per replicate. |
| `graph_imu_real.csv`, `graph_imu2_real.csv` | `GRAPH_IMU_real.png`, `GRAPH_IMU2_real.png` | `extract_graph_imu_real.py` | Categorical 3-row (Stuck/Flat/Inclined) binary state heatmap, not a continuous series (Informe 1 already noted this). Fully-automatic per-image calibration (spine + tick-mark pixel detection, no hardcoded numbers). Re-plotted and compared side-by-side against the original — transition timing (e.g. the striped region ~43-56s and ~65-90s in `GRAPH_IMU_real`) matches to visual inspection. |
| `neu_imu_real.csv`, `neu_imu2_real.csv` | `NEU_IMU_real.png`, `NEU_IMU2_real.png` | `extract_neu_imu_real.py` | 4-subplot per-neuron grayscale raster (Locomotion 1/2, Decision 1/2). Panel boxes auto-detected by pairing spine ROWS with spine COLUMNS of matching span (a naive row-only detector mis-identified boundaries because a fully-active neuron's solid data band is indistinguishable from a spine by row alone — see the script's docstring). Activation reported **normalized 0–1 per panel**, not rescaled to each panel's own colorbar units, because `results.tex`'s narrative about these figures is about *when* a neuron activates, never the raw magnitude. Re-plotted and visually compared against the originals — X13/X4/X8/X9/X11/X12 solid-active bands, the X0/X1 and X15/X16 striped/transition patterns all match at the timing level. |

## Method notes carried over from round 1 (still apply)

- Legend boxes / colorbars sharing bar colors must be explicitly excluded before color-masking (see `extract_fig5.py`) or explicitly separated from the main axes box by span-clustering (see `extract_neu_imu_real.py`) — the single biggest source of extraction bugs this round was accidentally including a legend/colorbar patch as if it were data.
- Always validate by re-plotting from the extracted CSV and eyeballing it next to the original before trusting the numbers — three of the five extractions in round 2 needed a bug fix (an `axis=1`/`axis=0` mean-direction bug, a right-spine-vs-colorbar-edge confusion, a tick-mark-row-offset error) that only became obvious once the first re-plot came out visibly wrong. This is exactly the point of the validation step, not a sign anything is unusually fragile here.

All five figures originally flagged in `experiments/N-02-physical-figure-regeneration/README.md`
§"Remaining work" are now done — see that file's updated status.

## Extracted 2026-08-27 (round 3, after author audit) — NEU_EST_UNIG/MUL_real

| CSV | Source PNG | Script | Validation |
|---|---|---|---|
| `neu_est_unig_real.csv` | `NEU_EST_UNIG_real.png` | `extract_neu_est_real.py` | 8-panel multi-column raster (Lidar Network / Locomotion / Gait Decision modules). Re-plotted and compared against the original — matches closely (Lidar L3/L4 and Locomotion X8/X9/X11 activity windows ~35-50s, Decision X15/X16 block pattern). Required generalizing `extract_neu_imu_real.find_panel_boxes()` for multi-column layouts (see that script's docstring) and fixing a hardcoded 20s tick-step assumption — this figure's x-axis actually labels every 10s. |
| `neu_est_mul_real.csv` | `NEU_EST_MUL_real.png` | `extract_neu_est_real.py` | 12-panel layout (adds a 4-panel Basal Ganglia column: GPi/GPe/STN/STR, R/G/B rows). Re-plotted and compared — activity windows (~24-35s, ~43-50s, late gradient ~70-90s) match the original across all 4 columns. |

Both supersede the round-1 CSV-based "aggregate substitute" for these two figures, which the author
rejected outright ("no representan lo mismo... no rehacer") — that substitute approach is no longer
part of the pipeline (`real_plot_suite.py`'s old `build_neu_est()` was deleted, not just deprecated).

## Extracted 2026-08-27 (R02-01-04 §5 step 1) — fig1_Obstacle_macro.png panel C

| CSV | Source PNG | Script | Validation |
|---|---|---|---|
| `fig1_obstacle_latency.csv` | `assets/fig1_Obstacle_macro.png` (panel C, "Decision Latency Profile") | `extract_fig1_obstacle_latency.py` | `experiments/simulation/familia_a_obstaculo` has 0/15 populated latency values in either `trial_summary.json.exp_latency` or `metrics_raw.csv.latency_s` (verified directly -- corrects Informe 2's original F-Data-01 diagnosis, which assumed `metrics_raw.csv` had it). Panel C's errorbar plot (5 points, sigma=0..4, teal-green `(0,158,115)`) was vectorized by pixel color: x/y gridlines calibrated from the panel's own dashed gridlines, mean/SD read from the symmetric-yerr error-bar extent (top/bottom cap midpoint = mean, half-span = SD) -- confirmed this matches `macro_robustness.py`'s own symmetric-yerr convention for the other 3 (real-data) scenarios in the same figure. Result: sigma=[0,1,2,3,4] -> mean=[1091.2, 1211.4, 1315.7, 1518.2, 991.5] ms, sd=[55.9, 531.3, 402.8, 519.2, 36.3] ms -- matches a plain visual read of the published PNG at each point to within a few percent. Consumed by `macro_robustness.py`'s Obstacle-row latency column (falls back to the "no data" annotation if this CSV is absent) and by `fig1_noise_robustness_grid.png`'s fused rejilla. **This is reconstructed by vectorization of a previously-published figure, not derived from a fresh simulation run -- flagged as such in `results.tex`'s figure caption/prose, per the project's standard traceability discipline (never present vectorized data as if it were raw CSV).**

## Extracted 2026-08-27 (R02-01-05 §1, corrects the report's own diagnosis) — NEU_EST_UNIB/UNIG/MUL (simulation)

| CSV | Source PNG | Script | Validation |
|---|---|---|---|
| `neu_est_unib.csv` | `assets/NEU_EST_UNIB.png` | `extract_neu_est_sim.py` | R02-01-05 §1 claimed these 3 simulation NEU_EST figures had real per-neuron CSV available (`metrics_raw.csv`) and did not need vectorizing -- **wrong, corrected here**: `metrics_raw.csv` in all 3 source families (`familia_a_apetitivo`/`familia_a_obstaculo`/`familia_b_compleja`) has only aggregate columns (`firing_variance`, `temporal_consistency`, `lambda_efficiency`, `mode`, `red_present`, `blue_present`), no per-neuron X0-X17/L0-L4 columns anywhere -- same class of report error as F-Data-01 (Obstacle latency, R02-01-04). Vectorized instead, reusing `extract_neu_est_real.py`'s generic panel-detection/intensity-extraction unchanged (2-panel-module layout: Locomotion Module + Gait Decision Module, 4 boxes). Re-plotted via `imu_terrain_real.build_neu_est()` (same function used for the already-approved `_real` versions) and compared against the original -- X3/X6/X7/X9-X13 Locomotion activity, X0 dashed + X3 gradient in Decision 1, X16 solid block in Decision 2, X17 late-activation block in Locomotion 2 all match. |
| `neu_est_unig.csv` | `assets/NEU_EST_UNIG.png` | `extract_neu_est_sim.py` | Same correction as above. Confirmed this figure's panel layout/order is IDENTICAL to the already-vectorized `NEU_EST_UNIG_real.png` (8 panels: Lidar/Input/Response/Auxiliary + Locomotion_1/2 + Decision_1/2) -- reused `UNIG_PANELS`' neuron-label structure directly, only the per-image tick_step differs (5s here vs. 10s for the physical version). Re-plotted and compared -- Lidar L0/L3/L4, Input/Response/Auxiliary rows 1-5, Locomotion_1 X6/X9-X12, Decision_1 X0 (dashed)/X4, Decision_2 X14/X16 all match. |
| `neu_est_mul.csv` | `assets/NEU_EST_MUL.png` | `extract_neu_est_sim.py` | Same correction as above. Layout confirmed identical to `NEU_EST_MUL_real.png`'s 12-panel order (Basal Ganglia GPi/GPe/STN/STR + Locomotion_1/2 + Lidar/Input/Response/Auxiliary + Decision_1/2). Needed `find_panel_boxes(row_span_tol=10)` (new optional parameter, default stays 6) instead of the shared default -- this image's "Input" panel's left/right spine black-runs differ by 7px top-to-bottom (antialiasing), just outside the default tolerance, causing it to go undetected (11/12 boxes found) at tol=6. Confirmed the higher tolerance is scoped to this call only: re-running the two already-approved `_real` extractions with tol=10 instead breaks them (UNIG_real jumps from 8 to 15 detected boxes) -- tested, not assumed, so the shared function's default remains 6 and only this one call opts into 10. Re-plotted and compared -- GPi/GPe/STN/STR R/G/B patterns, Locomotion_1 X3-X13, Locomotion_2 X17 late block, Lidar L0/L3, Decision_1 X0/X3/X4, Decision_2 X14/X15/X16 all match. |

All three correct F-01's "March Decision Module" -> "Gait Decision Module" and "Auxiliar" -> "Auxiliary" mistranslation via `build_neu_est()`'s already-corrected group-title strings (same fix already applied to the `_real` counterparts) -- no separate title-fix step needed, it falls out of reusing the same rendering function.

## Extracted 2026-08-27 (R02-01-05 §3, Group A) — fig_stability_phases.png

| CSV | Source PNG | Script | Validation |
|---|---|---|---|
| `stability_phases.csv` | `assets/fig_stability_phases.png` | `extract_stability_phases.py` | $N=268$ walk-cycle run never archived to `experiments/` (confirmed again, no `stability_log.csv` has 268 rows). Vectorized real geometry (stance-foot + swing-foot marker pixel coordinates, color-masked, calibrated against each panel's own -0.3..0.3m gridlines — one global 1950px/m scale, confirmed shared across all 6 panels) rather than fabricating positions; CoM is not extracted (body-frame plot, always at the origin by construction). Had to exclude a green-mask false-positive: the 4 swing-phase panels' "TR = x.xxx" label box uses a similar green tone to the stance-foot markers, initially leaking 4-5 spurious "feet" per panel — fixed by dropping clusters with data-y > 0.25 (stance feet never appear there). Incenter/inradius for the 4 triangular panels computed analytically from the extracted vertices (standard side-weighted incenter, area/semiperimeter), not pixel-extracted, since it's an exact derived quantity given real vertices. TR/SM/timestamp/phase-name text read directly off the figure (plain labels, not calibrated pixel values) — per D-6 (unchanged), `tab:crawl_stability`'s numbers stay the source of truth; this figure is redrawn only to accompany them with a code-traceable version. Re-plotted (`experiments/_plotting/builders/stability_phases.py`) and compared side-by-side against the original — polygon shapes, stance/swing/CoM positions, incenter circles, and all TR/SM/Static-stance labels match panel-for-panel (A/C/D/F triangles with TR 0.706/0.748/0.774/0.746; B/E quadrilaterals, no TR/SM shown, matching the original).
