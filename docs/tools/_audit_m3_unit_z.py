"""Audit M3 UnitMarker / Entrance Z: missing Z or outliers vs local cluster."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from statistics import median

MAP = Path(__file__).resolve().parents[3] / "jazz-maps" / "Maps" / "isJdmPy" / "objects.lua"


def main() -> None:
    text = MAP.read_text(encoding="utf-8", errors="replace")
    units = []
    for m in re.finditer(
        r"PlaceObj\('UnitMarker',\s*\{(.*?)\},\s*nil,\s*\d+\)",
        text,
        re.S,
    ):
        body = m.group(1)
        pos = re.search(r"'Pos',\s*point\(([^)]+)\)", body)
        if not pos:
            continue
        parts = [p.strip() for p in pos.group(1).split(",")]
        x, y = int(parts[0]), int(parts[1])
        z = int(parts[2]) if len(parts) >= 3 else None
        ud = re.search(r"UnitDataDefId',\s*\"([^\"]+)\"", body)
        units.append(
            {
                "ud": ud.group(1) if ud else "?",
                "x": x,
                "y": y,
                "z": z,
                "raw": pos.group(1),
            }
        )

    no_z = [u for u in units if u["z"] is None]
    with_z = [u for u in units if u["z"] is not None]
    zs = [u["z"] for u in with_z]
    print(f"UnitMarkers={len(units)} with_z={len(with_z)} missing_z={len(no_z)}")
    if zs:
        print(f"Z range: min={min(zs)} max={max(zs)} median={int(median(zs))}")
    print("\nMissing Z:")
    for u in no_z:
        print(f"  {u['ud']} @ ({u['x']},{u['y']})")

    # Local outlier: Z differs a lot from nearest neighbors by XY
    print("\nLocal Z outliers (|z-median_neighbors|>4000, neigh<=8 within 40 tiles):")
    slab = 2400
    for u in with_z:
        neigh = []
        for o in with_z:
            if o is u:
                continue
            dx, dy = abs(o["x"] - u["x"]), abs(o["y"] - u["y"])
            tiles = (dx * dx + dy * dy) ** 0.5 / slab
            if tiles <= 40:
                neigh.append(o["z"])
        if len(neigh) < 2:
            continue
        med = median(neigh)
        if abs(u["z"] - med) > 4000:
            print(
                f"  {u['ud']} z={u['z']} neigh_med={int(med)} delta={u['z']-int(med)} @ ({u['x']},{u['y']})"
            )

    # Entrances
    print("\nEntrances:")
    for m in re.finditer(
        r"PlaceObj\('GridMarker',\s*\{(.*?)\},\s*nil,\s*\d+\)",
        text,
        re.S,
    ):
        body = m.group(1)
        if "'Type', \"Entrance\"" not in body:
            continue
        pos = re.search(r"'Pos',\s*point\(([^)]+)\)", body)
        groups = re.search(r"'Groups',\s*\{\s*\"([^\"]+)\"", body)
        print(f"  {groups.group(1) if groups else '?'} pos=({pos.group(1) if pos else '?'})")


if __name__ == "__main__":
    main()
