# -*- coding: utf-8 -*-
from pathlib import Path
import re

rows = [
    (890000000001931, "Мимикрия", "Mimicry", "jazz:CharacterEffect/Jazz_Perk_Mimicry.lua"),
    (
        890000000001932,
        "Проходит проверки на разговорные перки <em>Переговорщик</em>, <em>Тёртый калач</em> и <em>Псих</em> без их боевых и экономических эффектов.",
        "Passes <em>Negotiator</em>, <em>Scoundrel</em>, and <em>Psycho</em> conversation perk checks without their combat or economy effects.",
        "jazz:CharacterEffect/Jazz_Perk_Mimicry.lua",
    ),
    (890000000001933, "Ветеран", "Veteran", "jazz:CharacterEffect/Jazz_Perk_Veteran.lua"),
    (
        890000000001934,
        "Бонус <em>+10</em> ко всем проверкам навыков и характеристик (диалоги, исследование, skill checks).",
        "<em>+10</em> bonus to all skill and attribute checks (dialogue, exploration, skill checks).",
        "jazz:CharacterEffect/Jazz_Perk_Veteran.lua",
    ),
    (890000000001935, "Снайпер", "Sniper", "jazz:CharacterEffect/Jazz_Perk_Sniper.lua"),
    (
        890000000001936,
        "Максимальный уровень прицеливания <em>+1</em> при стрельбе из любого оружия.",
        "Maximum aiming level <em>+1</em> when firing any weapon.",
        "jazz:CharacterEffect/Jazz_Perk_Sniper.lua",
    ),
]


def q(s: str) -> str:
    if any(c in s for c in ",\n\""):
        return '"' + s.replace('"', '""') + '"'
    return s


root = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
ids = {str(r[0]) for r in rows}

for name in ("English.csv", "Russian.csv"):
    path = root / name
    lines = path.read_text(encoding="utf-8").splitlines()
    lines = [ln for ln in lines if not any(ln.startswith(i + ",") for i in ids)]
    # Format matches Jazz_Perk_Lynx (890000000000868): id, RU, EN, empty, src
    for rid, ru, en, src in rows:
        lines.append(f"{rid},{q(ru)},{q(en)},,{src}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(name, "ok", len(rows), "rows")
