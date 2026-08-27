"""Builder for the physical-scenario figures that have a full CSV source (Tarea 3, CSV-rebuild
part — no vectorization needed): Appetitive/Aversive/Obstacle/Complex_Real_Plot_{1,2,3}.png,
NEU_EST_UNIG_real.png, NEU_EST_MUL_real.png.

Scenario -> folder mapping per experiments/real/MANIFEST.md (Tarea 2):
  Appetitive -> StimuliB_t01..t04   Aversive -> StimuliR_t01..t03
  Obstacle   -> StimuliG_t01..t03   Complex  -> MultiRGB_t01..t03 (D-2, MultiRB discarded)

Column semantics, confirmed by direct inspection (no generating script survives, so this was
reverse-engineered from the raw values, not assumed): `combined_metrics.csv`'s `Tswitch` is a STEP
function, not a running clock -- it holds `0.0` for the rows before the mode switch (placeholder,
undefined) then jumps to a single fixed value and plateaus there for the rest of the recording
(verified row-by-row on `StimuliB_t01`: 5 rows at exactly `0.0`, then every subsequent row of the
288-row trial at exactly `0.875503...`, bit-identical). That plateau value IS the switching delay
in seconds -- "switching delay" here is defined as `max(Tswitch.dropna().unique())` per trial. For
Aversive/Obstacle trials the column never shows a `0.0` segment at all (the recording apparently
starts after the switch already happened, consistent with `results.tex`'s own description of the
Aversive pipeline as a "near-zero computational tick" reflex) -- `max()` still returns the correct
constant value in that case.
"""
from __future__ import annotations

import glob
import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import SCENARIO_COLORS, DPI  # noqa: E402

SCENARIO_FOLDERS = {
    "Appetitive": "StimuliB_t*",
    "Aversive": "StimuliR_t*",
    "Obstacle": "StimuliG_t*",
    "Complex": "MultiRGB_t*",
}


def _trial_dirs(real_root: str, pattern: str) -> list[str]:
    dirs = sorted(glob.glob(os.path.join(real_root, pattern)))
    # exclude anything carrying a DISCARDED.md marker (defensive, MultiRB already excluded by pattern)
    return [d for d in dirs if not os.path.exists(os.path.join(d, "DISCARDED.md"))]


def switching_delay_s(trial_dir: str) -> float | None:
    df = pd.read_csv(os.path.join(trial_dir, "combined_metrics.csv"))
    tsw = df["Tswitch"].dropna()
    if tsw.empty:
        return None
    return float(tsw.max())


def build_ecdf(real_root: str, output_dir: str) -> dict:
    """Plot 1 per scenario: Switching Delay ECDF."""
    results = {}
    for scenario, pattern in SCENARIO_FOLDERS.items():
        dirs = _trial_dirs(real_root, pattern)
        delays = [d for d in (switching_delay_s(t) for t in dirs) if d is not None]
        results[scenario] = delays
        fig, ax = plt.subplots(figsize=(3.2, 3.2))
        if delays:
            x = np.sort(delays)
            y = np.arange(1, len(x) + 1) / len(x)
            ax.step(x, y, where="post", color=SCENARIO_COLORS[scenario], linewidth=2)
            ax.scatter(x, y, color=SCENARIO_COLORS[scenario], s=20, zorder=3)
        ax.set_xlabel("Switching delay (s)")
        ax.set_ylabel("ECDF")
        ax.set_title(f"{scenario} — Switching Delay ECDF (N={len(delays)})")
        fig.tight_layout()
        out = os.path.join(output_dir, f"{scenario}_Real_Plot_1_Switching_Delay_ECDF.png")
        fig.savefig(out, dpi=DPI)
        plt.close(fig)
    return results


def build_bg_dynamics(real_root: str, output_dir: str) -> None:
    """Plot 2 per scenario: firing-variance / mode dynamics over time, first trial as representative."""
    for scenario, pattern in SCENARIO_FOLDERS.items():
        dirs = _trial_dirs(real_root, pattern)
        if not dirs:
            continue
        df = pd.read_csv(os.path.join(dirs[0], "neural_metrics.csv"))
        t = df["sim_time_s"] - df["sim_time_s"].iloc[0]
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.plot(t, df["firing_variance"], color=SCENARIO_COLORS[scenario], linewidth=1.2)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Firing variance")
        ax.set_title(f"{scenario} — Basal Ganglia Dynamics (trial {os.path.basename(dirs[0])})")
        fig.tight_layout()
        out = os.path.join(output_dir, f"{scenario}_Real_Plot_2_Basal_Ganglia_Dynamics.png")
        fig.savefig(out, dpi=DPI)
        plt.close(fig)


def build_rms_dynamics(real_root: str, output_dir: str) -> None:
    """Plot 3 per scenario: Roll/Pitch RMS over time, first trial as representative."""
    for scenario, pattern in SCENARIO_FOLDERS.items():
        dirs = _trial_dirs(real_root, pattern)
        if not dirs:
            continue
        df = pd.read_csv(os.path.join(dirs[0], "combined_metrics.csv"))
        t = df["time_s"] - df["time_s"].iloc[0]
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.plot(t, df["roll_rms"], color=SCENARIO_COLORS[scenario], linewidth=1.2, label="Roll RMS")
        ax.plot(t, df["pitch_rms"], color=SCENARIO_COLORS[scenario], linewidth=1.2, linestyle="--",
                label="Pitch RMS", alpha=0.7)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("RMS (deg)")
        ax.set_title(f"{scenario} — Pitch/Roll RMS Dynamics (trial {os.path.basename(dirs[0])})")
        ax.legend(fontsize=7)
        fig.tight_layout()
        out = os.path.join(output_dir, f"{scenario}_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png")
        fig.savefig(out, dpi=DPI)
        plt.close(fig)


def build_neu_est(real_root: str, output_dir: str) -> None:
    """NEU_EST_UNIG_real.png (Obstacle) / NEU_EST_MUL_real.png (Complex).

    CAVEAT (documented, not silently glossed over): the currently-published NEU_EST_*_real figures
    show individual per-neuron activations (X_0..X_16, gait-decision module, LiDAR "Auxiliary"
    subplot per Informe 1 F-01). experiments/real/*/neural_metrics.csv only has AGGREGATE columns
    (firing_variance, temporal_consistency, lambda_efficiency, mode, red_present, blue_present) --
    it does NOT contain individual X_i neuron traces. This builder therefore produces a simplified,
    aggregate-only substitute (mode timeline + firing variance + stimulus-presence flags), not a
    full reproduction of the original multi-panel raster. This is the same class of gap as
    F-Data-04/05 (simulation IMU-terrain rasters) -- flagged here as a new, analogous finding for
    the physical NEU_EST_* figures, not previously called out this precisely in Informe 2's
    original "Completo" verdict for these two figures.
    """
    configs = [("Obstacle", "StimuliG_t*", "NEU_EST_UNIG_real.png"),
               ("Complex", "MultiRGB_t*", "NEU_EST_MUL_real.png")]
    for scenario, pattern, filename in configs:
        dirs = _trial_dirs(real_root, pattern)
        if not dirs:
            continue
        df = pd.read_csv(os.path.join(dirs[0], "neural_metrics.csv"))
        t = df["sim_time_s"] - df["sim_time_s"].iloc[0]
        fig, axes = plt.subplots(3, 1, figsize=(6, 6), sharex=True)
        axes[0].plot(t, df["firing_variance"], color=SCENARIO_COLORS[scenario])
        axes[0].set_ylabel("Firing variance")
        axes[1].plot(t, df["red_present"], label="red_present", color="red")
        axes[1].plot(t, df["blue_present"], label="blue_present", color="blue")
        axes[1].set_ylabel("Stimulus present")
        axes[1].legend(fontsize=7)
        axes[2].plot(t, pd.Categorical(df["mode"]).codes, drawstyle="steps-post",
                     color=SCENARIO_COLORS[scenario])
        axes[2].set_yticks(range(len(pd.Categorical(df["mode"]).categories)))
        axes[2].set_yticklabels(pd.Categorical(df["mode"]).categories)
        axes[2].set_ylabel("Gait mode")
        axes[2].set_xlabel("Time (s)")
        fig.suptitle(f"{scenario} — aggregate substitute for {filename}\n"
                     f"(no per-neuron X_i data in neural_metrics.csv, see docstring)", fontsize=9)
        fig.tight_layout(rect=(0, 0, 1, 0.93))
        fig.savefig(os.path.join(output_dir, filename.replace(".png", "_AGGREGATE_SUBSTITUTE.png")),
                    dpi=DPI)
        plt.close(fig)


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--real-root", default="experiments/real")
    p.add_argument("--output-dir", default="experiments/N-02-physical-figure-regeneration/output")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    delays = build_ecdf(args.real_root, args.output_dir)
    build_bg_dynamics(args.real_root, args.output_dir)
    build_rms_dynamics(args.real_root, args.output_dir)
    build_neu_est(args.real_root, args.output_dir)

    print("Switching delays (s) per scenario:", delays)
    print(f"Wrote 14 figures to {args.output_dir}")
