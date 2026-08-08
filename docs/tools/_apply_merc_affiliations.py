#!/usr/bin/env python3
"""Set Affiliation=MERC on Jazz_* roster UnitData (JAZZ-UI-MERC-001)."""
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(__file__).resolve().parents[3] / "jazz-units" / "UnitData"
# parents: tools -> docs -> jazz -> Mods; jazz-units is sibling of jazz
UNITS = Path(__file__).resolve().parents[2].parent / "jazz-units" / "UnitData"

SHELF = [
    "Jazz_Flo",
    "Jazz_Cougar",
    "Jazz_Madman",
    "Jazz_Blade",
    "Jazz_Conrad",
    "Jazz_Dynamo",
    "Jazz_Gaston",
    "Jazz_Nervous",
    "Jazz_Ricochet",
    "Jazz_Cord",
    "Jazz_Hobbit",
    "Jazz_Horg",
    "Jazz_Meat",
    "Jazz_Shank",
    "Jazz_Biff",
]

WORLD_VANILLA = ["Larry", "Larry_Clean", "Smiley"]


def ensure_affiliation(path: Path, affiliation: str = "MERC") -> bool:
    if not path.exists():
        print("MISSING", path.name)
        return False
    text = path.read_text(encoding="utf-8")
    if re.search(r'Affiliation\s*=\s*"MERC"', text):
        print("ok", path.name)
        return False
    if re.search(r"Affiliation\s*=", text):
        text2, n = re.subn(
            r'Affiliation\s*=\s*"[^"]*"',
            f'Affiliation = "{affiliation}"',
            text,
            count=1,
        )
        if n != 1:
            raise RuntimeError(f"Affiliation replace failed {path.name}")
        path.write_text(text2, encoding="utf-8")
        print("replaced", path.name)
        return True
    # Insert after DefineClass / first field block: after opening `{`
    m = re.search(r"(UndefineClass\([^\)]*\)\s*\nDefineClass\.[^\n]+\s*=\s*\{)", text)
    if not m:
        m = re.search(r"(DefineClass\.[^\n]+\s*=\s*\{)", text)
    if not m:
        # PlaceObj style
        m = re.search(r"(PlaceObj\([^\n]+,\s*\{)", text)
    if not m:
        raise RuntimeError(f"no insert point {path.name}")
    insert = m.group(1) + f'\n\tAffiliation = "{affiliation}",'
    text2 = text[: m.start()] + insert + text[m.end() :]
    path.write_text(text2, encoding="utf-8")
    print("inserted", path.name)
    return True


def main() -> int:
    print("UNITS", UNITS)
    for sid in SHELF:
        ensure_affiliation(UNITS / f"{sid}.lua")
    for sid in WORLD_VANILLA:
        p = UNITS / f"{sid}.lua"
        if p.exists():
            ensure_affiliation(p)
        else:
            print("vanilla not overridden (ok):", sid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
