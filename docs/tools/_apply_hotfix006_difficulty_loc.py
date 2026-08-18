# -*- coding: utf-8 -*-
"""HOTFIX-006: rewrite GameDifficultyDef tooltips (Normal/Hard/VeryHard) in items.lua + RU/EN CSV.

Runtime CSV: Text = RU T() source; Russian.csv Translation = RU; English.csv Translation = EN.
"""
from __future__ import annotations

import csv
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
RU = ROOT / "Russian.csv"
EN = ROOT / "English.csv"

FOOTER_RU = "<color FlavorStyle>Сложность можно изменить в любой момент.</color>"
FOOTER_EN = "<color FlavorStyle>Difficulty can be changed at any time.</color>"

# id -> (ru source, en translation)
LOC = {
    "852333811131": (
        "Стандартная сложность. Стартовый капитал +25%.<newline>"
        "В отрядах Легиона больше медиков; действует лимит копий редких классов.<newline><newline>"
        + FOOTER_RU,
        "Standard difficulty. Starting funds +25%.<newline>"
        "Legion squads field more medics; copy limits on rare classes still apply.<newline><newline>"
        + FOOTER_EN,
    ),
    "698130726969": (
        "Повышенная сложность. Стартовый капитал без бонуса.<newline>"
        "В отрядах Легиона обычная плотность медиков; лимит копий классов действует.<newline><newline>"
        + FOOTER_RU,
        "Increased difficulty. No starting-funds bonus.<newline>"
        "Legion squads use the usual medic density; class copy limits still apply.<newline><newline>"
        + FOOTER_EN,
    ),
    "830857112086": (
        "Максимальная сложность. Стартовый капитал −50%.<newline>"
        "Враги сильнее и с более высокими характеристиками.<newline>"
        "В отрядах Легиона нет лимита копий одного класса (капы снайперов и пулемётов остаются); медиков меньше.<newline><newline>"
        + FOOTER_RU,
        "Maximum difficulty. Starting funds −50%.<newline>"
        "Enemies are tougher and have higher stats.<newline>"
        "Legion squads have no per-class copy limit (sniper and MG caps stay); fewer medics.<newline><newline>"
        + FOOTER_EN,
    ),
}

CTX = {
    "852333811131": "jazz:items.lua:GameDifficultyDef Normal",
    "698130726969": "jazz:items.lua:GameDifficultyDef Hard",
    "830857112086": "jazz:items.lua:GameDifficultyDef VeryHard",
}


def patch_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    for lid, (ru, _en) in LOC.items():
        pat = re.compile(
            rf"(description = T\({lid}, --\[\[ModItemGameDifficultyDef \w+ description\]\] ).*?(\),)",
            re.S,
        )
        m = pat.search(text)
        if not m:
            raise SystemExit(f"items.lua: description T({lid}) not found")
        lua_src = ru.replace("\\", "\\\\").replace('"', '\\"')
        repl = f'{m.group(1)}"{lua_src}"{m.group(2)}'
        text, n = pat.subn(repl, text, count=1)
        if n != 1:
            raise SystemExit(f"items.lua: failed to replace T({lid})")
        print(f"items.lua T({lid})")
    ITEMS.write_text(text, encoding="utf-8")


def upsert_csv(path: Path, lang: str) -> None:
    raw = path.read_text(encoding="utf-8-sig")
    rows = list(csv.reader(io.StringIO(raw)))
    if not rows:
        raise SystemExit(f"empty {path}")
    by_id = {r[0]: i for i, r in enumerate(rows) if r}
    for lid, (ru, en) in LOC.items():
        translation = ru if lang == "ru" else en
        ctx = CTX[lid]
        if lid not in by_id:
            raise SystemExit(f"{path.name} missing {lid}")
        i = by_id[lid]
        row = rows[i]
        while len(row) < 5:
            row.append("")
        row[1] = ru
        row[2] = translation
        row[4] = ctx
        rows[i] = row
        print(f"{path.name} {lid}")
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n", quoting=csv.QUOTE_MINIMAL).writerows(rows)
    path.write_text(buf.getvalue(), encoding="utf-8")


def main() -> None:
    patch_items()
    upsert_csv(RU, "ru")
    upsert_csv(EN, "en")


if __name__ == "__main__":
    main()
