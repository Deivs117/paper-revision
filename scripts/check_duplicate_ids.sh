#!/usr/bin/env bash
# Blocking check (unlike check_hardcoded_refs.sh/check_target_conflicts.sh, which are advisory):
# scans PROGRESS.md for any ID (first table column) that appears more than once and exits 1 if
# found. This is the direct fix for the C-09/C-10/C-11 incident (README.md §10.3/CLAUDE.md) --
# two contributors each ran next_id.sh against their own not-yet-synced PROGRESS.md and
# independently landed on the same ID before either side pushed; the merge itself produced no git
# conflict (the two row insertions didn't collide textually), so nothing caught the duplicate
# until someone noticed it by eye.
#
# Run from three places so the failure mode is caught no matter who skips what:
#   1. scripts/next_id.sh -- before allocating a NEW id (refuses to hand out one more on top of an
#      existing collision).
#   2. scripts/hooks/pre-commit -- blocks a LOCAL commit that would introduce or carry a dupe.
#   3. .github/workflows/ci.yml -- blocks a PR merge even if a contributor bypassed their local
#      hook with --no-verify, or never ran scripts/install_hooks.sh at all. This is the one that
#      actually makes the rule unbreakable with 4+ people pushing branches -- a local hook is only
#      as strong as everyone remembering to install it.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

DUPES="$(grep -oE '^\| [A-Za-z0-9-]+ \|' "$REPO_ROOT/PROGRESS.md" | sed -E 's/^\| //; s/ \|$//' | sort | uniq -d)"

if [ -n "$DUPES" ]; then
  echo "error: PROGRESS.md has duplicate IDs -- resolve before committing/merging:" >&2
  echo "$DUPES" >&2
  exit 1
fi

echo "OK: no duplicate PROGRESS.md IDs."
exit 0
