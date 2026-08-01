"""Wire FAMAS MagNormal → Magazine/FAMAS_Mag25.png (Style B)."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Magazine/FAMAS_Mag25.png"
MARKER = 'id = "JAZZ_MagNormal"'
OLD = (
    'ApplyTo = "FAMAS",\n'
    '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineFAMAS",\n'
    '\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/expanded_FAMAS_magazine",\n'
    '\t\t\t\t\t\t\t\tSlot = "Magazine",'
)
NEW = (
    'ApplyTo = "FAMAS",\n'
    '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineFAMAS",\n'
    f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
    '\t\t\t\t\t\t\t\tSlot = "Magazine",'
)


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if ICON in body and 'ApplyTo = "FAMAS"' in body:
        print("already")
    elif OLD in body:
        body = body.replace(OLD, NEW, 1)
        print("ok")
    else:
        raise SystemExit("needle missing")
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
