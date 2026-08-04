# -*- coding: utf-8 -*-
"""Static: FortressPierre must NOT be remapped away from vanilla Pierre boss.

Bug: SQUAD_REMAP FortressPierre → LegionJAZZSquadT2 dropped Pierre; an elite
Legion unit inherited DefenderPriority group \"Pierre\" and spoke Pierre_1 with
GenerateEliteUnitName (e.g. Kingboy Life).

Checks jazz-nomaps/Code/NoMaps_Autonomy.lua SQUAD_REMAP table.
Exit 0 = OK, 1 = FAIL.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOMAPS = ROOT.parent / "jazz-nomaps" / "Code" / "NoMaps_Autonomy.lua"


def main() -> int:
    if not NOMAPS.is_file():
        print(f"FAIL: missing {NOMAPS}")
        return 1
    text = NOMAPS.read_text(encoding="utf-8")
    # Extract SQUAD_REMAP = { ... } roughly until ROLE_LISTS
    m = re.search(
        r"local SQUAD_REMAP\s*=\s*\{(.*?)\n\}",
        text,
        re.DOTALL,
    )
    if not m:
        print("FAIL: SQUAD_REMAP block not found")
        return 1
    body = m.group(1)
    # Forbidden: FortressPierre = "something" that is not FortressPierre / omitted
    assigns = re.findall(
        r"^\s*FortressPierre\s*=\s*([\"'])([^\"']+)\1",
        body,
        re.MULTILINE,
    )
    if not assigns:
        print("OK: FortressPierre absent from SQUAD_REMAP (vanilla Pierre kept)")
        return 0
    targets = [t for _q, t in assigns]
    bad = [t for t in targets if t != "FortressPierre"]
    if bad:
        print(f"FAIL: FortressPierre remapped to {bad} (must omit or self-map)")
        return 1
    print("OK: FortressPierre self-mapped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
