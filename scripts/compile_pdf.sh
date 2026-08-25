#!/usr/bin/env bash
# Real compilation check — requires a local LaTeX toolchain. See README.md §5.6.
# The only script in scripts/ allowed to depend on external tooling.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

if [ ! -f "$MIRROR_FILE" ]; then
  echo "error: $MIRROR_FILE not found" >&2
  exit 1
fi

TEX_SRC="$BUILD_DIR/tex-src"
rm -rf "$TEX_SRC"
mkdir -p "$TEX_SRC"

if [ -d "$ASSETS_DIR" ]; then
  rsync -a "$ASSETS_DIR"/ "$TEX_SRC"/
fi
cp "$MIRROR_FILE" "$TEX_SRC/$OVERLEAF_MAIN_FILE"

cd "$TEX_SRC"

LOG_FILE="$TEX_SRC/compile.log"

if command -v latexmk >/dev/null 2>&1; then
  if latexmk -pdf -interaction=nonstopmode -halt-on-error "$OVERLEAF_MAIN_FILE" > "$LOG_FILE" 2>&1; then
    COMPILE_OK=1
  else
    COMPILE_OK=0
  fi
elif command -v pdflatex >/dev/null 2>&1; then
  BASENAME="${OVERLEAF_MAIN_FILE%.tex}"
  {
    pdflatex -interaction=nonstopmode "$OVERLEAF_MAIN_FILE" &&
    { command -v bibtex >/dev/null 2>&1 && bibtex "$BASENAME" || true; } &&
    pdflatex -interaction=nonstopmode "$OVERLEAF_MAIN_FILE" &&
    pdflatex -interaction=nonstopmode "$OVERLEAF_MAIN_FILE"
  } > "$LOG_FILE" 2>&1
  if [ -f "$BASENAME.pdf" ]; then COMPILE_OK=1; else COMPILE_OK=0; fi
else
  echo "error: no LaTeX toolchain found (latexmk or pdflatex required)" >&2
  exit 1
fi

if [ "$COMPILE_OK" = "1" ]; then
  PDF_NAME="${OVERLEAF_MAIN_FILE%.tex}.pdf"
  cp "$TEX_SRC/$PDF_NAME" "$BUILD_DIR/paper.pdf"
  echo "OK: compiled -> $BUILD_DIR/paper.pdf"
  exit 0
else
  echo "FAIL: compilation failed. Log tail:" >&2
  tail -n 40 "$LOG_FILE" >&2
  exit 1
fi
