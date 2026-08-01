# -*- coding: utf-8 -*-
"""Rewrite mistaken ModItemInventoryItemCompositeDef stubs in metadata.lua as ModResourcePreset."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "metadata.lua"


def main() -> int:
    text = META.read_text(encoding="utf-8")
    pat = re.compile(
        r"\n\t\t\t-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-BEGIN\n"
        r".*?"
        r"\n\t\t\t-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-END\n",
        re.S,
    )
    m = pat.search(text)
    if not m:
        # already fixed?
        if "-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-BEGIN" in text and "ModResourcePreset" in text[
            text.find("-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-BEGIN") : text.find(
                "-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-END"
            )
            + 10
        ]:
            print("already ModResourcePreset form")
            return 0
        raise SystemExit("removable items metadata block not found")

    block = m.group(0)
    ids = re.findall(r"'Id', \"([^\"]+)\"", block)
    print("rewriting", len(ids), "ModResourcePreset entries")
    lines = []
    for cid in ids:
        lines.append("\t\tPlaceObj('ModResourcePreset', {")
        lines.append('\t\t\t\'Class\', "InventoryItemCompositeDef",')
        lines.append(f'\t\t\t\'Id\', "{cid}",')
        lines.append('\t\t\t\'ClassDisplayName\', "Inventory item",')
        lines.append("\t\t}),")
    new = (
        "\n\t\t-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-BEGIN\n"
        + "\n".join(lines)
        + "\n\t\t-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-END\n"
    )
    META.write_text(text[: m.start()] + new + text[m.end() :], encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
