---
name: scientific-visualization
description: Create and audit truthful, accessible, publication-ready scientific figures with Matplotlib, Seaborn, or Plotly. Use for figure design, multi-panel layouts, uncertainty and missing-data displays, color/contrast review, image metadata validation, and journal export planning.
license: MIT
compatibility: Requires Python 3.11+ and uv for pinned examples. Bundled CLIs are network-free and load Matplotlib, Pillow, or pypdf only when needed. Plotly static export with Kaleido v1 requires a compatible Chrome/Chromium installation.
allowed-tools: Read Write Edit Bash Glob Grep
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
  source: https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-visualization
  imported: 2026-08-27
---

# Scientific Visualization

Build figures that preserve scientific meaning before optimizing appearance. Separate universal principles from dated publisher rules, preserve raw data and transformations, use color redundantly, and inspect delivered files rather than trusting plotting defaults.

## Non-negotiable guardrails

- Never alter, hide, invent, or selectively enhance data to improve a figure.
- Preserve raw tables/images, exclusions, missing-value codes, analysis code, normalization, binning, image adjustments, and random seeds.
- Do not infer journal requirements. Identify the exact journal, article type, figure type, and submission phase; verify its live official guidance.
- Do not claim that a palette, DPI value, format, or automated report makes a figure accessible or journal-compliant.
- Do not silently connect missing observations, suppress inconvenient points, upsample images as if detail increased, or tune axes/dual axes to exaggerate a conclusion.
- Keep interactive and static outputs as distinct deliverables. Interactive hover is not a substitute for labels, alt text, keyboard access, an accessible data table, or a static fallback.

Read `references/publication_guidelines.md` for deceptive-encoding and integrity checks (fetch on
demand, not mirrored locally — see note at the end of this file). Read `references/journal_requirements.md`
only after the target and phase are known.

## Workflow

### 1. Define the evidence and destination

Record:

- audience and medium: manuscript, web, slide, poster, supplement;
- exact publisher/journal, article type, submission phase, and intended final width;
- variable semantics, units, sample/replicate structure, missing/censored values;
- estimator and uncertainty definition;
- transformations: filtering, aggregation, normalization, smoothing, bins, image processing;
- source-data paths/identifiers and output provenance.

If requirements are not known, create a provisional general figure and label all publisher choices as pending verification.

**This project (ROBOT-D-26-00122R1, Robotics and Autonomous Systems / Elsevier):** target width is
a single-column figure unless the manuscript's `\includegraphics[width=...]` says otherwise (check
`sections/results.tex`); no official Elsevier figure-style profile has been verified against the
live submission guidelines as of this import — treat any DPI/format choice as provisional until
that's checked.

### 2. Choose an honest encoding

Prefer position on a common scale. Before coding, check:

- **Bars/areas:** normally include zero because length/area is measured from a baseline.
- **Points/lines:** nonzero limits can be valid; show context and disclose breaks.
- **Uncertainty:** name SD, SE, CI, percentile, posterior, or another interval; state `n` and the unit of replication.
- **Raw observations:** show them when feasible; do not let jitter obscure categories/values.
- **Missing data:** distinguish missing, zero, censored, and excluded; use gaps or explicit model/interpolation styling.
- **Area/volume:** scale area/volume, not radius/diameter; avoid decorative 3D.
- **Log axes:** label the base/transform and declare how zero/negative values are handled.
- **Binning/smoothing:** record edges, bandwidth/window, method, and sensitivity.
- **Normalization:** state formula/reference and keep limits consistent across compared panels.
- **Dual axes:** prefer aligned panels; if unavoidable, justify units and do not engineer apparent correlation.
- **Images:** preserve originals, disclose whole-image adjustments, show scale bars, and avoid clipped/erased background.

### 3. Design accessibility in, not after

- Use color plus marker, line style, hatching, direct label, or panel separation.
- Choose qualitative, sequential, diverging, or cyclic color according to data semantics.
- Audit foreground/background contrast at the rendered size.
- Make missing and out-of-range values explicit.
- Provide alt text, a longer description for complex figures, and underlying data for web delivery.
- Treat WCAG 2.2 as web guidance: 4.5:1 normal text, 3:1 large text, and 3:1 for graphical objects required for understanding; color cannot be the only cue. Applicability and exceptions matter.

See `references/color_palettes.md` (fetch on demand). A grayscale screen is useful but is not a
complete color-vision or accessibility test.

### 4. Implement with scoped styles

Use Matplotlib's object-oriented API and a project style file — `assets/publication.mplstyle`
(mirrored locally in this skill folder) is the starting point already wired into
`experiments/_plotting/style.py`:

```python
import matplotlib.pyplot as plt
plt.style.use(".claude/skills/scientific-visualization/assets/publication.mplstyle")

fig, ax = plt.subplots(figsize=(3.5, 2.5), layout="constrained")
ax.plot(x, y, marker="o", label="Observed")
ax.set(xlabel="Time (hours)", ylabel="Response (unit)")
ax.legend()
```

`layout="constrained"` supports colorbars, nested GridSpec, subfigures, and `subplot_mosaic`. Do not call `tight_layout()` afterward; it disables constrained layout.

For exact physical dimensions, do not use `bbox_inches="tight"` unless the changed page size is intentional.

#### Color normalization

```python
import matplotlib as mpl

norm = mpl.colors.TwoSlopeNorm(vmin=-2, vcenter=0, vmax=5)
cmap = mpl.colormaps["RdBu_r"].with_extremes(bad="#777777")
image = ax.imshow(values, norm=norm, cmap=cmap, interpolation="nearest")
fig.colorbar(image, ax=ax, label="Change (unit)")
```

Use `LogNorm`, `CenteredNorm`, `SymLogNorm`, `BoundaryNorm`, or `TwoSlopeNorm` only when its mapping matches the scientific meaning.

#### Seaborn

Seaborn 0.13.2 uses the current `errorbar` API:

```python
sns.lineplot(
    data=frame,
    x="time",
    y="response",
    hue="treatment",
    style="treatment",
    markers=True,
    errorbar=("ci", 95),
    n_boot=5000,
    seed=20260723,
    ax=ax,
)
```

Axes-level functions fit custom Matplotlib layouts; figure-level functions create their own figures/facets. Do not customize Seaborn's internal artist lists as if they were stable API.

### 5. Export explicitly and record provenance

- `dpi=300` minimum for print figures in this project (matches the manuscript's other assets).
- Prefer `bbox_inches=None` (preserve declared figure dimensions) over `"tight"` unless a changed
  page size is intentional — `"tight"` is what every builder in `experiments/_plotting/` used
  before this import; revisit case by case.
- Use an opaque explicit background unless transparency is required; blending against another
  background changes apparent contrast.
- Record what raw data / transformation produced the figure — every `experiments/_plotting/builders/*.py`
  and `experiments/_plotting/extract/*.py` script's docstring already does this; keep that
  discipline for anything new.

### 6. Inspect, compare, and review

1. Inspect file metadata (size, DPI, embedded fonts).
2. Audit palette contrast/grayscale separation.
3. Compare against the manuscript's own already-published figures for visual family consistency.
4. View at final size in the manuscript context (i.e. re-check inside the compiled PDF, not just the standalone PNG).
5. Manually review fonts, clipping, legends, scale bars, image integrity, caption, and source data.
6. Re-verify Elsevier's live figure-submission guidance immediately before the final submission pass — not assumed from this file.

## Pinned snapshot (upstream, informational — this project uses its own `experiments/.venv_plotting/`)

The upstream skill's examples/smoke tests use direct package pins current on 2026-07-23:
`matplotlib==3.11.1`, `seaborn==0.13.2`, `plotly==6.9.0`, `kaleido==1.3.0`, `pillow==12.3.0`,
`pypdf==6.14.2`. This project's own venv (`experiments/.venv_plotting/`, gitignored) has its own
resolved versions — check with `experiments/.venv_plotting/bin/pip freeze` rather than assuming
these match.

## Assets mirrored locally

- `assets/publication.mplstyle` — general print starting point (Okabe-Ito colorblind-safe 5-color
  cycle, no default grid, clean sans-serif, 300dpi export). **Already wired into
  `experiments/_plotting/style.py`** as of 2026-08-27.
- Not mirrored (fetch on demand if needed): `assets/nature.mplstyle` (Nature-specific, not our
  journal), `assets/presentation.mplstyle`, `assets/color_palettes.py`, `assets/publisher_profiles.json`,
  and the bundled CLIs (`scripts/image_metadata.py`, `scripts/palette_audit.py`,
  `scripts/export_plan.py`, `scripts/style_preview.py`) — none of these were needed for this
  project's first pass; fetch from
  `https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/scientific-visualization/<path>`
  if a future task needs them.

## References not mirrored locally

Fetch on demand from the URL pattern above:
- `references/publication_guidelines.md` — integrity, deceptive encodings, accessibility, static/interactive output.
- `references/color_palettes.md` — palette semantics, exact values, WCAG contrast, grayscale caveats.
- `references/journal_requirements.md` — phase-specific official publisher snapshots (no Elsevier/RAS profile verified yet for this project).
- `references/matplotlib_examples.md` — current, runnable Matplotlib/Seaborn/Plotly patterns.
- `references/sources.md` — official URLs, dates, versions.

## Final review checklist

- [ ] Raw data/images and transformation code are preserved.
- [ ] Missing values, exclusions, bins, normalization, and uncertainty are explicit.
- [ ] Baselines, scales, limits, and area/volume encodings are honest.
- [ ] Color is redundant and rendered contrast was reviewed.
- [ ] Figure has an accessible description/data alternative where applicable.
- [ ] Physical dimensions, DPI, format, fonts, transparency, and file size were inspected after export.
- [ ] Publisher rules were verified for the exact journal and phase (Elsevier/RAS — not yet done for this project).
- [ ] No automated report is presented as a scientific, accessibility, or compliance certification.
