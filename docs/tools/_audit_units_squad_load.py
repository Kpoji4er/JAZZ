# -*- coding: utf-8 -*-
"""Audit jazz-units EnemySquad CheckDifficulty format + M4 InitialSquads drift."""
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
MAPS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\items.lua")
JA3 = Path(r"F:\SteamLibrary\steamapps\common\Jagged Alliance 3")

text = UNITS.read_text(encoding="utf-8")
maps = MAPS.read_text(encoding="utf-8")

# --- delimiter / stacked ---
print("() imbalance", text.count("(") - text.count(")"))
print("{} imbalance", text.count("{") - text.count("}"))
print("[] imbalance", text.count("[") - text.count("]"))
stacked = list(re.finditer(r"\}\),\s*\}\),", text))
print("stacked }),}), count", len(stacked))
for m in stacked[:5]:
    line = text.count("\n", 0, m.start()) + 1
    print("  at L", line)

# --- CheckDifficulty styles ---
# false-style: 'Difficulty', "X"
# true-style: Difficulty = "X"
false_style = list(
    re.finditer(
        r"PlaceObj\('CheckDifficulty',\s*\{\s*'Difficulty',\s*\"([^\"]+)\"",
        text,
    )
)
true_style = list(
    re.finditer(
        r"PlaceObj\('CheckDifficulty',\s*\{\s*Difficulty\s*=\s*\"([^\"]+)\"",
        text,
    )
)
print("CheckDifficulty false-style (assert risk):", len(false_style))
print("CheckDifficulty true-style:", len(true_style))
if false_style:
    first = false_style[0]
    print("  first false at L", text.count("\n", 0, first.start()) + 1)

# other conditions with quoted-key style inside EnemySquads?
cond_false = re.findall(
    r"PlaceObj\('(Check\w+|Has\w+)',\s*\{\s*'(\w+)',",
    text,
)
from collections import Counter

print("Condition PlaceObj with 'key', style (top):")
for (cls, key), n in Counter(cond_false).most_common(15):
    print(f"  {cls} '{key}' x{n}")

# --- M4 InitialSquads ---
print("--- M4 InitialSquads ---")
for label, pat in [
    ("ModItemSector", r"'sectorId', \"M4\"[\s\S]{0,1200}?'InitialSquads', \{([\s\S]*?)\},"),
    ("Campaign Id M4", r"'Id', \"M4\"[\s\S]{0,1200}?'InitialSquads', \{([\s\S]*?)\},"),
]:
    hits = list(re.finditer(pat, maps))
    print(label, "hits", len(hits))
    for h in hits:
        ids = re.findall(r'"([^"]+)"', h.group(1))
        print(" ", ids)

# --- LegionOutlook displayName ---
m = re.search(
    r"PlaceObj\('ModItemEnemySquads', \{[\s\S]*?id = \"LegionOutlook_Easy\",",
    text,
)
if m:
    block = m.group(0)
    dn = re.search(r"displayName = T\([^)]+\)[^\n]*\"([^\"]+)\"", block)
    print("LegionOutlook_Easy displayName:", dn.group(1) if dn else "MISSING")
    print("  has CheckDifficulty:", "CheckDifficulty" in block)

# Extra marksmen
m2 = re.search(
    r"PlaceObj\('ModItemEnemySquads', \{[\s\S]*?id = \"LegionExtra_Ernie_Marksmen\",",
    text,
)
if m2:
    block = m2.group(0)
    dn = re.search(r"displayName = T\([^)]+\)[^\n]*\"([^\"]+)\"", block)
    print("LegionExtra_Ernie_Marksmen displayName:", dn.group(1) if dn else "MISSING")

# vanilla sample if present
for cand in JA3.rglob("EnemySquads.lua"):
    sample = cand.read_text(encoding="utf-8", errors="ignore")[:5000]
    if "CheckDifficulty" in sample:
        print("vanilla sample file", cand)
        for line in sample.splitlines():
            if "CheckDifficulty" in line or "Difficulty" in line:
                print(" ", line.strip()[:120])
                break
        break
