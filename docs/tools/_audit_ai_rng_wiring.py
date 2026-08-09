#!/usr/bin/env python3
"""Brace-aware audit of AIActionMobileShot in jazz-units/items.lua."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
text = UNITS.read_text(encoding="utf-8", errors="replace")


def extract_placeobjs(src: str, classname: str) -> list[str]:
    needle = f"PlaceObj('{classname}',"
    out = []
    i = 0
    while True:
        j = src.find(needle, i)
        if j < 0:
            break
        k = src.find("{", j)
        if k < 0:
            break
        depth = 0
        for p in range(k, len(src)):
            ch = src[p]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    out.append(src[k + 1 : p])
                    i = p + 1
                    break
        else:
            break
    return out


blocks = extract_placeobjs(text, "AIActionMobileShot")
print("AIActionMobileShot count", len(blocks))

aids = Counter()
bias = Counter()
kw_sets = Counter()
real_rng_kw = Counter()
fake_rng = 0  # BiasId RunAndGun, action not RunAndGun*

for b in blocks:
    aid_m = re.search(r"'action_id',\s*\"([^\"]+)\"", b)
    aid = aid_m.group(1) if aid_m else "(default MobileShot)"
    aids[aid] += 1
    bias_m = re.search(r"'BiasId',\s*\"([^\"]+)\"", b)
    bias_id = bias_m.group(1) if bias_m else "(none)"
    bias[bias_id] += 1
    kw_m = re.search(r"'RequiredKeywords',\s*\{([^}]*)\}", b, re.S)
    if kw_m:
        kws = tuple(re.findall(r"\"([^\"]+)\"", kw_m.group(1))) or ("(empty)",)
    else:
        kws = ("(none)",)
    kw_sets[kws] += 1
    if aid == "RunAndGun":
        real_rng_kw[kws] += 1
    elif bias_id == "RunAndGun":
        fake_rng += 1

print("\naction_id:")
for k, v in aids.most_common():
    print(f"  {v:4d}  {k}")
print("\nBiasId:")
for k, v in bias.most_common():
    print(f"  {v:4d}  {k}")
print("\nRequiredKeywords (all MobileShot entries):")
for k, v in kw_sets.most_common():
    print(f"  {v:4d}  {k}")
print("\nRequiredKeywords on real action_id=RunAndGun:")
for k, v in real_rng_kw.most_common():
    print(f"  {v:4d}  {k}")
print(f"\nBiasId=RunAndGun but action_id != RunAndGun: {fake_rng}")

# AIAttackSingleTarget action_ids (signature dump attacks)
atk = extract_placeobjs(text, "AIAttackSingleTarget")
print(f"\nAIAttackSingleTarget count: {len(atk)}")
atk_aids = Counter()
for b in atk:
    aid_m = re.search(r"'action_id',\s*\"([^\"]+)\"", b)
    atk_aids[aid_m.group(1) if aid_m else "(default)"] += 1
print("AIAttackSingleTarget action_id:")
for k, v in atk_aids.most_common(30):
    print(f"  {v:4d}  {k}")

jazz_hits = [
    "JAZZ_Zipper",
    "JAZZ_TargetSweep",
    "JAZZ_DoubleTap",
    "JAZZ_Mozambique",
    "JAZZ_MobileShotgun",
    "RunAndGun_Carbine",
    "JAZZ_Fanning",
    "JAZZ_SmgStorm",
    "JAZZ_ControllableBurst",
    "JAZZ_LargeAutoFire",
    "JAZZ_Bullseye",
]
print("\nJazz combat actions in units items (any mention):")
for aid in jazz_hits:
    n = text.count(f'"{aid}"')
    print(f"  {aid}: {n}")
