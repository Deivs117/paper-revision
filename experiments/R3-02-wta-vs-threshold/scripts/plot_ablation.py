"""Publication figures for the R3-01/R3-02 basal-ganglia ablation study.

Reads output/ablation_stats_summary.csv (already computed by analyze_ablation.py) and writes:
  - output/fig_ablation_success_rate.png   (success rate by variant x scenario, Fisher p vs full)
  - output/fig_ablation_complex_stability.png (roll_rms/pitch_rms by variant, Complex Navigation only,
    Mann-Whitney p vs full)

Not promoted to assets/ yet -- see README.md for that step (scripts/promote_figure.sh).
"""
import csv
import os

import matplotlib.pyplot as plt

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "_plotting"))
from style import COLOR_BLUE, COLOR_ORANGE, COLOR_GREEN, COLOR_PINK, DPI  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "..", "output", "ablation_stats_summary.csv")
OUT_DIR = os.path.join(HERE, "..", "output")

VARIANT_ORDER = ["full", "no_lateral_inhibition", "no_stn_str", "threshold_only"]
VARIANT_LABEL = {
    "full": "Full (control)",
    "no_lateral_inhibition": "No lateral\ninhibition",
    "no_stn_str": "No STN/STR\nlayers",
    "threshold_only": "Threshold\nonly",
}
VARIANT_COLOR = {
    "full": COLOR_BLUE,
    "no_lateral_inhibition": COLOR_ORANGE,
    "no_stn_str": COLOR_PINK,
    "threshold_only": COLOR_GREEN,
}
SCENARIO_LABEL = {"appetitive": "Appetitive Targeting\n(no conflict)", "complex": "Complex Navigation\n(3-stimulus conflict)"}


def load_rows():
    with open(CSV_PATH, newline="") as f:
        return list(csv.DictReader(f))


def fmt_p(p):
    if p == "" or p is None:
        return ""
    p = float(p)
    if p < 0.001:
        return "p<0.001"
    return f"p={p:.3f}"


def plot_success_rate(rows):
    # Single panel, Complex Navigation only -- the Appetitive (no-conflict) scenario shows no
    # meaningful separation between variants (91.7-100%, p=1.0 across the board) and is stated
    # in prose instead of plotted (2026-08-31, author request).
    scenario = "complex"
    fig, ax = plt.subplots(figsize=(5, 4.5))
    vals = {r["mode"]: float(r["value"]) for r in rows
            if r["scenario"] == scenario and r["metric"] == "success_rate"}
    ps = {r["mode"]: r["p_value_vs_full"] for r in rows
          if r["scenario"] == scenario and r["metric"] == "success_rate"}
    xs = list(range(len(VARIANT_ORDER)))
    heights = [vals[m] * 100 for m in VARIANT_ORDER]
    colors = [VARIANT_COLOR[m] for m in VARIANT_ORDER]
    ax.bar(xs, heights, color=colors, width=0.6)
    for x, m in zip(xs, VARIANT_ORDER):
        label = fmt_p(ps[m]) if ps[m] else ""
        ax.text(x, heights[x] + 3, label, ha="center", va="bottom", fontsize=9)
    ax.set_xticks(xs)
    ax.set_xticklabels([VARIANT_LABEL[m] for m in VARIANT_ORDER], fontsize=9)
    ax.set_ylim(0, 115)
    ax.set_ylabel("Success rate (%)")
    ax.set_title("Complex Navigation (3-stimulus conflict)\nFisher exact $p$ vs. full circuit, $n=12$/cell", fontsize=10)
    fig.tight_layout()
    out = os.path.join(OUT_DIR, "fig_ablation_success_rate.png")
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print("wrote", out)


def plot_complex_stability(rows):
    metrics = ["roll_rms", "pitch_rms"]
    metric_label = {"roll_rms": "Roll RMS (deg)", "pitch_rms": "Pitch RMS (deg)"}
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    for ax, metric in zip(axes, metrics):
        sub = {r["mode"]: r for r in rows if r["scenario"] == "complex" and r["metric"] == metric}
        xs = list(range(len(VARIANT_ORDER)))
        heights = [float(sub[m]["value"]) for m in VARIANT_ORDER]
        colors = [VARIANT_COLOR[m] for m in VARIANT_ORDER]
        errs = []
        for m in VARIANT_ORDER:
            lo, hi, v = sub[m]["ci_low"], sub[m]["ci_high"], float(sub[m]["value"])
            if lo == "" or hi == "":
                errs.append([0, 0])
            else:
                errs.append([v - float(lo), float(hi) - v])
        errs = list(zip(*errs))  # [(lower...), (upper...)]
        ax.bar(xs, heights, color=colors, width=0.6,
               yerr=errs, capsize=3, error_kw={"linewidth": 1})
        for x, m in zip(xs, VARIANT_ORDER):
            p = sub[m]["p_value_vs_full"]
            if p:
                ax.text(x, heights[x] + errs[1][x] + 0.03, fmt_p(p), ha="center", va="bottom", fontsize=8)
        ax.set_xticks(xs)
        ax.set_xticklabels([VARIANT_LABEL[m] for m in VARIANT_ORDER], fontsize=8)
        ax.set_title(metric_label[metric], fontsize=10)
        ax.set_ylabel(metric_label[metric])
    fig.suptitle("Attitude stability under conflict (Complex Navigation), Mann-Whitney p vs. full", fontsize=10)
    fig.tight_layout()
    out = os.path.join(OUT_DIR, "fig_ablation_complex_stability.png")
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    rows = load_rows()
    plot_success_rate(rows)
    plot_complex_stability(rows)
