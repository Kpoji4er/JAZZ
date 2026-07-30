# -*- coding: utf-8 -*-
"""Offline CTH matrix: weapons x shooter profiles x distances (iron sights)."""
from __future__ import annotations

import csv
import json
import math
import os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(ROOT, "docs", "technical", "weapons", "data", "weapons.csv")
OUT_DIR = os.path.join(ROOT, "docs", "tools")


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


def cth(w, dex, mrk, lvl, aim_clicks, d, optic_reach=0.0, optic_min=0.0, optic_near=1.0):
    snap_raw = (dex * 4 + mrk + lvl * 5) / 6
    prec_raw = (mrk * 4 + dex + lvl * 5) / 6
    snap = skill_curve(snap_raw)
    prec = skill_curve(prec_raw)
    max_aim = max(0, w["MaxAimActions"])
    aim = min(aim_clicks, max_aim)
    prog = clamp(aim / max_aim, 0, 1) if max_aim else 0.0
    shot_skill = snap + prog * max(prec - snap, 0)
    gain = max(0, aim) * w["AimAccuracy"] * aim_mastery(mrk) / 100
    skill_core = clamp(shot_skill + gain, 0, 100)
    R = w["WeaponRange"]
    if not R or d >= R:
        return 0
    BDR = clamp(w["BulletDropRange"] or R / 2, 0, R)
    G = w["Grouping"] or 50
    eps = 0.01
    E = clamp(min(R - eps, BDR + optic_reach * prog), 0, R - eps)
    power = max(0.25, BDR * 0.05 + G / 100)
    if d <= E:
        rf = 1.0
    else:
        t = clamp((d - E) / (R - E), 0, 1)
        rf = max(1 - (t**power), 0)
    core = skill_core * rf
    near = 1.0
    if optic_min > 0 and d < optic_min:
        prox = clamp((optic_min - d) / optic_min, 0, 1)
        near = 1 + (optic_near - 1) * prox
    return int(clamp(round_h(core * near), 2, 100))


def load_weapons():
    weapons = []
    with open(CSV_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("catalog_status") != "active":
                continue
            weapons.append(
                {
                    "id": row["id"],
                    "name": row["display_name"],
                    "family": row["family_id"],
                    "tier": row["tier_label"] or "",
                    "caliber": row["caliber"],
                    "dmg": int(float(row["damage"] or 0)),
                    "AimAccuracy": int(float(row["aim_accuracy"] or 0)),
                    "MaxAimActions": int(float(row["max_aim_actions"] or 0)),
                    "WeaponRange": int(float(row["weapon_range"] or 0)),
                    "BulletDropRange": int(float(row["bullet_drop_range"] or 0)),
                    "Grouping": int(float(row["grouping"] or 0)),
                    "burst": int(float(row["burst_shots"] or 0)),
                    "auto": int(float(row["auto_shots"] or 0)),
                    "Recoil": int(float(row["recoil"] or 0)),
                }
            )
    return weapons


PROFILES = [
    ("G40s", 40, 40, 1, 0),
    ("G40f", 40, 40, 1, 99),
    ("A70s", 70, 70, 5, 0),
    ("A70f", 70, 70, 5, 99),
    ("E90s", 90, 100, 10, 0),
    ("E90f", 90, 100, 10, 99),
]

DISTS = [4, 8, 12, 16, 20, 24, 30, 40, 50]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    weapons = load_weapons()
    by_f = defaultdict(list)
    for w in weapons:
        by_f[w["family"]].append(w)

    lines = []
    lines.append("=== FAMILY CTH STAT MEDIANS (iron) ===")
    for fam in sorted(by_f):
        ws = by_f[fam]

        def med(k):
            xs = sorted(x[k] for x in ws)
            return xs[len(xs) // 2]

        lines.append(
            f"{fam:22} n={len(ws):2} AA={med('AimAccuracy'):2} MaxAim={med('MaxAimActions')} "
            f"R={med('WeaponRange'):2} BDR={med('BulletDropRange'):2} G={med('Grouping'):3}"
        )

    # Full matrix JSON for HTML/canvas
    matrix = []
    for w in weapons:
        entry = {
            "id": w["id"],
            "name": w["name"],
            "family": w["family"],
            "tier": w["tier"],
            "AA": w["AimAccuracy"],
            "MaxAim": w["MaxAimActions"],
            "R": w["WeaponRange"],
            "BDR": w["BulletDropRange"],
            "G": w["Grouping"],
            "dmg": w["dmg"],
            "caliber": w["caliber"],
            "burst": w["burst"],
            "auto": w["auto"],
            "Recoil": w["Recoil"],
            "cth": {},
        }
        for plabel, dex, mrk, lvl, aim in PROFILES:
            entry["cth"][plabel] = {str(d): cth(w, dex, mrk, lvl, aim, d) for d in DISTS}
        matrix.append(entry)

    # Family averages A70f
    lines.append("")
    lines.append("=== FAMILY AVG CTH  A70 full aim ===")
    lines.append("family                 " + " ".join(f"d{d:02d}" for d in DISTS))
    fam_avg = {}
    for fam in sorted(by_f):
        avgs = []
        for d in DISTS:
            xs = [cth(w, 70, 70, 5, 99, d) for w in by_f[fam]]
            avgs.append(sum(xs) / len(xs))
        fam_avg[fam] = avgs
        lines.append(f"{fam:22} " + " ".join(f"{a:5.1f}" for a in avgs))

    # Aim gain @12
    lines.append("")
    lines.append("=== AIM VALUE (full - snap) @ d12 A70 ===")
    for fam in sorted(by_f):
        deltas = []
        for w in by_f[fam]:
            deltas.append(cth(w, 70, 70, 5, 99, 12) - cth(w, 70, 70, 5, 0, 12))
        deltas.sort()
        lines.append(
            f"{fam:22} median={deltas[len(deltas)//2]:3}  min={deltas[0]:3} max={deltas[-1]:3}"
        )

    # Within-family outliers on A70f @12 and @20
    lines.append("")
    lines.append("=== WITHIN-FAMILY OUTLIERS |z|>=1.8  A70f @12/@20 ===")
    outliers = []
    for fam in sorted(by_f):
        ws = by_f[fam]
        if len(ws) < 4:
            continue
        for d, tag in ((12, "@12"), (20, "@20")):
            xs = [cth(w, 70, 70, 5, 99, d) for w in ws]
            mean = sum(xs) / len(xs)
            sd = math.sqrt(sum((x - mean) ** 2 for x in xs) / len(xs)) or 1.0
            for w, x in zip(ws, xs):
                z = (x - mean) / sd
                if abs(z) >= 1.8:
                    row = {
                        "family": fam,
                        "id": w["id"],
                        "tier": w["tier"],
                        "dist": d,
                        "cth": x,
                        "z": round(z, 2),
                        "AA": w["AimAccuracy"],
                        "R": w["WeaponRange"],
                        "BDR": w["BulletDropRange"],
                        "G": w["Grouping"],
                        "MaxAim": w["MaxAimActions"],
                    }
                    outliers.append(row)
                    lines.append(
                        f"  {fam} {w['id']:20} tier={w['tier']:5} CTH{tag}={x:3} z={z:+.2f} "
                        f"AA={w['AimAccuracy']} R={w['WeaponRange']} BDR={w['BulletDropRange']} "
                        f"G={w['Grouping']} MaxAim={w['MaxAimActions']}"
                    )

    # Cross-class at same distance: who is accurate at 20 with A70f
    lines.append("")
    lines.append("=== TOP/BOTTOM 15  A70f @20 (all families) ===")
    scored = [(cth(w, 70, 70, 5, 99, 20), w) for w in weapons]
    scored.sort(key=lambda t: (-t[0], t[1]["id"]))
    lines.append("TOP:")
    for c, w in scored[:15]:
        lines.append(
            f"  {c:3}%  {w['id']:20} {w['family']:22} tier={w['tier']:5} "
            f"AA={w['AimAccuracy']:2} R={w['WeaponRange']:2} BDR={w['BulletDropRange']:2} G={w['Grouping']:3}"
        )
    lines.append("BOTTOM (possible only, CTH>0):")
    bottom = [t for t in scored if t[0] > 0][-15:]
    for c, w in bottom:
        lines.append(
            f"  {c:3}%  {w['id']:20} {w['family']:22} tier={w['tier']:5} "
            f"AA={w['AimAccuracy']:2} R={w['WeaponRange']:2} BDR={w['BulletDropRange']:2} G={w['Grouping']:3}"
        )

    # Impossible at 20 (R<=20)
    dead = [w for w in weapons if w["WeaponRange"] <= 20]
    lines.append("")
    lines.append(f"=== R <= 20 (cannot shoot d=20): {len(dead)} ===")
    for w in sorted(dead, key=lambda x: (x["WeaponRange"], x["id"])):
        lines.append(f"  R={w['WeaponRange']:2}  {w['id']:20} {w['family']} tier={w['tier']}")

    # Special cases
    lines.append("")
    lines.append("=== SPECIAL IDS (user notes) ===")
    for wid in [
        "FAMAS",
        "CAR15",
        "UMP45",
        "AR10DMR",
        "RSH12",
        "AK47",
        "M16A2",
        "Glock17",
        "DragunovSVD",
        "Winchester1894",
        "HiPower",
        "FiveSeven",
        "AS_Val",
        "VSS",
        "M24Sniper",
        "BarretM82",
    ]:
        w = next((x for x in weapons if x["id"] == wid), None)
        if not w:
            lines.append(f"{wid} NOT FOUND")
            continue
        lines.append(
            f"{wid:16} tier={w['tier']:5} AA={w['AimAccuracy']:2} MaxAim={w['MaxAimActions']} "
            f"R={w['WeaponRange']:2} BDR={w['BulletDropRange']:2} G={w['Grouping']:3} "
            f"burst={w['burst']} auto={w['auto']} Recoil={w['Recoil']} dmg={w['dmg']}"
        )
        for d in [8, 12, 20, 30, 40]:
            lines.append(
                f"  d={d:2}  G40f={cth(w,40,40,1,99,d):3}  A70s={cth(w,70,70,5,0,d):3}  "
                f"A70f={cth(w,70,70,5,99,d):3}  E90f={cth(w,90,100,10,99,d):3}"
            )

    # Snap vs aimed usefulness for low-AA vs high-AA
    lines.append("")
    lines.append("=== LOW AIMACCURACY (<=6) vs HIGH (>=14)  A70 @12 ===")
    low = [w for w in weapons if w["AimAccuracy"] <= 6]
    high = [w for w in weapons if w["AimAccuracy"] >= 14]
    for label, group in (("LOW AA", low), ("HIGH AA", high)):
        if not group:
            continue
        snaps = [cth(w, 70, 70, 5, 0, 12) for w in group]
        fulls = [cth(w, 70, 70, 5, 99, 12) for w in group]
        lines.append(
            f"{label:8} n={len(group):3}  snap_avg={sum(snaps)/len(snaps):5.1f}  "
            f"full_avg={sum(fulls)/len(fulls):5.1f}  aim_delta={sum(f-s for f,s in zip(fulls,snaps))/len(group):5.1f}"
        )

    report_path = os.path.join(OUT_DIR, "cth-sim-report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    json_path = os.path.join(OUT_DIR, "cth-sim-matrix.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "profiles": [
                    {"id": p[0], "dex": p[1], "mrk": p[2], "lvl": p[3], "aim": p[4]}
                    for p in PROFILES
                ],
                "distances": DISTS,
                "weapons": matrix,
                "family_avg_A70f": fam_avg,
                "outliers_A70f": outliers,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print("\n".join(lines))
    print()
    print("Wrote", report_path)
    print("Wrote", json_path)


if __name__ == "__main__":
    main()
