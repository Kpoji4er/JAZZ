# -*- coding: utf-8 -*-
from pathlib import Path

for name in ("items.lua", "metadata.lua"):
    b = Path(name).read_bytes()
    print(name, "nulls", b.count(b"\x00"), "utf8", end=" ")
    try:
        b.decode("utf-8")
        print("ok")
    except UnicodeDecodeError as e:
        print("FAIL", e)

# Try to emulate Ged load: compile as Lua chunk via a minimal approach —
# count PlaceObj calls that would run; ensure return table length
items = Path("items.lua").read_text(encoding="utf-8")
assert items.lstrip().startswith("return {")
# Find if any function body has `end)` without comma issues near Reload — already ok

# Check ModItemCombatAction required: compare keys of Reload vs FoldStock
import re

def keys_of(id_name: str) -> set[str]:
    m = re.search(rf"PlaceObj\('ModItemCombatAction', \{{(.*?)\n\t\t\t\tid = \"{id_name}\"", items, re.S)
    if not m:
        # try 3-tab id
        m = re.search(rf"PlaceObj\('ModItemCombatAction', \{{(.*?)\nid = \"{id_name}\"", items, re.S)
    if not m:
        return set()
    body = m.group(1)
    return set(re.findall(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=", body)) | set(
        re.findall(r"(?m)^\s*'([A-Za-z_][A-Za-z0-9_]*)'\s*,", body)
    )

print("Reload keys", sorted(keys_of("Reload"))[:40], "count", len(keys_of("Reload")))
print("FoldStock keys count", len(keys_of("FoldStock")))
print("Bandage keys count", len(keys_of("Bandage")))
print("Reload missing vs Fold", sorted(keys_of("FoldStock") - keys_of("Reload")))
