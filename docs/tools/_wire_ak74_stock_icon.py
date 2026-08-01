"""Wire AK74 wooden stock Icon on JAZZ_StockNormal ApplyTo=AK74."""
from __future__ import annotations

from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Stock/AK74_StockNormal.png"
MARKER = 'id = "JAZZ_StockNormal"'
OLD = (
    'ApplyTo = "AK74",\n'
    '\t\t\t\t\t\t\t\tEntity = "AK74FullStock",\n'
    '\t\t\t\t\t\t\t\tSlot = "Stock",'
)
NEW = (
    'ApplyTo = "AK74",\n'
    '\t\t\t\t\t\t\t\tEntity = "AK74FullStock",\n'
    f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
    '\t\t\t\t\t\t\t\tSlot = "Stock",'
)


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    if end < 0:
        raise SystemExit("StockNormal missing")
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if OLD not in body:
        i = body.find("AK74FullStock")
        print(repr(body[max(0, i - 100) : i + 160]))
        raise SystemExit("needle missing")
    if ICON in body:
        print("already wired")
        return
    nbody = body.replace(OLD, NEW, 1)
    ITEMS.write_text(text[:start] + nbody + rest, encoding="utf-8", newline="\n")
    print("wired", ICON)


if __name__ == "__main__":
    main()
