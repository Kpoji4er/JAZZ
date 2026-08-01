# -*- coding: utf-8 -*-
from pathlib import Path
import re

items = Path("items.lua").read_text(encoding="utf-8")
meta = Path("metadata.lua").read_text(encoding="utf-8")
companions = [
    "InventoryItem/JAZZ_BarrelParts.lua",
    "InventoryItem/JAZZ_RemovableAttachment.lua",
    "InventoryItem/FineSteelPipe.lua",
    "InventoryItem/OpticalLens.lua",
    "InventoryItem/Microchip.lua",
    "InventoryItem/Parts.lua",
    "InventoryItem/M72LAW.lua",
    "InventoryItem/AK74.lua",
    "InventoryItem/vanillunique/LionRoar.lua",
]
for c in companions:
    p = Path(c)
    cid = p.stem
    has_id = bool(re.search(rf"'Id',\s*\"{re.escape(cid)}\"", items))
    print(f"{cid}: companion={p.exists()} Id={has_id}")
for f in [
    "System_WeaponComponent_Set.lua",
    "System_WeaponResourceMaintenance.lua",
    "System_WeaponRemovableModify.lua",
    "System_DisposableLaunchers.lua",
    "System_ReloadStyle.lua",
]:
    print(f"metadata loads {f}: {f in meta}")

# key wave loc IDs parity RU/EN
ids = ["543656846802", "990002001", "990002002", "990002003", "990002004", "990002010", "990002011", "990002012", "253479657834"]
ru = Path("Russian.csv").read_text(encoding="utf-8")
en = Path("English.csv").read_text(encoding="utf-8")
for i in ids:
    print(f"loc {i}: RU={i in ru} EN={i in en}")
