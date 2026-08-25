# experiments/ — Generating New Figures/Data

`sections/` and `patches/` assume the figure or number being written about already exists
somewhere reachable (`assets/`, the manuscript's own text). Several checklist items don't work
that way — they need a figure or table that doesn't exist yet (e.g. R3-01 basal-ganglia ablation,
R3-04 noise-robustness sweeps, R3-05 inspection metrics). `experiments/` is where that gets
produced, *before* it ever touches `assets/` or `sections/`.

Full spec: README.md §9. This file is just the short pointer + the layout.

## Layout

```
experiments/
└── <ID>-<slug>/            e.g. R3-01-basal-ganglia-ablation/
    ├── README.md           what/why, parameters+seed, provenance, how to regenerate, output list
    ├── config.yaml          (or .json — run parameters, kept out of code so reruns are exact)
    ├── scripts/             generation code — numpy/matplotlib/pandas/ROS2/etc. all allowed here
    ├── data/                gitignored — raw sim/hardware output (bags, logs, video); regenerable
    └── output/               committed — final processed artifacts: small CSVs + the exact figure
                               files that get promoted into assets/
```

- Directory name reuses the `PROGRESS.md` ID, same convention as `patches/<id>-<slug>.tex`.
- `data/` is gitignored (see root `.gitignore`) — never commit raw rosbags/video/logs. If a run
  isn't reproducible from `scripts/` + `config.yaml` alone, the experiment's `README.md` must say
  exactly what manual step (hardware run, dataset location) produced `data/` instead.
- `output/` **is** committed — it's small (CSVs, final PNG/PDF figures) and is the only thing
  `scripts/promote_figure.sh` is allowed to copy from.

## Workflow

1. `PROGRESS.md` row gets a `Data source` value pointing at `experiments/<ID>-<slug>/` once work
   starts on a data-needing item.
2. Create the experiment directory, write `README.md` there first (goal, method, parameters,
   provenance — including a pinned commit hash if it pulls from `PETER_SIMULATION`, since that
   sibling repo isn't version-locked to this one).
3. Run the generation scripts; final artifacts land in `output/`.
4. `scripts/promote_figure.sh experiments/<ID>-<slug>/output/<file> <assets/relative/path>` copies
   it into `assets/` at the exact path the LaTeX will reference. Refuses to silently overwrite an
   existing asset (use `--force` only when you mean it).
5. From here it's a normal patch: edit `sections/<slug>.tex` to `\includegraphics`/cite the new
   asset and write the surrounding prose, record it in `patches/<id>-<slug>.tex`, update
   `PROGRESS.md` status. `push_to_overleaf.sh` mirrors the promoted asset back like any other.

## External dependencies

Scripts under `experiments/*/scripts/` are exempt from the repo's "bash/Python-stdlib only" rule —
they may use numpy/matplotlib/pandas/ROS2/whatever the analysis needs. This is the second explicit
exception alongside `compile_pdf.sh`; every other script in `scripts/` stays stdlib-only.
