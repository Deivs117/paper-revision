"""Vectorizes assets/fig6_computational_cost.png -> experiments/_plotting/vectorized/classifier_fig6.csv

Calibration (log-scale y-axis, each subplot calibrated independently -- their pixel-per-decade
spacing differs since matplotlib scales each subplot's ylim to fill the same pixel height):
  - Left panel (inference latency, us/sample): axes box cols 138.5-881.5, rows 74.5-668.5.
    Gridlines at row 277 (=10^1) and row 564 (=10^0).
  - Right panel (model size, parameters/tree nodes): axes box cols 1023.5-1766.5, same rows.
    Gridlines at row 243 (=10^4) and row 456 (=10^3).
  - Bar colors: tab:blue (31,119,180) left panel, tab:orange (255,127,14) right panel.
"""
from __future__ import annotations

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from color_extract import load_rgb, extract_bar_tops, pixel_to_value  # noqa: E402

CLASSIFIERS = ["Logistic Reg.", "SVM (RBF)", "Random Forest", "MLP (150-80)"]


def extract(image_path: str) -> pd.DataFrame:
    arr = load_rgb(image_path)
    rows = []

    # left panel -- inference latency (us/sample), log10 calibration: row277->1, row564->0
    left_bars = sorted(extract_bar_tops(arr, (31, 119, 180), y_baseline=668, x_gap=3, tol=25),
                        key=lambda b: b[0])
    assert len(left_bars) == 4, f"expected 4 latency bars, got {len(left_bars)}"
    for classifier, (x0, x1, top) in zip(CLASSIFIERS, left_bars):
        log_val = pixel_to_value(top, [564, 277], [0.0, 1.0])
        rows.append({"classifier": classifier, "metric": "inference_latency_us",
                     "value": round(10 ** log_val, 4)})

    # right panel -- model size (params/tree nodes), log10 calibration: row456->3, row243->4
    right_bars = sorted(extract_bar_tops(arr, (255, 127, 14), y_baseline=668, x_gap=3, tol=25),
                         key=lambda b: b[0])
    assert len(right_bars) == 4, f"expected 4 model-size bars, got {len(right_bars)}"
    for classifier, (x0, x1, top) in zip(CLASSIFIERS, right_bars):
        log_val = pixel_to_value(top, [456, 243], [3.0, 4.0])
        rows.append({"classifier": classifier, "metric": "model_size_params",
                     "value": round(10 ** log_val, 1)})

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = extract("assets/fig6_computational_cost.png")
    out = "experiments/_plotting/vectorized/classifier_fig6.csv"
    df.to_csv(out, index=False)
    print(df.pivot(index="classifier", columns="metric", values="value").to_string())
    print(f"Wrote {out}")
