# Figure-regeneration candidates for further merging — for the team, not yet executed

**Status:** 🔲 Reference list only, no `sections/*.tex` or `experiments/*` edits made from this doc.
Split out from `intake/processed/figure_merge_audit.md` (`C-26`/`C-27`) — this is a wider, more
aggressive second pass over the same figure inventory, looking specifically for anything left after
those two patches, including candidates that need touching `experiments/_plotting/` before a merge
is safe.

**Origin:** author request (2026-08-31) — a handoff list for a teammate to execute; be aggressive,
list everything plausible even if some items carry real risk, so the team can triage rather than me
silently dropping borderline candidates.

## Group 1 — No image regeneration needed (pure `sections/*.tex` merges, same class as `C-26`)

These have **no baked-in letters and no internal-panel prose references** — they were simply missed
in the `C-26` pass, not excluded for a technical reason. Lowest risk, fastest to execute.

### 1a. `fig:robot` + `fig:pata` (methodology.tex, lines 11–22)

Two consecutive 3D CAD renders — "3D design of the quadruped robotic platform" (`0.5\textwidth`,
`angle=-7`) and "3D design of the robotic limb" (`0.4\textwidth`) — introduced back-to-back, each
referenced once in plain prose with no letter suffix. Merge into one 2-subfigure figure, same
mechanical pattern as `C-26`'s `Terreno_irre`/`Terreno_incli` fusion. **Only wrinkle:** `fig:robot`
uses `angle=-7` (rotated render) — keep that per-subfigure, it's independent of the outer subfigure
wrapper.

### 1b. `fig:appetitive_micro` + `fig:aversive_micro` + `fig:obstacle_micro` + `fig:complex_micro` (results.tex, lines ~66–125)

Four simulation "representative trial" figures, one per scenario (Appetitive Targeting, Aversive
Escape, Obstacle Evasion, Complex Navigation), each `0.75\textwidth`, each referenced once in plain
prose ("see Figure~\ref{fig:appetitive_micro}", "Fig.~\ref{fig:complex_micro}") — **no letters, no
regen needed.**

**Precedent argues strongly for merging:** `fig:noise_robustness_grid`'s own caption in this exact
subsection says it "fuses what were four separate per-scenario robustness figures into one" — i.e.
this exact merge (4 parallel per-scenario simulation figures → 1 grid) was already done once, for a
different figure set, in the same subsubsection. A 2×2 grid (same shape as `fig:mlp_eval_grid`,
already accepted in `C-19`) is the obvious layout.

**Counter-argument (why this wasn't just done automatically):** each of these 4 figures currently
sits immediately next to its own scenario paragraph — a reader gets the figure right where its
prose discusses it. Merging into one grid means either (a) placing the grid once, after all 4
paragraphs, so the first 3 scenarios' prose no longer has an adjacent figure, or (b) keeping the grid
near the last paragraph and accepting that the first-mentioned scenarios' figure is now a page or two
later than its own discussion. `C-19` faced this same tension for the physical-scenario `*_real_compound`
quad and the author explicitly said **do not merge** those 4 — but that precedent cuts the other way
from `fig:noise_robustness_grid`'s own precedent for *this* subsubsection. Genuinely a coin-flip; flagging
aggressively here specifically so the author can make the call with both precedents in view, not
because the case is one-sided.

**Estimated savings:** 4 figure environments → 1, `~4×0.75\textwidth` singles → one `figure*` 2×2 grid.

### 1c. `fig:MLP` + `fig:DATOSMLP` (methodology.tex, lines ~360–390)

MLP network-structure diagram (`0.6\textwidth`) and its input-vector diagram (`0.8\textwidth`) —
conceptually paired (structure, then what feeds it) but currently **not adjacent**: `table:DIR_BINARY`
(the 3-bit motion-code table) sits between them. To merge, move the table to *after* both figures (or
before both) — a small reordering, not a content change, but touches more of the surrounding prose
flow than 1a/1b, so slightly higher risk of an awkward read-order. Flagged because it's still
achievable without any image regeneration.

## Group 2 — Needs image regeneration (baked-in group letters, same family as `NEU_IMU`)

These all use the same `build_neu_est`/`build_neu_imu` builders
(`experiments/_plotting/builders/imu_terrain_real.py`) with `group_letters` set, meaning the
letters are drawn as pixels into the PNG and are what `results.tex` cites by manually-typed suffix
(`Figure~\ref{fig:X}a`, `...b`, etc.) — merging any pair here means regenerating without letters,
verifying the regen, promoting, merging in LaTeX, and rewording every prose sentence that relies on
the old letter meaning. Same procedure as `NEU_IMU`/`NEU_IMU2` below; only the specifics differ.

### 2a. `NEU_IMU` + `NEU_IMU2` (simulation, results.tex) — already scoped in detail

- **Where:** `results.tex`, `\subsubsection{Response to Variable Topographies}` (simulation), two
  figures ~15 lines apart (`fig:NEU_IMU`, `fig:NEU_IMU2`), `0.5\textwidth`/`0.4\textwidth`.
- **Letters:** built by `regenerate_neu_panels.py` with `group_letters={"Locomotion_1": "a",
  "Decision_1": "b"}` for both.
- **To do it properly:**
  1. Drop the `group_letters` kwarg from the two `NEU_IMU`/`NEU_IMU2` call sites in
     `regenerate_neu_panels.py` (lines ~68–71) — leave `NEU_EST_UNIB`/`UNIG`/`MUL` calls untouched.
  2. Regenerate, diff against the currently published `assets/NEU_IMU.png`/`NEU_IMU2.png` (same
     traces, just without the drawn letters).
  3. `scripts/promote_figure.sh --force` both into `assets/`.
  4. Merge into one 2-subfigure figure in `sections/results.tex` (pattern: `patches/c-27-neu-imu-real-merge.tex`).
  5. Reword the two sentences currently saying "Figure~\ref{fig:NEU_IMU2}a"/"...b" (they mean
     "Locomotion Module"/"Gait Decision Module" group *inside* that image — after the merge, `a`/`b`
     means "irregular"/"inclined" terrain instead). Name the panel directly instead.
  6. Normal flow: `next_id.sh C` → `validate_tex.sh`/`check_roundtrip.sh` → `compile_pdf.sh` (check
     page count — `C-27`'s equivalent physical-pair merge moved it by 1 page, this one may or may
     not) → `PROGRESS.md` row → `patches/` record.

### 2b. `NEU_EST_UNIB` + `NEU_EST_UNIG` (simulation, results.tex, lines ~38–53)

Two single-stimulus rasters: `NEU_EST_UNIB` (appetitive, letters a=Locomotion, b=Gait Decision) and
`NEU_EST_UNIG` (obstacle, letters a=Lidar, b=Locomotion, c=Gait Decision), both `width=1.0\textwidth`.
Checked the actual citation count (grep `fig:NEU_EST_UNIB`/`fig:NEU_EST_UNIG` in `results.tex`): only
**one** letter-suffixed reference exists across both — "Figure~\ref{fig:NEU_EST_UNIG}b shows the
activations of the locomotor decision network" (line 45) — every other citation to either figure is
already plain (no letter). So the reword step here is smaller than `NEU_IMU`'s, even though the
regeneration/promotion mechanics are identical. **Bonus motivation beyond simplification:** the
physical side has *already* consolidated the equivalent obstacle+appetitive content into **one**
combined image (`NEU_EST_UNIG_real` covers both stimuli, per `C-18`) — merging the simulation pair
would bring simulation's structure in line with physical's already-leaner one, not just save space.
Regeneration means dropping `group_letters` from both `build_neu_est(...)` calls in
`regenerate_neu_panels.py` (lines ~39–53), then rewording that one line-45 citation.

### 2c. `NEU_EST_MUL` (simulation) + `NEU_EST_MUL_real` (physical) — cross-domain pairing, biggest job in this doc

A different kind of merge from everything else here: instead of pairing two terrain/stimulus variants
*within* one domain, this pairs the **same** multi-stimulus scenario across simulation and physical —
"compare sim vs. hardware for the identical trial type" is a naturally reviewer-friendly framing. Both
images are full-width, both have 4 baked group letters (a=Basal Ganglia, b=Lidar, c=Locomotion,
d=Gait Decision — identical letter scheme on both sides, see `regenerate_neu_panels.py` lines 57–66
for sim and `imu_terrain_real.py`'s `__main__` for physical). Regenerating both, merging, and
rewording touches **two separate results.tex subsections** (Simulation Results' "Response to Multiple
Stimuli" and Physical Implementation Results' "Response to Multiple Stimuli") and, per an actual grep
count, **7 letter-suffixed citations total** across both (sim: `fig:NEU_EST_MUL}b/c` at line 111,
`}a` at line 113, `}d` at line 117; physical: `fig:NEU_EST_MUL_real}b` at line 507, `}d` at line 516,
`}c` at line 551 — most of these are `C-25`'s already-tightened prose, so reword carefully to keep
that tightening intact). **Not for a first pass** — flagging because it's a
real, structurally distinct merge opportunity, but budget it as the largest item in this document.

## Group 3 — Reviewed, flagged but not recommended to execute

- **`Modos_Locomocion` / `Modos_LocomocionV2`** (methodology.tex, full-width gait-decision network
  diagrams, before/after the MLP integration). No letters, no regen needed — a pure layout call
  (shrink both to `~0.48\textwidth` side by side). Not recommended: these are dense circuit diagrams
  read closely for the connectivity change between versions; halving their width risks illegible
  neuron/synapse labels. Listed only so the team has the full inventory, not as a real suggestion.

## Priority order, if the team wants one

1. **1a, 1b, 1c** — no regeneration, same risk profile as the already-merged `C-26` pairs. Do these
   first regardless of appetite for the `experiments/` work below.
2. **2a** (`NEU_IMU`/`NEU_IMU2`) — smallest regeneration job, already fully scoped.
3. **2b** (`NEU_EST_UNIB`/`NEU_EST_UNIG`) — same mechanics as 2a, more citations to track down, but
   comes with the added bonus of fixing a real sim/physical structural asymmetry.
4. **2c** (`NEU_EST_MUL` cross-domain) — biggest, most citations, most files touched; do last, or
   skip if the team decides the page-count return isn't worth the risk surface.
5. **Group 3** — skip unless someone specifically wants to revisit the diagram-legibility tradeoff.
