# -*- coding: utf-8 -*-
"""Strip Freeswap lines from docs/wiki/weapons/*.md for weapons without the slot.

Uses weapon-component-options.csv (`slot_type=Freeswap`). Keeps MP5K/MicroUZI/Scorpion.
Also updates components.md option count. Run after `_strip_handgun_freeswap.py --apply`
when node/weapons-docs.mjs is unavailable.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OPTS = ROOT / "docs/technical/weapons/data/weapon-component-options.csv"
WIKI = ROOT / "docs/wiki/weapons"


def main() -> int:
    keep = {
        row["weapon_id"]
        for row in csv.DictReader(OPTS.open(encoding="utf-8"))
        if row.get("slot_type") == "Freeswap"
    }
    print("keep Freeswap:", sorted(keep))
    frag = re.compile(r"(?:<br>)?Freeswap:\s*[^|<]+(?:★)?(?:<br>)?", re.I)
    changed = []
    for path in sorted(WIKI.glob("*.md")):
        if path.name == "components.md":
            continue
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)
        out = []
        file_changed = False
        for line in lines:
            m = re.search(r"`([A-Za-z0-9_]+)`", line)
            if m and "|" in line and "Freeswap" in line and m.group(1) not in keep:
                new = frag.sub("", line)
                new = re.sub(r"(?:<br>)+\|", "|", new)
                new = re.sub(r"\|(?:<br>)+", "|", new)
                new = re.sub(r"(?:<br>){2,}", "<br>", new)
                if new != line:
                    file_changed = True
                    line = new
            out.append(line)
        if file_changed:
            path.write_text("".join(out), encoding="utf-8")
            changed.append(path.name)

    comp = WIKI / "components.md"
    if comp.exists():
        t = comp.read_text(encoding="utf-8")
        t2, n = re.subn(
            r"(\| Freeswap \|[^\n]*\| )\d+( \|)\s*$",
            rf"\g<1>{len(keep)}\2",
            t,
            count=1,
            flags=re.M,
        )
        if n:
            comp.write_text(t2, encoding="utf-8")
            changed.append("components.md")
        else:
            print("WARN: components.md Freeswap count not updated")

    print("wiki updated:", changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
