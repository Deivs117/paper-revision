"""Builder for the 5 vectorized physical terrain-IMU figures (Tarea 3, harder tier, completed
2026-08-27): GRAPH_IMU_real/2_real (with F-05's N0/N1/N2 relabeling applied), NEU_IMU_real/2_real,
and FigReal_Terrain_Latencies_4Panels. Consumes the CSVs in experiments/_plotting/vectorized/,
produced by extract_graph_imu_real.py / extract_neu_imu_real.py / extract_terrain_latencies.py.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import DPI  # noqa: E402

ROW_LABELS_F05 = {"Flat": "Flat ($N_0$)", "Inclined": "Inclined ($N_1$)", "Stuck": "Stuck ($N_2$)"}
ROW_ORDER = ["Stuck", "Flat", "Inclined"]  # top-to-bottom, matches the published figure


def build_graph_imu(csv_path: str, output_path: str, title_suffix: str) -> None:
    df = pd.read_csv(csv_path)
    t = sorted(df[df.row == "Stuck"]["time_s"].unique())
    mat = np.array([df[df.row == r].sort_values("time_s")["state"].values for r in ROW_ORDER])
    fig, ax = plt.subplots(figsize=(9, 2.6))
    ax.imshow(mat, aspect="auto", cmap="gray_r", extent=[t[0], t[-1], 3, 0], vmin=0, vmax=1,
              interpolation="nearest")
    ax.set_yticks([0.5, 1.5, 2.5])
    ax.set_yticklabels([ROW_LABELS_F05[r] for r in ROW_ORDER])  # F-05: N0/N1/N2 notation added
    ax.set_xlabel("Time (s)")
    ax.set_title(f"MLP output states: Flat ($N_0$) / Inclined ($N_1$) / Stuck ($N_2$) --{title_suffix}")
    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


def build_neu_imu(csv_path: str, output_path: str) -> None:
    df = pd.read_csv(csv_path)
    panels = ["Locomotion_1", "Locomotion_2", "Decision_1", "Decision_2"]
    titles = {"Locomotion_1": "Locomotion 1", "Locomotion_2": "Locomotion 2",
              "Decision_1": "Decision 1", "Decision_2": "Decision 2"}
    fig, axes = plt.subplots(4, 1, figsize=(8, 10))
    for ax, p in zip(axes, panels):
        sub = df[df.panel == p]
        neurons = list(sub["neuron"].unique())
        t = sorted(sub["time_s"].unique())
        mat = np.array([sub[sub.neuron == n].sort_values("time_s")["activation_normalized"].values
                        for n in neurons])
        ax.imshow(mat, aspect="auto", cmap="gray_r", extent=[t[0], t[-1], len(neurons), 0],
                  vmin=0, vmax=1, interpolation="nearest")
        ax.set_yticks(np.arange(len(neurons)) + 0.5)
        ax.set_yticklabels(neurons)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Neuron")
        ax.set_title(titles[p])
    # Two group titles matching the original figure's layout (Locomotion Module above panels
    # 0-1, Gait Decision Module above panels 2-3) instead of one combined suptitle.
    fig.tight_layout(rect=(0, 0, 1, 0.94), h_pad=3.5)
    fig.text(0.5, 0.975, "Locomotion Module", ha="center", fontsize=11)
    fig.text(0.5, 0.475, "Gait Decision Module", ha="center", fontsize=11)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


def build_terrain_latencies(csv_path: str, output_path: str) -> None:
    df = pd.read_csv(csv_path)
    panel_specs = [
        ("A_Tresponse_Quad2Diff", "#1f77b4", "A. Neural Processing Latency ($T_{response}$)\n"
         "[Quadrupedal $\\to$ Differential Mobile]", "Time Delay (s)"),
        ("B_Tresponse_Diff2Quad", "#ff7f0e", "B. Neural Processing Latency ($T_{response}$)\n"
         "[Differential Mobile $\\to$ Quadrupedal]", "Time Delay (s)"),
        ("C_Tswitch_Quad2Diff", "#2ca089", "C. Electromechanical Coupling Latency ($T_{switch}$)\n"
         "[Quadrupedal $\\to$ Differential Mobile]", "Settling Time (s)"),
        ("D_Tswitch_Diff2Quad", "#d2691e", "D. Electromechanical Coupling Latency ($T_{switch}$)\n"
         "[Differential Mobile $\\to$ Quadrupedal]", "Settling Time (s)"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(11, 8.5))
    for ax, (panel, color, title, xlabel) in zip(axes.flat, panel_specs):
        vals = np.sort(df[df.panel == panel]["value"].values)
        # reconstruct a 15-replicate step ECDF from the N distinct jump values found: each
        # detected jump may represent >1 tied replicate -- without that multiplicity (not stored
        # by the extractor) this assumes equal spacing, i.e. a lower-fidelity ECDF than the
        # original but topologically the same step pattern, ADEQUATE for shape validation, not
        # for citing exact per-replicate values -- see vectorized/README.md caveat
        n = len(vals)
        y = np.arange(1, n + 1) / n
        ax.step(np.concatenate([[vals[0]], vals]), np.concatenate([[0], y]), where="post",
                color=color, linewidth=2, label="Hardware Replicates (reconstructed)")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Empirical Probability $P(T \\leq t)$")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3, linestyle="--")
    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


def build_neu_est(csv_path: str, output_path: str, panels: list[str], group_titles: dict) -> None:
    """NEU_EST_UNIG_real.png / NEU_EST_MUL_real.png -- multi-column raster, see
    extract/extract_neu_est_real.py. `group_titles` maps a panel name to the group title placed
    above it (only set on the first panel of each group)."""
    df = pd.read_csv(csv_path)
    n = len(panels)
    ncols = 2
    nrows = (n + 1) // 2
    fig, axes = plt.subplots(nrows, ncols, figsize=(6 * ncols, 2.6 * nrows))
    axes = axes.flatten() if n > 1 else [axes]
    for ax, p in zip(axes, panels):
        sub = df[df.panel == p]
        neurons = list(sub["neuron"].unique())
        t = sorted(sub["time_s"].unique())
        mat = np.array([sub[sub.neuron == n_].sort_values("time_s")["activation_normalized"].values
                        for n_ in neurons])
        ax.imshow(mat, aspect="auto", cmap="gray_r", extent=[t[0], t[-1], len(neurons), 0],
                  vmin=0, vmax=1, interpolation="nearest")
        ax.set_yticks(np.arange(len(neurons)) + 0.5)
        ax.set_yticklabels(neurons, fontsize=6)
        ax.set_xlabel("Time (s)")
        ax.set_title(p.replace("_", " "), fontsize=8)
        if p in group_titles:
            ax.annotate(group_titles[p], xy=(0.5, 1.28), xycoords="axes fraction",
                        ha="center", fontsize=10)
    for ax in axes[n:]:
        ax.axis("off")
    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


if __name__ == "__main__":
    vec = "experiments/_plotting/vectorized"
    out = "experiments/N-02-physical-figure-regeneration/output"

    build_graph_imu(f"{vec}/graph_imu_real.csv", f"{out}/GRAPH_IMU_real.png", " Rugged Terrain (Physical)")
    build_graph_imu(f"{vec}/graph_imu2_real.csv", f"{out}/GRAPH_IMU2_real.png", " Inclined Slope (Physical)")
    build_neu_imu(f"{vec}/neu_imu_real.csv", f"{out}/NEU_IMU_real.png")
    build_neu_imu(f"{vec}/neu_imu2_real.csv", f"{out}/NEU_IMU2_real.png")
    build_terrain_latencies(f"{vec}/terrain_latencies.csv", f"{out}/FigReal_Terrain_Latencies_4Panels.png")

    build_neu_est(
        f"{vec}/neu_est_unig_real.csv", f"{out}/NEU_EST_UNIG_real.png",
        ["Lidar", "Input", "Response", "Auxiliary", "Locomotion_1", "Locomotion_2",
         "Decision_1", "Decision_2"],
        {"Lidar": "Lidar Network Module", "Locomotion_1": "Locomotion Module",
         "Decision_1": "Gait Decision Module"},
    )
    build_neu_est(
        f"{vec}/neu_est_mul_real.csv", f"{out}/NEU_EST_MUL_real.png",
        ["BasalGanglia_GPi", "BasalGanglia_GPe", "BasalGanglia_STN", "BasalGanglia_STR",
         "Locomotion_1", "Locomotion_2", "Lidar", "Input", "Response", "Auxiliary",
         "Decision_1", "Decision_2"],
        {"BasalGanglia_GPi": "Basal Ganglia Module", "Lidar": "Lidar Network Module",
         "Locomotion_1": "Locomotion Module", "Decision_1": "Gait Decision Module"},
    )
    print("Wrote all 7 vectorized-figure regenerations to", out)
