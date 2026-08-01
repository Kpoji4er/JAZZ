# -*- coding: utf-8 -*-
"""Remap JAZZ_BarrelParts AdditionalCosts on non-Barrel components -> Parts."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"

def component_slot(block: str) -> str | None:
    # Strip Visuals = { ... }, nested braces
    cleaned = []
    i = 0
    while i < len(block):
        j = block.find("Visuals = {", i)
        if j < 0:
            cleaned.append(block[i:])
            break
        cleaned.append(block[i:j])
        depth = 0
        k = block.find("{", j)
        while k < len(block):
            if block[k] == "{":
                depth += 1
            elif block[k] == "}":
                depth -= 1
                if depth == 0:
                    k += 1
                    break
            k += 1
        i = k
    text = "".join(cleaned)
    m = re.search(r'\n\s*Slot = "([^"]+)"', text)
    return m.group(1) if m else None

def main():
    apply = "--apply" in sys.argv
    text = ITEMS.read_text(encoding="utf-8")
    parts = re.split(r"(PlaceObj\('ModItemWeaponComponent')", text)
    # parts[0] preamble, then pairs (marker, body)...
    out = [parts[0]]
    hits = []
    i = 1
    while i < len(parts):
        marker = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        block = marker + body
        # body ends at next marker already split; but body includes everything until next split point
        # Actually split keeps delimiter; structure: [pre, delim, after, delim, after, ...]
        im = re.search(r'\nid = "([^"]+)"', block)
        slot = component_slot(block)
        cid = im.group(1) if im else "?"
        if slot and slot != "Barrel" and "JAZZ_BarrelParts" in block:
            new_block, n = re.subn(
                r"('Type',\s*)\"JAZZ_BarrelParts\"",
                r'\1"Parts"',
                block,
            )
            if n:
                hits.append((cid, slot, n))
                block = new_block
        out.append(block)
        i += 2

    print("hits=%d" % len(hits))
    for cid, slot, n in hits:
        print("%s slot=%s remapped_x%d" % (cid, slot, n))

    if not apply:
        print("dry-run; pass --apply to write")
        return
    if not hits:
        return
    new_text = "".join(out)
    bak = ITEMS.with_suffix(".lua.bak_stock_barrelparts")
    bak.write_text(text, encoding="utf-8")
    ITEMS.write_text(new_text, encoding="utf-8")
    print("wrote", ITEMS.name, "bak", bak.name)

if __name__ == "__main__":
    main()
