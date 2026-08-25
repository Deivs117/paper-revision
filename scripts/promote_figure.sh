#!/usr/bin/env bash
# Copies a finished figure/table file out of experiments/<id>-<slug>/output/ into assets/, at the
# exact relative path the LaTeX will \includegraphics. This is the ONLY way a new asset should
# enter assets/ by hand (everything else in assets/ is a 1:1 mirror written by
# pull_from_overleaf.sh / push_to_overleaf.sh). See README.md §9 for the full experiments/ workflow.
#
# Usage: scripts/promote_figure.sh <experiments/ID-slug/output/file.png> <assets/relative/path.png>
#
# Safety: refuses to overwrite an existing assets/ file unless --force is passed, since assets/ is
# also the Overleaf mirror — silently clobbering an asset a co-author added/changed there would be
# exactly the kind of silent data loss the pull/push guards exist to prevent.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

FORCE=0
ARGS=()
for arg in "$@"; do
  if [[ "$arg" == "--force" ]]; then
    FORCE=1
  else
    ARGS+=("$arg")
  fi
done

if [[ ${#ARGS[@]} -ne 2 ]]; then
  echo "Usage: $0 [--force] <experiments/ID-slug/output/file> <assets-relative-path>" >&2
  exit 1
fi

SRC="${ARGS[0]}"
DEST_REL="${ARGS[1]}"
DEST="$ASSETS_DIR/$DEST_REL"

if [[ ! -f "$SRC" ]]; then
  echo "ERROR: source file not found: $SRC" >&2
  exit 1
fi

case "$(cd "$(dirname "$SRC")" && pwd)/$(basename "$SRC")" in
  "$EXPERIMENTS_DIR"/*/output/*) ;;
  *)
    echo "ERROR: source must live under experiments/<id>-<slug>/output/ — got: $SRC" >&2
    echo "       (this keeps every promoted figure traceable back to the experiment that made it)" >&2
    exit 1
    ;;
esac

if [[ -e "$DEST" && "$FORCE" -ne 1 ]]; then
  echo "ERROR: $DEST_REL already exists in assets/. Pass --force to overwrite deliberately." >&2
  echo "       If a co-author changed this asset on Overleaf, pull first and reconcile by hand." >&2
  exit 1
fi

mkdir -p "$(dirname "$DEST")"
cp "$SRC" "$DEST"
echo "Promoted: $SRC -> assets/$DEST_REL"
echo "Remember to: (1) record this in the experiment's README.md output list, (2) reference it with"
echo "\\includegraphics in the target sections/*.tex file as a normal patch."
