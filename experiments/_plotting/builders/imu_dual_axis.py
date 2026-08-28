"""Builder for GRAPH_IMU.png / GRAPH_IMU2.png (simulation, F-04) from the vectorized
experiments/_plotting/vectorized/graph_imu.csv / graph_imu2.csv (see extract_graph_imu_sim.py).

Applies all of F-04's fixes in one pass: double Y-axis (was a single mixed "V A L U E" axis
superposing m/s^2 and degrees), corrected legend text ("Standar dev accel z" -> "sigma_az -- Std.
dev. accel. Z", matching methodology.tex:354's notation; "Pitch angle" -> "Pitch (deg)"), an added
3.7 threshold line on the acceleration axis (U_{sigma_az}, methodology.tex:354/275 -- the value
results.tex:199 already cites but the original figure never drew), and a title differentiated by
terrain instead of the generic "IMU activity" repeated on both.
"""
from __future__ import annotations

import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import DPI  # noqa: E402

U_SIGMA_AZ = 3.7  # methodology.tex:275/354, cited (undrawn) in the original by results.tex:199


def build(csv_path: str, output_path: str, title_suffix: str) -> None:
    df = pd.read_csv(csv_path)
    accel = df[df.series == "std_accel_z"].sort_values("time_s")
    pitch = df[df.series == "pitch_angle"].sort_values("time_s")

    fig, ax1 = plt.subplots(figsize=(9, 4.5))
    ax2 = ax1.twinx()

    l1, = ax1.plot(accel.time_s, accel.value, color="#1f77b4", linewidth=1.2,
                   label=r"$\sigma_{az}$ --- Std. dev. accel. Z")
    ax1.axhline(U_SIGMA_AZ, color="#1f77b4", linestyle="--", linewidth=1.2, alpha=0.7)
    ax1.annotate(r"$U_{\sigma_{az}}$ threshold", xy=(accel.time_s.max() * 0.98, U_SIGMA_AZ),
                ha="right", va="bottom", fontsize=8, color="#1f77b4")
    l2, = ax2.plot(pitch.time_s, pitch.value, color="#ff7f0e", linewidth=1.2, label="Pitch (deg)")

    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel(r"Std. dev. acceleration, Z axis (m/s$^2$)", color="#1f77b4")
    ax2.set_ylabel("Pitch angle (deg)", color="#ff7f0e")
    ax1.tick_params(axis="y", labelcolor="#1f77b4")
    ax2.tick_params(axis="y", labelcolor="#ff7f0e")
    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)
    ax1.grid(alpha=0.3, linestyle="--")
    ax1.set_title(f"IMU activity --- {title_suffix} (Simulation)")
    ax1.legend(handles=[l1, l2], loc="upper left", fontsize=8)

    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


if __name__ == "__main__":
    vec = "experiments/_plotting/vectorized"
    out = "experiments/N-01-simulation-figure-regeneration/output"
    build(f"{vec}/graph_imu.csv", f"{out}/GRAPH_IMU.png", "Rugged Terrain")
    build(f"{vec}/graph_imu2.csv", f"{out}/GRAPH_IMU2.png", "Inclined Slope")
    print("Wrote GRAPH_IMU.png / GRAPH_IMU2.png")
