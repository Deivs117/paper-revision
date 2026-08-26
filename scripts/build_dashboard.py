#!/usr/bin/env python3
"""Parses PROGRESS.md's table into docs/data.json for the GitHub Pages traceability dashboard
(docs/index.html). PROGRESS.md is the single source of truth — this script never writes back to
it, only reads. Run after any change to PROGRESS.md; the pre-commit hook (scripts/hooks/
pre-commit) does this automatically when PROGRESS.md is part of the commit. See README.md §12.

Column order in PROGRESS.md (must match — the header row is not parsed for order, just skipped):
  ID | Reviewer | Requirement (short) | Target section(s) | Data source | Category | Owner |
  Status | Patch file
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROGRESS_FILE = REPO_ROOT / "PROGRESS.md"
OUT_FILE = REPO_ROOT / "docs" / "data.json"

EXPECTED_COLUMNS = 9


def strip_md_inline(text: str) -> str:
    """Light markdown-to-plain-text cleanup for display: drops **bold**/`code`/*italic* markup
    and collapses whitespace. Not a full markdown parser -- good enough for table-cell prose."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_table(md_text: str):
    rows = []
    header_seen = False
    for line in md_text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) != EXPECTED_COLUMNS:
            continue
        if not header_seen:
            # First matching row is the header; the next (all-dashes) is the separator.
            header_seen = True
            continue
        if all(re.fullmatch(r"-+", c) for c in cells):
            continue  # separator row
        rows.append(cells)
    return rows


def git_last_commit_iso(path: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "log", "-1", "--format=%cI", "--", str(path.relative_to(REPO_ROOT))],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return out or ""
    except Exception:
        return ""


def main():
    if not PROGRESS_FILE.exists():
        print(f"error: {PROGRESS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    rows = parse_table(PROGRESS_FILE.read_text(encoding="utf-8"))

    tasks = []
    for cells in rows:
        task_id, reviewer, requirement, target, data_source, category, owner, status, patch_file = cells
        tasks.append({
            "id": strip_md_inline(task_id),
            "reviewer": strip_md_inline(reviewer),
            "requirement": strip_md_inline(requirement),
            "target": strip_md_inline(target),
            "dataSource": strip_md_inline(data_source),
            "category": strip_md_inline(category),
            "owner": [o.strip() for o in strip_md_inline(owner).split(",") if o.strip()],
            "status": strip_md_inline(status),
            "patchFile": strip_md_inline(patch_file),
        })

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "progressLastCommit": git_last_commit_iso(PROGRESS_FILE),
        "tasks": tasks,
    }

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(tasks)} tasks -> {OUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
