# -*- coding: utf-8 -*-
"""Strip accidental MED injects from ammo/ordnance Drop_* lists; patch PierreGuard_Ordnance."""
from pathlib import Path
import re

path = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
text = path.read_text(encoding="utf-8")

starts = [m.start() for m in re.finditer(r"PlaceObj\('ModItemLootDef', \{", text)]
spans = []
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
    spans.append((start, end, m.group(1), block))

MED_LINE = re.compile(
    r"\n\t+PlaceObj\('LootEntryInventoryItem', \{ item = \"JAZZ_(?:Bandage|Morphine|SurgicalKit)\"[^}]*\}\),"
)

STRIP_ID = re.compile(r"^(Drop_|.*_ammo|40mm$)", re.I)
# also Comment = "list" ammo pools
stripped = 0
patched = 0

out = []
last = 0
for start, end, lid, block in spans:
    out.append(text[last:start])
    new = block
    should_strip = bool(STRIP_ID.search(lid)) or (
        'Comment = "list"' in block and "JAZZ_Bandage" in block and "FirstAidKit" not in block and "Medkit" not in block
    )
    # keep real combat kits even if Comment=list somehow
    if should_strip and "JAZZ_Bandage" in block:
        cleaned = MED_LINE.sub("", block)
        if cleaned != block:
            stripped += 1
            new = cleaned
    elif lid == "PierreGuard_Ordnance" and "JAZZ_Bandage" not in block:
        indent = "\t\t\t\t\t\t"
        inserts = (
            f"\n{indent}PlaceObj('LootEntryInventoryItem', {{ item = \"JAZZ_Bandage\", stack_min = 1, stack_max = 3, drop_chance = 65 }}),"
            f"\n{indent}PlaceObj('LootEntryInventoryItem', {{ item = \"JAZZ_Morphine\", drop_chance = 25 }}),"
        )
        # after first LootEntryLootDef
        m = re.search(r"PlaceObj\('LootEntryLootDef', \{", block)
        if m:
            i = block.find("{", m.start())
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
                        new = block[:k] + inserts + block[k:]
                        patched += 1
                        break
    out.append(new)
    last = end

out.append(text[last:])
path.write_text("".join(out), encoding="utf-8")
print({"stripped": stripped, "patched_pierre": patched})
