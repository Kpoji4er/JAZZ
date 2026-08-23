# -*- coding: utf-8 -*-
"""Static MED-007: deferred MaxHP debt + HP-level travel tiredness (порог 100)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def must(cond: bool, msg: str, errors: list[str]) -> None:
    if not cond:
        errors.append(msg)


def main() -> int:
    errors: list[str] = []
    med7 = read("Code/System_Medicine_MED007.lua")
    med6 = read("Code/System_Medicine_MED006.lua")
    energy = read("Code/System_EnergyLadder.lua")
    sat = read("Code/SatelliteSquad.lua")
    med = read("Code/Systems_Medicine.lua")
    meta = read("metadata.lua")
    en = read("English.csv")
    ru = read("Russian.csv")

    must("System_Medicine_MED007.lua" in meta, "MED007 not in metadata.code", errors)
    must("'name', \"System_Medicine_MED007\"" in read("items.lua"), "MED007 ModItemCode missing from items.lua", errors)
    must("function JazzUnitSkipsTraumaMaxHpDebt" in med7, "skip helper missing", errors)
    must("g_JAZZ_MED007_ForceDebt" in med7, "force-debt flag missing", errors)
    must("function OnMsg.CombatStart" in med7, "CombatStart hook missing", errors)
    must("function OnMsg.CombatEnd" in med7, "CombatEnd hook missing", errors)
    must("JazzApplyPendingTraumaMaxHpDebt" in med7, "force apply helper missing", errors)
    must("JazzUnitSkipsTraumaMaxHpDebt" in med6, "MED006 wrap does not call skip helper", errors)
    must("ApplyTempHitPoints" not in med7, "MED007 must not grant grit for debt", errors)

    must("function JazzGetHpTirednessTravelDiff" in energy, "HP tiredness diff missing", errors)
    must("HP_TIREDNESS_LIMIT = 100" in energy, "порог must be 100 HP, not vanilla 75", errors)
    must("RIBS_TIREDNESS_MUL" not in energy, "Ribs must not shorten travel tiredness", errors)
    must("JazzGetCurrentHpLevelPercent" not in energy, "must not use bar-percent helper", errors)
    must("unit.HitPoints" in energy or "unit and unit.HitPoints" in energy, "diff must read current HitPoints", errors)
    must("GetInitialMaxHitPoints" not in energy.split("function JazzGetHpTirednessTravelDiff", 1)[-1][:400], "diff must not use Health/base max", errors)

    # ReachSectorCenter still calls GetHPAdditionalTiredTime; it must stay 0.
    idx = sat.find("function GetHPAdditionalTiredTime")
    must(idx >= 0, "GetHPAdditionalTiredTime missing", errors)
    chunk = sat[idx : idx + 400]
    must("return 0" in chunk, "GetHPAdditionalTiredTime must return 0", errors)

    must("890000000010293" in med, "in-combat debt loc missing in tooltip", errors)
    must("890000000010292" in med, "out-of-combat debt loc missing", errors)
    must("890000000010293" in en and "890000000010293" in ru, "010293 missing from runtime CSV", errors)
    must("После этого боя" in ru, "RU 010293 missing", errors)
    must("After this fight" in en, "EN 010293 missing", errors)

    wiki = read("docs/wiki/combat-and-accuracy.md")
    ru_sc = read("docs/showcase/ru/combat-and-accuracy.md")
    en_sc = read("docs/showcase/en/combat-and-accuracy.md")
    must("после боя" in wiki and "100 ОЗ" in wiki, "wiki MED-007 facts", errors)
    must("после боя" in ru_sc and "100 ОЗ" in ru_sc, "showcase RU MED-007", errors)
    must("after the fight" in en_sc and "100 HP" in en_sc, "showcase EN MED-007", errors)

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("OK MED-007 static audit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
