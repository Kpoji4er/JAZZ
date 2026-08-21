# -*- coding: utf-8 -*-
"""Upsert officer-aura / directive player-facing localization (CMD-001 UI).

Runtime CSV columns: ID, Text, Translation, VoiceActor, Context
- Russian.csv: Translation = Russian (RU client reads Translation).
- English.csv: Text = RU source; Translation = English.

IDs:
  6100–6105 — Jazz_Perk_OfficerAura / Influence DisplayName/Description/AddEffectText
  6106–6111 — directive display names (HoldLine…FocusFire)
  6112–6113 — current-order tooltip lines
  6114 — no-order fallback label
  6115–6117 — OccupyBuildings / TakeCover / GoHidden
  6118 — OccupyHeights
  6119–6123 — per-directive buff labels
  6124 — order effect tooltip line
  6125 — FocusFire target name line
"""
from __future__ import annotations

import csv
from pathlib import Path

ROWS = [
    (
        "890000000006100",
        "Командная аура",
        "Command aura",
        "jazz:CharacterEffect/Jazz_Perk_OfficerAura.lua",
    ),
    (
        "890000000006101",
        "Этот командир отдаёт приказы союзникам поблизости.",
        "This commander issues orders to nearby allies.",
        "jazz:CharacterEffect/Jazz_Perk_OfficerAura.lua",
    ),
    (
        "890000000006102",
        "Отдаёт приказы",
        "Issuing orders",
        "jazz:CharacterEffect/Jazz_Perk_OfficerAura.lua",
    ),
    (
        "890000000006103",
        "Под влиянием ауры",
        "Under aura influence",
        "jazz:CharacterEffect/Jazz_Perk_OfficerAuraInfluence.lua",
    ),
    (
        "890000000006104",
        "Боец следует приказам командира и получает небольшой бонус текущего приказа. Эффект снимается, если командир погиб или боец вышел из зоны влияния.",
        "This fighter follows the commander's orders and gains a small bonus from the current order. Removed if the commander dies or the fighter leaves the influence zone.",
        "jazz:CharacterEffect/Jazz_Perk_OfficerAuraInfluence.lua",
    ),
    (
        "890000000006105",
        "Под приказом",
        "Under orders",
        "jazz:CharacterEffect/Jazz_Perk_OfficerAuraInfluence.lua",
    ),
    (
        "890000000006106",
        "Держать линию",
        "Hold the line",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006107",
        "Давить",
        "Push",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006108",
        "Охват",
        "Envelop",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006109",
        "Низкая видимость — держать",
        "Low visibility — hold",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006110",
        "Отход",
        "Fall back",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006111",
        "Сосредоточить огонь",
        "Focus fire",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006112",
        "Текущий приказ: <em><order></em>",
        "Current order: <em><order></em>",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006113",
        "Следует приказу: <em><order></em>",
        "Following order: <em><order></em>",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006114",
        "приказ не выбран",
        "no order selected",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006115",
        "Занимать дома",
        "Occupy buildings",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006116",
        "Спрятаться",
        "Take cover",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006117",
        "Скрыться",
        "Go hidden",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006118",
        "Занять высоты",
        "Take the high ground",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006119",
        "+2 к шансу попадания",
        "+2 chance to hit",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006120",
        "+1 ОД на ход",
        "+1 AP per turn",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006121",
        "+5 к шансу попадания",
        "+5 chance to hit",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006122",
        "−5 к шансу попадания по этому бойцу",
        "−5 chance to hit against this fighter",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006123",
        "−3 к шансу попадания по этому бойцу",
        "−3 chance to hit against this fighter",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006124",
        "Эффект приказа: <em><buff></em>",
        "Order effect: <em><buff></em>",
        "jazz:Code/AIContextProfiles.lua",
    ),
    (
        "890000000006125",
        "Цель: <em><name></em>",
        "Target: <em><name></em>",
        "jazz:Code/AIContextProfiles.lua",
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


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    rewrite(root / "Russian.csv", "ru")
    rewrite(root / "English.csv", "en")


if __name__ == "__main__":
    main()
