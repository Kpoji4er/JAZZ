# -*- coding: utf-8 -*-
"""Polish MED-006 loc: kit % phrasing + Bandage CA desc; Manual 010290-292."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

HINTS = {
    "890000000010024": {
        "en": (
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Stabilizes one eligible light trauma "
            "(eases combat penalties one tier; does not heal trauma)\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores HP as % of max HP "
            "(scales with Medical: 9–30% from Medical 30 to 100)\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Clears pain and wound infection; rallies downed\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically while in inventory"
        ),
        "ru": (
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Стабилизирует одну подходящую лёгкую травму "
            "(ослабляет боевые штрафы на один тир; не лечит травму)\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Восстанавливает ОЗ в % от макс. ОЗ "
            "(зависит от Медицины: 9–30% при Медицине от 30 до 100)\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снимает все кровотечения\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снимает боль и загноение; поднимает из downed\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одно применение расходует один предмет из стака\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически, пока лежит в инвентаре"
        ),
    },
    "890000000010027": {
        "en": (
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Stabilizes one eligible medium or light trauma "
            "(eases combat penalties one tier; does not heal trauma)\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores HP as % of max HP "
            "(scales with Medical: 18–60% from Medical 50 to 100)\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Clears pain and wound infection; rallies downed\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack"
        ),
        "ru": (
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Стабилизирует одну подходящую среднюю или лёгкую травму "
            "(ослабляет боевые штрафы на один тир; не лечит травму)\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Восстанавливает ОЗ в % от макс. ОЗ "
            "(зависит от Медицины: 18–60% при Медицине от 50 до 100)\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снимает все кровотечения\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снимает боль и загноение; поднимает из downed\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одно применение расходует один предмет из стака"
        ),
    },
    "890000000010030": {
        "en": (
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Stabilizes one eligible trauma of any severity "
            "(eases combat penalties one tier; does not heal trauma)\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores HP as % of max HP "
            "(scales with Medical: 30–100% from Medical 80 to 100)\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Clears pain and wound infection; rallies downed\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically from inventory"
        ),
        "ru": (
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Стабилизирует одну подходящую травму любой тяжести "
            "(ослабляет боевые штрафы на один тир; не лечит травму)\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Восстанавливает ОЗ в % от макс. ОЗ "
            "(зависит от Медицины: 30–100% при Медицине от 80 до 100)\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снимает все кровотечения\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снимает боль и загноение; поднимает из downed\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одно применение расходует один предмет из стака\n"
            "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически, пока лежит в инвентаре"
        ),
    },
    "890000000010213": {
        "en": (
            "Treat an ally with a small, medium, or large medkit. Restores HP as a % of max HP scaled by Medical "
            "(at Medical 100: 30/60/100%; at the kit’s Medical gate: 30% of those values). Clears all bleeding, eases pain, "
            "clears wound infection, can rally the downed, and stabilizes one eligible trauma "
            "(eases combat penalties one tier — does not heal trauma). Field bandages use a separate action."
        ),
        "ru": (
            "Лечит союзника маленькой, средней или большой аптечкой. Восстанавливает ОЗ в % от макс. ОЗ в зависимости от Медицины "
            "(при Медицине 100: 30/60/100%; у порога аптечки — 30% от этих значений). Снимает все кровотечения, боль и загноение, "
            "поднимает из downed и стабилизирует одну подходящую травму "
            "(ослабляет боевые штрафы на один тир — не лечит травму). Для бинтов есть отдельное действие."
        ),
    },
    "890000000010290": {
        "en": "<target> trauma stabilized",
        "ru": "<target>: травма стабилизирована",
    },
    "890000000010291": {
        "en": "Stabilized: combat penalties eased (one tier lighter). Does not heal the trauma — field treatment / hospital required.",
        "ru": "Стабилизирована: боевые штрафы ослаблены (на один тир легче). Не лечит травму — нужна полевая операция / госпиталь.",
    },
    "890000000010292": {
        "en": "Max HP debt from this trauma: <em><pct>%</em>.",
        "ru": "Долг макс. ОЗ от этой травмы: <em><pct>%</em>.",
    },
}


def upsert_runtime(path: Path, lang: str) -> None:
    rows = []
    seen = set()
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.reader(f):
            if not row:
                continue
            rid = row[0]
            if rid in HINTS:
                en = HINTS[rid]["en"]
                ru = HINTS[rid]["ru"]
                if lang == "en":
                    rows.append([rid, en, en, "", "jazz:MED-006"])
                else:
                    rows.append([rid, en, ru, "", "jazz:MED-006"])
                seen.add(rid)
            else:
                rows.append(row)
    for rid, texts in HINTS.items():
        if rid not in seen:
            if lang == "en":
                rows.append([rid, texts["en"], texts["en"], "", "jazz:MED-006"])
            else:
                rows.append([rid, texts["en"], texts["ru"], "", "jazz:MED-006"])
    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)
    print("updated", path.name)


def append_manual(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8")
    # drop stale MED-006 rows on VoiceResponse IDs if present as medicine text
    lines = text.splitlines()
    out = []
    for line in lines:
        if "manual-translation-MED-006" in line and any(
            x in line for x in ("890000000010220", "890000000010221", "890000000010222")
        ):
            continue
        if any(f",{rid}," in f",{line}," or line.startswith(f"{i},") for i, rid in enumerate([])):
            pass
        skip = False
        for rid in ("890000000010290", "890000000010291", "890000000010292"):
            if f",{rid}," in f",{line}," or ("," + rid + ",") in ("," + line):
                # remove old MED append for these if re-running
                if "MED-006" in line:
                    skip = True
        if skip:
            continue
        out.append(line)
    # find next index
    next_idx = 1
    for line in out:
        try:
            next_idx = max(next_idx, int(line.split(",", 1)[0]) + 1)
        except ValueError:
            pass
    for rid in ("890000000010290", "890000000010291", "890000000010292", "890000000010213", "890000000010024", "890000000010027", "890000000010030"):
        en = HINTS[rid]["en"]
        ru = HINTS[rid]["ru"]
        # escape quotes for CSV
        def q(s: str) -> str:
            if any(c in s for c in ',"\n'):
                return '"' + s.replace('"', '""') + '"'
            return s

        if lang == "en":
            out.append(f"{next_idx},{rid},{q(en)},{q(en)},manual-translation-MED-006")
        else:
            out.append(f"{next_idx},{rid},{q(en)},{q(ru)},manual-translation-MED-006")
        next_idx += 1
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("manual", path.name)


def patch_companions() -> None:
    mapping = {
        "InventoryItem/FirstAidKit.lua": "890000000010024",
        "InventoryItem/Medkit.lua": "890000000010027",
        "InventoryItem/Reanimationsset.lua": "890000000010030",
    }
    for rel, rid in mapping.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        en = HINTS[rid]["en"]
        # Replace T(ID, "...") AdditionalHint — fragile; use apply via known start
        import re

        pat = rf"(AdditionalHint = T\({rid}, )(\"(?:\\.|[^\"\\])*\"|\[\[.*?\]\])"
        # multiline string in double quotes with \n escapes in source
        # companions use real newlines? Check - they use \n in one line typically
        # Our companions have one long line with \n escapes
        new_literal = '"' + en.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'
        new_text, n = re.subn(
            rf"AdditionalHint = T\({rid}, \".*?\"\)",
            f"AdditionalHint = T({rid}, {new_literal})",
            text,
            count=1,
            flags=re.S,
        )
        if n != 1:
            # try without re.S on non-greedy across escaped
            print("WARN companion", rel, "replacements", n)
        else:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            print("companion", rel)


def main() -> None:
    upsert_runtime(ROOT / "English.csv", "en")
    upsert_runtime(ROOT / "Russian.csv", "ru")
    append_manual(ROOT / "Localization/EnglishManual.csv", "en")
    append_manual(ROOT / "Localization/RussianManual.csv", "ru")
    # items.lua AdditionalHint is large — rely on companion + items sync from apply script pattern
    print("done")


if __name__ == "__main__":
    main()
