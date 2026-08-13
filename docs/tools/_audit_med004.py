#!/usr/bin/env python3
"""Static regression checks for JAZZ-MED-004 (no game runtime required)."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def fn_body(src: str, name: str, next_name: str) -> str:
    start = src.find(f"function {name}")
    if start < 0:
        raise AssertionError(f"missing {name}")
    end = src.find(f"function {next_name}", start + 1)
    if end < 0:
        end = len(src)
    return src[start:end]


def main() -> int:
    med = (ROOT / "Code" / "Systems_Medicine.lua").read_text(encoding="utf-8")
    armor = (ROOT / "Code" / "System_ArmorRating.lua").read_text(encoding="utf-8")
    frag = (ROOT / "InventoryItem" / "FragGrenade.lua").read_text(encoding="utf-8")
    he = (ROOT / "InventoryItem" / "HE_Grenade.lua").read_text(encoding="utf-8")
    items = (ROOT / "items.lua").read_text(encoding="utf-8")

    check("JazzTraumaDamageFloor = 20" in med, "floor constant 20")
    check("JazzTraumaHeavyMaxHpPct = 50" in med, "heavy MaxHP pct 50")

    roll = fn_body(med, "JazzTryRollTraumaFromBodyPart", "JazzStripCombatWounded")
    check("thr_light" not in roll, "no d100 thr_light in body-part roller")
    check("JazzWantedTraumaTierFromDamage" in roll, "roller uses damage-band helper")
    check("jazz_pending_trauma_hit" in roll, "roller reads pending hit")

    want = fn_body(med, "JazzWantedTraumaTierFromDamage", "JazzTryRollTraumaFromBodyPart")
    check("JazzTraumaDamageFloor" in want, "wanted tier uses floor")
    check("cur_rank + 1" in want, "same-zone +1 rank")
    check("JazzTraumaHeavyMaxHpPct" in want, "wanted tier uses MaxHP heavy pct")

    start = med.find("function JazzTryApplyExplosionConcussionAndTrauma")
    nxt = med.find("-- JAZZ-GRENADES-002", start)
    blast = med[start:nxt]
    check("JazzHitHasShotRoller" in blast, "blast skips leftover *shot")
    check("trauma_gate" not in blast, "no random 40/100 blast trauma gate")
    check('zone = zone or "Ribs"' in blast, "blast zone fallback Ribs")
    check('AddStatusEffect("Concussion")' in blast, "concussion still guaranteed")

    timer = fn_body(med, "JazzInitTraumaProgressTimer", "JazzTraumaHoursUntilNextCheck")
    check("from_time" in timer, "timer accepts due time")
    check("base + hours * scale_h" in timer, "next check from due, not only CampaignTime")

    hour = fn_body(med, "JazzTraumaProgressOnNewHour", "OnMsg.DataLoaded")
    check("while next_t" in hour, "NewHour catch-up loop")
    check("guard < 96" in hour, "catch-up iteration cap")

    check("jazz_pending_trauma_hit" in armor, "ApplyDamageAndEffects stashes pending hit")
    check("jazz_applied_hp" in armor, "hit stores applied HP")

    for blob, label in ((frag, "FragGrenade.lua"), (he, "HE_Grenade.lua")):
        check('"Headshot"' not in blob, f"{label} has no Headshot")
        check('"Armsshot"' not in blob, f"{label} has no Armsshot")
        check('"Legsshot"' not in blob, f"{label} has no Legsshot")

    for item_id in ("FragGrenade", "HE_Grenade"):
        marker = f"'Id', \"{item_id}\""
        i = items.find(marker)
        check(i >= 0, f"items.lua has {item_id}")
        nxt = items.find("PlaceObj('ModItemInventoryItemCompositeDef'", i + 1)
        block = items[i:nxt]
        center = block.find("'CenterAppliedEffects'")
        check(center >= 0, f"{item_id} still has CenterAppliedEffects")
        end = block.find("'AreaOfEffect'", center)
        center_blob = block[center:end]
        for shot in ('"Headshot"', '"Armsshot"', '"Legsshot"'):
            check(shot not in center_blob, f"items.lua {item_id} center has no {shot}")

    check("function JazzTraumaPainOnZoneUse" in med, "zone-use Pain helper still present")
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
