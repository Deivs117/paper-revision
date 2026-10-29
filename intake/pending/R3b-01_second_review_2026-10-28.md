# R3b-01 / R3b-05 / R2b-01 / R2b-06 — second review (2026-10-28, on `main` after PR #1 and #2)

Method: 4 independent read-only passes (methodology, results, cross-section, skeptical Reviewer 3),
checked against `round2_decision_letter_2026-10-25.md`. Items marked ✔ were re-verified by `grep`
after the passes; the rest are the agents' findings with their stated confidence.
**Rule for every trim below: cut the PROSE, never the caption** — R2b-05/R3b-02/R3b-05 need captions
self-contained. **Do not touch:** joint-noise caveat (R2b-02/R3b-03 ask for more of it), n=12 and N in
captions, anomalous Obstacle-trial exclusion (R2b-03, Diego), physical-energy block (done).

Verdict: R3b-05 (Sebas) **complete**. R3b-01 (Sebas) **partial** — below. R2b-01/R2b-06 (Sam)
**complete**, with two follow-ups.

## For Sebas — R3b-01 round 2 (keep the row `applied`; add a `C-xx` follow-up, `next_id.sh C`)

### Methodology (`methodology.tex`)
1. ✔ **Duplicate weight in Table Locom_NN** (lines 255 and 268): `ω_{Gpe_R→X_4}` and `ω_GpeR` are both 2.0
   (eq. z4 uses only `ω_GpeR`). Keep one row. **Confirm in `PETER_SIMULATION` before merging** — the only
   evidence found is a comment (`red_neuronal.py:379`), not the literal assignment. Same check for the
   pair `ω_{X4→X7}`/`ω_{X3→X8}` = 10.0 vs `w` = 10.0 (medium confidence).
2. **Rationale paragraph (l.291)** restates table values (160.0, 2.0, 1.0, 10.0): keep the *why*, drop the numbers.
3. ✔ **`HI` defined three times** (eq. at l.227, table note, rationale): keep the equation's definition.
4. Lower priority: stimulus→mode arrows re-written in parentheses (l.306); `σ_az` defined at l.68 and again
   ~l.337; sensor roles described at l.27 and l.74; inspection scenario (20 trials, 90 s, no noise) in l.62
   and in `tab:inspection_metrics`' caption.

### Results (`results.tex`) — prose ↔ caption repeats, trim the prose
5. l.562 vs 567: inspection scatter numbers ($1.081\pm0.042$ m …) restated in prose.
6. l.317 vs 296: "all 30 trials never crossed TR" — already in the caption.
7. l.320 vs 303: tail numbers (13.3%, ≈0.6 s, 0.9–1.8 ms) in prose and caption.
8. l.142 vs 152: "8 tipovers and 4 crashes out of 27" in prose and caption.
9. l.91/82/128 + 73: "every retained trial across all five levels succeeded" said four times; one sentence before the per-scenario paragraphs.
10. Lower: l.575 vs 580 (11/20, 93–99%).
*(Ablation, l.194/213/215/219: Deivi handles it — touches R3b-02 and Sam's paragraph. Don't edit.)*

### Conclusions / abstract wording (`conclusions.tex`)
11. l.4–6: paragraphs 2 and 4 re-narrate neurons/signals already in Results; ✔ `L_4` and `σ_az` appear in
    Conclusions but **nowhere in `results.tex`** — drop or cite the figure.
12. ✔ **RESOLVED — wording only.** `conclusions.tex:8` and `methodology.tex:196` say "184--534 ms" as if it were
    a range, but per the caption of `fig:FourPanelLatencies` (`results.tex:1025`) they are the *means of two
    different directions*, over 15 hardware replicates: Panel A Quadrupedal→Differential Rolling μ=0.184 s,
    Panel B Differential Rolling→Quadrupedal μ=0.534 s. Reword both places as "mean neural latency of 184 ms
    (quadrupedal→rolling) and 534 ms (rolling→quadrupedal)". No need to re-check the figure; Results' own prose
    already states the split correctly.
13. Medium/low: the contribution list in Conclusions (l.12) doesn't match the three "differentiating
    properties" in the Introduction (~l.34); limitations/future-work paragraphs (l.14–18) overlap `ssec:Limitations`.

## For Sam — follow-ups (rows stay `applied`) — **only item 14 is required**
14. ✔ **`preamble.tex:85` (Abstract): "consistently avoided critical instability" is untraceable** — the phrase
    appears in no other section. Replace with a measured claim (Roll/Pitch RMS) or soften.
15. ✔ **RESOLVED — Sam has nothing to do here.** The GA's 15/15, 0/15, 17/20 and 9/20 are all correct:
    `experiments/R2-02-fsm-baseline/output/table_master_comparison.csv` (built by `build_master_table.py`) has
    Complex Neural n_attempted=15/n_success=15, Complex FSM 15/0, Inspection Neural 20/17, Inspection FSM 20/9.
    The only gap is that `tab:fsm_comparison` in the manuscript doesn't print N per row; Deivi adds it under R2b-05.
16. Optional: the R2b-01 paragraph (results l.219) re-derives n=12, p and the CI for *threshold only* that
    already appear at l.196/213; shorten it to the two conclusions + the future-work sentence.

## For Deivi (own rows)
- **R3b-02/R3b-01 overlap:** ablation Roll/Pitch % and p-values are written in full in the (b) caption
  (l.213) and in the prose (l.215); l.194 also repeats the success-rate numbers. Trim the prose, keep captions.
- **R2b-05:** `fig:mode_timeline_inspection` (l.580) lacks N and how the representative trial was chosen;
  `tab:fsm_comparison` has no per-row N.
- **R2b-03 (Diego, reopened):** the FSM caveat must also go into the 3 FSM figure captions (l.546/555/613).
