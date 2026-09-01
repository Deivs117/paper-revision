"""Timelines modales Neural vs. FSM — Familia B (compleja) y Familia E (inspección),
`R2-02_fsm_baseline_reference.md` §8.1: "el contraste visual entre la riqueza adaptativa del
neural y el bloqueo en X de la FSM es el argumento más directo".

Un trial representativo por sistema (el primero encontrado, sin selección manual para evitar
cherry-picking) — grafica el modo activo (C/H/X) como función escalonada del tiempo, leído
directamente de la columna `mode` de `metrics_raw.csv`.

R2-02-specific — vive en `experiments/R2-02-fsm-baseline/scripts/`, no en la librería compartida.
"""
from __future__ import annotations

import glob
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

_PLOTTING = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "_plotting")
sys.path.insert(0, _PLOTTING)
from style import DPI  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
EXP_ROOT = os.path.dirname(os.path.dirname(HERE))

MODE_ORDER = ["C", "H", "X"]  # fixed y-axis order, same across all panels
MODE_COLOR = "#4B0082"

FAMILIES = [
    ("Complex", "familia_b_compleja_fsm", "simulation/familia_b_compleja"),
    ("Inspection", "familia_e_inspeccion_fsm", "R3-05-inspection/data"),
]


def _first_trial_dir(family_dir: str) -> str:
    dirs = sorted(glob.glob(os.path.join(family_dir, "test_*")))
    if not dirs:
        raise RuntimeError(f"No trial dirs found in {family_dir}")
    return dirs[0]


def _verdict_word(trial_dir: str) -> str:
    """Human-readable outcome word from the trial dir name, without exposing the raw
    test_NNN_<VERDICT> folder name itself (README.md §11.1)."""
    name = os.path.basename(trial_dir)
    if name.endswith("_SUCCESS"):
        return "successful trial"
    if "FAILURE" in name:
        return "failed trial (" + name.split("FAILURE_", 1)[1].lower().replace("_", " ") + ")"
    return "trial"


def _plot_mode_step(ax, trial_dir: str, label: str) -> None:
    df = pd.read_csv(os.path.join(trial_dir, "metrics_raw.csv"))
    t = df["sim_time_s"] - df["sim_time_s"].iloc[0]
    y = df["mode"].map(lambda m: MODE_ORDER.index(m) if m in MODE_ORDER else None)
    ax.step(t, y, where="post", color=MODE_COLOR, linewidth=1.3)
    ax.set_yticks(range(len(MODE_ORDER)))
    ax.set_yticklabels(MODE_ORDER)
    ax.set_ylim(-0.3, len(MODE_ORDER) - 0.7)
    ax.set_title(f"{label} (representative {_verdict_word(trial_dir)})", fontsize=9)


def build(data_root: str, output_dir: str) -> dict[str, str]:
    os.makedirs(output_dir, exist_ok=True)
    written = {}
    for label, fsm_dir, neural_dir in FAMILIES:
        neural_trial = _first_trial_dir(os.path.join(EXP_ROOT, neural_dir))
        fsm_trial = _first_trial_dir(os.path.join(data_root, fsm_dir))

        fig, (ax_n, ax_f) = plt.subplots(2, 1, figsize=(9, 5), sharex=False)
        _plot_mode_step(ax_n, neural_trial, "Neural")
        _plot_mode_step(ax_f, fsm_trial, "FSM")
        ax_f.set_xlabel("Experimental Time (s)")
        fig.suptitle(f"{label} — Active Gait Mode Over Time", fontsize=11, y=0.98)
        fig.tight_layout()
        fig.subplots_adjust(top=0.88)

        out_path = os.path.join(output_dir, f"fig_mode_timeline_{label.lower()}.png")
        fig.savefig(out_path, dpi=DPI)
        plt.close(fig)
        written[label] = out_path
    return written


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--data-root", default="experiments/R2-02-fsm-baseline/data")
    p.add_argument("--output-dir", default="experiments/R2-02-fsm-baseline/output")
    args = p.parse_args()

    out = build(args.data_root, args.output_dir)
    for label, path in out.items():
        print(f"[mode_timelines] wrote {label} -> {path}")
