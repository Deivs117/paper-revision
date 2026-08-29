#!/usr/bin/env bash
# Advisory-only word-count tripwire for sections/*.tex, relative to the R2-01 closing baseline
# (commit 51c07b4, the last patch of the redundancy-condensation round Referee 2 originally
# requested: "cut repetitive descriptions... merge unified metric definitions... shorten the
# symbolic warehouse simulation section"). Growth since then is NOT inherently bad -- most of it
# is genuine new required content (R2-02/R3-01/02/04/05/06, N-xx figure work) -- this script does
# not judge redundancy (that needs a human/LLM re-read, see intake/pending/ for the scheduled
# closing audit). It only makes growth visible on every push so nobody discovers a large,
# unexplained jump only at final compile time. Advisory only: always exits 0, never blocks
# anything. Same pattern as check_hardcoded_refs.sh, see README.md §10.1.
#
# Word counts are raw `wc -w` on the .tex source (includes LaTeX markup, not prose-only) --
# internally consistent for tracking delta over time, not meant to match any prose-only tally
# quoted in PROGRESS.md.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

if [ ! -d "$SECTIONS_DIR" ]; then
  exit 0
fi

# Baseline: raw `wc -w` of each file at commit 51c07b4 (R2-01's final patch).
declare -A BASELINE=(
  [closing.tex]=82
  [conclusions.tex]=1327
  [introduction.tex]=1193
  [methodology.tex]=5660
  [preamble.tex]=581
  [results.tex]=8645
)

echo "Word-count growth since R2-01 closed (advisory, commit 51c07b4 baseline):"
for file in "${!BASELINE[@]}"; do
  path="$SECTIONS_DIR/$file"
  [ -f "$path" ] || continue
  current="$(wc -w < "$path")"
  base="${BASELINE[$file]}"
  delta=$((current - base))
  sign=""
  [ "$delta" -gt 0 ] && sign="+"
  printf "  %-16s %5d -> %5d words (%s%d)\n" "$file" "$base" "$current" "$sign" "$delta"
done

echo "  (Growth is expected from genuine new content -- R2-02/R3-01/02/04/05/06, N-xx figure work."
echo "   This only flags visibility; judging whether growth is redundant needs a human/LLM re-read.)"

exit 0
