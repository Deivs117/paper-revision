#!/usr/bin/env bash
# Fast structural sanity check on source/main_monolithic.tex — no LaTeX toolchain required.
# See README.md §5.5. Checks: balanced braces, exactly one \begin{document}/\end{document},
# every \begin{X} has a matching \end{X}.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

if [ ! -f "$MIRROR_FILE" ]; then
  echo "error: $MIRROR_FILE not found" >&2
  exit 1
fi

python3 - "$MIRROR_FILE" <<'PYEOF'
import re
import sys

path = sys.argv[1]
with open(path, "r", encoding="utf-8") as f:
    raw_text = f.read()


def strip_comments(raw):
    """Remove LaTeX line comments (an unescaped % to end of line) before checking structure —
    otherwise a \\begin{document} or brace mentioned inside a comment gets counted as real."""
    out_lines = []
    for line in raw.split("\n"):
        result = []
        i = 0
        while i < len(line):
            c = line[i]
            if c == "\\" and i + 1 < len(line):
                result.append(c)
                result.append(line[i + 1])
                i += 2
                continue
            if c == "%":
                break
            result.append(c)
            i += 1
        out_lines.append("".join(result))
    return "\n".join(out_lines)


text = strip_comments(raw_text)

# 1. Balanced braces.
open_count = text.count("{")
close_count = text.count("}")
if open_count != close_count:
    print(f"FAIL: unbalanced braces ({{={open_count}, }}={close_count})")
    sys.exit(1)

# 2. Exactly one \begin{document} and one \end{document}.
begin_doc = len(re.findall(r"\\begin\{document\}", text))
end_doc = len(re.findall(r"\\end\{document\}", text))
if begin_doc != 1:
    print(f"FAIL: expected exactly one \\begin{{document}}, found {begin_doc}")
    sys.exit(1)
if end_doc != 1:
    print(f"FAIL: expected exactly one \\end{{document}}, found {end_doc}")
    sys.exit(1)

# 3. Every \begin{X} has a matching \end{X} (stack-based).
stack = []
for m in re.finditer(r"\\(begin|end)\{([^}]*)\}", text):
    kind, env = m.group(1), m.group(2)
    if kind == "begin":
        stack.append(env)
    else:
        if not stack:
            line = text.count("\n", 0, m.start()) + 1
            print(f"FAIL: \\end{{{env}}} with no matching \\begin (line {line})")
            sys.exit(1)
        top = stack.pop()
        if top != env:
            line = text.count("\n", 0, m.start()) + 1
            print(f"FAIL: \\end{{{env}}} does not match innermost \\begin{{{top}}} (line {line})")
            sys.exit(1)
if stack:
    print(f"FAIL: unclosed environment(s): {', '.join(stack)}")
    sys.exit(1)

print("OK: braces balanced, document markers present, all environments matched.")
PYEOF
