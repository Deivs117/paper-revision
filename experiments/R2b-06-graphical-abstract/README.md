# R2b-06 — Graphical abstract aligned with the round-1 contributions

## Goal

Replace `assets/GRAPHICAL_ABSTRACT.pdf` (hand-made in Canva, Dec 2025) for `PROGRESS.md` row
`R2b-06`. Reviewer 2: the old abstract "only illustrates the original sensing–decision–locomotion
pipeline" and does not reflect the ablation study, the FSM baseline comparison or the inspection-task
experiments. The Highlights half of the same row is a plain `sections/preamble.tex` edit (see
`patches/r2b-06-graphical-abstract-highlights.tex`).

## Method

`scripts/build_graphical_abstract.py` (matplotlib) rebuilds the abstract as four panels:

1. **Core idea** — simulated and physical robot (photos reused from the original abstract).
2. **Method** — camera/LiDAR/IMU → basal-ganglia winner-take-all circuit → three locomotion modes
   (all photos/diagram reused from the original abstract).
3. **Ablation study** — success rate under three-stimulus conflict for the intact circuit and the
   three ablations (`fig:ablation_success_rate`), n = 12 per variant, Fisher's exact p vs. intact.
4. **FSM baseline & inspection** — Neural vs. FSM success rate in the three-stimulus conflict suite
   and the inspection task (`tab:fsm_comparison`).

Both chart panels use a minimal graphical-abstract style: no value axis or ticks, every bar labelled
directly with its % (plus k/n on the FSM panel), the metric stated in words at the top of the card,
and only the zero baseline kept so a 0% bar reads as zero rather than missing. The inspection task's
$d_{final}$ precision was dropped from the abstract (one message per panel); it stays in the text.

Visual language (title, `#ffbd59` panel fill, photo set) is kept from the original so the abstract
reads as a revision of the same figure, not a different paper. Chart colours follow the repo's
Okabe–Ito palette (`experiments/_plotting/style.py`).

## Parameters / seed

`config.json` — every plotted number, each block annotated with the manuscript location it was
copied from. Deterministic (no randomness).

## Data provenance

- Numbers: transcribed from `sections/results.tex` (cross-checked against
  `experiments/R3-02-wta-vs-threshold/output/ablation_stats_summary.csv` and
  `experiments/R2-02-fsm-baseline/output/table_master_comparison.csv` for the trial counts).
  If those manuscript values change, update `config.json` and re-run.
- Photos/diagram: extracted at run time with poppler's `pdfimages` from the **original** abstract,
  recovered from git history at the commit pinned in `config.json` (`original_ga_commit`), since the
  live `assets/GRAPHICAL_ABSTRACT.pdf` is now this experiment's own output. Extracted files land in
  `data/` (gitignored, regenerable).

## How to regenerate

```
# from the repo root; needs git + poppler (pdfimages)
uv run --with matplotlib --with numpy --with pillow \
    python experiments/R2b-06-graphical-abstract/scripts/build_graphical_abstract.py
scripts/promote_figure.sh --force \
    experiments/R2b-06-graphical-abstract/output/GRAPHICAL_ABSTRACT.pdf GRAPHICAL_ABSTRACT.pdf
```

`output/*.pdf` matches the repo-wide `*.pdf` ignore rule, so stage it with `git add -f`.

## Output files

| File in `output/` | Promoted to (`assets/...`) | Used in |
|---|---|---|
| `GRAPHICAL_ABSTRACT.pdf` | `assets/GRAPHICAL_ABSTRACT.pdf` (overwrites the Canva original, `--force`) | `sections/preamble.tex`, `graphicalabstract` env |
| `GRAPHICAL_ABSTRACT.png` | — (preview / upload copy for the submission system) | — |
