"""Regenerates the 5 simulation raster figures covered by N-06/N-08: NEU_EST_UNIB/UNIG/MUL.png
(F-01) and NEU_IMU/NEU_IMU2.png (F-01 vectorized branch), using the shared `build_neu_est`/
`build_neu_imu` builders in `experiments/_plotting/builders/imu_terrain_real.py`.

Why this script exists (2026-08-29): the first pass that produced these 5 files was run ad hoc --
no script was saved, so the output wasn't reproducible from source, and (found during R02-01-05's
frame-by-frame review) it also dropped the a)/b)/c)/d) panel-letter annotations that `results.tex`
cites by letter for NEU_EST_UNIG/NEU_EST_MUL/NEU_IMU2 (\\ref{fig:NEU_EST_UNIG}b,
\\ref{fig:NEU_EST_MUL}a-d, \\ref{fig:NEU_IMU2}a/b), and reordered NEU_EST_MUL's 4 module-groups
(swapping Lidar Network and Locomotion). This script is the fix: it explicitly orders each
figure's panels to match what the prose already cites, and passes `group_letters` so the builder
draws the correct letter under each group. See intake/pending/
R02-01-05_simulacion_grupo2_vectorizacion.md §0ter for the full diagnosis.

Letter-to-content mapping restored (matches the pre-existing 2x2-grid original, and matches
results.tex's citations):
  NEU_EST_UNIB: a=Locomotion Module, b=Gait Decision Module
  NEU_EST_UNIG: a=Lidar Network Module, b=Locomotion Module, c=Gait Decision Module
  NEU_EST_MUL:  a=Basal Ganglia Module, b=Lidar Network Module, c=Locomotion Module,
                d=Gait Decision Module
  NEU_IMU / NEU_IMU2: a=Locomotion Module, b=Gait Decision Module
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "_plotting"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "_plotting", "builders"))
from builders.imu_terrain_real import build_neu_est, build_neu_imu  # noqa: E402

VEC = "experiments/_plotting/vectorized"
OUT = "experiments/N-01-simulation-figure-regeneration/output"


def main():
    os.makedirs(OUT, exist_ok=True)

    build_neu_est(
        f"{VEC}/neu_est_unib.csv", f"{OUT}/NEU_EST_UNIB.png",
        panels=["Locomotion_1", "Locomotion_2", "Decision_1", "Decision_2"],
        group_titles={"Locomotion_1": "Locomotion Module", "Decision_1": "Gait Decision Module"},
        group_letters={"Locomotion_1": "a", "Decision_1": "b"},
    )

    build_neu_est(
        f"{VEC}/neu_est_unig.csv", f"{OUT}/NEU_EST_UNIG.png",
        panels=["Lidar", "Input", "Response", "Auxiliary", "Locomotion_1", "Locomotion_2",
                "Decision_1", "Decision_2"],
        group_titles={"Lidar": "Lidar Network Module", "Locomotion_1": "Locomotion Module",
                      "Decision_1": "Gait Decision Module"},
        group_letters={"Lidar": "a", "Locomotion_1": "b", "Decision_1": "c"},
    )

    # NOTE the panel order here: Lidar (b) comes BEFORE Locomotion (c) -- this is the fix for
    # the group-swap bug found in R02-01-05 §0ter, restoring the order the a-d letters assume.
    build_neu_est(
        f"{VEC}/neu_est_mul.csv", f"{OUT}/NEU_EST_MUL.png",
        panels=["BasalGanglia_GPi", "BasalGanglia_GPe", "BasalGanglia_STN", "BasalGanglia_STR",
                "Lidar", "Input", "Response", "Auxiliary",
                "Locomotion_1", "Locomotion_2",
                "Decision_1", "Decision_2"],
        group_titles={"BasalGanglia_GPi": "Basal Ganglia Module", "Lidar": "Lidar Network Module",
                      "Locomotion_1": "Locomotion Module", "Decision_1": "Gait Decision Module"},
        group_letters={"BasalGanglia_GPi": "a", "Lidar": "b", "Locomotion_1": "c", "Decision_1": "d"},
    )

    # C-53: "Locomotion_2" (neuron X17) dropped from both panels below -- verified against this
    # same CSV that X17 is tonically active near-constant ~0.5 the whole trial (not silent), but
    # carries no interpretable temporal variation for the reader. See
    # redundancy_closing_audit_consolidation_2026-09-02.md, finding [FIG-X17].
    build_neu_imu(f"{VEC}/neu_imu.csv", f"{OUT}/NEU_IMU.png",
                   group_letters={"Locomotion_1": "a", "Decision_1": "b"},
                   panels=["Locomotion_1", "Decision_1", "Decision_2"])
    build_neu_imu(f"{VEC}/neu_imu2.csv", f"{OUT}/NEU_IMU2.png",
                   group_letters={"Locomotion_1": "a", "Decision_1": "b"},
                   panels=["Locomotion_1", "Decision_1", "Decision_2"])

    print(f"Wrote NEU_EST_UNIB/UNIG/MUL.png and NEU_IMU/NEU_IMU2.png to {OUT}")


if __name__ == "__main__":
    main()
