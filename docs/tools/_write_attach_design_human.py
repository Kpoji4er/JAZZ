# -*- coding: utf-8 -*-
"""Parse live attachment effects into human-readable category notes."""
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "docs/technical/weapons/data"
OUT_MD = ROOT / "docs/design/attachments-by-category.md"
OUT_JSON = ROOT / "docs/tools/_attach_effects_parsed.json"

SLOT_TITLE = {
    "Scope": "Прицелы",
    "Stock": "Приклады",
    "Barrel": "Стволы",
    "Under": "Рукоятки и подствольное (Under)",
    "Handgrip": "Пистолетные рукояти",
    "Handguard": "Цевьё",
    "Side": "Лазер / фонарь (боковая планка)",
    "Magazine": "Магазины",
    "Muzzle": "Дульные устройства",
    "Bipod": "Сошки",
    "Freeswap": "Быстрая смена оружия",
    "General": "Общее",
    "Grenadelauncher": "Гранатомёт (отдельный слот)",
    "Side2": "Доп. боковой",
    "Trigger": "УСМ / режимы огня",
    "Mountfront": "Передний крепёж",
}

SLOT_INTRO = {
    "Scope": (
        "Решают, **на какой дистанции** комфортно бить и сколько AP/кликов платишь за прицел.\n\n"
        "- **Коллиматоры (Reflex)** — меньше кликов aim, шире overwatch, лучше реакции; "
        "дистанцию почти не сдвигают.\n"
        "- **Штурмовые (CombatScope ~2–4×)** — сдвигают комфортную дистанцию, +AP за выстрел, "
        "чуть сужают сектор ожидания.\n"
        "- **Длинная оптика (Scope 6–12×)** — ещё дальше, ещё дороже, сильнее сужают OW, "
        "часто крит на полном aim и больше кликов до потолка.\n"
        "- **Ночные** — как штурмовые/средние, плюс нормальная работа в темноте "
        "(часто только на полном aim)."
    ),
    "Stock": "Решают, **насколько ствол сидит в плече** vs насколько ты мобилен (в т.ч. сложенный приклад).",
    "Barrel": "Решают **дальность и характер** того же оружия: коротыш для CQB или длинный для дальней дистанции.",
    "Under": "Рукоятки держат **очередь**; сюда же часто садится **подствольный гранатомёт** или сошки.",
    "Handgrip": "Замена пистолетной рукояти — обычно эргономика, не дистанция.",
    "Handguard": "Часто только **внешний вид / крепление**; игровой смысл есть, если цевьё даёт рукоять или гранатомёт.",
    "Side": "Ближний бой и темнота: **видеть**, **подсветить**, **помочь накоротке** — не замена оптике.",
    "Magazine": "**Сколько пуль** до перезарядки и насколько магазин тяжёлый/ненадёжный.",
    "Muzzle": "**Отдача**, **тишина** или (у дробовика) **конус дроби**.",
    "Bipod": "**Позиционный** огонь лёжа: очередь держится дольше, когда ты уже лёг.",
    "Freeswap": "Жест «достал второе оружие» без обычной задержки смены.",
    "General": "Редкие спец-детали (ремни, нижние ресиверы и т.п.).",
    "Grenadelauncher": "Отдельный слот гранатомёта на части стволов (например AUG).",
    "Side2": "Второй боковой слот (например спидлоадер револьвера).",
    "Trigger": "Включает режимы огня, которых у базы не было.",
    "Mountfront": "Крепёж/ручка спереди — обычно без боевого эффекта.",
}

# Short gloss for the top glossary table only
EFFECT_GLOSS = {
    "DecreaseMaxAimActions": "меньше кликов прицеливания до потолка",
    "IncreaseMaxAimActions": "больше кликов прицеливания до потолка",
    "ExtraOverwatchShots": "больше выстрелов в overwatch",
    "ScopeOverwatchAngleIncreace": "шире сектор ожидания",
    "ScopeOverwatchAngleIncreaceBig": "сильно шире сектор ожидания",
    "ScopeOverwatchAngleDecrease": "уже сектор ожидания",
    "ScopeOverwatchAngleDecreaseBig": "сильно уже сектор ожидания",
    "IncreaseOverwatchAngle": "шире сектор ожидания",
    "MagazineSizeAdd": "больше патронов (+N)",
    "MagazineSizeIncrease": "больше патронов",
    "MagazineSizeMultiplier": "ёмкость × множитель",
    "ReduceMagazineSize": "меньше патронов",
    "SilencerHandlingReduce": "глушитель хуже Handling (legacy)",
    "SilencerHandlingDecrease": "глушитель хуже «лёгкости»",
    "SilencerJamChance": "выше шанс клина от глушителя",
    "BarrelRecoilIncrease": "ствол усиливает отдачу",
    "BarrelGroupingReduce": "ствол чуть портит кучность",
    "BarrelGroupingIncrease": "лучше кучность (Grouping)",
    "FreeWeaponSwap": "быстрая смена оружия",
    "EnableFullAuto": "включает автоогонь",
    "EnableBurst": "включает очередь",
    "ExtraBurstShots": "длиннее короткая очередь",
    "ExtraAutoShots": "длиннее автоочередь",
    "zzStockEquipped": "флаг складного приклада",
    "StockHandlingIncrease": "приклад легче (legacy)",
    "Cumbersome": "оружие громоздкое",
    "FirstShotIncreasedAim": "первая атака хода уже с min_aim",
    "PointBlankBonus": "бонус на упор",
    "LaserMark": "лазерная пометка / legacy лазер",
    "EnableRunNGun": "открывает Run&Gun",
    "ChangeCaliberToBMG": "калибр → .50 BMG",
    "IncreaseDamage": "больше базовый урон",
    "ReduceAimAccuracy20Percent": "заметно хуже AimAccuracy",
    "ReduceAimAccuracy50Percent": "сильно хуже AimAccuracy",
    "ReduceAimAccuracy80Percent": "почти ломает AimAccuracy",
    "ReduceAimAccuracy90Percent": "почти ломает AimAccuracy",
    "ReduceAimAccuracy15Percent": "чуть хуже AimAccuracy (−15%)",
    "IncreaseAimAccuracy15Percent": "чуть лучше AimAccuracy",
    "MinAim": "нужен минимум кликов aim",
    "OpportunityAttackBonusCth": "лучше реакции / перехват",
    "ScopeHandlingReduce": "штраф Handling (legacy, не в CTH)",
    "ScopeMagnification": "сдвигает комфортную дистанцию (кратность)",
    "SmallMagnification": "вторая (меньшая) кратность",
    "IncreaseShotAP": "выстрел дороже по AP",
    "ReduceShootAP": "выстрел дешевле по AP",
    "CritBonusWhenFullyAimed": "больше крит на полном aim",
    "IgnoreInTheDark": "не штрафует темнота",
    "IgnoreInTheDarkWhenFullyAimed": "в темноте ок только на полном aim",
    "ReduceAuto75Percent": "сильно режет авто",
    "ReduceBurst50Percent": "режет очередь",
    "IncreaseAimAccuracy": "лучше AimAccuracy",
    "ReduceAimAccuracy": "хуже AimAccuracy",
    "RecoilDecrease": "меньше отдача в очереди",
    "RecoilIncrease": "очередь размазывает сильнее",
    "ShotsBeforeRecoilProne": "лёжа больше пуль до сильной отдачи",
    "AccuracyBonusProne": "лёжа лучше (часто legacy flat)",
    "AccuracyBonusSameTarget": "повтор по той же цели проще",
    "BipodsHandlingDecrease": "сошки тяжелее в профиле",
    "GripHandlingIncrease": "рукоятка удобнее (legacy)",
    "GLHandlingDecrease": "гранатомёт утяжеляет",
    "GrenadeLauncher": "открывает подствольный ГП",
    "SilentShots": "тихие выстрелы",
    "StealthKillBonusPerAim": "бонус скрытного убийства за aim",
    "ReduceReliability": "хуже надёжность / чаще клин",
    "ReduceReliabilityPercent": "режет надёжность %",
    "IncreaseReliability": "надёжнее",
    "SilencerGroupingReduce10": "глушитель чуть портит кучность",
    "SilencerGroupingReduce30": "глушитель заметно портит кучность",
    "SilencerGroupingReduce50": "глушитель сильно портит кучность",
    "IncreaseReloadAP": "перезарядка дороже",
    "ReduceReloadAP": "перезарядка быстрее",
    "MagazineHandlingDecrease": "магазин тяжелее в обращении",
    "MagazineHandlingIncrease": "магазин легче",
    "BarrelRangeIncrease": "дальше WeaponRange",
    "BarrelRangeReduce": "короче WeaponRange",
    "CloseRangeIncrease": "расширяет ближнюю неэффективную зону",
    "CloseRangeDecrease": "сужает ближнюю неэффективную зону",
    "CloseRangeFactorIncrease": "смягчает штраф в упор",
    "CloseRangeFactorDecrease": "усиливает штраф в упор",
    "BarrelBulletDropIncrease": "дальше BulletDropRange",
    "BarrelBulletDropReduce": "ближе «падает» траектория",
    "BarrelAccuracyIncrease": "лучше профиль ствола",
    "BarrelHandlingIncrease": "ствол удобнее (legacy)",
    "BarrelHandlingReduce": "ствол тяжелее (legacy)",
    "BarrelRecoilRecude": "меньше отдача от ствола",
    "IncreasedSingleShotAccuracy": "лучше одиночный (часто legacy)",
    "HalfRangeDmgIncrease": "больше урон на ½ дистанции (дробовик)",
    "IncreaseRange": "дальше",
    "ReduceRange": "ближе",
    "IncreaseBuckshotAngle": "шире конус дроби",
    "DecreaseBuckshotAngle": "уже конус дроби",
    "MarkWhenFullyAimed": "на полном aim помечает цель",
    "IncreaseCritChangeScaled": "выше шанс крита (scaled)",
    "LaserCTH": "плоский CTH лазера накоротке (legacy)",
    "ChangeWeaponTypeToAssaultRifle": "меняет класс оружия",
    "NightsIronsBonus": "ночные открытые прицелы (legacy)",
    "MinorAccuracyBonus": "мелкий плоский CTH (legacy)",
    "AccuracyBonusWhenAimed": "плоский CTH при aim (legacy)",
}


def load_csv(name):
    with (DATA / name).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_params(raw: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for chunk in (raw or "").split(";"):
        chunk = chunk.strip()
        if not chunk or "=" not in chunk:
            continue
        k, v = chunk.split("=", 1)
        v = v.strip()
        if v in ("", "<", ">"):
            continue
        out[k.strip()] = v
    return out


def _num(params: dict, *keys, default=None):
    for k in keys:
        if k in params:
            try:
                return int(params[k])
            except ValueError:
                try:
                    return float(params[k])
                except ValueError:
                    return params[k]
    return default


def _mag_text(params: dict) -> str:
    mag = _num(params, "ScopeMagnification")
    sub = _num(params, "ScopeSubMagnification")
    if mag is None:
        return ""
    if sub:
        return f"{mag}.{sub}×"
    return f"{mag}×"


def describe_effects(effect_ids: list[str], params: dict) -> str:
    """One human sentence-ish string: where which effect lands."""
    bits: list[str] = []
    used_fx: set[str] = set()

    def take(*eids: str) -> bool:
        hit = [e for e in eids if e in effect_ids]
        if not hit:
            return False
        used_fx.update(hit)
        return True

    def add(text: str):
        bits.append(text)

    p = params

    # Optics / aim economy
    if take("DecreaseMaxAimActions"):
        n = _num(p, "MaxAimActionsDecrease", default=1)
        add(f"на {n} меньше кликов aim до потолка")
    if take("IncreaseMaxAimActions"):
        n = _num(p, "IncreaseMaxAimActions", default=1)
        add(f"на {n} больше кликов aim до потолка")
    if take("MinAim"):
        m = _num(p, "min_aim", "ScopeAimLevel")
        add("нужен минимум aim" + (f" ({m})" if m is not None else ""))
    if take("ScopeMagnification"):
        mag = _mag_text(p)
        aim_lv = _num(p, "ScopeAimLevel")
        t = "сдвигает комфортную дистанцию"
        if mag:
            t += f" (~{mag})"
        if aim_lv is not None:
            t += f", оптика «включается» с {aim_lv}-го клика aim"
        add(t)
    if take("SmallMagnification"):
        add("есть вторая (меньшая) кратность / переключатель профиля")
    if take("IncreaseShotAP"):
        n = _num(p, "ShotAP", default=1)
        add(f"каждый выстрел дороже на {n} AP")
    if take("ReduceShootAP"):
        n = _num(p, "ShootAPDecrease", default=1)
        add(f"выстрел дешевле на {n} AP")

    # Overwatch
    if take("ExtraOverwatchShots"):
        n = _num(p, "extra_attacks", default=1)
        add(f"+{n} выстрел в overwatch" if n == 1 else f"+{n} выстрела в overwatch")
    if take("ScopeOverwatchAngleIncreaceBig", "ScopeOverwatchAngleIncreace"):
        n = _num(p, "OverwatchAngleIncrease")
        big = "ScopeOverwatchAngleIncreaceBig" in used_fx
        t = ("сильно шире" if big else "шире") + " сектор ожидания"
        if n is not None:
            t += f" (+{n})"
        add(t)
    elif take("IncreaseOverwatchAngle"):
        n = _num(p, "OverwatchAngleIncrease")
        t = "шире сектор ожидания"
        if n is not None:
            t += f" (+{n})"
        add(t)
    if take("ScopeOverwatchAngleDecreaseBig"):
        add("сильно уже сектор ожидания (длинная оптика)")
    elif take("ScopeOverwatchAngleDecrease"):
        add("уже сектор ожидания")

    if take("OpportunityAttackBonusCth"):
        add("лучше попадание в реакциях / перехвате")
    if take("CritBonusWhenFullyAimed"):
        add("больше крит, когда полностью прицелился")
    if take("MarkWhenFullyAimed"):
        add("на полном aim помечает цель")
    if take("IgnoreInTheDark"):
        add("не штрафует темнота")
    if take("IgnoreInTheDarkWhenFullyAimed"):
        add("в темноте нормально бьёшь только на полном aim")
    if take("ScopeHandlingReduce"):
        n = _num(p, "ScopeHandlingReduce")
        t = "штраф Handling (legacy, в CTH не идёт)"
        if n is not None:
            t += f" (−{n})"
        add(t)

    # Recoil / prone / grip
    if take("RecoilDecrease"):
        n = _num(p, "Recoil")
        add("легче держать очередь" + (f" (Recoil −{n})" if n is not None else ""))
    if take("RecoilIncrease"):
        n = _num(p, "Recoil")
        add("очередь размазывает сильнее" + (f" (Recoil +{n})" if n is not None else ""))
    if take("AccuracyBonusProne"):
        n = _num(p, "bonus_cth_bipod", "BonusCTH", "bonus_cth")
        add("лёжа лучше" + (f" (+{n} CTH legacy)" if n is not None else " (часто legacy flat)"))
    if take("ShotsBeforeRecoilProne"):
        add("лёжа больше пуль до сильной отдачи")
    if take("AccuracyBonusSameTarget"):
        add("повтор по той же цели чуть проще")
    if take("BipodsHandlingDecrease"):
        add("сошки делают профиль тяжелее")
    if take("GripHandlingIncrease"):
        add("рукоятка удобнее (legacy Handling)")
    if take("GLHandlingDecrease"):
        add("гранатомёт утяжеляет обращение")
    if take("GrenadeLauncher"):
        add("открывает подствольный гранатомёт")

    # Mag
    if take("MagazineSizeMultiplier"):
        m = _num(p, "MagazineSizeMultiplier")
        if isinstance(m, (int, float)):
            add(f"ёмкость ×{m / 100:.2f}".rstrip("0").rstrip("."))
        else:
            add("ёмкость × множитель")
    if take("MagazineSizeAdd", "MagazineSizeIncrease"):
        n = _num(p, "MagazineSize", "extra_shots")
        add(f"+{n} патронов в магазине" if n is not None else "больше патронов в магазине")
    if take("ReduceMagazineSize"):
        add("меньше патронов в магазине")
    if take("IncreaseReloadAP"):
        n = _num(p, "ReloadAPIncrease", default=1)
        add(f"перезарядка дороже на {n} AP")
    if take("ReduceReloadAP"):
        n = _num(p, "ReloadAPDecrease", default=1)
        add(f"перезарядка быстрее (−{n} AP)")
    if take("MagazineHandlingDecrease"):
        add("магазин тяжелее в обращении")
    if take("MagazineHandlingIncrease"):
        add("магазин легче в обращении")

    # Reliability / aim accuracy
    if take("ReduceReliability", "ReduceReliabilityPercent"):
        n = _num(p, "ReliabilityDecrease")
        add("хуже надёжность" + (f" (−{n})" if n is not None else "") + " / чаще клин")
    if take("IncreaseReliability"):
        n = _num(p, "ReliabilityIncrease")
        add("надёжнее" + (f" (+{n})" if n is not None else ""))
    if take("ReduceAimAccuracy15Percent"):
        add("чуть хуже AimAccuracy (−15%)")
    if take("ReduceAimAccuracy20Percent"):
        add("заметно хуже AimAccuracy (−20%)")
    if take("ReduceAimAccuracy50Percent"):
        add("сильно хуже AimAccuracy (−50%)")
    if take("ReduceAimAccuracy80Percent", "ReduceAimAccuracy90Percent"):
        add("почти ломает AimAccuracy")
    if take("ReduceAimAccuracy"):
        add("хуже AimAccuracy")
    if take("IncreaseAimAccuracy", "IncreaseAimAccuracy15Percent"):
        n = _num(p, "AimAccuracyIncrease")
        add("лучше AimAccuracy" + (f" (+{n})" if n is not None else ""))

    # Barrel
    if take("BarrelRangeIncrease", "IncreaseRange"):
        n = _num(p, "RangeIncrease")
        add("дальше WeaponRange" + (f" (+{n})" if n is not None else ""))
    if take("BarrelRangeReduce", "ReduceRange"):
        n = _num(p, "RangeDecrease", "RangeReduce")
        add("короче WeaponRange" + (f" (−{n})" if n is not None else ""))
    if take("CloseRangeIncrease"):
        n = _num(p, "CloseRangeIncrease")
        add("расширяет ближнюю неэффективную зону" + (f" (+{n} тайла)" if n is not None else ""))
    if take("CloseRangeDecrease"):
        n = _num(p, "CloseRangeDecrease")
        add("сужает ближнюю неэффективную зону" + (f" (−{n} тайла)" if n is not None else ""))
    if take("CloseRangeFactorIncrease"):
        n = _num(p, "CloseRangeFactorIncrease")
        add("смягчает штраф в упор" + (f" (+{n}%)" if n is not None else ""))
    if take("CloseRangeFactorDecrease"):
        n = _num(p, "CloseRangeFactorDecrease")
        add("усиливает штраф в упор" + (f" (−{n}%)" if n is not None else ""))
    if take("BarrelBulletDropIncrease"):
        n = _num(p, "BulletDropIncrease", "EffectiveRange")
        add("дальше комфорт дистанции (BulletDrop)" + (f" (+{n})" if n is not None else ""))
    if take("BarrelBulletDropReduce"):
        n = _num(p, "BulletDropReduce")
        add("ближе «падает» траектория" + (f" (−{n})" if n is not None else ""))
    if take("BarrelAccuracyIncrease"):
        n = _num(p, "AimAccuracyIncrease")
        add("лучше профиль ствола" + (f" (AimAccuracy +{n})" if n is not None else ""))
    if take("BarrelGroupingIncrease"):
        add("лучше кучность (Grouping)")
    if take("BarrelGroupingReduce"):
        add("чуть хуже кучность (Grouping)")
    if take("BarrelRecoilRecude"):
        n = _num(p, "BarrelRecoilRecude", "Recoil")
        add("меньше отдача от ствола" + (f" ({n})" if n is not None else ""))
    if take("BarrelRecoilIncrease"):
        add("ствол усиливает отдачу")
    if take("BarrelHandlingIncrease"):
        add("ствол удобнее (legacy)")
    if take("BarrelHandlingReduce"):
        add("ствол тяжелее (legacy)")
    if take("IncreasedSingleShotAccuracy"):
        add("лучше одиночный (часто legacy)")
    if take("HalfRangeDmgIncrease"):
        add("больше урон на половине дистанции (дробовик)")
    if take("IncreaseBuckshotAngle"):
        add("шире конус дроби")
    if take("DecreaseBuckshotAngle"):
        add("уже конус дроби")

    # Muzzle / stealth
    if take("SilentShots"):
        add("тихие выстрелы (меньше шум/детекция)")
    if take("StealthKillBonusPerAim"):
        add("бонус скрытного убийства за клики aim")
    for sil in (
        "SilencerGroupingReduce10",
        "SilencerGroupingReduce30",
        "SilencerGroupingReduce50",
        "SilencerHandlingReduce",
        "SilencerHandlingDecrease",
        "SilencerJamChance",
    ):
        if take(sil):
            add(EFFECT_GLOSS.get(sil, sil))

    # Stock / modes / misc
    if take("zzStockEquipped"):
        add("флаг складного приклада")
    if take("StockHandlingIncrease"):
        add("приклад легче (legacy)")
    if take("FreeWeaponSwap"):
        add("быстрая смена оружия без обычной цены")
    if take("EnableFullAuto"):
        add("включает автоматический огонь")
    if take("EnableBurst"):
        add("включает очередь")
    if take("ExtraBurstShots"):
        n = _num(p, "extra_shots")
        add("длиннее короткая очередь" + (f" (+{n})" if n is not None else ""))
    if take("ExtraAutoShots"):
        n = _num(p, "extra_shots")
        add("длиннее автоочередь" + (f" (+{n})" if n is not None else ""))
    if take("EnableRunNGun"):
        add("открывает маневренный бой (Run&Gun)")
    if take("ChangeCaliberToBMG"):
        add("меняет калибр на .50 BMG")
    if take("IncreaseDamage"):
        n = _num(p, "DamageIncrease", "Damage", "damage")
        add("больше базовый урон" + (f" (+{n})" if n is not None else ""))
    if take("ChangeWeaponTypeToAssaultRifle"):
        add("меняет класс оружия")
    if take("Cumbersome"):
        add("оружие громоздкое")
    if take("FirstShotIncreasedAim"):
        add("первая атака хода как будто уже с min_aim")
    if take("PointBlankBonus"):
        add("бонус на очень близкой дистанции")
    if take("LaserMark", "LaserCTH"):
        n = _num(p, "LaserCTH", "bonus_cth")
        d = _num(p, "LaserDistance")
        t = "лазер: плоский CTH накоротке (legacy)"
        if n is not None:
            t += f" (+{n}"
            if d is not None:
                t += f" до {d} тайлов"
            t += ")"
        add(t)
    if take("IncreaseCritChangeScaled"):
        add("выше шанс крита (scaled)")
    if take("MinorAccuracyBonus", "AccuracyBonusWhenAimed"):
        n = _num(p, "bonus_cth", "BonusCTH")
        add("мелкий плоский CTH (legacy)" + (f" +{n}" if n is not None else ""))
    if take("NightsIronsBonus"):
        add("ночные открытые прицелы (legacy)")
    if take("ReduceAuto75Percent"):
        add("сильно режет автоматический огонь")
    if take("ReduceBurst50Percent"):
        add("режет очередь")

    for eid in effect_ids:
        if eid in used_fx:
            continue
        add(EFFECT_GLOSS.get(eid, f"см. `{eid}`"))
        used_fx.add(eid)

    return "; ".join(bits) if bits else "—"


def gloss_effect(eid: str, meta: dict | None = None) -> str:
    if eid in EFFECT_GLOSS:
        return EFFECT_GLOSS[eid]
    meta = meta or {}
    desc = (meta.get("description") or "").replace("\n", " ").strip()
    desc = re.sub(r"<[^>]+>", "", desc)
    if desc:
        return desc
    return f"см. эффект `{eid}`"


def main():
    effects_meta = {r["effect_id"]: r for r in load_csv("weapon-component-effects.csv")}
    comps = {r["component_id"]: r for r in load_csv("weapon-components.csv")}
    weapons = {r["id"]: r for r in load_csv("weapons.csv")}
    active = {w for w, r in weapons.items() if r.get("catalog_status") == "active"}

    used = defaultdict(lambda: {"weapons": set(), "defaults": set(), "slot": ""})
    for o in load_csv("weapon-component-options.csv"):
        if o["weapon_id"] not in active:
            continue
        if (o.get("slot_type") or "").lower() == "mount":
            continue
        mod = (o.get("modifiable") or "").lower() == "true"
        is_def = (o.get("is_default") or "").lower() == "true"
        if not mod and not is_def:
            continue
        cid = (o.get("component_id") or "").strip()
        if not cid:
            continue
        used[cid]["weapons"].add(o["weapon_id"])
        used[cid]["slot"] = o.get("slot_type") or comps.get(cid, {}).get("slot") or "?"
        if is_def:
            used[cid]["defaults"].add(o["weapon_id"])

    effect_usage = Counter()
    by_slot = defaultdict(list)
    parsed_rows = []

    for cid, info in used.items():
        c = comps.get(cid, {})
        slot = info["slot"] or c.get("slot") or "?"
        fx = [e for e in (c.get("effects") or "").split(";") if e]
        params = parse_params(c.get("parameters") or "")
        for e in fx:
            effect_usage[e] += 1
        human = describe_effects(fx, params)
        empty = not fx and not params
        entry = {
            "id": cid,
            "name": c.get("display_name") or cid,
            "n": len(info["weapons"]),
            "ndef": len(info["defaults"]),
            "effects": fx,
            "params": params,
            "human": human,
            "empty": empty,
        }
        by_slot[slot].append(entry)
        parsed_rows.append(entry)

    for slot in by_slot:
        by_slot[slot].sort(key=lambda x: (-x["n"], x["id"]))

    lines: list[str] = []
    lines.append("# Аттачи — человеческое описание (эффекты словами)")
    lines.append("")
    lines.append(
        "Спарсено с **active**-оружия: компонент «на стволе», если слот можно модить "
        "или компонент стоит по умолчанию. Mount не учитывается."
    )
    lines.append("")
    lines.append(
        "Ниже по категориям: **зачем слот**, потом каждый живой обвес — "
        "**где какой эффект** обычными словами (числа из параметров данных)."
    )
    lines.append("")
    lines.append("## Словарь частых эффектов")
    lines.append("")
    lines.append("| Эффект в данных | Смысл |")
    lines.append("| --- | --- |")
    for eid, n in effect_usage.most_common(45):
        lines.append(f"| `{eid}` (×{n}) | {gloss_effect(eid, effects_meta.get(eid))} |")
    lines.append("")

    order = [
        "Scope",
        "Stock",
        "Barrel",
        "Under",
        "Handgrip",
        "Handguard",
        "Side",
        "Magazine",
        "Muzzle",
        "Bipod",
        "Freeswap",
        "Trigger",
        "Side2",
        "Grenadelauncher",
        "General",
        "Mountfront",
    ]
    for slot in order:
        if slot not in by_slot:
            continue
        items = by_slot[slot]
        lines.append(f"## {SLOT_TITLE.get(slot, slot)}")
        lines.append("")
        lines.append(SLOT_INTRO.get(slot, ""))
        lines.append("")
        lines.append(f"Живых вариантов: **{len(items)}**.")
        lines.append("")

        with_fx = [x for x in items if not x["empty"]]
        empty = [x for x in items if x["empty"]]

        if with_fx:
            lines.append("### Что реально меняет бой")
            lines.append("")
            lines.append("| Обвес | Стволов | Эффекты словами |")
            lines.append("| --- | ---: | --- |")
            for x in with_fx:
                name = (x["name"] or "").replace("|", "/")
                ncell = str(x["n"]) + (f" ({x['ndef']} def)" if x["ndef"] else "")
                lines.append(f"| `{x['id']}` — {name} | {ncell} | {x['human']} |")
            lines.append("")

        if empty:
            lines.append("### Без боевого эффекта (визуал / база / крепёж)")
            lines.append("")
            lines.append(", ".join(f"`{x['id']}` ({x['n']})" for x in empty) + ".")
            lines.append("")
            lines.append(
                "Не показывать игроку как апгрейд: дефолтный меш или пустая деталь."
            )
            lines.append("")

    lines.append("## Как читать выбор")
    lines.append("")
    lines.append("1. **Прицел** — где силён по дистанции и сколько платишь AP/кликами.")
    lines.append("2. **Ствол** — коротыш (CQB) или дальняя дистанция.")
    lines.append("3. **Приклад** — устойчивость или мобильность (в т.ч. сложить).")
    lines.append("4. **Рукоятка** — держать очередь или поставить гранатомёт.")
    lines.append("5. **Магазин** — запас патронов ценой reload/надёжности.")
    lines.append("6. **Дуло** — компенсатор (отдача) или глушитель (тишина).")
    lines.append("7. **Фонарь/лазер** — темнота и упор, не снайперка.")
    lines.append("8. **Сошки** — лёг и давлю, не бегаю.")
    lines.append("")
    lines.append(
        "Связано: `docs/tools/attachments-catalog.html`, "
        "`docs/technical/weapons/accuracy-model.md`. "
        "Пересбор: `python docs/tools/_write_attach_design_human.py`."
    )
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "effect_usage": effect_usage.most_common(),
                "components": parsed_rows,
                "gloss": EFFECT_GLOSS,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {OUT_MD} ({OUT_MD.stat().st_size} bytes)")
    print(f"effects unique={len(effect_usage)} comps={len(parsed_rows)}")


if __name__ == "__main__":
    main()
