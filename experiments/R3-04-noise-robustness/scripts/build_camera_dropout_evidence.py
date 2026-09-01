"""Figura R3 (`robustez_transferencia_tecnica.md` §11 y §2): evidencia directa de que un evento de
dropout de detección de cámara se propaga hasta un fallo de tarea completo.

Datos: `familia_a_apetitivo`, `trial_index=7`, comparando su intento fallido
(`test_007_FAILURE_TIMEOUT`, `noise_level_idx=1`) contra su reintento exitoso con el mismo índice
(`test_007_SUCCESS`) — el mismo par que documenta
`intake/pending/R3-04_audit_and_plan.md` §2 ("Verificación de que la perturbación llega a la
decisión de marcha, no solo al sensor").

Este script es específico de R3-04 (un par de trials puntual, no una función reusable contra
cualquier `--simulation-root`), por eso vive en `experiments/R3-04-noise-robustness/scripts/` y no
en la librería compartida `experiments/_plotting/builders/` — mismo criterio que separa scripts
de un experimento de los builders reusables entre experimentos (ver README.md raíz §9.2).
"""
from __future__ import annotations

import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

_PLOTTING = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "_plotting")
sys.path.insert(0, _PLOTTING)
from style import DPI  # noqa: E402

FAMILY = "familia_a_apetitivo"
FAILED_TRIAL = "test_007_FAILURE_TIMEOUT"
RETRY_TRIAL = "test_007_SUCCESS"


def build(data_root: str, output_path: str) -> None:
    family_dir = os.path.join(data_root, FAMILY)
    failed = pd.read_csv(os.path.join(family_dir, FAILED_TRIAL, "metrics_raw.csv"))
    retry = pd.read_csv(os.path.join(family_dir, RETRY_TRIAL, "metrics_raw.csv"))

    fig, axes = plt.subplots(2, 1, figsize=(8, 5), sharex=False)

    for ax, df, label, verdict_color in [
        (axes[0], failed, f"{FAILED_TRIAL} (FAILURE_TIMEOUT)", "#D55E00"),
        (axes[1], retry, f"{RETRY_TRIAL} (SUCCESS)", "#0072B2"),
    ]:
        t = df["sim_time_s"] - df["sim_time_s"].iloc[0]
        ax.fill_between(t, 0, df["blue_present"], step="mid", color=verdict_color, alpha=0.6)
        ax.set_ylim(-0.1, 1.1)
        ax.set_yticks([0, 1])
        ax.set_ylabel("blue_present")
        frac = df["blue_present"].mean()
        ax.set_title(f"{label} — blue_present_frac ≈ {frac:.2f}", fontsize=10)

    axes[-1].set_xlabel("Experimental Time (s)")
    fig.suptitle("Camera Detection Dropout Propagating to Task Failure\n"
                 f"({FAMILY}, trial_index=7, noise_level_idx=1, both attempts)", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--data-root", default="experiments/R3-04-noise-robustness/data")
    p.add_argument("--output", default="experiments/R3-04-noise-robustness/output/fig_R3_camera_dropout_evidence.png")
    args = p.parse_args()

    build(args.data_root, args.output)
    print(f"Wrote {args.output}")
