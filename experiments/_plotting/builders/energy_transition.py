"""Builder for FigReal_Morphological_Transition_Energy.png.

Source: experiments/real/Test_current_integrated_t01/imu_ina.csv (current_A, voltage_V -> power_W).

DATA-QUALITY CAVEAT (new finding, document before promoting): power_W in this file is ~1e-4 W in
magnitude (current_A ~ -0.07 A, voltage_V ~ 0.00125 V) -- voltage_V in particular is far too small
for a robot battery rail (expected ~7-11 V for a typical 2S/3S LiPo). This strongly suggests either
an uncalibrated raw sensor register (INA219-style current/power monitors report raw ADC counts that
need a conversion-factor multiply that may never have been applied here) or a unit/column mismatch.
The transition instant located below (absolute power-draw peak) is still usable as a RELATIVE marker
within the trial, but the absolute Joule/Wh figures this produces should NOT be trusted at face
value until this is resolved -- flag prominently in the regenerated figure's caption.

There is also an unused `robot_cmd` column (categorical teleoperation key codes: 'c','z','o','i',
'k','u' in this file) that is a plausible ALTERNATIVE marker for the operator-issued transition
command, not used here for lack of a key->action mapping in this repo -- worth investigating before
this figure is promoted, as it would be a more direct signal than an inferred power peak.
"""
from __future__ import annotations

import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import COLOR_BLUE, COLOR_ORANGE, DPI  # noqa: E402


def build(real_root: str, output_path: str) -> dict:
    path = os.path.join(real_root, "Test_current_integrated_t01", "imu_ina.csv")
    df = pd.read_csv(path)
    t = df["time_s"] - df["time_s"].iloc[0]
    peak_idx = df["power_W"].abs().idxmax()
    t_transition = t.iloc[peak_idx]

    fig, ax1 = plt.subplots(figsize=(6, 3.5))
    ax1.plot(t, df["power_W"], color=COLOR_BLUE, linewidth=1)
    ax1.axvline(t_transition, color="red", linestyle="--", linewidth=1,
                label=f"Peak power draw (candidate transition instant, t={t_transition:.1f}s)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Power (W) -- SEE DATA-QUALITY CAVEAT IN DOCSTRING, magnitude not yet validated")
    ax1.legend(fontsize=7)
    ax1.set_title("Morphological Transition Energy -- power draw (Test_current_integrated_t01)")
    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)

    energy_before = (df["power_W"].iloc[:peak_idx].abs() * 0.2).sum()  # ~0.2s sample spacing
    energy_after = (df["power_W"].iloc[peak_idx:].abs() * 0.2).sum()
    return {"t_transition_s": float(t_transition), "energy_before_J_uncalibrated": float(energy_before),
            "energy_after_J_uncalibrated": float(energy_after)}


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--real-root", default="experiments/real")
    p.add_argument("--output", default="experiments/N-02-physical-figure-regeneration/output/FigReal_Morphological_Transition_Energy.png")
    args = p.parse_args()
    stats = build(args.real_root, args.output)
    print(stats)
