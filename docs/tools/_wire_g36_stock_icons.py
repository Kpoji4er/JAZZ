"""Wire G36 MagNormal Stock Visual → Stock/G36_Stock_Normal.png (Style B)."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Stock/G36_Stock_Normal.png"
MARKER = 'id = "JAZZ_StockNormal"'


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    old = (
        'ApplyTo = "G36",\n'
        '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_StockHKG36_01",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",'
    )
    new = (
        'ApplyTo = "G36",\n'
        '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_StockHKG36_01",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",'
    )
    if ICON in body and 'ApplyTo = "G36"' in body and "WeaponAttA_StockHKG36_01" in body:
        # check icon already on this visual
        i = body.find('ApplyTo = "G36"')
        while i >= 0:
            win = body[i : i + 280]
            if "WeaponAttA_StockHKG36_01" in win and ICON in win:
                print("already")
                break
            i = body.find('ApplyTo = "G36"', i + 1)
        else:
            if old not in body:
                raise SystemExit("needle missing")
            body = body.replace(old, new, 1)
            print("ok")
    elif old in body:
        body = body.replace(old, new, 1)
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
