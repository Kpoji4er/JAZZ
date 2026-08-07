# -*- coding: utf-8 -*-
"""Apply canonical bilingual AME mail bodies and listing pitches."""
import codecs
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

WELCOME_EN = """Commander,

Welcome to the African Mercenary Exchange — a local board for fighters who have not spent years building an A.I.M. reputation. Their rates are lower because you are meeting them before the medals and headlines. You are hiring people with room to grow; what they make of the opportunity depends on them, and on whoever gives them the chance.

The board turns over roughly every two weeks. The A.M.E. tab is always open in your PDA, so talk to a candidate while the name is still there.

People we would call first:
<listing>

— A.M.E. desk"""

WELCOME_RU = """Командир,

Африканская биржа наёмников — местная доска тех, кто ещё не успел обзавестись медалями, громким именем и расценками A.I.M. Здесь платят не за легенду, а за человека перед вами. Кто-то только ищет своё место, кто-то уже знает цену выстрелу, но каждому ещё есть куда расти.

Витрина обновляется примерно раз в две недели. Вкладка A.M.E. открыта в КПК с первого дня, поэтому не откладывайте разговор: завтра имени уже может не быть в списке.

Те, кому мы позвонили бы первыми:
<listing>

— Диспетчерская A.M.E."""

LISTING_EN = """Commander,

The board has turned over: a few contracts closed, and new names took their place. These are the people we would call first right now:

<listing>

Specialists rarely wait long for an offer.

— A.M.E. desk"""

LISTING_RU = """Командир,

витрина сменилась: несколько контрактов закрыто, а на их месте появились новые имена. Сейчас мы начали бы с этих:

<listing>

Специалисты редко ждут предложения долго.

— Диспетчерская A.M.E."""

PITCHES = [
    ("890000000006960", "keeps a squad moving after the shooting starts", "поможет отряду снова встать на ноги после стрельбы"),
    ("890000000006961", "knows how to turn raw hands into a team", "умеет собрать команду из необстрелянных людей"),
    ("890000000006962", "makes distance work in your favor", "умеет превратить расстояние в преимущество"),
    ("890000000006963", "understands mines, charges, and stubborn doors", "разбирается в минах, зарядах и упрямых дверях"),
    ("890000000006964", "keeps worn guns and gear alive", "возвращает к жизни изношенные стволы и снаряжение"),
    ("890000000006965", "steady with a rifle and easy to work with", "уверенно держит винтовку и не усложняет работу другим"),
    ("890000000006966", "brings automatic fire when the line needs weight", "добавляет линии огня вес, когда это нужнее всего"),
    ("890000000006967", "holds ground behind a heavy gun", "умеет удержать позицию за тяжёлым стволом"),
    ("890000000006968", "reaches enemies who think a wall is enough", "достанет тех, кто слишком поверил в свою стену"),
    ("890000000006970", "a reliable shot", "стреляет без неприятных сюрпризов"),
    ("890000000006971", "can keep a wound from becoming a funeral", "умеет не дать ране стать причиной похорон"),
    ("890000000006972", "knows one end of a toolkit from the other", "знает, с какой стороны браться за инструмент"),
    ("890000000006973", "does not lose their nerve around explosives", "не теряет головы рядом со взрывчаткой"),
    ("890000000006974", "can carry more than their share", "возьмёт на себя больше своей доли груза"),
    ("890000000006975", "hard to put down", "его нелегко свалить с ног"),
    ("890000000006976", "people tend to listen", "умеет говорить так, что люди слушают"),
    ("890000000006977", "learns quickly", "быстро схватывает новое"),
    ("890000000006978", "moves well under fire", "не теряет лёгкости под огнём"),
    ("890000000006979", "good hands under pressure", "сохраняет точность движений под давлением"),
    ("890000000006980", "an affordable start with room to grow", "недорогой шанс вырастить бойца под себя"),
    ("890000000006981", "ready for field work", "готов к полевой работе"),
    ("890000000006982", "already tested under fire", "уже знает, как звучит настоящий бой"),
    ("890000000006983", "a scarce skill worth securing", "редкое умение, которое лучше не упускать"),
    ("890000000006984", "looking for steady work", "ищет постоянную работу"),
]


def lua_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def patch_items():
    path = ROOT / "items.lua"
    raw = path.read_bytes()
    bom = raw.startswith(codecs.BOM_UTF8)
    text = raw[len(codecs.BOM_UTF8) if bom else 0 :].decode("utf-8")

    def repl(eid: str, tid: int, body: str) -> None:
        nonlocal text
        pat = re.compile(
            rf"(PlaceObj\('ModItemEmail', \{{\s*body = T\({tid}, --\[\[ModItemEmail {eid} body\]\] \")(.*?)(\"\),)",
            re.S,
        )
        m = pat.search(text)
        if not m:
            raise SystemExit(f"body not found for {eid} / {tid}")
        escaped = lua_escape(body)
        text = pat.sub(lambda match: match.group(1) + escaped + match.group(3), text, count=1)

    repl("AME_Welcome", 890000000006907, WELCOME_EN)
    repl("AME_ListingUpdate", 890000000006910, LISTING_EN)
    payload = text.encode("utf-8")
    path.write_bytes((codecs.BOM_UTF8 + payload) if bom else payload)
    print("items.lua: AME email sales copy updated")


def upsert_loc():
    from _apply_ris_editorial import LocEntry, parse_csv_document, upsert_runtime_csv

    rows_def = [
        ("890000000006907", WELCOME_EN, WELCOME_RU),
        ("890000000006910", LISTING_EN, LISTING_RU),
    ] + list(PITCHES)
    entries = {
        localization_id: LocEntry(
            source_en=english,
            russian=russian,
            english=english,
            context="JAZZ-UI-AME-001",
            category="ame",
            locations="",
        )
        for localization_id, english, russian in rows_def
    }
    for path, language in (
        (ROOT / "Russian.csv", "russian"),
        (ROOT / "English.csv", "english"),
    ):
        document = parse_csv_document(path, path.read_bytes())
        updated = upsert_runtime_csv(
            document,
            entries,
            language=language,
            label=path.name,
        )
        path.write_bytes(updated.render())
        print(f"{path.name}: upserted {len(rows_def)} sales/pitch rows")


def main():
    patch_items()
    upsert_loc()


if __name__ == "__main__":
    main()
