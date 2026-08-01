# -*- coding: utf-8 -*-
from pathlib import Path
import re

for name in ("items.lua", "metadata.lua"):
    t = Path(name).read_text(encoding="utf-8")
    print("===", name, "len", len(t), "lines", t.count("\n") + 1)
    print("start", repr(t[:100]))
    print("end", repr(t[-160:]))
    print("delta () {} []", t.count("(") - t.count(")"), t.count("{") - t.count("}"), t.count("[") - t.count("]"))
    print("stacked", "}),)," in t or bool(re.search(r"\}\),\s*\),", t)))
    print("backslash1", "\\1" in t)

items = Path("items.lua").read_text(encoding="utf-8")
# top-level ModItemFolder names
folders = re.findall(r"PlaceObj\('ModItemFolder',\s*\{\s*'name',\s*\"([^\"]+)\"", items)
print("ModItemFolder count", len(folders), "first20", folders[:20])
print("has Reload id", 'id = "Reload"' in items)
# find Reload block surroundings
idx = items.find('id = "Reload"')
print("Reload idx", idx)
if idx >= 0:
    start = items.rfind("PlaceObj('ModItemCombatAction'", 0, idx)
    end = items.find("}),", idx)
    print("block start", start, "approx end", end)
    # check function string balance inside Reload GetAPCost
    chunk = items[start:start+8000]
    print("chunk paren", chunk.count("(")-chunk.count(")"))
    print("chunk brace", chunk.count("{")-chunk.count("}"))

# count PlaceObj at root return
print("return PlaceObj", items.lstrip()[:40])
# unfinished short strings near Reload
m = re.search(r'id = "Reload".{0,200}', items, re.S)
print("Reload context", m.group(0)[:200] if m else None)
