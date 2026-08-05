# -*- coding: utf-8 -*-
"""Add E8,E9,E11,F13,G13 to GreatDesert; keep sorted; no overlap with other regions."""
from pathlib import Path
import re

ITEMS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\items.lua")
ADD = ["E8", "E9", "E11", "F13", "G13"]

def region_block(text, rid):
    needle = f'\t\t\t\tid = "{rid}",'
    i = text.find(needle)
    if i < 0:
        raise SystemExit(f"missing {rid}")
    start = text.rfind("PlaceObj('ModItemRegion'", 0, i)
    return start, i, text[start:i]

def sectors_of(block):
    sm = re.search(r"Sectors = \{(.*?)\}", block, re.S)
    return re.findall(r'"([A-Z]\d+)"', sm.group(1)), sm

def replace_sectors(text, rid, sectors):
    start, i, block = region_block(text, rid)
    sm = re.search(r"(Sectors = \{).*?(\n\t\t\t\t\},)", block, re.S)
    abs_a = start + sm.start(1)
    abs_b = start + sm.end(2)
    body = ",\n".join(f'\t\t\t\t\t"{s}"' for s in sectors)
    repl = "Sectors = {\n" + body + ",\n\t\t\t\t},"
    return text[:abs_a] + repl + text[abs_b:]

def main():
    text = ITEMS.read_text(encoding="utf-8")
    # check overlaps
    for rid in ("MountainSteppe", "FleatownEnvirons", "LaBarrier", "GreatForest", "PortCacaoEnvirons", "SeagullIsland", "ErnieIsland"):
        _, _, block = region_block(text, rid)
        secs, _ = sectors_of(block)
        hit = sorted(set(secs) & set(ADD))
        if hit:
            raise SystemExit(f"overlap with {rid}: {hit}")
    _, _, gd_block = region_block(text, "GreatDesert")
    secs, _ = sectors_of(gd_block)
    for s in ADD:
        if s not in secs:
            secs.append(s)
    # stable order: by col then number
    secs = sorted(set(secs), key=lambda s: (s[0], int(s[1:])))
    text = replace_sectors(text, "GreatDesert", secs)
    ITEMS.write_text(text, encoding="utf-8")
    print("GreatDesert n=", len(secs), "added", ADD)

if __name__ == "__main__":
    main()
