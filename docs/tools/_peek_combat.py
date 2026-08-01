# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.insert(0, "docs/tools")
from _apply_attach_001 import placeobj_blocks, prop

text = Path("items.lua").read_text(encoding="utf-8")
for cid in ["JAZZ_CombatScope_2x", "JAZZ_CombatScope_ACOG"]:
    for b in placeobj_blocks(text, "ModItemWeaponComponent"):
        if prop(b.text, "id") != cid:
            continue
        # print from ModificationEffects through Slot
        m = re.search(
            r"(ModificationEffects = \{.*?Parameters = \{.*?\},)",
            b.text,
            re.S,
        )
        print("====", cid)
        print(m.group(1) if m else b.text[b.text.find("Cost") : b.text.find("Visuals")])
        break
