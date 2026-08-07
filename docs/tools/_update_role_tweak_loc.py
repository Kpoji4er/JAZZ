#!/usr/bin/env python3
"""Update Russian.csv / English.csv AdditionalHint rows for role tweaks."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RU = {
    998151280081: (
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Быстрый одиночный \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Скорострельный \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Сильная отдача \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Ненадежный"
    ),
    259441942196: (
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Убойный вблизи \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Без приклада \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Скорострельный \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Ненадежный"
    ),
    534112939755: (
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Много обвеса \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Можно забрать домой после срочной службы"
    ),
    155361024222: (
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Максимум обвеса \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Слабая отдача"
    ),
    707852110578: (
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Самый точный полуавтомат \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Убойный \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный"
    ),
}

EN = {
    998151280081: (
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Cheap single shot \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> High rate of fire \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Heavy recoil \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Unreliable"
    ),
    259441942196: (
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Lethal up close \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> No stock \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> High rate of fire \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Unreliable"
    ),
    534112939755: (
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Accurate \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Reliable \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Highly modifiable \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Yours to keep after military service"
    ),
    155361024222: (
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Accurate \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Reliable \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Fully railed \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Soft recoil"
    ),
    707852110578: (
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Most accurate semi-auto \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> High damage \n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Reliable"
    ),
}

# polished RU column (ё where used historically)
RU2 = {
    998151280081: RU[998151280081].replace("Ненадежный", "Ненадёжный"),
    259441942196: RU[259441942196].replace("Ненадежный", "Ненадёжный"),
    534112939755: RU[534112939755].replace("Надежный", "Надёжный", 1),
    155361024222: RU[155361024222].replace("Надежный", "Надёжный", 1),
    707852110578: RU[707852110578].replace("Надежный", "Надёжный"),
}


def update(path: Path, mode: str) -> int:
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    n = 0
    out = []
    for row in rows:
        if not row:
            out.append(row)
            continue
        try:
            tid = int(row[0])
        except ValueError:
            out.append(row)
            continue
        if tid in RU:
            if mode == "ru":
                row[1] = RU[tid]
                if len(row) > 2 and row[2] is not None:
                    row[2] = RU2[tid]
            else:
                row[1] = RU[tid]
                if len(row) > 2:
                    row[2] = EN[tid]
            n += 1
        out.append(row)
    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(out)
    return n


def main() -> None:
    a = update(ROOT / "Russian.csv", "ru")
    b = update(ROOT / "English.csv", "en")
    print(f"Russian.csv updated {a}; English.csv updated {b}")


if __name__ == "__main__":
    main()
