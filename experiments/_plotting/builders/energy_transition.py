"""Builder for FigReal_Morphological_Transition_Energy.png.

ROUND 2 (2026-08-27) -- REPLACES the round-1 single-inferred-peak approach entirely, per a critical
finding: the `mode` column in Test_current_integrated_*/neural_metrics.csv never changes (always
'C') across all 5 recordings, so it cannot locate real transitions or validate the round-1 figure's
premise. The author supplied the ACTUAL mode-transition-detection logic used by the original
(lost) plotting script: `robot_cmd` carries structural mode-transition commands mixed in with
directional teleop keys -- filtering `robot_cmd` to {'c','z','x'} (Quadrupedal/Differential
Mobile/Omnidirectional) and diffing consecutive values locates real transition events; a
pre-calibrated mechanical-coupling window then gets integrated for energy. The window durations
(2.92s for a "->z" transition i.e. Quadrupedal->Differential, 1.56s for "->c" i.e. Differential
->Quadrupedal) are the SAME values already published in FigReal_Terrain_Latencies_4Panels's
caption (panels C/D) -- confirms this is the original methodology, not a new invention.

Real transition counts found across the 5 Test_current_integrated_* files (robot_cmd diffed,
first-row starts excluded): 16x Quadrupedal->Differential ("c"->"z"), 19x Differential->Quadrupedal
("z"->"c"), 1x Quadrupedal->Omnidirectional ("c"->"x", too few for statistics, EXCLUDED -- no
pre-calibrated window duration was supplied for it either). N=16/19 is a real, adequate sample for
a mean+-SD bar chart, unlike round 1's single inferred peak.

ROUND 3 (2026-08-27) -- power_W CALIBRATION CAVEAT RESOLVED, per the author (confirmed by their
hardware team): `current_A` is a trustworthy real ampere reading; `voltage_V` is NOT (that column
is what produced the implausible ~1e-4 W figures) -- the platform runs on a fixed 7.2V NiMH pack
(3300 mAh), so power is derived as `abs(current_A) * 7.2` instead of using the logged `power_W`/
`voltage_V` columns at all. Sanity check: this gives 0.28-5.9 W over the observed current range
(0.04-0.82 A), consistent with a small legged robot's servo draw (idle to active movement) --
physically plausible, unlike the raw `power_W` column's ~1e-4 W. Energy is now reported in real
Joules, no longer flagged as uncalibrated.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import COLOR_BLUE, COLOR_ORANGE, DPI  # noqa: E402

TEST_DIRS = [
    "Test_current_integrated_floor_t01", "Test_current_integrated_ramp_t01",
    "Test_current_integrated_ramp_t02", "Test_current_integrated_static_t01",
    "Test_current_integrated_t01",
]
# command -> (mode name, window duration in seconds) -- durations match
# FigReal_Terrain_Latencies_4Panels's published panels C/D exactly (author-supplied).
WINDOW_S = {"z": 2.92, "c": 1.56}  # 'x' excluded: N=1, no calibrated window supplied
DIRECTION_LABEL = {("c", "z"): "Quadrupedal -> Differential Mobile",
                    ("z", "c"): "Differential Mobile -> Quadrupedal"}


def find_transitions(real_root: str) -> list[dict]:
    """Returns one dict per real structural-command transition: trial, t_start (absolute time_s),
    prev/curr command, direction label, window duration."""
    events = []
    for d in TEST_DIRS:
        path = os.path.join(real_root, d, "imu_ina.csv")
        df = pd.read_csv(path)
        struct = df[df["robot_cmd"].isin(["c", "z", "x"])].copy()
        struct["prev"] = struct["robot_cmd"].shift(1)
        trans = struct[(struct["robot_cmd"] != struct["prev"]) & (struct["prev"].notna())]
        for _, row in trans.iterrows():
            prev, curr = row["prev"], row["robot_cmd"]
            if curr not in WINDOW_S:
                continue  # excludes ->x (no calibrated window, N=1)
            events.append({
                "trial": d, "t_start": float(row["time_s"]), "prev": prev, "curr": curr,
                "direction": DIRECTION_LABEL.get((prev, curr), f"{prev}->{curr}"),
                "window_s": WINDOW_S[curr],
            })
    return events


NOMINAL_VOLTAGE_V = 7.2  # fixed NiMH pack (3300 mAh), confirmed by the author's hardware team --
                          # NOT the logged voltage_V column, which is what produced implausible
                          # power_W values in rounds 1-2 (see module docstring).


def integrate_energy(real_root: str, event: dict) -> float:
    """Trapezoidal integral of power = |current_A| * NOMINAL_VOLTAGE_V over
    [t_start, t_start+window_s] for one trial. Real Joules, not the logged (broken) power_W/
    voltage_V columns."""
    df = pd.read_csv(os.path.join(real_root, event["trial"], "imu_ina.csv"))
    mask = (df["time_s"] >= event["t_start"]) & (df["time_s"] <= event["t_start"] + event["window_s"])
    window = df.loc[mask].sort_values("time_s")
    if len(window) < 2:
        return float("nan")
    t = window["time_s"].values
    p = window["current_A"].abs().values * NOMINAL_VOLTAGE_V  # Watts
    return float(np.trapezoid(p, t))  # Joules


def build(real_root: str, output_path: str) -> dict:
    events = find_transitions(real_root)
    for e in events:
        e["energy_J_uncalibrated"] = integrate_energy(real_root, e)

    by_direction = {"Quadrupedal -> Differential Mobile": [], "Differential Mobile -> Quadrupedal": []}
    for e in events:
        if e["direction"] in by_direction and not np.isnan(e["energy_J_uncalibrated"]):
            by_direction[e["direction"]].append(e["energy_J_uncalibrated"])

    labels = ["Quadrupedal $\\to$\nDifferential Mobile", "Differential Mobile\n$\\to$ Quadrupedal"]
    means = [np.mean(v) for v in by_direction.values()]
    sds = [np.std(v) for v in by_direction.values()]
    ns = [len(v) for v in by_direction.values()]

    fig, ax = plt.subplots(figsize=(6, 5))
    colors = [COLOR_BLUE, COLOR_ORANGE]
    bars = ax.bar(labels, means, yerr=sds, capsize=5, color=colors, width=0.5)
    for i, (bar, n) in enumerate(zip(bars, ns)):
        ax.annotate(f"N={n}", xy=(bar.get_x() + bar.get_width() / 2, means[i] + sds[i]),
                    ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("Transition Energy (J)")
    ax.set_title("Morphological Transition Energy per Direction")
    fig.text(0.5, 0.01, "Power = |current_A| x 7.2V (fixed NiMH pack voltage); N = real detected"
              " robot_cmd transitions, not an inferred peak", ha="center", fontsize=7, color="#555555")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)

    return {"n_events_total": len(events), "by_direction_n": ns, "by_direction_mean": means,
            "by_direction_sd": sds, "excluded_c_to_x": sum(1 for e in events if e["curr"] == "x")}


if __name__ == "__main__":
    stats = build("experiments/real", "experiments/N-02-physical-figure-regeneration/output/FigReal_Morphological_Transition_Energy.png")
    print(stats)
