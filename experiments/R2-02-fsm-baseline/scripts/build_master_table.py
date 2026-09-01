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

# Terrain families (C1/C2) landed 2026-09-02 — handled separately from FAMILIES because the
# Neural/BG side must be restricted to noise_level_idx==0 (the only genuinely noise-free condition
# in that dataset; the FSM code hardcodes noise off entirely, so its noise_level_idx label is
# vestigial — see data/familia_c_fsm/experiment_c_terrain.md §2-3). n_attempted/n_success for the
# Neural side therefore count only that filtered subset, not the family's full attempt pool.
TERRAIN_FAMILIES = [
    ("Rugged Terrain (C1)", "familia_c_fsm/familia_c1_terreno_rugoso_fsm",
     "R3-04-noise-robustness/data/familia_c1_terreno_rugoso"),
    ("Inclined Slope (C2)", "familia_c_fsm/familia_c2_pendiente_fsm",
     "R3-04-noise-robustness/data/familia_c2_pendiente"),
]
TERRAIN_CAVEAT = (
    "Neural restricted to noise_level_idx=0 (only noise-free condition available; FSM ignores "
    "noise entirely, see experiment_c_terrain.md §2). Neural N is small (C1=6, C2=3 attempts) "
    "vs. FSM's full pool -- verdict-rate differences (e.g. tipover) are not statistically "
    "conclusive at this sample size. Tswitch/Tresponse are NOT shown here: the two codebases use "
    "different Upitch thresholds, tchange offsets, and Tswitch formulas (experiment_c_terrain.md "
    "§1) and are not directly comparable without re-running with matched parameters."
)


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


def collect(family_dir: str, noise_level_idx: int | None = None) -> dict:
    all_trials = load_trial_summaries(family_dir, verdict=None)
    success = load_trial_summaries(family_dir, verdict="SUCCESS")
    if noise_level_idx is not None:
        all_trials = all_trials[all_trials["noise_level_idx"] == noise_level_idx]
        if not success.empty:
            success = success[success["noise_level_idx"] == noise_level_idx]
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
    for label, fsm_dir, neural_dir in TERRAIN_FAMILIES:
        neural = collect(os.path.join(EXP_ROOT, neural_dir), noise_level_idx=0)
        fsm = collect(os.path.join(data_root, fsm_dir))
        for system, stats in [("Neural", neural), ("FSM", fsm)]:
            rows.append({"Family": label, "System": system, "note": TERRAIN_CAVEAT, **stats})

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


def _fmt(m, sd, digits=2):
    if m is None:
        return "—"
    if sd is None:
        return f"{m:.{digits}f}"
    return f"{m:.{digits}f} ± {sd:.{digits}f}"


LAMBDA_NOTE = (
    "λ (whole trial) averages every timestep, including instants with no red/blue conflict "
    "(which count as 1.0 by definition -- see neural_recorder.py::_compute_lambda_efficiency). "
    "λ (conflict only) averages just the timesteps where both stimuli were present "
    "simultaneously, i.e. only the moments the metric is actually meant to characterize. Neither "
    "reproduces the reference doc's earlier-cited 0.982/0.837 exactly -- reported as two "
    "transparent, independently-reproducible aggregations instead. See "
    "intake/pending/R2-02_audit_and_plan.md Pregunta 3."
)


def build_display_table(rows: list[dict], output_path: str) -> list[dict]:
    """Reader-facing version of the master table (2026-09-02 rework, r202_audit_notes: table
    rejected as first drafted). Fixes applied: dropped n_attempted/n_success (Success Rate alone
    is what matters for the comparison -- the raw counts live in table_master_comparison.csv for
    traceability); renamed sim_time -> "Task Completion Time (s)" (a reader-facing description,
    not the raw CSV column name, per README.md §11.1); renamed roll_rms_mean -> "Roll RMS (deg)"
    (no underscore); the two lambda columns are now explicitly labeled "(whole trial)" /
    "(conflict only)" with LAMBDA_NOTE explaining why both exist instead of one unexplained number.
    """
    display_rows = []
    for r in rows:
        display_rows.append({
            "Family": r["Family"], "System": r["System"],
            "Success Rate (%)": f"{r['success_rate']:.1f}" if r.get("success_rate") is not None else "—",
            "Task Completion Time (s)": _fmt(r.get("sim_time_mean"), r.get("sim_time_sd")),
            "Roll RMS (deg)": _fmt(r.get("roll_rms_mean"), r.get("roll_rms_sd"), digits=3),
            "λ (whole trial)": f"{r['lambda_whole_trial_mean']:.3f}" if r.get("lambda_whole_trial_mean") is not None else "—",
            "λ (conflict only)": f"{r['lambda_conflict_only_mean']:.3f}" if r.get("lambda_conflict_only_mean") is not None else "—",
            "Note": r.get("note", ""),
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = ["Family", "System", "Success Rate (%)", "Task Completion Time (s)",
                  "Roll RMS (deg)", "λ (whole trial)", "λ (conflict only)", "Note"]
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(display_rows)
    return display_rows


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

    display_path = args.output.replace(".csv", "_display.csv")
    display_rows = build_display_table(rows, display_path)
    print(f"\nWrote {len(display_rows)} display rows -> {display_path}")
    for r in display_rows:
        print(" ", r)
    print(f"\nLambda note (goes with the display table as a caption/footnote):\n{LAMBDA_NOTE}")
    print(f"\nTerrain caveat (goes with the C1/C2 rows):\n{TERRAIN_CAVEAT}")
