#!/usr/bin/env bash
# Verifies source/main_monolithic.tex is exactly what scripts/reassemble.py would produce from
# the CURRENTLY committed sections/*.tex -- i.e. the two haven't drifted apart.
#
# This is a different (and, for a multi-writer repo, more load-bearing) check than
# check_roundtrip.sh: that script tests split(monolith)->reassemble == monolith, a
# self-consistency property of split_sections.py/reassemble.py that says nothing about whether a
# given commit's sections/ edits were actually folded back into the monolith. The normal path
# (scripts/hooks/pre-commit) runs reassemble.py on every commit touching sections/, so this never
# drifts locally -- but that hook only works if it's installed (scripts/install_hooks.sh) and
# wasn't bypassed with --no-verify. With 4+ contributors now pushing branches directly (see
# CLAUDE.md "Multi-writer workflow"), this script is what catches a stale monolith in CI even when
# both of those local safeguards were skipped.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

if [ ! -f "$MIRROR_FILE" ]; then
  echo "error: $MIRROR_FILE not found" >&2
  exit 1
fi

TMP_COMMITTED="$(mktemp)"
cleanup() { rm -f "$TMP_COMMITTED"; }
trap cleanup EXIT
cp "$MIRROR_FILE" "$TMP_COMMITTED"

python3 "$SCRIPT_DIR/reassemble.py" > /dev/null

if diff -u "$TMP_COMMITTED" "$MIRROR_FILE" > /tmp/.monolith-fresh-diff.$$; then
  rm -f /tmp/.monolith-fresh-diff.$$
  echo "OK: source/main_monolithic.tex matches sections/*.tex (reassemble.py produces no diff)."
  exit 0
else
  echo "FAIL: source/main_monolithic.tex is stale relative to sections/*.tex. Diff:" >&2
  cat /tmp/.monolith-fresh-diff.$$ >&2
  echo >&2
  echo "Fix: run 'python3 scripts/reassemble.py', commit the result, and make sure" >&2
  echo "scripts/install_hooks.sh has been run in your clone so this doesn't recur." >&2
  rm -f /tmp/.monolith-fresh-diff.$$
  # restore the committed version so a failed check doesn't leave the working tree altered
  cp "$TMP_COMMITTED" "$MIRROR_FILE"
  exit 1
fi
