#!/usr/bin/env python3
"""Unwraps every \\revblue{...} invocation in sections/*.tex, keeping the inner text and dropping
the wrapper — used at the start of a new revision round to turn last round's colored (accepted)
changes back into plain baseline text. Never touches the \\newcommand{\\revblue}... definition
itself (that string doesn't contain the literal "\\revblue{" this script searches for). See
README.md §11 / CLAUDE.md "Revision-round color convention".

Usage:
  scripts/strip_revblue.py           # dry run: reports what would change, writes nothing
  scripts/strip_revblue.py --apply   # writes the stripped files in place

Brace matching mirrors validate_tex.sh's escape handling: a backslash escapes the next character
(so literal \\{ or \\} are never counted as structural), and depth counting only sees real braces.
"""
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SECTIONS_DIR = SCRIPT_DIR.parent / "sections"
MACRO = "\\revblue{"


def strip_once(text: str) -> tuple[str, int]:
    """Removes every top-level \\revblue{...} wrapper in one left-to-right pass. Returns
    (new_text, count_removed). Nested \\revblue{\\revblue{...}} (not expected in practice) needs a
    second pass — the caller loops until count_removed is 0."""
    out = []
    i = 0
    n = len(text)
    count = 0
    while i < n:
        if text.startswith(MACRO, i):
            start_content = i + len(MACRO)
            depth = 1
            j = start_content
            while j < n and depth > 0:
                c = text[j]
                if c == "\\" and j + 1 < n:
                    j += 2
                    continue
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                j += 1
            if depth != 0:
                raise ValueError(f"unbalanced \\revblue{{ starting at offset {i} — no matching close brace")
            inner = text[start_content:j - 1]
            out.append(inner)
            count += 1
            i = j
        else:
            out.append(text[i])
            i += 1
    return "".join(out), count


def strip_all(text: str) -> tuple[str, int]:
    total = 0
    for _ in range(10):  # safety cap against pathological nesting
        text, n = strip_once(text)
        total += n
        if n == 0:
            break
    return text, total


def main():
    apply = "--apply" in sys.argv[1:]
    grand_total = 0
    for path in sorted(SECTIONS_DIR.glob("*.tex")):
        raw = path.read_text(encoding="utf-8")
        new_text, count = strip_all(raw)
        if count == 0:
            continue
        grand_total += count
        print(f"{path.name}: {count} \\revblue{{}} wrapper(s) {'stripped' if apply else 'would be stripped'}")
        if apply:
            path.write_text(new_text, encoding="utf-8")
    print(f"Total: {grand_total} wrapper(s) {'stripped' if apply else 'would be stripped'} across sections/*.tex.")
    if not apply and grand_total > 0:
        print("Dry run only — re-run with --apply to write changes.")


if __name__ == "__main__":
    main()
