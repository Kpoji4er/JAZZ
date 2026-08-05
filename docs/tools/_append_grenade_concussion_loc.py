# Append/upsert Concussion loc + update FragGrenade AdditionalHint in Russian.csv / English.csv.
#
# Runtime CSV: sep=, then data rows (NO header). Columns: ID, Text, Translation, VoiceActor, Context
# - Russian.csv: Translation MUST be Russian (RU client reads Translation).
# - English.csv: Translation MUST be English.
# - Text matches T() source (EN for Concussion CharacterEffect).
#
# Do NOT write id,RU,EN into Russian.csv — that made Concussion tooltips English on RU UI
# (same class as IMP Mimicry / MED AdditionalHint mag-hint stomp).
from __future__ import annotations

import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CONCUSSION = [
    (
        "890000000010277",
        "Concussion",
        "Контузия",
        "jazz:CharacterEffect/Concussion.lua",
    ),
    (
        "890000000010278",
        "Disoriented by blast: <color EmStyle>−<APLoss> AP</color>, <color EmStyle>−<cth_penalty>% chance to hit</color>, move cost <color EmStyle>+<move_ap_modifier>%</color>, no Free Move. Lasts about 1–2 turns.",
        "Дезориентация от взрыва: <color EmStyle>−<APLoss> ОД</color>, <color EmStyle>−<cth_penalty>% к точности</color>, стоимость хода <color EmStyle>+<move_ap_modifier>%</color>, без Free Move. Около 1–2 ходов.",
        "jazz:CharacterEffect/Concussion.lua",
    ),
    (
        "890000000010279",
        "<color EmStyle><DisplayName></color> is concussed",
        "<color EmStyle><DisplayName></color> контужен",
        "jazz:CharacterEffect/Concussion.lua",
    ),
    (
        "890000000010280",
        "<color EmStyle><DisplayName></color> clears concussion",
        "<color EmStyle><DisplayName></color> приходит в себя после контузии",
        "jazz:CharacterEffect/Concussion.lua",
    ),
]

FRAG_OLD = (
    "На близкой дистанции только разброс (Ловкость + Взрывчатка; уверенно примерно с 30)"
)
FRAG_NEW_RU = (
    FRAG_OLD
    + "\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> "
    + "В центре взрыва: шанс <color EmStyle>контузии</color> и зональных <color EmStyle>травм</color>"
)


def read_csv(path: Path) -> tuple[str | None, list[list[str]]]:
    raw = path.read_text(encoding="utf-8-sig")
    sep = None
    body = raw
    if raw.startswith("sep="):
        nl = raw.find("\n")
        sep = raw[:nl].rstrip("\r") if nl >= 0 else raw.rstrip("\r")
        body = raw[nl + 1 :] if nl >= 0 else ""
    return sep, list(csv.reader(io.StringIO(body)))


def write_csv(path: Path, sep: str | None, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        if sep:
            f.write(sep + "\n")
        csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_MINIMAL).writerows(rows)


def upsert_concussion(path: Path, *, russian: bool) -> None:
    sep, rows = read_csv(path)
    changed = 0
    for iid, en, ru, ctx in CONCUSSION:
        text = en
        trans = ru if russian else en
        found = False
        for row in rows:
            if row and row[0] == iid:
                while len(row) < 5:
                    row.append("")
                if row[1] != text or row[2] != trans or row[4] != ctx:
                    row[1], row[2], row[4] = text, trans, ctx
                    changed += 1
                found = True
        if not found:
            rows.append([iid, text, trans, "", ctx])
            changed += 1
    write_csv(path, sep, rows)
    print(f"{path.name}: concussion upsert ({changed} changed)")


def patch_frag_hint(path: Path) -> None:
    text = path.read_text(encoding="utf-8-sig")
    if "243383619902" in text:
        idx = text.find("243383619902")
        window = text[idx : idx + 900]
        if "контузии" in window:
            print(f"{path.name}: Frag hint already mentions concussion")
            return
    if FRAG_OLD not in text:
        raise SystemExit(f"{path.name}: Frag old hint not found")
    text = text.replace(FRAG_OLD, FRAG_NEW_RU)
    path.write_text(text, encoding="utf-8-sig")
    print(f"{path.name}: Frag hint updated")


def main() -> None:
    upsert_concussion(ROOT / "Russian.csv", russian=True)
    upsert_concussion(ROOT / "English.csv", russian=False)
    patch_frag_hint(ROOT / "Russian.csv")
    patch_frag_hint(ROOT / "English.csv")


if __name__ == "__main__":
    main()
