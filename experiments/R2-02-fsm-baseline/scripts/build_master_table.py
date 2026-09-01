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


def _lambda_whole_trial(family_dir: str) -> float | None:
    """Mean of lambda_efficiency over every timestep of every trial in the family. Kept as a
    general efficiency indicator only -- NOT the conflict-resolution argument (see CONFLICT_NOTE
    for why a lambda-based conflict metric doesn't work, per the team's 2026-09-02 diagnosis)."""
    all_vals = []
    for p in sorted(glob.glob(os.path.join(family_dir, "test_*", "metrics_raw.csv"))):
        with open(p) as f:
            for row in csv.DictReader(f):
                try:
                    all_vals.append(float(row["lambda_efficiency"]))
                except (ValueError, KeyError):
                    continue
    return _mean_sd(all_vals)[0]


def _conflict_exposure(family_dir: str) -> tuple[float | None, float | None]:
    """Returns (mean % of trial time spent with red+blue simultaneously present, mean seconds of
    that per trial), averaged per-trial (not pooled) so trials of different length weigh equally.

    Replaces the earlier lambda-based "conflict" metric per the team's 2026-09-02 diagnosis (see
    CONFLICT_NOTE): the cited 0.982/0.837 lambda figures in R2-02_fsm_baseline_reference.md §5.2
    were confirmed a documentation error, not reproducible from any aggregation, and the
    conflict-only lambda mean is itself uninformative (cmd_mag / ||neural activity|| mixes
    incompatible scales and is small by construction, not because of worse decisions). Conflict
    EXPOSURE -- how long each system stays in unresolved simultaneous-stimulus conflict, timed
    from sim_time_s deltas rather than assumed row cadence -- is what the team confirmed is the
    real, reproducible driver of the Family B outcome gap."""
    fracs, secs = [], []
    for p in sorted(glob.glob(os.path.join(family_dir, "test_*", "metrics_raw.csv"))):
        with open(p) as f:
            rows = list(csv.DictReader(f))
        if not rows or "red_present" not in rows[0]:
            continue
        times = [float(r["sim_time_s"]) for r in rows]
        total = times[-1] - times[0] if len(times) > 1 else 0.0
        if total <= 0:
            continue
        conflict_t = 0.0
        for i in range(1, len(rows)):
            dt = times[i] - times[i - 1]
            prev = rows[i - 1]
            if float(prev.get("red_present", 0)) == 1.0 and float(prev.get("blue_present", 0)) == 1.0:
                conflict_t += dt
        fracs.append(100.0 * conflict_t / total)
        secs.append(conflict_t)
    if not fracs:
        return None, None
    return _mean_sd(fracs)[0], _mean_sd(secs)[0]


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
    lam_all = _lambda_whole_trial(family_dir)
    exposure_pct, exposure_s = _conflict_exposure(family_dir)
    return {
        "n_attempted": n_attempted, "n_success": len(success),
        "success_rate": 100.0 * len(success) / n_attempted if n_attempted else None,
        "sim_time_mean": sim_m, "sim_time_sd": sim_sd,
        "roll_rms_mean": roll_m, "roll_rms_sd": roll_sd,
        "lambda_whole_trial_mean": lam_all,
        "conflict_exposure_pct": exposure_pct, "conflict_exposure_s": exposure_s,
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
                  "lambda_whole_trial_mean", "conflict_exposure_pct", "conflict_exposure_s", "note"]
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


CONFLICT_NOTE = (
    "2026-09-02, resolved by the team (see intake/pending/R2-02_audit_and_plan.md Pregunta 3): "
    "the '0.982 Neural / 0.837 FSM' lambda-efficiency figures cited in "
    "R2-02_fsm_baseline_reference.md §5.2 were confirmed a documentation error from an earlier "
    "session, not reproducible from metrics_raw.csv under any aggregation the team tried "
    "(final-value, whole-trial pooled/per-trial, conflict-only pooled/per-trial). The "
    "conflict-only lambda mean is itself not a valid metric here -- its formula "
    "(cmd_mag / ||neural activity||) mixes incompatible scales (m/s vs. a raw activity-vector "
    "norm) and is small by construction, not because either system makes worse decisions. "
    "REMOVED from this table and from the paper. The reproducible, meaningful number is "
    "conflict EXPOSURE below -- how long each system spends in genuine simultaneous-stimulus "
    "conflict (both red_present and blue_present) before resolving it, computed here from exact "
    "sim_time_s deltas rather than an assumed row cadence. For Family B: Neural ~0.2s/trial vs. "
    "FSM ~6.1s/trial -- seconds/trial match the team's own estimate exactly. The % of trial time "
    "figures (1.7% Neural / 4.7% FSM here vs. the team's quick estimate of 1.1%/4.3%) differ "
    "slightly because of how 'total trial time' is defined (exact elapsed sim_time_s span here "
    "vs. a row-count-based estimate there) -- both agree FSM stays unresolved roughly 3x longer "
    "as a fraction of its own trial, and ~30x longer in absolute seconds. Only meaningful where a "
    "family actually has simultaneous red+blue stimuli (Complex) -- '—' elsewhere is expected, "
    "not missing data."
)


def build_display_table(rows: list[dict], output_path: str) -> list[dict]:
    """Reader-facing version of the master table (2026-09-02 rework, r202_audit_notes 3 rondas):
    ronda 1 rejected the first draft outright; ronda 2 dropped the "Note" column (caveats belong
    in prose/README, not the LaTeX-facing table) and the lambda-conflict-only column, replaced by
    Conflict Exposure once the team confirmed lambda-conflict-only was invalid -- see
    CONFLICT_NOTE. **Ronda 3:** Conflict Exposure itself dropped from the table too -- author
    feedback was that two columns that read "0.0" for 5 of 7 families (only Complex has real
    red+blue conflict) are visual clutter/inefficient for a LaTeX table; the two numbers (Neural
    ~0.2s/trial, FSM ~6.1s/trial) belong in the write-up's prose instead, not as table columns --
    see CONFLICT_NOTE, which still carries them for the writing session. Also: dropped
    n_attempted/n_success (Success Rate alone is what matters here -- raw counts live in
    table_master_comparison.csv for traceability); renamed sim_time -> "Task Completion Time (s)"
    (reader-facing, not the raw CSV column name, per README.md §11.1); renamed roll_rms_mean ->
    "Roll RMS (deg)" (no underscore).
    """
    display_rows = []
    for r in rows:
        display_rows.append({
            "Family": r["Family"], "System": r["System"],
            "Success Rate (%)": f"{r['success_rate']:.1f}" if r.get("success_rate") is not None else "—",
            "Task Completion Time (s)": _fmt(r.get("sim_time_mean"), r.get("sim_time_sd")),
            "Roll RMS (deg)": _fmt(r.get("roll_rms_mean"), r.get("roll_rms_sd"), digits=3),
            "λ (whole trial)": f"{r['lambda_whole_trial_mean']:.3f}" if r.get("lambda_whole_trial_mean") is not None else "—",
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = ["Family", "System", "Success Rate (%)", "Task Completion Time (s)",
                  "Roll RMS (deg)", "λ (whole trial)"]
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
    print(f"\nConflict exposure note (prose for the writing session, not the LaTeX table):\n{CONFLICT_NOTE}")
    print(f"\nTerrain caveat (prose for the writing session, not the LaTeX table):\n{TERRAIN_CAVEAT}")
