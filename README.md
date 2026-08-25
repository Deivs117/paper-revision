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
* **Two independent git repositories are involved.** See §3 for how they relate. Do not confuse them:
  * The **Overleaf repo** (clone of `git.overleaf.com/<project-id>`) — the human collaboration surface.
  * **This repo, `paper-revision`** (GitHub) — the engineering surface: diffing, section splitting, AI patching, revision tracking.

---

### 3. Repository Topology & File Mapping

| Repo | Local path (example) | Remote | Canonical file |
|---|---|---|---|
| Overleaf mirror | `../<overleaf-project-id>/` (sibling directory to this repo) | `https://git.overleaf.com/<overleaf-project-id>` | `elsarticle-template-num-names.tex` |
| `paper-revision` (this repo) | `.` | GitHub, `origin` | `source/main_monolithic.tex` |

**These two filenames refer to the same manuscript content but are never the same file on disk.** The Overleaf file keeps its Overleaf name; this repo's mirror is always called `source/main_monolithic.tex`. All renaming happens inside `scripts/pull_from_overleaf.sh` and `scripts/push_to_overleaf.sh` — no other script or process should assume these filenames are interchangeable.

Overleaf git authentication uses a per-project git token (`olp_...`) as the password with username `git`, cached locally via `git config --global credential.helper store`. Never write this token into any file inside either repository (no `.env`, no config file, no code comment). It is not a repository secret — it lives only in the local git credential store.

---

### 4. Automation Pipeline

```
[Overleaf web UI]                                        [paper-revision repo]
   co-author edits                                          AI agent patches
        │                                                          │
        ▼                                                          │
  Overleaf auto-commit                                             │
  (git.overleaf.com)                                               │
        │                                                          │
        ▼   scripts/pull_from_overleaf.sh                          │
  git pull (cached token) ──copy + rename──▶  source/main_monolithic.tex
                                                     │
                                          commit "sync: ..."
                                                     │
                                                     ▼
                                        scripts/split_sections.py
                                        source/main_monolithic.tex
                                           ──▶ sections/*.tex
                                           ──▶ sections/manifest.json
                                                     │
                                                     ▼
                                          scripts/find_section.py
                                        (upward-scan on the sync diff:
                                         which sections/*.tex changed)
                                                     │
                                                     ▼
                                     agent edits the relevant sections/NN_*.tex
                                     file(s) directly, using PROGRESS.md to pick
                                     which reviewer requirement to address
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
        ◀───────────── scripts/push_to_overleaf.sh ─┘
  guard: git pull Overleaf repo first;
  abort if it brings new commits
        │
        ▼ (only if guard passes)
  copy + rename inverse, commit, git push
        │
        ▼
  Overleaf reflects the change live
  (PROGRESS.md status → synced-to-overleaf)
```

**Golden rule:** `source/main_monolithic.tex` and `sections/*.tex` are never both hand-edited independently. `sections/*.tex` is the editable working copy; `source/main_monolithic.tex` is always a generated artifact of either `pull_from_overleaf.sh` (from Overleaf) or `reassemble.py` (from `sections/`). Never edit `source/main_monolithic.tex` directly.

---

### 5. Script Specifications

All scripts live in `scripts/` and read shared paths from `scripts/config.sh` (bash) — a single file defining:

```bash
OVERLEAF_DIR="../<overleaf-project-id>"        # path to the Overleaf repo clone
OVERLEAF_MAIN_FILE="elsarticle-template-num-names.tex"
MIRROR_FILE="source/main_monolithic.tex"
```

Nothing else in the codebase should hardcode these paths/names — always source `config.sh`.

#### 5.1 `scripts/pull_from_overleaf.sh`
1. `git -C "$OVERLEAF_DIR" pull origin main`. On failure (auth, conflict), print the error and exit 1 — do not attempt to resolve conflicts automatically.
2. Copy `$OVERLEAF_DIR/$OVERLEAF_MAIN_FILE` → `$MIRROR_FILE` (overwrite).
3. If `git diff --quiet -- "$MIRROR_FILE"` shows no changes, print `"No changes since last sync."` and exit 0 without committing.
4. Otherwise: `git add "$MIRROR_FILE"`, commit with message `sync: pull from Overleaf (<YYYY-MM-DD HH:MM>)`, using the local timestamp.
5. Invoke `scripts/split_sections.py` (§5.2) as the final step so `sections/` is always in sync with `source/main_monolithic.tex` after a pull.

Exit codes: `0` = success (with or without new changes), `1` = error (git pull failed, file not found).

#### 5.2 `scripts/split_sections.py`
Splits `source/main_monolithic.tex` into `sections/`. Pure text/regex split — no LaTeX parser, no `\input`/`\include` resolution.

* Split points are lines matching `^\s*\\section\{`. Only **top-level** `\section{}` commands are split boundaries; `\subsection{}`, `\subsubsection{}` etc. stay embedded inside their parent section's file.
* Everything from the start of the file up to (not including) the first `\section{}` → `sections/00_preamble.tex` (includes `\documentclass`, packages, `\begin{document}`, title/abstract if placed before the first section).
* Each `\section{Title}` block → `sections/NN_<slug>.tex`, where `NN` is a 2-digit zero-padded sequential index in order of appearance (`01`, `02`, ...), and `<slug>` is the title lowercased, non-alphanumeric characters replaced with `-`, collapsed/trimmed (e.g. `\section{Related Work}` → `sections/02_related-work.tex`).
* Everything from `\end{document}` (inclusive) plus anything trailing after the last section (bibliography commands, appendices not under a `\section`) → `sections/99_closing.tex`.
* Before writing, delete all existing `sections/*.tex` files (full regeneration every run — never leave stale files from a previous split).
* Also write `sections/manifest.json`: an ordered array of `{"file": "01_introduction.tex", "title": "Introduction"}` objects (preamble and closing included, using `"title": null` for those two). This is what `reassemble.py` uses for exact join order, and what `find_section.py` uses to report human-readable section names.

#### 5.3 `scripts/reassemble.py`
Reads `sections/manifest.json` in order, concatenates each listed file's contents (with a single blank line between files), writes the result to `source/main_monolithic.tex`. No other logic — this is the exact inverse of `split_sections.py`'s join, not a general LaTeX assembler.

#### 5.4 `scripts/find_section.py`
Upward-scan / diff-to-section mapper. Usage: `find_section.py [<git-rev-range>]`, default range `HEAD~1..HEAD`.

1. Run `git diff <range> -- source/main_monolithic.tex` (or, if `sections/` already exists, `-- sections/`) and parse unified-diff hunk headers (`@@ -a,b +c,d @@`).
2. For each hunk, take the starting line number in the new file and scan upward (toward line 1) through `source/main_monolithic.tex` until finding the nearest preceding `^\s*\\section\{...\}` line, or the top of file (→ preamble).
3. Print one line per hunk: `<section-title> (sections/NN_slug.tex): lines <start>-<end> changed`, using `sections/manifest.json` to resolve title → filename.

This script is read-only: it never modifies files, only reports which sections were touched since the last sync, so the agent knows where to look.

#### 5.5 `scripts/push_to_overleaf.sh`
1. **Guard:** `git -C "$OVERLEAF_DIR" pull origin main`. If this pull brings in new commits (i.e. `HEAD` changed), **abort** with a clear message telling the user to re-run `pull_from_overleaf.sh` and re-check for conflicts before pushing. Never force-push, never auto-merge.
2. If the guard passes (no new commits from the pull): copy `$MIRROR_FILE` → `$OVERLEAF_DIR/$OVERLEAF_MAIN_FILE` (overwrite).
3. `git -C "$OVERLEAF_DIR" add "$OVERLEAF_MAIN_FILE"`, commit with message `sync: apply patches from paper-revision (<YYYY-MM-DD HH:MM>)`, `git push origin main`.

---

### 6. `PROGRESS.md` — Reviewer Checklist Tracking

A markdown table at the repo root, one row per reviewer requirement, IDs fixed as below (do not renumber — these IDs are referenced by patch filenames and commit messages):

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

Status values (exactly these strings, lowercase): `pending` → `drafted` → `applied` → `synced-to-overleaf`. Update the row's `Status` and `Patch file` columns as work progresses; fill `Target section(s)` with the actual `sections/NN_*.tex` filename(s) once identified via `find_section.py` or manual inspection.

---

### 7. `patches/` — Audit Trail

One file per patch: `patches/<id>-<slug>.tex` (lowercase ID, e.g. `patches/r3-02-wta-ablation.tex`). This is a **record of what changed**, not the live working file (the live copy is the corresponding `sections/NN_*.tex`, edited in place). Header format, as LaTeX comments:

```latex
% PATCH: R3-02
% Reviewer: 3
% Target section: sections/07_ablation-study.tex
% Requirement: Comparative tests removing key neural layers or inhibitory
%   connections to justify the Winner-Take-All (WTA) mechanism over threshold logic.
% Status: applied

<the new/changed LaTeX content, exactly as inserted into the target section file>
```

Commit convention for applying a patch: stage both the modified `sections/NN_*.tex` and the new `patches/<id>-<slug>.tex`, plus the `PROGRESS.md` status update, in one commit: `patch: <ID> <short summary>` (e.g. `patch: R3-02 add WTA ablation comparison`).

---

## Repository Setup & Execution Guide

### Current state

Both repositories already exist and are linked:

* Overleaf mirror cloned at a sibling path (e.g. `~/Documents/Paper/<overleaf-project-id>/`), git token cached via `git config --global credential.helper store`.
* This repo (`paper-revision`) initialized, linked to `origin` on GitHub, with `README.md`, `CLAUDE.md`, `.gitignore`, and empty `source/`, `sections/`, `patches/`, `scripts/` directories, baseline committed and pushed.

Remaining setup (implementation phase, not yet done):

1. Create `scripts/config.sh` with `OVERLEAF_DIR`, `OVERLEAF_MAIN_FILE`, `MIRROR_FILE` (§5).
2. Implement `scripts/pull_from_overleaf.sh`, `scripts/split_sections.py`, `scripts/reassemble.py`, `scripts/find_section.py`, `scripts/push_to_overleaf.sh` per the specs in §5. Each script should be small and dependency-free (bash + Python 3 standard library only — no LaTeX parsing libraries, no external packages) since the logic is deliberately simple regex/line-based text processing, not a LaTeX AST.
3. Create `PROGRESS.md` at the repo root using the table in §6.
4. Run `scripts/pull_from_overleaf.sh` once to produce the first real `source/main_monolithic.tex` and `sections/*.tex` from the actual manuscript content.

`.gitignore` excludes LaTeX build artifacts: `*.aux *.log *.out *.toc *.bbl *.blg *.pdf *.synctex.gz`.

### Daily revision loop (once scripts exist)

1. `scripts/pull_from_overleaf.sh` — sync from Overleaf, regenerate `sections/`.
2. `scripts/find_section.py` — see which sections changed since last sync.
3. Pick a `pending` row in `PROGRESS.md`, identify its target `sections/NN_*.tex` file.
4. Edit that section file directly to satisfy the reviewer requirement; save a copy of the change to `patches/<id>-<slug>.tex`; update `PROGRESS.md` to `applied`; commit as `patch: <ID> <summary>`.
5. `scripts/reassemble.py` — rebuild `source/main_monolithic.tex` from `sections/`.
6. `scripts/push_to_overleaf.sh` — guarded push back to Overleaf; update `PROGRESS.md` to `synced-to-overleaf` on success.
