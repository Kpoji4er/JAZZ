"""Audit UnitMarker distance to M3 (isJdmPy) Entrance markers vs UnawareSightRange."""
from __future__ import annotations

import re
from pathlib import Path

MAP = Path(__file__).resolve().parents[3] / "jazz-maps" / "Maps" / "isJdmPy" / "objects.lua"
SLAB = 2400
UNAWARE = 22
AWARE = 46


def main() -> None:
    text = MAP.read_text(encoding="utf-8", errors="replace")
    entrances = []
    for m in re.finditer(
        r"PlaceObj\('GridMarker',\s*\{(.*?)\},\s*nil,\s*\d+\)",
        text,
        re.S,
    ):
        body = m.group(1)
        if "'Type', \"Entrance\"" not in body and "'Type', 'Entrance'" not in body:
            continue
        pos = re.search(r"'Pos',\s*point\((\d+),\s*(\d+)", body)
        if not pos:
            continue
        groups = re.search(r"'Groups',\s*\{\s*\"([^\"]+)\"", body)
        intel = "SectorHasIntel" in body
        entrances.append(
            {
                "x": int(pos.group(1)),
                "y": int(pos.group(2)),
                "group": groups.group(1) if groups else "?",
                "intel_gate": intel,
            }
        )

    units = []
    for m in re.finditer(
        r"PlaceObj\('UnitMarker',\s*\{(.*?)\},\s*nil,\s*\d+\)",
        text,
        re.S,
    ):
        body = m.group(1)
        pos = re.search(r"'Pos',\s*point\((\d+),\s*(\d+)", body)
        if not pos:
            continue
        ud = re.search(r"UnitDataDefId',\s*\"([^\"]+)\"", body)
        side = re.search(r"'Side',\s*\"([^\"]+)\"", body)
        units.append(
            {
                "x": int(pos.group(1)),
                "y": int(pos.group(2)),
                "ud": ud.group(1) if ud else "?",
                "side": side.group(1) if side else "?",
            }
        )

    print(f"entrances={len(entrances)} units={len(units)}")
    for e in entrances:
        print(
            f"\nEntrance {e['group']} @ ({e['x']},{e['y']}) intel_gate={e['intel_gate']}"
        )
        near = []
        for u in units:
            if u["side"] not in ("enemy1", "enemy2"):
                continue
            dx = abs(u["x"] - e["x"])
            dy = abs(u["y"] - e["y"])
            tiles = (dx * dx + dy * dy) ** 0.5 / SLAB
            if tiles <= AWARE:
                near.append((tiles, u))
        near.sort(key=lambda t: t[0])
        for tiles, u in near[:15]:
            flag = "UNAWARE-RANGE" if tiles <= UNAWARE else "aware-only"
            print(
                f"  {tiles:5.1f}t [{flag}] {u['side']} {u['ud']} @ ({u['x']},{u['y']})"
            )
        print(f"  total <=AwareSight {len(near)}")


if __name__ == "__main__":
    main()
