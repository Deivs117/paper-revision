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

Two statistics are computed per mode:
  - INTRA-SEGMENT: mean and SD of individual power samples within steady-state segments. For modes
    with multiple segments (C, H), samples from all segments are pooled. This captures moment-to-
    moment power variability during operation and is directly comparable across all three modes
    regardless of how many segments exist.
  - INTER-SEGMENT (C and H only): mean and SD of per-segment means. Reflects between-trial/
    condition variability; not computable for X (single segment). The high CV of C and H in this
    metric (~74-94%) reflects physical-condition heterogeneity across recordings (floor/ramp/static),
    not measurement noise.

CAVEATS (report alongside results, do not silently omit):
  1. Only ONE steady-state Omnidirectional segment exists (floor_t01, 38.6s, N=194 samples).
     Intra-segment statistics are valid; inter-segment replication is not available for X.
  2. C and H inter-segment variance is inflated by mixed physical conditions (floor/ramp/static).
  3. current_A is confirmed trustworthy; voltage/power_W columns are broken and ignored throughout.
  4. "Long-term average" means averaged over available bench recordings, not a multi-hour mission.
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
                "trial": d,
                "mode": MODE_OF_CMD[cmds[i]],
                "mean_power_W": float(power.mean()),
                "sd_power_W": float(power.std(ddof=1)),
                "n_samples": int(len(power)),
                "duration_s": float(t1 - steady_start),
            })
    return segments


def intra_segment_stats(segments: list[dict]) -> dict:
    """Pooled intra-segment statistics per mode.

    Pools all individual power samples across all segments of the same mode.
    Mean is the grand mean; SD is the pooled within-segment SD (not SD of segment means).
    This statistic is homogeneous across modes regardless of how many segments exist.
    """
    by_mode: dict[str, dict] = {m: {"sum": 0.0, "sum_sq": 0.0, "n": 0, "n_segs": 0}
                                 for m in MODE_OF_CMD.values()}
    for s in segments:
        m = s["mode"]
        n = s["n_samples"]
        mu = s["mean_power_W"]
        sd = s["sd_power_W"]
        by_mode[m]["sum"] += mu * n
        by_mode[m]["sum_sq"] += (sd ** 2) * (n - 1) + mu ** 2 * n
        by_mode[m]["n"] += n
        by_mode[m]["n_segs"] += 1

    result = {}
    for m, acc in by_mode.items():
        n_total = acc["n"]
        if n_total < 2:
            result[m] = {"mean": acc["sum"] / max(n_total, 1), "sd": float("nan"),
                         "n_samples": n_total, "n_segments": acc["n_segs"]}
            continue
        grand_mean = acc["sum"] / n_total
        pooled_variance = (acc["sum_sq"] - n_total * grand_mean ** 2) / (n_total - 1)
        result[m] = {
            "mean": grand_mean,
            "sd": float(np.sqrt(max(pooled_variance, 0.0))),
            "n_samples": n_total,
            "n_segments": acc["n_segs"],
        }
    return result


def inter_segment_stats(segments: list[dict]) -> dict:
    """Between-segment statistics per mode (mean and SD of per-segment means)."""
    by_mode: dict[str, list[float]] = {m: [] for m in MODE_OF_CMD.values()}
    for s in segments:
        by_mode[s["mode"]].append(s["mean_power_W"])
    result = {}
    for m, vals in by_mode.items():
        result[m] = {
            "mean": float(np.mean(vals)) if vals else float("nan"),
            "sd": float(np.std(vals, ddof=1)) if len(vals) > 1 else float("nan"),
            "n_segments": len(vals),
        }
    return result


def build(real_root: str, output_path: str) -> dict:
    segments = steady_state_segments(real_root)
    intra = intra_segment_stats(segments)
    inter = inter_segment_stats(segments)

    modes = list(MODE_OF_CMD.values())
    means = [intra[m]["mean"] for m in modes]
    sds = [intra[m]["sd"] if not np.isnan(intra[m]["sd"]) else 0.0 for m in modes]
    ns_segs = [intra[m]["n_segments"] for m in modes]
    ns_samples = [intra[m]["n_samples"] for m in modes]

    fig, ax = plt.subplots(figsize=(7, 5.5))
    colors = [MODE_COLORS[m] for m in modes]
    bars = ax.bar(modes, means, yerr=sds, capsize=5, color=colors, width=0.5)
    for bar, n_seg, n_samp, sd in zip(bars, ns_segs, ns_samples, sds):
        label = f"{n_seg} seg / {n_samp} samples"
        ax.annotate(label, xy=(bar.get_x() + bar.get_width() / 2, bar.get_height() + sd),
                    ha="center", va="bottom", fontsize=7)
    ax.set_ylim(0, max(m + s for m, s in zip(means, sds)) * 1.25)
    ax.set_ylabel("Steady-state power draw (W)")
    ax.set_title("Long-Term Average Power Consumption per Locomotion Mode\n(intra-segment mean ± SD)")
    fig.text(0.5, 0.01,
             "Power = |current_A| × 7.2 V; transition windows excluded (2.92 s / 1.56 s).\n"
             "X: full segment used (no calibrated coupling window). Error bars: pooled within-segment SD.",
             ha="center", fontsize=7, color="#555555")
    fig.tight_layout(rect=(0.02, 0.09, 0.98, 1))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)

    import csv
    csv_path = os.path.join(os.path.dirname(output_path), "mode_energy_stats.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["mode", "intra_mean_W", "intra_sd_W", "intra_n_samples", "n_segments",
                    "inter_mean_W", "inter_sd_W"])
        for m in modes:
            w.writerow([m,
                        round(intra[m]["mean"], 4), round(intra[m]["sd"], 4) if not np.isnan(intra[m]["sd"]) else "",
                        intra[m]["n_samples"], intra[m]["n_segments"],
                        round(inter[m]["mean"], 4), round(inter[m]["sd"], 4) if not np.isnan(inter[m]["sd"]) else ""])

    return {"intra": intra, "inter": inter, "segments": segments}


if __name__ == "__main__":
    stats = build("experiments/real", "experiments/R2-04-mode-energy/output/FigReal_ModeSteadyStateEnergy.png")
    print("\n=== Intra-segment statistics (pooled within-segment samples) ===")
    for m, v in stats["intra"].items():
        print(f"  {m}: mean={v['mean']:.3f} W, SD={v['sd']:.3f} W, "
              f"N_samples={v['n_samples']}, N_segments={v['n_segments']}")
    print("\n=== Inter-segment statistics (between-segment means) ===")
    for m, v in stats["inter"].items():
        print(f"  {m}: mean={v['mean']:.3f} W, SD={v['sd']:.3f} W, N_segments={v['n_segments']}")
