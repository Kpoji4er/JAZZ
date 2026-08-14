# -*- coding: utf-8 -*-
"""MED-005: field bandage/morphine AP-ladder loc (RU+EN + Strings catalog)."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

HINT_BANDAGE_EN = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage — one use spends one bandage per bleed stack (up to your stock), each −1 tier\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> No Medical skill required\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> AP cost by Medical: 5 (0–19) / 4 (20–39) / 3 (40–59) / 2 (60–79) / 1 (80+)\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Self or ally"
)
HINT_BANDAGE_RU = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Бинт — за одно применение тратит по бинту на каждый стак крови (пока хватает запаса), каждый −1 тир\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Навык медицины не требуется\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> ОД от Медицины: 5 (0–19) / 4 (20–39) / 3 (40–59) / 2 (60–79) / 1 (80+)\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Можно применить к себе или союзнику"
)

HINT_MORPHINE_EN = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Morphine — suppresses Pain penalties\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Stabilizes and rallies downed characters (like a medkit)\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Does not stop bleeding, restore HP, or heal trauma\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> No Medical skill required\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> AP cost by Medical: 3 (0–39) / 2 (40–79) / 1 (80+)\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Self or ally"
)
HINT_MORPHINE_RU = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Морфий — глушит штрафы Боли\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Стабилизирует и поднимает из downed (как аптечка)\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Не останавливает кровь, не восстанавливает ОЗ и не лечит травмы\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Навык медицины не требуется\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> ОД от Медицины: 3 (0–39) / 2 (40–79) / 1 (80+)\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Можно применить к себе или союзнику"
)

DESC_BANDAGE_EN = (
    "Apply a field bandage to stop bleeding by one tier on self or ally. "
    "No Medical gate. AP 5/4/3/2/1 at Medical 0/20/40/60/80. Does not restore HP or heal trauma."
)
DESC_BANDAGE_RU = (
    "Наложить бинт: снижает кровотечение на один тир у себя или союзника. "
    "Без порога Медицины. ОД 5/4/3/2/1 при Медицине 0/20/40/60/80. Не восстанавливает ОЗ и не лечит травмы."
)

DESC_MORPHINE_EN = (
    "Inject morphine to suppress Pain or rally a downed ally (no HP heal). "
    "No Medical gate. AP 3/2/1 at Medical 0/40/80. Does not stop bleeding."
)
DESC_MORPHINE_RU = (
    "Вколоть морфий: глушит Боль или поднимает из downed (без хила ОЗ). "
    "Без порога Медицины. ОД 3/2/1 при Медицине 0/40/80. Кровь не останавливает."
)

UPDATES = {
    "890000000010013": (HINT_BANDAGE_EN, HINT_BANDAGE_RU),
    "890000000010016": (HINT_MORPHINE_EN, HINT_MORPHINE_RU),
    "890000000010028": (DESC_MORPHINE_EN, DESC_MORPHINE_RU),
    "890000000010201": (DESC_BANDAGE_EN, DESC_BANDAGE_RU),
}


def patch_runtime(path: Path, *, english_file: bool) -> int:
    rows = []
    n = 0
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] in UPDATES:
                en, ru = UPDATES[row[0]]
                if english_file:
                    row[1] = en
                    if len(row) > 2:
                        row[2] = en
                else:
                    row[1] = en
                    if len(row) > 2:
                        row[2] = ru
                n += 1
            rows.append(row)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(rows)
    print(f"patched {path.name}: {n}")
    return n


def main() -> None:
    ru_n = patch_runtime(ROOT / "Russian.csv", english_file=False)
    en_n = patch_runtime(ROOT / "English.csv", english_file=True)
    if ru_n != len(UPDATES) or en_n != len(UPDATES):
        raise SystemExit(f"expected {len(UPDATES)} ids each; ru={ru_n} en={en_n}")


if __name__ == "__main__":
    main()
