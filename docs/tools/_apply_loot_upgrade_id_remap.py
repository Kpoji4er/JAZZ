#!/usr/bin/env python3
"""Remap legacy WeaponComponent IDs inside LootEntryUpgradedWeapon.upgrades in jazz-units.

Only rewrites quoted IDs that appear inside `upgrades = { ... }` tables of
LootEntryUpgradedWeapon blocks. Uses explicit map + auto JAZZ_<id> when that
WeaponComponent exists in jazz/items.lua.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units" / "items.lua"

EXPLICIT: dict[str, str] = {
    "Compensator": "JAZZ_Compensator",
    "LaserDot": "JAZZ_LaserDot",
    "LaserDot_PSG_M1": "JAZZ_LaserDot_PSG_M1",
    "LaserDot_aa12": "JAZZ_LaserDot_aa12",
    "PistolSuppressor": "JAZZ_PistolSuppressor",
    "Suppressor": "JAZZ_Suppressor",
    "SuppressorImproved": "JAZZ_SuppressorImproved",
    "VerticalGrip": "JAZZ_VerticalGrip",
    "Bipod": "JAZZ_Bipod",
    "Bipod_Galil": "JAZZ_Bipod_Galil",
    "Flashlight": "JAZZ_Flashlight",
    "FlashlightDot": "JAZZ_FlashlightDot",
    "UVDot": "JAZZ_UVDot",
    "MagNormal": "JAZZ_MagNormal",
    "MagNormalFine": "JAZZ_MagNormalFine",
    "MagLarge": "JAZZ_MagLarge",
    "MagLarge_18_20": "JAZZ_MagLarge_18_20",
    "MagLarge_20_30": "JAZZ_MagLarge_20_30",
    "MagLarge_30_40": "JAZZ_MagLarge_30_40",
    "MagLarge_30_45": "JAZZ_MagLarge_30_45",
    "GP25": "JAZZ_GP25",
    "AUGCompensator_03": "JAZZ_AUGCompensator_01",
    "Jazz_G36Sight": "JAZZ_G36Sight",
    "Jazz_G36Scope": "JAZZ_G36Scope",
    "ReflexSight": "JAZZ_Reflex_Closed",
    "ScopeCOG": "JAZZ_CombatScope_ACOG",
}

# Do NOT remap stock/barrel/ironsight vanilla IDs unless we know a JAZZ twin —
# many remain valid DefaultComponent names on jazz weapons.


def load_jazz_component_ids() -> set[str]:
    text = (JAZZ / "items.lua").read_text(encoding="utf-8")
    ids = set(re.findall(r"\bid\s*=\s*\"(JAZZ_[^\"]+)\"", text))
    ids.update(re.findall(r"'Id',\s*\"(JAZZ_[^\"]+)\"", text))
    # Companion inventory remountables often share component id
    for p in (JAZZ / "InventoryItem").glob("JAZZ_*.lua"):
        ids.add(p.stem)
    return ids


def resolve(old: str, jazz_ids: set[str]) -> str | None:
    if old.startswith("JAZZ_"):
        return None
    if old in EXPLICIT:
        target = EXPLICIT[old]
        return target if target in jazz_ids or target.startswith("JAZZ_") else None
    twin = f"JAZZ_{old}"
    if twin in jazz_ids:
        return twin
    return None


def main() -> int:
    jazz_ids = load_jazz_component_ids()
    text = UNITS.read_text(encoding="utf-8")
    counts: Counter[str] = Counter()
    skipped: Counter[str] = Counter()

    def repl_upgrades(m: re.Match[str]) -> str:
        body = m.group(1)

        def repl_id(im: re.Match[str]) -> str:
            old = im.group(1)
            new = resolve(old, jazz_ids)
            if not new:
                skipped[old] += 1
                return im.group(0)
            if new not in jazz_ids and new not in EXPLICIT.values():
                skipped[old] += 1
                return im.group(0)
            counts[f"{old}->{new}"] += 1
            return f'"{new}"'

        new_body = re.sub(r'"([A-Za-z0-9_]+)"', repl_id, body)
        return "upgrades = {" + new_body + "}"

    # Only inside LootEntryUpgradedWeapon: safer to replace all upgrades = { } then
    # verify we're not touching non-weapon tables with same key (rare).
    new_text, n = re.subn(
        r"upgrades\s*=\s*\{([^{}]*)\}",
        repl_upgrades,
        text,
        flags=re.S,
    )
    if new_text == text:
        print("no changes")
        return 0
    UNITS.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"upgrades_blocks_touched~={n}")
    print("remapped:")
    for k, v in counts.most_common():
        print(f"  {v:4} {k}")
    print("left_legacy (in upgrades):")
    for k, v in sorted(skipped.items(), key=lambda kv: (-kv[1], kv[0])):
        if k.startswith("JAZZ_"):
            continue
        print(f"  {v:4} {k}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
