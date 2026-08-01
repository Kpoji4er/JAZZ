# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.insert(0, "docs/tools")
from _apply_attach_001 import placeobj_blocks, prop

text = Path("items.lua").read_text(encoding="utf-8")

# For each Scope component, list ApplyTo AK* Mount visuals
westernish = (
    "Scope_12x",
    "Scope_6x",
    "Scope_Scout",
    "CombatScope_ACOG",
    "CombatScope_2x",
    "NightScope",
    "Reflex_Aimpoint",
    "Reflex_M68",
    "Reflex_Eotech",
    "Reflex_Closed",
    "Reflex_Open",
)
easternish = (
    "Scope_PSO",
    "CombatScope_1P29",
    "NightScope_NSPU",
    "Reflex_Cobra",
    "Reflex_PKAS",
)

print("=== Scope comps: AK* Mount ApplyTo ===")
for b in placeobj_blocks(text, "ModItemWeaponComponent"):
    cid = prop(b.text, "id") or ""
    if prop(b.text, "Slot") != "Scope":
        continue
    if not any(k in cid for k in westernish + easternish):
        continue
    mounts = []
    # parse Visuals PlaceObj chunks crudely
    for m in re.finditer(
        r"Entity = \"([^\"]+)\"[\s\S]{0,120}?Slot = \"(Mount[^\"]*)\"[\s\S]{0,80}?ApplyTo = \"([^\"]+)\"",
        b.text,
    ):
        ent, slot, apply = m.group(1), m.group(2), m.group(3)
        if apply.startswith("AK") or apply in ("RPK", "RPK74", "Type56", "Zastava_M70", "AN94"):
            mounts.append((apply, slot, ent))
    # also ApplyTo before Entity order variants
    for m in re.finditer(
        r"ApplyTo = \"([^\"]+)\"[\s\S]{0,80}?Entity = \"([^\"]+)\"[\s\S]{0,80}?Slot = \"(Mount[^\"]*)\"",
        b.text,
    ):
        apply, ent, slot = m.group(1), m.group(2), m.group(3)
        if apply.startswith("AK") or apply in ("RPK", "RPK74", "Type56", "Zastava_M70", "AN94"):
            mounts.append((apply, slot, ent))
    print(cid, "AK-family mounts:", sorted(set(mounts)) or "NONE")

print("\n=== All Mount visuals ApplyTo AKM across any component ===")
for b in placeobj_blocks(text, "ModItemWeaponComponent"):
    cid = prop(b.text, "id") or ""
    for m in re.finditer(
        r"Entity = \"([^\"]+)\"[\s\S]{0,160}?Slot = \"(Mount[^\"]*)\"[\s\S]{0,100}?ApplyTo = \"AKM\"",
        b.text,
    ):
        print(cid, "->", m.group(1), m.group(2))
    for m in re.finditer(
        r"ApplyTo = \"AKM\"[\s\S]{0,100}?Entity = \"([^\"]+)\"[\s\S]{0,100}?Slot = \"(Mount[^\"]*)\"",
        b.text,
    ):
        print(cid, "->", m.group(1), m.group(2), "(alt order)")

print("\n=== Mount ComponentSlots remaining ===")
for b in placeobj_blocks(text, "ModItemInventoryItemCompositeDef"):
    if "SlotType', \"Mount\"" in b.text:
        print("weapon", prop(b.text, "id"))
