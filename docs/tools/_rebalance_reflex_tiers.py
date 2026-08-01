# -*- coding: utf-8 -*-
"""Differentiate JAZZ_Reflex_* into Precision / Overwatch / Universal.

Canon: docs/design/reflex-collimator-tiers.md

Target feel (AKM mid merc): top Precision ~x1.20 close vs irons snap
via AimAccuracy% + CloseRangeFactorIncrease (soft hip deadzone).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop, atomic_write

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"

# close_add: CloseRangeFactorIncrease (Add on weapon CloseRangeFactor; AKM 85 → 85+add)
PROFILES = {
    "JAZZ_Reflex_Garand": {
        "comment": "Reflex Precision T1 — budget AimAccuracy + close soft",
        "archetype": "precision",
        "aim_pct": 120,
        "close_add": 15,
        "extra": 0,
        "ow": None,
        "oa": None,
        "cost": 30,
        "diff": -15,
    },
    "JAZZ_Reflex_Aimpoint5000": {
        "comment": "Reflex Precision T1 — budget Aimpoint + close soft",
        "archetype": "precision",
        "aim_pct": 120,
        "close_add": 15,
        "extra": 0,
        "ow": None,
        "oa": None,
        "cost": 35,
        "diff": -10,
    },
    "JAZZ_Reflex_Closed": {
        "comment": "Reflex Precision T2 — tube AimAccuracy + close soft",
        "archetype": "precision",
        "aim_pct": 135,
        "close_add": 20,
        "extra": 0,
        "ow": None,
        "oa": None,
        "cost": 50,
        "diff": 0,
    },
    "JAZZ_Reflex_M68": {
        "comment": "Reflex Precision T3 — military AimAccuracy + close soft",
        "archetype": "precision",
        "aim_pct": 150,
        "close_add": 25,
        "extra": 0,
        "ow": None,
        "oa": None,
        "cost": 75,
        "diff": 10,
    },
    "JAZZ_Reflex_PKAS": {
        "comment": "Reflex Precision T4 — premium AimAccuracy + close soft (~+20% CQB)",
        "archetype": "precision",
        "aim_pct": 160,
        "close_add": 35,
        "extra": 0,
        "ow": None,
        "oa": None,
        "cost": 100,
        "diff": 15,
    },
    "JAZZ_Reflex_Cobra": {
        "comment": "Reflex Overwatch T1 — eastern open, mild close soft, no OA",
        "archetype": "overwatch",
        "aim_pct": None,
        "close_add": 15,
        "extra": 1,
        "ow": 140,
        "oa": None,
        "cost": 35,
        "diff": -10,
    },
    "JAZZ_Reflex_Open": {
        "comment": "Reflex Overwatch T2 — compact open (2 OW shots) + close soft",
        "archetype": "overwatch",
        "aim_pct": None,
        "close_add": 15,
        "extra": 2,
        "ow": 150,
        "oa": 8,
        "cost": 50,
        "diff": 0,
    },
    "JAZZ_Reflex_Pistol": {
        "comment": "Reflex Overwatch T2 — pistol compact (2 OW shots) + close soft",
        "archetype": "overwatch",
        "aim_pct": None,
        "close_add": 15,
        "extra": 2,
        "ow": 150,
        "oa": 8,
        "cost": 45,
        "diff": 0,
    },
    "JAZZ_Reflex_Eotech": {
        "comment": "Reflex Universal T4 — mid AimAccuracy + mid OW + close soft",
        "archetype": "universal",
        "aim_pct": 135,
        "close_add": 20,
        "extra": 1,
        "ow": 145,
        "oa": 8,
        "cost": 90,
        "diff": 10,
    },
}


def effects_list(profile: dict) -> list[str]:
    # AimAccuracyPercent hangs on MinAim; CTH applies only when aim >= AimAccuracyAimLevel (default 1).
    effects = ["DecreaseMaxAimActions", "MinAim", "CloseRangeFactorIncrease"]
    if profile["extra"] and profile["extra"] > 0:
        effects.append("ExtraOverwatchShots")
    if profile["ow"] is not None:
        effects.append(
            "ScopeOverwatchAngleIncreaceBig"
            if profile["archetype"] in ("overwatch", "universal")
            else "ScopeOverwatchAngleIncreace"
        )
    if profile["oa"] is not None:
        effects.append("OpportunityAttackBonusCth")
    return effects


def effects_block(profile: dict) -> str:
    lines = effects_list(profile)
    body = ",\n".join(f'\t\t\t\t\t\t\t\t"{name}"' for name in lines)
    return "ModificationEffects = {\n" + body + ",\n\t\t\t\t\t\t\t},"


def params_block(profile: dict) -> str:
    parts: list[tuple[str, int]] = [
        ("MaxAimActionsDecrease", 1),
        ("CloseRangeFactorIncrease", profile["close_add"]),
    ]
    if profile["aim_pct"] is not None:
        parts.append(("AimAccuracyPercent", profile["aim_pct"]))
        parts.append(("AimAccuracyAimLevel", 1))
    if profile["extra"] and profile["extra"] > 0:
        parts.append(("extra_attacks", profile["extra"]))
    if profile["ow"] is not None:
        parts.append(("ScopeOverwatchAngle", profile["ow"]))
    if profile["oa"] is not None:
        parts.append(("bonus_cth", profile["oa"]))
    chunks = []
    for name, value in parts:
        chunks.append(
            "\t\t\t\t\t\t\t\tPlaceObj('PresetParamNumber', {\n"
            f"\t\t\t\t\t\t\t\t\t'Name', \"{name}\",\n"
            f"\t\t\t\t\t\t\t\t\t'Value', {value},\n"
            f"\t\t\t\t\t\t\t\t\t'Tag', \"<{name}>\",\n"
            "\t\t\t\t\t\t\t\t}),"
        )
    return "Parameters = {\n" + "\n".join(chunks) + "\n\t\t\t\t\t\t\t},"


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
    if re.search(r"Cost = \d+,", text):
        text = re.sub(r"Cost = \d+,", f"Cost = {profile['cost']},", text, count=1)
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
            r"(\n\t\t\t\t\t\t\tgroup = \"Scope\",)",
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
        print("patched", cid, f"AA={aa} close+{p['close_add']}")
    atomic_write(ITEMS, text)
    print("total", n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
