#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build sector atlas / transfer / sheet-vs-runtime docs from:
  - docs/technical/maps/data/sectors-runtime.json (from export-jazz-maps-sectors.py)
  - embedded Google Sheet «Карта» snapshot (gid 863693534, captured 2026-08-01)

Usage (from jazz/):
  python docs/tools/export-jazz-maps-sectors.py
  python docs/tools/build-sector-atlas-docs.py

Writes under docs/technical/maps/ (+ data/*.csv).
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

LETTERS = "ABCDEFGHIJKLMNOP"
COLS = range(1, 33)

# --- Google Sheet «Карта» new-grid notes (rows A–P × 1–32) ---
# Empty string = blank cell in sheet. Sea/filler kept as sheet text.
SHEET_NEW: dict[str, str] = {
    # A
    "A1": "Саванна (Берег)",
    "A2": "Саванна (Берег)",
    "A3": "Саванна (Берег)",
    "A4": "Даймонд-Рэд",
    "A9": "А9 тоже горы и тоже без деталей",
    "A12": "А12 Горы (Пока без деталей)",
    "A13": "А13 Военный аванпост - Горный",
    "A15": "А15 Лагерь на холме (Тут пенитрируют Бифа)",
    "A24": "А24 Горная дорога (Конь не валялся)",
    "A25": "A25 Шахта Драхенберг",
    "A26": "А26 Лансбах Порт",
    "A27": "Река (Обрыв Запад)",
    # B
    "B1": "Море",
    "B2": "Море",
    "B3": "Море",
    "B4": "Саванна (Берег)",
    "B5": "Саванна (Берег)",
    "B6": "B6 Запланирован аванпост",
    "B7": "B7 Пещера в Саванне",
    "B11": "B11 Горы (Бездетальные)",
    "B15": "B15 Ферма Нигде",
    "B17": "B17 Санаторий",
    "B24": "B24 Горная дорога (Конь не валялся)",
    "B25": "Река",
    "B26": "Река",
    "B28": "B28 Орлиное гнездо",
    # C
    "C1": "Море",
    "C2": "Море",
    "C3": "Чаячий остров",
    "C4": "Острова, маленькие",
    "C6": "Саванна (Берег)",
    "C7": "С7 Саванна (Нужно уточнение!!!!)",
    "C8": "С8 Саванна (Нужно уточнение!!!!!!)",
    "C12": "С12 Пит-Стоп",
    "C13": "С13 Горы",
    "C14": "С14 Старая бензоколонка",
    "C15": "Филер, или нет, пока маленькое нихуя",
    "C22": "С22 Пустоши",
    "C23": "С23 Пустоши",
    "C24": "С24 Перекресток дохлых зверей",
    "C25": "С25 Пустоши",
    "C26": "Река",
    "C27": "Вершина скалы (лифт; в sheet помечено как C26)",
    # D
    "D1": "Море",
    "D2": "Море",
    "D6": "Море",
    "D7": "Саванна (Берег)",
    "D9": "D9 Лагерь Браконьеров",
    "D15": "D15 Шахта Фосс-Нуар",
    "D22": "D22 Разлом (Аванпост)",
    "D23": "D23 Оазис",
    "D25": "Река",
    "D26": "D26 каменные ступени",
    "D27": "D27 Штурмвассерский каньон",
    "D29": "D29 Остров ШтурмВассер",
    # E
    "E1": "Море",
    "E2": "Море",
    "E4": "E4 Чаячий остров",
    "E6": "Море",
    "E7": "Море",
    "E8": "E8 Кладбище брокеннхилл",
    "E9": "E9 Саванна (Нужно уточнение)",
    "E10": "E10 Аванпост Кам-саван",
    "E11": "E11 Саванна (Устроить пожар)",
    "E12": "E12 Саванна (Заложница по квесту из лагеря беженцев)",
    "E13": "Саванна переходная в зеленку",
    "E14": "Е14 Окраины Понтагрюэля",
    "E15": "Е15 Трущебы Понтагрюэля",
    "E16": "Е16 Центр Понтагрюэля",
    "E25": "Река",
    "E26": "E26 Берег реки в джунглях",
    # F
    "F1": "Море",
    "F2": "Море",
    "F3": "Море",
    "F4": "Море",
    "F5": "Море",
    "F6": "Море",
    "F7": "Море",
    "F8": "F8 Побережье саванны",
    "F9": "F9 Саванна (Рюкзаки, следы присутствия MERC)",
    "F10": "F10 Саванна (Устроить пожар)",
    "F11": "F11 Саванна (Устроить пожар)",
    "F12": "F12 Саванна",
    "F13": "F13 Лагерь Беженцев",
    "F17": "F17 Берег реки в джунглях",
    "F19": "F19 Берег в джунглях",
    "F20": "F20 Укрытие Гиен (Нужно уточнение)",
    "F21": "F21 Укрытие Гиен",
    "F22": "F22 Проклятый лес (Хижина ведьмы)",
    "F23": "F23 Кам-Гран-При (Аванпост)",
    "F24": "F24 В планах ещё бензоколонка",
    "F25": "F25 Берег реки в джунглях (водный путь)",
    "F26": "Река",
    "F28": "F28 Иль-Мора",
    # G
    "G1": "Море",
    "G2": "Море",
    "G3": "Море",
    "G4": "Море",
    "G5": "Море",
    "G6": "Море",
    "G7": "Море",
    "G8": "Море",
    "G9": "G9 Код д азур (Порт)",
    "G10": "G10 Поселение Ла-Палисад",
    "G11": "G11 Саванна (Два трупа из квеста охота на охотника)",
    "G13": "G13 Колодец",
    "G15": "G15 Берег реки в джунглях",
    "G16": "G16 Минное поле",
    "G17": "G17 Великий лес (Вудуисты)",
    "G18": "G18 Берег реки в джунглях",
    "G22": "G22 Кам-Съен_Саваж (Аванпост с гиенами)",
    "G23": "G23 Проклятый лес",
    "G25": "G25",
    "G26": "Река",
    "G27": "G27 Шале-Де-ла-Пе (Деревня вудуистов)",
    "G28": "G28 Филер (Пока пусто)",
    "G30": "G30 Эль-Мора",
    "G31": "G31 Болота",
    # H
    "H1": "Море",
    "H2": "Море",
    "H3": "Море",
    "H4": "Море",
    "H5": "Море",
    "H6": "Море",
    "H7": "Море",
    "H8": "Море",
    "H9": "Море",
    "H10": "Саванна (Берег)",
    "H14": "H14 Шахта Мфуму",
    "H15": "H15 начало зеленки (Джунглей) (переделать в мелкое поселение)",
    "H17": "Н17 Захоронения",
    "H18": "Н18 Флитаун рынок",
    "H19": "H19 Флитаун (Порт)",
    "H21": "Н21 Берег Реки",
    "H22": "Н22 Старые укрепления с бункером",
    "H23": "H23 Пещера с фашней / опер штаб наземный",
    "H24": "H24 Берег реки в джунглях",
    "H25": "Н25 река",
    "H26": "Река",
    "H27": "Н27 ТЗ Болота, нет локации",
    "H31": "H31 Вассерграб (Шахта)",
    "H32": "H32 Вассерграб (Мрачная деревня)",
    # I
    "I1": "Море",
    "I2": "I2 Жилье доктора, Бывшие военные укрепления",
    "I3": "I3 Мост в нижней части карты (Дорога) над рекой",
    "I4": "I4 Филер (Дорога Эрни-Мост) над обрывом",
    "I5": "I5 Деревня Эрни (Берег)",
    "I6": "I6 Жестянка",
    "I7": "I7 Форт Ло-Блё",
    "I8": "Море",
    "I9": "Море",
    "I10": "Море",
    "I11": "Саванна (Берег)",
    "I16": "I16 Заброшенный особняк (призрак)",
    "I22": "I22 Дом на холме, секретный вход в метро",
    "I23": "I23 Великий лес",
    "I24": "Река",
    "I25": "I25 Грязноводный мост (Город)",
    "I31": "I31 Хижина ведьмы",
    # J
    "J1": "Море",
    "J2": "Море",
    "J3": "Море",
    "J4": "J4 Дорога из J5 в I4",
    "J5": "J5 Деревня эрни без берега (Фермы)",
    "J6": "J6 Дорога контрабандистов",
    "J7": "J7 Изумрудный берег",
    "J8": "Море",
    "J9": "Море",
    "J10": "Море",
    "J11": "Море",
    "J12": "J12 Саванна (Берег-Порт) (Укреп район)",
    "J13": "J13 Деревня с золотодобычей, дома на сваях",
    "J14": "J14 Римвиль (Особняк бандосов)",
    "J15": "J15 Берег реки",
    "J16": "Зеленка",
    "J17": "Зеленка (Маленькая река)",
    "J18": "Зеленка",
    "J19": "Зеленка (Берег реки на углу)",
    "J23": "J23 Старое кладбище",
    "J24": "Река",
    "J25": "Река",
    "J28": "J28 Болота с входом в метро",
    "J29": "J29 Лагерь надежды",
    # K
    "K1": "Море",
    "K2": "Море",
    "K3": "K3 Походный Лагерь Легиона 1",
    "K4": "K4 Флаговый холм",
    "K5": "K5 Походный Лагерь Легиона 5",
    "K6": "K6 Резервный лагерь Контрабандистов",
    "K7": "K7 Заброшенный скалистый берег, сожженная деревня",
    "K8": "Море",
    "K9": "Море",
    "K10": "Море",
    "K11": "Река",
    "K12": "Река",
    "K13": "Река",
    "K14": "Река",
    "K15": "K15 T Река ниже берег джунглей",
    "K19": "K19 Аванпост Развалины фабрики",
    "K20": "Река",
    "K21": "К21 Кам Бьян Шьен",
    "K24": "К24 Берег, пустая лока",
    "K25": "Река уходит вверх",
    "K29": "К29 Санаторий",
    "K32": "К32 Усадьбы близнецы",
    # L
    "L1": "L1 Лагерь повстанцев",
    "L2": "L2 Гора с водопадом и оттоками",
    "L3": "L3 Походный Лагерь Легиона 2",
    "L4": "L4 Походный Лагерь Легиона 3",
    "L5": "L5 Походный Лагерь Легиона 4",
    "L6": "L6 Бункер",
    "L7": "L7 Деревня на берегу, не большая",
    "L8": "Море",
    "L9": "Море",
    "L10": "Море",
    "L11": "L11 Остров с укреплениями",
    "L12": "L12 Река",
    "L13": "L13 Ещё один остров с укреплением",
    "L14": "L14 Река",
    "L15": "L15 Кам-Ла-Барьер",
    "L16": "L16 Великий лес",
    "L17": "L17 Разбойничий форт",
    "L19": "L19 Т речные островки (Локации нет)",
    "L20": "Река",
    "L21": "Река",
    "L22": "Река",
    "L23": "Река",
    "L24": "L24 Река",
    "L25": "Река",
    "L31": "L31 Фермы",
    # M
    "M1": "M1 Зона высадки",
    "M2": "М2 Водопад",
    "M3": "М3 Побережье",
    "M4": "М4 Смотровая площадка",
    "M5": "М5 Заброс, скалы",
    "M6": "М6 Заброс, скалы",
    "M7": "Заглушка",
    "M8": "Море",
    "M9": "Море",
    "M10": "Море",
    "M11": "Река",
    "M12": "Река",
    "M13": "Река",
    "M14": "Река",
    "M15": "Река",
    "M16": "Река",
    "M17": "Река",
    "M18": "Река",
    "M19": "Река",
    "M20": "Река",
    "M21": "Река",
    "M22": "Река",
    "M23": "Река",
    "M24": "M24 Тут должен быть какой-то порт - дамба",
    "M31": "M31 Фермы",
    # N
    "N1": "Море",
    "N2": "Море",
    "N3": "Море",
    "N4": "Море",
    "N5": "Море",
    "N6": "Море",
    "N7": "Море",
    "N8": "Море",
    "N9": "Море",
    "N10": "Море",
    "N11": "N11 укреп смотрящий за входом в реку",
    "N12": "N12 Порт Какао город",
    "N13": "N13 Доки порт Какао",
    "N14": "N14 ТС",
    "N15": "N15 ТС",
    "N16": "N16 (ТС) Упавший самолет (Лаз в разбойничий форт)",
    "N17": "N17 Река",
    "N18": "N18 Река",
    "N19": "N19 Река",
    "N20": "Река",
    "N21": "Река",
    "N22": "N22 Причал",
    "N23": "N23 Старое кладбище",
    "N24": "N24 Фермы",
    "N27": "N27 Фермы",
    "N28": "N28 Фермы",
    "N29": "N29 Фермы",
    "N30": "N30 Фермы",
    "N31": "N31 Фермы",
    # O
    "O1": "Море",
    "O2": "Море",
    "O3": "Море",
    "O4": "Море",
    "O5": "Море",
    "O6": "Море",
    "O7": "Море",
    "O8": "Море",
    "O9": "Море",
    "O10": "О10 Филер",
    "O11": "О11 Великий лес берег (Фермы)",
    "O13": "O13 Свалка",
    "O14": "О14 Филер (Лес)",
    "O16": "О16 Олд-Даймонд",
    "O17": "О17 Филер (Лес)",
    "O18": "O18 Часть моста левая",
    "O21": "О21 Великий лес (Берег)",
    # P
    "P1": "Море",
    "P2": "Море",
    "P3": "Море",
    "P4": "Море",
    "P5": "Море",
    "P6": "Море",
    "P7": "Море",
    "P8": "P8 Хорошее место",
    "P9": "Р9 Берег рядом с тюрьмой",
    "P11": "Р11 Великий лес (Убежище богача из заброшенного особняка)",
    "P15": "Р15 Лес",
    "P16": "Р16 гдегдевезде",
    "P17": "Р17 Камп-де-крокодиль (Аванпост)",
    "P19": "Р19 Заброшенный аэродром",
    "P26": "P26 Военная База - ЮГ",
}

# Transfer rows from sheet «Трансфер локаций» + suite-known extras.
# source: sheet | suite-docs
TRANSFERS: list[dict[str, str]] = [
    {"vanilla_id": "A2", "maps_id": "A4", "name_ru": "Даймонд Рэд", "notes": "", "source": "sheet"},
    {"vanilla_id": "A11", "maps_id": "B15", "name_ru": "Ферма Нигде (Nowhere)", "notes": "", "source": "sheet"},
    {"vanilla_id": "A20", "maps_id": "B28", "name_ru": "Орлиное гнездо", "notes": "Major HQ", "source": "sheet"},
    {"vanilla_id": "B2", "maps_id": "C6", "name_ru": "Порт (рядом с Даймонд Рэд)", "notes": "sheet писал С6 (кириллица С)", "source": "sheet"},
    {"vanilla_id": "B12", "maps_id": "A25", "name_ru": "Шахта Драхенберг", "notes": "sheet: Драхтенберг", "source": "sheet"},
    {"vanilla_id": "B13", "maps_id": "A26", "name_ru": "Ландсбах / Лансбах", "notes": "", "source": "sheet"},
    {"vanilla_id": "B16", "maps_id": "D22", "name_ru": "Разлом (Аванпост)", "notes": "", "source": "sheet"},
    {"vanilla_id": "C5", "maps_id": "D9", "name_ru": "Лагерь Браконьеров", "notes": "", "source": "sheet"},
    {"vanilla_id": "C7", "maps_id": "E15", "name_ru": "Окраина Понтагрюэля (Мастерская)", "notes": "sheet target E15; D7 тоже → E15", "source": "sheet"},
    {"vanilla_id": "D7", "maps_id": "E15", "name_ru": "Понтагрюэль", "notes": "sheet: D7→E15 (трущобы/хаб — уточнять с runtime names)", "source": "sheet"},
    {"vanilla_id": "D8", "maps_id": "E16", "name_ru": "Понтагрюэль Больница", "notes": "", "source": "sheet"},
    {"vanilla_id": "D10", "maps_id": "F23", "name_ru": "Аванпост Гран-При", "notes": "", "source": "sheet"},
    {"vanilla_id": "E9", "maps_id": "F13", "name_ru": "Лагерь Беженцев", "notes": "", "source": "sheet"},
    {"vanilla_id": "F5", "maps_id": "G9", "name_ru": "Код-Дазур (берег со сломанным кораблём)", "notes": "", "source": "sheet"},
    {"vanilla_id": "H2", "maps_id": "I5", "name_ru": "Деревня Эрни", "notes": "", "source": "sheet"},
    {"vanilla_id": "H3", "maps_id": "I6", "name_ru": "Жестянка", "notes": "sheet: H3 - I6", "source": "sheet"},
    {"vanilla_id": "H4", "maps_id": "I7", "name_ru": "Форт Ло-Блё (Аванпост)", "notes": "Ernie outpost / Global AI", "source": "sheet"},
    {"vanilla_id": "H7", "maps_id": "H14", "name_ru": "Шахта (около Флитауна)", "notes": "", "source": "sheet"},
    {"vanilla_id": "I1", "maps_id": "K4", "name_ru": "Флаговый холм", "notes": "", "source": "sheet"},
    {"vanilla_id": "I2", "maps_id": "M4", "name_ru": "Смотровая площадка", "notes": "vanilla I2 ≠ maps I2 (доктор)", "source": "sheet"},
    {"vanilla_id": "I3", "maps_id": "M7", "name_ru": "Изумрудный берег (пляж с минами)", "notes": "sheet → M7 (заглушка); runtime Emerald Coast = J7", "source": "sheet"},
    # suite extras (not in sheet transfer block)
    {
        "vanilla_id": "I1",
        "maps_id": "M1",
        "name_ru": "Старт кампании (зона высадки)",
        "notes": "suite: InitialSector M1; sheet I1→K4 is Flag Hill. This row is start remap, not Flag Hill.",
        "source": "suite-docs",
    },
]


SEA_FILLER_RE = re.compile(
    r"^(Море|Река|Саванна \(Берег\)|Зеленка|Заглушка|Филер)",
    re.I,
)


def sector_sort_key(sid: str):
    m = re.match(r"^([A-P])(\d+)(_Underground)?$", sid or "")
    if not m:
        return (99, 0, 1, sid or "")
    return (ord(m.group(1)) - ord("A"), int(m.group(2)), 1 if m.group(3) else 0, sid)


def classify(sheet_note: str, has_runtime: bool) -> str:
    note = (sheet_note or "").strip()
    if has_runtime and not note:
        return "runtime_only"
    if has_runtime and note:
        return "authored"
    if note:
        low = note.lower()
        # strip leading sector id like "L12 " / "Н25 "
        bare = re.sub(r"^[A-PА-Я]\d+\s*", "", note, flags=re.I).strip()
        bare_low = bare.lower()
        if (
            note in ("Море", "Река")
            or bare in ("Море", "Река")
            or low.startswith("море")
            or bare_low.startswith("море")
            or note.startswith("Река")
            or bare.startswith("Река")
            or "река" == bare_low
            or bare_low.startswith("река ")
        ):
            return "sea_or_filler"
        if "филер" in low or note == "Заглушка" or bare == "Заглушка":
            return "sea_or_filler"
        return "sheet_only"
    return "empty"


def md_escape(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--maps-root",
        type=Path,
        default=Path(__file__).resolve().parents[3] / "jazz-maps",
        help="Unused for IO; kept for CLI compat. Runtime JSON is under jazz docs.",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Content dir (default: jazz/docs/technical/maps)",
    )
    args = ap.parse_args()
    jazz_root = Path(__file__).resolve().parents[2]
    content_dir = (args.out or (jazz_root / "docs" / "technical" / "maps")).resolve()
    data_dir = content_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    runtime_path = data_dir / "sectors-runtime.json"
    if not runtime_path.is_file():
        print(f"ERROR: run export-jazz-maps-sectors.py first ({runtime_path})", file=sys.stderr)
        return 1
    runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
    by_id = {s["sectorId"]: s for s in runtime["sectors"]}
    surface_ids = {sid for sid, s in by_id.items() if not s.get("underground")}

    # --- sheet grid CSV ---
    sheet_csv = data_dir / "sheet-karta-new-grid.csv"
    with sheet_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["sectorId", "sheet_note"])
        w.writeheader()
        for letter in LETTERS:
            for col in COLS:
                sid = f"{letter}{col}"
                if sid in SHEET_NEW:
                    w.writerow({"sectorId": sid, "sheet_note": SHEET_NEW[sid]})

    # --- transfer CSV + statuses ---
    transfer_rows = []
    for t in TRANSFERS:
        mid = t["maps_id"]
        if mid in by_id:
            status = "ok"
        else:
            status = "missing_moditem"
        transfer_rows.append({**t, "runtime_status": status})

    transfer_csv = data_dir / "sector-transfer.csv"
    with transfer_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=[
                "vanilla_id",
                "maps_id",
                "name_ru",
                "notes",
                "source",
                "runtime_status",
            ],
        )
        w.writeheader()
        w.writerows(transfer_rows)

    # --- atlas CSV ---
    atlas_rows = []
    for letter in LETTERS:
        for col in COLS:
            sid = f"{letter}{col}"
            note = SHEET_NEW.get(sid, "")
            rt = by_id.get(sid)
            has_rt = rt is not None
            kind = classify(note, has_rt)
            atlas_rows.append(
                {
                    "sectorId": sid,
                    "sheet_note": note,
                    "display_name": (rt or {}).get("display_name", ""),
                    "comment": (rt or {}).get("comment", ""),
                    "mapName": (rt or {}).get("mapName", ""),
                    "Label1": (rt or {}).get("Label1", ""),
                    "City": (rt or {}).get("City", ""),
                    "WeatherZone": (rt or {}).get("WeatherZone", ""),
                    "kind": kind,
                    "has_moditem": "yes" if has_rt else "no",
                }
            )
    # underground appendix
    for sid in sorted(
        (s for s in by_id if by_id[s].get("underground")), key=sector_sort_key
    ):
        rt = by_id[sid]
        atlas_rows.append(
            {
                "sectorId": sid,
                "sheet_note": "(underground — not on sheet surface grid)",
                "display_name": rt.get("display_name", ""),
                "comment": rt.get("comment", ""),
                "mapName": rt.get("mapName", ""),
                "Label1": rt.get("Label1", ""),
                "City": rt.get("City", ""),
                "WeatherZone": rt.get("WeatherZone", ""),
                "kind": "underground",
                "has_moditem": "yes",
            }
        )

    atlas_csv = data_dir / "sector-atlas.csv"
    with atlas_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=[
                "sectorId",
                "sheet_note",
                "display_name",
                "comment",
                "mapName",
                "Label1",
                "City",
                "WeatherZone",
                "kind",
                "has_moditem",
            ],
        )
        w.writeheader()
        w.writerows(atlas_rows)

    # --- diffs ---
    transfer_missing = [t for t in transfer_rows if t["runtime_status"] != "ok"]
    sheet_named = {
        sid: note
        for sid, note in SHEET_NEW.items()
        if note
        and classify(note, sid in by_id) == "sheet_only"
    }
    runtime_no_sheet = sorted(
        (
            sid
            for sid in surface_ids
            if sid not in SHEET_NEW or not SHEET_NEW.get(sid, "").strip()
        ),
        key=sector_sort_key,
    )
    # named sheet cells that look intentional but missing runtime
    sheet_only_named = sorted(sheet_named.items(), key=lambda x: sector_sort_key(x[0]))

    # --- MD: transfer ---
    transfer_md = content_dir / "sector-transfer.md"
    lines = [
        "# Трансфер локаций: vanilla HotDiamonds → jazz-maps",
        "",
        "Канон дизайна: Google Sheet «Карта» → блок **Трансфер локаций** "
        "(spreadsheet `19Je4n5Ju4cYmTLimzw45aFq_Ll8Wxz21RLIETFRsH2g`, gid `863693534`, снимок 2026-08-01).",
        "",
        "Machine-readable: [`data/sector-transfer.csv`](data/sector-transfer.csv).",
        "",
        "Профиль **без maps** (`jazz-nomaps`) сохраняет vanilla ID — эта таблица для authored `jazz-maps` / `HotDiamonds` с `sector_bottomright = P32`.",
        "",
        "| vanilla | maps | Название | runtime | source | notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for t in transfer_rows:
        lines.append(
            f"| `{t['vanilla_id']}` | `{t['maps_id']}` | {md_escape(t['name_ru'])} | "
            f"`{t['runtime_status']}` | {t['source']} | {md_escape(t['notes'])} |"
        )
    lines += [
        "",
        "## Статусы",
        "",
        "- `ok` — есть `ModItemSector` с этим `sectorId` в `jazz-maps/items.lua`.",
        "- `missing_moditem` — target из sheet/suite не найден среди 245 authored sectors.",
        "",
        "## Связанные документы",
        "",
        "- [Атлас секторов](sector-atlas.md)",
        "- [Сверка sheet ↔ runtime](sector-sheet-vs-runtime.md)",
        "- Suite: [`maps-quests-content-catalog.md`](../systems/maps-quests-content-catalog.md)",
        "",
    ]
    transfer_md.write_text("\n".join(lines), encoding="utf-8")

    # --- MD: atlas ---
    atlas_md = content_dir / "sector-atlas.md"
    authored = [r for r in atlas_rows if r["kind"] == "authored"]
    sheet_only = [r for r in atlas_rows if r["kind"] == "sheet_only"]
    sea = [r for r in atlas_rows if r["kind"] == "sea_or_filler"]
    runtime_only = [r for r in atlas_rows if r["kind"] == "runtime_only"]
    underground = [r for r in atlas_rows if r["kind"] == "underground"]

    alines = [
        "# Атлас секторов Grand Chien (jazz-maps)",
        "",
        "Расширенная кампания `HotDiamonds`: сетка **A–P × 1–32** (`sector_bottomright = P32`), "
        "старт **`M1`**, сателлит [`GrandChien2.png`](../../../../jazz-maps/Images/GrandChien2.png) "
        "(`map_file = Mod/FhNNYd/Images/GrandChien2.png`). Underground: `Images/BigMap_Under_1.png`.",
        "",
        f"Снимок runtime: **{runtime['count']}** `ModItemSector` "
        f"(surface {runtime['surface']}, underground {runtime['underground']}) "
        "из `items.lua` — без обхода `Maps/`.",
        "",
        "Дизайн-заметки ячеек — из Google Sheet «Карта» (новая сетка). Колонка `sheet_note` "
        "**не** равна runtime `display_name`.",
        "",
        "Данные: [`data/sector-atlas.csv`](data/sector-atlas.csv), "
        "[`data/sectors-runtime.csv`](data/sectors-runtime.csv), "
        "[`data/sheet-karta-new-grid.csv`](data/sheet-karta-new-grid.csv).",
        "",
        "## Сводка kind",
        "",
        f"| kind | count |",
        f"| --- | ---: |",
        f"| authored (sheet+ModItem) | {len(authored)} |",
        f"| sheet_only | {len(sheet_only)} |",
        f"| sea_or_filler | {len(sea)} |",
        f"| runtime_only (ModItem, пустой sheet) | {len(runtime_only)} |",
        f"| empty (ни sheet, ни ModItem) | {sum(1 for r in atlas_rows if r['kind']=='empty')} |",
        f"| underground | {len(underground)} |",
        "",
        "## Authored surface (есть ModItemSector)",
        "",
        "| Id | display_name | comment | mapName | sheet_note |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in sorted(
        [x for x in atlas_rows if x["has_moditem"] == "yes" and x["kind"] != "underground"],
        key=lambda x: sector_sort_key(x["sectorId"]),
    ):
        alines.append(
            f"| `{r['sectorId']}` | {md_escape(r['display_name'])} | {md_escape(r['comment'])} | "
            f"`{r['mapName']}` | {md_escape(r['sheet_note'])} |"
        )

    alines += [
        "",
        "## Underground",
        "",
        "| Id | display_name | comment | mapName |",
        "| --- | --- | --- | --- |",
    ]
    for r in underground:
        alines.append(
            f"| `{r['sectorId']}` | {md_escape(r['display_name'])} | "
            f"{md_escape(r['comment'])} | `{r['mapName']}` |"
        )

    alines += [
        "",
        "## Sheet-only (заметка есть, ModItemSector нет)",
        "",
        "Полный список — в сверке. Здесь первые 40:",
        "",
        "| Id | sheet_note |",
        "| --- | --- |",
    ]
    for sid, note in sheet_only_named[:40]:
        alines.append(f"| `{sid}` | {md_escape(note)} |")
    if len(sheet_only_named) > 40:
        alines.append(f"| … | ещё {len(sheet_only_named) - 40} в [sector-sheet-vs-runtime.md](sector-sheet-vs-runtime.md) |")

    alines += [
        "",
        "## Связанные документы",
        "",
        "- [Трансфер](sector-transfer.md)",
        "- [Сверка sheet ↔ runtime](sector-sheet-vs-runtime.md)",
        "- [Квесты / локации / враги](../../../../jazz-maps/docs/content/quests-locations-enemies.md)",
        "",
    ]
    atlas_md.write_text("\n".join(alines), encoding="utf-8")

    # --- MD: diff ---
    diff_md = content_dir / "sector-sheet-vs-runtime.md"
    dlines = [
        "# Сверка: Google Sheet «Карта» ↔ jazz-maps runtime",
        "",
        "Дата снимка sheet: **2026-08-01**. Runtime: `items.lua` / `ModItemSector` "
        f"(**{runtime['count']}**).",
        "",
        "Цвета ячеек sheet (готово / в планах / в разработке) через export **недоступны** — "
        "статус работ только если он есть в тексте заметки.",
        "",
        "## Transfer targets без ModItemSector",
        "",
    ]
    if not transfer_missing:
        dlines.append("_Нет — все target ID из таблицы трансфера найдены._")
    else:
        dlines += [
            "| vanilla | maps | name | source |",
            "| --- | --- | --- | --- |",
        ]
        for t in transfer_missing:
            dlines.append(
                f"| `{t['vanilla_id']}` | `{t['maps_id']}` | {md_escape(t['name_ru'])} | {t['source']} |"
            )

    dlines += [
        "",
        f"## Sheet-only named cells (нет ModItemSector) — {len(sheet_only_named)}",
        "",
        "| Id | sheet_note |",
        "| --- | --- |",
    ]
    for sid, note in sheet_only_named:
        dlines.append(f"| `{sid}` | {md_escape(note)} |")

    dlines += [
        "",
        f"## Runtime surface без подписи в sheet — {len(runtime_no_sheet)}",
        "",
        "Сектора с `ModItemSector`, у которых в новой сетке sheet нет текста "
        "(или ячейка отсутствует в снимке).",
        "",
        "<details><summary>Список ID</summary>",
        "",
        ", ".join(f"`{s}`" for s in runtime_no_sheet),
        "",
        "</details>",
        "",
        "## Замечания по именам / коллизиям",
        "",
        "| Тема | Деталь |",
        "| --- | --- |",
        "| Понтагрюэль | Sheet: `D7→E15`, `C7→E15`, `D8→E16`; runtime names брать из `display_name`/`comment` на E15/E16. |",
        "| Изумрудный берег | Sheet: vanilla `I3→M7` (заглушка); в runtime демо Эрни Emerald Coast = **`J7`**. |",
        "| Смотровая | Sheet: vanilla `I2→M4`; maps **`I2`** — жильё доктора (другая локация). |",
        "| Старт | Suite `InitialSector=M1`; Flag Hill sheet `I1→K4` — не путать со стартом. |",
        "| Орлиное гнездо | `A20→B28` (Major HQ). |",
        "| Форт Ло-Блё | `H4→I7`. |",
        "| Кириллица С vs C | Sheet иногда пишет `С6` — нормализовано в `C6`. |",
        "",
        "## Пересборка",
        "",
        "```text",
        "python docs/tools/export-jazz-maps-sectors.py",
        "python docs/tools/build-sector-atlas-docs.py",
        "```",
        "",
    ]
    diff_md.write_text("\n".join(dlines), encoding="utf-8")

    print(f"Wrote {sheet_csv}")
    print(f"Wrote {transfer_csv}")
    print(f"Wrote {atlas_csv}")
    print(f"Wrote {transfer_md}")
    print(f"Wrote {atlas_md}")
    print(f"Wrote {diff_md}")
    print(
        f"transfer={len(transfer_rows)} missing={len(transfer_missing)} "
        f"sheet_only={len(sheet_only_named)} runtime_no_sheet={len(runtime_no_sheet)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
