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

### introduction.tex — fully read this round
Motivation (infrastructure inspection hazards), a substantial literature review (wheeled-legged
robots: ANYmal, CERBERUS, CENTAURO, Ascento; basal-ganglia computational models: Gurney's GPR model,
Prescott, Girard, Baston, Prescott2024), the novelty claim, contribution, and a closing paragraph that
maps the paper's own section structure.

- **R3-06 target, easier than expected**: the literature review **already narratively contrasts**
  action-selection approaches — "hand-coded threshold logic", MPC, and "end-to-end RL policies [...]
  as a black-box behavior" are explicitly named as the alternatives to the basal-ganglia approach used
  here (paragraph starting "A critical observation emerges..."). R3-06 likely just needs this existing
  comparison **converted into a table**, not written from scratch. One gap: CPG is discussed elsewhere
  in the intro (next paragraph) only as a *rhythm-execution* layer below BG arbitration, not framed as
  an alternative *action-selection* paradigm — the table will need to reframe CPG as a third
  comparison point even though this paper doesn't use it that way itself.
- **Cross-reference risk**: the last paragraph literally says *"Section 2 details the methodology...
  Section 3 presents the experimental results... Section 4 outlines the conclusions"* — hardcoded
  numbers, not `\ref{}`. If R2-03 (or anything else) adds/removes/reorders a top-level `\section`,
  this paragraph must be updated by hand or it goes stale.
- No FSM mention here either (consistent with methodology.tex — R2-02 is new content, full stop).

### methodology.tex (501 lines) — fully read this round
Four components stated up front: (1) robot morphology/transformation, (2) Gazebo simulation, (3)
neuronal control circuits, (4) physical construction. Four subsections:

- `\subsection{Platform Design}` (`\label{ssec:Platform_Design}`, line 6) — 3-DOF legs (3 servos +
  1 geared wheel motor each), LiDAR/camera/IMU sensor suite, low center of mass + passive support
  wheel. Not relevant to R3-01/R3-02/R2-02.
- `\subsection{Gazebo Simulation}` (line 28) — URDF from SolidWorks, Gazebo Harmonic. Terrain has
  three zones: flat, gravel-roughness, and a slope with $5°/10°/25°/45°$ inclines; separately, the
  neural-arbitration validation terrain uses calibrated inclines + **procedurally generated
  Perlin-noise surfaces** + simple static obstacles. Visual stimuli are red/blue 3D shapes
  (appetitive/aversive).
- `\subsection{Neuronal Control System}` (line 60) — **the core section**. Explicitly names four
  modules in order: obstacle-sensory, basal-ganglia, locomotion, gait-decision.
  - `\subsubsection{Obstacle Sensory Module}` (line 68) — 16-unit Gaussian neuron ring (LiDAR
    angular encoding, after \citet{pardo2022bio}) feeding front/rear/left/right integrator "tank"
    neurons $L_0$–$L_3$ and accumulator $L_4$, plus input/response/auxiliary layers $I_n/R_n/A_n$.
    Eqs.~\eqref{eq:ring}, \eqref{eq:L0}–\eqref{eq:L4}. Not the ablation target itself but $L_0$–$L_4$
    feed directly into both the basal-ganglia and locomotion modules.
  - `\subsubsection{Basal Ganglia Module}` (line 154) — **the R3-01/R3-02 target.** STN/GPe/GPi/STR
    winner-take-all circuit after \citet{sarvestani2013computational}, Eqs.~\eqref{eq:stn}–\eqref{eq:str},
    hyperparameters in Table~\ref{table:Ganglia} (all weights currently 1.0, only time constants
    differ: $\tau_{STN}=\tau_{Gpe}=\tau_{STR}=2.0$, $\tau_{Gpi}=1.0$). **Important for framing R3-01/
    R3-02**: an existing `\revblue{}` paragraph (line 200, already written in a *prior* revision
    round) already argues the architecture's merits vs. RL/MPC — citing \citet{Gurney2001a,Gurney2001b,
    Prescott2006Robot} as "canonical arbitration circuits validated in computational neuroscience" and
    citing a measured **decision latency of ~47 ms** (cross-referenced as "Section~3", i.e.
    results.tex) as evidence of real-time operation without training/inference infrastructure. This is
    useful groundwork/citations to reuse, but it is a justification paragraph, **not an ablation study
    or a WTA-vs-threshold-logic comparison** — that content still does not exist anywhere.
    Confirmed: **no existing ablation study on the basal-ganglia network itself** anywhere in the
    paper (the only ablation content anywhere is the MLP terrain-classifier architecture ablation in
    results.tex, unrelated to the BG circuit).
  - `\subsubsection{Locomotion Module}` (line 202) — sensory/integrative/decisional sublayers,
    $\theta_s$/$\theta_p$ direction encoding, explicit **20° threshold** on units $X_5$/$X_6$ defining
    "frontal zone", stop signal from unit $X_{17}$ gated by `Ar = 28.0` (pinhole-camera-derived, full
    derivation given in a `\revblue{}` paragraph at line 305). **Relevant to R3-02**: this module
    already uses explicit hard thresholds (the 20° frontal cone, `Ar`) as part of its own design —
    i.e. the paper already mixes WTA (basal ganglia) with threshold logic (locomotion module) in
    different places, which could be leveraged when framing a "WTA vs. threshold-only" comparison,
    though no formal side-by-side study exists.
  - `\subsubsection{Gait Decision Module}` (`\label{ssec:Gait_Decision_Module}`, line 313) — Naka–
    Rushton nonlinearity (Eq.~\eqref{eq:Naka}), two instantiations $f_{Imu}$/$f_{Mode}$. Original
    3-mode network (Eqs.~\eqref{eq:Z0}–\eqref{eq:Z16}, Fig.~`Modos_Locomocion`) plus a **second,
    MLP-informed version** (Eqs.~\eqref{eq:Z0V2}–\eqref{eq:Z16V2}, Fig.~`Modos_LocomocionV2`) that
    replaces raw IMU thresholding with a 2-hidden-layer (150, 80 units) MLP classifying flat/inclined
    terrain + stagnation from a $9\times15=135$-dim windowed IMU+direction input. Simulation and
    physical implementation use **different** gait-decision networks (unit $X_2$ dropped for
    physical, since one MLP output already encodes combined roll/pitch tilt).
- `\subsection{Physical Platform Construction and Experimental Setup}` (`\label{ssec:Construction}`,
  line 447) — N20 wheel motors (104 RPM), MG996R leg servos (11 kg·cm), ESP32-S3 Zero MCU,
  PCA9685 + mini-L298N drivers, MPU-6050 IMU, HMC5883L magnetometer, Logitech C270 camera, 7.2V/
  3300mAh Li-ion battery, PLA/PETG 3D-printed structure. Physical test terrains: a 20° incline +
  flat platform rig, and a **physically fabricated** Perlin-noise terrain (`\revblue{}`, line 485)
  matching the simulated one 1:1 — laser-cut MDF, $1300\times900$mm, $250\times250$ grid, reported
  stats ($\sigma_h=2.339$mm, $R_q=2.339$mm, mean slope 0.155). This is the real-world counterpart to
  the simulated Perlin terrain in Gazebo Simulation above — relevant if R3-04 (noise robustness) or
  R3-01/R3-02 ablations need a physical (not just simulated) validation terrain.
- Confirmed by full read: **no mention of FSM (Finite State Machine) anywhere in this file** —
  R2-02's baseline comparison is entirely new content, not a rewrite of existing material.

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

### conclusions.tex — fully read this round
Summary of findings, comparison against \citet{sarvestani2013computational}, a **second, separate**
limitations paragraph, forward-looking remarks, and a closing `\revblue{}` summary paragraph. Also
contains the paper's trailing unnumbered backmatter as `\section*{}` blocks in the same file
(Acknowledgements, Author Contributions, Declaration of Competing Interest, AI-assisted writing
disclosure) — these aren't split out separately since `split_sections.py` only splits on non-starred
`\section{}`, and they fall before the closing-boundary markers.

- **R2-03, important correction to the earlier read**: there are **two separate limitations
  discussions**, not one — results.tex's `\subsection{Limitations of the Present Work}` (low-torque
  servos/open-loop gait, lab-only validation scope, symbolic sim caveat) AND an unlabeled paragraph
  here starting *"Several limitations must be acknowledged..."* (manual parameter tuning/no adaptive
  optimization, no hardware-failure/sensor-dropout resilience testing, no formal sensor-fusion
  framework, illumination-invariance untested for color-based vision). **Consolidating means merging
  two different lists, not deleting a duplicate** — the content itself doesn't overlap much.
- **Found a real inconsistency (candidate `C-xx` correction, independent of R2-03)**: this paragraph
  states *"Classification metrics for strengthening the MLP-based terrain classifier were also not
  evaluated"* — but results.tex's `\revblue{}` MLP subsection **already reports** accuracy/precision/
  recall/F1/ROC-AUC and a full ablation+classifier-comparison study. This sentence is stale, almost
  certainly left over from before that content was added in a prior revision round. Needs a fix
  independent of the reviewer checklist — flag as `C-01` (see PROGRESS.md).

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
  `ssec:Gait_Decision_Module`, confirmed at methodology.tex line 313).
- methodology.tex's basal-ganglia `\revblue{}` justification paragraph (line 200) cross-references
  "Section 3" for the ~47ms decision-latency figure — that number lives in results.tex, not
  methodology.tex; verify it before reusing it in R3-01/R3-02 text.
- introduction.tex's closing paragraph hardcodes "Section 2/3/4" for methodology/results/conclusions,
  and methodology.tex's BG-justification paragraph (line 200) hardcodes "Section~3" for the same
  results.tex cross-reference — update both by hand if the top-level section structure changes (e.g.
  R2-03 promoting Limitations to its own section). `scripts/check_hardcoded_refs.sh` detects both
  automatically (advisory, run before push — see README.md §10.1).
- conclusions.tex's stale "MLP metrics not evaluated" sentence contradicts results.tex's own
  `\revblue{}` MLP evaluation subsection — see `C-01` in PROGRESS.md.
- All four sections (introduction.tex, methodology.tex, results.tex, conclusions.tex) have now been
  fully read at least once this round. `methodology.tex`'s full read confirms R3-01/R3-02 are real
  gaps (no BG ablation, no WTA-vs-threshold study) but surfaces reusable groundwork: the existing
  `\revblue{}` justification paragraph (citations + 47ms latency) and the locomotion module's own use
  of explicit thresholds (20° frontal cone, `Ar=28.0`) as a natural "threshold logic" contrast point.
