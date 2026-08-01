# -*- coding: utf-8 -*-
"""Apply Russian translations for workshop merc AIM SNYPE hire chat lines."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RU_CSV = ROOT / "Russian.csv"
MANUAL = ROOT / "Localization" / "RussianManual.csv"

# ID -> Russian Translation (SourceText / Text stays English from T())
TRANSLATIONS: dict[str, str] = {
    # --- Merc_SamuelNkosi ---
    "592681872481": "С вами говорит Самуэль Нкоси. Чем могу помочь?",
    "979669120158": (
        "Здравствуйте, вы дозвонились до Самуэля Нкоси. Извините, я пропустил ваш звонок. "
        "Сейчас я особенно занят, но если оставите номер и короткое сообщение, "
        "я перезвоню при первой возможности."
    ),
    "399892814797": "Привет, рад снова с вами поговорить.",
    "518273598044": "Эй, у меня не весь день. Зачем вы звонили?",
    "462159909484": "Ваши условия звучат справедливо. Я согласен.",
    "852151262223": "Эй, нам нужно поговорить о моём контракте. Надеюсь, мы снова договоримся.",
    "734949798117": "Это достойное предложение. Я принимаю.",
    "813014999872": (
        "Мне не очень хочется работать с этим немцем по имени Грунти. "
        "Но мы можем договориться, если вы добавите сверху к моей зарплате "
        "за возможные неудобства с его стороны."
    ),
    # Nick typo fix (was «Самулэь»); keep Text=EN source in apply logic
    "141954478311": "Самуэль",
    # --- Merc_JerrySinclair ---
    "162045764185": "С вами говорит Джерри Синклер. Нужна механическая помощь?",
    "352332137969": (
        "Вы дозвонились до Джерри Синклера. К сожалению, я сейчас не могу ответить, "
        "но оставьте сообщение — и я быстро перезвоню."
    ),
    "105486838898": "Я знал, что вы перезвоните. Я лучший механик, которого можно найти за ваши деньги.",
    "172029544435": (
        "Да ладно вам, мне правда нужно выгулять собаку. "
        "Скажите, чего хотите, или уже кладите трубку."
    ),
    "857370343482": "Ладно, звучит как хорошая сделка. Выезжаю немедленно.",
    "120667680807": "Это Джерри. Нам нужно поговорить о моём контракте. Интересует продление?",
    "940539384341": "Большое спасибо за доверие. Вы не пожалеете.",
    "492954200051": (
        "Я уже работал с этим пьющим русским. Скажу прямо — удовольствия было мало. "
        "Но думаю, за доплату мы как-нибудь сработаемся."
    ),
    # --- Merc_MildredPatterson ---
    "169750321810": (
        "Вы дозвонились до Милдред Паттерсон. Спасибо за звонок. "
        "Оставьте короткое сообщение, и я отвечу, как только позволит время."
    ),
    "641341334949": (
        "Доброе утро, с вами говорит Милдред Паттерсон. "
        "Пожалуйста, объясните причину вашего звонка."
    ),
    "971375804811": "С вами говорит Милдред Паттерсон. Скажите, пожалуйста, чем могу помочь?",
    "482117704614": "Простите, не могли бы вы уже сказать, в чём причина вашего звонка?",
    "118276112116": (
        "Я могу согласиться на эти условия контракта. "
        "Было приятно с вами поговорить. Встретимся на месте."
    ),
    "110729622402": "Нам нужно обсудить новый контракт. Что скажете насчёт продления?",
    "584882121239": "Я рада, что мы пришли к новому соглашению.",
    # --- Merc_HectorSanchez (broken speech, matches VR style) ---
    "135993321037": "Ты говорить с Гектор Санчес. Гектор плохо английский. Что ты хотеть?",
    "730561750335": (
        "Ты позвонить Гектор Санчес. Гектор нет здесь. "
        "Оставить номер после Бип, и Гектор перезвонить потом."
    ),
    "523627989001": "Это Гектор. Что ты хотеть?",
    "411154719819": "Алло... Алло? — Гектор не любить розыгрыш... Говорить с Гектор!",
    "313244239742": "Гектор доволен условиями. У нас сделка.",
    "573437956087": "Гектор рад и хочет остаться. Гектору нужен новый контракт. Мы делать сделка?",
    "406968238869": "Отлично! Гектор заплатит за следующий круг пива!",
    "321599305977": "Гектор не любить воевать с ребёнком как MD. Гектор хотеть больше денег!",
}


def write_csv(path: Path, header_sep: bool, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        if header_sep:
            f.write("sep=,\n")
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            lineterminator="\n",
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    with RU_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        first = f.readline()
        if not first.startswith("sep="):
            raise SystemExit(f"Unexpected Russian.csv header: {first!r}")
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    by_id = {r["ID"]: r for r in rows}
    missing = [i for i in TRANSLATIONS if i not in by_id]
    if missing:
        raise SystemExit(f"Missing IDs in Russian.csv: {missing}")

    updated = 0
    for tid, ru in TRANSLATIONS.items():
        row = by_id[tid]
        # Nick: restore EN Text from T(), put RU in Translation (was typo «Самулэь»).
        if tid == "141954478311":
            if row.get("Text") != "Samuel":
                row["Text"] = "Samuel"
            if row.get("Translation") != ru:
                row["Translation"] = ru
                updated += 1
            continue
        if row.get("Translation") != ru:
            row["Translation"] = ru
            updated += 1

    write_csv(RU_CSV, True, fieldnames, rows)
    print(f"Russian.csv: updated Translation for {updated} IDs (of {len(TRANSLATIONS)} targets)")

    # Append / upsert RussianManual by SourceText
    with MANUAL.open("r", encoding="utf-8-sig", newline="") as f:
        mreader = csv.DictReader(f)
        mfields = list(mreader.fieldnames or [])
        mrows = list(mreader)

    by_source = {r.get("SourceText"): i for i, r in enumerate(mrows)}
    next_n = 1
    for r in mrows:
        try:
            next_n = max(next_n, int(r.get("N") or 0) + 1)
        except ValueError:
            pass

    manual_added = 0
    manual_updated = 0
    for tid, ru in TRANSLATIONS.items():
        src = by_id[tid].get("Text") or ""
        if tid == "141954478311":
            src = "Samuel"
        entry = {
            "N": str(next_n),
            "AnchorID": tid,
            "SourceText": src,
            "Russian": ru,
            "Notes": "manual-translation",
        }
        if src in by_source:
            idx = by_source[src]
            old = mrows[idx]
            entry["N"] = old.get("N") or entry["N"]
            if old.get("Russian") != ru or old.get("Notes") != "manual-translation":
                mrows[idx] = entry
                manual_updated += 1
        else:
            mrows.append(entry)
            by_source[src] = len(mrows) - 1
            next_n += 1
            manual_added += 1

    write_csv(MANUAL, False, mfields, mrows)
    print(f"RussianManual.csv: added={manual_added} updated={manual_updated}")

    # Verify
    import re

    with RU_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        f.readline()
        check = {r["ID"]: r for r in csv.DictReader(f)}
    bad = []
    for tid, ru in TRANSLATIONS.items():
        tr = check[tid]["Translation"]
        if tr != ru:
            bad.append(tid)
        elif tid != "141954478311" and not re.search(r"[\u0400-\u04FF]", tr):
            bad.append(tid)
    if bad:
        raise SystemExit(f"Verify failed for {bad}")
    print("OK: all target Translations set with Cyrillic (except verified equals).")
    print("Sample Samuel GreetingAndOffer:", TRANSLATIONS["592681872481"])


if __name__ == "__main__":
    main()
