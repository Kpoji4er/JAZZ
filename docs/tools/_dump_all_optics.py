# -*- coding: utf-8 -*-
import csv
import re
from pathlib import Path

comps = list(csv.DictReader(Path("docs/technical/weapons/data/weapon-components.csv").open(encoding="utf-8")))
scopes = [c for c in comps if (c.get("slot") or "").lower() == "scope" and c["component_id"].startswith("JAZZ_")]


def group_of(cid: str) -> str:
    if "Reflex" in cid:
        return "Reflex"
    if "Night" in cid:
        return "Night"
    if "Combat" in cid:
        return "Combat"
    if re.search(r"Scope_(12x|6x|Scout|PSO|3x|8x|DA|ZF)", cid) or "Scope_" in cid:
        return "Scope"
    if "Iron" in cid or "Ironsight" in cid or "Sight" in cid:
        return "Iron/built-in"
    return "Other"


def parse_params(s: str) -> dict:
    out = {}
    if not s:
        return out
    for part in s.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


order = {"Reflex": 0, "Combat": 1, "Scope": 2, "Night": 3, "Iron/built-in": 4, "Other": 5}
scopes.sort(key=lambda c: (order.get(group_of(c["component_id"]), 9), c["component_id"]))

cur = None
for c in scopes:
    g = group_of(c["component_id"])
    if g != cur:
        print(f"\n### {g}")
        cur = g
    p = parse_params(c["parameters"] or "")
    fx = (c["effects"] or "").replace(";", ", ")
    bits = []
    for k in (
        "ScopeMagnification",
        "ScopeAimLevel",
        "SmallMagnification",
        "SmallAimLevel",
        "AimAccuracyPercent",
        "ScopeOverwatchAngle",
        "extra_attacks",
        "bonus_cth",
        "ShotAP",
        "IncreaseMaxAimActions",
        "MaxAimActionsDecrease",
    ):
        if k in p:
            bits.append(f"{k}={p[k]}")
    print(f"- {c['component_id']} | {c['display_name']} | cost={c['cost']} used={c['used_by_count']}")
    print(f"  params: {', '.join(bits) if bits else '—'}")
    print(f"  effects: {fx or '—'}")

print(f"\nTOTAL {len(scopes)}")
