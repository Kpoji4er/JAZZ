#!/usr/bin/env python3
"""Static acceptance audit for JAZZ-WEAPONS-003 physical recoil data."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "docs/technical/weapons/data/weapons.csv"


def number(row: dict[str, str], name: str) -> int:
    return int(row[name])


def static_acceptance() -> None:
    with CSV.open(encoding="utf-8-sig", newline="") as stream:
        active = [row for row in csv.DictReader(stream) if row["catalog_status"] == "active"]
    required = ("weapon_mass", "cyclic_rpm", "weapon_size_class", "burst_limiter")
    missing = [row["id"] for row in active if any(not row.get(key) for key in required)]
    assert not missing, f"missing physical fields: {', '.join(missing)}"
    by_id = {row["id"]: row for row in active}
    for weapon_id, lo, hi in (("AK74", 14, 15), ("AKM", 24, 26), ("FNFAL", 42, 44)):
        assert lo <= number(by_id[weapon_id], "recoil") <= hi, weapon_id
    assert number(by_id["MicroUZI"], "recoil") > number(by_id["Sterling"], "recoil")
    assert number(by_id["MicroUZI"], "recoil") > number(by_id["MP5K"], "recoil")
    assert number(by_id["M16A2"], "burst_limiter") == 3
    assert number(by_id["M16A2"], "burst_shots") <= 3
    assert number(by_id["AN94"], "burst_limiter") == 2
    assert number(by_id["AN94"], "burst_shots") == 2
    print(f"PASS active={len(active)} anchors=AK74/AKM/FNFAL smg=MicroUZI>MP5K,Sterling")

"""Audit Recoil values and burst retention curves."""

import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "InventoryItem"


def sim_bullets(p0: float, retention: float, n: int = 6) -> list[int]:
    out = []
    for i in range(1, n + 1):
        chance = p0 * (retention ** (i - 1))
        out.append(max(2, min(100, round(chance))))
    return out


def main() -> None:
    static_acceptance()
    vals: list[tuple[str, int, str]] = []
    by_class: dict[str, list[int]] = defaultdict(list)

    for p in sorted(ROOT.glob("*.lua")):
        if p.name.endswith(".bak"):
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"Recoil\s*=\s*(\d+)", t)
        if not m:
            continue
        r = int(m.group(1))
        cls = "?"
        for pat in (
            r'ObjectClass\s*=\s*"(\w+)"',
            r'WeaponType\s*=\s*"([^"]+)"',
            r'DisplayClass\s*=\s*"([^"]+)"',
        ):
            mm = re.search(pat, t)
            if mm:
                cls = mm.group(1)
                break
        if cls == "?":
            cm = re.search(r'PlaceObj\(\s*"(\w+)"', t)
            if cm:
                cls = cm.group(1)
        vals.append((p.stem, r, cls))
        by_class[cls].append(r)

    rs = [v[1] for v in vals]
    print(f"count={len(vals)} min={min(rs)} med={statistics.median(rs)} mean={statistics.mean(rs):.1f} max={max(rs)}")
    print("distribution:")
    for k, c in sorted(Counter(rs).items()):
        print(f"  Recoil={k}: {c}")

    print("\nby class (mean):")
    for cls in sorted(by_class, key=lambda x: statistics.mean(by_class[x])):
        arr = by_class[cls]
        print(f"  {cls}: n={len(arr)} mean={statistics.mean(arr):.1f} range={min(arr)}-{max(arr)}")

    print("\nlowest 20:")
    for name, r, cls in sorted(vals, key=lambda x: x[1])[:20]:
        print(f"  {name}: {r} ({cls})")

    print("\nhighest 15:")
    for name, r, cls in sorted(vals, key=lambda x: -x[1])[:15]:
        print(f"  {name}: {r} ({cls})")

    print("\n--- retention curves (standing Str50, no perk/support) ---")
    # strength_factor at Str50 = 1.25 - 50/200 = 1.0
    # stance standing = 1.0
    print("P0=70 BurstFire 3 / AutoFire 6 bullets")
    for recoil in (4, 8, 10, 12, 15, 18, 20, 25, 32, 40):
        eff = recoil * 1.0  # Str50 standing
        ret = max(0.15, min(1.0, 1 - eff / 100))
        burst = sim_bullets(70, ret, 3)
        auto = sim_bullets(70, ret, 6)
        expected_burst = sum(p / 100 for p in burst)
        expected_auto = sum(p / 100 for p in auto)
        print(
            f"  Recoil={recoil:2d} ret={ret:.2f} "
            f"burst={burst} E~{expected_burst:.2f}  "
            f"auto={auto} E~{expected_auto:.2f}"
        )

    print("\n--- same with Compensator-ish Recoil-3 equivalent (scale numbers) ---")
    for recoil in (8, 12, 15, 20):
        eff = max(0, recoil - 3)
        ret = max(0.15, min(1.0, 1 - eff / 100))
        auto = sim_bullets(70, ret, 6)
        print(f"  Recoil {recoil}->eff{eff} ret={ret:.2f} auto={auto}")

    print("\n--- AutoWeapons perk (*0.85) on Recoil=12 ---")
    for recoil in (12, 15, 20):
        eff = recoil * 0.85
        ret = max(0.15, min(1.0, 1 - eff / 100))
        auto = sim_bullets(70, ret, 6)
        print(f"  Recoil={recoil} eff={eff:.1f} ret={ret:.2f} auto={auto}")

    print("\n--- Recoil needed for target falloff ---")
    for target_bullet, target_frac in ((3, 0.5), (3, 0.6), (4, 0.5), (6, 0.4), (6, 0.5)):
        exp = target_bullet - 1
        ret = target_frac ** (1 / exp)
        recoil = (1 - ret) * 100
        print(f"  bullet{target_bullet} @ {int(target_frac*100)}% of P0 => ret={ret:.3f} Recoil~{recoil:.1f}")

    print("\n--- if formula uses Recoil/50 instead of /100 ---")
    for recoil in (8, 10, 12, 15, 20, 25):
        eff = recoil
        ret = max(0.15, min(1.0, 1 - eff / 50))
        auto = sim_bullets(70, ret, 6)
        print(f"  Recoil={recoil:2d} ret={ret:.2f} auto={auto}")


if __name__ == "__main__":
    main()
