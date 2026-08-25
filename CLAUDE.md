# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Revision-tracking + AI-patching layer for manuscript `ROBOT-D-26-00122R1` (*Robotics and Autonomous Systems*),
deadline **August 31, 2026**. The manuscript is edited by non-technical co-authors on Overleaf. **All real work
happens in this repo** — text patching, asset management, compilation. The sibling Overleaf repo clone is
sync-only. Full spec: **README.md — read it before implementing any script here**, it is the source of truth for
file formats, script behavior, and naming.

## Hard rules

- Never edit `source/main_monolithic.tex` by hand. It is generated: written by `scripts/pull_from_overleaf.sh`
  (from Overleaf) or `scripts/reassemble.py` (from `sections/`).
- Never edit `sections/*.tex` filenames or `manifest.json` order outside `scripts/split_sections.py` — it fully
  regenerates `sections/` on every run. Edit section **content** in place, not the split itself. Filenames have no
  numeric prefix; order lives only in `sections/manifest.json`.
- `assets/` mirrors the Overleaf project 1:1 (bibliography, figures, class files), under original relative paths.
  It is editable in place (unlike `source/main_monolithic.tex`) and mirrors back on push.
- The Overleaf repo clone is **sync-only** — never hand-edit files there.
- `scripts/pull_from_overleaf.sh` must abort if `PROGRESS.md` has any row with `Status = applied` — that means
  local work isn't pushed to Overleaf yet, and pulling would silently overwrite it.
- `scripts/push_to_overleaf.sh` must always `git pull` the Overleaf repo first and abort on new commits, and must
  run `scripts/validate_tex.sh` (+ `compile_pdf.sh` if a LaTeX toolchain is available) before pushing — never
  force-push, never auto-merge, never push unvalidated LaTeX.
- All scripts read shared paths from `scripts/config.sh` — never hardcode `OVERLEAF_DIR`, `ASSETS_DIR`, or
  `source/main_monolithic.tex` elsewhere.
- Never write the Overleaf git token (`olp_...`) into any file in either repo. It lives only in
  `~/.git-credentials` via `git config --global credential.helper store`.
- Text-processing scripts (`split_sections.py`, `reassemble.py`, `find_section.py`, `validate_tex.sh`) are
  bash/Python-stdlib only, regex/line-based by design — no LaTeX parser. `compile_pdf.sh` is the only script
  allowed to depend on external tooling (a LaTeX distribution).
- Keep `sync:` commits (from pulling Overleaf) and `patch:` commits (from applying a reviewer fix) separate — never
  combine them in one commit.

## Key files

- `README.md` — full architecture, script specs, file formats (`sections/manifest.json`, `patches/*.tex` header,
  `PROGRESS.md` table). Treat as the spec to implement against.
- `PROGRESS.md` — status per reviewer requirement (`pending` → `drafted` → `applied` → `synced-to-overleaf`). Check
  before starting new patch work; update after. Also gates `pull_from_overleaf.sh` (see Hard rules).
- `patches/<id>-<slug>.tex` — audit copy of each applied change, not the live file (that's `sections/<slug>.tex`
  or `assets/`).
- `build/` — gitignored, disposable compile output from `compile_pdf.sh`. Never commit anything from it.

## Commands

Not yet implemented — see README.md §"Repository Setup & Execution Guide" for what to build and the daily loop
(`pull_from_overleaf.sh` → `find_section.py` → edit `sections/`/`assets/` → `reassemble.py` → `validate_tex.sh` /
`compile_pdf.sh` → `push_to_overleaf.sh`).
