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
        "title_en": "Warehouse scrap: Mosin, MAT-49, double-barrels",
        "title_ru": "Складской хлам: Мосин, MAT-49, двустволки",
        "body_en": (
            "R.I.S. field note — Legion supply\n\n"
            "The Major is still emptying old warehouses. Day-one patrols carry wartime leftovers: "
            "Mosin and MAS-36 bolt guns, MAT-49 and MP40 subguns, Winchester lever carbines, "
            "double-barrel shotguns, tired service pistols. Machine-gun nests are DP-27 / MAC 24/29 era. "
            "Ammo is thin; armor is mostly wishful thinking.\n\n"
            "Early Legion patrols are poorly equipped — but there are a lot of them. "
            "Do not mistake rust for safety.\n\n"
            "— Recon Intelligence Services"
        ),
        "body_ru": (
            "Полевая заметка R.I.S. — снабжение Легиона\n\n"
            "Майор по-прежнему вычищает старые склады. У патрулей на старте — военный хлам: "
            "Мосин и MAS-36, MAT-49 и MP40, рычажные Winchester, двустволки, уставшие служебные пистолеты. "
            "Пулемётные гнёзда — эпохи ДП-27 / MAC 24/29. "
            "Патронов мало; броня — в основном фантазия.\n\n"
            "Ранние патрули Легиона слабо экипированы — но их много. "
            "Не путайте ржавчину с безопасностью.\n\n"
            "— Recon Intelligence Services"
        ),
    },
    "12": {
        "title_id": "890000000011302",
        "body_id": "890000000011303",
        "title_en": "Grease Guns, Sterlings, Garands in the mix",
        "title_ru": "В обороте Grease Gun, Sterling, Garand",
        "body_en": (
            "R.I.S. field note — Legion supply\n\n"
            "Shipments look a little less desperate. Grease Guns and Sterlings are mixing with "
            "M1 Garands, M2 carbines, StG 44s, Model 1897 shotguns — still wartime generation, "
            "but less scrap-metal roulette. Sidearms improve: Lugers, TT-33s, better revolvers.\n\n"
            "— Recon Intelligence Services"
        ),
        "body_ru": (
            "Полевая заметка R.I.S. — снабжение Легиона\n\n"
            "Поставки чуть менее отчаянные. Grease Gun и Sterling смешиваются с "
            "M1 Garand, карабинами M2, StG 44, дробовиками Model 1897 — всё ещё военное поколение, "
            "но меньше рулетки из металлолома. Боковики лучше: Люгеры, ТТ-33, приличные револьверы.\n\n"
            "— Recon Intelligence Services"
        ),
    },
    "13": {
        "title_id": "890000000011304",
        "body_id": "890000000011305",
        "title_en": "Early kit peaks: PPSh, Thompson, 1911s",
        "title_ru": "Пик раннего кита: ППШ, Thompson, 1911",
        "body_en": (
            "R.I.S. field note — Legion supply\n\n"
            "First-wave issue is peaking: PPSh and PPS-43, Thompsons, MPL, the odd Scorpion; "
            "FG 42 / G43 / SVT-40 battle rifles; Auto-5 shotguns; MG 42 belts. "
            "Service pistols that actually fire — Makarov, Colt 1911, P38. "
            "Still generation-one gear, but the Major has stopped issuing pure museum pieces as standard.\n\n"
            "— Recon Intelligence Services"
        ),
        "body_ru": (
            "Полевая заметка R.I.S. — снабжение Легиона\n\n"
            "Первая волна выдачи на пике: ППШ и ППС-43, Thompson, MPL, редкий Scorpion; "
            "боевые FG 42 / G43 / СВТ-40; Auto-5; ленты MG 42. "
            "Служебные пистолеты, которые реально стреляют — Макаров, Colt 1911, P38. "
            "Всё ещё первое поколение, но Майор перестал раздавать чистый музей как норму.\n\n"
            "— Recon Intelligence Services"
        ),
    },
    "21": {
        "title_id": "890000000011306",
        "body_id": "890000000011307",
        "title_en": "Second wave: UZI, MAC-10, pipe bombs",
        "title_ru": "Вторая волна: UZI, MAC-10, самодельные бомбы",
        "body_en": (
            "R.I.S. field note — Legion supply\n\n"
            "Second wave. Compact SMGs — UZI, MAC-10, Micro UZI, Agram — and Hi-Power pistols "
            "are showing up beside early M16A1 / Type 56 rifles and Mini-14 carbines. "
            "Roughnecks have started carrying pipe bombs. This is no longer a scavenger parade.\n\n"
            "— Recon Intelligence Services"
        ),
        "body_ru": (
            "Полевая заметка R.I.S. — снабжение Легиона\n\n"
            "Вторая волна. Компактные ПП — UZI, MAC-10, Micro UZI, Agram — и пистолеты Hi-Power "
            "рядом с ранними M16A1 / Type 56 и карабинами Mini-14. "
            "У головорезов появились самодельные бомбы. Это уже не парад мародёров.\n\n"
            "— Recon Intelligence Services"
        ),
    },
    "22": {
        "title_id": "890000000011308",
        "body_id": "890000000011309",
        "title_en": "CAR-15, FAMAS, M14-pattern rifles arriving",
        "title_ru": "Идут CAR-15, FAMAS, винтовки M14",
        "body_en": (
            "R.I.S. field note — Legion supply\n\n"
            "Carbines and battle rifles in the crates: CAR-15, FAMAS, Zastava M70, M14 SAW patterns, "
            "Remington 870s. Marksmen pick up FR F2 / Zastava M76. "
            "Someone is buying for a real fight, not a roadblock shakedown.\n\n"
            "— Recon Intelligence Services"
        ),
        "body_ru": (
            "Полевая заметка R.I.S. — снабжение Легиона\n\n"
            "В ящиках — карабины и боевые винтовки: CAR-15, FAMAS, Zastava M70, схемы M14 SAW, "
            "Remington 870. У стрелков — FR F2 / Zastava M76. "
            "Кто-то закупается под настоящий бой, а не под тряску на блокпосте.\n\n"
            "— Recon Intelligence Services"
        ),
    },
    "23": {
        "title_id": "890000000011310",
        "body_id": "890000000011311",
        "title_en": "AKs in volume — Legion looks like an army",
        "title_ru": "АК оптом — Легион уже похож на армию",
        "body_en": (
            "R.I.S. field note — Legion supply\n\n"
            "Kalashnikovs in volume: AK-47, AKM, AKS-74U, the occasional Bizon or Spectre. "
            "FN FAL battle rifles, Striker shotguns, M21 / RPK / M60 support. "
            "The Legion is finally looking like an army that owns rifles, not a militia that borrows them.\n\n"
            "— Recon Intelligence Services"
        ),
        "body_ru": (
            "Полевая заметка R.I.S. — снабжение Легиона\n\n"
            "Калашниковы оптом: АК-47, АКМ, АКС-74У, редкий «Бизон» или Spectre. "
            "Боевые FN FAL, дробовики Striker, поддержка M21 / РПК / M60. "
            "Легион наконец похож на армию, у которой есть свои винтовки, а не на ополчение, которое их одалживает.\n\n"
            "— Recon Intelligence Services"
        ),
    },
    "24": {
        "title_id": "890000000011312",
        "body_id": "890000000011313",
        "title_en": "MP5 family and M4A1 in Legion hands",
        "title_ru": "В руках Легиона MP5 и M4A1",
        "body_en": (
            "R.I.S. field note — Legion supply\n\n"
            "Western SMGs and carbines: MP5A2 / MP5K, TMP, M4A1, HK33, AK-74, Galil. "
            "SPAS-12, Dragunov / M700 glass, RPK-74 and M60E3 belts. Serious sidearms — USP, Kimber. "
            "Expect tighter fire and fewer jams when you push a fortified position.\n\n"
            "— Recon Intelligence Services"
        ),
        "body_ru": (
            "Полевая заметка R.I.S. — снабжение Легиона\n\n"
            "Западные ПП и карабины: MP5A2 / MP5K, TMP, M4A1, HK33, АК-74, Galil. "
            "SPAS-12, оптика Dragunov / M700, ленты РПК-74 и M60E3. Серьёзные боковики — USP, Kimber. "
            "Ждите более плотный огонь и меньше клинов, когда прёте на укреплённую позицию.\n\n"
            "— Recon Intelligence Services"
        ),
    },
    "25": {
        "title_id": "890000000011314",
        "body_id": "890000000011315",
        "title_en": "G36c, VSS — late second-wave spike",
        "title_ru": "G36c, ВСС — поздний скачок второй волны",
        "body_en": (
            "R.I.S. field note — Legion supply\n\n"
            "Late second-wave spike: G36 / G36c, AUG, VSS, G3 battle rifles, Minimi / MAG / PKM support, "
            "modern pistols. Quality jumped again — veteran squads are properly armed, not upgraded scavengers.\n\n"
            "— Recon Intelligence Services"
        ),
        "body_ru": (
            "Полевая заметка R.I.S. — снабжение Легиона\n\n"
            "Поздний скачок второй волны: G36 / G36c, AUG, ВСС, боевые G3, поддержка Minimi / MAG / ПКМ, "
            "современные пистолеты. Качество снова выросло — ветеранов стоит считать нормально вооружёнными, "
            "а не «чуть лучшими мародёрами».\n\n"
            "— Recon Intelligence Services"
        ),
    },
    "31": {
        "title_id": "890000000011316",
        "body_id": "890000000011317",
        "title_en": "Third wave: Sig 550, M60E4, real optics",
        "title_ru": "Третья волна: Sig 550, M60E4, настоящая оптика",
        "body_en": (
            "R.I.S. field note — Legion supply\n\n"
            "Third wave. Sig 550 / 552 rifles, MP5SD, M60E4 machine guns, M1A glass, better sidearms. "
            "The Major is issuing kit meant to hold ground against professionals.\n\n"
            "— Recon Intelligence Services"
        ),
        "body_ru": (
            "Полевая заметка R.I.S. — снабжение Легиона\n\n"
            "Третья волна. Винтовки Sig 550 / 552, MP5SD, пулемёты M60E4, оптика M1A, лучше боковики. "
            "Майор выдаёт кит, рассчитанный держать землю против профессионалов.\n\n"
            "— Recon Intelligence Services"
        ),
    },
    "32": {
        "title_id": "890000000011318",
        "body_id": "890000000011319",
        "title_en": "Custom Sigs, SVU, Arctic Warfare",
        "title_ru": "Кастомные Sig, СВУ, Arctic Warfare",
        "body_en": (
            "R.I.S. field note — Legion supply\n\n"
            "Precision and special weapons: custom Sigs, MP7 / P90, SVU, Arctic Warfare rifles, "
            "USAS-12, HK21 / HK23 belts. Marksmen and assault elements are no longer an afterthought.\n\n"
            "— Recon Intelligence Services"
        ),
        "body_ru": (
            "Полевая заметка R.I.S. — снабжение Легиона\n\n"
            "Точность и спецстволы: кастомные Sig, MP7 / P90, СВУ, Arctic Warfare, "
            "USAS-12, ленты HK21 / HK23. Снайперы и штурм уже не «на потом».\n\n"
            "— Recon Intelligence Services"
        ),
    },
    "33": {
        "title_id": "890000000011320",
        "body_id": "890000000011321",
        "title_en": "Barrett, PSG-1, AA-12 — top-shelf threats",
        "title_ru": "Barrett, PSG-1, AA-12 — угрозы высшего полка",
        "body_en": (
            "R.I.S. field note — Legion supply\n\n"
            "Top shelf. Barrett anti-materiel rifles, PSG-1 precision guns, AS Val carbines, AA-12 shotguns. "
            "If you see this kit in the field, assume the Major wants someone dead — permanently.\n\n"
            "— Recon Intelligence Services"
        ),
        "body_ru": (
            "Полевая заметка R.I.S. — снабжение Легиона\n\n"
            "Высшая полка. Противоматериальные Barrett, точные PSG-1, карабины АС «Вал», дробовики AA-12. "
            "Если такое в поле — считайте, Майор хочет кого-то мёртвым. Насовсем.\n\n"
            "— Recon Intelligence Services"
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
