# -*- coding: utf-8 -*-
"""Long scopes: T1 vintage → T5 10x; mild AA% on T3+.

Canon: docs/design/long-scope-tiers.md
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
    # --- T1 vintage / low-tier ---
    "JAZZ_Scope_PU": {
        "kind": "long",
        "comment": "Long Scope T1 — PU 3x vintage + AimAccuracy 112 @ AimLevel",
        "mag": 3,
        "aim": 2,
        "ow": 75,
        "shot": 1,
        "max_aim_plus": 0,
        "min_range": 6,
        "near": 85,
        "aim_pct": 112,
        "cost": 40,
        "diff": -10,
        "small": None,
    },
    "JAZZ_Scope_Garand": {
        "kind": "long",
        "comment": "Long Scope T1 — Garand 2x vintage + AimAccuracy 110 @ AimLevel",
        "mag": 2,
        "aim": 2,
        "ow": 82,
        "shot": 1,
        "max_aim_plus": 0,
        "min_range": 5,
        "near": 88,
        "aim_pct": 110,
        "cost": 40,
        "diff": -15,
        "small": None,
    },
    "JAZZ_Scope_Springfield": {
        "kind": "long",
        "comment": "Long Scope T1 — Springfield 2x vintage + AimAccuracy 110 @ AimLevel",
        "mag": 2,
        "aim": 2,
        "ow": 80,
        "shot": 1,
        "max_aim_plus": 0,
        "min_range": 5,
        "near": 88,
        "aim_pct": 110,
        "cost": 45,
        "diff": -10,
        "small": None,
    },
    # --- T2 classic 4x (full-aim AA% ≈ Combat ACOG; unlock later) ---
    "JAZZ_Scope_PSO": {
        "kind": "long",
        "comment": "Long Scope T2 — PSO 4x, AA 155 @ AimLevel 3 (full ≈ ACOG)",
        "mag": 4,
        "aim": 3,
        "ow": 65,
        "shot": 1,
        "max_aim_plus": 0,
        "min_range": 8,
        "near": 78,
        "aim_pct": 155,
        "cost": 60,
        "diff": 0,
        "small": None,
    },
    "JAZZ_Scope_ZF4": {
        "kind": "long",
        "comment": "Long Scope T2 — ZF4 4x, AA 155 @ AimLevel 3",
        "mag": 4,
        "aim": 3,
        "ow": 65,
        "shot": 1,
        "max_aim_plus": 0,
        "min_range": 8,
        "near": 78,
        "aim_pct": 155,
        "cost": 60,
        "diff": 0,
        "small": None,
    },
    # --- T3 6x ---
    "JAZZ_Scope_6x": {
        "kind": "long",
        "comment": "Long Scope T3 — 1-6x variable + mild AimAccuracy 115",
        "mag": 6,
        "aim": 3,
        "ow": 55,
        "shot": 1,
        "max_aim_plus": 0,
        "min_range": 10,
        "near": 62,
        "aim_pct": 115,
        "cost": 80,
        "diff": 0,
        "small": {"SmallMagnification": 1, "SmallSubMagnification": None, "SmallAimLevel": 1},
    },
    "JAZZ_Scope_DA15_6x": {
        "kind": "long",
        "comment": "Long Scope T3 — Zeiss 1.5-6x + mild AimAccuracy 115",
        "mag": 6,
        "aim": 3,
        "ow": 55,
        "shot": 1,
        "max_aim_plus": 0,
        "min_range": 10,
        "near": 62,
        "aim_pct": 115,
        "cost": 80,
        "diff": 0,
        "small": {"SmallMagnification": 1, "SmallSubMagnification": 5, "SmallAimLevel": 1},
    },
    # --- T4 7–9x ---
    "JAZZ_Scope_Scout": {
        "kind": "long",
        "comment": "Long Scope T4 — Scout 7x far + AimAccuracy 120",
        "mag": 7,
        "aim": 3,
        "ow": 52,
        "shot": 1,
        "max_aim_plus": 0,
        "min_range": 12,
        "near": 55,
        "aim_pct": 120,
        "cost": 100,
        "diff": 0,
        "small": {"SmallMagnification": 2, "SmallSubMagnification": None, "SmallAimLevel": 1},
    },
    "JAZZ_Scope_8x_SCROME": {
        "kind": "long",
        "comment": "Long Scope T4 — SCROME 8x + AimAccuracy 120",
        "mag": 8,
        "aim": 3,
        "ow": 48,
        "shot": 1,
        "max_aim_plus": 0,
        "min_range": 13,
        "near": 50,
        "aim_pct": 120,
        "cost": 100,
        "diff": 0,
        "small": None,
    },
    "JAZZ_Scope_3x_9x": {
        "kind": "long",
        "comment": "Long Scope T4 — Redfield 3-9x +MaxAim + AimAccuracy 120",
        "mag": 9,
        "aim": 4,
        "ow": 45,
        "shot": 1,
        "max_aim_plus": 1,
        "min_range": 13,
        "near": 48,
        "aim_pct": 120,
        "cost": 110,
        "diff": 0,
        "small": {"SmallMagnification": 3, "SmallSubMagnification": None, "SmallAimLevel": 1},
    },
    # --- T5 10x ---
    "JAZZ_Scope_12x": {
        "kind": "long",
        "comment": "Long Scope T5 — Mark4 10x +MaxAim + AimAccuracy 125",
        "mag": 10,
        "aim": 4,
        "ow": 42,
        "shot": 1,
        "max_aim_plus": 1,
        "min_range": 14,
        "near": 40,
        "aim_pct": 125,
        "cost": 130,
        "diff": 10,
        "small": None,
    },
    # --- Night ---
    "JAZZ_NightScope": {
        "kind": "night",
        "comment": "Night Scope — 5x dark + near tax",
        "mag": 5,
        "aim": 3,
        "ow": 60,
        "shot": 1,
        "max_aim_plus": 0,
        "min_range": 9,
        "near": 70,
        "aim_pct": None,
        "cost": 100,
        "diff": 10,
        "small": None,
    },
    "JAZZ_NightScope_NSPU": {
        "kind": "night",
        "comment": "Night Scope — NSPU 3x dark + near tax",
        "mag": 3,
        "aim": 3,
        "ow": 70,
        "shot": 1,
        "max_aim_plus": 0,
        "min_range": 7,
        "near": 80,
        "aim_pct": None,
        "cost": 100,
        "diff": 10,
        "small": None,
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


def effects_list(profile: dict) -> list[str]:
    if profile["kind"] == "night":
        return [
            "ScopeMagnification",
            "IncreaseShotAP",
            "IgnoreInTheDarkWhenFullyAimed",
            "ScopeOverwatchAngleDecrease",
        ]
    # AimAccuracyPercent is a ScopeMagnification param; CTH gates by AimAccuracyAimLevel/ScopeAimLevel.
    fx = [
        "ScopeMagnification",
        "IncreaseShotAP",
        "CritBonusWhenFullyAimed",
        "ScopeOverwatchAngleDecreaseBig",
    ]
    if profile.get("small"):
        fx.insert(1, "SmallMagnification")
    if profile.get("max_aim_plus"):
        fx.insert(0, "IncreaseMaxAimActions")
    return fx


def effects_block(profile: dict) -> str:
    body = ",\n".join(f'\t\t\t\t\t\t\t\t"{n}"' for n in effects_list(profile))
    return "ModificationEffects = {\n" + body + ",\n\t\t\t\t\t\t\t},"


def params_block(profile: dict) -> str:
    parts = [
        param("ScopeMagnification", profile["mag"]),
        param("ScopeSubMagnification", None),
        param("ScopeAimLevel", profile["aim"]),
        param("OpticMinRange", profile["min_range"]),
        param("OpticNearFactor", profile["near"]),
        param("ScopeOverwatchAngle", profile["ow"]),
        param("ShotAP", profile["shot"]),
    ]
    if profile.get("aim_pct") is not None:
        parts.append(param("AimAccuracyPercent", profile["aim_pct"]))
        parts.append(param("AimAccuracyAimLevel", profile["aim"]))
    small = profile.get("small")
    if small:
        parts.append(param("SmallMagnification", small["SmallMagnification"]))
        parts.append(param("SmallSubMagnification", small.get("SmallSubMagnification")))
        parts.append(param("SmallAimLevel", small["SmallAimLevel"]))
    if profile.get("max_aim_plus"):
        parts.append(param("IncreaseMaxAimActions", profile["max_aim_plus"]))
    return "Parameters = {\n" + "\n".join(parts) + "\n\t\t\t\t\t\t\t},"


def patch_block(text: str, profile: dict) -> str:
    text = re.sub(
        r"ModificationEffects = \{.*?\},",
        effects_block(profile),
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
    if profile.get("diff") is not None and re.search(
        r"ModificationDifficulty = -?\d+,", text
    ):
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
        p = PROFILES[cid]
        aa = p["aim_pct"] if p["aim_pct"] is not None else "—"
        print("patched", cid, p["comment"].split("—")[0].strip(), f"AA%={aa}")
    atomic_write(ITEMS, text)
    print("total", n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
