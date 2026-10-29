# C-60 — Trim the ablation prose that duplicates the figure captions (owner: Sam)

Self-contained brief: everything needed is in this repo. Nothing from the author's personal files is required.
Read first: `OUTLINE.md`, `CLAUDE.md` (revblue convention, patch flow, your row stops at `applied`),
`intake/pending/round2_decision_letter_2026-10-25.md` (R3 item 1 = the redundancy ask; R3 item 2 = captions).

## Problem
Reviewer 3 item 1 asks to condense duplicated statements. In `sections/results.tex`, subsection
"Basal Ganglia Ablation Study" (`\subsubsection{Basal Ganglia Ablation Study}`, ~l.190–219), the same numbers are
written twice, once in a caption and once in the prose next to it. The captions are NOT to be shortened: the
reviewer also asked for self-contained captions (R3 item 2, R2 item 5), and they were just rewritten for that.
**Cut the prose.**

## What to do (line numbers as of `main` @ 25c26ed — re-check with `grep` before editing)
1. **~l.194** (success-rate paragraph, Complex Navigation): repeats 25.0 %, 33.3 %, 83.3 % and their p-values, all
   in `fig:ablation_success_rate` / the umbrella caption (~l.211). Keep the gradient and the interpretation
   ("removing mechanism collapses success; threshold-only degrades mildly and non-significantly"), cite the
   figure for the numbers. Keep the no-conflict result (91.7–100 %, p=1.000): it is not in any caption.
2. **~l.215** (latency + attitude paragraph): Roll RMS (+43.6 / +45.9 / +22.0 %) and Pitch RMS
   (+6.4 / −11.3 / −5.7 %) with p-values are in the umbrella caption (b). Keep the **decision-latency** numbers
   (81.7/66.6/75.9/109.1 ms with CIs, p=0.014): they appear in no caption. Keep the interpretation (roll degrades
   for all three; pitch diverges, plausibly because of failed trials). Drop the percentages and p-values that the
   caption already carries.
3. **~l.219** (your own R2b-01 paragraph, optional): re-derives n=12, p and the CI for *threshold only* that
   appear above. Shorten to the two conclusions + the future-work sentence. **Keep** the Fisher boundary
   argument (≥5 of 12 failures needed for p<0.05) and the future-work sentence: they answer reviewer 2 item 1.

## Do NOT touch
- Any `\caption` in that subsection (mine, merged in PR #3).
- The `\revblue{}` wrapper convention: trimmed-away text needs no marker; rewritten sentences do.
- n=12 anywhere in the prose of this subsection (R2b-01 wants it explicit).

## Numbers source (in repo)
`experiments/R3-02-wta-vs-threshold/output/ablation_stats_summary.csv` (committed). `experiments/*/data/` is
gitignored — you do not need raw data for a prose trim.

## Flow
`git pull origin main` → branch → edit `sections/results.tex` → `python3 scripts/reassemble.py`,
`scripts/validate_tex.sh`, `scripts/check_roundtrip.sh` → patch record `patches/c-60-ablation-prose-trim.tex` →
set row C-60 to `applied` in `PROGRESS.md` → PR into `main`. Never run the Overleaf scripts.
Acceptance: no number or p-value in the two paragraphs also appears in the umbrella caption or subcaptions,
except where the sentence would stop being understandable.
