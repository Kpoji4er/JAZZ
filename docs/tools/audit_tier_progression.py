# -*- coding: utf-8 -*-
"""Audit weapon tier progression within families (accuracy/utility focused)."""
from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "docs/technical/weapons/data/weapons.csv"

# Intentional "worst of class" — do not flag as bugs
INTENTIONAL_WORST = {"Type56", "STG44", "FG42"}


def clamp(v, lo, hi):
    return min(hi, max(lo, v))


def round_h(v):
    return math.floor(v + 0.5) if v >= 0 else math.ceil(v - 0.5)


def skill(x):
    return 20 + max(0, x) ** 1.25 * 0.25


def mastery(m):
    m = clamp(m, 0, 100)
    v = (
        min(m, 60) * 20 / 60
        + clamp(m - 60, 0, 20)
        + clamp(m - 80, 0, 10) * 2
        + clamp(m - 90, 0, 6) * 20 / 6
        + clamp(m - 96, 0, 4) * 5
    )
    return min(100, round_h(v))


def cth(w, d, aim_full=True, dex=70, mrk=70, lvl=5):
    snap = skill((dex * 4 + mrk + lvl * 5) / 6)
    prec = skill((mrk * 4 + dex + lvl * 5) / 6)
    maxa = max(0, w["MaxAim"])
    aim = maxa if aim_full else 0
    prog = aim / maxa if maxa else 0
    core = clamp(snap + prog * max(prec - snap, 0) + aim * w["AA"] * mastery(mrk) / 100, 0, 100)
    R = w["R"]
    if not R or d >= R:
        return 0
    BDR = clamp(w["BDR"], 0, R)
    G = w["G"] or 50
    E = clamp(min(R - 0.01, BDR), 0, R - 0.01)
    power = max(0.25, BDR * 0.05 + G / 100)
    rf = 1.0 if d <= E else max(1 - ((d - E) / (R - E)) ** power, 0)
    return int(clamp(round_h(core * rf), 2, 100))


def tier_key(w):
    t, s = w["tier_maj"], w["tier_sub"]
    if t is None:
        return (99, 99, w["id"])
    sub = 90 if s == "UNIQ" else (int(s) if str(s).isdigit() else 50)
    return (t, sub, w["id"])


def load():
    weapons = []
    with CSV.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("catalog_status") != "active":
                continue
            label = row.get("tier_label") or ""
            maj = sub = None
            if label:
                parts = label.split("-", 1)
                if parts[0].isdigit():
                    maj = int(parts[0])
                    sub = parts[1] if len(parts) > 1 else "1"
            weapons.append(
                {
                    "id": row["id"],
                    "name": row["display_name"],
                    "family": row["family_id"],
                    "tier": label,
                    "tier_maj": maj,
                    "tier_sub": sub,
                    "caliber": row["caliber"],
                    "dmg": int(float(row["damage"] or 0)),
                    "AA": int(float(row["aim_accuracy"] or 0)),
                    "MaxAim": int(float(row["max_aim_actions"] or 0)),
                    "R": int(float(row["weapon_range"] or 0)),
                    "BDR": int(float(row["bullet_drop_range"] or 0)),
                    "G": int(float(row["grouping"] or 0)),
                    "ShootAP": int(float(row["shoot_ap"] or 0)),
                    "ReloadAP": int(float(row["reload_ap"] or 0)),
                    "Mag": int(float(row["magazine_size"] or 0)),
                    "Rel": int(float(row["reliability"] or 0)),
                    "Cost": int(float(row["cost"] or 0)),
                    "Recoil": int(float(row["recoil"] or 0)),
                    "auto": int(float(row["auto_shots"] or 0)),
                    "burst": int(float(row["burst_shots"] or 0)),
                }
            )
    for w in weapons:
        # Accuracy score: weighted CTH at class-relevant distances + AA/R package
        fam = w["family"]
        if fam in ("pistol", "autopistol", "revolver"):
            dists = [4, 8, 12]
        elif fam in ("submachine-gun", "shotgun"):
            dists = [8, 12, 16]
        elif fam in ("carbine",):
            dists = [12, 20, 30]
        elif fam in ("sniper-rifle", "battle-rifle", "machine-gun"):
            dists = [20, 30, 40]
        else:
            dists = [12, 20, 30]
        cths = [cth(w, d, True) for d in dists]
        w["cth_avg"] = sum(cths) / len(cths)
        w["cth_mid"] = cths[1] if len(cths) > 1 else cths[0]
        # Utility: lower ShootAP better; ignore Recoil=100 as N/A
        recoil = w["Recoil"] if w["Recoil"] < 100 else None
        w["acc_score"] = (
            w["cth_avg"] * 1.0
            + w["AA"] * 0.8
            + w["R"] * 0.15
            + w["BDR"] * 0.4
            + w["MaxAim"] * 2
            + (0 if recoil is None else max(0, 20 - recoil) * 0.3)
        )
        # AP efficiency: cheaper shots better for "fast" guns
        w["ap_score"] = max(0, 8000 - w["ShootAP"]) / 100
        w["overall"] = w["acc_score"] + w["ap_score"] * 0.15 + w["Rel"] * 0.05 + min(w["Mag"], 40) * 0.1
    return weapons


def main():
    weapons = [w for w in load() if w["tier_maj"] is not None]
    by_f = defaultdict(list)
    for w in weapons:
        by_f[w["family"]].append(w)

    print("=== TIER BAND MEDIANS (overall / cth_avg / AA / R / BDR / ShootAP) ===")
    for fam in sorted(by_f):
        print(f"\n## {fam}")
        bands = defaultdict(list)
        for w in by_f[fam]:
            bands[w["tier_maj"]].append(w)
        for maj in sorted(bands):
            ws = bands[maj]

            def med(k):
                xs = sorted(x[k] for x in ws)
                return xs[len(xs) // 2]

            print(
                f"  T{maj} n={len(ws):2}  overall={med('overall'):5.1f}  cth={med('cth_avg'):5.1f}  "
                f"AA={med('AA'):2} R={med('R'):2} BDR={med('BDR'):2} AP={med('ShootAP'):4} Rel={med('Rel'):2}"
            )

    print("\n=== INVERSIONS: higher major-tier worse overall than lower (same family) ===")
    print("(skip intentional worst; compare each weapon to best of lower major tiers)\n")
    issues = []
    for fam in sorted(by_f):
        ws = [w for w in by_f[fam] if w["id"] not in INTENTIONAL_WORST]
        for hi in ws:
            lowers = [w for w in ws if w["tier_maj"] < hi["tier_maj"]]
            if not lowers:
                continue
            best_low = max(lowers, key=lambda w: w["overall"])
            # meaningful gap: hi clearly worse
            if hi["overall"] + 4 < best_low["overall"] and hi["cth_avg"] + 3 < best_low["cth_avg"]:
                issues.append((fam, hi, best_low))
                print(
                    f"{fam:22} {hi['id']:18} T{hi['tier']:5} overall={hi['overall']:5.1f} cth={hi['cth_avg']:4.1f} AA={hi['AA']:2} R={hi['R']:2} BDR={hi['BDR']:2} AP={hi['ShootAP']}"
                    f"\n{'':22}   worse than {best_low['id']:18} T{best_low['tier']:5} overall={best_low['overall']:5.1f} cth={best_low['cth_avg']:4.1f} AA={best_low['AA']:2} R={best_low['R']:2} BDR={best_low['BDR']:2}"
                )

    print("\n=== WITHIN SAME MAJOR TIER: late subtier worse than early (gap) ===")
    for fam in sorted(by_f):
        ws = [w for w in by_f[fam] if w["id"] not in INTENTIONAL_WORST and w["tier_sub"] != "UNIQ"]
        by_maj = defaultdict(list)
        for w in ws:
            by_maj[w["tier_maj"]].append(w)
        for maj, group in sorted(by_maj.items()):
            if len(group) < 3:
                continue
            group = sorted(group, key=tier_key)
            for i, late in enumerate(group):
                earlier = group[:i]
                if not earlier:
                    continue
                best_e = max(earlier, key=lambda w: w["overall"])
                # late subtier should not be clearly worse than earlier in same major
                try:
                    late_sub = int(late["tier_sub"])
                    early_sub = int(best_e["tier_sub"])
                except ValueError:
                    continue
                if late_sub <= early_sub:
                    continue
                if late["overall"] + 6 < best_e["overall"] and late["cth_avg"] + 4 < best_e["cth_avg"]:
                    print(
                        f"{fam:22} {late['id']:18} T{late['tier']} overall={late['overall']:5.1f} cth={late['cth_avg']:4.1f}"
                        f"  <  {best_e['id']} T{best_e['tier']} overall={best_e['overall']:5.1f} cth={best_e['cth_avg']:4.1f}"
                    )

    print("\n=== PER-FAMILY: weakest T2/T3 that lose to strong T1 on accuracy package ===")
    for fam in sorted(by_f):
        t1 = [w for w in by_f[fam] if w["tier_maj"] == 1 and w["id"] not in INTENTIONAL_WORST]
        later = [w for w in by_f[fam] if w["tier_maj"] >= 2 and w["id"] not in INTENTIONAL_WORST]
        if not t1 or not later:
            continue
        best_t1 = max(t1, key=lambda w: w["cth_avg"])
        for w in later:
            if w["cth_avg"] + 5 < best_t1["cth_avg"] and w["AA"] <= best_t1["AA"] and w["R"] <= best_t1["R"] + 2:
                print(
                    f"{fam:22} {w['id']:18} T{w['tier']} cth={w['cth_avg']:4.1f} AA={w['AA']} R={w['R']} BDR={w['BDR']}"
                    f"  << T1 {best_t1['id']} cth={best_t1['cth_avg']:4.1f} AA={best_t1['AA']} R={best_t1['R']}"
                )


if __name__ == "__main__":
    main()
