# Legion units

[Overview](home.md) · [Legion strategy](legion-strategy.md) · [Ernie campaign](ernie-campaign.md) · [Русский](../ru/legion-units.md)

Source: `jazz-units/UnitData/JAZZ_Legion_*.lua`, quest `JAZZ_LegionTier` / `Code/UtilityFunc.lua`, composition/prices in `jazz/Code/Legion*.lua`. Cross-checked with technical `legion-units-equipment-tiers.md`.

## Two axes

1. **Class T1–T4** — fixed UnitData (stats, role, AI, root preset). Living units do **not** morph mid-fight.
2. **Campaign gear tier** `JAZZ_Legion_Tier` — loot pool for `CreateStartingEquipment`; rises with your sector count; regenerates on satellite open.

Satellite squad roles: [Legion strategy](legion-strategy.md).

## Catalog: 38 UnitData

37 combat + `JAZZ_Legion_Recruit`. Display names from UnitData:

### Assault (`Legion_Assaulter`)

| T | Id | Name | Lvl |
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

### Front (`Legion_Frontliner`)

| T | Id | Name | Lvl |
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

### Flanker (`Legion_Flanker`)

| T | Id | Name | Lvl |
| --- | --- | --- | ---: |
| 1 | FlankerT1_Warden | Дозорный | 3 |
| 2 | FlankerT2_Scout | Скаут | 6 |
| 2 | FlankerT2_Skirmisher | Застрельщик | 6 |
| 3 | FlankerT3_Recon | Разведчик | 10 |
| 3 | FlankerT3_Pathfinder | Следопыт | 10 |
| 4 | FlankerT4_Ranger | Рейнджер | 18 |

### Gunner (`Legion_Machinegunner`)

| T | Id | Name | Lvl |
| --- | --- | --- | ---: |
| 1 | GunnerT1_Gunner | Пуляло | 3 |
| 2 | GunnerT2_GMPG | Пулемётчик | 6 |
| 2 | GunnerT2_AssaultGunner | Коммандо | 8 |
| 3 | GunnerT3_VeteranGunner | Подавитель | 14 |
| 4 | GunnerT4_MercGunner | Наемник Пулеметчик | 16 |

### Leaders

| T | Id | Name | Lvl |
| --- | --- | --- | ---: |
| 1 | LeaderT1_Sergeant | Бригадир | 3 |
| 2 | LeaderT2_Lieutenant | Командир | 7 |
| 3 | LeaderT3_Captain | Советник | 6 |
| 4 | LeaderT4_MercenaryCaptain | Мастер | 8 |

Leader levels are **not** monotonic (as loaded). Strategic T4 squads need MercenaryCaptain; officer density Sergeant/8, Lieutenant/15–20, Captain/30 (`LegionSquadComposition.lua`).

### Artillery

| T | Id | Name | Lvl |
| --- | --- | --- | ---: |
| 1 | HeavyT1_Rocketeer | Ракетчик | 5 |
| 2 | HeavyT2_Grenadier | Гранатомётчик | 8 |
| 3 | HeavyT3_Mortarman | Миномётчик | 8 |

## Gear tier

Quest var starts at **11**. From `PlayerControlSectors` (TCE in `JAZZ_LegionTier`):

| Sectors | Tier |
| ---: | ---: |
| 0–1 | 11 |
| 2 | 12 |
| 3 | 13 |
| 4…8 | 21…25 |
| 9+ | 31…33 |

Regen: flag → `OnMsg.OpenSatelliteView` → rebuild starting equipment (`UtilityFunc.lua`). Hundreds of LootDef conditions on `JAZZ_Legion_Tier`.

## Strategic prices

`LegionUnitPrices.lua`: line **500/1000/2000/3500**, specialist **800/1500/2800/4500**, leader **800/1500/2500/4000** (T1→T4).
