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

## Not yet extracted (Tarea 3, remaining work)

Five physical terrain-IMU figures still need this treatment — flagged as the harder tier (dense,
continuous time series vs. the discrete bar charts above) rather than rushed with unreliable
calibration: `GRAPH_IMU_real.png`, `GRAPH_IMU2_real.png`, `NEU_IMU_real.png`, `NEU_IMU2_real.png`,
`FigReal_Terrain_Latencies_4Panels.png`. See
`experiments/N-02-physical-figure-regeneration/README.md` §"Remaining work" for the concrete next
steps and why they were sequenced after the two done here.
