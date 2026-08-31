# Reviewer-simulation trim audit — A+B+C applied as C-22/C-23/C-24, D still awaiting author decision

**Status:** ✅ Author decided (2026-08-31) to proceed with candidates A+B+C now; D held. Applied as
`C-22` (caption trim, candidate A), `C-23` (conclusions.tex closing-paragraphs merge, candidate B),
`C-24` (terrain-latency paragraph merge, candidate C) — see their `PROGRESS.md` rows and
`patches/c-22-*`/`c-23-*`/`c-24-*`. `compile_pdf.sh` recompiled clean at 91 pages (unchanged — same
"prose cuts don't cross a page boundary here" effect already seen in `C-20`/`C-21`). Candidate D
(sim/physical neuron-by-neuron narration trim) remains an open decision — this doc stays in
`intake/pending/` until D is resolved one way or the other.

**Origin:** author request (2026-08-31, in-chat) — "simulate being a paper reviewer, look for what could
be omitted or is superfluous, report how much [page count] could be reduced by cutting it." Distinct
from `intake/processed/redundancy_closing_audit.md` (2026-08-31, same day): that audit hunted
near-verbatim restatement of the *same fact* across sections (R2-01's original complaint). This audit
instead asks a broader question — reading as a Reviewer 2/3 who thinks the paper is still too long and
wants deletions/condensations, not just dedup — so it also flags legitimately-informative-but-verbose
prose, caption bloat, and structural over-narration that isn't literal restatement.

## Method

Read `introduction.tex`, `methodology.tex`, `results.tex` (980 lines, full), `conclusions.tex` end to
end in this pass, adopting the stance: "if I were told to cut 10% of this paper's length without losing
its scientific claims, what would I mark first?" Candidates below are ranked by confidence (how likely
the cut is safe/uncontroversial) and risk (whether it removes content that answers a specific,
already-satisfied reviewer request from an earlier round — cutting that content risks reopening a
closed reviewer item).

## Candidates, ranked by confidence

### A. High confidence, low risk — mechanical caption trimming (results.tex)

Two frame-sequence figures each carry 4–6 subfigure captions plus a main caption, and the subcaptions
largely re-narrate what the body prose already says a few lines above/below:
- `fig:robot-6frames` (D1/D3/D5/D6, lines 507–538): ~140 words across 4 subcaptions, duplicating body
  prose at lines 505/540/542 (Hunting Instinct hold, aversive dispatch at ~46s, appetitive approach at
  ~50s/90s — all stated in prose already).
- `fig:RES_IMU_real` (E1/E3/E5/E6, lines 599–631): ~110 words, duplicating body prose at line 597.
- `fig:real_variable_topography_sequence` (Frames 1–6, lines 698–736 subcaptions + main caption): ~220
  words, duplicating Table~\ref{tab:terrain_sequence}'s own "Trigger / mechanism" column (lines 672–688)
  — the table and the 6 photo captions currently say the same six things twice.

**Estimated savings: ~250–300 words.** Fix: cut subcaptions to short factual labels ("t≈13s: enters
irregular terrain", not a full sentence re-deriving the mechanism); let the table or body prose carry
the explanation once. Low scientific risk — captions aren't where reviewers look for rigor, and nothing
here answers a specific reviewer question that isn't answered elsewhere.

### B. High confidence, low-medium risk — conclusions.tex's two overlapping closing paragraphs

Missed by the same-day redundancy audit because it only checked *cross-section* repeats — this pair is
**within** `conclusions.tex` itself. The paragraph starting "The findings provide a highly efficient
baseline..." (line 16, ~140 words) and the final paragraph starting "In conclusion, this paper
presented..." (line 20, ~90 words) both restate: bio-inspired architecture, works on embedded hardware,
avoids the training/computational overhead of RL/MPC. Line 20 is close to a compressed re-statement of
line 16 plus the contributions paragraph (line 12), functioning as a second "in conclusion" after the
paper already had one.

**Estimated savings: ~100–120 words.** Fix: merge into one closing paragraph — keep line 16's concrete
claims (embedded-hardware validation, sim+physical, energy-aware efficiency framing) and line 20's
hardware-boundary caveat, drop the restated "no heavy computational overhead / no expensive training"
clause since it's already said once. This is a genuine redundancy finding (same category as `C-20`/
`C-21`), not merely a length judgment call — worth doing regardless of whether it moves the page count.

### C. Medium confidence, low risk — terrain-latency 4-panel narrative (results.tex, lines 897–901)

Three consecutive paragraphs each walk through what the panels "reflect"/"capture" one at a time
(neural latency split, electromechanical coupling, emergency retraction) — informative but formulaically
repetitive in structure ("Panel X... reflects...", "Panel Y... by contrast..."). Could merge into one
tighter paragraph without dropping any of the four numeric latency claims (already stated once in the
caption itself, line 893).

**Estimated savings: ~80–100 words.**

### D. Medium confidence, medium-high risk — sim/physical single- and multi-stimulus neuron-by-neuron narration

`Single Stimulus Response` and `Response to Multiple Stimuli` are narrated twice — once for simulation
(lines 36–121, ~700 words combined) and once for the physical robot (lines 469–542, ~460 words combined)
— each walking through which specific neuron ($X_4$, $X_{11}$, $L_0$...) fires when. This is the closest
thing in the paper to what R2-01 originally flagged ("duplicated neural raster plots... between
simulation and physical tests"), but R2-01 already accepted this structure once (it's not near-verbatim
restatement — sim and physical differ in actual timing/values, e.g. the appetitive-approach paragraph
explicitly contrasts sim vs. physical rotation direction). Trimming here means deciding the
neuron-by-neuron walkthrough itself is more detail than needed, not fixing a duplicate.

**Estimated savings if trimmed ~30%: ~350 words.** Flagging as a candidate, not recommending
unilaterally — this content directly demonstrates the neural architecture's mechanism match between sim
and hardware, which is a substantive claim, not filler. Author should decide whether to cut.

### E. Low priority — introduction.tex citation-dump clause (line 8, final sentence)

"Recent platforms such as those published by \citet{Liu2024Max}, \citet{Cui2025FLORES}, and
\citet{Jiang2025RTaichi} further expand the design space..." (~35 words) adds three citations with no
individual discussion. Minor, ~35 words, not worth flagging as a real lever — listed for completeness
only.

### Reviewed, not flagged

- **QuantReal per-scenario mechanistic paragraphs** (Appetitive/Aversive/Complex/Obstacle,
  results.tex lines 766/789/812/835, ~560 words combined): each explains a *physical* cause (torque
  limiting, camera FOV, trajectory smoothing) for a pattern in the data — this is exactly the kind of
  explanatory depth a reviewer asks for when a figure alone would raise "why does this look like that?"
  questions. Not recommended as a cut target despite the length.
- **Methodology.tex**: no cut candidates found — it's the reproducibility backbone (equations,
  hyperparameter tables, physical BOM); cutting there trades page count for reviewer-facing rigor, a
  worse trade than anywhere in results.tex.
- **Reactive Inspection Task subsection** (results.tex lines 421–462): verbose but built specifically to
  answer R3-05's request point-by-point (SR, $d_{final}$, $T_{acquisition}$, timeout analysis,
  path-planning-scope caveat); cutting risks reopening that reviewer item.

## Total estimate and the honest caveat on page count

Summing the confident/medium items (A + B + C, the ones with low-to-medium risk): **≈430–520 words**.
Adding D (the riskier, author-judgment-call item): **≈780–870 words** total if everything here were cut.

This is 5–6× larger than the ~140 words cut in `C-20`/`C-21` earlier today, which left the compiled page
count unchanged at 91 pages (confirmed by recompile) — that cut was too small to cross a page boundary
in a results.tex section dominated by full-width figures/tables, where prose reflows into existing
whitespace around floats rather than pushing content onto a new page. ~800 words is a more plausible
candidate to move the count, but **this is not guaranteed** without an actual recompile after the edits
— float placement in LaTeX is non-linear, and a paragraph shrinking by a few lines can just tighten a page
that was already going to break there, doing nothing to the final count. Recommend: apply items A/B/C
(the safer ones) first, recompile, measure the actual delta, then decide whether item D is worth the
tradeoff based on the real number rather than this estimate.

## Next step

Awaiting author decision on: (1) proceed with A+B+C as `C-xx` corrections now, (2) also include D,
or (3) hold this audit as reference only and take no action. Once a decision is made, follow the normal
`next_id.sh C` → edit → `validate_tex.sh`/`check_roundtrip.sh` → `compile_pdf.sh` → `PROGRESS.md` row →
`patches/` record flow, same as `C-20`/`C-21`.
