# -*- coding: utf-8 -*-
"""Append/fix MERC mail+UI loc (JAZZ-UI-MERC-001). Mirrors _append_ame_mail_loc.py CSV handling."""
from __future__ import annotations

import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

WELCOME_EN = (
    "Commander!\n\n"
    "Great news — M.E.R.C. is OPEN FOR BUSINESS again. Fresh site, same low daily rates, "
    "and you don't pay up front. Hire now, settle the account when you can. "
    "(I'll nudge you. Friendly-like.)\n\n"
    "One snag. My partner Biff was supposed to keep the books. He hasn't checked in. "
    "If you bump into him out there, tell him Speck needs him back at the desk. "
    "Preferably still breathing.\n\n"
    "Open M.E.R.C. in your PDA browser and pick a contractor. We're not A.I.M. — we're cheaper.\n\n"
    "Your friend in the hiring business,\n"
    "Speck T. Kline\n"
    "M.E.R.C. — More Economic Recruiting Center"
)

WELCOME_RU = (
    "Командир!\n\n"
    "Отличные новости — M.E.R.C. СНОВА ОТКРЫТ. Новый сайт, те же низкие дневные ставки, "
    "и платить вперёд не надо. Нанимайте сейчас, счёт закроете когда сможете. "
    "(Я напомню. Дружески.)\n\n"
    "Одна загвоздка. Партнёр Бифф должен был вести книги — и пропал. "
    "Если наткнётесь на него в поле, передайте: Спеку он нужен за столом. "
    "Желательно живым.\n\n"
    "Откройте M.E.R.C. в браузере КПК и выбирайте бойца. Мы не A.I.M. — мы дешевле.\n\n"
    "Ваш друг по найму,\n"
    "Спек Т. Клайн\n"
    "M.E.R.C. — More Economic Recruiting Center"
)

# eid, en_src (Text for RU csv / Translation for EN csv patterns per AME tool), ru, en
ROWS = [
    ("890000000009900", "Org:", "Орг.:", "Org:"),
    ("890000000009901", "Status:", "Статус:", "Status:"),
    (
        "890000000009902",
        "<style AimCopyrightTextC><copyright></style> M.E.R.C.",
        "<style AimCopyrightTextC><copyright></style> M.E.R.C.",
        "<style AimCopyrightTextC><copyright></style> M.E.R.C.",
    ),
    ("890000000009903", "All", "Все", "All"),
    ("890000000009904", "Available", "Доступны", "Available"),
    (
        "890000000009905",
        "My Team [<MERCPlayerMercCount()>]",
        "Моя команда [<MERCPlayerMercCount()>]",
        "My Team [<MERCPlayerMercCount()>]",
    ),
    ("890000000009906", "M.E.R.C.", "M.E.R.C.", "M.E.R.C."),
    (
        "890000000009907",
        "<style PDAMercPrice_Dead>Killed in action</style>",
        "<style PDAMercPrice_Dead>Погиб в бою</style>",
        "<style PDAMercPrice_Dead>Killed in action</style>",
    ),
    ("890000000009908", "Missing in action", "Пропал без вести", "Missing in action"),
    ("890000000009909", "Speck <speck@merc.com>", "Спек <speck@merc.com>", "Speck <speck@merc.com>"),
    ("890000000009910", WELCOME_EN, WELCOME_RU, WELCOME_EN),
    (
        "890000000009911",
        "M.E.R.C. is OPEN — and where's Biff?",
        "M.E.R.C. ОТКРЫТ — а где Бифф?",
        "M.E.R.C. is OPEN — and where's Biff?",
    ),
    ("890000000009912", "Speck <accounts@merc.com>", "Спек <accounts@merc.com>", "Speck <accounts@merc.com>"),
    (
        "890000000009913",
        "Commander!\n\n"
        "Hate to bother a valued customer, but your M.E.R.C. account still shows $<balance> outstanding.\n\n"
        "Daily rates, remember? Pay Account on the site before my people start writing resignation notes "
        "in muddy boots.\n\n"
        "Speck",
        "Командир!\n\n"
        "Не люблю дёргать ценного клиента, но на счету M.E.R.C. всё ещё $<balance>.\n\n"
        "Дневные ставки, помните? Жмите Pay Account на сайте, пока мои люди не начнут писать "
        "заявления об уходе в грязных ботинках.\n\n"
        "Спек",
        "Commander!\n\n"
        "Hate to bother a valued customer, but your M.E.R.C. account still shows $<balance> outstanding.\n\n"
        "Daily rates, remember? Pay Account on the site before my people start writing resignation notes "
        "in muddy boots.\n\n"
        "Speck",
    ),
    ("890000000009914", "M.E.R.C. — please settle up", "M.E.R.C. — закройте счёт", "M.E.R.C. — please settle up"),
    ("890000000009915", "Speck <accounts@merc.com>", "Спек <accounts@merc.com>", "Speck <accounts@merc.com>"),
    (
        "890000000009916",
        "Commander!\n\n"
        "I warned you. $<balance> still unpaid. My contractors walked.\n\n"
        "Want them back? Clear the ledger first — if any of them still answer the phone.\n\n"
        "Speck",
        "Командир!\n\n"
        "Я предупреждал. $<balance> так и висит. Контрактники ушли.\n\n"
        "Хотите вернуть — сначала закройте счёт. Если кто-то ещё возьмёт трубку.\n\n"
        "Спек",
        "Commander!\n\n"
        "I warned you. $<balance> still unpaid. My contractors walked.\n\n"
        "Want them back? Clear the ledger first — if any of them still answer the phone.\n\n"
        "Speck",
    ),
    ("890000000009917", "M.E.R.C. — they're walking", "M.E.R.C. — они уходят", "M.E.R.C. — they're walking"),
    ("890000000009918", "MERC due: $<balance>", "Долг MERC: $<balance>", "MERC due: $<balance>"),
    ("890000000009919", "Pay Account", "Оплатить счёт", "Pay Account"),
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
        eid = row[0]
        if eid in IDS and len(row) < 5:
            continue
        if eid in IDS:
            continue
        cleaned.append(row)

    for eid, en_src, ru, en in ROWS:
        if kind == "ru":
            cleaned.append([eid, en_src, ru, "", "JAZZ-UI-MERC-001"])
        else:
            cleaned.append([eid, ru, en, "", "JAZZ-UI-MERC-001"])

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
