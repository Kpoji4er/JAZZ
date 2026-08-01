# -*- coding: utf-8 -*-
"""Optic CTH matrix on a reference firearm (default: DragunovSVD).

AKM was exploratory for AR CQB; long/mid optic roles evaluate better on SVD-class
(BDR/R/Close suited to optics). Optics listed are design archetypes, not only
the weapon's AvailableComponents.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SIM_PATH = ROOT / "docs/tools/_sim_akm_optic_cth.py"

spec = importlib.util.spec_from_file_location("sim", SIM_PATH)
sim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sim)

WPN_CSV = ROOT / "docs/technical/weapons/data/weapons.csv"
COMP_CSV = ROOT / "docs/technical/weapons/data/weapon-components.csv"
OPT_CSV = ROOT / "docs/technical/weapons/data/weapon-component-options.csv"

# Design archetypes to always show (even if not on this gun's slot list)
ARCHETYPES = [
    ("Irons", None),
    # Reflex
    ("Reflex T1 Aimpoint5000", "JAZZ_Reflex_Aimpoint5000"),
    ("Reflex T2 Closed", "JAZZ_Reflex_Closed"),
    ("Reflex T3 M68", "JAZZ_Reflex_M68"),
    ("Reflex T4 PKAS", "JAZZ_Reflex_PKAS"),
    ("Reflex OW Open", "JAZZ_Reflex_Open"),
    ("Reflex Uni Eotech", "JAZZ_Reflex_Eotech"),
    # Combat
    ("Combat T1 2x", "JAZZ_CombatScope_2x"),
    ("Combat T2 3x", "JAZZ_CombatScope_3x"),
    ("Combat T3 ACOG", "JAZZ_CombatScope_ACOG"),
    ("Combat T3 1P29", "JAZZ_CombatScope_1P29"),
    # Long entry / vintage (T1) then classic long ladder
    ("Long T1 PU 3x", "JAZZ_Scope_PU"),
    ("Long T1 Garand 2x", "JAZZ_Scope_Garand"),
    ("Long T1 Springfield 2x", "JAZZ_Scope_Springfield"),
    ("Long T2 PSO", "JAZZ_Scope_PSO"),
    ("Long T2 ZF4", "JAZZ_Scope_ZF4"),
    ("Long T3 6x", "JAZZ_Scope_6x"),
    ("Long T4 Scout", "JAZZ_Scope_Scout"),
    ("Long T5 10x", "JAZZ_Scope_12x"),
    # Night
    ("Night NSPU", "JAZZ_NightScope_NSPU"),
    ("Night 5x", "JAZZ_NightScope"),
]


def load_weapon(weapon_id: str) -> dict:
    return next(r for r in csv.DictReader(WPN_CSV.open(encoding="utf-8")) if r["id"] == weapon_id)


def slot_scopes(weapon_id: str) -> set[str]:
    return {
        r["component_id"]
        for r in csv.DictReader(OPT_CSV.open(encoding="utf-8"))
        if r["weapon_id"] == weapon_id and r["slot_type"] == "Scope"
    }


def run_row(wpn: dict, comps: dict, cid: str | None, dex: int, mrk: int, lvl: int, dists: list[int], mode: str):
    base = wpn
    comp = comps.get(cid) if cid else None
    aa, mx, mina = sim.setup_weapon(base, comp)
    if mode == "snap":
        aim = 1 if mina else 0
    elif mode == "plus1":
        aim = min(mx, (1 if mina else 0) + 1)
    else:
        aim = mx
    aa = sim.optic_aim_accuracy(aa, comp, aim)
    reach, omin, onear = sim.optic_profile(comp, aim)
    # CloseRangeFactor may be buffed by reflex CloseRangeFactorIncrease
    close_pct = int(float(base["close_range_factor"]))
    if comp:
        fx = set((comp.get("effects") or "").split(";"))
        p = sim.parse_params(comp.get("parameters") or "") if hasattr(sim, "parse_params") else {}
        # inline parse
        p = {}
        for part in (comp.get("parameters") or "").split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                try:
                    p[k] = float(v)
                except ValueError:
                    pass
        if "CloseRangeFactorIncrease" in fx and "CloseRangeFactorIncrease" in p:
            close_pct = int(close_pct + p["CloseRangeFactorIncrease"])
            close_pct = min(150, close_pct)

    vals = []
    info = None
    for d in dists:
        v, info = sim.cth(
            dex=dex,
            mrk=mrk,
            lvl=lvl,
            aim=aim,
            max_aim=mx,
            aim_accuracy=aa,
            d=d,
            weapon_range=int(float(base["weapon_range"])),
            bdr=int(float(base["bullet_drop_range"])),
            grouping=int(float(base["grouping"])),
            close_range=int(float(base["close_range"])),
            close_range_factor_pct=close_pct,
            optic_reach=reach,
            optic_min=omin,
            optic_near=onear,
        )
        vals.append(v)
    return vals, info, aim, mx, aa, reach, omin, onear, close_pct


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weapon", default="DragunovSVD")
    ap.add_argument("--dex", type=int, default=70)
    ap.add_argument("--mrk", type=int, default=70)
    ap.add_argument("--lvl", type=int, default=5)
    ap.add_argument(
        "--dists",
        default="5,10,20,25,30,40,50",
        help="comma-separated tile distances",
    )
    ap.add_argument("--mode", default="full", choices=["snap", "plus1", "full", "all"])
    args = ap.parse_args()

    wpn = load_weapon(args.weapon)
    comps = {r["component_id"]: r for r in csv.DictReader(COMP_CSV.open(encoding="utf-8"))}
    on_gun = slot_scopes(args.weapon)
    dists = [int(x) for x in args.dists.split(",") if x.strip()]

    print(
        f"{args.weapon} AA={wpn['aim_accuracy']} MaxAim={wpn['max_aim_actions']} "
        f"BDR={wpn['bullet_drop_range']} R={wpn['weapon_range']} "
        f"Close={wpn['close_range']}@{wpn['close_range_factor']}% tier={wpn.get('tier_label')}"
    )
    print(f"Shooter Dex={args.dex} Mrk={args.mrk} Lvl={args.lvl} mastery={sim.aim_mastery(args.mrk)}")
    print(f"Scope slot on gun: {len(on_gun)} options; matrix shows design archetypes (* = on this gun)")
    print()

    modes = ["snap", "plus1", "full"] if args.mode == "all" else [args.mode]
    for mode in modes:
        print(f"=== {mode} ===")
        hdr = f"{'optic':28} {'gun':>3} " + " ".join(f"{d:>5}" for d in dists) + "   meta"
        print(hdr)
        print("-" * len(hdr))
        base_vals = None
        for label, cid in ARCHETYPES:
            if cid and cid not in comps:
                print(f"{label:28} MISSING {cid}")
                continue
            vals, info, aim, mx, aa, reach, omin, onear, cp = run_row(
                wpn, comps, cid, args.dex, args.mrk, args.lvl, dists, mode
            )
            mark = "*" if (cid is None or cid in on_gun) else " "
            if base_vals is None:
                base_vals = vals
                delta = ""
            else:
                delta = "  d " + "/".join(f"{vals[i]-base_vals[i]:+d}" for i in range(len(dists)))
            meta = (
                f"aim={aim}/{mx} AA={aa:.1f} r={reach:g} "
                f"near={omin:g}@{onear:.0%} cf={cp} E={info['E']}"
            )
            print(
                f"{label:28} {mark:>3} "
                + " ".join(f"{v:4d}%" for v in vals)
                + f"  {meta}{delta}"
            )
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
