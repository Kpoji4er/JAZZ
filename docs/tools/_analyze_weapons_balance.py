#!/usr/bin/env python3
"""One-shot balance audit over docs/technical/weapons/data/weapons.csv.

Scores weapons within family (z-score composite), finds tier residuals,
rare/unique AvailableAttacks, and writes .tmp/weapon_analysis.json.
"""
from __future__ import annotations

import collections
import csv
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "docs/technical/weapons/data/weapons.csv"
OUT_PATH = ROOT / ".tmp/weapon_analysis.json"


def n(r: dict, k: str, default: float = 0.0) -> float:
    v = r.get(k, "")
    if v is None or v == "":
        return default
    try:
        return float(v)
    except ValueError:
        return default


def shoot_ap(r: dict) -> float:
    return n(r, "shoot_ap") / 1000.0


def dps_single(r: dict) -> float:
    ap = shoot_ap(r)
    return n(r, "damage") / ap if ap > 0 else 0.0


def burst_dps(r: dict) -> float:
    shots = n(r, "burst_shots")
    if shots <= 0:
        return 0.0
    return n(r, "damage") * shots / (shoot_ap(r) + 1.0)


def auto_dps(r: dict) -> float:
    shots = n(r, "auto_shots")
    if shots <= 0:
        return 0.0
    return n(r, "damage") * shots / (shoot_ap(r) + 2.0)


def pen_total(r: dict) -> float:
    return n(r, "penetration_class") + n(r, "penetration_bonus") / 10.0


def attacks(r: dict) -> list[str]:
    return [a for a in (r.get("available_attacks") or "").split(";") if a]


SPECIAL_BASE = {
    "AbakanBurst",
    "AbakanAutoFire",
    "DoubleBarrel",
    "BuckshotBurst",
    "RunAndGun",
    "RunAndGun_Carbine",
    "MGSetup",
    "MobileShot",
}


def specials(atts: list[str]) -> list[str]:
    return [a for a in atts if a.startswith("JAZZ_") or a in SPECIAL_BASE]


def zscore(vals: list[float], v: float) -> float:
    if len(vals) < 2:
        return 0.0
    m = statistics.mean(vals)
    s = statistics.pstdev(vals)
    if s < 1e-9:
        return 0.0
    return (v - m) / s


WEIGHTS = {
    "damage": 1.4,
    "pen": 1.2,
    "weapon_range": 0.9,
    "aim_accuracy": 0.8,
    "crit_chance_scaled": 0.5,
    "magazine_size": 0.6,
    "reliability": 0.4,
    "max_aim_actions": 0.5,
    "component_option_count": 0.3,
    "dps": 1.0,
    "bdps": 0.7,
    "adps": 0.5,
    "special_count": 0.6,
    "recoil": -1.0,
    "shoot_ap": -0.9,
    "noise": -0.2,
    "base_jam_chance": -0.3,
    "weapon_mass": -0.3,
}


def score_family(fam_rows: list[dict]) -> list[dict]:
    keys = {
        "damage": lambda r: n(r, "damage"),
        "pen": lambda r: r["_pen"],
        "weapon_range": lambda r: n(r, "weapon_range"),
        "aim_accuracy": lambda r: n(r, "aim_accuracy"),
        "crit_chance_scaled": lambda r: n(r, "crit_chance_scaled"),
        "magazine_size": lambda r: n(r, "magazine_size"),
        "reliability": lambda r: n(r, "reliability"),
        "max_aim_actions": lambda r: n(r, "max_aim_actions"),
        "component_option_count": lambda r: n(r, "component_option_count"),
        "dps": lambda r: r["_dps"],
        "bdps": lambda r: r["_bdps"],
        "adps": lambda r: r["_adps"],
        "special_count": lambda r: r["_special_count"],
        "recoil": lambda r: n(r, "recoil"),
        "shoot_ap": lambda r: r["_shoot_ap_u"],
        "noise": lambda r: n(r, "noise"),
        "base_jam_chance": lambda r: n(r, "base_jam_chance"),
        "weapon_mass": lambda r: n(r, "weapon_mass"),
    }
    series = {k: [fn(r) for r in fam_rows] for k, fn in keys.items()}
    for r in fam_rows:
        s = 0.0
        parts = {}
        for k, fn in keys.items():
            contrib = WEIGHTS[k] * zscore(series[k], fn(r))
            parts[k] = round(contrib, 3)
            s += contrib
        r["_score"] = s
        r["_parts"] = parts
    return fam_rows


def fit_linear(xs: list[float], ys: list[float]) -> tuple[float, float]:
    mx, my = statistics.mean(xs), statistics.mean(ys)
    var = sum((x - mx) ** 2 for x in xs)
    if var < 1e-9:
        return 0.0, my
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = cov / var
    return slope, my - slope * mx


def main() -> None:
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    active = [r for r in rows if r.get("catalog_status", "") == "active"]
    print(f"total={len(rows)} active={len(active)}")
    print("families:", sorted({r["family_id"] for r in active}))

    att_count: collections.Counter[str] = collections.Counter()
    for r in active:
        for a in attacks(r):
            att_count[a] += 1

    for r in active:
        r["_shoot_ap_u"] = shoot_ap(r)
        r["_pen"] = pen_total(r)
        r["_dps"] = dps_single(r)
        r["_bdps"] = burst_dps(r)
        r["_adps"] = auto_dps(r)
        r["_attacks"] = attacks(r)
        r["_specials"] = specials(r["_attacks"])
        r["_special_count"] = len(r["_specials"])

    print("\nRare attacks (<=5 weapons):")
    rare_attacks = {a: c for a, c in att_count.items() if c <= 5}
    for a, c in sorted(rare_attacks.items(), key=lambda x: (-x[1], x[0])):
        owners = [r["id"] for r in active if a in r["_attacks"]]
        print(f"  {a}: {c} -> {owners}")

    print("\nAttack frequency:")
    for a, c in att_count.most_common():
        print(f"  {a}: {c}")

    print("\nWeapons with ultra-rare attacks (<=3 owners):")
    for r in sorted(active, key=lambda x: (x["family_id"], x["tier_label"], x["id"])):
        rare = [a for a in r["_attacks"] if att_count[a] <= 3]
        if rare:
            print(
                f"  {r['id']} [{r['family_id']} {r['tier_label']}]: {rare}"
            )

    families = sorted({r["family_id"] for r in active})
    by_fam: dict[str, list[dict]] = {}
    all_scored: list[dict] = []
    for fam in families:
        fr = [r for r in active if r["family_id"] == fam]
        scored = score_family(fr)
        by_fam[fam] = sorted(scored, key=lambda r: -r["_score"])
        all_scored.extend(scored)

    for fam, fr in by_fam.items():
        if len(fr) < 3:
            for r in fr:
                r["_resid_lin"] = 0.0
                r["_exp_lin"] = r["_score"]
            continue
        xs = [n(r, "balance_tier") for r in fr]
        ys = [r["_score"] for r in fr]
        slope, intercept = fit_linear(xs, ys)
        for r in fr:
            exp = intercept + slope * n(r, "balance_tier")
            r["_exp_lin"] = exp
            r["_resid_lin"] = r["_score"] - exp

    global_rank = sorted(all_scored, key=lambda r: -r["_score"])
    print("\n=== TOP 15 within-family composite ===")
    for r in global_rank[:15]:
        print(
            f"{r['_score']:+.2f}  {r['id']:22s} {r['family_id']:18s} "
            f"T{r['tier_label']:4s} dmg={r['damage']} pen={r['_pen']:.1f} "
            f"rng={r['weapon_range']} ap={r['_shoot_ap_u']:.0f} "
            f"recoil={r['recoil']} mag={r['magazine_size']} "
            f"specials={r['_specials']}"
        )

    print("\n=== BOTTOM 10 ===")
    for r in global_rank[-10:]:
        print(
            f"{r['_score']:+.2f}  {r['id']:22s} {r['family_id']:18s} "
            f"T{r['tier_label']:4s} dmg={r['damage']} pen={r['_pen']:.1f} "
            f"rng={r['weapon_range']} ap={r['_shoot_ap_u']:.0f} "
            f"recoil={r['recoil']}"
        )

    resid_sorted = sorted(all_scored, key=lambda r: -r.get("_resid_lin", 0.0))
    print("\n=== Overperformers vs tier trend ===")
    for r in resid_sorted[:12]:
        print(
            f"  resid={r['_resid_lin']:+.2f} score={r['_score']:+.2f} "
            f"exp={r['_exp_lin']:+.2f}  {r['id']:22s} {r['family_id']:16s} "
            f"T{r['tier_label']} dmg={r['damage']} pen={r['_pen']:.1f} "
            f"ap={r['_shoot_ap_u']:.0f} recoil={r['recoil']} "
            f"att={';'.join(r['_specials'][:5])}"
        )

    print("\n=== Underperformers vs tier trend ===")
    for r in resid_sorted[-12:]:
        print(
            f"  resid={r['_resid_lin']:+.2f} score={r['_score']:+.2f} "
            f"exp={r['_exp_lin']:+.2f}  {r['id']:22s} {r['family_id']:16s} "
            f"T{r['tier_label']} dmg={r['damage']} pen={r['_pen']:.1f} "
            f"ap={r['_shoot_ap_u']:.0f} recoil={r['recoil']} "
            f"att={';'.join(r['_specials'][:5])}"
        )

    print("\n=== BEST PER FAMILY ===")
    for fam in families:
        fr = by_fam[fam]
        if not fr:
            continue
        b = fr[0]
        print(
            f"{fam:18s}: {b['id']:22s} T{b['tier_label']} "
            f"score={b['_score']:+.2f} dmg={b['damage']} pen={b['_pen']:.1f} "
            f"rng={b['weapon_range']} recoil={b['recoil']} "
            f"ap={b['_shoot_ap_u']:.0f} mag={b['magazine_size']} "
            f"specials={b['_specials']}"
        )

    print("\n=== ABSOLUTE PEAKS ===")

    def show(label: str, key_fn, fmt_fn):
        top = sorted(active, key=key_fn, reverse=True)[:5]
        print(label + ":", ", ".join(fmt_fn(r) for r in top))

    show("damage", lambda r: n(r, "damage"), lambda r: f"{r['id']}({r['damage']})")
    show("pen", lambda r: r["_pen"], lambda r: f"{r['id']}({r['_pen']:.1f})")
    show(
        "range",
        lambda r: n(r, "weapon_range"),
        lambda r: f"{r['id']}({r['weapon_range']})",
    )
    show("dps_single", lambda r: r["_dps"], lambda r: f"{r['id']}({r['_dps']:.2f})")
    show("burst_dps", lambda r: r["_bdps"], lambda r: f"{r['id']}({r['_bdps']:.2f})")
    show("auto_dps", lambda r: r["_adps"], lambda r: f"{r['id']}({r['_adps']:.2f})")
    show(
        "crit",
        lambda r: n(r, "crit_chance_scaled"),
        lambda r: f"{r['id']}({r['crit_chance_scaled']})",
    )
    show(
        "mag",
        lambda r: n(r, "magazine_size"),
        lambda r: f"{r['id']}({r['magazine_size']})",
    )
    show(
        "aim_acc",
        lambda r: n(r, "aim_accuracy"),
        lambda r: f"{r['id']}({r['aim_accuracy']})",
    )
    show(
        "lowest_recoil",
        lambda r: -n(r, "recoil"),
        lambda r: f"{r['id']}({r['recoil']})",
    )
    show(
        "lowest_ap",
        lambda r: -r["_shoot_ap_u"],
        lambda r: f"{r['id']}({r['_shoot_ap_u']:.0f})",
    )

    print("\n=== ATTACK SET OUTLIERS ===")
    for fam, fr in by_fam.items():
        counts = collections.Counter(a for r in fr for a in r["_attacks"])
        common = {a for a, c in counts.items() if c >= max(1, len(fr) * 0.5)}
        for r in fr:
            s = set(r["_attacks"])
            r["_att_extra"] = sorted(s - common)
            r["_att_missing"] = sorted(common - s)
            union = s | common
            r["_att_j"] = (len(s & common) / len(union)) if union else 1.0
        odd = sorted(fr, key=lambda r: r["_att_j"])
        for r in odd[:4]:
            if r["_att_j"] >= 0.9 and not r["_att_extra"]:
                continue
            print(
                f"  {r['id']:22s} {fam:16s} j={r['_att_j']:.2f} "
                f"+{r['_att_extra']} -{r['_att_missing']}"
            )

    # Per-tier champions within family (tier 3-4 especially)
    print("\n=== TIER 4 / HIGH-END SNAPSHOT ===")
    for fam in families:
        hi = [r for r in by_fam[fam] if n(r, "balance_tier") >= 3]
        if not hi:
            continue
        print(f"-- {fam} --")
        for r in sorted(hi, key=lambda x: -x["_score"])[:4]:
            print(
                f"  {r['_score']:+.2f} {r['id']:22s} T{r['tier_label']} "
                f"dmg={r['damage']} pen={r['_pen']:.1f} rng={r['weapon_range']} "
                f"recoil={r['recoil']} ap={r['_shoot_ap_u']:.0f} "
                f"burst/auto={r['burst_shots']}/{r['auto_shots']} "
                f"specials={r['_specials']}"
            )

    export = []
    for r in all_scored:
        export.append(
            {
                "id": r["id"],
                "name": r["display_name"],
                "family": r["family_id"],
                "family_ru": r["family_name_ru"],
                "tier": r["tier_label"],
                "tier_n": int(n(r, "balance_tier") or 0),
                "sub": int(n(r, "balance_subtier") or 0),
                "damage": int(n(r, "damage")),
                "pen": round(r["_pen"], 2),
                "range": int(n(r, "weapon_range")),
                "ap": r["_shoot_ap_u"],
                "recoil": int(n(r, "recoil")),
                "mag": int(n(r, "magazine_size")),
                "crit": int(n(r, "crit_chance_scaled")),
                "aim": int(n(r, "aim_accuracy")),
                "max_aim": int(n(r, "max_aim_actions")),
                "reliability": int(n(r, "reliability")),
                "noise": int(n(r, "noise")),
                "mass": n(r, "weapon_mass"),
                "burst": int(n(r, "burst_shots")),
                "auto": int(n(r, "auto_shots")),
                "dps": round(r["_dps"], 2),
                "bdps": round(r["_bdps"], 2),
                "adps": round(r["_adps"], 2),
                "score": round(r["_score"], 3),
                "resid": round(r.get("_resid_lin", 0.0), 3),
                "specials": r["_specials"],
                "attacks": r["_attacks"],
                "att_extra": r.get("_att_extra", []),
                "att_missing": r.get("_att_missing", []),
                "cost": int(n(r, "cost")),
                "caliber": r["caliber"].replace("JAZZ_Caliber_", ""),
                "size": r.get("weapon_size_class", ""),
                "cumbersome": r.get("cumbersome", "0"),
                "hand": r.get("hand_slot", ""),
            }
        )

    OUT_PATH.parent.mkdir(exist_ok=True)
    payload = {
        "count": len(export),
        "attack_freq": dict(att_count),
        "weapons": export,
        "best_per_family": {
            fam: by_fam[fam][0]["id"] for fam in families if by_fam[fam]
        },
        "overperformers": [r["id"] for r in resid_sorted[:12]],
        "underperformers": [r["id"] for r in resid_sorted[-12:][::-1]],
    }
    OUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nWrote {OUT_PATH} ({len(export)} weapons)")


if __name__ == "__main__":
    main()
