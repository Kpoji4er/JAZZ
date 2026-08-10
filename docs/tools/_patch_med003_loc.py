# -*- coding: utf-8 -*-
"""Patch MED-003 hint/description rows in Russian.csv / English.csv."""
from pathlib import Path
import csv
import io

ROOT = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")

HINTS = {
    "890000000010024": {
        "en": (
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores HP and stabilizes downed characters\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Starts healing on one untreated light trauma\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Clears pain and wound infection; rallies downed\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically while in inventory"
        ),
        "ru": (
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Восстанавливает ОЗ и стабилизирует умирающего бойца\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снимает все кровотечения\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Запускает заживление одной необработанной лёгкой травмы\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снимает боль и загноение; поднимает из downed\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одно применение расходует один предмет из стака\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически, пока лежит в инвентаре"
        ),
    },
    "890000000010027": {
        "en": (
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores HP and stabilizes downed characters\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage healing bonus: 50%.\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Starts healing on one untreated medium or light trauma\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Clears pain and wound infection; rallies downed\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack"
        ),
        "ru": (
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Восстанавливает ОЗ и стабилизирует умирающего бойца\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Бонус к лечению при перевязке: 50%.\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снимает все кровотечения\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Запускает заживление одной необработанной средней или лёгкой травмы\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снимает боль и загноение; поднимает из downed\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одно применение расходует один предмет из стака"
        ),
    },
    "890000000010030": {
        "en": (
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores lost HP and stabilizes dying characters\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage healing bonus: 100%\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Starts healing on any untreated trauma\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Clears pain and wound infection; rallies downed\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically from inventory"
        ),
        "ru": (
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Восстанавливает потерянные ОЗ и стабилизирует умирающих бойцов\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Бонус к лечению при перевязке: 100%.\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снимает все кровотечения\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Запускает заживление любой необработанной травмы\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снимает боль и загноение; поднимает из downed\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одно применение расходует один предмет из стака\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически, пока лежит в инвентаре"
        ),
    },
    "890000000010213": {
        "en": (
            "Treat an ally with a small, medium, or large medkit. Restores HP based on Medical, clears all bleeding, "
            "eases pain, clears wound infection, and can rally the downed. Small starts healing on a light trauma; "
            "medium on medium or light; large on any trauma. Field bandages use a separate action."
        ),
        "ru": (
            "Лечит союзника маленькой, средней или большой аптечкой. Восстанавливает ОЗ с учётом Медицины, снимает все кровотечения, "
            "боль и загноение, поднимает из downed. Маленькая запускает заживление лёгкой травмы; средняя — средней или лёгкой; "
            "большая — любой. Для бинтов есть отдельное действие."
        ),
    },
    "890000000010033": {
        "en": "<target> trauma set to healing",
        "ru": "<target>: запущено заживление травмы",
    },
}


def patch_csv(path: Path, lang: str) -> None:
    # Preserve multiline CSV via csv module
    text = path.read_text(encoding="utf-8-sig")
    # Use excel dialect
    rows = list(csv.reader(io.StringIO(text)))
    out = []
    seen = set()
    for row in rows:
        if not row:
            out.append(row)
            continue
        rid = row[0]
        if rid in HINTS:
            en = HINTS[rid]["en"]
            ru = HINTS[rid]["ru"]
            # columns: id, Text/Source, Translation, ...
            if lang == "ru":
                row[1] = en
                if len(row) > 2:
                    row[2] = ru
            else:
                row[1] = en
                if len(row) > 2:
                    row[2] = en
            seen.add(rid)
        out.append(row)
    missing = set(HINTS) - seen
    if missing:
        raise SystemExit(f"{path.name} missing IDs: {missing}")
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerows(out)
    path.write_text(buf.getvalue(), encoding="utf-8")
    print("patched", path.name, sorted(seen))


if __name__ == "__main__":
    patch_csv(ROOT / "Russian.csv", "ru")
    patch_csv(ROOT / "English.csv", "en")
