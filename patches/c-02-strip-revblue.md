<!--
PATCH: C-02
Reviewer: —
Target section: all sections/*.tex (except closing.tex — 0 occurrences)
Requirement: Start of a new revision round — last round's \revblue{} (accepted-change markup) is
  stripped back to plain baseline text, since it's no longer "this round's changes". See the new
  revision-round color convention in OUTLINE.md / CLAUDE.md: any NEW text added from here on in
  this round must be wrapped in \revblue{...} again.
Status: applied
-->

Repo-wide structural change, not new prose — recorded as a summary rather than a content copy
(the convention in README.md §7 assumes a single-section content patch; this touched every file).

**What ran:** `python3 scripts/strip_revblue.py --apply`

**Result:** 265 `\revblue{...}` wrappers removed, inner text kept, across:

| File | Wrappers stripped |
|---|---|
| `preamble.tex` | 1 (the abstract) |
| `introduction.tex` | 7 |
| `methodology.tex` | 24 |
| `results.tex` | 229 |
| `conclusions.tex` | 4 |
| `closing.tex` | 0 |

The `\newcommand{\revblue}[1]{\textcolor{blue}{#1}}` macro definition in `preamble.tex:47` was
**not** touched — the script only strips actual invocations (`\revblue{`), not the definition
(whose text contains `\revblue}`, not `\revblue{`).

**Verification:** `scripts/reassemble.py` → `scripts/validate_tex.sh` (pass) →
`scripts/check_roundtrip.sh` (pass, byte-identical split↔reassemble on the new baseline).
