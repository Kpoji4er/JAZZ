# -*- coding: utf-8 -*-
"""AKM CTH at 5/10/20 tiles under representative optics (offline JAZZ formula)."""
from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WPN = ROOT / "docs/technical/weapons/data/weapons.csv"
COMP = ROOT / "docs/technical/weapons/data/weapon-components.csv"


def clamp(v, lo, hi):
    return min(hi, max(lo, v))


def round_h(v):
    return math.floor(v + 0.5) if v >= 0 else math.ceil(v - 0.5)


def skill_curve(x):
    x = max(0, x)
    return 20 + (x**1.25) * 0.25


def aim_mastery(m):
    m = clamp(m, 0, 100)
    v = (
        min(m, 60) * 20 / 60
        + clamp(m - 60, 0, 20) * 20 / 20
        + clamp(m - 80, 0, 10) * 20 / 10
        + clamp(m - 90, 0, 6) * 20 / 6
        + clamp(m - 96, 0, 4) * 20 / 4
    )
    return min(100, round_h(v))


def parse_params(s: str) -> dict[str, float]:
    out = {}
    if not s:
        return out
    for part in s.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            try:
                out[k] = float(v)
            except ValueError:
                pass
    return out


def cth(
    *,
    dex,
    mrk,
    lvl,
    aim,
    max_aim,
    aim_accuracy,
    d,
    weapon_range,
    bdr,
    grouping,
    close_range,
    close_range_factor_pct,
    optic_reach,
    optic_min,
    optic_near,  # 0..1 at d=0
):
    snap_raw = (dex * 4 + mrk + lvl * 5) / 6
    prec_raw = (mrk * 4 + dex + lvl * 5) / 6
    snap = skill_curve(snap_raw)
    prec = skill_curve(prec_raw)
    max_aim = max(0, max_aim)
    aim = clamp(aim, 0, max_aim)
    prog = (aim / max_aim) if max_aim else 0.0
    shot_skill = snap + prog * max(prec - snap, 0)
    gain = max(0, aim) * aim_accuracy * aim_mastery(mrk) / 100
    skill_core = clamp(shot_skill + gain, 0, 100)

    R = weapon_range
    if not R or d >= R:
        return 0, {}
    BDR = clamp(bdr, 0, R)
    eps = 0.01
    E = clamp(min(R - eps, BDR + optic_reach * prog), 0, R - eps)
    power = max(1.25, BDR * 0.05 + grouping / 100)
    if d <= E:
        rf = 1.0
    else:
        t = clamp((d - E) / (R - E), 0, 1)
        rf = 0.25 + (1 - 0.25) * (1 - t**power)

    core = skill_core * rf

    # optic near
    near = 1.0
    if optic_min > 0 and d < optic_min:
        prox = clamp((optic_min - d) / optic_min, 0, 1)
        near = 1 + (optic_near - 1) * prox

    # weapon close-range
    close = 1.0
    if close_range > 0 and d < close_range:
        f0 = close_range_factor_pct / 100.0
        prox = clamp((close_range - d) / close_range, 0, 1)
        close = 1 + (f0 - 1) * prox

    final = int(clamp(round_h(core * near * close), 2, 100))
    return final, {
        "skill": round(skill_core, 1),
        "gain": round(gain, 1),
        "prog": round(prog, 2),
        "E": round(E, 1),
        "rf": round(rf, 3),
        "near": round(near, 3),
        "close": round(close, 3),
        "AA": round(aim_accuracy, 2),
        "aim": aim,
        "max": max_aim,
        "reach": optic_reach,
    }


def optic_profile(comp: dict | None, aim: int):
    """Return reach, min_range, near_factor(0..1) for current aim."""
    if not comp:
        return 0.0, 0.0, 1.0
    fx = set((comp.get("effects") or "").split(";"))
    p = parse_params(comp.get("parameters") or "")
    cid = comp["component_id"]

    if "ScopeMagnification" in fx:
        mag = p.get("ScopeMagnification", 1) + p.get("ScopeSubMagnification", 0) / 10
        aim_level = int(p.get("ScopeAimLevel", 0))
        aim_ok = aim >= aim_level
        reach = (p.get("OpticReach") if "OpticReach" in p else max(0, (mag - 1) * 3)) if aim_ok else 0
        if "OpticMinRange" in p:
            min_r = p["OpticMinRange"]
        else:
            min_r = round(mag * 0.9) if mag >= 4 else 0
        if "OpticNearFactor" in p:
            near = p["OpticNearFactor"] / 100.0
        elif mag >= 4:
            near = max(0.35, 1 - (mag - 2) * 0.09)
        else:
            near = 1.0
        return float(reach), float(min_r), float(near)

    # Reflex / no ScopeMagnification → fallback (name contains Reflex)
    if "Reflex" in cid or "Reflex" in (comp.get("display_name") or ""):
        # aim_level 0, reach 2 always when mounted
        return 2.0, 0.0, 1.0

    return 0.0, 0.0, 1.0


def setup_weapon(base: dict, comp: dict | None):
    aa = float(base["aim_accuracy"])
    max_aim = int(float(base["max_aim_actions"]))
    if not comp:
        return aa, max_aim, False
    fx = set((comp.get("effects") or "").split(";"))
    p = parse_params(comp.get("parameters") or "")
    # Legacy always-on AA% effect (non-optic stocks etc.) still baked in if present.
    if "IncreaseAimAccuracy15Percent" in fx and "AimAccuracyPercent" in p:
        aa = aa * p["AimAccuracyPercent"] / 100.0
    if "DecreaseMaxAimActions" in fx:
        max_aim -= int(p.get("MaxAimActionsDecrease", 0))
    if "IncreaseMaxAimActions" in fx:
        max_aim += int(p.get("IncreaseMaxAimActions", 0) or p.get("MaxAimActionsIncrease", 0) or 0)
    mina = "MinAim" in fx
    return aa, max(0, max_aim), mina


def optic_aim_accuracy(base_aa: float, comp: dict | None, aim: int) -> float:
    """Mirror JAZZ_CTHGetOpticAimAccuracyPercent: AA% only when AimLevel met."""
    if not comp:
        return base_aa
    fx = set((comp.get("effects") or "").split(";"))
    p = parse_params(comp.get("parameters") or "")
    # If still using legacy always-on effect, base_aa already includes it — don't double-apply.
    if "IncreaseAimAccuracy15Percent" in fx:
        return base_aa
    pct = p.get("AimAccuracyPercent")
    if pct is None:
        return base_aa
    if "ScopeMagnification" in fx:
        unlock = int(p.get("AimAccuracyAimLevel", p.get("ScopeAimLevel", 0)))
    elif "MinAim" in fx:
        unlock = int(p.get("AimAccuracyAimLevel", 1))
    else:
        unlock = int(p.get("AimAccuracyAimLevel", 0))
    if aim >= unlock:
        return base_aa * pct / 100.0
    return base_aa


def main():
    base = next(r for r in csv.DictReader(WPN.open(encoding="utf-8")) if r["id"] == "AKM")
    comps = {r["component_id"]: r for r in csv.DictReader(COMP.open(encoding="utf-8"))}

    # label, component_id or None
    optics = [
        ("Irons", None),
        ("Reflex Aimpoint5000", "JAZZ_Reflex_Aimpoint5000"),
        ("Reflex Closed", "JAZZ_Reflex_Closed"),
        ("Reflex M68", "JAZZ_Reflex_M68"),
        ("Reflex PKAS", "JAZZ_Reflex_PKAS"),
        ("Reflex Open (OW)", "JAZZ_Reflex_Open"),
        ("Reflex Eotech", "JAZZ_Reflex_Eotech"),
        ("Combat 2x", "JAZZ_CombatScope_2x"),
        ("Combat ACOG 4x", "JAZZ_CombatScope_ACOG"),
        ("PSO 4x", "JAZZ_Scope_PSO"),
        ("Scope 6x", "JAZZ_Scope_6x"),
        ("Scout ~7x", "JAZZ_Scope_Scout"),
        ("Mark4 10x", "JAZZ_Scope_12x"),
    ]

    # Merc profile: solid mid (Dex70 Mrk70 Lvl5) — readable deltas
    dex, mrk, lvl = 70, 70, 5
    dists = [5, 10, 20]

    print(f"AKM AA={base['aim_accuracy']} MaxAim={base['max_aim_actions']} BDR={base['bullet_drop_range']} R={base['weapon_range']} Close={base['close_range']}@{base['close_range_factor']}%")
    print(f"Shooter Dex={dex} Mrk={mrk} Lvl={lvl} mastery={aim_mastery(mrk)}")
    print("Modes: snap(=min aim), +1 paid click, full aim")
    print()

    modes = [
        ("snap", lambda mina, mx: 1 if mina else 0),
        ("+1clk", lambda mina, mx: min(mx, (1 if mina else 0) + 1)),
        ("full", lambda mina, mx: mx),
    ]

    for mode_name, aim_fn in modes:
        print(f"=== {mode_name} ===")
        hdr = f"{'optic':22} " + " ".join(f"{d:>7}" for d in dists) + "   notes"
        print(hdr)
        print("-" * len(hdr))
        base_vals = None
        for label, cid in optics:
            comp = comps.get(cid) if cid else None
            aa, max_aim, mina = setup_weapon(base, comp)
            aim = aim_fn(mina, max_aim)
            aa = optic_aim_accuracy(aa, comp, aim)
            reach, omin, onear = optic_profile(comp, aim)
            vals = []
            detail = None
            for d in dists:
                v, info = cth(
                    dex=dex,
                    mrk=mrk,
                    lvl=lvl,
                    aim=aim,
                    max_aim=max_aim,
                    aim_accuracy=aa,
                    d=d,
                    weapon_range=int(float(base["weapon_range"])),
                    bdr=int(float(base["bullet_drop_range"])),
                    grouping=int(float(base["grouping"])),
                    close_range=int(float(base["close_range"])),
                    close_range_factor_pct=int(float(base["close_range_factor"])),
                    optic_reach=reach,
                    optic_min=omin,
                    optic_near=onear,
                )
                vals.append(v)
                detail = info
            if base_vals is None:
                base_vals = vals
                delta = ""
            else:
                delta = "  Δ " + "/".join(
                    f"{vals[i]-base_vals[i]:+d}" for i in range(len(dists))
                )
            note = f"aim={detail['aim']}/{detail['max']} AA={detail['AA']} reach={detail['reach']} E@full≈{detail['E']}"
            print(
                f"{label:22} "
                + " ".join(f"{v:6d}%" for v in vals)
                + f"  {note}{delta}"
            )
        print()


if __name__ == "__main__":
    main()
