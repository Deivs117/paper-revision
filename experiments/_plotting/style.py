"""Shared matplotlib style for every figure builder under experiments/_plotting/.

One source of truth for palette, fonts and export settings so every regenerated figure looks
consistent with the rest of the manuscript, and so a future style change (e.g. brand palette swap)
happens in one file instead of N builders. See intake/pending/R02-01_data_traceability_and_plotting_plan.md
§3 for the rationale.

Style source (2026-08-27): `.claude/skills/scientific-visualization/assets/publication.mplstyle`,
imported from the `scientific-visualization` Claude Code skill
(https://github.com/K-Dense-AI/scientific-agent-skills) per the author's explicit request to bring
this project's figure typography/precision up to the standard of e.g. `assets/fig1_Obstacle_macro.png`.
Do not hand-edit the color/font constants below without also checking whether the underlying
.mplstyle file should change instead — the .mplstyle is the actual source of truth for rcParams;
this file only adds the semantic color aliases (SCENARIO_COLORS, TERRAIN_COLORS) our builders use.
"""
import os

import matplotlib

matplotlib.use("Agg")  # headless — these scripts never open a window
import matplotlib.pyplot as plt

_STYLE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    ".claude", "skills", "scientific-visualization", "assets", "publication.mplstyle",
)

# Okabe-Ito colorblind-safe palette (WCAG 3:1 against white in sRGB), same 5 colors the
# .mplstyle file sets as axes.prop_cycle — named here so builders can pick a specific one
# deliberately (e.g. "blue for Appetitive") instead of relying on cycle order.
COLOR_BLUE = "#0072B2"
COLOR_ORANGE = "#D55E00"
COLOR_GREEN = "#009E73"
COLOR_PINK = "#CC79A7"
COLOR_BLACK = "#000000"
COLOR_GRAY = "#7f7f7f"  # not in the Okabe-Ito 5 — informational/muted use only, never a data series

SCENARIO_COLORS = {
    "Appetitive": COLOR_BLUE,
    "Aversive": COLOR_ORANGE,
    "Obstacle": COLOR_GREEN,
    "Complex": COLOR_PINK,
}

TERRAIN_COLORS = {
    "Rugged Terrain": COLOR_BLUE,
    "Inclined Slope": COLOR_ORANGE,
}

DPI = 300  # matches savefig.dpi in publication.mplstyle


def apply_style():
    if os.path.exists(_STYLE_FILE):
        plt.style.use(_STYLE_FILE)
    else:
        # Fallback if the skill folder isn't present in this checkout — keeps builders runnable,
        # but the real style source is the .mplstyle file; regenerate figures after fetching it.
        plt.rcParams.update({
            "figure.dpi": 100, "savefig.dpi": DPI, "font.size": 8, "axes.titlesize": 9,
            "axes.labelsize": 8, "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
            "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
            "savefig.bbox": "standard", "font.family": "sans-serif",
        })


apply_style()
