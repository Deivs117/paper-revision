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

**Rehecho 2026-09-01** (`r304_audit_notes_2026-09-01.md`, veredicto ❌ rechazar/re-hacer):
- Un solo panel superpuesto (no dos paneles apilados) — la comparación entre el intento fallido y
  el reintento exitoso se ve de un vistazo, con una leyenda distinguiéndolos, en vez de exigir
  comparar dos ejes por separado.
- Etiquetas humanas, sin nombres técnicos de carpeta (`test_007_FAILURE_TIMEOUT`/`test_007_SUCCESS`
  ya no aparecen en la imagen) — sigue la regla de README.md §11.1 (nunca nombres de archivo/prueba
  crudos en material orientado al lector), la misma que ya motivó quitar la nota superior de las
  figuras `fig2_*_micro` en esta misma ronda de revisión.
- Título pegado al contenido (antes había una franja vacía entre el título y la gráfica).
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

FAILED_LABEL = "Failed attempt (timeout)"
RETRY_LABEL = "Successful retry"
FAILED_COLOR = "#D55E00"
RETRY_COLOR = "#0072B2"


def build(data_root: str, output_path: str) -> None:
    family_dir = os.path.join(data_root, FAMILY)
    failed = pd.read_csv(os.path.join(family_dir, FAILED_TRIAL, "metrics_raw.csv"))
    retry = pd.read_csv(os.path.join(family_dir, RETRY_TRIAL, "metrics_raw.csv"))

    fig, ax = plt.subplots(figsize=(8, 4))

    for df, label, color, frac_zorder in [
        (retry, RETRY_LABEL, RETRY_COLOR, 1),
        (failed, FAILED_LABEL, FAILED_COLOR, 2),
    ]:
        t = df["sim_time_s"] - df["sim_time_s"].iloc[0]
        frac = df["blue_present"].mean()
        ax.fill_between(t, 0, df["blue_present"], step="mid", color=color, alpha=0.45,
                         zorder=frac_zorder, label=f"{label} (target detected {frac:.0%} of the time)")

    ax.set_ylim(-0.05, 1.15)
    ax.set_yticks([0, 1])
    ax.set_ylabel("Target detected")
    ax.set_xlabel("Experimental Time (s)")
    ax.legend(loc="upper right", fontsize=9)
    ax.set_title("Camera Detection Dropout Propagating to Task Failure", fontsize=11, pad=8)
    fig.tight_layout()
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
