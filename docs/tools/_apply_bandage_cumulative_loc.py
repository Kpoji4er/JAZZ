# -*- coding: utf-8 -*-
"""Update bandage loc strings for cumulative field bandage."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

HINT_EN = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage — one use spends one bandage per bleed stack (up to your stock), each −1 tier\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> No Medical skill required\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Low AP cost\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Self or ally"
)
HINT_RU = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Бинт — за одно применение тратит по бинту на каждый стак крови (пока хватает запаса), каждый −1 тир\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Навык медицины не требуется\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Низкая стоимость в ОД\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Можно применить к себе или союзнику"
)
LOG_EN = "<target> bleeding reduced by bandage ×<amount>"
LOG_RU = "<target> кровотечение снижено бинтом ×<amount>"

UPDATES = {
    "890000000010013": (HINT_EN, HINT_RU),
    "890000000010021": (LOG_EN, LOG_RU),
}


def patch(path: Path, *, english_file: bool) -> None:
    rows = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] in UPDATES:
                en, ru = UPDATES[row[0]]
                # Russian.csv: col1=EN source, col2=RU translation
                # English.csv: col1=EN, col2=EN (mirror)
                if english_file:
                    row[1] = en
                    if len(row) > 2:
                        row[2] = en
                else:
                    row[1] = en
                    if len(row) > 2:
                        row[2] = ru
            rows.append(row)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(rows)
    print("patched", path.name)


def main() -> None:
    patch(ROOT / "Russian.csv", english_file=False)
    patch(ROOT / "English.csv", english_file=True)


if __name__ == "__main__":
    main()
