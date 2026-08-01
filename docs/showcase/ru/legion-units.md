# Юниты Легиона

[К обзору](home.md) · [Легион на стратегии](legion-strategy.md) · [Кампания на Эрни](ernie-campaign.md) · [English](../en/legion-units.md)

Источник: `jazz-units/UnitData/JAZZ_Legion_*.lua`, quest `JAZZ_LegionTier` / `Code/UtilityFunc.lua`, composition/prices в `jazz/Code/Legion*.lua`.

## Две оси

1. **Класс T1–T4** — фиксированный UnitData (stats, роль, AI, корневой пресет). Живой юнит **не морфится** в следующий класс.
2. **Campaign gear tier** `JAZZ_Legion_Tier` — пул лута при `CreateStartingEquipment`; растёт с числом ваших секторов; реген при открытии satellite.

Стратегические роли отрядов: [Легион на стратегии](legion-strategy.md).

## Каталог: 38 UnitData

37 боевых + `JAZZ_Legion_Recruit`. DisplayName из UnitData:

### Штурм (`Legion_Assaulter`)

| T | Id | Имя | Lvl |
| --- | --- | --- | ---: |
| 1 | AssaultT1_Roughneck | Головорез | 2 |
| 1 | AssaultT1_Grenadier | Гренадёр | 3 |
| 1 | AssaultT1_Crusher | Громила | 4 |
| 2 | AssaultT2_Pillager | Грабитель | 5 |
| 2 | AssaultT2_ShockTrooper | Штурмовик | 6 |
| 2 | AssaultT2_Pyro | Пироман | 7 |
| 3 | AssaultT3_Punisher | Каратель | 10 |
| 3 | AssaultT3_SkullCrusher | Череполом | 12 |
| 4 | AssaultT4_Headsman | Палач | 15 |

### Front / стрелки (`Legion_Frontliner`)

| T | Id | Имя | Lvl |
| --- | --- | --- | ---: |
| 1 | FrontT1_Rifleman | Стрелок | 4 |
| 1 | FrontT1_Bonemaker | Костоправ | 5 |
| 1 | FrontT1_Marauder | Мародёр | 5 |
| 2 | FrontT2_Ambusher | Засадник | 8 |
| 2 | FrontT2_Raider | Налётчик | 8 |
| 2 | FrontT2_Marksman | Охотник | 10 |
| 3 | FrontT3_Sniper | Снайпер | 12 |
| 3 | FrontT3_Veteran | Ветеран | 12 |
| 4 | FrontT4_Mercenary | Наемник | 15 |
| 4 | FrontT4_MercenarySniper | Наемник снайпер | 15 |

### Фланкеры (`Legion_Flanker`)

| T | Id | Имя | Lvl |
| --- | --- | --- | ---: |
| 1 | FlankerT1_Warden | Дозорный | 3 |
| 2 | FlankerT2_Scout | Скаут | 6 |
| 2 | FlankerT2_Skirmisher | Застрельщик | 6 |
| 3 | FlankerT3_Recon | Разведчик | 10 |
| 3 | FlankerT3_Pathfinder | Следопыт | 10 |
| 4 | FlankerT4_Ranger | Рейнджер | 18 |

### Пулемёты (`Legion_Machinegunner`)

| T | Id | Имя | Lvl |
| --- | --- | --- | ---: |
| 1 | GunnerT1_Gunner | Пуляло | 3 |
| 2 | GunnerT2_GMPG | Пулемётчик | 6 |
| 2 | GunnerT2_AssaultGunner | Коммандо | 8 |
| 3 | GunnerT3_VeteranGunner | Подавитель | 14 |
| 4 | GunnerT4_MercGunner | Наемник Пулеметчик | 16 |

### Командиры

| T | Id | Имя | Lvl |
| --- | --- | --- | ---: |
| 1 | LeaderT1_Sergeant | Бригадир | 3 |
| 2 | LeaderT2_Lieutenant | Командир | 7 |
| 3 | LeaderT3_Captain | Советник | 6 |
| 4 | LeaderT4_MercenaryCaptain | Мастер | 8 |

Уровни командиров **не** монотонны (как в загруженном UnitData). T4-отряды на стратегии требуют MercenaryCaptain; плотность офицеров: Sergeant/8, Lieutenant/15–20, Captain/30 (`LegionSquadComposition.lua`).

### Артиллерия

| T | Id | Имя | Lvl |
| --- | --- | --- | ---: |
| 1 | HeavyT1_Rocketeer | Ракетчик | 5 |
| 2 | HeavyT2_Grenadier | Гранатомётчик | 8 |
| 3 | HeavyT3_Mortarman | Миномётчик | 8 |

## Gear tier

Quest var стартует с **11**.

**Остров Эрни (с maps):** по числу ваших секторов (TCE в `JAZZ_LegionTier`):

| Секторов | Tier |
| ---: | ---: |
| 0–1 | 11 |
| 2 | 12 |
| 3 | 13 |
| 4…8 | 21…25 |
| 9+ | 31…33 |

**Материк с JAZZ Vanilla Maps (без jazz-maps):** тир **II** через **3 дня** после первой захваченной шахты; тир **III** после **World Flip**. Подтиры: на I — каждые **3 дня**, на II и III — каждые **две недели**. Тир только растёт.

Реген: флаг → открытие satellite → пересборка starting equipment **только у Легиона**.

## Цены стратегии

`LegionUnitPrices.lua`: линия **500/1000/2000/3500**, специалист **800/1500/2800/4500**, лидер **800/1500/2500/4000** (T1→T4).
