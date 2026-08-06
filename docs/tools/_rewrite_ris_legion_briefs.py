# -*- coding: utf-8 -*-
"""Rewrite RIS Legion tier briefs from loadout unlock map; remint loc IDs off AME collisions.

Canon unlocks (line troops only): scripts/legion-loadouts + weapons.csv tier_label.
Do not claim PPSh at tier 11 (unlocks at 13).
"""
from __future__ import annotations

import csv
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAG = "JAZZ-UI-RIS-001"

# New IDs in free RIS band (title, body) — avoids AME 6960/61/63/64/66/67/70/72 collisions.
BRIEFS = {
    "11": {
        "title_id": "890000000011300",
        "body_id": "890000000011301",
        "title_en": "Old warehouse stock on Legion patrols",
        "title_ru": "У патрулей Легиона — оружие со старых складов",
        "body_en": (
            "Fresh reports from Legion road patrols point to old warehouse stock. "
            "Mosin and MAS-36 rifles are turning up beside MAT-49s, MP40s, Winchester carbines "
            "and double-barrel shotguns. DP-27s and MAC 24/29s make up the heavier end of "
            "the same shipments. The deliveries remain a mixed collection of old designs.\n\n"
            "None of it is sophisticated, but there are plenty of rifles and plenty of recruits "
            "to carry them. Treat every roadblock as dangerous, even when the weapons look older "
            "than the men holding them.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "По свежим донесениям, дорожные патрули Легиона вооружены тем, что удалось выгрести "
            "со старых складов. Винтовки Мосина и MAS-36 соседствуют с MAT-49, MP40, карабинами "
            "Winchester и двустволками. Из более тяжёлого оружия в тех же партиях идут ДП-27 "
            "и MAC 24/29. Поставки по-прежнему представляют собой сборную солянку из старых образцов.\n\n"
            "Ничего современного, зато винтовок и рекрутов хватает. Считайте опасным каждый "
            "блокпост, даже если оружие выглядит старше бойцов, которые его держат.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "12": {
        "title_id": "890000000011302",
        "body_id": "890000000011303",
        "title_en": "Better weapons are reaching the patrols",
        "title_ru": "До патрулей дошло оружие получше",
        "body_en": (
            "Recent crates contain fewer castoffs and more serviceable wartime weapons. "
            "Grease Guns and Sterlings are appearing alongside M1 Garands, M2 carbines, "
            "StG 44s and Model 1897 shotguns. Sidearms now include Lugers, TT-33s and better revolvers.\n\n"
            "The improvement is modest but visible. Guards around roads and depots now receive usable "
            "weapons in regular batches instead of taking whatever happens to be left in a box.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "В последних ящиках меньше откровенного хлама и больше исправного оружия военных лет. "
            "К Grease Gun и Sterling добавились M1 Garand, карабины M2, StG 44 и дробовики Model 1897. "
            "Из личного оружия всё чаще встречаются Luger, ТТ-33 и приличные револьверы.\n\n"
            "Перемены пока невелики, но уже заметны. Охрана дорог и складов теперь получает исправное "
            "оружие партиями, а не берёт первое, что осталось на дне ящика.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "13": {
        "title_id": "890000000011304",
        "body_id": "890000000011305",
        "title_en": "The Major has cleaned out the old armories",
        "title_ru": "Майор выгреб старые арсеналы",
        "body_en": (
            "The Major's buyers have gone deeper into the old armories. Patrols now carry PPShs, "
            "PPS-43s, Thompsons and MPLs, with the occasional Scorpion mixed in. FG 42s, G43s and "
            "SVT-40s are reaching riflemen; Auto-5 shotguns and MG 42s are appearing with support teams. "
            "Makarovs, Colt 1911s and P38s are replacing the worst of the old sidearms.\n\n"
            "The designs are old, but most were built for war and still deserve respect.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "Закупщики Майора добрались до дальних рядов старых арсеналов. У патрулей появились "
            "ППШ, ППС-43, Thompson и MPL, изредка попадается Scorpion. Стрелкам достаются FG 42, "
            "G43 и СВТ-40; группы поддержки получают Auto-5 и MG 42. Худшие старые пистолеты "
            "заменяют на пистолеты Макарова, Colt 1911 и P38.\n\n"
            "Образцы немолодые, но большинство создавали для войны. Недооценивать их не стоит.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "21": {
        "title_id": "890000000011306",
        "body_id": "890000000011307",
        "title_en": "New imports are changing the roadblocks",
        "title_ru": "Новые поставки меняют блокпосты",
        "body_en": (
            "Newer compact weapons are appearing at Legion roadblocks: UZIs, MAC-10s, Micro UZIs "
            "and Agrams, backed by Hi-Power pistols. Riflemen are also receiving M16A1s, Type 56s "
            "and Mini-14 carbines.\n\n"
            "Several field reports place improvised pipe bombs with Roughneck teams, though the "
            "sightings are not yet consistent. Do not assume every patrol carries explosives, "
            "but check bags and webbing before crowding a doorway.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "На блокпостах Легиона появилось более новое компактное оружие: UZI, MAC-10, Micro UZI "
            "и Agram, а также пистолеты Hi-Power. Стрелкам выдают M16A1, Type 56 и карабины Mini-14.\n\n"
            "В нескольких донесениях у групп головорезов отмечены самодельные бомбы, но пока это "
            "не стало правилом. Не ждите взрывчатки у каждого патруля, однако перед штурмом тесного "
            "помещения присмотритесь к сумкам и разгрузкам.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "22": {
        "title_id": "890000000011308",
        "body_id": "890000000011309",
        "title_en": "Carbines and marksman rifles in the crates",
        "title_ru": "В ящиках — карабины и винтовки для метких стрелков",
        "body_en": (
            "Crates intercepted along the main roads contain CAR-15 carbines, FAMAS and Zastava M70 "
            "rifles, plus M14s and Remington 870 shotguns. FR F2s and Zastava M76s are being passed "
            "to the better shots.\n\n"
            "This is procurement with a plan: short weapons for assaults, full-power rifles for the "
            "line, and dedicated rifles for men watching the approaches. The Legion is preparing "
            "for more than roadside extortion.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "В перехваченных на главных дорогах ящиках лежат карабины CAR-15, винтовки FAMAS и "
            "Zastava M70, а также M14 и дробовики Remington 870. Лучшим стрелкам передают FR F2 "
            "и Zastava M76.\n\n"
            "Закупки явно идут по плану: короткое оружие для штурма, мощные винтовки для основной "
            "линии и точные винтовки для тех, кто следит за подступами. Легион готовится не только "
            "собирать дань на дорогах.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "23": {
        "title_id": "890000000011310",
        "body_id": "890000000011311",
        "title_en": "Kalashnikovs are becoming the Legion's standard",
        "title_ru": "Калашниковы становятся штатным оружием",
        "body_en": (
            "AK-47s and AKMs are arriving in volume, with M16A2s also appearing among the riflemen. "
            "AKS-74Us are going to troops that need shorter weapons, while Bizons and Spectres are "
            "showing up with close-assault teams. FN FALs and Striker shotguns fill out the line.\n\n"
            "Support gunners now have RPKs and M60s, and selected marksmen are carrying M21 rifles. "
            "The Legion is starting to look like a force with its own armory rather than a militia "
            "borrowing weapons for the day.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "АК-47 и АКМ поступают крупными партиями, у стрелков также замечены M16A2. АКС-74У "
            "достаются тем, кому нужно оружие покороче, а «Бизоны» и Spectre появляются у штурмовых "
            "групп. Основную линию дополняют FN FAL и дробовики Striker.\n\n"
            "Пулемётчики получают РПК и M60, отдельным метким стрелкам выдают винтовки M21. Легион "
            "всё больше похож на силу с собственным арсеналом, а не на ополчение, которое одалживает "
            "оружие на один день.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "24": {
        "title_id": "890000000011312",
        "body_id": "890000000011313",
        "title_en": "Modern weapons have reached fortified positions",
        "title_ru": "Современное оружие дошло до укреплённых позиций",
        "body_en": (
            "Fortified Legion positions now show MP5A2s, MP5Ks and TMPs, while riflemen carry M4A1s, "
            "HK33s, AK-74s and Galils. SPAS-12 shotguns are appearing indoors; Dragunovs and M700s "
            "cover longer approaches. RPK-74 and M60E3 machine guns provide support, with USPs and "
            "Kimbers among the sidearms.\n\n"
            "The mix points to deliberate preparation for both close assaults and defended ground.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "На укреплённых позициях Легиона замечены MP5A2, MP5K и TMP, а стрелки получают M4A1, "
            "HK33, АК-74 и Galil. В помещениях всё чаще встречаются SPAS-12; дальние подступы прикрывают "
            "стрелки с Dragunov и M700. Поддержку обеспечивают РПК-74 и M60E3, среди пистолетов появились "
            "USP и Kimber.\n\n"
            "Такой набор явно подбирали и для штурма в тесноте, и для обороны подготовленных позиций.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "25": {
        "title_id": "890000000011314",
        "body_id": "890000000011315",
        "title_en": "Front-line squads are receiving modern weapons",
        "title_ru": "Передовые отряды получают современное оружие",
        "body_en": (
            "Front-line Legion squads are turning up with G36s and G36cs, AUGs, VSS carbines and G3 rifles. "
            "Their support weapons now include Minimis, MAGs and PKMs, and modern pistols are common "
            "enough to be more than personal trophies.\n\n"
            "These squads are being armed as units, not from whatever happens to be at hand. Plan for "
            "weapons chosen for specific jobs rather than a random assortment from one crate.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "У передовых отрядов Легиона замечены G36 и G36c, AUG, карабины ВСС и винтовки G3. "
            "В качестве оружия поддержки они получают Minimi, MAG и ПКМ, а современные пистолеты "
            "встречаются уже слишком часто, чтобы считать их личными трофеями.\n\n"
            "Такие отряды вооружают как единое целое, а не чем придётся. Ждите оружие, подобранное "
            "под конкретные задачи, а не случайный набор из одного ящика.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "31": {
        "title_id": "890000000011316",
        "body_id": "890000000011317",
        "title_en": "Professional-grade rifles are in circulation",
        "title_ru": "В обороте оружие профессионального уровня",
        "body_en": (
            "Sig 550 and Sig 552 rifles are now in Legion service, along with suppressed MP5SDs and "
            "M60E4 machine guns. M1A rifles are being used for deliberate fire at longer ranges, "
            "and the sidearms carried by these units have improved as well.\n\n"
            "Whatever the quality of the troops, this armament makes them dangerous. "
            "Identify the rifles and machine guns before committing to an approach.\n\n"
            "— R.I.S. Field Desk"
        ),
        "body_ru": (
            "На вооружении Легиона появились винтовки Sig 550 и Sig 552, малошумные MP5SD и пулемёты "
            "M60E4. Винтовки M1A используют для прицельного огня на дальних дистанциях; личное оружие "
            "у этих подразделений тоже стало лучше.\n\n"
            "Как бы ни были подготовлены бойцы, такое вооружение делает их опасными. "
            "Перед сближением определите, где винтовки и пулемёты.\n\n"
            "— Полевой отдел R.I.S."
        ),
    },
    "32": {
        "title_id": "890000000011318",
        "body_id": "890000000011319",
        "title_en": "Special-purpose weapons confirmed",
        "title_ru": "Подтверждены специальные образцы",
        "body_en": (
            "Special-purpose weapons are now confirmed in Legion hands: customized Sig rifles, MP7s and "
            "P90s, SVU and Arctic Warfare precision rifles, and USAS-12 shotguns. Reports also place "
            "HK21s and HK23s in the same flow of weapons.\n\nThe mix suggests the Legion may be grouping "
            "marksmen, assault troops and gunners around particular tasks. That is still only an "
            "assessment: identify the weapons before assuming how the squad will fight.\n\n— R.I.S. Field "
            "Desk"
        ),
        "body_ru": (
            "У Легиона подтверждены специальные образцы: доработанные винтовки Sig, MP7 и P90, точные СВУ "
            "и Arctic Warfare, а также дробовики USAS-12. В тех же поставках отмечены HK21 и HK23.\n\nТакой "
            "набор позволяет предположить, что Легион может собирать метких стрелков, штурмовиков и "
            "пулемётчиков под конкретные задачи. Пока это лишь предположение: сначала определите оружие и "
            "только потом решайте, как будет действовать отряд.\n\n— Полевой отдел R.I.S."
        ),
    },
    "33": {
        "title_id": "890000000011320",
        "body_id": "890000000011321",
        "title_en": "Barrett, PSG-1, AS Val and AA-12 confirmed",
        "title_ru": "Подтверждены Barrett, PSG-1, АС «Вал» и AA-12",
        "body_en": (
            "Barrett anti-materiel rifles, PSG-1 precision rifles, AS Val carbines and AA-12 shotguns are "
            "now confirmed in Legion stocks.\n\nAny Legion line squad carrying one of these weapons can "
            "change the fight immediately. Identify the weapon, work out what it can reach, and change "
            "the plan before it opens fire.\n\n— R.I.S. Field Desk"
        ),
        "body_ru": (
            "Подтверждено наличие у Легиона противоматериальных винтовок Barrett, точных PSG-1, карабинов "
            "АС «Вал» и дробовиков AA-12.\n\nЛюбой линейный отряд Легиона с одним из этих образцов может "
            "сразу изменить ход боя. Определите оружие, оцените его дальность и измените план до первого "
            "выстрела.\n\n— Полевой отдел R.I.S."
        ),
    },
}

# Old brief-only IDs to drop from CSV (do NOT touch AME-owned collisions).
ORPHAN_BRIEF_IDS = {
    "890000000006940",
    "890000000006942",
    "890000000006943",
    "890000000006945",
    "890000000006946",
    "890000000006948",
    "890000000006949",
    "890000000006951",
    "890000000006952",
    "890000000006954",
    "890000000006955",
    "890000000006957",
    "890000000006958",
    "890000000006969",
}


def lua_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def load_csv(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    prefix = ""
    if text.startswith("sep="):
        first_nl = text.find("\n")
        prefix = text[: first_nl + 1]
        body = text[first_nl + 1 :]
    else:
        body = text
    rows = list(csv.reader(io.StringIO(body)))
    return prefix, rows


def write_csv(path: Path, prefix: str, rows):
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    for row in rows:
        w.writerow(row)
    path.write_text(prefix + out.getvalue(), encoding="utf-8-sig")


def upsert_rows(rows, rid: str, en: str, ru: str):
    for i, row in enumerate(rows):
        if row and row[0] == rid:
            rows[i] = [rid, en, ru, "", TAG]  # Russian.csv shape: EN, RU
            return
    rows.append([rid, en, ru, "", TAG])


def upsert_rows_en_file(rows, rid: str, en: str, ru: str):
    for i, row in enumerate(rows):
        if row and row[0] == rid:
            rows[i] = [rid, ru, en, "", TAG]  # English.csv shape: RU, EN
            return
    rows.append([rid, ru, en, "", TAG])


def patch_csvs():
    ru_prefix, ru_rows = load_csv(ROOT / "Russian.csv")
    en_prefix, en_rows = load_csv(ROOT / "English.csv")
    # drop orphans
    ru_rows = [r for r in ru_rows if not (r and r[0] in ORPHAN_BRIEF_IDS)]
    en_rows = [r for r in en_rows if not (r and r[0] in ORPHAN_BRIEF_IDS)]
    for b in BRIEFS.values():
        upsert_rows(ru_rows, b["title_id"], b["title_en"], b["title_ru"])
        upsert_rows(ru_rows, b["body_id"], b["body_en"], b["body_ru"])
        upsert_rows_en_file(en_rows, b["title_id"], b["title_en"], b["title_ru"])
        upsert_rows_en_file(en_rows, b["body_id"], b["body_en"], b["body_ru"])
    write_csv(ROOT / "Russian.csv", ru_prefix, ru_rows)
    write_csv(ROOT / "English.csv", en_prefix, en_rows)
    print("CSV upserted", len(BRIEFS) * 2, "strings; orphans removed", len(ORPHAN_BRIEF_IDS))


def patch_items():
    path = ROOT / "items.lua"
    text = path.read_text(encoding="utf-8")
    for tier, b in BRIEFS.items():
        eid = f"RIS_LegionBrief_{tier}"
        # body
        body_pat = re.compile(
            rf'body = T\(\d+, --\[\[ModItemEmail {re.escape(eid)} body\]\] ".*?"\),',
            re.S,
        )
        body_repl = (
            f'body = T({b["body_id"]}, --[[ModItemEmail {eid} body]] '
            f'"{lua_escape(b["body_en"])}"),'
        )
        text, n = body_pat.subn(lambda _m, r=body_repl: r, text, count=1)
        if n != 1:
            raise SystemExit(f"{eid} body replace n={n}")
        # title
        title_pat = re.compile(
            rf'title = T\(\d+, --\[\[ModItemEmail {re.escape(eid)} title\]\] ".*?"\),',
            re.S,
        )
        title_repl = (
            f'title = T({b["title_id"]}, --[[ModItemEmail {eid} title]] '
            f'"{lua_escape(b["title_en"])}"),'
        )
        text, n = title_pat.subn(lambda _m, r=title_repl: r, text, count=1)
        if n != 1:
            raise SystemExit(f"{eid} title replace n={n}")
    path.write_text(text, encoding="utf-8")
    print("items.lua briefs reminted")


def main():
    patch_csvs()
    patch_items()


if __name__ == "__main__":
    main()
