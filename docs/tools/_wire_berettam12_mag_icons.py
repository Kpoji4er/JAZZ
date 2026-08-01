"""Wire MagNormal ApplyTo BerettaM12 → Magazine/BerettaM12_Mag32.png."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Magazine/BerettaM12_Mag32.png"


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find('id = "JAZZ_MagNormal"')
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    old = (
        'ApplyTo = "BerettaM12",\n'
        '\t\t\t\t\t\t\t\tEntity = "BerettaM12Mag",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",'
    )
    new = (
        'ApplyTo = "BerettaM12",\n'
        '\t\t\t\t\t\t\t\tEntity = "BerettaM12Mag",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",'
    )
    if ICON in body and 'ApplyTo = "BerettaM12"' in body:
        print("already")
    elif old not in body:
        raise SystemExit("needle missing")
    else:
        body = body.replace(old, new, 1)
        print("ok")
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
