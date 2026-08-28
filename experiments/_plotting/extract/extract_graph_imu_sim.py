"""Vectorizes assets/GRAPH_IMU.png / GRAPH_IMU2.png (simulation) -> experiments/_plotting/
vectorized/graph_imu.csv / graph_imu2.csv

R02-01-05 §2 (F-04): both figures are single-axis line plots (matplotlib defaults: tab:blue
(31,119,180) "Standar dev accel z", tab:orange (255,127,14) "Pitch angle"), NOT the categorical
heatmap the already-closed physical F-05 fix turned out to be -- confirmed by direct visual
inspection, do not confuse the two (see vectorized/README.md's Group C note). No raw per-timestep
acceleration/pitch CSV exists in familia_c1_terreno_rugoso/familia_c2_pendiente (confirmed by
Informe 2 F-Data-04/05), so both full curves are vectorized by pixel color, per D-1/D-8 (full
series, not just cited peak events).

Axis calibration: gridlines are solid light gray (176,176,176), NOT dashed -- a higher color-match
tolerance than the dashed-gridline scripts elsewhere in this project. x: 6 ticks (0,20,40,60,80,100
s). y: 8 ticks (0,2,4,...,14, shared unit axis in the original, mixed m/s^2 and degrees -- see
imu_dual_axis.py for the double-axis fix applied on re-plotting).

Per column, the line's data value = the vertical CENTROID of that column's color-matched pixels
(not the topmost pixel, unlike a step/ECDF extractor) -- appropriate for a moderately-thin
(~2px) continuous line trace, confirmed by checking centroid vs. raw pixel spread on a handful of
columns (spread stayed within +-1 row, i.e. sub-0.05-unit noise at this scale).
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from color_extract import color_mask  # noqa: E402

BLUE = (31, 119, 180)
ORANGE = (255, 127, 14)


def _gridlines(arr: np.ndarray, plot_y0: int, plot_y1: int, plot_x0: int, plot_x1: int):
    is_gray = ((np.abs(arr[:, :, 0].astype(int) - 176) < 6)
               & (np.abs(arr[:, :, 1].astype(int) - 176) < 6)
               & (np.abs(arr[:, :, 2].astype(int) - 176) < 6))
    colfrac = is_gray[plot_y0:plot_y1, :].mean(axis=0)
    cols = np.where(colfrac > 0.3)[0]
    xg = [int(np.mean(g)) for g in np.split(cols, np.where(np.diff(cols) > 3)[0] + 1)]
    rowfrac = is_gray[:, plot_x0:plot_x1].mean(axis=1)
    rows = np.where(rowfrac > 0.3)[0]
    yg = [int(np.mean(g)) for g in np.split(rows, np.where(np.diff(rows) > 3)[0] + 1)]
    return xg, yg


def _spine_x_range(arr: np.ndarray) -> tuple[int, int]:
    """Left/right axes-box spine columns -- the plot area extends a bit past the last labeled
    gridline (matplotlib's default margin), so the color-extraction scan must use these, not the
    gridline extent, or it silently truncates any data past the last tick (caught here: GRAPH_IMU2's
    late-run pitch peak sits at x=856, beyond its last gridline at x=821)."""
    black = arr.max(axis=2) < 60
    cols = np.where(black.sum(axis=0) > 0.5 * arr.shape[0])[0]
    return int(cols.min()), int(cols.max())


def extract(image_path: str, x_ticks_val: list[float], y_ticks_val: list[float],
            legend_box: tuple[int, int, int, int]) -> pd.DataFrame:
    arr = np.array(Image.open(image_path).convert("RGB"))
    h, w, _ = arr.shape
    xg, yg = _gridlines(arr, plot_y0=int(h * 0.13), plot_y1=int(h * 0.9),
                        plot_x0=int(w * 0.13), plot_x1=int(w * 0.9))
    assert len(xg) == len(x_ticks_val), f"expected {len(x_ticks_val)} x-ticks, found {xg}"
    assert len(yg) == len(y_ticks_val), f"expected {len(y_ticks_val)} y-ticks, found {yg}"
    xcoef = np.polyfit(xg, x_ticks_val, 1)
    ycoef = np.polyfit(yg, y_ticks_val, 1)

    # Exclude the legend swatch: a TIGHT box around just the two short sample-line segments
    # (confirmed by inspection: ~29px wide, one row each, e.g. GRAPH_IMU2.png has them at
    # x=[705,740], y=[85,150]) -- NOT a broad top-right quadrant. GRAPH_IMU2's real pitch-angle
    # curve legitimately peaks near the top-right corner late in the run (~t=53, value ~38), so a
    # loose quadrant exclusion silently clips real data there; a box scoped to the legend's own
    # narrow x-span leaves that peak untouched.
    lx0, lx1, ly0, ly1 = legend_box

    rows = []
    for color, name in [(BLUE, "std_accel_z"), (ORANGE, "pitch_angle")]:
        mask = color_mask(arr, color, tol=30)
        mask[ly0:ly1, lx0:lx1] = False
        x0, x1 = _spine_x_range(arr)
        for col in range(x0, x1 + 1):
            colmask = mask[:, col]
            ys = np.where(colmask)[0]
            if len(ys) == 0:
                continue
            row_centroid = ys.mean()
            t = float(np.polyval(xcoef, col))
            val = float(np.polyval(ycoef, row_centroid))
            rows.append({"series": name, "time_s": round(t, 3), "value": round(val, 4)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    # Per-image tick values -- read directly off each figure's own labeled axes, NOT shared:
    # GRAPH_IMU.png spans ~98s (x: 0,20,..100) / 0..14 (y, step 2); GRAPH_IMU2.png spans ~53s
    # (x: 0,10,..50) / 0..35 (y, step 5) -- confirmed by visual inspection, do not assume these
    # match GRAPH_IMU.png's or the _real versions' ranges.
    configs = [
        ("assets/GRAPH_IMU.png", "experiments/_plotting/vectorized/graph_imu.csv",
         [0, 20, 40, 60, 80, 100], [14, 12, 10, 8, 6, 4, 2, 0], (705, 745, 85, 150)),
        ("assets/GRAPH_IMU2.png", "experiments/_plotting/vectorized/graph_imu2.csv",
         [0, 10, 20, 30, 40, 50], [35, 30, 25, 20, 15, 10, 5, 0], (705, 745, 85, 150)),
    ]
    for src, out, x_ticks, y_ticks, legend_box in configs:
        df = extract(src, x_ticks, y_ticks, legend_box)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        df.to_csv(out, index=False)
        print(src, "-> rows:", len(df))
        print(df.groupby("series")["value"].agg(["min", "max", "mean"]).to_string())
