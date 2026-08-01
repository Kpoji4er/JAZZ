# -*- coding: utf-8 -*-
"""Audit attachment IDs: prefix, mount, unused."""
import csv
from collections import Counter, defaultdict
from pathlib import Path

DATA = Path("docs/technical/weapons/data")
comps = {r["component_id"]: r for r in csv.DictReader(open(DATA / "weapon-components.csv", encoding="utf-8"))}
weapons = {r["id"]: r for r in csv.DictReader(open(DATA / "weapons.csv", encoding="utf-8"))}
active = {w for w, r in weapons.items() if r.get("catalog_status") == "active"}
opts = list(csv.DictReader(open(DATA / "weapon-component-options.csv", encoding="utf-8")))

used_live = set()
used_any = set()
by_slot_live = defaultdict(set)
mount_live = []

for o in opts:
    cid = (o.get("component_id") or "").strip()
    slot = (o.get("slot_type") or "").lower()
    wid = o["weapon_id"]
    if cid:
        used_any.add(cid)
    if wid not in active:
        continue
    if slot == "mount":
        mount_live.append(o)
        continue
    mod = (o.get("modifiable") or "").lower() == "true"
    is_def = (o.get("is_default") or "").lower() == "true"
    if not mod and not is_def:
        continue
    if cid:
        used_live.add(cid)
        by_slot_live[o.get("slot_type") or "?"].add(cid)

print("comps total", len(comps))
print("used on any option row", len(used_any))
print("used live (active, non-mount, mod|def)", len(used_live))
print("never referenced in options", len(set(comps) - used_any))

never = sorted(set(comps) - used_any)
print("never examples:", never[:25], "...", len(never))

jazz = [c for c in used_live if c.startswith("JAZZ_") or c.startswith("Jazz_")]
non = sorted(used_live - set(jazz))
print("live with jazz prefix", len(jazz))
print("live WITHOUT jazz prefix", len(non))
by_slot = Counter()
for cid in non:
    by_slot[comps.get(cid, {}).get("slot") or "?"] += 1
print("non-prefix by slot:", dict(by_slot))
print("sample non-prefix:", non[:40])

print("mount option rows on active:", len(mount_live))
for o in mount_live:
    print(" ", o["weapon_id"], o.get("component_id"), "mod", o.get("modifiable"), "def", o.get("is_default"))

# slot=Mount comps
mount_comps = sorted(c for c, r in comps.items() if (r.get("slot") or "").lower() == "mount")
print("comps slot=Mount", len(mount_comps), mount_comps)
