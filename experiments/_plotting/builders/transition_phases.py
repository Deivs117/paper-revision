"""Builder for the fused, reversible mode-transition figure (N-09).

Replaces `fig_transition_phases_v9_part1.png`/`_part2.png` (6 directed-transition rows, 3 snapshot
columns each) with a single figure: 3 rows (one per undirected mode pair: C<->H, H<->X, X<->C), 2
columns (the pair's two end states), a double-headed arrow between the two mode boxes instead of a
single directed arrow, and TR/SM reported as a range instead of a single value.

Data provenance (2026-08-29, N-09): no CSV/pipeline exists for the underlying N_total=979-sample
six-transition run (confirmed absent from experiments/simulation/, same situation as N-07's N=268
walk-cycle run) -- per D-1, vectorized directly from the published PNGs instead.

Extraction method (verified, not guessed):
  - Stance-foot vertices (4 per mode) were pixel-extracted from one representative panel per mode
    (C from panel A1, H from panel A3, X from panel B3 of fig_transition_phases_v9_part1.png) using
    the same green-marker color mask + clustering as extract_stability_phases.py (RGB ~(56,142,60),
    885 px per marker, filtered from a handful of much-smaller false-positive clusters near the
    "TR=" label boxes). Axis calibration: 9 evenly-spaced tick marks per axis (detected as short
    black segments just outside each panel's spine), giving x0=-0.4m at the left spine, 1146.25
    px/m, identical scale on both axes and across all 6 row-panels (verified by re-detecting ticks
    independently for rows A/B/C).
  - TR and SM are NOT pixel-extracted -- they are read directly off each panel's own plain-text
    "TR=" label and "SM=... cm" arrow annotation (12 panels read: A1/A3, B1/B3, C1/C3 from part1;
    D1/D3, E1/E3, F1/F3 from part2), same "read the text, don't re-derive it" discipline as
    stability_phases.py. Each mode (C/H/X) appears as either the onset or the final pose in 4 of
    the 6 rows; all 4 readings per mode agree closely (e.g. State C: TR in [0.003, 0.014] across
    A1/C3/D1/F3), which is itself the empirical evidence that both transition directions are
    equally stable -- reported here as a single min-max range per mode rather than per direction.
  - The critical edge (nearest polygon edge to the CoM) and the SM arrow are recomputed
    analytically from the extracted vertices (minimum point-to-segment distance from the origin
    over all 4 edges) -- verified against the text-read SM value for all 3 modes (C: 0.1353 vs
    0.135 published; H: 0.1058 vs 0.105; X: 0.2084 vs 0.208 -- all within extraction noise). The
    inradius circle radius is back-derived from TR = 1 - SM/r_in (same formula as
    sssec:variable_topo_quant), using each mode's mid-range TR/SM.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import DPI  # noqa: E402 -- applies the mandatory serif/10-11-12pt style on import

MODE_COLOR = {"C": (40 / 255, 113 / 255, 197 / 255),
              "H": (232 / 255, 95 / 255, 20 / 255),
              "X": (118 / 255, 45 / 255, 162 / 255)}
MODE_NAME = {"C": "Quadrupedal Walking (C)", "H": "Differential Rolling (H)", "X": "Omnidirectional Motion (X)"}

# Pixel-extracted stance-foot vertices (body-frame metres), one representative panel per mode.
MODE_VERTICES = {
    "C": [(-0.161, -0.107), (0.129, -0.184), (0.141, 0.164), (-0.162, 0.109)],  # from panel A1
    "H": [(-0.308, -0.122), (0.308, -0.125), (0.310, 0.082), (-0.308, 0.130)],  # from panel A3
    "X": [(-0.205, -0.246), (0.217, -0.264), (0.242, 0.232), (-0.212, 0.262)],  # from panel B3
}

# Text-read TR / SM(cm), min-max across all 4 occurrences of that mode across the 6 original rows.
MODE_TR_RANGE = {"C": (0.003, 0.014), "H": (0.078, 0.079), "X": (0.049, 0.049)}
MODE_SM_RANGE_CM = {"C": (13.5, 13.9), "H": (10.5, 10.5), "X": (20.8, 20.8)}

PAIRS = [("C", "H"), ("H", "X"), ("X", "C")]


def _critical_edge(vertices: list[tuple[float, float]]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Returns (ordered vertex array, closest point on the nearest edge to the origin, SM distance)."""
    pts = np.array(vertices)
    ang = np.arctan2(pts[:, 1], pts[:, 0])
    pts = pts[np.argsort(ang)]
    n = len(pts)
    best = None
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        ab = b - a
        t = np.clip(np.dot(-a, ab) / np.dot(ab, ab), 0, 1)
        closest = a + t * ab
        dist = np.linalg.norm(closest)
        if best is None or dist < best[0]:
            best = (dist, i, closest)
    _, i, closest = best
    return pts, i, closest


def _draw_mode_panel(ax, mode: str) -> None:
    pts, crit_i, closest = _critical_edge(MODE_VERTICES[mode])
    n = len(pts)
    color = MODE_COLOR[mode]

    ax.fill(pts[:, 0], pts[:, 1], color=color, alpha=0.15, zorder=1)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        is_crit = i == crit_i
        ax.plot([a[0], b[0]], [a[1], b[1]], color="red" if is_crit else "steelblue",
                linewidth=2.2 if is_crit else 1.6, zorder=3)
    ax.scatter(pts[:, 0], pts[:, 1], color="forestgreen", edgecolor="black", s=70, zorder=4)

    tr_lo, tr_hi = MODE_TR_RANGE[mode]
    sm_lo, sm_hi = MODE_SM_RANGE_CM[mode]
    r_in = ((sm_lo + sm_hi) / 2 / 100.0) / (1 - (tr_lo + tr_hi) / 2)
    ax.add_patch(Circle((0, 0), r_in, fill=False, linestyle="--", edgecolor="gray", linewidth=1, zorder=2))
    ax.annotate("", xy=(closest[0], closest[1]), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="red", linewidth=1.6), zorder=5)
    # 2026-08-29 audit fix: the SM label no longer follows the arrow (it collided with the
    # polygon/arrow in several panels) -- fixed to a centred position just above the X axis
    # instead, same spot in every panel regardless of arrow direction.
    sm_label = f"SM={sm_lo:.1f} cm" if sm_lo == sm_hi else f"SM={sm_lo:.1f}–{sm_hi:.1f} cm"
    ax.text(0.5, 0.035, sm_label, transform=ax.transAxes, fontsize=10, color="darkred",
            ha="center", va="bottom", zorder=6)
    ax.plot(0, 0, marker="+", color="gray", markersize=13, markeredgewidth=1.4, zorder=4.5)
    ax.plot(0, 0, marker="P", color="red", markeredgecolor="black", markersize=11, zorder=5)

    tr_label = f"TR={tr_lo:.3f}" if tr_lo == tr_hi else f"TR={tr_lo:.3f}–{tr_hi:.3f}"
    ax.text(0.97, 0.95, tr_label, transform=ax.transAxes, ha="right", va="top", fontsize=10,
            bbox=dict(boxstyle="round", facecolor="palegreen", edgecolor="black", linewidth=0.6))
    badge = FancyBboxPatch((0.02, 0.85), 0.10, 0.10, transform=ax.transAxes,
                            boxstyle="round,pad=0.02", facecolor=color, edgecolor="black", linewidth=0.6)
    ax.add_patch(badge)
    ax.text(0.07, 0.90, mode, transform=ax.transAxes, ha="center", va="center",
            color="white", fontsize=10, fontweight="bold")

    ax.set_xlim(-0.42, 0.42)
    ax.set_ylim(-0.42, 0.42)
    ax.set_aspect("equal")
    ax.set_xlabel("Body X [m]")
    ax.set_ylabel("Body Y [m]")
    ax.grid(True, linestyle=":", alpha=0.5)


def _mode_box_label(mode: str) -> str:
    """Two-line wrapped mode name, matching the original figure's external label boxes
    (e.g. 'Omnidirectional\\nMotion (X)')."""
    words = MODE_NAME[mode].split(" ")
    mid = len(words) // 2 if len(words) > 2 else 1
    return " ".join(words[:mid]) + "\n" + " ".join(words[mid:])


def _draw_label_stack(ax, mode_a: str, mode_b: str) -> None:
    """Reproduces the original figure's side label style (2026-08-29 revision): two stacked
    colour-coded mode boxes connected by a vertical arrow, restored to the left of each row
    instead of a horizontal arrow placed between the two plots (which overlapped the data).
    Only the arrowhead changed, from single ('->') to double-headed ('<->'), to symbolise that
    the transition is reversible and equally stable in both directions."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # 2026-08-29 audit fix: boxes tightened around the 2-line label (was 0.28 tall, most of it
    # empty colour above/below the text) -- now sized to just fit the text plus a small margin.
    for mode, (y0, y1) in ((mode_a, (0.74, 0.90)), (mode_b, (0.10, 0.26))):
        box = FancyBboxPatch((0.08, y0), 0.84, y1 - y0, boxstyle="round,pad=0.02",
                              facecolor=MODE_COLOR[mode], edgecolor="black", linewidth=1.0,
                              transform=ax.transAxes)
        ax.add_patch(box)
        ax.text(0.5, (y0 + y1) / 2, _mode_box_label(mode), transform=ax.transAxes, ha="center",
                va="center", color="white", fontsize=10, fontweight="bold")

    arrow = FancyArrowPatch((0.5, 0.72), (0.5, 0.28), transform=ax.transAxes,
                             arrowstyle="<->", mutation_scale=18, color="black", linewidth=1.6)
    ax.add_patch(arrow)


def build(output_path: str) -> None:
    fig = plt.figure(figsize=(9.6, 10.5))
    gs = fig.add_gridspec(3, 3, width_ratios=[1.35, 2, 2], wspace=0.35, hspace=0.5)

    for row, (mode_a, mode_b) in enumerate(PAIRS):
        ax_label = fig.add_subplot(gs[row, 0])
        ax_a = fig.add_subplot(gs[row, 1])
        ax_b = fig.add_subplot(gs[row, 2])

        _draw_label_stack(ax_label, mode_a, mode_b)
        _draw_mode_panel(ax_a, mode_a)
        _draw_mode_panel(ax_b, mode_b)
        ax_a.set_title(MODE_NAME[mode_a])
        ax_b.set_title(MODE_NAME[mode_b])

    fig.suptitle("Static Stability Across Reversible Locomotion Mode Transitions\n"
                 "Generalised McGhee–Frank (1968) Support Polygon", fontsize=12)

    # 2026-08-29 audit fix: restore the marker/line legend the original figure carried at the
    # bottom (Support Polygon / Critical Edge / SM Arrow / Polygon Centre / CoM / Stance Feet)
    # plus the mode-colour key -- dropped by mistake when this figure was fused from the 6
    # original rows down to 3. "Swing Foot" is intentionally omitted: unlike the original's
    # snapshot sequences, every panel here is a settled end-state with all 4 feet on the ground,
    # so there is no swing foot to legend.
    legend_handles = [
        Line2D([0], [0], color="steelblue", linewidth=1.6, label="Support Polygon"),
        Line2D([0], [0], color="red", linewidth=2.2, label="Critical Edge"),
        Line2D([0], [0], color="red", marker=">", markersize=6, linewidth=1.6, label="SM Arrow (CoM → Critical Edge)"),
        Line2D([0], [0], color="gray", marker="+", markersize=10, linewidth=0, label="Polygon Centre"),
        Line2D([0], [0], color="red", marker="P", markeredgecolor="black", markersize=9, linewidth=0, label="CoM (base_link)"),
        Line2D([0], [0], color="forestgreen", marker="o", markeredgecolor="black", markersize=8, linewidth=0, label="Stance Feet"),
        Line2D([0], [0], color="gray", linestyle="--", linewidth=1, label="Inradius Circle ($r_{in}$)"),
        Patch(facecolor=MODE_COLOR["C"], edgecolor="black", label="C — Quadrupedal Walking"),
        Patch(facecolor=MODE_COLOR["H"], edgecolor="black", label="H — Differential Rolling"),
        Patch(facecolor=MODE_COLOR["X"], edgecolor="black", label="X — Omnidirectional Motion"),
    ]
    fig.legend(handles=legend_handles, loc="lower center", ncol=4, frameon=True,
               bbox_to_anchor=(0.5, -0.01), fontsize=10)

    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--output", default="experiments/N-01-simulation-figure-regeneration/output/fig_transition_phases_v10.png")
    args = p.parse_args()
    build(args.output)
    print("Wrote", args.output)
