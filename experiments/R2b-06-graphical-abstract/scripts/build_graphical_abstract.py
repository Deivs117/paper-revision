"""Regenerates the graphical abstract (R2b-06).

Keeps the original Canva abstract's visual language (title, orange #ffbd59 panels, the same robot/
sensor/circuit photos — extracted from the pre-R2b-06 PDF pinned in config.json) and replaces its
single generic "Key Results" panel with the round-1 contributions the reviewer said were missing:
the basal-ganglia ablation study, the FSM baseline comparison and the inspection task. Every plotted
number comes from config.json, which in turn cites the manuscript location it was copied from.

Run from the repo root:
    uv run --with matplotlib --with numpy --with pillow \
        python experiments/R2b-06-graphical-abstract/scripts/build_graphical_abstract.py
Requires poppler's `pdfimages` and git (to recover the original PDF from history).
"""
from __future__ import annotations

import json
import os
import subprocess

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "output")

PANEL = "#ffbd59"      # original Canva panel fill
CARD = "#ffffff"
INK = "#1a1a1a"
MUTED = "#5a4a32"
NEURAL = "#0072B2"     # Okabe-Ito blue, same as experiments/_plotting/style.py
FSM = "#7f7f7f"        # neutral gray: the baseline, not a competing "brand" color
ABL_KEEP = "#0072B2"
ABL_DROP = "#D55E00"   # Okabe-Ito vermilion for the ablated variants

plt.rcParams.update({
    "font.family": ["Noto Sans", "DejaVu Sans"],
    "pdf.fonttype": 42,  # embed TrueType so text stays selectable/editable
})


# --------------------------------------------------------------------------- source images
def extract_original_images(cfg) -> dict[str, Image.Image]:
    """Recover the original abstract from git history and pull out its embedded photos."""
    os.makedirs(os.path.join(DATA, "extracted"), exist_ok=True)
    pdf = os.path.join(DATA, "original_ga.pdf")
    with open(pdf, "wb") as f:
        f.write(subprocess.check_output(
            ["git", "-C", REPO, "show", f"{cfg['original_ga_commit']}:{cfg['original_ga_path']}"]))
    prefix = os.path.join(DATA, "extracted", "img")
    subprocess.check_call(["pdfimages", "-png", pdf, prefix])

    def load(idx, mask_idx=None):
        im = Image.open(f"{prefix}-{idx:03d}.png").convert("RGB")
        if mask_idx is not None:
            im.putalpha(Image.open(f"{prefix}-{mask_idx:03d}.png").convert("L"))
        return im

    # Indices follow `pdfimages -list` order of the pinned PDF (image, then its smask).
    return {
        "camera": load(0, 1), "lidar": load(2, 3), "imu": load(4, 5),
        "circuit": load(6, 7), "modes": load(8), "sim_robot": load(10),
        "real_robot": load(11, 12),
    }


# --------------------------------------------------------------------------- layout helpers
def panel(fig, x, y, w, h, color=PANEL, radius=0.012):
    fig.patches.append(FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
        transform=fig.transFigure, facecolor=color, edgecolor="none", zorder=-10))


def place_image(fig, img, x, y, w, h):
    """Fit `img` inside the figure-fraction box (x, y, w, h), centered, aspect preserved."""
    fw, fh = fig.get_size_inches()
    box_ar = (w * fw) / (h * fh)
    img_ar = img.width / img.height
    if img_ar > box_ar:
        nh = w * fw / img_ar / fh
        rect = (x, y + (h - nh) / 2, w, nh)
    else:
        nw = h * fh * img_ar / fw
        rect = (x + (w - nw) / 2, y, nw, h)
    ax = fig.add_axes(rect, zorder=5)
    ax.imshow(np.asarray(img), interpolation="lanczos")
    ax.axis("off")
    return ax


def arrow(fig, x, y0, y1):
    fig.patches.append(FancyArrowPatch(
        (x, y0), (x, y1), transform=fig.transFigure, arrowstyle="-|>,head_width=6,head_length=8",
        linewidth=3.2, color=INK, zorder=3))


def header(fig, x, y, text):
    fig.text(x, y, text, ha="center", va="top", fontsize=21, fontweight="bold", color=INK)


def body(fig, x, y, text, size=15, **kw):
    kw.setdefault("ha", "center")
    kw.setdefault("va", "top")
    kw.setdefault("color", INK)
    fig.text(x, y, text, fontsize=size, linespacing=1.05, **kw)


def style_chart_axes(ax, baseline):
    """Minimal GA chart: no value axis, no ticks — every bar carries its own % label, so only the
    zero baseline is kept (so a 0% bar reads as zero, not as missing data)."""
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side == baseline)
    ax.spines[baseline].set_color(MUTED)
    ax.spines[baseline].set_linewidth(1.4)
    ax.tick_params(colors=INK, labelsize=13, length=0)


def chart_card(fig, x, w, card_y, top, metric):
    """White card holding a chart, with the plotted metric stated in words at its top."""
    panel(fig, x + 0.012, card_y, w - 0.024, top - card_y, color=CARD, radius=0.008)
    body(fig, x + w / 2, top - 0.018, metric, size=13, fontweight="bold")


def panel_frame(fig, x, w, y0, h, title, subtitle):
    """Draws the orange panel, its header and 2-line subtitle; returns the y where content starts."""
    panel(fig, x, y0, w, h)
    top = y0 + h
    header(fig, x + w / 2, top - 0.022, title)
    body(fig, x + w / 2, top - 0.085, subtitle)
    return top - 0.185


# --------------------------------------------------------------------------- panels
def core_idea(fig, imgs, x, w, y0, h):
    top = panel_frame(fig, x, w, y0, h, "Core idea", "Hybrid wheel–leg quadruped\nwith three locomotion modes")
    pad = 0.012
    img_h = (top - (y0 + 0.11)) / 2
    place_image(fig, imgs["sim_robot"], x + pad, top - img_h, w - 2 * pad, img_h - 0.008)
    place_image(fig, imgs["real_robot"], x + pad, top - 2 * img_h, w - 2 * pad, img_h - 0.008)
    body(fig, x + w / 2, y0 + 0.095, "Validated in Gazebo simulation\nand on a physical prototype", size=14)


def method(fig, imgs, x, w, y0, h):
    top = panel_frame(fig, x, w, y0, h, "Method", "Multimodal sensing drives\nneural gait arbitration")
    cx = x + w / 2
    sw = (w - 0.03) / 3
    sens_h = 0.075
    for i, (key, label) in enumerate((("camera", "Camera"), ("lidar", "LiDAR"), ("imu", "IMU"))):
        sx = x + 0.015 + i * sw
        place_image(fig, imgs[key], sx + 0.012, top - sens_h, sw - 0.024, sens_h)
        body(fig, sx + sw / 2, top - sens_h - 0.006, label, size=13)
    y = top - sens_h - 0.05
    arrow(fig, cx, y, y - 0.035)
    y -= 0.042
    card_h = 0.19
    panel(fig, x + 0.012, y - card_h, w - 0.024, card_h, color=CARD, radius=0.008)
    place_image(fig, imgs["circuit"], x + 0.016, y - card_h + 0.036, w - 0.032, card_h - 0.042)
    body(fig, cx, y - card_h + 0.032, "Basal-ganglia winner-take-all circuit", size=12.5,
         fontweight="bold")
    y -= card_h + 0.007
    arrow(fig, cx, y, y - 0.035)
    y -= 0.042
    body(fig, cx, y, "Quadrupedal · Differential · Omnidirectional", size=13)
    place_image(fig, imgs["modes"], x + 0.012, y0 + 0.012, w - 0.024, y - 0.045 - (y0 + 0.012))


def ablation(fig, cfg, x, w, y0, h):
    a = cfg["ablation"]
    top = panel_frame(fig, x, w, y0, h, "Ablation study",
                      "Removing basal-ganglia mechanisms\nbreaks conflict resolution")
    card_y = y0 + 0.09
    chart_card(fig, x, w, card_y, top, "Success rate under stimulus conflict")
    ax = fig.add_axes((x + 0.098, card_y + 0.02, w - 0.128, top - card_y - 0.085), zorder=5)
    ypos = np.arange(len(a["variants"]))[::-1]
    colors = [ABL_KEEP] + [ABL_DROP] * (len(a["variants"]) - 1)
    ax.barh(ypos, a["success_pct"], color=colors, height=0.62)
    for yp, v, p in zip(ypos, a["success_pct"], a["p_vs_full"]):
        inside = v > 60
        ax.text(v - 2 if inside else v + 2, yp, f"{v:.0f}%", va="center",
                ha="right" if inside else "left", fontsize=13,
                color="white" if inside else INK, fontweight="bold")
        if p is not None:
            # Inside a long bar the p-value sits left of the % label (white, inside the bar) so it
            # never runs past the axes/card edge; on short bars it follows the % label outside.
            ax.text(v - 26 if inside else v + 27, yp, p, va="center",
                    ha="right" if inside else "left", fontsize=11.5,
                    color="white" if inside else MUTED)
    ax.set_yticks(ypos, a["variants"])
    ax.set_xlim(0, 100)
    ax.set_xticks([])
    style_chart_axes(ax, baseline="left")
    body(fig, x + w / 2, card_y - 0.012,
         f"Simulation · n = {a['n_per_variant']} trials per variant\nFisher's exact p vs. intact circuit",
         size=12.5, color=MUTED)


def baseline_comparison(fig, cfg, x, w, y0, h):
    f = cfg["fsm"]
    top = panel_frame(fig, x, w, y0, h, "FSM baseline & inspection",
                      "Neural arbitration outperforms a\npriority-rule FSM baseline")
    card_y = y0 + 0.09
    chart_card(fig, x, w, card_y, top, "Success rate")
    # Legend as colored words under the metric title — no separate legend box to decode.
    cx = x + w / 2
    fig.text(cx - 0.006, top - 0.058, "■ Basal ganglia", ha="right", va="top", fontsize=13,
             color=NEURAL, fontweight="bold")
    fig.text(cx + 0.006, top - 0.058, "■ FSM", ha="left", va="top", fontsize=13, color=FSM,
             fontweight="bold")
    ax = fig.add_axes((x + 0.03, card_y + 0.12, w - 0.06, top - card_y - 0.23), zorder=5)
    xs = np.arange(len(f["suites"]))
    bw = 0.36
    for off, data, color in ((-bw / 2, f["neural_success"], NEURAL), (bw / 2, f["fsm_success"], FSM)):
        pct = [100 * s / n for s, n in data]
        ax.bar(xs + off, pct, bw * 0.92, color=color)
        for xi, (s, n), v in zip(xs + off, data, pct):
            ax.text(xi, v + 11, f"{v:.0f}%", ha="center", va="bottom", fontsize=14, color=INK,
                    fontweight="bold")
            ax.text(xi, v + 2, f"{s}/{n}", ha="center", va="bottom", fontsize=11.5, color=MUTED)
    ax.set_xticks(xs, f["suites"])
    ax.set_xlim(-0.6, len(xs) - 0.4)
    ax.set_ylim(0, 125)
    ax.set_yticks([])
    style_chart_axes(ax, baseline="bottom")
    ax.tick_params(axis="x", labelsize=12.5)
    n_txt = " / ".join(str(d[1]) for d in f["neural_success"])
    body(fig, cx, card_y - 0.012, f"Simulation · n = {n_txt} trials per controller\nmatched trial conditions",
         size=12.5, color=MUTED)


# --------------------------------------------------------------------------- main
def main():
    with open(os.path.join(HERE, "config.json")) as fh:
        cfg = json.load(fh)
    imgs = extract_original_images(cfg)
    fig = plt.figure(figsize=cfg["figure_size_in"], facecolor="white")
    fig.text(0.5, 0.982, cfg["title"], ha="center", va="top", fontsize=24, fontweight="bold",
             color=INK, linespacing=1.0)

    y0, h, gap, margin = 0.015, 0.83, 0.012, 0.012
    widths = np.array([0.205, 0.27, 0.255, 0.27])
    widths *= (1 - 2 * margin - gap * (len(widths) - 1)) / widths.sum()
    xs = margin + np.concatenate(([0], np.cumsum(widths[:-1] + gap)))
    core_idea(fig, imgs, xs[0], widths[0], y0, h)
    method(fig, imgs, xs[1], widths[1], y0, h)
    ablation(fig, cfg, xs[2], widths[2], y0, h)
    baseline_comparison(fig, cfg, xs[3], widths[3], y0, h)

    os.makedirs(OUT, exist_ok=True)
    for ext in ("pdf", "png"):
        path = os.path.join(OUT, f"GRAPHICAL_ABSTRACT.{ext}")
        fig.savefig(path, dpi=cfg["dpi"], facecolor="white")
        print(f"wrote {os.path.relpath(path, REPO)}")


if __name__ == "__main__":
    main()
