# experiments/real/ — Manifest (Tarea 2, standardization pass, 2026-08-27)

Physical-robot test folders are **frozen** (per the author, 2026-08-27: no re-runs planned "hasta
que se determine lo contrario") — this manifest exists so the next pass (Tarea 3: regenerate every
physical-section figure) doesn't have to re-derive folder↔figure↔status from scratch every time.
Machine-readable twin: `manifest.json` (same rows, structured for scripts). Full analysis behind
every row: `intake/pending/R02-01_data_traceability_and_plotting_plan.md` §1.2/§2.

**Standardization applied this pass:** renamed every `imu_ina_<timestamp>.csv` to `imu_ina.csv`
and `pitch_latency_<timestamp>.csv` to `pitch_latency.csv` (timestamp is still recoverable from git
history / the original filename noted below) — one predictable filename per file type across all
folders, matching the convention already used by `combined_metrics.csv`/`neural_metrics.csv`.
`MultiRB_t01..t03` marked `DISCARDED.md` in place (see below) rather than deleted, per the author's
instruction to keep historical folders as reference.

## Folder → scenario → status

| Folder(s) | Scenario (confirmed) | N trials | Files | Status |
|---|---|---|---|---|
| `StimuliB_t01..t04` | Appetitive (blue stimulus — verified: `blue_present` sum>0, `red_present`=0 in `neural_metrics.csv`) | 4 | `combined_metrics.csv`, `neural_metrics.csv` | ✅ Usable as-is (CSV) |
| `StimuliR_t01..t03` | Aversive (red stimulus — verified: `red_present` dominates) | 3 | same | ✅ Usable as-is (CSV) |
| `StimuliG_t01..t03` | Obstacle (green stimulus — verified: `red_present`/`blue_present` near-zero) | 3 | same | ✅ Usable as-is (CSV) |
| `MultiRGB_t01..t03` | **Complex — canonical (D-2)** | 3 | same | ✅ Usable as-is (CSV) |
| `MultiRB_t01..t03` | — **DISCARDED (D-2)**, not used for any figure | 3 | same + `DISCARDED.md` | ⛔ Do not use |
| `Test_current_integrated_floor_t01` | Terrain IMU/energy (candidate: flat/rugged — **not content-verified**, name-based only) | 1 | `combined_metrics.csv`, `neural_metrics.csv`, `imu_ina.csv` (renamed, orig. `imu_ina_20260610_203132.csv`) | 🖼️ Figures sourced from it are vectorized instead (D-7) — energy figure still CSV-based (see below) |
| `Test_current_integrated_ramp_t01`, `_ramp_t02` | Terrain IMU/energy (candidate: inclined slope — **not content-verified**) | 2 | same pattern (orig. `imu_ina_20260610_203456.csv`, `imu_ina_20260610_203909.csv`) | same as above |
| `Test_current_integrated_static_t01` | Terrain IMU/energy (candidate: stagnation/static — **not content-verified**) | 1 | same pattern (orig. `imu_ina_20260610_205948.csv`) | same as above |
| `Test_current_integrated_t01` | Morphological-transition energy source — **content-independent of the terrain question above**, used for `FigReal_Morphological_Transition_Energy.png` | 1 | same pattern (orig. `imu_ina_20260610_202759.csv`) | ✅ Usable as-is (CSV) — `current_A`×`voltage_V`=`power_W`, transition instant = power-draw peak |
| `Test_current_t01` | Preliminary/duplicate current+IMU capture, 3 sub-runs (`imu_ina_prueba.csv`, `imu_ina_t01.csv`, `imu_ina_t02.csv` — names left as-is, already distinct and meaningful) | 3 | `imu_ina_*.csv` only, no `combined_metrics`/`neural_metrics` | ℹ️ Not currently mapped to any published figure — likely superseded by `Test_current_integrated_*` |
| `Imu_pitch_test_t01` | Dedicated pitch-triggered switching-latency test (25 trials alternating stimulus 12.0°/0.0°) | 25 (trial rows, 1 folder) | `pitch_latency.csv` (renamed, orig. `pitch_latency_20260610_232108.csv`) | ℹ️ Strong candidate for `FigReal_Terrain_Latencies_4Panels.png`, but figure itself is being vectorized directly (D-7) rather than rebuilt from this file — see Tarea 3 |

## Figures this maps to (physical section only)

| Figure | Source | Status for Tarea 3 |
|---|---|---|
| `Appetitive/Aversive/Obstacle/Complex_Real_Plot_{1,2,3}.png` (12 figures) | `StimuliB/R/G` + `MultiRGB` | CSV rebuild, no vectorization |
| `NEU_EST_UNIG_real.png` | `StimuliG_t01..t03` | CSV rebuild |
| `NEU_EST_MUL_real.png` | `MultiRGB_t01..t03` | CSV rebuild |
| `GRAPH_IMU_real.png`, `NEU_IMU_real.png` | not trusted from `Test_current_integrated_*` by folder name (D-7) | Vectorize |
| `GRAPH_IMU2_real.png`, `NEU_IMU2_real.png` | same | Vectorize |
| `FigReal_Terrain_Latencies_4Panels.png` | same | Vectorize |
| `FigReal_Morphological_Transition_Energy.png` | `Test_current_integrated_t01`/`imu_ina.csv` | CSV rebuild (not part of D-7's distrust set — see Informe 2 §1.2 note) |

## Why `Test_current_integrated_*`'s terrain identity stays "not content-verified"

D-7 (Informe 2) already decided **not** to use folder-name association (`floor`/`ramp`/`static`) as
the source for the 5 vectorized figures — this manifest documents that decision's scope precisely
so it isn't accidentally re-litigated or accidentally relied on later: these 3 folders remain
useful for `FigReal_Morphological_Transition_Energy.png` (which never depended on the
floor/ramp/static terrain distinction, only on the current/power draw signal), but nothing else in
this repository should treat "floor" as "confirmed rugged terrain" or "ramp" as "confirmed slope".
