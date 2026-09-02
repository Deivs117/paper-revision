"""Vectorizes assets/fig3_training_loss.png -> experiments/_plotting/vectorized/fig3_training_loss.csv

2026-09-02 (C-21 pixel-level audit follow-up): same situation as extract_fig2_roc_curve.py -- no
builder script anywhere in the repo, and the author confirmed no raw per-epoch training-loss log
survives to regenerate this from an actual training run. Vectorized directly from the published
PNG per the project's standard D-1/D-11 method.

Calibration:
  - Axes box: left spine col~132, bottom spine row~683.
  - x ticks (8, protruding below the bottom spine, rows 684-692): px
    [170,277,384,491,599,706,813,920] -> data [0,10,20,30,40,50,60,70] (Epoch).
  - y ticks (8, protruding left of the left spine, cols 124-131): px
    [138,212,286,360,434,508,582,656] -> data [0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0] (Training loss).
  - Curve color: matplotlib tab:blue (31,119,180) -- this figure has no legend to exclude (single
    unlabeled series), unlike fig2_roc_curve.png.
  - This figure has a visible light-gray grid (231,231,231) -- not color-matched (well outside the
    blue tolerance), no exclusion needed.
  - Per-column extraction = vertical CENTROID of matched pixels, same method as
    extract_graph_imu_sim.py / extract_fig2_roc_curve.py.
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
X_TICKS_PX = [170, 277, 384, 491, 599, 706, 813, 920]
X_TICKS_VAL = [0, 10, 20, 30, 40, 50, 60, 70]
Y_TICKS_PX = [138, 212, 286, 360, 434, 508, 582, 656]
Y_TICKS_VAL = [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]


def extract(image_path: str) -> pd.DataFrame:
    arr = np.array(Image.open(image_path).convert("RGB"))
    mask = color_mask(arr, BLUE, tol=30)
    x_coeffs = np.polyfit(X_TICKS_PX, X_TICKS_VAL, 1)
    y_coeffs = np.polyfit(Y_TICKS_PX, Y_TICKS_VAL, 1)

    rows = []
    cols_with_data = np.where(mask.any(axis=0))[0]
    for col in cols_with_data:
        row_idxs = np.where(mask[:, col])[0]
        centroid_row = float(row_idxs.mean())
        epoch = float(np.polyval(x_coeffs, col))
        loss = float(np.polyval(y_coeffs, centroid_row))
        rows.append({"epoch": round(epoch, 2), "loss": round(max(0.0, loss), 4)})

    df = pd.DataFrame(rows).drop_duplicates(subset="epoch").sort_values("epoch").reset_index(drop=True)
    return df


if __name__ == "__main__":
    df = extract("assets/fig3_training_loss.png")
    out = "experiments/_plotting/vectorized/fig3_training_loss.csv"
    df.to_csv(out, index=False)
    print(df.to_string())
    print(f"Epoch range: {df['epoch'].min():.1f}-{df['epoch'].max():.1f}, "
          f"loss range: {df['loss'].max():.3f} -> {df['loss'].min():.3f}")
    print(f"Wrote {out}")
