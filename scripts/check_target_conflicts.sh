#!/usr/bin/env bash
# Advisory only: lists other PROGRESS.md rows whose "Target section(s)" text already mentions the
# given section slug and aren't yet synced-to-overleaf. There is no file-locking in this system (a
# single primary writer makes it low-risk) — run this before starting work on a section to check
# whether another in-flight item claims the same file, so you can sequence them instead of editing
# in parallel. See README.md §10.4.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

SLUG="${1:-}"
if [[ -z "$SLUG" ]]; then
  echo "Usage: $0 <section-slug>   (e.g. results, methodology — matches '<slug>.tex' in PROGRESS.md)" >&2
  exit 1
fi

MATCHES="$(grep -E '^\|' "$REPO_ROOT/PROGRESS.md" | grep -F "${SLUG}.tex" | grep -v 'synced-to-overleaf' || true)"

if [[ -z "$MATCHES" ]]; then
  echo "No other active PROGRESS.md rows target ${SLUG}.tex."
  exit 0
fi

echo "Rows currently targeting ${SLUG}.tex (not yet synced-to-overleaf):"
echo "$MATCHES"
echo
echo "No automatic locking exists for sections/ files. If more than one of these is actively being"
echo "worked on, finish and commit one before starting the other to avoid clobbering edits in the"
echo "same file."
