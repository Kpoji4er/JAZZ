# -*- coding: utf-8 -*-
"""Static: melee/legacy CTH applies Pain/trauma after accuracy clamp; Arms pain on melee."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def must(path: Path, needle: str) -> None:
    text = path.read_text(encoding="utf-8")
    if needle not in text:
        raise SystemExit(f"{path.relative_to(ROOT)}: missing {needle!r}")


def must_not(path: Path, needle: str) -> None:
    text = path.read_text(encoding="utf-8")
    if needle in text:
        raise SystemExit(f"{path.relative_to(ROOT)}: unexpected {needle!r}")


def main() -> None:
    unit = ROOT / "Code" / "System_OR_Unit.lua"
    med = ROOT / "Code" / "Systems_Medicine.lua"
    pain = ROOT / "CharacterEffect" / "Pain.lua"
    text = unit.read_text(encoding="utf-8")
    legacy = text.split("local JAZZ_CTHLegacyCalcChanceToHit", 1)[0]
    if "reaction_add" not in legacy:
        raise SystemExit("legacy CalcChanceToHit: missing reaction_add after-clamp apply")
    if "Clamp(base + penalty, 0, MaxCTH)" not in legacy:
        raise SystemExit("legacy CalcChanceToHit: missing accuracy clamp")
    if "final + reaction_add" not in legacy:
        raise SystemExit("legacy CalcChanceToHit: Pain/trauma not applied after accuracy")
    must(unit, "mod_add = 0")
    must(unit, "mod_mul = 100")
    must(med, "function OnMsg.OnAttack")
    must(med, 'action.ActionType == "Melee Attack"')
    must(med, "JazzTraumaPainOnZoneUse(attacker, \"Arms\")")
    must(pain, "'Name', \"cth_penalty\"")
    must(pain, "'Value', 5,")
    print("OK melee Pain/trauma CTH + Arms zone-use")


if __name__ == "__main__":
    raise SystemExit(main())
