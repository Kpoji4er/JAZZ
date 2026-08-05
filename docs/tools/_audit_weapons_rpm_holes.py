#!/usr/bin/env python3
"""Audit WEAPONS-003 holes: select-fire with rpm/burst/auto=0, missing limiters, etc."""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "docs/technical/weapons/data/weapons.csv"
INV = ROOT / "InventoryItem"

KNOWN_LIMITERS = {
    "M16A2": 3,
    "M16A4": 3,
    "AN94": 2,
    "G36": 2,
    "G36c": 2,
    "Beretta93r": 3,
    "FAMAS": 3,
    "AUG": 3,
    "HK33": 3,
    "Sig550": 3,
    "Sig550Custom": 3,
    "G3A3": 3,
    "G3A4": 3,
}

BURST_MODES = {"BurstFire", "AbakanBurst", "MGBurstFire"}
AUTO_MODES = {"AutoFire", "AbakanAutoFire", "JAZZ_LargeAutoFire"}


def attack_set(attacks: str) -> set[str]:
    return {p.strip() for p in (attacks or "").replace(",", ";").split(";") if p.strip()}


def load_csv() -> list[dict[str, str]]:
    with CSV.open(encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if r.get("catalog_status") == "active"]


def companion_props(wid: str) -> dict[str, str]:
    for path in (INV / f"{wid}.lua", INV / "vanillunique" / f"{wid}.lua"):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        out = {}
        for key in (
            "CyclicRPM", "BurstShots", "AutoShots", "BurstLimiter",
            "Recoil", "WeaponMass", "WeaponSizeClass",
        ):
            m = re.search(rf"\b{key}\s*=\s*(\"[^\"]*\"|-?\d+)", text)
            if m:
                out[key] = m.group(1).strip('"')
        return out
    return {}


def main() -> None:
    rows = load_csv()
    holes = []
    lim_mismatch = []
    csv_comp_mismatch = []
    zero_rpm_select = []
    zero_shots_with_mode = []
    autofire_auto0 = []
    burstfire_burst0 = []
    mass80_long_smg = []
    by_family = defaultdict(list)

    for r in rows:
        wid = r["id"]
        tokens = attack_set(r.get("available_attacks") or "")
        rpm = int(r.get("cyclic_rpm") or 0)
        burst = int(r.get("burst_shots") or 0)
        auto = int(r.get("auto_shots") or 0)
        lim = int(r.get("burst_limiter") or 0)
        mass = int(r.get("weapon_mass") or 0)
        size = r.get("weapon_size_class") or ""
        cls = (r.get("object_class") or "").lower()
        fam = r.get("family_id") or "?"

        has_burst = bool(tokens & BURST_MODES)
        has_auto = bool(tokens & AUTO_MODES)
        needs_cyclic = has_burst or has_auto

        if needs_cyclic and rpm <= 0:
            zero_rpm_select.append((wid, fam, sorted(tokens & (BURST_MODES | AUTO_MODES))))
            by_family[fam].append(wid)

        if has_auto and auto <= 0:
            autofire_auto0.append((wid, fam, rpm, auto, lim))
        if has_burst and burst <= 0:
            burstfire_burst0.append((wid, fam, rpm, burst, lim, sorted(tokens & BURST_MODES)))

        if wid in KNOWN_LIMITERS and lim != KNOWN_LIMITERS[wid]:
            lim_mismatch.append((wid, lim, KNOWN_LIMITERS[wid]))

        if "submachine" in cls and mass >= 70 and size == "Long":
            mass80_long_smg.append((wid, mass, size, rpm))

        # CSV vs companion drift on key fields
        comp = companion_props(wid)
        if comp:
            for key, csv_key in (
                ("CyclicRPM", "cyclic_rpm"),
                ("BurstShots", "burst_shots"),
                ("AutoShots", "auto_shots"),
                ("BurstLimiter", "burst_limiter"),
                ("Recoil", "recoil"),
            ):
                if key not in comp:
                    continue
                cv = str(r.get(csv_key) or "")
                if cv and comp[key] != cv:
                    csv_comp_mismatch.append((wid, key, cv, comp[key]))

        # Expected burst from rpm (informational when lim set but burst > lim)
        if lim > 0 and burst > lim:
            holes.append(f"{wid}: BurstShots={burst} > BurstLimiter={lim}")

    print("=== Select-fire / MG with CyclicRPM=0 ===")
    if not zero_rpm_select:
        print("OK none")
    else:
        for row in zero_rpm_select:
            print(f"  {row[0]:20} family={row[1]:16} modes={row[2]}")

    print("\n=== Has AutoFire-class mode but AutoShots=0 ===")
    if not autofire_auto0:
        print("OK none")
    else:
        for wid, fam, rpm, auto, lim in autofire_auto0:
            print(f"  {wid:20} fam={fam:14} rpm={rpm} auto={auto} lim={lim}")

    print("\n=== Has Burst/MG/Abakan mode but BurstShots=0 ===")
    if not burstfire_burst0:
        print("OK none")
    else:
        for wid, fam, rpm, burst, lim, modes in burstfire_burst0:
            print(f"  {wid:20} fam={fam:14} rpm={rpm} burst={burst} lim={lim} modes={modes}")

    print("\n=== Known BurstLimiter mismatch ===")
    if not lim_mismatch:
        print("OK", KNOWN_LIMITERS)
    else:
        for wid, got, want in lim_mismatch:
            print(f"  {wid}: got={got} want={want}")

    print("\n=== SMG placeholder mass>=70 + Long ===")
    if not mass80_long_smg:
        print("OK none")
    else:
        for row in mass80_long_smg:
            print(" ", row)

    print("\n=== CSV vs companion drift (key fields) ===")
    if not csv_comp_mismatch:
        print("OK none")
    else:
        for row in csv_comp_mismatch[:40]:
            print(f"  {row[0]} {row[1]} csv={row[2]} comp={row[3]}")
        if len(csv_comp_mismatch) > 40:
            print(f"  ... +{len(csv_comp_mismatch) - 40} more")

    print("\n=== BurstLimiter>0 but BurstShots>Limiter ===")
    if not holes:
        print("OK none")
    else:
        for h in holes:
            print(" ", h)

    # Spec anchors spot-check
    print("\n=== Spec anchors (WEAPONS-003 examples) ===")
    want = {
        "AK74": dict(rpm=650, burst=3, auto=(6, 7), lim=0),
        "M4A1": dict(rpm=800, burst=4, auto=(8, 8), lim=0),
        "M16A2": dict(rpm=700, burst=3, auto=(7, 7), lim=3),
        "AN94": dict(rpm=1800, burst=2, auto=(14, 14), lim=2),
        "MicroUZI": dict(rpm=1200, burst=6, auto=(12, 12), lim=0),
    }
    by_id = {r["id"]: r for r in rows}
    for wid, w in want.items():
        r = by_id.get(wid)
        if not r:
            print(f"  {wid}: MISSING from CSV")
            continue
        rpm = int(r["cyclic_rpm"] or 0)
        burst = int(r["burst_shots"] or 0)
        auto = int(r["auto_shots"] or 0)
        lim = int(r["burst_limiter"] or 0)
        ok = (
            rpm == w["rpm"]
            and burst == w["burst"]
            and w["auto"][0] <= auto <= w["auto"][1]
            and lim == w["lim"]
        )
        mark = "OK" if ok else "DRIFT"
        print(
            f"  {mark} {wid}: rpm={rpm}/{w['rpm']} b={burst}/{w['burst']} "
            f"a={auto}/{w['auto']} lim={lim}/{w['lim']}"
        )

    # Families still with any rpm0 select-fire
    print("\n=== Families with remaining select-fire rpm0 ===")
    if not by_family:
        print("OK none")
    else:
        for fam, ids in sorted(by_family.items()):
            print(f"  {fam}: {', '.join(ids)}")

    # Report candidates: full-auto AR/carbine/SMG with lim=0 that IRL often have 2/3
    print("\n=== Possible missing BurstLimiter (heuristic, not auto-fix) ===")
    candidates = []
    for r in rows:
        wid = r["id"]
        if wid in KNOWN_LIMITERS:
            continue
        tokens = attack_set(r.get("available_attacks") or "")
        lim = int(r.get("burst_limiter") or 0)
        if lim:
            continue
        # German/US burst-fire famous platforms not yet tagged
        name = (r.get("display_name") or wid).lower()
        if any(k in wid.lower() or k in name for k in ("m16a4", "hk33", "g3", "aug", "famas", "sig550")):
            if "BurstFire" in tokens:
                candidates.append((wid, r.get("object_class"), r.get("available_attacks")))
    for c in candidates:
        print(f"  ? {c[0]:16} {c[1]:16} {c[2]}")
    if not candidates:
        print("  (none matching heuristic names)")


if __name__ == "__main__":
    main()
