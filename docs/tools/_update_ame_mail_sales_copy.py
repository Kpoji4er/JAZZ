# -*- coding: utf-8 -*-
"""Sales-pitch AME mail listing: update Email bodies + pitch loc (JAZZ-UI-AME-001)."""
from pathlib import Path
import csv
import io
import re

ROOT = Path(__file__).resolve().parents[2]

WELCOME_EN = """Commander,

Welcome to the African Mercenary Exchange — the local board for fighters without an A.I.M. brand name. Cheaper because the market prices reputation, not because of where they were born. You are buying potential: people who can grow on your payroll.

We rotate the shelf about every two weeks. Read this mail to unlock the A.M.E. tab in your PDA — then hire while the names below are still available.

This week's picks:
<listing>

Questions? Open A.M.E. and talk to them yourself.

— A.M.E. Exchange desk"""

WELCOME_RU = """Командир,

добро пожаловать на Африканскую биржу наёмников — местную доску для бойцов без бренда A.I.M. Дешевле, потому что рынок ценит имя, а не происхождение. Вы покупаете потенциал: людей, которые могут вырасти у вас на службе.

Витрина крутится примерно раз в две недели. Прочитайте письмо — откроется вкладка A.M.E. в КПК. Пока эти имена на доске, их ещё можно нанять.

Подборка недели:
<listing>

Вопросы? Откройте A.M.E. и поговорите с ними сами.

— Стойка A.M.E. Exchange"""

LISTING_EN = """Commander,

Fresh names on the board — and a few contracts walked. Here is who is worth a look right now (and why):

<listing>

Don't sleep on specialists: medics, instructors, and snipers do not stay Available forever.

— A.M.E. Exchange desk"""

LISTING_RU = """Командир,

на доске свежие имена — часть контрактов ушла. Кого стоит глянуть прямо сейчас (и почему):

<listing>

Не зевайте на специалистов: медики, инструкторы и снайперы на витрине надолго не задерживаются.

— Стойка A.M.E. Exchange"""

PITCHES = [
    ("890000000006960", "keeps your people on their feet", "держит ваших людей на ногах"),
    ("890000000006961", "turns green recruits into fighters", "делает из зелени бойцов"),
    ("890000000006962", "puts rounds where it hurts from far out", "бьёт больно и издалека"),
    ("890000000006963", "handles bombs, traps, and loud solutions", "бомбы, ловушки и громкие решения"),
    ("890000000006964", "fixes guns and gear when the bush eats them", "чинит стволы, когда кусты их жрут"),
    ("890000000006965", "solid rifle work, no drama", "нормальная винтовка, без драмы"),
    ("890000000006966", "lays down automatic fire when you need volume", "даёт автоогонь, когда нужен объём"),
    ("890000000006967", "anchors the line with a heavy gun", "держит линию тяжёлым стволом"),
    ("890000000006968", "throws trouble over walls and into rooms", "закидывает беду через стены и в комнаты"),
    ("890000000006970", "a sharp shooter", "меткий стрелок"),
    ("890000000006971", "knows how to patch wounds", "умеет зашивать раны"),
    ("890000000006972", "handy with tools and weapons", "на ты с инструментами и оружием"),
    ("890000000006973", "comfortable around explosives", "спокойно с взрывчаткой"),
    ("890000000006974", "built like a truck", "крепкий как грузовик"),
    ("890000000006975", "tough as nails", "живучий до упора"),
    ("890000000006976", "people listen when they speak", "к ним прислушиваются"),
    ("890000000006977", "high growth potential", "высокий потенциал роста"),
    ("890000000006978", "moves fast under fire", "быстрый под огнём"),
    ("890000000006979", "steady hands", "твёрдые руки"),
    ("890000000006980", "cheap entry — room to grow on your payroll", "дешёвый вход — расти будет на вашей зарплате"),
    ("890000000006981", "ready for real jobs, not just guard duty", "готов к настоящей работе, не только к караулу"),
    ("890000000006982", "already blooded — less babysitting", "уже обстрелян — меньше няньки"),
    ("890000000006983", "scarce skill — worth the weekly", "редкий навык — стоит своей недели"),
    ("890000000006984", "looking for steady work", "ищет стабильную работу"),
]


def lua_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def patch_items():
    path = ROOT / "items.lua"
    text = path.read_text(encoding="utf-8")

    def repl(eid: str, tid: int, body: str) -> None:
        nonlocal text
        pat = re.compile(
            rf"(PlaceObj\('ModItemEmail', \{{\s*body = T\({tid}, --\[\[ModItemEmail {eid} body\]\] \")(.*?)(\"\),)",
            re.S,
        )
        m = pat.search(text)
        if not m:
            raise SystemExit(f"body not found for {eid} / {tid}")
        # IMPORTANT: escape for Lua string, then escape for re.sub backrefs
        escaped = lua_escape(body).replace("\\", "\\\\")
        text = pat.sub(rf"\g<1>{escaped}\g<3>", text, count=1)

    repl("AME_Welcome", 890000000006907, WELCOME_EN)
    repl("AME_ListingUpdate", 890000000006910, LISTING_EN)
    path.write_text(text, encoding="utf-8")
    print("items.lua: AME email sales copy updated")


def load_csv(path: Path):
    raw = path.read_text(encoding="utf-8-sig")
    sep = None
    body = raw
    if raw.startswith("sep="):
        nl = raw.find("\n")
        sep = raw[:nl]
        body = raw[nl + 1 :]
    return sep, list(csv.reader(io.StringIO(body)))


def save_csv(path: Path, sep, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    for row in rows:
        w.writerow(row)
    out = buf.getvalue()
    if sep:
        out = sep + "\n" + out
    if not out.endswith("\n"):
        out += "\n"
    path.write_text(out, encoding="utf-8")


def upsert_loc():
    rows_def = [
        ("890000000006907", WELCOME_EN, WELCOME_RU),
        ("890000000006910", LISTING_EN, LISTING_RU),
    ] + list(PITCHES)
    ids = {r[0] for r in rows_def}
    for path, kind in ((ROOT / "Russian.csv", "ru"), (ROOT / "English.csv", "en")):
        sep, rows = load_csv(path)
        cleaned = [r for r in rows if r and r[0] not in ids]
        for eid, en, ru in rows_def:
            if kind == "ru":
                cleaned.append([eid, en, ru, "", "JAZZ-UI-AME-001"])
            else:
                cleaned.append([eid, ru, en, "", "JAZZ-UI-AME-001"])
        save_csv(path, sep, cleaned)
        print(f"{path.name}: upserted {len(rows_def)} sales/pitch rows")


def main():
    patch_items()
    upsert_loc()


if __name__ == "__main__":
    main()
