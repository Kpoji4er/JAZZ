"""Find InitialSquads by sectorId in jazz-maps."""
from __future__ import annotations

import re
from pathlib import Path

t = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\items.lua").read_text(
    encoding="utf-8"
)
for sid in ["M4", "M5", "M6", "I2", "I3", "I4", "L1", "L2", "L6", "L6_Underground", "I7"]:
    matches = list(
        re.finditer(
            rf"'sectorId', \"{sid}\"[\s\S]{{0,2500}}?'InitialSquads', \{{([\s\S]*?)\}},",
            t,
        )
    )
    print(f"=== {sid} matches={len(matches)} ===")
    for m in matches:
        packs = re.findall(r'"([^"]+)"', m.group(1))
        print(" ", packs)
