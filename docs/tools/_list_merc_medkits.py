# -*- coding: utf-8 -*-
"""List merc Medicine kits from jazz-units Mercs loot defs."""
from __future__ import annotations

import re
import sys
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
KITS = ("FirstAidKit", "Medkit", "Reanimationsset")
OUT = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\docs\tools\_merc_medkits_list.txt")


def extract_loot_blocks(text: str) -> list[tuple[str, str, str]]:
    """Return (id, group, block) for ModItemLootDef."""
    results = []
    for m in re.finditer(r"PlaceObj\('ModItemLootDef',\s*\{", text):
        start = m.end()
        depth = 1
        i = start
        while i < len(text) and depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        block = text[start : i - 1]
        idm = re.search(r"\bid\s*=\s*\"([^\"]+)\"", block)
        gm = re.search(r"\bgroup\s*=\s*\"([^\"]+)\"", block)
        if idm:
            results.append((idm.group(1), gm.group(1) if gm else "", block))
    return results


def kits_in_block(block: str) -> list[str]:
    found = []
    for kit in KITS:
        for em in re.finditer(
            rf"item\s*=\s*\"{kit}\"[^}}]{{0,200}}",
            block,
        ):
            chunk = em.group(0)
            smin = re.search(r"stack_min\s*=\s*(\d+)", chunk)
            smax = re.search(r"stack_max\s*=\s*(\d+)", chunk)
            # one-liner PlaceObj(... stack_min = N, stack_max = M)
            if not smin:
                smin = re.search(rf'item = "{kit}", stack_min = (\d+), stack_max = (\d+)', block)
                if smin:
                    found.append(f"{kit} x{smin.group(1)}-{smin.group(2)}")
                    continue
            a = smin.group(1) if smin else "?"
            b = smax.group(1) if smax else a
            found.append(f"{kit} x{a}-{b}")
    return found


def main() -> None:
    text = UNITS.read_text(encoding="utf-8")
    rows = []
    for loot_id, group, block in extract_loot_blocks(text):
        if group != "Mercs":
            continue
        kits = kits_in_block(block)
        if kits:
            rows.append((loot_id, kits))
    rows.sort()
    lines = [f"Mercs loot defs with medkits: {len(rows)}"]
    for loot_id, kits in rows:
        # strip leaf suffixes like _50 for readability? keep full id
        lines.append(f"- {loot_id}: {', '.join(kits)}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    sys.stdout.buffer.write(("\n".join(lines) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
