# -*- coding: utf-8 -*-
"""AKM accuracy-relevant optic comparison (static levers)."""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
COMP_CSV = ROOT / "docs/technical/weapons/data/weapon-components.csv"
OPT_CSV = ROOT / "docs/technical/weapons/data/weapon-component-options.csv"
WPN_CSV = ROOT / "docs/technical/weapons/data/weapons.csv"


def parse_params(s: str) -> dict[str, str]:
    out = {}
    if not s:
        return out
    for part in s.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k] = v
    return out


def main() -> None:
    wpn = next(r for r in csv.DictReader(WPN_CSV.open(encoding="utf-8")) if r["id"] == "AKM")
    print("AKM base:")
    for k in [
        "aim_accuracy",
        "max_aim_actions",
        "weapon_range",
        "bullet_drop_range",
        "close_range",
        "close_range_factor",
        "tier_label",
    ]:
        print(f"  {k}={wpn.get(k)}")

    opts = [
        r["component_id"]
        for r in csv.DictReader(OPT_CSV.open(encoding="utf-8"))
        if r["weapon_id"] == "AKM" and r["slot_type"] == "Scope"
    ]
    comps = {
        r["component_id"]: r
        for r in csv.DictReader(COMP_CSV.open(encoding="utf-8"))
        if r["component_id"] in opts or r["component_id"] in {
            "JAZZ_Reflex_Garand",
            "JAZZ_Reflex_PKAS",
            "JAZZ_Reflex_Pistol",
            "JAZZ_CombatScope_3x",
            "JAZZ_CombatScope_FeroZ24",
            "JAZZ_Scope_PSO",
            "JAZZ_Scope_6x",
            "JAZZ_Scope_12x",
            "JAZZ_Scope_Scout",
        }
    }

    print("\nAKM Scope slot options:")
    rows = []
    for cid in opts:
        r = comps.get(cid)
        if not r:
            print("  MISSING", cid)
            continue
        p = parse_params(r["parameters"])
        fx = set(r["effects"].split(";")) if r["effects"] else set()
        rows.append((cid, r, p, fx))

    # also note irons: empty scope
    print(f"  (empty / irons) — base AA={wpn.get('aim_accuracy')} MaxAim={wpn.get('max_aim_actions')}")

    hdr = f"{'optic':36} {'AA%':>4} {'MinA':>4} {'-Max':>4} {'Mag':>3} {'AimL':>4} {'Near':>8} {'OW':>5} {'ShotAP':>6} {'Crit':>4}"
    print("\n" + hdr)
    print("-" * len(hdr))
    print(f"{'(irons / empty Scope)':36} {'—':>4} {'—':>4} {'—':>4} {'—':>3} {'—':>4} {'—':>8} {'—':>5} {'—':>6} {'—':>4}")

    for cid, r, p, fx in rows:
        aa = p.get("AimAccuracyPercent", "—")
        mina = "yes" if "MinAim" in fx else "—"
        dmax = p.get("MaxAimActionsDecrease", "—") if "DecreaseMaxAimActions" in fx else "—"
        mag = p.get("ScopeMagnification", "—")
        aiml = p.get("ScopeAimLevel", "—")
        near = ""
        if p.get("OpticMinRange") or p.get("OpticNearFactor"):
            near = f"{p.get('OpticMinRange','?')}@{p.get('OpticNearFactor','?')}%"
        elif mag not in ("—", None) and "ScopeMagnification" in fx:
            near = "default"
        else:
            near = "—"
        ow = p.get("ScopeOverwatchAngle", "—")
        shot = p.get("ShotAP", "—") if "IncreaseShotAP" in fx else "—"
        crit = "yes" if "CritBonusWhenFullyAimed" in fx else "—"
        name = (r.get("display_name") or cid)[:34]
        print(f"{name:36} {aa:>4} {mina:>4} {dmax:>4} {mag:>3} {aiml:>4} {near:>8} {ow:>5} {shot:>6} {crit:>4}")

    # Effective MaxAim / AA sketch
    base_aa = int(float(wpn["aim_accuracy"]))
    base_max = int(float(wpn["max_aim_actions"]))
    print(f"\nSketch (AA multiply only; MinAim floor +1; MaxAim after -N):")
    print(f"{'optic':36} {'effAA':>5} {'minAim':>6} {'maxAim':>6} {'aim@1clk':>8} {'full clicks':>11}")
    print("-" * 80)
    print(f"{'(irons)':36} {base_aa:>5} {0:>6} {base_max:>6} {1:>8} {base_max:>11}")
    for cid, r, p, fx in rows:
        aa_pct = int(p["AimAccuracyPercent"]) if "AimAccuracyPercent" in p else 100
        eff_aa = round(base_aa * aa_pct / 100, 1)
        mina = 1 if "MinAim" in fx else 0
        dmax = int(p.get("MaxAimActionsDecrease", 0) or 0) if "DecreaseMaxAimActions" in fx else 0
        # IncreaseMaxAimActions?
        imax = int(p.get("IncreaseMaxAimActions", 0) or 0) if "IncreaseMaxAimActions" in fx else 0
        max_aim = base_max - dmax + imax
        # clicks available from min: if MinAim, first paid click starts higher — model: free floor mina, paid clicks = max_aim - mina
        # aim level after 1 paid click:
        aim_after_1 = mina + 1
        name = (r.get("display_name") or cid)[:34]
        print(f"{name:36} {eff_aa:>5} {mina:>6} {max_aim:>6} {aim_after_1:>8} {max(0,max_aim-mina):>11}")


if __name__ == "__main__":
    main()
