# -*- coding: utf-8 -*-
"""Sync SteroidPunch ModItem in items.lua from CharacterEffect companion + RU/EN CSV.

Uses fresh loc IDs 890000000009930/9931 (6512/6513 collide with Jazz_Gamos VR).

Usage (from jazz/):
  python docs/tools/_apply_steroidpunch_passive.py
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
CE = ROOT / "CharacterEffect" / "SteroidPunch.lua"
RU = ROOT / "Russian.csv"
EN = ROOT / "English.csv"

# Collision: 6512/6513 = Jazz_Gamos VR in jazz-units.
LOC_ID_NAME = "890000000009930"
LOC_ID_DESC = "890000000009931"
# Restore Gamos lines if Steroid previously overwrote them.
RESTORE_GAMOS = {
    "890000000006512": (
        "Я закончил, босс.",
        "I'm finished, boss.",
        "jazz-units:VoiceResponse Jazz_Gamos",
    ),
    "890000000006513": (
        "У меня все в порядке.",
        "I'm all right.",
        "jazz-units:VoiceResponse Jazz_Gamos",
    ),
}

RU_NAME = "Удар анаболика"
EN_NAME = "Anabolic Punch"
RU_DESC = (
    "Пассивный навык. Точность всех ударов кулаками и оружием ближнего боя зависит от "
    "<em>Силы</em> вместо Ловкости. Успешные удары <em>кулаками</em> отбрасывают цель "
    "(как ванильный Steroid Smash) с побочным уроном окружению. Стимуляторы не вызывают "
    "потери <em>энергии</em> (усталости). Урон со временем от эффекта <em>горения</em> "
    "снижен на <em>30%</em>."
)
EN_DESC = (
    "Passive. Fist and melee accuracy uses <em>Strength</em> instead of Agility. Successful "
    "<em>unarmed</em> hits knock the target back like vanilla Steroid Smash (with collateral). "
    "Combat stims do not cause <em>Energy</em> (tiredness) loss. Burning DoT reduced by "
    "<em>30%</em>."
)
SRC = "jazz:CharacterEffect/SteroidPunch.lua"


def companion_body() -> str:
    text = CE.read_text(encoding="utf-8")
    m = re.search(
        r"DefineClass\.SteroidPunch\s*=\s*\{(.*)\n\}\s*$",
        text,
        flags=re.S,
    )
    if not m:
        raise SystemExit("SteroidPunch companion body not found")
    body = m.group(1)
    body = re.sub(r"\n\t__parents = \{[^}]+\},\n", "\n", body)
    body = re.sub(r"\n\t__generated_by_class = \"[^\"]+\",\n", "\n", body)
    return body.strip("\n")


def to_moditem(body: str) -> str:
    indented = "\n".join(("\t\t\t\t\t" + line if line else line) for line in body.splitlines())
    return (
        "\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n"
        "\t\t\t\t\t'Group', \"Perk-Personal\",\n"
        "\t\t\t\t\t'Id', \"SteroidPunch\",\n"
        f"{indented}\n"
        "\t\t\t\t}),"
    )


def replace_moditem(items: str, moditem: str) -> str:
    pat = re.compile(
        r"\t\t\t\tPlaceObj\('ModItemCharacterEffectCompositeDef', \{\n"
        r"\t\t\t\t\t'Group', \"Perk-Personal\",\n"
        r"\t\t\t\t\t'Id', \"SteroidPunch\",.*?\n"
        r"\t\t\t\t\}\),",
        flags=re.S,
    )
    new, n = pat.subn(moditem, items, count=1)
    if n != 1:
        raise SystemExit(f"SteroidPunch ModItem replace count={n}")
    return new


def upsert_csv(path: Path) -> None:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rest = [row for row in reader if row]
    by_id = {row[0]: row for row in rest}

    for rid, (ru, en, src) in RESTORE_GAMOS.items():
        by_id[rid] = [rid, ru, en, "", src]

    by_id[LOC_ID_NAME] = [LOC_ID_NAME, RU_NAME, EN_NAME, "", SRC]
    by_id[LOC_ID_DESC] = [LOC_ID_DESC, RU_DESC, EN_DESC, "", SRC]

    out = [header]
    seen = set()
    for row in rest:
        rid = row[0]
        if rid in by_id:
            out.append(by_id[rid])
            seen.add(rid)
        else:
            out.append(row)
    for rid in list(RESTORE_GAMOS) + [LOC_ID_NAME, LOC_ID_DESC]:
        if rid not in seen:
            out.append(by_id[rid])
            seen.add(rid)

    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(out)


def main() -> None:
    body = companion_body()
    moditem = to_moditem(body)
    items = ITEMS.read_text(encoding="utf-8")
    ITEMS.write_text(replace_moditem(items, moditem), encoding="utf-8", newline="\n")
    upsert_csv(RU)
    upsert_csv(EN)
    print("OK SteroidPunch -> items.lua + CSV (ids 9930/9931; restored Gamos 6512/6513)")


if __name__ == "__main__":
    main()
