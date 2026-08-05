#!/usr/bin/env python3
"""Apply JAZZ-WEAPONS-003/008 physical firearm authoring data.

Reads the active rows in weapons.csv, assigns the authored mass/RPM/size/limiter
profile, derives Recoil/BurstShots/AutoShots, and writes the same values to the
InventoryItem companion, ModItemInventoryItemCompositeDef in items.lua, and CSV.
Default operation is a dry run; --apply writes .bak siblings once per file.

JAZZ-WEAPONS-008: SMG mass/size placeholders (80/Long) replaced; SMG floor 12;
true MG auto cap ignores SubmachineGun substring.

Carbine hole fix: class default + ignore csv cyclic_rpm=0 when Burst/Auto exist;
G36/G36c BurstLimiter=2; carbine Recoil floor 12 (same as AR/SMG).
"""
from __future__ import annotations

import argparse
import csv
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "docs/technical/weapons/data/weapons.csv"
ITEMS = ROOT / "items.lua"
INV = ROOT / "InventoryItem"

SIZE_FACTOR = {"Compact": 1.15, "Carbine": 1.00, "Rifle": .92, "Long": .85}
IMPULSE = {
    "9x18": 9, "9x19": 12, "762x25": 12, "38": 10, "45ACP": 13, "44CAL": 18,
    "50AE": 24, "57": 11, "46": 10, "545": 17, "556": 18, "300BLK": 20,
    "762x39": 24, "762x51": 40, "762x54R": 41, "308": 40, "30-06": 41,
    "30cal": 15,  # .30 Carbine (M2Carbine)
    "8mm": 39, "12gauge": 30, "20gauge": 24, "50BMG": 54, "127": 54,
}

# Exact authoring corrections.  All other active firearms receive the explicit
# class/caliber profile below, keeping this table small enough to audit.
# Tuple: mass (0.1 kg), rpm, size, limiter, optional Recoil override.
AUTHORED_OVERRIDES = {
    "AK74": (35, 650, "Rifle", 0, 15),
    "AKM": (36, 600, "Rifle", 0, 25),
    "FNFAL": (43, 650, "Rifle", 0, 43),
    "MicroUZI": (27, 1200, "Compact", 0, None),
    "MP5K": (30, 900, "Compact", 0, None),
    "MP5": (30, 800, "Carbine", 0, None),
    "MP5A2": (31, 800, "Carbine", 0, None),
    "MP5A4": (31, 800, "Carbine", 0, None),
    "MP5SD": (34, 800, "Carbine", 0, None),
    "Sterling": (33, 550, "Carbine", 0, None),
    "BerettaM12": (32, 600, "Carbine", 0, None),
    "MAT49": (36, 600, "Carbine", 0, None),
    "MP40": (40, 500, "Carbine", 0, None),
    "M3GreaseGun": (36, 450, "Carbine", 0, None),
    "PPS43": (30, 600, "Carbine", 0, None),
    "PPSH": (36, 900, "Carbine", 0, None),
    "Thompson": (48, 700, "Carbine", 0, None),
    "MPL": (30, 550, "Carbine", 0, None),
    "Agram2000": (22, 800, "Compact", 0, None),
    "UZI": (35, 600, "Carbine", 0, None),
    "M45": (35, 600, "Carbine", 0, None),
    "PP19Bizon": (27, 680, "Carbine", 0, None),
    "SpectreM4": (29, 850, "Compact", 0, None),
    "TMP": (25, 900, "Compact", 0, None),
    "UMP45": (30, 600, "Carbine", 0, None),
    "MP7": (21, 950, "Compact", 0, None),
    "P90": (28, 900, "Compact", 0, None),
    "LionRoar": (35, 700, "Carbine", 0, None),
    "M16A2": (34, 700, "Rifle", 3, None),
    "M16A4": (34, 700, "Rifle", 3, None),  # burst-cut like A2; Jazz has LargeAutoFire separately
    "AN94": (39, 1800, "Rifle", 2, None),
    # G36 family: mechanical 2-rd burst (BurstLimiter caps BurstFire only).
    "G36": (36, 750, "Rifle", 2, None),
    "G36c": (30, 750, "Carbine", 2, None),
    # 3-rd mechanical burst platforms (BurstFire capped; AutoFire length unchanged).
    "FAMAS": (37, 900, "Rifle", 3, None),
    "AUG": (36, 700, "Rifle", 3, None),
    "HK33": (37, 750, "Rifle", 3, None),
    "Sig550": (41, 700, "Rifle", 3, None),
    "Sig550Custom": (41, 700, "Rifle", 3, None),
    "G3A3": (44, 550, "Rifle", 3, None),
    "G3A4": (43, 550, "Rifle", 3, None),
    # Carbines (WEAPONS-003 M4A1 anchor 800/4/8; class was previously rpm=0 hole).
    "M4A1": (33, 800, "Carbine", 0, None),
    "CAR15": (30, 750, "Carbine", 0, None),
    "AKSU": (27, 700, "Carbine", 0, None),
    "Sig552": (32, 700, "Carbine", 0, None),
    "Sig552SWAT": (32, 700, "Carbine", 0, None),
    "AS_Val": (28, 900, "Carbine", 0, None),
    "ZastavaM92": (33, 700, "Carbine", 0, None),
    "VSS": (28, 800, "Carbine", 0, None),  # BurstFire only → AutoShots=0
    "SVU": (48, 650, "Long", 0, None),  # BurstFire DMR; sniper class previously forced rpm=0
    # Component-gated auto (JAZZ_Autofire Trigger): base AvailableAttacks stay semi-only,
    # but Burst/Auto shot counts must be authored for EnableFullAuto/EnableBurst.
    "M2Carbine": (28, 750, "Carbine", 0, None),
    "Mini14": (30, 750, "Carbine", 0, None),  # AC-556; JAZZ_Autofire Trigger (same as M2)
    "MAC10": (28, 1100, "Compact", 0, None),
    "Glock18": (26, 1200, "Compact", 0, None),
    "Beretta93r": (26, 1100, "Compact", 3, None),
    "APS": (30, 750, "Compact", 0, None),
}

# Weapons whose Burst/Auto come from EnableBurst/EnableFullAuto components, not AvailableAttacks.
COMPONENT_GATED_AUTOFIRE = frozenset({"M2Carbine", "Mini14"})



@dataclass(frozen=True)
class Profile:
    mass: int
    rpm: int
    size: str
    limiter: int
    recoil: int
    burst: int
    auto: int


def caliber_key(caliber: str) -> str:
    text = caliber.lower().replace("jazz_caliber_", "").replace(".", "")
    for key in IMPULSE:
        if key in text:
            return key
    return "762x39" if "762" in text else "9x19"


def is_true_machinegun(cls: str) -> bool:
    """SubmachineGun contains 'machinegun'; do not treat SMG as belt MG."""
    return "submachine" not in cls and (
        cls in {"machinegun", "lightmachinegun"} or cls.endswith("machinegun")
    )


def attack_set(attacks: str) -> set[str]:
    """CSV/companion attack lists use ';' — never substring-match (MGBurstFire ⊃ BurstFire)."""
    return {part.strip() for part in (attacks or "").replace(",", ";").split(";") if part.strip()}


def needs_cyclic_rpm(attacks: str) -> bool:
    """Select-fire / auto platforms must not keep placeholder CyclicRPM=0."""
    tokens = attack_set(attacks)
    return bool(tokens & {
        "AutoFire", "BurstFire", "MGBurstFire", "JAZZ_LargeAutoFire",
        "AbakanBurst", "AbakanAutoFire",
    })


def class_default_profile(cls: str, attacks: str) -> tuple[int, int, str, int, float]:
    cyclic = 700 if needs_cyclic_rpm(attacks) else 0
    if "sniper" in cls or "precision" in cls:
        # Semi bolt/DMR keep rpm=0; BurstFire SVU-class must get cyclic (was forced 0 hole).
        return 55, cyclic, "Long", 0, 1.0
    # SubmachineGun before MachineGun: "submachinegun" contains "machinegun".
    if "submachine" in cls:
        return 32, 700, "Carbine", 0, 1.0
    if is_true_machinegun(cls):
        return 80, 700, "Long", 0, .92
    if "shotgun" in cls:
        return 36, 0, "Rifle", 0, 1.0
    if "carbine" in cls:
        # Short AR / select-fire carbines; semi-only stay rpm=0.
        return 32, cyclic, "Carbine", 0, 1.0
    if "assault" in cls or "battle" in cls:
        return 36, cyclic, "Rifle", 0, 1.0
    if "autopistol" in cls:
        return 27, 900, "Compact", 0, 1.0
    if "pistol" in cls or "revolver" in cls:
        return 10, 0, "Compact", 0, 1.0
    if "rifle" in cls:
        return 40, 0, "Long", 0, 1.0
    return 35, cyclic, "Rifle", 0, 1.0


def default_profile(row: dict[str, str]) -> tuple[int, int, str, int, float]:
    cls = row["object_class"].lower()
    attacks = row.get("available_attacks") or ""
    def_mass, def_rpm, def_size, def_lim, family_f = class_default_profile(cls, attacks)
    # Prefer CSV-authored mass/rpm/size when present (unique/quest companions),
    # but reject known SMG placeholders (mass≥70 + Long) from WEAPONS-003 drift.
    # csv cyclic_rpm=0 is a placeholder when the platform has Burst/Auto — use class default.
    csv_mass = int(row["weapon_mass"] or 0) if row.get("weapon_mass") else 0
    csv_rpm = int(row["cyclic_rpm"] or 0) if row.get("cyclic_rpm") else 0
    csv_size = row.get("weapon_size_class") or ""
    csv_lim = int(row["burst_limiter"] or 0) if row.get("burst_limiter") else 0
    smg_placeholder = "submachine" in cls and csv_mass >= 70 and csv_size == "Long"
    if csv_mass and csv_size in SIZE_FACTOR and not smg_placeholder:
        rpm = csv_rpm if csv_rpm > 0 else def_rpm
        return csv_mass, rpm, csv_size, csv_lim, family_f
    return def_mass, def_rpm, def_size, def_lim, family_f


def authored_profile(row: dict[str, str]) -> Profile:
    mass, rpm, size, limiter, family_f = default_profile(row)
    override = AUTHORED_OVERRIDES.get(row["id"])
    recoil_override = None
    if override:
        mass, rpm, size, limiter, recoil_override = override
    impulse = IMPULSE[caliber_key(row["caliber"])]
    mass_f = max(.70, min(1.45, 35 / mass))
    rpm_f = 1 + max(-.08, min(.18, (rpm - 700) / 2000))
    recoil = round(impulse * mass_f * SIZE_FACTOR[size] * rpm_f * family_f)
    cls = row["object_class"].lower()
    # WEAPONS-008: SMG floor 12 (was 18 — flattened all ПП). AR/Carbine also 12.
    if "pistol" in cls or "revolver" in cls:
        floor = 5
    elif "submachine" in cls or "assault" in cls or "carbine" in cls:
        floor = 12
    else:
        floor = 18
    recoil = max(floor, min(70, recoil_override if recoil_override is not None else recoil))
    tokens = attack_set(row["available_attacks"])
    gated = row["id"] in COMPONENT_GATED_AUTOFIRE
    # Shotgun pellet count is BuckshotProjectiles (JAZZ-WEAPONS-006), not AutoShots.
    # BurstFire / AbakanBurst / MGBurstFire (BurstShots feeds GetAutofireShots MG fallback).
    # COMPONENT_GATED_AUTOFIRE: JAZZ_Autofire enables modes at runtime — still author shot counts.
    has_burst_mode = gated or bool(tokens & {"BurstFire", "AbakanBurst", "MGBurstFire"})
    burst = max(2, min(8, round(rpm / 200))) if rpm and has_burst_mode else 0
    if limiter and burst:
        burst = min(burst, limiter)
    auto_max = 10 if is_true_machinegun(cls) else 14
    has_auto_mode = gated or bool(tokens & {"AutoFire", "AbakanAutoFire", "JAZZ_LargeAutoFire"})
    auto = max(3, min(auto_max, round(rpm / 100))) if rpm and has_auto_mode else 0
    return Profile(mass, rpm, size, limiter, recoil, burst, auto)


def paren_end(text: str, start: int) -> int:
    depth, quote, i = 0, None, start
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unclosed PlaceObj")


def item_blocks(text: str) -> list[tuple[int, int, str]]:
    found, pos = [], 0
    match_re = re.compile(r"PlaceObj\((?:'|\")ModItemInventoryItemCompositeDef(?:'|\")")
    while (match := match_re.search(text, pos)) is not None:
        start = match.start()
        end = paren_end(text, text.find("(", start))
        found.append((start, end, text[start:end]))
        pos = end
    return found


def id_of(block: str) -> str | None:
    # Prefer the ModItem Id near the head (avoid later nested keys).
    match = re.search(r"(?:'|\")Id(?:'|\"),\s*\"([^\"]+)\"", block[:1200])
    if match:
        return match.group(1)
    match = re.search(r"(?:'|\")id(?:'|\"),\s*\"([^\"]+)\"", block[:1200], re.IGNORECASE)
    return match.group(1) if match else None


def set_lua_prop(text: str, key: str, value: int | str, placeobj: bool) -> str:
    rendered = f'"{value}"' if isinstance(value, str) else str(value)
    pattern = (rf"(?P<prefix>'{re.escape(key)}',\s*)(?:\"[^\"]*\"|-?\d+)"
               if placeobj else rf"(?P<prefix>\b{re.escape(key)}\s*=\s*)(?:\"[^\"]*\"|-?\d+)")
    if re.search(pattern, text):
        return re.sub(pattern, rf"\g<prefix>{rendered}", text, count=1)
    anchor = re.search(
        r"(\n\s*(?:'Recoil',\s*\d+,|Recoil\s*=\s*\d+,|"
        r"'AutoShots',\s*\d+,|AutoShots\s*=\s*\d+,|"
        r"'MaxAimActions',\s*\d+,|MaxAimActions\s*=\s*\d+,))",
        text,
    )
    if not anchor:
        raise ValueError(f"cannot locate property insertion point for {key}")
    indent = re.search(r"\n(\s*)", anchor.group(1)).group(1)
    entry = f"\n{indent}'{key}', {rendered}," if placeobj else f"\n{indent}{key} = {rendered},"
    return text[:anchor.start()] + entry + text[anchor.start():]


def apply_profile(text: str, profile: Profile, placeobj: bool) -> str:
    for key, value in (
        ("WeaponMass", profile.mass), ("CyclicRPM", profile.rpm),
        ("WeaponSizeClass", profile.size), ("BurstLimiter", profile.limiter),
        ("Recoil", profile.recoil), ("BurstShots", profile.burst), ("AutoShots", profile.auto),
    ):
        text = set_lua_prop(text, key, value, placeobj)
    return text


def write(path: Path, content: str, apply: bool) -> None:
    if apply and path.read_text(encoding="utf-8") != content:
        backup = path.with_suffix(path.suffix + ".bak")
        if not backup.exists():
            shutil.copy2(path, backup)
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)


def update_csv(profiles: dict[str, Profile], apply: bool) -> None:
    with CSV.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    for row in rows:
        profile = profiles.get(row["id"])
        if not profile:
            continue
        row["weapon_mass"] = str(profile.mass)
        row["cyclic_rpm"] = str(profile.rpm)
        row["weapon_size_class"] = profile.size
        row["burst_limiter"] = str(profile.limiter)
        row["recoil"] = str(profile.recoil)
        if "burst_shots" in row:
            row["burst_shots"] = str(profile.burst)
        if "auto_shots" in row:
            row["auto_shots"] = str(profile.auto)
    if not apply:
        return
    backup = CSV.with_suffix(CSV.suffix + ".bak")
    if not backup.exists():
        shutil.copy2(CSV, backup)
    with CSV.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    with CSV.open(encoding="utf-8-sig", newline="") as stream:
        active = [row for row in csv.DictReader(stream) if row["catalog_status"] == "active"]
    profiles = {row["id"]: authored_profile(row) for row in active}
    profile_ids = {weapon_id.lower(): weapon_id for weapon_id in profiles}
    items = ITEMS.read_text(encoding="utf-8")
    seen = set()
    for start, end, block in reversed(item_blocks(items)):
        item_id = id_of(block)
        weapon_id = profile_ids.get(item_id.lower()) if item_id else None
        if weapon_id is None:
            continue
        items = items[:start] + apply_profile(block, profiles[weapon_id], True) + items[end:]
        seen.add(weapon_id)
    write(ITEMS, items, args.apply)
    companion_missing = []
    moditem_missing = []
    for weapon_id, profile in profiles.items():
        path = INV / f"{weapon_id}.lua"
        if not path.exists():
            path = INV / "vanillunique" / f"{weapon_id}.lua"
        if path.exists():
            write(path, apply_profile(path.read_text(encoding="utf-8"), profile, False), args.apply)
        else:
            companion_missing.append(weapon_id)
        if weapon_id not in seen:
            # Unique/quest companions may exist without a ModItem block in items.lua.
            moditem_missing.append(weapon_id)
    update_csv(profiles, args.apply)
    print(f"{'applied' if args.apply else 'dry-run'} active={len(profiles)} items={len(seen)}")
    for weapon_id in (
        "AK74", "AKM", "FNFAL", "MicroUZI", "MP5K", "MP5A2", "Sterling",
        "MAT49", "UZI", "P90", "LionRoar", "TexRevolver",
        "M4A1", "G36", "G36c", "CAR15", "AKSU", "VSS", "AS_Val", "ZastavaM92", "AN94",
        "SVU", "FAMAS", "AUG", "M16A4", "HK33", "Sig550", "G3A3", "M2Carbine", "Mini14",
    ):
        if weapon_id in profiles:
            print(f"{weapon_id}: {profiles[weapon_id]}")
    # Guard: BurstLimiter>0 must keep BurstShots>0; no BurstFire⊂MGBurstFire false positive.
    bad_lim = [
        wid for wid, p in profiles.items()
        if p.limiter > 0 and p.burst <= 0
    ]
    if bad_lim:
        raise SystemExit("BurstLimiter with BurstShots=0: " + ", ".join(bad_lim))
    false_burst = []
    for row in active:
        p = profiles[row["id"]]
        tokens = attack_set(row["available_attacks"])
        gated = row["id"] in COMPONENT_GATED_AUTOFIRE
        if p.burst > 0 and not gated and not (tokens & {"BurstFire", "AbakanBurst", "MGBurstFire"}):
            false_burst.append(row["id"])
    if false_burst:
        raise SystemExit("BurstShots without burst mode: " + ", ".join(false_burst))
    carb = [
        (row["id"], profiles[row["id"]])
        for row in active
        if "carbine" in row["object_class"].lower() and row["id"] in profiles
    ]
    if carb:
        zero_rpm = [wid for wid, p in carb if p.rpm == 0 and needs_cyclic_rpm(
            next(r["available_attacks"] for r in active if r["id"] == wid)
        )]
        print(f"Carbine n={len(carb)} select-fire rpm0={zero_rpm or 'ok'}")
    smg = [
        (row["id"], profiles[row["id"]])
        for row in active
        if "submachine" in row["object_class"].lower() and row["id"] in profiles
    ]
    if smg:
        recoils = sorted({p.recoil for _, p in smg})
        print(f"SMG Recoil set={recoils} n={len(smg)}")
    if companion_missing:
        raise SystemExit("missing companions: " + ", ".join(companion_missing))
    if moditem_missing:
        print("note: no ModItem in items.lua (companion-only): " + ", ".join(moditem_missing))


if __name__ == "__main__":
    main()
