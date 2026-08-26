# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Revision-tracking + AI-patching layer for manuscript `ROBOT-D-26-00122R1` (*Robotics and Autonomous Systems*),
deadline **August 31, 2026**. The manuscript is edited by non-technical co-authors on Overleaf. **All real work
happens in this repo** — text patching, asset management, compilation. The sibling Overleaf repo clone is
sync-only. Full spec: **README.md — read it before implementing any script here**, it is the source of truth for
file formats, script behavior, and naming.

## Token-efficient editing (read `OUTLINE.md` first)

For any section-level edit: read `OUTLINE.md` (cheap global context) + the relevant `PROGRESS.md` row + only the
target `sections/<slug>.tex` file(s). Do not read `source/main_monolithic.tex` as a default move — it's the full
monolith and defeats the point of `sections/`. Only read additional section files, or the monolith, when the
requirement itself genuinely spans sections and `OUTLINE.md` doesn't resolve it.

## Processing an `intake/` document

`intake/pending/*.md` is the entry point for anything that isn't a reviewer requirement — new content to write up
(e.g. a teammate's implementation) or a loose list of corrections. Read `OUTLINE.md` first, then the doc, then (only
if it references one) the specific files it points to in a repo listed in `intake/SOURCES.md` — read-only, never
edit outside `paper-revision/`. For each distinct change found, add a `PROGRESS.md` row with the next `N-xx` (new
content) or `C-xx` (correction) ID, its `Category` (Escritura/Pruebas/Métricas) and `Owner`, then follow the
normal patch flow. If the change needs a figure/plot that
doesn't exist yet (common for write-ups of a teammate's simulation/hardware work), set that row's `Data source`
to `experiments/<id>-<slug>/` and follow README.md §9 before touching `sections/`. `git mv` the doc to
`intake/processed/` once every change it produced has reached `applied` or later.

## Hard rules

- Never edit `source/main_monolithic.tex` by hand. It is generated: written by `scripts/pull_from_overleaf.sh`
  (from Overleaf) or `scripts/reassemble.py` (from `sections/`).
- Never edit `sections/*.tex` filenames or `manifest.json` order outside `scripts/split_sections.py` — it fully
  regenerates `sections/` on every run. Edit section **content** in place. Filenames have no numeric prefix; order
  lives only in `sections/manifest.json`.
- `split_sections.py`/`reassemble.py` must round-trip byte-identically with no edits in between (`scripts/
  check_roundtrip.sh` verifies this) — never insert separators or normalize whitespace during split/join.
- `assets/` mirrors the Overleaf project 1:1 (bibliography, figures, class files), under original relative paths.
  Editable in place; mirrors back on push.
- The Overleaf repo clone is **sync-only** — never hand-edit files there.
- `scripts/pull_from_overleaf.sh` must abort if any commit since the last `sync:`/`chore: mark synced` marker
  touches `source/`, `sections/`, or `assets/` — that means local work isn't pushed yet, and pulling would
  silently overwrite it. This is a git-log check, not a `PROGRESS.md`-only check — it must catch every local
  change, not just ones tied to a tracked reviewer ID.
- Every edit, however small, goes through `sections/` + a `PROGRESS.md` row + a `patches/` record — no untracked
  "quick edit" path. This is what lets the pull guard trust marker-less history as proof nothing is unsynced.
- `scripts/push_to_overleaf.sh` must always `git pull` the Overleaf repo first and abort on new commits, run
  `scripts/validate_tex.sh` (+ `compile_pdf.sh` if available) before pushing, and on success commit an empty
  `chore: mark synced to Overleaf` marker in this repo — never force-push, never auto-merge, never push
  unvalidated LaTeX.
- All scripts read shared paths from `scripts/config.sh` — never hardcode `OVERLEAF_DIR`, `ASSETS_DIR`, or
  `source/main_monolithic.tex` elsewhere.
- Never write the Overleaf git token (`olp_...`) into any file in either repo — it lives only in
  `~/.git-credentials` via `git config --global credential.helper store`.
- Text-processing scripts (`split_sections.py`, `reassemble.py`, `find_section.py`, `validate_tex.sh`,
  `check_roundtrip.sh`) are bash/Python-stdlib only — no LaTeX parser. `compile_pdf.sh` and scripts under
  `experiments/*/scripts/` are the only ones allowed to depend on external tooling (LaTeX distribution;
  numpy/matplotlib/pandas/ROS 2/etc. respectively).
- A `PROGRESS.md` row that needs a figure/number that doesn't exist yet gets a `Data source` value pointing at
  `experiments/<id>-<slug>/` — never generate that data ad hoc outside `experiments/`, and never place a new
  file directly into `assets/` by hand. `scripts/promote_figure.sh` is the only path from
  `experiments/*/output/` into `assets/`; it refuses to overwrite an existing asset without `--force`.
  `experiments/*/data/` is gitignored (raw/regenerable); `experiments/*/output/` (final figures/CSVs) is
  committed. See README.md §9.
- Keep `sync:` commits (pulling Overleaf), `patch:` commits (applying a reviewer fix), and `chore: mark synced`
  commits (marking a push) separate — never combine them.
- Never hand-pick an `N-xx`/`C-xx` ID — get it from `scripts/next_id.sh N` / `scripts/next_id.sh C` (max seen + 1,
  never reused). `R2-xx`/`R3-xx` stay the fixed reviewer list from README.md §6.
- `scripts/check_hardcoded_refs.sh` and `scripts/check_target_conflicts.sh` are advisory-only — they never block
  a commit or push, they just print. Don't skip reading their output when it's non-empty; don't treat their
  silence as a guarantee either (§10.4 is deliberately coarse).
- Run `scripts/install_hooks.sh` once per clone (and again if `scripts/hooks/pre-commit` changes) — installs the
  pre-commit hook that regenerates `source/main_monolithic.tex` and runs `validate_tex.sh`/`check_roundtrip.sh`
  whenever a commit touches `sections/` or `source/`, and regenerates `docs/data.json` whenever `PROGRESS.md`
  changes. See README.md §10.2/§12.
- `docs/data.json` is generated by `scripts/build_dashboard.py` from `PROGRESS.md` — never hand-edit it, same
  rule as `source/main_monolithic.tex`. When adding/reassigning a `PROGRESS.md` row, always fill in its
  `Category` and `Owner` columns — that's what the GitHub Pages dashboard (`docs/`) renders. See README.md §12.
- **Revision-round color convention**: any new or materially changed text written into `sections/*.tex` this
  round — reviewer fixes, `intake/` write-ups, corrections, everything — must be wrapped in `\revblue{...}`
  (defined in `sections/preamble.tex`). Pure typo fixes with zero meaning change can skip it; default to
  wrapping otherwise. At the *start* of the *next* revision round (not this one), run
  `scripts/strip_revblue.py --apply` once to turn this round's accepted `\revblue{}` back into plain baseline
  text before that round's new edits begin. See OUTLINE.md's "Revision convention" section for full detail and
  current state.

## Key files

- `README.md` — full architecture, script specs, file formats. Treat as the spec to implement against.
- `RESUMEN.md` — Spanish-language general-understanding companion doc. Not the spec; README.md wins on
  any conflict. Update it when a change affects what it describes (deadline, status, folder roles).
- `OUTLINE.md` — hand-maintained global summary (abstract, per-section one-liner, key terms, cross-references).
  Read this, not the monolith, for context.
- `PROGRESS.md` — status per reviewer requirement (`pending` → `drafted` → `applied` → `synced-to-overleaf`). Check
  before starting new patch work; update after.
- `patches/<id>-<slug>.tex` — audit copy of each applied change, not the live file (that's `sections/<slug>.tex`
  or `assets/`).
- `intake/pending/` / `intake/processed/` — raw docs waiting to be triaged into `PROGRESS.md` rows / already fully
  triaged. `intake/SOURCES.md` — registry of sibling repos readable (not writable) as reference material.
- `experiments/<id>-<slug>/` — scripts/notebooks/data that generate a figure or table that doesn't exist yet,
  before it's promoted into `assets/`. `experiments/README.md` — short pointer + layout. `_TEMPLATE/` — copy to
  start a new one.
- `build/` — gitignored, disposable compile output. Never commit anything from it.
- `docs/` — GitHub Pages traceability dashboard (category/owner/status per `PROGRESS.md` row). `data.json` is
  generated by `scripts/build_dashboard.py` — never hand-edited.

## Commands

All implemented under `scripts/` (see README.md §5/§9/§10/§12 for exact behavior). Daily loop:
`pull_from_overleaf.sh` → `find_section.py` → read `OUTLINE.md` + target `sections/`/`assets/` →
(if `Data source` is set, generate via `experiments/` + `promote_figure.sh` first) → edit →
`reassemble.py` → `validate_tex.sh` / `compile_pdf.sh` → `push_to_overleaf.sh`. One-time per clone:
`install_hooks.sh`. As needed: `next_id.sh`, `check_target_conflicts.sh`, `build_dashboard.py`
(auto-runs from the pre-commit hook when `PROGRESS.md` changes — manual run only needed if the
hook isn't installed or was bypassed with `--no-verify`).
