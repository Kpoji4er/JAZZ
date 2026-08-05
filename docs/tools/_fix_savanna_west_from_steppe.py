# -*- coding: utf-8 -*-
"""Restore western A9–A12 / B9–B12 / C8–C12 to GreatDesert; trim MountainSteppe; drop D11–D12 overlap."""
from __future__ import annotations

import re
from pathlib import Path

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
ITEMS = JAZZ / "items.lua"


def sector_list(ranges):
    out = []
    for col, a, b in ranges:
        for n in range(a, b + 1):
            out.append(f"{col}{n}")
    return out


def fmt_sectors(sectors, indent="\t\t\t\t\t"):
    return ",\n".join(f'{indent}"{s}"' for s in sectors)


def replace_region_sectors(text: str, region_id: str, sectors: list[str]) -> str:
    """Replace Sectors={} only inside the PlaceObj that ends with id = region_id."""
    id_pat = f'\tid = "{region_id}",'
    # find id line with region tabs
    needle = f'\t\t\t\tid = "{region_id}",'
    i = text.find(needle)
    if i < 0:
        raise SystemExit(f"id {region_id} not found")
    start = text.rfind("PlaceObj('ModItemRegion'", 0, i)
    if start < 0:
        raise SystemExit(f"PlaceObj for {region_id} not found")
    block = text[start:i]
    sm = re.search(r"(Sectors = \{).*?(\n\t\t\t\t\},)", block, re.S)
    if not sm:
        raise SystemExit(f"Sectors block missing in {region_id}")
    abs_a = start + sm.start(1)
    abs_b = start + sm.end(2)
    replacement = "Sectors = {\n" + fmt_sectors(sectors) + ",\n\t\t\t\t},"
    return text[:abs_a] + replacement + text[abs_b:]


def main():
    gd = (
        sector_list(
            [
                ("A", 1, 12),
                ("B", 4, 12),
                ("C", 6, 12),
                ("D", 7, 12),
            ]
        )
        + ["E10"]
        + sector_list(
            [
                ("F", 8, 12),
                ("G", 9, 12),
                ("H", 10, 13),
                ("I", 11, 13),
                ("J", 12, 13),
            ]
        )
    )
    ms = sector_list(
        [
            ("A", 13, 20),
            ("B", 13, 20),
            ("C", 13, 20),
            ("D", 13, 20),
            ("E", 12, 20),
            ("F", 19, 19),
        ]
    )
    assert "D18" in ms and "A10" in gd and "A10" not in ms
    assert not (set(gd) & set(ms)), sorted(set(gd) & set(ms))

    text = ITEMS.read_text(encoding="utf-8")
    text = replace_region_sectors(text, "GreatDesert", gd)
    text = replace_region_sectors(text, "MountainSteppe", ms)
    ITEMS.write_text(text, encoding="utf-8")
    print(f"GreatDesert n={len(gd)}; MountainSteppe n={len(ms)}; overlap=0")


if __name__ == "__main__":
    main()
