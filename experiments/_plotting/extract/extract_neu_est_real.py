"""Vectorizes assets/NEU_EST_UNIG_real.png / NEU_EST_MUL_real.png -> experiments/_plotting/
vectorized/neu_est_unig_real.csv / neu_est_mul_real.csv.

Decision 2026-08-27 (author, after reviewing n02_audit_notes): the earlier CSV-based "aggregate
substitute" for these two figures was rejected ("no representan lo mismo... no rehacer") -- instead,
apply the SAME pixel-intensity vectorization technique that worked for NEU_IMU_real/NEU_IMU2_real
(the per-neuron raster data is directly readable from the published PNG, no separate raw log needed).

These two figures are structurally bigger than NEU_IMU_real (multi-column layout, 8 and 12 panels
respectively, vs. NEU_IMU_real's single column of 4) -- this required generalizing
`extract_neu_imu_real.find_panel_boxes()` to handle multiple side-by-side columns whose rows can
coincidentally align (see that function's docstring for the colorbar-vs-spine disambiguation this
needed). Reuses that generalized function + `find_x_ticks` directly, only the per-image panel
label specs are new.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_neu_imu_real import PanelSpec, find_panel_boxes, find_x_ticks  # noqa: E402

# Panel order matches find_panel_boxes()'s column-first, top-to-bottom output -- verified by
# printing the detected boxes and comparing against a visual read of each figure (see this
# script's own smoke test at the bottom).
UNIG_PANELS = [
    PanelSpec("Lidar", [f"L{i}" for i in range(5)], colorbar_max_visual_estimate=0.5),
    PanelSpec("Input", [str(i) for i in range(1, 17)], colorbar_max_visual_estimate=0.25),
    PanelSpec("Response", [str(i) for i in range(1, 17)], colorbar_max_visual_estimate=0.2),
    PanelSpec("Auxiliary", [str(i) for i in range(1, 17)], colorbar_max_visual_estimate=0.2),
    PanelSpec("Locomotion_1", [f"X{i}" for i in range(3, 14)], colorbar_max_visual_estimate=85),
    PanelSpec("Locomotion_2", ["X17"], colorbar_max_visual_estimate=1e-6),
    PanelSpec("Decision_1", [f"X{i}" for i in range(0, 5)], colorbar_max_visual_estimate=35),
    PanelSpec("Decision_2", ["X14", "X15", "X16"], colorbar_max_visual_estimate=5),
]

MUL_PANELS = [
    PanelSpec("BasalGanglia_GPi", ["R", "G", "B"], colorbar_max_visual_estimate=120),
    PanelSpec("BasalGanglia_GPe", ["R", "G", "B"], colorbar_max_visual_estimate=120),
    PanelSpec("BasalGanglia_STN", ["R", "G", "B"], colorbar_max_visual_estimate=120),
    PanelSpec("BasalGanglia_STR", ["R", "G", "B"], colorbar_max_visual_estimate=120),
    PanelSpec("Locomotion_1", [f"X{i}" for i in range(3, 14)], colorbar_max_visual_estimate=280),
    PanelSpec("Locomotion_2", ["X17"], colorbar_max_visual_estimate=1.2),
    PanelSpec("Lidar", [f"L{i}" for i in range(5)], colorbar_max_visual_estimate=0.6),
    PanelSpec("Input", [str(i) for i in range(1, 17)], colorbar_max_visual_estimate=0.25),
    PanelSpec("Response", [str(i) for i in range(1, 17)], colorbar_max_visual_estimate=0.2),
    PanelSpec("Auxiliary", [str(i) for i in range(1, 17)], colorbar_max_visual_estimate=0.2),
    PanelSpec("Decision_1", [f"X{i}" for i in range(0, 5)], colorbar_max_visual_estimate=230),
    PanelSpec("Decision_2", ["X14", "X15", "X16"], colorbar_max_visual_estimate=5),
]


def _reliable_px_per_unit(arr: np.ndarray, boxes: list[tuple[int, int, int, int]],
                           tick_step: int) -> float:
    """Every panel in these two figures shares the same time-axis range (verified visually), so
    one clean tick detection anchors all of them -- more robust than trusting per-panel detection
    on every column, some of which (the Lidar/Input/Response/Auxiliary column specifically) sit
    right next to a near-full-width data band that corrupts naive tick-row scanning even after
    filtering sparse rows. Uses the first box whose tick detection returns a clean, evenly-spaced
    result. `tick_step` must match the axis's actual labeled tick spacing -- read directly off the
    published figure, NOT assumed: NEU_EST_UNIG_real.png labels every 10s (0,10,...60), while
    NEU_EST_MUL_real.png and every GRAPH_IMU*/NEU_IMU* figure processed so far labels every 20s.
    `find_x_ticks()` itself only detects tick POSITIONS, not their step -- getting this constant
    wrong silently doubles/halves every extracted timestamp (caught once already: an earlier pass
    of this script used a hardcoded 20s step for NEU_EST_UNIG_real.png and produced a time axis
    running to ~130s against a published range of ~65s, exactly the 2x error re-using MUL's step
    would produce)."""
    for left, right, top, bottom in boxes:
        ticks, labels = find_x_ticks(arr, left, right, bottom)
        if len(ticks) >= 4:
            diffs = np.diff(ticks)
            if np.std(diffs) < 5:  # evenly spaced -> trustworthy
                return float(np.mean(diffs)) / tick_step
    raise RuntimeError("no panel produced a reliable tick calibration")


def extract(image_path: str, panel_specs: list[PanelSpec], tick_step: int = 20,
            row_span_tol: int = 6) -> pd.DataFrame:
    arr = np.array(Image.open(image_path).convert("RGB"))
    boxes = find_panel_boxes(arr, row_span_tol=row_span_tol)
    assert len(boxes) == len(panel_specs), (
        f"expected {len(panel_specs)} panels, found {len(boxes)}: {boxes}")
    px_per_unit = _reliable_px_per_unit(arr, boxes, tick_step)

    rows = []
    for spec, (left, right, top, bottom) in zip(panel_specs, boxes):
        # time = (pixel - left_spine) / px_per_unit, anchored at this panel's own left spine
        # (all panels start at t=0) using the ONE globally-reliable px-per-unit ratio above,
        # instead of re-detecting ticks per panel.
        coeffs = (1.0 / px_per_unit, -left / px_per_unit)
        n = len(spec.neuron_labels)
        band_h = (bottom - top) / n
        for i, neuron in enumerate(spec.neuron_labels):
            y0 = int(top + i * band_h + band_h * 0.25)
            y1 = int(top + i * band_h + band_h * 0.75)
            band = arr[y0:y1, left:right + 1]
            gray = band.mean(axis=2)
            intensity = 1.0 - (gray.mean(axis=0) / 255.0)
            for col_offset, val in enumerate(intensity):
                t = np.polyval(coeffs, left + col_offset)
                rows.append({"panel": spec.name, "neuron": neuron, "time_s": round(float(t), 3),
                            "activation_normalized": round(float(val), 4)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    for src, out, specs, tick_step in [
        # tick_step read directly off each published figure's x-axis (see _reliable_px_per_unit
        # docstring) -- UNIG labels every 10s, MUL every 20s. Do not assume these match.
        ("assets/NEU_EST_UNIG_real.png", "experiments/_plotting/vectorized/neu_est_unig_real.csv", UNIG_PANELS, 10),
        ("assets/NEU_EST_MUL_real.png", "experiments/_plotting/vectorized/neu_est_mul_real.csv", MUL_PANELS, 20),
    ]:
        df = extract(src, specs, tick_step=tick_step)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        df.to_csv(out, index=False)
        active_frac = df.groupby(["panel", "neuron"])["activation_normalized"].apply(
            lambda s: (s > 0.5).mean())
        print(src, "-> rows:", len(df))
        print(active_frac.to_string())
