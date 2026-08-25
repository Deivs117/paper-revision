<!--
PATCH: C-05
Reviewer: —
Target section: sections/results.tex, sections/conclusions.tex
Requirement: Review of Sebas's 16-commit R2-01/R2-03/C-01/C-03 push (done before syncing to
  Overleaf) found several patches with materially rewritten prose that was NOT wrapped in
  \revblue{...}, violating the revision-round color convention established this round (already
  documented in CLAUDE.md/README.md/OUTLINE.md before his commits started). One patch (R2-01 7/12)
  had \revblue{} fragmented around \ref{}/math instead of wrapping the whole sentence, which would
  render as blue/black/blue/black patchwork instead of a clean blue block.
Status: applied
-->

No content, numbers, or claims were changed — this patch only adds/repairs `\revblue{}` wrapping so
the compiled PDF correctly shows this round's changes in blue for reviewers/editors.

**Wrapped (previously unwrapped):**
- `results.tex`: single-stimulus (sim) intro paragraph (R2-01 2/12)
- `results.tex`: physical multi-stimuli intro paragraph (R2-01 5/12)
- `results.tex`: 4 physical-scenario opening sentences, Appetitive/Aversive/Complex/Obstacle (R2-01 7/12 — previously fragmented, now one clean block per scenario)
- `results.tex`: 12 paragraphs from the verbal-tightening pass — 4×(neural dynamics + attitude/mechanical) per scenario, energy consumption, terrain-latency intro, decision-latency, electromechanical-coupling (R2-01 12/12)
- `conclusions.tex`: the 2 merged closing paragraphs (R2-01 13/12)

**Verified after:** `reassemble.py` → `validate_tex.sh` → `check_roundtrip.sh` all pass.

**Also fixed in passing:** `patches/c-03-disable-graphical-abstract.tex`'s embedded LaTeX comment
still said "C-02" (stale — the row was renumbered to C-03 during the C-02 ID-collision
reconciliation, `9460624`, but the patch snapshot wasn't updated at the time). Corrected to C-03 to
match the live `sections/preamble.tex` comment.

**Left as-is (lower priority, doesn't affect the compiled document):** `patches/r2-01-04-*.tex` and
`patches/r2-01-10-*.tex` contain a literal `...` elision instead of the full patch text; `patches/r2-01-12-*.tex`
and `patches/r2-01-13-*.tex` point to "see git diff" instead of recording the before/after text
inline. These are audit-trail completeness gaps only — the actual content is correct and recoverable
via `git show`, not re-fixed here to keep this patch's scope to the \revblue{} issue that actually
blocked an Overleaf sync decision.
