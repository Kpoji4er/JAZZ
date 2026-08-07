#!/usr/bin/env python3
"""Audit AME biographies, profile blurbs, and their roster projection.

Use --generated after running _gen_ame_unitdata.py to additionally verify the
runtime CSV and jazz-units UnitData projection.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import io
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT.parent / "jazz-units"
TOOLS = Path(__file__).resolve().parent
MERC_LOC_BASE = 890000000005100
MERC_LOC_STRIDE = 10

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

META_EN = re.compile(
    r"\b(?:stats?|tier|level\s*\d*|marksmanship|wisdom|agility|dexterity|"
    r"growth potential|starting kit|irregulars|fighters|hardened|specialists|"
    r"A\.?M\.?E\.?)\b",
    re.I,
)
META_RU = re.compile(
    r"\b(?:статы?|тир(?:ы|ов)?|уров(?:ень|ня|нем|не)|меткост(?:ь|и)|"
    r"мудрост(?:ь|и)|ловкост(?:ь|и)|потенциал роста|стартов\w+ (?:кит|комплект)|"
    r"новобранц\w*|закал[её]нн\w*|специалист\w*|A\.?M\.?E\.?)\b",
    re.I,
)
PROFILE_META = re.compile(
    r"\b(?:stats?|tier|level|marksmanship|wisdom|agility|dexterity|"
    r"статы?|тир(?:ы|ов)?|уров(?:ень|ня)|меткост(?:ь|и)|мудрост(?:ь|и))\b",
    re.I,
)


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _csv_rows(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8-sig")
    if text.startswith("sep="):
        text = text.split("\n", 1)[1]
    return {
        row["ID"]: row
        for row in csv.DictReader(io.StringIO(text))
        if row.get("ID")
    }


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]


def _words(text: str) -> list[str]:
    return re.findall(r"[A-Za-zА-Яа-яЁёÀ-ÖØ-öø-ÿ'-]+", text)


def _opening(text: str) -> str:
    return " ".join(word.casefold() for word in _words(text)[:4])


def _companion_field(path: Path, field: str) -> str | None:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        rf"\b{re.escape(field)}\s*=\s*T\(\d+,\s*\"((?:\\.|[^\"\\])*)\"\)",
        text,
    )
    if not match:
        return None
    escapes = {"n": "\n", "r": "\r", "t": "\t", '"': '"', "\\": "\\"}
    return re.sub(r"\\(.)", lambda item: escapes.get(item.group(1), item.group(1)), match.group(1))


def main(*, check_generated: bool = False) -> int:
    roster_mod = _load_module("ame_roster", TOOLS / "_gen_ame_roster_60.py")
    roster = roster_mod.ROSTER
    copy_bank = roster_mod.AME_COPY_BANK
    ru_csv = _csv_rows(ROOT / "Russian.csv") if check_generated else {}
    en_csv = _csv_rows(ROOT / "English.csv") if check_generated else {}
    errors: list[str] = []
    openings_ru: Counter[str] = Counter()
    openings_en: Counter[str] = Counter()
    sentences_ru: Counter[str] = Counter()
    sentences_en: Counter[str] = Counter()

    if len(roster) != 60:
        errors.append(f"roster has {len(roster)} entries, expected 60")
    if set(copy_bank) != set(range(1, 61)):
        errors.append("copy bank slots differ from exact range 1..60")

    for slot, merc in enumerate(roster, 1):
        uid = f"JAZZ_AME_{slot:02d}"
        copy = copy_bank.get(slot)
        ru = str(merc.get("bio") or "").strip()
        en = str(merc.get("bio_en") or "").strip()
        profile = merc.get("profile")
        label = f"{uid} {merc.get('name', '?')}"

        if not isinstance(copy, dict):
            errors.append(f"{label}: copy bank entry missing")
        else:
            if merc.get("bio") != copy.get("ru"):
                errors.append(f"{label}: ROSTER bio differs from copy bank ru")
            if merc.get("bio_en") != copy.get("en"):
                errors.append(f"{label}: ROSTER bio_en differs from copy bank en")
            if profile != copy.get("profile"):
                errors.append(f"{label}: ROSTER profile differs from copy bank")

        for language, text, meta_re, openings, sentence_counter in (
            ("RU", ru, META_RU, openings_ru, sentences_ru),
            ("EN", en, META_EN, openings_en, sentences_en),
        ):
            sentence_list = _sentences(text)
            word_count = len(_words(text))
            if not 3 <= len(sentence_list) <= 4:
                errors.append(
                    f"{label}: {language} bio has {len(sentence_list)} sentences, expected 3-4"
                )
            if not 38 <= word_count <= 105:
                errors.append(
                    f"{label}: {language} bio has {word_count} words, expected 38-105"
                )
            match = meta_re.search(text)
            if match:
                errors.append(f"{label}: {language} bio contains meta term {match.group(0)!r}")
            if text:
                openings[_opening(text)] += 1
                sentence_counter.update(sentence.casefold() for sentence in sentence_list)

        if not isinstance(profile, dict):
            errors.append(f"{label}: profile mapping missing")
        else:
            for key in ("ru", "en"):
                value = str(profile.get(key) or "").strip()
                if not value:
                    errors.append(f"{label}: profile.{key} missing")
                elif PROFILE_META.search(value):
                    errors.append(f"{label}: profile.{key} contains stat/meta wording")

        if check_generated:
            loc_id = str(MERC_LOC_BASE + (slot - 1) * MERC_LOC_STRIDE + 3)
            ru_row = ru_csv.get(loc_id)
            en_row = en_csv.get(loc_id)
            if not ru_row or not en_row:
                errors.append(f"{label}: localization row {loc_id} missing")
            else:
                if ru_row.get("Text") != en or ru_row.get("Translation") != ru:
                    errors.append(
                        f"{label}: Russian.csv bio projection differs from copy bank"
                    )
                if en_row.get("Text") != en or en_row.get("Translation") != en:
                    errors.append(
                        f"{label}: English.csv bio projection differs from copy bank"
                    )

            companion = UNITS / "UnitData" / f"{uid}.lua"
            if not companion.is_file():
                errors.append(f"{label}: UnitData companion missing")
            else:
                projected = _companion_field(companion, "Bio")
                if projected != en:
                    errors.append(f"{label}: UnitData Bio differs from copy bank")

    for language, openings in (("RU", openings_ru), ("EN", openings_en)):
        for opening, count in openings.items():
            if opening and count > 1:
                errors.append(f"{language}: repeated four-word opening {opening!r} ({count} bios)")
    for language, sentences in (("RU", sentences_ru), ("EN", sentences_en)):
        for sentence, count in sentences.items():
            if sentence and count > 1:
                errors.append(f"{language}: repeated full sentence {sentence!r} ({count} bios)")

    if errors:
        print(f"FAIL AME copy audit ({len(errors)} issues)")
        for error in errors:
            print(f"  {error}")
        return 1
    scope = " + generated files" if check_generated else ""
    print(
        "PASS AME copy audit: 60 distinct RU/EN bios + profiles "
        f"+ exact ROSTER projection{scope}"
    )
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--generated",
        action="store_true",
        help="also verify Russian.csv, English.csv, and jazz-units UnitData",
    )
    args = parser.parse_args()
    raise SystemExit(main(check_generated=args.generated))
