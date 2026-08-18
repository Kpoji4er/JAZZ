# Legion units

[Overview](home.md) · [Legion strategy](legion-strategy.md) · [Ernie campaign](ernie-campaign.md) · [Русский](../ru/legion-units.md)

Source: `jazz-units/UnitData/JAZZ_Legion_*.lua`, quest `JAZZ_LegionTier` / `Code/UtilityFunc.lua`, composition/prices in `jazz/Code/Legion*.lua`. Cross-checked with technical `legion-units-equipment-tiers.md`.

## Two axes

1. **Class T1–T4** — fixed UnitData (stats, role, AI, root preset). Living units do **not** morph mid-fight.
2. **Campaign gear tier** `JAZZ_Legion_Tier` — loot pool for `CreateStartingEquipment`; rises by campaign time / mainland occupation / mines (see Gear tier); regenerates on satellite open.

Satellite squad roles: [Legion strategy](legion-strategy.md).

On the satellite squad stack, Legion unit portraits are **schematic red badges** (not faces): family mark at the top of the shield, role silhouette below it, and class-tier dots T1–T4 under the shield. Commanders show rank insignia instead of weapons. Do not confuse them with **squad role** icons (filled shields on the map).

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

The Skirmisher uses battle rifles with rifle modification packages and Match ammunition, not the old SMG flanker branch.

### Gunner (`Legion_Machinegunner`)

| T | Id | Name | Lvl |
| --- | --- | --- | ---: |
| 1 | GunnerT1_Gunner | Пуляло | 3 |
| 2 | GunnerT2_GMPG | Пулемётчик | 6 |
| 2 | GunnerT2_AssaultGunner | Коммандо | 8 |
| 3 | GunnerT3_VeteranGunner | Подавитель | 14 |
| 4 | GunnerT4_MercGunner | Наемник Пулеметчик | 16 |

The Commando deploys with a machine gun plus a guaranteed Machete and Molotov; the machete is equipped in the second hand slot.

### Leaders

| T | Id | Name | Lvl |
| --- | --- | --- | ---: |
| 1 | LeaderT1_Sergeant | Бригадир | 3 |
| 2 | LeaderT2_Lieutenant | Командир | 7 |
| 3 | LeaderT3_Captain | Советник | 6 |
| 4 | LeaderT4_MercenaryCaptain | Мастер | 8 |

Leader levels are **not** monotonic (as loaded). Strategic T4 squads need MercenaryCaptain; officer density Sergeant/8, Lieutenant/15–20, Captain/30 (`LegionSquadComposition.lua`).

In combat, leaders issue a **command aura** and orders to allies in range — see [Command aura](officer-aura.md).

### Artillery

| T | Id | Name | Lvl |
| --- | --- | --- | ---: |
| 1 | HeavyT1_Rocketeer | Ракетчик | 5 |
| 2 | HeavyT2_Grenadier | Гранатомётчик | 8 |
| 3 | HeavyT3_Mortarman | Миномётчик | 8 |

## Gear tier

Quest var starts at **11**.

**Ernie / maps package:** time and campaign beats (not sector count):

| Step | Trigger | Tier |
| --- | --- | ---: |
| T1 sub | every **~7** campaign days | `11` → `12` → `13` (~2 weeks to T1 cap) |
| T2-1 | **occupy** first mainland (non-Ernie) surface sector | `21` |
| T2/T3 sub | every **~30** days after entering that major | `22`…`25` / `32`…`33` |
| T3-1 | **5** player-owned mines | `31` |

Stay on the island without taking mainland land → cap **`13`**. Hiring mercs or traveling through a sector without changing ownership does **not** unlock T2. Tier only rises.

**Mainland with JAZZ Vanilla Maps (no jazz-maps):** tier **II** **3 days** after your first captured mine; tier **III** after **World Flip**. Subtiers: every **3 days** on I, every **two weeks** on II and III. Tier only rises. While tier is still **I**, map spawns use **class T1 only** (`LegionJAZZSquadT1_Early`); heavier classes unlock with major II/III.

Regen: flag → open satellite → rebuild starting equipment for **Legion only**.

The **carbine** (`M2Carbine`) drops from day one: wood stock on Wardens and Bonemakers; no stock as an SMG on Roughnecks/Grenadiers. Select-fire (M2) is rarer, from T1-2. Carbine roles sometimes roll a compact assault rifle with a folded/light stock (low chance).

**Veteran** and **Mercenary** have a small chance of a secondary launcher (M79 / disposable **M72 LAW** / late China Lake). **Rocketeer** launchers roll RPG-7 or M72 LAW.

Combat Legion squads (patrol, garrison, recon, QRF, etc.) field roughly **one Bonemaker (medic) per 10–20 fighters** (at least one once the squad is 10+). He carries a Small Medkit (stack 5), rarely a Medium (5%), bandages **1–10**, morphine **0–3**, and **50 Meds**. **T2** troopers may drop bandages **1–2**; **T3** may drop morphine ×1 at **~30%**. **First Blood** fields slightly more medics; **Commando** uses the usual density; **Mission Impossible** slightly fewer — they are the main enemy source of medical supplies. On **Mission Impossible** the per-class copy limit is off (sniper and MG caps stay).

## Strategic prices

`LegionUnitPrices.lua`: line **500/1000/2000/3500**, specialist **800/1500/2800/4500**, leader **800/1500/2500/4000** (T1→T4).
