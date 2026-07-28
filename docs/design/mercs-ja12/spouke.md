---
status: ready
priority: high
origin: jazz
unit_id: JAZZ_Merc_Spouke
portrait_id: Spouke
affiliation: AIM
role: Demolitions
tier: Veteran
specialization: ExplosiveExpert
gender: Male
nationality: USA
voice_source: new
starting_level: 4
will: 70
salary:
  starting: 2000
  increase: 210
  lv1: 750
  max: 5000
medical_deposit: standard
haggling: normal
executable: true
---

# Фраг — Эрни Споук «Фраг»

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Эрни Споук «Фраг» | Ernie Spouke "Frag" |
| Nick | Фраг | Frag |
| AllCapsNick | ФРАГ | FRAG |
| Title | Жизни Саперов Важны | Sapper Lives Matter |
| Email | CHPOK!@aim.com | CHPOK!@aim.com |
| snype_nick | letsgoboom | letsgoboom |

## Bio

**RU:** as-shipped `JAZZ_Merc_Spouke.lua` — портовый пацан, морпех-сапёр, ранение, AIM за деньгами.

**EN:** CSV.

## Stats

| Stat | Value |
| --- | --- |
| Health | 93 |
| Agility | 81 |
| Dexterity | 80 |
| Strength | 94 |
| Wisdom | 79 |
| Will | (default) |
| Leadership | 20 |
| Marksmanship | 80 |
| Mechanical | 15 |
| Explosives | 93 |
| Medical | 27 |
| MaxHitPoints | (default) |
| StartingLevel | 4 |

## Perks

### StartingPerks

- `Jazz_Perk_00`
- `BreachAndClear`
- `Throwing`
- `HitTheDeck`
- `HeavyWeaponsTraining`
- `BreachAndClear` (duplicate in UnitData as-shipped)

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_00` |
| type | passive (timer interaction) |
| DisplayName RU/EN | 00:00 |
| Description RU/EN | При активации взрывчатка с таймером, кинутая Споуком, взорвётся в начале вражеского хода. |
| Mechanics | As-shipped; clears effect value OnCombatEnd |

## Personality

- Likes: Ice, Len, Spike
- Mitigations when those hired; ExtraPartingWords recommends Ice

## Hire

- Access: AIM
- DaysUntilOnline: 0

## Inventory

- `Loot_JAZZ_Sapper` → `JAZZ_Sapper50/35/25/20`
- *50: `JazzArmor_PoliceVest`, `R870`, `JAZZ_AMMO_12gauge_Buckshot`×20, `FragGrenade`×2, `ConcussiveGrenade`

## JA2 face reference

Нет файла в архиве `портировать.rar` для этого мерка. Перед генерацией портрета добавить `spouke.ja2-face.*` или явно согласовать face ref.

## Portrait prompt

**CHARACTER_DESCRIPTION:** African-American male sapper, athletic, street-to-marine vibe, demo satchel and detonator clacker on chest, EOD patch — NO shotgun in hands. Confident grin.

**Class kit:** demo satchel, detonator, EOD patch, frag pouches  
**Refs:** existing `Spouke.png` / `Spouke_Big.png`

## Phrases — AIM chat

As-shipped UnitData (Offline, Greeting «Отдел по борьбе с минной опасностью…», Idle «Тик-так…», Parting, Rehire, Mitigations).

## Phrases — VoiceResponse

As-shipped `JAZZ_Merc_Spouke`; FallbackMissingVR = Grizzly.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | JAZZ_Spouke |
| VoiceResponseId | JAZZ_Merc_Spouke |
| FallbackMissingVR | Grizzly |
| Portrait | Mod/Dv3mFVN/MercPortraits/Spouke.png |
| Equipment | Loot_JAZZ_Sapper |
| Sources | `JAZZ_Merc_Spouke.lua`, `Loot_JAZZ_Sapper` |

## Open blockers

- none
