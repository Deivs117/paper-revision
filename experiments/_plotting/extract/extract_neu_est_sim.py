"""Vectorizes assets/NEU_EST_UNIB.png / NEU_EST_UNIG.png / NEU_EST_MUL.png (simulation neural
rasters) -> experiments/_plotting/vectorized/neu_est_{unib,unig,mul}.csv

CORRECTS intake/pending/R02-01-05_simulacion_grupo2_vectorizacion.md §1's diagnosis: it claimed
these 3 figures had real per-neuron CSV available (`metrics_raw.csv` columns sim_time_s, mode,
red_present, blue_present, firing_variance, temporal_consistency, lambda_efficiency) and did not
need vectorizing. Direct inspection of `metrics_raw.csv` in all three source families
(familia_a_apetitivo / familia_a_obstaculo / familia_b_compleja) shows NO per-neuron (X0-X17,
L0-L4) columns exist anywhere -- only aggregate metrics. These figures show individual-neuron
raster activations, which cannot be reconstructed from aggregate firing_variance/lambda_efficiency.
Same situation as the already-corrected F-Data-01 (Obstacle latency, see R02-01-04) -- the report's
"CSV real disponible" claim was wrong here too, confirmed by directly checking the file, not by
trusting the report's column list.

Reuses `extract_neu_imu_real.find_panel_boxes()` / `find_x_ticks()` / `PanelSpec`, and the same
column-first panel-detection + per-panel intensity-band extraction as
`extract_neu_est_real.extract()`, unmodified -- these 3 simulation figures turned out to share the
EXACT panel layout/order as their already-vectorized `_real` counterparts (confirmed by visual
side-by-side comparison): NEU_EST_UNIG.png matches UNIG_PANELS' 8-panel order, NEU_EST_MUL.png
matches MUL_PANELS' 12-panel order. NEU_EST_UNIB.png (2 modules, no Lidar) is smaller than either
existing spec, so it gets its own 4-panel list built from the same neuron-label sublists.

Per-image tick_step (read directly off each figure's own labeled x-axis ticks, NOT assumed from
the _real counterpart -- these are different simulation runs with different durations):
  NEU_EST_UNIB.png: ticks every 10s (0..70)
  NEU_EST_UNIG.png: ticks every 5s (0..25)
  NEU_EST_MUL.png:  ticks every 20s (0..80)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_neu_imu_real import PanelSpec  # noqa: E402
from extract_neu_est_real import extract  # noqa: E402

LOCOMOTION_1 = [f"X{i}" for i in range(3, 14)]
LOCOMOTION_2 = ["X17"]
DECISION_1 = [f"X{i}" for i in range(0, 5)]
DECISION_2 = ["X14", "X15", "X16"]
LIDAR = [f"L{i}" for i in range(5)]
INPUT16 = [str(i) for i in range(1, 17)]

UNIB_PANELS = [
    PanelSpec("Locomotion_1", LOCOMOTION_1, colorbar_max_visual_estimate=75),
    PanelSpec("Locomotion_2", LOCOMOTION_2, colorbar_max_visual_estimate=1.2),
    PanelSpec("Decision_1", DECISION_1, colorbar_max_visual_estimate=75),
    PanelSpec("Decision_2", DECISION_2, colorbar_max_visual_estimate=4.5),
]

UNIG_PANELS = [
    PanelSpec("Lidar", LIDAR, colorbar_max_visual_estimate=1.1),
    PanelSpec("Input", INPUT16, colorbar_max_visual_estimate=0.4),
    PanelSpec("Response", INPUT16, colorbar_max_visual_estimate=0.3),
    PanelSpec("Auxiliary", INPUT16, colorbar_max_visual_estimate=0.3),
    PanelSpec("Locomotion_1", LOCOMOTION_1, colorbar_max_visual_estimate=115),
    PanelSpec("Locomotion_2", LOCOMOTION_2, colorbar_max_visual_estimate=0.1),
    PanelSpec("Decision_1", DECISION_1, colorbar_max_visual_estimate=11),
    PanelSpec("Decision_2", DECISION_2, colorbar_max_visual_estimate=4.5),
]

MUL_PANELS = [
    PanelSpec("BasalGanglia_GPi", ["R", "G", "B"], colorbar_max_visual_estimate=50),
    PanelSpec("BasalGanglia_GPe", ["R", "G", "B"], colorbar_max_visual_estimate=50),
    PanelSpec("BasalGanglia_STN", ["R", "G", "B"], colorbar_max_visual_estimate=50),
    PanelSpec("BasalGanglia_STR", ["R", "G", "B"], colorbar_max_visual_estimate=50),
    PanelSpec("Locomotion_1", LOCOMOTION_1, colorbar_max_visual_estimate=130),
    PanelSpec("Locomotion_2", LOCOMOTION_2, colorbar_max_visual_estimate=0.8),
    PanelSpec("Lidar", LIDAR, colorbar_max_visual_estimate=0.8),
    PanelSpec("Input", INPUT16, colorbar_max_visual_estimate=0.25),
    PanelSpec("Response", INPUT16, colorbar_max_visual_estimate=0.2),
    PanelSpec("Auxiliary", INPUT16, colorbar_max_visual_estimate=0.2),
    PanelSpec("Decision_1", DECISION_1, colorbar_max_visual_estimate=80),
    PanelSpec("Decision_2", DECISION_2, colorbar_max_visual_estimate=5),
]

if __name__ == "__main__":
    out_dir = "experiments/_plotting/vectorized"
    os.makedirs(out_dir, exist_ok=True)
    # NEU_EST_MUL.png needed row_span_tol=10 (vs. the shared default of 6): its "Input" panel's
    # left/right spine black-runs differ by 7px top-to-bottom (287-447 vs 283-440, antialiasing),
    # just outside the default tolerance -- caused the two spines to be grouped under different
    # row-span keys and the panel to go undetected (11/12 boxes found). This tol is passed ONLY
    # for this call, not changed as a new default: re-running extract_neu_est_real.py's own
    # UNIG_real/MUL_real extraction with tol=10 instead of 6 breaks THOSE images (produces 15
    # boxes instead of 8 for UNIG_real -- a higher tolerance over-merges distinct row-spans there)
    # -- confirmed by testing, not assumed. The two already-approved `_real` CSVs on disk are
    # untouched by this change (their own extract() calls keep the default tol=6).
    for src, out, specs, tick_step, tol in [
        ("assets/NEU_EST_UNIB.png", f"{out_dir}/neu_est_unib.csv", UNIB_PANELS, 10, 6),
        ("assets/NEU_EST_UNIG.png", f"{out_dir}/neu_est_unig.csv", UNIG_PANELS, 5, 6),
        ("assets/NEU_EST_MUL.png", f"{out_dir}/neu_est_mul.csv", MUL_PANELS, 20, 10),
    ]:
        df = extract(src, specs, tick_step=tick_step, row_span_tol=tol)
        df.to_csv(out, index=False)
        active_frac = df.groupby(["panel", "neuron"])["activation_normalized"].apply(
            lambda s: (s > 0.5).mean())
        print(src, "-> rows:", len(df))
        print(active_frac.to_string())
