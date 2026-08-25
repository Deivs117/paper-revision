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
content) or `C-xx` (correction) ID, then follow the normal patch flow. `git mv` the doc to `intake/processed/` once
every change it produced has reached `applied` or later.

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
  `check_roundtrip.sh`) are bash/Python-stdlib only — no LaTeX parser. `compile_pdf.sh` is the only script allowed
  to depend on external tooling (a LaTeX distribution).
- Keep `sync:` commits (pulling Overleaf), `patch:` commits (applying a reviewer fix), and `chore: mark synced`
  commits (marking a push) separate — never combine them.

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
- `build/` — gitignored, disposable compile output. Never commit anything from it.

## Commands

Not yet implemented — see README.md §"Repository Setup & Execution Guide" for what to build and the daily loop
(`pull_from_overleaf.sh` → `find_section.py` → read `OUTLINE.md` + target `sections/`/`assets/` → edit → `reassemble.py`
→ `validate_tex.sh` / `compile_pdf.sh` → `push_to_overleaf.sh`).
