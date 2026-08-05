# -*- coding: utf-8 -*-
"""Restore ErnieIsland.Sectors from HEAD; keep MajorSupplyPriority."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
path = ROOT / "items.lua"
wt = path.read_text(encoding="utf-8")
head = subprocess.check_output(["git", "show", "HEAD:items.lua"], cwd=ROOT, text=True, encoding="utf-8")


def ernie_chunk(text: str) -> tuple[int, int, str]:
    a = text.find("PlaceObj('ModItemRegion', {\n\t\t\t\tDisplayName = \"Остров Эрни\"")
    if a < 0:
        raise SystemExit("ErnieIsland PlaceObj not found")
    b = text.find('id = "ErnieIsland"', a)
    b = text.find("}),", b) + 3
    return a, b, text[a:b]


_, _, head_chunk = ernie_chunk(head)
hm = re.search(r"Sectors = \{(.*?)\}", head_chunk, re.S)
if not hm:
    raise SystemExit("HEAD Ernie Sectors not found")
head_sectors = hm.group(0)

a, b, wt_chunk = ernie_chunk(wt)
wm = re.search(r"Sectors = \{(.*?)\}", wt_chunk, re.S)
if not wm:
    raise SystemExit("WT Ernie Sectors not found")

new_chunk = wt_chunk[: wm.start()] + head_sectors + wt_chunk[wm.end() :]
# Ensure MajorSupplyPriority remains if present in wt
if "MajorSupplyPriority" not in new_chunk and "MajorSupplyPriority" in wt_chunk:
    new_chunk = new_chunk.replace(
        "LegionAIEnabled = true,\n",
        "LegionAIEnabled = true,\n\t\t\t\tMajorSupplyPriority = 100,\n",
        1,
    )

path.write_text(wt[:a] + new_chunk + wt[b:], encoding="utf-8")
print("Restored ErnieIsland.Sectors from HEAD")
secs = re.findall(r'"([A-Z]\d+)"', re.search(r"Sectors = \{(.*?)\}", new_chunk, re.S).group(1))
print("n=", len(secs), "has I7=", "I7" in secs, "first=", secs[:5], "last=", secs[-5:])
print("MajorSupplyPriority" in new_chunk)
