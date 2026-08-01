# -*- coding: utf-8 -*-
"""Remove duplicate Mag family ModResourcePreset block in metadata.lua.

After mag-family split, 37 InventoryItemCompositeDef presets were inserted twice
contiguously (second copy starts at MagDrum_30_100_G3 after MagSmall30_15_TMP).
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "metadata.lua"

PRESET_BLOCK = re.compile(
    r"\t\tPlaceObj\('ModResourcePreset', \{\n"
    r"\t\t\t'Class', \"InventoryItemCompositeDef\",\n"
    r"\t\t\t'Id', \"([^\"]+)\",\n"
    r"\t\t\t'ClassDisplayName', \"Inventory item\",\n"
    r"\t\t\}\),\n"
)


def main() -> int:
    text = META.read_text(encoding="utf-8")
    ids = [m.group(1) for m in PRESET_BLOCK.finditer(text)]
    c = Counter(ids)
    dups = {k for k, v in c.items() if v > 1 and k.startswith("JAZZ_Mag")}
    print(f"matched blocks={len(ids)} mag_dup_ids={len(dups)}")

    matches = list(PRESET_BLOCK.finditer(text))
    # Find first MagSmall30_15_TMP then following run of all-dup Mag ids
    tmp_idxs = [i for i, m in enumerate(matches) if m.group(1) == "JAZZ_MagSmall30_15_TMP"]
    if len(tmp_idxs) < 1:
        print("TMP preset not found")
        return 1
    start_i = tmp_idxs[0] + 1
    if start_i >= len(matches) or matches[start_i].group(1) != "JAZZ_MagDrum_30_100_G3":
        print("expected MagDrum after first TMP, got", matches[start_i].group(1) if start_i < len(matches) else None)
        return 1

    end_i = start_i
    while end_i < len(matches) and matches[end_i].group(1) in dups:
        end_i += 1
    block = matches[start_i:end_i]
    print(f"will remove {len(block)} presets: {block[0].group(1)} .. {block[-1].group(1)}")
    if not all(m.group(1) in dups for m in block):
        print("refuse: not all dup")
        return 1
    if len(block) != len(dups):
        print(f"warn: block {len(block)} != dup set {len(dups)}")

    if "--apply" not in sys.argv:
        print("dry-run; pass --apply")
        return 0

    start = block[0].start()
    end = block[-1].end()
    new = text[:start] + text[end:]
    tmp = META.with_suffix(".lua.tmp_dedupe")
    tmp.write_text(new, encoding="utf-8")
    tmp.replace(META)

    text2 = META.read_text(encoding="utf-8")
    ids2 = [m.group(1) for m in PRESET_BLOCK.finditer(text2)]
    c2 = Counter(ids2)
    d2 = sum(1 for v in c2.values() if v > 1)
    print(f"after: blocks={len(ids2)} unique={len(c2)} dup_ids={d2}")
    return 0 if d2 == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
