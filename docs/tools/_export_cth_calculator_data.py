# -*- coding: utf-8 -*-
"""Export compact CTH calculator data: weapons + CTH-relevant components + slots.

Reads canonical CSVs. Writes docs/tools/cth-calculator-data.json.
Used by _gen_cth_calculator.py.
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
WPN = ROOT / "docs/technical/weapons/data/weapons.csv"
COMP = ROOT / "docs/technical/weapons/data/weapon-components.csv"
OPT = ROOT / "docs/technical/weapons/data/weapon-component-options.csv"
OUT = HERE / "cth-calculator-data.json"

CTH_SLOTS = (
    "Scope",
    "Barrel",
    "Stock",
    "Handgrip",
    "Handguard",
    "Magazine",
    "Side",
    "Muzzle",
    "Bipod",
    "Under",
)

CTH_EFFECTS = {
    "ScopeMagnification",
    "SmallMagnification",
    "MinAim",
    "IncreaseAimAccuracy15Percent",
    "ReduceAimAccuracy15Percent",
    "IncreaseAimAccuracy",
    "DecreaseMaxAimActions",
    "IncreaseMaxAimActions",
    "CloseRangeFactorIncrease",
    "CloseRangeFactorDecrease",
    "CloseRangeIncrease",
    "CloseRangeDecrease",
    "BarrelBulletDropIncrease",
    "BarrelBulletDropReduce",
    "BarrelRangeIncrease",
    "BarrelRangeReduce",
    "BarrelGroupingIncrease",
    "BarrelGroupingReduce",
    "BarrelRecoilIncrease",
    "BarrelRecoilRecude",
    "RecoilIncrease",
    "RecoilDecrease",
    "LaserMark",
    "OpportunityAttackBonusCth",
    "NightsIronsBonus",
    "IgnoreInTheDark",
    "IgnoreInTheDarkWhenFullyAimed",
    "AccuracyBonusProne",
    "ShotsBeforeRecoilProne",
    "MinorAccuracyBonus",
}

MG_CLASSES = {"MachineGun", "LightMachineGun"}

ARCHETYPES = [
    {"id": None, "label": "Открытый прицел", "labelEn": "Iron sights", "family": "irons", "tier": "—"},
    {"id": "JAZZ_IronSight_AIM", "label": "Точный прицел (+5 AA)", "labelEn": "Precision irons (+5 AA)", "family": "irons", "tier": "AIM"},
    {"id": "JAZZ_Reflex_Aimpoint5000", "label": "Aimpoint 5000", "labelEn": "Aimpoint 5000", "family": "reflex", "tier": "T1"},
    {"id": "JAZZ_Reflex_Closed", "label": "Закрытый", "labelEn": "Closed reflex", "family": "reflex", "tier": "T2"},
    {"id": "JAZZ_Reflex_M68", "label": "Aimpoint M68", "labelEn": "Aimpoint M68", "family": "reflex", "tier": "T3"},
    {"id": "JAZZ_Reflex_PKAS", "label": "ПК-АА", "labelEn": "PK-AA", "family": "reflex", "tier": "T4"},
    {"id": "JAZZ_Reflex_Cobra", "label": "Кобра (OW)", "labelEn": "Cobra (OW)", "family": "reflex-ow", "tier": "T1"},
    {"id": "JAZZ_Reflex_Open", "label": "Компактный (OW)", "labelEn": "Compact (OW)", "family": "reflex-ow", "tier": "T2"},
    {"id": "JAZZ_Reflex_Pistol", "label": "Пистолетный (OW)", "labelEn": "Pistol reflex (OW)", "family": "reflex-ow", "tier": "T2"},
    {"id": "JAZZ_Reflex_Eotech", "label": "Eotech", "labelEn": "Eotech", "family": "reflex-uni", "tier": "T4"},
    {"id": "JAZZ_CombatScope_2x", "label": "Combat 2×", "labelEn": "Combat 2×", "family": "combat", "tier": "T1"},
    {"id": "JAZZ_CombatScope_3x", "label": "Combat 3×", "labelEn": "Combat 3×", "family": "combat", "tier": "T2"},
    {"id": "JAZZ_G36Scope", "label": "G36 3×", "labelEn": "G36 3×", "family": "combat", "tier": "T2"},
    {"id": "JAZZ_CombatScope_ACOG", "label": "ACOG 4×", "labelEn": "ACOG 4×", "family": "combat", "tier": "T3"},
    {"id": "JAZZ_CombatScope_1P29", "label": "1П29 4×", "labelEn": "1P29 4×", "family": "combat", "tier": "T3"},
    {"id": "JAZZ_CombatScope_FeroZ24", "label": "Fero Z24 4×", "labelEn": "Fero Z24 4×", "family": "combat", "tier": "T3"},
    {"id": "JAZZ_Scope_PU", "label": "ПУ 3.5×", "labelEn": "PU 3.5×", "family": "long", "tier": "T1"},
    {"id": "JAZZ_Scope_Garand", "label": "M84 2.2×", "labelEn": "M84 2.2×", "family": "long", "tier": "T1"},
    {"id": "JAZZ_Scope_Springfield", "label": "Springfield 2.75×", "labelEn": "Springfield 2.75×", "family": "long", "tier": "T1"},
    {"id": "JAZZ_Scope_PSO", "label": "ПСО 4×", "labelEn": "PSO 4×", "family": "long", "tier": "T2"},
    {"id": "JAZZ_Scope_ZF4", "label": "ZF4 4×", "labelEn": "ZF4 4×", "family": "long", "tier": "T2"},
    {"id": "JAZZ_Scope_6x", "label": "1-6×", "labelEn": "1-6×", "family": "long", "tier": "T3"},
    {"id": "JAZZ_Scope_DA15_6x", "label": "Zeiss 1.5-6×", "labelEn": "Zeiss 1.5-6×", "family": "long", "tier": "T3"},
    {"id": "JAZZ_Scope_Scout", "label": "Scout 2-7×", "labelEn": "Scout 2-7×", "family": "long", "tier": "T4"},
    {"id": "JAZZ_Scope_12x", "label": "Mark 4 10×", "labelEn": "Mark 4 10×", "family": "long", "tier": "T5"},
    {"id": "JAZZ_NightScope_NSPU", "label": "НСПУ 3.5×", "labelEn": "NSPU 3.5×", "family": "night", "tier": "T1"},
    {"id": "JAZZ_NightScope", "label": "Ночной 5×", "labelEn": "Night 5×", "family": "night", "tier": "T2"},
]


def parse_params(s: str) -> dict:
    out = {}
    if not s:
        return out
    for part in s.split(";"):
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        try:
            fv = float(v)
            out[k] = int(fv) if fv.is_integer() else fv
        except ValueError:
            out[k] = v
    return out


def classify_scope(cid: str, name: str, effects: set[str]) -> str:
    blob = f"{cid} {name}"
    if "Reflex" in blob or "Collimator" in blob or "Коллиматор" in blob:
        if "Eotech" in blob:
            return "reflex-uni"
        if any(x in cid for x in ("Open", "Pistol", "Cobra")):
            return "reflex-ow"
        return "reflex"
    if "CombatScope" in cid or cid == "JAZZ_G36Scope":
        return "combat"
    if "NightScope" in cid:
        return "night"
    if cid.startswith("JAZZ_Scope_") or "ScopeMagnification" in effects:
        return "long"
    if "IronSight" in cid or "Irons" in blob:
        return "irons"
    return "other"


def num(row, key, default=0):
    try:
        return int(float(row.get(key) or default))
    except (TypeError, ValueError):
        return default


def main() -> int:
    weapons = []
    with WPN.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("catalog_status") != "active":
                continue
            cls = row.get("object_class") or ""
            weapons.append(
                {
                    "id": row["id"],
                    "name": row["display_name"],
                    "fam": row["family_id"],
                    "famRu": row.get("family_name_ru") or row["family_id"],
                    "cls": cls,
                    "tier": row.get("tier_label") or "",
                    "aa": num(row, "aim_accuracy"),
                    "maxAim": num(row, "max_aim_actions"),
                    "r": num(row, "weapon_range"),
                    "bdr": num(row, "bullet_drop_range"),
                    "g": num(row, "grouping"),
                    "close": num(row, "close_range"),
                    "closeF": num(row, "close_range_factor", 100),
                    "recoil": num(row, "recoil"),
                    "burst": num(row, "burst_shots"),
                    "auto": num(row, "auto_shots"),
                    "mg": cls in MG_CLASSES,
                    "lmg": cls == "LightMachineGun",
                    "pistol": cls == "Pistol",
                }
            )

    raw_comps = {}
    with COMP.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            raw_comps[row["component_id"]] = row

    def make_comp(row: dict) -> dict:
        effects = [e for e in (row.get("effects") or "").split(";") if e]
        fx = set(effects)
        slot = row.get("slot") or ""
        return {
            "id": row["component_id"],
            "name": row.get("display_name") or row["component_id"],
            "slot": slot,
            "fx": effects,
            "p": parse_params(row.get("parameters") or ""),
            "fam": classify_scope(row["component_id"], row.get("display_name") or "", fx)
            if slot == "Scope"
            else "",
        }

    comps = {}
    for cid, row in raw_comps.items():
        effects = [e for e in (row.get("effects") or "").split(";") if e]
        slot = row.get("slot") or ""
        if slot == "Scope" or (set(effects) & CTH_EFFECTS):
            comps[cid] = make_comp(row)

    slots: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    defaults: dict[str, dict[str, str]] = defaultdict(dict)
    emptyable: dict[str, dict[str, bool]] = defaultdict(dict)
    with OPT.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            slot = row.get("slot_type") or ""
            if slot not in CTH_SLOTS:
                continue
            wid = row["weapon_id"]
            cid = row.get("component_id") or ""
            if cid and cid not in slots[wid][slot]:
                slots[wid][slot].append(cid)
            if cid and cid not in comps and cid in raw_comps:
                comps[cid] = make_comp(raw_comps[cid])
            elif cid and cid not in comps:
                comps[cid] = {
                    "id": cid,
                    "name": row.get("component_name") or cid,
                    "slot": slot,
                    "fx": [],
                    "p": {},
                    "fam": "irons" if slot == "Scope" else "",
                }
            if row.get("can_be_empty") == "true":
                emptyable[wid][slot] = True
            if row.get("is_default") == "true" and cid:
                defaults[wid][slot] = cid

    payload = {
        "source": "docs/technical/weapons/data/*.csv",
        "weapons": weapons,
        "comps": comps,
        "slots": {wid: dict(s) for wid, s in slots.items()},
        "defaults": {wid: dict(d) for wid, d in defaults.items()},
        "emptyable": {wid: dict(e) for wid, e in emptyable.items()},
        "archetypes": ARCHETYPES,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(
        f"Wrote {OUT} weapons={len(weapons)} comps={len(comps)} "
        f"guns_with_slots={len(slots)} bytes={OUT.stat().st_size}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
