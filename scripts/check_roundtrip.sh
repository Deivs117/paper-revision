#!/usr/bin/env bash
# Verifies the round-trip idempotency invariant (README.md §5.3 / §5.7):
# split_sections.py immediately followed by reassemble.py, with no edits in between, must
# reproduce source/main_monolithic.tex byte-for-byte. Cheap, dependency-free.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

if [ ! -f "$MIRROR_FILE" ]; then
  echo "error: $MIRROR_FILE not found" >&2
  exit 1
fi

TMP_ORIGINAL="$(mktemp)"
cleanup() { rm -f "$TMP_ORIGINAL"; }
trap cleanup EXIT

cp "$MIRROR_FILE" "$TMP_ORIGINAL"

python3 "$SCRIPT_DIR/split_sections.py"
python3 "$SCRIPT_DIR/reassemble.py"

if diff -u "$TMP_ORIGINAL" "$MIRROR_FILE" > /tmp/.roundtrip-diff.$$; then
  rm -f /tmp/.roundtrip-diff.$$
  echo "OK: split -> reassemble round-trip is byte-identical."
  exit 0
else
  echo "FAIL: round-trip produced a different file. Diff:" >&2
  cat /tmp/.roundtrip-diff.$$ >&2
  rm -f /tmp/.roundtrip-diff.$$
  # restore the original so a failed check doesn't leave main_monolithic.tex altered
  cp "$TMP_ORIGINAL" "$MIRROR_FILE"
  python3 "$SCRIPT_DIR/split_sections.py" > /dev/null
  exit 1
fi
