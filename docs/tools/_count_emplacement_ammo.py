#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Count MachineGunEmplacement ammo_template / weapon_template in jazz-maps."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2].parent / "jazz-maps" / "Maps"


def main() -> None:
    ammo: Counter[str] = Counter()
    weapon: Counter[str] = Counter()
    n = 0
    for p in sorted(ROOT.rglob("objects.lua")):
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        i = 0
        while i < len(lines):
            if "PlaceObj('MachineGunEmplacement'" in lines[i]:
                n += 1
                block: list[str] = []
                i += 1
                depth = 1
                while i < len(lines) and depth > 0:
                    if "{" in lines[i]:
                        depth += lines[i].count("{")
                    if "}" in lines[i]:
                        depth -= lines[i].count("}")
                    block.append(lines[i])
                    i += 1
                b = "\n".join(block)
                am = re.search(r"'ammo_template',\s*\"([^\"]+)\"", b)
                wm = re.search(r"'weapon_template',\s*\"([^\"]+)\"", b)
                ammo[am.group(1) if am else "(default)"] += 1
                weapon[wm.group(1) if wm else "(default BrowningM2HMG)"] += 1
            else:
                i += 1
    print(f"emplacements={n}")
    print("ammo", dict(ammo))
    print("weapon", dict(weapon))


if __name__ == "__main__":
    main()
