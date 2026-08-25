#!/usr/bin/env bash
# Push local changes back to Overleaf. See README.md §5.8.
#
# 1. Guard: pull the Overleaf repo first; abort if it brings new commits (never force-push,
#    never auto-merge — a genuine conflict needs a human to look at both sides).
# 2. Validate the manuscript structurally (and compile it, if a LaTeX toolchain is available).
# 3. Mirror assets/ and the main tex back into the Overleaf repo clone.
# 4. Commit and push there.
# 5. Mark this repo's new synced checkpoint.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"
cd "$REPO_ROOT"

if [ ! -f "$MIRROR_FILE" ]; then
  echo "error: $MIRROR_FILE not found — nothing to push" >&2
  exit 1
fi

# --- 1. Guard: pull Overleaf first, abort on new commits ----------------------------------------
if [ ! -d "$OVERLEAF_DIR" ]; then
  echo "error: OVERLEAF_DIR not found: $OVERLEAF_DIR" >&2
  exit 1
fi

BEFORE="$(git -C "$OVERLEAF_DIR" rev-parse HEAD)"
if ! git -C "$OVERLEAF_DIR" pull origin main; then
  echo "error: git pull failed in $OVERLEAF_DIR" >&2
  exit 1
fi
AFTER="$(git -C "$OVERLEAF_DIR" rev-parse HEAD)"

if [ "$BEFORE" != "$AFTER" ]; then
  echo "error: Overleaf has new commits since your last sync (co-author edits?)." >&2
  echo "Run scripts/pull_from_overleaf.sh, review what changed, resolve manually, then retry push." >&2
  exit 1
fi

# --- 2. Validate before pushing anything ---------------------------------------------------------
if ! "$SCRIPT_DIR/validate_tex.sh"; then
  echo "error: validate_tex.sh failed — not pushing invalid LaTeX." >&2
  exit 1
fi

if command -v latexmk >/dev/null 2>&1 || command -v pdflatex >/dev/null 2>&1; then
  if ! "$SCRIPT_DIR/compile_pdf.sh"; then
    echo "error: compile_pdf.sh failed — not pushing a manuscript that doesn't compile." >&2
    exit 1
  fi
else
  echo "warning: no LaTeX toolchain found (latexmk/pdflatex) — skipping real compile check." >&2
fi

# Advisory only — never blocks the push, just surfaces it every time (§10.1).
"$SCRIPT_DIR/check_hardcoded_refs.sh"

# --- 3. Mirror back --------------------------------------------------------------------------
rsync -a --delete --exclude='.git' "$ASSETS_DIR"/ "$OVERLEAF_DIR"/
cp "$MIRROR_FILE" "$OVERLEAF_DIR/$OVERLEAF_MAIN_FILE"

# --- 4. Commit and push to Overleaf -----------------------------------------------------------
git -C "$OVERLEAF_DIR" add -A
if git -C "$OVERLEAF_DIR" diff --cached --quiet; then
  echo "Nothing to push — Overleaf already matches this repo's content."
  exit 0
fi
git -C "$OVERLEAF_DIR" commit -m "sync: apply patches from paper-revision ($(date '+%Y-%m-%d %H:%M'))"
git -C "$OVERLEAF_DIR" push origin main

# --- 5. Mark the new synced checkpoint in this repo ---------------------------------------------
git commit --allow-empty -m "chore: mark synced to Overleaf ($(date '+%Y-%m-%d %H:%M'))"

echo "Pushed to Overleaf and marked synced. Remember to update PROGRESS.md rows to synced-to-overleaf."
