# -*- coding: utf-8 -*-
"""Trim broken MED-001 loc append and rewrite RU/EN rows for 890000000010200+."""
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

ROWS = [
    # id, ru_text, en_text, context
    ("890000000010200", "Бинт", "Field Bandage", "jazz:MED-001-JazzBandage"),
    (
        "890000000010201",
        "Наложить бинт: снижает кровотечение на один тир у себя или союзника. Без Медицины. Не восстанавливает ОЗ и не лечит травмы.",
        "Apply a field bandage to stop bleeding by one tier on self or ally. No Medical skill. Does not restore HP or heal trauma.",
        "jazz:MED-001-JazzBandage",
    ),
    ("890000000010202", "БИНТ", "BANDAGE", "jazz:MED-001-JazzBandage"),
    (
        "890000000010203",
        "Следующая проверка прогресса: ожидание.",
        "Next progress check: pending.",
        "jazz:MED-001-trauma-timing",
    ),
    (
        "890000000010204",
        "Следующая проверка прогресса: <em>сейчас</em> (может улучшиться или ухудшиться).",
        "Next progress check: <em>due now</em> (may improve or worsen).",
        "jazz:MED-001-trauma-timing",
    ),
    (
        "890000000010205",
        "Следующая проверка прогресса через <em><hours> ч</em> (может улучшиться или ухудшиться).",
        "Next progress check in <em><hours> h</em> (may improve or worsen).",
        "jazz:MED-001-trauma-timing",
    ),
    (
        "890000000010206",
        "Лёгкая травма может сойти сама со временем.",
        "Light trauma can clear on its own over time.",
        "jazz:MED-001-trauma-timing",
    ),
    (
        "890000000010207",
        "Без лечения может улучшиться или ухудшиться.",
        "Without treatment this may improve or worsen.",
        "jazz:MED-001-trauma-timing",
    ),
    (
        "890000000010208",
        "Тяжёлая травма почти не улучшается без госпиталя / полевой хирургии.",
        "Heavy trauma rarely improves without hospital / field surgery.",
        "jazz:MED-001-trauma-timing",
    ),
    (
        "890000000010210",
        "<merc>: травма улучшилась (снята)",
        "<merc> trauma improved (cleared)",
        "jazz:MED-001-trauma-timing",
    ),
    (
        "890000000010211",
        "<merc>: травма улучшилась до более лёгкого тира",
        "<merc> trauma improved to a lighter tier",
        "jazz:MED-001-trauma-timing",
    ),
    (
        "890000000010212",
        "<merc>: травма ухудшилась",
        "<merc> trauma worsened",
        "jazz:MED-001-trauma-timing",
    ),
    (
        "890000000010213",
        "Лечение ИФАК/аптечкой/хирургическим набором. Восстанавливает ОЗ (Медицина) и снимает стаки крови. Не использует стопку бинтов.",
        "Treat an ally with an IFAK, Medkit, or surgical kit. Restores HP (Medical skill) and clears bleeding stacks. Does not use stack bandages.",
        "jazz:MED-001-Bandage-kit",
    ),
]


def csv_escape(s: str) -> str:
    if any(c in s for c in ',"\n'):
        return '"' + s.replace('"', '""') + '"'
    return s


def trim_and_append(path: Path, use_ru: bool) -> None:
    text = path.read_bytes().decode("utf-8-sig")
    lines = text.splitlines()
    kept = []
    for line in lines:
        if line.startswith("890000000010200") or line.startswith("890000000010209"):
            break
        kept.append(line)
    # Drop dangling multiline leftovers after a cut mid-record.
    while kept and (
        kept[-1].startswith("<timing>")
        or kept[-1].startswith("<flavor>")
        or (kept[-1].startswith('"') and "flavor>" in kept[-1])
    ):
        kept.pop()

    for row_id, ru, en, ctx in ROWS:
        # JA3 runtime: Text = English source, Translation = language text
        text_col = en
        trans_col = ru if use_ru else en
        kept.append(f"{row_id},{csv_escape(text_col)},{csv_escape(trans_col)},,{ctx}")

    path.write_text("\n".join(kept) + "\n", encoding="utf-8-sig")
    print(f"{path.name}: lines={len(kept)} last={kept[-1][:70]}")


def main() -> None:
    trim_and_append(BASE / "Russian.csv", use_ru=True)
    trim_and_append(BASE / "English.csv", use_ru=False)


if __name__ == "__main__":
    main()
