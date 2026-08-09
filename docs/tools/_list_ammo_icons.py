# -*- coding: utf-8 -*-
"""List Ammo ModItemInventoryItemCompositeDef from items.lua."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
AMMOPICS = ROOT / "Ammopics"


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8", errors="replace")
    # Each ammo ModItem starts here; take a window forward for fields.
    starts = [
        m.start()
        for m in re.finditer(r"PlaceObj\('ModItemInventoryItemCompositeDef'", text)
    ]
    rows: list[tuple[str, str, str, str]] = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else min(len(text), start + 8000)
        chunk = text[start:end]
        if not re.search(r"'object_class',\s*\"Ammo\"", chunk):
            continue
        mid = re.search(r"'Id',\s*\"([^\"]+)\"", chunk)
        cal = re.search(r"'Caliber',\s*\"([^\"]+)\"", chunk)
        icon = re.search(r"'Icon',\s*\"([^\"]+)\"", chunk)
        disp = re.search(
            r"'DisplayName',\s*T\([^)]*?\"([^\"]*)\"",
            chunk,
            re.S,
        )
        if not mid:
            continue
        rows.append(
            (
                cal.group(1) if cal else "?",
                mid.group(1),
                disp.group(1) if disp else "",
                icon.group(1) if icon else "",
            )
        )

    rows.sort(key=lambda r: (r[0], r[1]))
    print(f"TOTAL {len(rows)}")
    cur = None
    for cal, iid, dn, icon in rows:
        if cal != cur:
            cur = cal
            print(f"\n## {cal}")
        fname = icon.rsplit("/", 1)[-1] if icon else ""
        exists = ""
        if fname:
            exists = "OK" if (AMMOPICS / fname).exists() else "MISSING"
        print(f"- {iid}\t{dn}\t{fname}\t{exists}")


if __name__ == "__main__":
    main()
