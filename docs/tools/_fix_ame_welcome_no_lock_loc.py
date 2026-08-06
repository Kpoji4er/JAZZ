# -*- coding: utf-8 -*-
from pathlib import Path
import csv
import io

ROOT = Path(__file__).resolve().parents[2]
ID = "890000000006907"
EN = (
    "Commander,\n\nWelcome to the African Mercenary Exchange — the local board for fighters without an A.I.M. brand name. "
    "Cheaper because the market prices reputation, not because of where they were born. You are buying potential: people who can grow on your payroll.\n\n"
    "We rotate the shelf about every two weeks. Open the A.M.E. tab in your PDA anytime — hire while the names below are still available.\n\n"
    "This week's picks:\n<listing>\n\nQuestions? Open A.M.E. and talk to them yourself.\n\n— A.M.E. Exchange desk"
)
RU = (
    "Командир,\n\nдобро пожаловать на Африканскую биржу наёмников — местную доску объявлений для бойцов без бренда A.I.M. "
    "Они дешевле, потому что рынок ценит имя и репутацию, а не потому что «местные». Вы платите за потенциал: людей, которые могут вырасти у вас на службе.\n\n"
    "Мы не выкладываем весь пул сразу. Витрина обновляется примерно раз в две недели — кто-то уходит к другим, кто-то пропадает, появляются новые имена. "
    "Вкладку A.M.E. в браузере КПК можно открыть в любой момент.\n\n"
    "Сейчас на витрине:\n<listing>\n\n— Стойка A.M.E. Exchange"
)


def csv_line(row):
    bio = io.StringIO()
    csv.writer(bio, lineterminator="").writerow(row)
    return bio.getvalue()


for name in ("English.csv", "Russian.csv"):
    p = ROOT / name
    lines = p.read_text(encoding="utf-8-sig").splitlines()
    out = []
    for line in lines:
        if not line.strip() or line.startswith("sep="):
            out.append(line)
            continue
        row = next(csv.reader([line]))
        if row and row[0] == ID:
            tag = row[4] if len(row) > 4 else "JAZZ-UI-AME-001"
            empty = row[3] if len(row) > 3 else ""
            if name == "English.csv":
                row = [ID, RU, EN, empty, tag]
            else:
                row = [ID, EN, RU, empty, tag]
            out.append(csv_line(row))
        else:
            out.append(line)
    p.write_text("\n".join(out) + "\n", encoding="utf-8-sig")
    print(name, "ok")
