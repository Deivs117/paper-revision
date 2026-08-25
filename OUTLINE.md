# Outline — ROBOT-D-26-00122R1

## Abstract (1 line)
A shape-shifting quadruped robot (quadrupedal / differential-drive / omnidirectional modes) uses a
basal-ganglia-inspired neural arbitration circuit to select gaits/behaviors for infrastructure
inspection tasks, validated in Gazebo simulation and on physical hardware.

## Sections
- introduction.tex — motivation (infrastructure inspection, hazards of manual inspection), literature
  gap, contribution. **R3-06 target**: needs a comparative table (Basal Ganglia vs CPG vs RL-based
  action selection) added to the literature review here.
- methodology.tex — four components: (1) robot morphology (quadruped/diff-drive/omni transformation),
  (2) Gazebo simulation setup, (3) neuronal control circuits (basal ganglia arbitration), (4)
  [remainder not yet read in full]. Likely target for **R3-01/R3-02** (ablation methodology) and
  **R2-02** (FSM baseline description) — needs verification.
- results.tex — largest section (~980 lines): simulation results in a Gazebo warehouse scenario,
  gait-switching tests on a three-topology terrain map, presumably also the hardware/real-robot
  results. Likely target for most Reviewer 2/3 experimental additions (**R2-01, R2-04, R3-01 through
  R3-05**) — needs a closer read before assuming exact placement, this section is large and may need
  internal reorganization (e.g. R2-01 asks to remove duplication between sim/hardware plots here).
- conclusions.tex — summary of findings (stable/adaptive navigation across stimulus configurations and
  terrain variations). Candidate location for **R2-03**'s consolidated limitations section (new
  subsection, or promote to its own top-level section before conclusions).

## Key terms / notation
- WTA = Winner-Take-All (arbitration mechanism used instead of threshold logic — subject of R3-02)
- FSM = Finite State Machine (the baseline R2-02 asks to compare against)
- CPG = Central Pattern Generator (a literature comparison point for R3-06)
- Basal ganglia arbitration network = the core neural decision-making circuit being ablated in R3-01

## Known cross-references
- Not yet mapped in detail — this file is a first pass from a quick skim of each section's opening
  paragraph, done right after the first `pull_from_overleaf.sh`. Update it as sections are actually
  read/edited; do not treat the placements above as final.
