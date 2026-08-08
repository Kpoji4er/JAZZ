#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static QA after AME clothes-from-map patch."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
JU = JAZZ.parent / "jazz-units"
ITEMS = JU / "items.lua"
MAP = JAZZ / "docs" / "design" / "ame-appearance-map.json"

BEGIN = "-- JAZZ-UNITS-005-AME-APP-BEGIN"
END = "-- JAZZ-UNITS-005-AME-APP-END"


def extract_ame(text: str) -> dict[str, str]:
    a = text.find(BEGIN)
    b = text.find(END)
    section = text[a:b]
    out = {}
    needle = "PlaceObj('ModItemAppearancePreset'"
    i = 0
    while True:
        start = section.find(needle, i)
        if start < 0:
            break
        brace = section.find("{", start)
        depth = 0
        j = brace
        while j < len(section):
            c = section[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    end = j + 1
                    block = section[start:end]
                    m = re.search(r'\bid\s*=\s*"([^"]+)"', block)
                    if m:
                        out[m.group(1)] = block
                    i = end
                    break
            j += 1
        else:
            break
    return out


def mesh(block: str, key: str) -> str:
    m = re.search(rf'{key}\s*=\s*"([^"]*)"', block)
    return m.group(1) if m else ""


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    ame = extract_ame(text)
    rows = json.loads(MAP.read_text(encoding="utf-8"))
    bad = []
    print(f"AME presets in section={len(ame)}")
    legion_heads = []
    aim_hair = []
    hat_with_hair = []
    helmets = []
    for aid, blk in sorted(ame.items()):
        h = mesh(blk, "Head")
        if h.startswith("Faction_Legion_Head_"):
            legion_heads.append((aid, h))
        hair = mesh(blk, "Hair")
        if hair.startswith("Equipment"):
            aim_hair.append((aid, hair))
        hat = mesh(blk, "Hat")
        hat2 = mesh(blk, "Hat2")
        if (hat or hat2) and hair:
            hat_with_hair.append((aid, hair, hat or hat2))
        for label, m in (("Hat", hat), ("Hat2", hat2)):
            if m and re.search(
                r"Helmet|WW2Helmet|SkullHat|LarryAddicted_Hat|"
                r"^FactionMale_Hat_08$|^FactionMale_Hat_09$",
                m,
                re.I,
            ):
                helmets.append((aid, label, m))
    irreg = [r for r in rows if r["cat"] == "Irregulars" and not r.get("female")]
    irreg_leg = sum(
        1
        for r in irreg
        if r["donor"].startswith("Legion") and not r["donor"].startswith("Legion_")
    )
    print(f"Irregular male jazz_Legion* donors={irreg_leg}/{len(irreg)}")
    print(
        f"Legion warpaint heads={len(legion_heads)} AIM hair={len(aim_hair)} "
        f"hat+hair={len(hat_with_hair)} helmets={len(helmets)}"
    )
    for x in legion_heads[:5]:
        print("  legion head", x)
    for x in aim_hair[:5]:
        print("  aim hair", x)
    for x in hat_with_hair[:5]:
        print("  hat+hair", x)
    for x in helmets[:8]:
        print("  helmet", x)
    fem = [r for r in rows if r.get("female")]
    for r in fem:
        print(f"  {r['id']} donor={r['donor']} hair={r.get('hair','?')!r}")
    if legion_heads or aim_hair or hat_with_hair or helmets:
        return 1
    if irreg_leg < 10:
        print("FAIL: expected ≥10 Irregular jazz Legion* donors")
        return 1
    print("QA OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
