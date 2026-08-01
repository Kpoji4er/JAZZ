#!/usr/bin/env python3
"""Static check JAZZ-COMPAT-005: LegionJAZZSquadT1_Early is T1-only; NoMaps remap/cap present."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNITS_ITEMS = ROOT.parent / "jazz-units" / "items.lua"
UNITS_META = ROOT.parent / "jazz-units" / "metadata.lua"
NOMAPS = ROOT.parent / "jazz-nomaps" / "Code" / "NoMaps_Autonomy.lua"

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def extract_squad_block(text: str, squad_id: str) -> str | None:
    id_m = re.search(rf'\bid\s*=\s*"{re.escape(squad_id)}"', text)
    if not id_m:
        return None
    start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, id_m.start())
    if start < 0:
        return None
    return text[start : id_m.end()]


def main() -> int:
    if not UNITS_ITEMS.is_file():
        fail(f"missing {UNITS_ITEMS}")
    if not NOMAPS.is_file():
        fail(f"missing {NOMAPS}")
    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1

    units = UNITS_ITEMS.read_text(encoding="utf-8")
    block = extract_squad_block(units, "LegionJAZZSquadT1_Early")
    if not block:
        fail("LegionJAZZSquadT1_Early missing from jazz-units/items.lua")
    else:
        types = re.findall(r"'unitType',\s*\"(JAZZ_Legion_[^\"]+)\"", block)
        if not types:
            fail("Early squad has no unitType entries")
        for t in types:
            if not re.search(r"T1_", t):
                fail(f"non-T1 unitType in Early: {t}")

    meta = UNITS_META.read_text(encoding="utf-8")
    if 'Id", "LegionJAZZSquadT1_Early"' not in meta and "Id', \"LegionJAZZSquadT1_Early\"" not in meta:
        # metadata uses 'Id', "…"
        if "'Id', \"LegionJAZZSquadT1_Early\"" not in meta:
            fail("LegionJAZZSquadT1_Early missing from jazz-units/metadata.lua")

    nomaps = NOMAPS.read_text(encoding="utf-8")
    for needle in (
        "lResolveTieredLegionSquad",
        "LegionJAZZSquadT1_Early",
        "major <= 1",
        "COMPAT-005",
    ):
        if needle not in nomaps:
            fail(f"NoMaps_Autonomy missing {needle!r}")

    if "LegionRustIni = \"LegionJAZZSquadT1_Early\"" not in nomaps:
        fail("LegionRustIni remap not pointed at Early")

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("OK — Early T1-only + NoMaps COMPAT-005 wiring")
    return 0


if __name__ == "__main__":
    sys.exit(main())
