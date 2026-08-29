"""Vectorizes assets/fig5_classifier_comparison.png -> experiments/_plotting/vectorized/classifier_fig5.csv

Calibration (documented per Informe 2's trazabilidad-inversa rule):
  - Axes box found via near-black spine pixels: top spine row~74.5 (=value 1.0), bottom spine
    row~786.5 (=value 0.0), left spine col~132.5, right spine col~1469.5. ylim is exactly [0,1] so
    spine rows double as the calibration points (no separate gridline detection needed).
  - Legend box (color swatches for accuracy/precision/recall/f1, same tab10 colors as the bars)
    blanked out at arr[74:140, 133:850] before bar detection, to avoid the legend swatches being
    misread as a 5th "bar" per color.
  - Bar colors: matplotlib tab10 blue/orange/green/red, tol=25.
"""
from __future__ import annotations

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from color_extract import load_rgb, extract_bar_tops, pixel_to_value  # noqa: E402

COLORS = {"accuracy": (31, 119, 180), "precision": (255, 127, 14),
          "recall": (44, 160, 44), "f1": (214, 39, 40)}
CLASSIFIERS = ["Logistic Reg.", "SVM (RBF)", "Random Forest", "MLP (150-80)"]
Y0_PIXEL, Y1_PIXEL = 786.5, 74.5  # value 0.0, 1.0


def extract(image_path: str) -> pd.DataFrame:
    arr = load_rgb(image_path).copy()
    arr[74:140, 133:850] = 255  # blank legend box
    rows = []
    for metric, color in COLORS.items():
        bars = extract_bar_tops(arr, color, y_baseline=787, x_gap=3, tol=25)
        bars = sorted(bars, key=lambda b: b[0])
        assert len(bars) == 4, f"expected 4 bars for {metric}, got {len(bars)}"
        for classifier, (x0, x1, top) in zip(CLASSIFIERS, bars):
            value = pixel_to_value(top, [Y0_PIXEL, Y1_PIXEL], [0.0, 1.0])
            rows.append({"classifier": classifier, "metric": metric, "value": round(value, 4)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = extract("assets/fig5_classifier_comparison.png")
    out = "experiments/_plotting/vectorized/classifier_fig5.csv"
    df.to_csv(out, index=False)
    print(df.pivot(index="classifier", columns="metric", values="value").to_string())
    print(f"Wrote {out}")
