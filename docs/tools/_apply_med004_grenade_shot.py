#!/usr/bin/env python3
"""MED-004: strip Frag/HE CenterAppliedEffects *shot rollers; update blast trauma hint."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

FRAG_OLD = '''	CenterAppliedEffects = {
		"Headshot",
		"Armsshot",
		"Legsshot",
	},'''
FRAG_NEW = """	CenterAppliedEffects = {
	},"""

HE_OLD = '''	CenterAppliedEffects = {
		"Armsshot",
		"Headshot",
		"Legsshot",
	},'''
HE_NEW = """	CenterAppliedEffects = {
	},"""

ITEMS_FRAG_OLD = '''					'CenterAppliedEffects', {
						"Headshot",
						"Armsshot",
						"Legsshot",
					},'''
ITEMS_FRAG_NEW = """					'CenterAppliedEffects', {
					},"""

ITEMS_HE_OLD = '''					'CenterAppliedEffects', {
						"Armsshot",
						"Headshot",
						"Legsshot",
					},'''
ITEMS_HE_NEW = """					'CenterAppliedEffects', {
					},"""

HINT_RU_OLD = "Поражённые взрывом: гарантированная <color EmStyle>контузия</color>; шанс зональных <color EmStyle>травм</color>"
HINT_RU_NEW = "Поражённые взрывом: гарантированная <color EmStyle>контузия</color>; одна зональная <color EmStyle>травма</color> при уроне ≥ 20 (тяжёлая при ≥ 50% ОЗ)"
HINT_EN_OLD = "Units caught in the blast are guaranteed to suffer <color EmStyle>Concussion</color> and may suffer location-specific <color EmStyle>Trauma</color>"
HINT_EN_NEW = "Units caught in the blast are guaranteed to suffer <color EmStyle>Concussion</color>; one zone <color EmStyle>Trauma</color> if after-armor damage ≥ 20 (heavy at ≥ 50% Max HP)"
HINT_RU_ALT = [
    "Поражённые взрывом гарантированно получают <color EmStyle>контузию</color>; возможны зональные <color EmStyle>травмы</color>",
    "Поражённые взрывом гарантированно получают <color EmStyle>контузию</color> и могут получить зональные <color EmStyle>травмы</color>",
]


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{path.name}: expected 1 occurrence of {label}, found {n}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"OK {path.relative_to(ROOT)}: {label}")


def replace_all(path: Path, old: str, new: str, label: str, expected: int) -> None:
    text = path.read_text(encoding="utf-8")
    n = text.count(old)
    if n != expected:
        raise SystemExit(f"{path.name}: expected {expected} of {label}, found {n}")
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"OK {path.relative_to(ROOT)}: {label} x{n}")


def main() -> int:
    replace_once(ROOT / "InventoryItem" / "FragGrenade.lua", FRAG_OLD, FRAG_NEW, "Frag *shot")
    replace_once(ROOT / "InventoryItem" / "HE_Grenade.lua", HE_OLD, HE_NEW, "HE *shot")
    items = ROOT / "items.lua"
    replace_once(items, ITEMS_FRAG_OLD, ITEMS_FRAG_NEW, "items Frag *shot")
    replace_once(items, ITEMS_HE_OLD, ITEMS_HE_NEW, "items HE *shot")

    for rel in (
        "InventoryItem/FragGrenade.lua",
        "InventoryItem/HE_Grenade.lua",
        "items.lua",
    ):
        replace_all(ROOT / rel, HINT_RU_OLD, HINT_RU_NEW, "hint RU", 1 if "items" not in rel else 2)

    ru = ROOT / "Russian.csv"
    en = ROOT / "English.csv"
    replace_all(ru, HINT_RU_OLD, HINT_RU_NEW, "Russian.csv hint", 2)
    # English.csv column1 is often still the Russian source for these IDs.
    ru_en_old = HINT_RU_OLD
    if ru_en_old in en.read_text(encoding="utf-8"):
        replace_all(en, HINT_RU_OLD, HINT_RU_NEW, "English.csv RU source", 2)
    if HINT_EN_OLD in en.read_text(encoding="utf-8"):
        replace_all(en, HINT_EN_OLD, HINT_EN_NEW, "English.csv EN", 2)
    if HINT_EN_OLD in ru.read_text(encoding="utf-8"):
        replace_all(ru, HINT_EN_OLD, HINT_EN_NEW, "Russian.csv EN col", 2)
    for alt in HINT_RU_ALT:
        ru_text = ru.read_text(encoding="utf-8")
        n = ru_text.count(alt)
        if n:
            ru.write_text(ru_text.replace(alt, HINT_RU_NEW), encoding="utf-8")
            print(f"OK Russian.csv alt x{n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
