# -*- coding: utf-8 -*-
"""Dump long-scope profiles + AKM CTH at 5/20/25/30/35."""
from __future__ import annotations

import csv
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "docs/tools"))
from _apply_attach_001 import placeobj_blocks, prop

spec = importlib.util.spec_from_file_location("sim", ROOT / "docs/tools/_sim_akm_optic_cth.py")
sim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sim)

ITEMS = ROOT / "items.lua"
WPN = next(
    r
    for r in csv.DictReader((ROOT / "docs/technical/weapons/data/weapons.csv").open(encoding="utf-8"))
    if r["id"] == "AKM"
)

LONG_IDS = [
    "JAZZ_Scope_PSO",
    "JAZZ_Scope_6x",
    "JAZZ_Scope_Scout",
    "JAZZ_Scope_12x",
    "JAZZ_Scope_3x_9x",
    "JAZZ_Scope_8x_SCROME",
    "JAZZ_Scope_DA15_6x",
    "JAZZ_Scope_ZF4",
    "JAZZ_Scope_PU",
    "JAZZ_Scope_Springfield",
    "JAZZ_Scope_Garand",
    "JAZZ_NightScope",
    "JAZZ_NightScope_NSPU",
]


def parse_block(text: str) -> dict:
    fx_m = re.search(r"ModificationEffects = \{(.*?)\},", text, re.S)
    fx = re.findall(r'"([^"]+)"', fx_m.group(1)) if fx_m else []
    params = {}
    for m in re.finditer(
        r"'Name', \"([^\"]+)\"\s*,\s*(?:'Value', ([^\n,]+),)?",
        text,
    ):
        name, val = m.group(1), m.group(2)
        if val is not None:
            params[name] = val.strip()
        else:
            params.setdefault(name, None)
    cost = re.search(r"Cost = (\d+)", text)
    return {
        "fx": fx,
        "params": params,
        "cost": int(cost.group(1)) if cost else None,
    }


def main():
    text = ITEMS.read_text(encoding="utf-8")
    blocks = {}
    for b in placeobj_blocks(text, "ModItemWeaponComponent"):
        cid = prop(b.text, "id")
        if cid in LONG_IDS:
            blocks[cid] = parse_block(b.text)

    print("=== Current long/night profiles ===")
    for cid in LONG_IDS:
        if cid not in blocks:
            print(cid, "MISSING")
            continue
        d = blocks[cid]
        p = d["params"]
        keys = [
            "ScopeMagnification",
            "ScopeAimLevel",
            "ScopeOverwatchAngle",
            "ShotAP",
            "IncreaseMaxAimActions",
            "AimAccuracyPercent",
            "OpticMinRange",
            "OpticNearFactor",
        ]
        pp = {k: p.get(k) for k in keys if k in p}
        print(f"{cid}: cost={d['cost']} fx={d['fx']}")
        print(f"  {pp}")

    base_aa = float(WPN["aim_accuracy"])
    base_max = int(float(WPN["max_aim_actions"]))
    dex, mrk, lvl = 70, 70, 5
    dists = [5, 20, 25, 30, 35]

    def run(aim, mx, aa, d, reach, omin, onear):
        v, info = sim.cth(
            dex=dex,
            mrk=mrk,
            lvl=lvl,
            aim=aim,
            max_aim=mx,
            aim_accuracy=aa,
            d=d,
            weapon_range=int(float(WPN["weapon_range"])),
            bdr=int(float(WPN["bullet_drop_range"])),
            grouping=int(float(WPN["grouping"])),
            close_range=int(float(WPN["close_range"])),
            close_range_factor_pct=int(float(WPN["close_range_factor"])),
            optic_reach=reach,
            optic_min=omin,
            optic_near=onear,
        )
        return v, info

    print("\n=== AKM CTH now (full aim) ===")
    print(f"{'optic':16}", " ".join(f"{d:>5}" for d in dists), "  E reach")
    # irons
    row = []
    for d in dists:
        v, info = run(3, 3, base_aa, d, 0, 0, 1)
        row.append(v)
    print(f"{'Irons':16}", " ".join(f"{v:4d}%" for v in row), f"  E={info['E']}")

    # ACOG current for compare
    comps = {
        r["component_id"]: r
        for r in csv.DictReader(
            (ROOT / "docs/technical/weapons/data/weapon-components.csv").open(encoding="utf-8")
        )
    }
    for label, cid in [
        ("ACOG", "JAZZ_CombatScope_ACOG"),
        ("PSO", "JAZZ_Scope_PSO"),
        ("6x", "JAZZ_Scope_6x"),
        ("Scout", "JAZZ_Scope_Scout"),
        ("12x", "JAZZ_Scope_12x"),
    ]:
        c = comps[cid]
        aa, mx, _ = sim.setup_weapon(WPN, c)
        # use max aim
        aim = mx
        reach, omin, onear = sim.optic_profile(c, aim)
        row = []
        for d in dists:
            v, info = run(aim, mx, aa, d, reach, omin, onear)
            row.append(v)
        print(
            f"{label:16}",
            " ".join(f"{v:4d}%" for v in row),
            f"  aim={aim}/{mx} reach={reach} E={info['E']} near={omin}@{onear:.0%}",
        )

    # Preferred-mode ratios at 25/30 vs irons full
    print("\n=== vs irons full ===")
    iron25 = run(3, 3, base_aa, 25, 0, 0, 1)[0]
    iron30 = run(3, 3, base_aa, 30, 0, 0, 1)[0]
    iron5 = run(3, 3, base_aa, 5, 0, 0, 1)[0]
    print(f"irons full 5/25/30 = {iron5}/{iron25}/{iron30}")
    for cid in ["JAZZ_CombatScope_ACOG", "JAZZ_Scope_PSO", "JAZZ_Scope_6x", "JAZZ_Scope_Scout", "JAZZ_Scope_12x"]:
        c = comps[cid]
        aa, mx, _ = sim.setup_weapon(WPN, c)
        reach, omin, onear = sim.optic_profile(c, mx)
        v5 = run(mx, mx, aa, 5, reach, omin, onear)[0]
        v25 = run(mx, mx, aa, 25, reach, omin, onear)[0]
        v30 = run(mx, mx, aa, 30, reach, omin, onear)[0]
        print(
            f"{cid:28} 5={v5} ({v5/iron5:.2f}x) 25={v25} ({v25/iron25:.2f}x) 30={v30} ({v30/iron30:.2f}x)"
        )


if __name__ == "__main__":
    main()
