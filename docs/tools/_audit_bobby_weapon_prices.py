# -*- coding: utf-8 -*-
"""Audit weapon InventoryItem.Cost: current vs realism USD vs proposed game Cost.

Usage:
  python docs/tools/_audit_bobby_weapon_prices.py
  python docs/tools/_audit_bobby_weapon_prices.py --json .tmp/bobby_weapon_prices.json

`proposed` — канонический game `$` для **всех** active стволов (не только Bobby):
  Bobby Ray buy base, и позже world buy/sell ops (ECON-002/003) от того же `Cost`.
  `shop=out_*` = вне каталога Bobby (`CanAppearInShop=false`), но Cost всё равно нужен.

Realism = rough real-world USD (surplus / civilian / gray-market order of magnitude).
Proposed blends realism with balance tier so progression holds.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WEAPONS_CSV = ROOT / "docs/technical/weapons/data/weapons.csv"

# Standalone heavy weapons missing from weapons.csv (GrenadeLauncher / RocketLauncher).
# UnderslungGrenadeLauncher — не в каталоге Bobby (модуль/подствол, не витринный ствол).
EXTRA_HEAVY: list[dict] = [
    {
        "id": "M79",
        "display_name": "M79",
        "family_id": "grenade-launcher",
        "balance_tier": "1",
        "balance_subtier": "1",
        "tier_label": "1-1",
        "catalog_status": "active",
        "cost": "5000",
        "caliber": "JAZZ_Caliber_40mmGrenade",
    },
    {
        "id": "China_Lake",
        "display_name": "China Lake",
        "family_id": "grenade-launcher",
        "balance_tier": "2",
        "balance_subtier": "4",
        "tier_label": "2-4",
        "catalog_status": "active",
        "cost": "10000",
        "caliber": "JAZZ_Caliber_40mmGrenade",
    },
    {
        "id": "MGL",
        "display_name": "MGL",
        "family_id": "grenade-launcher",
        "balance_tier": "3",
        "balance_subtier": "1",
        "tier_label": "3-1",
        "catalog_status": "active",
        "cost": "55000",
        "caliber": "JAZZ_Caliber_40mmGrenade",
    },
    {
        "id": "RPG7",
        "display_name": "RPG-7",
        "family_id": "rocket-launcher",
        "balance_tier": "2",
        "balance_subtier": "1",
        "tier_label": "2-1",
        "catalog_status": "active",
        "cost": "60000",
        "caliber": "JAZZ_Caliber_Warhead",
    },
    {
        "id": "M72LAW",
        "display_name": "M72 LAW",
        "family_id": "rocket-launcher",
        "balance_tier": "2",
        "balance_subtier": "3",
        "tier_label": "2-3",
        "catalog_status": "active",
        "cost": "14000",
        "caliber": "JAZZ_Caliber_Warhead",
    },
]

# Approximate real USD (order of magnitude). Conflict-surplus / civilian / gray market.
REALISM_USD: dict[str, int] = {
    # pistols
    "MAC1950": 450,
    "Luger": 800,
    "SWModel52": 900,
    "TT33": 150,
    "CZ52": 250,
    "Colt1911": 500,
    "Makarov": 200,
    "P210": 1800,
    "P38": 400,
    "PB": 600,
    "HiPower": 550,
    "SWModel5906": 400,
    "VectorCP1": 350,
    "Bereta92": 550,
    "CZ75": 500,
    "MP446VIKING": 450,
    "DesertEagle": 1800,
    "Kimber": 900,
    "USP45": 1000,
    "Glock17": 550,
    "GrizzlyLAR": 2200,
    "P220": 900,
    "P226": 1000,
    "FiveSeven": 1200,
    # autopistols
    "Scorpion": 400,
    "MAC10": 600,
    "MicroUZI": 700,
    "Beretta93r": 2500,
    "APS": 800,
    "Glock18": 3500,
    # revolvers
    "SWModel10": 250,
    "Colt38Special": 250,
    "ColtM1917": 350,
    "ColtPeacemaker": 600,
    "SWModel19": 550,
    "Welrod": 2000,
    "Webley": 400,
    "MR73": 2500,
    "SWModel29": 900,
    "ColtAnaconda": 1200,
    "RSH12": 8000,
    "Korth": 4500,
    "TexRevolver": 3500,
    # SMG
    "MAT49": 350,
    "MP40": 500,
    "M3GreaseGun": 400,
    "Sterling": 600,
    "MPL": 500,
    "PPS43": 250,
    "PPSH": 350,
    "Thompson": 1200,
    "Agram2000": 450,
    "M45": 500,
    "UZI": 700,
    "BerettaM12": 800,
    "PP19Bizon": 900,
    "SpectreM4": 1100,
    "MP5A2": 1500,
    "MP5K": 1600,
    "TMP": 1800,
    "MP5A4": 1700,
    "UMP45": 1400,
    "MP5SD": 2200,
    "MP7": 1800,
    "P90": 2500,
    "LionRoar": 2000,
    # shotguns
    "DoubleBarrelShotgun": 250,
    "M1897": 450,
    "Auto5": 700,
    "Ithaca": 500,
    "R870": 450,
    "Striker": 900,
    "SPAS12": 1200,
    "Stoeger": 800,
    "M41Shotgun": 1400,
    "USAS12": 2500,
    "AA12": 4000,
    "Auto5_quest": 900,
    # carbines
    "Winchester1894": 500,
    "M2Carbine": 600,
    "DeLisle": 3500,
    "Mini14": 800,
    "ZastavaM92": 700,
    "CAR15": 900,
    "AKSU": 900,
    "M4A1": 1100,
    "G36c": 1600,
    "VSS": 3500,
    "Sig552": 2000,
    "Sig552SWAT": 2400,
    "AS_Val": 4000,
    "Winchester_Quest": 1200,
    # AR
    "STG44": 2000,
    "M16A1": 700,
    "Type56": 250,
    "FAMAS": 900,
    "Zastava_M70": 350,
    "AK47": 400,
    "AKM": 350,
    "M16A2": 800,
    "AK74": 550,
    "AR10DMR": 1600,
    "HK33": 1200,
    "AUG": 1800,
    "G36": 1700,
    "M16A4": 1000,
    "Sig550": 2200,
    "Sig550Custom": 2800,
    "AN94": 5000,
    # BR
    "Mas36": 300,
    "SKS": 250,
    "M1Garand": 800,
    "FG42": 4500,
    "G43": 1200,
    "SVT40": 900,
    "AVT40": 2500,
    "AR10": 1400,
    "MAS49": 600,
    "M14SAW": 1200,
    "FNFAL": 900,
    "Galil": 1100,
    "G3A3": 1000,
    "G3A4": 1200,
    "Galil_FlagHill": 2000,
    # sniper
    "Mosin": 200,
    "Gewehr98": 450,
    "Springfield": 700,
    "FRF2": 2500,
    "ZastavaM76": 900,
    "M21": 1400,
    "DragunovSVD": 1200,
    "M700": 900,
    "G3SniperV1": 1800,
    "M24Sniper": 3500,
    "M1A": 1400,
    "ArcticWarfare": 4500,
    "SVU": 2800,
    "BarretM82": 10000,
    "PSG1": 8000,
    "ScoutSniper": 3500,
    "DragunovSVD_Custom": 2000,
    "GoldenGun": 5000,
    # LMG
    "MAC2429": 900,
    "BAR": 1500,
    "RPD": 700,
    "U100": 1800,
    "RPK": 800,
    "RPK74": 1000,
    "FNMinimi": 3500,
    "HK21": 5000,
    "HK23e": 5500,
    # MG
    "DP27": 600,
    "MG42": 2000,
    "MG58": 2500,
    "AA52": 1500,
    "M60": 2500,
    "M60E3": 3000,
    "FNMAG": 4500,
    "PKM": 2800,
    "M60E4": 4000,
    "BrowningM2HMG": 12000,
    # heavy (not in weapons.csv)
    "M79": 900,
    "China_Lake": 2500,
    "MGL": 4500,
    "RPG7": 1200,  # surplus-common in conflicts
    "M72LAW": 800,
}

# Family × major-tier anchor bands (game $). Subtier spreads inside the band.
FAMILY_BANDS: dict[str, dict[int, tuple[int, int]]] = {
    # pistols: чуть ниже (owner 2026-08-07)
    "pistol": {1: (280, 950), 2: (700, 3600), 3: (2000, 7200)},
    "autopistol": {1: (800, 1500), 2: (1800, 9000), 3: (8000, 16000)},
    "revolver": {1: (350, 1100), 2: (800, 3500), 3: (3000, 9000)},
    "submachine-gun": {1: (700, 2200), 2: (2000, 9000), 3: (9000, 22000)},
    "shotgun": {1: (600, 1800), 2: (1800, 8000), 3: (8000, 22000)},
    "carbine": {1: (1200, 3500), 2: (3500, 14000), 3: (12000, 32000)},
    "assault-rifle": {1: (1500, 3500), 2: (3500, 16000), 3: (14000, 40000)},
    "battle-rifle": {1: (900, 3500), 2: (3500, 14000), 3: (12000, 28000)},
    "sniper-rifle": {1: (900, 2800), 2: (5000, 22000), 3: (20000, 90000)},
    "light-machine-gun": {1: (2500, 6000), 2: (7000, 28000), 3: (28000, 70000)},
    "machine-gun": {1: (2500, 7000), 2: (9000, 35000), 3: (30000, 80000)},
    "grenade-launcher": {1: (3500, 7000), 2: (8000, 22000), 3: (18000, 40000)},
    "rocket-launcher": {1: (4000, 9000), 2: (7000, 22000), 3: (16000, 35000)},
}

# Manual proposed overrides where formula would miss flavor / UNIQ / quest.
# proposed = InventoryItem.Cost для Bobby buy И world buy/sell (ECON-002/003).
# why-текст — для колонки «Почему» в canvas/TSV.
PROPOSED_OVERRIDE: dict[str, tuple[int, str]] = {
    "PB": (1800, "UNIQ Cost (мир); вне Bobby"),
    "Welrod": (12000, "silent rare: BR4, низкий RestockWeight later"),
    "DeLisle": (22000, "silent carbine rare/дорого: BR4"),
    "Stoeger": (4000, "вертикалка UNIQ (у легов нет) — в Bobby ok"),
    "AN94": (55000, "Абакан BR5 RW5; early U=1 → ×81 ≈4.5M / вес ×0.0001"),
    "Winchester1894": (2200, "lever ~2005 gray ok, early BR1"),
    "BAR": (5500, "WW2 LMG ещё встречается; BR1"),
    "Thompson": (3500, "Tommy ещё на рынке; BR1"),
    "M1897": (1800, "trench shotgun ок; BR1"),
    "P38": (1100, "WW2 service pistol surplus; BR1; pistol band↓"),
    "TexRevolver": (12000, "квест Cost (мир); вне Bobby"),
    "Korth": (7500, "премиум-револьвер T3: реализм высокий (~$4.5k), не vanilla 500"),
    "DesertEagle": (4500, "зрелищный .44; pistol↓ mid T2"),
    "GrizzlyLAR": (5200, ".50 AE редко; чуть выше DE; pistol↓"),
    "FiveSeven": (6500, "редкий 5.7; pistol↓ с 8k"),
    "Glock18": (12000, "авто-Glock: restricted/редко → дороже обычного G17"),
    "Beretta93r": (6500, "burst-пистолет редко на рынке; был занижен (1250)"),
    "VSS": (28000, "спец 9×39: редко + тир 2-5; срезали 100k"),
    "AS_Val": (32000, "T3 спец 9×39; чуть выше VSS"),
    "AVT40": (5500, "UNIQ WWII Cost (мир); вне Bobby"),
    "BarretM82": (75000, "антиматерия .50: реализм ~$10k × премиум T3; срезали 120k"),
    "PSG1": (55000, "match-снайпер HK: редко/дорого, ниже Barrett"),
    "ScoutSniper": (48000, "UNIQ Cost (мир); вне Bobby; срезали 160k"),
    "ArcticWarfare": (42000, "T3 bolt precision: реализм высокий, ниже PSG1/Barrett"),
    "SVU": (38000, "T3 bullpup SVD-линии; срезали 90k"),
    "BrowningM2HMG": (55000, "HMG .50 Cost (мир/трофей); вне Bobby"),
    "PKM": (28000, "GPMG массовый: реализм ~$2.8k, не 120k; тир 2-5"),
    "HK21": (45000, "редкий belt LMG 7.62; срезали 150k"),
    "HK23e": (48000, "редкий belt LMG 5.56; рядом с HK21"),
    "AA12": (28000, "T3 авто-дробовик: дорого, но не 75k"),
    "USAS12": (22000, "T3 авто-12g; чуть дешевле AA12"),
    "Sig550Custom": (32000, "T3 RIS-пакет; срезали 100k"),
    "Sig550": (24000, "T3 швейцарский AR; премиум vs AUG/G36"),
    "Sig552": (22000, "T3 карбин SIG; рядом с 550"),
    "Sig552SWAT": (26000, "T3 SWAT-вариант; чуть выше 552"),
    "Glock17": (2500, "массовый 9mm; pistol↓ с 3200"),
    "Kimber": (2200, "кастом 1911; pistol↓"),
    "HiPower": (1100, "классика 9mm T2-1; pistol↓"),
    "MAT49": (1600, "Cost (мир); вне Bobby ~2005"),
    "M79": (5500, "40mm break-action; BR1; commonish GL"),
    "China_Lake": (14000, "pump 40mm rare US; BR3"),
    "MGL": (32000, "Milkor 6-shot; срезали 55k; BR4"),
    "RPG7": (16000, "массовый RPG surplus; срезали 60k; BR2"),
    "M72LAW": (9000, "одноразовый LAW; BR2–3"),
    "M14SAW": (7500, "T2 battle rifle; был 1250 (баг) → band+реализм"),
    "AK74": (8500, "массовый 5.45: срезали 60k; surplus×тир 2-4"),
    "AKSU": (9000, "короткий 5.45: срезали 28k; чуть выше AK74"),
    "RPK74": (14000, "LMG 5.45: срезали 75k; между RPK и Minimi"),
    "FNMinimi": (22000, "NATO SAW: реализм ~$3.5k + тир 2-5"),
    "TMP": (9000, "компакт PDW; срезали 28k"),
    "SPAS12": (7500, "икона/редковат; срезали 28k к реализму+тиру"),
    "M41Shotgun": (9000, "полуавто 12g T3-1; срезали 32k"),
    "Type56": (2800, "самый дешёвый AK-клон: реализм ~$250, тир тянет вверх"),
    "AK47": (4500, "массовый 7.62: реализм дешёвый → mid T2, не 8.5k"),
    "AKM": (4200, "чуть ниже AK47 (тот же класс surplus)"),
    "M16A1": (4000, "ранний 5.56 NATO; рядом с Type56/AK band"),
    "AUG": (14000, "bullpup T2-5: премиум vs M16A4"),
    "G36": (13500, "поздний 5.56; рядом с AUG"),
    "M16A4": (12000, "стандартный late 5.56; ниже AUG/G36"),
    "HK33": (11000, "HK 5.56; между M16A4 и AUG"),
    "AR10DMR": (12000, "DMR 7.62 в AR-слоте; точность-премиум"),
    "STG44": (3200, "WW2 StG Cost (мир); вне Bobby"),
    "Galil_FlagHill": (14000, "квест Cost (мир); вне Bobby"),
    "LionRoar": (10000, "квест Cost (мир); вне Bobby"),
    "Winchester_Quest": (5000, "квест Cost (мир); вне Bobby"),
    "Auto5_quest": (4500, "квест Cost (мир); вне Bobby"),
    "DragunovSVD_Custom": (22000, "квест Cost (мир); вне Bobby"),
    "GoldenGun": (25000, "квест Cost (мир); вне Bobby"),
    "MG58": (7000, "UNIQ MG Cost (мир); вне Bobby"),
    "RSH12": (18000, "UNIQ экзот .50 Cost (мир); вне Bobby"),
    # antiques / out_old — Cost для лута и world sell/buy, не витрина Bobby
    "Luger": (1900, "antique Cost (мир); вне Bobby"),
    "MP40": (1600, "antique Cost (мир); вне Bobby"),
    "Auto5": (2100, "antique Cost (мир); вне Bobby"),
    "M1Garand": (2700, "antique Cost (мир); вне Bobby"),
    "ColtPeacemaker": (1600, "antique Cost (мир); вне Bobby"),
    "ColtM1917": (1100, "antique Cost (мир); вне Bobby"),
    "FG42": (6500, "rare WWII Cost (мир); вне Bobby"),
    "G43": (3800, "antique Cost (мир); вне Bobby"),
    "Gewehr98": (1800, "antique Cost (мир); вне Bobby"),
    "MG42": (7000, "WWII MG Cost (мир); вне Bobby"),
    "Mas36": (1400, "antique Cost (мир); вне Bobby"),
    "Springfield": (2300, "antique Cost (мир); вне Bobby"),
    "MAC2429": (3600, "antique LMG Cost (мир); вне Bobby"),
    "SVT40": (3200, "antique Cost (мир); вне Bobby"),
    "MAC1950": (1100, "antique Cost (мир); вне Bobby"),
    "SWModel52": (2100, "antique Cost (мир); вне Bobby"),
}

QUEST_UNIQUES = {
    "Galil_FlagHill",
    "LionRoar",
    "GoldenGun",
    "DragunovSVD_Custom",
    "Winchester_Quest",
    "Auto5_quest",
    "BrowningM2HMG",
    "TexRevolver",
}

# UNIQ, которые всё же продаём у Bobby (редко/дорого где указано).
BOBBY_ALLOWED_UNIQUES = {
    "Welrod",
    "DeLisle",
    "Stoeger",
    "AN94",
}

# Forced BR item.Tier for specials (overrides balance map).
BOBBY_TIER_OVERRIDE = {
    "Welrod": 4,  # редко
    "DeLisle": 4,  # дорого и редко
    "Stoeger": 2,
    "AN94": 5,  # Абакан — самый конец
    "Winchester1894": 1,
    "BAR": 1,
    "Thompson": 1,
    "M1897": 1,
    "P38": 1,
    "M79": 1,
    "China_Lake": 3,
    "MGL": 4,
    "RPG7": 2,
    "M72LAW": 3,
}

# RestockWeight: выше = чаще в restock (vanilla default 100).
RESTOCK_OVERRIDE: dict[str, int] = {
    "Welrod": 12,
    "DeLisle": 10,
    "AN94": 5,
    "Stoeger": 40,
    "BarretM82": 14,
    "PSG1": 16,
    "ScoutSniper": 8,
    "FiveSeven": 22,
    "Glock18": 18,
    "Beretta93r": 25,
    "VSS": 20,
    "AS_Val": 18,
    "DesertEagle": 35,
    "GrizzlyLAR": 28,
    "Korth": 30,
    "AA12": 22,
    "USAS12": 24,
    "HK21": 18,
    "HK23e": 18,
    "FNMinimi": 40,
    "PKM": 45,
    "Type56": 145,
    "AK47": 135,
    "AKM": 130,
    "Makarov": 125,
    "M79": 55,
    "China_Lake": 22,
    "MGL": 14,
    "RPG7": 70,
    "M72LAW": 45,
    "TT33": 120,
    "Colt1911": 110,
    "SKS": 115,
    "Mosin": 110,
    "DoubleBarrelShotgun": 120,
    "R870": 95,
    "M16A1": 90,
    "MP5A2": 70,
    "P90": 35,
    "MP7": 35,
    "Sig550": 40,
    "Sig550Custom": 28,
    "Winchester1894": 70,
    "BAR": 55,
    "Thompson": 65,
    "M1897": 75,
    "P38": 85,
}

# Вне Bobby: не типичный чёрный рынок ~2001–2005.
# Оставляем: TT, 1911, P38, Makarov, SKS, Mosin, Thompson, M1897, BAR, Winchester1894…
TOO_OLD_IDS = {
    "ColtPeacemaker",
    "ColtM1917",
    "STG44",
    "Luger",
    "MP40",
    "MAT49",
    "FG42",
    "G43",
    "Gewehr98",
    "MG42",
    "Mas36",
    "M1Garand",
    "Springfield",
    "MAC2429",
    "SVT40",
    "Auto5",
    "MAC1950",
    "SWModel52",
}


# Bobby Ray unlock tiers: total = 5 (|| Legion majors+steps, not vanilla 3).
# Item.Tier must be <= UnlockedTier to restock. Quest unlock 4–5 ещё не вквесте.
BOBBY_TIER_TOTAL = 5

# Unlock ladder (plan — quest TCEs later):
# 1 shop open || Legion major1
# 2 ~2 mines / mainland || Legion ~21
# 3 mid campaign || Legion ~23–25
# 4 WorldFlip / late mid || Legion ~31
# 5 late || Legion 33
BOBBY_UNLOCK_PLAN = [
    (1, "Open shop", "Legion major 1 (11–13)"),
    (2, "≥2 mines / mainland", "Legion ~21–22"),
    (3, "Mid (time/mines)", "Legion ~23–25"),
    (4, "WorldFlip / late-mid", "Legion ~31–32"),
    (5, "Late campaign", "Legion 33"),
]



def round_price(n: float) -> int:
    n = max(50, int(round(n)))
    if n < 1000:
        return int(round(n / 50.0) * 50)
    if n < 5000:
        return int(round(n / 100.0) * 100)
    if n < 20000:
        return int(round(n / 250.0) * 250)
    if n < 50000:
        return int(round(n / 500.0) * 500)
    return int(round(n / 1000.0) * 1000)


def parse_major_tier(tier_label: str, balance_tier: str) -> int:
    if balance_tier and str(balance_tier).isdigit():
        return int(balance_tier)
    if tier_label and tier_label[0].isdigit():
        return int(tier_label[0])
    return 2


def parse_subtier(tier_label: str, balance_subtier: str) -> float:
    s = str(balance_subtier or "")
    if s.isdigit():
        return min(5, max(1, int(s))) / 5.0
    if "UNIQ" in (tier_label or "").upper():
        return 1.0
    parts = (tier_label or "").split("-")
    if len(parts) >= 2 and parts[1].isdigit():
        return min(5, max(1, int(parts[1]))) / 5.0
    return 0.5


def shop_exclusion(row: dict) -> tuple[str | None, str]:
    """Return (status, reason) if weapon is out of Bobby Ray catalog."""
    wid = row["id"]
    label = (row.get("tier_label") or "").upper()
    if wid in BOBBY_ALLOWED_UNIQUES:
        return None, ""
    if "UNIQ" in label or wid in QUEST_UNIQUES:
        return "out_unique", "вне Bobby: уникал / квест"
    if wid in TOO_OLD_IDS:
        return "out_old", "вне Bobby: не типичный black market ~2005"
    return None, ""


def proposed_bobby_tier(row: dict) -> int | None:
    """Map weapon balance tier → Bobby Ray item.Tier (1..5). None if out of shop."""
    excl, _ = shop_exclusion(row)
    if excl:
        return None
    wid = row["id"]
    if wid in BOBBY_TIER_OVERRIDE:
        return BOBBY_TIER_OVERRIDE[wid]

    label = (row.get("tier_label") or "").upper()
    maj = parse_major_tier(row.get("tier_label", ""), row.get("balance_tier", ""))
    sub_raw = str(row.get("balance_subtier") or "")
    if sub_raw.isdigit():
        sub = int(sub_raw)
    elif "UNIQ" in label:
        return 4  # allowed uniq without override → late-ish
    else:
        sub = 3

    if maj <= 1:
        return 1
    if maj == 2:
        if sub <= 2:
            return 2
        if sub <= 4:
            return 3
        return 4
    if maj >= 3:
        if sub <= 2:
            return 4
        return 5
    return 3


def companion_item_tier(wid: str) -> int | None:
    paths = list((ROOT / "InventoryItem").rglob(f"{wid}.lua"))
    if not paths:
        return None
    t = paths[0].read_text(encoding="utf-8", errors="replace")
    m = re.search(r"Tier\s*=\s*(\d+)", t)
    return int(m.group(1)) if m else None


def companion_restock_weight(wid: str) -> int | None:
    """None = unset (vanilla default 100 for shop items)."""
    paths = list((ROOT / "InventoryItem").rglob(f"{wid}.lua"))
    if not paths:
        return None
    t = paths[0].read_text(encoding="utf-8", errors="replace")
    m = re.search(r"RestockWeight\s*=\s*(\d+)", t)
    return int(m.group(1)) if m else None


def rarity_label(weight: int) -> str:
    if weight <= 8:
        return "очень редко"
    if weight <= 20:
        return "редко"
    if weight <= 45:
        return "нечасто"
    if weight <= 90:
        return "обычно"
    if weight <= 120:
        return "часто"
    return "очень часто"


def proposed_restock_weight(row: dict) -> int | None:
    """Proposed RestockWeight for Bobby catalog; None if out of shop."""
    if shop_exclusion(row)[0]:
        return None
    wid = row["id"]
    if wid in RESTOCK_OVERRIDE:
        return RESTOCK_OVERRIDE[wid]
    br = proposed_bobby_tier(row) or 3
    # Higher BR unlock → slightly rarer baseline
    base = {1: 100, 2: 85, 3: 70, 4: 50, 5: 32}.get(br, 70)
    # Price tax: expensive guns rarer
    prop = row.get("proposed") or int(row.get("cost") or 0) or 3000
    if prop >= 40000:
        base = min(base, 22)
    elif prop >= 20000:
        base = min(base, 35)
    elif prop >= 10000:
        base = min(base, 55)
    # Family soft bias
    fam = row.get("family_id") or ""
    if fam == "pistol" and br <= 2:
        base = min(130, base + 15)
    if fam == "revolver" and br <= 2:
        base = min(130, base + 10)
    if fam in ("machine-gun", "light-machine-gun", "sniper-rifle") and br >= 3:
        base = max(18, base - 15)
    if fam in ("grenade-launcher", "rocket-launcher"):
        base = max(14, base - 10)
    return int(base)


def propose(row: dict) -> tuple[int, int, str]:
    """Return realism_usd, proposed_game_cost, why."""
    wid = row["id"]
    realism = REALISM_USD.get(wid, 800)
    realism_note = "" if wid in REALISM_USD else " (реализм fallback $800)"

    family = row["family_id"]
    major = parse_major_tier(row.get("tier_label", ""), row.get("balance_tier", ""))
    sub = parse_subtier(row.get("tier_label", ""), row.get("balance_subtier", ""))
    bands = FAMILY_BANDS.get(family, {1: (1000, 3000), 2: (3000, 10000), 3: (10000, 30000)})
    lo, hi = bands.get(major, bands.get(2, (3000, 10000)))
    band = lo + (hi - lo) * sub
    realism_game = realism * 4.5

    if wid in PROPOSED_OVERRIDE:
        price, why = PROPOSED_OVERRIDE[wid]
        return realism, price, why + realism_note

    blended = 0.55 * band + 0.45 * realism_game
    bits = [
        f"band T{major} {int(lo)}–{int(hi)} @sub≈{sub:.0%}→{int(band)}",
        f"реализм ${realism}×4.5={int(realism_game)}",
        "blend 55/45",
    ]

    if "UNIQ" in (row.get("tier_label") or "").upper():
        blended *= 1.35
        bits.append("UNIQ ×1.35")

    if wid in QUEST_UNIQUES or (
        not row.get("tier_label") and wid.endswith(("_Quest", "_quest"))
    ):
        blended *= 1.25
        bits.append("quest ×1.25")

    proposed = round_price(blended)
    now = int(row.get("cost") or 0)
    if now and abs(proposed - now) >= max(1000, now * 0.25):
        direction = "↑" if proposed > now else "↓"
        bits.append(f"vs now {now} {direction}")

    # Relative pull explanation
    if realism_game < band * 0.7:
        bits.append("surplus дёшев → тир тянет вверх")
    elif realism_game > band * 1.4:
        bits.append("рынок дороже band → реализм тянет вверх")

    return realism, proposed, "; ".join(bits) + realism_note


def family_sort_key(fid: str) -> tuple[int, str]:
    order = [
        "pistol",
        "autopistol",
        "revolver",
        "submachine-gun",
        "shotgun",
        "carbine",
        "assault-rifle",
        "battle-rifle",
        "sniper-rifle",
        "light-machine-gun",
        "machine-gun",
        "grenade-launcher",
        "rocket-launcher",
    ]
    try:
        return (order.index(fid), fid)
    except ValueError:
        return (99, fid)


def load_rows() -> list[dict]:
    with WEAPONS_CSV.open(encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["catalog_status"] == "active"]
    seen = {r["id"] for r in rows}
    for extra in EXTRA_HEAVY:
        if extra["id"] not in seen:
            rows.append(dict(extra))
            seen.add(extra["id"])
    for r in rows:
        realism, proposed, why = propose(r)
        excl, excl_why = shop_exclusion(r)
        r["realism_usd"] = realism
        r["proposed"] = proposed
        r["cost_now"] = int(r["cost"] or 0)
        r["delta"] = proposed - r["cost_now"]
        r["shop"] = excl or "bobby"
        r["br_tier_now"] = companion_item_tier(r["id"])
        r["br_tier"] = proposed_bobby_tier(r)
        r["rw_now"] = companion_restock_weight(r["id"])
        r["rw"] = proposed_restock_weight(r)
        r["rarity"] = rarity_label(r["rw"]) if r["rw"] is not None else "—"
        if excl:
            r["why"] = f"{excl_why}. Cost (мир/продажа): {why}"
        else:
            br = r["br_tier"]
            br_now = r["br_tier_now"]
            br_bit = f"BR tier {br}/{BOBBY_TIER_TOTAL}"
            if br_now is not None and br is not None and br_now != br:
                br_bit += f" (сейчас item.Tier={br_now})"
            elif br_now is None and br is not None:
                br_bit += " (Tier unset→default 1)"
            rw = r["rw"]
            rw_now = r["rw_now"]
            rw_bit = f"{r['rarity']} RW{rw}"
            if rw_now is not None and rw_now != rw:
                rw_bit += f" (now {rw_now})"
            elif rw_now is None:
                rw_bit += " (now unset→100)"
            r["why"] = f"{why}; {br_bit}; {rw_bit}"
        r["note"] = r["shop"]
        ratio = (proposed / r["cost_now"]) if r["cost_now"] else math.inf
        r["ratio"] = ratio
    rows.sort(
        key=lambda r: (
            0 if r["shop"] == "bobby" else 1,
            r.get("br_tier") or 99,
            family_sort_key(r["family_id"]),
            r.get("tier_label") or "9",
            r["id"],
        )
    )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path)
    ap.add_argument("--tsv", type=Path)
    args = ap.parse_args()
    rows = load_rows()

    bobby = [r for r in rows if r["shop"] == "bobby"]
    out_u = [r for r in rows if r["shop"] == "out_unique"]
    out_o = [r for r in rows if r["shop"] == "out_old"]
    weird = [r for r in bobby if r["cost_now"] <= 600 and r["proposed"] >= 2000]
    huge = [r for r in bobby if abs(r["delta"]) >= 20000]
    print(f"active weapons: {len(rows)}")
    print(f"  bobby catalog: {len(bobby)}")
    print(f"  out unique: {len(out_u)}")
    print(f"  out old/not-2005: {len(out_o)}")
    from collections import Counter

    brc = Counter(r.get("br_tier") for r in bobby)
    print(f"  BR tiers total={BOBBY_TIER_TOTAL} dist={dict(sorted((k, v) for k, v in brc.items() if k))}")
    print(f"stuck-cheap now (<=600) but proposed>=2000 (bobby): {len(weird)}")
    print(f"|delta|>=20k (bobby): {len(huge)}")
    for r in huge[:15]:
        print(
            f"  {r['tier_label'] or '?':7} {r['id']:20} now={r['cost_now']:7} "
            f"real={r['realism_usd']:5} prop={r['proposed']:7} d={r['delta']:+8}"
        )

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        payload = [
            {
                "family": r["family_id"],
                "tier": r["tier_label"] or "—",
                "id": r["id"],
                "name": r["display_name"],
                "now": r["cost_now"],
                "realism": r["realism_usd"],
                "proposed": r["proposed"],
                "delta": r["delta"],
                "shop": r["shop"],
                "why": r["why"],
                "br_tier": r.get("br_tier"),
                "br_tier_now": r.get("br_tier_now"),
                "br_tier_total": BOBBY_TIER_TOTAL,
                "rw": r.get("rw"),
                "rw_now": r.get("rw_now"),
                "rarity": r.get("rarity"),
            }
            for r in rows
        ]
        args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print("wrote", args.json)

    if args.tsv:
        args.tsv.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "family\ttier\tid\tname\tnow\trealism_usd\tproposed\tdelta\tshop\tbr_tier\tbr_tier_now\trarity\trw\trw_now\twhy"
        ]
        for r in rows:
            lines.append(
                "\t".join(
                    map(
                        str,
                        [
                            r["family_id"],
                            r["tier_label"] or "—",
                            r["id"],
                            r["display_name"],
                            r["cost_now"],
                            r["realism_usd"],
                            r["proposed"],
                            r["delta"],
                            r["shop"],
                            r.get("br_tier") if r.get("br_tier") is not None else "",
                            r.get("br_tier_now") if r.get("br_tier_now") is not None else "",
                            r.get("rarity") or "",
                            r.get("rw") if r.get("rw") is not None else "",
                            r.get("rw_now") if r.get("rw_now") is not None else "",
                            r["why"].replace("\t", " "),
                        ],
                    )
                )
            )
        args.tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("wrote", args.tsv)


if __name__ == "__main__":
    main()
