"""Builder for FigA_Stability_Profile / FigB_Decision_Delay / FigC_Terrain_Adaptability.

All three come from the same 15+15 trials (familia_c1_terreno_rugoso = Rugged Terrain,
familia_c2_pendiente = Inclined Slope) and are the figures behind M-01-M-04 (already verified
correct against this exact data in Informe 2 §0) — regenerating them here is meant to produce a
byte-fresh, code-traceable version of what's already published, not to change the numbers.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loaders import load_stability_log_aligned, load_trial_summaries, list_trial_dirs  # noqa: E402
from style import TERRAIN_COLORS, DPI  # noqa: E402

TERRAINS = [("Rugged Terrain", "familia_c1_terreno_rugoso"), ("Inclined Slope", "familia_c2_pendiente")]


def _resample_mean_sd(trial_dirs: list[str], grid: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    curves = []
    for d in trial_dirs:
        stab = load_stability_log_aligned(d)
        curves.append(np.interp(grid, stab["t_aligned"], stab["TR"], left=np.nan, right=np.nan))
    arr = np.array(curves)
    return np.nanmean(arr, axis=0), np.nanstd(arr, axis=0)


def build_fig_a(simulation_root: str, output_path: str) -> None:
    grid = np.linspace(-5, 10, 300)
    fig, axes = plt.subplots(2, 1, figsize=(4.5, 6), sharex=True)
    for ax, (label, family_name) in zip(axes, TERRAINS):
        trial_dirs = list_trial_dirs(os.path.join(simulation_root, family_name), verdict="SUCCESS")
        mean, sd = _resample_mean_sd(trial_dirs, grid)
        color = TERRAIN_COLORS[label]
        ax.plot(grid, mean, color=color, linewidth=1.5)
        ax.fill_between(grid, mean - sd, mean + sd, color=color, alpha=0.25)
        ax.axhline(1.0, color="red", linestyle="--", linewidth=1, label="Overturning boundary (TR=1.0)")
        ax.axvline(0.0, color="gray", linestyle=":", linewidth=1)
        ax.set_ylabel("Tipover Risk (TR)")
        ax.set_title(label)
        ax.set_ylim(0, 1.15)
    axes[-1].set_xlabel("Time relative to mode-switch instant (s)")
    axes[0].legend(loc="upper right", fontsize=7)
    # 2026-08-29 audit fix: dropped the extra fig.suptitle() stacked above the two per-panel
    # titles — that redundant title band was the "espacio perdido" the author flagged; the
    # published fig1/FigA precedent (assets/FigA_Stability_Profile.png) never had one, only the
    # per-panel titles carry the needed context ("N=15" folded into each panel's own title
    # instead of a separate "N=15/terrain" line above both).
    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


def _ecdf(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = np.sort(values)
    y = np.arange(1, len(x) + 1) / len(x)
    return x, y


def build_fig_b(simulation_root: str, output_path: str) -> None:
    # 2026-08-29 audit: the T_response ECDF panel was dropped (it read ~0 for every trial in both
    # terrains and added no explicability — see the audit notes). That value is now reported as
    # prose in results.tex instead of plotted. Only the two T_switch (mechanical transition) ECDF
    # panels remain, one per terrain, relettered (A)/(B).
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.2))

    for i, (label, family_name) in enumerate(TERRAINS):
        df = load_trial_summaries(os.path.join(simulation_root, family_name), verdict="SUCCESS")
        vals = df["tswitch"].values * 1000.0  # -> ms
        x, y = _ecdf(vals)
        ax = axes[i]
        ax.step(x, y, where="post", color=TERRAIN_COLORS[label])
        letter = chr(ord("A") + i)
        ax.set_title(f"{letter}. {label} ($T_{{switch}}$)", fontsize=11)
        ax.set_xlabel("Mechanical transition latency (ms)")
    axes[0].set_ylabel("ECDF")

    # 2026-08-29 audit fix: same "espacio perdido" pattern as FigA — dropped the outer
    # fig.suptitle() (its "N=15/terrain" content is already in the results.tex caption, per the
    # published fig precedent assets/FigB_Decision_Delay.png, which titles each panel directly
    # with no outer suptitle either) and kept only the short per-panel titles.
    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


def report_tresponse_summary(simulation_root: str) -> dict[str, dict[str, float]]:
    """Prints/returns the T_response stats that used to be the dropped ECDF panel, so the
    replacement prose sentence in results.tex can cite a real number instead of just "~0"."""
    summary: dict[str, dict[str, float]] = {}
    for label, family_name in TERRAINS:
        df = load_trial_summaries(os.path.join(simulation_root, family_name), verdict="SUCCESS")
        vals = np.abs(df["tresponse"].values)
        summary[label] = {"mean": float(np.mean(vals)), "max": float(np.max(vals)), "n": int(len(vals))}
    return summary


def build_fig_c(simulation_root: str, output_path: str) -> None:
    fig, ax = plt.subplots(figsize=(5, 5))
    markers = {"Rugged Terrain": "s", "Inclined Slope": "^"}
    pitch_means = {}
    for label, family_name in TERRAINS:
        df = load_trial_summaries(os.path.join(simulation_root, family_name), verdict="SUCCESS")
        ax.scatter(df["roll_rms"], df["pitch_rms"], color=TERRAIN_COLORS[label],
                   marker=markers[label], label=label, s=50, edgecolor="black", linewidth=0.5)
        pitch_means[label] = float(df["pitch_rms"].mean())

    # 2026-08-29 audit fix: the separation between clusters is on the Pitch RMS axis, not Roll RMS
    # (results.tex:280 already states the Roll-RMS overlap is deliberate evidence of comparably
    # effective lateral stabilisation — no divider is drawn there). Divider sits at the midpoint
    # between the two terrain means, labelled by zone instead of left as an unexplained line.
    boundary = (pitch_means["Rugged Terrain"] + pitch_means["Inclined Slope"]) / 2.0
    ax.axhline(boundary, color="gray", linestyle="--", linewidth=1)
    ax.text(ax.get_xlim()[1], boundary, f"  Pitch RMS ≈ {boundary:.2f}° boundary",
            va="center", ha="left", fontsize=7, color="gray", clip_on=False)
    # Zone labels sit in the empty mid-right band of the plot (x~0.55 in axes fraction) to avoid
    # overlapping the data, which clusters at low Roll RMS on both sides of the boundary.
    y0, y1 = ax.get_ylim()
    boundary_frac = (boundary - y0) / (y1 - y0)
    ax.text(0.55, boundary_frac - 0.03, "Rugged Terrain zone", transform=ax.transAxes,
            fontsize=8, color=TERRAIN_COLORS["Rugged Terrain"], va="top", ha="center")
    ax.text(0.55, boundary_frac + 0.03, "Inclined Slope zone", transform=ax.transAxes,
            fontsize=8, color=TERRAIN_COLORS["Inclined Slope"], va="bottom", ha="center")

    ax.set_xlabel("Transversal Variance — Roll RMS (deg)")
    ax.set_ylabel("Longitudinal Variance — Pitch RMS (deg)")
    ax.set_title("Terrain Adaptability Phase Space (N=30)")
    # 2026-08-29 audit fix: the legend swatches (same square/triangle markers as the real data)
    # were easy to mistake for actual points sitting in that corner — shade the legend box itself
    # (opaque white fill, gray border) so it reads as UI chrome, not data.
    ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="gray",
              framealpha=0.95).set_zorder(10)
    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--simulation-root", default="experiments/simulation")
    p.add_argument("--output-dir", default="experiments/N-01-simulation-figure-regeneration/output")
    args = p.parse_args()

    build_fig_a(args.simulation_root, os.path.join(args.output_dir, "FigA_Stability_Profile.png"))
    build_fig_b(args.simulation_root, os.path.join(args.output_dir, "FigB_Decision_Delay.png"))
    build_fig_c(args.simulation_root, os.path.join(args.output_dir, "FigC_Terrain_Adaptability.png"))
    print("Wrote FigA/FigB/FigC to", args.output_dir)
