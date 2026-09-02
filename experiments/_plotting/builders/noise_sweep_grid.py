"""Successor to macro_robustness.py's fig1_noise_robustness_grid.png, purpose-built for the R3-04
per-sensor noise-robustness dataset (`experiments/R3-04-noise-robustness/data/`).

**Decision 2026-08-31 (`intake/pending/R3-04_images_pipeline_audit.md`, "fig1 grid" question,
author choice: reemplazar por completo):** this is a NEW module, not an edit to
`macro_robustness.py` — `macro_robustness.py` stays exactly as-is, still valid for regenerating the
OLD generic-noise dataset (`experiments/simulation/`) if ever needed again, per its own D-12
design. This module reuses the same `loaders`/`style` primitives but:

1. Adds a 4th column, **Mode-Switch Latency $T_{switch}$ (ms)** — the metric the simulation team
   proposed as "Figura R1" (`robustez_transferencia_tecnica.md` §11), absent from the original
   3-column grid. Folding it into the same grid instead of a separate figure avoids the exact kind
   of duplication R2-01 already asked to cut.
2. Replaces the generic "Sensory Noise Index (σ)" x-axis label with an explicit statement of what
   the single swept index actually controls in this dataset — IMU drift + LiDAR range noise +
   camera illumination, **combined, not isolated per sensor** (see
   `experiments/R3-04-noise-robustness/config.yaml` and
   `robustez_transferencia_tecnica.md` §7 "Perturbaciones combinadas/simultáneas" for why: there is
   no condition in this dataset that perturbs only one sensor at a time).
3. Points at `experiments/R3-04-noise-robustness/data/` by default (still overridable via
   `--simulation-root`, same D-12 flag convention) and no longer needs the Obstacle-latency
   vectorized fallback (`familia_a_obstaculo` has real `exp_latency` data in this dataset, verified
   directly — see the images-pipeline audit doc, Pregunta 4).

`FigC_Terrain_Adaptability`-style noise encoding for `familia_c1_terreno_rugoso`/
`familia_c2_pendiente` is intentionally NOT added here — those two live in `terrain_noise_sweep.py`
("Figura R2"), not this grid, same split the original pipeline already had between
`macro_robustness.py` (4 behavioral scenarios) and `ecdf_phase_space.py` (2 terrain scenarios).
"""
from __future__ import annotations

import os
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loaders import load_trial_summaries  # noqa: E402
from style import SCENARIO_COLORS, DPI  # noqa: E402

SCENARIOS = [
    ("Appetitive", "familia_a_apetitivo"),
    ("Aversive", "familia_a_aversivo"),
    ("Obstacle", "familia_a_obstaculo"),
    ("Complex", "familia_b_compleja"),
]

AXIS_LABEL = "Combined Perturbation Level (index)"
FOOTNOTE = ("Index 0–4 jointly scales IMU drift + LiDAR range noise + camera illumination distortion "
            "(no single-sensor-isolated condition exists in this dataset).\n"
            "Each point averages only 3 trials — read point-to-point zig-zags as sampling variance, "
            "not a mechanistic effect.")


def collect_scenario(family_dir: str) -> dict:
    """Per-noise-level mean/sd for T_sim, pitch_rms, latency (ms), and tswitch (ms)."""
    df = load_trial_summaries(family_dir, verdict="SUCCESS")
    if df.empty:
        raise RuntimeError(f"No SUCCESS trials found in {family_dir}")

    noise_levels = sorted(df["noise_level_idx"].dropna().unique().astype(int))
    result = {"noise_levels": noise_levels, "T_sim": [], "T_sim_sd": [],
              "pitch": [], "pitch_sd": [], "latency": [], "latency_sd": [],
              "tswitch": [], "tswitch_sd": []}

    for n in noise_levels:
        sub = df[df["noise_level_idx"] == n]
        result["T_sim"].append(sub["sim_time_s"].mean())
        result["T_sim_sd"].append(sub["sim_time_s"].std(ddof=0) if len(sub) > 1 else 0.0)
        result["pitch"].append(sub["pitch_rms"].mean())
        result["pitch_sd"].append(sub["pitch_rms"].std(ddof=0) if len(sub) > 1 else 0.0)

        lat = sub["exp_latency"].dropna()
        lat = lat[lat >= 0]
        result["latency"].append(lat.mean() * 1000.0 if len(lat) else np.nan)
        result["latency_sd"].append(lat.std(ddof=0) * 1000.0 if len(lat) > 1 else 0.0)

        tsw = sub["tswitch"].dropna()
        result["tswitch"].append(tsw.mean() * 1000.0 if len(tsw) else np.nan)
        result["tswitch_sd"].append(tsw.std(ddof=0) * 1000.0 if len(tsw) > 1 else 0.0)

    return result


def build_grid(simulation_root: str, output_path: str) -> dict:
    fig, axes = plt.subplots(4, 4, figsize=(13, 11), sharex=True)
    col_titles = ["Mission Time $T_{sim}$ (s)", "Pitch RMS (deg)",
                  "Decision Latency (ms)", "Mode-Switch Latency $T_{switch}$ (ms)"]
    all_data = {}

    # First pass: collect every scenario's data before plotting, so the Pitch RMS column can share
    # a common ceiling across all 4 rows (tight, not the old fixed 0-4 deg) — per author feedback
    # (r304_audit_notes_2026-09-01.md): keep magnitude comparable row-to-row (unlike per-row
    # auto-scaling, which would hide that Complex/Aversive/Appetitive sit well below Obstacle's
    # range) while still showing the smaller scenarios' variation, which the old fixed 0-4 ceiling
    # flattened into near-invisible lines.
    for scenario, family_name in SCENARIOS:
        family_dir = os.path.join(simulation_root, family_name)
        all_data[scenario] = collect_scenario(family_dir)

    pitch_ceiling = max(
        (y + sd for d in all_data.values() for y, sd in zip(d["pitch"], d["pitch_sd"]) if y == y),
        default=4.0,
    )
    pitch_ceiling = pitch_ceiling * 1.1  # small headroom so the topmost error bar cap isn't clipped

    for row, (scenario, family_name) in enumerate(SCENARIOS):
        data = all_data[scenario]
        color = SCENARIO_COLORS[scenario]
        x = data["noise_levels"]

        series = [
            (data["T_sim"], data["T_sim_sd"]),
            (data["pitch"], data["pitch_sd"]),
            (data["latency"], data["latency_sd"]),
            (data["tswitch"], data["tswitch_sd"]),
        ]
        for col, (y, sd) in enumerate(series):
            ax = axes[row, col]
            if all(v != v for v in y):  # all-NaN
                ax.text(0.5, 0.5, "No data recorded\nin this run", ha="center", va="center",
                        fontsize=7, color="gray", transform=ax.transAxes)
                ax.set_xticks(x)
            else:
                ax.errorbar(x, y, yerr=sd, marker="o", color=color, capsize=3, linewidth=1.5)
            ax.set_xticks(x)  # integer-only ticks, no matplotlib-inserted decimals
            if row == 0:
                ax.set_title(col_titles[col])
            if row == 3:
                ax.set_xlabel(AXIS_LABEL, fontsize=9)
            if col == 1:
                ax.set_ylim(0, pitch_ceiling)
        axes[row, 0].set_ylabel(scenario, fontsize=10, fontweight="bold")

    fig.suptitle("Multisensor Noise-Robustness Battery — 4 Scenarios x 4 Metrics\n"
                 "(simulation, R3-04 dataset, N=15 trials/scenario)", fontsize=11)
    fig.text(0.5, 0.005, FOOTNOTE, ha="center", va="bottom", fontsize=7.5, color="gray")
    fig.tight_layout(rect=(0, 0.045, 1, 0.95))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)
    return all_data


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--simulation-root", default="experiments/R3-04-noise-robustness/data")
    p.add_argument("--output", default="experiments/R3-04-noise-robustness/output/fig1_noise_robustness_grid.png")
    args = p.parse_args()

    data = build_grid(args.simulation_root, args.output)
    print(f"Wrote {args.output}")
