# -*- coding: utf-8 -*-
"""Static checks for IMP certificate playtest fix (loc + Sniper tactical + icons)."""
from pathlib import Path
import csv
import re
import sys

root = Path(__file__).resolve().parents[2]
errors = []

# --- CSV ---
rows_by_file = {}
for name in ("Russian.csv", "English.csv"):
    with (root / name).open(encoding="utf-8", newline="") as f:
        f.readline()  # sep=,
        rows_by_file[name] = {cols[0]: cols for cols in csv.reader(f) if cols}

for iid, expect_ru, expect_en in (
    ("890000000001931", "Мимикрия", "Mimicry"),
    ("890000000001933", "Ветеран", "Veteran"),
    ("890000000001935", "Снайпер", "Sniper"),
):
    ru = rows_by_file["Russian.csv"].get(iid)
    en = rows_by_file["English.csv"].get(iid)
    if not ru or ru[2] != expect_ru:
        errors.append(f"Russian.csv {iid} Translation want {expect_ru!r} got {ru[2] if ru else None!r}")
    if not en or en[2] != expect_en:
        errors.append(f"English.csv {iid} Translation want {expect_en!r} got {en[2] if en else None!r}")

# --- items.lua ---
items = (root / "items.lua").read_text(encoding="utf-8")
for perk_id, group, icon in (
    ("Jazz_Perk_Mimicry", "Perk-Personality", "Bond"),
    ("Jazz_Perk_Veteran", "Perk-Personality", "OldDog"),
    ("Jazz_Perk_Sniper", "Perk-Specialization", "Deadeye"),
):
    m = re.search(
        rf"'Id',\s*\"{perk_id}\".{{0,800}}?'Icon',\s*\"([^\"]+)\"",
        items,
        re.S,
    )
    g = re.search(
        rf"'Group',\s*\"([^\"]+)\",\s*\n\s*'Id',\s*\"{perk_id}\"",
        items,
    )
    if not g or g.group(1) != group:
        errors.append(f"{perk_id} Group want {group} got {g.group(1) if g else None}")
    if not m or icon not in m.group(1):
        errors.append(f"{perk_id} Icon want *{icon}* got {m.group(1) if m else None}")

perks = (root / "Code" / "System_IMP_Perks.lua").read_text(encoding="utf-8")
if "Jazz_Perk_Sniper" in re.search(
    r"JAZZ_IMP_EXTRA_PERSONAL\s*=\s*\{([^}]+)\}", perks, re.S
).group(1):
    errors.append("Jazz_Perk_Sniper still in JAZZ_IMP_EXTRA_PERSONAL")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("OK IMP certificate static checks")
