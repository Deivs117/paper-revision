#!/usr/bin/env python3
"""List the open PROGRESS.md rows owned by one person (stdlib only).

Usage: python3 scripts/my_tasks.py <Name-or-GitHub-login>   e.g. Sam, Sebas, Diego, Deivi, sammcar
       python3 scripts/my_tasks.py --all                    one block per owner

"Open" = Status `pending` or `drafted`. Rows in `applied` are listed by ID only (done, waiting for the
repo owner's Overleaf sync). A row may carry a deadline written as `Due YYYY-MM-DD` in its text.
Always run `git pull origin main` first: PROGRESS.md on a stale checkout gives a stale answer.
"""
import re
import sys
from pathlib import Path

ALIASES = {
    "sammcar": "sam", "samuel": "sam",
    "sebas2868": "sebas", "sebastian": "sebas", "sebastián": "sebas",
    "diegoacaro": "diego",
    "deivs117": "deivi", "david": "deivi",
}
OPEN = {"pending", "drafted"}
HARD_STOP = "2026-11-04"


def rows(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(cells) != 9 or cells[0] in ("ID", "") or set(cells[0]) <= {"-", " "}:
            continue
        yield dict(zip(("id", "rev", "req", "target", "data", "cat", "owner", "status", "patch"), cells))


def owners_of(row):
    return {ALIASES.get(o.strip().lower(), o.strip().lower()) for o in row["owner"].split(",")}


def show(name, all_rows):
    key = ALIASES.get(name.lower(), name.lower())
    mine = [r for r in all_rows if key in owners_of(r)]
    open_rows = [r for r in mine if r["status"] in OPEN]
    done = [r["id"] for r in mine if r["status"] == "applied"]
    due = lambda r: (re.search(r"Due (\d{4}-\d\d-\d\d)", r["req"]) or [None, "9999"])[1]
    print(f"== {name}: {len(open_rows)} open task(s)  (hard stop for the whole round: {HARD_STOP})")
    for r in sorted(open_rows, key=due):
        d = due(r)
        print(f"\n[{r['id']}] status={r['status']}  due={d if d != '9999' else 'not set'}")
        print(f"  task:   {r['req']}")
        print(f"  where:  {r['target']}")
        for doc in sorted(set(re.findall(r"intake/(?:pending|processed)/[\w.\-]+\.md", r["req"]))):
            print(f"  brief:  {doc}")
        if r["data"] not in ("", "—"):
            print(f"  data:   {r['data']}")
    if done:
        print(f"\nDone by you, waiting for the repo owner's Overleaf sync (nothing to do): {', '.join(done)}")
    if not mine:
        print("\nNo rows with this owner. Check the spelling (Sam, Sebas, Diego, Deivi).")
    print("\nHow to land a task: README.md section 13 (branch -> PR into main; your row stops at `applied`).")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    all_rows = list(rows(Path(__file__).resolve().parent.parent / "PROGRESS.md"))
    names = ["Sam", "Sebas", "Diego", "Deivi"] if sys.argv[1] == "--all" else [sys.argv[1]]
    for n in names:
        show(n, all_rows)
        print()
    bad = [r["id"] for r in all_rows if r["status"] in OPEN and not r["owner"].strip("— ")]
    if bad:
        print(f"WARNING: open rows with no owner (nobody will see them): {', '.join(bad)}")


if __name__ == "__main__":
    main()
