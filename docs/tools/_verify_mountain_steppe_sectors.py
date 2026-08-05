# -*- coding: utf-8 -*-
from pathlib import Path
import re

t = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\items.lua").read_text(encoding="utf-8")
for rid in ["GreatDesert", "MountainSteppe"]:
    i = t.find(f'id = "{rid}"')
    assert i > 0, rid
    start = t.rfind("PlaceObj('ModItemRegion'", 0, i)
    block = t[start:i]
    part = block.split("Sectors")[1].split("Shipment")[0]
    secs = re.findall(r'"([A-P]\d+)"', part)
    print(
        rid,
        "n=",
        len(secs),
        "A10",
        "A10" in secs,
        "A12",
        "A12" in secs,
        "A13",
        "A13" in secs,
        "C8",
        "C8" in secs,
        "D10",
        "D10" in secs,
        "D18",
        "D18" in secs,
        "E10",
        "E10" in secs,
    )
