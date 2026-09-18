# -*- coding: utf-8 -*-
"""Upsert JAZZ-UI-MERC-002 chip/popup/CombatLog/timeline loc (890000000009944–009957)."""
from __future__ import annotations

import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = "JAZZ-UI-MERC-002"

# eid, en_src, ru, en
ROWS = [
    ("890000000009944", "MERC $<balance>", "MERC $<balance>", "MERC $<balance>"),
    ("890000000009945", "M.E.R.C. account", "Счёт M.E.R.C.", "M.E.R.C. account"),
    (
        "890000000009946",
        "Unpaid credit. Click to open M.E.R.C. and Pay Account.",
        "Неоплаченный кредит. Нажмите, чтобы открыть M.E.R.C. и оплатить счёт.",
        "Unpaid credit. Click to open M.E.R.C. and Pay Account.",
    ),
    (
        "890000000009947",
        "M.E.R.C. — settle the account",
        "M.E.R.C. — закройте счёт",
        "M.E.R.C. — settle the account",
    ),
    (
        "890000000009948",
        "Speck: your M.E.R.C. account shows $<balance>. All hired MERC contractors leave in 3 days if you do not pay.",
        "Спек: на счету M.E.R.C. $<balance>. Все нанятые контрактники MERC уйдут через 3 дня, если не оплатите.",
        "Speck: your M.E.R.C. account shows $<balance>. All hired MERC contractors leave in 3 days if you do not pay.",
    ),
    (
        "890000000009949",
        "M.E.R.C. — they leave tomorrow",
        "M.E.R.C. — завтра уходят",
        "M.E.R.C. — they leave tomorrow",
    ),
    (
        "890000000009950",
        "Speck: $<balance> still unpaid. Hired MERC contractors leave tomorrow.",
        "Спек: $<balance> всё ещё висит. Нанятые контрактники MERC уходят завтра.",
        "Speck: $<balance> still unpaid. Hired MERC contractors leave tomorrow.",
    ),
    ("890000000009951", "Later", "Позже", "Later"),
    (
        "890000000009952",
        "M.E.R.C. contractors left: <names>",
        "Контрактники M.E.R.C. ушли: <names>",
        "M.E.R.C. contractors left: <names>",
    ),
    ("890000000009953", "M.E.R.C. contractors", "Контрактники M.E.R.C.", "M.E.R.C. contractors"),
    (
        "890000000009954",
        "Hired MERC contractors leave if $<balance> is unpaid.",
        "Нанятые контрактники MERC уйдут, если не закрыть $<balance>.",
        "Hired MERC contractors leave if $<balance> is unpaid.",
    ),
    (
        "890000000009955",
        "Pay Account on the M.E.R.C. site. Right-click opens the site.",
        "Оплатите счёт на сайте M.E.R.C. ПКМ открывает сайт.",
        "Pay Account on the M.E.R.C. site. Right-click opens the site.",
    ),
    (
        "890000000009956",
        "Speck will demand payment. Contractors leave 3 days later if $<balance> is still unpaid.",
        "Спек потребует оплату. Контрактники уйдут через 3 дня, если $<balance> так и висит.",
        "Speck will demand payment. Contractors leave 3 days later if $<balance> is still unpaid.",
    ),
    ("890000000009957", "Open M.E.R.C.", "Открыть M.E.R.C.", "Open M.E.R.C."),
]

IDS = {r[0] for r in ROWS}


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
    cleaned = []
    for row in rows:
        if not row:
            continue
        if row[0] in IDS:
            continue
        cleaned.append(row)

    for eid, en_src, ru, en in ROWS:
        if kind == "ru":
            cleaned.append([eid, en_src, ru, "", SPEC])
        else:
            cleaned.append([eid, ru, en, "", SPEC])

    save_csv(path, sep, cleaned)
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
