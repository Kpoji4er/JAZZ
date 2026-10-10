#!/usr/bin/env python3
"""Put required rails in front of gated loot upgrades.

LootEntryUpgradedWeapon:GenerateLoot calls SetWeaponComponent in list order.
A scope, side device or grip that needs a dovetail, rail, side rail, railed
handguard or conversion is dropped when that mount is not already installed.
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "docs/technical/weapons/data/weapon-component-options.csv"
UNITS = ROOT.parent / "jazz-units" / "items.lua"
MAPS = ROOT.parent / "jazz-maps" / "items.lua"

EASTERN = {
    "JAZZ_Scope_PSO",
    "JAZZ_Reflex_Cobra",
    "JAZZ_Reflex_PKAS",
    "JAZZ_CombatScope_1P29",
    "JAZZ_NightScope_NSPU",
}
IRONS = {
    "JAZZ_CarryHandle_AR15",
    "JAZZ_G36Sight",
    "JAZZ_AUGScope_Default",
    "JAZZ_DefaultIronsight_AR15",
    "JAZZ_BaseIronsight_Anaconda",
}
FAL_TAC = "JAZZ_FNFAL_TacHandguard"
FAL_LONG = {"JAZZ_BarrelLong", "JAZZ_BarrelLongImproved"}
FAL_FOLD = {"JAZZ_StockLightUnFolded", "JAZZ_StockLightFolded"}
RIS = "JAZZ_Handguard_RIS"

# Mirrors JAZZ_RailRules in Code/System_WeaponComponent_Set.lua.
RULES = {
    "AKM": {"dove": "JAZZ_Dovetail_AK", "nato": "JAZZ_Rail_NATO_AK", "scope": "split"},
    "AK74": {"dove": "JAZZ_Dovetail_AK", "scope": "east"},
    "AK74M": {"nato": "JAZZ_Rail_NATO_AK", "factory": True, "scope": "split"},
    "AK105": {"nato": "JAZZ_Rail_NATO_AK", "factory": True, "scope": "split"},
    "AEK971": {"dove": "JAZZ_Dovetail_AK", "nato": "JAZZ_Rail_NATO_AK", "scope": "west"},
    "AKSU": {"dove": "JAZZ_Dovetail_AKSU", "side": "dove"},
    "DragunovSVD": {"dove": "JAZZ_Dovetail_SVD", "nato": "JAZZ_Rail_NATO_SVD", "scope": "split"},
    "AS_Val": {"nato": "JAZZ_Rail_NATO_Val", "factory": True, "scope": "split", "side": "nato"},
    "VSS": {"nato": "JAZZ_Rail_NATO_Val", "factory": True, "scope": "split"},
    "PP19Bizon": {"dove": "JAZZ_Dovetail_AK", "scope": "east"},
    "AR10": {"rail": "JAZZ_Rail_AR", "scope": "rail"},
    "CAR15": {"rail": "JAZZ_Rail_AR", "scope": "rail"},
    "M16A1": {"rail": "JAZZ_Rail_AR", "scope": "rail"},
    "M16A2": {"rail": "JAZZ_Rail_M16A2", "rail2": "JAZZ_Rail_M16A2_Side", "scope": "rail", "side": "rail2"},
    "AUG": {"rail": "JAZZ_Rail_AUG", "rail2": "JAZZ_Rail_AUG_Side", "scope": "rail", "side": "rail2"},
    "FAMAS": {"rail": "JAZZ_Rail_FAMAS", "side": "rail"},
    "FNFAL": {"rail": "JAZZ_Rail_FAL", "scope": "rail", "side": "rail", "grips": "rail", "handguard_satisfies": FAL_TAC},
    "G3A3": {"rail": "JAZZ_Rail_G3", "scope": "rail"},
    "G3A4": {"rail": "JAZZ_Rail_G3", "scope": "rail"},
    "G3SniperV1": {"rail": "JAZZ_Rail_G3", "scope": "rail"},
    "G36": {"rail": "JAZZ_Rail_G36", "scope": "rail", "side": "rail", "grips": "rail"},
    "HK21": {"rail": "JAZZ_Rail_HK21", "scope": "rail", "side": "rail", "grips": "rail"},
    "HK33": {"rail": "JAZZ_Rail_HK33", "scope": "rail"},
    "Galil": {"rail": "JAZZ_Rail_Galil", "scope": "rail", "side": "rail"},
    "M24Sniper": {"rail": "JAZZ_Rail_M24", "scope": "rail", "side": "rail"},
    "Winchester1894": {"rail": "JAZZ_Rail_Winchester", "scope": "rail"},
    "AA12": {"rail": "JAZZ_Rail_AA12", "scope": "rail", "side": "rail"},
    "Ithaca": {"rail": "JAZZ_Rail_Ithaca", "scope": "rail"},
    "R870": {"rail": "JAZZ_Rail_R870", "scope": "rail", "side": "rail"},
    "UMP45": {"rail": "JAZZ_Rail_UMP", "scope": "rail"},
    "MP5K": {"rail": "JAZZ_Rail_MP5K", "scope": "rail"},
    "UZI": {"rail": "JAZZ_Rail_UZI", "scope": "rail"},
    "MicroUZI": {"rail": "JAZZ_Rail_MicroUZI", "scope": "rail", "side": "rail"},
    "M14SAW": {"rail": "JAZZ_Rail_M14", "scope": "rail"},
    "M21": {"rail": "JAZZ_Rail_M21", "scope": "rail", "side": "rail", "grips": "rail"},
    "JAZZ_M14_MkIII": {"rail": "JAZZ_Rail_MkIII", "scope": "rail", "side": "rail", "grips": "rail"},
    "M1A": {"rail": "JAZZ_Rail_M1A", "handguard": "JAZZ_HandguardM1ARail", "scope": "rail", "side": "handguard", "grips": "handguard"},
    "M4Commando": {"rail": "JAZZ_Rail_Commando", "side": "rail", "grips": "rail"},
    "PSG1": {"rail": "JAZZ_Rail_PSG", "side": "rail"},
    "Bereta92": {"rail": "JAZZ_Rail_Beretta", "side": "rail"},
    "CZ52": {"rail": "JAZZ_Rail_PistolUnder", "side": "rail"},
    "MAC1950": {"rail": "JAZZ_Rail_PistolUnder", "side": "rail"},
    "P220": {"rail": "JAZZ_Rail_P220", "scope": "rail", "side": "rail"},
    "ColtAnaconda": {"rail": "JAZZ_Rail_Anaconda", "scope": "rail"},
    "VZ58": {"handguard": RIS, "scope": "handguard", "grips": "handguard"},
    "Mosin": {"conv": "JAZZ_Conversion_Mosin", "conv_scopes": {"JAZZ_Scope_PU"}},
    "SVT40": {"conv": "JAZZ_Conversion_SVT", "conv_scopes": {"JAZZ_Scope_PU"}},
    "G43": {"conv": "JAZZ_Conversion_G43", "conv_scopes": {"JAZZ_Scope_ZF4"}},
    "Springfield": {"conv": "JAZZ_Conversion_Springfield", "conv_scopes": {"JAZZ_Scope_Springfield"}},
    "Gewehr98": {"conv": "JAZZ_Conversion_Gewehr", "conv_any": True},
    "STG44": {"conv": "JAZZ_Conversion_STG", "conv_scopes": {"JAZZ_Scope_ZF4"}},
    "M1Garand": {"conv": "JAZZ_Conversion_Garand", "conv_scopes": {"JAZZ_Reflex_Garand", "JAZZ_Scope_Garand"}},
}

BLOCK = re.compile(
    r"PlaceObj\('LootEntryUpgradedWeapon',\s*\{(?P<body>.*?)\n(?P<indent>[ \t]*)\}\),",
    re.S,
)


def is_iron(component_id: str) -> bool:
    if not component_id:
        return True
    if component_id in IRONS:
        return True
    return "IronSight" in component_id or "Ironsight" in component_id


def is_grip(component_id: str) -> bool:
    return "VerticalGrip" in component_id or "TacGrip" in component_id


def load_slots(path: Path = CSV) -> tuple[dict[tuple[str, str], str], dict[str, str]]:
    pair: dict[tuple[str, str], str] = {}
    by_id: dict[str, str] = {}
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            weapon = row["weapon_id"]
            component = row["component_id"]
            slot = row["slot_type"]
            pair[(weapon, component)] = slot
            by_id.setdefault(component, slot)
    return pair, by_id


def slot_of(weapon: str, component: str, pair: dict, by_id: dict) -> str | None:
    return pair.get((weapon, component)) or by_id.get(component)


def scope_req(rule: dict | None, scope: str) -> str | None:
    if not rule or is_iron(scope):
        return None
    if rule.get("conv"):
        if rule.get("conv_any") or scope in rule.get("conv_scopes", ()):
            return "conv"
        return None
    mode = rule.get("scope")
    if mode == "east":
        return "dove" if scope in EASTERN else "blocked"
    if mode == "west":
        return "nato"
    if mode == "split":
        return "dove" if scope in EASTERN else "nato"
    if mode == "rail":
        return "rail"
    if mode == "handguard":
        return "handguard"
    return None


def parts_for(rule: dict, req: str, upgrades: list[str]) -> list[str]:
    if req in (None, "blocked"):
        return []
    if req == "dove":
        return [rule["dove"]] if rule.get("dove") else []
    if req == "nato":
        parts = []
        if rule.get("dove") and not rule.get("factory"):
            parts.append(rule["dove"])
        if rule.get("nato"):
            parts.append(rule["nato"])
        return parts
    if req == "rail":
        if rule.get("handguard_satisfies") in upgrades:
            return []
        return [rule["rail"]] if rule.get("rail") else []
    if req == "rail2":
        return [rule["rail2"]] if rule.get("rail2") else []
    if req == "handguard":
        return [rule["handguard"]] if rule.get("handguard") else []
    if req == "conv":
        return [rule["conv"]] if rule.get("conv") else []
    return []


def order_upgrades(weapon: str, upgrades: list[str], pair: dict, by_id: dict) -> tuple[list[str], list[str]]:
    """Return (ordered upgrades, blocked component ids that still cannot install)."""
    rule = RULES.get(weapon)
    needed: list[str] = []
    blocked: list[str] = []
    forced_handguard = None

    def add(parts: list[str]) -> None:
        for part in parts:
            if part and part not in needed:
                needed.append(part)

    for component in upgrades:
        slot = slot_of(weapon, component, pair, by_id)
        if rule:
            req = None
            if slot == "Scope":
                req = scope_req(rule, component)
                if req == "blocked":
                    blocked.append(component)
            elif slot == "Side" and component != "JAZZ_HandlingWrap" and rule.get("side"):
                req = rule["side"]
            elif slot == "Under" and is_grip(component) and rule.get("grips"):
                req = rule["grips"]
            if req and req != "blocked":
                add(parts_for(rule, req, upgrades))
                if req == "handguard":
                    forced_handguard = rule.get("handguard")
        if weapon in ("M4A1", "M16A4") and slot in ("Side", "Under") and component:
            add([RIS])
            forced_handguard = RIS

    if weapon == "FNFAL" and not any(part in FAL_FOLD for part in upgrades):
        wants_tac = (
            FAL_TAC in upgrades
            or "JAZZ_StockHeavy" in upgrades
            or any(part in FAL_LONG for part in upgrades)
        )
        if wants_tac:
            needed = [part for part in needed if part != (rule or {}).get("rail")]
            if FAL_TAC not in needed:
                needed.insert(0, FAL_TAC)
    elif FAL_TAC in upgrades:
        needed = [part for part in needed if part != (rule or {}).get("rail")]

    drop = set()
    if forced_handguard:
        for component in upgrades:
            if slot_of(weapon, component, pair, by_id) == "Handguard" and component != forced_handguard:
                drop.add(component)
    if FAL_TAC in upgrades and rule and rule.get("rail"):
        drop.add(rule["rail"])

    ordered = list(needed)
    seen = set(needed)
    for component in upgrades:
        if component in drop or component in seen:
            continue
        ordered.append(component)
        seen.add(component)
    return ordered, blocked


def rewrite(text: str, pair: dict, by_id: dict) -> tuple[str, list[str], list[str]]:
    notes: list[str] = []
    blocked_notes: list[str] = []
    newline = "\n"

    def replace(match: re.Match) -> str:
        body = match.group("body")
        weapon_match = re.search(r'weapon\s*=\s*"([^"]+)"', body)
        upgrades_match = re.search(
            r"(?P<indent>[ \t]*)upgrades\s*=\s*\{(?P<inner>[^}]*)\}",
            body,
        )
        if not weapon_match or not upgrades_match:
            return match.group(0)
        weapon = weapon_match.group(1)
        current = re.findall(r'"([^"]+)"', upgrades_match.group("inner"))
        ordered, blocked = order_upgrades(weapon, current, pair, by_id)
        if blocked:
            blocked_notes.append(f"{weapon}: {', '.join(blocked)}")
        if ordered == current:
            return match.group(0)
        indent = upgrades_match.group("indent")
        entry_indent = indent + "\t"
        inner_lines = [f'{newline}{entry_indent}"{component}",' for component in ordered]
        new_upgrades = f"{indent}upgrades = {{{''.join(inner_lines)}{newline}{indent}}}"
        new_body = body[: upgrades_match.start()] + new_upgrades + body[upgrades_match.end() :]
        notes.append(f"{weapon}: {current} -> {ordered}")
        closing = match.group("indent")
        return f"PlaceObj('LootEntryUpgradedWeapon', {{{new_body}{newline}{closing}}}),"

    updated = BLOCK.sub(replace, text)
    return updated, notes, blocked_notes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    paths = args.paths or [UNITS, MAPS]
    pair, by_id = load_slots()
    for path in paths:
        if not path.is_file():
            print(f"skip {path}")
            continue
        original = path.read_text(encoding="utf-8")
        crlf = "\r\n" in original
        updated, notes, blocked = rewrite(original.replace("\r\n", "\n"), pair, by_id)
        print(f"{path.name}: {len(notes)} loadouts")
        for line in notes[:30]:
            print(" ", line)
        if len(notes) > 30:
            print(f"  ... {len(notes) - 30} more")
        if blocked:
            print(f"  blocked optics left in place: {len(blocked)}")
        if args.apply and updated != original.replace("\r\n", "\n"):
            path.write_text(updated, encoding="utf-8", newline="\r\n" if crlf else "\n")
            print(f"  wrote {path}")


if __name__ == "__main__":
    main()
