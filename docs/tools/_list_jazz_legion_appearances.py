#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""List handcrafted jazz-units Legion* AppearancePreset ids (canon pool)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JU = Path(__file__).resolve().parents[2].parent / "jazz-units"
ITEMS = JU / "items.lua"
VANILLA_AP = Path(
    r"F:\SteamLibrary\steamapps\common\Jagged Alliance 3"
    r"\ModTools\Src\Data\AppearancePreset.lua"
)


def extract_moditem_appearances(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    needle = "PlaceObj('ModItemAppearancePreset'"
    i = 0
    while True:
        start = text.find(needle, i)
        if start < 0:
            break
        brace = text.find("{", start)
        depth = 0
        j = brace
        while j < len(text):
            c = text[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    end = j + 1
                    if end < len(text) and text[end] == ")":
                        end += 1
                    block = text[start:end]
                    m = re.search(r"\bid\s*=\s*\"([^\"]+)\"", block)
                    if m:
                        out[m.group(1)] = block
                    i = end
                    break
            j += 1
        else:
            break
    return out


def is_canon_legion(aid: str) -> bool:
    if not aid.startswith("Legion"):
        return False
    if aid.startswith("Legion_"):
        return False
    if "Armor" in aid:
        return False
    return True


def main() -> int:
    apps = extract_moditem_appearances(ITEMS.read_text(encoding="utf-8"))
    legion = sorted(a for a in apps if is_canon_legion(a))
    print(f"canon Legion* count={len(legion)}")
    for a in legion:
        print(a)
    if VANILLA_AP.is_file():
        vt = VANILLA_AP.read_text(encoding="utf-8", errors="replace")
        hairs = sorted(set(re.findall(r'Hair\s*=\s*"(NPCFemale_Hair_[^"]+)"', vt)))
        print("NPCFemale_Hair in vanilla:", hairs or "(none found via Hair=)")
        # also Entity/mesh name scan
        all_h = sorted(set(re.findall(r'"(NPCFemale_Hair_[^"]+)"', vt)))
        print("NPCFemale_Hair string refs:", all_h)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
