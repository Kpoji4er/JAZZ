# -*- coding: utf-8 -*-
"""Verify LateAwakenMinTier per ModItemRegion in jazz/items.lua (Regions folder)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
lines = (ROOT / "items.lua").read_text(encoding="utf-8").splitlines()
# Only count region presets that close with `}),` then next PlaceObj or folder end.
starts = []
for i, l in enumerate(lines):
    if "PlaceObj('ModItemRegion'" in l:
        starts.append(i)
starts.append(len(lines))
for idx in range(len(starts) - 1):
    s, e = starts[idx], starts[idx + 1]
    block = lines[s:e]
    # Stop at first id= inside this PlaceObj (region id is last props, but only one id=).
    rid = None
    late = None
    enabled = None
    for l in block:
        t = l.strip()
        if t.startswith('id = "') and rid is None:
            rid = t.split('"')[1]
        elif t.startswith("LateAwakenMinTier"):
            late = t.rstrip(",")
        elif t.startswith("LegionAIEnabled"):
            enabled = t.rstrip(",")
        # End of this PlaceObj
        if t == "})," and rid is not None:
            break
    if rid in (
        "ErnieIsland",
        "PortCacaoEnvirons",
        "GreatDesert",
        "MountainSteppe",
        "SeagullIsland",
        "FleatownEnvirons",
        "LaBarrier",
        "GreatForest",
    ) or (enabled is not None):
        print(f"{rid}: {late or 'LateAwaken=(none/default 0)'} | {enabled or 'LegionAI=?'}")
