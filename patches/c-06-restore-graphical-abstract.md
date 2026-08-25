<!--
PATCH: C-06
Reviewer: —
Target section: sections/preamble.tex, assets/GRAPHICAL_ABSTRACT.pdf, .gitignore
Requirement: Supersedes C-03. C-03 diagnosed GRAPHICAL_ABSTRACT as missing from assets/ and
  commented out the graphicalabstract block — the diagnosis was wrong. The file was present on
  disk in assets/ (byte-identical to the copy tracked in the Overleaf repo) but the repo's
  .gitignore had a blanket `*.pdf` rule (meant for compile byproducts like build/paper.pdf) that
  was silently excluding it from git entirely, so it never reached GitHub and Sebas's clone
  legitimately never had it.
Status: applied
-->

**Root-cause fix:** `.gitignore` gained `!/assets/**` after the compile-byproduct patterns —
`assets/` mirrors the Overleaf project 1:1 and must never be excluded by extension, since it
legitimately holds PDF figures/graphics alongside images. `assets/GRAPHICAL_ABSTRACT.pdf` is now
tracked (`git add -f`-equivalent via the negation rule), verified byte-identical (`md5sum`) to the
copy in the Overleaf repo clone before staging.

**Content fix:** restored `sections/preamble.tex`'s `graphicalabstract` block to its original,
uncommented form — C-03's workaround is no longer needed.

**Verified:** `reassemble.py` → `validate_tex.sh` → `check_roundtrip.sh` all pass. No LaTeX
toolchain available on this machine to confirm a real `pdflatex`/`latexmk` compile succeeds with
the graphical abstract included — flagged as still-unverified, same limitation noted since the
pipeline was first built.

**Also worth checking:** the `!/assets/**` fix only surfaced because this one file was reported
missing. No other `assets/*.pdf` files were found silently excluded (checked via `git status
--ignored` before this fix — only `GRAPHICAL_ABSTRACT.pdf` was affected), but any future PDF asset
added before this fix landed would have hit the same silent exclusion.
