"""Tabla R1 (tasa de fallo por familia y tipo) y Tabla R2 (parámetros de perturbación por sensor),
`robustez_transferencia_tecnica.md` §11. Ambas son conteos/valores ya tabulados a mano en ese
documento (§10 y §3 respectivamente) — este script solo los regenera de forma reproducible desde
los datos crudos (Tabla R1) y desde `config.yaml` (Tabla R2), en vez de dejarlos solo como
prosa/tablas manuales sin fuente ejecutable.

R3-04-specific (no reusable entre experimentos) — vive en
`experiments/R3-04-noise-robustness/scripts/`, no en `experiments/_plotting/builders/`.
"""
from __future__ import annotations

import csv
import glob
import os

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


# Extraído literalmente de experiments/R3-04-noise-robustness/config.yaml / initctes() en
# red_neuronal.py (ver robustez_transferencia_tecnica.md §3 para la tabla completa con
# implementación exacta) — duplicado aquí en vez de parseado desde el YAML porque PyYAML no está
# instalado en experiments/.venv_plotting/ (venv desechable, solo numpy/matplotlib/pandas/pillow);
# si se agrega PyYAML al venv en el futuro, esto puede parsear config.yaml directamente.
TABLE_R2_ROWS = [
    {"Parameter": "noise_level_idx", "Sensor": "Compartido (LiDAR + deriva IMU + iluminación)",
     "Unit": "índice entero 0-4", "Values": "0, 1, 2, 3, 4", "Default": "0"},
    {"Parameter": "IMUDriftLevels_accel", "Sensor": "IMU", "Unit": "m/s^2 por paso (random-walk)",
     "Values": "0.0, 0.01, 0.03, 0.06, 0.09", "Default": "índice 0 -> 0.0"},
    {"Parameter": "IMUDriftLevels_angle", "Sensor": "IMU", "Unit": "deg por paso (random-walk)",
     "Values": "0.0, 0.01, 0.04, 0.08, 0.12", "Default": "índice 0 -> 0.0"},
    {"Parameter": "LidarNoiseLevels", "Sensor": "LiDAR", "Unit": "fracción del rango medido",
     "Values": "0.0, 0.05, 0.10, 0.15, 0.20", "Default": "índice 0 -> 0.0"},
    {"Parameter": "IllumLevels", "Sensor": "Cámara", "Unit": "severidad adimensional 0-1",
     "Values": "0.0, 0.10, 0.20, 0.30, 0.30", "Default": "índice 0 -> 0.0"},
    {"Parameter": "AreaIllumLevels", "Sensor": "Cámara (indirecto, umbral stop)",
     "Unit": "unidades de área bounding box", "Values": "28, 24, 20, 18, 14", "Default": "índice 0 -> 28"},
    {"Parameter": "illum_direction", "Sensor": "Cámara", "Unit": "categórico {-1, +1}",
     "Values": "-1 (oscurecida) / +1 (sobreexpuesta)", "Default": "-1"},
    {"Parameter": "NoiseSeed", "Sensor": "Todos (RNG)", "Unit": "entero",
     "Values": "42 (fijo)", "Default": "42"},
]


def build_table_r2(output_path: str) -> list[dict]:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Parameter", "Sensor", "Unit", "Values", "Default"])
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
    r2 = build_table_r2(os.path.join(args.output_dir, "table_R2_perturbation_params.csv"))
    print(f"Table R1: {len(r1)} rows -> {args.output_dir}/table_R1_failure_rate.csv")
    for row in r1:
        print(" ", row)
    print(f"Table R2: {len(r2)} rows -> {args.output_dir}/table_R2_perturbation_params.csv")
