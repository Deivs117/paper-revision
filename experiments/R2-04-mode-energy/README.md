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

## Result (2026-08-29, final — intra-segment statistics)

The reporting framework was updated on 2026-08-29: **intra-segment statistics** (mean and SD of
individual power samples pooled across all steady-state segments per mode) replace the previous
inter-segment statistics for the paper table. This makes all three modes comparable regardless of
segment count, and gives X a valid SD (within the single available segment). The hardware was
subsequently decommissioned — no additional X-mode recordings are possible.

| Mode | N segments | N samples | Mean power ± SD (intra-segment) |
|---|---|---|---|
| Quadrupedal (C) | 20 | 1 873 | 2.73 ± 2.29 W |
| Differential Rolling (H) | 20 | 3 297 | 1.13 ± 1.08 W |
| Omnidirectional (X) | 1 | 194 (38.6 s) | 5.71 ± 0.73 W |

Inter-segment stats (C: 1.94 ± 1.82 W / H: 1.36 ± 1.01 W) are preserved in
`output/mode_energy_stats.csv` for reference.

`scripts/build_mode_energy.py` → `output/FigReal_ModeSteadyStateEnergy.png` (bar chart, sanity-check
visualization) + `output/mode_energy_stats.csv` (both intra- and inter-segment stats).
**The author decided a table fits the manuscript better than a graph** — the figure stays as the
computation record, not the artifact to promote.

The full analysis and writing instructions for the paper update are in
`intake/pending/R2-04-02_energy_analysis_for_writing.md` — that document is the source of truth
for what goes into `sections/results.tex`.

## Caveats

1. **Omnidirectional (X):** a single 38.6 s segment from floor_t01. SD (0.73 W, CV 12.8 %) reflects
   moment-to-moment variability during operation, not between-trial replication. Hardware
   decommissioned — no further recordings possible.
2. C/H intra-segment means differ from inter-segment means (C: 2.73 vs 1.94 W; H: 1.13 vs 1.36 W)
   because longer segments (more samples) weight more in the temporal average. Both are correct;
   they answer different questions (time-weighted vs. trial-weighted average).
3. C/H inter-segment CV (~74–94 %) is inflated by physical-condition heterogeneity across recordings
   (floor/ramp/static), not pure measurement noise.
4. "Long-term average" = averaged over available bench recordings, not a multi-hour mission profile.

## Decision: table, not a figure (2026-08-27)

The author's assessment, followed here: a bar chart for 3 categories is not very informative on its
own, and a table is far cheaper to update. See
`intake/processed/R02-01-03_energia_transicion_y_modo_R2-04.md` §3/§5 for the executed table
integration (`intake/R02-01_INDEX.md` for the full block index).
