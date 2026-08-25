#!/usr/bin/env python3
"""Upward-scan diff-to-section mapper. Read-only — never modifies files. See README.md §5.4.

Usage: find_section.py [<git-rev-range>]   (default: HEAD~1..HEAD)

For each changed hunk in source/main_monolithic.tex within the given range, scans upward from the
hunk's start line to the nearest preceding \\section{} line (or the top of file -> preamble), and
prints which sections/*.tex file that corresponds to.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_FILE = REPO_ROOT / "source" / "main_monolithic.tex"
MANIFEST_FILE = REPO_ROOT / "sections" / "manifest.json"

# Reuse split_sections.py's own boundary regexes so section detection can never drift between the
# two scripts — duplicate section titles (e.g. two "Related Work") are only disambiguated correctly
# if both scripts agree on which line starts which section, by position, not by title text.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from split_sections import SECTION_RE, CLOSING_RE  # noqa: E402

HUNK_HEADER_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def section_boundaries(lines):
    """Return an ordered list of (start_line_index, title) for each real section split point,
    i.e. \\section{} lines before the closing boundary — same logic as split_sections.py."""
    all_starts = [(i, m.group(1)) for i, line in enumerate(lines)
                  for m in [SECTION_RE.match(line)] if m]
    search_from = all_starts[0][0] if all_starts else 0
    closing_start = len(lines)
    for i in range(search_from, len(lines)):
        if CLOSING_RE.match(lines[i]):
            closing_start = i
            break
    return [s for s in all_starts if s[0] < closing_start]


def load_manifest():
    if not MANIFEST_FILE.exists():
        return None
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    rev_range = sys.argv[1] if len(sys.argv) > 1 else "HEAD~1..HEAD"

    if not SOURCE_FILE.exists():
        print(f"error: {SOURCE_FILE} not found", file=sys.stderr)
        return 1

    try:
        diff = subprocess.run(
            ["git", "diff", rev_range, "--", "source/main_monolithic.tex"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except subprocess.CalledProcessError as e:
        print(f"error: git diff failed: {e.stderr}", file=sys.stderr)
        return 1

    # For each hunk, find the tight range of new-file line numbers actually touched by '+'/'-'
    # lines (the hunk header's own range includes surrounding context lines, which would point
    # the upward scan at the wrong section if used directly).
    hunks = []
    pointer = None
    first_changed = None
    last_changed = None

    def flush():
        nonlocal first_changed, last_changed
        if first_changed is not None:
            hunks.append((first_changed, last_changed))
        first_changed = None
        last_changed = None

    for line in diff.splitlines():
        m = HUNK_HEADER_RE.match(line)
        if m:
            flush()
            pointer = int(m.group(1))
            continue
        if pointer is None:
            continue  # before the first hunk (diff --git / --- / +++ header lines)
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith(" "):
            pointer += 1
        elif line.startswith("+"):
            first_changed = pointer if first_changed is None else min(first_changed, pointer)
            last_changed = pointer
            pointer += 1
        elif line.startswith("-"):
            first_changed = pointer if first_changed is None else min(first_changed, pointer)
            last_changed = pointer if last_changed is None else max(last_changed, pointer)
            # removed line: doesn't exist in the new file, pointer does not advance
    flush()

    if not hunks:
        print("No changes to source/main_monolithic.tex in this range.")
        return 0

    with open(SOURCE_FILE, "r", encoding="utf-8", newline="") as f:
        lines = f.readlines()

    boundaries = section_boundaries(lines)  # [(line_index, title), ...] in file order
    manifest = load_manifest()

    for start, end in hunks:
        # Find the last section boundary at or before the hunk (1-indexed -> 0-indexed line).
        target_line = min(start, len(lines)) - 1
        section_index = None  # index into `boundaries`, None => preamble
        for i, (line_idx, _title) in enumerate(boundaries):
            if line_idx <= target_line:
                section_index = i
            else:
                break

        if section_index is None:
            title_display = "(preamble)"
            label = "preamble.tex"
        else:
            title_display = boundaries[section_index][1]
            # manifest is [preamble, section_0, section_1, ..., closing] — same order as
            # `boundaries`, so position (not title text) is what disambiguates duplicates.
            if manifest is not None and section_index + 1 < len(manifest):
                label = manifest[section_index + 1]["file"]
            else:
                label = "(manifest.json missing or stale — re-run split_sections.py)"
        print(f"{title_display} (sections/{label}): lines {start}-{end} changed")

    return 0


if __name__ == "__main__":
    sys.exit(main())
