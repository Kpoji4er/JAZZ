# -*- coding: utf-8 -*-
import csv
import re
from pathlib import Path

text = Path("items.lua").read_text(encoding="utf-8")
names = sorted(set(re.findall(r"ModItemWeaponComponentEffect (\w+) Description", text)))
print("mod effect presets (from comments):", len(names))

comps = list(csv.DictReader(open("docs/technical/weapons/data/weapon-components.csv", encoding="utf-8")))
fx_on_any = set()
for c in comps:
    for e in (c.get("effects") or "").split(";"):
        if e:
            fx_on_any.add(e)

declared = {
    r["effect_id"]
    for r in csv.DictReader(
        open("docs/technical/weapons/data/weapon-component-effects.csv", encoding="utf-8")
    )
}

print("effects.csv:", len(declared))
print("on any component:", len(fx_on_any))
orphan = sorted(declared - fx_on_any)
print("declared, zero comps:", orphan)

# also check PointBlankBonus as weapon property
pp = len(re.findall(r"'PointBlankBonus'", text))
print("PointBlankBonus string hits in items.lua:", pp)

# Handling effects
hand = sorted(e for e in fx_on_any if "Handling" in e or e == "Cumbersome")
print("Handling-ish still on comps:", hand)

# mod presets not referenced by any component
mod_unused = sorted(set(names) - fx_on_any)
print("mod presets unused by any comp:", len(mod_unused))
for e in mod_unused:
    print(" ", e)

# after handling strip, these become unused too
would_free = sorted((set(hand) | set(orphan)) & set(names))
print("delete candidates after strip (mod-owned):", would_free)
