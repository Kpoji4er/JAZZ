# -*- coding: utf-8 -*-
"""Append/replace JAZZ-IMP-001 Mimicry/Veteran/Sniper localization rows.

Runtime CSV columns: ID, Text, Translation, VoiceActor, Context
- Russian.csv: Translation must be Russian (RU client reads Translation).
- English.csv: Translation must be English; Text keeps RU source (Lynx pattern).

Do NOT write id,RU,EN into Russian.csv — that made tooltips English on RU UI.
"""
from pathlib import Path
import csv

ROWS = [
    (
        "890000000001931",
        "Мимикрия",
        "Mimicry",
        "jazz:CharacterEffect/Jazz_Perk_Mimicry.lua",
    ),
    (
        "890000000001932",
        "Проходит проверки на разговорные перки <em>Переговорщик</em>, <em>Тёртый калач</em> и <em>Псих</em> без их боевых и экономических эффектов.",
        "Passes <em>Negotiator</em>, <em>Scoundrel</em>, and <em>Psycho</em> conversation perk checks without their combat or economy effects.",
        "jazz:CharacterEffect/Jazz_Perk_Mimicry.lua",
    ),
    (
        "890000000001933",
        "Ветеран",
        "Veteran",
        "jazz:CharacterEffect/Jazz_Perk_Veteran.lua",
    ),
    (
        "890000000001934",
        "Бонус <em>+10</em> ко всем проверкам навыков и характеристик (диалоги, исследование, skill checks).",
        "<em>+10</em> bonus to all skill and attribute checks (dialogue, exploration, skill checks).",
        "jazz:CharacterEffect/Jazz_Perk_Veteran.lua",
    ),
    (
        "890000000001935",
        "Снайпер",
        "Sniper",
        "jazz:CharacterEffect/Jazz_Perk_Sniper.lua",
    ),
    (
        "890000000001936",
        "Максимальный уровень прицеливания <em>+1</em> при стрельбе из любого оружия.",
        "Maximum aiming level <em>+1</em> when firing any weapon.",
        "jazz:CharacterEffect/Jazz_Perk_Sniper.lua",
    ),
]


def rewrite(path: Path, mode: str) -> None:
    ids = {r[0] for r in ROWS}
    with path.open(encoding="utf-8", newline="") as f:
        sep = f.readline()
        rows = [cols for cols in csv.reader(f) if cols and cols[0] not in ids]
    for iid, ru, en, src in ROWS:
        if mode == "ru":
            rows.append([iid, ru, ru, "", src])
        else:
            rows.append([iid, ru, en, "", src])
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write(sep if sep.endswith("\n") else sep + "\n")
        csv.writer(f, lineterminator="\n").writerows(rows)
    print(path.name, "ok", len(ROWS), "rows")


root = Path(__file__).resolve().parents[2]
rewrite(root / "Russian.csv", "ru")
rewrite(root / "English.csv", "en")
