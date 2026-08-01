"""Wire JAZZ_BarrelNormal Icon (style B) + ChipIcon."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Barrel/JAZZ_BarrelNormal.png"
CHIP = "Mod/e6L4ECj/Icons/Upgrades/Chips/JAZZ_BarrelNormal.png"
MARKER = 'id = "JAZZ_BarrelNormal"'


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    if end < 0:
        raise SystemExit("missing BarrelNormal")
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]

    old_icon = 'Icon = "UI/Icons/Upgrades/default_barrel",'
    new_icon = f'Icon = "{ICON}",'
    if ICON in body.split("Visuals")[0]:
        print("Icon already")
    elif old_icon in body:
        # only first Icon in header (before Visuals)
        head, vis = body.split("Visuals", 1)
        if old_icon not in head:
            raise SystemExit("header Icon missing")
        head = head.replace(old_icon, new_icon, 1)
        body = head + "Visuals" + vis
        print("Icon ok")
    else:
        raise SystemExit("default_barrel Icon not found")

    head, vis = body.split("Visuals", 1)
    chip_line = f'\t\t\t\t\tChipIcon = "{CHIP}",\n'
    if "ChipIcon" in head:
        print("Chip already")
    else:
        # after Icon line
        if new_icon in head:
            head = head.replace(new_icon + "\n", new_icon + "\n" + chip_line, 1)
        else:
            raise SystemExit("cannot insert ChipIcon")
        body = head + "Visuals" + vis
        print("Chip ok")

    tmp = ITEMS.with_suffix(".lua.tmp")
    tmp.write_text(text[:start] + body + rest, encoding="utf-8", newline="\n")
    for _ in range(25):
        try:
            os.replace(tmp, ITEMS)
            print("done")
            return
        except OSError:
            time.sleep(0.3)
    raise SystemExit("locked")


if __name__ == "__main__":
    main()
