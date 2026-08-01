"""Wire MAT49 MagNormal → Magazine/MAT49_Mag32.png."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Magazine/MAT49_Mag32.png"
MARKER = 'id = "JAZZ_MagNormal"'
OLD = (
    'ApplyTo = "MAT49",\n'
    '\t\t\t\t\t\t\t\tEntity = "MAT49Mag",\n'
    '\t\t\t\t\t\t\t\tSlot = "Magazine",'
)
NEW = (
    'ApplyTo = "MAT49",\n'
    '\t\t\t\t\t\t\t\tEntity = "MAT49Mag",\n'
    f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
    '\t\t\t\t\t\t\t\tSlot = "Magazine",'
)


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    n = body.count(OLD)
    if n == 0:
        if ICON in body:
            print("already")
        else:
            raise SystemExit("needle missing")
    else:
        body = body.replace(OLD, NEW)
        print(f"ok x{n}")
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
