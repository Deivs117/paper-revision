# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Revision-tracking + AI-patching layer for manuscript `ROBOT-D-26-00122R1` (*Robotics and Autonomous Systems*),
deadline **August 31, 2026**. The manuscript is edited by non-technical co-authors on Overleaf. This repo bridges
Overleaf and a reviewer-response checklist via two sibling git repos. Full spec: **README.md — read it before
implementing any script here**, it is the source of truth for file formats, script behavior, and naming.

## Hard rules

- Never edit `source/main_monolithic.tex` by hand. It is a generated artifact: written by
  `scripts/pull_from_overleaf.sh` (from Overleaf) or `scripts/reassemble.py` (from `sections/`).
- Never edit `sections/*.tex` filenames or structure by hand outside `scripts/split_sections.py` — it fully
  regenerates `sections/` on every run. Edit section **content** in place, not the split itself.
- All scripts read shared paths from `scripts/config.sh` — never hardcode `OVERLEAF_DIR`, the Overleaf filename, or
  `source/main_monolithic.tex` elsewhere.
- Never write the Overleaf git token (`olp_...`) into any file in either repo. It lives only in
  `~/.git-credentials` via `git config --global credential.helper store`.
- `scripts/push_to_overleaf.sh` must always `git pull` the Overleaf repo first and abort on new commits — never
  force-push, never auto-merge a conflict.
- Scripts are bash + Python 3 stdlib only. No LaTeX parser, no external dependencies — splitting/reassembly is
  regex/line-based on `\section{...}` boundaries by design (see README §5).
- Keep `sync:` commits (from pulling Overleaf) and `patch:` commits (from applying a reviewer fix) separate —
  never combine them in one commit.

## Key files

- `README.md` — full architecture, script specs, file formats (`sections/manifest.json`, `patches/*.tex` header,
  `PROGRESS.md` table). Treat as the spec to implement against.
- `PROGRESS.md` — status per reviewer requirement (`pending` → `drafted` → `applied` → `synced-to-overleaf`). Check
  before starting new patch work; update after.
- `patches/<id>-<slug>.tex` — audit copy of each applied change, not the live file (that's `sections/NN_*.tex`).

## Commands

Not yet implemented — see README.md §"Repository Setup & Execution Guide" for what to build and the intended daily
loop (`pull_from_overleaf.sh` → `find_section.py` → edit `sections/` → `reassemble.py` → `push_to_overleaf.sh`).
