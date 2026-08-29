"""Vectorizes panel C ("Decision Latency Profile") of assets/fig1_Obstacle_macro.png ->
experiments/_plotting/vectorized/fig1_obstacle_latency.csv

R02-01-04 §3/§5 step 1: `experiments/simulation/familia_a_obstaculo` has 0/15 populated latency
values in either `trial_summary.json.exp_latency` or `metrics_raw.csv.latency_s` (verified
directly, corrects Informe 2's original F-Data-01 diagnosis) -- the published figure's panel C
cannot be reproduced from any CSV currently in the repo, so it is vectorized from the PNG per D-1.

Panel C is a `errorbar(x, y, yerr=sd, marker='o', ...)` plot, 5 points (sigma = 0..4), same visual
family as the other two panels in this figure and as the other 3 `fig1_*_macro.png` figures.
Extraction strategy (pixel color, no WebPlotDigitizer needed -- same refinement as Groups B/D, see
`experiments/_plotting/vectorized/README.md`):

1. Crop the right third of the 4234x1234 source image (panel C occupies columns ~2823-4234).
2. Locate the panel's left axis spine and bottom axis spine as the tallest/widest runs of
   near-black pixels within the crop -- found at column 170 and row 1072 (crop-relative).
3. Locate x-axis gridline centers (light-gray dashed vertical lines, RGB ~(223,223,223)) within
   the plot area -- 5 evenly-spaced columns at crop-relative x = [101, 354, 607, 859, 1112],
   corresponding to sigma = [0, 1, 2, 3, 4] (confirmed evenly spaced, ~253px/step).
4. Locate y-axis gridline centers the same way -- 7 evenly-spaced rows at crop-relative
   y = [157, 289, 421, 554, 686, 818, 951], corresponding to the published tick labels
   [2000, 1800, 1600, 1400, 1200, 1000, 800] ms (linear fit, ~132px/200ms).
5. For each sigma's x column (+-8px band, wide enough to catch the marker/line/caps, narrow
   enough to stay clear of neighbouring points at this point spacing), mask pixels close to the
   panel's teal-green line color (0, 158, 115) -- Okabe-Ito "bluish green", confirmed by direct
   pixel sampling, not assumed from a generic palette.
6. `errorbar`'s symmetric-yerr convention means the top and bottom extent of the green mask in
   that column band are the +-SD caps, and the marker (mean) sits exactly at their midpoint --
   confirmed against macro_robustness.py's own `ax.errorbar(x, y, yerr=sd, ...)` call, which uses
   the same symmetric convention for the other 3 (real-data) scenarios in the same figure family.
   (An earlier attempt at finding the mean via "widest row in the column" locked onto the error
   bar's horizontal cap instead of the marker -- caps are wider than the circular marker in this
   figure's style -- hence the switch to the midpoint-of-extent approach.)

Validation: resulting means (1091/1211/1316/1518/992 ms for sigma=0..4) visually match a plain
read of the published PNG at each point (approximate values ~1100/1210/1320/1520/1030 ms) to
within a few percent -- consistent with the precision loss expected from pixel extraction on an
errorbar plot, not a mis-calibration.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from color_extract import color_mask  # noqa: E402

IMG = "assets/fig1_Obstacle_macro.png"
OUT_CSV = "experiments/_plotting/vectorized/fig1_obstacle_latency.csv"

# Panel C crop: right third of the full figure.
PANEL_X0_FRAC = 2 / 3
LEFT_SPINE = 170
BOTTOM_SPINE = 1072

X_TICK_PX = [101, 354, 607, 859, 1112]
SIGMAS = [0, 1, 2, 3, 4]

Y_TICK_PX = [157, 289, 421, 554, 686, 818, 951]
Y_TICK_VAL = [2000, 1800, 1600, 1400, 1200, 1000, 800]

LINE_COLOR = (0, 158, 115)
BAND_HALF_WIDTH = 8


def main():
    img = Image.open(IMG).convert("RGB")
    arr = np.array(img)
    h, w, _ = arr.shape
    x0 = int(w * PANEL_X0_FRAC)
    crop = arr[:, x0:]
    plot = crop[:BOTTOM_SPINE, LEFT_SPINE:]

    mask = color_mask(plot, LINE_COLOR, tol=60)
    coeffs = np.polyfit(Y_TICK_PX, Y_TICK_VAL, 1)
    y2v = lambda y: float(np.polyval(coeffs, y))  # noqa: E731

    rows = []
    for xt, sigma in zip(X_TICK_PX, SIGMAS):
        band = mask[:, max(0, xt - BAND_HALF_WIDTH):xt + BAND_HALF_WIDTH + 1]
        ys = np.where(band.any(axis=1))[0]
        assert len(ys) > 0, f"no line-color pixels found for sigma={sigma}"
        top, bottom = int(ys.min()), int(ys.max())
        mean_v = y2v((top + bottom) / 2)
        sd_v = (y2v(top) - y2v(bottom)) / 2
        rows.append({"noise_level_idx": sigma, "latency_ms_mean": round(mean_v, 1),
                     "latency_ms_sd": round(sd_v, 1)})

    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    df.to_csv(OUT_CSV, index=False)
    print(f"Wrote {OUT_CSV}")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
