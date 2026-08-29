"""Vectorizes assets/fig_stability_phases.png -> experiments/_plotting/vectorized/stability_phases.csv

R02-01-05 §3 (Group A, F-08/F-Data-03): this N=268 walk-cycle run was never archived to
experiments/ (confirmed by three separate checks across this project's rounds: no
stability_log.csv anywhere has 268 rows). Per D-6 (still in force), tab:crawl_stability's
TR_mean=0.439 stays the source of truth for the AGGREGATE number -- this script only reconstructs
the 6-panel illustrative figure that accompanies it, so the regenerated PNG is code-traceable
instead of a historical file with no known generator.

Extraction strategy (pixel color + geometry, not WebPlotDigitizer -- same refinement as every
other figure this round): each of the 6 panels (A-F, a 2x3 grid) plots a top-down body-frame
support-polygon diagram. Per panel:
  - Stance feet (green circle markers, RGB ~(56,142,60)) -- 3 per panel in the 4 swing-phase
    panels (A, C, D, F), 4 per panel in the 2 static-stance panels (B, E).
  - Swing foot (orange X marker, RGB ~(245,124,0)) -- present only in A/C/D/F.
  - CoM is NOT extracted -- by construction, "Body X/Y" is a body-frame plot centered on
    base_link, so CoM sits at the origin (0,0) in every panel; confirmed visually (the red cross
    is at the plot center in all 6 panels).
Axis calibration: all 6 panels share an identical -0.3..0.3 m grid on both axes (confirmed by
detecting the dashed gridline pixel columns/rows independently per panel-column/panel-row and
finding the same 1950 px/m scale everywhere) -- one global px-per-metre constant, plus each
panel's own top-left tick pixel as its local origin, is enough; no per-panel recalibration needed.

One color-mask pitfall found and handled: the 4 swing-phase panels (A/C/D/F) carry a green-bordered
"TR = x.xxx" label box in their top-right corner, using a similar green tone to the stance-foot
markers -- left unfiltered, this leaks 4-5 small spurious "feet" per panel from the label's text/
border pixels. Fixed by dropping any green-mask cluster with data-y > 0.25 (stance feet never
appear there; the label box does) rather than trying to color-distinguish the two greens, which
are too close to separate reliably.

The incenter + inscribed-circle overlay (drawn only on the 4 triangular swing-phase panels, per
the original) is NOT extracted from pixels -- it's recomputed analytically from the extracted
triangle vertices (standard side-length-weighted incenter formula, inradius = area/semiperimeter),
which is exact given real vertices, rather than adding a second pixel-detection pass for a
derived quantity. TR, SM, and the per-panel timestamp/phase-name are read directly off the
figure's own plain-text labels (not pixel-graph values needing calibration) -- t/phase-name/TR/SM
for A/C/D/F, "Static stance" for B/E.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
from PIL import Image

IMG = "assets/fig_stability_phases.png"
OUT_CSV = "experiments/_plotting/vectorized/stability_phases.csv"

COL_X0 = [192, 1962, 3732]  # "-0.3" tick column, one per panel-column
ROW_Y0 = [435, 2029]  # "+0.3" tick row, one per panel-row
PX_PER_M = 1950.0

# Read directly off the published figure's own text labels (not pixel-extracted values).
PANEL_META = {
    "A": dict(t=120.46, phase="LU Swing Phase", tr=0.706, sm_cm=2.8),
    "B": dict(t=121.06, phase="4-Leg Stance", tr=None, sm_cm=None),
    "C": dict(t=121.40, phase="RD Swing Phase", tr=0.748, sm_cm=2.5),
    "D": dict(t=121.91, phase="RU Swing Phase", tr=0.774, sm_cm=2.2),
    "E": dict(t=122.42, phase="4-Leg Stance", tr=None, sm_cm=None),
    "F": dict(t=122.75, phase="LD Swing Phase", tr=0.746, sm_cm=2.5),
}
PANEL_GRID = ["A", "B", "C", "D", "E", "F"]  # row-major, 2 rows x 3 cols


def _green_mask(a):
    return ((np.abs(a[:, :, 0].astype(int) - 56) < 40) & (np.abs(a[:, :, 1].astype(int) - 142) < 40)
            & (np.abs(a[:, :, 2].astype(int) - 60) < 40))


def _orange_mask(a):
    return ((np.abs(a[:, :, 0].astype(int) - 245) < 20) & (np.abs(a[:, :, 1].astype(int) - 124) < 25)
            & (a[:, :, 2].astype(int) < 60))


def _cluster_points(ys, xs, dist=40):
    clusters = []  # [sum_x, sum_y, count]
    for x, y in zip(xs.tolist(), ys.tolist()):
        for cl in clusters:
            cx, cy = cl[0] / cl[2], cl[1] / cl[2]
            if (cx - x) ** 2 + (cy - y) ** 2 < dist ** 2:
                cl[0] += x; cl[1] += y; cl[2] += 1  # noqa: E702
                break
        else:
            clusters.append([x, y, 1])
    return [(c[0] / c[2], c[1] / c[2], c[2]) for c in clusters]


def _px_to_xy(col, row, cx0, ry0):
    return -0.3 + (col - cx0) / PX_PER_M, 0.3 - (row - ry0) / PX_PER_M


def extract() -> pd.DataFrame:
    arr = np.array(Image.open(IMG).convert("RGB"))
    rows = []
    for idx, name in enumerate(PANEL_GRID):
        r, c = divmod(idx, 3)
        cx0, ry0 = COL_X0[c], ROW_Y0[r]
        y0, y1 = ry0 - 100, ry0 + 1170 + 150
        x0, x1 = cx0 - 150, cx0 + 1169 + 150
        crop = arr[y0:y1, x0:x1]

        gm = _green_mask(crop)
        gy, gx = np.where(gm)
        stance_px = [(cx + x0, cy + y0, n) for cx, cy, n in _cluster_points(gy, gx) if n >= 50]
        stance_xy = [_px_to_xy(cx, cy, cx0, ry0) for cx, cy, _ in stance_px]
        stance_xy = [(x, y) for x, y in stance_xy if y < 0.25]  # drop TR-label-box artifacts

        om = _orange_mask(crop)
        oy, ox = np.where(om)
        swing_xy = None
        if len(ox):
            oc = [c for c in _cluster_points(oy, ox) if c[2] >= 20]
            if oc:
                bx, by, _ = max(oc, key=lambda z: z[2])
                swing_xy = _px_to_xy(bx + x0, by + y0, cx0, ry0)

        for i, (fx, fy) in enumerate(stance_xy):
            rows.append({"panel": name, "point": f"stance_{i}", "x_m": round(fx, 4),
                        "y_m": round(fy, 4)})
        if swing_xy:
            rows.append({"panel": name, "point": "swing", "x_m": round(swing_xy[0], 4),
                        "y_m": round(swing_xy[1], 4)})
        rows.append({"panel": name, "point": "com", "x_m": 0.0, "y_m": 0.0})

        meta = PANEL_META[name]
        rows.append({"panel": name, "point": "meta_t_s", "x_m": meta["t"], "y_m": None})
        rows.append({"panel": name, "point": "meta_phase", "x_m": meta["phase"], "y_m": None})
        rows.append({"panel": name, "point": "meta_tr", "x_m": meta["tr"], "y_m": None})
        rows.append({"panel": name, "point": "meta_sm_cm", "x_m": meta["sm_cm"], "y_m": None})

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = extract()
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    df.to_csv(OUT_CSV, index=False)
    print(f"Wrote {OUT_CSV}")
    for p in PANEL_GRID:
        sub = df[df.panel == p]
        n_stance = (sub.point.str.startswith("stance_")).sum()
        print(p, "stance points:", n_stance, "has swing:", (sub.point == "swing").any())
