"""Vectorizes assets/FigReal_Terrain_Latencies_4Panels.png -> experiments/_plotting/vectorized/terrain_latencies.csv

4-panel step-ECDF, N=15 "Hardware Replicates" per panel (steps of 1/15 visible on every y-axis).
Because it's a step function with exactly 15 known y-levels, extraction doesn't need y-axis
calibration at all -- only x-axis (time-delay / settling-time) calibration, done per panel from its
own dashed vertical gridlines (values read directly off the published axis tick labels, the only
manual input this script takes -- everything else is pixel detection).

Panel layout (quadrants of the 3269x2520 source image):
  A (top-left,  blue   #1f77b4): T_response, Quadrupedal->Differential Mobile,  x ticks 0.183..0.190 step 0.001
  B (top-right, orange #ff7f0e): T_response, Differential Mobile->Quadrupedal,  x ticks 0.5342..0.5354 step 0.0002
  C (bot-left,  teal   #2ca089): T_switch,   Quadrupedal->Differential Mobile,  x ticks 2.7..3.1 step 0.1
  D (bot-right, orange-red #d2691e): T_switch, Differential Mobile->Quadrupedal, x ticks 1.4..1.8 step 0.1
Colors sampled directly from the line pixels (see `LINE_COLORS`), not assumed from a generic palette.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from color_extract import color_mask  # noqa: E402

IMG = "assets/FigReal_Terrain_Latencies_4Panels.png"

PANELS = {
    # name: (x0,x1,y0,y1 quadrant crop, tick_values list, line_color RGB)
    "A_Tresponse_Quad2Diff": dict(quad=(0, 1634, 0, 1260), ticks=np.arange(0.183, 0.1901, 0.001),
                                   color=(31, 119, 180)),
    "B_Tresponse_Diff2Quad": dict(quad=(1634, 3269, 0, 1260), ticks=np.arange(0.5342, 0.53551, 0.0002),
                                   color=(255, 127, 14)),
    "C_Tswitch_Quad2Diff": dict(quad=(0, 1634, 1260, 2520), ticks=np.arange(2.7, 3.101, 0.1),
                                 color=(44, 160, 137)),
    "D_Tswitch_Diff2Quad": dict(quad=(1634, 3269, 1260, 2520), ticks=np.arange(1.4, 1.801, 0.1),
                                 color=(210, 105, 30)),
}
N_REPLICATES = 15


def find_left_spine_and_gridlines(gray_arr: np.ndarray) -> tuple[int, list[int]]:
    """Within one panel's cropped RGB array, find the left spine col and the vertical dashed
    gridline columns (light-gray, low duty cycle since dashed)."""
    h, w, _ = gray_arr.shape
    black = gray_arr.max(axis=2) < 60
    col_black = black.sum(axis=0)
    spine_cols = np.where(col_black > 0.5 * h)[0]
    left_spine = int(spine_cols.min())

    is_gray = ((np.abs(gray_arr[:, :, 0].astype(int) - gray_arr[:, :, 1].astype(int)) < 10)
               & (np.abs(gray_arr[:, :, 1].astype(int) - gray_arr[:, :, 2].astype(int)) < 10)
               & (gray_arr[:, :, 0] > 180) & (gray_arr[:, :, 0] < 245))
    colfrac = is_gray[: int(h * 0.95), :].mean(axis=0)  # exclude bottom tick-label area
    cols = np.where(colfrac > 0.12)[0]
    groups = np.split(cols, np.where(np.diff(cols) > 4)[0] + 1) if len(cols) else []
    centers = [int(np.mean(g)) for g in groups if abs(np.mean(g) - left_spine) > 10]
    return left_spine, sorted(centers)


def extract_panel(arr: np.ndarray, spec: dict) -> np.ndarray:
    x0, x1, y0, y1 = spec["quad"]
    crop = arr[y0:y1, x0:x1]
    left_spine, gridlines = find_left_spine_and_gridlines(crop)
    ticks = spec["ticks"]
    assert len(gridlines) == len(ticks), (
        f"expected {len(ticks)} gridlines, found {len(gridlines)}: {gridlines}")
    coeffs = np.polyfit(gridlines, ticks, 1)

    mask = color_mask(crop, spec["color"], tol=40)
    # for each column, find the line's row (the step is drawn thick; take the topmost matching
    # pixel per column as "just above the step", consistent across the whole panel)
    step_x = []
    prev_row = None
    for col in range(crop.shape[1]):
        rows = np.where(mask[:, col])[0]
        if len(rows) == 0:
            continue
        row = int(rows.min())
        if prev_row is not None and row != prev_row:
            step_x.append(col)
        prev_row = row
    # collapse near-duplicate detections (anti-aliased edges spanning a couple columns)
    step_x = sorted(step_x)
    collapsed = []
    for c in step_x:
        if not collapsed or c - collapsed[-1] > 10:
            collapsed.append(c)
    values = np.polyval(coeffs, collapsed)
    return values


def main():
    arr = np.array(Image.open(IMG).convert("RGB"))
    rows = []
    for name, spec in PANELS.items():
        vals = extract_panel(arr, spec)
        print(name, "n_steps_found=", len(vals), np.round(vals, 5))
        for v in vals:
            rows.append({"panel": name, "value": float(v)})
    df = pd.DataFrame(rows)
    out = "experiments/_plotting/vectorized/terrain_latencies.csv"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    df.to_csv(out, index=False)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
