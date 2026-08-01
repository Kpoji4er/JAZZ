# -*- coding: utf-8 -*-
from pathlib import Path
import re
t = Path("items.lua").read_text(encoding="utf-8")
# Find blocks that contain Slot = "Stock" and extract id + costs
pos = 0
while True:
    i = t.find('Slot = "Stock"', pos)
    if i < 0:
        break
    start = t.rfind("PlaceObj('ModItemWeaponComponent'", 0, i)
    end = t.find("PlaceObj('ModItemWeaponComponent'", i + 1)
    if end < 0:
        end = i + 4000
    block = t[start:end]
    im = re.search(r'id = "([^"]+)"', block)
    costs = re.findall(r"'Type',\s*\"([^\"]+)\"", block)
    amounts = re.findall(r"'Amount',\s*(\d+)", block)
    cost_field = re.search(r'\n\t+Cost = (\d+)', block)
    slot = "Stock"
    # also check if Slot is really Stock for this component (might match Visual Slot)
    if 'Slot = "Stock"' in block[block.rfind("comment") if "comment" in block else 0:]:
        pass
    cid = im.group(1) if im else "?"
    if "Stock" in cid or re.search(r'\n\t+Slot = "Stock"', block):
        # prefer component-level Slot near end
        if re.search(r'\n\t+Slot = "Stock"', block) or "Stock" in cid:
            print(cid, "Cost=", cost_field.group(1) if cost_field else "?", "Types=", list(zip(costs, amounts))[:6])
    pos = i + 1
