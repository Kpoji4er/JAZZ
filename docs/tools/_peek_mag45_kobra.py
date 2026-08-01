# -*- coding: utf-8 -*-
from pathlib import Path
import re

t = Path("items.lua").read_text(encoding="utf-8")
for cid in [
    "JAZZ_MagLarge_30_45",
    "JAZZ_Reflex_Kobra",
    "JAZZ_Reflex_Closed",
    "JAZZ_Reflex_Open",
    "JAZZ_Reflex_Eotech",
]:
    i = t.find(f'id = "{cid}"')
    print("===", cid, i)
    if i < 0:
        continue
    start = t.rfind("PlaceObj('ModItemWeaponComponent'", 0, i)
    block = t[start : i + 120]
    m = re.search(r"ModificationEffects = \{(.*?)\}", block, re.S)
    print("effects", re.findall(r'"([^"]+)"', m.group(1)) if m else None)
    print("params", re.findall(r"'Name',\s*\"(\w+)\"", block)[:15])
    m = re.search(r"Description = T\((\d+),\s*--[[.*?]]\s*\"(.*?)\"\)", block, re.S)
    if not m:
        m = re.search(r'Description = T\((\d+).*?"((?:\\.|[^"\\])*)"', block, re.S)
    print("desc", m.group(2)[:160] if m else None)

# CloseRange effect descriptions
for eid in ["IncreaseCloseRange", "CloseRangeBonus", "CloseRangeFactorIncrease", "ReduceCloseRange"]:
    i = t.find(f'id = "{eid}"')
    if i < 0:
        continue
    start = t.rfind("PlaceObj('ModItemWeaponComponentEffect'", 0, i)
    block = t[start : i + 40]
    m = re.search(r'Description = T\((\d+).*?"((?:\\.|[^"\\])*)"', block, re.S)
    print("EFFECT", eid, "->", m.group(2)[:120] if m else None)
