## Technical Summary: Architecture & Pipeline Overview

### 1. Core Challenge & Technical Requirements

* **Journal & Deadline:** Major revision for *Robotics and Autonomous Systems* (Manuscript `ROBOT-D-26-00122R1`). Resubmission deadline is **Agust 31, 2026** (7 days).
* **Reviewer Requirements Breakdown:**
* **Reviewer 2 (Streamlining & Minor Additions):**
* Heavily condense repetitive text, remove duplicate neural raster plots/identical stability curves between simulation and hardware tests, merge metric definitions, and shorten the symbolic warehouse simulation section.
* Add Finite State Machine (FSM) gait arbitration baseline comparisons.
* Consolidate all limitations into a dedicated section.
* Add multi-mode long-term average energy consumption data and onboard MLP computing overhead analysis.


* **Reviewer 3 (Major Structural & Experimental Additions - High Priority):**
* Conduct explicit ablation analysis on the basal ganglia arbitration network.
* Perform comparative tests removing key neural layers or inhibitory connections to justify the Winner-Take-All (WTA) mechanism over threshold logic.
* Supplement control strategies or compensation algorithms for low-torque servo constraints and open-loop gait instability.
* Design perception-decision noise robustness experiments (IMU drift, LiDAR noise, camera illumination distortion).
* Add inspection task performance metrics (target tracking accuracy, coverage rate, autonomous re-planning).
* Revise the literature review with horizontal comparative tables contrasting Basal Ganglia, CPG, and RL-based action selection algorithms.





---

### 2. Team Workflow & System Constraints

* **Source Format:** The entire manuscript exists as a single monolithic `.tex` file on Overleaf.
* **Team Operations:** Co-authors and professors operate exclusively within the Overleaf web interface without Git usage, branches, or standardized commit discipline.
* **Structural Variability:** Edits in Overleaf involve arbitrary line additions, text reordering, section movement, and block deletions.

---

### 3. Hybrid Automation Pipeline (Local Git + AI Agent)

To manage these constraints without imposing Git overhead on non-technical team members:

```
[Overleaf Monolithic File] ──(Manual Export)──> [Local Repository Source]
                                                         │
                                               (Git Diff Tracking)
                                                         │
                                                         ▼
                                             [Upward-Scanning Script]
                                                         │
                                                         ▼
                                            [AI Agent Section Patching]
                                                         │
                                                         ▼
                                             [Monolithic Reassembly]
                                                         │
                                                         ▼
                                            [Paste Back to Overleaf]

```

* **Version Isolation:** The master repository is maintained locally by you. The Overleaf file is exported periodically as a monolithic `.tex` document.
* **Upward-Scanning Logic:** Local scripts inspect `git diff` output to isolate line shifts, scanning upward from altered lines to locate parent `\section{...}` headers.
* **AI Ambiguity Resolution:** Rather than relying on rigid syntax parsers, the AI agent evaluates structural deltas (distinguishing moved sections from added/deleted ones) and generates precise LaTeX patch blocks corresponding to Reviewer 2 and 3 mandates.

---

## Repository Setup & Execution Guide

The following steps establish your local repository, track changes against Overleaf exports, and prepare the workspace for automated section updates.

### Step 1: Initialize the Local Directory & Git Tracking

Run the following commands in your local terminal:

```bash
# Create project folder and step inside
mkdir paper-revision
cd paper-revision

# Initialize Git repository
git init
git branch -M main

# Build file structure for exports, modules, and scripts
mkdir -p source sections patches scripts

```

---

### Step 2: Configure Git Ignore & Add Initial Monolithic File

1. Download the current monolithic `.tex` file directly from Overleaf.
2. Place the file into `source/` and name it `main_monolithic.tex`.
3. Create a `.gitignore` file to filter compilation logs:

```bash
cat << 'EOF' > .gitignore
*.aux
*.log
*.out
*.toc
*.bbl
*.blg
*.pdf
*.synctex.gz
EOF

```

4. Stage and commit the baseline manuscript:

```bash
git add .
git commit -m "chore: initial baseline commit of monolithic paper from Overleaf"

```

---

### Step 3: Link to Remote GitHub Repository

1. Create a new **Private** repository on GitHub named `paper-revision` (do not initialize with a README or license).
2. Link your local repository and push:

```bash
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/paper-revision.git
git push -u origin main

```

---

### Step 4: Daily Synchronized Revision Loop

Follow this procedure every time a co-author completes edits on Overleaf or when applying AI revisions:

1. **Fetch Latest File:** Download `main.tex` from Overleaf and overwrite `source/main_monolithic.tex`.
2. **Review Diff:** Check changes made by teammates using:
```bash
git diff source/main_monolithic.tex

```


3. **Commit State:** Commit the downloaded snapshot to maintain a clear line-history:
```bash
git add source/main_monolithic.tex
git commit -m "sync: updated monolithic file from Overleaf edits"
git push origin main

```


4. **Isolate & Patch:** Extract the target section (e.g., `03_related_work.tex` or `05_experiments.tex`), pass the snippet to the AI agent along with the reviewer requirement, and paste the generated LaTeX code directly back into `source/main_monolithic.tex` before copying to Overleaf.