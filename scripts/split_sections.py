#!/usr/bin/env python3
"""Split source/main_monolithic.tex into sections/*.tex + sections/manifest.json.

Pure text/regex split — no LaTeX parser, no \\input/\\include resolution. See README.md §5.2.

Split boundaries (in order of precedence):
  - Each line matching ^\\s*\\section\\{...\\}  -> starts a new section file.
  - The first line matching \\end{document}, \\bibliography{, \\bibliographystyle{, or \\appendix
    (whichever comes first after the last \\section boundary) -> starts sections/closing.tex.
    This keeps bibliography/appendix material out of the last content section's file, matching the
    intent described in the README even though it isn't literally a \\section{} boundary.

Byte-exact invariant: every byte of the source file ends up in exactly one output file, in the same
order, with nothing added/removed/normalized. reassemble.py is required to invert this exactly.
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_FILE = REPO_ROOT / "source" / "main_monolithic.tex"
SECTIONS_DIR = REPO_ROOT / "sections"
MANIFEST_FILE = SECTIONS_DIR / "manifest.json"

SECTION_RE = re.compile(r"^\s*\\section\{(.*?)\}")
CLOSING_RE = re.compile(r"^\s*\\(end\{document\}|bibliography\{|bibliographystyle\{|appendix\b)")


def slugify(title, seen):
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    if not slug:
        slug = "section"
    base = slug
    n = 2
    while slug in seen:
        slug = f"{base}-{n}"
        n += 1
    seen.add(slug)
    return slug


def main():
    if not SOURCE_FILE.exists():
        print(f"error: {SOURCE_FILE} not found", file=sys.stderr)
        return 1

    with open(SOURCE_FILE, "r", encoding="utf-8", newline="") as f:
        lines = f.readlines()  # keeps line endings attached to each line

    all_section_starts = []  # list of (line_index, title), whole file
    for i, line in enumerate(lines):
        m = SECTION_RE.match(line)
        if m:
            all_section_starts.append((i, m.group(1)))

    # Find the closing boundary: first closing-marker line at or after the first section
    # (or from the start of file if there are no sections at all).
    search_from = all_section_starts[0][0] if all_section_starts else 0
    closing_start = len(lines)
    for i in range(search_from, len(lines)):
        if CLOSING_RE.match(lines[i]):
            closing_start = i
            break

    # Any \section{} appearing at or after the closing boundary (e.g. inside \appendix) is
    # NOT a split point of its own — that content belongs to closing.tex, matched verbatim.
    section_starts = [s for s in all_section_starts if s[0] < closing_start]

    manifest = []
    seen_slugs = set()

    def write_file(name, text):
        (SECTIONS_DIR / name).write_text(text, encoding="utf-8", newline="")

    # Regenerate sections/ from scratch every run.
    if SECTIONS_DIR.exists():
        for f in SECTIONS_DIR.glob("*.tex"):
            f.unlink()
    SECTIONS_DIR.mkdir(exist_ok=True)

    # Preamble: everything before the first \section{}, capped at the closing boundary
    # (covers the pathological case of a manuscript with no \section{} commands at all).
    preamble_end = min(section_starts[0][0], closing_start) if section_starts else closing_start
    write_file("preamble.tex", "".join(lines[0:preamble_end]))
    manifest.append({"file": "preamble.tex", "title": None})

    # Each section runs from its \section{} line to the next section's line, or to the
    # closing boundary for the last one.
    for idx, (start, title) in enumerate(section_starts):
        end = section_starts[idx + 1][0] if idx + 1 < len(section_starts) else closing_start
        end = min(end, closing_start)
        slug = slugify(title, seen_slugs)
        filename = f"{slug}.tex"
        write_file(filename, "".join(lines[start:end]))
        manifest.append({"file": filename, "title": title})

    # Closing: the boundary line to EOF.
    write_file("closing.tex", "".join(lines[closing_start:]))
    manifest.append({"file": "closing.tex", "title": None})

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Split into {len(manifest)} files ({len(section_starts)} sections) -> {SECTIONS_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
