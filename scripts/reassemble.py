#!/usr/bin/env python3
"""Rebuild source/main_monolithic.tex from sections/*.tex, in sections/manifest.json order.

Exact inverse of split_sections.py: concatenates each listed file's raw bytes with NO separator
inserted. Running split_sections.py then reassemble.py with no edits in between MUST reproduce the
original file byte-for-byte — verified by check_roundtrip.sh. See README.md §5.3.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_FILE = REPO_ROOT / "source" / "main_monolithic.tex"
SECTIONS_DIR = REPO_ROOT / "sections"
MANIFEST_FILE = SECTIONS_DIR / "manifest.json"


def main():
    if not MANIFEST_FILE.exists():
        print(f"error: {MANIFEST_FILE} not found — run split_sections.py first", file=sys.stderr)
        return 1

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    parts = []
    for entry in manifest:
        path = SECTIONS_DIR / entry["file"]
        if not path.exists():
            print(f"error: {path} listed in manifest.json but missing", file=sys.stderr)
            return 1
        parts.append(path.read_text(encoding="utf-8", newline=""))

    SOURCE_FILE.parent.mkdir(parents=True, exist_ok=True)
    SOURCE_FILE.write_text("".join(parts), encoding="utf-8", newline="")

    print(f"Reassembled {len(manifest)} files -> {SOURCE_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
