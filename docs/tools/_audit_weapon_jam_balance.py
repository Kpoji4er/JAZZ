#!/usr/bin/env python3
"""Audit the JAZZ-WEAPONS-010 additive jam curve.

The audit models Reliability/BaseJamChance, current condition, permanent
max-resource wear (dominant + half secondary stack), the normal-condition
10% cap, soft 99% ceiling while any resource remains, and the owner-provided
MP40/Mosin anchors. It also checks that the runtime contains this contract.
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


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(value, high))


def base_jam_score(reliability: int, base_jam: int) -> int:
    """Mirror JazzGetBaseJamScore: Rel clamped 5..95; Rel>=95 → 0 base."""
    reliability = clamp(reliability, 5, 95)
    if reliability >= 95:
        return 0
    reliability_score = max(0, 100 - reliability)
    if base_jam >= 0:
        scaled = (base_jam * reliability_score + 95 // 2) // 95
        score = max(reliability_score, scaled)
    else:
        score = reliability_score + base_jam
    return clamp(score, 0, 100)


def resource_penalty(resource_percent: int) -> int:
    resource_percent = clamp(resource_percent, 0, 100)
    if resource_percent <= 0:
        return 1000
    if resource_percent < 10:
        return 450
    if resource_percent < 20:
        return 320
    if resource_percent < 30:
        return 230
    if resource_percent < 40:
        return 160
    if resource_percent < 50:
        return 110
    if resource_percent < 60:
        return 80
    if resource_percent < 70:
        return 60
    if resource_percent < 80:
        return 55
    if resource_percent < 90:
        return 50
    if resource_percent < 100:
        return 10
    return 0


def raw_jam_score(
    reliability: int,
    base_jam: int,
    current_resource: int,
    max_resource: int,
    factory_resource: int,
) -> int:
    if max_resource <= 0 or factory_resource <= 0:
        return 1000
    condition = clamp(div_round(current_resource * 100, max_resource), 0, 100)
    permanent = clamp(div_round(max_resource * 100, factory_resource), 0, 100)
    if condition <= 0 or permanent <= 0:
        return 1000
    condition_pen = resource_penalty(condition)
    permanent_pen = resource_penalty(permanent)
    score = (
        base_jam_score(reliability, base_jam)
        + max(condition_pen, permanent_pen)
        + div_round(min(condition_pen, permanent_pen), 2)
    )
    if condition >= 80 and permanent >= 80:
        score = min(score, 100)
    service = min(condition, permanent)
    service_discount = (50 * service * service + 5000) // 10000
    score = max(0, score - service_discount)
    if condition > 0 and permanent > 0:
        score = min(score, 990)
    return clamp(score, 0, 1000)


def display_percent(score: int) -> int:
    return div_round(score, 10)


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
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    weapons, ammo = load_data()
    weapon_by_id = {weapon.item_id: weapon for weapon in weapons}
    rows: list[tuple[int, str, str, int, int, int]] = []
    failures: list[str] = []
    runtime = (ROOT / "Code" / "System_OR_Weapons.lua").read_text(encoding="utf-8")
    for fragment in (
        "local function JazzGetBaseJamScore(item)",
        'Clamp(item:GetProperty("Reliability") or 50, 5, 95)',
        "if reliability >= 95 then",
        "MulDivRound(base_jam, reliability_score, 95)",
        "score = Max(reliability_score, scaled)",
        "score = reliability_score + base_jam",
        "return Clamp(score, 0, 100)",
        "local function JazzGetJamResourcePenalty(resource_percent)",
        "MulDivRound(resource, 100, max_resource)",
        "MulDivRound(max_resource, 100, factory)",
        "Max(condition_penalty, permanent_penalty)",
        "DivRound(Min(condition_penalty, permanent_penalty), 2)",
        "if condition_percent >= 80 and permanent_percent >= 80 then",
        "raw_chance = Min(raw_chance, 100)",
        "MulDivRound(50, service * service, 10000)",
        "raw_chance = Max(0, raw_chance - service_discount)",
        "raw_chance = Min(raw_chance, 990)",
    ):
        if fragment not in runtime:
            failures.append(f"runtime additive-curve contract missing: {fragment}")
    for forbidden in ("JazzPerfectConditionAmmoJamScore", "degrade_mult"):
        if forbidden in runtime:
            failures.append(f"obsolete multiplicative contract remains: {forbidden}")

    expected_penalties = {
        100: 0,
        90: 10,
        80: 50,
        70: 55,
        60: 60,
        50: 80,
        40: 110,
        30: 160,
        20: 230,
        10: 320,
        1: 450,
        0: 1000,
    }
    penalty_body_match = re.search(
        r"local function JazzGetJamResourcePenalty\(resource_percent\)"
        r"(?P<body>.*?)\nend",
        runtime,
        re.S,
    )
    if not penalty_body_match:
        failures.append("cannot parse runtime resource-penalty helper")
        penalty_body = ""
    else:
        penalty_body = penalty_body_match.group("body")
    runtime_steps = (
        (10, 450),
        (20, 320),
        (30, 230),
        (40, 160),
        (50, 110),
        (60, 80),
        (70, 60),
        (80, 55),
        (90, 50),
        (100, 10),
    )
    for threshold, penalty in runtime_steps:
        if not re.search(
            rf"resource_percent < {threshold} then\s+return {penalty}\b",
            penalty_body,
        ):
            failures.append(
                f"runtime penalty step <{threshold} -> {penalty} missing"
            )
    if not re.search(
        r"resource_percent <= 0 then\s+return 1000\b", penalty_body
    ):
        failures.append("runtime zero-resource 100% gate missing")
    if not re.search(r"\breturn 0\s*$", penalty_body):
        failures.append("runtime perfect-resource zero penalty missing")

    for resource_percent, expected in expected_penalties.items():
        actual = resource_penalty(resource_percent)
        if actual != expected:
            failures.append(
                f"resource penalty {resource_percent}%: {actual} != {expected}"
            )

    mp40 = weapon_by_id.get("MP40")
    if not mp40:
        failures.append("MP40 definition missing")
    else:
        expected_mp40 = {100: 0, 90: 2, 80: 7, 0: 100}
        for condition, expected in expected_mp40.items():
            score = raw_jam_score(
                mp40.reliability,
                mp40.base_jam,
                condition * 10,
                1000,
                1000,
            )
            actual = display_percent(score)
            if actual != expected:
                failures.append(
                    f"MP40 condition {condition}%: {actual}% != {expected}%"
                )

    extreme_normal = display_percent(raw_jam_score(0, 1000, 800, 1000, 1000))
    if extreme_normal != 7:
        failures.append(
            f"normal-condition extreme after service softener: {extreme_normal}% != 7%"
        )
    extreme_perfect = display_percent(raw_jam_score(0, 1000, 1000, 1000, 1000))
    if extreme_perfect != 5:
        failures.append(
            f"perfect-condition extreme after -5pp softener: {extreme_perfect}% != 5%"
        )

    mosin = weapon_by_id.get("Mosin")
    if not mosin:
        failures.append("Mosin definition missing")
    else:
        mosin_base = display_percent(
            raw_jam_score(
                mosin.reliability,
                mosin.base_jam,
                3280,
                6507,
                7000,
            )
        )
        mosin_capped = display_percent(
            raw_jam_score(0, 1000, 3280, 6507, 7000)
        )
        mosin_mid = display_percent(
            raw_jam_score(
                mosin.reliability,
                mosin.base_jam,
                3080,
                4830,
                7000,
            )
        )
        if mosin_base != 8:
            failures.append(f"Mosin 3280/6507/7000 base: {mosin_base}% != 8%")
        if mosin_capped != 17:
            failures.append(
                f"Mosin 3280/6507/7000 capped base: {mosin_capped}% != 17%"
            )
        if mosin_mid != 8:
            failures.append(f"Mosin 3080/4830/7000 base: {mosin_mid}% != 8%")

    if base_jam_score(50, -30) != 20:
        failures.append("negative BaseJamChance no longer reduces reliability risk")
    if base_jam_score(90, 30) != 10:
        failures.append(
            "Rel90 BaseJam30 should stay on reliability_score after ammo scaling"
        )
    if base_jam_score(95, 1000) != 0:
        failures.append("Rel95 must zero base jam even with extreme BaseJamChance")
    if base_jam_score(50, 30) != 50:
        failures.append("MP40 Rel50 BaseJam30 base score drifted from 50")
    if display_percent(raw_jam_score(95, 1000, 1000, 1000, 1000)) != 0:
        failures.append("Rel95 + extreme ammo still jams at perfect resource")

    for weapon in weapons:
        for cartridge in ammo:
            if weapon.caliber != cartridge.caliber:
                continue
            reliability = weapon.reliability + cartridge.reliability_add
            base_jam = weapon.base_jam + cartridge.base_jam_add
            loaded = display_percent(
                raw_jam_score(reliability, base_jam, 1000, 1000, 1000)
            )
            rows.append((
                loaded,
                weapon.item_id,
                cartridge.item_id,
                reliability,
                base_jam,
                base_jam_score(reliability, base_jam),
            ))
            if loaded > 5:
                failures.append(
                    f"{weapon.item_id} + {cartridge.item_id}: "
                    f"perfect resource {loaded}% > 5%"
                )

    print(f"weapons={len(weapons)} degraded_ammo={len(ammo)} pairs={len(rows)}")
    print("loaded reliability base_jam base_score weapon + ammo")
    for loaded, weapon_id, ammo_id, reliability, base_jam, score in sorted(
        rows, reverse=True
    )[:args.top]:
        print(
            f"{loaded:>3}% rel={reliability:>3} jam={base_jam:>4} "
            f"score={score:>3} {weapon_id} + {ammo_id}"
        )

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
