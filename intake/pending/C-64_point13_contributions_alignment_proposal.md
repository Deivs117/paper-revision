# C-64 point 13 -- proposal: align Conclusions' contributions with the Introduction (NOT applied)

Source: `R3b-01_second_review_2026-10-28.md`, item 13. Status: proposal for author decision; no `sections/` file touched.

## The mismatch

| Introduction (`introduction.tex:34`), "three differentiating properties" | Conclusions (`conclusions.tex`, "contributions beyond the state of the art") |
|---|---|
| (i) biological interpretability (neuroscientific grounding) | -- not mentioned as a contribution |
| (ii) modularity: perception, arbitration and motor generation decoupled | -- only appears in the next-to-last paragraph, as a closing remark |
| (iii) autonomous energy-aware mode selection (wheels on flat ground, legs on complex terrain) | "First": multimodal robot that switches locomotion pattern (same idea, no energy framing) |
| -- | "Second": inertial sensor for postural stability (not an Introduction claim) |
| -- | "Finally": Naka--Rushton locomotor network with smoother transitions (not an Introduction claim) |

A reader (and Reviewer 3) sees two different lists for the same claim.

## Proposed replacement (Conclusions, the "However, this work introduces..." sentences)

Option A (recommended): make Conclusions mirror the Introduction and fold the two extra items in as evidence.

> However, this work contributes three differentiating properties beyond the state of the art. First, biological interpretability:
> the basal-ganglia-inspired arbitration and the Naka--Rushton-modulated locomotor network keep every decision traceable to named
> neural units. Second, modularity: perception, arbitration and motor generation are decoupled, so an individual stage (for example
> the inertial stability monitor) can be upgraded without redesigning the others. Third, autonomous mode selection that combines
> the efficiency of wheeled locomotion on flat surfaces with legged capability on complex terrain, switching gait in response to
> inertial and visual cues.

Claims are all backed elsewhere in the paper (Methodology: BG module and Naka--Rushton; Results: terrain switching and the physical-energy block). "Energy-aware" is kept out of the sentence's wording on purpose: say it only if the physical-energy block is explicitly framed as a comparison (author to confirm).

Option B: leave Conclusions as is and edit the Introduction's three properties to match. Not recommended: the Introduction wording is the one reviewers already read in round 1.

## Second half of item 13 (limitations / future work overlap)

`conclusions.tex` has a pointer paragraph to `ssec:Limitations` plus a final paragraph with the future-work list. They do overlap with `ssec:Limitations`, but the pointer paragraph is already one sentence and the future-work list is not repeated verbatim there. Recommendation: no change.

## To decide (author)
1. Option A or B (or neither).
2. Whether "energy-aware" may appear as a claim.
Once decided, add the approved edit under C-64 (row is still `drafted`).
