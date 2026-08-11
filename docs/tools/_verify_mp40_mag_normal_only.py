# -*- coding: utf-8 -*-
from pathlib import Path
import re

jazz = Path(__file__).resolve().parents[2]
items = (jazz / "items.lua").read_text(encoding="utf-8")
mp40 = (jazz / "InventoryItem" / "MP40.lua").read_text(encoding="utf-8")
units = (jazz.parent / "jazz-units" / "items.lua").read_text(encoding="utf-8")
code = (jazz / "Code" / "System_WeaponComponent_Set.lua").read_text(encoding="utf-8")

assert "JAZZ_MagLarge_50_MP40" not in items
assert "JAZZ_MagLarge_50_MP40" not in mp40
assert "JAZZ_MagLarge_50_MP40" not in units
assert 'DefaultComponent", "JAZZ_MagNormal"' in mp40 or "DefaultComponent', \"JAZZ_MagNormal\"" in mp40
assert "JAZZ_MagNormal" in mp40
assert "JazzObsoleteMagazineReseat" in code
assert "JAZZ_MagLarge_50_MP40" in code  # reseat map key only

m = re.search(
    r"id = \"JAZZ_GenW_MP40_assault_m1_9x19_smg_ammo\"(.*?PlaceObj\('LootEntryLootDef')",
    units,
    re.S,
)
assert m and "LootEntryInventoryItem" in m.group(1) and "UpgradedWeapon" not in m.group(1)
print("OK MP40 MagNormal-only + loot + reseat")
