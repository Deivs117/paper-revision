"""Builder for the MLP-classifier figure block (Tarea 3, included by explicit author instruction
even though not physical-specific): fig1_confusion_matrix, fig4_architecture_ablation (both from
values already in results.tex prose, no vectorization -- Informe 2 F-Data-06), and the F-03 fused
1x3 panel from fig5/fig6 (vectorized this round, experiments/_plotting/vectorized/classifier_fig5.csv
and classifier_fig6.csv -- see experiments/_plotting/extract/extract_fig5.py / extract_fig6.py for
the exact pixel calibration used).
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import DPI  # noqa: E402

# fig1_confusion_matrix.png -- values confirmed exact by Informe 1 M-05 (TP/FN/FP/TN sum to n=120,
# reproduce accuracy=0.800/precision=0.747/recall=0.918 cited in results.tex:571 to the third digit)
CONFUSION = {"TP": 56, "FN": 5, "FP": 19, "TN": 40}

# fig4_architecture_ablation.png -- F1 values already cited in results.tex:598
ARCHITECTURE_F1 = {"(50)": 0.747, "(100)": 0.766, "(150,80)": 0.771, "(200,100,50)": 0.766}


def build_fig1_confusion(output_path: str) -> None:
    mat = np.array([[CONFUSION["TN"], CONFUSION["FP"]], [CONFUSION["FN"], CONFUSION["TP"]]])
    fig, ax = plt.subplots(figsize=(3.5, 3.2))
    im = ax.imshow(mat, cmap="Blues")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(mat[i, j]), ha="center", va="center", fontsize=14)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Pred. Flat", "Pred. Inclined"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["True Flat", "True Inclined"])
    n = sum(CONFUSION.values())
    acc = (CONFUSION["TP"] + CONFUSION["TN"]) / n
    prec = CONFUSION["TP"] / (CONFUSION["TP"] + CONFUSION["FP"])
    rec = CONFUSION["TP"] / (CONFUSION["TP"] + CONFUSION["FN"])
    ax.set_title(f"MLP confusion matrix (n={n})\nacc={acc:.3f} prec={prec:.3f} rec={rec:.3f}", fontsize=8)
    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


def build_fig4_ablation(output_path: str) -> None:
    fig, ax = plt.subplots(figsize=(4.5, 3.2))
    names = list(ARCHITECTURE_F1.keys())
    vals = list(ARCHITECTURE_F1.values())
    colors = ["#d62728" if v < max(vals) else "#2ca02c" for v in vals]
    ax.bar(names, vals, color=colors)
    ax.set_ylim(0.65, 0.80)  # y-axis rescaled so the real 0.024-F1 spread is legible
    ax.set_ylabel("F1-score")
    ax.set_title("Architecture ablation")
    ax.annotate("y-axis truncated for legibility", xy=(0.02, 0.02), xycoords="axes fraction",
                fontsize=6, color="#555555")
    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


def build_f03_fused_panel(fig5_csv: str, fig6_csv: str, output_path: str) -> None:
    f5 = pd.read_csv(fig5_csv)
    f6 = pd.read_csv(fig6_csv)
    classifiers = ["Logistic Reg.", "SVM (RBF)", "Random Forest", "MLP (150-80)"]

    fig, axes = plt.subplots(1, 3, figsize=(11, 3.5))

    # (a) classification metrics, grouped bars
    metrics = ["accuracy", "precision", "recall", "f1"]
    metric_colors = {"accuracy": "#1f77b4", "precision": "#ff7f0e", "recall": "#2ca02c", "f1": "#d62728"}
    x = np.arange(len(classifiers))
    width = 0.2
    for i, m in enumerate(metrics):
        vals = [f5[(f5.classifier == c) & (f5.metric == m)]["value"].iloc[0] for c in classifiers]
        axes[0].bar(x + (i - 1.5) * width, vals, width, label=m, color=metric_colors[m])
    axes[0].set_xticks(x); axes[0].set_xticklabels(classifiers, rotation=20, ha="right", fontsize=7)
    axes[0].set_ylabel("Score (5-fold CV mean)")
    axes[0].set_ylim(0, 1.0)
    axes[0].legend(fontsize=6, ncol=2)
    axes[0].set_title("(a) Classification metrics")

    # (b) inference latency, log scale
    lat = [f6[(f6.classifier == c) & (f6.metric == "inference_latency_us")]["value"].iloc[0] for c in classifiers]
    axes[1].bar(classifiers, lat, color="#1f77b4")
    axes[1].set_yscale("log")
    axes[1].set_ylabel("Inference time (us/sample)")
    axes[1].tick_params(axis="x", rotation=20)
    axes[1].set_title("(b) Per-sample inference latency")

    # (c) model size, log scale
    size = [f6[(f6.classifier == c) & (f6.metric == "model_size_params")]["value"].iloc[0] for c in classifiers]
    axes[2].bar(classifiers, size, color="#ff7f0e")
    axes[2].set_yscale("log")
    axes[2].set_ylabel("Parameters / tree nodes")
    axes[2].tick_params(axis="x", rotation=20)
    axes[2].set_title("(c) Model size")

    fig.suptitle("Classifier accuracy/latency/size trade-off (F-03 fused panel; (b),(c) vectorized from "
                 "the currently-published fig5/fig6, see experiments/_plotting/vectorized/README.md)",
                 fontsize=8)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI)
    plt.close(fig)


if __name__ == "__main__":
    out_dir = "experiments/N-02-physical-figure-regeneration/output"
    build_fig1_confusion(os.path.join(out_dir, "fig1_confusion_matrix.png"))
    build_fig4_ablation(os.path.join(out_dir, "fig4_architecture_ablation.png"))
    build_f03_fused_panel(
        "experiments/_plotting/vectorized/classifier_fig5.csv",
        "experiments/_plotting/vectorized/classifier_fig6.csv",
        os.path.join(out_dir, "fig_classifier_tradeoff_fused.png"),
    )
    print("Wrote fig1/fig4/fused-panel to", out_dir)
