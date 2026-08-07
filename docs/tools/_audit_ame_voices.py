"""Audit AME voice assignment, audio files, and bilingual subtitles."""
from __future__ import annotations

import csv
import io
import re
from collections import Counter
from pathlib import Path

from _ame_voice_subtitles_ru import russian_subtitle

JAZZ = Path(__file__).resolve().parents[2]
JU = Path(__file__).resolve().parents[2].parent / "jazz-units"
UD = JU / "UnitData"
ITEMS = JU / "items.lua"
VOICES = JU / "voices"
VR_BEGIN = "-- JAZZ-UNITS-005-AME-VR-BEGIN"
VR_END = "-- JAZZ-UNITS-005-AME-VR-END"
VOICE_LOC_CONTEXT = "jazz-units:items.lua:VoiceResponse AME"


def _csv_by_id(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8-sig")
    if text.startswith("sep="):
        text = text.split("\n", 1)[1]
    rows = csv.DictReader(io.StringIO(text))
    return {row["ID"]: row for row in rows if row.get("ID")}


def _voice_rows() -> list[tuple[str, str, str]]:
    text = ITEMS.read_text(encoding="utf-8")
    begin = text.find(VR_BEGIN)
    end = text.find(VR_END)
    if begin < 0 or end <= begin:
        raise AssertionError("AME VoiceResponse marked block missing")
    block = text[begin:end]
    rows = re.findall(
        r'T\((\d+), --\[\[ModItemVoiceResponse ([A-Za-z0-9_]+) [^\r\n]*?\]\] "((?:\\.|[^"\\])*)"\)',
        block,
    )
    return [
        (localization_id, preset, bytes(source, "utf-8").decode("unicode_escape"))
        if "\\" in source
        else (localization_id, preset, source)
        for localization_id, preset, source in rows
    ]


def main() -> int:
    errors: list[str] = []
    c: Counter[str] = Counter()
    details: list[tuple[str, str]] = []
    for p in sorted(UD.glob("JAZZ_AME_*.lua")):
        text = p.read_text(encoding="utf-8")
        vr = "?"
        for line in text.splitlines():
            if "VoiceResponseId" in line:
                vr = line.split("=", 1)[1].strip().rstrip(",").strip('"')
                break
        c[vr] += 1
        details.append((p.stem, vr))

    n = len(details)
    imp = sum(v for k, v in c.items() if k.startswith("IMP_"))
    jazz = sum(v for k, v in c.items() if k.startswith("Jazz_"))
    other = n - imp - jazz
    print(f"total={n}")
    print(f"IMP={imp} ({100 * imp / n:.1f}%)")
    print(f"Jazz_AME={jazz} ({100 * jazz / n:.1f}%)")
    print(f"other={other} ({100 * other / n:.1f}%)")
    print("breakdown:")
    for k, v in c.most_common():
        print(f"  {k}: {v}")
    print("slots:")
    for stem, vr in details:
        print(f"  {stem}: {vr}")

    if n != 60:
        errors.append(f"expected 60 AME UnitData companions, found {n}")

    rows = _voice_rows()
    if len(rows) != 114:
        errors.append(f"expected 114 generated voice lines, found {len(rows)}")
    if len({localization_id for localization_id, _, _ in rows}) != len(rows):
        errors.append("duplicate localization IDs in AME VoiceResponse block")

    ru = _csv_by_id(JAZZ / "Russian.csv")
    en = _csv_by_id(JAZZ / "English.csv")
    for localization_id, preset, source in rows:
        if re.search(r"\b(Legion|Major|Grand Chien|national symbols?)\b", source, re.I):
            errors.append(f"{localization_id}: faction-specific donor line: {source!r}")
        try:
            expected_ru = russian_subtitle(source, preset)
        except KeyError as error:
            errors.append(str(error))
            continue
        ru_row = ru.get(localization_id)
        en_row = en.get(localization_id)
        if not ru_row or not en_row:
            errors.append(f"{localization_id}: missing runtime localization row")
            continue
        if ru_row["Text"] != source or ru_row["Translation"] != expected_ru:
            errors.append(f"{localization_id}: Russian.csv differs from audible phrase")
        if en_row["Text"] != source or en_row["Translation"] != source:
            errors.append(f"{localization_id}: English.csv differs from audible phrase")
        if not (VOICES / f"{localization_id}.opus").is_file():
            errors.append(f"{localization_id}: opus missing")

    expected_ids = {localization_id for localization_id, _, _ in rows}
    for name, table in (("Russian.csv", ru), ("English.csv", en)):
        managed_ids = {
            localization_id
            for localization_id, row in table.items()
            if row.get("Context") == VOICE_LOC_CONTEXT
        }
        if managed_ids != expected_ids:
            errors.append(
                f"{name}: managed voice IDs differ from items "
                f"(missing={len(expected_ids - managed_ids)}, extra={len(managed_ids - expected_ids)})"
            )

    if errors:
        print("FAIL:")
        for error in errors:
            print(f"  {error}")
        return 1
    print(f"PASS AME voice copy/audio sync ({len(rows)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
