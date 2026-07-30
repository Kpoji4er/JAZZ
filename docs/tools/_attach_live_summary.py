# -*- coding: utf-8 -*-
"""Summarize real (modifiable|default) attachments on active weapons."""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "docs/technical/weapons/data"
OUT = ROOT / "docs/tools/_attach_live_summary.json"

PARAM_HINTS = {
    "Recoil": "отдача (ниже = лучше удержание)",
    "ScopeMagnification": "кратность (целая)",
    "ScopeSubMagnification": "десятые кратности",
    "ScopeAimLevel": "мин. aim-кликов для оптики",
    "ScopeHandlingReduce": "штраф Handling (legacy)",
    "AimAccuracyIncrease": "+AimAccuracy / клик",
    "ShotAP": "+ShootAP",
    "IncreaseMaxAimActions": "+MaxAimActions",
    "MaxAimActionsDecrease": "−MaxAimActions",
    "MagazineSize": "+ёмкость",
    "MagazineSizeMultiplier": "ёмкость ×(v/100)",
    "ReliabilityIncrease": "+Reliability",
    "ReliabilityDecrease": "−Reliability",
    "RangeIncrease": "+WeaponRange",
    "RangeDecrease": "−WeaponRange",
    "NoiseMultiplier": "шум ×",
    "stealth_kill_bonus": "stealth kill",
    "LaserCTH": "flat CTH лазер",
    "LaserDistance": "дистанция лазера",
    "bonus_cth": "legacy flat +CTH",
    "BonusCTH": "legacy flat +CTH",
    "OverwatchAngleIncrease": "+overwatch угол",
    "extra_attacks": "+overwatch shots",
    "min_aim": "мин. aim",
    "BarrelRecoilRecude": "−Recoil ствола (typo Recude)",
    "BuckshotAngleIncrease": "угол дроби",
    "DamageIncrease": "+Damage",
}

EFFECT_ROLE = {
    "DecreaseMaxAimActions": "меньше кликов aim",
    "IncreaseMaxAimActions": "больше кликов aim",
    "ExtraOverwatchShots": "+выстрелы overwatch",
    "ScopeOverwatchAngleIncreace": "+угол OW",
    "ScopeOverwatchAngleIncreaceBig": "+угол OW (большой)",
    "IncreaseOverwatchAngle": "+угол OW",
    "MinAim": "мин. aim",
    "OpportunityAttackBonusCth": "+CTH OA",
    "ScopeHandlingReduce": "штраф handling",
    "ScopeMagnification": "кратность / aim zone",
    "IncreaseShotAP": "дороже выстрел",
    "IncreaseAimAccuracy": "+AA",
    "CritBonusWhenFullyAimed": "+crit на полном aim",
    "ReduceAuto75Percent": "режет auto",
    "ReduceBurst50Percent": "режет burst",
    "MinorAccuracyBonus": "legacy flat CTH",
    "AccuracyBonusWhenAimed": "legacy flat CTH aimed",
    "NightsIronsBonus": "ночные irons",
    "MagazineSizeIncrease": "+магазин",
    "ChangeWeaponTypeToAssaultRifle": "меняет класс",
}


def parse_params(raw: str):
    out = []
    for chunk in (raw or "").split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" in chunk:
            k, v = chunk.split("=", 1)
        else:
            k, v = chunk, ""
        out.append({"key": k, "value": v, "hint": PARAM_HINTS.get(k, "")})
    return out


def main():
    effects = {r["effect_id"]: r for r in csv.DictReader((DATA / "weapon-component-effects.csv").open(encoding="utf-8"))}
    comps = {r["component_id"]: r for r in csv.DictReader((DATA / "weapon-components.csv").open(encoding="utf-8"))}
    weapons = {r["id"]: r for r in csv.DictReader((DATA / "weapons.csv").open(encoding="utf-8"))}
    active = {wid for wid, w in weapons.items() if w.get("catalog_status") == "active"}

    used = defaultdict(lambda: {"weapons": [], "defaults": [], "slots": set()})
    by_slot = defaultdict(set)

    for o in csv.DictReader((DATA / "weapon-component-options.csv").open(encoding="utf-8")):
        wid = o["weapon_id"]
        if wid not in active:
            continue
        if (o.get("slot_type") or "").lower() == "mount":
            continue
        mod = (o.get("modifiable") or "").lower() == "true"
        is_def = (o.get("is_default") or "").lower() == "true"
        if not mod and not is_def:
            continue
        cid = (o.get("component_id") or "").strip()
        if not cid:
            continue
        slot = o.get("slot_type") or "?"
        used[cid]["weapons"].append(wid)
        used[cid]["slots"].add(slot)
        if is_def:
            used[cid]["defaults"].append(wid)
        by_slot[slot].add(cid)

    rows = []
    for cid, info in sorted(used.items()):
        c = comps.get(cid, {})
        slot = next(iter(info["slots"]), c.get("slot") or "?")
        fx_ids = [e for e in (c.get("effects") or "").split(";") if e]
        params = parse_params(c.get("parameters") or "")
        fx_detail = []
        for eid in fx_ids:
            er = effects.get(eid, {})
            fx_detail.append(
                {
                    "id": eid,
                    "role": EFFECT_ROLE.get(eid, ""),
                    "desc": (er.get("description") or er.get("display_name") or "")[:160],
                    "defaults": er.get("parameters") or "",
                }
            )
        flags = []
        if not fx_ids and not params:
            flags.append("empty")
        if not fx_ids and params:
            flags.append("orphan_params")
        flat_keys = {"bonus_cth", "BonusCTH", "ScopeCTH", "bonus_cth_bipod", "LaserCTH"}
        if {p["key"] for p in params} & flat_keys or any(
            e in ("MinorAccuracyBonus", "AccuracyBonusWhenAimed", "ScopeCTHBonus", "NightsIronsBonus") for e in fx_ids
        ):
            flags.append("legacy_flat_cth")
        if "BarrelRecoilRecude" in {p["key"] for p in params}:
            flags.append("typo_recoil")
        jazz = cid.startswith("JAZZ_") or cid.startswith("Jazz_")
        if slot == "Scope" and not jazz and any(x in cid for x in ("Ironsight", "IronSight", "Scope_Default")):
            flags.append("entity_visual")
        elif slot == "Scope" and jazz and "IronSight" in cid:
            flags.append("entity_visual")

        # design notes heuristic
        design = []
        if "empty" in flags and slot not in ("Magazine",) and not cid.startswith("MagNormal"):
            design.append("нет эффектов — только визуал/placeholder; либо дать эффект, либо не показывать как апгрейд")
        if "legacy_flat_cth" in flags:
            design.append("плоский CTH конфликтует с accuracy-model — перевести в AA/aim/OW/recoil")
        if slot == "Scope" and jazz and "empty" not in flags:
            design.append("ок: JAZZ-оптика через aim zone / OW / AP")
        if slot == "Magazine" and any(p["key"].startswith("Magazine") for p in params) or any("Magazine" in e for e in fx_ids):
            design.append("ёмкость — ок; следить за handling/cumbersome на барабанах")
        if slot == "Muzzle" and "Suppressor" in cid or "Suppressor" in cid:
            design.append("тишина vs range/handling — держать явный trade")

        rows.append(
            {
                "id": cid,
                "name": c.get("display_name") or cid,
                "slot": slot,
                "n_weapons": len(set(info["weapons"])),
                "n_defaults": len(set(info["defaults"])),
                "weapons": sorted(set(info["weapons"])),
                "default_on": sorted(set(info["defaults"])),
                "effects": fx_detail,
                "params": params,
                "raw_effects": c.get("effects") or "",
                "raw_params": c.get("parameters") or "",
                "flags": flags,
                "cost": c.get("cost") or "",
                "source": c.get("source") or "",
            }
        )

    # slot summaries
    slot_sum = {}
    for slot, cids in sorted(by_slot.items()):
        slot_rows = [r for r in rows if r["slot"] == slot]
        slot_sum[slot] = {
            "count": len(slot_rows),
            "empty": sum(1 for r in slot_rows if "empty" in r["flags"]),
            "legacy_flat_cth": sum(1 for r in slot_rows if "legacy_flat_cth" in r["flags"]),
            "with_effects": sum(1 for r in slot_rows if r["effects"]),
        }

    # problem clusters
    problems = {
        "empty": [r["id"] for r in rows if "empty" in r["flags"]],
        "legacy_flat_cth": [r["id"] for r in rows if "legacy_flat_cth" in r["flags"]],
        "orphan_params": [r["id"] for r in rows if "orphan_params" in r["flags"]],
        "scope_entity_only": [r["id"] for r in rows if "entity_visual" in r["flags"]],
    }

    OUT.write_text(
        json.dumps(
            {
                "total": len(rows),
                "by_slot": slot_sum,
                "problems": {k: {"n": len(v), "ids": v} for k, v in problems.items()},
                "components": rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {OUT} components={len(rows)}")
    for s, st in slot_sum.items():
        print(f"  {s}: {st['count']} (empty={st['empty']} legacy={st['legacy_flat_cth']})")


if __name__ == "__main__":
    main()
