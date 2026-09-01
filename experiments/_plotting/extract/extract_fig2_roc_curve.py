"""Vectorizes assets/fig2_roc_curve.png -> experiments/_plotting/vectorized/fig2_roc_curve.csv

2026-09-02 (C-21 pixel-level audit follow-up): this figure has no builder script anywhere in the
repo (confirmed by exhaustive search of experiments/**/*.py) and the author confirmed no raw
prediction-probabilities CSV survives to regenerate it from the actual model -- same situation as
the other "no raw data" entries in vectorized/README.md. Vectorized directly from the published
PNG instead, per the same D-1/D-11 method used there.

Calibration:
  - Axes box found via near-black spine pixels: left spine col~132, bottom spine row~783.
  - x ticks (6, protruding below the bottom spine, rows 784-792): px [165,299,433,567,701,835] ->
    data [0.0,0.2,0.4,0.6,0.8,1.0] (False Positive Rate).
  - y ticks (6, protruding left of the left spine, cols 124-131): px [106,235,364,492,621,750] ->
    data [1.0,0.8,0.6,0.4,0.2,0.0] (True Positive Rate).
  - Curve color: matplotlib tab:blue (31,119,180), the only blue in the image besides its own
    legend swatch.
  - Legend swatch exclusion: a small blue line sample at x=[500,558], y=[699,702] (the "MLP
    (AUC = 0.866)" legend entry) -- confirmed isolated from the real curve (narrow ~4px band, far
    from the curve's own trend at that x-range) before blanking it out. The "Chance" diagonal
    (black dashed, y=x) is NOT vectorized -- it's a fixed analytical reference line, trivially
    redrawn in the rebuild without any pixel-reading.
  - Per-column extraction = vertical CENTROID of matched pixels (thin ~2-3px line), same method as
    extract_graph_imu_sim.py. The curve is a step function (empirical ROC), so a jump column's
    centroid sits between its two plateau values -- acceptable for a shape-faithful redraw (this
    is a republished figure's visual content, not a re-derivation of the classifier's exact
    predictions), consistent with the precision caveat already accepted project-wide for
    pixel-vectorized figures (see vectorized/README.md).
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
X_TICKS_PX = [165, 299, 433, 567, 701, 835]
X_TICKS_VAL = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
Y_TICKS_PX = [106, 235, 364, 492, 621, 750]
Y_TICKS_VAL = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]
LEGEND_BOX = (490, 570, 690, 715)  # x0, x1, y0, y1 -- blanked before extraction


def extract(image_path: str) -> pd.DataFrame:
    arr = np.array(Image.open(image_path).convert("RGB")).copy()
    x0, x1, y0, y1 = LEGEND_BOX
    arr[y0:y1, x0:x1] = 255  # blank the legend swatch so it can't leak into the curve

    mask = color_mask(arr, BLUE, tol=30)
    x_coeffs = np.polyfit(X_TICKS_PX, X_TICKS_VAL, 1)
    y_coeffs = np.polyfit(Y_TICKS_PX, Y_TICKS_VAL, 1)

    rows = []
    cols_with_data = np.where(mask.any(axis=0))[0]
    for col in cols_with_data:
        row_idxs = np.where(mask[:, col])[0]
        centroid_row = float(row_idxs.mean())
        fpr = float(np.polyval(x_coeffs, col))
        tpr = float(np.polyval(y_coeffs, centroid_row))
        rows.append({"fpr": round(max(0.0, min(1.0, fpr)), 4),
                     "tpr": round(max(0.0, min(1.0, tpr)), 4)})

    df = pd.DataFrame(rows).drop_duplicates(subset="fpr").sort_values("fpr").reset_index(drop=True)
    return df


if __name__ == "__main__":
    df = extract("assets/fig2_roc_curve.png")
    out = "experiments/_plotting/vectorized/fig2_roc_curve.csv"
    df.to_csv(out, index=False)
    # trapezoidal AUC from the extracted points, cross-check against the published "AUC = 0.866"
    auc = float(np.trapezoid(df["tpr"], df["fpr"]))
    print(df.to_string())
    print(f"Extracted AUC (trapezoidal) = {auc:.3f} -- published figure says AUC = 0.866")
    print(f"Wrote {out}")
