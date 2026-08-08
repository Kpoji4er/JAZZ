# -*- coding: utf-8 -*-
"""JAZZ-UNITS-006 batch 1: sync items.lua + metadata.code + RU/EN CSV from rewritten companions.

Companions are source of truth for DisplayName / Description / unit_reactions (and status fields).
Does not rewrite unrelated CSV rows. Does not bump metadata version / last_changes.
"""
from __future__ import annotations

import csv
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
CE = ROOT / "CharacterEffect"

# Id -> Group for ModItemCharacterEffectCompositeDef
PERKS = [
    ("Jazz_Perk_Blade", "Perk-Personal"),
    ("Jazz_Perk_Madman", "Perk-Personal"),
    ("Jazz_Perk_Mike", "Perk-Personal"),
    ("Jazz_Perk_Nervous", "Perk-Personal"),
    ("Jazz_Perk_Dynamo", "Perk-Personal"),
    ("Jazz_Perk_Henning", "Perk-Personal"),
    ("Jazz_Perk_Shank", "Perk-Personal"),
    ("Jazz_Perk_Vince", "Perk-Personal"),
    ("Jazz_Perk_Steiger", "Perk-Personal"),
    ("Jazz_Perk_Lucky", "Perk-Personal"),
    ("Jazz_Perk_Laura", "Perk-Personal"),
]

STATUSES = [
    ("Jazz_OrderAP", "StatusEffect"),
    ("Jazz_CombatMedicBuff", "StatusEffect"),
]

# loc_id -> (ru_text, en_translation, context)
LOC: dict[str, tuple[str, str, str]] = {
    "890000000001800": (
        "Вырезать алфавит",
        "Carve the Alphabet",
        "jazz:CharacterEffect/Jazz_Perk_Blade.lua",
    ),
    "890000000001801": (
        "Зверство: за каждый успешный удар в цепочке наносится ещё один удар.",
        "Brutalize: each successful hit in the chain deals one extra hit.",
        "jazz:CharacterEffect/Jazz_Perk_Blade.lua",
    ),
    "890000000002100": (
        "Бешеный пес",
        "Mad Dog",
        "jazz:CharacterEffect/Jazz_Perk_Madman.lua",
    ),
    "890000000002101": (
        "Критический удар или убийство в ближнем бою снижает силу воли всех в радиусе 5 клеток на 10 (включая союзников).",
        "A melee critical hit or kill reduces Willpower of everyone within 5 tiles by 10 (including allies).",
        "jazz:CharacterEffect/Jazz_Perk_Madman.lua",
    ),
    "890000000002300": (
        "Быстрая реакция",
        "Quick Reflexes",
        "jazz:CharacterEffect/Jazz_Perk_Mike.lua",
    ),
    "890000000002301": (
        "Овервотч и контроль получают +2 дополнительные атаки. Ответные атаки срабатывают, когда доступны.",
        "Overwatch and Pin Down gain +2 extra attacks. Reaction attacks fire when available.",
        "jazz:CharacterEffect/Jazz_Perk_Mike.lua",
    ),
    "890000000002900": (
        "Нервный, но азартный",
        "Nervous but Eager",
        "jazz:CharacterEffect/Jazz_Perk_Nervous.lua",
    ),
    "890000000002901": (
        "Каждое попадание очереди или автоогня добавляет пулю к следующей очереди (максимум +10).",
        "Each burst/autofire hit adds a bullet to the next burst (maximum +10).",
        "jazz:CharacterEffect/Jazz_Perk_Nervous.lua",
    ),
    "890000000003400": (
        "Медвежатник",
        "Safe-Cracker",
        "jazz:CharacterEffect/Jazz_Perk_Dynamo.lua",
    ),
    "890000000003401": (
        "Взлом замков не активирует ловушки на замках.",
        "Picking locks does not trigger lock traps.",
        "jazz:CharacterEffect/Jazz_Perk_Dynamo.lua",
    ),
    "890000000004000": (
        "Полевой командир",
        "Field Commander",
        "jazz:CharacterEffect/Jazz_Perk_Henning.lua",
    ),
    "890000000004001": (
        "В начале хода союзники в радиусе 10 клеток получают +3 ОД.",
        "At turn start, allies within 10 tiles gain +3 AP.",
        "jazz:CharacterEffect/Jazz_Perk_Henning.lua",
    ),
    "890000000005029": (
        "Дефицит ресурсов",
        "Resource Shortage",
        "jazz:CharacterEffect/Jazz_Perk_Vince.lua",
    ),
    "890000000005030": (
        "Пока Винс в отряде, расход аптечек и медикаментов снижен примерно на 25% (шанс не потратить заряд).",
        "While Vince is in the squad, medkit and medicine use is reduced by about 25% (chance not to spend a charge).",
        "jazz:CharacterEffect/Jazz_Perk_Vince.lua",
    ),
    "890000000005041": (
        "Вожак стаи",
        "Pack Leader",
        "jazz:CharacterEffect/Jazz_Perk_Steiger.lua",
    ),
    "890000000005042": (
        "Ночью и под землёй в начале хода союзники в радиусе 10 клеток получают +5 к шансу попадания.",
        "At night and underground, at turn start allies within 10 tiles gain +5 chance to hit.",
        "jazz:CharacterEffect/Jazz_Perk_Steiger.lua",
    ),
    "890000000005043": (
        "Госпожа Удача",
        "Lady Luck",
        "jazz:CharacterEffect/Jazz_Perk_Lucky.lua",
    ),
    "890000000005044": (
        "Если шанс попадания был 70% и выше и выстрел промахнулся, бросок повторяется.",
        "If chance to hit was 70% or higher and the shot missed, the roll is repeated.",
        "jazz:CharacterEffect/Jazz_Perk_Lucky.lua",
    ),
    "890000000005045": (
        "Боевой медик",
        "Combat Medic",
        "jazz:CharacterEffect/Jazz_Perk_Laura.lua",
    ),
    "890000000005046": (
        "После лечения союзника Лора получает +15 к шансу попадания и критическому удару до конца следующего хода.",
        "After healing an ally, Laura gains +15 chance to hit and critical chance until the end of her next turn.",
        "jazz:CharacterEffect/Jazz_Perk_Laura.lua",
    ),
    "890000000005056": (
        "Не подходи ко мне!",
        "Don't Come Near Me!",
        "jazz:CharacterEffect/Jazz_Perk_Shank.lua",
    ),
    "890000000005057": (
        "50% защита в ближнем бою. При промахе по Шенку он отбрасывает нож, если цель в 8 клетках.",
        "50% melee defense. When a melee attack misses Shank, he throws a knife back if the attacker is within 8 tiles.",
        "jazz:CharacterEffect/Jazz_Perk_Shank.lua",
    ),
    "890000000006218": (
        "Приказ: ОД",
        "Order: AP",
        "jazz:CharacterEffect/Jazz_OrderAP.lua",
    ),
    "890000000006219": (
        "+3 ОД на этот ход от полевого командира.",
        "+3 AP this turn from the field commander.",
        "jazz:CharacterEffect/Jazz_OrderAP.lua",
    ),
    "890000000006220": (
        "Боевой медик",
        "Combat Medic",
        "jazz:CharacterEffect/Jazz_CombatMedicBuff.lua",
    ),
    "890000000006221": (
        "+15 к шансу попадания и критическому удару до конца следующего хода.",
        "+15 chance to hit and critical chance until the end of the next turn.",
        "jazz:CharacterEffect/Jazz_CombatMedicBuff.lua",
    ),
}


def _brace_end(text: str, open_idx: int) -> int:
    """open_idx points at '{'; return index of matching '}'."""
    depth = 0
    i = open_idx
    n = len(text)
    while i < n:
        c = text[i]
        if c == "-" and text.startswith("--[[", i):
            close = text.find("]]", i + 4)
            i = n if close < 0 else close + 2
            continue
        if c == "-" and text.startswith("--", i) and not text.startswith("--[[", i):
            nl = text.find("\n", i)
            i = n if nl < 0 else nl + 1
            continue
        if c in ("'", '"'):
            q = c
            i += 1
            while i < n:
                if text[i] == "\\":
                    i += 2
                    continue
                if text[i] == q:
                    i += 1
                    break
                i += 1
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError("unbalanced braces")


def extract_define_props(path: Path) -> tuple[str, str]:
    """Return (class_id, top-level props body without __parents/__generated)."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"DefineClass\.(\w+)\s*=\s*\{", text)
    if not m:
        raise SystemExit(f"no DefineClass in {path}")
    class_id = m.group(1)
    open_brace = m.end() - 1
    close = _brace_end(text, open_brace)
    inner = text[open_brace + 1 : close]
    # Drop __parents / __generated_by_class assignments (and blank lines after them).
    lines = inner.splitlines(True)
    out: list[str] = []
    skip_keys = {"__parents", "__generated_by_class"}
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        key_m = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s*=", stripped)
        if key_m and key_m.group(1) in skip_keys:
            # skip until this assignment ends (may be multi-line table)
            if "{" in line and "}" not in line.split("=", 1)[-1]:
                # rare; __parents is usually one line
                pass
            i += 1
            # skip following blank lines
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            continue
        out.append(line)
        i += 1
    # Trim leading/trailing blank lines
    while out and out[0].strip() == "":
        out.pop(0)
    while out and out[-1].strip() == "":
        out.pop()
    return class_id, "".join(out)


def companion_props_to_items(props: str) -> str:
    """Convert top-level `key =` to `'key',` for ModItem serialization."""
    lines = props.splitlines(True)
    out: list[str] = []
    depth = 0  # relative brace depth inside props
    for line in lines:
        # Track braces ignoring strings/comments roughly via previous helper on full text —
        # for line-level, count { } outside quotes.
        stripped = line.lstrip()
        if depth == 0:
            km = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", stripped, re.S)
            if km:
                key, rest = km.group(1), km.group(2)
                indent = line[: len(line) - len(stripped)]
                # Re-indent for items PlaceObj body (one extra tab vs companion which uses one tab)
                # Companion uses \t; items outer fields use \t\t\t\t\t
                # Keep companion indent for nested unit_reactions content; only rewrite top-level keys.
                line = f"{indent}'{key}', {rest}"
                if not line.endswith("\n"):
                    line += "\n"
        # update depth after processing line
        depth += line.count("{") - line.count("}")
        if depth < 0:
            depth = 0
        out.append(line)
    return "".join(out)


def build_moditem(class_id: str, group: str, props_items: str) -> str:
    # Normalize prop indent: companion uses single leading tab; items PlaceObj uses five tabs
    # for top-level fields. Nested PlaceObj inside unit_reactions keeps relative tabs.
    prop_lines = []
    for line in props_items.splitlines(True):
        if line.startswith("\t"):
            # companion top-level was \tKEY; after convert still \t'KEY'
            # bump to 5 tabs for ModItem fields; nested content that had more tabs gets +4
            # companion: \t (1) top, \t\t (2) PlaceObj, \t\t\t (3) Event
            # items OrderCTH uses 6 tabs for PlaceObj inside unit_reactions sometimes.
            # Practical approach: strip one leading tab from companion, then prefix five tabs
            # only for lines that were top-level (1 tab) — for deeper lines, strip 1 and add 5.
            rest = line[1:]  # drop companion's first tab
            prop_lines.append("\t\t\t\t\t" + rest)
        else:
            prop_lines.append("\t\t\t\t\t" + line if line.strip() else line)
    body = "".join(prop_lines)
    # Ensure body ends with newline
    if body and not body.endswith("\n"):
        body += "\n"
    return (
        "\t\t\t\tPlaceObj('ModItemCharacterEffectCompositeDef', {\n"
        f"\t\t\t\t\t'Group', \"{group}\",\n"
        f"\t\t\t\t\t'Id', \"{class_id}\",\n"
        f"{body}"
        "\t\t\t\t}),\n"
    )


def find_moditem_span(text: str, class_id: str) -> tuple[int, int] | None:
    """Return [start, end) of PlaceObj('ModItemCharacterEffectCompositeDef'...) for Id."""
    # Find 'Id', "ClassId" inside a ModItemCharacterEffectCompositeDef
    needle = f"'Id', \"{class_id}\""
    pos = 0
    while True:
        idx = text.find(needle, pos)
        if idx < 0:
            return None
        # Walk back to PlaceObj('ModItemCharacterEffectCompositeDef'
        start = text.rfind("PlaceObj('ModItemCharacterEffectCompositeDef'", 0, idx)
        if start < 0:
            pos = idx + 1
            continue
        # Ensure no other Id between start and idx
        between = text[start:idx]
        if between.count("'Id',") > 0 and between.rfind("'Id',") != between.find("'Id',"):
            pos = idx + 1
            continue
        brace = text.find("{", start)
        end_brace = _brace_end(text, brace)
        # include trailing `),` optionally with newline
        end = end_brace + 1
        if text.startswith("),", end):
            end += 2
        if text.startswith("\n", end):
            end += 1
        # Include same-line leading indent so replacement does not double-indent.
        line_start = text.rfind("\n", 0, start) + 1
        if text[line_start:start].strip() == "":
            start = line_start
        return start, end


def sync_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    for class_id, group in PERKS:
        path = CE / f"{class_id}.lua"
        cid, props = extract_define_props(path)
        assert cid == class_id
        props_items = companion_props_to_items(props)
        block = build_moditem(class_id, group, props_items)
        span = find_moditem_span(text, class_id)
        if not span:
            raise SystemExit(f"missing ModItem for {class_id}")
        text = text[: span[0]] + block + text[span[1] :]
        print(f"items synced {class_id}")

    # Status effects: replace if present, else insert after Jazz_OrderCTH
    for class_id, group in STATUSES:
        path = CE / f"{class_id}.lua"
        cid, props = extract_define_props(path)
        assert cid == class_id
        props_items = companion_props_to_items(props)
        block = build_moditem(class_id, group, props_items)
        span = find_moditem_span(text, class_id)
        if span:
            text = text[: span[0]] + block + text[span[1] :]
            print(f"items synced {class_id}")
        else:
            cth = find_moditem_span(text, "Jazz_OrderCTH")
            if not cth:
                raise SystemExit("Jazz_OrderCTH missing; cannot insert status effects")
            text = text[: cth[1]] + block + text[cth[1] :]
            print(f"items inserted {class_id} after Jazz_OrderCTH")

    ITEMS.write_text(text, encoding="utf-8")
    print("wrote", ITEMS)


def sync_metadata_code() -> None:
    text = META.read_text(encoding="utf-8")
    needle = '"CharacterEffect/Jazz_OrderCTH.lua",'
    inserts = [
        '"CharacterEffect/Jazz_OrderAP.lua",',
        '"CharacterEffect/Jazz_CombatMedicBuff.lua",',
    ]
    if "Jazz_OrderAP.lua" in text and "Jazz_CombatMedicBuff.lua" in text:
        print("metadata.code already lists OrderAP + CombatMedicBuff")
        return
    if needle not in text:
        raise SystemExit("Jazz_OrderCTH.lua missing from metadata.code")
    add = needle
    for line in inserts:
        if line.strip('"').rstrip(",") not in text.replace("\\", "/"):
            # check properly
            pass
    block = (
        '"CharacterEffect/Jazz_OrderCTH.lua",\n'
        '\t\t"CharacterEffect/Jazz_OrderAP.lua",\n'
        '\t\t"CharacterEffect/Jazz_CombatMedicBuff.lua",'
    )
    if '"CharacterEffect/Jazz_OrderAP.lua"' not in text:
        text = text.replace(needle, block, 1)
        META.write_text(text, encoding="utf-8")
        print("metadata.code: added OrderAP + CombatMedicBuff")
    else:
        print("metadata.code: OrderAP present")


def _format_csv_row(loc_id: str, text: str, translation: str, context: str) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="")
    w.writerow([loc_id, text, translation, "", context])
    return buf.getvalue()


def _is_row_start(line: str, loc_id: str) -> bool:
    return line.startswith(loc_id + ",") or line.startswith("\ufeff" + loc_id + ",")


def sync_csv(path: Path, *, english: bool) -> None:
    raw = path.read_text(encoding="utf-8")
    # Preserve exact prefix (sep=, + header). Work line-oriented for single-line loc rows.
    lines = raw.splitlines(True)
    by_id: dict[str, int] = {}
    for i, line in enumerate(lines):
        for loc_id in LOC:
            if _is_row_start(line, loc_id):
                by_id[loc_id] = i
                break

    changed = 0
    for loc_id, (ru, en, ctx) in LOC.items():
        translation = en if english else ru
        new_line = _format_csv_row(loc_id, ru, translation, ctx) + (
            "\n" if not (by_id.get(loc_id) is not None and lines[by_id[loc_id]].endswith("\n") is False) else ""
        )
        # always end with \n for consistency
        if not new_line.endswith("\n"):
            new_line += "\n"
        if loc_id in by_id:
            old = lines[by_id[loc_id]]
            # Keep existing Context if present and non-empty unless ours is more specific
            try:
                old_row = next(csv.reader([old.rstrip("\n")]))
                if len(old_row) >= 5 and old_row[4] and not old_row[4].startswith("jazz:CharacterEffect/"):
                    # preserve remapped notes if still useful — prefer new CE context for batch1
                    pass
            except csv.Error:
                pass
            if old != new_line and old.rstrip("\n") != new_line.rstrip("\n"):
                lines[by_id[loc_id]] = new_line
                changed += 1
            else:
                # force rewrite to new text/translation even if only Context differs
                if old.rstrip("\n") != new_line.rstrip("\n"):
                    lines[by_id[loc_id]] = new_line
                    changed += 1
                else:
                    lines[by_id[loc_id]] = new_line  # normalize
                    if old != new_line:
                        changed += 1
        else:
            # Insert in numeric order among existing ID lines
            insert_at = None
            target = int(loc_id)
            for i, line in enumerate(lines):
                m = re.match(r"^(\d+),", line)
                if not m:
                    continue
                if int(m.group(1)) > target:
                    insert_at = i
                    break
            if insert_at is None:
                if lines and not lines[-1].endswith("\n"):
                    lines[-1] += "\n"
                lines.append(new_line)
            else:
                lines.insert(insert_at, new_line)
            changed += 1
            # refresh indices after insert
            by_id = {}
            for i, line in enumerate(lines):
                for lid in LOC:
                    if _is_row_start(line, lid):
                        by_id[lid] = i
                        break
            print(f"  inserted {loc_id}")

    path.write_text("".join(lines), encoding="utf-8")
    print(f"{path.name}: touched/rewrote ~{changed} of {len(LOC)} ids")


def verify_henning_display() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    span = find_moditem_span(text, "Jazz_Perk_Henning")
    assert span
    chunk = text[span[0] : span[1]]
    if 'T("Perk")' in chunk or "\"Perk\"" in chunk and "Полевой командир" not in chunk:
        raise SystemExit("Henning DisplayName still broken")
    if "Полевой командир" not in chunk:
        raise SystemExit("Henning DisplayName missing Полевой командир")
    if "Jazz_OrderAP" not in chunk and "Jazz_OrderAP" not in text[span[0] : span[0] + 5000]:
        # OrderAP is applied to allies, must appear in Henning reactions
        if "Jazz_OrderAP" not in chunk:
            raise SystemExit("Henning reactions missing Jazz_OrderAP")
    print("Henning DisplayName OK; OrderAP wired in reaction")


def main() -> None:
    sync_items()
    verify_henning_display()
    sync_metadata_code()
    sync_csv(ROOT / "Russian.csv", english=False)
    sync_csv(ROOT / "English.csv", english=True)
    print("DONE")


if __name__ == "__main__":
    main()
