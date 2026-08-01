"""Wire MP40 MagNormal → Magazine/MP40_Mag32.png (replace magpictures)."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Magazine/MP40_Mag32.png"
OLD_ICON = "Mod/e6L4ECj/magpictures/MP40_mag_normal.png"
MARKER = 'id = "JAZZ_MagNormal"'


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if ICON in body and "MP40" in body:
        print("already")
    elif OLD_ICON in body:
        # only on MP40 visual — replace Icon line near MP40
        old = (
            'ApplyTo = "MP40",\n'
            '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineMP40_01",\n'
            f'\t\t\t\t\t\t\t\tIcon = "{OLD_ICON}",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",'
        )
        new = (
            'ApplyTo = "MP40",\n'
            '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineMP40_01",\n'
            f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",'
        )
        if old not in body:
            raise SystemExit("needle missing")
        body = body.replace(old, new, 1)
        print("ok")
    else:
        raise SystemExit("no MP40 icon path")
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
