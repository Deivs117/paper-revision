# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository status

This repository currently contains only `README.md`, which documents the intended setup for a paper-revision
workflow. None of the directory structure or scripts it describes (`source/`, `sections/`, `patches/`, `scripts/`,
`.gitignore`, git remote, etc.) have been created yet — see "Repository Setup & Execution Guide" in the README for
the exact commands to bootstrap them.

## Purpose of this repository

This repo manages the revision of a manuscript ("Manuscript ROBOT-D-26-00122R1", journal *Robotics and Autonomous
Systems*) that is undergoing major revision. Resubmission deadline: **September 3, 2026**.

The manuscript itself is authored and edited collaboratively by non-technical co-authors in Overleaf as a single
monolithic `.tex` file. This repo exists to layer git-based change tracking and AI-assisted section patching on top
of that Overleaf workflow, without requiring co-authors to use git.

## Architecture: the hybrid automation pipeline

```
[Overleaf Monolithic File] --(Manual Export)--> [Local Repository Source]
                                                         |
                                               (Git Diff Tracking)
                                                         |
                                                         v
                                             [Upward-Scanning Script]
                                                         |
                                                         v
                                            [AI Agent Section Patching]
                                                         |
                                                         v
                                             [Monolithic Reassembly]
                                                         |
                                                         v
                                            [Paste Back to Overleaf]
```

- **Version isolation:** The monolithic `.tex` file is periodically exported from Overleaf and placed at
  `source/main_monolithic.tex`. This local file is the git-tracked snapshot of the manuscript.
- **Upward-scanning logic:** Because Overleaf edits cause arbitrary line shifts (reordering, insertions, block
  deletions), locating which `\section{...}` a changed line belongs to isn't a fixed-line-number problem. Scripts
  under `scripts/` are meant to scan `git diff` output and walk upward from each changed line to find its parent
  section header, rather than relying on stable line numbers.
- **AI ambiguity resolution:** Because the diffs aren't clean adds/deletes (sections get moved, not just edited), the
  AI agent's job when patching is to distinguish a *moved* section from an *added/deleted* one before generating a
  LaTeX patch block — don't naively diff line ranges when helping with this.
- **No syntax-level LaTeX parser:** the design intentionally avoids a rigid LaTeX parser in favor of structural-delta
  reasoning by the agent. Keep that approach when extending the scripts.

## Daily revision workflow

1. Overwrite `source/main_monolithic.tex` with the latest export from Overleaf.
2. `git diff source/main_monolithic.tex` to see what co-authors changed.
3. Commit that snapshot on its own (`sync: updated monolithic file from Overleaf edits`) before making any AI-assisted
   edits — keeps sync commits separate from patch commits.
4. Isolate the target section (e.g. `03_related_work.tex`, `05_experiments.tex`), and apply the relevant reviewer
   requirement (below) as a patch directly in `source/main_monolithic.tex`. Paste the result back into Overleaf.

`.gitignore` should exclude LaTeX build artifacts: `*.aux *.log *.out *.toc *.bbl *.blg *.pdf *.synctex.gz`.

## Reviewer requirements driving the current revision

**Reviewer 2 (streamlining / minor additions):**
- Condense repetitive text; remove duplicate neural raster plots and identical stability curves between simulation
  and hardware tests; merge metric definitions; shorten the symbolic warehouse simulation section.
- Add FSM (Finite State Machine) gait arbitration baseline comparisons.
- Consolidate all limitations into one dedicated section.
- Add multi-mode long-term average energy consumption data and onboard MLP computing overhead analysis.

**Reviewer 3 (major structural/experimental additions — high priority):**
- Explicit ablation analysis on the basal ganglia arbitration network.
- Comparative tests removing key neural layers or inhibitory connections to justify Winner-Take-All (WTA) over
  threshold logic.
- Supplement control strategies/compensation algorithms for low-torque servo constraints and open-loop gait
  instability.
- Perception-decision noise robustness experiments (IMU drift, LiDAR noise, camera illumination distortion).
- Add inspection task performance metrics (target tracking accuracy, coverage rate, autonomous re-planning).
- Revise the literature review with horizontal comparative tables contrasting Basal Ganglia, CPG, and RL-based action
  selection algorithms.

When patching a section, tie the change explicitly to the reviewer item it addresses.
