# -*- coding: utf-8 -*-
"""Barrel tiers: effective distance via BDR% + CloseRange*; weak R; keep Recoil.

BDR is Multiply percent (scales for pistols/revolvers). R stays ±1 absolute.
Canon: docs/design/barrel-tiers.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop, atomic_write

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"


def param(name: str, value: int | None) -> str:
    val = "" if value is None else f"\n\t\t\t\t\t\t\t\t\t'Value', {value},"
    return (
        "\t\t\t\t\t\t\t\tPlaceObj('PresetParamNumber', {\n"
        f"\t\t\t\t\t\t\t\t\t'Name', \"{name}\",{val}\n"
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


# bdr_pct: Multiply on BulletDropRange (70 = 70% of base). r: absolute WeaponRange ±.
PROFILES: dict[str, dict] = {
    "JAZZ_BarrelShort": {
        "kind": "short",
        "comment": "Barrel Short — near↑ BDR 70% R-1 Recoil+2 Rel-10",
        "bdr_pct": 70,
        "r": 1,
        "close": 3,
        "factor": 12,
        "recoil": 2,
        "rel": 10,
        "cost": 15,
    },
    "JAZZ_BarrelShortImproved": {
        "kind": "short",
        "comment": "Barrel Short Improved — near↑ BDR 70% R-1 Recoil+2",
        "bdr_pct": 70,
        "r": 1,
        "close": 3,
        "factor": 12,
        "recoil": 2,
        "rel": None,
        "cost": 35,
    },
    "JAZZ_BarrelShort_AUG": {
        "kind": "short",
        "comment": "Barrel Short AUG — near↑ BDR 70% R-1 Recoil+2 Rel-10",
        "bdr_pct": 70,
        "r": 1,
        "close": 3,
        "factor": 12,
        "recoil": 2,
        "rel": 10,
        "cost": 15,
    },
    "JAZZ_BarrelShortImproved_AUG": {
        "kind": "short",
        "comment": "Barrel Short Improved AUG — near↑ BDR 70% R-1 Recoil+2",
        "bdr_pct": 70,
        "r": 1,
        "close": 3,
        "factor": 12,
        "recoil": 2,
        "rel": None,
        "cost": 35,
    },
    "JAZZ_BarrelShortRunNGun": {
        "kind": "short_rng",
        "comment": "Barrel Short RunNGun — near↑ BDR 70% R-1 Recoil+2 Rel-10",
        "bdr_pct": 70,
        "r": 1,
        "close": 3,
        "factor": 12,
        "recoil": 2,
        "rel": 10,
        "cost": 15,
    },
    "JAZZ_BarrelShort_Pistol": {
        "kind": "short_pistol",
        "comment": "Barrel Short Pistol — CQB zone 3@115% BDR 85% Recoil+1",
        "bdr_pct": 85,
        "r": 0,
        "close": 3,
        "factor": 15,
        "recoil": 1,
        "rel": None,
        "cost": 15,
    },
    "JAZZ_BarrelLong": {
        "kind": "long",
        "comment": "Barrel Long — far↑ BDR 130% R+1 Recoil-2 near-tax",
        "bdr_pct": 130,
        "r": 1,
        "close": 3,
        "factor": 8,
        "recoil": 2,
        "rel": None,
        "cost": 75,
    },
    "JAZZ_BarrelLongImproved": {
        "kind": "long",
        "comment": "Barrel Long Improved — far↑ BDR 130% R+1 Recoil-2 Rel+10",
        "bdr_pct": 130,
        "r": 1,
        "close": 3,
        "factor": 8,
        "recoil": 2,
        "rel": 10,
        "cost": 100,
    },
    "JAZZ_BarrelLong_AUG": {
        "kind": "long",
        "comment": "Barrel Long AUG — far↑ BDR 130% R+1 Recoil-2 near-tax",
        "bdr_pct": 130,
        "r": 1,
        "close": 3,
        "factor": 8,
        "recoil": 2,
        "rel": None,
        "cost": 70,
    },
    "JAZZ_BarrelLongImproved_AUG": {
        "kind": "long",
        "comment": "Barrel Long Improved AUG — far↑ BDR 130% R+1 Recoil-2 Rel+10",
        "bdr_pct": 130,
        "r": 1,
        "close": 3,
        "factor": 8,
        "recoil": 2,
        "rel": 10,
        "cost": 100,
    },
    "JAZZ_BarrelHeavy": {
        "kind": "heavy",
        "comment": "Barrel Heavy — Recoil-5 BDR 115% near-tax, no flat CTH",
        "bdr_pct": 115,
        "r": 0,
        "close": 2,
        "factor": 8,
        "recoil": 5,
        "rel": None,
        "cost": 30,
    },
    "JAZZ_BarrelShortShotgun": {
        "kind": "short_sg",
        "comment": "Barrel Short Shotgun — CQB BDR 80% R-1",
        "bdr_pct": 80,
        "r": 1,
        "close": 1,
        "factor": 12,
        "recoil": None,
        "rel": 10,
        "buck": 115,
        "cost": 15,
    },
    "JAZZ_BarrelShortShotgun_Benelli": {
        "kind": "benelli_sg",
        "comment": "Barrel Short Benelli — CQB R-1 Mag-2 no ShootAP",
        "bdr_pct": 0,
        "r": 1,
        "close": 1,
        "factor": 12,
        "recoil": None,
        "rel": 10,
        "buck": 115,
        "mag": 2,
        "cost": 15,
    },
    "JAZZ_BarrelLongShotgun": {
        "kind": "long_sg",
        "comment": "Barrel Long Shotgun — BDR 120% R+1 soft close",
        "bdr_pct": 120,
        "r": 1,
        "close": 1,
        "factor": 10,
        "recoil": None,
        "rel": None,
        "cost": 75,
    },
}


def effects_list(profile: dict) -> list[str]:
    kind = profile["kind"]
    if kind == "short":
        fx = [
            "BarrelBulletDropReduce",
            "BarrelRecoilIncrease",
            "BarrelGroupingReduce",
            "CloseRangeDecrease",
            "CloseRangeFactorIncrease",
        ]
        if profile.get("r"):
            fx.insert(0, "BarrelRangeReduce")
        if profile.get("rel"):
            fx.insert(0, "ReduceReliability")
        return fx
    if kind == "short_pistol":
        # Base CloseRange=0 on pistols/revolvers — grant a short CQB buff zone.
        fx = [
            "BarrelBulletDropReduce",
            "BarrelRecoilIncrease",
            "BarrelGroupingReduce",
            "CloseRangeIncrease",
            "CloseRangeFactorIncrease",
        ]
        return fx
    if kind == "short_rng":
        fx = [
            "EnableRunNGun",
            "BarrelBulletDropReduce",
            "BarrelRecoilIncrease",
            "BarrelGroupingIncrease",
            "CloseRangeDecrease",
            "CloseRangeFactorIncrease",
        ]
        if profile.get("r"):
            fx.insert(1, "BarrelRangeReduce")
        if profile.get("rel"):
            fx.insert(0, "ReduceReliability")
        return fx
    if kind == "long":
        fx = [
            "BarrelBulletDropIncrease",
            "BarrelRecoilRecude",
            "BarrelGroupingIncrease",
            "CloseRangeIncrease",
            "CloseRangeFactorDecrease",
        ]
        if profile.get("r"):
            fx.insert(0, "BarrelRangeIncrease")
        if profile.get("rel"):
            fx.insert(0, "IncreaseReliability")
        return fx
    if kind == "heavy":
        return [
            "BarrelBulletDropIncrease",
            "BarrelRecoilRecude",
            "CloseRangeIncrease",
            "CloseRangeFactorDecrease",
        ]
    if kind == "short_sg":
        fx = [
            "BarrelBulletDropReduce",
            "BarrelGroupingReduce",
            "CloseRangeDecrease",
            "CloseRangeFactorIncrease",
            "IncreaseBuckshotAngle",
            "ReduceReliability",
        ]
        if profile.get("r"):
            fx.insert(0, "BarrelRangeReduce")
        return fx
    if kind == "benelli_sg":
        return [
            "ReduceRange",
            "CloseRangeDecrease",
            "CloseRangeFactorIncrease",
            "IncreaseBuckshotAngle",
            "ReduceMagazineSize",
            "ReduceReliability",
        ]
    if kind == "long_sg":
        fx = [
            "BarrelBulletDropIncrease",
            "BarrelGroupingIncrease",
            "CloseRangeDecrease",
            "CloseRangeFactorIncrease",
        ]
        if profile.get("r"):
            fx.insert(0, "BarrelRangeIncrease")
        return fx
    raise ValueError(kind)


def params_list(profile: dict) -> list[str]:
    kind = profile["kind"]
    parts: list[str] = []
    if kind in ("short", "short_rng", "short_sg"):
        if profile.get("r"):
            parts.append(param("BarrelRangeReduce", profile["r"]))
        if profile.get("bdr_pct"):
            parts.append(param_pct("BulletDropReduce", profile["bdr_pct"]))
        if profile.get("recoil") is not None:
            parts.append(param("BarrelRecoilIncrease", profile["recoil"]))
        parts.append(param("CloseRangeDecrease", profile["close"]))
        parts.append(param("CloseRangeFactorIncrease", profile["factor"]))
        if profile.get("rel"):
            parts.append(param("ReliabilityDecrease", profile["rel"]))
        if kind == "short_sg":
            parts.append(param("BuckshotAngleIncrease", profile["buck"]))
        if kind == "short_rng":
            parts.append(param_pct("SilencerGroupingReduce", 110))
        else:
            parts.append(param_pct("BarrelGroupingReduce", 90))
    elif kind == "short_pistol":
        parts.append(param_pct("BulletDropReduce", profile["bdr_pct"]))
        parts.append(param("BarrelRecoilIncrease", profile["recoil"]))
        parts.append(param("CloseRangeIncrease", profile["close"]))
        parts.append(param("CloseRangeFactorIncrease", profile["factor"]))
        parts.append(param_pct("BarrelGroupingReduce", 90))
    elif kind == "benelli_sg":
        parts.append(param("RangeDecrease", profile["r"]))
        parts.append(param("CloseRangeDecrease", profile["close"]))
        parts.append(param("CloseRangeFactorIncrease", profile["factor"]))
        parts.append(param("BuckshotAngleIncrease", profile["buck"]))
        parts.append(param("MagazineSizeDecrease", profile["mag"]))
        parts.append(param("ReliabilityDecrease", profile["rel"]))
    elif kind == "long":
        if profile.get("r"):
            parts.append(param("BarrelRangeIncrease", profile["r"]))
        parts.append(param_pct("BulletDropIncrease", profile["bdr_pct"]))
        parts.append(param("BarrelRecoilRecude", profile["recoil"]))
        parts.append(param("CloseRangeIncrease", profile["close"]))
        parts.append(param("CloseRangeFactorDecrease", profile["factor"]))
        parts.append(param_pct("SilencerGroupingReduce", 110))
        if profile.get("rel"):
            parts.append(param("ReliabilityIncrease", profile["rel"]))
    elif kind == "heavy":
        parts.append(param_pct("BulletDropIncrease", profile["bdr_pct"]))
        parts.append(param("BarrelRecoilRecude", profile["recoil"]))
        parts.append(param("CloseRangeIncrease", profile["close"]))
        parts.append(param("CloseRangeFactorDecrease", profile["factor"]))
    elif kind == "long_sg":
        if profile.get("r"):
            parts.append(param("BarrelRangeIncrease", profile["r"]))
        parts.append(param_pct("BulletDropIncrease", profile["bdr_pct"]))
        parts.append(param("CloseRangeDecrease", profile["close"]))
        parts.append(param("CloseRangeFactorIncrease", profile["factor"]))
        parts.append(param_pct("SilencerGroupingReduce", 110))
    return parts


def effects_block(profile: dict) -> str:
    body = ",\n".join(f'\t\t\t\t\t\t\t\t"{n}"' for n in effects_list(profile))
    return "ModificationEffects = {\n" + body + ",\n\t\t\t\t\t\t\t},"


def params_block(profile: dict) -> str:
    return "Parameters = {\n" + "\n".join(params_list(profile)) + "\n\t\t\t\t\t\t\t},"


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
        print("patched", cid, f"BDR%={p.get('bdr_pct')} R±={p.get('r')} Recoil={p.get('recoil')}")
    atomic_write(ITEMS, text)
    print("total", n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
