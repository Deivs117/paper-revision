#!/usr/bin/env python3
"""
analyze_ablation.py — R3-01 / R3-02: analisis estadistico del ablation study
sobre el circuito de ganglios basales (STN/GPi/GPe/STR).

Lee los trial_summary.json de las 6 suites en ../data/ (12 replicas c/u,
generadas por PETER_SIMULATION/ros2_ws/src/peter_robot/scripts/test_manager.py)
y calcula:

  1. Tasa de exito por suite (SUCCESS / total) + test exacto de Fisher
     comparando full vs. cada ablation, por escenario.
  2. Medias +/- IC95% de las metricas continuas (lambda de eficiencia de
     conflicto, latencia de decision, Tswitch, roll_rms, pitch_rms) por
     variante, y test de Mann-Whitney U (full vs. cada ablation) por escenario.

No genera graficas ni tablas con formato de publicacion -- eso es un paso
posterior. Salida: output/ablation_stats_summary.json + .csv (legible por
humanos y por cualquier script de graficas/tablas futuro).

Uso:
    python3 analyze_ablation.py
"""

import csv
import json
import math
from pathlib import Path

from scipy import stats

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

# Escenario -> (suite full, {ablation_mode: suite_name})
SCENARIOS = {
    "appetitive": {
        "full": "ablation_appetitive_full",
        "no_lateral_inhibition": "ablation_appetitive_no_lateral_inhibition",
        "threshold_only": "ablation_appetitive_threshold_only",
    },
    "complex": {
        "full": "ablation_complex_full",
        "no_lateral_inhibition": "ablation_complex_no_lateral_inhibition",
        "threshold_only": "ablation_complex_threshold_only",
    },
}

# Metricas continuas de trial_summary.json -> final_metrics a comparar
METRICS = ["exp_lambda", "exp_latency", "tswitch", "roll_rms", "pitch_rms"]


def load_suite(suite_name: str) -> list[dict]:
    suite_dir = DATA_DIR / suite_name
    trials = []
    for trial_dir in sorted(suite_dir.glob("test_*")):
        summary_path = trial_dir / "trial_summary.json"
        if not summary_path.exists():
            continue
        with open(summary_path) as f:
            trials.append(json.load(f))
    return trials


def mean_ci95(values: list[float]) -> tuple[float, float, float]:
    """Media, limite inferior y superior del IC95% (aprox. normal, n pequeno)."""
    n = len(values)
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    mean = sum(values) / n
    if n < 2:
        return (mean, mean, mean)
    var = sum((v - mean) ** 2 for v in values) / (n - 1)
    sd = math.sqrt(var)
    se = sd / math.sqrt(n)
    margin = 1.96 * se
    return (mean, mean - margin, mean + margin)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    summary: dict = {"scenarios": {}}
    csv_rows: list[dict] = []

    for scenario, modes in SCENARIOS.items():
        scenario_out: dict = {"success_rate": {}, "metrics": {}}

        # ---- Cargar trials por modo ----
        trials_by_mode = {mode: load_suite(suite) for mode, suite in modes.items()}

        # ---- Tasa de exito + Fisher exact (full vs. cada ablation) ----
        n_success = {}
        n_total = {}
        for mode, trials in trials_by_mode.items():
            n_total[mode] = len(trials)
            n_success[mode] = sum(1 for t in trials if t["verdict"] == "SUCCESS")
            rate = n_success[mode] / n_total[mode] if n_total[mode] else float("nan")
            scenario_out["success_rate"][mode] = {
                "n_success": n_success[mode],
                "n_total": n_total[mode],
                "rate": round(rate, 4),
            }
            csv_rows.append({
                "scenario": scenario, "mode": mode, "metric": "success_rate",
                "n": n_total[mode], "value": round(rate, 4),
                "ci_low": "", "ci_high": "", "p_value_vs_full": "",
            })

        for mode in ("no_lateral_inhibition", "threshold_only"):
            table = [
                [n_success["full"], n_total["full"] - n_success["full"]],
                [n_success[mode], n_total[mode] - n_success[mode]],
            ]
            _, p = stats.fisher_exact(table)
            scenario_out["success_rate"].setdefault("fisher_exact_vs_full", {})[mode] = round(p, 6)
            for row in csv_rows:
                if row["scenario"] == scenario and row["mode"] == mode and row["metric"] == "success_rate":
                    row["p_value_vs_full"] = round(p, 6)

        # ---- Metricas continuas: media +/- IC95% + Mann-Whitney U ----
        for metric in METRICS:
            metric_out: dict = {}
            values_by_mode = {}
            for mode, trials in trials_by_mode.items():
                vals = [
                    t["final_metrics"][metric]
                    for t in trials
                    if metric in t.get("final_metrics", {}) and t["final_metrics"][metric] is not None
                ]
                values_by_mode[mode] = vals
                mean, lo, hi = mean_ci95(vals)
                metric_out[mode] = {
                    "n": len(vals), "mean": round(mean, 6),
                    "ci95_low": round(lo, 6), "ci95_high": round(hi, 6),
                }
                csv_rows.append({
                    "scenario": scenario, "mode": mode, "metric": metric,
                    "n": len(vals), "value": round(mean, 6),
                    "ci_low": round(lo, 6), "ci_high": round(hi, 6),
                    "p_value_vs_full": "",
                })

            for mode in ("no_lateral_inhibition", "threshold_only"):
                full_vals = values_by_mode["full"]
                mode_vals = values_by_mode[mode]
                if len(full_vals) >= 1 and len(mode_vals) >= 1 and len(set(full_vals + mode_vals)) > 1:
                    try:
                        _, p = stats.mannwhitneyu(full_vals, mode_vals, alternative="two-sided")
                        p = round(float(p), 6)
                    except ValueError:
                        p = None
                else:
                    p = None
                metric_out.setdefault("mannwhitney_vs_full", {})[mode] = p
                for row in csv_rows:
                    if (row["scenario"] == scenario and row["mode"] == mode
                            and row["metric"] == metric):
                        row["p_value_vs_full"] = p

            scenario_out["metrics"][metric] = metric_out

        summary["scenarios"][scenario] = scenario_out

    # ---- Escribir salidas ----
    json_path = OUTPUT_DIR / "ablation_stats_summary.json"
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)

    csv_path = OUTPUT_DIR / "ablation_stats_summary.csv"
    fieldnames = ["scenario", "mode", "metric", "n", "value", "ci_low", "ci_high", "p_value_vs_full"]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"[OK] {json_path}")
    print(f"[OK] {csv_path}")

    # ---- Resumen legible en consola ----
    for scenario, data in summary["scenarios"].items():
        print(f"\n=== {scenario} ===")
        sr = data["success_rate"]
        for mode in ("full", "no_lateral_inhibition", "threshold_only"):
            r = sr[mode]
            print(f"  {mode:24s} success_rate={r['rate']*100:5.1f}% ({r['n_success']}/{r['n_total']})")
        for mode in ("no_lateral_inhibition", "threshold_only"):
            p = sr.get("fisher_exact_vs_full", {}).get(mode)
            print(f"    Fisher exact full vs {mode}: p={p}")
        print("  --- lambda (eficiencia de conflicto) ---")
        lam = data["metrics"]["exp_lambda"]
        for mode in ("full", "no_lateral_inhibition", "threshold_only"):
            m = lam[mode]
            print(f"    {mode:24s} mean={m['mean']:.4f}  IC95=[{m['ci95_low']:.4f}, {m['ci95_high']:.4f}]  n={m['n']}")
        for mode in ("no_lateral_inhibition", "threshold_only"):
            p = lam.get("mannwhitney_vs_full", {}).get(mode)
            print(f"    Mann-Whitney full vs {mode}: p={p}")


if __name__ == "__main__":
    main()
