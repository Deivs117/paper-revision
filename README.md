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

---

### 3. Repository Topology & Folder Structure

| Repo | Local path (example) | Remote | Role |
|---|---|---|---|
| Overleaf mirror | `../<overleaf-project-id>/` (sibling directory to this repo) | `https://git.overleaf.com/<overleaf-project-id>` | Sync-only pass-through. |
| `paper-revision` (this repo) | `.` | GitHub, `origin` | Editing, patching, compiling. |

```
paper-revision/
├── source/
│   └── main_monolithic.tex      # generated — never hand-edited (§4)
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
├── scripts/
│   ├── config.sh
│   ├── pull_from_overleaf.sh
│   ├── push_to_overleaf.sh
│   ├── split_sections.py
│   ├── reassemble.py
│   ├── find_section.py
│   ├── validate_tex.sh
│   └── compile_pdf.sh
├── PROGRESS.md
├── README.md
└── CLAUDE.md
```

**Filename mapping.** The Overleaf main file (`elsarticle-template-num-names.tex`) and this repo's mirror (`source/main_monolithic.tex`) refer to the same content but are never the same file on disk — renaming happens only inside `pull_from_overleaf.sh` / `push_to_overleaf.sh`. Everything else in the Overleaf project (bibliography, figures, class/style files) mirrors into `assets/` **under its original relative path and filename** — no renaming for those.

Overleaf git authentication uses a per-project git token (`olp_...`) as the password with username `git`, cached via `git config --global credential.helper store`. Never write this token into any file in either repository — it lives only in the local git credential store.

---

### 4. Automation Pipeline

```
[Overleaf web UI]                                        [paper-revision repo: all real work]
   co-author edits                                          text patching · asset updates · compile
        │                                                          │
        ▼                                                          │
  Overleaf auto-commit                                             │
  (git.overleaf.com)                                               │
        │                                                          │
        ▼   scripts/pull_from_overleaf.sh                          │
        │   guard: abort if PROGRESS.md has any                    │
        │   row with Status = applied (unsynced                    │
        │   local work would otherwise be lost)                    │
        ▼                                                          │
  git pull (cached token)                                          │
     │        │                                                    │
     │        └─copy+rename main tex──▶ source/main_monolithic.tex │
     └─mirror everything else─────────▶ assets/                    │
                                                     │               │
                                          commit "sync: ..."         │
                                                     │               │
                                                     ▼               │
                                        scripts/split_sections.py    │
                                        source/main_monolithic.tex   │
                                           ──▶ sections/*.tex        │
                                           ──▶ sections/manifest.json│
                                                     │               │
                                                     ▼               │
                                          scripts/find_section.py    │
                                        (upward-scan on the sync diff:
                                         which sections/*.tex changed)
                                                     │
                                                     ▼
                                     agent edits sections/*.tex and/or assets/
                                     (new figures, updated .bib) directly, using
                                     PROGRESS.md to pick which requirement to address
                                                     │
                                          commit "patch: <ID> <summary>"
                                       (+ patches/<ID>-<slug>.tex audit copy,
                                          PROGRESS.md status → applied)
                                                     │
                                                     ▼
                                          scripts/reassemble.py
                                        sections/*.tex (manifest order)
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
  mirror assets/ + copy/rename main tex, commit, git push
        │
        ▼
  Overleaf reflects the change live
  (PROGRESS.md status → synced-to-overleaf)
```

**Golden rules:**
- `source/main_monolithic.tex` is always generated (by `pull_from_overleaf.sh` or `reassemble.py`) — never hand-edited.
- `sections/*.tex` is the editable working copy of the manuscript text. `assets/` is the editable working copy of everything else (bibliography, figures, class files) — both are mirrored to/from Overleaf, but edited locally in between syncs.
- The Overleaf repo clone is **sync-only** — no drafting, patching, or compiling happens there.

---

### 5. Script Specifications

All scripts live in `scripts/` and read shared paths from `scripts/config.sh` (bash):

```bash
OVERLEAF_DIR="../<overleaf-project-id>"        # path to the Overleaf repo clone
OVERLEAF_MAIN_FILE="elsarticle-template-num-names.tex"
MIRROR_FILE="source/main_monolithic.tex"
ASSETS_DIR="assets"
BUILD_DIR="build"
```

Nothing else in the codebase should hardcode these paths/names — always source `config.sh`.

#### 5.1 `scripts/pull_from_overleaf.sh`
1. **Guard against data loss:** grep `PROGRESS.md` for any row with `Status` = `applied`. If one or more exist, abort with an error listing their IDs and telling the user to run `push_to_overleaf.sh` first. (`drafted` rows do not block — nothing in `sections/`/`assets/` depends on them yet.)
2. `git -C "$OVERLEAF_DIR" pull origin main`. On failure (auth, conflict), print the error and exit 1.
3. Copy `$OVERLEAF_DIR/$OVERLEAF_MAIN_FILE` → `$MIRROR_FILE` (overwrite).
4. Mirror everything else: `rsync -a --delete --exclude='.git' --exclude="$OVERLEAF_MAIN_FILE" "$OVERLEAF_DIR"/ "$ASSETS_DIR"/` (the `--delete` keeps `assets/` an exact mirror, removing files deleted on Overleaf's side too).
5. If `git diff --quiet -- "$MIRROR_FILE" "$ASSETS_DIR"` shows no changes, print `"No changes since last sync."` and exit 0 without committing.
6. Otherwise: `git add "$MIRROR_FILE" "$ASSETS_DIR"`, commit with message `sync: pull from Overleaf (<YYYY-MM-DD HH:MM>)`.
7. Invoke `scripts/split_sections.py` as the final step so `sections/` is always in sync with `source/main_monolithic.tex` after a pull.

Exit codes: `0` = success, `1` = error or guard-abort.

#### 5.2 `scripts/split_sections.py`
Splits `source/main_monolithic.tex` into `sections/`. Pure text/regex split — no LaTeX parser, no `\input`/`\include` resolution.

* Split points are lines matching `^\s*\\section\{`. Only **top-level** `\section{}` commands are split boundaries; `\subsection{}` etc. stay embedded inside their parent section's file.
* Start of file up to (not including) the first `\section{}` → `sections/preamble.tex`.
* Each `\section{Title}` block → `sections/<slug>.tex`, where `<slug>` is the title lowercased, non-alphanumeric characters replaced with `-`, collapsed/trimmed (e.g. `\section{Related Work}` → `sections/related-work.tex`). **No numeric prefix** — ordering lives only in `manifest.json`, so a section that gets reordered in Overleaf keeps the same filename and its git history stays intact.
* If two sections produce the same slug (duplicate titles, e.g. two "Results" sections), disambiguate deterministically by appending `-2`, `-3`, ... in order of appearance.
* `\end{document}` (inclusive) plus anything trailing after the last section (bibliography commands, appendices not under a `\section`) → `sections/closing.tex`.
* Before writing, delete all existing `sections/*.tex` files (full regeneration every run).
* Write `sections/manifest.json`: an ordered array of `{"file": "related-work.tex", "title": "Related Work"}` objects (`preamble.tex` and `closing.tex` included, `"title": null` for those two). This array's order is authoritative for reassembly — filenames alone never imply order.

When an agent adds a **brand-new** section locally (not yet present in Overleaf's file — e.g. R2-03's "consolidate limitations into a dedicated section"), it creates `sections/<slug>.tex` directly and inserts an entry for it at the right position in `manifest.json` by hand. The next `split_sections.py` run (after that content has been pushed to Overleaf and pulled back) will regenerate the manifest from the real file and keep it consistent.

#### 5.3 `scripts/reassemble.py`
Reads `sections/manifest.json` in order, concatenates each listed file's contents (with a single blank line between files), writes the result to `source/main_monolithic.tex`. Exact inverse of `split_sections.py`'s join.

#### 5.4 `scripts/find_section.py`
Upward-scan / diff-to-section mapper. Usage: `find_section.py [<git-rev-range>]`, default range `HEAD~1..HEAD`.

1. Run `git diff <range> -- source/main_monolithic.tex` and parse unified-diff hunk headers (`@@ -a,b +c,d @@`).
2. For each hunk, take the starting line number in the new file and scan upward through `source/main_monolithic.tex` until finding the nearest preceding `^\s*\\section\{...\}` line, or the top of file (→ preamble).
3. Print one line per hunk: `<section-title> (sections/<slug>.tex): lines <start>-<end> changed`, using `sections/manifest.json` to resolve title → filename.

Read-only: never modifies files.

#### 5.5 `scripts/validate_tex.sh`
Fast structural sanity check on `source/main_monolithic.tex`, no LaTeX toolchain required:
* Braces `{`/`}` balanced (equal count).
* `\begin{document}` and `\end{document}` both present, exactly once each.
* Every `\begin{X}` has a matching `\end{X}` (stack-based check by environment name).

Exit 1 with a description of the first failure found; exit 0 if all checks pass. Run before every `push_to_overleaf.sh`.

#### 5.6 `scripts/compile_pdf.sh`
Real compilation check, requires a local LaTeX toolchain (`latexmk` preferred, fallback `pdflatex` + `bibtex`/`biber` run twice). Not part of the "no dependencies" scripts — this one legitimately needs LaTeX installed.

1. `rm -rf "$BUILD_DIR/tex-src"`, recreate it.
2. Copy `$ASSETS_DIR/` into `$BUILD_DIR/tex-src/` (preserving relative paths).
3. Copy `source/main_monolithic.tex` into `$BUILD_DIR/tex-src/$OVERLEAF_MAIN_FILE` (using the original Overleaf filename, so the assembled build directory matches what Overleaf itself would compile).
4. `cd "$BUILD_DIR/tex-src" && latexmk -pdf -interaction=nonstopmode "$OVERLEAF_MAIN_FILE"` (or the `pdflatex`/`bibtex` fallback sequence if `latexmk` isn't installed).
5. On success, copy the resulting PDF to `$BUILD_DIR/paper.pdf`. On failure, print the LaTeX log tail and exit 1.

`build/` is gitignored entirely — it's a disposable compilation workspace, never committed.

#### 5.7 `scripts/push_to_overleaf.sh`
1. **Guard:** `git -C "$OVERLEAF_DIR" pull origin main`. If this brings in new commits, **abort** — tells the user to re-run `pull_from_overleaf.sh` and re-check for conflicts before pushing. Never force-push, never auto-merge.
2. Run `scripts/validate_tex.sh`; abort on failure. Run `scripts/compile_pdf.sh` if a LaTeX toolchain is available; abort on failure (warn-and-continue only if the toolchain itself is missing, not if compilation fails).
3. Mirror back: `rsync -a --delete --exclude='.git' "$ASSETS_DIR"/ "$OVERLEAF_DIR"/`, then copy `$MIRROR_FILE` → `$OVERLEAF_DIR/$OVERLEAF_MAIN_FILE`.
4. `git -C "$OVERLEAF_DIR" add -A`, commit `sync: apply patches from paper-revision (<YYYY-MM-DD HH:MM>)`, `git push origin main`.

---

### 6. `PROGRESS.md` — Reviewer Checklist Tracking

A markdown table at the repo root, one row per reviewer requirement, IDs fixed as below (do not renumber — these IDs are referenced by patch filenames, commit messages, and the pull guard in §5.1):

| ID | Reviewer | Requirement (short) | Target section(s) | Status | Patch file |
|---|---|---|---|---|---|
| R2-01 | 2 | Condense repetitive text / remove duplicate plots / merge metric definitions / shorten warehouse sim section | TBD | pending | — |
| R2-02 | 2 | Add FSM gait arbitration baseline comparison | TBD | pending | — |
| R2-03 | 2 | Consolidate limitations into one dedicated section | TBD | pending | — |
| R2-04 | 2 | Add multi-mode energy consumption + onboard MLP compute overhead analysis | TBD | pending | — |
| R3-01 | 3 | Ablation analysis on basal ganglia arbitration network | TBD | pending | — |
| R3-02 | 3 | Comparative tests removing neural layers/inhibitory connections to justify WTA over threshold logic | TBD | pending | — |
| R3-03 | 3 | Control/compensation strategies for low-torque servo constraints and open-loop gait instability | TBD | pending | — |
| R3-04 | 3 | Perception-decision noise robustness experiments (IMU drift, LiDAR noise, camera illumination distortion) | TBD | pending | — |
| R3-05 | 3 | Inspection task performance metrics (tracking accuracy, coverage rate, autonomous re-planning) | TBD | pending | — |
| R3-06 | 3 | Literature review comparative tables: Basal Ganglia vs CPG vs RL-based action selection | TBD | pending | — |

Status values (exactly these strings, lowercase): `pending` → `drafted` → `applied` → `synced-to-overleaf`. `applied` means committed locally but **not yet pushed to Overleaf** — `pull_from_overleaf.sh` refuses to run while any row is in this state (§5.1). Update `Target section(s)` with the actual `sections/<slug>.tex` file(s) once identified.

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

Commit convention: stage the modified `sections/<slug>.tex` (and/or `assets/` files), the new `patches/<id>-<slug>.tex`, and the `PROGRESS.md` status update, in one commit: `patch: <ID> <short summary>` (e.g. `patch: R3-02 add WTA ablation comparison`).

---

## Repository Setup & Execution Guide

### Current state

Both repositories exist and are linked:

* Overleaf mirror cloned at a sibling path (e.g. `~/Documents/Paper/<overleaf-project-id>/`), git token cached via `git config --global credential.helper store`. **Sync-only** — never edited by hand.
* This repo (`paper-revision`) initialized, linked to `origin` on GitHub, with `README.md`, `CLAUDE.md`, `.gitignore`, and empty `source/`, `sections/`, `assets/`, `patches/`, `scripts/`, `build/` (gitignored) directories, baseline committed and pushed.

Remaining setup (implementation phase, not yet done):

1. Create `scripts/config.sh` with the variables in §5.
2. Implement `scripts/pull_from_overleaf.sh`, `scripts/split_sections.py`, `scripts/reassemble.py`, `scripts/find_section.py`, `scripts/validate_tex.sh`, `scripts/compile_pdf.sh`, `scripts/push_to_overleaf.sh` per §5. The text-processing scripts (`split_sections.py`, `reassemble.py`, `find_section.py`, `validate_tex.sh`) are bash/Python-stdlib only — deliberately simple regex/line-based logic, no LaTeX parser. `compile_pdf.sh` is the one script allowed to depend on external tooling (a LaTeX distribution).
3. Create `PROGRESS.md` at the repo root using the table in §6.
4. Run `scripts/pull_from_overleaf.sh` once to produce the first real `source/main_monolithic.tex`, `sections/*.tex`, and populated `assets/` from the actual manuscript project.

### Daily revision loop (once scripts exist)

1. `scripts/pull_from_overleaf.sh` — sync from Overleaf (blocked if unsynced local patches exist), regenerate `sections/`.
2. `scripts/find_section.py` — see which sections changed since last sync.
3. Pick a `pending` row in `PROGRESS.md`, identify its target `sections/<slug>.tex` file(s) (and/or `assets/` files, e.g. new figures).
4. Edit those files directly to satisfy the reviewer requirement; save a copy of the change to `patches/<id>-<slug>.tex`; update `PROGRESS.md` to `applied`; commit as `patch: <ID> <summary>`.
5. `scripts/reassemble.py` — rebuild `source/main_monolithic.tex` from `sections/`.
6. `scripts/validate_tex.sh` (and `scripts/compile_pdf.sh` if the LaTeX toolchain is installed) — must pass before continuing.
7. `scripts/push_to_overleaf.sh` — guarded push back to Overleaf; update `PROGRESS.md` to `synced-to-overleaf` on success.
