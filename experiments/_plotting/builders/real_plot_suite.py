"""Builder for the physical-scenario figures that have a full CSV source (Tarea 3, CSV-rebuild
part — no vectorization needed): Appetitive/Aversive/Obstacle/Complex_Real_Plot_{1,3}.png.

**Decision 2026-08-27 (author audit round, n02_audit_notes):** `*_Real_Plot_2_Basal_Ganglia_Dynamics.png`
is REMOVED from this pipeline's output, not just deprioritized — the author's plan is to answer the
reviewer's "cut repetitive descriptions, duplicated neural raster plots and identical stability
curves between simulation and physical tests" request by dropping this redundant STANDALONE figure.
**Correction (round 2 of the audit, same day):** `*_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png`
was NEVER a single-panel RMS-only figure — verified directly against the published originals
(`assets/Appetitive_Real_Plot_3_..._.png` etc.): it always had two stacked panels, **A) "Basal
Ganglia Neural Response Dynamics"** (the same firing-variance line `_Real_Plot_2` also showed, fixed
orange `#D55E00`) and **B) "Chasis Kinematic Attitude Stabilization Space"** (Pitch/Roll RMS, fixed
purple `#4B0082`/lavender `#B8A9D9` — NOT scenario-colored, confirmed fixed across scenarios by
inspecting two different originals). `_Real_Plot_2` was redundant with panel A specifically, not
with the whole figure — the first pass of this fix incorrectly dropped panel A entirely instead of
just removing the now-redundant standalone `_2` figure, and misplaced the red/blue stimulus-presence
shading on panel B instead of panel A. Fixed here: `build_rms_dynamics()` restores both panels with
their original fixed colors, and the shading (Appetitive/Aversive/Complex only — NOT Obstacle, whose
stimulus is green and doesn't fit the red/blue scheme, confirmed by the author) is on panel A only.
`build_bg_dynamics()` (the old standalone-only version) is kept below, unused, as a reference.

`NEU_EST_UNIG_real.png`/`NEU_EST_MUL_real.png` moved OUT of this file — they're now vectorized by
pixel-intensity extraction (same technique as `NEU_IMU_real.png`), see `extract/extract_neu_est_real.py`.
The CSV-based "aggregate substitute" this file used to produce for them was REJECTED by the author
("no representan lo mismo... no rehacer" — i.e. don't try to approximate them from aggregate
columns at all, only a true per-neuron reproduction counts).

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
        ax.set_xlabel("Switching delay (s)")
        ax.set_ylabel("ECDF")
        ax.set_title(f"{scenario} — Switching Delay ECDF (N={len(delays)})")
        fig.tight_layout()
        out = os.path.join(output_dir, f"{scenario}_Real_Plot_1_Switching_Delay_ECDF.png")
        fig.savefig(out, dpi=DPI)
        plt.close(fig)
    return results


def build_bg_dynamics(real_root: str, output_dir: str) -> None:
    """DEPRECATED, not called from __main__ (see module docstring, decision 2026-08-27).

    Kept only as a reference for what data the removed *_Real_Plot_2_Basal_Ganglia_Dynamics.png
    used, in case the later results.tex pass needs to pull a number from it."""
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


def _stimulus_presence_spans(neural_csv: str, t0: float, t_grid: np.ndarray) -> dict:
    """Resamples red_present/blue_present from neural_metrics.csv onto combined_metrics.csv's
    time grid (different sampling, same epoch base — verified directly, not assumed) and returns
    a boolean mask per color for shading."""
    n = pd.read_csv(neural_csv)
    nt = n["sim_time_s"] - t0
    red = np.interp(t_grid, nt, n["red_present"], left=0, right=0) > 0.5
    blue = np.interp(t_grid, nt, n["blue_present"], left=0, right=0) > 0.5
    return {"red": red, "blue": blue}


def build_rms_dynamics(real_root: str, output_dir: str) -> None:
    """Plot 3 per scenario: Roll/Pitch RMS over time, first trial as representative.

    Decision 2026-08-27: shades the background red/blue wherever the aversive/appetitive stimulus
    was in view (from the companion neural_metrics.csv, resampled onto this file's time grid) --
    folds in what the removed *_Real_Plot_2_Basal_Ganglia_Dynamics.png used to show separately,
    per the author's instruction, instead of a standalone firing-variance line plot.

    ROUND-2 FIX (2026-08-27): restores the original two-panel A/B structure (see module
    docstring) instead of only regenerating panel B. Shading moves to panel A, and only applies to
    Appetitive/Aversive/Complex -- Obstacle's stimulus is green, so the red/blue scheme doesn't
    apply there and its panel A stays exactly like the published original (confirmed explicitly by
    the author, "NO COLOREAR ESTÍMULOS A LA VISTA" for Obstacle)."""
    FIRING_VARIANCE_COLOR = "#D55E00"  # fixed orange, matches every published original inspected
    PITCH_COLOR = "#4B0082"            # fixed purple
    ROLL_COLOR = "#B8A9D9"             # fixed lavender
    SHADED_SCENARIOS = {"Appetitive", "Aversive", "Complex"}  # NOT Obstacle -- see docstring

    for scenario, pattern in SCENARIO_FOLDERS.items():
        dirs = _trial_dirs(real_root, pattern)
        if not dirs:
            continue
        trial_dir = dirs[0]
        combined = pd.read_csv(os.path.join(trial_dir, "combined_metrics.csv"))
        t0 = combined["time_s"].iloc[0]
        t_b = combined["time_s"] - t0

        neural = pd.read_csv(os.path.join(trial_dir, "neural_metrics.csv"))
        t_a = neural["sim_time_s"] - t0

        fig, (ax_a, ax_b) = plt.subplots(2, 1, figsize=(7, 7))

        if scenario in SHADED_SCENARIOS:
            presence = _stimulus_presence_spans(os.path.join(trial_dir, "neural_metrics.csv"), t0, t_a.values)
            ax_a.fill_between(t_a, 0, 1, where=presence["red"], transform=ax_a.get_xaxis_transform(),
                              color="#D55E00", alpha=0.15, step="mid", label="Aversive stimulus in view")
            ax_a.fill_between(t_a, 0, 1, where=presence["blue"], transform=ax_a.get_xaxis_transform(),
                              color="#0072B2", alpha=0.15, step="mid", label="Appetitive stimulus in view")
            ax_a.legend(fontsize=8, loc="upper left")
        ax_a.plot(t_a, neural["firing_variance"], color=FIRING_VARIANCE_COLOR, linewidth=1.5)
        ax_a.set_ylabel("Firing Variance $Var(z)$")
        ax_a.set_title("A. Basal Ganglia Neural Response Dynamics")

        ax_b.plot(t_b, combined["pitch_rms"], color=PITCH_COLOR, linewidth=1.5, label="Pitch RMS")
        ax_b.plot(t_b, combined["roll_rms"], color=ROLL_COLOR, linewidth=1.5, linestyle="--",
                  label="Roll RMS")
        ax_b.set_xlabel("Experimental Time (s)")
        ax_b.set_ylabel("Attitude Space RMS (deg)")
        ax_b.set_title("B. Chasis Kinematic Attitude Stabilization Space")
        ax_b.legend(loc="lower right")

        fig.tight_layout(rect=(0, 0, 1, 0.96))
        fig.suptitle(f"{scenario} (trial {os.path.basename(trial_dir)})", fontsize=10)
        out = os.path.join(output_dir, f"{scenario}_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png")
        fig.savefig(out, dpi=DPI)
        plt.close(fig)


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--real-root", default="experiments/real")
    p.add_argument("--output-dir", default="experiments/N-02-physical-figure-regeneration/output")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    delays = build_ecdf(args.real_root, args.output_dir)
    build_rms_dynamics(args.real_root, args.output_dir)
    # build_bg_dynamics() intentionally NOT called -- see module docstring, decision 2026-08-27.
    # NEU_EST_UNIG_real/NEU_EST_MUL_real moved to extract/extract_neu_est_real.py (vectorized).

    print("Switching delays (s) per scenario:", delays)
    print(f"Wrote 8 figures to {args.output_dir}")
