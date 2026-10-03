# Legion units

Legion SMG/carbine pools include the Mosin Obrez from T1-1, with lower weight at T2. The M38 joins battle rifles alongside the MAS-36 at T1-1 with a low selection weight, increasing roughly fivefold at T1-2. The long Mosin, including its PU configuration, enters sniper-role pools at T1-3. Tables have passed static checks; in-game distribution still awaits verification.

The October 2 6B3 revision adds a new model with front and rear sections, pouches and side straps. Shoulder straps now follow the torso without arm influence. Its fit still awaits in-game verification.

[Overview](home.md) · [Tactical AI](tactical-ai.md) · [Legion strategy](legion-strategy.md) · [Ernie campaign](ernie-campaign.md) · [Русский](../ru/legion-units.md)

Source: `jazz-units/UnitData/JAZZ_Legion_*.lua`, quest `JAZZ_LegionTier` / `Code/UtilityFunc.lua`, composition/prices in `jazz/Code/Legion*.lua`. Cross-checked with technical `legion-units-equipment-tiers.md`.

## Starting world tier and progression

New-game rules offer **Starting world tier** (T1-1 through T3-3) and **Tier progression**. Click a row to cycle its value. Defaults are T1-1 and Campaign. The starting tier immediately controls Legion equipment and existing tier-linked strategy, including region activation and squad growth. Skipped tiers do not dispatch retroactive convoys. Quests, mines, money and mercenary equipment are not granted automatically.

**Campaign** retains the mainland, mine and story conditions described below. With a higher starting tier, the next sub-tier interval begins at the selected tier. **Timed x1/x2/x4** advance through the entire ladder `T1-1 → T1-2 → T1-3 → T2-1 → … → T2-5 → T3-1 → T3-2 → T3-3` independently of captures and story events. At x1, an outgoing T1 step takes 7 days with JAZZ Maps or 3 days without maps; a T2/T3 step takes 30 or 14 days respectively. This also covers T1-3→T2-1 and T2-5→T3-1. x2/x4 divide these intervals by 2/4. Progression stops at T3-3.

These choices belong to the new campaign and persist in saves. Existing campaigns keep their original progression. The host controls both choices in multiplayer lobbies.

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

## Experimental armor visuals

The September 26 trial rebuild gives chainmail separate plates on leather straps, the brigantine broad tire bands, and heavy tire armor large tread sections and forearm guards. Buckles, rivets, and side lacing add construction detail. The cuirass is preserved. These models still await in-game and visual acceptance; strap fit during extreme bends is not final.

The local experimental build includes the improvised cuirass, chainmail, brigantine, tire armor, and nine Twaron, Guardian, and Zylon torso variants, plus vanilla stand-ins for Flak / Interceptor vests and the mapped helmets. Light, Medium, and Full differ by protective components; test fighters use MP40s and remain outside campaign squads. Only JAZZ Legion males show these visuals. The modern custom vests were reshaped around the test Legion fighter's shirt to reduce excessive rear clearance. Clothing fit and animations still require in-game validation.

The Soviet helmet on male JAZZ Legion fighters uses a dedicated SSh-68 model, also equipped by the 6B3 test fighter. The item retains its SSh-40 name; the new model still needs an in-game fit check.

Leather armor now has its own improvised plate carrier with riveted shoulder straps, side belts and worn leather texture. It appears on male JAZZ Legion fighters without changing the item's protection. The model is installed in the local experimental build; in-game fit and animation acceptance are still pending.

The improvised brigandine, tire armor and leather vest have new models. Chainmail replaces the upper-body garment and includes the torso beneath its neckline; upper shoulder plates follow the torso while sleeves blend toward the arms. Its original icon is restored. Installed for in-game testing; final animation acceptance remains open.
