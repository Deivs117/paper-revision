"""Attempts-needed-to-success vs. noise level, Neural vs. FSM, for the 3 single-stimulus families.

Replaces the original build_sr_vs_nl.py's "Success Rate (%)" metric (C-32/C-55,
redundancy_closing_audit_consolidation_2026-09-02.md): every mission in this dataset eventually
succeeds (mission-level SR = 100% at every noise level for all 3 families, both controllers --
see PROGRESS.md C-32), so a per-noise-level "success rate" plot built on raw, non-deduplicated
attempt counts collides with that mission-level 100% reported elsewhere (tab:fsm_comparison,
tab:consolidated_simulation_metrics) under the same name. The underlying finding -- Neural needs
more retries as noise increases, FSM never does -- is real and unaffected; it's just not a
"success rate" in the sense used everywhere else in the paper. This script reports it under its
own name instead: mean number of attempts (original + retries) needed before a mission that was
eventually going to succeed lands, per noise level. A trial_index that succeeds on its first try
counts as 1 attempt; one retried once before landing counts as 2; etc. -- values are always >= 1,
with 1.0 meaning "never needed a retry at that level."

R2-02-specific -- lives in `experiments/R2-02-fsm-baseline/scripts/`, not the shared library.
"""
from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt

_PLOTTING = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "_plotting")
sys.path.insert(0, _PLOTTING)
from loaders import load_trial_summaries  # noqa: E402
from style import DPI  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
EXP_ROOT = os.path.dirname(os.path.dirname(HERE))

FAMILIES = [
    ("Appetitive", "familia_a_apetitivo_fsm", "simulation/familia_a_apetitivo"),
    ("Aversive", "familia_a_aversivo_fsm", "simulation/familia_a_aversivo"),
    ("Obstacle", "familia_a_obstaculo_fsm", "simulation/familia_a_obstaculo"),
]
NEURAL_COLOR = "#0072B2"
FSM_COLOR = "#D55E00"


def _attempts_per_mission_by_noise_level(family_dir: str) -> dict[int, float]:
    """raw attempt count / distinct trial_index count, per noise_level_idx -- see module
    docstring. Every trial_index in this dataset has a SUCCESS row eventually (mission-level
    SR=100%, verified in C-32), so this is well-defined at every level without a separate
    success/failure split."""
    all_trials = load_trial_summaries(family_dir, verdict=None)
    out = {}
    for nl in sorted(all_trials["noise_level_idx"].dropna().unique().astype(int)):
        sub = all_trials[all_trials["noise_level_idx"] == nl]
        n_attempts = len(sub)
        n_missions = sub["trial_dir"].apply(lambda s: s.split("_SUCCESS")[0].split("_FAILURE")[0]).nunique()
        out[nl] = n_attempts / n_missions if n_missions else None
    return out


def build(data_root: str, output_path: str) -> dict:
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
    all_data = {}

    for ax, (label, fsm_dir, neural_dir) in zip(axes, FAMILIES):
        neural_att = _attempts_per_mission_by_noise_level(os.path.join(EXP_ROOT, neural_dir))
        fsm_att = _attempts_per_mission_by_noise_level(os.path.join(data_root, fsm_dir))
        all_data[label] = {"neural": neural_att, "fsm": fsm_att}

        nx = sorted(neural_att)
        fx = sorted(fsm_att)
        # FSM is flat at 1.0 (never retries) for all 3 families at every level -- draw it first
        # (solid) so Neural's dashed line, where it also sits at 1.0 (Obstacle, and Appetitive/
        # Aversive at some levels), is visible on top instead of being hidden underneath.
        neural_style = "--" if label == "Obstacle" else "-"
        ax.plot(fx, [fsm_att[n] for n in fx], marker="s", color=FSM_COLOR, linewidth=3, label="FSM")
        ax.plot(nx, [neural_att[n] for n in nx], marker="o", color=NEURAL_COLOR,
                linestyle=neural_style, label="Neural")
        ax.set_xticks(sorted(set(nx) | set(fx)))
        ax.axhline(1.0, color="0.7", linestyle=":", linewidth=1, zorder=0)
        ax.set_title(label)
        ax.set_xlabel("Noise Level (index)")

    axes[0].set_ylim(0.9, 1.85)
    axes[0].set_ylabel("Attempts needed per completed mission")
    axes[0].legend(loc="upper left", fontsize=9)
    fig.suptitle("Attempts Needed per Mission vs. Noise Level — Neural vs. FSM (single-stimulus families)",
                 fontsize=11)
    fig.tight_layout()
    fig.subplots_adjust(top=0.85)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)
    return all_data


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--data-root", default="experiments/R2-02-fsm-baseline/data")
    p.add_argument("--output", default="experiments/R2-02-fsm-baseline/output/fig_attempts_vs_noise_level.png")
    args = p.parse_args()

    data = build(args.data_root, args.output)
    print(f"Wrote {args.output}")
    for fam, d in data.items():
        print(" ", fam, d)
