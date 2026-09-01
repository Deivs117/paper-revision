"""Tabla R1 (tasa de fallo por familia y tipo) y Tabla R2 (parámetros de perturbación por sensor),
`robustez_transferencia_tecnica.md` §11. Ambas son conteos/valores ya tabulados a mano en ese
documento (§10 y §3 respectivamente) — este script solo los regenera de forma reproducible desde
los datos crudos (Tabla R1) y desde `config.yaml` (Tabla R2), en vez de dejarlos solo como
prosa/tablas manuales sin fuente ejecutable.

**Rehecho 2026-09-01** (`r304_audit_notes_2026-09-01.md`):
- Tabla R1 (❌ rechazar/re-hacer — "muchos datos en cero, ¿hay una forma más eficiente?"):
  reemplazada por un gráfico de barras horizontales apiladas (`build_fig_r1_stacked_bar`,
  autor eligió explícitamente "reemplazar" sobre "generar ambas"). El CSV plano
  (`build_table_r1`) se conserva como dato crudo de respaldo, no como la pieza a promover.
- Tabla R2 (⚠ ajustar — "eliminar columna default" + "fila noise seed se puede mencionar en el
  texto"): columna `Default` eliminada; fila `NoiseSeed` eliminada de la tabla (queda solo como
  mención en prosa, fuera del alcance de esta sesión de imágenes/datos).

R3-04-specific (no reusable entre experimentos) — vive en
`experiments/R3-04-noise-robustness/scripts/`, no en `experiments/_plotting/builders/`.
"""
from __future__ import annotations

import csv
import glob
import os

import matplotlib.pyplot as plt

import sys
_PLOTTING = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "_plotting")
sys.path.insert(0, _PLOTTING)
from style import DPI  # noqa: E402

FAMILIES = [
    "familia_a_apetitivo", "familia_a_aversivo", "familia_a_obstaculo",
    "familia_b_compleja", "familia_c1_terreno_rugoso", "familia_c2_pendiente",
]

VERDICTS = ["SUCCESS", "FAILURE_TIMEOUT", "FAILURE_TIPOVER", "FAILURE_CRASH"]


def build_table_r1(data_root: str, output_path: str) -> list[dict]:
    """Conteo literal de intentos por familia y verdict, leído de los nombres de carpeta
    test_NNN_<VERDICT> (incluye TODOS los intentos registrados, no solo los 15 SUCCESS retenidos
    por familia) — mismo criterio que robustez_transferencia_tecnica.md §10's "Verdicts por
    familia (conteo literal de trials, no tasas ni porcentajes)"."""
    rows = []
    for family in FAMILIES:
        family_dir = os.path.join(data_root, family)
        counts = {v: 0 for v in VERDICTS}
        total = 0
        for d in sorted(glob.glob(os.path.join(family_dir, "test_*"))):
            if not os.path.isdir(d):
                # familia_c1_terreno_rugoso has 3 excluded .zip files matching this glob (test_0.zip
                # etc.) — not trial directories. See R3-04_audit_and_plan.md §3d: their internal
                # manifest doesn't match the family's own, excluded from all counts.
                continue
            name = os.path.basename(d)
            total += 1
            matched = False
            for v in VERDICTS:
                if name.endswith(f"_{v}"):
                    counts[v] += 1
                    matched = True
                    break
            if not matched:
                raise RuntimeError(f"Unrecognized verdict suffix in trial dir: {name}")
        row = {"Familia": family, **counts, "Total intentos": total}
        rows.append(row)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Familia", *VERDICTS, "Total intentos"])
        writer.writeheader()
        writer.writerows(rows)
    return rows


VERDICT_COLORS = {
    "SUCCESS": "#009E73", "FAILURE_TIMEOUT": "#E69F00",
    "FAILURE_TIPOVER": "#D55E00", "FAILURE_CRASH": "#CC0000",
}
VERDICT_LABELS = {
    "SUCCESS": "Success", "FAILURE_TIMEOUT": "Failure (timeout)",
    "FAILURE_TIPOVER": "Failure (tipover)", "FAILURE_CRASH": "Failure (crash)",
}
# Human-readable scenario names, not raw folder identifiers — same README.md §11.1 rule already
# applied to the other R3-04 figures this round (fig2_*_micro's dropped suptitle, Fig R3's
# "Successful retry"/"Failed attempt" labels instead of test_NNN_VERDICT).
FAMILY_LABELS = {
    "familia_a_apetitivo": "Appetitive", "familia_a_aversivo": "Aversive",
    "familia_a_obstaculo": "Obstacle", "familia_b_compleja": "Complex",
    "familia_c1_terreno_rugoso": "Rugged Terrain", "familia_c2_pendiente": "Inclined Slope",
}


def build_fig_r1_stacked_bar(rows: list[dict], output_path: str) -> None:
    """Replaces the sparse (mostly-zero) Table R1 with one horizontal stacked bar per family —
    proportional (% of that family's own attempts), so families with a different total attempt
    count (e.g. familia_c1_terreno_rugoso's 27 vs. the rest's 15-21) are still directly comparable
    by width."""
    fig, ax = plt.subplots(figsize=(8, 0.55 * len(rows) + 1.2))
    families = [FAMILY_LABELS.get(r["Familia"], r["Familia"]) for r in rows]
    y = range(len(rows))

    for i, r in enumerate(rows):
        total = r["Total intentos"]
        left = 0.0
        for v in VERDICTS:
            frac = 100.0 * r[v] / total if total else 0.0
            if frac <= 0:
                continue
            bar = ax.barh(i, frac, left=left, color=VERDICT_COLORS[v], edgecolor="white", linewidth=0.5)
            if frac >= 6:  # skip labeling slivers too thin to hold text
                ax.bar_label(bar, labels=[f"{r[v]}"], label_type="center", fontsize=8, color="white")
            left += frac

    ax.set_yticks(list(y))
    ax.set_yticklabels(families, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("% of that family's total attempts (n shown per segment)")
    ax.set_xlim(0, 100)
    handles = [plt.Rectangle((0, 0), 1, 1, color=VERDICT_COLORS[v]) for v in VERDICTS]
    ax.legend(handles, [VERDICT_LABELS[v] for v in VERDICTS], loc="upper center",
              bbox_to_anchor=(0.5, -0.18), ncol=4, fontsize=8, frameon=False)
    ax.set_title("Trial Outcome by Family (all recorded attempts, incl. retries)", fontsize=11)
    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


# Extraído literalmente de experiments/R3-04-noise-robustness/config.yaml / initctes() en
# red_neuronal.py (ver robustez_transferencia_tecnica.md §3 para la tabla completa con
# implementación exacta) — duplicado aquí en vez de parseado desde el YAML porque PyYAML no está
# instalado en experiments/.venv_plotting/ (venv desechable, solo numpy/matplotlib/pandas/pillow);
# si se agrega PyYAML al venv en el futuro, esto puede parsear config.yaml directamente.
# "Default" column dropped (author feedback) — it only ever said "índice 0 -> <value>", redundant
# with the índice-0 entry already visible in "Values" for every row. NoiseSeed row dropped too —
# a single fixed constant (42) is a one-line prose fact, not a per-sensor perturbation parameter,
# so it doesn't belong in a table whose columns are Sensor/Unit/Values.
TABLE_R2_ROWS = [
    {"Parameter": "noise_level_idx", "Sensor": "Compartido (LiDAR + deriva IMU + iluminación)",
     "Unit": "índice entero 0-4", "Values": "0, 1, 2, 3, 4"},
    {"Parameter": "IMUDriftLevels_accel", "Sensor": "IMU", "Unit": "m/s^2 por paso (random-walk)",
     "Values": "0.0, 0.01, 0.03, 0.06, 0.09"},
    {"Parameter": "IMUDriftLevels_angle", "Sensor": "IMU", "Unit": "deg por paso (random-walk)",
     "Values": "0.0, 0.01, 0.04, 0.08, 0.12"},
    {"Parameter": "LidarNoiseLevels", "Sensor": "LiDAR", "Unit": "fracción del rango medido",
     "Values": "0.0, 0.05, 0.10, 0.15, 0.20"},
    {"Parameter": "IllumLevels", "Sensor": "Cámara", "Unit": "severidad adimensional 0-1",
     "Values": "0.0, 0.10, 0.20, 0.30, 0.30"},
    {"Parameter": "AreaIllumLevels", "Sensor": "Cámara (indirecto, umbral stop)",
     "Unit": "unidades de área bounding box", "Values": "28, 24, 20, 18, 14"},
    {"Parameter": "illum_direction", "Sensor": "Cámara", "Unit": "categórico {-1, +1}",
     "Values": "-1 (oscurecida) / +1 (sobreexpuesta)"},
]


def build_table_r2(output_path: str) -> list[dict]:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Parameter", "Sensor", "Unit", "Values"])
        writer.writeheader()
        writer.writerows(TABLE_R2_ROWS)
    return TABLE_R2_ROWS


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--data-root", default="experiments/R3-04-noise-robustness/data")
    p.add_argument("--output-dir", default="experiments/R3-04-noise-robustness/output")
    args = p.parse_args()

    r1 = build_table_r1(args.data_root, os.path.join(args.output_dir, "table_R1_failure_rate.csv"))
    build_fig_r1_stacked_bar(r1, os.path.join(args.output_dir, "fig_R1_failure_by_family.png"))
    r2 = build_table_r2(os.path.join(args.output_dir, "table_R2_perturbation_params.csv"))
    print(f"Table R1 (raw CSV, backup): {len(r1)} rows -> {args.output_dir}/table_R1_failure_rate.csv")
    print(f"Fig R1 (stacked bar, promote this instead): {args.output_dir}/fig_R1_failure_by_family.png")
    for row in r1:
        print(" ", row)
    print(f"Table R2: {len(r2)} rows -> {args.output_dir}/table_R2_perturbation_params.csv")
