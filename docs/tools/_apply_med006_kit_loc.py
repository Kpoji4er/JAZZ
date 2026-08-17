# -*- coding: utf-8 -*-
"""MED-006: kit AdditionalHint + stabilize/debt loc; strip MED-003 heal_modifier."""
from __future__ import annotations

import csv
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ICON = "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120>"


def hint_lines(*lines: str) -> str:
    return "\n".join(f"{ICON} {line}" for line in lines)


HINTS = {
    "890000000010024": {
        "en": hint_lines(
            "Stabilizes one eligible light trauma (eases combat penalties one tier; does not heal trauma)",
            "Restores HP as % of max HP (scales with Medical: 9–30% from Medical 30 to 100)",
            "Removes all bleeding",
            "Clears pain and wound infection; rallies downed",
            "One use = one item from the stack",
            "Used automatically while in inventory",
        ),
        "ru": hint_lines(
            "Стабилизирует одну подходящую лёгкую травму (ослабляет боевые штрафы на один тир; не лечит травму)",
            "Восстанавливает ОЗ в % от макс. ОЗ (зависит от Медицины: 9–30% от Медицины 30 до 100)",
            "Снимает все кровотечения",
            "Снимает боль и загноение; поднимает из downed",
            "Одно применение расходует один предмет из стака",
            "Используется автоматически, пока лежит в инвентаре",
        ),
    },
    "890000000010027": {
        "en": hint_lines(
            "Stabilizes one eligible medium or light trauma (eases combat penalties one tier; does not heal trauma)",
            "Restores HP as % of max HP (scales with Medical: 18–60% from Medical 50 to 100)",
            "Removes all bleeding",
            "Clears pain and wound infection; rallies downed",
            "One use = one item from the stack",
        ),
        "ru": hint_lines(
            "Стабилизирует одну подходящую среднюю или лёгкую травму (ослабляет боевые штрафы на один тир; не лечит травму)",
            "Восстанавливает ОЗ в % от макс. ОЗ (зависит от Медицины: 18–60% от Медицины 50 до 100)",
            "Снимает все кровотечения",
            "Снимает боль и загноение; поднимает из downed",
            "Одно применение расходует один предмет из стака",
        ),
    },
    "890000000010030": {
        "en": hint_lines(
            "Stabilizes one eligible trauma of any severity (eases combat penalties one tier; does not heal trauma)",
            "Restores HP as % of max HP (scales with Medical: 30–100% from Medical 80 to 100)",
            "Removes all bleeding",
            "Clears pain and wound infection; rallies downed",
            "One use = one item from the stack",
            "Used automatically from inventory",
        ),
        "ru": hint_lines(
            "Стабилизирует одну подходящую травму любой тяжести (ослабляет боевые штрафы на один тир; не лечит травму)",
            "Восстанавливает ОЗ в % от макс. ОЗ (зависит от Медицины: 30–100% от Медицины 80 до 100)",
            "Снимает все кровотечения",
            "Снимает боль и загноение; поднимает из downed",
            "Одно применение расходует один предмет из стака",
            "Используется автоматически, пока лежит в инвентаре",
        ),
    },
    "890000000010220": {
        "en": "<target> trauma stabilized",
        "ru": "<target>: травма стабилизирована",
    },
    "890000000010221": {
        "en": (
            "Stabilized: combat penalties eased (one tier lighter). "
            "Does not heal the trauma — field treatment / hospital required."
        ),
        "ru": (
            "Стабилизирована: боевые штрафы ослаблены (на один тир легче). "
            "Не лечит травму — нужна полевая операция / госпиталь."
        ),
    },
    "890000000010222": {
        "en": "Max HP debt from this trauma: <em><pct>%</em>.",
        "ru": "Долг макс. ОЗ от этой травмы: <em><pct>%</em>.",
    },
}

COMPANION_HINTS = {
    "FirstAidKit.lua": HINTS["890000000010024"]["en"],
    "Medkit.lua": HINTS["890000000010027"]["en"],
    "Reanimationsset.lua": HINTS["890000000010030"]["en"],
}


def patch_csv(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8-sig")
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
            if lang == "ru":
                row[1] = en
                if len(row) > 2:
                    row[2] = ru
            else:
                row[1] = en
                if len(row) > 2:
                    row[2] = en
            # retarget location note for reclaimed medicine IDs
            if rid in ("890000000010220", "890000000010221", "890000000010222") and len(row) > 4:
                row[4] = "jazz:MED-006"
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


def append_manual(path: Path, col_name: str) -> None:
    """Append SourceText→translation rows for MED-006 (keyed by SourceText)."""
    text = path.read_text(encoding="utf-8-sig")
    # find next N
    last_n = 0
    for line in text.splitlines():
        if not line or line.startswith("N,"):
            continue
        try:
            last_n = max(last_n, int(line.split(",", 1)[0]))
        except ValueError:
            pass
    # skip if SourceText already present
    existing_sources = set()
    rows = list(csv.reader(io.StringIO(text)))
    for row in rows[1:]:
        if len(row) >= 3:
            existing_sources.add(row[2])

    new_rows = []
    n = last_n
    for rid, pair in HINTS.items():
        src = pair["en"]
        val = pair["en"] if col_name == "English" else pair["ru"]
        if src in existing_sources:
            continue
        n += 1
        new_rows.append([str(n), rid, src, val, "manual-translation-MED-006"])
    if not new_rows:
        print(path.name, "manual: nothing to append")
        return
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    # rewrite full file to keep quoting consistent, then append
    w.writerows(rows)
    for row in new_rows:
        w.writerow(row)
    path.write_text(buf.getvalue(), encoding="utf-8")
    print(path.name, "manual appended", len(new_rows))


def patch_companion(name: str, hint_en: str) -> None:
    path = ROOT / "InventoryItem" / name
    text = path.read_text(encoding="utf-8")
    # AdditionalHint
    m = re.search(
        r"(AdditionalHint = T\(8900000000100(?:24|27|30), )\"\"\".*?\"\"\""
        r"|(AdditionalHint = T\(8900000000100(?:24|27|30), )\"(?:\\.|[^\"\\])*\"",
        text,
        re.S,
    )
    # simpler: replace the T(...) string for known IDs
    def repl_hint(match: re.Match) -> str:
        tid = match.group(1)
        return f'AdditionalHint = T({tid}, "{_lua_escape(hint_en)}")'

    text2, n = re.subn(
        r'AdditionalHint = T\((8900000000100(?:24|27|30)), "(?:\\.|[^"\\])*"\)',
        repl_hint,
        text,
        count=1,
    )
    if n != 1:
        raise SystemExit(f"{name}: AdditionalHint replace failed ({n})")

    # strip unit_reactions OnCalcHealAmount for Medkit / Reanimationsset
    if name in ("Medkit.lua", "Reanimationsset.lua"):
        text3, n2 = re.subn(
            r"\n\tunit_reactions = \{\n\t\tPlaceObj\('UnitReaction', \{\n"
            r"\t\t\tEvent = \"OnCalcHealAmount\",\n"
            r"\t\t\tHandler = function\(self, target, patient, medic, medkit, data\)\n"
            r"\t\t\t\tif self == medkit then\n"
            r"\t\t\t\t\tdata\.heal_modifier = data\.heal_modifier \+ (?:50|100)\n"
            r"\t\t\t\tend\n"
            r"\t\t\tend,\n"
            r"\t\t\}\),\n"
            r"\t\},\n",
            "\n",
            text2,
            count=1,
        )
        if n2 == 0 and "heal_modifier" not in text2:
            pass  # already stripped
        elif n2 != 1:
            raise SystemExit(f"{name}: heal_modifier strip failed ({n2})")
        else:
            text2 = text3

    path.write_text(text2, encoding="utf-8")
    print("companion", name)


def _lua_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def patch_items_lua() -> None:
    path = ROOT / "items.lua"
    text = path.read_text(encoding="utf-8")

    # Replace AdditionalHint T strings by ID
    for tid, pair in (
        ("890000000010024", HINTS["890000000010024"]["en"]),
        ("890000000010027", HINTS["890000000010027"]["en"]),
        ("890000000010030", HINTS["890000000010030"]["en"]),
    ):
        pat = rf"('AdditionalHint', T\({tid}, )\"(?:\\.|[^\"\\])*\""
        escaped = _lua_escape(pair)

        def repl(match: re.Match, _esc: str = escaped) -> str:
            return f'{match.group(1)}"{_esc}"'

        text2, n = re.subn(pat, repl, text, count=1)
        if n != 1:
            # already updated (idempotent): accept if hint text present
            if _lua_escape(pair) in text or pair.split("\n")[0] in text:
                print(f"items.lua AdditionalHint {tid} already patched")
                continue
            raise SystemExit(f"items.lua AdditionalHint {tid} replace failed ({n})")
        text = text2

    # Strip unit_reactions blocks on Medkit and Reanimationsset PlaceObj
    # (Medkit has a slightly mis-indented Handler end,; allow flexible whitespace)
    for kit_id, bonus in (("Medkit", 50), ("Reanimationsset", 100)):
        pat = (
            rf"('Id', \"{kit_id}\",\n"
            rf"\t\t\t\t'object_class', \"JazzStackableMedicine\",\n)"
            r"\t\t\t\t'unit_reactions', \{\n"
            r"\t\t\t\t\tPlaceObj\('UnitReaction', \{\n"
            r"\t\t\t\t\t\tEvent = \"OnCalcHealAmount\",\n"
            r"\t\t\t\t\t\tHandler = function \(self, target, patient, medic, medkit, data\)\n"
            r"\t\t\t\t\t\t\tif self == medkit then\n"
            rf"\t\t\t\t\t\t\t\tdata\.heal_modifier = data\.heal_modifier \+ {bonus}\n"
            r"\t\t\t\t\t\t\tend\n"
            r"\t+\tend,\n"
            r"\t\t\t\t\t\}\),\n"
            r"\t\t\t\t\},\n"
        )
        text2, n = re.subn(pat, r"\1", text, count=1)
        if n == 0 and f"'Id', \"{kit_id}\"" in text and "heal_modifier" not in text[
            text.find(f"'Id', \"{kit_id}\"") : text.find(f"'Id', \"{kit_id}\"") + 800
        ]:
            print(f"items.lua {kit_id} heal_modifier already stripped")
            continue
        if n != 1:
            raise SystemExit(f"items.lua {kit_id} heal_modifier strip failed ({n})")
        text = text2

    path.write_text(text, encoding="utf-8")
    print("patched items.lua")


def main() -> None:
    for name, hint in COMPANION_HINTS.items():
        patch_companion(name, hint)
    patch_items_lua()
    patch_csv(ROOT / "Russian.csv", "ru")
    patch_csv(ROOT / "English.csv", "en")
    append_manual(ROOT / "Localization" / "EnglishManual.csv", "English")
    append_manual(ROOT / "Localization" / "RussianManual.csv", "Russian")
    print("done")


if __name__ == "__main__":
    main()
