# R2b-05 — trial count N in every experimental figure caption (owner: Sam, reassigned from Deivi 2026-10-28)

**DEADLINE: Thursday 2026-10-29 (end of day), merged into `main`.** R3b-04 (labeling sim vs physical in the same captions) is
blocked until this lands, and the Overleaf push must happen well before the 2026-11-04 deadline.

Self-contained brief: every number needed is in this repo (no author-private files, no `.gitignore`d data).
Read first: `OUTLINE.md`, `CLAUDE.md`, `intake/pending/round2_decision_letter_2026-10-25.md` (Reviewer 2, item 5:
"every experimental figure shows the number of trials N directly inside its caption, not only mentioned inside
main-text paragraphs"). Flow and `\revblue{}` rule: `CLAUDE.md`. Your row stops at `applied`.

## Already done (do not redo)
- `tab:fsm_comparison`: per-row N column + caption sentence (`patches/r2b-05-fsm-table-n.tex`).
- Already carry N: `fig:ablation_combined` (+ both subfigures), `fig:noise_robustness_extra_combined`,
  `fig:variable_topo_metrics`, `fig:attempts_vs_noise_level`, `fig:inspection_dfinal_scatter`,
  `fig:MorphologicalEnergy` (N=16/19), `fig:FourPanelLatencies` (15 replicates), `fig:mlp_eval_grid`.

## Scope
Figures in `sections/results.tex` that show measured/simulated data and whose caption has no N. Find them with
`grep -n 'begin{figure' sections/results.tex` and read each caption. Roughly:
- **Simulation traces/panels:** `RESPUESTAS_EST_UNI`, `NEU_EST_UNIG/UNIB`, `appetitive/aversive/obstacle/complex_micro`,
  `noise_robustness_grid`, `NEU_EST_MUL`, `RES_EST_MUL`, `NEU_IMU(2)`, `res_imu_pair`, `graph_imu_pair`,
  `stability_phases` (caption/prose already give N=268 samples), `transition_phases` (N=979 samples),
  `mode_timeline_complex`, `mode_timeline_inspection` (representative single trial: say "one representative trial;
  N=… per controller").
- **Physical traces:** `RESPUESTAS_EST_UNI_real`, `NEU_EST_UNIG_real`, `NEU_EST_MUL_real`, `RES_IMU_real`,
  `RES_IMU2_real`, `neu_imu_real_pair`, `graph_imu_real_pair`, the 4 `*_real_compound` figures,
  `classifier_tradeoff`.
- **Out of scope (no N applies — say so in the patch record, one line):** photo montages (`robot-6frames`,
  `real_variable_topography_sequence`), scene screenshots (`depot_simulation`), and every figure in
  `methodology.tex` (hardware photos, architecture/network diagrams, stimulus schematics).
- For a figure that shows ONE representative trial, write both: "(one representative trial of N=… )".

## Where each N comes from (all versioned)
- Simulation: `experiments/simulation/<familia>/` (one folder per trial; counts per family),
  `experiments/simulation/experiments_config.yaml`, and `experiments/R2-02-fsm-baseline/output/table_master_comparison.csv`
  (n_attempted / n_success; mission vs attempt, see the `tab:fsm_comparison` caption).
- Physical: `experiments/real/MANIFEST.md` / `manifest.json` list folders per scenario: `StimuliB` (Appetitive) t01..t04,
  `StimuliR` (Aversive) 3, `StimuliG` (Obstacle) 3, `MultiRGB` (Complex) 3 (`MultiRB` is DISCARDED, never count it),
  pitch-latency test 25 trials, morphological energy 16+19 transitions (already in its caption).
  **CONFLICT TO RESOLVE, DO NOT PICK ONE:** the manuscript already says "three hardware replicates" for the Appetitive
  physical figure (`results.tex` ~l.875/894), but the repo has FOUR Appetitive folders (t01..t04, all "usable"). Keep the
  published "three" and list this in your PR description for the author to confirm (was t04 excluded on purpose?).
- **Several physical captions already state their N** ("three hardware replicates" in the 4 `*_real_compound` captions,
  ~l.875–971). Read each caption before editing; do not duplicate or contradict it. A `grep` for `n=`/`N=` misses them.
- Inspection: `experiments/R3-05-inspection/` (data is versioned there); noise robustness and ablation: committed
  `output/` CSVs under `experiments/R3-04-noise-robustness/` and `experiments/R3-02-wta-vs-threshold/`.
  (Their raw `data/` folders are `.gitignore`d; you do not need them — the committed summaries and the numbers
  already in the manuscript suffice.)

## Do NOT guess — report instead
`experiments/real/MANIFEST.md` marks the `Test_current_integrated_{floor,ramp,static}_*` folders (terrain IMU/energy)
as **"not content-verified, name-based only"**. If a physical-terrain figure's N depends on them, do NOT write a
number: list the figure and the candidate N in the PR description for the author to confirm. Same rule for any
figure whose N you cannot trace to a file above.

## Coordination
R3b-04 (Deivi) will later edit the SAME captions to mark simulation vs physical and unify plot style. Merge your
PR first and tell the author; do not start the simulation/physical labeling yourself. C-60 (ablation prose trim,
`intake/pending/C-60_ablation_prose_trim_brief.md`) is a different region of `results.tex`; do them in separate PRs.

## Flow
`git pull origin main` → branch → edit captions → `python3 scripts/reassemble.py`, `scripts/validate_tex.sh`,
`scripts/check_roundtrip.sh` → `patches/r2b-05-figure-caption-n.tex` → keep row R2b-05 `pending` until every
in-scope caption is done, then `applied` → PR into `main`. Never run the Overleaf scripts.
