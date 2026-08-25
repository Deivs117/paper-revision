#!/usr/bin/env bash
# Flags prose like "Section 2" / "Section~4" in sections/*.tex that is NOT a real \ref{} — these go
# stale silently if the top-level \section{} structure changes (e.g. R2-03 promoting a subsection
# to its own top-level section). Advisory only: always exits 0, never blocks anything. See
# README.md §10.1.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

if [ ! -d "$SECTIONS_DIR" ]; then
  exit 0
fi

FOUND=0
for file in "$SECTIONS_DIR"/*.tex; do
  [ -f "$file" ] || continue
  matches="$(grep -noE '\<Sections?[ ~][0-9]+([-–—][0-9]+)?' "$file" || true)"
  if [ -n "$matches" ]; then
    FOUND=1
    echo "  $(basename "$file"):"
    while IFS= read -r m; do
      echo "    line ${m%%:*}: ${m#*:}"
    done <<< "$matches"
  fi
done

if [ "$FOUND" -eq 1 ]; then
  echo
  echo "^ hardcoded section numbers found above (not \\ref{}) — verify these still match the"
  echo "  current top-level \\section{} order in sections/manifest.json before this push, and"
  echo "  update by hand if it has changed since these were written."
else
  echo "No hardcoded 'Section N' references found in sections/*.tex."
fi
