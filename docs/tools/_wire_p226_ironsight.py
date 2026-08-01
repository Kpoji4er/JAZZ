"""Wire JAZZ_IronSight ApplyTo=P226 (rear) → Optics/P226_IronSight.png."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Optics/P226_IronSight.png"
MARKER = 'id = "JAZZ_IronSight"'
OLD = (
    'ApplyTo = "P226",\n'
    '\t\t\t\t\t\t\t\tEntity = "P226SightsR",\n'
    '\t\t\t\t\t\t\t\tSlot = "Sightsr",'
)
NEW = (
    'ApplyTo = "P226",\n'
    '\t\t\t\t\t\t\t\tEntity = "P226SightsR",\n'
    f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
    '\t\t\t\t\t\t\t\tSlot = "Sightsr",'
)


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    if end < 0:
        raise SystemExit("missing IronSight")
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if NEW in body or (ICON in body and "P226SightsR" in body):
        print("already")
    elif OLD not in body:
        raise SystemExit("needle missing")
    else:
        body = body.replace(OLD, NEW, 1)
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
