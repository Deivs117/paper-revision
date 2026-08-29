"""R2-04 -- long-term average steady-state power consumption per locomotion mode.

Reviewer ask (R2-04, PROGRESS.md): "Supplement long-term average energy consumption of three
locomotion modes for onboard deployment analysis." This is DISTINCT from
experiments/N-02-physical-figure-regeneration/'s FigReal_Morphological_Transition_Energy.png, which
measures energy spent DURING a mode transition (a brief event) -- this measures average power draw
WHILE OPERATING in each of the 3 modes (Quadrupedal/Differential Mobile/Omnidirectional), excluding
the transition windows themselves. Do not conflate the two.

Method: same robot_cmd structural-command detection as the transition-energy figure
(experiments/_plotting/builders/energy_transition.py) -- 'c'/'z'/'x' mark entry into Quadrupedal
(C)/Differential Mobile (H)/Omnidirectional (X). For each maximal segment where the active mode is
constant, EXCLUDE the pre-calibrated electromechanical coupling window from the segment's start
(2.92s for a segment entered via 'z', 1.56s via 'c' -- same values already published in
FigReal_Terrain_Latencies_4Panels; no calibrated window exists for 'x', so X segments use their
full duration, unadjusted -- see caveat below) and average power = |current_A| * 7.2V (fixed NiMH
pack voltage, confirmed by the author's hardware team) over what remains: the genuine steady-state
portion.

CAVEATS (report alongside the figure, do not silently omit):
  1. Only ONE real steady-state Omnidirectional segment exists across all 5 instrumented recordings
     (floor_t01, 38.6s) -- no SD, no cross-trial replication for that mode. C and H have N=20
     segments each.
  2. The 5 source recordings span different physical conditions (flat floor, inclined ramp, static
     in-place test) mixed together -- part of the within-mode variance reflects that heterogeneity,
     not just measurement noise. Segment-level power values are printed below for transparency.
  3. Still subject to the same instrumentation caveat as the transition-energy figure: current_A is
     confirmed trustworthy, but these are short (bench/lab) recordings, not a true long-duration
     mission profile -- "long-term average" here means "averaged over the available steady-state
     segments", not a multi-hour endurance test.
"""
from __future__ import annotations

import glob
import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "_plotting"))
from style import DPI  # noqa: E402

TEST_DIRS = [
    "Test_current_integrated_floor_t01", "Test_current_integrated_ramp_t01",
    "Test_current_integrated_ramp_t02", "Test_current_integrated_static_t01",
    "Test_current_integrated_t01",
]
WINDOW_S = {"z": 2.92, "c": 1.56, "x": 0.0}  # x: no calibrated window, full segment used
MODE_OF_CMD = {"c": "Quadrupedal (C)", "z": "Differential Mobile (H)", "x": "Omnidirectional (X)"}
MODE_COLORS = {"Quadrupedal (C)": "#0072B2", "Differential Mobile (H)": "#D55E00",
               "Omnidirectional (X)": "#009E73"}
NOMINAL_VOLTAGE_V = 7.2


def steady_state_segments(real_root: str) -> list[dict]:
    segments = []
    for d in TEST_DIRS:
        df = pd.read_csv(os.path.join(real_root, d, "imu_ina.csv"))
        struct = df[df["robot_cmd"].isin(["c", "z", "x"])].copy()
        struct["prev"] = struct["robot_cmd"].shift(1)
        events = struct[struct["robot_cmd"] != struct["prev"]]
        times = events["time_s"].tolist()
        cmds = events["robot_cmd"].tolist()
        for i in range(len(times)):
            t0 = times[i]
            t1 = times[i + 1] if i + 1 < len(times) else df["time_s"].iloc[-1]
            steady_start = t0 + WINDOW_S[cmds[i]]
            if steady_start >= t1:
                continue
            mask = (df["time_s"] >= steady_start) & (df["time_s"] <= t1)
            seg = df.loc[mask]
            if len(seg) < 2:
                continue
            power = seg["current_A"].abs().values * NOMINAL_VOLTAGE_V
            segments.append({
                "trial": d, "mode": MODE_OF_CMD[cmds[i]], "mean_power_W": float(power.mean()),
                "duration_s": float(t1 - steady_start),
            })
    return segments


def build(real_root: str, output_path: str) -> dict:
    segments = steady_state_segments(real_root)
    by_mode: dict[str, list[float]] = {m: [] for m in MODE_OF_CMD.values()}
    for s in segments:
        by_mode[s["mode"]].append(s["mean_power_W"])

    modes = list(MODE_OF_CMD.values())
    means = [np.mean(by_mode[m]) if by_mode[m] else np.nan for m in modes]
    sds = [np.std(by_mode[m]) if len(by_mode[m]) > 1 else 0.0 for m in modes]
    ns = [len(by_mode[m]) for m in modes]

    fig, ax = plt.subplots(figsize=(7, 5.5))
    colors = [MODE_COLORS[m] for m in modes]
    bars = ax.bar(modes, means, yerr=sds, capsize=5, color=colors, width=0.5)
    for bar, n, sd in zip(bars, ns, sds):
        note = f"N={n}" if n > 1 else f"N={n}\n(single segment)"
        ax.annotate(note, xy=(bar.get_x() + bar.get_width() / 2, bar.get_height() + sd),
                    ha="center", va="bottom", fontsize=8)
    ax.set_ylim(0, max(m + s for m, s in zip(means, sds)) * 1.22)
    ax.set_ylabel("Steady-state power draw (W)")
    ax.set_title("Long-Term Average Power Consumption per Locomotion Mode")
    fig.text(0.5, 0.01, "Power = |current_A| x 7.2V; transition windows excluded per segment\n"
              "(2.92s/1.56s; no calibrated window for X, full segment used)",
              ha="center", fontsize=7, color="#555555")
    fig.tight_layout(rect=(0.02, 0.09, 0.98, 1))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)

    return {"n_by_mode": dict(zip(modes, ns)), "mean_by_mode": dict(zip(modes, means)),
            "sd_by_mode": dict(zip(modes, sds)), "segments": segments}


if __name__ == "__main__":
    stats = build("experiments/real", "experiments/R2-04-mode-energy/output/FigReal_ModeSteadyStateEnergy.png")
    print("N per mode:", stats["n_by_mode"])
    print("Mean power (W):", {k: round(v, 3) for k, v in stats["mean_by_mode"].items()})
    print("SD (W):", {k: round(v, 3) for k, v in stats["sd_by_mode"].items()})
