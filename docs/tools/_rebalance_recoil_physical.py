#!/usr/bin/env python3
"""Apply JAZZ-WEAPONS-003 physical firearm authoring data.

Reads the active rows in weapons.csv, assigns the authored mass/RPM/size/limiter
profile, derives Recoil/BurstShots/AutoShots, and writes the same values to the
InventoryItem companion and its ModItemInventoryItemCompositeDef in items.lua.
Default operation is a dry run; --apply writes .bak siblings once per file.
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
    "8mm": 39, "12gauge": 30, "20gauge": 24, "50BMG": 54, "127": 54,
}

# Exact authoring corrections.  All other active firearms receive the explicit
# class/caliber profile below, keeping this table small enough to audit.
AUTHORED_OVERRIDES = {
    "AK74": (35, 650, "Rifle", 0, 15),
    "AKM": (36, 600, "Rifle", 0, 25),
    "FNFAL": (43, 650, "Rifle", 0, 43),
    "MicroUZI": (27, 1200, "Compact", 0, None),
    "MP5K": (30, 900, "Compact", 0, None),
    "MP5": (30, 800, "Carbine", 0, None),
    "MP5A2": (31, 800, "Carbine", 0, None),
    "Sterling": (33, 550, "Carbine", 0, None),
    "BerettaM12": (32, 600, "Carbine", 0, None),
    "M16A2": (34, 700, "Rifle", 3, None),
    "AN94": (39, 1800, "Rifle", 2, None),
    "MAC10": (28, 1100, "Compact", 0, None),
    "Glock18": (26, 1200, "Compact", 0, None),
    "Beretta93r": (26, 1100, "Compact", 3, None),
    "APS": (30, 750, "Compact", 0, None),
}


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


def default_profile(row: dict[str, str]) -> tuple[int, int, str, int, float]:
    cls = row["object_class"].lower()
    # Prefer CSV-authored mass/rpm/size when present (unique/quest companions).
    csv_mass = int(row["weapon_mass"] or 0) if row.get("weapon_mass") else 0
    csv_rpm = int(row["cyclic_rpm"] or 0) if row.get("cyclic_rpm") else 0
    csv_size = row.get("weapon_size_class") or ""
    csv_lim = int(row["burst_limiter"] or 0) if row.get("burst_limiter") else 0
    if csv_mass and csv_size in SIZE_FACTOR:
        return csv_mass, csv_rpm, csv_size, csv_lim, 1.0
    if "sniper" in cls or "precision" in cls:
        return 55, 0, "Long", 0, 1.0
    # SubmachineGun before MachineGun: "submachinegun" contains "machinegun".
    if "submachine" in cls:
        return 32, 700, "Carbine", 0, 1.0
    if cls in {"machinegun", "lightmachinegun"} or cls.endswith("machinegun"):
        return 80, 700, "Long", 0, .92
    if "shotgun" in cls:
        return 36, 0, "Rifle", 0, 1.0
    if "assault" in cls or "battle" in cls:
        return 36, 700, "Rifle", 0, 1.0
    if "autopistol" in cls:
        return 27, 900, "Compact", 0, 1.0
    if "pistol" in cls or "revolver" in cls:
        return 10, 0, "Compact", 0, 1.0
    if "rifle" in cls:
        return 40, 0, "Long", 0, 1.0
    return 35, 0, "Rifle", 0, 1.0


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
    floor = 5 if ("pistol" in cls or "revolver" in cls) else 12 if "assault" in cls else 18
    recoil = max(floor, min(70, recoil_override if recoil_override is not None else recoil))
    attacks = row["available_attacks"]
    # Shotgun pellet count is BuckshotProjectiles (JAZZ-WEAPONS-006), not AutoShots.
    burst = max(2, min(8, round(rpm / 200))) if rpm and ("BurstFire" in attacks or limiter) else 0
    if limiter:
        burst = min(burst, limiter) if burst else 0
    auto_max = 10 if "machinegun" in cls else 14
    auto = max(3, min(auto_max, round(rpm / 100))) if rpm and "AutoFire" in attacks else 0
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
    match = re.search(r"(?:'|\")id(?:'|\"),\s*\"([^\"]+)\"", block, re.IGNORECASE)
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
    print(f"{'applied' if args.apply else 'dry-run'} active={len(profiles)} items={len(seen)}")
    for weapon_id in ("AK74", "AKM", "FNFAL", "MicroUZI", "MP5K", "MP5", "Sterling", "BerettaM12", "LionRoar", "TexRevolver"):
        if weapon_id in profiles:
            print(f"{weapon_id}: {profiles[weapon_id]}")
    if companion_missing:
        raise SystemExit("missing companions: " + ", ".join(companion_missing))
    if moditem_missing:
        print("note: no ModItem in items.lua (companion-only): " + ", ".join(moditem_missing))


if __name__ == "__main__":
    main()
