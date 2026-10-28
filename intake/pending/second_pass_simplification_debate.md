# Second-pass simplification debate (2026-10-28)

Proposer pass over `introduction.tex`, `methodology.tex`, `results.tex`, `conclusions.tex` and the abstract, made after
the R3b-01 first pass (`patches/r3b-01-condense-redundant-definitions.tex`). Nothing that pass already condensed is
proposed again. Every proposal removes a duplicate or filler only: each one says where the information still lives.
Quotes are the start of the target text and can be found with `grep -n`. Word savings are rough. Any replacement
text that goes into `sections/` still needs `\revblue{}` when it changes meaning (pure deletions need no marker).

## Proposals

### P-01 — Take the "reviewer's request" wording and R-IDs out of the manuscript prose
- **Location:** 10 sites. `methodology.tex` `ssec:FSMBaseline` "To address the reviewer's request for a finite state machine (FSM) baseline"; `results.tex` ablation subsubsection "To directly address the reviewer's request for an ablation analysis"; same subsubsection "directly addressing the reviewer's request to quantify the consequence" and "(R3-01)" / "(R3-02)" in "Taken together, these results support the winner-take-all"; `sssec:transition_stability` "To address the reviewer's request for systematic quantitative metrics"; `sssec:fsm_baseline_comparison` "To address the reviewer's request for a finite state machine"; `sssec:reactive_inspection` "To directly address the reviewer's request for inspection-oriented task indicators", "directly addressing the reviewer's request for target tracking accuracy", "This experiment also provides quantitative evidence responding to the reviewer's request"; `sssec:mlp_eval` "to directly address the reviewer's request for an onboard deployment analysis"; energy paragraph "To directly address the reviewer's request for long-term average energy".
- **Type:** tighten (same sentence pattern repeated)
- **Owner:** Sebas for 8 sites. The 3 ablation sites belong to Sam (R2b-01) / Deivi (R3b-02).
- **Proposed change:** remove the framing clause and keep the content. Examples: "To provide a finite state machine (FSM) baseline under identical experimental conditions, a second mode-arbitration controller…"; "For inspection-oriented task indicators, the platform was evaluated…"; "…$d_{final} = 1.076 \pm 0.038$~m (Table…): the BG$\rightarrow X_{17}$ loop converges…"; "This experiment also quantifies re-routing after obstacle blockage: …"; "…(PyTorch)…; the same forward pass was additionally re-implemented in C…"; "Table~\ref{tab:mode_steady_state_energy} reports the mean steady-state power…". Delete ", directly addressing the reviewer's request … (R3-01)" outright, and delete "(R3-01)" and "(R3-02)". Sites in transition-stability, FSM-results and energy are rewritten in full in P-06, P-18 and P-22.
- **Why it's safe:** the reviewer→change mapping is in the response letter and in `PROGRESS.md`. A published article can't refer to "the reviewer" or to internal IDs, so the editor would ask for these to come out anyway.
- **Est. saving:** ~130 words

### P-02 — Shorten the second-to-last conclusions paragraph, which restates paragraphs 1, 3 and 4
- **Location:** `conclusions.tex` `sec:conclusions`, the paragraph starting "The findings provide a highly efficient baseline demonstrating that lightweight".
- **Type:** duplicate + tighten
- **Owner:** Sebas (the R2b-04 external-computer clauses are Sebas's own round-2 text)
- **Proposed change:** replace the whole paragraph with:
  "The findings show that lightweight, bio-inspired neural networks can arbitrate multimodal gait transitions and reactive behaviors from visual and inertial cues \revblue{on a real robotic platform, with the neural circuits executed on an external computer}. The perception-decision pipeline additionally retained task-level performance under combined IMU-drift and LiDAR-noise perturbation, and, conditionally on the scenario, camera illumination distortion (Section~\ref{ssec:NoiseRobustnessEval}), evaluated jointly rather than as isolated single-sensor degradations. Despite the prototype's hardware boundaries (Section~\ref{ssec:Limitations}), these results indicate that complex multi-stimulus mobility decisions are feasible for resource-constrained platforms; \revblue{onboard feasibility was assessed only for the MLP terrain classifier on the ESP32-S3 (Section~\ref{sssec:mlp_eval}), not for the full neural pipeline}."
- **Why it's safe:** the deleted sentences are all said elsewhere. "Ability to switch locomotion modes based on inertial stability metrics … flat, rough, and inclined surfaces" is the conclusions paragraph starting "On irregular surfaces and steep slopes". "Dynamic goal prioritization, collision avoidance … collision-free goal approach, validated in both simulation and physical" is paragraph 1 ("physical robot reliably reaches the appetitive stimulus while avoiding obstacles") and paragraph 3 ("consistently prioritized the most relevant objective"). "When scaled onto robust physical platforms … power-plant monitoring" is filler; the deployment direction is in the next paragraph's future-work list ("migrating the arbitration logic to industrial-grade platforms"). "Low-torque actuation and open-loop locomotion profiles" is in the Limitations pointer paragraph ("spanning the physical platform's hardware envelope"). The duplicate "future-work priorities detailed below" signpost also goes; the Limitations-pointer paragraph already has one. The noise-caveat sentence and both external-computer clauses are kept word for word.
- **Est. saving:** ~120 words

### P-03 — Ablation: Roll/Pitch RMS numbers appear in full in both the caption and the prose
- **Location:** `results.tex`, Basal Ganglia Ablation Study, the paragraph starting "Decision latency under conflict is unaffected by removing basal-ganglia mechanism". Also `fig:ablation_combined`, caption (a) sentence "Under the no-conflict Appetitive Targeting scenario (not shown), all four".
- **Type:** duplicate
- **Owner:** Sam (R2b-01, prose) / Deivi (R3b-02, caption)
- **Proposed change:** (1) In the prose, keep the decision-latency sentence with its CIs (it is not in the caption). Replace everything from "Roll RMS increases significantly for all three ablations" to the end of the paragraph with: "Roll RMS increases significantly under all three ablations, so attitude destabilization under conflict is a shared consequence of weakening the arbitration mechanism, whichever component is removed; Pitch RMS instead diverges by ablation type (Figure~\ref{fig:ablation_complex_stability}; percentages and $p$-values in the caption)." (2) In caption (a), delete the "Under the no-conflict Appetitive Targeting scenario (not shown) … $p=1.000$ for all three comparisons" sentence. The paragraph starting "Without stimulus conflict, all four variants perform" gives it in full.
- **Why it's safe:** every percentage and $p$-value removed from the prose stays in caption (b), word for word ("+43.6%, p<0.001 … −11.3% and −5.7%, both p<0.005 … plausibly reflecting reduced net locomotor activity"). The Appetitive 91.7–100% / $p=1.000$ result stays in the prose. $n=12$ and the simulation-only caveat are not touched.
- **Est. saving:** ~105 words

### P-04 — Obstacle Sensory Module: the index/notation paragraphs after Eqs. L0–L4 are wordy and redundant
- **Location:** `methodology.tex` `sssec` Obstacle Sensory Module, three paragraphs starting "In Equations~\eqref{eq:L0}–\eqref{eq:L4} the subscripts are used to enumerate", "Likewise, the indices $n$ and $r$ enumerate the neurons", and "The matrices $W^{(IR)}$, $W^{(RR)}$, and $W^{(RA)}$ denote connectivity".
- **Type:** merge + tighten
- **Owner:** Sebas
- **Proposed change:** replace the three paragraphs with one:
  "Here $Z_i$ is the $i$-th ring neuron, ordered angularly around the robot; the sums $\sum_{i=a}^{b} Z_i$ group the ring into the front, rear, left, and right sectors integrated by $L_0$–$L_3$ (Figure~\ref{fig:lidar-combined}). $I_n$, $R_n$, and $A_n$ are the $n$-th neurons of the input, response, and auxiliary layers; $i$, $j$, and $r$ are summation indices. $W^{(IR)}$, $W^{(RR)}$, and $W^{(RA)}$ are fixed (binary or patterned) structural connectivity matrices of the Integrating Neural Network (Figure~\ref{fig:IntLidar})."
- **Why it's safe:** the roles of $L_0$–$L_3$ ("tank neurons… front, rear, left, and right sectors") are already in the paragraph starting "Additionally, directional groups were defined". $L_4$ as the store of evasive-stimulus intensity is in "These layers determine the predominance of the evasive action ---information that is stored in the accumulator neuron $L_4$". "Fixed uniform" is in the Table-LiDAR notation ("These weights are fixed uniform values").
- **Est. saving:** ~90 words

### P-05 — Transition stability: the opening sentence and the "Stability metrics" paragraph say the same thing
- **Location:** `results.tex` `sssec:transition_stability`, "To address the reviewer's request for systematic quantitative metrics", plus the `\paragraph{Stability metrics.}` paragraph "The Normalized Stability Margin ($SM$) and Tipover Risk".
- **Type:** merge
- **Owner:** Sebas
- **Proposed change:** replace both with one paragraph, and delete the `\paragraph{Stability metrics.}` heading:
  "This subsubsection quantifies static stability for the Quadrupedal Walking gait and all six pairwise transitions among the three locomotion modes, using the Normalized Stability Margin ($SM$) and Tipover Risk ($TR$) of Section~\ref{sssec:variable_topo_quant}, computed frame-by-frame from the foot-contact positions logged in simulation."
- **Why it's safe:** both originals say "Quadrupedal Walking gait and all six pairwise transitions". The metric definitions stay pointed at `sssec:variable_topo_quant`. This also removes one P-01 site.
- **Est. saving:** ~45 words

### P-06 — Mode-transition stability: the prose re-describes the figure, and the "four feet in contact / no instability" argument appears three times
- **Location:** `results.tex` `sssec:transition_stability`, `\paragraph{Mode-transition stability.}`. Sentence "Figure~\ref{fig:transition_phases} shows the three undirected mode pairs"; paragraph "A critical property of the mode-switching protocol is that"; paragraph "Regarding oscillation amplitude during transitions:".
- **Type:** duplicate + tighten
- **Owner:** Sebas
- **Proposed change:** (1) Replace the "Figure … shows the three undirected mode pairs … rather than as two separate directed rows." sentence with: "Both directions of each mode pair converge to statistically indistinguishable support-polygon geometries and $TR$ values, so Figure~\ref{fig:transition_phases} shows each undirected pair ($C \leftrightarrow H$, $H \leftrightarrow X$, $X \leftrightarrow C$) once." (2) In the "A critical property…" paragraph, delete "The support polygon therefore remains non-degenerate throughout the entire switching interval." and change "and all $N_{\mathrm{total}} = 979$ logged samples," to "and all logged samples,". (3) Shorten the start of the oscillation paragraph to "Because reconfiguration is performed with all four feet in contact, no abrupt postural discontinuity is introduced at the switching instant. The steady-state Roll and Pitch RMS bounds …" and keep the rest.
- **Why it's safe:** the double-headed arrow and the per-mode ranges are explained in the `fig:transition_phases` caption ("one row per undirected mode pair… the double-headed arrow denotes…"). $N_{\mathrm{total}} = 979$ is stated earlier in the same subsubsection ("($N_{\mathrm{total}} = 979$ samples across the complete sequence)") and again in the instantaneous-reading caveat. "Non-degenerate support polygon" is in the preceding sentence ("constrained to states in which all four feet simultaneously maintain ground contact") and in the caption ("all four feet maintain ground contact throughout"). See also Side note S-05 (the 1.36° bound).
- **Est. saving:** ~70 words

### P-07 — Phase-space paragraph ends by restating its own opening and the subcaption
- **Location:** `results.tex` `sssec:variable_topo_quant`, last sentence of the paragraph "To quantitatively assess the adaptive morphology and environmental specialization", starting "The Pitch-RMS separation between both domains provides empirical evidence". Also subcaption `fig:terrain_adaptability`, the clause ", demonstrating that the neural controller synthesizes a distinct, terrain-specialized locomotive signature".
- **Type:** duplicate
- **Owner:** Sebas (prose); the subcaption trim needs coordination with Deivi (R2b-05/R3b-04 caption sweep)
- **Proposed change:** delete the final prose sentence. In the subcaption, replace ", demonstrating that … for each environment." with "." Also shorten the paragraph's opening to "The steady-state kinematics of both terrains were mapped onto a Roll RMS ($\phi_{\text{RMS}}$) vs. Pitch RMS ($\theta_{\text{RMS}}$) phase space across all 30 successful trials (Figure~\ref{fig:terrain_adaptability})."
- **Why it's safe:** "clear separation in Pitch RMS … partial overlap in Roll RMS" is the paragraph's second sentence. "Terrain-specialized" and "lateral stabilization comparably effective" are in the subcaption ("…the overlap between terrains is itself the evidence of comparably effective lateral stabilization"). The per-terrain means stay.
- **Est. saving:** ~70 words

### P-08 — Tipover-risk paragraph: TR = 1.0 explained three times; "15 runs / 30 trials / never crossed" repeats the subcaption
- **Location:** `results.tex` `sssec:variable_topo_quant`, the paragraph starting "To quantitatively evaluate the dynamic stability and structural safety of the hybrid".
- **Type:** tighten + duplicate
- **Owner:** Sebas
- **Proposed change:** (1) Replace the opening sentence with "The Tipover Risk ($TR$) index was tracked across 15 randomized runs per terrain (Figure~\ref{fig:stability_profile})." (2) Delete "By aligning the temporal records around the exact neural mode-switch instant ($t = 0.0\,\text{s}$), the physical efficacy of the bio-inspired controller was made directly observable." (3) Change "well below the critical overturning threshold throughout the recorded window" to "throughout the recorded window". (4) Shorten the last sentence to "Across all 30 trials the $\pm 1\sigma$ envelope never crossed $TR = 1.0$." The definition sentence ($TR = 1 - SM/r_{in}$, McGhee–Frank), the 0.0/1.0 interpretation, the means, the 0.77 spike and the inclined-slope flatness all stay.
- **Why it's safe:** alignment at $t=0$ is in subcaption (a) ("aligned around the neural mode-switch instant ($t = 0.0\,\text{s}$)") and in main caption (A). "15 trials" and "No trial violated this limit across all 30 runs" are in subcaption (a). $TR=1.0$ as the overturning boundary stays once in the definition sentence. Dropping "under stochastic noise conditions" is deliberate; see S-02.
- **Est. saving:** ~65 words

### P-09 — Shorten the simulated energy-consumption paragraph to one sentence
- **Location:** `results.tex` `sssec:transition_stability`, paragraph "Regarding energy consumption: the Gazebo simulation environment was not instrumented".
- **Type:** tighten
- **Owner:** Sebas
- **Proposed change:** replace it with "Joint-level energy was not logged in Gazebo (no power-monitoring plugin); energy per mode is characterized on the physical platform in Section~\ref{ssec:QuantReal}."
- **Why it's safe:** both claims are kept (no simulated energy data; physical energy reported elsewhere). The vague "physical implementation section" becomes a real `\ref`.
- **Est. saving:** ~55 words

### P-10 — Simulation scenario paragraphs: "every retained trial succeeded at all five levels" appears four times, plus filler
- **Location:** `results.tex`, Quantitative Validation: Single-Stimuli / Multi-Modal, in the bold-led paragraphs "\textbf{Appetitive Targeting", "\textbf{Aversive Escape", "\textbf{Obstacle Evasion", "\textbf{Complex Navigation".
- **Type:** duplicate + tighten
- **Owner:** Sebas, but this touches the noise caveat, so check with Diego (R2b-02)
- **Proposed change:** put one sentence after "The performance of the platform was evaluated under isolated sensory stimuli…": "In all four scenarios, three successful trials were retained at every combined-perturbation level (Figure~\ref{fig:noise_robustness_grid}); attempts discarded before reaching that count are analyzed in Section~\ref{sssec:noise_robustness_extra}." Then delete the per-paragraph versions: "every retained trial reaches the target regardless of severity level (…)"; "with every retained trial across all five severity levels resolving the threat successfully (…)"; "Every retained trial across all five combined-perturbation levels completed evasion successfully (…)"; "Every retained trial across all five combined-perturbation severity levels resolves this three-stimulus encounter successfully (…)", keeping the "evidencing that the arbitration network does not suffer from computational deadlocks…" clause as its own sentence. Also delete the filler "demonstrating the efficiency of the neural gating mechanism", "The sensory-locomotor coupling is precise:" and "The complex navigation suite culminates the simulation validation,". **Keep** the Appetitive paragraph's joint-perturbation caveat sentence word for word ("This robustness is evaluated under the combined perturbation … not against any single sensor's contribution in isolation").
- **Why it's safe:** the per-level outcomes live in `fig:noise_robustness_grid` and in `fig:failure_by_family`. As written, "every *retained* trial succeeded" is close to tautological: retained trials are by construction the successful ones (`ssec:NoiseRobustnessEval`: "retaining three successful replicates per severity level"). One sentence that says so honestly is more accurate than four that imply 100% robustness.
- **Est. saving:** ~70 words

### P-11 — MLP evaluation: AUC 0.864 appears four times; LR F1 = 0.692 twice; the "rationale … given below" signpost
- **Location:** `results.tex` `sssec:mlp_eval`. Sentences "As illustrated in Figure~\ref{fig:mlp_eval_grid}a, the final model produced a confusion" and "The classifier's discrimination capacity is further supported by the ROC curve". The paragraph "The MLP was further benchmarked against alternative classifiers" ending "the rationale for nonetheless selecting the MLP is given below, alongside the per-sample latency comparison". The next paragraph's "To assess whether the accuracy gap with respect to SVM-RBF and Random Forest justifies" and "while substantially outperforming Logistic Regression ($\text{F1} = 0.692$) at a comparable latency".
- **Type:** duplicate + merge
- **Owner:** Sebas
- **Proposed change:** (1) Delete the "As illustrated … produced a confusion matrix on the held-out test set." sentence. Add "(confusion matrix: Figure~\ref{fig:mlp_eval_grid}a)" after "On the held-out test set ($n = 120$)". (2) Change the ROC sentence to "The ROC curve (Figure~\ref{fig:mlp_eval_grid}b) stays well above the chance diagonal across the operating range." (3) End the benchmark paragraph after "(Figure~\ref{fig:classifier_tradeoff}a)." and start the latency paragraph with "Per-sample inference latency (Figure~\ref{fig:classifier_tradeoff}b) explains why the MLP was nonetheless selected: it requires only…". (4) Change "while substantially outperforming Logistic Regression ($\text{F1} = 0.692$) at a comparable latency of $0.54\,\mu\text{s}$" to "while Logistic Regression, at a comparable $0.54\,\mu\text{s}$, is markedly less accurate". (5) Change "a directly relevant factor for deployment on resource-constrained embedded hardware" to "relevant for embedded deployment".
- **Why it's safe:** AUC 0.864 stays in the test-set sentence and in both the subcaption and main caption of `fig:mlp_eval_grid`. LR F1 = 0.692 stays in the benchmark paragraph. "Resource-constrained embedded microcontroller" stays in the revblue rationale clause.
- **Est. saving:** ~65 words

### P-12 — Reactive Inspection: reactive-behavior restatement, a duplicated "route doesn't matter" claim, and circular Limitations pointers
- **Location:** `results.tex` `sssec:reactive_inspection`. Paragraph "As described in Section~\ref{ssec:Gazebo_Simulation}, the system's behavior in this task is purely reactive"; sentence "What both subgroups clearly share is that route complexity does not degrade"; the three pointers "(see Section~\ref{ssec:Limitations})" (coverage rate), "(Section~\ref{ssec:Limitations})" after "first-acquisition metric, not re-acquisition…", and "(Section~\ref{ssec:Limitations})" after "unfavorable dynamic configurations".
- **Type:** duplicate
- **Owner:** Sebas
- **Proposed change:** (1) Shorten the first two sentences to "As described in Section~\ref{ssec:Gazebo_Simulation}, behavior in this task is purely reactive (no map, no spatial memory); re-routing emerges from the BG/WTA arbitration." and keep the coverage-rate and indicator sentences. (2) Delete the "What both subgroups clearly share …" sentence. (3) Delete the three Limitations pointers.
- **Why it's safe:** "no map … no global re-route … same basal-ganglia/winner-take-all arbitration … to laterally evade each obstacle in real time while continuing toward the target once visible" is in `methodology.tex` `ssec:Gazebo_Simulation` ("As in the other simulated scenarios, the robot's behavior in this task is purely reactive"). "Route complexity doesn't degrade precision" is in the earlier sentence "the BG$\rightarrow X_{17}$ loop converges to essentially the same stopping distance … regardless of the route taken", and in "converges at least as tightly". The Limitations pointers are circular: the last Limitations paragraph says these constraints "are established alongside that experiment's own results … and are not restated here". So the pointers lead a reader to a paragraph that sends them straight back.
- **Est. saving:** ~65 words

### P-13 — FSM single-stimulus paragraph and figure: "not a success rate" said three times; "FSM never retries" twice in the prose
- **Location:** `results.tex` `sssec:fsm_baseline_comparison`, the paragraph "In the three single-stimulus suites (Appetitive, Aversive, Obstacle), the FSM's fixed priority". Caption of `fig:attempts_vs_noise_level`, "(not a success-rate metric --- every mission in this dataset eventually".
- **Type:** duplicate
- **Owner:** Sebas (the figure caption: coordinate with Deivi R2b-05)
- **Proposed change:** (1) In the prose, change "the FSM never requires one, at any noise level, while the Neural system occasionally does as noise increases. Figure~\ref{…} makes this explicit with its own metric, attempts needed per completed mission (not a success rate) --- Neural needs up to …" to "Figure~\ref{fig:attempts_vs_noise_level} quantifies this as attempts needed per completed mission: Neural needs up to …". (2) In the caption, shorten the parenthetical to "(not a success rate: every mission eventually succeeds; this counts attempts including retries)" and delete "FSM never needs a retry at any level in any of the three panels (flat at $1.0$)."
- **Why it's safe:** "FSM stays at exactly one attempt throughout" closes the same prose sentence. The success-rate definition sentence ("this is the only sense in which 'success rate' is used anywhere in this paper") stays. In the caption, "flat at 1.0" for FSM is still implied by the Obstacle-panel sentence and stated in the prose.
- **Est. saving:** ~50 words

### P-14 — The physical-scenario paragraphs repeat the "emergency reflex / bypasses trajectory filtering" explanation
- **Location:** `results.tex` `ssec:QuantReal`, "\textbf{Obstacle (see Figure~\ref{fig:obstacle_real_compound}):} Using physical barriers in the laboratory"; "\textbf{Complex (see …):} Under chained, safety-critical transformations over an extended". Captions of `fig:aversive_real_compound` ("revealing the near-instantaneous emergency reflex") and `fig:obstacle_real_compound` ("massive transient hyper-excitation peak … induced by volumetric geometric input").
- **Type:** duplicate + tighten
- **Owner:** Sebas (prose); the caption clauses need coordination with Deivi (R2b-05/R3b-04)
- **Proposed change:** (1) Change the first Obstacle sentence to "As in the Aversive scenario, the step response is immediate and consistent across all three replicates: geometric blockages are handled as emergency reflexes without trajectory ramp filtering." (2) Change the first Complex sentence to "Across successive back-to-back transformations, the deterministic step response shows the low-level controller managing electromechanical inertia and trajectory blending, protecting the joints from cumulative torque stress." (3) In the captions, drop the interpretation and describe the panels only: "(a) ECDF of mode-switching latency $T_{switch}$." and "(top) transient peak in neural firing variance $Var(z)$ (no stimulus-presence shading—non-chromatic obstacle cue)".
- **Why it's safe:** the reflex/bypass mechanism is in the Aversive paragraph ("the ROS~2 Control architecture bypasses heavy trajectory filtering…"). "Instantaneous" and "≈1100, transient" are in `tab:consolidated_physical_metrics`. The interpretations removed from the captions are given in the prose paragraphs next to them.
- **Est. saving:** ~50 words

### P-15 — Variable-topography main caption repeats its three subcaptions and ends with a filler sentence
- **Location:** `results.tex` `fig:variable_topo_metrics` main caption, "Quantitative performance profiles for the variable-topography experimental battery (15 trials each".
- **Type:** duplicate + tighten
- **Owner:** Deivi (R2b-05/R3b-04 caption sweep: keep N and the sim label)
- **Proposed change:** replace with "Quantitative performance profiles for the variable-topography battery (simulation, 15 trials per terrain): (A)~tipover risk aligned at the mode-switch instant; (B)~ECDF of mechanical transition time; (C)~Roll RMS vs.\ Pitch RMS phase space."
- **Why it's safe:** "neural response latency is reported numerically in the text, not plotted" is also in subcaption (b) ("Neural response latency ($T_{\text{response}}$) is not plotted here…"). The "Together, these three profiles provide the quantitative evidence base…" sentence carries no information. N = 15 is kept.
- **Est. saving:** ~50 words

### P-16 — Introduction: the CPG-arbitration argument appears twice, and the table's five rows are listed in prose
- **Location:** `introduction.tex` `sec:introduction`, paragraph "A critical observation emerges from this body of work". Sentences "Table~\ref{table:action_selection_comparison} summarizes this landscape along axes relevant" and "CPGs are predominantly used as a rhythm-\emph{generation} mechanism, but a body".
- **Type:** duplicate
- **Owner:** Sebas (the content was added for round-1 R3-06, which is closed)
- **Proposed change:** replace both sentences with "Table~\ref{table:action_selection_comparison} contrasts these approaches with central pattern generators (CPGs) and the basal-ganglia winner-take-all arbitration adopted here."
- **Why it's safe:** the five approaches are the table's row labels. The CPG-can-arbitrate point and its citations (`Fukui2019VestibularCPG`, `Owaki2017SpontaneousGait`) are in the table's CPG row ("feedback-modulated variants also arbitrate transitions") and in the later paragraph ("while feedback-modulated CPGs can themselves arbitrate discrete gait transitions \citep{Fukui2019VestibularCPG,Owaki2017SpontaneousGait}, the present design deliberately keeps that decision…"). The removed sentence itself only says "the rationale … is given below". The critic should check that R3-06's closing note didn't require the earlier placement.
- **Est. saving:** ~60 words

### P-17 — Gait Decision Module: Eqs. NakaImu/NakaMode just repeat Eq. Naka with σ substituted
- **Location:** `methodology.tex` `ssec:Gait_Decision_Module`, paragraph "Based on this general formulation, two task-specific activation functions are defined", plus `\label{eq:NakaImu}` and `\label{eq:NakaMode}`.
- **Type:** tighten (remove two display equations)
- **Owner:** Sebas
- **Proposed change:** replace the paragraph and both equation environments with "Two instantiations of Equation~\eqref{eq:Naka} are used: $f_{\mathrm{Imu}}(x) = f(x;\sigma_I)$ and $f_{\mathrm{Mode}}(x) = f(x;\sigma_M)$, whose different half-saturation constants match the dynamic range of the IMU and mode-selection pathways." Also delete ", where $(\cdot)_+$ denotes the rectified (positive-part) operator" before Eq. Naka, and "$x_+ = \max(x,0)$ is the rectified input;" in its where-clause (see P-27).
- **Why it's safe:** `grep` finds no `\eqref{eq:NakaImu}` or `\eqref{eq:NakaMode}` outside this one paragraph, so no reference breaks. Same content; $\sigma_I$/$\sigma_M$ stay in `table:Locom_NN`, and their roles in the rationale paragraph ("$\sigma_M$ provides rapid mode switching… $\sigma_I$ affords greater noise tolerance").
- **Est. saving:** ~45 words (+ 2 display equations)

### P-18 — The FSM results opening repeats the methodology's FSM opening almost word for word
- **Location:** `results.tex` `sssec:fsm_baseline_comparison`, "To address the reviewer's request for a finite state machine (FSM) baseline under identical".
- **Type:** duplicate
- **Owner:** Sebas (the prose only; the caption is Diego's R2b-03 and is not touched)
- **Proposed change:** replace the first sentence with "Table~\ref{tab:fsm_comparison} compares the FSM controller of Section~\ref{ssec:FSMBaseline} with the basal-ganglia network on all seven simulated suites, reporting success rate, task completion time, Roll RMS, and $\lambda$ --- a motor-command clarity ratio (commanded-velocity magnitude relative to neural activity norm; higher indicates more decisive output)." and delete the following "Table … reports … for both controllers in each suite." sentence.
- **Why it's safe:** "identical experimental conditions … same seven simulated suites under matching trial counts, noise levels, and success criteria" is in `methodology.tex` `ssec:FSMBaseline`. The λ definition is kept. The timing-fairness caveat paragraph ("On the two terrain suites…") is not touched.
- **Est. saving:** ~40 words

### P-19 — Compound-course prose restates its own segment list and trial count
- **Location:** `results.tex`, physical Response to Variable Topographies. "The sequential adaptation of the locomotion arbitration network throughout this compound course" and "Across the compound course (double-ascent ramp $\rightarrow$ elevated plane".
- **Type:** duplicate
- **Owner:** Sebas
- **Proposed change:** (1) Replace "The sequential adaptation … across six representative frames." with "Figure~\ref{fig:real_variable_topography_sequence} and Table~\ref{tab:terrain_sequence} document the resulting gait-switching sequence." (2) Change "Across the compound course (double-ascent ramp … 15 trials), the arbitration network autonomously transitions through the gait sequence summarised in Table~\ref{tab:terrain_sequence} (Figure~\ref{…})." to "The arbitration network autonomously transitions through this sequence."
- **Why it's safe:** the four segments and "15 continuous repetitive trials" are in the sentence just before. 15 trials is also in both the table and figure captions. "Observed across all 15 trials" stays in the closing sentence.
- **Est. saving:** ~45 words

### P-20 — The methodology opening paragraph restates the subsection list and the Construction subsection's citation
- **Location:** `methodology.tex` `sec:methodology`, "This study was structured around four main components. First, the robot".
- **Type:** tighten
- **Owner:** Sebas
- **Proposed change:** replace with "The work comprised four stages: designing a morphology that transforms among quadrupedal, differential-drive, and omnidirectional modes (Section~\ref{ssec:Platform_Design}); simulating it with its sensors in Gazebo (Section~\ref{ssec:Gazebo_Simulation}); developing the neural control circuits for LiDAR obstacle detection, motion direction, and locomotion-mode selection, complemented by an MLP terrain-instability detector; and building the physical robot (Section~\ref{ssec:Construction}). Fabrication drew on the prior engineering development of \citet{Grajales_Des_2025}, but the simulation design was kept as the morphological baseline to ensure virtual–physical consistency."
- **Why it's safe:** every claim is kept: the four stages, the MLP, the Grajales citation, and the sim-as-baseline decision. Only the "First… Second… Third… Additionally… Finally" scaffolding and the "definitive morphological reference / baseline" doubling go.
- **Est. saving:** ~40 words

### P-21 — The Limitations opening paragraph says "low-cost / low-torque / lightweight PLA" twice
- **Location:** `results.tex` `ssec:Limitations`, "As an open, low-cost exploratory research baseline, the physical robot is constructed". Also the virtual-environment paragraph "Regarding the virtual test environment: the Gazebo world used for".
- **Type:** duplicate + tighten
- **Owner:** Sebas
- **Proposed change:** (1) Change "This constraint is a direct consequence of the platform's low-cost mechanical design ---low-torque servomotors and a lightweight PLA structure--- rather than a limitation of the neural arbitration architecture itself." to "This constraint stems from the hardware, not from the neural arbitration architecture." and change the opening to "…constructed using low-torque servomotors and a lightweight PLA structure…". (2) Shorten the virtual-environment paragraph to "The Gazebo world of Figure~\ref{fig:depot_simulation} is a symbolic representation of an industrial storage facility: it was not built from measurements of any real facility, and its spatial statistics (corridor width, obstacle density, scene dimensions) were not benchmarked against real inspection deployments. Simulation results therefore demonstrate algorithmic behavior in a representative constrained environment, not performance guarantees for specific industrial buildings."
- **Why it's safe:** "low-torque" and "lightweight PLA" stay once each. Every caveat in the depot paragraph is kept; only "included to contextualize the platform's application domain" goes, and that is already in `results.tex` "to contextualize the simulation within its intended inspection application domain".
- **Est. saving:** ~45 words

### P-22 — The energy prose repeats the steady-state table caption's sampling description
- **Location:** `results.tex` `ssec:QuantReal`, energy paragraph "The energetic cost of physical adaptation was quantified from individually detected". The last sentence starts "To directly address the reviewer's request for long-term average energy".
- **Type:** duplicate
- **Owner:** Sebas (R3b-05 text; the caption is untouched)
- **Proposed change:** (1) Change "the between-direction difference is not statistically significant \revblue{(see caption)}, so neither direction should be read as more energetically costly than the other." to "the between-direction difference is not statistically significant \revblue{(see caption)}." (2) Replace the last sentence with "Table~\ref{tab:mode_steady_state_energy} reports the mean steady-state power draw of each mode."
- **Why it's safe:** "computed from pooled intra-segment power samples … electromechanical coupling window excluded … structural-command" is word for word in the `tab:mode_steady_state_energy` caption, together with the R3b-05 battery spec and sampling rule, which stay in place. "Not significant" already says neither direction costs more.
- **Est. saving:** ~40 words

### P-23 — Template sentences ("The differential equations … are presented below") and redundant "In Figure X, … are shown" sentences
- **Location:** `methodology.tex`: "The differential equations~\eqref{eq:stn}–\eqref{eq:str} that describe the dynamics"; "The differential equations~\eqref{eq:Z_3}–\eqref{eq:Z_17} describing the dynamics"; "The differential equations~\eqref{eq:Z0}–\eqref{eq:Z16} describing the dynamics of"; "The hyperparameters (Table~\ref{table:Locom_MLP}) and the Equations". `results.tex`: "In Figure~\ref{fig:GRAPH_IMU2}, the data recorded by the inertial sensor are shown."; "In Figure~\ref{fig:GRAPH_IMU_real}, the activations of the MLP outputs"; "In Figure~\ref{fig:GRAPH_IMU2_real}, the activations of the MLP outputs and"; the `fig:mode_timeline_inspection` caption's "Same qualitative pattern as Figure~\ref{fig:mode_timeline_complex}, reproduced here for this suite."
- **Type:** tighten (the same sentence template repeated)
- **Owner:** Sebas (the caption fragment: coordinate with Deivi)
- **Proposed change:** in the methodology, delete the stn–str sentence's "The differential equations … are presented below." tail, and trim the Z0–Z16 sentence the same way. The table refs are already in the where-clauses or table notation, and `table:Ganglia` is cited in the where-clause. Shorten the Z3–Z17 sentence to "In Equation~\eqref{eq:Z_13}, $HI$ denotes…" (keep the HI definition). Shorten the Z0V2 sentence to "Equations~\eqref{eq:Z0V2}–\eqref{eq:Z16V2} give the modified units (thresholds in Table~\ref{table:Locom_MLP})." In results, replace the two physical "In Figure…, the activations … are shown." sentences with one at the end of the second paragraph: "MLP outputs and stagnation state for both scenarios are shown in Figure~\ref{fig:graph_imu_real_pair}." Delete the simulated GRAPH_IMU2 sentence; `fig:graph_imu_pair` is already cited for (a). Delete the caption fragment, since the prose already says "follows the same pattern described for the Complex suite".
- **Why it's safe:** the equations follow these sentences directly, every table is still cited at least once, and every figure keeps at least one in-text `\ref` (check (a) and (b) of `fig:graph_imu_pair`/`fig:graph_imu_real_pair` after editing).
- **Est. saving:** ~70 words

### P-24 — The BG justification paragraph in methodology pre-states the results latencies
- **Location:** `methodology.tex` `sssec:Basal_Ganglia_Module`, "The architectural framework of the basal ganglia model adopted here is grounded". The clause starts "This is evidenced by the near-instantaneous neural decision dispatch".
- **Type:** duplicate
- **Owner:** Sebas (C-15 text from round 1, now baseline)
- **Proposed change:** replace "Its decentralized winner-take-all dynamics enable low-latency conflict resolution… This is evidenced by … (Section~\ref{sec:results}) --- well within real-time constraints…" with "Its decentralized winner-take-all dynamics resolve conflicts with low latency (measured in Sections~\ref{sssec:variable_topo_quant} and~\ref{ssec:QuantReal}) and need neither the training cycles nor the inference infrastructure of deep reinforcement learning or model predictive control, making interpretability and low runtime overhead intrinsic properties of the design."
- **Why it's safe:** $T_{response}=0.0$~s is in `sssec:variable_topo_quant`, and 184/534 ms are in the `fig:FourPanelLatencies` caption and in the Conclusions ("184--534~ms"). The pointer becomes more specific than `sec:results`. Note that C-15 deliberately put traceable numbers here; the critic may prefer to keep them, and it's a fair call.
- **Est. saving:** ~40 words

### P-25 — The Limitations noise sentence says "jointly, not isolated" twice in one sentence
- **Location:** `results.tex` `ssec:Limitations`. In the paragraph "Beyond the hardware and simulation-environment constraints above", the sentence "Notwithstanding these design simplifications, the perception-decision noise-robustness evaluation", and the clause after "Section~\ref{sssec:noise_robustness_extra})" starting "indicating that combined sensory perturbation degrades".
- **Type:** duplicate
- **Owner:** Diego (R2b-02/R3b-03 noise caveat)
- **Proposed change:** (1) Change "…perturbation, evaluated jointly rather than isolated per sensor --- no configuration in this evaluation exercises a single sensor's degradation in isolation from the other two." to "…perturbation, applied jointly: no configuration isolates a single sensor's degradation." (2) Shorten the Rugged Terrain clause to "…(Section~\ref{sssec:noise_robustness_extra}), although trials that complete show no trend toward instability."
- **Why it's safe:** the joint-not-isolated caveat is kept once and stays explicit. The IMU white-noise caveat sentence and the 8/4/27 numbers are not touched. The "degrades structural stability specifically on this terrain" reading is in `sssec:noise_robustness_extra` ("the only suite where the robot's structural stability … was compromised").
- **Est. saving:** ~30 words

### P-26 — The "neural pipeline runs on an external laptop" fact is stated five times
- **Location:** `results.tex` `sssec:mlp_eval` revblue clause ", the external laptop described in Section~\ref{ssec:HardwareSpec}, which also ran the neural circuits". Also `ssec:Limitations` "Regarding the computing platform: the neural circuits, the MLP terrain classifier".
- **Type:** duplicate
- **Owner:** Sebas (R2b-04)
- **Proposed change:** (1) In `sssec:mlp_eval`, keep the clause ", the external laptop of Section~\ref{ssec:HardwareSpec}" and delete "which also ran the neural circuits during the physical experiments". (2) Change the Limitations sentence's start to "Regarding the computing platform: as described in Section~\ref{ssec:HardwareSpec}, the neural circuits, the MLP terrain classifier, and the image processing ran off-board." and delete "linked to the robot through a serial connection … sensor acquisition and actuator control". Keep the onboard-feasibility sentence.
- **Why it's safe:** `ssec:HardwareSpec` prose and `table:HardwareParams` state the off-board computer, the serial link and the ESP32's role in full. The Conclusions keep their own (shortened, P-02) mention, so the fact still appears in Methods, Limitations and Conclusions.
- **Est. saving:** ~35 words

### P-27 — The rectifier $(\cdot)_+$ is defined three times; the 20° frontal zone twice
- **Location:** `methodology.tex`. "In the following equations, the subscript $(\cdot)_+$ denotes a rectifying operator" (Obstacle Sensory Module; keep this one). The repeats are in `ssec:Gait_Decision_Module` ("where $(\cdot)_+$ denotes the rectified (positive-part) operator" and "$x_+ = \max(x,0)$ is the rectified input"). Locomotion Module where-clause "and the bracketed term encodes a $20^\circ$ angular margin defining the frontal zone".
- **Type:** duplicate
- **Owner:** Sebas
- **Proposed change:** keep the first rectifier definition but cut its second sentence ("This ensures that only nonnegative inputs contribute … through this term."). Delete the two Gait-Decision repeats (they overlap P-17). In the Locomotion where-clause, delete ", and the bracketed term encodes a $20^\circ$ angular margin defining the frontal zone of the robot's field of view".
- **Why it's safe:** $(x)_+=\max(x,0)$ is defined once and applies to every equation that follows. The 20° frontal zone is in the preceding paragraph ("considers an object to be in front when it lies within twenty degrees … inhibitory thresholds on the activation of those neurons").
- **Est. saving:** ~45 words

### P-28 — X2 removal said twice; N0–N2 re-defined twice more
- **Location:** `methodology.tex` `ssec:Gait_Decision_Module`, "Using the new information, the gait-decision network was adjusted", and the where-clause "In Equations~\eqref{eq:Z0V2}–\eqref{eq:Z16V2}: $N_0$ is the MLP output". `results.tex`, simulated Response to Variable Topographies: "In the physical robot, this information corresponds to the MLP outputs:".
- **Type:** duplicate
- **Owner:** Sebas
- **Proposed change:** (1) Replace the "Using the new information…" paragraph with "Using this information, the gait-decision network was adjusted for the physical implementation only (Figure~\ref{fig:Modos_LocomocionV2}): unit $X_2$ is removed, since one MLP output already flags combined roll/pitch tilt, so simulation and hardware use separate gait-decision modules; inputs $X_0$ and $X_1$ now correspond to $N_0$ and $N_1$." (2) Shorten the where-clause to "In Equations~\eqref{eq:Z0V2}–\eqref{eq:Z16V2}, $U_{N_0}$ and $U_{N_1}$ are the activation thresholds of $N_0$ and $N_1$ (Table~\ref{table:Locom_MLP})." (3) In results, change the sentence to "In the physical robot, this information corresponds to the MLP outputs $N_0$–$N_2$ (Section~\ref{ssec:Gait_Decision_Module})."
- **Why it's safe:** $N_0$/$N_1$ (flat/inclined probability) and $N_2$ (binary stuck indicator) are defined in the paragraph starting "The ninth position includes a binary value". The $U_{N}$ definition must stay here: R3b-01 deleted the table-notation copy because this where-clause holds it.
- **Est. saving:** ~60 words

### P-29 — Filler closing sentences in methodology
- **Location:** `methodology.tex`. "These parameter choices reflect a balance between biological plausibility, computational efficiency" (Locomotion rationale). "This layout ensures a highly controlled and reproducible virtual environment" (`ssec:Gazebo_Simulation`). "Together, this layered strategy --- static stability by gait design, torque-aware" (`ssec:ServoCompensation`).
- **Type:** tighten
- **Owner:** Sebas
- **Proposed change:** delete the first two sentences outright, and change "the multi-body physical simulations were strictly restricted to structured topographies" to "simulations were restricted to structured topographies". In ServoCompensation, change "Together, this layered strategy --- … --- constitutes the compensating control approach for the platform's low-torque, open-loop actuation constraints. It does not substitute…" to "This layered strategy does not substitute…".
- **Why it's safe:** none of these sentences adds a fact. The three ServoCompensation techniques are the three "First/Second/Third" paragraphs just above. The open-limitation sentence and its `\ref{ssec:Limitations}` stay.
- **Est. saving:** ~55 words

### P-30 — Short openers: results intro, QuantReal intro, Obstacle-module sensor roles
- **Location:** `results.tex` `sec:results`, "Initially, simulations of the platform were performed in the Gazebo environment." `ssec:QuantReal`, "This subsection presents a rigorous quantitative analysis of the proposed bio-inspired". `methodology.tex` Obstacle Sensory Module, "To perceive appetitive and aversive stimuli, a visual input was implemented" and "For obstacle detection, a LiDAR sensor was used, as it provides precise".
- **Type:** tighten
- **Owner:** Sebas
- **Proposed change:** (1) Results intro: "Results are reported first for Gazebo simulation (single and multiple stimuli, and gait switching on the three-topology terrain of Figure~\ref{fig:TERR_IMU}) and then for the physical platform." (2) QuantReal intro: "This subsection reports four stimulus scenarios on the physical platform (three hardware replicates each, consolidated in Table~\ref{tab:consolidated_physical_metrics}), followed by energy and latency profiling over variable terrain." (3) Obstacle module: merge the two openers into "As outlined in Section~\ref{ssec:Platform_Design}, the camera identifies and localizes appetitive and aversive stimuli through image processing, while the LiDAR localizes obstacles. To transform the LiDAR output into neural activations…" and continue with "a ring of neurons was implemented…".
- **Why it's safe:** the results roadmap is also in the Introduction's last paragraph ("separating virtual multi-body simulation tests from physical prototype validations"). "Rigorous", "publication-quality analytical plots" and "full statistical transparency" are puffery with no content. The sensor roles are in `ssec:Platform_Design` ("The camera captures visual stimuli…, the LiDAR provides information regarding the presence and position of obstacles"). The three-replicate N stays.
- **Est. saving:** ~70 words

**Total if all accepted:** ~1,900 words.

## Side notes (not cuts — inconsistencies spotted while reading; for whoever owns the area)

- **S-01 (`sssec:variable_topo_quant`):** "Both ECDF distributions collapsed into a perfect Heaviside step function" is contradicted two sentences later (long tail to ≈0.6 s; 0.9–1.8 ms staircase). Consider deleting that clause.
- **S-02 (`sssec:variable_topo_quant`):** the TR/latency paragraphs say "under stochastic noise conditions" / "filtered out the injected sensor noise". But `sssec:noise_robustness_extra` calls this battery "the unperturbed Rugged Terrain/Inclined Slope trials". One of the two is wrong.
- **S-03 (`ssec:Limitations`):** "system resilience was also not assessed under … temporary sensory dropout conditions" conflicts with `fig:camera_dropout_evidence`, which shows camera-dropout evidence.
- **S-04 (`conclusions.tex`):** "direction-switching neural latencies of 184--534~ms" is attributed to appetitive/aversive arbitration. `fig:FourPanelLatencies` measures terrain-mode transitions (Quadrupedal↔Rolling), not stimulus conflicts.
- **S-05 (`sssec:transition_stability`):** "Roll … RMS bounds … remain below $1.36^\circ$". `tab:consolidated_simulation_metrics` has Obstacle Roll 1.55° and Complex 1.03±0.35.
- **S-06 (methodology vs results):** the methodology says steep inclines → differential rolling (also results "the platform adopts the differential rolling mode"). The Gait Decision Module says instability engages quadrupedal, and results say "$X_1$ … excites unit $X_{15}$, issuing the command to transform into quadrupedal mode" on the slope. Also "$X_1$ — inclination greater than five degrees" vs $U_{Pitch}=U_{Roll}=15$.
- **S-07 (`ssec:QuantReal`):** the Appetitive paragraph says the BG network "operates at the microsecond scale" vs 184–534 ms neural latency. The Obstacle/Complex paragraphs attribute the firing-variance spike to obstacles "flooding the camera sensor with spatial and depth data", but the C270 has no depth channel and obstacles are LiDAR-detected.
- **S-08 (`ssec:FSMBaseline`):** "any behavioral difference … is attributable exclusively to this mode-selection mechanism" is in tension with the results' admission of three terrain-configuration differences. That's within R2b-03's (Diego) fairness scope.

## Critic verdicts


Critic pass, 2026-10-28. Every quote below was checked with `grep -n` against `sections/*.tex` on branch
`sebas` (working tree, including the uncommitted R3b-01 edits). Rule for every ACCEPT/ACCEPT-MODIFIED item:
any rewritten (not purely deleted) text goes inside `\revblue{}`.

- **P-01 — ACCEPT-MODIFIED (ablation sites DEFER-TO-OWNER: Sam, R2b-01)**
  - Verification: there are 10 "reviewer's request" sites (methodology.tex:460; results.tex:192, 194, 326, 511, 566, 572, 602, 736, 1025) plus "(R3-01)" at :194 and "(R3-01)"/"(R3-02)" at :217. No reviewer asked for this framing. The R1 writing plans (`intake/processed/R3-01-02_ablation_writing_plan.md`, `R3-05-inspection_writing_plan.md`) added it as response-letter shorthand. Internal tracker IDs in a manuscript are always wrong. Apply Sebas's sites only; :192/:194/:217 sit inside Sam's open R2b-01 paragraph.
  - Final text (sites not covered by P-05/P-18/P-22):
    - methodology.tex `ssec:FSMBaseline`: "To address the reviewer's request for a finite state machine (FSM) baseline under identical experimental conditions," → "\revblue{To provide a finite state machine (FSM) baseline under identical experimental conditions,}"
    - results.tex :566: "To directly address the reviewer's request for inspection-oriented task indicators, \revblue{the platform was evaluated" → "\revblue{To obtain inspection-oriented task indicators, the platform was evaluated" (keep the rest of the existing revblue).
    - :572: "(Table~\ref{tab:inspection_metrics}), directly addressing the reviewer's request for target tracking accuracy: the BG" → "(Table~\ref{tab:inspection_metrics}): the BG"
    - :602: "This experiment also provides quantitative evidence responding to the reviewer's request for autonomous re-planning after obstacle blockage:" → "\revblue{This experiment also quantifies re-routing after obstacle blockage:}"
    - :736: "; to directly address the reviewer's request for an onboard deployment analysis, the same forward pass" → "; the same forward pass"
  - Note to Sam (R2b-01): please remove ", directly addressing the reviewer's request … (R3-01)", "(R3-01)", "(R3-02)" and the "To directly address the reviewer's request for an ablation analysis … and a quantitative comparison against simple threshold-based decision logic," opener when you edit that paragraph.

- **P-02 — ACCEPT-MODIFIED**
  - Verification: the deleted sentences are covered as claimed. "flat, rough, and inclined" → the "On irregular surfaces…" paragraph. Goal prioritization → paragraph 3. Sim + physical → paragraph 1. Future-work signpost → the Limitations-pointer paragraph ("consolidated below"). "power-plant monitoring" appears only here, but it is aspirational filler. C-26 merged the two closing paragraphs into this one but did not lock its wording. One objection: the proposal swaps R2b-04's deliberately weakened "can be taken for such resource-constrained platforms" (`patches/r2b-04-hardware-spec.tex`: "'executed on such resource-constrained platforms' -> qualified") for "are feasible for", which brings back the implied onboard claim. Keep the R2b-04 wording.
  - Final text (replaces the whole paragraph): "The findings show that lightweight, bio-inspired neural networks ---arbitrating between locomotion modes and reactive behaviors driven by visual and inertial cues--- can manage multimodal gait transitions \revblue{on a real robotic platform, with the neural circuits executed on an external computer}. The perception-decision pipeline additionally retained task-level performance under combined IMU-drift and LiDAR-noise perturbation, and, conditionally on the scenario, camera illumination distortion (Section~\ref{ssec:NoiseRobustnessEval}), evaluated jointly rather than as isolated single-sensor degradations. \revblue{Although the physical prototype displays hardware-level boundaries (Section~\ref{ssec:Limitations}),} these results substantiate that complex, multi-stimulus mobility decisions can be \revblue{taken for such resource-constrained platforms; onboard feasibility was assessed only for the MLP terrain classifier on the ESP32-S3 (Section~\ref{sssec:mlp_eval}), not for the full neural pipeline}."

- **P-03 — DEFER-TO-OWNER (Sam R2b-01 prose; Deivi R3b-02 caption)**
  - Verification: the duplication is real. Every Roll/Pitch % and p-value at results.tex:215 also appears word for word in `fig:ablation_combined` caption (b), and R3b-01 already flagged this pair. Critic's view on merit: trim the prose, not the caption. R3b-02 asks this caption to explain the variants and the sample size, and the caption's no-conflict sentence keeps it self-contained.
  - Note to Sam: the prose Roll/Pitch block can shrink to the proposed pointer sentence. Note to Deivi: keep the caption's "(not shown) … $p=1.000$" sentence.

- **P-04 — ACCEPT**
  - Verification: the three paragraphs exist (methodology.tex after `eq:L4`). The sector roles of $L_0$–$L_3$ are in "Additionally, directional groups were defined…", $L_4$ is in "stored in the accumulator neuron $L_4$", and "fixed uniform values" is in the Table-LiDAR notation. The replacement keeps every symbol ($Z_i$, $I_n$, $R_n$, $A_n$, $i,j,r$, the three $W$ matrices). Wrap the replacement in `\revblue{}`. (Unrelated: Eq. `eq:L4` sums over $r$ but its summand is $A_n$, an existing notation slip. Not part of this cut; flag it to the authors.)

- **P-05 — ACCEPT**
  - Verification: both the opener and the `\paragraph{Stability metrics.}` text say "Quadrupedal Walking gait and all six pairwise transitions" (results.tex:326–339). The definitions stay pointed at `sssec:variable_topo_quant`. Afterwards, update OUTLINE.md:213, which quotes the deleted "To address the reviewer's request…" sentence.

- **P-06 — ACCEPT**
  - Verification: the `fig:transition_phases` caption covers the double-headed arrow and the per-mode ranges. $N_{\mathrm{total}} = 979$ is still stated earlier in the same paragraph block and in the instantaneous-reading caveat. "Non-degenerate" follows from the all-four-feet sentence just before it. Dropping "regardless of the chassis velocity" is fine, because "does not require the robot to halt" stays. Do not touch the "$1.36^\circ$" bound while editing; see S-05.

- **P-07 — ACCEPT-MODIFIED (subcaption part DEFER-TO-OWNER: Deivi)**
  - Rebuttal: the proposal deletes the prose sentence and also the subcaption's "terrain-specialized locomotive signature" clause, and it cites each as the copy that survives the other's removal. If both go, the paragraph's only interpretive claim ("distinct, repeatable, terrain-specialized posture … rather than a generic, environment-agnostic control law") disappears from the paper. Keep a shortened prose version. The subcaption trim is a separate decision for Deivi's R2b-05/R3b-04 caption sweep.
  - Final text: opening → "\revblue{The steady-state kinematics of both terrains were mapped onto a Roll RMS ($\phi_{\text{RMS}}$) vs.\ Pitch RMS ($\theta_{\text{RMS}}$) phase space across all 30 successful trials (Figure~\ref{fig:terrain_adaptability}).}". Last sentence ("The Pitch-RMS separation between both domains provides empirical evidence … rather than being terrain-specific.") → "\revblue{The Pitch-RMS separation indicates that the network selects a distinct, repeatable posture for each terrain rather than applying an environment-agnostic control law.}" (the Roll-overlap reading stays in the subcaption).

- **P-08 — ACCEPT**
  - Verification: subcaption (a) has "aligned around the neural mode-switch instant ($t = 0.0\,\text{s}$)", "15 independent trials" and "No trial violated this limit across all 30 runs", and main caption (A) has "aligned at the mode-switch instant". The $TR = 1 - SM/r_{in}$ definition and the 0.0/1.0 interpretation stay. Dropping "under stochastic noise conditions" is a good thing, because that phrase is the S-02 contradiction. Rewritten sentences go in `\revblue{}`.

- **P-09 — ACCEPT**
  - Verification: results.tex:490–497 has both claims (no Gazebo power plugin; physical energy characterized elsewhere). `ssec:QuantReal` exists and holds the energy figure and table. The dropped "per-motor current" wording is also less accurate than the caption's single INA current sensor ("current sampled … by the onboard INA sensor"). Use `\revblue{}`.

- **P-10 — ACCEPT-MODIFIED (the "every retained trial" consolidation DEFER-TO-OWNER: Diego, R2b-02)**
  - Rebuttal: the proposed consolidation sentence ("three successful trials were retained at every level; discarded attempts are analyzed in…") is a substantive reframing of the noise-sweep result claims. It is arguably more honest, but it falls under R2b-02's main-text noise-caveat scope, and `tab:consolidated_simulation_metrics` reports "100.0\%" for the same suites, so the two must be reconciled together. Apply only the filler deletions now.
  - Final text: Aversive, delete ", demonstrating the efficiency of the neural gating mechanism" (sentence ends "…leaves the field of view."). Obstacle, "The sensory-locomotor coupling is precise: neural firing variance stays" → "Neural firing variance stays". Complex, "The complex navigation suite culminates the simulation validation, presenting the obstacle" → "The complex navigation suite presents the obstacle".
  - Note to Diego: four per-paragraph "every retained trial … succeeded" sentences read as 100% robustness; the proposer's single honest sentence is worth considering inside R2b-02.

- **P-11 — ACCEPT**
  - Verification: AUC 0.864 stays in the test-set sentence, in subcaption (b) and in the `fig:mlp_eval_grid` main caption. LR F1 = 0.692 stays in the benchmark paragraph. "resource-constrained embedded microcontroller" stays in the R2b-04 revblue clause. Every subfigure of `fig:mlp_eval_grid` / `fig:classifier_tradeoff` keeps an in-text citation (a, b, c, d; a, b, c). Rewritten connectives go in `\revblue{}`.

- **P-12 — ACCEPT-MODIFIED**
  - Verification: (2) and (3) hold. Limitations' last paragraph does say these constraints "are established alongside that experiment's own results … and are not restated here", so the three pointers are circular. On (1): C-41 deliberately kept the BG/WTA sentence. Methodology now says the same about evasion, but "integrates LiDAR and camera information in real time" appears only here, and the BG/WTA acronym is introduced here. Keep both.
  - Final text for (1): replace the first two sentences with "\revblue{As described in Section~\ref{ssec:Gazebo_Simulation}, behavior in this task is purely reactive (no map, no spatial memory); re-routing emerges from the basal-ganglia/winner-take-all (BG/WTA) arbitration network integrating LiDAR and camera input in real time.}"

- **P-13 — ACCEPT-MODIFIED (prose only; caption REJECTED)**
  - Rebuttal: the caption's "FSM never needs a retry at any level in any of the three panels (flat at $1.0$)" is the only place the caption describes the FSM line in the Appetitive/Aversive panels, and the caption should stay self-contained. The prose "(not a success rate)" belongs to C-55's explicit author request to keep the two metrics apart, so keep it. Applying the proposal literally would also put two colons in one sentence.
  - Final text: "The two controllers diverge, however, in how often that retry is needed: the FSM never requires one, at any noise level, while the Neural system occasionally does as noise increases. Figure~\ref{fig:attempts_vs_noise_level} makes this explicit with its own metric, attempts needed per completed mission (not a success rate) ---" → "\revblue{The two controllers diverge, however, in how often that retry is needed (Figure~\ref{fig:attempts_vs_noise_level}; attempts needed per completed mission, not a success rate):}" followed by the existing "Neural needs up to $1.67\times$ … while FSM stays at exactly one attempt throughout."

- **P-14 — ACCEPT-MODIFIED (prose only; caption parts DEFER-TO-OWNER: Deivi)**
  - Verification: the Aversive paragraph states the reflex/bypass mechanism ("bypasses heavy trajectory filtering"), so prose (1) and (2) are safe as proposed (wrap in `\revblue{}`). Caption trims fall under R2b-05/R3b-04. Note to Deivi: "volumetric geometric input" in the `fig:obstacle_real_compound` caption is also part of S-07.

- **P-15 — DEFER-TO-OWNER (Deivi, R2b-05/R3b-04)**
  - Verification: the duplication claim holds (subcaption (b) already says $T_{\text{response}}$ is not plotted, and "Together, these three profiles…" carries no information). Note to Deivi: the proposed text is a good base, but drop "under stochastic variable-topography conditions" regardless (S-02), and add the simulation label your sweep requires.

- **P-16 — ACCEPT-MODIFIED**
  - Verification: the CPG row of `table:action_selection_comparison` says "feedback-modulated variants also arbitrate transitions" with `Fukui2019VestibularCPG,Owaki2017SpontaneousGait`. The later paragraph repeats the arbitration point with the same two citations. C-14 reduced this sentence to "literature fact + forward pointer". Removing the fact here is consistent with that, but "from vestibular or load feedback" exists only in this sentence. Keep that phrase.
  - Final text (replaces "Table~\ref{table:action_selection_comparison} summarizes this landscape … alongside the CPG description itself."): "\revblue{Table~\ref{table:action_selection_comparison} contrasts these approaches with central pattern generators (CPGs) ---including feedback-modulated variants that trigger gait transitions from vestibular or load feedback--- and with the basal-ganglia winner-take-all arbitration adopted here.}"

- **P-17 — ACCEPT-MODIFIED**
  - Verification: `grep` confirms that `eq:NakaImu`/`eq:NakaMode` are referenced only inside the paragraph that introduces them (methodology.tex:323), so no `\eqref` breaks. Eqs. Z0–Z16 use `f_{Imu}`/`f_{Mode}`, which the replacement still defines. Keep the where-clause "$x_+ = \max(x,0)$ is the rectified input;". The other rectifier definition sits two subsubsections earlier, in different notation ($(x)_+$ vs. $x_+$), and keeping this one costs 7 words.
  - Final text: lead-in sentence → "The general form is given in Equation~\eqref{eq:Naka}." (drop ", where $(\cdot)_+$ denotes the rectified (positive-part) operator"). Replace the "Based on this general formulation…" paragraph and both equation environments with "\revblue{Two instantiations of Equation~\eqref{eq:Naka} are used, $f_{\mathrm{Imu}}(x) = f(x;\sigma_I)$ and $f_{\mathrm{Mode}}(x) = f(x;\sigma_M)$, whose different half-saturation constants match the dynamic range of the IMU and mode-selection pathways.}"

- **P-18 — ACCEPT**
  - Verification: methodology `ssec:FSMBaseline` already states "same seven simulated suites under matching trial counts, noise levels, and success criteria". The λ definition is kept, and the caption (Diego R2b-03) and the timing-fairness paragraph are not touched. Wrap in `\revblue{}`.

- **P-19 — ACCEPT**
  - Verification: the four segments and "15 continuous repetitive trials" are in the sentence immediately before. N = 15 is in both the `tab:terrain_sequence` and `fig:real_variable_topography_sequence` captions, and "observed across all 15 trials" stays. The cut also drops "enforced by the bio-inspired basal-ganglia controller", which wrongly credits gait switching to the BG rather than the gait-decision module. Wrap in `\revblue{}`.

- **P-20 — ACCEPT**
  - Verification: all four stages, the MLP, `\citet{Grajales_Des_2025}` and the sim-as-baseline decision are kept, and the three `\ref` targets exist. Wrap in `\revblue{}`.

- **P-21 — ACCEPT**
  - Verification: "low-torque servomotors" and "lightweight" each appear twice in the opening paragraph (results.tex:1065). "to contextualize the simulation within its intended inspection application domain" is at results.tex:10. The "used for obstacle-evasion and stimulus-response experiments" detail that goes is also in the `fig:depot_simulation` caption. R2-01 explicitly asked to shorten the warehouse material. All caveats survive. Wrap the rewrites in `\revblue{}`.

- **P-22 — ACCEPT-MODIFIED**
  - Verification: the "pooled intra-segment … coupling window excluded" description is in the `tab:mode_steady_state_energy` caption word for word, and the R3b-05 battery/sampling text is untouched. Keep the phrase "long-term average", which is R2-04's own requirement wording and matches the table caption.
  - Final text: (1) as proposed. (2) last sentence → "\revblue{Table~\ref{tab:mode_steady_state_energy} reports the long-term average steady-state power draw of each mode.}"

- **P-23 — ACCEPT-MODIFIED (methodology parts and the physical-figure merge only)**
  - Rebuttal, caption fragment: REJECT. `grep "ref{fig:mode_timeline_complex}"` finds exactly one citation of that figure in the whole paper: the `fig:mode_timeline_inspection` caption fragment the proposal wants to delete. C-43 deliberately reduced that caption to this cross-reference. Deleting it would leave `fig:mode_timeline_complex` uncited. (Pre-existing gap worth fixing separately: that figure is never cited from prose. The Complex paragraph of `sssec:fsm_baseline_comparison` is the natural place.)
  - Rebuttal, simulated `GRAPH_IMU2` sentence: REJECT the deletion. "In Figure~\ref{fig:GRAPH_IMU2}…" is the only in-text citation of panel (b) of `fig:graph_imu_pair` (the parent label is never `\ref`'d). Keep it.
  - Accepted: the methodology template-sentence trims (stn–str, Z3–Z17 → keep the $HI$ sentence, Z0–Z16, Z0V2 → "\revblue{Equations~\eqref{eq:Z0V2}–\eqref{eq:Z16V2} give the modified units (thresholds in Table~\ref{table:Locom_MLP}).}"). `table:Ganglia` stays cited in the where-clause and `table:Locom_NN` in several places. Also accepted: merging the two physical "In Figure…, the activations of the MLP outputs…" sentences into "\revblue{MLP outputs and stagnation state for both scenarios are shown in Figure~\ref{fig:graph_imu_real_pair}.}" at the end of the second paragraph.

- **P-24 — REJECT**
  - Rebuttal: C-15 deliberately put traceable numbers here to replace the untraceable "47 ms", and the proposer concedes this. The real problem with the sentence is not redundancy but S-04/S-09: it presents terrain-mode-transition latencies (184–534 ms, `fig:FourPanelLatencies`) as evidence of conflict-resolution speed and says they are "well within real-time constraints on resource-constrained embedded hardware", although per R2b-04 the circuits ran on the laptop. The proposed replacement keeps the misattribution and only hides the numbers. Fix it when S-04/S-09 are resolved, not as a cut.

- **P-25 — DEFER-TO-OWNER (Diego, R2b-02/R3b-03)**
  - Verification: the double "jointly rather than isolated per sensor --- no configuration … in isolation" is real (results.tex Limitations, 4th paragraph). This is the noise caveat that R2b-02/R3b-03 reviewers asked to make more prominent, so its wording belongs to Diego. Note to Diego: one statement of "applied jointly: no configuration isolates a single sensor's degradation" is enough.

- **P-26 — ACCEPT-MODIFIED**
  - Verification: `ssec:HardwareSpec` prose and `table:HardwareParams` ("Off-board computing platform … serial link to the robot") cover the deleted detail. R2b-04's reviewer was specifically confused about where computation happens, so Limitations should still name the laptop explicitly, not just say "off-board".
  - Final text: in `sssec:mlp_eval`, keep "\revblue{, the external laptop described in Section~\ref{ssec:HardwareSpec}}" and drop ", which also ran the neural circuits during the physical experiments". In Limitations, replace the first sentence with "\revblue{Regarding the computing platform: the neural circuits, the MLP terrain classifier, and the image processing ran on the external laptop of Section~\ref{ssec:HardwareSpec}, not on the robot's ESP32-S3.}" Keep the onboard-feasibility sentence.

- **P-27 — ACCEPT-MODIFIED**
  - Verification: "within twenty degrees of the center of the visual field … inhibitory thresholds" precedes Eqs. Z_5/Z_6, so the where-clause 20° clause is a duplicate. Delete it, and delete the rectifier's second sentence ("This ensures that only nonnegative inputs…"). For the Gait-Decision repeats, follow P-17: delete only the lead-in "(·)_+" clause and keep the where-clause $x_+$ definition.

- **P-28 — ACCEPT**
  - Verification: $N_0$/$N_1$/$N_2$ are defined in "The ninth position includes a binary value…" three short paragraphs above. The $U_{N_0}$/$U_{N_1}$ definition stays in the where-clause, which R3b-01 relies on. The R3b-01 requirement is itself "condense repeated metric definitions". Wrap the rewrites in `\revblue{}`.

- **P-29 — ACCEPT-MODIFIED**
  - Verification: the Locomotion-rationale and Gazebo closers carry no facts. Also, "before its embedded physical implementation" (Gazebo closer) is another R2b-04-inconsistent "embedded" claim, which is one more reason to delete it. But the ServoCompensation "Together…" sentence is the explicit statement that answers R3-03 (control/compensation strategies for low-torque servos), and "This layered strategy" on its own would refer to nothing. Keep a short synthesis.
  - Final text: delete the two closers as proposed; "the multi-body physical simulations were strictly restricted" → "simulations were restricted". ServoCompensation: "Together, this layered strategy --- static stability by gait design, torque-aware trajectory shaping, and feed-forward compliance correction --- constitutes the compensating control approach for the platform's low-torque, open-loop actuation constraints. It does not substitute for" → "\revblue{Together, these measures compensate for the platform's low-torque, open-loop actuation but do not substitute for}" (the rest of the sentence and its `\ref{ssec:Limitations}` stay).

- **P-30 — ACCEPT**
  - Verification: `ssec:Platform_Design` has "The camera captures visual stimuli…, the LiDAR provides information regarding the presence and position of obstacles". The QuantReal intro keeps the one `tab:consolidated_physical_metrics` pointer that C-14 moved there, and N = 3 replicates is kept. The results roadmap is also in the Introduction's last paragraph. Wrap in `\revblue{}`.

### Inconsistency checks (S-01..S-08, plus critic additions)

- **S-01 — CONFIRMED.** "Both ECDF distributions collapsed into a perfect Heaviside step function" (variable_topo_quant latency paragraph) vs. "remaining 2 trials … long tail out to $\approx 0.6\,\text{s}$" and "five-to-six-step staircase rather than collapsing onto a single value" two sentences later. Also, the ECDF plots $T_{switch}$ only; $T_{response}$ is explicitly "not plotted". Text-only fix: delete the clause and start with "The neural latency was…".
- **S-02 — CONFIRMED (the resolution NEEDS-AUTHOR).** "under stochastic noise conditions" (TR paragraph), "filtered out the injected sensor noise" (latency paragraph) and the `fig:variable_topo_metrics` caption's "under stochastic variable-topography conditions" vs. `sssec:noise_robustness_extra`: "a separate battery from the unperturbed Rugged Terrain/Inclined Slope trials analyzed in Section~\ref{sssec:variable_topo_quant}". Check: the noise level configured for the 30 variable-topography trials behind FigA/B/C (`experiments/N-01-simulation-figure-regeneration/` / `experiments/simulation/` trial configs). P-08 already drops one instance.
- **S-03 — CONFIRMED.** Limitations: "system resilience was also not assessed under partial hardware failures or temporary sensory dropout conditions" vs. `fig:camera_dropout_evidence` / methodology "a probabilistic detection dropout" in the illumination model. Text-only fix: qualify it, e.g. "temporary sensory dropout beyond the simulated camera-detection dropout of Section~\ref{sssec:noise_robustness_extra}".
- **S-04 — CONFIRMED.** Conclusions: "In scenarios presenting simultaneous appetitive and aversive stimuli, … this behavior yielded direction-switching neural latencies of 184--534~ms (Figure~\ref{fig:FourPanelLatencies})" vs. the figure, which shows Quadrupedal↔Differential Rolling terrain transitions on a "continuous multi-terrain navigation mission". C-36 chose this range only for traceability. The only conflict-decision latency in the paper is the ablation's full-circuit "$75.9$~ms, 95\%~CI $[59.3, 92.6]$" (simulation, Complex Navigation). Fix by citing that number or by re-attributing 184–534 ms to terrain-mode transitions. No new data is needed.
- **S-05 — CONFIRMED (Roll); Pitch NEEDS-AUTHOR.** "these values remain below $1.36^\circ$ and $6.95^\circ$ respectively across all tested conditions" vs. `tab:consolidated_simulation_metrics` Obstacle Roll "1.55 $\pm$ 0.15", the variable-topography means $\mu_{\phi} \approx 1.59^{\circ}$/$1.47^{\circ}$, and FSM-table Rugged Terrain Neural Roll 1.827. Nothing in the cited table or figure gives 6.95° (the largest pitch value is Inclined Slope 6.751 ± 7.160 in `tab:fsm_comparison`, a different table). Check where 1.36/6.95 came from (1.36 = Aversive Roll only).
- **S-06 — CONFIRMED (which mode is correct NEEDS-AUTHOR + code check).** Simulated slope: "However, due to the slope, the platform adopts the differential rolling mode" vs. a few lines later "neuron $X_{1}$---associated with detecting an inclination greater than five degrees---excites unit $X_{15}$, issuing the command to transform into quadrupedal mode". The equations side with rolling: $z_1 = f_{Imu}(Roll - U_{Roll})$ with $U_{Roll}=15$ (not 5°, and roll, not inclination), and $z_1$/$z_2$ feed $z_{16}$ ("$+ 0.7z_1 + 0.7z_2$", $X_{16}$ = differential rolling), not $z_{15}$. Additional physical-side conflicts: "neuron $X_{14}$, which commands the robot to climb the ramp using the differential rolling mode" ($X_{14}$ = omnidirectional everywhere else). `tab:terrain_sequence` Frame 1 "Double-ramp ascent & Quadrupedal Walking" vs. the `fig:FourPanelLatencies` prose "forced the robot from Quadrupedal to Differential Rolling Mode to climb a steep incline". Conclusions: "On irregular surfaces and steep slopes … transition from H-mode to quadrupedal mode". Check the gait-decision code / physical logs for the slope mode and which unit drives it.
- **S-07 — CONFIRMED (the mechanism NEEDS-AUTHOR).** Appetitive: "the basal ganglia network---which operates at the microsecond scale" vs. `fig:FourPanelLatencies` ("The basal ganglia loop's decision latency", 0.184/0.534 s). Obstacle: "the volumetric obstacle flooding the camera sensor with spatial and depth data", and Complex: "the physical barrier's high spatial density flooding the camera sensor", vs. `table:HardwareParams` (Logitech C270, no depth channel; obstacles via LDROBOT STL-19P LiDAR). The authors must say what actually drives the $Var(z)$ spike on the physical robot. (Also: "3D-printed actuators" in the Appetitive paragraph; the actuators are MG996R servos, and only the structure is PLA.)
- **S-08 — CONFIRMED, DEFER-TO-OWNER (Diego, R2b-03).** Methodology: "any behavioral difference between them is attributable exclusively to this mode-selection mechanism, not to differences in perception, low-level navigation, or experimental configuration" vs. results: "three configuration differences from the basal-ganglia code's terrain-transition logic (the pitch-instability threshold, a transition timing offset, and the switching-time formula's margin term)". Suggested scope fix: "exclusively", except on the two terrain suites (see Section~\ref{sssec:fsm_baseline_comparison}).
- **S-09 (critic) — CONFIRMED.** Leftover "embedded hardware" claims that contradict R2b-04 ("executed on that external laptop … not on the robot itself"). Methodology BG paragraph: "--- well within real-time constraints on resource-constrained embedded hardware". Limitations paragraph 1: "a highly efficient basal-ganglia inspired arbitration network capable of managing multimodal mobility on resource-constrained embedded hardware". Gazebo closer: "before its embedded physical implementation" (removed by P-29). Sebas, R2b-04 follow-up.
- **S-10 (critic) — CONFIRMED.** `fig:mode_timeline_complex` has no prose citation. Its only `\ref` is inside another figure's caption (`fig:mode_timeline_inspection`). Add one in the Complex-suite paragraph of `sssec:fsm_baseline_comparison`.

## Surviving changes

ACCEPT: P-04, P-05, P-06, P-08, P-09, P-11, P-18, P-19, P-20, P-21, P-28, P-30.
ACCEPT-MODIFIED (apply the critic's final text, not the proposer's): P-01 (Sebas sites only), P-02, P-07 (prose
only), P-10 (filler only), P-12, P-13 (prose only), P-14 (prose only), P-16, P-17, P-22, P-23 (no caption
fragment, keep GRAPH_IMU2 sentence), P-26, P-27, P-29.
REJECT: P-24.

## Deferred to owners

- **Sam (R2b-01):** P-01 ablation sites (results.tex:192/194/217, including "(R3-01)"/"(R3-02)"), P-03 prose.
- **Deivi (R3b-02, R2b-05/R3b-04):** P-03 caption (keep it), P-07 subcaption clause, P-14 caption trims, P-15.
- **Diego (R2b-02/R3b-03, R2b-03):** P-10 "every retained trial" consolidation, P-25, S-08.

## Inconsistencies

Confirmed: S-01, S-03, S-04, S-05 (Roll), S-06, S-07, S-08, S-09, S-10. Confirmed text conflict whose
resolution needs a data/code check: S-02 (variable-topography noise level), S-05 Pitch (source of 6.95°),
S-06 (actual slope mode / driving unit), S-07 (driver of the physical $Var(z)$ spike).
