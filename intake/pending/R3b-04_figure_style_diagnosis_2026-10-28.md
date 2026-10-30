# R3b-04 — figure style diagnosis (2026-10-28) — owner: Deivi

Reviewer 3, item 4 (verbatim, `round2_decision_letter_2026-10-25.md`): "Format styles are inconsistent between
simulation and real-robot plots. Unify font and legend styles, and mark clearly whether each plot comes from
simulation or physical trials in captions."

## Method and limits (read before trusting any row)
3 independent read-only vision passes (model `fable`), 53 data figures (photo montages, scene screenshots and every
`methodology.tex` schematic excluded): A = 19 simulation (robustness/stability/ablation/timelines), B = 16 simulation
(neuron/IMU/MLP), C = 18 physical + 3 simulation references. Target standard: `experiments/_plotting/style.py`.
- Pillow was not installed; crops were made with ImageMagick / a scratchpad venv. Font sizes in pt are **estimates**
  (visual + builder code), not measured. A's "effective size in the PDF" assumes `\textwidth` ≈ 6 in, **unverified**.
- C zoomed into only 9 of its 18 images; the other 9 were judged at full view (typeface is reliable, fine legend/size
  details are not). Re-check those 9 before regenerating: Plot_1 ×4, Plot_3 Aversive/Obstacle, NEU_IMU2_real,
  GRAPH_IMU2_real, NEU_EST_MUL_real, RES_*_real.
- Builders were not executed: "the PNG predates `style.py`" is an inference.
- Verified by me directly (opened the images): `fig2_Obstacle` legend struck through by the dashed Roll line;
  `fig2_*` panel B title typo "Chasis" (→ Chassis); `GRAPH_IMU.png` is serif/tab10/dashed grid/legend 8 pt with a
  literal "---" in its title, while `GRAPH_IMU_real.png` is **sans-serif** (and shows a different quantity, MLP output
  states). Everything else below is the agents' finding, not independently confirmed.
- The earlier audit `intake/processed/C-21_*.md` ("no further findings") does not hold for style, and missed
  occlusions in at least `fig2_Obstacle` (verified) and, per the agents, `GRAPH_IMU2` and `NEU_IMU/NEU_IMU2`.

## Result: 12 OK, 41 to change (most minor)
OK: fig1_noise_robustness_grid, fig_R3_camera_dropout_evidence, fig_ablation_success_rate, FigB_Decision_Delay,
fig_inspection_dfinal_vs_nlidar, fig2_roc_curve, fig3_training_loss, RES_EST_UNI_real, the 4 `*_Real_Plot_1_*_ECDF`
(Aversive/Obstacle flagged OK* for the unit below).

## The reviewer's actual complaint, concretely (sim vs physical)
1. **Typeface:** `NEU_IMU_real`, `NEU_IMU2_real`, `GRAPH_IMU_real`, `GRAPH_IMU2_real` are sans-serif; their
   simulation counterparts and almost everything else are serif. Same builder family (`imu_terrain_real.py`).
2. **Palette:** `FigReal_Terrain_Latencies_4Panels` uses matplotlib default colors + dashed grid; physical `Plot_3`
   paints variance orange in all 4 scenarios (orange = Aversive elsewhere); `FigReal_Morphological_Transition_Energy`
   reuses blue/orange for transition direction.
3. **Legends:** sizes range 6.5 / 7 / 8 / 9 / 10 pt; some with a gray frame (`FigC`, `fig_transition_phases_v10`),
   most without. **Effective size in the PDF** varies from ~3.4 pt (`fig_stability_phases`) and ~5 pt
   (`fig_attempts_vs_noise_level`) to ~12–13 pt (`FigA`, `FigC`, ablation) because `figsize` differs by builder.
4. **Origin mark:** no figure says simulation vs physical except `GRAPH_IMU*` ("(Simulation)"/"(Physical)"),
   `fig1` ("simulation") and `Terrain_Latencies`. Per the letter this belongs in the **captions** (blocked on R2b-05, due Fri 2026-10-30).
5. **X-axis unit of the physical ECDF `Plot_1`:** (s) for Appetitive/Complex, (ms) for Aversive/Obstacle. ✔ confirmed in
   `real_plot_suite.py:100` (`use_ms` flag chooses per scenario) — a builder choice, not a data error. Unify to one unit.

## Real defects (legibility / error), not just style
- `fig2_Obstacle` legend "Roll RMS" struck through by data (✔ verified); `fig2_*` typo "Chasis" (✔).
- `NEU_IMU`, `NEU_IMU2`: X3..X13 labels overlap and are unreadable; "Time (s)" collides with the panel letter.
- `GRAPH_IMU2`: the "U_σaz threshold" annotation is crossed by the blue curve.
- `fig_classifier_tradeoff_fused`: legend 6.5 pt, xticks 7 pt in panel (a).
- `fig_stability_phases`: figsize 15×9.5 → ~3.4 pt effective text; suptitle with literal "---"; CoM marker still peeking at "SM=2.8 cm".
- `fig_ablation_complex_stability`: p-value labels overlap the "(deg)" descenders of the panel titles (**my R3b-02 figure**).
- Internal jargon inside images: "R3-04 dataset" (`fig_R2`), "StimuliB_t01…" (physical `Plot_3` ×4), "robot_cmd/NiMH" footnote
  (`FigReal_Morphological_Transition_Energy`), "Hardware Replicates (reconstructed)".
- Low resolution: `RES_IMU2.0_real` 789 px, `RES_EST_MUL` 966 px, `RES_IMU2.0` 1348 px.
- Titles inside the image duplicate the caption in 17+ figures (R1 even says "family" where the caption says "scenario").

## Fix map by builder (one change fixes a group)
| Builder / file | Figures | Change |
|---|---|---|
| `experiments/_plotting/style.py` (global) | all | legend defaults (frameon False, 10 pt), grid off, add `OUTCOME_COLORS`/`MODE_COLORS`, title policy |
| `builders/imu_terrain_real.py` | NEU_IMU(2)_real, GRAPH_IMU(2)_real, NEU_EST_*_real, Terrain_Latencies | regenerate in serif; Okabe-Ito palette; Terrain_Latencies grid/sizes |
| `builders/imu_dual_axis.py` | GRAPH_IMU, GRAPH_IMU2 | style colors, legend 10 pt, grid off, move threshold annotation |
| `builders/micro_dynamics.py` | 4 × `fig2_*_micro` | legend B outside data (Obstacle), 8→10 pt, "Chasis", line colors |
| `builders/real_plot_suite.py` | 4 × `Plot_1` ECDF, 4 × `Plot_3` | one x unit; non-orange variance; legend swatches; drop trial-ID suptitle |
| `build_neu_est` / `build_neu_imu` | NEU_EST_*, NEU_IMU(2) | font sizes ≥8 pt, overlapping labels, panel letters |
| `classifier_suite.py` (+ fig4, fused) | fig1/fig4/fused | tab10 → style colors; sizes; drop duplicate titles |
| `stability_phases.py`, `transition_phases.py`, `ecdf_phase_space.py`, `terrain_noise_sweep.py`, `build_mode_timelines.py`, `build_attempts_vs_nl.py`, `plot_ablation.py`, `build_tables.py` | rest | figsize, legend, palette, titles (see per-figure rows in the three agent reports) |
| **no builder** | 4 × `RES_*` sim captures, `RES_EST_UNI_real`, `RES_IMU2.0_real` | crop simulator UI ("67.56 %", "99.30 %", orange buttons); one numbering font; resolution — needs decision |
| **vectorized from CSV, no raw data** | `NEU_*`, `GRAPH_IMU*`, `stability_phases`, `transition_phases` | regenerate from `experiments/_plotting/vectorized/*.csv` only; never re-derive data |

## Proposed tiers (a decision for the author — deadline 2026-11-04)
- **Tier 1 (reviewer-visible, cheap):** global `style.py` legend/grid defaults; regenerate the 4 sans-serif IMU
  figures; fix `fig2_*` (legend, "Chasis"); `GRAPH_IMU2` annotation; `NEU_IMU(2)` labels; `fused` sizes; `stability_phases`
  figsize; strip internal jargon/IDs; unify the ECDF unit; ablation p-label overlap.
- **Tier 2:** palette collisions (variance orange, blue/orange reuse), remove duplicated in-image titles.
- **Tier 3 (decision):** the 6 raw simulator/photo `RES_*` captures — crop UI and unify numbering, or accept.
- Each regenerated asset goes through `scripts/promote_figure.sh --force`; one `C-xx` row + `patches/` record per
  batch; captions (simulation vs physical) only after R2b-05 is merged.

---

# ADDENDUM (2026-10-28, later) — author decisions, my own zoomed re-inspection, and the execution plan

## Author decisions (chat, 2026-10-28)
- **Serif everywhere** is the author's chosen typeface; the sans-serif figures must be regenerated in serif. This is the first thing to fix.
- `GRAPH_IMU` (sim) vs `GRAPH_IMU_real` show **different quantities** (σ_az + pitch vs MLP output states), so they are not like-for-like
  plots; only their typography/style is to be unified, not their content.
- **Tier 1 ("cheap and visible") is non-negotiable; Tier 2 also gets done.** All internal jargon listed above goes too.
- The author verified every finding above against the images except the p-value one (explained below).

## Re-inspection of the 9 physical figures the subagent did not zoom into (done by me, crops in the scratchpad, 2026-10-28)
Plot_1 ×4, Plot_3 Aversive/Obstacle, NEU_IMU2_real, GRAPH_IMU2_real, NEU_EST_MUL_real, RES_EST_UNI_real, RES_IMU2.0_real. Confirmed:
- **Plot_1 ECDF ×4:** serif, Okabe-Ito colors, no legend. Defects: x unit mixes s (Appetitive, Complex) and ms (Aversive, Obstacle);
  **y axis starts at 0.25–0.3 instead of 0** (an ECDF should span 0–1); the in-image title carries "(N=…)" that duplicates the caption.
- **🔴 Appetitive ECDF title says "N=4"** (the other three say N=3). The repo manifest and data also have 4 Appetitive folders
  (`StimuliB_t01..t04`), but the **manuscript caption says "three hardware replicates"** (`results.tex` ~l.875/894).
  Three sources say 4, one says 3. **Open question for the author: are there 4 Appetitive physical trials?** If yes, the manuscript
  text must change to four. This **supersedes** the instruction in `R2b-05_figure_caption_N_brief.md` ("keep three") — Sam must not
  settle it alone; update the brief once the author answers.
- **Plot_3 Aversive/Obstacle:** suptitle is an internal trial ID ("Aversive (trial StimuliR_t01)"); in Aversive the legend swatches
  ("Aversive/Appetitive stimulus in view") are nearly invisible on the shaded bands; legend ~8 pt top-left.
- **NEU_IMU2_real / GRAPH_IMU2_real:** sans-serif (DejaVu Sans), module titles and tick labels tiny, no panel letters, literal "--"
  in the GRAPH title ("... -- Inclined Slope (Physical)").
- **🔴 NEU_IMU2_real, panel "Locomotion 2 / X17" is completely empty.** If X17 is intentionally inactive here, an empty panel reads
  as an error to a reviewer. In simulation X17 is tonically active (see C-53). **Open question for the author: what should this panel show?**
- **NEU_EST_MUL_real:** serif, but a huge "a)" panel letter (~28 pt) sits between groups whose tick labels are ~6 pt.
- **RES_EST_UNI_real:** white page; a)/b)/c) in a geometric sans; numbers 1–6 already inside small white boxes.
- **RES_IMU2.0_real:** 789 px wide, numbers 1–6 in plain sans, black text on the photo, no box.

## The p-value item in `fig_ablation_complex_stability.png` (my R3b-02 figure) — what it actually is
Not a data error and not text printed over text. In each panel the p-label of the tallest bar sits directly under the panel title with no
margin; zoomed, the descender of the "g" of "(deg)" reaches the top of "p=0.004". They **touch, they do not overprint** → vertical-spacing
problem (raise `ylim` or the title pad). Two extra points on the same figure: each panel title repeats its y-label ("Roll RMS (deg)" twice)
and the image itself does not say what the error bars are (the caption now does: 95% CI). Rounding: image shows p=0.003, the prose p=0.0029.

## Idea for the `RES_*` simulator/photo captures (author's proposal, assessed)
Standard = **small white box + serif numeral** (already the look of `RES_EST_UNI_real`); letters a)/b)/c) re-typed in serif on the white
page background (easy: background is white). Cover the old glyph with a slightly larger white box, then draw the new label.
- Do it with a **reproducible script + coordinates config** under `experiments/R3b-04-res-labels/`, promoted with `promote_figure.sh --force`;
  never a hand-edited asset (repo rule). Pilot first on `RES_IMU2.0_real` (6 labels).
- Risks: the box may hide a few photo pixels; the new serif numeral will look sharper than the 789 px photo (acceptable).
- Orthogonal and still undecided: cropping simulator UI ("67.56 %", "99.30 %", orange button) from `RES_IMU`/`RES_EST_*`, and the ~40 % empty sky in `RES_IMU`.

## Execution plan (tiers are the author's; one `C-xx` row + `patches/` record per batch; `scripts/next_id.sh C` for IDs)
Environment: system python has no matplotlib/Pillow; `experiments/.venv_plotting` exists, and `uv` is available
(`uv run --with matplotlib --with numpy --with pillow python …`). Builders only read committed CSVs (physical: `experiments/real/`,
simulation: `experiments/simulation/`, vectorized: `experiments/_plotting/vectorized/`); never re-derive data.
1. **Batch 1 — global + typeface:** `style.py` (legend frameon False/10 pt, grid off, add `OUTCOME_COLORS`/`MODE_COLORS`, title policy, figsize
   targets); regenerate `NEU_IMU(2)_real`, `GRAPH_IMU(2)_real` in serif (via `imu_terrain_real.py`).
2. **Batch 2 — visible defects:** `fig2_*_micro` (Obstacle legend struck by data, "Chasis"→"Chassis", legend 10 pt); `GRAPH_IMU2` annotation;
   `NEU_IMU`/`NEU_IMU2` overlapping labels; `fused` sizes; `fig_stability_phases` figsize/suptitle/CoM marker; ablation p-label spacing; ECDF x unit + y from 0.
3. **Batch 3 — jargon and duplicated titles:** "R3-04 dataset", "StimuliB_t01…", "robot_cmd/NiMH" footnote, "Hardware Replicates (reconstructed)", titles that
   duplicate captions (17+), "---"/"--" literals, "family" vs "scenario".
4. **Batch 4 (Tier 2) — palette:** orange variance in physical `Plot_3`, blue/orange reuse in `Energy`, `Terrain_Latencies` tab10, `fig4`/`fused`/`stability_phases`
   hardcoded colors → semantic aliases from `style.py`.
5. **Batch 5 — `RES_*` labels** (after the pilot is approved) and resolution/UI decisions.
6. **Last:** captions "simulation vs physical" in `results.tex` (needs R2b-05 merged, due Fri 2026-10-30); compile the PDF; only then the Overleaf push (author, token).
Blocking questions for the author: (a) Appetitive physical N = 3 or 4; (b) what `NEU_IMU2_real` "Locomotion 2 / X17" must show; (c) approve the `RES_*` pilot.
