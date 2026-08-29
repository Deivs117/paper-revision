"""Generic direct-pixel-color extraction utility (Informe 2 D-11, refined this round: agent-executed
extraction uses this instead of driving WebPlotDigitizer through browser automation -- same
principle, more precise/auditable for code-driven execution. See vectorized/README.md.)

Two building blocks:
  - find_gridline_rows(): locates horizontal gridline pixel-rows inside a plot's axes box, for
    calibrating a pixel-row -> data-value mapping from evenly-spaced ticks (e.g. 0.0..1.0 step 0.2).
  - extract_bar_tops(): for a known bar color, finds each bar's topmost pixel row (=its value)
    by column, clustering contiguous x-columns into individual bars.

Every calibration point used here is documented alongside the extracted CSV in
experiments/_plotting/vectorized/README.md, per the trazabilidad-inversa rule.
"""
from __future__ import annotations

import numpy as np
from PIL import Image


def load_rgb(path: str) -> np.ndarray:
    return np.array(Image.open(path).convert("RGB"))


def find_gridline_rows(arr: np.ndarray, x0: int, x1: int, min_frac: float = 0.6,
                        gray_tol: int = 12) -> list[int]:
    """Rows within [x0,x1) where a large fraction of pixels are light gray (matplotlib gridlines)."""
    strip = arr[:, x0:x1, :]
    is_gray = (
        (np.abs(strip[:, :, 0].astype(int) - strip[:, :, 1].astype(int)) < gray_tol)
        & (np.abs(strip[:, :, 1].astype(int) - strip[:, :, 2].astype(int)) < gray_tol)
        & (strip[:, :, 0] > 150) & (strip[:, :, 0] < 235)
    )
    frac = is_gray.mean(axis=1)
    rows = np.where(frac > min_frac)[0]
    # collapse consecutive rows into single gridline centers
    if len(rows) == 0:
        return []
    groups = np.split(rows, np.where(np.diff(rows) > 1)[0] + 1)
    return [int(np.mean(g)) for g in groups]


def color_mask(arr: np.ndarray, color: tuple[int, int, int], tol: int = 20) -> np.ndarray:
    diff = np.abs(arr.astype(int) - np.array(color).astype(int))
    return (diff.max(axis=2) <= tol)


def extract_bar_tops(arr: np.ndarray, color: tuple[int, int, int], y_baseline: int,
                      x_gap: int = 5, tol: int = 20) -> list[tuple[int, int, int]]:
    """Returns [(x_start, x_end, top_row), ...] for each contiguous bar of `color`, scanning up to
    y_baseline (the pixel row of data value 0)."""
    mask = color_mask(arr[:y_baseline, :, :], color, tol=tol)
    cols_with_color = np.where(mask.any(axis=0))[0]
    if len(cols_with_color) == 0:
        return []
    groups = np.split(cols_with_color, np.where(np.diff(cols_with_color) > x_gap)[0] + 1)
    bars = []
    for g in groups:
        sub = mask[:, g[0]:g[-1] + 1]
        rows_with_color = np.where(sub.any(axis=1))[0]
        top = int(rows_with_color.min())
        bars.append((int(g[0]), int(g[-1]), top))
    return bars


def pixel_to_value(pixel_row: int, gridline_rows: list[int], gridline_values: list[float]) -> float:
    """Linear fit pixel-row -> data value from calibration gridlines."""
    coeffs = np.polyfit(gridline_rows, gridline_values, 1)
    return float(np.polyval(coeffs, pixel_row))
