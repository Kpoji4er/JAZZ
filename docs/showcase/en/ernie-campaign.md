# Ernie campaign

[Overview](home.md) · [Grand Chien map](grand-chien-map.md) · [Legion units](legion-units.md) · [Legion strategy](legion-strategy.md) · [Русский](../ru/ernie-campaign.md)

Source: `jazz-maps/items.lua` (sectors, quests, setpieces). Demo scope is Ernie Island; mainland data exists, full playthrough is not promised. Expanded grid and landmark remaps: [Grand Chien map](grand-chien-map.md).

## Start

| | |
| --- | --- |
| Campaign | `HotDiamonds` |
| InitialSector | **M1** — Landing Zone («Зона высадки») |
| Enter setpiece | `M1Landing` (map `EPA7FVN`) |
| Boot | reveal `M1`/`M2`/`M3` |

Cities: **Ernie** (`ErnieVillage`), rebel base (`Rebels_Ernie`), smugglers (`SmugglersErnie`).

On large landing fights (**M1**), allied rebel turns are shortened: less position/cover deliberation and faster playback of their actions when auto Fast Forward is on.

## Ernie sectors (from code)

Filter: `WeatherZone=Erny` **or** city `ErnieVillage`/`Rebels_Ernie` **or** `Label1=Ernie` → **20** sectors (not the older catalog’s “23”).

| Id | Data name | Note |
| --- | --- | --- |
| M1 | Landing Zone | Start |
| M2 | Rocky shore | |
| M4 | The Outlook | Label Ernie |
| M5 | Coastline | |
| M6 | Old port | |
| I2 | Lighthouse clinic | City ErnieVillage |
| I5 | Village of Ernie | Hub |
| I6 | The Rust | Label Ernie |
| I6_Underground | Bunker FB45-68 | Label Ernie |
| I7 | Fort L'Eau Bleu | Outpost / Global AI |
| J5 | Ernie farms | |
| J7 | Emerald Coast | Herman |
| K4 | Flag Hill | |
| K5 | Legion camp | |
| K6 | Smuggler fallback camp | |
| L1 | Partisan base | City Rebels_Ernie |
| L2 | Impassable terrain | Rebels_Ernie |
| L5 | Legion camp | |
| L6 | Abandoned bunker entrance | Rebels_Ernie |
| L7 | Fishing village | |

On the island but **without** Ernie tags in ModItemSector: `K2` (Old Relay Tower), `I3`/`I4` (road to lighthouse), `M3` (waterfall), `K3`/`L3`/`L4` (villa quest), `I7_Underground`, `L6_Underground`.

## Quests (from items.lua)

### QuestGroup “Ernie Island”

| Id | DisplayName | Hidden |
| --- | --- | --- |
| `TakeTheFortress` | Fort L'Eau Bleu | no |
| `RescueHerMan` | Herman is missing | no |
| `FortifyErnie` | Helping Ernie Village | no |
| `ReduceFortressStrength` | How to reduce the Fort's defenses | yes |
| `LegionFlag` | Fooling Pierre | yes |
| `Ernie_CounterAttack` | *(unnamed)* | yes |

After liberating the village while the fort is still enemy — a **quest** sat attack from the fort on the village (~16 h). On maps: `ErnieCounterAttack` ~**30** (RPG + 2 T1 thrower grenadiers + mortar). On **Vanilla Maps (NoMaps):** `ErnieCounterAttack_NoMaps` ~**20**, **no mortar**. Not the generic Legion “Retaliation” AI recipe. Ordinary vanilla periodic sorties from the managed fort stay off.
| `ErnieSideQuests` | *(unnamed)* | yes |
| `ErnieSideQuests_WorldFlip` | *(unnamed)* | yes |
| `RescueTeam` | We didn't sign up to be rescuers | no |
| `RebelsSavior` | Supplies for the Rebels | no |

### Intro / liberation

| Id | DisplayName |
| --- | --- |
| `01_Landing` | Meet the employer (RU) |
| `02_LiberateErnie` | Retake Ernie Village |
| `02A_LiberateErnie_2` | Liberate Ernie Island (RU) |
| `PierreDefeated` | Pierre |
| `JoseFamily` | Bastien |

### Ernie_Rebels / local JAZZ

| Id | DisplayName |
| --- | --- |
| `JAZZ_REBELS_0_MeetTheRebels` | The rebels (RU) |
| `JAZZ_REBELS_1_SeizeTheOutlook` | Attack the Outlook (RU) |
| `Jazz_Doctor_need_Help` | Unwanted doctor (RU) |
| `JAZZ_Ernie_Locals_M2_SaveMyFamily` | Save Kiki (RU) |
| `Jazz_ClearTheWay` | Clear camps around the villa (RU) |
| `Jazz_DeadPigs` | Pig-sticker |
| `Jazz_Alkatraz` | Clear the Bunker |

## Repaired quest chains

- At K5 the rebels accept only the full shipment: **4 Zastava M76 rifles + 4 Medkits**. Once delivered, pilot-smuggler Berriman Seal appears by the tents and can join for free.
- The prisoner rescue on the pier succeeds only if the hostage survives; report back to the sergeant afterward.
- The doctor's quest requires stabilizing **three** wounded rebels independently.
- Accepting “Pig-sticker” brings **four** of Balumba's allies into the K6 fight.
- Rebel helpers at K4 and M4 no longer disappear because of a wrong sector condition.
- Herman's trail leads to **J7**; the bunker-clearance job runs through **L6 Underground** and returns to L1.

## Setpieces

Registered in maps: **`M1Landing`**, **`EncounterHerman`**. Ernie flow also plays (often vanilla IDs): `PierreLucTalk`, `ErnieReturn_FirstEnter`, `FortressBasement_FirstEnter`, `PierreDies` / `PierreRetreat`, `HangingLuc`, `BastienDies`.
