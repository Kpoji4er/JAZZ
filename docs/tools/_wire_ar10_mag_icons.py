"""Insert MagNormal Visuals for AR10 + AR10DMR → Magazine/AR10_Mag20.png.

AR10 has no Magazine slot (mag in mesh). Not shared with M14 (different entities / rock-and-lock).
"""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Magazine/AR10_Mag20.png"
MARKER = 'id = "JAZZ_MagNormal"'


def block(apply: str) -> str:
    return (
        "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
        f'\t\t\t\t\t\t\t\tApplyTo = "{apply}",\n'
        '\t\t\t\t\t\t\t\tEntity = "",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",\n'
        "\t\t\t\t\t\t\t\tparam_bindings = false,\n"
        "\t\t\t\t\t\t\t}),\n"
    )


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    for apply in ("AR10", "AR10DMR"):
        if f'ApplyTo = "{apply}"' in body and "AR10_Mag20" in body:
            print(apply, "already")
            continue
        inserted = False
        for key in (
            'ApplyTo = "AR15"',
            'ApplyTo = "AK74"',
            'ApplyTo = "AK47"',
            'ApplyTo = "AN94"',
            'ApplyTo = "AVT40"',
        ):
            needle = (
                "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
                f"\t\t\t\t\t\t\t\t{key},"
            )
            i = body.find(needle)
            if i >= 0:
                body = body[:i] + block(apply) + body[i:]
                print(apply, "ok near", key)
                inserted = True
                break
        if not inserted:
            raise SystemExit(f"{apply} insert point missing")
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
