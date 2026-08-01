# -*- coding: utf-8 -*-
"""Calibrate optic levers for AKM toward +20% close (reflex) / +20-30% mid (combat)."""
from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SIM = ROOT / "docs/tools/_sim_akm_optic_cth.py"

spec = importlib.util.spec_from_file_location("sim", SIM)
sim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sim)

WPN = next(
    r
    for r in csv.DictReader(
        (ROOT / "docs/technical/weapons/data/weapons.csv").open(encoding="utf-8")
    )
    if r["id"] == "AKM"
)


def base_w():
    return dict(
        weapon_range=int(float(WPN["weapon_range"])),
        bdr=int(float(WPN["bullet_drop_range"])),
        grouping=int(float(WPN["grouping"])),
        close_range=int(float(WPN["close_range"])),
        close_range_factor_pct=int(float(WPN["close_range_factor"])),
        base_aa=float(WPN["aim_accuracy"]),
        base_max=int(float(WPN["max_aim_actions"])),
    )


def eval_cth(
    *,
    dex,
    mrk,
    lvl,
    aim,
    max_aim,
    aa,
    d,
    reach,
    omin,
    onear,
    close_range=None,
    close_pct=None,
):
    w = base_w()
    v, info = sim.cth(
        dex=dex,
        mrk=mrk,
        lvl=lvl,
        aim=aim,
        max_aim=max_aim,
        aim_accuracy=aa,
        d=d,
        weapon_range=w["weapon_range"],
        bdr=w["bdr"],
        grouping=w["grouping"],
        close_range=close_range if close_range is not None else w["close_range"],
        close_range_factor_pct=close_pct if close_pct is not None else w["close_range_factor_pct"],
        optic_reach=reach,
        optic_min=omin,
        optic_near=onear,
    )
    return v, info


def irons(dex, mrk, lvl, aim, d):
    w = base_w()
    return eval_cth(
        dex=dex,
        mrk=mrk,
        lvl=lvl,
        aim=aim,
        max_aim=w["base_max"],
        aa=w["base_aa"],
        d=d,
        reach=0,
        omin=0,
        onear=1,
    )[0]


def find_aa_pct_for_target(
    *,
    dex,
    mrk,
    lvl,
    aim,
    max_aim,
    d,
    reach,
    omin,
    onear,
    target,
    close_range=None,
    close_pct=None,
    lo=100,
    hi=250,
):
    """Binary search AimAccuracyPercent on base AA."""
    w = base_w()
    best = None
    for pct in range(lo, hi + 1):
        aa = w["base_aa"] * pct / 100.0
        v, _ = eval_cth(
            dex=dex,
            mrk=mrk,
            lvl=lvl,
            aim=aim,
            max_aim=max_aim,
            aa=aa,
            d=d,
            reach=reach,
            omin=omin,
            onear=onear,
            close_range=close_range,
            close_pct=close_pct,
        )
        if v >= target:
            return pct, v
        best = (pct, v)
    return best


def find_reach_for_target(
    *,
    dex,
    mrk,
    lvl,
    aim,
    max_aim,
    aa,
    d,
    omin,
    onear,
    target,
):
    best = None
    for reach in range(0, 40):
        v, info = eval_cth(
            dex=dex,
            mrk=mrk,
            lvl=lvl,
            aim=aim,
            max_aim=max_aim,
            aa=aa,
            d=d,
            reach=reach,
            omin=omin,
            onear=onear,
        )
        if v >= target:
            return reach, v, info["E"]
        best = (reach, v, info["E"])
    return best


def main():
    # Calibration shooter: mid merc (readable campaign baseline)
    dex, mrk, lvl = 70, 70, 5
    w = base_w()
    print(f"AKM AA={w['base_aa']} MaxAim={w['base_max']} BDR={w['bdr']} R={w['weapon_range']}")
    print(f"Shooter Dex={dex} Mrk={mrk} Lvl={lvl} mastery={sim.aim_mastery(mrk)}")
    print()

    # --- Irons baselines ---
    print("=== Irons baselines ===")
    for label, aim, d in [
        ("snap@5", 0, 5),
        ("snap@10", 0, 10),
        ("+1@5", 1, 5),
        ("+1@10", 1, 10),
        ("full@5", 3, 5),
        ("full@10", 3, 10),
        ("full@20", 3, 20),
    ]:
        print(f"  {label:10} {irons(dex, mrk, lvl, aim, d)}%")
    print()

    # Targets relative to irons same mode
    # Reflex: close band, short aim (snap with MinAim=aim1, and +1clk=aim2)
    iron_snap5 = irons(dex, mrk, lvl, 0, 5)
    iron_snap10 = irons(dex, mrk, lvl, 0, 10)
    iron_p1_5 = irons(dex, mrk, lvl, 1, 5)
    iron_p1_10 = irons(dex, mrk, lvl, 1, 10)
    iron_full20 = irons(dex, mrk, lvl, 3, 20)
    iron_full10 = irons(dex, mrk, lvl, 3, 10)

    t_reflex_snap5 = round(iron_snap5 * 1.20)
    t_reflex_snap10 = round(iron_snap10 * 1.20)
    t_reflex_p1_5 = round(iron_p1_5 * 1.20)
    t_combat_20_lo = round(iron_full20 * 1.20)
    t_combat_20_hi = round(iron_full20 * 1.30)

    print("=== Targets (x1.20 / x1.30 vs irons same mode) ===")
    print(f"  Reflex snap@5:  {iron_snap5} -> {t_reflex_snap5}  (+{t_reflex_snap5 - iron_snap5})")
    print(f"  Reflex snap@10: {iron_snap10} -> {t_reflex_snap10}")
    print(f"  Reflex +1clk@5: {iron_p1_5} -> {t_reflex_p1_5}")
    print(f"  Combat full@20: {iron_full20} -> {t_combat_20_lo}..{t_combat_20_hi}")
    print()

    # --- Reflex path A: AA% only (MinAim, MaxAim=2, reach=2, no near) ---
    print("=== Reflex: AA% only (MinAim aim=1/2, reach=2) ===")
    for label, aim, d, target in [
        ("T4 snap@5", 1, 5, t_reflex_snap5),
        ("T4 snap@10", 1, 10, t_reflex_snap10),
        ("T4 +1@5 (=full)", 2, 5, t_reflex_p1_5),
    ]:
        pct, v = find_aa_pct_for_target(
            dex=dex,
            mrk=mrk,
            lvl=lvl,
            aim=aim,
            max_aim=2,
            d=d,
            reach=2,
            omin=0,
            onear=1,
            target=target,
        )
        print(f"  {label:18} need AimAccuracyPercent>={pct} -> {v}% (target {target})")
    print()

    # --- Reflex path B: AA% + CloseRangeFactor buff (reflex softens hip deadzone) ---
    print("=== Reflex: AA% + CloseRangeFactor=100 (cancel AKM 85% hip) ===")
    for label, aim, d, target in [
        ("T4 snap@5", 1, 5, t_reflex_snap5),
        ("T4 +1@5", 2, 5, t_reflex_p1_5),
    ]:
        pct, v = find_aa_pct_for_target(
            dex=dex,
            mrk=mrk,
            lvl=lvl,
            aim=aim,
            max_aim=2,
            d=d,
            reach=2,
            omin=0,
            onear=1,
            target=target,
            close_pct=100,
        )
        print(f"  {label:18} need AA%>={pct} -> {v}% (target {target})")
    print()

    # --- Reflex path C: flat +AimAccuracy (on top of base), MinAim ---
    print("=== Reflex: flat +AimAccuracy (base 11 + N), AA%=100, MinAim ===")
    for add in range(0, 25):
        aa = w["base_aa"] + add
        v5, _ = eval_cth(
            dex=dex, mrk=mrk, lvl=lvl, aim=1, max_aim=2, aa=aa, d=5, reach=2, omin=0, onear=1
        )
        v10, _ = eval_cth(
            dex=dex, mrk=mrk, lvl=lvl, aim=1, max_aim=2, aa=aa, d=10, reach=2, omin=0, onear=1
        )
        vf, _ = eval_cth(
            dex=dex, mrk=mrk, lvl=lvl, aim=2, max_aim=2, aa=aa, d=5, reach=2, omin=0, onear=1
        )
        if v5 >= t_reflex_snap5 and vf >= t_reflex_p1_5:
            print(f"  first +{add} AA: snap5={v5} full5={vf} (targets {t_reflex_snap5}/{t_reflex_p1_5})")
            break
    else:
        print("  not reachable with +0..24 AA alone")
    print()

    # --- Combat: keep current near profile, tune reach and/or AA% ---
    # ACOG-like: MaxAim=3, AimLevel unlock at aim>=2 for reach, near 12@88
    print("=== Combat T3 full@20: tune reach (AA%=115, near 12@88, aim=3/3) ===")
    aa115 = w["base_aa"] * 1.15
    for target, tag in [(t_combat_20_lo, "x1.20"), (t_combat_20_hi, "x1.30")]:
        reach, v, E = find_reach_for_target(
            dex=dex,
            mrk=mrk,
            lvl=lvl,
            aim=3,
            max_aim=3,
            aa=aa115,
            d=20,
            omin=12,
            onear=0.88,
            target=target,
        )
        # mag equivalent if reach=(mag-1)*3 => mag = reach/3+1
        mag_eq = reach / 3 + 1 if reach is not None else None
        print(f"  {tag}: need reach>={reach} (mag~{mag_eq:.1f} if (mag-1)*3) -> {v}% E={E} (target {target})")
    print()

    print("=== Combat T3 full@20: tune AA% (reach fixed at current 9 = 4x) ===")
    for target, tag in [(t_combat_20_lo, "x1.20"), (t_combat_20_hi, "x1.30")]:
        pct, v = find_aa_pct_for_target(
            dex=dex,
            mrk=mrk,
            lvl=lvl,
            aim=3,
            max_aim=3,
            d=20,
            reach=9,
            omin=12,
            onear=0.88,
            target=target,
            lo=100,
            hi=300,
        )
        print(f"  {tag}: need AA%>={pct} -> {v}% (target {target})")
    print()

    # Combined modest: reach bump + AA%
    print("=== Combat hybrid proposals @20 full ===")
    for reach, pct in [(9, 115), (12, 115), (12, 125), (15, 115), (15, 120), (18, 115)]:
        aa = w["base_aa"] * pct / 100
        v20, info = eval_cth(
            dex=dex, mrk=mrk, lvl=lvl, aim=3, max_aim=3, aa=aa, d=20, reach=reach, omin=12, onear=0.88
        )
        v5, _ = eval_cth(
            dex=dex, mrk=mrk, lvl=lvl, aim=3, max_aim=3, aa=aa, d=5, reach=reach, omin=12, onear=0.88
        )
        v10, _ = eval_cth(
            dex=dex, mrk=mrk, lvl=lvl, aim=3, max_aim=3, aa=aa, d=10, reach=reach, omin=12, onear=0.88
        )
        rel = v20 / iron_full20
        print(
            f"  reach={reach:2d} AA%={pct}: 5={v5}% 10={v10}% 20={v20}% ({rel:.2f}x vs irons20) E={info['E']}"
        )
    print()

    # Reflex tier ladder proposal hitting ~1.20 at T4 with CloseRange cancel + AA%
    print("=== Proposed Reflex ladder (CloseRangeFactor->100, MinAim, MaxAim-1, reach=2) ===")
    # Find T4 pct for snap5 x1.2 with close=100
    t4_pct, t4_v = find_aa_pct_for_target(
        dex=dex, mrk=mrk, lvl=lvl, aim=1, max_aim=2, d=5, reach=2, omin=0, onear=1,
        target=t_reflex_snap5, close_pct=100,
    )
    # Spread T1..T4 linearly ending at t4_pct; T1 ~ halfway current feel
    # Also show without close cancel for comparison
    print(f"  T4 needs AA%~{t4_pct} with CloseRange cancel (snap5={t4_v})")
    for pct in [110, 120, 130, 140, 150, 160, t4_pct]:
        aa = w["base_aa"] * pct / 100
        rows = []
        for aim, d in [(1, 5), (1, 10), (2, 5), (2, 10), (2, 20)]:
            v, _ = eval_cth(
                dex=dex, mrk=mrk, lvl=lvl, aim=aim, max_aim=2, aa=aa, d=d,
                reach=2, omin=0, onear=1, close_pct=100,
            )
            rows.append(v)
        print(
            f"  AA%{pct}: snap5/10={rows[0]}/{rows[1]} full5/10/20={rows[2]}/{rows[3]}/{rows[4]}"
            f"  | vs iron snap5 {rows[0]/iron_snap5:.2f}x full20 {rows[4]/iron_full20:.2f}x"
        )
    print()

    # Without close cancel - what AA% for x1.2
    print("=== Reflex T4 AA% only (no CloseRange cancel) for snap5 x1.2 ===")
    pct, v = find_aa_pct_for_target(
        dex=dex, mrk=mrk, lvl=lvl, aim=1, max_aim=2, d=5, reach=2, omin=0, onear=1,
        target=t_reflex_snap5, lo=100, hi=400,
    )
    print(f"  need AA%>={pct} -> {v}%")
    print()

    # Long optic note: what reach for x1.25 at 20 with AA=11, aim=3, harsh near
    print("=== Long optic @20 full (AA=11, MaxAim=3, no AA%): reach for x1.25 ===")
    t_long = round(iron_full20 * 1.25)
    reach, v, E = find_reach_for_target(
        dex=dex, mrk=mrk, lvl=lvl, aim=3, max_aim=3, aa=w["base_aa"], d=20,
        omin=0, onear=1, target=t_long,
    )
    print(f"  target {t_long}: reach>={reach} -> {v}% E={E}")
    # with near penalty at 5 for mag 6/10 defaults
    for mag, omin_f, onear_f in [(4, 3.6, 0.82), (6, 5.4, 0.64), (10, 9.0, 0.35)]:
        # use integer min from formula mag*0.9
        omin = round(mag * 0.9)
        onear = max(0.35, 1 - (mag - 2) * 0.09)
        reach = (mag - 1) * 3
        v5, _ = eval_cth(dex=dex, mrk=mrk, lvl=lvl, aim=3, max_aim=3, aa=11, d=5, reach=reach, omin=omin, onear=onear)
        v20, info = eval_cth(dex=dex, mrk=mrk, lvl=lvl, aim=3, max_aim=3, aa=11, d=20, reach=reach, omin=omin, onear=onear)
        print(f"  {mag}x reach={reach} near={omin}@{onear:.0%}: 5={v5}% 20={v20}% ({v20/iron_full20:.2f}x) E={info['E']}")


if __name__ == "__main__":
    main()
