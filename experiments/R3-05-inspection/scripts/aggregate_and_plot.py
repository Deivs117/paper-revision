"""R3-05 -- Reactive Inspection Task (Experiment E): aggregate stats + d_final-vs-N_lidar scatter.

Reviewer ask (R3-05, PROGRESS.md / referee #3.5, HIGH): inspection-task metrics (target tracking
accuracy, coverage rate, autonomous re-planning after obstacle blockage). Full diagnosis of what is
and isn't measurable, and why, lives in intake/pending/R3-05_inspection_handoff.md -- this script
only computes the two artifacts the writing plan needs: the aggregate table and the scatter figure.

Data: 20 trials in ../data/ (test_0NN_<VERDICT>/), produced by `familia_e_inspeccion`
(PETER_SIMULATION, branch sam, commit 6d5a2e6 -- see ../README.md for full provenance). 17
SUCCESS, 3 FAILURE_TIMEOUT (trials 7, 11, 17).

Two outputs:
  1. output/inspection_summary_stats.csv -- mean/SD/min/max of d_final_m, N_lidar_events,
     N_mode_X_events, T_acquisition_s, sim_time_s over the 17 successful trials, plus SR.
  2. output/fig_dfinal_vs_nlidar.png -- scatter of the 17 successful trials, N_lidar_events (x)
     vs d_final_m (y), split into "clean" (N_lidar_events < 10) vs "elevated" (>= 10) by marker
     color/shape. The threshold is descriptive, not a fitted boundary: the data itself clusters at
     4-5 (clean) and 11+ (elevated) with no trial in between (see handoff doc §9.3). Purpose: show
     d_final stays flat regardless of path complexity -- the quantitative backbone of the "target
     tracking accuracy is robust to route variability" claim in the new results.tex subsection.
"""
from __future__ import annotations

import csv
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "_plotting"))
from style import DPI, COLOR_BLUE, COLOR_ORANGE  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402  (after matplotlib.use("Agg") in style.py)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "..", "data")
OUTPUT_DIR = os.path.join(HERE, "..", "output")
CLEAN_THRESHOLD = 10  # N_lidar_events < 10 => "clean", >= 10 => "elevated" (see docstring)

METRICS = ["d_final_m", "N_lidar_events", "N_mode_X_events", "T_acquisition_s"]


def load_trials() -> list[dict]:
    trials = []
    for d in sorted(glob.glob(os.path.join(DATA_DIR, "test_*"))):
        insp_path = os.path.join(d, "inspection_summary.json")
        summ_path = os.path.join(d, "trial_summary.json")
        if not (os.path.isfile(insp_path) and os.path.isfile(summ_path)):
            continue
        with open(insp_path) as f:
            insp = json.load(f)
        with open(summ_path) as f:
            summ = json.load(f)
        trials.append({
            "trial": os.path.basename(d),
            "success": bool(insp["success"]),
            "d_final_m": insp.get("d_final_m"),
            "N_lidar_events": insp.get("N_lidar_events"),
            "N_mode_X_events": insp.get("N_mode_X_events"),
            "T_acquisition_s": insp.get("T_acquisition_s"),
            "sim_time_s": summ.get("final_metrics", {}).get("sim_time_s"),
        })
    return trials


def write_stats_csv(trials: list[dict], path: str) -> None:
    successes = [t for t in trials if t["success"]]
    sr = len(successes) / len(trials) if trials else float("nan")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "mean", "sd", "min", "max", "n"])
        w.writerow(["success_rate", round(sr, 4), "", "", "", len(trials)])
        for metric in METRICS + ["sim_time_s"]:
            vals = np.array([t[metric] for t in successes if t[metric] is not None], dtype=float)
            w.writerow([metric, round(vals.mean(), 4), round(vals.std(ddof=1), 4),
                        round(vals.min(), 4), round(vals.max(), 4), len(vals)])


def write_group_stats_csv(trials: list[dict], path: str) -> None:
    """Per-group (clean vs elevated) breakdown of d_final_m -- NOT just the pooled stats above.

    Written because a plain read of the pooled d_final_m SD (0.038) undersells what the scatter
    figure actually shows: the two groups don't just both sit near the pooled mean, the elevated
    group is *tighter* (lower SD, narrower range) than the clean group, despite far messier paths.
    Kept as a committed CSV so this claim is traceable to numbers, not to eyeballing the PNG.
    """
    successes = [t for t in trials if t["success"]]
    groups = {
        "clean (N_lidar_events < 10)": [t for t in successes if t["N_lidar_events"] < CLEAN_THRESHOLD],
        "elevated (N_lidar_events >= 10)": [t for t in successes if t["N_lidar_events"] >= CLEAN_THRESHOLD],
    }
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["group", "n", "d_final_mean", "d_final_sd", "d_final_min", "d_final_max", "d_final_range"])
        for name, group in groups.items():
            vals = np.array([t["d_final_m"] for t in group], dtype=float)
            w.writerow([name, len(vals), round(vals.mean(), 4), round(vals.std(ddof=1), 4),
                        round(vals.min(), 4), round(vals.max(), 4), round(vals.max() - vals.min(), 4)])


def plot_scatter(trials: list[dict], path: str) -> None:
    successes = [t for t in trials if t["success"]]
    clean = [t for t in successes if t["N_lidar_events"] < CLEAN_THRESHOLD]
    elevated = [t for t in successes if t["N_lidar_events"] >= CLEAN_THRESHOLD]

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.scatter([t["N_lidar_events"] for t in clean], [t["d_final_m"] for t in clean],
               color=COLOR_BLUE, marker="o", s=50, label=f"Clean traversal (N < {CLEAN_THRESHOLD}, n={len(clean)})")
    ax.scatter([t["N_lidar_events"] for t in elevated], [t["d_final_m"] for t in elevated],
               color=COLOR_ORANGE, marker="^", s=50, label=f"Elevated evasion (N ≥ {CLEAN_THRESHOLD}, n={len(elevated)})")
    ax.set_xlabel("$N_{lidar\\_events}$ (sensory obstacle-detection transitions)")
    ax.set_ylabel("$d_{final}$ (m)")
    ax.set_title("Approach Precision vs. Path Complexity\n(17 successful trials, Reactive Inspection Task)")
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=DPI)
    plt.close(fig)


if __name__ == "__main__":
    trials = load_trials()
    assert len(trials) == 20, f"expected 20 trials, found {len(trials)}"
    n_success = sum(t["success"] for t in trials)
    print(f"Loaded {len(trials)} trials ({n_success} SUCCESS, {len(trials) - n_success} FAILURE).")

    stats_csv = os.path.join(OUTPUT_DIR, "inspection_summary_stats.csv")
    write_stats_csv(trials, stats_csv)
    print(f"Wrote {stats_csv}")

    group_csv = os.path.join(OUTPUT_DIR, "inspection_group_stats.csv")
    write_group_stats_csv(trials, group_csv)
    print(f"Wrote {group_csv}")

    fig_path = os.path.join(OUTPUT_DIR, "fig_dfinal_vs_nlidar.png")
    plot_scatter(trials, fig_path)
    print(f"Wrote {fig_path}")
