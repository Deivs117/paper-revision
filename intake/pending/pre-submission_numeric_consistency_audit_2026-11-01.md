# Pre-submission numeric consistency audit — 2026-11-01

Run while waiting on Diego's two rows. Nobody owned this; it is the kind of check that has already
caught two real problems this round (the Roll RMS contradiction → `C-69`, the Appetitive replicate
count → still open). **No number was changed anywhere. One finding needs an author decision.**

## Method
Recomputed the manuscript's reported statistics directly from the archived per-trial JSON under
`experiments/`, and cross-checked every figure quoted in the abstract and conclusions against the
body. Everything below is reproducible with `experiments/.venv_plotting/bin/python`.

## ✔ Clean

**Abstract.** All five figures (25 %, 33 %, 45 %, 85 %, 100 %) trace to the body and mean the same
thing there: the ablation collapse (25.0 % / 33.3 % from 100 %), Complex conflict (Neural 100 % vs
FSM 0 %) and the inspection task (85 % vs 45 %). No orphan number.

**Conclusions.** Every figure appears in `results.tex`/`methodology.tex`. The single apparent
exception, "2.5", is the term "2.5D maps", not a measurement.

**`tab:consolidated_simulation_metrics` vs the raw logs.** All **12 cells** (4 suites × T_sim / Roll
/ Pitch) reproduce exactly from `experiments/simulation/`, with the documented exclusion of
`familia_a_obstaculo/test_007_SUCCESS`. The table is faithful to its data.

## ⚠️ FINDING — the manuscript uses two different standard deviations, and does not say so

Reproducing those 12 cells only works with the **population** standard deviation (÷ n). With the
**sample** SD (÷ n−1) every cell is ~3.5 % larger. The discrepancy is perfectly systematic: the
ratio is sqrt(14/15) in every one, which is what identified it.

| Table | SD actually used | What the caption says |
|---|---|---|
| `tab:consolidated_simulation_metrics` | **population** (12/12 cells verified) | says nothing |
| `tab:fsm_comparison` | **population** (verified: Inclined Slope/Neural 7.160) | says nothing specific |
| `tab:inspection_metrics` | **sample** (verified: T_task 12.33 → 12.3) | "mean ± **sample SD**" ✔ |

So two tables report one convention and a third reports the other, none of the three agreeing on
what they disclose. `tab:inspection_metrics` is the only one that is both explicit and correct.

**Why it matters more than the 3.5 % suggests.** The correction factor is sqrt(n/(n−1)), so it grows
as n shrinks — and `tab:fsm_comparison` has rows with n = 3:

| Cell | n | as published (population) | as sample SD |
|---|---|---|---|
| `tab:fsm_comparison` Inclined Slope / Neural Roll RMS | 3 | 6.751 ± **7.160** | 6.751 ± **8.769** |
| `tab:fsm_comparison` Rugged Terrain / Neural Roll RMS | 6 | 1.827 ± **0.033** | 1.827 ± **0.040** |
| `tab:consolidated_simulation_metrics` T_sim Complex | 15 | 24.96 ± **10.36** | 24.96 ± **10.72** |
| `tab:consolidated_simulation_metrics` T_sim Aversive | 15 | 9.98 ± **2.07** | 9.98 ± **2.14** |

Reporting the population SD describes the 15 runs that were made; the sample SD estimates the
spread of the process those runs came from, which is what a reader comparing two controllers
assumes. For a paper whose Reviewer 2 opened with a sample-size objection (item 1), and which added
a whole paragraph on the limits of n = 12, the inconsistency is the kind of thing a statistically
attentive reviewer notices — and `R3b-05` explicitly asked for "statistical rules for experimental
samples" in the captions, which only `tab:inspection_metrics` currently provides.

## Options for the author (none applied)

1. **Disclose, change nothing.** Add "population SD over the n runs" to the two silent captions.
   Cheapest, honest, and leaves every published number intact — but keeps two conventions in one
   paper, which a reviewer may still flag.
2. **Unify on sample SD.** The usual convention for reporting a sample of trials. Requires
   regenerating both tables and re-checking any prose that quotes those ± values (the n = 3 row
   moves the most, 7.160 → 8.769). The means do not move at all.
3. **Unify on population SD.** Also defensible, but then `tab:inspection_metrics`'s caption has to
   stop saying "sample SD", and it is the convention a reviewer is less likely to expect.

Recommendation: **option 2** if there is time before the deadline, since it is what a reader assumes
and it removes the inconsistency rather than documenting it; **option 1** if there is not, because
an undisclosed convention is the only part that is actually wrong today.

## Not checked
`tab:mode_steady_state_energy` and the physical-trial tables: their per-trial sources were not
re-derived in this pass. If option 2 is chosen they need the same treatment.
