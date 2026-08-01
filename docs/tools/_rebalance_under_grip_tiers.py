# -*- coding: utf-8 -*-
"""Under/Handgrip/Wrap grip tiers — small cheap role bonuses.

Canon: docs/design/under-grip-tiers.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop, atomic_write, list_region


def _field_span(text: str, name: str) -> tuple[int, int] | None:
    region = list_region(text, name)
    if region is None:
        return None
    m = re.search(rf"\b{re.escape(name)}\s*=\s*\{{", text)
    if not m:
        return None
    end = region[1]
    if end < len(text) and text[end] == ",":
        end += 1
    while end < len(text) and text[end] in " \t":
        end += 1
    if end < len(text) and text[end] == "\n":
        end += 1
    return m.start(), end


def _replace_or_remove_field(text: str, name: str, replacement: str | None) -> str:
    span = _field_span(text, name)
    if span is None:
        if replacement is None:
            return text
        if name == "Parameters":
            fx = _field_span(text, "ModificationEffects")
            if fx is not None:
                return text[: fx[1]] + replacement + "\n" + text[fx[1] :]
        return re.sub(
            r"(DisplayName = T\([^\n]+\),)",
            rf"\1\n\t\t\t\t\t\t\t{replacement}",
            text,
            count=1,
        )
    start, end = span
    if replacement is None:
        return text[:start] + text[end:]
    body = replacement if replacement.endswith("\n") else replacement + "\n"
    return text[:start] + body + text[end:]


ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"


def param(name: str, value: int) -> str:
    return (
        "\t\t\t\t\t\t\t\tPlaceObj('PresetParamNumber', {\n"
        f"\t\t\t\t\t\t\t\t\t'Name', \"{name}\",\n"
        f"\t\t\t\t\t\t\t\t\t'Value', {value},\n"
        f"\t\t\t\t\t\t\t\t\t'Tag', \"<{name}>\",\n"
        "\t\t\t\t\t\t\t\t}),"
    )


def param_pct(name: str, value: int) -> str:
    return (
        "\t\t\t\t\t\t\t\tPlaceObj('PresetParamPercent', {\n"
        f"\t\t\t\t\t\t\t\t\t'Name', \"{name}\",\n"
        f"\t\t\t\t\t\t\t\t\t'Value', {value},\n"
        f"\t\t\t\t\t\t\t\t\t'Tag', \"<{name}>%\",\n"
        "\t\t\t\t\t\t\t\t}),"
    )


PROFILES: dict[str, dict] = {
    "JAZZ_VerticalGrip": {
        "kind": "vertical",
        "comment": "Grip Vertical — Recoil-1 queue control",
        "recoil": 1,
        "cost": 15,
        "diff": 0,
    },
    "JAZZ_VerticalGrip_M14": {
        "kind": "vertical",
        "comment": "Grip Vertical M14 — Recoil-1",
        "recoil": 1,
        "cost": 15,
        "diff": 0,
    },
    "JAZZ_VerticalGrip_Commando": {
        "kind": "vertical",
        "comment": "Grip Vertical Commando — Recoil-1 (was FirstAim)",
        "recoil": 1,
        "cost": 15,
        "diff": 0,
    },
    "JAZZ_AKSU_VerticalGrip": {
        "kind": "vertical",
        "comment": "Grip Vertical AKSU — Recoil-1",
        "recoil": 1,
        "cost": 15,
        "diff": 0,
    },
    "JAZZ_RPK74_VerticalGrip": {
        "kind": "vertical",
        "comment": "Grip Vertical RPK74 — Recoil-1",
        "recoil": 1,
        "cost": 15,
        "diff": 0,
    },
    "JAZZ_TacGrip": {
        "kind": "close",
        "comment": "Grip Tac — CloseRangeFactor+5",
        "factor": 5,
        "cost": 10,
        "diff": 0,
    },
    "JAZZ_TacGrip_M14": {
        "kind": "close",
        "comment": "Grip Tac M14 — CloseRangeFactor+5",
        "factor": 5,
        "cost": 10,
        "diff": 0,
    },
    "JAZZ_HandlingWrap": {
        "kind": "close",
        "comment": "Grip Wrap Side — CloseRangeFactor+5",
        "factor": 5,
        "cost": 10,
        "diff": 0,
    },
    "JAZZ_Handgrip_Ergo": {
        "kind": "ergo",
        "comment": "Grip Ergo — AimAccuracy 105%",
        "aa_pct": 105,
        "cost": 15,
        "diff": 0,
    },
    "JAZZ_SigErgoHandGrip": {
        "kind": "ergo",
        "comment": "Grip Sig Ergo — AimAccuracy 105%",
        "aa_pct": 105,
        "cost": 15,
        "diff": 0,
    },
    "JAZZ_Handgrip_Default": {
        "kind": "empty",
        "comment": "Grip Default — visual only",
        "cost": 5,
        "diff": 0,
    },
    "JAZZ_PKMDefHandGrip": {
        "kind": "empty",
        "comment": "Grip PKM default — visual only",
        "cost": None,
        "diff": None,
    },
    "JAZZ_PKMModHandGrip": {
        "kind": "empty",
        "comment": "Grip PKM mod — visual only",
        "cost": None,
        "diff": None,
    },
    "JAZZ_VerticalGripFld": {
        "kind": "empty",
        "comment": "Grip Vertical folded visual — no combat",
        "cost": 10,
        "diff": 0,
    },
}


def effects_list(profile: dict) -> list[str]:
    kind = profile["kind"]
    if kind == "empty":
        return []
    if kind == "vertical":
        return ["RecoilDecrease"]
    if kind == "close":
        return ["CloseRangeFactorIncrease"]
    if kind == "ergo":
        return ["IncreaseAimAccuracy15Percent"]
    raise ValueError(kind)


def params_list(profile: dict) -> list[str]:
    kind = profile["kind"]
    parts: list[str] = []
    if kind == "vertical":
        parts.append(param("Recoil", profile["recoil"]))
    elif kind == "close":
        parts.append(param("CloseRangeFactorIncrease", profile["factor"]))
    elif kind == "ergo":
        parts.append(param_pct("AimAccuracyPercent", profile["aa_pct"]))
    return parts


def effects_block(profile: dict) -> str:
    fx = effects_list(profile)
    if not fx:
        return "ModificationEffects = {\n\t\t\t\t\t\t\t},"
    body = ",\n".join(f'\t\t\t\t\t\t\t\t"{n}"' for n in fx)
    return "ModificationEffects = {\n" + body + ",\n\t\t\t\t\t\t\t},"


def params_block(profile: dict) -> str:
    parts = params_list(profile)
    if not parts:
        return "Parameters = {\n\t\t\t\t\t\t\t},"
    return "Parameters = {\n" + "\n".join(parts) + "\n\t\t\t\t\t\t\t},"


def patch_block(text: str, profile: dict) -> str:
    fx = effects_list(profile)
    params = params_list(profile)

    if not fx:
        text = _replace_or_remove_field(text, "ModificationEffects", None)
        text = _replace_or_remove_field(text, "Parameters", None)
    else:
        text = _replace_or_remove_field(text, "ModificationEffects", effects_block(profile))
        if params:
            text = _replace_or_remove_field(text, "Parameters", params_block(profile))
        else:
            text = _replace_or_remove_field(text, "Parameters", None)

    if profile.get("cost") is not None:
        if re.search(r"Cost = \d+,", text):
            text = re.sub(r"Cost = \d+,", f"Cost = {profile['cost']},", text, count=1)
        else:
            text = re.sub(
                r"(DisplayName = T\([^\n]+\),)",
                rf"\1\n\t\t\t\t\t\t\tCost = {profile['cost']},",
                text,
                count=1,
            )

    if profile.get("diff") is not None:
        if re.search(r"ModificationDifficulty = -?\d+,", text):
            text = re.sub(
                r"ModificationDifficulty = -?\d+,",
                f"ModificationDifficulty = {profile['diff']},",
                text,
                count=1,
            )
        else:
            text = re.sub(
                r"(DisplayName = T\([^\n]+\),)",
                rf"\1\n\t\t\t\t\t\t\tModificationDifficulty = {profile['diff']},",
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
        print("patched", cid, PROFILES[cid]["kind"])
    atomic_write(ITEMS, text)
    found = {
        prop(b.text, "id")
        for b in placeobj_blocks(text, "ModItemWeaponComponent")
        if prop(b.text, "id") in PROFILES
    }
    miss = set(PROFILES) - found
    if miss:
        print("MISSING", sorted(miss))
    print("total", n)
    return 0 if not miss else 1


if __name__ == "__main__":
    raise SystemExit(main())
