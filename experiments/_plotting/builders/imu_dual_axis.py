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
from style import DPI, COLOR_BLUE, COLOR_ORANGE  # noqa: E402

U_SIGMA_AZ = 3.7  # methodology.tex:275/354, cited (undrawn) in the original by results.tex:199


def build(csv_path: str, output_path: str, title_suffix: str) -> None:
    df = pd.read_csv(csv_path)
    accel = df[df.series == "std_accel_z"].sort_values("time_s")
    pitch = df[df.series == "pitch_angle"].sort_values("time_s")

    fig, ax1 = plt.subplots(figsize=(9, 4.5))
    ax2 = ax1.twinx()

    l1, = ax1.plot(accel.time_s, accel.value, color=COLOR_BLUE, linewidth=1.2,
                   label="$\\sigma_{az}$\u2014Std. dev. accel. Z")
    ax1.axhline(U_SIGMA_AZ, color=COLOR_BLUE, linestyle="--", linewidth=1.2, alpha=0.7)
    # R3b-04 batch 2: the sigma_az trace oscillates across the threshold at the right edge, so the
    # curve used to strike through this label (Reviewer 3 item 4). Kept at the right edge -- the left
    # one is taken by the legend -- and given an opaque white backing, so the trace now passes behind
    # the text instead of through it, whatever the data does.
    ax1.annotate(r"$U_{\sigma_{az}}$ threshold", xy=(accel.time_s.max() * 0.98, U_SIGMA_AZ),
                ha="right", va="bottom", color=COLOR_BLUE,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    l2, = ax2.plot(pitch.time_s, pitch.value, color=COLOR_ORANGE, linewidth=1.2, label="Pitch (deg)")

    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel(r"Std. dev. acceleration, Z axis (m/s$^2$)", color=COLOR_BLUE)
    ax2.set_ylabel("Pitch angle (deg)", color=COLOR_ORANGE)
    ax1.tick_params(axis="y", labelcolor=COLOR_BLUE)
    ax2.tick_params(axis="y", labelcolor=COLOR_ORANGE)
    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)
    ax1.set_title(f"IMU activity\u2014{title_suffix} (Simulation)")
    # Opaque backing for the same reason as the annotation above: the horizontal threshold line
    # runs at y=3.7 straight through this legend's text. The shared style sets frameon False,
    # which is right for figures with nothing behind the legend; here there is.
    ax1.legend(handles=[l1, l2], loc="upper left", frameon=True, facecolor="white",
               edgecolor="none", framealpha=1.0)

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
