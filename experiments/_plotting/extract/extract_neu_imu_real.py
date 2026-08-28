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


def find_panel_boxes(arr: np.ndarray, row_span_tol: int = 6) -> list[tuple[int, int, int, int]]:
    """Returns [(left, right, top, bottom), ...] for every panel in the image, ordered
    column-first then top-to-bottom within each column, by pairing spine columns that share the
    same row-span (within a small tolerance).

    IMPORTANT: multiple panels can share the same row-span (e.g. two side-by-side columns of
    panels whose rows happen to align, as in NEU_EST_MUL_real.png's Basal-Ganglia/Lidar columns).
    A naive "take the first two spine-column clusters" approach silently merges the LEFT panel's
    spine with the wrong RIGHT panel's spine in that case -- so each row-span's column list is
    split into ALL of its x-clusters (not just the first two), and consecutive clusters are paired
    up (0&1, 2&3, ...) as separate boxes' left/right spines, assuming clusters alternate
    left-spine/right-spine/left-spine/right-spine in x order (verified true for every figure in
    this project so far -- re-check this assumption if a future figure returns an odd box count).
    """
    black = arr.max(axis=2) < 60
    cols = _spine_columns(black)
    # group by row-span (top,bottom) with tolerance, collect the columns present for each span
    spans: dict[tuple[int, int], list[int]] = {}
    for col, top, bottom in cols:
        matched = None
        for (t0, b0) in spans:
            if abs(t0 - top) <= row_span_tol and abs(b0 - bottom) <= row_span_tol:
                matched = (t0, b0)
                break
        key = matched or (top, bottom)
        spans.setdefault(key, []).append(col)

    boxes = []
    for (top, bottom), col_list in spans.items():
        if bottom - top < 100:  # discard tiny/stray matches (data bands, not real panel height)
            continue
        col_list = sorted(set(col_list))
        raw_clusters = np.split(col_list, np.where(np.diff(col_list) > 15)[0] + 1)
        # A colorbar's own left+right border forms a tight "doublet" cluster (both edges within
        # 15px of each other) -- discard those before pairing, they are never a real panel spine
        # on their own. Distinguish by DENSITY, not raw width: a real spine (even a somewhat thick
        # one, e.g. 6px of solid anti-aliased line) has every pixel column present across its
        # span; a colorbar doublet is two thin edges with a gap between them (e.g. columns 860 and
        # 867 only, nothing in between) -- sparse relative to its span. A flat width cutoff
        # mis-classified a genuine 6px-wide spine as noise on NEU_EST_MUL_real.png; density does not.
        def _is_dense(c):
            span = int(c[-1] - c[0]) + 1
            return len(c) >= 0.5 * span
        clusters = [c for c in raw_clusters if _is_dense(c)]
        # Greedy nearest-distant-partner pairing, not naive even/odd pairing: a colorbar right
        # next to a panel (its own thin left+right border, both within 15px of each other) forms
        # its own cluster that must be skipped entirely, not paired with the real spine two slots
        # away -- naive (0,1),(2,3),... pairing mismatches a spine with a colorbar edge whenever
        # an odd number of noise clusters sits between two real panels (as in
        # NEU_EST_MUL_real.png's Basal-Ganglia-column colorbars). Instead: walk left to right,
        # and for each candidate left spine, take the FIRST later cluster at least a real panel's
        # width away (>=200px) as its right spine, skipping anything closer as noise.
        i = 0
        while i < len(clusters):
            left = int(clusters[i][0])
            j = i + 1
            right = None
            while j < len(clusters):
                if int(clusters[j][-1]) - left >= 200:
                    right = int(clusters[j][-1])
                    break
                j += 1
            if right is not None:
                boxes.append((left, right, top, bottom))
                i = j + 1
            else:
                i += 1  # no distant partner found -- this cluster is noise, skip it
    # column-first, then top-to-bottom within a column: cluster boxes by left-edge proximity
    boxes.sort(key=lambda b: b[0])
    col_groups = []
    for b in boxes:
        placed = False
        for g in col_groups:
            if abs(g[0][0] - b[0]) < 100:
                g.append(b)
                placed = True
                break
        if not placed:
            col_groups.append([b])
    ordered = []
    for g in col_groups:
        ordered.extend(sorted(g, key=lambda b: b[2]))
    return ordered


def find_x_ticks(arr: np.ndarray, left: int, right: int, bottom: int) -> tuple[list[int], list[int]]:
    """Detects tick marks below the axes box, restricted to the plot's own x-range.

    Scans a slightly taller window (bottom..bottom+9) than a single tick mark needs, then keeps
    only the SPARSE rows (a handful of black columns, not the whole width) -- a thick spine line
    (occasionally 2-3px, sometimes bleeding into a solid data band right at the axis edge, as seen
    on NEU_EST_MUL_real.png's right-column panels) is a nearly-full-width black row and must be
    excluded, or it swallows the real (sparse) tick-mark columns into one giant bogus cluster.
    """
    width = right - left + 1
    row_start, row_end = bottom, bottom + 7
    strip = arr[row_start:row_end, left:right + 1, :]
    black_full = strip.max(axis=2) < 60
    row_black_frac = black_full.mean(axis=1)
    sparse_rows = row_black_frac < 0.3  # excludes spine/data rows, keeps tick-mark rows
    black = black_full[sparse_rows, :]
    cols = np.where(black.sum(axis=0) >= 1)[0] if black.size else np.array([], dtype=int)
    # drop columns coinciding with the box's own left/right spine (col 0 or width-1 in this
    # crop's local coordinates) -- a spine pixel can survive into a "sparse" row and gets
    # mistaken for a tick mark otherwise, which is off by one position in the evenly-spaced label
    # assignment below.
    cols = cols[(cols > 1) & (cols < width - 2)]
    groups = np.split(cols, np.where(np.diff(cols) > 3)[0] + 1) if len(cols) else []
    centers = [int(np.mean(g)) + left for g in groups]
    # Keep only the longest run of evenly-spaced centers -- stray columns (anti-aliased data
    # pixels landing in a "sparse enough" row, digit strokes from the tick-label text below)
    # produce spurious extra centers close to a real tick; a flat 20-per-index label assignment
    # over the RAW center list then assigns wrong labels to everything after the first stray one.
    # Greedily grow the longest chain whose consecutive gaps agree within 20% of the chain's
    # running median gap.
    best_chain = centers[:1]
    if len(centers) > 1:
        chains = []
        chain = [centers[0]]
        for c in centers[1:]:
            gap = c - chain[-1]
            ref = np.median(np.diff(chain)) if len(chain) > 1 else gap
            if ref > 0 and abs(gap - ref) / ref < 0.2:
                chain.append(c)
            else:
                chains.append(chain)
                chain = [c]
        chains.append(chain)
        best_chain = max(chains, key=len)
    centers = best_chain
    labels = [20 * i for i in range(len(centers))]
    return centers, labels


def _reliable_px_per_unit(arr: np.ndarray, boxes: list[tuple[int, int, int, int]],
                           tick_step: int = 20) -> float:
    """Same rationale as extract_neu_est_real.py's version: anchor every panel's calibration on
    ONE panel's clean tick spacing (px-per-unit ratio) rather than trusting each panel's own
    origin, which the "longest evenly-spaced chain" filter in find_x_ticks can start at a
    non-zero label when the true label-0 tick got excluded as noise -- a constant-offset error
    that a spacing-only ratio, applied from each panel's own left spine as t=0, cannot have."""
    for left, right, top, bottom in boxes:
        ticks, _ = find_x_ticks(arr, left, right, bottom)
        if len(ticks) >= 2:
            diffs = np.diff(ticks)
            if len(diffs) == 0 or np.std(diffs) < 5:
                return float(np.mean(diffs)) / tick_step if len(diffs) else None
    raise RuntimeError("no panel produced a reliable tick calibration")


def extract(image_path: str) -> pd.DataFrame:
    arr = np.array(Image.open(image_path).convert("RGB"))
    boxes = find_panel_boxes(arr)
    assert len(boxes) == 4, f"expected 4 panels, found {len(boxes)}: {boxes}"
    px_per_unit = _reliable_px_per_unit(arr, boxes)

    rows = []
    for spec, (left, right, top, bottom) in zip(PANEL_ORDER, boxes):
        coeffs = (1.0 / px_per_unit, -left / px_per_unit)
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
