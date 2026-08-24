#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lexical QA for combat AI barks. Source: _aibark_bank_data.py

  python docs/tools/_aibark_bank_data.py   # emit markdown
  python docs/tools/_check_aibark_bank.py
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from _aibark_bank_data import BANK, ID0, TAGS, iter_rows, row_count  # noqa: E402

RU_MAX = 42
EN_MAX = 48
VARIANTS = 5
PAIR_STEM = 3  # fail if this many of the five share a content stem
OVERUSE = 2
MIN_FREE = 2  # untagged fallbacks per slot
EXEMPT_PLACE = frozenset({"order_buildings", "order_heights"})
PLACE_STEMS = ("хат", "улиц", "двор", "окн", "двер", "крыш", "холм", "трав")
HOUSE_TOKS = frozenset({"дом", "дома", "дому", "домом", "доме"})

WORD_RU = re.compile(r"[а-яё]+", re.IGNORECASE)

LEX_RU: dict[str, tuple[str, ...]] = {
    "army": (
        "отход",
        "сектор",
        "завес",
        "фланг",
        "рубеж",
        "нажим",
        "охват",
        "очеред",
        "директив",
        "устав",
        "занима",
        "приём",
        "понял",
        "высот",
        "ближн",
    ),
    "clerical": (
        "осуществ",
        "являет",
        "данн",
        "вышеуказ",
        "необход",
        "надлеж",
        "в целях",
        "согласно",
        "достаточно",
    ),
    "literary": (
        "дабы",
        "оный",
        "сей ",
        "довольно",
        "свинц",
        "класть легче",
    ),
    "fenya": (
        "братв",
        "ксив",
        "ксива",
        "стрелк",
        "ментам",
        "мусор",
    ),
    "caption": (
        "гранат",
        "фаер",
        "дымов",
        "пулемёт",
        "пулемет",
        "ракет",
        "стим",
        "снайпер",
        "пистолет",
    ),
    "calque": (
        "в одного",
        "не торчать",
        "держать линию",
        "сосредоточить",
        "размазывать",
        "чтоб морды видно",
        "морды видать",
        "в упор этим",
        "этим в упор",
        "этим в хат",
        "этим в окн",
        "этим в двер",
        "сближа",
        "я рывком",
        "я уже!",
        "подствол",
        "с этим",
        "долго бежать",
    ),
    "label": (
        "серое",  # smoke as "the grey"
    ),
}

# One-word leftovers that are not a spoken shout.
ORPHAN_RU = re.compile(r"^(пру|серое|так|долго)\.?$", re.IGNORECASE)

# "На <ствол>!" as a weapon-switch caption, not a spoken line.
SWITCH_NA = re.compile(
    r"^на (длинный|короткий|ленту|дробь|коротыш|большую|дальний|трубу|нож|железо)!?$",
    re.IGNORECASE,
)

LEX_EN: dict[str, tuple[str, ...]] = {
    "army": (
        "break contact",
        "roger",
        "wilco",
        "affirmative",
        "sector",
        "suppress",
        "flank them",
        "high ground",
        "focus fire",
        "copy that",
    ),
    "staff": (
        "initiat",
        "tactical",
        "deploy",
        "illuminat",
        "occup",
        "proceed",
    ),
    "caption": (
        "grenade",
        "flare gun",
        "smoke grenade",
        "machinegun",
        "machine gun",
        "sniper rifle",
        "pistol",
    ),
}

CONTENT_PREFIX = ("накр",)
CONTENT_WHOLE = ("живо",)


def placeholders(s: str) -> set[str]:
    return set(re.findall(r"<[a-z0-9_]+>", s))


def tokens_ru(s: str) -> list[str]:
    return [m.group(0).lower() for m in WORD_RU.finditer(s)]


def field_hits(text: str, field: dict[str, tuple[str, ...]]) -> list[tuple[str, str]]:
    low = text.lower()
    hits = []
    for cat, needles in field.items():
        for needle in needles:
            if needle in low:
                hits.append((cat, needle))
    return hits


def stem_hits(text: str) -> list[str]:
    found = []
    for tok in tokens_ru(text):
        if tok in CONTENT_WHOLE:
            found.append(tok)
        for stem in CONTENT_PREFIX:
            if tok.startswith(stem):
                found.append(stem)
    return found


def place_hits(ru: str) -> list[str]:
    hits = []
    for tok in tokens_ru(ru):
        if tok == "домой":
            continue
        if tok in HOUSE_TOKS:
            hits.append(tok)
        for stem in PLACE_STEMS:
            if tok.startswith(stem):
                hits.append(stem)
    return hits


def main() -> int:
    errors: list[str] = []
    n = row_count()
    if n != len(list(iter_rows())):
        errors.append("iter_rows mismatch")
    if n != ID0 + n - ID0:
        pass

    seen_ids: set[int] = set()
    stem_at: dict[str, list[str]] = defaultdict(list)
    pair_stems: dict[tuple[str, str], list[str]] = defaultdict(list)

    for event, band, lines in BANK:
        if len(lines) != VARIANTS:
            errors.append(f"{event}/{band}: {len(lines)} lines, want {VARIANTS}")
        free = sum(1 for _ru, _en, tags in lines if not tags)
        if free < MIN_FREE:
            errors.append(f"{event}/{band}: {free} untagged lines, want ≥{MIN_FREE}")

    for event, band, ru, en, tags, sid in iter_rows():
        loc = f"{event}/{band}"
        if sid in seen_ids:
            errors.append(f"{loc}: duplicate id {sid}")
        seen_ids.add(sid)
        if tags - TAGS:
            errors.append(f"{loc}: unknown tags {sorted(tags - TAGS)} «{ru}»")
        if event not in EXEMPT_PLACE:
            places = place_hits(ru)
            if places and not tags:
                errors.append(f"{loc}: place {places} without ctx tag «{ru}»")
        if len(ru) > RU_MAX:
            errors.append(f"{loc}: RU len {len(ru)}>{RU_MAX} «{ru}»")
        if len(en) > EN_MAX:
            errors.append(f"{loc}: EN len {len(en)}>{EN_MAX} «{en}»")
        if ru != ru.strip() or en != en.strip():
            errors.append(f"{loc}: space")
        if placeholders(ru) != placeholders(en):
            errors.append(f"{loc}: placeholder mismatch")
        for cat, needle in field_hits(ru, LEX_RU):
            errors.append(f"{loc}: RU {cat} «{needle}» in «{ru}»")
        for cat, needle in field_hits(en, LEX_EN):
            errors.append(f"{loc}: EN {cat} «{needle}» in «{en}»")
        if SWITCH_NA.match(ru.rstrip(".")):
            errors.append(f"{loc}: switch-caption «{ru}»")
        if ORPHAN_RU.match(ru.strip()):
            errors.append(f"{loc}: orphan-fragment «{ru}»")
        stems = stem_hits(ru)
        for stem in stems:
            stem_at[stem].append(f"{loc}:{event}")
        pair_stems[(event, band)].extend(stems)

    for (event, band), stems in pair_stems.items():
        counts: dict[str, int] = defaultdict(int)
        for stem in stems:
            counts[stem] += 1
        for stem, c in counts.items():
            if c >= PAIR_STEM:
                errors.append(f"{event}/{band}: {c} variants share stem «{stem}»")

    for stem, locs in stem_at.items():
        events = {item.split(":")[-1] for item in locs}
        if len(locs) > OVERUSE and len(events) > 1:
            errors.append(f"overuse stem «{stem}» x{len(locs)} across {sorted(events)}")

    if errors:
        print("FAIL lexical")
        for err in errors:
            print(f"  {err}")
        return 1
    print(f"OK lexical groups={len(BANK)} rows={n} ids={ID0}..{ID0 + n - 1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
