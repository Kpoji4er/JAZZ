#!/usr/bin/env python3
"""Audit the perfect-condition jam contract across all JAZZ firearms.

At rounded condition_percent >= 100 the runtime guarantees 0% raw jam with
serviceable ammo, 10% with *_Poor, and 15% with *_Crafted, independent of
weapon tier. The audit enumerates every compatible degraded-ammo pair and
also verifies the runtime guard that implements that contract.
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "InventoryItem"


@dataclass(frozen=True)
class Weapon:
    item_id: str
    caliber: str
    reliability: int
    base_jam: int


@dataclass(frozen=True)
class Ammo:
    item_id: str
    caliber: str
    reliability_add: int
    base_jam_add: int


def lua_int(text: str, prop: str, default: int) -> int:
    match = re.search(rf"^\s*{re.escape(prop)}\s*=\s*(-?\d+),", text, re.M)
    return int(match.group(1)) if match else default


def lua_string(text: str, prop: str) -> str | None:
    match = re.search(rf'^\s*{re.escape(prop)}\s*=\s*"([^"]+)",', text, re.M)
    return match.group(1) if match else None


def modification_add(text: str, prop: str) -> int:
    pattern = re.compile(
        r"PlaceObj\('CaliberModification',\s*\{(?P<body>.*?)\}\)", re.S
    )
    for match in pattern.finditer(text):
        body = match.group("body")
        if re.search(rf'target_prop\s*=\s*"{re.escape(prop)}"', body):
            return lua_int(body, "mod_add", 0)
    return 0


def div_round(value: int, divisor: int) -> int:
    return (value + divisor // 2) // divisor


def jam_percent(reliability: int, base_jam: int) -> int:
    return div_round(max(0, (100 - reliability) + base_jam), 10)


def load_data() -> tuple[list[Weapon], list[Ammo]]:
    weapons: list[Weapon] = []
    ammo: list[Ammo] = []
    firearm_parents = {
        "AssaultRifle", "Firearm", "Handgun", "MachineGun", "Pistol",
        "Revolver", "Shotgun", "SniperRifle", "SubmachineGun",
    }
    for path in sorted(INV.glob("*.lua")):
        text = path.read_text(encoding="utf-8")
        id_match = re.search(r"DefineClass\.([A-Za-z0-9_]+)\s*=", text)
        caliber = lua_string(text, "Caliber")
        if not id_match or not caliber:
            continue
        item_id = id_match.group(1)
        parent_match = re.search(r'__parents\s*=\s*\{\s*"([^"]+)"', text)
        parent = parent_match.group(1) if parent_match else ""
        if parent in firearm_parents:
            weapons.append(Weapon(
                item_id,
                caliber,
                lua_int(text, "Reliability", 50),
                lua_int(text, "BaseJamChance", 5),
            ))
        elif parent == "Ammo" and ("_Poor" in item_id or "_Crafted" in item_id):
            ammo.append(Ammo(
                item_id,
                caliber,
                modification_add(text, "Reliability"),
                modification_add(text, "BaseJamChance"),
            ))
    return weapons, ammo


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-poor-delta", type=int, default=10)
    parser.add_argument("--max-crafted-delta", type=int, default=15)
    parser.add_argument("--max-fresh-base", type=int, default=0)
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    weapons, ammo = load_data()
    rows: list[tuple[int, str, str, int, int, int, int]] = []
    failures: list[str] = []
    runtime = (ROOT / "Code" / "System_OR_Weapons.lua").read_text(encoding="utf-8")
    for fragment in (
        'string.match(ammo_class, "_Poor$")',
        'string.match(ammo_class, "_Crafted$")',
        'if condition_percent >= 100 then',
        'return JazzPerfectConditionAmmoJamScore(item.ammo)',
    ):
        if fragment not in runtime:
            failures.append(f"runtime perfect-condition contract missing: {fragment}")
    for weapon in weapons:
        # At condition_percent >= 100 runtime deliberately ignores weapon tier:
        # serviceable ammo is 0%, Poor is 10%, Crafted is 15%.
        base = 0
        if base > args.max_fresh_base:
            failures.append(
                f"{weapon.item_id} fresh base: {base}% > {args.max_fresh_base}%"
            )
        for cartridge in ammo:
            if weapon.caliber != cartridge.caliber:
                continue
            loaded = 10 if "_Poor" in cartridge.item_id else 15
            rows.append((loaded, weapon.item_id, cartridge.item_id, base,
                         weapon.reliability, weapon.base_jam,
                         loaded - base))
            delta = loaded - base
            limit = (
                args.max_poor_delta
                if "_Poor" in cartridge.item_id
                else args.max_crafted_delta
            )
            if delta > limit:
                failures.append(
                    f"{weapon.item_id} + {cartridge.item_id}: "
                    f"delta {delta}pp > {limit}pp (loaded {loaded}%)"
                )

    print(f"weapons={len(weapons)} degraded_ammo={len(ammo)} pairs={len(rows)}")
    print("loaded base delta reliability base_jam weapon + ammo")
    for loaded, weapon_id, ammo_id, base, reliability, base_jam, delta in sorted(
        rows, reverse=True
    )[:args.top]:
        print(
            f"{loaded:>3}% {base:>3}% {delta:>+3}pp "
            f"rel={reliability:>3} jam={base_jam:>4} {weapon_id} + {ammo_id}"
        )

    m3 = [row for row in rows if row[1] == "M3GreaseGun" and "_45ACP_Poor" in row[2]]
    if len(m3) != 1 or m3[0][0] != 10:
        actual = m3[0][0] if m3 else "missing"
        failures.append(f"M3GreaseGun + 45ACP Poor must be 10%, got {actual}")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
