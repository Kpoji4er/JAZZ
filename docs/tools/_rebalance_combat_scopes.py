# -*- coding: utf-8 -*-
"""Combat scopes: mid universal, mild near, OW↓, AimAccuracy% for ~+20-30% mid.

Canon: docs/design/combat-scope-tiers.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop, atomic_write

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"

PROFILES = {
    "JAZZ_CombatScope_2x": {
        "comment": "Combat Universal T1 — mid 2x, mild near ~6, OW 85%, AimAccuracy 125",
        "mag": 2,
        "aim": 1,
        "min_range": 6,
        "near_pct": 92,
        "ow_pct": 85,
        "aim_pct": 125,
        "cost": 50,
        "diff": 0,
    },
    "JAZZ_CombatScope_3x": {
        "comment": "Combat Universal T2 — mid 3x, mild near ~9, OW 78%, AimAccuracy 140",
        "mag": 3,
        "aim": 2,
        "min_range": 9,
        "near_pct": 90,
        "ow_pct": 78,
        "aim_pct": 140,
        "cost": 60,
        "diff": 0,
    },
    "JAZZ_G36Scope": {
        "comment": "Combat Universal T2 — G36 3x, mild near ~9, OW 78%, AimAccuracy 140",
        "mag": 3,
        "aim": 2,
        "min_range": 9,
        "near_pct": 90,
        "ow_pct": 78,
        "aim_pct": 140,
        "cost": None,
        "diff": None,
    },
    "JAZZ_CombatScope_ACOG": {
        "comment": "Combat Universal T3 — ACOG mid 4x, mild near ~12, OW 70%, AimAccuracy 155",
        "mag": 4,
        "aim": 2,
        "min_range": 12,
        "near_pct": 88,
        "ow_pct": 70,
        "aim_pct": 155,
        "cost": 100,
        "diff": 0,
    },
    "JAZZ_CombatScope_1P29": {
        "comment": "Combat Universal T3 — 1P29 mid 4x, mild near ~12, OW 70%, AimAccuracy 155",
        "mag": 4,
        "aim": 2,
        "min_range": 12,
        "near_pct": 88,
        "ow_pct": 70,
        "aim_pct": 155,
        "cost": 100,
        "diff": 0,
    },
    "JAZZ_CombatScope_FeroZ24": {
        "comment": "Combat Universal T3 — Fero Z24 mid 4x, mild near ~12, OW 70%, AimAccuracy 155",
        "mag": 4,
        "aim": 2,
        "min_range": 12,
        "near_pct": 88,
        "ow_pct": 70,
        "aim_pct": 155,
        "cost": 100,
        "diff": 0,
    },
}


def param(name: str, value: int | None) -> str:
    if value is None:
        return (
            "\t\t\t\t\t\t\t\tPlaceObj('PresetParamNumber', {\n"
            f"\t\t\t\t\t\t\t\t\t'Name', \"{name}\",\n"
            f"\t\t\t\t\t\t\t\t\t'Tag', \"<{name}>\",\n"
            "\t\t\t\t\t\t\t\t}),"
        )
    return (
        "\t\t\t\t\t\t\t\tPlaceObj('PresetParamNumber', {\n"
        f"\t\t\t\t\t\t\t\t\t'Name', \"{name}\",\n"
        f"\t\t\t\t\t\t\t\t\t'Value', {value},\n"
        f"\t\t\t\t\t\t\t\t\t'Tag', \"<{name}>\",\n"
        "\t\t\t\t\t\t\t\t}),"
    )


def effects_block() -> str:
    # AimAccuracyPercent is a param on ScopeMagnification; applied in CTH only when AimLevel met.
    return (
        "ModificationEffects = {\n"
        '\t\t\t\t\t\t\t\t"ScopeMagnification",\n'
        '\t\t\t\t\t\t\t\t"ScopeOverwatchAngleDecrease",\n'
        "\t\t\t\t\t\t\t},"
    )


def params_block(profile: dict) -> str:
    parts = [
        param("ScopeMagnification", profile["mag"]),
        param("ScopeSubMagnification", None),
        param("ScopeAimLevel", profile["aim"]),
        param("AimAccuracyAimLevel", profile["aim"]),
        param("OpticMinRange", profile["min_range"]),
        param("OpticNearFactor", profile["near_pct"]),
        param("ScopeOverwatchAngle", profile["ow_pct"]),
        param("AimAccuracyPercent", profile["aim_pct"]),
    ]
    return "Parameters = {\n" + "\n".join(parts) + "\n\t\t\t\t\t\t\t},"


def patch_block(text: str, profile: dict) -> str:
    text = re.sub(
        r"ModificationEffects = \{.*?\},",
        effects_block(),
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r"Parameters = \{.*?\},",
        params_block(profile),
        text,
        count=1,
        flags=re.S,
    )
    if profile.get("cost") is not None and re.search(r"Cost = \d+,", text):
        text = re.sub(r"Cost = \d+,", f"Cost = {profile['cost']},", text, count=1)
    if profile.get("diff") is not None:
        text = re.sub(
            r"ModificationDifficulty = -?\d+,",
            f"ModificationDifficulty = {profile['diff']},",
            text,
            count=1,
        )
    if re.search(r'comment = "[^"]*"', text):
        text = re.sub(
            r'comment = "[^"]*"',
            f'comment = "{profile["comment"]}"',
            text,
            count=1,
        )
    else:
        text = re.sub(
            r"(\n\t\t\t\t\t\t\t(?:group|Slot) = )",
            f'\n\t\t\t\t\t\t\tcomment = "{profile["comment"]}",\\1',
            text,
            count=1,
        )
    return text


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    n = 0
    for block in reversed(placeobj_blocks(text, "ModItemWeaponComponent")):
        cid = prop(block.text, "id")
        if cid not in PROFILES:
            continue
        new = patch_block(block.text, PROFILES[cid])
        text = text[: block.start] + new + text[block.end :]
        n += 1
        print("patched", cid, f"AimAccuracy={PROFILES[cid]['aim_pct']}%")
    atomic_write(ITEMS, text)
    print("total", n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
