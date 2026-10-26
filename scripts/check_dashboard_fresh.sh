#!/usr/bin/env bash
# CI-only (see check_monolith_fresh.sh for the same pattern/rationale): verifies docs/data.json
# matches what scripts/build_dashboard.py would currently produce from PROGRESS.md -- i.e. nobody
# committed a PROGRESS.md change without the dashboard being regenerated (normally automatic via
# the pre-commit hook, README.md §12.3, but that only runs if the hook is installed and wasn't
# bypassed). Ignores two metadata fields that legitimately differ on every regeneration without
# indicating real staleness: "generatedAt" (wall-clock timestamp) and "progressLastCommit" (sourced
# from `git log` on PROGRESS.md at hook-run time, which is necessarily the PREVIOUS commit --
# pre-commit hooks run before the new commit object exists, so this field is always one commit
# behind by construction, not a sign anything was skipped). Compares the "tasks" array, which is
# the field that actually reflects PROGRESS.md's content.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

DATA_FILE="$REPO_ROOT/docs/data.json"

if [ ! -f "$DATA_FILE" ]; then
  echo "error: $DATA_FILE not found" >&2
  exit 1
fi

TMP_COMMITTED="$(mktemp)"
cleanup() { rm -f "$TMP_COMMITTED"; }
trap cleanup EXIT
cp "$DATA_FILE" "$TMP_COMMITTED"

python3 "$SCRIPT_DIR/build_dashboard.py" > /dev/null

STATUS=0
python3 - "$TMP_COMMITTED" "$DATA_FILE" <<'PYEOF' || STATUS=$?
import json
import sys

committed_path, regenerated_path = sys.argv[1], sys.argv[2]

with open(committed_path, encoding="utf-8") as f:
    committed = json.load(f)
with open(regenerated_path, encoding="utf-8") as f:
    regenerated = json.load(f)

if committed.get("tasks") != regenerated.get("tasks"):
    print("FAIL: docs/data.json's tasks are stale relative to PROGRESS.md.", file=sys.stderr)
    print("Fix: run 'python3 scripts/build_dashboard.py' and commit docs/data.json.", file=sys.stderr)
    sys.exit(1)

print("OK: docs/data.json's tasks match PROGRESS.md (build_dashboard.py produces no meaningful diff).")
PYEOF

# restore the committed version so this check never leaves the working tree altered
cp "$TMP_COMMITTED" "$DATA_FILE"
exit "$STATUS"
