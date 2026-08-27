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
    fig.suptitle("Dynamic Stability Profile aligned at mode-switch (N=15/terrain)")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


def _ecdf(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = np.sort(values)
    y = np.arange(1, len(x) + 1) / len(x)
    return x, y


def build_fig_b(simulation_root: str, output_path: str) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2))
    tresponse_all = []
    for label, family_name in TERRAINS:
        df = load_trial_summaries(os.path.join(simulation_root, family_name), verdict="SUCCESS")
        tresponse_all.append(df["tresponse"].values)
    ax = axes[0]
    for (label, _), vals in zip(TERRAINS, tresponse_all):
        x, y = _ecdf(np.abs(vals))
        ax.step(x, y, where="post", color=TERRAIN_COLORS[label], label=label)
    ax.set_title(r"$T_{response}$ ECDF")
    ax.set_xlabel("Neural response latency (s)")
    ax.set_ylabel("ECDF")
    ax.legend(fontsize=7)

    for i, (label, family_name) in enumerate(TERRAINS):
        df = load_trial_summaries(os.path.join(simulation_root, family_name), verdict="SUCCESS")
        vals = df["tswitch"].values * 1000.0  # -> ms
        x, y = _ecdf(vals)
        ax2 = axes[1 + i]
        ax2.step(x, y, where="post", color=TERRAIN_COLORS[label])
        ax2.set_title(f"$T_{{switch}}$ ECDF — {label}")
        ax2.set_xlabel("Mechanical transition latency (ms)")

    fig.suptitle("Decision Delay: neural (A) and mechanical (B, C) latency ECDFs, N=15/terrain")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


def build_fig_c(simulation_root: str, output_path: str) -> None:
    fig, ax = plt.subplots(figsize=(5, 5))
    markers = {"Rugged Terrain": "s", "Inclined Slope": "^"}
    for label, family_name in TERRAINS:
        df = load_trial_summaries(os.path.join(simulation_root, family_name), verdict="SUCCESS")
        ax.scatter(df["roll_rms"], df["pitch_rms"], color=TERRAIN_COLORS[label],
                   marker=markers[label], label=label, s=50, edgecolor="black", linewidth=0.5)
    ax.set_xlabel("Transversal Variance — Roll RMS (deg)")
    ax.set_ylabel("Longitudinal Variance — Pitch RMS (deg)")
    ax.set_title("Terrain Adaptability Phase Space (N=30)")
    ax.legend()
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
