# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
items = ROOT / "items.lua"
t = items.read_text(encoding="utf-8")
t = t.replace('"StockLightFolded"', '"JAZZ_StockLightFolded"')
t = t.replace('"StockLightUnFolded"', '"JAZZ_StockLightUnFolded"')


def inject(m: re.Match) -> str:
    body = m.group(0)
    if "JAZZ_FlashlightOff" in body:
        return body
    if '"JAZZ_Flashlight"' not in body:
        return body
    return body.replace(
        '"JAZZ_Flashlight",',
        '"JAZZ_Flashlight",\n\t\t\t\t\t\t\t\t"JAZZ_FlashlightOff",',
        1,
    )


t = re.sub(r"'AvailableComponents',\s*\{[^}]*\}", inject, t, flags=re.S)
items.write_text(t, encoding="utf-8")
print("FlashlightOff in items", t.count("JAZZ_FlashlightOff"))

for rel in (ROOT / "InventoryItem").glob("*.lua"):
    tt = rel.read_text(encoding="utf-8")
    if "JAZZ_Flashlight" not in tt or "JAZZ_FlashlightOff" in tt:
        continue
    if '"JAZZ_Flashlight",' not in tt:
        continue
    tt2 = tt.replace(
        '"JAZZ_Flashlight",',
        '"JAZZ_Flashlight",\n\t\t\t\t"JAZZ_FlashlightOff",',
        1,
    )
    if tt2 != tt:
        rel.write_text(tt2, encoding="utf-8")
        print("companion", rel.name)
