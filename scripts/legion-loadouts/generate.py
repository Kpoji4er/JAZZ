#!/usr/bin/env python3
"""JAZZ-UNITS-003: recipes + catalogs -> Legion LootDef patches in jazz-units/items.lua."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # jazz/
DATA = Path(__file__).resolve().parent / "data"
UNITS = ROOT.parent / "jazz-units"
ITEMS = UNITS / "items.lua"
WEAPONS_CSV = ROOT / "docs/technical/weapons/data/weapons.csv"
COMP_CSV = ROOT / "docs/technical/weapons/data/weapon-component-options.csv"
PRICES_LUA = ROOT / "Code/LegionUnitPrices.lua"

CLASS_TO_TAG = {
    "Pistol": ["pistol", "sidearm"],
    "Autopistol": ["pistol", "smg", "sidearm"],
    "Revolver": ["pistol", "revolver", "sidearm"],
    "SubmachineGun": ["smg"],
    "Carbine": ["carbine"],
    "AssaultRifle": ["assault"],
    "BattleRifle": ["battle", "rifle"],
    "SniperRifle": ["sniper", "rifle"],
    "Shotgun": ["shotgun"],
    "LightMachineGun": ["lmg", "mg"],
    "MachineGun": ["mg"],
}

KEYWORD_MATCH = {
    "reflex": lambda c: "Reflex" in c or "Aimpoint" in c or "Eotech" in c or "Open" in c,
    "scope_2x": lambda c: "2x" in c or "CombatScope_2x" in c,
    "scope_4x": lambda c: "ACOG" in c or "4x" in c,
    "scope_6x": lambda c: "Scope_6x" in c or "1-6" in c,
    "scope_12x": lambda c: "12x" in c or "Scope_12x" in c,
    "mag_large": lambda c: "MagLarge" in c or "Large" in c and "Mag" in c,
    "mag_normal": lambda c: c == "MagNormal" or c.startswith("MagNormal"),
    "mag_drum": lambda c: "Drum" in c,
    "laser": lambda c: "Laser" in c,
    "suppressor": lambda c: "Suppressor" in c or "Silencer" in c,
    "compensator": lambda c: "Compensator" in c,
    "bipod": lambda c: "Bipod" in c,
    "stock": lambda c: "Stock" in c,
}

ARMOR = {
    "Light": ("LegionTorsoLightArmor", "LegionLegsLightArmor", "LegionHelmetsLightArmor"),
    "Middle": ("LegionTorsoMiddleArmor", "LegionLegsMiddleArmor", "LegionHelmetsMiddleArmor"),
    "Heavy": ("LegionTorsoHeavyArmor", "LegionLegsHeavyArmor", "LegionHelmetsHeavyArmor"),
}

NIGHT_CHANCE = [45, 55, 65]
NIGHT_STACK = [(3, 6), (4, 8), (5, 10)]
FLARE_BUMP = [1.0, 1.15, 1.3]

MARKER_BEGIN = "--[[ JAZZ-UNITS-003-GENERATED-BEGIN ]]"
MARKER_END = "--[[ JAZZ-UNITS-003-GENERATED-END ]]"


def load_json(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def parse_prices() -> dict[str, int]:
    text = PRICES_LUA.read_text(encoding="utf-8")
    return {m.group(1): int(m.group(2)) for m in re.finditer(r"(JAZZ_Legion_\w+)\s*=\s*(\d+)", text)}


def inventory_class_id(csv_id: str, source_file: str | None) -> str:
    """CSV id may be a docs slug (Mas36); loot/weapon fields need DefineClass id (MAS36)."""
    rel = (source_file or "").strip() or f"InventoryItem/{csv_id}.lua"
    path = ROOT / rel
    if path.is_file():
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"UndefineClass\('([^']+)'\)", text)
        if m:
            return m.group(1)
        m = re.search(r"DefineClass\.([A-Za-z0-9_]+)", text)
        if m:
            return m.group(1)
    return csv_id


def load_weapons(overrides: dict):
    rows = []
    with WEAPONS_CSV.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r.get("catalog_status") == "excluded_disabled":
                continue
            if not (r.get("balance_tier") or "").isdigit():
                continue
            sub_raw = (r.get("balance_subtier") or "1").strip()
            if not sub_raw.isdigit():
                continue  # skip UNIQ / non-ladder weapons from tiered pools
            tags = list(CLASS_TO_TAG.get(r["object_class"], []))
            tags += overrides.get(r["id"], [])
            class_id = inventory_class_id(r["id"], r.get("source_file"))
            rows.append(
                {
                    "id": r["id"],
                    "class_id": class_id,
                    "object_class": r["object_class"],
                    "caliber": r["caliber"],
                    "balance_tier": int(r["balance_tier"]),
                    "balance_subtier": int(sub_raw),
                    "tier_label": r["tier_label"],
                    "tags": set(tags),
                }
            )
    return rows


def load_components():
    by_weapon = defaultdict(lambda: defaultdict(list))
    with COMP_CSV.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            by_weapon[r["weapon_id"]][r["slot_type"]].append(r["component_id"])
    return by_weapon


def resolve_package(weapon_id: str, package: dict, comps) -> list[str]:
    upgrades = []
    slots = comps.get(weapon_id, {})
    for slot, keywords in (package.get("keywords") or {}).items():
        options = slots.get(slot, [])
        if not options:
            continue
        picked = None
        for kw in keywords:
            fn = KEYWORD_MATCH.get(kw)
            if not fn:
                continue
            for c in options:
                if fn(c):
                    picked = c
                    break
            if picked:
                break
        if picked:
            upgrades.append(picked)
    return upgrades


def indent(n: int) -> str:
    return "\t" * n


def quest_ge(amount: int, level: int = 8) -> str:
    pad = indent(level)
    return (
        f"{pad}game_conditions = {{\n"
        f"{pad}\tPlaceObj('QuestIsVariableNum', {{\n"
        f"{pad}\t\tAmount = {amount},\n"
        f"{pad}\t\tProp = \"JAZZ_Legion_Tier\",\n"
        f"{pad}\t\tQuestId = \"JAZZ_LegionTier\",\n"
        f"{pad}\t}}),\n"
        f"{pad}}},\n"
    )


def quest_ge_le(amount: int, upper: int, level: int = 8) -> str:
    pad = indent(level)
    return (
        f"{pad}game_conditions = {{\n"
        f"{pad}\tPlaceObj('QuestIsVariableNum', {{\n"
        f"{pad}\t\tAmount = {amount},\n"
        f"{pad}\t\tProp = \"JAZZ_Legion_Tier\",\n"
        f"{pad}\t\tQuestId = \"JAZZ_LegionTier\",\n"
        f"{pad}\t}}),\n"
        f"{pad}\tPlaceObj('QuestIsVariableNum', {{\n"
        f"{pad}\t\tAmount = {upper},\n"
        f"{pad}\t\tCondition = \"<=\",\n"
        f"{pad}\t\tProp = \"JAZZ_Legion_Tier\",\n"
        f"{pad}\t\tQuestId = \"JAZZ_LegionTier\",\n"
        f"{pad}\t}}),\n"
        f"{pad}}},\n"
    )


def quest_arch_band(arch: int, level: int = 7, unlock_floor: int | None = None) -> str:
    """Exclusive loot-tier band for arch: 1→[11,19], 2→[21,29], 3→[31,+∞)."""
    lo = 10 * arch + 1
    if unlock_floor is not None:
        lo = max(lo, unlock_floor)
    if arch >= 3:
        return quest_ge(lo, level)
    hi = 10 * arch + 9  # 19 / 29
    return quest_ge_le(lo, hi, level)


def night_cond(level: int = 8) -> str:
    pad = indent(level)
    return (
        f"{pad}game_conditions = {{\n"
        f"{pad}\tPlaceObj('IsTimeOfDay', {{\n"
        f"{pad}\t\tTimeOfDay = \"Night\",\n"
        f"{pad}\t}}),\n"
        f"{pad}}},\n"
    )


def emit_shared(caliber_ammo: dict, weapon_combos: dict[str, str] | None = None) -> str:
    """Shared generated LootDefs used by class inventories."""
    parts = [MARKER_BEGIN, "\t\t\t\t\t-- Shared pools owned by JAZZ-UNITS-003 generator"]
    # Night lights — exclusive arch bands + night TOD
    night_entries = []
    for arch_i, (chance, (smin, smax)) in enumerate(zip(NIGHT_CHANCE, NIGHT_STACK), start=1):
        lo = 10 * arch_i + 1
        hi = 10 * arch_i + 9
        for item in ("GlowStick", "FlareStick"):
            conds = [
                "\t\t\t\t\t\t\tgame_conditions = {",
                "\t\t\t\t\t\t\t\tPlaceObj('IsTimeOfDay', {",
                "\t\t\t\t\t\t\t\t\tTimeOfDay = \"Night\",",
                "\t\t\t\t\t\t\t\t}),",
                "\t\t\t\t\t\t\t\tPlaceObj('QuestIsVariableNum', {",
                f"\t\t\t\t\t\t\t\t\tAmount = {lo},",
                "\t\t\t\t\t\t\t\t\tProp = \"JAZZ_Legion_Tier\",",
                "\t\t\t\t\t\t\t\t\tQuestId = \"JAZZ_LegionTier\",",
                "\t\t\t\t\t\t\t\t}),",
            ]
            if arch_i < 3:
                conds += [
                    "\t\t\t\t\t\t\t\tPlaceObj('QuestIsVariableNum', {",
                    f"\t\t\t\t\t\t\t\t\tAmount = {hi},",
                    "\t\t\t\t\t\t\t\t\tCondition = \"<=\",",
                    "\t\t\t\t\t\t\t\t\tProp = \"JAZZ_Legion_Tier\",",
                    "\t\t\t\t\t\t\t\t\tQuestId = \"JAZZ_LegionTier\",",
                    "\t\t\t\t\t\t\t\t}),",
                ]
            conds.append("\t\t\t\t\t\t\t},")
            night_entries.append(
                "\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {\n"
                + "\n".join(conds)
                + "\n"
                + f"\t\t\t\t\t\t\tgenerate_chance = {chance},\n"
                + f"\t\t\t\t\t\t\titem = \"{item}\",\n"
                + f"\t\t\t\t\t\t\tstack_max = {smax},\n"
                + f"\t\t\t\t\t\t\tstack_min = {smin},\n"
                + f"\t\t\t\t\t\t\tweight = {10000 if item == 'FlareStick' else 3000},\n"
                + "\t\t\t\t\t\t}),"
            )
    night_entries.append("\t\t\t\t\t\tPlaceObj('LootEntryNoLoot', {\n\t\t\t\t\t\t\tweight = 5000,\n\t\t\t\t\t\t}),")
    parts.append(
        "\t\t\t\t\tPlaceObj('ModItemLootDef', {\n"
        "\t\t\t\t\t\tComment = \"JAZZ-UNITS-003\",\n"
        "\t\t\t\t\t\tgroup = \"Enemy - Legion\",\n"
        "\t\t\t\t\t\tid = \"JAZZ_Gen_NightEquipment\",\n"
        + "\n".join(night_entries)
        + "\n\t\t\t\t\t}),"
    )

    # Misc
    misc_items = ["JazzArmor_Sunglasses", "GasMask", "JazzArmor_BallisticMask"]
    misc_body = []
    for it in misc_items:
        misc_body.append(
            f"\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {{\n"
            f"\t\t\t\t\t\t\titem = \"{it}\",\n"
            f"\t\t\t\t\t\t\tweight = 1000,\n"
            f"\t\t\t\t\t\t}}),"
        )
    misc_body.append("\t\t\t\t\t\tPlaceObj('LootEntryNoLoot', {\n\t\t\t\t\t\t\tweight = 97000,\n\t\t\t\t\t\t}),")
    parts.append(
        "\t\t\t\t\tPlaceObj('ModItemLootDef', {\n"
        "\t\t\t\t\t\tComment = \"JAZZ-UNITS-003\",\n"
        "\t\t\t\t\t\tgroup = \"Enemy - Legion\",\n"
        "\t\t\t\t\t\tid = \"JAZZ_Gen_MiscGear\",\n"
        + "\n".join(misc_body)
        + "\n\t\t\t\t\t}),"
    )

    # Sidearm shared ladder
    parts.append(
        "\t\t\t\t\tPlaceObj('ModItemLootDef', {\n"
        "\t\t\t\t\t\tComment = \"JAZZ-UNITS-003\",\n"
        "\t\t\t\t\t\tgroup = \"Enemy - Legion\",\n"
        "\t\t\t\t\t\tid = \"JAZZ_Gen_Sidearm\",\n"
        "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
        "\t\t\t\t\t\t\tloot_def = \"LegionT1_PistolList\",\n"
        "\t\t\t\t\t\t\tweight = 10000,\n"
        "\t\t\t\t\t\t}),\n"
        "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
        f"{quest_ge(20, 7)}"
        "\t\t\t\t\t\t\tloot_def = \"LegionT2_PistolList\",\n"
        "\t\t\t\t\t\t\tweight = 100000,\n"
        "\t\t\t\t\t\t}),\n"
        "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
        f"{quest_ge(30, 7)}"
        "\t\t\t\t\t\t\tloot_def = \"LegionT3_PistolList\",\n"
        "\t\t\t\t\t\t\tweight = 1000000,\n"
        "\t\t\t\t\t\t}),\n"
        "\t\t\t\t\t}),"
    )

    # Flaregun
    parts.append(
        "\t\t\t\t\tPlaceObj('ModItemLootDef', {\n"
        "\t\t\t\t\t\tComment = \"JAZZ-UNITS-003\",\n"
        "\t\t\t\t\t\tgroup = \"Enemy - Legion\",\n"
        "\t\t\t\t\t\tid = \"JAZZ_Gen_FlareGun\",\n"
        "\t\t\t\t\t\tloot = \"all\",\n"
        "\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {\n"
        "\t\t\t\t\t\t\titem = \"FlareHandgun\",\n"
        "\t\t\t\t\t\t\tstack_max = 1,\n"
        "\t\t\t\t\t\t\tstack_min = 1,\n"
        "\t\t\t\t\t\t}),\n"
        "\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {\n"
        "\t\t\t\t\t\t\titem = \"FlareAmmo\",\n"
        "\t\t\t\t\t\t\tstack_max = 6,\n"
        "\t\t\t\t\t\t\tstack_min = 2,\n"
        "\t\t\t\t\t\t}),\n"
        "\t\t\t\t\t}),"
    )

    # Valuables by price bands (no DiamondBriefcase)
    for band, pmin, pmax, drop, tiny_min, tiny_max in [
        ("Low", 0, 600, 35, 1, 1),
        ("Mid", 601, 1600, 45, 1, 3),
        ("High", 1601, 3000, 55, 3, 7),
        ("Elite", 3001, 99999, 65, 4, 10),
    ]:
        parts.append(
            "\t\t\t\t\tPlaceObj('ModItemLootDef', {\n"
            "\t\t\t\t\t\tComment = \"JAZZ-UNITS-003 unit_price pocket\",\n"
            "\t\t\t\t\t\tgroup = \"Enemy - Legion\",\n"
            f"\t\t\t\t\t\tid = \"JAZZ_Gen_Valuables_{band}\",\n"
            "\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {\n"
            f"\t\t\t\t\t\t\tgenerate_chance = {drop},\n"
            "\t\t\t\t\t\t\titem = \"TinyDiamonds\",\n"
            f"\t\t\t\t\t\t\tstack_max = {tiny_max},\n"
            f"\t\t\t\t\t\t\tstack_min = {tiny_min},\n"
            "\t\t\t\t\t\t\tweight = 10000,\n"
            "\t\t\t\t\t\t}),\n"
            + (
                "\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {\n"
                f"\t\t\t\t\t\t\tgenerate_chance = {max(5, drop // 5)},\n"
                "\t\t\t\t\t\t\titem = \"BigDiamond\",\n"
                "\t\t\t\t\t\t\tstack_max = 1,\n"
                "\t\t\t\t\t\t\tstack_min = 1,\n"
                "\t\t\t\t\t\t\tweight = 2000,\n"
                "\t\t\t\t\t\t}),\n"
                if band == "Elite"
                else ""
            )
            + "\t\t\t\t\t\tPlaceObj('LootEntryNoLoot', {\n"
            f"\t\t\t\t\t\t\tweight = {100000 - drop * 100},\n"
            "\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t}),"
        )

    if weapon_combos:
        parts.append("\t\t\t\t\t-- Weapon+ammo combo defs")
        for cid in sorted(weapon_combos):
            parts.append(weapon_combos[cid])

    parts.append(MARKER_END)
    return "\n".join(parts)


def valuables_band(price: int) -> str:
    if price <= 600:
        return "Low"
    if price <= 1600:
        return "Mid"
    if price <= 3000:
        return "High"
    return "Elite"


def tags_for_recipe(recipe: dict, arch: int) -> set[str]:
    tags = set(recipe.get("primary_tags") or [])
    if arch >= 2 and recipe.get("arch2_extra_tags"):
        tags |= set(recipe["arch2_extra_tags"])
    if arch >= 3 and recipe.get("arch3_extra_tags"):
        tags |= set(recipe["arch3_extra_tags"])
    return tags


def parse_tier_label(label: str) -> tuple[int, int]:
    major_s, _, sub_s = str(label).partition("-")
    return int(major_s), int(sub_s or "1")


def weapon_excluded_by_recipe(w: dict, recipe: dict | None) -> bool:
    """Optional recipe filters: exclude_tags, primary_max_tier_label (SMG class only)."""
    if not recipe:
        return False
    exclude = set(recipe.get("exclude_tags") or [])
    if exclude and (w["tags"] & exclude):
        return True
    cap = recipe.get("primary_max_tier_label")
    if cap and w.get("object_class") == "SubmachineGun":
        c_maj, c_sub = parse_tier_label(cap)
        bt, bs = w["balance_tier"], w["balance_subtier"]
        if bt > c_maj or (bt == c_maj and bs > c_sub):
            return True
    return False


def weapon_weight(w: dict, arch: int, recipe: dict | None = None) -> tuple[int, int] | None:
    """Return (min_tier_amount, weight) or None if excluded."""
    if weapon_excluded_by_recipe(w, recipe):
        return None
    bt = w["balance_tier"]
    if bt == arch:
        # prefer matching sub mid-high
        amin = 10 * arch + min(w["balance_subtier"], 5)
        # Optional: commanders unlock all arch1 subs from day-one quest tier
        # (e.g. MPL 1-3 at Amount=11 instead of waiting for 13).
        floor = (recipe or {}).get("arch1_all_subs_from") if arch == 1 else None
        if floor is not None:
            amin = min(amin, int(floor))
        return amin, 100000 + w["balance_subtier"] * 1000
    if bt == arch - 1 and arch == 2:
        # ~1% remnant of tier1 on arch2 (tuned vs mid pool; evidence AC-004)
        return 20, 1400
    if bt < arch - 1:
        return None
    if bt > arch:
        return None
    return None


# Weapon-pool LootDef ids must never appear as ammo in weapon+ammo combos
# (loot="all" would spawn a second firearm — Crusher dual-shotgun bug).
AMMO_LOOT_DENYLIST = re.compile(
    r"^LegionT[123]_(Shotgun|Rifle|SMG|Assault|PistolList|OneHSMG|Revolver|AutoPistol)$"
)


def ammo_loot_id(weapon: dict, caliber_ammo: dict, recipe: dict, arch: int) -> str | None:
    cal = weapon["caliber"]
    mapping = caliber_ammo.get(cal) or caliber_ammo.get(cal.replace("JAZZ_Caliber_", "")) or {}
    use_ap = arch >= 2 and recipe.get("ammo_cap") in ("Army", "AP", "Match", "EPR")
    if arch >= 3 and recipe.get("ammo_cap") in ("AP", "Match"):
        use_ap = True
    if "sniper" in weapon["tags"] and mapping.get("sniper"):
        return mapping["sniper"]
    if "mg" in weapon["tags"] and mapping.get("mg"):
        return mapping["mg"]
    if "pistol" in weapon["tags"] and "smg" not in weapon["tags"]:
        if use_ap and mapping.get("pistol_ap"):
            return mapping["pistol_ap"]
        if mapping.get("pistol_base"):
            return mapping["pistol_base"]
    if use_ap and mapping.get("ap"):
        return mapping["ap"]
    return mapping.get("base")


def validate_caliber_ammo(caliber_ammo: dict) -> None:
    bad = []
    for cal, mapping in caliber_ammo.items():
        for key, loot_id in mapping.items():
            if loot_id and AMMO_LOOT_DENYLIST.match(str(loot_id)):
                bad.append(f"{cal}.{key}={loot_id}")
    if bad:
        raise SystemExit(
            "caliber_ammo.json maps to weapon pools (not ammo): " + "; ".join(bad)
        )


def combo_id(weapon_id: str, pkg_name: str, ammo: str | None) -> str:
    safe_pkg = re.sub(r"[^A-Za-z0-9_]", "_", pkg_name)
    safe_ammo = re.sub(r"[^A-Za-z0-9_]", "_", ammo or "noammo")
    return f"JAZZ_GenW_{weapon_id}_{safe_pkg}_{safe_ammo}"


def emit_weapon_combo(
    combo_loot_id: str,
    weapon_id: str,
    upgrades: list[str],
    ammo: str | None,
    class_id: str | None = None,
) -> str:
    inv_id = class_id or weapon_id
    lines = [
        "\t\t\t\t\tPlaceObj('ModItemLootDef', {",
        "\t\t\t\t\t\tComment = \"JAZZ-UNITS-003 weapon+ammo\",",
        "\t\t\t\t\t\tgroup = \"Enemy - Legion\",",
        f"\t\t\t\t\t\tid = \"{combo_loot_id}\",",
        "\t\t\t\t\t\tloot = \"all\",",
    ]
    if upgrades:
        lines += [
            "\t\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {",
            "\t\t\t\t\t\t\tupgrades = {",
            *[f"\t\t\t\t\t\t\t\t\"{u}\"," for u in upgrades],
            "\t\t\t\t\t\t\t},",
            f"\t\t\t\t\t\t\tweapon = \"{inv_id}\",",
            "\t\t\t\t\t\t}),",
        ]
    else:
        lines += [
            "\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {",
            f"\t\t\t\t\t\t\titem = \"{inv_id}\",",
            "\t\t\t\t\t\t\tstack_max = 1,",
            "\t\t\t\t\t\t\tstack_min = 1,",
            "\t\t\t\t\t\t}),",
        ]
    if ammo:
        lines += [
            "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {",
            f"\t\t\t\t\t\t\tloot_def = \"{ammo}\",",
            "\t\t\t\t\t\t}),",
        ]
    lines.append("\t\t\t\t\t}),")
    return "\n".join(lines)


def collect_firearm_plan(
    recipe: dict,
    weapons: list,
    packages: dict,
    comps,
    caliber_ammo: dict,
) -> tuple[list[tuple], dict[str, str]]:
    """Return (firearm entries meta, combo_id -> combo block text)."""
    entries_meta = []
    combos: dict[str, str] = {}
    weapons_by_id = {w["id"]: w for w in weapons}

    def append_entry(w: dict, arch: int, amin: int, weight: int) -> None:
        pkg_name = (recipe.get("packages_by_arch") or ["m0", "m0", "m0"])[arch - 1]
        package = packages.get(pkg_name) or packages["m0"]
        upgrades = resolve_package(w["id"], package, comps) if package.get("keywords") else []
        ammo = ammo_loot_id(w, caliber_ammo, recipe, arch)
        cid = combo_id(w["id"], pkg_name, ammo)
        if cid not in combos:
            combos[cid] = emit_weapon_combo(
                cid, w["id"], upgrades, ammo, class_id=w.get("class_id")
            )
        # Exclusive arch bands: arch1 ≤19, arch2 ≤29, arch3 open.
        # Remnant tier1 on arch2 already uses amin=20 weight≈1%.
        if arch == 2 and w["balance_tier"] == 1:
            upper = 29
        elif arch >= 3:
            upper = None
        else:
            upper = 10 * arch + 9  # 19 / 29
        entries_meta.append((cid, amin, upper, weight))

    for arch in (1, 2, 3):
        tags = tags_for_recipe(recipe, arch)
        candidates = [w for w in weapons if w["tags"] & tags]
        for w in candidates:
            gate = weapon_weight(w, arch, recipe)
            if not gate:
                continue
            amin, weight = gate
            append_entry(w, arch, amin, weight)

    # Optional: pull named higher-ladder guns into the arch1 band at a gated Amount
    # (e.g. M45@11, MAC10@12 / T1-2, UZI/Agram@13). Explicit IDs bypass exclude_tags
    # (Sergeant pistol filter) but still respect primary_max_tier_label for SMGs.
    early = recipe.get("arch1_early_ids") or {}
    if early:
        pkg_arch = 1
        early_recipe = {**recipe, "exclude_tags": []}
        for wid, unlock in early.items():
            w = weapons_by_id.get(wid)
            if not w or weapon_excluded_by_recipe(w, early_recipe):
                continue
            tags = tags_for_recipe(recipe, pkg_arch)
            if not (w["tags"] & tags):
                continue
            amin = int(unlock)
            weight = 100000 + w["balance_subtier"] * 1000
            append_entry(w, pkg_arch, amin, weight)

    return entries_meta, combos


def emit_firearm_from_plan(fid: str, entries_meta: list[tuple]) -> str:
    entries = []
    for cid, amin, upper, weight in entries_meta:
        cond = quest_ge_le(amin, upper, 7) if upper is not None else quest_ge(amin, 7)
        entries.append(
            "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
            f"{cond}"
            f"\t\t\t\t\t\t\tloot_def = \"{cid}\",\n"
            f"\t\t\t\t\t\t\tweight = {weight},\n"
            "\t\t\t\t\t\t}),"
        )
    # Unconditional fallback (pre-003 LegionT1_* style): if quest var missing/0 or no band
    # matches, still roll a weapon. Low weight vs gated pools when they are active.
    fallback_cid = entries_meta[0][0] if entries_meta else "LegionT1_SMG"
    fallback_weight = 1000 if entries_meta else 10000
    entries.append(
        "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
        "\t\t\t\t\t\t\tcomment = \"JAZZ-UNITS-004 unconditional fallback\",\n"
        f"\t\t\t\t\t\t\tloot_def = \"{fallback_cid}\",\n"
        f"\t\t\t\t\t\t\tweight = {fallback_weight},\n"
        "\t\t\t\t\t\t}),"
    )
    return (
        "\t\t\t\t\tPlaceObj('ModItemLootDef', {\n"
        "\t\t\t\t\t\tComment = \"JAZZ-UNITS-003 generated\",\n"
        "\t\t\t\t\t\tgroup = \"Default\",\n"
        f"\t\t\t\t\t\tid = \"{fid}\",\n"
        + "\n".join(entries)
        + "\n\t\t\t\t\t}),"
    )


def emit_inventory(unit_id: str, recipe: dict, prices: dict) -> str:
    inv = recipe["inventory"]
    fir = recipe["firearm"]
    lines = [
        "\t\t\t\t\tPlaceObj('ModItemLootDef', {",
        "\t\t\t\t\t\tComment = \"JAZZ-UNITS-003 generated\",",
        "\t\t\t\t\t\tgroup = \"Default\",",
        f"\t\t\t\t\t\tid = \"{inv}\",",
        "\t\t\t\t\t\tloot = \"all\",",
        "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {",
        f"\t\t\t\t\t\t\tloot_def = \"{fir}\",",
        "\t\t\t\t\t\t}),",
    ]
    if recipe.get("keep_existing_heavy"):
        launcher = inv.replace("_Inventory", "_Launcher")
        lines += [
            "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {",
            f"\t\t\t\t\t\t\tloot_def = \"{launcher}\",",
            "\t\t\t\t\t\t}),",
        ]

    side = recipe.get("sidearm")
    if side:
        unlock = int(side.get("unlock") or 11)
        chance = int(side.get("chance") or 50)
        lines.append("\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {")
        lines.append(quest_ge(unlock, 7).rstrip("\n"))
        lines += [
            f"\t\t\t\t\t\t\tgenerate_chance = {chance},",
            "\t\t\t\t\t\t\tloot_def = \"JAZZ_Gen_Sidearm\",",
            "\t\t\t\t\t\t}),",
        ]

    melee = recipe.get("melee")
    if melee:
        item = melee.get("item") or "Weapon_Knife"
        # Prefer common melee ids present in loot; Knife fallbacks
        if item == "Weapon_Knife":
            item = "Knife"
        chances = melee.get("chance_by_arch") or [50, 50, 50]
        for arch_i, ch in enumerate(chances, start=1):
            if ch <= 0:
                continue
            lines.append("\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {")
            lines.append(quest_arch_band(arch_i, 7).rstrip("\n"))
            lines += [
                f"\t\t\t\t\t\t\tgenerate_chance = {ch},",
                f"\t\t\t\t\t\t\titem = \"{item}\",",
                "\t\t\t\t\t\t\tstack_max = 1,",
                "\t\t\t\t\t\t\tstack_min = 1,",
                "\t\t\t\t\t\t}),",
            ]

    util = recipe.get("utility") or {}
    he = util.get("he") or {}
    if he.get("mode") == "guaranteed":
        counts = he.get("count_by_arch") or [3, 4, 5]
        for arch_i, cnt in enumerate(counts, start=1):
            lines.append("\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {")
            lines.append(quest_arch_band(arch_i, 7).rstrip("\n"))
            lines += [
                "\t\t\t\t\t\t\titem = \"FragGrenade\",",
                f"\t\t\t\t\t\t\tstack_max = {cnt},",
                f"\t\t\t\t\t\t\tstack_min = {max(1, cnt - 1)},",
                "\t\t\t\t\t\t}),",
            ]
    elif he.get("mode") == "chance":
        chances = he.get("chance_by_arch") or [10, 25, 40]
        for arch_i, ch in enumerate(chances, start=1):
            if ch <= 0:
                continue
            lines.append("\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {")
            lines.append(quest_arch_band(arch_i, 7).rstrip("\n"))
            lines += [
                f"\t\t\t\t\t\t\tgenerate_chance = {ch},",
                "\t\t\t\t\t\t\titem = \"FragGrenade\",",
                "\t\t\t\t\t\t\tstack_max = 2,",
                "\t\t\t\t\t\t\tstack_min = 1,",
                "\t\t\t\t\t\t}),",
            ]

    pipe = util.get("pipe")
    if pipe:
        unlock = int(pipe.get("unlock") or 21)
        chances = pipe.get("chance_by_arch") or [0, 20, 28]
        for arch_i, ch in enumerate(chances, start=1):
            if ch <= 0:
                continue
            lines.append("\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {")
            lines.append(quest_arch_band(arch_i, 7, unlock_floor=unlock).rstrip("\n"))
            lines += [
                f"\t\t\t\t\t\t\tgenerate_chance = {ch},",
                "\t\t\t\t\t\t\titem = \"PipeBomb\",",
                "\t\t\t\t\t\t\tstack_max = 1,",
                "\t\t\t\t\t\t\tstack_min = 1,",
                "\t\t\t\t\t\t}),",
            ]

    if util.get("molotov_guaranteed"):
        n = int(util["molotov_guaranteed"])
        lines += [
            "\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {",
            "\t\t\t\t\t\t\titem = \"Molotov\",",
            f"\t\t\t\t\t\t\tstack_max = {n},",
            f"\t\t\t\t\t\t\tstack_min = {n},",
            "\t\t\t\t\t\t}),",
        ]
    if util.get("molotov_chance"):
        lines += [
            "\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {",
            f"\t\t\t\t\t\t\tgenerate_chance = {int(util['molotov_chance'])},",
            "\t\t\t\t\t\t\titem = \"Molotov\",",
            "\t\t\t\t\t\t\tstack_max = 2,",
            "\t\t\t\t\t\t\tstack_min = 1,",
            "\t\t\t\t\t\t}),",
        ]
    if util.get("smoke_chance"):
        lines += [
            "\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {",
            f"\t\t\t\t\t\t\tgenerate_chance = {int(util['smoke_chance'])},",
            "\t\t\t\t\t\t\titem = \"SmokeGrenade\",",
            "\t\t\t\t\t\t}),",
        ]
    if util.get("conc_chance"):
        lines += [
            "\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {",
            f"\t\t\t\t\t\t\tgenerate_chance = {int(util['conc_chance'])},",
            "\t\t\t\t\t\t\titem = \"ConcussiveGrenade\",",
            "\t\t\t\t\t\t}),",
        ]
    if util.get("medkit"):
        lines += [
            "\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {",
            "\t\t\t\t\t\t\titem = \"Medkit\",",
            "\t\t\t\t\t\t\tstack_max = 1,",
            "\t\t\t\t\t\t\tstack_min = 1,",
            "\t\t\t\t\t\t}),",
        ]

    # Pre-003 frontliner secondary launcher roll (M79 / ChinaLake / M72 LAW).
    # LootDef LegionGL_5pc embeds ~15% weight vs NoLoot despite the "5pc" name.
    if util.get("gl_5pc"):
        lines += [
            "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {",
            "\t\t\t\t\t\t\tloot_def = \"LegionGL_5pc\",",
            "\t\t\t\t\t\t}),",
        ]

    lines += [
        "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {",
        "\t\t\t\t\t\t\tloot_def = \"JAZZ_Gen_NightEquipment\",",
        "\t\t\t\t\t\t}),",
    ]

    flare = int(recipe.get("flaregun") or 0)
    if flare > 0:
        for arch_i, bump in enumerate(FLARE_BUMP, start=1):
            ch = min(35, int(round(flare * bump)))
            lines.append("\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {")
            lines.append(quest_arch_band(arch_i, 7).rstrip("\n"))
            lines += [
                f"\t\t\t\t\t\t\tgenerate_chance = {ch},",
                "\t\t\t\t\t\t\tloot_def = \"JAZZ_Gen_FlareGun\",",
                "\t\t\t\t\t\t}),",
            ]

    misc = int(recipe.get("misc_chance") or 0)
    if misc > 0:
        lines += [
            "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {",
            f"\t\t\t\t\t\t\tgenerate_chance = {misc},",
            "\t\t\t\t\t\t\tloot_def = \"JAZZ_Gen_MiscGear\",",
            "\t\t\t\t\t\t}),",
        ]

    price = prices.get(unit_id, 500)
    band = valuables_band(price)
    val = recipe.get("valuables")
    if val not in (None, False, "none", "None"):
        # L19: pocket valuables for combat; logistics cargo is Global AI (no class DiamondBriefcase)
        lines += [
            "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {",
            f"\t\t\t\t\t\t\tloot_def = \"JAZZ_Gen_Valuables_{band}\",",
            "\t\t\t\t\t\t}),",
        ]

    torso, legs, helm = ARMOR[recipe.get("armor") or "Middle"]
    for a in (torso, legs, helm):
        lines += [
            "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {",
            f"\t\t\t\t\t\t\tloot_def = \"{a}\",",
            "\t\t\t\t\t\t}),",
        ]

    lines.append("\t\t\t\t\t}),")
    return "\n".join(lines)


def find_moditem_block(text: str, loot_id: str) -> tuple[int, int] | None:
    """Return [start, end) of PlaceObj('ModItemLootDef'... id=loot_id ...)."""
    needle = f'id = "{loot_id}"'
    pos = 0
    while True:
        i = text.find(needle, pos)
        if i < 0:
            return None
        # walk back to PlaceObj('ModItemLootDef'
        start = text.rfind("PlaceObj('ModItemLootDef'", 0, i)
        if start < 0:
            pos = i + 1
            continue
        # ensure no other id between start and needle
        chunk = text[start:i]
        if chunk.count("PlaceObj('ModItemLootDef'") != 1:
            pos = i + 1
            continue
        # brace match from first { after PlaceObj
        brace = text.find("{", start)
        depth = 0
        j = brace
        while j < len(text):
            c = text[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    end = j + 1
                    # ModItemLootDef closes as `}),` — consume PlaceObj `)` and optional `,`.
                    # Old code only ate `,` after `}`, leaving `),` tails; re-runs stacked
                    # `}),),),),` and broke the whole items.lua parse (all inventories).
                    if end < len(text) and text[end] == ")":
                        end += 1
                    if end < len(text) and text[end] == ",":
                        end += 1
                    return start, end
            j += 1
        return None


def replace_or_warn(text: str, loot_id: str, new_block: str) -> tuple[str, bool]:
    found = find_moditem_block(text, loot_id)
    if not found:
        print(f"WARN: missing ModItemLootDef id={loot_id}", file=sys.stderr)
        return text, False
    s, e = found
    return text[:s] + new_block + text[e:], True


def inject_shared(text: str, shared: str) -> str:
    if MARKER_BEGIN in text:
        s = text.find(MARKER_BEGIN)
        e = text.find(MARKER_END)
        if e < 0:
            raise SystemExit("broken generated markers")
        e = text.find("\n", e) + 1
        return text[:s] + shared + "\n" + text[e:]
    # insert before first Roughneck_Inventory
    found = find_moditem_block(text, "Roughneck_Inventory")
    if not found:
        raise SystemExit("cannot find Roughneck_Inventory to insert shared pools")
    s, _ = found
    return text[:s] + shared + "\n\t\t\t\t\t" + text[s:]


def validate_upgrades(text: str, comps) -> list[str]:
    errors = []
    for m in re.finditer(
        r"PlaceObj\('LootEntryUpgradedWeapon',\s*\{(.*?)\}\s*\),",
        text,
        re.S,
    ):
        block = m.group(1)
        if "JAZZ-UNITS-003" not in text[max(0, m.start() - 500) : m.start()]:
            # only check nearby generated - skip for speed; check if weapon in block
            pass
        wm = re.search(r'weapon\s*=\s*"([^"]+)"', block)
        if not wm:
            continue
        wid = wm.group(1)
        ups = re.findall(r'"([^"]+)"', re.search(r"upgrades\s*=\s*\{(.*?)\}", block, re.S).group(1)) if re.search(r"upgrades\s*=\s*\{(.*?)\}", block, re.S) else []
        allowed = {c for slots in comps.get(wid, {}).values() for c in slots}
        for u in ups:
            if u not in allowed:
                errors.append(f"{wid}: upgrade {u} not in component options")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true", help="Only Roughneck/ShockTrooper/Sniper")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--validate-only", action="store_true")
    args = ap.parse_args()

    recipes = load_json("recipes.json")
    packages = load_json("packages.json")
    caliber_ammo = load_json("caliber_ammo.json")
    validate_caliber_ammo(caliber_ammo)
    overrides = load_json("weapon_tag_overrides.json")
    weapons = load_weapons(overrides)
    comps = load_components()
    prices = parse_prices()

    pilot_ids = {
        "JAZZ_Legion_AssaultT1_Roughneck",
        "JAZZ_Legion_AssaultT2_ShockTrooper",
        "JAZZ_Legion_FrontT3_Sniper",
    }
    selected = {k: v for k, v in recipes.items() if (k in pilot_ids if args.pilot else True)}

    all_combos: dict[str, str] = {}
    plans: dict[str, list] = {}
    for unit_id, recipe in selected.items():
        meta, combos = collect_firearm_plan(recipe, weapons, packages, comps, caliber_ammo)
        plans[unit_id] = meta
        all_combos.update(combos)
        print(f"plan {unit_id}: {len(meta)} firearm entries, {len(combos)} combos")

    text = ITEMS.read_text(encoding="utf-8")
    shared = emit_shared(caliber_ammo, all_combos)
    text = inject_shared(text, shared)

    ok = 0
    for unit_id, recipe in selected.items():
        fir = emit_firearm_from_plan(recipe["firearm"], plans[unit_id])
        inv = emit_inventory(unit_id, recipe, prices)
        text, a = replace_or_warn(text, recipe["firearm"], fir)
        text, b = replace_or_warn(text, recipe["inventory"], inv)
        if a and b:
            ok += 1
            print(f"OK {unit_id}")
        else:
            print(f"FAIL {unit_id}")

    if "DiamondBriefcase" in shared:
        raise SystemExit("AC-006: DiamondBriefcase must not be emitted")

    # AC-003: upgrades only from component options (check combo blocks)
    upgrade_errs = []
    for cid, block in all_combos.items():
        wm = re.search(r'weapon\s*=\s*"([^"]+)"', block)
        if not wm:
            # bare InventoryItem — no upgrades
            continue
        wid = wm.group(1)
        um = re.search(r"upgrades\s*=\s*\{(.*?)\}", block, re.S)
        ups = re.findall(r'"([^"]+)"', um.group(1)) if um else []
        allowed = {c for slots in comps.get(wid, {}).values() for c in slots}
        for u in ups:
            if u not in allowed:
                upgrade_errs.append(f"{cid}: {wid} upgrade {u} not in options")
    if upgrade_errs:
        print("AC-003 FAIL:", *upgrade_errs[:20], sep="\n  ", file=sys.stderr)
        raise SystemExit(f"AC-003: {len(upgrade_errs)} illegal upgrades")

    # AC-004 sample: no tier1 remnant without upper bound in arch2 remnant entries
    for unit_id, meta in plans.items():
        for cid, amin, upper, weight in meta:
            if amin >= 30 and "tier1" in cid.lower():
                pass
            # remnant entries must have upper
            # detect by weight==1000 and amin==20 from weapon_weight
            if weight == 1400 and amin == 20 and upper is None:
                raise SystemExit(f"AC-004: remnant without upper bound in {unit_id} {cid}")

    if args.dry_run or args.validate_only:
        print(f"dry-run complete, would patch {ok}/{len(selected)}; combos={len(all_combos)}")
        return

    ITEMS.write_text(text, encoding="utf-8")
    print(f"Patched {ITEMS} ({ok}/{len(selected)} classes, {len(all_combos)} weapon combos)")
    print("Run sync audit on jazz-units after review.")


if __name__ == "__main__":
    main()
