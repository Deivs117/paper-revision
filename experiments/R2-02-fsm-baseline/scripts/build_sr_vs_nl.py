"""Tasa de éxito (SR) vs. nivel de ruido, Neural vs. FSM, para las 3 familias de estímulo único
(`R2-02_fsm_baseline_reference.md` §8.1, "Gráfica SR vs NL para Familias A").

R2-02-specific — vive en `experiments/R2-02-fsm-baseline/scripts/`, no en la librería compartida.
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


def _sr_by_noise_level(family_dir: str) -> dict[int, float]:
    all_trials = load_trial_summaries(family_dir, verdict=None)
    success = load_trial_summaries(family_dir, verdict="SUCCESS")
    out = {}
    for nl in sorted(all_trials["noise_level_idx"].dropna().unique().astype(int)):
        attempted = (all_trials["noise_level_idx"] == nl).sum()
        succeeded = (success["noise_level_idx"] == nl).sum() if not success.empty else 0
        out[nl] = 100.0 * succeeded / attempted if attempted else None
    return out


def build(data_root: str, output_path: str) -> dict:
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
    all_data = {}

    for ax, (label, fsm_dir, neural_dir) in zip(axes, FAMILIES):
        neural_sr = _sr_by_noise_level(os.path.join(EXP_ROOT, neural_dir))
        fsm_sr = _sr_by_noise_level(os.path.join(data_root, fsm_dir))
        all_data[label] = {"neural": neural_sr, "fsm": fsm_sr}

        nx = sorted(neural_sr)
        fx = sorted(fsm_sr)
        # Obstacle: both systems sit at 100% for every noise level (perfect overlap, verified
        # numerically) -- a solid line under a solid line would hide one entirely. Dash the Neural
        # line there so the reader can see both curves are present, not that one is missing.
        neural_style = "--" if label == "Obstacle" else "-"
        # FSM plotted first (solid), Neural drawn on top (dashed where they overlap) so the dashes
        # are visible instead of being painted over by the solid line underneath.
        ax.plot(fx, [fsm_sr[n] for n in fx], marker="s", color=FSM_COLOR, linewidth=3, label="FSM")
        ax.plot(nx, [neural_sr[n] for n in nx], marker="o", color=NEURAL_COLOR,
                linestyle=neural_style, label="Neural")
        ax.set_xticks(sorted(set(nx) | set(fx)))
        # r202_audit_notes ronda 2: in-plot annotation overlapped the axis -- removed. The overlap
        # explanation now belongs in the figure's caption/description (README.md, audit tool),
        # not baked into the image; the dashed line is the only in-image cue left.
        ax.set_title(label)
        ax.set_xlabel("Noise Level (index)")

    # Trimmed to the data's actual range (55-100%) instead of the full 0-100% axis -- the low end
    # never goes below 60% (Appetitive, noise_level_idx=3), so a 0-108 axis just wasted space.
    all_vals = [v for d in all_data.values() for sub in d.values() for v in sub.values() if v is not None]
    lo = min(all_vals) - 8
    axes[0].set_ylim(lo, 105)
    axes[0].set_ylabel("Success Rate (%)")
    axes[0].legend(loc="lower left", fontsize=9)
    fig.suptitle("Success Rate vs. Noise Level — Neural vs. FSM (single-stimulus families)", fontsize=11)
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
    p.add_argument("--output", default="experiments/R2-02-fsm-baseline/output/fig_sr_vs_noise_level.png")
    args = p.parse_args()

    data = build(args.data_root, args.output)
    print(f"Wrote {args.output}")
    for fam, d in data.items():
        print(" ", fam, d)
