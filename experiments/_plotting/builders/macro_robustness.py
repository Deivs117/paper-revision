"""Builder for the noise-robustness family: fig1_Appetitive/Aversive/Obstacle/Complex_macro.png,
now fused into a single 4x3 grid per Informe 1 F-02 / Informe 2 decision D-9.

Three columns per scenario, one row per scenario:
  (1) Mission Time T_sim (s) vs. Sensory Noise Index (sigma)
  (2) Pitch RMS (deg) vs. sigma
  (3) Decision Latency (ms) vs. sigma

Also resolves F-Data-01 (Informe 2): for familia_a_obstaculo, `trial_summary.json.exp_latency` is a
`-1.0` sentinel (never populated) — this builder falls back to the mean of `metrics_raw.csv`'s
`latency_s` column for that scenario only (decision D-4), matching what the currently-published
figure actually shows.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loaders import load_metrics_raw, load_trial_summaries, list_trial_dirs  # noqa: E402
from style import SCENARIO_COLORS, DPI  # noqa: E402

# scenario -> (family_dir_name, uses_metrics_raw_latency_fallback)
SCENARIOS = [
    ("Appetitive", "familia_a_apetitivo", False),
    ("Aversive", "familia_a_aversivo", False),
    ("Obstacle", "familia_a_obstaculo", True),  # F-Data-01 fix
    ("Complex", "familia_b_compleja", False),
]


def _obstacle_latency_fallback(family_dir: str) -> dict[int, list[float]]:
    """Per-noise-level list of mean-latency-per-trial, read from metrics_raw.csv.

    CORRECTION to Informe 2's original F-Data-01 (2026-08-27): the original diagnosis assumed
    metrics_raw.csv's latency_s column was populated for familia_a_obstaculo when
    trial_summary.json's exp_latency was not. Running this builder against the real data shows
    that assumption was wrong -- metrics_raw.csv's latency_s is ALSO empty for all 15 Obstacle
    trials (0/15 rows have a value, verified directly, not just in trial_summary.json). There is
    currently NO recorded latency source for this scenario in experiments/simulation/ at all. The
    published fig1_Obstacle_macro.png panel C (which Informe 1 describes as showing normal latency
    values) therefore could not have been generated from this exact dataset. This function now
    returns an empty dict on purpose; build_grid() renders an explicit "no data" annotation instead
    of silently plotting zeros. See this experiment's README.md for the corrected action item.
    """
    import json

    out: dict[int, list[float]] = {}
    for d in list_trial_dirs(family_dir, verdict="SUCCESS"):
        with open(os.path.join(d, "trial_summary.json")) as f:
            noise = json.load(f)["seed_info"]["noise_level_idx"]
        raw = load_metrics_raw(d)
        vals = raw["latency_s"].dropna()
        vals = vals[vals >= 0]
        if len(vals):
            out.setdefault(noise, []).append(float(vals.mean()) * 1000.0)  # -> ms
    return out


def collect_scenario(scenario: str, family_dir: str, latency_fallback: bool) -> dict:
    """Per-noise-level mean/sd for T_sim, pitch_rms, and latency (ms)."""
    df = load_trial_summaries(family_dir, verdict="SUCCESS")
    if df.empty:
        raise RuntimeError(f"No SUCCESS trials found in {family_dir}")

    noise_levels = sorted(df["noise_level_idx"].dropna().unique().astype(int))
    result = {"noise_levels": noise_levels, "T_sim": [], "T_sim_sd": [],
              "pitch": [], "pitch_sd": [], "latency": [], "latency_sd": []}

    latency_by_noise = _obstacle_latency_fallback(family_dir) if latency_fallback else None

    for n in noise_levels:
        sub = df[df["noise_level_idx"] == n]
        result["T_sim"].append(sub["sim_time_s"].mean())
        result["T_sim_sd"].append(sub["sim_time_s"].std(ddof=0) if len(sub) > 1 else 0.0)
        result["pitch"].append(sub["pitch_rms"].mean())
        result["pitch_sd"].append(sub["pitch_rms"].std(ddof=0) if len(sub) > 1 else 0.0)

        if latency_fallback:
            vals = latency_by_noise.get(n, [])
            result["latency"].append(np.mean(vals) if vals else np.nan)
            result["latency_sd"].append(np.std(vals) if len(vals) > 1 else 0.0)
        else:
            lat = sub["exp_latency"].dropna()
            lat = lat[lat >= 0]
            result["latency"].append(lat.mean() * 1000.0 if len(lat) else np.nan)
            result["latency_sd"].append(lat.std(ddof=0) * 1000.0 if len(lat) > 1 else 0.0)

    return result


def build_grid(simulation_root: str, output_path: str) -> dict:
    """Builds the fused 4x3 grid and writes it to output_path. Returns the raw per-scenario data
    (useful for also regenerating tab:consolidated_simulation_metrics from the same pass)."""
    fig, axes = plt.subplots(4, 3, figsize=(10, 11), sharex=True)
    col_titles = ["Mission Time $T_{sim}$ (s)", "Pitch RMS (deg)", "Decision Latency (ms)"]
    all_data = {}

    for row, (scenario, family_name, latency_fallback) in enumerate(SCENARIOS):
        family_dir = os.path.join(simulation_root, family_name)
        data = collect_scenario(scenario, family_dir, latency_fallback)
        all_data[scenario] = data
        color = SCENARIO_COLORS[scenario]
        x = data["noise_levels"]

        series = [
            (data["T_sim"], data["T_sim_sd"]),
            (data["pitch"], data["pitch_sd"]),
            (data["latency"], data["latency_sd"]),
        ]
        for col, (y, sd) in enumerate(series):
            ax = axes[row, col]
            if col == 2 and all(v != v for v in y):  # all-NaN latency (F-Data-01 correction)
                ax.text(0.5, 0.5, "No latency data recorded\nin this run (see README.md)",
                        ha="center", va="center", fontsize=7, color="gray", transform=ax.transAxes)
                ax.set_xticks(x)
            else:
                ax.errorbar(x, y, yerr=sd, marker="o", color=color, capsize=3, linewidth=1.5)
            if row == 0:
                ax.set_title(col_titles[col])
            if row == 3:
                ax.set_xlabel(r"Sensory Noise Index ($\sigma$)")
            if col == 1:
                ax.set_ylim(0, max(4.0, ax.get_ylim()[1]))
        axes[row, 0].set_ylabel(scenario, fontsize=10, fontweight="bold")

    fig.suptitle("Noise-Robustness Battery — 4 Scenarios x 3 Metrics (simulation, N=15 trials/scenario)",
                 fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)
    return all_data


def build_consolidated_table(simulation_root: str) -> "pd.DataFrame":  # noqa: F821
    """Recomputes tab:consolidated_simulation_metrics (Success %, T_sim, Roll, Pitch) per scenario,
    for cross-checking the currently-published table against the raw data."""
    import pandas as pd

    rows = []
    for scenario, family_name, _ in SCENARIOS:
        family_dir = os.path.join(simulation_root, family_name)
        all_trials = load_trial_summaries(family_dir, verdict=None)
        success = load_trial_summaries(family_dir, verdict="SUCCESS")
        # count distinct trial_index values attempted, vs. how many ended SUCCESS
        n_attempted = all_trials["trial_dir"].apply(lambda s: s.split("_SUCCESS")[0].split("_FAILURE")[0]).nunique() if not all_trials.empty else 0
        rows.append({
            "Suite": scenario,
            "Success %": 100.0 * len(success) / n_attempted if n_attempted else float("nan"),
            "T_sim (s) mean": success["sim_time_s"].mean(),
            "T_sim (s) sd": success["sim_time_s"].std(ddof=0),
            "Roll (deg) mean": success["roll_rms"].mean(),
            "Roll (deg) sd": success["roll_rms"].std(ddof=0),
            "Pitch (deg) mean": success["pitch_rms"].mean(),
            "Pitch (deg) sd": success["pitch_rms"].std(ddof=0),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--simulation-root", default="experiments/simulation")
    p.add_argument("--output", default="experiments/N-01-simulation-figure-regeneration/output/fig1_noise_robustness_grid.png")
    p.add_argument("--table-csv", default="experiments/N-01-simulation-figure-regeneration/output/tab_consolidated_simulation_metrics.csv")
    args = p.parse_args()

    data = build_grid(args.simulation_root, args.output)
    table = build_consolidated_table(args.simulation_root)
    os.makedirs(os.path.dirname(args.table_csv), exist_ok=True)
    table.to_csv(args.table_csv, index=False)
    print(f"Wrote {args.output}")
    print(f"Wrote {args.table_csv}")
    print(table.to_string(index=False))
