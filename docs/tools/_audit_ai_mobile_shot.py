#!/usr/bin/env python3
"""Audit AIActionMobileShot entries in jazz-units/items.lua."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

UNITS = Path(__file__).resolve().parents[2].parent / "jazz-units" / "items.lua"
if not UNITS.exists():
    UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")

text = UNITS.read_text(encoding="utf-8", errors="replace")
pat = re.compile(r"PlaceObj\('AIActionMobileShot',\s*\{(.*?)\}\s*,?\s*\)", re.S)
blocks = list(pat.finditer(text))
print("AIActionMobileShot count", len(blocks))

aids = Counter()
bias = Counter()
kws = Counter()
weights = Counter()
for m in blocks:
    b = m.group(1)
    aid = re.search(r"'action_id',\s*\"([^\"]+)\"", b) or re.search(r"'action_id',\s*'([^']+)'", b)
    aids[aid.group(1) if aid else "(default MobileShot)"] += 1
    bias_m = re.search(r"'BiasId',\s*\"([^\"]+)\"", b) or re.search(r"'BiasId',\s*'([^']+)'", b)
    bias[bias_m.group(1) if bias_m else "(none)"] += 1
    kw = re.search(r"'RequiredKeywords',\s*\{([^}]*)\}", b, re.S)
    if kw:
        ks = re.findall(r"\"([^\"]+)\"", kw.group(1)) or re.findall(r"'([^']+)'", kw.group(1))
        kws[tuple(ks) if ks else ("(empty)",)] += 1
    else:
        kws[("(none)",)] += 1
    w = re.search(r"'Weight',\s*(\d+)", b)
    weights[int(w.group(1)) if w else 0] += 1

print("\naction_id:")
for k, v in aids.most_common():
    print(f"  {v:4d}  {k}")
print("\nBiasId:")
for k, v in bias.most_common():
    print(f"  {v:4d}  {k}")
print("\nRequiredKeywords:")
for k, v in kws.most_common():
    print(f"  {v:4d}  {k}")

# How many UnitData have RunAndGun / MobileShot keywords
for kw in ("RunAndGun", "MobileShot", "Flank", "CQB"):
    n = len(re.findall(rf'"{kw}"', text))
    print(f"\nstring hits '{kw}': {n}")

# SignatureActions that use non-mobile jazz combat actions?
for aid in (
    "JAZZ_Zipper",
    "JAZZ_TargetSweep",
    "JAZZ_DoubleTap",
    "JAZZ_Mozambique",
    "JAZZ_MobileShotgun",
    "RunAndGun_Carbine",
    "JAZZ_Fanning",
    "JAZZ_ControllableBurst",
    "JAZZ_LargeAutoFire",
):
    n = text.count(f'"{aid}"') + text.count(f"'{aid}'")
    print(f"units items mention {aid}: {n}")
