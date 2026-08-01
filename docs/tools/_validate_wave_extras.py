# -*- coding: utf-8 -*-
from pathlib import Path
import csv
import re

root = Path(".")
rows = list(csv.DictReader((root / "docs/technical/weapons/data/weapons.csv").open(encoding="utf-8")))
for wid in ["TexRevolver", "LionRoar", "Winchester_Quest", "Galil_FlagHill", "GoldenGun", "Auto5_quest"]:
    r = next(x for x in rows if x["id"] == wid)
    candidates = [
        root / "InventoryItem" / f"{wid}.lua",
        root / "InventoryItem" / "vanillunique" / f"{wid}.lua",
    ]
    found = next((p for p in candidates if p.exists()), None)
    print(wid, "csv_mass=", r.get("weapon_mass"), "file=", found)
    if found:
        t = found.read_text(encoding="utf-8")
        print("  WeaponMass=", "WeaponMass" in t, "Recoil=", "Recoil" in t)

items = (root / "items.lua").read_text(encoding="utf-8")
for cid in ["FineSteelPipe", "OpticalLens", "Microchip", "JAZZ_BarrelParts", "JAZZ_RemovableAttachment"]:
    print(cid, "mentions", items.count(cid), "id=", len(re.findall(rf'id = "{cid}"', items)))
for wid in ["LionRoar", "TexRevolver", "GoldenGun"]:
    m = re.search(rf'id = "{wid}"', items)
    if not m:
        print(wid, "no ModItem id in items.lua")
        continue
    start = items.rfind("PlaceObj(", 0, m.start())
    block = items[start : m.end() + 50]
    print(wid, "WeaponMass in ModItem", "WeaponMass" in block)
