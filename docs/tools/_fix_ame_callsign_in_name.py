# Insert callsign into AME Name when Nick is a real callsign (not shortened given name).
# Vanilla quoting: T(id, --[[comment]] 'First "Nick" Last')
#
# Usage (from jazz/):
#   python docs/tools/_fix_ame_callsign_in_name.py
#   python docs/tools/_fix_ame_callsign_in_name.py --apply

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT.parent / "jazz-units"
UNITDATA = UNITS / "UnitData"
ITEMS = UNITS / "items.lua"
RU = ROOT / "Russian.csv"
EN = ROOT / "English.csv"

# unit -> (name_id, nick_id, name_en, nick_en, name_ru, nick_ru)
ROSTER = {
    "JAZZ_AME_23": (
        "890000000005320",
        "890000000005321",
        "Chukwuemeka Obi",
        "Emeka",
        "Чуквуэмека Оби",
        "Эмека",
    ),
    "JAZZ_AME_39": (
        "890000000005480",
        "890000000005481",
        "Joseph Mukendi",
        "Hyena",
        "Жозеф Мукенди",
        "Гиена",
    ),
    "JAZZ_AME_41": (
        "890000000005500",
        "890000000005501",
        "Sipho Khumalo",
        "Anvil",
        "Сифо Кхумало",
        "Наковальня",
    ),
    "JAZZ_AME_43": (
        "890000000005520",
        "890000000005521",
        "Didier Mbemba",
        "Smoke",
        "Дидье Мбемба",
        "Дым",
    ),
    "JAZZ_AME_47": (
        "890000000005560",
        "890000000005561",
        "Hassan Ibrahim",
        "Scorpion",
        "Хассан Ибрахим",
        "Скорпион",
    ),
}


def with_callsign(name: str, nick: str) -> str:
    parts = name.split()
    if len(parts) < 2:
        return f'{name} "{nick}"'
    return f'{parts[0]} "{nick}" {" ".join(parts[1:])}'


def apply_csv(path: Path, id_: str, new_text: str, new_translation: str) -> None:
    import io

    lines = path.read_text(encoding="utf-8-sig").splitlines(keepends=True)
    for i, line in enumerate(lines):
        if not line.startswith(f"{id_},"):
            continue
        row = next(csv.reader([line.rstrip("\r\n")]))
        while len(row) < 3:
            row.append("")
        row[1] = new_text
        row[2] = new_translation
        ending = "\r\n" if line.endswith("\r\n") else ("\n" if line.endswith("\n") else "")
        buf = io.StringIO()
        csv.writer(buf, lineterminator="").writerow(row)
        lines[i] = buf.getvalue() + ending
        path.write_text("".join(lines), encoding="utf-8-sig", newline="")
        return
    raise SystemExit(f"CSV id not found in {path.name}: {id_}")


def replace_companion_name(text: str, unit: str, name_id: str, name_en_new: str) -> str:
    new_line = (
        f"\tName = T({name_id}, --[[ModItemUnitDataCompositeDef {unit} Name]] "
        f"'{name_en_new}'),"
    )
    pat = re.compile(rf"^[ \t]*Name = T\({name_id},.*$", re.M)
    text2, n = pat.subn(new_line, text, count=1)
    if n != 1:
        raise SystemExit(f"companion Name replace failed: {unit}")
    return text2


def replace_items_name(items: str, unit: str, name_id: str, name_en_new: str) -> str:
    new_snip = (
        f"'Name', T({name_id}, --[[ModItemUnitDataCompositeDef {unit} Name]] "
        f"'{name_en_new}'),"
    )
    pat = re.compile(rf"^([ \t]*)'Name', T\({name_id},.*$", re.M)

    def repl(m: re.Match) -> str:
        return f"{m.group(1)}{new_snip}"

    items2, n = pat.subn(repl, items, count=1)
    if n != 1:
        raise SystemExit(f"items.lua Name replace failed: {unit} id={name_id}")
    return items2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    print(f"callsign Names to fix: {len(ROSTER)}")
    planned = []
    for unit, (name_id, nick_id, name_en, nick_en, name_ru, nick_ru) in ROSTER.items():
        name_en_new = with_callsign(name_en, nick_en)
        name_ru_new = with_callsign(name_ru, nick_ru)
        planned.append(
            {
                "unit": unit,
                "name_id": name_id,
                "nick_id": nick_id,
                "name_en": name_en,
                "nick_en": nick_en,
                "name_en_new": name_en_new,
                "name_ru_new": name_ru_new,
                "nick_ru": nick_ru,
            }
        )
        print(f"  {unit}: EN {name_en!r} -> {name_en_new!r}")
        print(f"           RU {name_ru!r} -> {name_ru_new!r}")

    if not args.apply:
        print("Dry-run only. Pass --apply to write.")
        return 0

    items = ITEMS.read_text(encoding="utf-8")
    for r in planned:
        path = UNITDATA / f"{r['unit']}.lua"
        text = replace_companion_name(
            path.read_text(encoding="utf-8"), r["unit"], r["name_id"], r["name_en_new"]
        )
        path.write_text(text, encoding="utf-8", newline="\n")
        items = replace_items_name(items, r["unit"], r["name_id"], r["name_en_new"])
        apply_csv(RU, r["name_id"], r["name_en_new"], r["name_ru_new"])
        apply_csv(EN, r["name_id"], r["name_en_new"], r["name_en_new"])
        # Anvil RU nick polish
        if r["unit"] == "JAZZ_AME_41":
            apply_csv(RU, r["nick_id"], r["nick_en"], r["nick_ru"])
            apply_csv(EN, r["nick_id"], r["nick_en"], r["nick_en"])

    ITEMS.write_text(items, encoding="utf-8", newline="\n")
    print("applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
