"""Wire JAZZ_Handgrip_Ergo ApplyTo=P210 Icon."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Handgrip/P210_Handgrip_Ergo.png"
MARKER = 'id = "JAZZ_Handgrip_Ergo"'
OLD = (
    'ApplyTo = "P210",\n'
    '\t\t\t\t\t\t\t\tEntity = "P210HandGripSport",\n'
    '\t\t\t\t\t\t\t\tSlot = "Handgrip",'
)
NEW = (
    'ApplyTo = "P210",\n'
    '\t\t\t\t\t\t\t\tEntity = "P210HandGripSport",\n'
    f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
    '\t\t\t\t\t\t\t\tSlot = "Handgrip",'
)


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if ICON in body and "P210HandGripSport" in body:
        print("already")
        return
    if OLD not in body:
        i = body.find("P210HandGripSport")
        print(repr(body[max(0, i - 80) : i + 120]))
        raise SystemExit("missing")
    body = body.replace(OLD, NEW, 1)
    tmp = ITEMS.with_suffix(".lua.tmp")
    tmp.write_text(text[:start] + body + rest, encoding="utf-8", newline="\n")
    for _ in range(20):
        try:
            os.replace(tmp, ITEMS)
            print("wired", ICON)
            return
        except OSError:
            time.sleep(0.3)
    raise SystemExit("locked")


if __name__ == "__main__":
    main()
