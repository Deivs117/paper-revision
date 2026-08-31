# Figure-merge / structural-consolidation audit — A+B(partial)+C applied as C-26

**Status:** ✅ Author decided (2026-08-31) to proceed with A+B+C. Applied as `C-26`:
- **A** (Terreno_irre/Terreno_incli) — applied as planned.
- **B** — applied *partially*: `GRAPH_IMU`/`GRAPH_IMU2` and `GRAPH_IMU_real`/`GRAPH_IMU2_real` merged.
  `NEU_IMU`/`NEU_IMU2` and `_real` counterparts were **excluded during execution** — found their
  captions' "(a)"/"(b)" letters are baked into the source PNG itself (referenced in prose as
  "Figure~\ref{fig:NEU_IMU2}a"), so wrapping them in outer LaTeX subfigure (a)/(b) labels would create
  ambiguous double-lettering. This downgrades the original B assessment; fixing it properly would
  require regenerating the source images (out of scope for a caption/layout-only patch).
- **C** (RES_IMU/RES_IMU2) — applied as planned, stacked 2-row figure.

`compile_pdf.sh` recompiled with **zero warnings** (no undefined refs, no float-too-large) at **89
pages** — unchanged from the `C-25` baseline; this round's float-count reduction (14 → 9 figure
environments) did not by itself cross a page boundary. 3 of 4 merged figures visually spot-checked via
rasterized PDF pages. D/E/F/G stay reviewed-and-declined as originally written; NEU_IMU pairs join that
list. See `PROGRESS.md` row `C-26` and `patches/c-26-figure-merges.tex`.

**Origin:** author request (2026-08-31, in-chat, follow-up to the reviewer-simulation trim audit) —
"dami una lista de graficas que se podrian fusionar o de secciones... que se podria hacer lo mismo,"
reading as a reviewer looking specifically at **figure count/layout** and **section structure**, not
prose. Distinct from `intake/processed/reviewer_simulation_trim_audit.md` (prose/caption trimming,
already fully applied as `C-22`–`C-25`) and `intake/processed/redundancy_closing_audit.md` (cross-section
fact restatement, `C-20`/`C-21`).

## Method

Inventoried every `\begin{figure}`/`\begin{figure*}` in `introduction.tex`, `methodology.tex`,
`results.tex` (75 figure environments total) by width, caption, and adjacency to its sibling(s), looking
for pairs/sets that are: same visual type, same caption template, physically adjacent in the file, and
not already merged. Cross-checked against `PROGRESS.md`'s `C-19` (already fused the MLP-eval 4-panel grid
and the stimulus-photo pairs — that's the established, already-accepted pattern this audit reuses) and
`R2-01`/`C-19`'s explicit decision **not** to merge the four `*_Real_compound` per-scenario figures
(results.tex lines 741–826) when the author considered it and said keep them separate — that precedent is
respected below (item F is flagged, not recommended).

## Candidates, ranked by confidence

### A. High confidence, low risk — `Terreno_irre` / `Terreno_incli` (methodology.tex, lines 477–488)

Two physical-terrain photos, both `width=0.48\textwidth`, immediately consecutive in the file, referenced
in the same sentence ("...is shown in Figure~\ref{fig:Terreno_irre}, while the inclined setup is shown in
Figure~\ref{fig:Terreno_incli}"). This is the **exact same pattern** as `fig:estimulos_reales` two figures
above it in the same file (two `0.23\textwidth` stimulus photos already merged into one 2-subfigure
figure) — just not yet done for the terrain photos. Merge into one figure, (a) Irregular terrain / (b)
Tilted terrain, each subfigure at `~0.48\textwidth` (fits side by side unchanged).

**Risk: low.** Identical to an already-accepted pattern in the same file, same section, same author.

### B. High confidence, low-medium risk — the four small IMU/MLP companion-figure pairs (results.tex)

Two terrain scenarios (irregular / inclined) are each documented with a 3-figure set
(trajectory-snapshot / neural-raster / IMU-or-MLP-graph), once in simulation and once physical — 12
figures total for what is structurally 4 repeating pairs. Two of those four pairs are already small
(`\leq 0.7\textwidth`) and purely parallel in caption template:

- `fig:GRAPH_IMU` (`0.7\textwidth`, "Std. dev. of accel-Z during transport on unstable terrain") +
  `fig:GRAPH_IMU2` (`0.5\textwidth`, "Pitch angle during motion in a steeply sloping terrain") — same
  family (IMU signal vs. time, one per terrain), consecutive-ish (separated only by one paragraph),
  simulation.
- `fig:GRAPH_IMU_real` (`0.5\textwidth`) + `fig:GRAPH_IMU2_real` (`0.5\textwidth`) — identical caption
  template ("MLP outputs and IMU state timeline on {uneven,inclined} terrain"), physical counterpart of
  the above.
- `fig:NEU_IMU` (`0.5\textwidth`) + `fig:NEU_IMU2` (`0.4\textwidth`) — identical caption template
  ("Neural activations during locomotion over {irregular,inclined} terrain (simulation). (a) Locomotion
  decision module; (b) Gait mode control module") — note each is *already* a 2-panel composite image
  (baked-in a/b), so merging the pair would produce one figure with 4 labeled panels (a/b irregular,
  c/d inclined), same pattern as `fig:mlp_eval_grid`'s 2×2 fusion in `C-19`.
- `fig:NEU_IMU_real` (`0.4\textwidth`) + `fig:NEU_IMU2_real` (`0.4\textwidth`) — physical counterpart,
  same caption template and already-composite a/b images.

**Estimated savings:** 4 fusions, 8 figures → 4. Each pair is small enough that side-by-side placement
at `\sim0.45$–$0.5\textwidth` per subfigure loses no legibility versus its current standalone width.

**Risk: low-medium.** Purely a layout change (no caption content lost, same images), but touches 4
separate spots across the file — more surface area than item A, and `NEU_IMU`/`NEU_IMU2` becoming a
4-label (a–d) figure needs its 2 in-prose reference sentences ("Figure~\ref{fig:NEU_IMU}",
"Figure~\ref{fig:NEU_IMU2}a") updated to the new sub-labels — mechanical but must be done carefully to
not break a cross-reference (same caution flagged in `C-19`'s own PROGRESS.md row about concurrent-edit
clobbering).

### C. Medium confidence, low risk — `fig:RES_IMU` / `fig:RES_IMU2` (results.tex, simulation trajectory strips)

Both are `width=1.0\textwidth` snapshot-strip photos (poses every 22s / 12s) documenting the two terrain
scenarios' trajectories. Unlike item B's pairs, these are already full-width, so merging into one figure
with two stacked full-width rows doesn't shrink either image — the saving here is purely in reduced float
count/caption overhead (one caption instead of two, one float placement instead of two), which may or may
not move the page count (same caveat as the previous audit — LaTeX float packing is non-linear).

**Risk: low**, but **savings uncertain** — recommend only if a recompile after item A+B confirms there's
still page-count headroom to chase; otherwise this one is cosmetic (fewer floats, not necessarily fewer
pages).

### D. Low confidence — `fig:Modos_Locomocion` / `fig:Modos_LocomocionV2` (methodology.tex, gait-decision network diagrams)

Both `width=\textwidth` — the original 3-mode gait-decision network and its MLP-informed V2 successor.
Structurally parallel (same subsection, sequential presentation of "before" and "after" the MLP
integration) but each is a dense full-width circuit diagram; shrinking either to `~0.48\textwidth` for a
side-by-side layout risks making the neuron/synapse labels illegible.

**Not recommending** — flagging only because the pair is structurally analogous to the fusions above;
the risk/reward here is inverted (these are read closely for the connectivity change between versions,
unlike the terrain photos which are illustrative-only).

### E. Reviewed, not flagged — `fig:MLP` / `fig:DATOSMLP` (methodology.tex)

Sequential MLP-related figures (network structure, input vector) but a full table
(`table:DIR_BINARY`) sits between them in the current layout — not adjacent, and reordering to make them
adjacent would itself be a bigger structural change than a caption/layout audit should recommend
unilaterally. Not flagged as a cut target.

### F. Reviewed, not flagged (precedent already set) — the four `*_Real_compound` scenario figures

`fig:appetitive_real_compound` / `aversive_real_compound` / `complex_real_compound` /
`obstacle_real_compound` (results.tex lines 741–826) are structurally identical in template (ECDF +
coupled neural/kinematic panel, three hardware replicates each) — the same shape of "4 parallel
per-scenario figures" as the ones fused in item B above. **Not flagging as new** because `C-19`
(2026-08-29) already put this exact question to the author for the photo-equivalent set and got an
explicit "no, do not merge/remove any of the 4" — the reasoning there (each figure is discussed in its
own dedicated paragraph immediately before it; merging would either separate the figure from its prose
or force all 4 scenarios' discussion to be read before seeing any of them) applies identically here.
Listed for completeness, not as an actionable item.

### G. Reviewed, not flagged — section-level restructuring (Simulation vs. Physical quantitative-analysis asymmetry)

`OUTLINE.md` already notes an asymmetry: simulation's per-scenario quantitative validation lives as
`\subsubsection`s *inside* `\subsection{Simulation Results}`, while the physical counterpart is pulled out
into its own top-level `\subsection{Quantitative Performance Analysis in Physical Multi-Stimuli and
Variable Terrain Environments}` (`ssec:QuantReal`). This is the structural root of what **R2-01** flagged
as duplication — but R2-01 is already `synced-to-overleaf`, resolved via **prose condensation and a
shared consolidated table**, not a hierarchy rewrite. Reopening the section structure now, on a paper
already once revised and now in its second revision round with a reviewer who has seen the prior
structure, is a much larger and riskier change than anything in this audit (renumbers subsection labels,
risks breaking cross-references throughout `sections/*.tex`, and second-guesses a reviewer item the team
already closed). **Not recommended.**

## Total estimate and honest caveat

Items A+B+C together: 5 figure-pair fusions (Terreno ×1, GRAPH_IMU ×2, NEU_IMU ×2, RES_IMU ×1 — 11
figures → 6 figures, net −5 float environments). Unlike the prose trims in the previous audit, page-count
impact from float-count reduction is genuinely harder to predict without a recompile — LaTeX's float
placement can absorb a removed float into existing whitespace around a page break, or it can do nothing.
Recommend: apply A (trivial, same pattern as an already-accepted fix) first as a `C-xx`, recompile and
measure; then decide on B/C based on the real delta, same protocol the last audit used successfully
(`C-20`→measure→`C-25` produced the real page-count movement, not the earlier items).

## Next step

Awaiting author decision on: (1) proceed with A only, (2) A+B, (3) A+B+C, (4) hold entirely. D/E/F/G are
flagged as reviewed-and-declined, not open decisions, unless the author explicitly wants to revisit one.
Once decided, follow the normal `next_id.sh C` → edit → `validate_tex.sh`/`check_roundtrip.sh` →
`compile_pdf.sh` → `PROGRESS.md` row → `patches/` record flow, same as the prior two audits.
