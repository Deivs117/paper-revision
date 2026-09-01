"""Figura R2 (`robustez_transferencia_tecnica.md` §11): Roll/Pitch RMS vs. combined perturbation
level, Rugged Terrain + Inclined Slope. Companion to `noise_sweep_grid.py` ("Figura R1"-equivalent
for the 4 behavioral scenarios) and to `ecdf_phase_space.py` (FigA/B/C, which never encode noise
level — see `intake/pending/R3-04_images_pipeline_audit.md` §3b).

Purpose: `ecdf_phase_space.build_fig_c()` (FigC_Terrain_Adaptability) shows roll_rms vs. pitch_rms
as a scatter with NO noise-level encoding at all — it cannot answer "does postural stability
degrade with perturbation severity", which is exactly R3-04's ask for the terrain scenarios. This
module answers that directly instead of overloading FigC's existing, already-approved design.
"""
from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loaders import load_trial_summaries  # noqa: E402
from style import TERRAIN_COLORS, DPI  # noqa: E402

TERRAINS = [("Rugged Terrain", "familia_c1_terreno_rugoso"), ("Inclined Slope", "familia_c2_pendiente")]
AXIS_LABEL = "Combined Perturbation Level (index)"
FOOTNOTE = ("Index 0–4 jointly scales IMU drift + LiDAR range noise + camera illumination "
            "distortion (no single-sensor-isolated condition exists in this dataset).")


def collect(family_dir: str) -> dict:
    df = load_trial_summaries(family_dir, verdict="SUCCESS")
    if df.empty:
        raise RuntimeError(f"No SUCCESS trials found in {family_dir}")
    noise_levels = sorted(df["noise_level_idx"].dropna().unique().astype(int))
    out = {"noise_levels": noise_levels, "roll": [], "roll_sd": [], "pitch": [], "pitch_sd": []}
    for n in noise_levels:
        sub = df[df["noise_level_idx"] == n]
        out["roll"].append(sub["roll_rms"].mean())
        out["roll_sd"].append(sub["roll_rms"].std(ddof=0) if len(sub) > 1 else 0.0)
        out["pitch"].append(sub["pitch_rms"].mean())
        out["pitch_sd"].append(sub["pitch_rms"].std(ddof=0) if len(sub) > 1 else 0.0)
    return out


def build(simulation_root: str, output_path: str) -> dict:
    fig, axes = plt.subplots(2, 2, figsize=(9, 6), sharex=True)
    col_titles = ["Roll RMS (deg)", "Pitch RMS (deg)"]
    all_data = {}

    for row, (label, family_name) in enumerate(TERRAINS):
        family_dir = os.path.join(simulation_root, family_name)
        data = collect(family_dir)
        all_data[label] = data
        color = TERRAIN_COLORS[label]
        x = data["noise_levels"]

        for col, (y, sd) in enumerate([(data["roll"], data["roll_sd"]), (data["pitch"], data["pitch_sd"])]):
            ax = axes[row, col]
            ax.errorbar(x, y, yerr=sd, marker="s", color=color, capsize=3, linewidth=1.5)
            if row == 0:
                ax.set_title(col_titles[col])
            if row == 1:
                ax.set_xlabel(AXIS_LABEL, fontsize=9)
        axes[row, 0].set_ylabel(label, fontsize=10, fontweight="bold")

    fig.suptitle("Postural Stability vs. Combined Perturbation Level\n"
                 "(Rugged Terrain + Inclined Slope, R3-04 dataset, N=15 trials/terrain)", fontsize=11)
    fig.text(0.5, 0.005, FOOTNOTE, ha="center", va="bottom", fontsize=7.5, color="gray")
    fig.tight_layout(rect=(0, 0.03, 1, 0.91))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)
    return all_data


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--simulation-root", default="experiments/R3-04-noise-robustness/data")
    p.add_argument("--output", default="experiments/R3-04-noise-robustness/output/fig_R2_terrain_stability_vs_noise.png")
    args = p.parse_args()

    data = build(args.simulation_root, args.output)
    print(f"Wrote {args.output}")
