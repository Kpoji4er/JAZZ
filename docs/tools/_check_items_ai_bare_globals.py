# Flag bare `prev` in jazz-units items.lua Score / PickCustom bodies.
# That name asserts in JA3 debug when the chunk env has no such global.
from __future__ import annotations

import re
import sys
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
ITEMS = JAZZ.parent / "jazz-units" / "items.lua"

FUNC_START = re.compile(
    r"^(\s*)'(Score|PickCustomArchetype)', function \("
)
BARE_PREV = re.compile(r"(?<![\w.])prev(?![\w.])")
LOCAL_PREV = re.compile(r"\blocal\s+[^=\n]*\bprev\b")


def main() -> int:
    if not ITEMS.is_file():
        print("FAIL: missing jazz-units/items.lua")
        return 1
    lines = ITEMS.read_text(encoding="utf-8").splitlines()
    failed: list[str] = []
    i = 0
    while i < len(lines):
        m = FUNC_START.match(lines[i])
        if not m:
            i += 1
            continue
        indent = m.group(1)
        end_pat = re.compile(rf"^{indent}end,?\s*$")
        has_local = False
        i += 1
        while i < len(lines):
            line = lines[i]
            if LOCAL_PREV.search(line):
                has_local = True
            if (not has_local) and BARE_PREV.search(line) and not line.lstrip().startswith("--"):
                failed.append(f"items.lua:{i + 1} bare prev in Score/PickCustom")
            if end_pat.match(line):
                break
            i += 1
        i += 1
    if failed:
        print("FAIL: items.lua AI closures bare-read prev")
        for row in failed:
            print(" -", row)
        return 1
    print("PASS: no bare prev in items.lua Score/PickCustom")
    return 0


if __name__ == "__main__":
    sys.exit(main())
