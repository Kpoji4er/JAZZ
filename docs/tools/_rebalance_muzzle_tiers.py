# -*- coding: utf-8 -*-
"""Muzzle tiers: Recoil vs Silent; no WeaponRange on muzzle.

Canon: docs/design/muzzle-tiers.md
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


def param_pct(name: str, value: int) -> str:
    return (
        "\t\t\t\t\t\t\t\tPlaceObj('PresetParamPercent', {\n"
        f"\t\t\t\t\t\t\t\t\t'Name', \"{name}\",\n"
        f"\t\t\t\t\t\t\t\t\t'Value', {value},\n"
        f"\t\t\t\t\t\t\t\t\t'Tag', \"<{name}>%\",\n"
        "\t\t\t\t\t\t\t\t}),"
    )


PROFILES: dict[str, dict] = {
    "JAZZ_Compensator": {
        "kind": "comp",
        "comment": "Muzzle Compensator — Recoil-3 + same-target",
        "recoil": 3,
        "cost": 30,
        "diff": 0,
    },
    "JAZZ_Galil_Brake_Default": {
        "kind": "brake",
        "comment": "Muzzle Brake Default — Recoil-1",
        "recoil": 1,
        "cost": 2,
        "diff": -25,
    },
    "JAZZ_FlashHider": {
        # M2/M3 carbine special: helps stealth shots, does NOT silence.
        "kind": "flash",
        "comment": "Muzzle FlashHider M2/M3 — Recoil-1 + StealthKill, no Silent",
        "recoil": 1,
        "stealth": 25,
        "cost": 10,
        "diff": 0,
    },
    "JAZZ_ImprovisedSuppressor": {
        # Wider mount coverage by design; SK mid, heavy tax (not top assassin).
        "kind": "sil_t0",
        "comment": "Muzzle Sil T0 Improvised — Noise40 SK40 Group50 Jam AA-15 Rel%-50",
        "noise": 40,
        "stealth": 40,
        "rel_pct": 50,
        "cost": 20,
        "diff": -25,
    },
    "JAZZ_Suppressor": {
        "kind": "sil_t1",
        "comment": "Muzzle Sil T1 — Noise33 SK55 Group70 Jam Rel-10, no Recoil",
        "noise": 33,
        "stealth": 55,
        "rel": 10,
        "cost": 40,
        "diff": 0,
    },
    "JAZZ_SuppressorImproved": {
        "kind": "sil_t2",
        "comment": "Muzzle Sil T2 — Noise25 SK80 Group90 Rel-5 no Jam/Recoil",
        "noise": 25,
        "stealth": 80,
        "rel": 5,
        "cost": 75,
        "diff": 10,
    },
    "JAZZ_PistolSuppressor": {
        "kind": "sil_pistol",
        "comment": "Muzzle Sil Pistol — Noise20 SK70 Group90 Rel-5 no Recoil",
        "noise": 20,
        "stealth": 70,
        "rel": 5,
        "cost": 35,
        "diff": -10,
    },
    "JAZZ_SuppressorIntegrated": {
        "kind": "sil_integ",
        "comment": "Muzzle Sil Integrated — Noise30 SK50 no tax",
        "noise": 30,
        "stealth": 50,
        "cost": 10,
        "diff": 0,
    },
    "JAZZ_DuckbillChoke": {
        "kind": "choke_wide",
        "comment": "Muzzle Choke Duckbill — BuckshotAngle 120",
        "buck": 120,
        "cost": 20,
        "diff": 0,
    },
    "JAZZ_FullChoke": {
        "kind": "choke_tight",
        "comment": "Muzzle Choke Full — BuckshotAngle 80, no Range",
        "buck": 80,
        "cost": 20,
        "diff": 0,
    },
}


def effects_list(profile: dict) -> list[str]:
    kind = profile["kind"]
    if kind == "comp":
        return ["RecoilDecrease", "AccuracyBonusSameTarget"]
    if kind == "brake":
        return ["RecoilDecrease"]
    if kind == "flash":
        return ["RecoilDecrease", "StealthKillBonusPerAim"]
    if kind == "sil_t0":
        return [
            "SilentShots",
            "StealthKillBonusPerAim",
            "ReduceReliabilityPercent",
            "SilencerGroupingReduce50",
            "SilencerJamChance",
            "ReduceAimAccuracy15Percent",
        ]
    if kind == "sil_t1":
        return [
            "SilentShots",
            "StealthKillBonusPerAim",
            "ReduceReliability",
            "SilencerGroupingReduce30",
            "SilencerJamChance",
        ]
    if kind == "sil_t2":
        return [
            "SilentShots",
            "StealthKillBonusPerAim",
            "ReduceReliability",
            "SilencerGroupingReduce10",
        ]
    if kind == "sil_pistol":
        return [
            "SilentShots",
            "StealthKillBonusPerAim",
            "ReduceReliability",
            "SilencerGroupingReduce10",
        ]
    if kind == "sil_integ":
        return ["SilentShots", "StealthKillBonusPerAim"]
    if kind == "choke_wide":
        return ["IncreaseBuckshotAngle"]
    if kind == "choke_tight":
        return ["DecreaseBuckshotAngle"]
    raise ValueError(kind)


def params_list(profile: dict) -> list[str]:
    kind = profile["kind"]
    parts: list[str] = []
    if kind == "comp":
        parts.append(param("Recoil", profile["recoil"]))
    elif kind == "brake":
        parts.append(param("Recoil", profile["recoil"]))
    elif kind == "flash":
        parts.append(param("Recoil", profile["recoil"]))
        parts.append(param_pct("stealth_kill_bonus", profile["stealth"]))
    elif kind == "sil_t0":
        parts.append(param_pct("NoiseMultiplier", profile["noise"]))
        parts.append(param_pct("stealth_kill_bonus", profile["stealth"]))
        parts.append(param("ReliabilityDecreasePercent", profile["rel_pct"]))
    elif kind in ("sil_t1", "sil_t2", "sil_pistol"):
        parts.append(param_pct("NoiseMultiplier", profile["noise"]))
        parts.append(param_pct("stealth_kill_bonus", profile["stealth"]))
        parts.append(param("ReliabilityDecrease", profile["rel"]))
    elif kind == "sil_integ":
        parts.append(param_pct("NoiseMultiplier", profile["noise"]))
        parts.append(param_pct("stealth_kill_bonus", profile["stealth"]))
    elif kind == "choke_wide":
        parts.append(param("BuckshotAngleIncrease", profile["buck"]))
    elif kind == "choke_tight":
        parts.append(param("BuckshotAngleDecrease", profile["buck"]))
    return parts


def effects_block(profile: dict) -> str:
    fx = effects_list(profile)
    body = ",\n".join(f'\t\t\t\t\t\t\t\t"{n}"' for n in fx)
    return "ModificationEffects = {\n" + body + ",\n\t\t\t\t\t\t\t},"


def params_block(profile: dict) -> str:
    parts = params_list(profile)
    return "Parameters = {\n" + "\n".join(parts) + "\n\t\t\t\t\t\t\t},"


def patch_block(text: str, profile: dict) -> str:
    text = re.sub(
        r"ModificationEffects = \{.*?\},",
        effects_block(profile),
        text,
        count=1,
        flags=re.S,
    )
    if re.search(r"Parameters = \{.*?\},", text, flags=re.S):
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
    print("total", n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
