"""Builder for fig_stability_phases.png (Group A, R02-01-05 §3/§5) from the vectorized
experiments/_plotting/vectorized/stability_phases.csv (see extract_stability_phases.py for the
extraction method and the incenter/inradius derivation used here).
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import DPI  # noqa: E402

PANEL_GRID = ["A", "B", "C", "D", "E", "F"]


def _order_polygon(points: np.ndarray) -> np.ndarray:
    """Sorts points by angle around their centroid, so drawing them in order traces a
    non-self-intersecting polygon -- exact for a convex quadrilateral (the 4-leg-stance case)."""
    c = points.mean(axis=0)
    ang = np.arctan2(points[:, 1] - c[1], points[:, 0] - c[0])
    return points[np.argsort(ang)]


def _triangle_incenter(pts: np.ndarray) -> tuple[np.ndarray, float]:
    """Side-length-weighted incenter + inradius (area/semiperimeter) for a triangle -- exact
    given real vertices, computed analytically rather than pixel-extracted (see module docstring
    of extract_stability_phases.py)."""
    a = np.linalg.norm(pts[1] - pts[2])
    b = np.linalg.norm(pts[0] - pts[2])
    c = np.linalg.norm(pts[0] - pts[1])
    incenter = (a * pts[0] + b * pts[1] + c * pts[2]) / (a + b + c)
    s = (a + b + c) / 2
    area = 0.5 * abs((pts[1][0] - pts[0][0]) * (pts[2][1] - pts[0][1])
                      - (pts[2][0] - pts[0][0]) * (pts[1][1] - pts[0][1]))
    return incenter, area / s


def build(csv_path: str, output_path: str) -> None:
    df = pd.read_csv(csv_path)
    fig, axes = plt.subplots(2, 3, figsize=(15, 9.5))

    for idx, name in enumerate(PANEL_GRID):
        ax = axes.flat[idx]
        sub = df[df.panel == name]
        stance = sub[sub.point.str.startswith("stance_")][["x_m", "y_m"]].astype(float).to_numpy()
        swing = sub[sub.point == "swing"][["x_m", "y_m"]].astype(float).to_numpy()
        meta = {row.point: row.x_m for row in sub[sub.point.str.startswith("meta_")].itertuples()}
        for k in ("meta_t_s", "meta_tr", "meta_sm_cm"):
            if meta.get(k) is not None:
                meta[k] = float(meta[k])

        ordered = _order_polygon(stance)
        closed = np.vstack([ordered, ordered[0]])
        ax.plot(closed[:, 0], closed[:, 1], color="#1f77b4", linewidth=2, zorder=3)
        ax.fill(closed[:, 0], closed[:, 1], color="#8fce8f", alpha=0.35, zorder=1)
        ax.scatter(stance[:, 0], stance[:, 1], color="#2ca02c", edgecolor="black", s=90, zorder=4,
                   label="Stance Feet")
        ax.scatter([0], [0], color="#d62728", marker="P", s=110, zorder=5, label="CoM (base_link)")

        if len(stance) == 3:
            incenter, r_in = _triangle_incenter(stance)
            ax.add_patch(Circle(incenter, r_in, fill=False, linestyle="--", color="gray",
                                linewidth=1, zorder=2))
            ax.scatter([incenter[0]], [incenter[1]], color="gray", marker="+", s=80, zorder=4,
                      label="Incenter")
            if len(swing):
                ax.scatter(swing[:, 0], swing[:, 1], color="#ff7f0e", marker="X", s=90, zorder=4,
                          label="Swing Foot")
            tr = meta.get("meta_tr")
            sm = meta.get("meta_sm_cm")
            ax.annotate("", xy=tuple(incenter), xytext=(0, 0),
                       arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.2))
            # 2026-09-02 audit fix: the SM label sits at the midpoint of the CoM->incenter arrow,
            # which lands right on top of the CoM (+) or incenter (+) marker whenever they're
            # close together (e.g. panels D/F) -- a digit of the value was getting hidden behind
            # the marker glyph. A white background box keeps the text legible regardless of what
            # it falls on, without having to hand-tune a per-panel offset.
            # zorder=6: above the CoM marker (5) and incenter marker (4) -- without this the "P"/"+"
            # marker glyphs painted on top of the (lower-zorder-by-default) text/bbox when the
            # midpoint landed on or near either marker, which is what caused the occlusion.
            ax.text(0.5 * incenter[0], 0.5 * incenter[1] + 0.02, f"SM = {sm:.1f} cm",
                   color="#d62728", fontsize=8, ha="center", zorder=6,
                   bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
            ax.text(0.97, 0.95, f"TR = {tr:.3f}", transform=ax.transAxes, ha="right", va="top",
                   fontsize=9, bbox=dict(boxstyle="round", fc="#c8e6c9", ec="black"))
        else:
            ax.text(0.97, 0.95, "Static stance", transform=ax.transAxes, ha="right", va="top",
                   fontsize=9, bbox=dict(boxstyle="round", fc="#bbdefb", ec="black"))

        ax.set_xlim(-0.3, 0.3)
        ax.set_ylim(-0.3, 0.3)
        ax.set_aspect("equal")
        ax.set_xlabel("Body X [m]")
        ax.set_ylabel("Body Y [m]")
        ax.grid(alpha=0.3, linestyle="--")
        t_s = meta.get("meta_t_s")
        phase = sub[sub.point == "meta_phase"]["x_m"].iloc[0]
        ax.set_title(f"t = {t_s:.2f} s  |  {phase}", fontsize=10, loc="left")
        ax.text(-0.02, 1.08, name, transform=ax.transAxes, fontsize=16, fontweight="bold")

    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=len(labels), fontsize=9,
              bbox_to_anchor=(0.5, 0.0))
    fig.suptitle("PETER Quadruped --- Static Stability Analysis\nMcGhee-Frank (1968) Stability Margin",
                fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0.06, 1, 0.93))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


if __name__ == "__main__":
    build("experiments/_plotting/vectorized/stability_phases.csv",
          "experiments/N-01-simulation-figure-regeneration/output/fig_stability_phases.png")
    print("Wrote fig_stability_phases.png")
