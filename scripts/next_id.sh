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
# the problem immediately instead of letting a second collision compound a first one. This is the
# same check scripts/check_duplicate_ids.sh runs (also wired into the pre-commit hook and CI) —
# delegate to it instead of duplicating the grep here, and remind the caller to pull first, since
# a stale local PROGRESS.md is the actual root cause, not something this check alone can fix.
if ! "$SCRIPT_DIR/check_duplicate_ids.sh" >/dev/null; then
  "$SCRIPT_DIR/check_duplicate_ids.sh" >&2 || true
  echo "error: resolve the duplicate above before allocating a new ID. If it wasn't there a" >&2
  echo "moment ago, run 'git pull origin main' first -- this is almost always a stale local" >&2
  echo "PROGRESS.md racing another contributor's already-pushed row." >&2
  exit 1
fi

MAX="$(grep -oE "\\b${NS}-[0-9]+\\b" "$REPO_ROOT/PROGRESS.md" | grep -oE '[0-9]+' | sort -n | tail -1 || true)"
MAX="${MAX:-0}"
NEXT=$((10#$MAX + 1))
printf "%s-%02d\n" "$NS" "$NEXT"
