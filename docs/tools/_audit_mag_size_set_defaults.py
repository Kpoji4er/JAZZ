# -*- coding: utf-8 -*-
"""Static audit: weapons whose default mag uses MagazineSizeSet (MagSize mul=0 bug surface)."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
items = (ROOT / "items.lua").read_text(encoding="utf-8")
inv = ROOT / "InventoryItem"

# Collect WeaponComponent ids that include MagazineSizeSet + their MagazineSize param
comp_set: dict[str, int] = {}
for m in re.finditer(
    r"PlaceObj\('ModItemWeaponComponent',\s*\{(.*?)\n\s*id = \"([^\"]+)\",",
    items,
    re.S,
):
    body, cid = m.group(1), m.group(2)
    if "MagazineSizeSet" not in body:
        continue
    vals = re.findall(r"'Name', \"MagazineSize\",\s*'Value', (\d+)", body)
    comp_set[cid] = int(vals[-1]) if vals else -1

print(f"MagazineSizeSet comps: {len(comp_set)}")

# Weapons with DefaultComponent in that set
hits = []
for path in sorted(inv.glob("*.lua")):
    text = path.read_text(encoding="utf-8")
    if "MagazineSize" not in text or "DefaultComponent" not in text:
        continue
    ms = re.search(r"MagazineSize = (\d+)", text)
    # Magazine slot default
    mslot = re.search(
        r"'SlotType', \"Magazine\".*?'DefaultComponent', \"([^\"]+)\"",
        text,
        re.S,
    )
    if not mslot:
        continue
    dc = mslot.group(1)
    if dc not in comp_set:
        continue
    hits.append((path.stem, ms.group(1) if ms else "?", dc, comp_set[dc]))

print("Weapons with MagSizeSet default mag:")
for wid, base, dc, n in hits:
    print(f"  {wid}: base={base} default={dc} Set={n}")

# Focus CAR15 / Glock18
for wid in ("CAR15", "Glock18"):
    row = next((h for h in hits if h[0] == wid), None)
    print(f"FOCUS {wid}:", row or "NO MagSizeSet default")
