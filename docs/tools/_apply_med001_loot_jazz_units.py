# -*- coding: utf-8 -*-
"""MED-001: inject Bandage/Morphine/SurgicalKit into jazz-units medical ModItemLootDef."""
from pathlib import Path
import re

path = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
text = path.read_text(encoding="utf-8")

# First undo prior partial injects to avoid duplicates on re-run
text = re.sub(
    r"\n\t+PlaceObj\('LootEntryInventoryItem', \{ item = \"JAZZ_(?:Bandage|Morphine|SurgicalKit)\"[^}]*\}\),",
    "",
    text,
)

DOCTOR_HINTS = (
    "MD50", "MD40", "MD30", "Spider50", "Spider40", "Spider30",
    "Laura50", "Laura40", "Vince50", "Vince40",
    "Gus50", "Gus40", "Mildred", "DrMangel", "AdonisMedic",
)


def entry(item, stack_min=1, stack_max=1, drop_chance=None, indent="\t\t\t\t\t"):
    parts = [f'item = "{item}"']
    if stack_min != 1 or stack_max != 1:
        parts.append(f"stack_min = {stack_min}")
        parts.append(f"stack_max = {stack_max}")
    if drop_chance is not None and drop_chance < 100:
        parts.append(f"drop_chance = {drop_chance}")
    inner = ", ".join(parts)
    return f"{indent}PlaceObj('LootEntryInventoryItem', {{ {inner} }}),"


# Find each ModItemLootDef by scanning balanced braces from PlaceObj('ModItemLootDef'
starts = [m.start() for m in re.finditer(r"PlaceObj\('ModItemLootDef', \{", text)]
stats = {"n": 0, "changed": 0, "bandage": 0, "morphine": 0, "surgical": 0}

out = []
last = 0
for start in starts:
    # find matching close for the opening { of this PlaceObj
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
                # include trailing ),
                end = j + 1
                if end < len(text) and text[end] == ",":
                    end += 1
                break
    if end is None:
        continue
    block = text[start:end]
    stats["n"] += 1

    m = re.search(r"\bid = \"([^\"]+)\"", block)
    if not m:
        out.append(text[last:start])
        out.append(block)
        last = end
        continue
    loot_id = m.group(1)

    has_fak = 'item = "FirstAidKit"' in block
    has_medkit = 'item = "Medkit"' in block
    has_meds = 'item = "Meds"' in block or 'loot_def = "MedsDrop"' in block
    if not (has_fak or has_medkit or has_meds):
        out.append(text[last:start])
        out.append(block)
        last = end
        continue

    is_doctor = any(h in loot_id for h in DOCTOR_HINTS)
    is_medic = ("Medic" in loot_id) or loot_id.startswith(
        ("Fox", "Mouse", "Scully", "Quinten", "Ira", "Henning", "Bonemaker", "IMP_equipment", "Highball")
    )

    # detect indent from FirstAidKit/Medkit line
    indent = "\t\t\t\t\t"
    for key in ("FirstAidKit", "Medkit", "Meds"):
        mm = re.search(rf"^(\t+)PlaceObj\('LootEntryInventoryItem'.*item = \"{key}\"", block, re.M)
        if mm:
            indent = mm.group(1)
            break

    inserts = []
    inserts.append(entry("JAZZ_Bandage", 2 if (has_fak or has_medkit) else 1, 5 if (has_fak or has_medkit) else 4,
                         drop_chance=None if (has_fak or has_medkit) else 80, indent=indent))
    stats["bandage"] += 1

    if has_fak or has_medkit or is_medic or is_doctor:
        sm, sx = (1, 3) if (is_doctor or has_medkit) else (1, 2)
        chance = None if (is_doctor or has_medkit) else 70
        inserts.append(entry("JAZZ_Morphine", sm, sx, drop_chance=chance, indent=indent))
        stats["morphine"] += 1

    if has_medkit and (is_doctor or loot_id in {"DrMangel", "AdonisMedic", "MD50", "Spider50", "Laura50", "Vince50", "Gus50"}):
        chance = 100 if loot_id == "DrMangel" else 40
        inserts.append(entry("JAZZ_SurgicalKit", 1, 1, drop_chance=chance, indent=indent))
        stats["surgical"] += 1

    # insert after first medicine inventory entry closing
    anchor = None
    for key in ("FirstAidKit", "Medkit", "Meds"):
        idx = block.find(f'item = "{key}"')
        if idx < 0:
            continue
        end_entry = block.find("}),", idx)
        if end_entry >= 0:
            anchor = end_entry + 3
            break
    if anchor is None:
        idx = block.find('loot_def = "MedsDrop"')
        if idx >= 0:
            end_entry = block.find("}),", idx)
            if end_entry >= 0:
                anchor = end_entry + 3

    out.append(text[last:start])
    if anchor is None:
        out.append(block)
    else:
        stats["changed"] += 1
        out.append(block[:anchor] + "\n" + "\n".join(inserts) + block[anchor:])
    last = end

out.append(text[last:])
path.write_text("".join(out), encoding="utf-8")
print(
    f"lootdefs_scanned={stats['n']} medical_changed={stats['changed']} "
    f"bandage={stats['bandage']} morphine={stats['morphine']} surgical={stats['surgical']}"
)
