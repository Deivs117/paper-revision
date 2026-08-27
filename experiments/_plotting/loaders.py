"""Pure data-loading functions for experiments/_plotting builders.

Isolates all CSV/JSON parsing from the plotting code (see
intake/pending/R02-01_data_traceability_and_plotting_plan.md §3.3, principle 1) — if a column name
changes in a future re-run of the simulation suite, this is the only file that needs to change.

Accepts ANY folder that follows the existing layout (family_dir/test_NNN[_VERDICT]/*.csv|json),
not just the six families currently under experiments/simulation/ — this is what makes the
pipeline reusable against a freshly re-run simulation batch (Tarea 1) without editing code, only
pointing generate_all.py at the new family directory.
"""
from __future__ import annotations

import glob
import json
import os

import pandas as pd


def list_trial_dirs(family_dir: str, verdict: str | None = "SUCCESS") -> list[str]:
    """All test_* subdirectories of a family, optionally filtered by trial_summary.json verdict."""
    dirs = sorted(glob.glob(os.path.join(family_dir, "test_*")))
    if verdict is None:
        return dirs
    out = []
    for d in dirs:
        js = os.path.join(d, "trial_summary.json")
        if not os.path.exists(js):
            continue
        with open(js) as f:
            data = json.load(f)
        if data.get("verdict") == verdict:
            out.append(d)
    return out


def load_trial_summaries(family_dir: str, verdict: str | None = "SUCCESS") -> pd.DataFrame:
    """One row per successful trial: final_metrics + seed_info.noise_level_idx + trial dir name."""
    rows = []
    for d in list_trial_dirs(family_dir, verdict=verdict):
        js = os.path.join(d, "trial_summary.json")
        with open(js) as f:
            data = json.load(f)
        fm = dict(data.get("final_metrics", {}))
        fm["trial_dir"] = os.path.basename(d)
        fm["verdict"] = data.get("verdict")
        fm["noise_level_idx"] = data.get("seed_info", {}).get("noise_level_idx")
        rows.append(fm)
    return pd.DataFrame(rows)


def load_metrics_raw(trial_dir: str) -> pd.DataFrame:
    """Per-timestep neural/kinematic series for one trial (metrics_raw.csv)."""
    path = os.path.join(trial_dir, "metrics_raw.csv")
    return pd.read_csv(path)


def load_stability_log(trial_dir: str) -> pd.DataFrame:
    """Per-timestep stability geometry for one trial (stability_log.csv, only in C1/C2 families)."""
    path = os.path.join(trial_dir, "stability_log.csv")
    return pd.read_csv(path)


def load_stability_log_aligned(trial_dir: str) -> pd.DataFrame:
    """stability_log.csv re-aligned so t=0 is the neural mode-switch instant.

    Resolves F-Data-02 (Informe 2): merges metrics_raw.csv (to locate t_switch = first timestamp
    where the `mode` column changes value) with stability_log.csv (the TR series), per decision D-5.
    Falls back to the raw (unaligned) timestamp if metrics_raw.csv has no mode change (single-mode
    trial) — in that case t_switch defaults to the trial's first timestamp.
    """
    raw = load_metrics_raw(trial_dir)
    t_switch = raw["sim_time_s"].iloc[0]
    if "mode" in raw.columns and raw["mode"].nunique() > 1:
        first_mode = raw["mode"].iloc[0]
        changed = raw[raw["mode"] != first_mode]
        if not changed.empty:
            t_switch = changed["sim_time_s"].iloc[0]

    stab = load_stability_log(trial_dir)
    stab = stab.copy()
    stab["t_aligned"] = stab["timestamp"] - t_switch
    return stab


def load_real_combined(trial_dir: str) -> pd.DataFrame:
    """Per-timestep aggregated series for one physical trial (combined_metrics.csv)."""
    path = os.path.join(trial_dir, "combined_metrics.csv")
    return pd.read_csv(path)


def load_real_neural(trial_dir: str) -> pd.DataFrame:
    """Per-timestep raw neural series for one physical trial (neural_metrics.csv)."""
    path = os.path.join(trial_dir, "neural_metrics.csv")
    return pd.read_csv(path)


def load_vectorized(csv_path: str) -> pd.DataFrame:
    """Load a hand-extracted CSV from experiments/_plotting/vectorized/.

    Same function as any other loader here on purpose (Informe 2 D-11 / §3.2): a vectorized CSV is
    expected to already carry the same column schema a builder would get from a real run, so no
    separate parsing path is needed — the only difference is documented in
    experiments/_plotting/vectorized/README.md, not in code.
    """
    return pd.read_csv(csv_path)
