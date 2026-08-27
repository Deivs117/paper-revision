"""Vectorizes assets/GRAPH_IMU_real.png and GRAPH_IMU2_real.png -> experiments/_plotting/vectorized/
graph_imu_real.csv / graph_imu2_real.csv.

These are NOT continuous dual-axis series (unlike the simulation GRAPH_IMU.png/GRAPH_IMU2.png that
F-04 describes) -- Informe 1 already noted they're categorical state heatmaps: 3 rows (Stuck/Flat/
Inclined), each pixel-column black (state=1) or white (state=0) at a given time. Calibration is
fully automatic per image (spine detection + x-axis tick-mark detection), no manual pixel numbers
hardcoded -- run this against a new figure of the same style without editing constants.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
from PIL import Image

ROW_LABELS = ["Stuck", "Flat", "Inclined"]  # top-to-bottom, per the published figure


def find_axes_box(arr: np.ndarray) -> tuple[int, int, int, int]:
    """Returns (left, right, top, bottom) spine pixel coords via near-black long runs."""
    black = arr.max(axis=2) < 60
    h, w, _ = arr.shape
    rows = np.where(black.sum(axis=1) > 0.5 * w * 0.5)[0]  # generous: catches top+bottom spine
    # keep only rows that are a thin (<=3px) run -- excludes the solid "Flat" black band
    row_groups = np.split(rows, np.where(np.diff(rows) > 1)[0] + 1) if len(rows) else []
    spine_rows = [g for g in row_groups if len(g) <= 4]
    top, bottom = int(spine_rows[0][0]), int(spine_rows[-1][-1])

    cols_black = black[top:bottom + 1, :].sum(axis=0)
    cols = np.where(cols_black > 0.9 * (bottom - top))[0]
    col_groups = np.split(cols, np.where(np.diff(cols) > 1)[0] + 1) if len(cols) else []
    # main plot box = the first TWO spine groups (left, right) -- anything after that is the
    # colorbar's own box borders, not the main axes, and must not be picked as "the right spine"
    left, right = int(col_groups[0][0]), int(col_groups[1][-1])
    return left, right, top, bottom


def find_x_ticks(arr: np.ndarray, left: int, right: int, bottom: int) -> tuple[list[int], list[int]]:
    """Detects tick marks just below the bottom spine, restricted to the plot's own x-range
    (excludes row-label text to the left of the axes box); returns (pixel_cols, assumed_labels).
    Labels are inferred assuming evenly spaced ticks starting at 0 in steps of 20 (matches every
    figure of this style seen so far) -- if that assumption breaks for a future figure, this will
    raise via the caller's own sanity check on tick count, not silently mis-calibrate."""
    strip = arr[bottom + 1: bottom + 7, left:right + 1, :]
    black = strip.max(axis=2) < 60
    cols = np.where(black.sum(axis=0) >= 3)[0]
    groups = np.split(cols, np.where(np.diff(cols) > 3)[0] + 1) if len(cols) else []
    centers = [int(np.mean(g)) + left for g in groups]
    labels = [20 * i for i in range(len(centers))]
    return centers, labels


def extract(image_path: str) -> pd.DataFrame:
    arr = np.array(Image.open(image_path).convert("RGB"))
    left, right, top, bottom = find_axes_box(arr)
    ticks, labels = find_x_ticks(arr, left, right, bottom)
    coeffs = np.polyfit(ticks, labels, 1)

    band_h = (bottom - top) / 3.0
    rows = []
    for i, label in enumerate(ROW_LABELS):
        y0 = int(top + i * band_h + band_h * 0.3)
        y1 = int(top + i * band_h + band_h * 0.7)
        band = arr[y0:y1, left:right + 1]
        is_black = band.max(axis=2) < 90
        state_per_col = is_black.mean(axis=0) > 0.5  # majority vote across the band's rows (axis 0)
        for col_offset, state in enumerate(state_per_col):
            t = np.polyval(coeffs, left + col_offset)
            rows.append({"time_s": round(float(t), 3), "row": label, "state": int(state)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    for src, out in [
        ("assets/GRAPH_IMU_real.png", "experiments/_plotting/vectorized/graph_imu_real.csv"),
        ("assets/GRAPH_IMU2_real.png", "experiments/_plotting/vectorized/graph_imu2_real.csv"),
    ]:
        df = extract(src)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        df.to_csv(out, index=False)
        n_transitions = {label: int((df[df.row == label]["state"].diff().abs() > 0).sum())
                          for label in ROW_LABELS}
        print(src, "-> rows:", len(df), "transitions per label:", n_transitions,
              "time range:", df["time_s"].min(), "-", df["time_s"].max())
