#!/usr/bin/env python3
import collections
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
w = json.loads((ROOT / ".tmp/weapon_analysis.json").read_text(encoding="utf-8"))[
    "weapons"
]
rows = list(
    csv.DictReader(
        (ROOT / "docs/technical/weapons/data/weapons.csv").open(encoding="utf-8")
    )
)

pc = collections.Counter(
    (r["penetration_class"], r["penetration_bonus"])
    for r in rows
    if r["catalog_status"] == "active"
)
print("raw pen pairs top:", pc.most_common(20))
print("unique pen pairs:", len(pc))

by_id = {x["id"]: x for x in w}


def dump(ids):
    for id_ in ids:
        x = by_id.get(id_)
        if not x:
            print(" missing", id_)
            continue
        print(
            f"{x['id']:20} {x['family']:16} T{x['tier']:7} "
            f"dmg={x['damage']:2} ap={x['ap']:.0f} recoil={x['recoil']:2} "
            f"rng={x['range']:3} mag={x['mag']:3} b/a={x['burst']}/{x['auto']} "
            f"crit={x['crit']:2} aim={x['aim']:2} score={x['score']:+.2f} "
            f"resid={x['resid']:+.2f} cal={x['caliber']} "
            f"specials={x['specials']}"
        )


print("\n=== AR peers ===")
dump(
    [
        "FAMAS",
        "AK74",
        "AN94",
        "M16A4",
        "Type56",
        "AUG",
        "G36",
        "HK33",
        "AR15",
        "M4Commando",
        "Sig550",
        "Sig550Custom",
        "AR10DMR",
    ]
)

print("\n=== SMG ===")
dump(
    [
        "UMP45",
        "MP5SD",
        "P90",
        "MP7",
        "Agram2000",
        "MAT49",
        "LionRoar",
        "BerettaM12",
        "MP5A4",
        "Vector",
        "UZI",
    ]
)

print("\n=== Sniper ===")
dump(
    [
        "SVU",
        "BarretM82",
        "ArcticWarfare",
        "PSG1",
        "M24Sniper",
        "DragunovSVD",
        "DragunovSVD_Custom",
        "ScoutSniper",
    ]
)

print("\n=== Uniques / hybrids ===")
dump(
    [
        "AR10DMR",
        "AN94",
        "Winchester_Quest",
        "Auto5_quest",
        "Welrod",
        "Galil_FlagHill",
        "BrowningM2HMG",
        "LionRoar",
        "AS_Val",
        "AA12",
        "Korth",
        "FiveSeven",
        "P226",
        "MAC10",
        "Glock18",
        "HK21",
        "M60E4",
    ]
)

print("\n=== Best non-empty assigned tier per family ===")
by = collections.defaultdict(list)
for x in w:
    if x["tier"] and "UNIQ" not in x["tier"] and x["tier_n"] > 0:
        by[x["family"]].append(x)
for fam, xs in sorted(by.items()):
    b = sorted(xs, key=lambda z: -z["score"])[0]
    print(
        f"{fam:18} {b['id']:20} T{b['tier']} score={b['score']:+.2f} "
        f"dmg={b['damage']} ap={b['ap']:.0f} recoil={b['recoil']} rng={b['range']}"
    )

print("\n=== Family size / score spread ===")
for fam, xs in sorted(collections.defaultdict(list, **{x["family"]: [] for x in w}).items()):
    pass
fam_groups = collections.defaultdict(list)
for x in w:
    fam_groups[x["family"]].append(x)
for fam, xs in sorted(fam_groups.items()):
    scores = [x["score"] for x in xs]
    print(
        f"{fam:18} n={len(xs):2} score_min={min(scores):+.2f} "
        f"max={max(scores):+.2f} spread={max(scores)-min(scores):.2f}"
    )

# Damage efficiency vs tier within AR
print("\n=== AR damage/AP and AutoShots ===")
ars = sorted(
    [x for x in w if x["family"] == "assault-rifle"],
    key=lambda x: (-x["damage"] / max(x["ap"], 0.1), -x["auto"]),
)
for x in ars:
    print(
        f"{x['id']:16} T{x['tier']:7} dmg/ap={x['damage']/x['ap']:.2f} "
        f"auto_dps={x['adps']:.1f} auto={x['auto']} burst={x['burst']} "
        f"recoil={x['recoil']} dmg={x['damage']}"
    )
