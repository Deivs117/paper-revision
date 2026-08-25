# Outline — ROBOT-D-26-00122R1

## Abstract (1 line)
A shape-shifting quadruped robot (quadrupedal / differential-drive / omnidirectional modes) uses a
basal-ganglia-inspired neural arbitration circuit to select gaits/behaviors for infrastructure
inspection tasks, validated in Gazebo simulation and on physical hardware.

## Revision convention: `\revblue{...}`
Text wrapped in `\revblue{...}` was added/changed in a **previous** revision round (rendered in blue
in the compiled PDF) — it's not this round's work. A large fraction of `results.tex` is already
`\revblue{}`, meaning a prior revision cycle already responded to earlier reviewer comments. Don't
assume `\revblue{}` content is untouched original text; it's already-negotiated revision material.
When this round adds new text, keep using `\revblue{}` for it (matches existing convention) unless
told otherwise.

## Sections

### introduction.tex
Motivation (infrastructure inspection, hazards of manual inspection), literature gap, contribution.
**R3-06 target**: needs a comparative table (Basal Ganglia vs CPG vs RL-based action selection) added
to the literature review here. Not yet verified by a full read of this file (only skimmed the
opening) — confirm before drafting.

### methodology.tex (501 lines)
Four components: (1) robot morphology/transformation, (2) Gazebo simulation setup, (3) neuronal
control circuits, (4) [not yet fully read]. Confirmed via targeted grep (not a full read):
- `\subsubsection{Basal Ganglia Module}` (~line 154) — **the** target for R3-01/R3-02. Defines the
  STN/GPe/GPi winner-take-all circuit after Sarvestani et al. 2013, with inhibitory loops resolving
  conflicts between competing behaviors. This is where an ablation-study subsection (removing
  layers/inhibitory connections, comparing WTA vs threshold logic) belongs. Equations, weights, and
  thresholds (e.g. `Ar = 28.0` derived from camera pinhole geometry) are already documented here in
  detail — an ablation section should reference this existing formalism, not restate it.
- No mention of FSM (Finite State Machine) anywhere in this file — **R2-02's baseline comparison is
  entirely new content**, not a rewrite of existing material.
- No existing ablation study on the basal ganglia network itself (the only ablation content in the
  whole paper is the MLP terrain-classifier architecture ablation in `results.tex`, unrelated to
  R3-01/R3-02).

### results.tex (980 lines) — fully read this round
Two top-level subsections: **Simulation Results** and **Physical Implementation Results**, followed
by a **Quantitative Performance Analysis (Physical)** subsection and a **Limitations** subsection.

- `\subsection{Simulation Results}` — single-stimulus response, quantitative validation (noise
  robustness across σ∈[0,4] for Appetitive/Aversive/Obstacle/Complex suites — this likely already
  substantially covers **R3-04**'s noise-robustness ask for simulation; verify it maps to IMU
  drift/LiDAR noise/illumination specifically, or is generic sensor noise), multi-stimuli response,
  variable-topography response (stability, ECDF decision-delay, terrain-adaptability phase space),
  and `\subsubsection{Quantitative Stability Analysis of Locomotion Mode Transitions}`
  (`\label{sssec:transition_stability}`) — this subsection's own text says *"To address the
  reviewer's request for systematic quantitative metrics on mode-switching behaviour..."*, i.e. it
  was already written in response to a prior review round. Relevant background for R3-01/R3-02 but
  is NOT a basal-ganglia ablation study — it's transition stability metrics (SM, TR indices), a
  different thing.
- `\subsection{Physical Implementation Results}` — mirrors the simulation structure on hardware
  (single stimulus, multi-stimuli, variable topography), plus
  `\subsubsection{Evaluation of the MLP-based terrain classifier}` which **already contains**: MLP
  architecture ablation (150-80 vs shallower/deeper), a classifier comparison (vs Logistic
  Regression/SVM/Random Forest), AND a per-sample inference latency comparison
  (`fig6_computational_cost.png`) — **this already substantially covers R2-04's "onboard MLP
  computing overhead analysis"** ask. Verify wording/framing satisfies the reviewer before treating
  as new work.
- `\subsection{Quantitative Performance Analysis in Physical Multi-Stimuli and Variable Terrain
  Environments}` (`\label{ssec:QuantReal}`) — per-scenario (Appetitive/Aversive/Complex/Obstacle)
  hardware plots: switching-delay ECDF, basal-ganglia neural dynamics, Pitch/Roll RMS — **structurally
  near-identical in framing to the simulation quantitative-validation subsubsections above**. This is
  the concrete duplication **R2-01** asks to remove ("remove duplicate...identical stability curves
  between simulation and hardware tests") — the sim and real sections tell the same four-scenario
  story twice with parallel figure sets; condensing/cross-referencing instead of repeating narration
  is the likely fix, not just deleting figures. Also contains an energy-consumption figure
  (morphological transition energy, `FigReal_Morphological_Transition_Energy.png`) — that's
  **transition-cost** energy, not the "multi-mode long-term average" energy **R2-04** asks for;
  likely still a gap. And a 4-panel terrain-latency figure (neural + electromechanical latencies per
  transition direction).
- `\subsection{Limitations of the Present Work}` (`\label{ssec:Limitations}`) — **already exists**,
  already covers: low-torque servos / open-loop gait limitations (directly relevant to **R3-03**, but
  only as an acknowledged limitation — no compensation strategy is proposed, which is what R3-03
  actually asks for), lab-only validation scope, and the symbolic (non-certified) warehouse sim
  caveat. **R2-03 ("consolidate all limitations into a dedicated section") may already be largely
  satisfied structurally** — verify whether limitations are mentioned anywhere else in the paper
  (introduction, conclusions) that would still need pulling in here, and whether "dedicated section"
  means promoting this from a `\subsection` of Results to its own top-level `\section`.

### conclusions.tex
Summary of findings (stable/adaptive navigation across stimulus configurations and terrain
variations). Not yet read this round — likely does not need R2-03 (limitations already has a home in
results.tex), but check for limitations content duplicated here that should be removed once R2-01/R2-03
condensing happens.

## Key terms / notation
- WTA = Winner-Take-All (the basal ganglia's arbitration mechanism — methodology.tex, "Basal Ganglia
  Module"; ablation/threshold-logic comparison is R3-02, not yet written anywhere)
- FSM = Finite State Machine (the baseline R2-02 asks to compare against — no existing content)
- CPG = Central Pattern Generator (literature comparison point for R3-06 — introduction.tex)
- STN/GPe/GPi = subthalamic nucleus / external / internal globus pallidus — the basal ganglia
  circuit's three structures (methodology.tex)
- `Ar = 28.0` — the approach-stop inhibition threshold, derived from camera pinhole geometry
  (methodology.tex) — likely relevant context if R3-02's threshold-logic comparison references it
- `TR` (Tipover Risk), `SM` (Normalised Stability Margin) — stability metrics already defined and
  used in results.tex's transition-stability analysis

## Known cross-references
- results.tex's "Limitations" subsection explicitly defers energy characterisation of locomotion
  modes to "the physical implementation section" — i.e. it already cross-references the energy figure
  earlier in the same file (`FigReal_Morphological_Transition_Energy.png`).
- The MLP ablation/classifier-comparison work in results.tex's "Evaluation of the MLP-based terrain
  classifier" is self-contained (references methodology's gait-decision module by section label
  `ssec:Gait_Decision_Module` — not yet located; grep methodology.tex for that label before assuming
  its exact location).
- Not yet mapped: introduction.tex and conclusions.tex internal structure/cross-references — only
  skimmed, not fully read.
