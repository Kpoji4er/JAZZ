# -*- coding: utf-8 -*-
from pathlib import Path
import re

fixes = {
    "Winchester_Quest": "Tube",
    "Auto5_quest": "Tube",
    "TexRevolver": "Revolver",
}
for wid, style in fixes.items():
    path = Path("InventoryItem/vanillunique") / f"{wid}.lua"
    text = path.read_text(encoding="utf-8")
    if re.search(r"ReloadStyle\s*=", text):
        text2 = re.sub(r'ReloadStyle\s*=\s*"[^"]+"', f'ReloadStyle = "{style}"', text, count=1)
    else:
        text2 = re.sub(r"(\n\tWeaponMass\s*=)", rf'\n\tReloadStyle = "{style}",\1', text, count=1)
        if text2 == text:
            text2 = re.sub(r"(\n\tRecoil\s*=)", rf'\n\tReloadStyle = "{style}",\1', text, count=1)
    if text2 != text:
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(text2)
        print("set", wid, style)
    else:
        print("unchanged", wid)

items = Path("items.lua").read_text(encoding="utf-8")
for old in ("FineSteelPipe", "OpticalLens", "Microchip"):
    print(old, "quoted leftovers", len(re.findall(rf"['\"]{old}['\"]", items)))
