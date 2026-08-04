# -*- coding: utf-8 -*-
"""MED-001 phase 2: Bandage/Morphine/(IFAK) on Equipment combat + merc kits.

Only touches:
- Equipment roots with loot=\"all\" (enemy/militia full kits)
- Merc tier leaf kits (group Mercs, inventory-bearing, id ends with ##)
Does NOT walk into ammo/armor/weapon sub-lootdefs.
Idempotent: skips blocks that already contain JAZZ_Bandage.
"""
from pathlib import Path
import re

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
path = UNITS / "items.lua"
text = path.read_text(encoding="utf-8")

starts = [m.start() for m in re.finditer(r"PlaceObj\('ModItemLootDef', \{", text)]
spans = []
by_id = {}
for start in starts:
    i = text.find("{", start)
    depth = 0
    end = None
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                end = j + 1
                if end < len(text) and text[end] == ",":
                    end += 1
                break
    block = text[start:end]
    m = re.search(r'\bid = "([^"]+)"', block)
    if not m:
        continue
    lid = m.group(1)
    spans.append((start, end, lid, block))
    by_id[lid] = block

eq_roots = set()
for p in (UNITS / "UnitData").glob("*.lua"):
    t = p.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r"Equipment\s*=\s*\{([^}]*)\}", t):
        for eid in re.findall(r'"([^"]+)"', m.group(1)):
            eq_roots.add(eid)

SKIP = re.compile(
    r"(Armor|GenW|Helmet|Torso|Legs|PistolList|Knife|Grenade|Ordnance|Valuables|"
    r"CeramicPlate|AKType|Shotgun|Revolver|Machete|OneHSMG|AutoPistol|Ammo|"
    r"Plate|Sidearm|Firearm|_ammo|Preset_)",
    re.I,
)


def entry(item, stack_min=1, stack_max=1, drop_chance=None, indent="\t\t\t\t\t"):
    parts = [f'item = "{item}"']
    if stack_min != 1 or stack_max != 1:
        parts.append(f"stack_min = {stack_min}")
        parts.append(f"stack_max = {stack_max}")
    if drop_chance is not None and drop_chance < 100:
        parts.append(f"drop_chance = {drop_chance}")
    return f"{indent}PlaceObj('LootEntryInventoryItem', {{ {', '.join(parts)} }}),"


def end_of_first_loot_entry(block: str):
    """Return index after the first complete PlaceObj('LootEntry…', {…}),"""
    m = re.search(r"PlaceObj\('LootEntry(?:InventoryItem|LootDef)',\s*\{", block)
    if not m:
        return None
    # match braces of the argument table, then require trailing ),
    i = block.find("{", m.start())
    depth = 0
    for j in range(i, len(block)):
        if block[j] == "{":
            depth += 1
        elif block[j] == "}":
            depth -= 1
            if depth == 0:
                # expect ), after table close
                k = j + 1
                if k < len(block) and block[k] == ")":
                    k += 1
                if k < len(block) and block[k] == ",":
                    k += 1
                return k
    return None


targets = set()

# 1) Equipment roots that are full kits (loot=all) and not pure armor stubs
for root in eq_roots:
    if SKIP.search(root):
        continue
    block = by_id.get(root)
    if not block:
        continue
    if 'loot = "all"' in block:
        targets.add(root)
    # weighted merc wrapper: include nested tier kits with inventory items
    for nid in re.findall(r'loot_def = "([^"]+)"', block):
        if SKIP.search(nid) or nid.startswith("Drop_"):
            continue
        nb = by_id.get(nid)
        if not nb:
            continue
        if 'Comment = "list"' in nb:
            continue
        if "LootEntryInventoryItem" in nb:
            targets.add(nid)

# 2) All Mercs-group inventory-bearing leaf kits
for lid, block in by_id.items():
    if 'group = "Mercs"' not in block:
        continue
    if SKIP.search(lid):
        continue
    if "LootEntryInventoryItem" not in block:
        continue
    # skip wrappers that only nest other lootdefs without own items — already handled
    targets.add(lid)

stats = {"targets": len(targets), "changed": 0, "skip_bandage": 0, "merc": 0, "enemy": 0}

out = []
last = 0
for start, end, lid, block in spans:
    out.append(text[last:start])
    if lid not in targets:
        out.append(block)
        last = end
        continue
    if "JAZZ_Bandage" in block:
        stats["skip_bandage"] += 1
        out.append(block)
        last = end
        continue

    indent = "\t\t\t\t\t"
    mm = re.search(r"^(\t+)PlaceObj\('LootEntry", block, re.M)
    if mm:
        indent = mm.group(1)

    had_kit = 'item = "FirstAidKit"' in block or 'item = "Medkit"' in block
    merc = 'group = "Mercs"' in block or bool(re.search(r"(?:Loot_JAZZ_|JAZZ_).*\d{2}$", lid)) or (
        bool(re.search(r"\d{2}$", lid)) and 'group = "Mercs"' in by_id.get(lid, block)
    )
    # tier kit under Mercs group
    if 'group = "Mercs"' in block and "LootEntryInventoryItem" in block:
        merc = True

    inserts = []
    if merc or had_kit:
        # Merc kits: Bandage x10, IFAK full MaxStacks=5 (see _apply_merc_med_full_stacks.py).
        # Medical enemy kits keep smaller bandage stacks when had_kit and not merc.
        if merc:
            inserts.append(entry("JAZZ_Bandage", 10, 10, indent=indent))
            inserts.append(entry("JAZZ_Morphine", 1, 2, drop_chance=None if had_kit else 80, indent=indent))
            if not had_kit:
                inserts.append(
                    f"{indent}PlaceObj('LootEntryInventoryItem', {{ item = \"FirstAidKit\", stack_min = 5, stack_max = 5 }}),"
                )
        else:
            # Enemy medical kits: single-use stacks (see _apply_enemy_med_stacks_min.py).
            inserts.append(entry("JAZZ_Bandage", 1, 1, indent=indent))
            inserts.append(entry("JAZZ_Morphine", 1, 1, drop_chance=None if had_kit else 80, indent=indent))
        stats["merc"] += 1
    else:
        inserts.append(entry("JAZZ_Bandage", 1, 1, drop_chance=65, indent=indent))
        inserts.append(entry("JAZZ_Morphine", 1, 1, drop_chance=25, indent=indent))
        stats["enemy"] += 1

    # Prefer insert after existing FirstAidKit/Medkit/Meds entry (full PlaceObj)
    anchor = None
    for key in ("FirstAidKit", "Medkit", "Meds"):
        idx = block.find(f'item = "{key}"')
        if idx < 0:
            continue
        # walk back to PlaceObj start
        p0 = block.rfind("PlaceObj(", 0, idx)
        if p0 < 0:
            continue
        i = block.find("{", p0)
        depth = 0
        for j in range(i, len(block)):
            if block[j] == "{":
                depth += 1
            elif block[j] == "}":
                depth -= 1
                if depth == 0:
                    k = j + 1
                    if k < len(block) and block[k] == ")":
                        k += 1
                    if k < len(block) and block[k] == ",":
                        k += 1
                    anchor = k
                    break
        if anchor is not None:
            break

    if anchor is None:
        anchor = end_of_first_loot_entry(block)

    if anchor is None:
        # empty-ish kit: before final }
        anchor = block.rfind("}")
        new_block = block[:anchor] + "\n" + "\n".join(inserts) + "\n" + block[anchor:]
    else:
        new_block = block[:anchor] + "\n" + "\n".join(inserts) + block[anchor:]

    stats["changed"] += 1
    out.append(new_block)
    last = end

out.append(text[last:])
path.write_text("".join(out), encoding="utf-8")
print(stats)
print("targets sample:", sorted(targets)[:50])
