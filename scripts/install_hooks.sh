#!/usr/bin/env bash
# One-time (per clone) setup: installs this repo's git hooks. Re-run after pulling if
# scripts/hooks/ changes, since .git/hooks/ isn't itself version-controlled. See README.md §10.2.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cp "$SCRIPT_DIR/hooks/pre-commit" "$REPO_ROOT/.git/hooks/pre-commit"
chmod +x "$REPO_ROOT/.git/hooks/pre-commit"

echo "Installed: .git/hooks/pre-commit (runs validate_tex.sh + check_roundtrip.sh when sections/ or source/ change)"
