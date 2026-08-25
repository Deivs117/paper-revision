#!/usr/bin/env bash
# Sync from Overleaf into this repo. See README.md §5.1.
#
# 1. Guard: abort if any commit since the last sync/push marker touches source/, sections/, or
#    assets/ — that means local work hasn't been pushed to Overleaf yet, and overwriting now
#    would silently lose it.
# 2. git pull the Overleaf repo clone.
# 3. Mirror the main .tex (renamed) and everything else (assets/) from it.
# 4. Regenerate sections/ from the new source/main_monolithic.tex.
# 5. Commit the whole sync as one checkpoint.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"
cd "$REPO_ROOT"

# --- 1. Guard against clobbering unpushed local work -------------------------------------------
# Multiple --grep options are OR'd together by default (no --all-match), which is what we want:
# either marker counts as "everything was in sync as of this commit".
LAST_MARKER="$(git log -1 --format=%H \
  --grep='^sync: pull from Overleaf' \
  --grep='^chore: mark synced to Overleaf' \
  -E 2>/dev/null || true)"

if [ -n "$LAST_MARKER" ]; then
  UNSYNCED="$(git log "$LAST_MARKER"..HEAD --oneline -- source sections assets 2>/dev/null || true)"
  if [ -n "$UNSYNCED" ]; then
    echo "error: local commits since the last sync/push touch source/, sections/, or assets/:" >&2
    echo "$UNSYNCED" >&2
    echo "Run scripts/push_to_overleaf.sh first, then re-run this script." >&2
    exit 1
  fi
fi

# --- 2. Pull the Overleaf repo -----------------------------------------------------------------
if [ ! -d "$OVERLEAF_DIR" ]; then
  echo "error: OVERLEAF_DIR not found: $OVERLEAF_DIR" >&2
  exit 1
fi

if ! git -C "$OVERLEAF_DIR" pull origin main; then
  echo "error: git pull failed in $OVERLEAF_DIR" >&2
  exit 1
fi

OVERLEAF_MAIN_PATH="$OVERLEAF_DIR/$OVERLEAF_MAIN_FILE"
if [ ! -f "$OVERLEAF_MAIN_PATH" ]; then
  echo "error: $OVERLEAF_MAIN_PATH not found" >&2
  exit 1
fi

# --- 3. Mirror main tex + everything else -------------------------------------------------------
mkdir -p "$(dirname "$MIRROR_FILE")" "$ASSETS_DIR"
cp "$OVERLEAF_MAIN_PATH" "$MIRROR_FILE"
rsync -a --delete --exclude='.git' --exclude="$OVERLEAF_MAIN_FILE" "$OVERLEAF_DIR"/ "$ASSETS_DIR"/

# --- 4. Anything actually changed? --------------------------------------------------------------
if git diff --quiet -- "$MIRROR_FILE" "$ASSETS_DIR" && \
   [ -z "$(git status --porcelain -- "$MIRROR_FILE" "$ASSETS_DIR")" ]; then
  echo "No changes since last sync."
  exit 0
fi

# --- 5. Regenerate sections/, commit everything as one checkpoint --------------------------------
python3 "$SCRIPT_DIR/split_sections.py"

git add "$MIRROR_FILE" "$ASSETS_DIR" "$SECTIONS_DIR"
git commit -m "sync: pull from Overleaf ($(date '+%Y-%m-%d %H:%M'))"

echo "Synced from Overleaf. Run scripts/find_section.py to see what changed."
