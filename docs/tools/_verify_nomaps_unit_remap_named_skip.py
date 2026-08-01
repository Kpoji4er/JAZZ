"""Static check: nomaps UnitData remap skips named Legion (Bastien / LegionRaider_Jose).

Mirrors jazz-nomaps Code/NoMaps_Autonomy.lua lMatchUnitFamily + UNIT_GENERIC_SUFFIX.
Exit 0 = OK.
"""
from __future__ import annotations

SUFFIXES = {
    "",
    "_Stronger",
    "_Stronger_Elite",
    "_Elite",
    "_Ernie_Elite",
    "_WeakFlagHill",
    "_Tutorial",
    "_SlowReloader",
    "_PresidentGuard",
}

STEMS = {
    "LegionGoon": "assault",
    "LegionManiac": "crusher",
    "LegionGrenadir": "grenadier",
    "LegionGrenadier": "grenadier",
    "LegionRaider": "front",
    "LegionGunner": "gunner",
    "LegionSniper": "sniper",
    "LegionSharpShooter": "marksman",
    "LegionSharpshooter": "marksman",
    "LegionScout": "flanker",
    "LegionRanger": "flanker",
    "Legion_Recon": "flanker",
    "LegionRaidLeader": "leader",
    "LegionSergant": "leader",
    "LegionSergeant": "leader",
    "LegionMedic": "medic",
    "Legion_WitchDoctor": "medic",
    "LegionRoceteer": "heavy",
    "LegionRocketeer": "heavy",
    "LegionMortalman": "heavy",
    "Legion_Artillery": "heavy",
    "LegionButcher": "butcher",
    "Legion_Soldier": "front",
    "Legion_Marksman": "marksman",
}


def match_unit_family(unit_id: str):
    if not unit_id or unit_id.startswith("JAZZ_Legion"):
        return False
    best, best_len = False, 0
    for stem, family in STEMS.items():
        if unit_id.startswith(stem) and len(stem) > best_len:
            best, best_len = family, len(stem)
    if not best:
        return False
    suffix = unit_id[best_len:]
    if suffix not in SUFFIXES:
        return False
    return best


CASES = [
    ("LegionRaider", "front"),
    ("LegionRaider_Stronger", "front"),
    ("LegionRaider_Stronger_Elite", "front"),
    ("LegionRaider_WeakFlagHill", "front"),
    ("LegionRaider_Jose", False),  # Bastien
    ("LegionHyena", False),
    ("LegionHyenaHandler", False),
    ("LegionKidnapper_1", False),
    ("LegionGoon_Stronger_Elite", "assault"),
    ("LegionGrenadier_Tutorial", "grenadier"),
    ("JAZZ_Legion_FrontT1_Marauder", False),
]


def main() -> int:
    failed = 0
    for uid, expect in CASES:
        got = match_unit_family(uid)
        ok = got == expect
        print(f"{'OK' if ok else 'FAIL'}: {uid} -> {got!r} (expect {expect!r})")
        if not ok:
            failed += 1
    if failed:
        print(f"FAILED {failed}/{len(CASES)}")
        return 1
    print(f"OK {len(CASES)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
