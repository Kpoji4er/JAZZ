#!/usr/bin/env python3
"""Diff workshop AIM LootDefs in jazz-units/items.lua vs _apply_workshop_aim_sheet MERCS targets."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
OUT = JAZZ / "docs/design/mercs-ja12/_workshop_loot_diff.txt"

spec = importlib.util.spec_from_file_location(
    "apply", JAZZ / "docs/tools/_apply_workshop_aim_sheet.py"
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

items = (UNITS / "items.lua").read_text(encoding="utf-8")


def extract_loot(loot_id: str):
    span = m._find_moditem_lootdef(items, loot_id)
    if not span:
        return None
    block = items[span[0] : span[1]]
    entries = []
    for um in re.finditer(
        r"PlaceObj\('LootEntryUpgradedWeapon',\s*\{(.*?)\}\),", block, re.S
    ):
        body = um.group(1)
        weapon = re.search(r'weapon\s*=\s*"([^"]+)"', body)
        ups = re.findall(r'"([^"]+)"', body)
        w = weapon.group(1) if weapon else "?"
        ups = [u for u in ups if u != w]
        entries.append(("upg", w, ups))
    for im in re.finditer(
        r"PlaceObj\('LootEntryInventoryItem',\s*\{(.*?)\}\),", block, re.S
    ):
        body = im.group(1)
        item = re.search(r'item\s*=\s*"([^"]+)"', body)
        mn = re.search(r"stack_min\s*=\s*(\d+)", body)
        entries.append(
            ("inv", item.group(1) if item else "?", int(mn.group(1)) if mn else 0)
        )
    for lm in re.finditer(
        r"PlaceObj\('LootEntryLootDef',\s*\{(.*?)\}\),", block, re.S
    ):
        body = lm.group(1)
        ld = re.search(r'loot_def\s*=\s*"([^"]+)"', body)
        w = re.search(r"weight\s*=\s*(\d+)", body)
        if w and int(w.group(1)) in (60000, 30000, 10000):
            continue  # parent weights
        entries.append(("loot", ld.group(1) if ld else "?"))
    return entries


def normalize_target(entries):
    out = []
    for e in entries:
        if e[0] == "inv":
            out.append(("inv", e[1], e[2]))
        elif e[0] == "upg":
            out.append(("upg", e[1], list(e[2])))
        elif e[0] == "loot":
            out.append(("loot", e[1]))
    return out


report = []
all_ok = True
for merc_id, cfg in m.MERCS.items():
    report.append(f"## {merc_id}")
    parent = extract_loot(merc_id)
    report.append(f"parent refs: {parent}")
    for suffix, target in cfg["tiers"].items():
        lid = merc_id + suffix
        cur = extract_loot(lid)
        tgt = normalize_target(target)
        # current may interleave loot refs; order-sensitive compare
        match = cur == tgt
        if not match:
            all_ok = False
        report.append(f"{suffix}% MATCH={match}")
        report.append(f"  current: {cur}")
        report.append(f"  target:  {tgt}")
    report.append("")

# item existence in jazz + jazz-units items
ids = set()
for cfg in m.MERCS.values():
    for entries in cfg["tiers"].values():
        for e in entries:
            if e[0] == "inv":
                ids.add(e[1])
            elif e[0] == "upg":
                ids.add(e[1])
                ids.update(e[2])
jazz_items = (JAZZ / "items.lua").read_text(encoding="utf-8")
ju_items = items
missing = []
for iid in sorted(ids):
    found = (
        f'id = "{iid}"' in ju_items
        or f"'Id', \"{iid}\"" in ju_items
        or f'id = "{iid}"' in jazz_items
        or f"'Id', \"{iid}\"" in jazz_items
    )
    if not found:
        missing.append(iid)
report.append("## Missing InventoryItem / component IDs")
report.append(str(missing) if missing else "(none)")
report.append("")
report.append(f"ALL_TIERS_MATCH={all_ok}")

OUT.write_text("\n".join(report), encoding="utf-8")
print(OUT)
print(f"ALL_TIERS_MATCH={all_ok}")
print(f"missing={missing}")
