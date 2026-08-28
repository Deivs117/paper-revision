# R2-04 — Long-Term Average Power Consumption per Locomotion Mode

**Reviewer ask:** "Supplement long-term average energy consumption of three locomotion modes for
onboard deployment analysis." **Distinct from** `experiments/N-02-physical-figure-regeneration/`'s
`FigReal_Morphological_Transition_Energy.png`, which measures energy spent *during* a mode
transition (a brief event) — this measures average power *while operating* in each of the 3 modes
(Quadrupedal `C` / Differential Mobile `H` / Omnidirectional `X`), transition windows excluded.

## Method

Same `robot_cmd` structural-command detection as the transition-energy figure (`c`/`z`/`x` mark
entry into `C`/`H`/`X`). For each maximal segment where the active mode stays constant, the
pre-calibrated electromechanical coupling window is excluded from the segment's start (2.92s for a
segment entered via `z`, 1.56s via `c` — same values already published in
`FigReal_Terrain_Latencies_4Panels`; no calibrated window exists for `x`, so `X` segments use their
full duration unadjusted). Power = `|current_A| × 7.2V` (fixed NiMH 3300mAh pack voltage, confirmed
by the author's hardware team) averaged over what remains of each segment.

## Result (2026-08-27, current data)

| Mode | N segments | Mean power ± SD |
|---|---|---|
| Quadrupedal (C) | 20 | 1.94 ± 1.77 W |
| Differential Mobile (H) | 20 | 1.36 ± 0.98 W |
| Omnidirectional (X) | **1** (single 38.6s segment, no replication) | 5.71 W |

`scripts/build_mode_energy.py` → `output/FigReal_ModeSteadyStateEnergy.png` (bar chart, built for
this planning round — **the author decided a table fits the manuscript better than a graph for
this metric**, see decision below; the script and figure stay here as the computation record /
sanity-check visualization, not as the artifact to promote).

## Caveats

1. **Omnidirectional (X) is a single-sample placeholder, not a real average.** The author's team
   confirmed (2026-08-27, verbally) that a dedicated Omnidirectional-mode energy test battery is
   planned. **When that data lands, this is a small, mechanical update** — rerun
   `scripts/build_mode_energy.py` against the new `experiments/real/` folder(s), the X row's
   mean±SD/N updates, nothing else in the pipeline changes.
2. The 20 C/H segments span different physical conditions (flat floor, inclined ramp, static
   in-place test) mixed together — part of the within-mode variance reflects that heterogeneity,
   not just measurement noise.
3. C vs. H is not statistically significant (Welch t≈1.26, two-sample unequal-variance).
4. "Long-term average" here means "averaged over the available steady-state segments" from short
   bench recordings, not a multi-hour endurance mission profile.

## Decision: table, not a figure (2026-08-27)

The author's assessment, followed here: a bar chart for 3 categories (one of them N=1, expected to
be replaced) is not very informative on its own, and a table is far cheaper to update once the
Omnidirectional data arrives (edit one row vs. regenerate + re-review a figure). See
`intake/pending/R02-01_metric_and_figure_audit.md` §9.9 for the drafted LaTeX table and integration
plan for the writing agent.
