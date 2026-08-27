"""Vectorizes assets/NEU_IMU_real.png / NEU_IMU2_real.png -> experiments/_plotting/vectorized/
neu_imu_real.csv / neu_imu2_real.csv.

Each image is 4 independent raster subplots (own axes box, own colorbar/grayscale scale):
  Locomotion 1 (11 neuron rows: X3..X13), Locomotion 2 (1 row: X17),
  Decision 1 (5 rows: X0..X4), Decision 2 (3 rows: X14..X16).

Panel boxes are auto-detected from vertical spine columns (NOT from horizontal spine rows alone --
an earlier attempt using only horizontal-row detection mis-identified panel boundaries because a
fully-active neuron's solid-black data band is indistinguishable from a spine by row alone; pairing
each spine ROW with a spine COLUMN of matching row-span disambiguates the two, see
find_panel_boxes()).

Grayscale intensity is reported NORMALIZED (0.0 white/inactive .. 1.0 black/max-activation) per
panel, not rescaled to each panel's own colorbar units -- results.tex's narrative about these
figures is about WHEN a neuron activates (timing), never about the raw activation magnitude, so the
normalized value is what matters for validating/regenerating the figure; the absolute colorbar
scale (e.g. "0..3" for Locomotion 1) was read visually and is noted in each panel's PanelSpec but
not required for the extraction itself.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from PIL import Image


@dataclass
class PanelSpec:
    name: str
    neuron_labels: list[str]
    colorbar_max_visual_estimate: float  # read by eye from the figure, informational only


PANEL_ORDER = [
    PanelSpec("Locomotion_1", [f"X{i}" for i in range(3, 14)], colorbar_max_visual_estimate=3.0),
    PanelSpec("Locomotion_2", ["X17"], colorbar_max_visual_estimate=1e-6),
    PanelSpec("Decision_1", [f"X{i}" for i in range(0, 5)], colorbar_max_visual_estimate=50.0),
    PanelSpec("Decision_2", ["X14", "X15", "X16"], colorbar_max_visual_estimate=5.0),
]


def _spine_columns(black: np.ndarray, min_run: int = 40) -> list[tuple[int, int, int]]:
    """Returns (col, row_start, row_end) for every vertical run of >=min_run consecutive black
    pixels in a single column -- these are panel spine columns (left/right edges)."""
    H, W = black.shape
    out = []
    for col in range(W):
        colmask = black[:, col]
        if colmask.sum() < min_run:
            continue
        idx = np.where(colmask)[0]
        groups = np.split(idx, np.where(np.diff(idx) > 2)[0] + 1)
        for g in groups:
            if len(g) >= min_run:
                out.append((col, int(g[0]), int(g[-1])))
    return out


def find_panel_boxes(arr: np.ndarray) -> list[tuple[int, int, int, int]]:
    """Returns [(left, right, top, bottom), ...] for the 4 panels, top-to-bottom, by pairing
    spine columns that share the same row-span (within a small tolerance)."""
    black = arr.max(axis=2) < 60
    cols = _spine_columns(black)
    # group by row-span (top,bottom) with tolerance, collect the columns present for each span
    spans: dict[tuple[int, int], list[int]] = {}
    for col, top, bottom in cols:
        matched = None
        for (t0, b0) in spans:
            if abs(t0 - top) <= 6 and abs(b0 - bottom) <= 6:
                matched = (t0, b0)
                break
        key = matched or (top, bottom)
        spans.setdefault(key, []).append(col)

    boxes = []
    for (top, bottom), col_list in spans.items():
        if bottom - top < 100:  # discard tiny/stray matches (data bands, not real panel height)
            continue
        col_list = sorted(col_list)
        # cluster columns by proximity -- the first two clusters are the main box's left/right
        # spine; any further cluster (e.g. a colorbar sharing this row-span) is discarded
        clusters = np.split(col_list, np.where(np.diff(col_list) > 15)[0] + 1)
        if len(clusters) < 2:
            continue
        left, right = int(clusters[0][0]), int(clusters[1][-1])
        if right - left < 200:  # a real panel is wide; anything narrower isn't the main box
            continue
        boxes.append((left, right, top, bottom))
    boxes.sort(key=lambda b: b[2])  # top-to-bottom
    return boxes


def find_x_ticks(arr: np.ndarray, left: int, right: int, bottom: int) -> tuple[list[int], list[int]]:
    strip = arr[bottom: bottom + 3, left:right + 1, :]
    black = strip.max(axis=2) < 60
    cols = np.where(black.sum(axis=0) >= 1)[0]
    groups = np.split(cols, np.where(np.diff(cols) > 3)[0] + 1) if len(cols) else []
    centers = [int(np.mean(g)) + left for g in groups]
    labels = [20 * i for i in range(len(centers))]
    return centers, labels


def extract(image_path: str) -> pd.DataFrame:
    arr = np.array(Image.open(image_path).convert("RGB"))
    boxes = find_panel_boxes(arr)
    assert len(boxes) == 4, f"expected 4 panels, found {len(boxes)}: {boxes}"

    rows = []
    for spec, (left, right, top, bottom) in zip(PANEL_ORDER, boxes):
        ticks, labels = find_x_ticks(arr, left, right, bottom)
        coeffs = np.polyfit(ticks, labels, 1)
        n = len(spec.neuron_labels)
        band_h = (bottom - top) / n
        for i, neuron in enumerate(spec.neuron_labels):
            y0 = int(top + i * band_h + band_h * 0.25)
            y1 = int(top + i * band_h + band_h * 0.75)
            band = arr[y0:y1, left:right + 1]
            gray = band.mean(axis=2)  # 0 (black) .. 255 (white)
            intensity = 1.0 - (gray.mean(axis=0) / 255.0)  # 0 white/inactive .. 1 black/active
            for col_offset, val in enumerate(intensity):
                t = np.polyval(coeffs, left + col_offset)
                rows.append({"panel": spec.name, "neuron": neuron, "time_s": round(float(t), 3),
                            "activation_normalized": round(float(val), 4)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    for src, out in [
        ("assets/NEU_IMU_real.png", "experiments/_plotting/vectorized/neu_imu_real.csv"),
        ("assets/NEU_IMU2_real.png", "experiments/_plotting/vectorized/neu_imu2_real.csv"),
    ]:
        df = extract(src)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        df.to_csv(out, index=False)
        active_frac = df.groupby(["panel", "neuron"])["activation_normalized"].apply(
            lambda s: (s > 0.5).mean())
        print(src, "-> rows:", len(df))
        print(active_frac.to_string())
