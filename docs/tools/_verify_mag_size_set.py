# -*- coding: utf-8 -*-
from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
items = (root / "items.lua").read_text(encoding="utf-8")
print("MagazineSizeSet effect:", bool(re.search(r'id = "MagazineSizeSet"', items)))
print("ModificationType Set:", 'ModificationType = "Set"' in items)
print("MagLarge_50 defs:", len(re.findall(r'id = "JAZZ_MagLarge_50"', items)))
print("generic MagLarge id defs:", len(re.findall(r'id = "JAZZ_MagLarge"', items)))
# 30_45
idx = items.find('id = "JAZZ_MagLarge_30_45"')
print("30_45 found", idx > 0)
if idx > 0:
    chunk = items[idx - 800 : idx + 200]
    print("has MagazineSizeSet fx", "MagazineSizeSet" in chunk)
    m = re.search(r"'Name', \"MagazineSize\",\s*'Value', (\d+)", chunk)
    print("MagazineSize value", m.group(1) if m else None)
mult = re.findall(r'id = "(JAZZ_Mag[^"]+)".{0,1500}?MagazineSizeMultiplier', items, re.S)
print("Mag* with Multiplier", mult)
# delimiters
for a, b in [("(", ")"), ("{", "}"), ("[", "]")]:
    print(a, items.count(a) - items.count(b))
