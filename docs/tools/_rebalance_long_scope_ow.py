# -*- coding: utf-8 -*-
"""Long scopes: OW sector narrows with magnification (ScopeOverwatchAngle%)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop, atomic_write

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"

LONG_OW = {
    "JAZZ_Scope_Garand": 82,
    "JAZZ_Scope_Springfield": 80,
    "JAZZ_Scope_PU": 75,
    "JAZZ_Scope_PSO": 65,
    "JAZZ_Scope_ZF4": 65,
    "JAZZ_Scope_ZRAK": 65,
    "JAZZ_Scope_6x": 55,
    "JAZZ_Scope_PSG": 55,
    "JAZZ_Scope_DA15_6x": 55,
    "JAZZ_Scope_Scout": 52,
    "JAZZ_Scope_8x_SCROME": 48,
    "JAZZ_Scope_3x_9x": 45,
    "JAZZ_Scope_12x": 42,
    "JAZZ_AUGScope_Default": 88,
}


def set_or_add_param(block: str, name: str, value: int) -> str:
    if re.search(rf"'Name', \"{re.escape(name)}\"", block):
        return re.sub(
            rf"('Name', \"{re.escape(name)}\",\s*\n\s*'Value', )\d+",
            rf"\g<1>{value}",
            block,
            count=1,
        )
    insert = (
        "\t\t\t\t\t\t\t\tPlaceObj('PresetParamNumber', {\n"
        f"\t\t\t\t\t\t\t\t\t'Name', \"{name}\",\n"
        f"\t\t\t\t\t\t\t\t\t'Value', {value},\n"
        f"\t\t\t\t\t\t\t\t\t'Tag', \"<{name}>\",\n"
        "\t\t\t\t\t\t\t\t}),\n"
    )
    return re.sub(r"(Parameters = \{\n)", rf"\1{insert}", block, count=1)


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    n = 0
    for block in reversed(placeobj_blocks(text, "ModItemWeaponComponent")):
        cid = prop(block.text, "id")
        if cid not in LONG_OW:
            continue
        if (
            "ScopeOverwatchAngleDecreaseBig" not in block.text
            and "ScopeOverwatchAngleDecrease" not in block.text
        ):
            print("skip", cid)
            continue
        new = set_or_add_param(block.text, "ScopeOverwatchAngle", LONG_OW[cid])
        text = text[: block.start] + new + text[block.end :]
        n += 1
        print("OW%", LONG_OW[cid], cid)
    atomic_write(ITEMS, text)
    print("total", n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
