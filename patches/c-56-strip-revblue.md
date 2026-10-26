<!--
PATCH: C-56
Reviewer: —
Target section: all sections/*.tex (except closing.tex — 0 occurrences)
Requirement: Start of the new revision round (editor decision on ROBOT-D-26-00122R2, received
  2026-10-26, minor revision requested, deadline 2026-11-04) — the previous round's \revblue{}
  (accepted-change markup, everything written/changed to produce the just-submitted R2 manuscript)
  is stripped back to plain baseline text, since it is no longer "this round's changes". Any NEW
  text written from here on to address the R2b/R3b reviewer items (see PROGRESS.md) must be wrapped
  in \revblue{...} again, per the convention in README.md §11 / OUTLINE.md.
Status: applied
-->

Repo-wide structural change, not new prose — recorded as a summary rather than a content copy,
same precedent as `patches/c-02-strip-revblue.md`.

**What ran:** `python3 scripts/strip_revblue.py --apply`

**Result:** 161 `\revblue{...}` wrappers removed, inner text kept, across:

| File | Wrappers stripped |
|---|---|
| `preamble.tex` | 1 |
| `introduction.tex` | 6 |
| `methodology.tex` | 23 |
| `results.tex` | 126 |
| `conclusions.tex` | 5 |
| `closing.tex` | 0 |

The `\newcommand{\revblue}[1]{\textcolor{blue}{#1}}` macro definition in `preamble.tex` was **not**
touched — the script only strips actual invocations (`\revblue{`), not the definition (whose text
contains `\revblue}`, not `\revblue{`).

**Verification:** `scripts/reassemble.py` → `scripts/validate_tex.sh` (pass) →
`scripts/check_roundtrip.sh` (pass, byte-identical split↔reassemble on the new baseline).
