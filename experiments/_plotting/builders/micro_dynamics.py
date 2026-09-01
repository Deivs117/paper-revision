"""Builder for fig2_{Scenario}_micro_{trial_dir}.png — single representative-trial temporal
dynamics figure per behavioral scenario (Appetitive/Aversive/Obstacle/Complex), simulation side.

**Decision 2026-08-31 (R3-04 images-pipeline audit, `intake/pending/R3-04_images_pipeline_audit.md`
Preguntas 2/3):** these 4 figures never had a generator script (verified by exhaustive repo search)
— they were produced once, out of band, for the old `experiments/simulation/` dataset. Rebuilding
them for the R3-04 noise-robustness dataset is a chance to bring them in line with the physical
counterpart this pipeline already produces (`real_plot_suite.py::build_rms_dynamics()`), per the
author's explicit request: same two-panel A/B structure, same fixed colors, same panel titles
("A. Basal Ganglia Neural Response Dynamics" / "B. Chasis Kinematic Attitude Stabilization Space"),
and the same red/blue stimulus-in-view shading on panel A (Appetitive/Aversive/Complex only — NOT
Obstacle, whose stimulus is green and doesn't fit the red/blue scheme; same rule the physical
version uses, confirmed applicable here too since `metrics_raw.csv` has no `green_present` column
to shade with).

**Differences from the physical version, forced by the data layout (not stylistic choices):**
- Trial selection: physical picks `dirs[0]` (first trial found); simulation now spans 5 noise
  levels per family, so `dirs[0]` is not a stable/meaningful "representative" trial anymore. Uses
  `loaders.find_trial_by_noise_level(family_dir, noise_level_idx=0)` instead — the undisturbed
  baseline, so this figure keeps showing "clean" single-trial dynamics (as the pre-R3-04 version
  implicitly did, sourced from a dataset with no per-sensor noise at all) while the noise-sweep
  figures (Fig R1/R2, `macro_robustness.py`/`ecdf_phase_space.py`) are where the ruido effect is
  shown. `NOISE_LEVEL_IDX` below is the single knob to change this later if the author decides a
  different representative level is wanted.
- Data split: `metrics_raw.csv` (panel A: `firing_variance`, `red_present`, `blue_present`, time
  column `sim_time_s`) + `unified_metrics.csv` (panel B: `pitch_rms`/`roll_rms`, time column
  `time_s`) — mirrors the physical `neural_metrics.csv`/`combined_metrics.csv` split exactly, just
  under simulation's own column names (see `loaders.load_metrics_raw`/`load_unified_metrics`).
- Filename kept as `fig2_{Scenario}_micro_{trial_dir}.png` (NOT renamed to `..._Sim_Plot_3_...`) —
  `sections/results.tex` already references `fig:appetitive_micro` etc. against this pattern; the
  author decided against a purely cosmetic rename that would force an otherwise-unneeded
  `sections/*.tex` edit next round.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loaders import (  # noqa: E402
    find_trial_by_noise_level, load_metrics_raw, load_unified_metrics,
)

NOISE_LEVEL_IDX = 0  # representative trial's noise level — see module docstring

SCENARIOS = [
    ("Appetitive", "familia_a_apetitivo"),
    ("Aversive", "familia_a_aversivo"),
    ("Obstacle", "familia_a_obstaculo"),
    ("Complex", "familia_b_compleja"),
]
SHADED_SCENARIOS = {"Appetitive", "Aversive", "Complex"}  # NOT Obstacle — green stimulus, no red/blue scheme

FIRING_VARIANCE_COLOR = "#D55E00"  # fixed orange — matches real_plot_suite.build_rms_dynamics()
PITCH_COLOR = "#4B0082"            # fixed purple
ROLL_COLOR = "#B8A9D9"             # fixed lavender
DPI = 300


def _stimulus_presence_masks(raw: pd.DataFrame) -> dict:
    """Boolean red/blue masks straight off metrics_raw.csv — no resampling needed here (unlike the
    physical version): panel A's own source file already carries red_present/blue_present on the
    same time grid as firing_variance, no separate neural_metrics.csv to interpolate from."""
    return {
        "red": raw["red_present"].fillna(0).to_numpy() > 0.5,
        "blue": raw["blue_present"].fillna(0).to_numpy() > 0.5,
    }


def build(simulation_root: str, output_dir: str) -> dict[str, str]:
    """Regenerates all 4 fig2_*_micro figures. Returns {scenario: output_path}."""
    os.makedirs(output_dir, exist_ok=True)
    written = {}

    for scenario, family_name in SCENARIOS:
        family_dir = os.path.join(simulation_root, family_name)
        trial_dir = find_trial_by_noise_level(family_dir, NOISE_LEVEL_IDX)
        if trial_dir is None:
            raise RuntimeError(
                f"No SUCCESS trial with noise_level_idx={NOISE_LEVEL_IDX} found in {family_dir}")
        trial_name = os.path.basename(trial_dir)

        raw = load_metrics_raw(trial_dir)
        t_a = raw["sim_time_s"] - raw["sim_time_s"].iloc[0]

        unified = load_unified_metrics(trial_dir)
        t_b = unified["time_s"] - unified["time_s"].iloc[0]

        fig, (ax_a, ax_b) = plt.subplots(2, 1, figsize=(7, 7))

        if scenario in SHADED_SCENARIOS:
            presence = _stimulus_presence_masks(raw)
            ax_a.fill_between(t_a, 0, 1, where=presence["red"], transform=ax_a.get_xaxis_transform(),
                              color="#D55E00", alpha=0.15, step="mid", label="Aversive stimulus in view")
            ax_a.fill_between(t_a, 0, 1, where=presence["blue"], transform=ax_a.get_xaxis_transform(),
                              color="#0072B2", alpha=0.15, step="mid", label="Appetitive stimulus in view")
            ax_a.legend(fontsize=8, loc="upper left")
        ax_a.plot(t_a, raw["firing_variance"], color=FIRING_VARIANCE_COLOR, linewidth=1.5)
        ax_a.set_ylabel("Firing Variance $Var(z)$")
        ax_a.set_title("A. Basal Ganglia Neural Response Dynamics")

        ax_b.plot(t_b, unified["pitch_rms"], color=PITCH_COLOR, linewidth=1.5, label="Pitch RMS")
        ax_b.plot(t_b, unified["roll_rms"], color=ROLL_COLOR, linewidth=1.5, linestyle="--",
                  label="Roll RMS")
        ax_b.set_xlabel("Experimental Time (s)")
        ax_b.set_ylabel("Attitude Space RMS (deg)")
        ax_b.set_title("B. Chasis Kinematic Attitude Stabilization Space")
        ax_b.legend(loc="lower right")

        # Same defensive NaN-lead-in guard real_plot_suite.py added for Obstacle (round 4):
        # sync panel A's x-range to panel B's autoscaled range in case either series starts with
        # NaNs that would otherwise leave one panel's dead lead-in unaligned with the other's.
        if np.isfinite(ax_b.get_xlim()).all():
            ax_a.set_xlim(ax_b.get_xlim())

        # Author feedback (r304_audit_notes_2026-09-01.md): remove the top suptitle — it exposed
        # raw internal test identifiers (test_NNN_SUCCESS, noise_level_idx) directly in the
        # figure, which README.md §11.1 already forbids in reader-facing material. The panel
        # titles alone (A./B.) carry the figure's content; scenario + representative-trial context
        # belongs in the results.tex caption, not baked into the image.
        fig.tight_layout()

        out_path = os.path.join(output_dir, f"fig2_{scenario}_micro_{trial_name}.png")
        fig.savefig(out_path, dpi=DPI)
        plt.close(fig)
        written[scenario] = out_path

    return written


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--simulation-root", default="experiments/R3-04-noise-robustness/data")
    p.add_argument("--output-dir", default="experiments/R3-04-noise-robustness/output")
    args = p.parse_args()

    out = build(args.simulation_root, args.output_dir)
    for scenario, path in out.items():
        print(f"[micro_dynamics] wrote {scenario} -> {path}")
