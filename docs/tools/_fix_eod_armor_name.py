"""Give JazzArmor_EOD its own loc IDs and EOD copy. Flak M69 IDs stay untouched."""
from __future__ import annotations

import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROWS = [
    (
        "890000000014200",
        "Бронежилет EOD",
        "Бронежилет EOD",
        "EOD Vest",
    ),
    (
        "890000000014201",
        "Бронежилеты EOD",
        "Бронежилеты EOD",
        "EOD Vests",
    ),
    (
        "890000000014202",
        "Тяжёлый сапёрный бронежилет для работ по разминированию. Толстые противоосколочные пакеты и высокий воротник хорошо держат взрывную волну, но от винтовочной пули толку мало, а сам жилет ощутимо тяжёлый.",
        "Тяжёлый сапёрный бронежилет для работ по разминированию. Толстые противоосколочные пакеты и высокий воротник хорошо держат взрывную волну, но от винтовочной пули толку мало, а сам жилет ощутимо тяжёлый.",
        "A heavy sapper vest for bomb disposal. Thick fragmentation packs and a high collar handle blast well, but it does little against a rifle round and the vest is noticeably heavy.",
    ),
    (
        "890000000014203",
        "Броня для разминирования",
        "Броня для разминирования",
        "Explosive ordnance disposal armor",
    ),
]
IDS = {row[0] for row in ROWS}
OLD = {
    "DisplayName": (
        'T(385127515445, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD DisplayName]] "Бронежилет Flak M69")',
        'T(890000000014200, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD DisplayName]] "Бронежилет EOD")',
    ),
    "DisplayNamePlural": (
        'T(306986696662, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD DisplayNamePlural]] "Бронежилеты Flak M69")',
        'T(890000000014201, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD DisplayNamePlural]] "Бронежилеты EOD")',
    ),
    "Description": (
        """T(470548861016, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD Description]] 'Модернизированная версия бронежилета "Флак". Фиберглассовые пластины заменены на нейлоновые, что улучшило подвижность бойца. Заодно был добавлен воротник для защиты шеи.')""",
        'T(890000000014202, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD Description]] "Тяжёлый сапёрный бронежилет для работ по разминированию. Толстые противоосколочные пакеты и высокий воротник хорошо держат взрывную волну, но от винтовочной пули толку мало, а сам жилет ощутимо тяжёлый.")',
    ),
    "AdditionalHint": (
        'T(830324932882, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD AdditionalHint]] "Старый американский бронежилет времен войны во вьетнаме")',
        'T(890000000014203, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD AdditionalHint]] "Броня для разминирования")',
    ),
}


def load_csv(path: Path):
    raw = path.read_text(encoding="utf-8")
    sep = ""
    body = raw
    if raw.startswith("sep="):
        first, _, rest = raw.partition("\n")
        sep = first
        body = rest
    rows = list(csv.reader(io.StringIO(body)))
    return sep, rows


def save_csv(path: Path, sep: str, rows):
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    for row in rows:
        writer.writerow(row)
    out = buf.getvalue()
    if sep:
        out = sep + "\n" + out
    if not out.endswith("\n"):
        out += "\n"
    path.write_text(out, encoding="utf-8")


def replace_lua(path: Path):
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in OLD.values():
        count = text.count(old)
        assert count == 1, (path.name, old[:40], count)
        text = text.replace(old, new, 1)
    assert text != original
    path.write_text(text, encoding="utf-8")


def upsert_runtime(path: Path, kind: str):
    sep, rows = load_csv(path)
    header, body = rows[0], [row for row in rows[1:] if row and row[0] not in IDS]
    loc = "jazz:InventoryItem/JazzArmor_EOD.lua"
    for eid, source, russian, english in ROWS:
        if kind == "ru":
            body.append([eid, source, russian, "", loc])
        else:
            body.append([eid, source, english, "", loc])
    save_csv(path, sep, [header] + body)


def upsert_manual(path: Path, kind: str):
    sep, rows = load_csv(path)
    header, body = rows[0], [row for row in rows[1:] if row and row[1] not in IDS]
    next_n = max(int(row[0]) for row in body if row and row[0].isdigit()) + 1
    for offset, (eid, source, russian, english) in enumerate(ROWS):
        if kind == "ru":
            body.append([str(next_n + offset), eid, source, russian, "manual-translation"])
        else:
            body.append([str(next_n + offset), eid, source, english, "manual-translation"])
    save_csv(path, sep, [header] + body)


def upsert_strings(path: Path):
    sep, rows = load_csv(path)
    header, body = rows[0], [row for row in rows[1:] if row and row[0] not in IDS]
    loc = "jazz:InventoryItem/JazzArmor_EOD.lua"
    for eid, source, russian, english in ROWS:
        body.append([
            eid, source, "", russian, english, "new-id",
            loc, "jazz", loc, "manual-translation",
        ])
    save_csv(path, sep, [header] + body)


def main():
    replace_lua(ROOT / "InventoryItem" / "JazzArmor_EOD.lua")
    replace_lua(ROOT / "items.lua")
    upsert_runtime(ROOT / "Russian.csv", "ru")
    upsert_runtime(ROOT / "English.csv", "en")
    upsert_manual(ROOT / "Localization" / "RussianManual.csv", "ru")
    upsert_manual(ROOT / "Localization" / "EnglishManual.csv", "en")
    upsert_strings(ROOT / "Localization" / "Strings.csv")
    for path in (
        ROOT / "InventoryItem" / "JazzArmor_EOD.lua",
        ROOT / "items.lua",
    ):
        text = path.read_text(encoding="utf-8")
        assert "890000000014200" in text and "JazzArmor_EOD" in text
        assert 'JazzArmor_EOD DisplayName]] "Бронежилет Flak M69"' not in text
    print("PASS EOD name split from Flak M69")


if __name__ == "__main__":
    main()
