# -*- coding: utf-8 -*-
from pathlib import Path
import re

# Mag45 block
t = Path("items.lua").read_text(encoding="utf-8")
i = t.find('id = "JAZZ_MagLarge_30_45"')
start = t.rfind("PlaceObj('ModItemWeaponComponent'", 0, i)
block = t[start:i+20]
print(block[:2500])
print("---")

# Search IncreaseReloadAP anywhere in jazz
for pat in ["IncreaseReloadAP", "ReduceReloadAP", "ReloadAPIncrease", "ReloadAPDecrease"]:
    print(pat, "count in items", t.count(pat))

# metadata resources for effects
meta = Path("metadata.lua").read_text(encoding="utf-8")
for pat in ["IncreaseReloadAP", "ReduceReloadAP"]:
    print(pat, "in metadata", pat in meta)

# check if jazz overrides the effect
for p in Path("Code").glob("*.lua"):
    txt = p.read_text(encoding="utf-8", errors="ignore")
    if "IncreaseReloadAP" in txt or "ReloadAPIncrease" in txt:
        print("code hit", p.name)
