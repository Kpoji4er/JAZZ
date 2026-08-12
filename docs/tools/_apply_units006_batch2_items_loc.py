# -*- coding: utf-8 -*-
"""JAZZ-UNITS-006 batch 2 (§C combat CHANGE): sync items.lua + metadata.code + RU/EN CSV.

Companions are source of truth for DisplayName / Description / unit_reactions / Parameters.
Does not bump metadata version / last_changes.
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
RU = ROOT / "Russian.csv"
EN = ROOT / "English.csv"

# Reuse batch1 brace/ModItem helpers via inline copies (keep script self-contained).

PERKS = [
    ("GruntyPerk_JAZZ", "Perk-Personal"),
    ("GrizzlyPerk", "Perk-Personal"),
    ("YouSeeIgor", "Perk-Personal"),
    ("WeGotThis", "Perk-Personal"),
    ("NailsPerk", "Perk-Personal"),
    ("JackOfAllTrades", "Perk-Personal"),
    ("SecondStoryMan", "Perk-Personal"),
    ("ShoulderToShoulder", "Perk-Personal"),
    ("SteroidPunch", "Perk-Personal"),
    ("IcePerk", "Perk-Personal"),
]

# Existing ModItems that must be replaced (already in items). New ones inserted after GrizzlyPerk CE.
EXISTING = {"GruntyPerk_JAZZ", "GrizzlyPerk"}

LOC: dict[str, tuple[str, str, str]] = {
    "845332100943": (
        "В начале боя получает +50% ОД на первый ход. На каждом следующем ходу с шансом <em>10% × уровень боевого духа</em> снова получает тот же бонус (+50% ОД).",
        "At combat start gains +50% AP for the first turn. On each later turn, with chance <em>10% × personal morale level</em>, gains the same +50% AP buff again.",
        "jazz:CharacterEffect/GruntyPerk_JAZZ.lua",
    ),
    "272740235755": (
        "<em>Сигнатурная пулемётная атака</em> игнорирует штрафы <em>без опоры</em> к точности и отдаче, даёт <em>вдвое больше пуль</em> и <em>вдвое сильнее подавление</em>, при пониженном уроне и жёстком контроле отдачи. Обычная очередь пулемёта эти бонусы не получает.",
        "<em>Signature machine-gun attack</em> ignores <em>unsupported</em> accuracy and recoil penalties, fires <em>twice as many shots</em> with <em>double suppression</em>, reduced damage, and tight recoil control. Ordinary MG burst does not get these bonuses.",
        "jazz:CharacterEffect/GrizzlyPerk.lua",
    ),
    "890000000006500": (
        "Видишь, Игорь…",
        "You See, Igor…",
        "jazz:CharacterEffect/YouSeeIgor.lua",
    ),
    "890000000006501": (
        "За каждое убийство получает <em>+3 ОД</em> (не полное восстановление ОД).",
        "Each kill grants <em>+3 AP</em> (not a full AP restore).",
        "jazz:CharacterEffect/YouSeeIgor.lua",
    ),
    "890000000006502": (
        "Мы справимся",
        "We Got This",
        "jazz:CharacterEffect/WeGotThis.lua",
    ),
    "890000000006503": (
        "После убийства весь отряд получает <em>+10 Силы воли (Grit)</em>.",
        "After a kill, the whole squad gains <em>+10 Grit</em>.",
        "jazz:CharacterEffect/WeGotThis.lua",
    ),
    "890000000006504": (
        "Гвоздь в цель",
        "Nailed It",
        "jazz:CharacterEffect/NailsPerk.lua",
    ),
    "890000000006505": (
        "После первого убийства в бою все атаки наносят <em>+20% урона</em> до конца боя.",
        "After the first kill in combat, all attacks deal <em>+20% damage</em> until combat ends.",
        "jazz:CharacterEffect/NailsPerk.lua",
    ),
    "890000000006506": (
        "Мастер на все руки",
        "Jack of All Trades",
        "jazz:CharacterEffect/JackOfAllTrades.lua",
    ),
    "890000000006507": (
        "Любые спутниковые операции выполняются примерно на <em>33% быстрее</em>.",
        "Any satellite operations complete about <em>33% faster</em>.",
        "jazz:CharacterEffect/JackOfAllTrades.lua",
    ),
    "890000000006508": (
        "Человек со второго этажа",
        "Second Story Man",
        "jazz:CharacterEffect/SecondStoryMan.lua",
    ),
    "890000000006509": (
        "Атаки <em>сверху</em> получают <em>+50%</em> к шансу критического удара.",
        "Attacks from <em>high ground</em> gain <em>+50%</em> crit chance.",
        "jazz:CharacterEffect/SecondStoryMan.lua",
    ),
    "890000000006510": (
        "Плечом к плечу",
        "Shoulder to Shoulder",
        "jazz:CharacterEffect/ShoulderToShoulder.lua",
    ),
    "890000000006511": (
        "В конце хода, если рядом есть союзник (≤1 клетка), Скалли и ближайшие союзники получают <em>+15 Силы воли (Grit)</em>.",
        "At turn end, if an ally is adjacent (≤1 tile), Scully and nearby allies gain <em>+15 Grit</em>.",
        "jazz:CharacterEffect/ShoulderToShoulder.lua",
    ),
    "890000000006512": (
        "Удар анаболика",
        "Steroid Smash",
        "jazz:CharacterEffect/SteroidPunch.lua",
    ),
    "890000000006513": (
        "Точность всего ближнего боя считается от <em>Силы</em>. Критический удар в ближнем бою валит цель (<em>Нокаут</em>). Нет штрафа от стимуляторов. От огня получает только <em>30%</em> урона.",
        "All melee accuracy uses <em>Strength</em>. A melee crit knocks the target out (<em>Unconscious</em>). No stim accuracy penalty. Takes only <em>30%</em> fire damage.",
        "jazz:CharacterEffect/SteroidPunch.lua",
    ),
    "890000000006514": (
        "Ледяной шторм",
        "Ice Storm",
        "jazz:CharacterEffect/IcePerk.lua",
    ),
    "890000000006515": (
        "Сигнатурная атака: пять выстрелов по конечностям цели.",
        "Signature attack: five shots at the target's limbs.",
        "jazz:CharacterEffect/IcePerk.lua",
    ),
}


def _brace_end(text: str, open_idx: int) -> int:
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
    text = path.read_text(encoding="utf-8")
    m = re.search(r"DefineClass\.(\w+)\s*=\s*\{", text)
    if not m:
        raise SystemExit(f"no DefineClass in {path}")
    class_id = m.group(1)
    open_brace = m.end() - 1
    close = _brace_end(text, open_brace)
    inner = text[open_brace + 1 : close]
    lines = inner.splitlines(True)
    out: list[str] = []
    skip_keys = {"__parents", "__generated_by_class"}
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        key_m = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s*=", stripped)
        if key_m and key_m.group(1) in skip_keys:
            i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            continue
        out.append(line)
        i += 1
    while out and out[0].strip() == "":
        out.pop(0)
    while out and out[-1].strip() == "":
        out.pop()
    return class_id, "".join(out)


def companion_props_to_items(props: str) -> str:
    lines = props.splitlines(True)
    out: list[str] = []
    depth = 0
    for line in lines:
        stripped = line.lstrip()
        if depth == 0:
            km = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", stripped, re.S)
            if km:
                key, rest = km.group(1), km.group(2)
                indent = line[: len(line) - len(stripped)]
                line = f"{indent}'{key}', {rest}"
                if not line.endswith("\n"):
                    line += "\n"
        depth += line.count("{") - line.count("}")
        if depth < 0:
            depth = 0
        out.append(line)
    return "".join(out)


def build_moditem(class_id: str, group: str, props_items: str) -> str:
    prop_lines = []
    for line in props_items.splitlines(True):
        if line.startswith("\t"):
            rest = line[1:]
            prop_lines.append("\t\t\t\t\t" + rest)
        else:
            prop_lines.append("\t\t\t\t\t" + line if line.strip() else line)
    body = "".join(prop_lines)
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
    needle = f"'Id', \"{class_id}\""
    pos = 0
    while True:
        idx = text.find(needle, pos)
        if idx < 0:
            return None
        start = text.rfind("PlaceObj('ModItemCharacterEffectCompositeDef'", 0, idx)
        if start < 0:
            pos = idx + 1
            continue
        between = text[start:idx]
        if between.count("'Id',") > 0 and between.rfind("'Id',") != between.find("'Id',"):
            pos = idx + 1
            continue
        brace = text.find("{", start)
        end_brace = _brace_end(text, brace)
        end = end_brace + 1
        if text.startswith("),", end):
            end += 2
        if text.startswith("\n", end):
            end += 1
        line_start = text.rfind("\n", 0, start) + 1
        if text[line_start:start].strip() == "":
            start = line_start
        return start, end


def sync_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    if not find_moditem_span(text, "GrizzlyPerk"):
        raise SystemExit("GrizzlyPerk ModItem missing")

    insert_cursor_id = "GrizzlyPerk"
    for class_id, group in PERKS:
        path = CE / f"{class_id}.lua"
        cid, props = extract_define_props(path)
        assert cid == class_id
        props_items = companion_props_to_items(props)
        block = build_moditem(class_id, group, props_items)
        span = find_moditem_span(text, class_id)
        if span:
            text = text[: span[0]] + block + text[span[1] :]
            print(f"items synced {class_id}")
            insert_cursor_id = class_id
        else:
            cursor = find_moditem_span(text, insert_cursor_id)
            if not cursor:
                raise SystemExit(f"insert cursor missing: {insert_cursor_id}")
            text = text[: cursor[1]] + block + text[cursor[1] :]
            insert_cursor_id = class_id
            print(f"items inserted {class_id} after previous")

    ITEMS.write_text(text, encoding="utf-8")
    print("wrote", ITEMS)


def sync_metadata_code() -> None:
    text = META.read_text(encoding="utf-8")
    files = [
        "CharacterEffect/YouSeeIgor.lua",
        "CharacterEffect/WeGotThis.lua",
        "CharacterEffect/NailsPerk.lua",
        "CharacterEffect/JackOfAllTrades.lua",
        "CharacterEffect/SecondStoryMan.lua",
        "CharacterEffect/ShoulderToShoulder.lua",
        "CharacterEffect/SteroidPunch.lua",
        "CharacterEffect/IcePerk.lua",
    ]
    anchor = '"CharacterEffect/GrizzlyPerk.lua",'
    if anchor not in text:
        raise SystemExit("GrizzlyPerk.lua missing from metadata.code")
    missing = [f for f in files if f'"{f}"' not in text]
    if not missing:
        print("metadata.code already lists batch2 CEs")
        return
    block = anchor + "\n" + "\n".join(f'\t\t"{f}",' for f in missing)
    text = text.replace(anchor, block, 1)
    META.write_text(text, encoding="utf-8")
    print("metadata.code inserted:", ", ".join(missing))


def upsert_csv(path: Path, loc: dict[str, tuple[str, str, str]], lang: str) -> None:
    # Runtime schema: ID, Text (T() source, usually RU), Translation (this file's language).
    # Russian.csv Translation must be Russian; English.csv Translation must be English.
    raw = path.read_text(encoding="utf-8-sig")
    reader = csv.reader(io.StringIO(raw))
    rows = list(reader)
    if not rows:
        raise SystemExit(f"empty {path}")
    by_id = {r[0]: i for i, r in enumerate(rows) if r}
    for lid, (ru, en, ctx) in loc.items():
        translation = ru if lang == "ru" else en
        if lid in by_id:
            i = by_id[lid]
            row = rows[i]
            ctx_existing = row[4] if len(row) > 4 else ""
            if "VoiceResponse" in (ctx_existing or ""):
                raise SystemExit(f"REFUSING to overwrite VoiceResponse id {lid} in {path.name}")
            while len(row) < 5:
                row.append("")
            row[1] = ru
            row[2] = translation
            row[4] = ctx
            rows[i] = row
            print(f"{path.name} updated {lid}")
        else:
            rows.append([lid, ru, translation, "", ctx])
            print(f"{path.name} inserted {lid}")
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    writer.writerows(rows)
    path.write_text(buf.getvalue(), encoding="utf-8")


def main() -> None:
    sync_items()
    sync_metadata_code()
    upsert_csv(RU, LOC, "ru")
    upsert_csv(EN, LOC, "en")
    print("batch2 apply done")


if __name__ == "__main__":
    main()
