# <ID> — <short title>

Copy this directory to `experiments/<ID>-<slug>/` and fill in every section before running anything.
See `experiments/README.md` and `README.md` §9 for the full workflow this fits into.

## Goal

What figure/table/number this produces, and which `PROGRESS.md` row it's for.

## Method

What the script(s) in `scripts/` actually do, in enough detail that someone who has read
`OUTLINE.md` but not the code can follow it.

## Parameters / seed

Point at `config.yaml` (or inline here if trivial). Any run that isn't seeded/deterministic must
say so explicitly — note here what's expected to vary between reruns.

## Data provenance

- Where the input data came from (a real hardware run, a `PETER_SIMULATION` simulation, synthetic).
- If it depends on `PETER_SIMULATION`: the exact commit pinned —
  `git -C ../../PETER_SIMULATION rev-parse HEAD` at the time this was run — since that repo is a
  live sibling, not version-locked to this one.
- If `data/` can't be regenerated purely from `scripts/` + `config.yaml` (e.g. it needs a physical
  robot run), say exactly what manual step produced it.

## How to regenerate

```
cd experiments/<ID>-<slug>
<exact command(s) to run scripts/ and populate output/>
```

## Output files

| File in `output/` | Promoted to (`assets/...`) | Used in |
|---|---|---|
| `example.png` | `assets/example.png` | `sections/<slug>.tex`, Fig.~\ref{fig:example} |
