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
   `fig1` ("simulation") and `Terrain_Latencies`. Per the letter this belongs in the **captions** (blocked on R2b-05, due Thu 2026-10-29).
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
