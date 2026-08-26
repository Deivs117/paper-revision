> **Looking for a general-understanding overview in Spanish?** See `RESUMEN.md`. This document
> stays the authoritative technical spec — `RESUMEN.md` is a companion, not a replacement.

## Technical Summary: Architecture & Pipeline Overview

### 1. Core Challenge & Technical Requirements

* **Journal & Deadline:** Major revision for *Robotics and Autonomous Systems* (Manuscript `ROBOT-D-26-00122R1`). Resubmission deadline: **August 31, 2026**.
* **Reviewer Requirements Breakdown:**

**Reviewer 2 (Streamlining & Minor Additions):**
* Heavily condense repetitive text, remove duplicate neural raster plots/identical stability curves between simulation and hardware tests, merge metric definitions, and shorten the symbolic warehouse simulation section.
* Add Finite State Machine (FSM) gait arbitration baseline comparisons.
* Consolidate all limitations into a dedicated section.
* Add multi-mode long-term average energy consumption data and onboard MLP computing overhead analysis.

**Reviewer 3 (Major Structural & Experimental Additions — High Priority):**
* Conduct explicit ablation analysis on the basal ganglia arbitration network.
* Perform comparative tests removing key neural layers or inhibitory connections to justify the Winner-Take-All (WTA) mechanism over threshold logic.
* Supplement control strategies or compensation algorithms for low-torque servo constraints and open-loop gait instability.
* Design perception-decision noise robustness experiments (IMU drift, LiDAR noise, camera illumination distortion).
* Add inspection task performance metrics (target tracking accuracy, coverage rate, autonomous re-planning).
* Revise the literature review with horizontal comparative tables contrasting Basal Ganglia, CPG, and RL-based action selection algorithms.

---

### 2. Team Workflow & System Constraints

* **Source Format:** The entire manuscript exists as a single monolithic `.tex` file, hosted on Overleaf and mirrored via Overleaf's built-in git bridge (`git.overleaf.com`).
* **Team Operations:** Co-authors and professors operate exclusively within the Overleaf web interface. They do not use branches or standardized commit discipline; Overleaf auto-commits their edits to its own git history.
* **Structural Variability:** Edits in Overleaf involve arbitrary line additions, text reordering, section movement, and block deletions. Line numbers are never stable across syncs.
* **Two independent git repositories are involved, with a strict division of labor:**
  * The **Overleaf repo** (clone of `git.overleaf.com/<project-id>`) — **sync-only**. Nothing is hand-edited here. Its sole purpose is exchanging content with Overleaf's web editor; it is never a place to draft, patch, or compile.
  * **This repo, `paper-revision`** (GitHub) — where all real work happens: text editing/patching, asset management (bibliography, figures, class files), and PDF compilation.
* **Primary editor is the repo owner, not just an AI agent.** All edits, human or AI-generated, go through the same formal path: a `sections/<slug>.tex` change tied to a `PROGRESS.md` row and recorded in `patches/`. This keeps every change — however small — traceable and prevents silent, unreviewable drift in the manuscript.

---

### 3. Repository Topology & Folder Structure

| Repo | Local path (example) | Remote | Role |
|---|---|---|---|
| Overleaf mirror | `../<overleaf-project-id>/` (sibling directory to this repo) | `https://git.overleaf.com/<overleaf-project-id>` | Sync-only pass-through. |
| `paper-revision` (this repo) | `.` | GitHub, `origin` | Editing, patching, compiling. |

```
paper-revision/
├── OUTLINE.md                   # cheap global-context map, read before any section-level edit (§4.5)
├── source/
│   └── main_monolithic.tex      # generated — never hand-edited (§5)
├── sections/
│   ├── manifest.json            # ordered list of section files; order lives HERE, not in filenames
│   ├── preamble.tex
│   ├── introduction.tex
│   ├── related-work.tex
│   └── ...                      # one file per top-level \section{}, named by slug only
├── assets/                      # 1:1 mirror of the Overleaf project root, excluding the main .tex
│   ├── references.bib
│   ├── <custom-class>.cls       # if the journal template ships one
│   └── figures/
│       └── ...
├── build/                       # gitignored — compile_pdf.sh output only
│   ├── tex-src/                 # assembled copy used for compilation
│   └── paper.pdf
├── patches/
│   └── <id>-<slug>.tex          # audit copy of each applied change
├── intake/                      # raw material you or teammates drop in (§8)
│   ├── pending/                 # not yet turned into PROGRESS.md rows
│   ├── processed/                # moved here once processed, kept for audit
│   └── SOURCES.md               # registry of sibling repos the agent may read (read-only)
├── experiments/                 # generates figures/data that don't exist yet (§9)
│   ├── README.md
│   ├── _TEMPLATE/                # copy this to start a new experiment
│   └── <ID>-<slug>/
│       ├── README.md            # goal, params/seed, data provenance, how to regenerate
│       ├── config.yaml
│       ├── scripts/              # numpy/matplotlib/ROS2/etc. allowed here (exempt from stdlib-only)
│       ├── data/                 # gitignored — raw sim/hardware output, regenerable
│       └── output/               # committed — final CSVs/figures, source for promote_figure.sh
├── scripts/
│   ├── config.sh
│   ├── pull_from_overleaf.sh
│   ├── push_to_overleaf.sh
│   ├── split_sections.py
│   ├── reassemble.py
│   ├── find_section.py
│   ├── validate_tex.sh
│   ├── compile_pdf.sh
│   ├── check_roundtrip.sh
│   ├── promote_figure.sh        # experiments/<id>/output/* -> assets/ (§9)
│   ├── check_hardcoded_refs.sh  # advisory: hardcoded "Section N" refs (§10.1)
│   ├── next_id.sh                # next available N-xx/C-xx ID (§10.3)
│   ├── check_target_conflicts.sh # advisory: other rows targeting the same section (§10.4)
│   ├── install_hooks.sh          # one-time: installs the pre-commit hook (§10.2)
│   ├── hooks/pre-commit          # template copied into .git/hooks/ by install_hooks.sh
│   ├── strip_revblue.py          # start-of-round: unwrap last round's \revblue{} (§11)
│   └── build_dashboard.py        # PROGRESS.md -> docs/data.json (§12)
├── docs/                        # GitHub Pages traceability dashboard (§12)
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── data.json                 # generated — never hand-edited
├── PROGRESS.md
├── README.md
└── CLAUDE.md
```

**Filename mapping.** The Overleaf main file (`elsarticle-template-num-names.tex`) and this repo's mirror (`source/main_monolithic.tex`) refer to the same content but are never the same file on disk — renaming happens only inside `pull_from_overleaf.sh` / `push_to_overleaf.sh`. Everything else in the Overleaf project (bibliography, figures, class/style files) mirrors into `assets/` **under its original relative path and filename** — no renaming for those.

Overleaf git authentication uses a per-project git token (`olp_...`) as the password with username `git`, cached via `git config --global credential.helper store`. Never write this token into any file in either repository — it lives only in the local git credential store.

---

### 4. Token-Efficient Agent Workflow

The point of `sections/` and `OUTLINE.md` together is that an agent (human or AI) doing one patch never needs to read the whole manuscript.

#### 4.1 What an agent reads for a typical patch
1. `OUTLINE.md` — always. Small (a few hundred tokens), gives global context: what each section covers, key terminology, and known cross-references between sections.
2. `PROGRESS.md` — to pick or confirm the requirement being addressed and its target section(s).
3. **Only** the target `sections/<slug>.tex` file(s) named in that `PROGRESS.md` row — not the full monolith, not unrelated sections.

#### 4.2 When a broader scan is warranted
If a requirement genuinely needs cross-section awareness (e.g. R2-01's "remove duplicate plots between simulation and hardware tests" spans two sections), the agent decides this itself from what `OUTLINE.md` and the requirement text imply, and reads the additional specific `sections/*.tex` files it identifies as relevant — never the full `source/main_monolithic.tex` as a default move. Reading the monolith directly should be rare and deliberate, not a fallback habit.

#### 4.3 `OUTLINE.md` — the cheap global-context file

Root-level file, maintained by hand (occasionally with agent help), **not regenerated automatically** by any sync script — accurate summarization needs understanding, not parsing. Update it whenever the section structure changes materially (a section added, merged, or its scope shifts).

Format:

```markdown
# Outline — ROBOT-D-26-00122R1

## Abstract (1 line)
<one-sentence summary of the paper's contribution>

## Sections
- introduction.tex — <1-line: what it covers>
- related-work.tex — <1-line, e.g. "comparative table Basal Ganglia vs CPG vs RL (R3-06)">
- ablation-study.tex — <1-line, note if new/empty pending R3-01/R3-02>
- ...

## Key terms / notation
- WTA = Winner-Take-All
- ...

## Known cross-references
- ablation-study.tex results are cited in discussion.tex
- ...
```

#### 4.4 Cost discipline
- Never pass the full `source/main_monolithic.tex` to an AI agent as routine input for a single-section patch.
- `OUTLINE.md` + `PROGRESS.md` row + target `sections/*.tex` file(s) is the default context bundle for a patch.
- `find_section.py` (§5.4) exists precisely so an agent can learn "what changed since last sync" without diffing or reading the whole file itself.

---

### 5. Automation Pipeline

```
[Overleaf web UI]                                        [paper-revision repo: all real work]
   co-author edits                                          text patching · asset updates · compile
        │                                                          │
        ▼                                                          │
  Overleaf auto-commit                                             │
  (git.overleaf.com)                                               │
        │                                                          │
        ▼   scripts/pull_from_overleaf.sh                          │
        │   guard: abort if any commit since the last              │
        │   "sync:"/"chore: mark synced" marker touches             │
        │   source/, sections/, or assets/ (§5.1) — unpushed        │
        │   local work would otherwise be lost                      │
        ▼                                                          │
  git pull (cached token)                                          │
     │        │                                                    │
     │        └─copy+rename main tex──▶ source/main_monolithic.tex │
     └─mirror everything else─────────▶ assets/                    │
                                                     │               │
                                        split_sections.py runs,      │
                                        THEN commit "sync: ..."      │
                                       (source + sections + assets   │
                                        all in one commit = new      │
                                        synced checkpoint)           │
                                                     │               │
                                                     ▼               │
                                          scripts/find_section.py    │
                                        (upward-scan on the sync diff:
                                         which sections/*.tex changed)
                                                     │
                                                     ▼
                                     agent reads OUTLINE.md + PROGRESS.md
                                     + only the target sections/*.tex (§4),
                                     edits sections/*.tex and/or assets/
                                     (new figures, updated .bib)
                                                     │
                                          commit "patch: <ID> <summary>"
                                       (+ patches/<ID>-<slug>.tex audit copy,
                                          PROGRESS.md status → applied)
                                                     │
                                                     ▼
                                          scripts/reassemble.py
                                        sections/*.tex (manifest order,
                                        byte-exact join — see §5.2/5.3)
                                          ──▶ source/main_monolithic.tex
                                                     │
                                                     ▼
                                   scripts/validate_tex.sh (fast structural check)
                                   scripts/compile_pdf.sh (real compile, if toolchain
                                   installed) — both must pass before pushing
                                                     │
        ◀───────────── scripts/push_to_overleaf.sh ─┘
  guard: git pull Overleaf repo first;
  abort if it brings new commits
        │
        ▼ (only if guard passes)
  mirror assets/ + copy/rename main tex, commit, git push,
  then commit "chore: mark synced to Overleaf" (empty commit,
  new synced checkpoint) in paper-revision
        │
        ▼
  Overleaf reflects the change live
  (PROGRESS.md status → synced-to-overleaf)
```

**Golden rules:**
- `source/main_monolithic.tex` is always generated (by `pull_from_overleaf.sh` or `reassemble.py`) — never hand-edited.
- `sections/*.tex` is the editable working copy of the manuscript text. `assets/` is the editable working copy of everything else (bibliography, figures, class files) — both are mirrored to/from Overleaf, but edited locally in between syncs.
- Every edit — human or AI, however small — goes through `sections/` + a `PROGRESS.md` row + a `patches/` record. There is no separate "quick edit" bypass; this is what keeps the pull guard (§5.1) able to trust "no marker-less commit touching these paths" as proof nothing is unsynced.
- The Overleaf repo clone is **sync-only** — no drafting, patching, or compiling happens there.

---

### 5.1 `scripts/pull_from_overleaf.sh`

1. **Guard against data loss:** find the most recent commit in this repo whose message starts with `sync: pull from Overleaf` or `chore: mark synced to Overleaf` (call it `$LAST_MARKER`; if none exists yet, skip this check — first run). Run `git log $LAST_MARKER..HEAD --oneline -- source sections assets`. If that returns any commits, abort: local work exists that hasn't been pushed to Overleaf yet. Run `push_to_overleaf.sh` first. (Cross-check `PROGRESS.md` for rows still in `applied` as a human-readable hint of what's pending, but the git-log check above is the actual guard — it catches every local change, not only ones tied to a tracked reviewer ID.)
2. `git -C "$OVERLEAF_DIR" pull origin main`. On failure (auth, conflict), print the error and exit 1.
3. Copy `$OVERLEAF_DIR/$OVERLEAF_MAIN_FILE` → `$MIRROR_FILE` (overwrite).
4. Mirror everything else: `rsync -a --delete --exclude='.git' --exclude="$OVERLEAF_MAIN_FILE" "$OVERLEAF_DIR"/ "$ASSETS_DIR"/`.
5. If `git diff --quiet -- "$MIRROR_FILE" "$ASSETS_DIR"` shows no changes, print `"No changes since last sync."` and exit 0 without committing.
6. Otherwise, run `scripts/split_sections.py` now (before committing), so `sections/` reflects the new content.
7. `git add "$MIRROR_FILE" "$ASSETS_DIR" sections/`, commit with message `sync: pull from Overleaf (<YYYY-MM-DD HH:MM>)`. This single commit is the new synced checkpoint referenced by step 1's guard.

Exit codes: `0` = success, `1` = error or guard-abort.

### 5.2 `scripts/split_sections.py`

Splits `source/main_monolithic.tex` into `sections/`. Pure text/regex split — no LaTeX parser, no `\input`/`\include` resolution.

* Split points are lines matching `^\s*\\section\{`. Only **top-level** `\section{}` commands are split boundaries; `\subsection{}` etc. stay embedded inside their parent section's file.
* Start of file up to (not including) the first `\section{}` → `sections/preamble.tex`.
* Each `\section{Title}` block → `sections/<slug>.tex`, where `<slug>` is the title lowercased, non-alphanumeric characters replaced with `-`, collapsed/trimmed (e.g. `\section{Related Work}` → `sections/related-work.tex`). **No numeric prefix** — ordering lives only in `manifest.json`.
* If two sections produce the same slug (duplicate titles), disambiguate deterministically by appending `-2`, `-3`, ... in order of appearance.
* `\end{document}` (inclusive) plus anything trailing after the last section → `sections/closing.tex`.
* **Byte-exact boundaries, required invariant:** each section's captured text runs from its `\section{}` line up to (but not including) the byte where the next split-boundary line starts — meaning all blank lines, trailing whitespace, and comments between two sections belong to the **earlier** section's file, exactly as they appeared in the source. No content is dropped, added, or normalized during the split.
* Before writing, delete all existing `sections/*.tex` files (full regeneration every run).
* Write `sections/manifest.json`: an ordered array of `{"file": "related-work.tex", "title": "Related Work"}` objects (`preamble.tex` and `closing.tex` included, `"title": null` for those two).

When an agent adds a **brand-new** section locally, it creates `sections/<slug>.tex` directly and inserts an entry for it at the right position in `manifest.json` by hand.

### 5.3 `scripts/reassemble.py`

Reads `sections/manifest.json` in order and **concatenates each listed file's raw bytes with no separator inserted** — the exact inverse of §5.2's byte-exact split. Writes the result to `source/main_monolithic.tex`.

**Required invariant — round-trip idempotency:** running `split_sections.py` immediately followed by `reassemble.py`, with no edits in between, MUST produce a `source/main_monolithic.tex` that is byte-identical to what went in. If it isn't, the split boundaries in §5.2 are wrong — treat any such diff as a bug, not an acceptable side effect. `scripts/check_roundtrip.sh` (§5.7) verifies this automatically.

### 5.4 `scripts/find_section.py`

Upward-scan / diff-to-section mapper. Usage: `find_section.py [<git-rev-range>]`, default range `HEAD~1..HEAD`.

1. Run `git diff <range> -- source/main_monolithic.tex` and parse unified-diff hunk headers (`@@ -a,b +c,d @@`).
2. For each hunk, take the starting line number in the new file and scan upward through `source/main_monolithic.tex` until finding the nearest preceding `^\s*\\section\{...\}` line, or the top of file (→ preamble).
3. Print one line per hunk: `<section-title> (sections/<slug>.tex): lines <start>-<end> changed`, using `sections/manifest.json` to resolve title → filename.

Read-only: never modifies files.

### 5.5 `scripts/validate_tex.sh`

Fast structural sanity check on `source/main_monolithic.tex`, no LaTeX toolchain required:
* Braces `{`/`}` balanced (equal count).
* `\begin{document}` and `\end{document}` both present, exactly once each.
* Every `\begin{X}` has a matching `\end{X}` (stack-based check by environment name).

Exit 1 with a description of the first failure found; exit 0 if all checks pass. Run before every `push_to_overleaf.sh`.

### 5.6 `scripts/compile_pdf.sh`

Real compilation check, requires a local LaTeX toolchain (`latexmk` preferred, fallback `pdflatex` + `bibtex`/`biber` run twice). The one script allowed to depend on external tooling.

1. `rm -rf "$BUILD_DIR/tex-src"`, recreate it.
2. Copy `$ASSETS_DIR/` into `$BUILD_DIR/tex-src/` (preserving relative paths).
3. Copy `source/main_monolithic.tex` into `$BUILD_DIR/tex-src/$OVERLEAF_MAIN_FILE` (original Overleaf filename, so the build matches what Overleaf itself would compile).
4. `cd "$BUILD_DIR/tex-src" && latexmk -pdf -interaction=nonstopmode "$OVERLEAF_MAIN_FILE"` (or the `pdflatex`/`bibtex` fallback sequence).
5. On success, copy the resulting PDF to `$BUILD_DIR/paper.pdf`. On failure, print the LaTeX log tail and exit 1.

`build/` is gitignored entirely — disposable, never committed.

### 5.7 `scripts/check_roundtrip.sh`

Verifies the invariant in §5.3. Copies current `source/main_monolithic.tex` aside, runs `split_sections.py` then `reassemble.py`, diffs the result against the copy, restores the original file, and exits 1 if any diff was found (printing it). Cheap, dependency-free — safe to run after any change to `split_sections.py`/`reassemble.py` themselves, and worth running once after implementing them.

### 5.8 `scripts/push_to_overleaf.sh`

1. **Guard:** `git -C "$OVERLEAF_DIR" pull origin main`. If this brings in new commits, **abort** — tells the user to re-run `pull_from_overleaf.sh` and re-check for conflicts before pushing. Never force-push, never auto-merge.
2. Run `scripts/validate_tex.sh`; abort on failure. Run `scripts/compile_pdf.sh` if a LaTeX toolchain is available; abort on failure (warn-and-continue only if the toolchain itself is missing).
3. Mirror back: `rsync -a --delete --exclude='.git' "$ASSETS_DIR"/ "$OVERLEAF_DIR"/`, then copy `$MIRROR_FILE` → `$OVERLEAF_DIR/$OVERLEAF_MAIN_FILE`.
4. `git -C "$OVERLEAF_DIR" add -A`, commit `sync: apply patches from paper-revision (<YYYY-MM-DD HH:MM>)`, `git push origin main`.
5. On success, in **this** repo: `git commit --allow-empty -m "chore: mark synced to Overleaf (<YYYY-MM-DD HH:MM>)"`. This is the new synced checkpoint the §5.1 guard looks for.

All shared paths (`OVERLEAF_DIR`, `OVERLEAF_MAIN_FILE`, `MIRROR_FILE`, `ASSETS_DIR`, `BUILD_DIR`) come from `scripts/config.sh` — no script hardcodes them.

---

### 6. `PROGRESS.md` — Unified Change Tracking

A markdown table at the repo root, one row per change — of **any** origin. Three ID namespaces share this one table and one pipeline:

* `R2-xx` / `R3-xx` — reviewer-mandated items, fixed list below (do not renumber).
* `N-xx` — new content, from an `intake/` doc describing something to write about (e.g. a teammate's implementation). Numbered sequentially as they're created, never reused.
* `C-xx` — standalone corrections/edits that don't map to a reviewer item. Same numbering rule.

Every row — regardless of namespace — goes through the identical flow: identify target section(s), edit, record in `patches/`, update status, push. There is no separate tracking file for `intake/`-originated work; see §8.

The `R2-xx`/`R3-xx` rows are fixed at the outset (do not renumber — these IDs are referenced by patch filenames and commit messages):

| ID | Reviewer | Requirement (short) | Target section(s) | Data source | Status | Patch file |
|---|---|---|---|---|---|---|
| R2-01 | 2 | Condense repetitive text / remove duplicate plots / merge metric definitions / shorten warehouse sim section | TBD | — | pending | — |
| R2-02 | 2 | Add FSM gait arbitration baseline comparison | TBD | TBD | pending | — |
| R2-03 | 2 | Consolidate limitations into one dedicated section | TBD | — | pending | — |
| R2-04 | 2 | Add multi-mode energy consumption + onboard MLP compute overhead analysis | TBD | TBD | pending | — |
| R3-01 | 3 | Ablation analysis on basal ganglia arbitration network | TBD | TBD | pending | — |
| R3-02 | 3 | Comparative tests removing neural layers/inhibitory connections to justify WTA over threshold logic | TBD | TBD | pending | — |
| R3-03 | 3 | Control/compensation strategies for low-torque servo constraints and open-loop gait instability | TBD | TBD | pending | — |
| R3-04 | 3 | Perception-decision noise robustness experiments (IMU drift, LiDAR noise, camera illumination distortion) | TBD | TBD | pending | — |
| R3-05 | 3 | Inspection task performance metrics (tracking accuracy, coverage rate, autonomous re-planning) | TBD | TBD | pending | — |
| R3-06 | 3 | Literature review comparative tables: Basal Ganglia vs CPG vs RL-based action selection | TBD | — | pending | — |

Status values (exactly these strings, lowercase): `pending` → `drafted` → `applied` → `synced-to-overleaf`. `applied` means committed locally but **not yet pushed to Overleaf**. Update `Target section(s)` with the actual `sections/<slug>.tex` file(s) once identified.

`Data source` is `—` for rows that are pure prose/reorganization, and points at `experiments/<ID>-<slug>/` for rows that need a figure/number that doesn't exist yet — see §9.

---

### 7. `patches/` — Audit Trail

One file per patch: `patches/<id>-<slug>.tex` (lowercase ID, e.g. `patches/r3-02-wta-ablation.tex`). A **record of what changed**, not the live working file (the live copy is the corresponding `sections/<slug>.tex`, edited in place). Header format, as LaTeX comments:

```latex
% PATCH: R3-02
% Reviewer: 3
% Target section: sections/ablation-study.tex
% Requirement: Comparative tests removing key neural layers or inhibitory
%   connections to justify the Winner-Take-All (WTA) mechanism over threshold logic.
% Status: applied

<the new/changed LaTeX content, exactly as inserted into the target section file>
```

The pasted content itself must be wrapped in `\revblue{...}` — see §11's revision-round color convention. A patch resulting from a repo-wide structural operation rather than a single-section content change (e.g. `C-02`, stripping `\revblue{}` at the start of this round) records a `.md` summary instead of a content copy — see `patches/c-02-strip-revblue.md` for the precedent.

Commit convention: stage the modified `sections/<slug>.tex` (and/or `assets/` files), the new `patches/<id>-<slug>.tex`, and the `PROGRESS.md` status update, in one commit: `patch: <ID> <short summary>` (e.g. `patch: R3-02 add WTA ablation comparison`).

---

### 8. `intake/` — Turning Raw Docs into Patches

The entry point for anything that isn't a reviewer requirement: context on a new system a teammate built (to be written up in, say, the Results section), a loose list of corrections, notes copied from elsewhere. This is the repo owner's primary way of feeding work into the pipeline.

#### 8.1 Dropping in a document
Place a markdown file in `intake/pending/`. No fixed format required — it can be freeform notes, a bullet list of corrections, a teammate's existing doc pasted in as-is. If it references material from another repo (e.g. firmware/simulation findings), say so in the doc and/or check `intake/SOURCES.md` for the right path — don't inline large external content, point at it.

#### 8.2 Processing a pending document
1. Read `OUTLINE.md` first (§4) for global context — same discipline as any other patch.
2. Read the `intake/pending/<doc>.md` file in full.
3. If it references an external repo, read only the specific files it points to from that repo (via `intake/SOURCES.md`) — read-only, never edit anything outside `paper-revision/`.
4. Decide which target section(s) in `sections/` this belongs to (using `OUTLINE.md`'s per-section descriptions; read the actual target section file(s) to see how the new material should fit stylistically).
5. For each distinct change identified in the document, add one row to `PROGRESS.md` with the next available `N-xx` (new content) or `C-xx` (correction) ID, its target section(s), and status `pending`.
6. From there, each row follows the normal flow (§5, §6, §7): draft → `sections/` edit → `patches/<id>-<slug>.tex` → `applied` → `reassemble` → `push` → `synced-to-overleaf`.
7. Once every change extracted from the document has reached `applied` or later, move the file from `intake/pending/` to `intake/processed/` (git `mv`, so history is preserved) — this is the record that the document was fully triaged, not just read.

#### 8.3 `intake/SOURCES.md`
A short registry of sibling repositories the agent may read from (never write to) when an intake document references implementation details it doesn't fully restate. One line per repo:

```markdown
- PETER_SIMULATION — ../PETER_SIMULATION — firmware, ROS 2 simulation, hardware findings. Read-only.
```

Add a line here whenever a new external repo becomes relevant as source material. This list is intentionally small — it's a pointer registry, not a mirror; nothing from these repos is copied into `paper-revision`.

---

### 9. `experiments/` — Generating New Figures/Data

§§5–8 all assume the figure or number being written about already exists somewhere reachable (`assets/`, the manuscript's own prior text). Several checklist items don't work that way: `R3-01` (basal-ganglia ablation), `R3-04` (noise-robustness sweeps), `R3-05` (inspection metrics), and potentially `R2-02`/`R2-04`/`R3-02`/`R3-03` need a figure or table that **does not exist yet**, likely produced by running new simulations (possibly via `PETER_SIMULATION`) or reprocessing real hardware logs. `experiments/` is where that generation work happens, strictly upstream of `assets/` and `sections/`.

#### 9.1 Layout

```
experiments/
├── README.md                    # short pointer version of this section
├── _TEMPLATE/                   # copy this to start a new experiment
└── <ID>-<slug>/                 # e.g. R3-01-basal-ganglia-ablation/
    ├── README.md                # goal, method, parameters/seed, data provenance, how to regenerate, output list
    ├── config.yaml               # run parameters, kept out of code so a rerun is exact/diffable
    ├── scripts/                  # generation code
    ├── data/                     # gitignored — raw sim/hardware output (bags, logs, video); regenerable
    └── output/                   # committed — final small CSVs + the exact figure files
```

* Directory name reuses the `PROGRESS.md` ID, same convention as `patches/<id>-<slug>.tex`.
* `data/` is gitignored repo-wide (`experiments/*/data/` in `.gitignore`) — never commit raw rosbags/video/logs. If a run isn't reproducible from `scripts/` + `config.yaml` alone (e.g. it needed a live hardware run), the experiment's `README.md` must say exactly what manual step produced `data/` instead of a script.
* `output/` **is** committed. It stays small by construction (summary CSVs, the final PNG/PDF figure files) and is the only place `scripts/promote_figure.sh` is allowed to copy from.

#### 9.2 External dependencies — second exemption from stdlib-only

Scripts under `experiments/*/scripts/` are exempt from the repo-wide "bash/Python-stdlib only" rule (§5) — they may use numpy/matplotlib/pandas/ROS 2/whatever the analysis genuinely needs. This is the second explicit exception alongside `compile_pdf.sh`; every script directly under `scripts/` (other than `compile_pdf.sh`) stays stdlib-only.

#### 9.3 Workflow

1. When a `PROGRESS.md` row needs new data, set its `Data source` column to `experiments/<ID>-<slug>/` (§6) and create that directory (copy `experiments/_TEMPLATE/`).
2. Fill in the experiment's `README.md` **before** running anything: goal, method, parameters/seed, and data provenance. If the run depends on `PETER_SIMULATION`, pin the exact commit used (`git -C ../PETER_SIMULATION rev-parse HEAD`) — that sibling repo is read-only reference material but is not version-locked to `paper-revision`, so an unpinned reference silently rots as teammates keep committing there.
3. Run the generation scripts; final artifacts land in `output/`.
4. `scripts/promote_figure.sh experiments/<ID>-<slug>/output/<file> <assets/relative/path>` copies it into `assets/` at the exact relative path the LaTeX will reference. It refuses to overwrite an existing `assets/` file unless `--force` is passed, and refuses any source path outside `experiments/*/output/` — every promoted asset stays traceable to the experiment that produced it.
5. From here it's a normal patch (§5–§7): edit `sections/<slug>.tex` to `\includegraphics`/cite the new asset and write the surrounding prose, record it in `patches/<id>-<slug>.tex`, update `PROGRESS.md` status to `drafted`/`applied`. `scripts/push_to_overleaf.sh` mirrors the promoted asset back to Overleaf like any other file in `assets/` — no changes needed there.
6. The promoted asset is now inside `assets/`, so the existing pull guard (§5.1) already protects it: `pull_from_overleaf.sh` will refuse to run if this work is committed but not yet synced, exactly like any other local change.

#### 9.4 Why this doesn't touch the pull/push guards

Both guards (§5.1, §5.8) key off git history touching `source/`, `sections/`, or `assets/` — not off *why* those files changed. A promoted figure is just another commit touching `assets/`, so it's covered automatically. `experiments/` itself is deliberately outside both guards' scope: work-in-progress scripts/data in `experiments/<ID>-<slug>/scripts/` and `output/` can be committed freely without tripping the pull guard, since nothing there is mirrored to Overleaf until `promote_figure.sh` moves it into `assets/`.

---

### 10. Minor Auxiliary Scripts — Advisory Checks & Convenience

Four smaller gaps, all low-risk given a single primary writer, addressed with lightweight scripts rather than heavier machinery. None of these change the core pull/push guard semantics in §5.

#### 10.1 `scripts/check_hardcoded_refs.sh` — hardcoded "Section N" cross-references

Prose like *"Section 2 details the methodology"* (not a real `\ref{}`) goes stale silently if the top-level `\section{}` structure changes — e.g. R2-03 promoting Limitations to its own section would shift every number after it. Auto-fixing this is unsafe (a script can't tell whether "Section 2" still means the same thing after a restructure), so this is **detection only**: greps `sections/*.tex` for `Section(s) <number>` patterns and prints file:line matches. Always exits 0 — never blocks anything.

Wired into `scripts/push_to_overleaf.sh` as an unconditional advisory step (prints after the validate/compile step, before mirroring) so it surfaces on every push without gating it. Known instances as of 2026-08-25: `introduction.tex` ("Section 2/3/4" in the closing paragraph) and `methodology.tex` ("Section~3" in the basal-ganglia justification paragraph) — see `OUTLINE.md`.

#### 10.2 Pre-commit hook — `scripts/hooks/pre-commit` + `scripts/install_hooks.sh`

Git hooks aren't version-controlled (`.git/hooks/` isn't tracked), so the real hook lives as a template at `scripts/hooks/pre-commit` and `scripts/install_hooks.sh` copies it into place — **run once per clone**, and again any time `scripts/hooks/pre-commit` changes.

The hook only acts when the staged diff touches `sections/` or `source/` (a README/PROGRESS.md-only commit stays fast). When it does act, it:
1. Runs `scripts/reassemble.py` and re-stages `source/main_monolithic.tex` — **necessary**, not optional: `validate_tex.sh`/`check_roundtrip.sh` check the monolith, not `sections/` directly, so without this step a broken `sections/` edit would validate a stale, still-passing monolith and slip through.
2. Runs `scripts/validate_tex.sh`; aborts the commit on failure.
3. Runs `scripts/check_roundtrip.sh`; aborts the commit on failure.

Bypass deliberately with `git commit --no-verify` (e.g. a deliberate WIP commit). Verified against both failure and success paths: a `sections/` edit that breaks brace-matching is blocked before it's committed; a valid `sections/` edit commits successfully with `source/main_monolithic.tex` auto-regenerated in the same commit.

#### 10.3 `scripts/next_id.sh` — automatic `N-xx`/`C-xx` allocation

`scripts/next_id.sh N` / `scripts/next_id.sh C` scans every ID that has ever appeared in `PROGRESS.md` for that namespace and prints the next one (max seen + 1, so a removed row's ID is never reused). `R2-xx`/`R3-xx` are the fixed reviewer list from §6 and are **not** allocated by this script — only used when adding an `intake/`-originated row (§8.2 step 5).

#### 10.4 `scripts/check_target_conflicts.sh` — same-section advisory

`scripts/check_target_conflicts.sh <slug>` greps `PROGRESS.md` for rows mentioning `<slug>.tex` that aren't yet `synced-to-overleaf`, and prints them. Run before starting work on a section to see whether another in-flight item already claims the same file. This is deliberately coarse (it matches anywhere in the row, including the `Requirement` prose column, not just `Target section(s)` — so it can over-report) rather than a real lock: with one primary writer, the practical fix for an actual overlap is just to finish and commit one item before starting the other, not build file-level locking into a git-based pipeline.

---

### 11. Revision-Round Color Convention — `\revblue{...}`

`\revblue{...}` is defined once in `sections/preamble.tex` (`\newcommand{\revblue}[1]{\textcolor{blue}{#1}}`) and marks text added or materially changed **in the current revision round**, rendering it blue in the compiled PDF so editors/reviewers can see what's new without a manual diff against the previous submission.

**The rule, every round, every patch:** any new or materially changed sentence/paragraph/value written into `sections/*.tex` — reviewer-requirement content, `intake/` write-ups, corrections — gets wrapped in `\revblue{...}`. A pure typo fix with zero meaning change can skip it; default to wrapping otherwise, since under-marking hides real changes from reviewers, which is the worse failure mode.

**At the start of a new round** (not mid-round), the *previous* round's `\revblue{}` becomes accepted baseline text and must be stripped back to plain, so the new round's own colored text isn't confused with old already-negotiated material:

1. `python3 scripts/strip_revblue.py` — dry run, reports what would change per file.
2. `python3 scripts/strip_revblue.py --apply` — writes the stripped files. Balanced-brace matching (same escape handling as `validate_tex.sh`: a backslash escapes the next character) unwraps `\revblue{X}` → `X`, keeping the inner text; loops until no `\revblue{` remains, so nested wrappers are handled too. The `\newcommand{\revblue}...` definition itself is never touched — its text contains `\revblue}`, not the literal `\revblue{` the script searches for.
3. `scripts/reassemble.py` → `scripts/validate_tex.sh` → `scripts/check_roundtrip.sh` to confirm the new baseline is still valid LaTeX and splits/reassembles cleanly.
4. Record it as a `C-xx` row in `PROGRESS.md` (get the ID from `scripts/next_id.sh C`) with a `.md` patch summary (not a content copy — see §7) listing wrapper counts per file, per the precedent in `patches/c-02-strip-revblue.md`.

This repo's round stripped 265 wrappers on 2026-08-25 (`C-02`) — see `OUTLINE.md`'s "Revision convention" section for the live state and per-section pointers to what used to be `\revblue{}`.

---

### 12. `docs/` — GitHub Pages Traceability Dashboard

A read-only, publicly viewable dashboard (`docs/index.html`) showing every `PROGRESS.md` row — category, owner, reviewer, status — with client-side filtering and summary metrics. Published via GitHub Pages (repo Settings → Pages → source: `main` branch, `/docs` folder — see [GitHub's publishing-source guide](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)).

This is scoped **outside** the reviewer-checklist pipeline (§1–§11) — it doesn't touch manuscript content, Overleaf, or the pull/push guards. It exists purely for the team to see who owns what and how far along it is, at a glance, without opening `PROGRESS.md` in an editor.

#### 12.1 Layout

```
docs/
├── index.html      # page structure — fetches data.json, no inline data
├── styles.css       # theme tokens (light/dark), stat tiles, filter pills, task cards
├── app.js           # fetch + render + client-side filter/search logic, no dependencies
└── data.json        # generated — never hand-edited (scripts/build_dashboard.py)
```

`data.json` is **generated**, not hand-maintained — same discipline as `source/main_monolithic.tex`: never edit it directly, it will be overwritten the next time `PROGRESS.md` changes.

#### 12.2 Data model

`PROGRESS.md`'s table (§6) carries two columns purpose-built for this dashboard:

- **`Category`** — one of `Escritura` (prose/text editing), `Pruebas` (experiments/ablations/comparisons to run), `Métricas` (new measurements/quantitative analysis).
- **`Owner`** — the person(s) actually doing the work, comma-separated if shared (e.g. `Diego, Sam`).

`scripts/build_dashboard.py` parses the whole table (stdlib-only `re`/`json`, no markdown library) into `docs/data.json`: one object per row (`id`, `reviewer`, `requirement`, `target`, `dataSource`, `category`, `owner` as an array, `status`, `patchFile`), plus a `generatedAt` timestamp and `PROGRESS.md`'s last commit time (via `git log`). `**bold**`/`` `code` ``/`*italic*` markdown is stripped for plain-text display — the dashboard shows prose, not rendered markdown.

#### 12.3 Keeping it in sync

`scripts/build_dashboard.py` runs automatically from the pre-commit hook (§10.2) whenever `PROGRESS.md` is part of the commit — `docs/data.json` is regenerated and staged into the same commit, so the published dashboard can never drift from what's actually in `PROGRESS.md`. Run it manually (`python3 scripts/build_dashboard.py`) after editing `PROGRESS.md` if the hook isn't installed or was bypassed with `--no-verify`.

#### 12.4 Design conventions

No emojis anywhere in the UI. Category and status each get a small fixed color set (not reused between the two dimensions, so a color always means one thing); owners render as plain text chips, not colored, since a second color-coded dimension would compete with category for attention. Every status badge pairs its color with a text label — never color alone. Light/dark mode both follow the visitor's OS/browser preference (`prefers-color-scheme`), no manual toggle. The whole page is dependency-free vanilla HTML/CSS/JS — no build step, no framework, so it stays as low-maintenance as the rest of this repo's tooling.

---

## Repository Setup & Execution Guide

### Current state

Both repositories exist and are linked:

* Overleaf mirror cloned at a sibling path (e.g. `~/Documents/Paper/<overleaf-project-id>/`), git token cached via `git config --global credential.helper store`. **Sync-only** — never edited by hand.
* This repo (`paper-revision`) initialized, linked to `origin` on GitHub, with `README.md`, `CLAUDE.md`, `.gitignore`, and empty `source/`, `sections/`, `assets/`, `patches/`, `intake/pending/`, `intake/processed/`, `scripts/`, `build/` (gitignored) directories, baseline committed and pushed.
* A sibling repo `../PETER_SIMULATION` also exists (firmware/ROS 2 simulation) — read-only reference material for `intake/` documents, registered in `intake/SOURCES.md`.

Remaining setup (implementation phase, not yet done):

1. Create `scripts/config.sh` with the variables in §5.8.
2. Implement `scripts/pull_from_overleaf.sh`, `scripts/split_sections.py`, `scripts/reassemble.py`, `scripts/find_section.py`, `scripts/validate_tex.sh`, `scripts/compile_pdf.sh`, `scripts/check_roundtrip.sh`, `scripts/push_to_overleaf.sh`, `scripts/promote_figure.sh` per §5/§9. The text-processing scripts (everything except `compile_pdf.sh` and anything under `experiments/*/scripts/`) are bash/Python-stdlib only — deliberately simple regex/line-based logic, no LaTeX parser.
3. Create `PROGRESS.md` at the repo root using the table in §6, and a first-pass `OUTLINE.md` (§4.3) once the real manuscript structure is known.
4. Run `scripts/pull_from_overleaf.sh` once to produce the first real `source/main_monolithic.tex`, `sections/*.tex`, and populated `assets/` from the actual manuscript project.
5. Run `scripts/check_roundtrip.sh` once right after step 4 to confirm the split boundaries are byte-exact for the real manuscript before relying on the pipeline.
6. Populate `intake/SOURCES.md` (§8.3) with any sibling repos currently relevant (e.g. `PETER_SIMULATION`).
7. Create `experiments/README.md` and `experiments/_TEMPLATE/` per §9 for any `PROGRESS.md` row that needs new data.
8. Run `scripts/install_hooks.sh` once per clone to install the pre-commit hook (§10.2). Re-run it any time `scripts/hooks/pre-commit` changes, since `.git/hooks/` itself isn't version-controlled.

### Daily revision loop (once scripts exist)

1. `scripts/pull_from_overleaf.sh` — sync from Overleaf (blocked if any unpushed local commit touches `source/`, `sections/`, or `assets/`), regenerate `sections/`.
2. `scripts/find_section.py` — see which sections changed since last sync.
3. Pick a `pending` row in `PROGRESS.md`, identify its target `sections/<slug>.tex` file(s) (and/or `assets/` files). Optionally run `scripts/check_target_conflicts.sh <slug>` (§10.4) if another in-flight row might target the same file. If the row is an `intake/`-originated `N-xx`/`C-xx` item without an ID yet, get one from `scripts/next_id.sh` (§10.3).
4. Read `OUTLINE.md` + the target file(s) only (§4) — not the full monolith, unless the requirement genuinely spans sections. If the row's `Data source` points at `experiments/<id>-<slug>/`, generate that first (§9) and promote the figure into `assets/` before writing the prose that references it.
5. Edit those files directly; save a copy of the change to `patches/<id>-<slug>.tex`; update `PROGRESS.md` to `applied`; commit as `patch: <ID> <summary>` — the pre-commit hook (§10.2) regenerates `source/main_monolithic.tex` and runs `validate_tex.sh`/`check_roundtrip.sh` automatically.
6. `scripts/reassemble.py` — rebuild `source/main_monolithic.tex` from `sections/` (redundant with step 5's hook if it's installed, but explicit here for the case it isn't).
7. `scripts/validate_tex.sh` (and `scripts/compile_pdf.sh` if the LaTeX toolchain is installed) — must pass before continuing.
8. `scripts/push_to_overleaf.sh` — guarded push back to Overleaf; also prints `scripts/check_hardcoded_refs.sh`'s advisory output (§10.1); updates the synced checkpoint on success; update `PROGRESS.md` to `synced-to-overleaf`.
