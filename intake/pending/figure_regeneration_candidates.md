# Figure-regeneration candidates for further merging — for the team, not yet executed

**Status:** 🔲 Reference list only, no `sections/*.tex` or `experiments/*` edits made from this doc.
Split out from `intake/processed/figure_merge_audit.md` (`C-26`/`C-27`) — those two applied every
merge that was possible with a caption/layout-only patch; the items below all need someone to touch
the plotting pipeline in `experiments/_plotting/` and regenerate a PNG before a merge is safe.

**Origin:** author request (2026-08-31) — a handoff list for a teammate to execute, since these go
beyond what a caption/layout patch can safely do.

## Background: why these weren't merged already

`C-26` merged 3 pairs of small figures (terrain photos, 2× IMU-signal plots) into subfigures purely
by editing `sections/*.tex` — no image changes needed. `C-27` found and merged a 4th pair
(`NEU_IMU_real`/`NEU_IMU2_real`) the same way, once a wrong assumption in `C-26` was corrected.

The pair below is different: its **source images have letters/labels physically drawn into the
pixels** by the plotting script, which would visually collide with the automatic (a)/(b) lettering
LaTeX adds when two figures are wrapped into one `subfigure` pair. Merging these safely means
regenerating the PNG without the baked-in letters first — a job for whoever owns
`experiments/_plotting/`, not a text-only patch.

## Candidate: `NEU_IMU` + `NEU_IMU2` (simulation, results.tex)

- **Where:** `results.tex`, `\subsubsection{Response to Variable Topographies}` (simulation), two
  figures currently ~15 lines apart (`fig:NEU_IMU`, `fig:NEU_IMU2`), `0.5\textwidth`/`0.4\textwidth`.
- **Why merge:** identical caption template ("Neural activations during locomotion over
  {irregular,inclined} terrain (simulation). (a) Locomotion decision module; (b) Gait mode control
  module") — same shape as the `NEU_IMU_real`/`NEU_IMU2_real` pair `C-27` already merged.
- **What's blocking it:** built by
  `experiments/N-01-simulation-figure-regeneration/scripts/regenerate_neu_panels.py`, which calls
  `build_neu_imu(..., group_letters={"Locomotion_1": "a", "Decision_1": "b"})` — the
  `imu_terrain_real.py` builder function's `_place_group_letter()` draws literal "(a)"/"(b)" text
  into the image at render time. (The physical pair `C-27` merged was generated *without*
  `group_letters` — that's the only reason that merge was possible without a regen; the sim pair is
  built with letters on purpose.)
- **To do it properly:**
  1. Regenerate `NEU_IMU.png`/`NEU_IMU2.png` by calling `build_neu_imu(...)` **without**
     `group_letters` (i.e., drop that kwarg from the two `NEU_IMU`/`NEU_IMU2` call sites in
     `regenerate_neu_panels.py`, lines ~68–71 — leave the `NEU_EST_UNIB`/`UNIG`/`MUL` calls in the
     same file untouched, their letters are load-bearing for different, already-correct citations).
  2. Confirm the regenerated PNGs still match the expected data (diff against the currently published
     `assets/NEU_IMU.png`/`NEU_IMU2.png` — same neural traces, just without the drawn letters).
  3. `scripts/promote_figure.sh --force` both into `assets/`.
  4. In `sections/results.tex`, merge the two `\begin{figure}` blocks into one 2-subfigure figure
     (same pattern as `patches/c-27-neu-imu-real-merge.tex`), keeping labels `fig:NEU_IMU`/
     `fig:NEU_IMU2` on the inner subfigures.
  5. **Reword the prose** — two sentences currently say "Figure~\ref{fig:NEU_IMU2}a" / "...b" (results.tex,
     `\subsubsection{Response to Variable Topographies}`, simulation), using a manually-typed letter
     to mean "that image's Locomotion Module / Gait Decision Module group." After the merge, `a`/`b`
     means "irregular terrain" / "inclined terrain" instead — same collision `C-27` fixed for the
     physical pair. Reword to name the panel directly (e.g., "Figure~\ref{fig:NEU_IMU2}, Gait
     Decision Module panel") instead of the bare letter.
  6. `next_id.sh C` → `validate_tex.sh`/`check_roundtrip.sh` → `compile_pdf.sh` (check page count —
     `C-27`'s equivalent physical-pair merge moved the count by 1 page; this one may or may not) →
     `PROGRESS.md` row → `patches/` record, same flow as `C-26`/`C-27`.

**Estimated effort:** small-medium — mostly mechanical once someone has the plotting venv set up
(`experiments/.venv_plotting/`, see `experiments/N-01-simulation-figure-regeneration/README.md`);
the risk is entirely in step 2 (confirming the regen didn't silently change anything else) and step 5
(getting the reworded sentences right).

## Reviewed, not recommended as a regeneration target

- **`Modos_Locomocion` / `Modos_LocomocionV2`** (methodology.tex, full-width gait-decision network
  diagrams) — flagged in the original figure-merge audit (item D) as structurally parallel but too
  dense to shrink to subfigure width without hurting legibility. Not a letter-collision problem like
  `NEU_IMU`, so no image regen needed even if the team decides to attempt it — it would be a pure
  layout call (shrink both to `~0.48\textwidth` side by side). Listed here only because it's the one
  other "maybe" left from the earlier audit; if pursued, treat it as a fresh layout-only decision, not
  bundled with this doc's `NEU_IMU` regeneration work.
