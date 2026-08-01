# Workshop Otherguy AIM — sheet targets applied

Source: [Google Sheet gid=1773591798](https://docs.google.com/spreadsheets/d/19Je4n5Ju4cYmTLimzw45aFq_Ll8Wxz21RLIETFRsH2g/edit?gid=1773591798#gid=1773591798)

Parser: `docs/tools/_apply_workshop_aim_sheet.py` (applies **right-hand** of `current->target` arrows).

## Merc_JerrySinclair

| Stat | Value |
| --- | ---: |
| Health | 54 |
| Agility | 45 |
| Dexterity | 68 |
| Strength | 85 |
| Wisdom | 76 |
| Leadership | 40 |
| Marksmanship | 67 |
| Mechanical | 84 |
| Explosives | 50 |
| Medical | 8 |

- Specialization: `Mechanic`
- StartingLevel: `1` (field omitted when 1)
- StartingPerks: `Merc_JerrySinclair_Perk`, `MrFixit`, `Claustrophobic`, `Optimist`
- Gear presets 60/30/10:
  - 60%: ColtPeacemaker×1, JAZZ_AMMO_357_FMJ×6, Parts×50, FineSteelPipe×1, OpticalLens×1
  - 30%: Parts×100, FineSteelPipe×2, OpticalLens×4
  - 10%: Parts×100, OpticalLens×2, Microchip×2
- Perk gap: Sheet personal perk: repair items to 120% + buff +1 dmg/range/accuracy while >100% condition. Runtime still crafts 40mm-TB every 7 days (Merc_JerrySinclair_Perk).

## Merc_MildredPatterson

| Stat | Value |
| --- | ---: |
| Health | 51 |
| Agility | 48 |
| Dexterity | 74 |
| Strength | 38 |
| Wisdom | 78 |
| Leadership | 50 |
| Marksmanship | 55 |
| Mechanical | 5 |
| Explosives | 2 |
| Medical | 90 |

- Specialization: `Doctor`
- StartingLevel: `1` (field omitted when 1)
- StartingPerks: `Merc_MildredPatterson_Bookworm`, `Teacher`, `OldDog`, `Optimist`
- Gear presets 60/30/10:
  - 60%: HiPower×1, JAZZ_AMMO_9x19_FMJ×13, FirstAidKit×1, loot:Merc_MildredPatterson_SkillMag
  - 30%: FirstAidKit×1, loot:Merc_MildredPatterson_SkillMag
  - 10%: Medkit×1, loot:Merc_MildredPatterson_SkillMag
- Note: Sheet «Аптечка»→FirstAidKit; «Большая аптечка»→Medkit.

## Merc_SamuelNkosi

| Stat | Value |
| --- | ---: |
| Health | 89 |
| Agility | 78 |
| Dexterity | 62 |
| Strength | 86 |
| Wisdom | 74 |
| Leadership | 14 |
| Marksmanship | 76 |
| Mechanical | 18 |
| Explosives | 21 |
| Medical | 13 |

- Specialization: `HeavyWeapons`
- StartingLevel: `1` (field omitted when 1)
- StartingPerks: `Merc_SamuelNkosi_Perk`, `HeavyWeaponsTraining`, `AutoWeapons`
- Gear presets 60/30/10:
  - 60%: Galil×1, JAZZ_AMMO_762x51_FMJ×120
  - 30%: HiPower×1, JAZZ_AMMO_9x19_FMJ×65
  - 10%: Sterling×1, JAZZ_AMMO_9x19_FMJ×90
- Perk gap: Sheet personal perk: heavy MGs not bulky for Samuel. Runtime perk still uses prior OnKill/overwatch-style workshop behavior — verify Merc_SamuelNkosi_Perk vs sheet.

## Merc_AnnieDubois

| Stat | Value |
| --- | ---: |
| Health | 81 |
| Agility | 74 |
| Dexterity | 86 |
| Strength | 53 |
| Wisdom | 79 |
| Leadership | 16 |
| Marksmanship | 82 |
| Mechanical | 5 |
| Explosives | 4 |
| Medical | 39 |

- Specialization: `Marksmen`
- StartingLevel: `1` (field omitted when 1)
- StartingPerks: `Merc_AnnieDubois_Perk`, `NightOps`, `Deadeye`
- Gear presets 60/30/10:
  - 60%: M21+JAZZ_Scope_6x, JAZZ_AMMO_762x51_FMJ×40
  - 30%: HiPower×1, JAZZ_AMMO_9x19_FMJ×26
  - 10%: M21+JAZZ_Reflex_Closed, JAZZ_AMMO_762x51_FMJ×20
- Perk gap: Sheet personal perk: 2 sniper headshots (replacing Inspired-on-kill). Runtime Merc_AnnieDubois_Perk still grants Inspired on kill.
- Note: Sheet note «L43 would suit her» left for owner (not applied).
- Note: Ammo counts not on sheet — used 40 / 26 / 20 FMJ as reasonable starters.

## Merc_HectorSanchez

| Stat | Value |
| --- | ---: |
| Health | 75 |
| Agility | 68 |
| Dexterity | 70 |
| Strength | 83 |
| Wisdom | 62 |
| Leadership | 70 |
| Marksmanship | 74 |
| Mechanical | 14 |
| Explosives | 28 |
| Medical | 5 |

- Specialization: `Leader`
- StartingLevel: `1` (field omitted when 1)
- StartingPerks: `Merc_HectorSanchez_Perk`, `Teacher`, `Psycho`
- Gear presets 60/30/10:
  - 60%: PPSH+JAZZ_MagDrum_35_71, JAZZ_AMMO_762x25_FMJ×142
  - 30%: Type56×1, JAZZ_AMMO_762x39_FMJ×60
  - 10%: M21+JAZZ_Reflex_Closed, JAZZ_AMMO_762x51_FMJ×20
- Perk gap: Sheet personal perk: 10%*level chance to train militia +2 tiers. Runtime Merc_HectorSanchez_Perk may still use older militia-efficiency workshop wording — verify behavior.
- Note: Ammo counts not fully on sheet for Type56/M21 — used 60 / 20 FMJ.

## Merc_CarolThompson

| Stat | Value |
| --- | ---: |
| Health | 76 |
| Agility | 82 |
| Dexterity | 70 |
| Strength | 61 |
| Wisdom | 83 |
| Leadership | 12 |
| Marksmanship | 76 |
| Mechanical | 89 |
| Explosives | 25 |
| Medical | 13 |

- Specialization: `Mechanic`
- StartingLevel: `1` (field omitted when 1)
- Tier: `Rookie`
- StartingPerks: `Merc_CarolThompson_Perk`, `AutoWeapons`, `MrFixit`, `Flanker`, `RelentlessAdvance`
- Gear presets 60/30/10:
  - 60%: Sterling×1, JAZZ_AMMO_9x19_FMJ×90, Merc_CarolThompson_Item×1
  - 30%: Winchester1894×1, JAZZ_AMMO_44CAL_FMJ×28, Merc_CarolThompson_Item×1
  - 10%: HiPower×1, JAZZ_AMMO_9x19_FMJ×26, Merc_CarolThompson_Item×1
- Perk gap: Sheet personal perk: chance to bring Parts/pipes/lens/chip on ops; toolbox lockpick. Runtime Merc_CarolThompson_Perk still auto-repairs equipped gear hourly — verify vs sheet scrap-find rates.
- Note: Dropped FlakVest from prior loot (not on sheet presets).
- Note: Ammo for Winchester/HiPower not on sheet — used 28 / 26.
- Note: Tier Veteran→Rookie with level 1.
