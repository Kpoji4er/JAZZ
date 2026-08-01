# -*- coding: utf-8 -*-
"""Stock tiers: Normal = empty default; Light ≡ Unfolded combat; Folded = mobility.

Canon: docs/design/stock-tiers.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop, atomic_write, list_region


def _field_span(text: str, name: str) -> tuple[int, int] | None:
    """Return [name = { ... },] span with brace-balanced body (avoids nested PlaceObj traps)."""
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


# Light and Unfolded share combat (Recoil+2). Unfolded adds zzStockEquipped only.
# Costs: Folded == Unfolded (== Light); Normal (full) slightly above fold pair.
PROFILES: dict[str, dict] = {
    "JAZZ_StockNormal": {
        "kind": "empty",
        "comment": "Stock Normal — full default stock, slightly above fold pair",
        "cost": 25,
        "diff": 0,
    },
    "JAZZ_StockHeavy": {
        "kind": "heavy",
        "comment": "Stock Heavy — Recoil-5 + AA115%",
        "recoil": 5,
        "cost": 40,
        "diff": 10,
    },
    "JAZZ_StockLight": {
        "kind": "light",
        "comment": "Stock Light — Recoil+2 (same as Unfolded, no fold)",
        "recoil": 2,
        "cost": 20,
        "diff": 0,
    },
    "JAZZ_StockLightUnFolded": {
        "kind": "unfolded",
        "comment": "Stock Unfolded — Recoil+2 + zz (same combat as Light)",
        "recoil": 2,
        "cost": 20,
        "diff": 0,
    },
    "JAZZ_StockLightFolded": {
        "kind": "folded",
        "comment": "Stock Folded — same Cost as UnFolded; hidden from ModifyWeapon craft list",
        "recoil": 5,
        "aa_pct": 85,
        "shoot_ap": 1,
        "max_aim": 1,
        "ow": 2,
        "cost": 20,
        "diff": 0,
    },
    "JAZZ_StockNo": {
        "kind": "nostock",
        "comment": "Stock No — ShootAP-1 Recoil+5 AA85% OW+2",
        "recoil": 5,
        "aa_pct": 85,
        "shoot_ap": 1,
        "ow": 2,
        "cost": 15,
        "diff": 10,
    },
    "JAZZ_StockFolded": {
        "kind": "nostock",
        "comment": "Stock Folded legacy — same Cost as fold pair; hidden from craft list",
        "recoil": 5,
        "aa_pct": 85,
        "shoot_ap": 1,
        "ow": 2,
        "cost": 20,
        "diff": 0,
    },
    "JAZZ_PKMModStock": {
        "kind": "empty",
        "comment": "Stock PKM visual only",
        "cost": None,
        "diff": None,
    },
    "JAZZ_UnfoldStocks": {
        "kind": "empty",
        "comment": "Stock Unfold visual only",
        "cost": None,
        "diff": None,
    },
}


def effects_list(profile: dict) -> list[str]:
    kind = profile["kind"]
    if kind == "empty":
        return []
    if kind == "heavy":
        return ["RecoilDecrease", "IncreaseAimAccuracy15Percent"]
    if kind == "light":
        return ["RecoilIncrease"]
    if kind == "unfolded":
        return ["RecoilIncrease", "zzStockEquipped"]
    if kind == "folded":
        return [
            "ReduceShootAP",
            "RecoilIncrease",
            "ReduceAimAccuracy15Percent",
            "ExtraOverwatchShots",
            "DecreaseMaxAimActions",
            "zzStockEquipped",
        ]
    if kind == "nostock":
        return [
            "ReduceShootAP",
            "RecoilIncrease",
            "ReduceAimAccuracy15Percent",
            "ExtraOverwatchShots",
        ]
    raise ValueError(kind)


def params_list(profile: dict) -> list[str]:
    kind = profile["kind"]
    parts: list[str] = []
    if kind == "empty":
        pass
    elif kind == "heavy":
        parts.append(param("Recoil", profile["recoil"]))
        parts.append(param_pct("AimAccuracyPercent", 115))
    elif kind in ("light", "unfolded"):
        parts.append(param("Recoil", profile["recoil"]))
    elif kind == "folded":
        parts.append(param("ShootAPDecrease", profile["shoot_ap"]))
        parts.append(param("Recoil", profile["recoil"]))
        parts.append(param_pct("AimAccuracyPercent", profile["aa_pct"]))
        parts.append(param("extra_attacks", profile["ow"]))
        parts.append(param("MaxAimActionsDecrease", profile["max_aim"]))
    elif kind == "nostock":
        parts.append(param("ShootAPDecrease", profile["shoot_ap"]))
        parts.append(param("Recoil", profile["recoil"]))
        parts.append(param_pct("AimAccuracyPercent", profile["aa_pct"]))
        parts.append(param("extra_attacks", profile["ow"]))
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

    # Brace-balanced: naive \{.*?\} truncates inside nested PresetParam PlaceObj.
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
