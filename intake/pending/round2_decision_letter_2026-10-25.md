# Round 2 decision letter — ROBOT-D-26-00122R2 (verbatim reviewer text)

Source: Editorial Manager email "Decision on submission to Robotics and Autonomous Systems", sent
2026-10-25 by Receiving Editor Maria Gini, forwarded to the team the same day (Gmail, read 2026-10-28).
Decision: minor revision, resubmit by **2026-11-04**. Reference copy of the reviewers' exact wording, so
`R2b-xx`/`R3b-xx` rows (README §6.1) can be checked against it instead of against their short summaries.

**Editor:** this is the last round of revisions. Please address the comments from the reviewers.

## Reviewer #2

The authors have substantially addressed most major concerns raised in the previous round, with supplementary ablation, baseline comparison, noise‑robustness and practical inspection‑task experiments. Several clarifications on experimental boundaries, figure captions, hardware documentation and manuscript organization are required prior to acceptance.

1) The ablation experiments rely on n=12 replicates per condition. Although statistical tests have been applied, the sample size is relatively limited for physical robot experiments. Please add an explicit statement in the corresponding results paragraph discussing this sample‑size limitation and note that larger‑scale repeated trials remain for future work. *(→ R2b-01)*

2) The noise‑robustness test injects IMU drift, LiDAR noise and camera illumination distortion "jointly at the same time", without isolating each sensor's individual contribution; furthermore only IMU drift is tested rather than IMU white noise. This caveat is mentioned in limitations, but should also be briefly noted within the main text results section for this experiment, not only buried in the Limitations subsection. Readers should be immediately aware when reading the noise‑robustness figures. *(→ R2b-02)*

3) The authors mention that some timing metrics cannot be fairly compared between the basal‑ganglia controller and FSM baseline due to internal parameter mismatches. This important fairness caveat is currently only in the main text prose. Please duplicate this note inside the "figure caption of FSM comparison plots", since reviewers/readers tend to read figure captions first. *(→ R2b-03)*

4) The manuscript heavily discusses the perception and bio‑inspired decision algorithm, yet key physical parameters of the real robot are scattered or missing. Please add a concise hardware‑parameter subsection: robot total mass, servo model, actuator specifications, onboard computing platform, battery parameters. This improves reproducibility of this physical‑robot work. *(→ R2b-04)*

5) Please ensure every experimental figure shows the number of trials N directly inside its caption, not only mentioned inside main‑text paragraphs. *(→ R2b-05)*

6) The current graphical abstract only illustrates the original sensing‑decision‑locomotion pipeline; it does "not reflect the key new contributions added in R2: ablation study, FSM baseline comparison, inspection‑oriented task experiments". Please revise graphical abstract and Highlights to align with updated manuscript contents. *(→ R2b-06)*

## Reviewer #3

This paper presents a multimodal wheel‑legged quadruped robot controlled by a basal‑ganglia‑inspired neural architecture to realize autonomous gait arbitration among walking, differential rolling and omnidirectional motion, and validates the system via both simulation and physical robot tests. Despite these contributions, several minor issues remain to be addressed:

1. Redundant descriptions and repeated metric definitions still exist in the main text. Please further condense duplicated statements and refer to consolidated tables instead of restating parameters repeatedly. *(→ R3b-01)*

2. The captions of ablation study figures lack essential experimental information. Add brief explanations for four circuit variants and sample size in figure captions for better self‑contained readability. *(→ R3b-02)*

3. The combined‑perturbation noise‑robustness test cannot separate individual sensor contributions. Add a short note in the corresponding figure caption to clarify this experimental limitation. *(→ R3b-03)*

4. Format styles are inconsistent between simulation and real‑robot plots. Unify font and legend styles, and mark clearly whether each plot comes from simulation or physical trials in captions. *(→ R3b-04)*

5. Supplement key background information in captions for the power‑consumption table and inspection‑task results, including battery specification and statistical rules for experimental samples. *(→ R3b-05)*
