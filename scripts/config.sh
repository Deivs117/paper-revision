#!/usr/bin/env bash
# Shared configuration for all scripts/ — source this, never hardcode these paths elsewhere.
# See README.md §5 for what each variable is used for.

# Resolve repo root regardless of the caller's working directory.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Path to the Overleaf repo clone (sync-only, sibling directory to this repo).
OVERLEAF_DIR="${OVERLEAF_DIR:-$REPO_ROOT/../6a23870b4fcac02449561a35}"

# The manuscript's filename as it exists inside the Overleaf project.
OVERLEAF_MAIN_FILE="${OVERLEAF_MAIN_FILE:-elsarticle-template-num-names.tex}"

# This repo's mirror of the manuscript (generated — never hand-edited).
MIRROR_FILE="${MIRROR_FILE:-$REPO_ROOT/source/main_monolithic.tex}"

# 1:1 mirror of the Overleaf project root, excluding the main .tex file.
ASSETS_DIR="${ASSETS_DIR:-$REPO_ROOT/assets}"

# Disposable compile workspace (gitignored).
BUILD_DIR="${BUILD_DIR:-$REPO_ROOT/build}"

# Editable per-section working copy of the manuscript text.
SECTIONS_DIR="${SECTIONS_DIR:-$REPO_ROOT/sections}"

# Scripts/notebooks/data that generate new figures/tables not yet in assets/.
EXPERIMENTS_DIR="${EXPERIMENTS_DIR:-$REPO_ROOT/experiments}"

export REPO_ROOT OVERLEAF_DIR OVERLEAF_MAIN_FILE MIRROR_FILE ASSETS_DIR BUILD_DIR SECTIONS_DIR EXPERIMENTS_DIR
