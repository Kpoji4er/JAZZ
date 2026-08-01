"""Wire JAZZ_IronSight ApplyTo=P210 → vanilla ironsights Icon."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "UI/Icons/Upgrades/ironsights"
MARKER = 'id = "JAZZ_IronSight"'
OLD = (
    'ApplyTo = "P210",\n'
    '\t\t\t\t\t\t\t\tEntity = "P210Sight",\n'
    '\t\t\t\t\t\t\t\tSlot = "Scope",'
)
NEW = (
    'ApplyTo = "P210",\n'
    '\t\t\t\t\t\t\t\tEntity = "P210Sight",\n'
    f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
    '\t\t\t\t\t\t\t\tSlot = "Scope",'
)


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    if end < 0:
        raise SystemExit("missing IronSight")
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if f'Icon = "{ICON}"' in body and 'Entity = "P210Sight"' in body:
        # check that Icon is on that block
        i = body.find('Entity = "P210Sight"')
        chunk = body[max(0, i - 80) : i + 120]
        if ICON in chunk:
            print("already wired")
            return
    if OLD not in body:
        i = body.find("P210Sight")
        print(repr(body[max(0, i - 100) : i + 160]))
        raise SystemExit("needle missing")
    body = body.replace(OLD, NEW, 1)
    tmp = ITEMS.with_suffix(".lua.tmp")
    tmp.write_text(text[:start] + body + rest, encoding="utf-8", newline="\n")
    for _ in range(15):
        try:
            os.replace(tmp, ITEMS)
            break
        except OSError:
            time.sleep(0.4)
    else:
        raise SystemExit("items.lua locked")
    print("wired", ICON)


if __name__ == "__main__":
    main()
