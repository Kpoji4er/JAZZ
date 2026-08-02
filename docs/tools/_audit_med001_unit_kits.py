# -*- coding: utf-8 -*-
"""Find unit Equipment LootDefs that still lack MED-001 consumables."""
from pathlib import Path
import re

units = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
items = (units / "items.lua").read_text(encoding="utf-8")

# Collect Equipment LootDef ids from UnitData companions
ud_refs = set()
for p in (units / "UnitData").glob("*.lua"):
    t = p.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r"Equipment\s*=\s*\{([^}]*)\}", t):
        for eid in re.findall(r'"([^"]+)"', m.group(1)):
            ud_refs.add(eid)

print("UnitData Equipment refs:", len(ud_refs))

# Parse all ModItemLootDef
starts = [m.start() for m in re.finditer(r"PlaceObj\('ModItemLootDef', \{", items)]
by_id = {}
for start in starts:
    i = items.find("{", start)
    depth = 0
    end = None
    for j in range(i, len(items)):
        if items[j] == "{":
            depth += 1
        elif items[j] == "}":
            depth -= 1
            if depth == 0:
                end = j + 1
                if end < len(items) and items[end] == ",":
                    end += 1
                break
    block = items[start:end]
    m = re.search(r'\bid = "([^"]+)"', block)
    if not m:
        continue
    by_id[m.group(1)] = block

print("LootDefs total:", len(by_id))


def block_has_med(block: str) -> bool:
    return (
        "FirstAidKit" in block
        or "Medkit" in block
        or 'item = "Meds"' in block
        or "JAZZ_Bandage" in block
        or "JAZZ_Morphine" in block
        or 'loot_def = "MedsDrop"' in block
    )


def nested_has_med(block: str, depth=0) -> bool:
    if depth > 4:
        return False
    if block_has_med(block):
        return True
    for nid in re.findall(r'loot_def = "([^"]+)"', block):
        nb = by_id.get(nid)
        if nb and nested_has_med(nb, depth + 1):
            return True
    return False


missing = []
present = []
orphan_eq = []
for eid in sorted(ud_refs):
    block = by_id.get(eid)
    if block is None:
        orphan_eq.append(eid)
        continue
    if nested_has_med(block):
        present.append(eid)
    else:
        missing.append(eid)

print("Equipment with med path:", len(present))
print("Equipment without med path:", len(missing))
print("Equipment ids not in items.lua:", len(orphan_eq))
print("--- missing sample ---")
for x in missing[:80]:
    print(x)
print("--- orphan sample ---")
for x in orphan_eq[:40]:
    print(x)
