# -*- coding: utf-8 -*-
from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
items = (root / "items.lua").read_text(encoding="utf-8")

# paren balance ignoring strings roughly via apply helper
print("raw paren", items.count("(") - items.count(")"))
print("raw brace", items.count("{") - items.count("}"))

# Find MagLarge_30_45 via id line then walk backwards to PlaceObj
idx = items.find('id = "JAZZ_MagLarge_30_45"')
assert idx > 0
start = items.rfind("PlaceObj('ModItemWeaponComponent'", 0, idx)
print("start", start)
block = items[start : idx + 80]
print(block)
print("---")
print("MagazineSizeSet in block", "MagazineSizeSet" in block)
print(re.findall(r"'Name', \"MagazineSize\",\s*'Value', (\d+)", block))

# Check MagLarge_50
idx2 = items.find('id = "JAZZ_MagLarge_50"')
start2 = items.rfind("PlaceObj('ModItemWeaponComponent'", 0, idx2)
block2 = items[start2 : idx2 + 80]
print("\n=== MagLarge_50 ===")
print(block2[:900])
