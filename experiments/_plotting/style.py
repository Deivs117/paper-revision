"""Shared matplotlib style for every figure builder under experiments/_plotting/.

One source of truth for palette, fonts and export settings so every regenerated figure looks
consistent with the rest of the manuscript, and so a future style change (e.g. brand palette swap)
happens in one file instead of N builders. See intake/pending/R02-01_data_traceability_and_plotting_plan.md
§3 for the rationale.
"""
import matplotlib

matplotlib.use("Agg")  # headless — these scripts never open a window
import matplotlib.pyplot as plt

# Palette matching the colors already used across the manuscript's existing figures (blue/orange/
# pink/green), per the Informe 1 audit's own description of the document's visual language.
COLOR_BLUE = "#1f77b4"
COLOR_ORANGE = "#ff7f0e"
COLOR_PINK = "#e377c2"
COLOR_GREEN = "#2ca02c"
COLOR_GRAY = "#7f7f7f"

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

DPI = 200


def apply_style():
    plt.rcParams.update(
        {
            "figure.dpi": 100,
            "savefig.dpi": DPI,
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "grid.linewidth": 0.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "savefig.bbox": "tight",
            "font.family": "sans-serif",
        }
    )


apply_style()
