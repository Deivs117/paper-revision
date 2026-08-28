# N-01 — Simulation Figure Regeneration Pipeline (Tarea 1)

**Goal:** a reusable pipeline that turns a simulation results folder (the same layout as
`experiments/simulation/familia_*/test_NNN[_VERDICT]/*.csv|json`) into the noise-robustness grid,
`FigA/FigB/FigC`, and `tab:consolidated_simulation_metrics` — so that when the team re-runs the
simulated tests (notified 2026-08-27, only the simulated battery), regenerating every affected
figure is one command, not a manual re-derivation.

**Provenance:** built from the shared library `experiments/_plotting/` (loaders/builders/style),
following the architecture and the 11 confirmed decisions (D-1–D-11), now documented in
`intake/pending/R02-01-05_simulacion_grupo2_vectorizacion.md` (§4) and `intake/processed/R02-01-02_fisico_regeneracion_N02-N05.md`
(§2) — see `intake/R02-01_INDEX.md` for the full block index. Council decisions specific to this
experiment, made 2026-08-27 in the follow-up planning round:

- **D-12 (versioning):** a future re-run lands in a **new sibling directory** next to the current
  `experiments/simulation/familia_*` folders (e.g. `experiments/simulation_2026XXXX/` or
  `familia_a_apetitivo_v2/` — exact naming TBD when the run actually lands), never overwriting the
  current ones. This pipeline takes `--simulation-root` as a CLI flag for exactly this reason — no
  code change needed to point it at the new batch, only the root path.
- **D-13 (execution scope):** built AND already executed once against the current
  `experiments/simulation/` data (this round), producing the files in `output/` below, to prove the
  pipeline end-to-end and leave a byte-fresh, code-traceable version of the already-published
  figures on hand.
- **D-14 (promotion):** output stays in `output/` for manual review — **not** promoted to `assets/`
  automatically. `scripts/promote_figure.sh` remains the only path into `assets/`, run by hand once
  the author has compared `output/` against the current published figures and (for M-01–M-04)
  decided the text redaction in `results.tex`.

## Scripts

- `experiments/_plotting/builders/macro_robustness.py` — the fused 4x3 noise-robustness grid
  (Informe 1 F-02, confirmed D-9) + `tab:consolidated_simulation_metrics` recompute.
- `experiments/_plotting/builders/ecdf_phase_space.py` — `FigA_Stability_Profile`,
  `FigB_Decision_Delay`, `FigC_Terrain_Adaptability` (the M-01–M-04 figures, already verified
  correct against this exact data in Informe 2 §0 — this regenerates a fresh, code-traceable copy,
  it does not change any number).
- `experiments/_plotting/generate_all_simulation.py` — entry point, calls both builders.

Run (from repo root, using the project's own throwaway venv — `experiments/.venv_plotting/`,
gitignored, created with `python3 -m venv experiments/.venv_plotting && experiments/.venv_plotting/bin/pip install numpy matplotlib pandas pillow`):

```bash
experiments/.venv_plotting/bin/python experiments/_plotting/generate_all_simulation.py \
  --simulation-root experiments/simulation \
  --output-dir experiments/N-01-simulation-figure-regeneration/output
```

## New finding this round — correction to Informe 2's F-Data-01

Running the pipeline against `familia_a_obstaculo` surfaced a mistake in Informe 2's original
diagnosis of F-Data-01: it assumed `metrics_raw.csv`'s `latency_s` column was populated for this
scenario (as a fallback for `trial_summary.json`'s `-1.0` sentinel). **It is not** — verified
directly: **0 of the 15 `familia_a_obstaculo` trials have a single non-empty `latency_s` value in
either file.** There is currently no recorded latency source for the Obstacle scenario anywhere in
`experiments/simulation/`. The regenerated grid (`output/fig1_noise_robustness_grid.png`) renders
an explicit "No latency data recorded in this run" annotation in that panel instead of silently
plotting zeros or an empty axis (as the very first draft of this pipeline accidentally did before
this was caught).

**Action item, folds naturally into the upcoming re-run (Task notified 2026-08-27):** when the
simulated battery is re-run, confirm the Obstacle scenario's latency instrumentation is actually
wired up before archiving the new `familia_a_obstaculo/` folder — otherwise this gap repeats. Until
then, `fig1_Obstacle_macro.png`'s currently-published panel C (which per Informe 1 shows normal
latency values) cannot be reproduced from anything in this repository; if that figure needs to
stay in the paper as-is, it should be treated as a vectorization candidate (Informe 2 §2 method),
not a CSV rebuild.

**Full list for the simulation team:** this is one of 10 items (4 blocking, 6 minor) found while
building this pipeline — see `experiments/simulation/SIMULATION_TEAM_ACTION_ITEMS.md` for the
complete, evidence-backed list to hand off before the re-run.

## Output

- `output/fig1_noise_robustness_grid.png` — fused 4x3 grid replacing the 4 `fig1_*_macro.png`.
- `output/FigA_Stability_Profile.png`, `output/FigB_Decision_Delay.png`,
  `output/FigC_Terrain_Adaptability.png` — regenerated from `experiments/simulation/familia_c1_terreno_rugoso`
  / `familia_c2_pendiente`, visually consistent with the currently published versions (spot-checked
  against Informe 1's own pixel-level description: flat TR≈0.58–0.60 with a transient bump around
  t=-1.3s to -0.5s in Rugged Terrain, flat TR≈0.59 in Inclined Slope — matches).
- `output/tab_consolidated_simulation_metrics.csv` — recomputed `tab:consolidated_simulation_metrics`
  values, for cross-checking against the currently published table before promoting.
