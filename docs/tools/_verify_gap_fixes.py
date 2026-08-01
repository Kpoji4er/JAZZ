# -*- coding: utf-8 -*-
from pathlib import Path
import re

t = Path("items.lua").read_text(encoding="utf-8")
for cid in ["FineSteelPipe", "OpticalLens", "Microchip", "JAZZ_BarrelParts", "Parts"]:
    print(cid, "Id count", len(re.findall(rf"'Id',\s*\"{cid}\"", t)))
print("Type FineSteel leftover", len(re.findall(r"'Type',\s*\"FineSteelPipe\"", t)))
print("bad Parts+optical", bool(re.search(r"'Id',\s*\"Parts\".{0,200}optical_lens", t, re.S)))
print("bad Parts+microchip", bool(re.search(r"'Id',\s*\"Parts\".{0,200}microchip", t, re.S)))
# FineSteelPipe shop
m = re.search(r"'Id',\s*\"FineSteelPipe\".{0,500}CanAppearInShop',\s*(true|false)", t, re.S)
print("FineSteelPipe CanAppearInShop", m.group(1) if m else None)
# AK74 recoil still in items?
m = re.search(r"'Id',\s*\"AK74\".{0,2500}'Recoil',\s*(\d+)", t, re.S)
print("AK74 Recoil in items", m.group(1) if m else None)
# unique companions
for wid in ["LionRoar", "TexRevolver"]:
    p = Path("InventoryItem/vanillunique") / f"{wid}.lua"
    text = p.read_text(encoding="utf-8")
    print(wid, "WeaponMass" in text, re.search(r"WeaponMass\s*=\s*(\d+)", text).group(1))
