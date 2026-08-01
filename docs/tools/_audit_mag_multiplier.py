# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "docs/technical/weapons/data"

opts = list(csv.DictReader((DATA / "weapon-component-options.csv").open(encoding="utf-8")))
comps = {r["component_id"]: r for r in csv.DictReader((DATA / "weapon-components.csv").open(encoding="utf-8"))}
weps = {r["id"]: r for r in csv.DictReader((DATA / "weapons.csv").open(encoding="utf-8"))}

mult_comps = []
for cid, c in comps.items():
    eff = c.get("effects") or ""
    if "MagazineSizeMultiplier" not in eff:
        continue
    params = c.get("parameters") or ""
    mult = None
    for p in params.split(";"):
        if p.startswith("MagazineSizeMultiplier="):
            mult = int(p.split("=")[1])
    mult_comps.append((cid, mult, c.get("display_name") or ""))

print("=== components with MagazineSizeMultiplier ===")
for cid, mult, name in sorted(mult_comps):
    print(f"{cid}\tx{mult}\t{name}")

print("\n=== mounts (weapon base -> approx final) ===")
by_comp = defaultdict(list)
for o in opts:
    if o.get("slot_type") != "Magazine":
        continue
    cid = o.get("component_id") or ""
    c = comps.get(cid)
    if not c or "MagazineSizeMultiplier" not in (c.get("effects") or ""):
        continue
    params = c.get("parameters") or ""
    mult = None
    for p in params.split(";"):
        if p.startswith("MagazineSizeMultiplier="):
            mult = int(p.split("=")[1])
    wid = o["weapon_id"]
    base = int((weps.get(wid) or {}).get("magazine_size") or 0)
    final = round(base * mult / 100) if mult and base else None
    add = (final - base) if final is not None else None
    by_comp[cid].append((wid, base, mult, final, add, o.get("is_default")))

for cid, rows in sorted(by_comp.items()):
    print(f"\n{cid}")
    groups = defaultdict(list)
    for wid, base, mult, final, add, d in rows:
        groups[(base, final, add)].append(wid)
    for (base, final, add), wids in sorted(groups.items()):
        print(f"  base {base} -> ~{final} (add +{add}): {', '.join(sorted(wids))}")
