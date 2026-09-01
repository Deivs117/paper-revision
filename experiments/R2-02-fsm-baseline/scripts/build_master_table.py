"""Tabla maestra Neural-vs-FSM (`R2-02_fsm_baseline_reference.md` §7.1), recalculada de forma
reproducible desde los datos crudos en vez de vivir solo como Markdown manual.

Reusa `experiments/_plotting/loaders.py` (mismo formato `family_dir/test_NNN[_VERDICT]/
trial_summary.json` que R3-04) — sin necesidad de un loader nuevo.

R2-02-specific (no reusable entre experimentos tal cual, por el mapeo Neural/FSM particular de
esta comparación) — vive en `experiments/R2-02-fsm-baseline/scripts/`, no en
`experiments/_plotting/builders/`.
"""
from __future__ import annotations

import csv
import glob
import json
import os
import sys

_PLOTTING = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "_plotting")
sys.path.insert(0, _PLOTTING)
from loaders import load_trial_summaries  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
EXP_ROOT = os.path.dirname(os.path.dirname(HERE))  # experiments/

# label, fsm_dir (relative to data/), neural_dir (relative to experiments/)
FAMILIES = [
    ("Appetitive", "familia_a_apetitivo_fsm", "simulation/familia_a_apetitivo"),
    ("Aversive", "familia_a_aversivo_fsm", "simulation/familia_a_aversivo"),
    ("Obstacle", "familia_a_obstaculo_fsm", "simulation/familia_a_obstaculo"),
    ("Complex", "familia_b_compleja_fsm", "simulation/familia_b_compleja"),
    ("Inspection", "familia_e_inspeccion_fsm", "R3-05-inspection/data"),
]
PENDING_FAMILIES = ["Rugged Terrain (C1)", "Inclined Slope (C2)"]


def _mean_sd(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None, None
    if len(vals) == 1:
        return vals[0], 0.0
    m = sum(vals) / len(vals)
    var = sum((v - m) ** 2 for v in vals) / len(vals)
    return m, var ** 0.5


def _lambda_both_aggregations(family_dir: str) -> tuple[float | None, float | None]:
    """Returns (mean over the WHOLE trial series, mean over ONLY red&blue-simultaneous rows) of
    lambda_efficiency, pooled across every trial in the family. Reported side by side, per the
    audit finding that neither reproduces the reference doc's cited 0.982/0.837 exactly — see
    intake/pending/R2-02_audit_and_plan.md Pregunta 3. Not every family has red/blue stimuli
    (Obstacle is green-only, Inspection has neither initially) -- conflict rows will be empty
    there, which is expected, not a bug."""
    all_vals, conflict_vals = [], []
    for p in sorted(glob.glob(os.path.join(family_dir, "test_*", "metrics_raw.csv"))):
        with open(p) as f:
            for row in csv.DictReader(f):
                try:
                    le = float(row["lambda_efficiency"])
                except (ValueError, KeyError):
                    continue
                all_vals.append(le)
                try:
                    if float(row.get("red_present", 0)) == 1.0 and float(row.get("blue_present", 0)) == 1.0:
                        conflict_vals.append(le)
                except ValueError:
                    pass
    return _mean_sd(all_vals)[0], (_mean_sd(conflict_vals)[0] if conflict_vals else None)


def collect(family_dir: str) -> dict:
    all_trials = load_trial_summaries(family_dir, verdict=None)
    success = load_trial_summaries(family_dir, verdict="SUCCESS")
    # RAW folder count (every test_NNN_<VERDICT> dir, retries included as separate attempts) —
    # matches R2-02_fsm_baseline_reference.md's own convention (e.g. Aversive Neural "N=17" counts
    # 2 retried slots as 2 attempts, not the 15 distinct trial_index values). A first version of
    # this script deduped by trial_index (nunique(), copied from macro_robustness.py's convention
    # for a different table) and silently inflated success rates for any family with retries —
    # caught by comparing against the reference doc's own N values before trusting this output.
    n_attempted = len(all_trials)
    sim_m, sim_sd = _mean_sd(success["sim_time_s"].tolist()) if not success.empty else (None, None)
    roll_m, roll_sd = _mean_sd(success["roll_rms"].tolist()) if not success.empty else (None, None)
    lam_all, lam_conflict = _lambda_both_aggregations(family_dir)
    return {
        "n_attempted": n_attempted, "n_success": len(success),
        "success_rate": 100.0 * len(success) / n_attempted if n_attempted else None,
        "sim_time_mean": sim_m, "sim_time_sd": sim_sd,
        "roll_rms_mean": roll_m, "roll_rms_sd": roll_sd,
        "lambda_whole_trial_mean": lam_all, "lambda_conflict_only_mean": lam_conflict,
    }


def build(data_root: str, output_path: str) -> list[dict]:
    rows = []
    for label, fsm_dir, neural_dir in FAMILIES:
        neural = collect(os.path.join(EXP_ROOT, neural_dir))
        fsm = collect(os.path.join(data_root, fsm_dir))
        for system, stats in [("Neural", neural), ("FSM", fsm)]:
            rows.append({"Family": label, "System": system, **stats})
    for label in PENDING_FAMILIES:
        rows.append({"Family": label, "System": "FSM", "n_attempted": None, "n_success": None,
                     "success_rate": None, "sim_time_mean": None, "sim_time_sd": None,
                     "roll_rms_mean": None, "roll_rms_sd": None,
                     "lambda_whole_trial_mean": None, "lambda_conflict_only_mean": None,
                     "note": "pending — FSM not yet executed, see R2-02_fsm_baseline_reference.md §9"})

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = ["Family", "System", "n_attempted", "n_success", "success_rate",
                  "sim_time_mean", "sim_time_sd", "roll_rms_mean", "roll_rms_sd",
                  "lambda_whole_trial_mean", "lambda_conflict_only_mean", "note"]
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in fieldnames})
    return rows


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--data-root", default="experiments/R2-02-fsm-baseline/data")
    p.add_argument("--output", default="experiments/R2-02-fsm-baseline/output/table_master_comparison.csv")
    args = p.parse_args()

    rows = build(args.data_root, args.output)
    print(f"Wrote {len(rows)} rows -> {args.output}")
    for r in rows:
        print(" ", {k: v for k, v in r.items() if v is not None})
