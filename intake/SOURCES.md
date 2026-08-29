# Intake Sources

Sibling repositories the agent may **read from** (never write to) when an `intake/pending/` document references
implementation details it doesn't fully restate. See `README.md` §8.3.

- **PETER_SIMULATION** — `../PETER_SIMULATION` — firmware, ROS 2 simulation, hardware findings (`Findings/`,
  `Repository/`, `ros2_ws/`). Read-only.
  - **R3-05 (reactive inspection task, Experiment E) pins branch `sam`, commit `6d5a2e6`**
    ("feat(exp-e): implementar experimento de inspección reactiva (Reviewer #3.5)"), not `main`.
    `inspection_recorder.py` and the `familia_e_inspeccion` suite (`test_manager.py`'s
    `SUITE_INSPECTION`/`_eval_inspection`, `experiments_config.yaml`'s `familia_e_inspeccion` entry)
    exist only on `sam` as of 2026-08-29 — verified absent on `main`/`dieguito`/`Deiv`. If a future
    check on `main` doesn't find this code, that's expected; re-check `sam` before assuming it
    regressed. Delivered results from this run live in `experiments/R3-05-inspection/data/` (see
    that experiment's own `README.md` for full provenance).

## Atomic task blocks — when a pending document grows too large

If a single `intake/pending/<doc>.md` grows to cover several unrelated groups of changes (or two documents end up
cross-referencing each other closely enough that they can desync — e.g. one saying a task is done while the
other still calls it blocked), split it into **one file per family of tasks that share the same
builder/decision/execution**, not one file per individual finding — a family is the largest group that can
reasonably be executed and closed in one pass.

Rules for the split:
- **Each block is self-contained**: it carries its own diagnosis + method + current status, so nobody has to open
  a second file to understand it. Some duplication between related blocks is fine; a block silently depending on
  another's context is not.
- **No separate index/summary document.** Status lives in each block's own header line and in `PROGRESS.md`
  (which already tracks every row's state) — an extra file whose only job is "explain what happened" duplicates
  that and rots the same way the original two-document setup did. This `SOURCES.md` entry is the one place that
  states the convention itself, not a log of any specific split.
- **Move, don't summarize, on close.** A block moves from `intake/pending/` to `intake/processed/` via `git mv`
  once every change it produced reaches `applied` or later (§8.2 in `README.md`) — it keeps its full content
  there as the audit trail; nothing gets rewritten into a shorter "what happened" note elsewhere.
- Name blocks so the family is obvious from the filename alone (e.g. `<origin-id>-<NN>_<slug>.md`) — a reader
  should be able to tell what's done vs. pending by scanning `intake/pending/` and `intake/processed/` directly,
  without needing another document to explain the listing.
