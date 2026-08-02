# -*- coding: utf-8 -*-
"""Audit MED-001 medical loot coverage in jazz-units/items.lua."""
from pathlib import Path
import re

path = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
text = path.read_text(encoding="utf-8")

starts = [m.start() for m in re.finditer(r"PlaceObj\('ModItemLootDef', \{", text)]
miss = []
meds_drop = None
counts = {"med": 0, "with_b": 0, "with_m": 0, "with_s": 0}

for start in starts:
    i = text.find("{", start)
    depth = 0
    end = None
    for j in range(i, len(text)):
        c = text[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = j + 1
                if end < len(text) and text[end] == ",":
                    end += 1
                break
    if end is None:
        continue
    block = text[start:end]
    m = re.search(r"\bid = \"([^\"]+)\"", block)
    if not m:
        continue
    loot_id = m.group(1)
    has_fak = 'item = "FirstAidKit"' in block
    has_medkit = 'item = "Medkit"' in block
    has_meds = 'item = "Meds"' in block or 'loot_def = "MedsDrop"' in block
    if loot_id == "MedsDrop":
        meds_drop = block
    if not (has_fak or has_medkit or has_meds or loot_id == "MedsDrop"):
        continue
    counts["med"] += 1
    has_b = "JAZZ_Bandage" in block
    has_mo = "JAZZ_Morphine" in block
    has_s = "JAZZ_SurgicalKit" in block
    if has_b:
        counts["with_b"] += 1
    if has_mo:
        counts["with_m"] += 1
    if has_s:
        counts["with_s"] += 1
    if not has_b:
        miss.append(loot_id)

print("medical LootDefs:", counts)
print("missing Bandage:", len(miss), miss[:50])
print("MedsDrop present:", meds_drop is not None)
if meds_drop:
    print("--- MedsDrop ---")
    print(meds_drop[:1200])

# Enemy-ish loadouts without any medical kit/bandage
PREFIXES = (
    "Army", "Legion", "Adonis", "Rebel", "Militia", "Thug", "Pirate",
    "Enemy", "IMP", "Civ", "Police", "Guard",
)
combat_no_med = []
for start in starts:
    i = text.find("{", start)
    depth = 0
    end = None
    for j in range(i, len(text)):
        c = text[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = j + 1
                if end < len(text) and text[end] == ",":
                    end += 1
                break
    if end is None:
        continue
    block = text[start:end]
    m = re.search(r"\bid = \"([^\"]+)\"", block)
    if not m:
        continue
    loot_id = m.group(1)
    if not any(loot_id.startswith(p) or p in loot_id for p in PREFIXES):
        continue
    has_any = (
        "FirstAidKit" in block
        or "Medkit" in block
        or 'item = "Meds"' in block
        or "JAZZ_Bandage" in block
        or "JAZZ_Morphine" in block
    )
    if not has_any:
        combat_no_med.append(loot_id)

print("enemy-ish LootDefs without med/bandage:", len(combat_no_med))
print("\n".join(combat_no_med[:80]))
