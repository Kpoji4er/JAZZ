# -*- coding: utf-8 -*-
from pathlib import Path
import re

t = Path("items.lua").read_text(encoding="utf-8")
# Mag45 full params with values
i = t.find('id = "JAZZ_MagLarge_30_45"')
start = t.rfind("PlaceObj('ModItemWeaponComponent'", 0, i)
block = t[start:i+40]
print(block[block.find("ModificationEffects"):block.find("Visuals") if "Visuals" in block else block.find("AdditionalCosts")])
print("---")
for name in ["IncreaseReloadAP", "CloseRangeFactorIncrease", "CloseRangeFactorDecrease", "CloseRangeIncrease", "CloseRangeDecrease"]:
    i = t.find(f'id = "{name}"')
    start = t.rfind("PlaceObj('ModItemWeaponComponentEffect'", 0, i)
    block = t[start:i+30]
    m = re.search(r"Description = T\((\d+),\s*--\[\[.*?\]\]\s*\"((?:\\.|[^\"\\])*)\"", block, re.S)
    print(name, m.group(1) if m else None, m.group(2) if m else None)

# find Kobra by DisplayName
for m in re.finditer(r'DisplayName = T\(\d+,\s*--\[\[.*?\]\]\s*\"([^\"]*Кобра[^\"]*)\"', t):
    nearby = t[max(0,m.start()-500):m.start()+200]
    idm = re.search(r'id = \"(JAZZ_[^\"]+)\"', nearby[nearby.rfind("PlaceObj"):] if False else t[m.start():m.start()+2500])
    # search forward for id
    idm = re.search(r'\nid = \"(JAZZ_[^\"]+)\"', t[m.start():m.start()+4000])
    print("Kobra display", m.group(1), "id", idm.group(1) if idm else "?")
