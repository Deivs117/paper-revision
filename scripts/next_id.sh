#!/usr/bin/env bash
# Prints the next available PROGRESS.md ID for a namespace. Usage:
#   scripts/next_id.sh N   ->  N-01, N-02, ...
#   scripts/next_id.sh C   ->  C-01, C-02, ...
# Scans every ID that has EVER appeared in PROGRESS.md (max seen + 1) — never reuses a number even
# if a row was later removed. R2-xx/R3-xx are a fixed reviewer list, not allocated by this script.
# See README.md §10.3.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

NS="${1:-}"
if [[ "$NS" != "N" && "$NS" != "C" ]]; then
  echo "Usage: $0 <N|C>   (N = new content, C = standalone correction — see README.md §6)" >&2
  exit 1
fi

# Guard: refuse to allocate on top of an existing collision. This is how the ID scheme actually
# broke in practice — two contributors each ran this script against their own local, not-yet-
# synced PROGRESS.md and independently computed the same "next" ID before either side pushed
# (2026-08-29 coherence audit: C-09/C-10/C-11 each collided this way). Catching it here surfaces
# the problem immediately instead of letting a second collision compound a first one.
DUPES="$(grep -oE '^\| [A-Za-z0-9-]+ \|' "$REPO_ROOT/PROGRESS.md" | sed -E 's/^\| //; s/ \|$//' | sort | uniq -d)"
if [ -n "$DUPES" ]; then
  echo "error: PROGRESS.md already has duplicate IDs -- resolve before allocating a new one:" >&2
  echo "$DUPES" >&2
  exit 1
fi

MAX="$(grep -oE "\\b${NS}-[0-9]+\\b" "$REPO_ROOT/PROGRESS.md" | grep -oE '[0-9]+' | sort -n | tail -1 || true)"
MAX="${MAX:-0}"
NEXT=$((10#$MAX + 1))
printf "%s-%02d\n" "$NS" "$NEXT"
