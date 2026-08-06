# -*- coding: utf-8 -*-
"""Append/fix AME mail loc (JAZZ-UI-AME-001). Proper multiline CSV via csv module."""
from pathlib import Path
import csv
import io

ROOT = Path(__file__).resolve().parents[2]

ROWS = [
    ("890000000006900", "Irregulars", "Новобранцы", "Irregulars"),
    ("890000000006901", "Fighters", "Бойцы", "Fighters"),
    ("890000000006902", "Hardened", "Закалённые", "Hardened"),
    ("890000000006903", "Specialists", "Специалисты", "Specialists"),
    ("890000000006904", "(no fighters listed right now)", "(сейчас на витрине никого нет)", "(no fighters listed right now)"),
    (
        "890000000006905",
        "AME Exchange <welcome@ame-exchange.net>",
        "AME Exchange <welcome@ame-exchange.net>",
        "AME Exchange <welcome@ame-exchange.net>",
    ),
    (
        "890000000006906",
        "African Mercenary Exchange — welcome",
        "Африканская биржа наёмников — добро пожаловать",
        "African Mercenary Exchange — welcome",
    ),
    (
        "890000000006907",
        "Commander,\n\nWelcome to the African Mercenary Exchange — a local hiring board for fighters who do not have an A.I.M. brand name behind them. They cost less because the market prices reputation, not because of where they were born. What you buy is potential: people who can grow on your payroll.\n\nWe do not put the whole pool on the shelf at once. The listing rotates about every two weeks — some leave for other work, some vanish, and new names appear. Open the A.M.E. tab in your PDA browser after you have read this message.\n\nCurrently available:\n<listing>\n\n— A.M.E. Exchange desk",
        "Командир,\n\nдобро пожаловать на Африканскую биржу наёмников — местную доску объявлений для бойцов без бренда A.I.M. Они дешевле, потому что рынок ценит имя и репутацию, а не потому что «местные». Вы платите за потенциал: людей, которые могут вырасти у вас на службе.\n\nМы не выкладываем весь пул сразу. Витрина обновляется примерно раз в две недели — кто-то уходит к другим, кто-то пропадает, появляются новые имена. Вкладку A.M.E. в браузере КПК можно открыть после прочтения этого письма.\n\nСейчас на витрине:\n<listing>\n\n— Стойка A.M.E. Exchange",
        "Commander,\n\nWelcome to the African Mercenary Exchange — a local hiring board for fighters who do not have an A.I.M. brand name behind them. They cost less because the market prices reputation, not because of where they were born. What you buy is potential: people who can grow on your payroll.\n\nWe do not put the whole pool on the shelf at once. The listing rotates about every two weeks — some leave for other work, some vanish, and new names appear. Open the A.M.E. tab in your PDA browser after you have read this message.\n\nCurrently available:\n<listing>\n\n— A.M.E. Exchange desk",
    ),
    (
        "890000000006908",
        "AME Exchange <desk@ame-exchange.net>",
        "AME Exchange <desk@ame-exchange.net>",
        "AME Exchange <desk@ame-exchange.net>",
    ),
    (
        "890000000006909",
        "A.M.E. — listing update",
        "A.M.E. — обновление витрины",
        "A.M.E. — listing update",
    ),
    (
        "890000000006910",
        "Commander,\n\nThe Exchange listing has changed. Some contracts closed or fighters moved on; new names are on the board.\n\nCurrently available:\n<listing>\n\nCheck the A.M.E. tab in your PDA when you can.\n\n— A.M.E. Exchange desk",
        "Командир,\n\nвитрина Биржи обновилась. Часть контрактов закрыта или бойцы ушли к другим работодателям; на доске появились новые имена.\n\nСейчас на витрине:\n<listing>\n\nЗагляните во вкладку A.M.E. в КПК, когда будет минута.\n\n— Стойка A.M.E. Exchange",
        "Commander,\n\nThe Exchange listing has changed. Some contracts closed or fighters moved on; new names are on the board.\n\nCurrently available:\n<listing>\n\nCheck the A.M.E. tab in your PDA when you can.\n\n— A.M.E. Exchange desk",
    ),
]

IDS = {r[0] for r in ROWS}


def load_csv(path: Path):
    raw = path.read_text(encoding="utf-8-sig")
    sep = None
    body = raw
    if raw.startswith("sep="):
        nl = raw.find("\n")
        sep = raw[:nl]
        body = raw[nl + 1 :]
    rows = list(csv.reader(io.StringIO(body)))
    return sep, rows


def save_csv(path: Path, sep, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    for row in rows:
        w.writerow(row)
    out = buf.getvalue()
    if sep:
        out = sep + "\n" + out
    if not out.endswith("\n"):
        out += "\n"
    path.write_text(out, encoding="utf-8")


def upsert(path: Path, kind: str):
    sep, rows = load_csv(path)
    # Drop broken partial rows from previous bad append (id only / short)
    cleaned = []
    for row in rows:
        if not row:
            continue
        eid = row[0]
        if eid in IDS and len(row) < 5:
            continue  # replace below
        if eid in IDS:
            continue  # will re-add
        cleaned.append(row)

    for eid, en_src, ru, en in ROWS:
        if kind == "ru":
            cleaned.append([eid, en_src, ru, "", "JAZZ-UI-AME-001"])
        else:
            cleaned.append([eid, ru, en, "", "JAZZ-UI-AME-001"])

    save_csv(path, sep, cleaned)
    # verify
    _, check = load_csv(path)
    by_id = {r[0]: r for r in check if r}
    for eid, *_ in ROWS:
        assert eid in by_id and len(by_id[eid]) >= 5, (eid, by_id.get(eid))
    print(f"{path.name}: OK {len(ROWS)} rows")


def main():
    upsert(ROOT / "Russian.csv", "ru")
    upsert(ROOT / "English.csv", "en")


if __name__ == "__main__":
    main()
