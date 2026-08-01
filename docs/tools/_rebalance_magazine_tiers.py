# -*- coding: utf-8 -*-
"""Magazine tiers: small / standard / expanded(no tax) / large(tax).

Canon: docs/design/magazine-tiers.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop, atomic_write

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


# size_mode: set | decrease | add | mult | none
# size_value: absolute MagazineSize for set; legacy parameter for other modes.
PROFILES: dict[str, dict] = {
    # --- small ---
    "JAZZ_MagSmall20_10": {
        "kind": "small",
        "comment": "Mag Small — size-10 Reload-1 Rel+15",
        "size_mode": "set",
        "size_value": 10,
        "cost": 15,
        "diff": 0,
    },
    "JAZZ_MagSmall30_15": {
        "kind": "small",
        "comment": "Mag Small — size-15 Reload-1 Rel+15",
        "size_mode": "set",
        "size_value": 15,
        "cost": 15,
        "diff": 0,
    },
    "JAZZ_MagSmall30_20": {
        "kind": "small",
        "comment": "Mag Small — size-20 Reload-1 Rel+15",
        "size_mode": "set",
        "size_value": 20,
        "cost": 15,
        "diff": 0,
    },
    # --- standard ---
    "JAZZ_MagNormal": {
        "kind": "normal",
        "comment": "Mag Standard — baseline",
        "cost": 25,
        "diff": 0,
    },
    "JAZZ_MagNormalFine": {
        "kind": "normal_fine",
        "comment": "Mag Standard Fine — Rel+10",
        "rel": 10,
        "cost": 15,
        "diff": 0,
    },
    "JAZZ_MagQuick": {
        "kind": "quick",
        "comment": "Mag Quick — ReloadAP-1",
        "reload_dec": 1,
        "cost": 15,
        "diff": 0,
    },
    "JAZZ_MagNormalG18": {
        "kind": "normal_size",
        "comment": "Mag G18 — size-20 only",
        "size_mode": "set",
        "size_value": 20,
        "cost": 25,
        "diff": 0,
    },
    # --- expanded (no tax) ---
    "JAZZ_MagLargeFine": {
        # Premium expanded: size only (no Reload/Rel/AA).
        "kind": "expanded_fine",
        "comment": "Mag Expanded Fine — size-45 no Reload tax",
        "size_mode": "set",
        "size_value": 45,
        "cost": 25,
        "diff": 0,
    },
    "JAZZ_MagLarge_17_33": {
        "kind": "expanded",
        "comment": "Mag Expanded — size-33 Reload+1",
        "size_mode": "set",
        "size_value": 33,
        "cost": 25,
        "diff": 0,
    },
    "JAZZ_MagLarge_5_10": {
        "kind": "expanded",
        "comment": "Mag Expanded — size-10 Reload+1",
        "size_mode": "set",
        "size_value": 10,
        "cost": 25,
        "diff": 0,
    },
    "JAZZ_MagLarge_8_10": {
        "kind": "expanded",
        "comment": "Mag Expanded — size-10 Reload+1",
        "size_mode": "set",
        "size_value": 10,
        "cost": 25,
        "diff": 0,
    },
    "JAZZ_MagLarge_7_10": {
        "kind": "expanded",
        "comment": "Mag Expanded — size-10 Reload+1",
        "size_mode": "set",
        "size_value": 10,
        "cost": 25,
        "diff": 0,
    },
    "JAZZ_MagLarge_18_20": {
        "kind": "expanded",
        "comment": "Mag Expanded — size-20 Reload+1",
        "size_mode": "set",
        "size_value": 20,
        "cost": 25,
        "diff": 0,
    },
    "JAZZ_MagLarge_30_40": {
        "kind": "expanded",
        "comment": "Mag Expanded — size-40 Reload+1",
        "size_mode": "set",
        "size_value": 40,
        "cost": 25,
        "diff": 0,
    },
    "JAZZ_MagLarge_30_45": {
        "kind": "expanded",
        "comment": "Mag Expanded — size-45 Reload+1",
        "size_mode": "set",
        "size_value": 45,
        "cost": 25,
        "diff": 0,
    },
    "JAZZ_MagLarge_30_42": {
        "kind": "expanded",
        "comment": "Mag Expanded — size-42 Reload+1",
        "size_mode": "set",
        "size_value": 42,
        "cost": 25,
        "diff": 0,
    },
    "JAZZ_MagLarge_10_20": {
        "kind": "expanded",
        "comment": "Mag Expanded — size-20 Reload+1",
        "size_mode": "set",
        "size_value": 20,
        "cost": 25,
        "diff": 0,
    },
    "JAZZ_MagLarge_20_30": {
        "kind": "expanded",
        "comment": "Mag Expanded — size-30 Reload+1",
        "size_mode": "set",
        "size_value": 30,
        "cost": 25,
        "diff": 0,
    },
    "JAZZ_MagLarge_25_40": {
        "kind": "expanded",
        "comment": "Mag Expanded — size-40 Reload+1",
        "size_mode": "set",
        "size_value": 40,
        "cost": 25,
        "diff": 0,
    },
    # --- large (tax) ---
    "JAZZ_MagDrum_30_50": {
        "kind": "large",
        "comment": "Mag Drum Large — size-50 Reload+2 Rel-15 AA-15%",
        "size_mode": "set",
        "size_value": 50,
        "cost": 50,
        "diff": 0,
    },
    "JAZZ_MagDrum_35_71": {
        "kind": "large",
        "comment": "Mag Drum Large — size-71 Reload+2 Rel-15 AA-15%",
        "size_mode": "set",
        "size_value": 71,
        "cost": 50,
        "diff": 0,
    },
    "JAZZ_MagDrum_30_75": {
        "kind": "large_ow",
        "comment": "Mag Drum Large — size-75 tax + ExtraOW",
        "size_mode": "set",
        "size_value": 75,
        "extra_shots": 5,
        "cost": 50,
        "diff": 0,
    },
    "JAZZ_MagDrum_30_100": {
        "kind": "large",
        "comment": "Mag Drum Large — size-100 Reload+2 Rel-15 AA-15%",
        "size_mode": "set",
        "size_value": 100,
        "cost": 50,
        "diff": 0,
    },
    "JAZZ_MagDrum_30_100_cumbersome": {
        "kind": "large",
        "comment": "Mag Drum Large cumbersome — size-100 tax",
        "size_mode": "set",
        "size_value": 100,
        "cost": 50,
        "diff": 0,
    },
    "JAZZ_MagBelt_40_100": {
        "kind": "large",
        "comment": "Mag Belt Large — size-100 Reload+2 Rel-15 AA-15%",
        "size_mode": "set",
        "size_value": 100,
        "cost": 50,
        "diff": 0,
    },
    "JAZZ_MagBelt_100_200": {
        "kind": "large",
        "comment": "Mag Belt XL — size-200 Reload+2 Rel-15 AA-15%",
        "size_mode": "set",
        "size_value": 200,
        "cost": 100,
        "diff": 0,
    },
}


def size_fx_and_param(profile: dict) -> tuple[str | None, str | None]:
    mode = profile.get("size_mode")
    val = profile.get("size_value")
    if mode == "set":
        return "MagazineSizeSet", param("MagazineSize", val)
    if mode == "decrease":
        return "ReduceMagazineSize", param("MagazineSizeDecrease", val)
    if mode == "add":
        return "MagazineSizeAdd", param("MagazineSize", val)
    if mode == "mult":
        return "MagazineSizeMultiplier", param("MagazineSizeMultiplier", val)
    return None, None


def effects_list(profile: dict) -> list[str]:
    kind = profile["kind"]
    size_fx, _ = size_fx_and_param(profile)
    if kind == "small":
        return ["ReduceReloadAP", "IncreaseReliability", size_fx]
    if kind == "normal":
        return []
    if kind == "normal_fine":
        return ["IncreaseReliability"]
    if kind == "quick":
        return ["ReduceReloadAP"]
    if kind == "normal_size":
        return [size_fx]
    if kind == "expanded":
        return [size_fx, "IncreaseReloadAP"]
    if kind == "expanded_fine":
        return [size_fx]
    if kind == "large":
        return [
            size_fx,
            "IncreaseReloadAP",
            "ReduceReliability",
            "ReduceAimAccuracy15Percent",
        ]
    if kind == "large_ow":
        return [
            "ExtraOverwatchShots",
            size_fx,
            "IncreaseReloadAP",
            "ReduceReliability",
            "ReduceAimAccuracy15Percent",
        ]
    raise ValueError(kind)


def params_list(profile: dict) -> list[str]:
    kind = profile["kind"]
    parts: list[str] = []
    _, size_p = size_fx_and_param(profile)
    if kind == "small":
        parts.append(param("ReloadAPDecrease", 1))
        parts.append(param("ReliabilityIncrease", 15))
        parts.append(size_p)
    elif kind == "normal":
        pass
    elif kind == "normal_fine":
        parts.append(param("ReliabilityIncrease", profile["rel"]))
    elif kind == "quick":
        parts.append(param("ReloadAPDecrease", profile["reload_dec"]))
    elif kind == "normal_size":
        parts.append(size_p)
    elif kind == "expanded":
        parts.append(size_p)
        parts.append(param("ReloadAPIncrease", 1))
    elif kind == "expanded_fine":
        parts.append(size_p)
    elif kind == "large":
        parts.append(size_p)
        parts.append(param("ReloadAPIncrease", 2))
        parts.append(param("ReliabilityDecrease", 15))
    elif kind == "large_ow":
        parts.append(param("extra_shots", profile["extra_shots"]))
        parts.append(size_p)
        parts.append(param("ReloadAPIncrease", 2))
        parts.append(param("ReliabilityDecrease", 15))
    return [p for p in parts if p]


def effects_block(profile: dict) -> str:
    fx = [f for f in effects_list(profile) if f]
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
    kind = profile["kind"]
    has_fx = bool(re.search(r"ModificationEffects = \{", text))
    has_params = bool(re.search(r"Parameters = \{", text))

    if kind == "normal":
        # strip effects/params if present
        if has_fx:
            text = re.sub(
                r"ModificationEffects = \{.*?\},?\n?",
                "",
                text,
                count=1,
                flags=re.S,
            )
        if has_params:
            text = re.sub(
                r"Parameters = \{.*?\},?\n?",
                "",
                text,
                count=1,
                flags=re.S,
            )
    else:
        if has_fx:
            text = re.sub(
                r"ModificationEffects = \{.*?\},",
                effects_block(profile),
                text,
                count=1,
                flags=re.S,
            )
        else:
            text = re.sub(
                r"(DisplayName = T\([^\n]+\),)",
                rf"\1\n\t\t\t\t\t\t\t{effects_block(profile)}",
                text,
                count=1,
            )
        if has_params:
            text = re.sub(
                r"Parameters = \{.*?\},",
                params_block(profile),
                text,
                count=1,
                flags=re.S,
            )
        else:
            text = re.sub(
                r"(ModificationEffects = \{.*?\},)",
                rf"\1\n\t\t\t\t\t\t\t{params_block(profile)}",
                text,
                count=1,
                flags=re.S,
            )

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

    if profile.get("diff") is not None and re.search(r"ModificationDifficulty = -?\d+,", text):
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
