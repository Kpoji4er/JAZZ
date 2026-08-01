"""Add component Icon on JAZZ_IronSight_AIM if missing."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
MARKER = 'id = "JAZZ_IronSight_AIM"'
COMP = "UI/Icons/Upgrades/ironsights_hands"


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    head = body.split("Visuals", 1)[0]
    if f'Icon = "{COMP}"' in head:
        print("already")
        return
    # ChipIcon line is oddly indented with fewer tabs
    needle = 'ChipIcon = "Mod/e6L4ECj/Icons/Upgrades/Chips/JAZZ_IronSight_AIM.png"'
    if needle not in body:
        raise SystemExit("chip missing")
    body = body.replace(
        needle,
        f'Icon = "{COMP}",\n\t\t\t\t\t{needle}',
        1,
    )
    tmp = ITEMS.with_suffix(".lua.tmp")
    tmp.write_text(text[:start] + body + rest, encoding="utf-8", newline="\n")
    for _ in range(20):
        try:
            os.replace(tmp, ITEMS)
            print("ok")
            return
        except OSError:
            time.sleep(0.3)
    raise SystemExit("locked")


if __name__ == "__main__":
    main()
