---
status: ready
priority: high
origin: ja2
unit_id: Jazz_Buzz
portrait_id: Buzz
affiliation: AIM
role: Autorifleman
tier: Elite
specialization: Autoriflemen
gender: Female
nationality: USA
voice_source: ja2
starting_level: 4
will: 49
salary:
  starting: 1950
  increase: 300
  lv1: 700
  max: 4300
medical_deposit: large
haggling: high
executable: true
---

# Тоска — Луиза Гарно «Тоска»

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Луиза Гарно «Тоска» | Louise Garneau "Tosca" |
| Nick | Тоска | Tosca |
| AllCapsNick | ТОСКА | TOSCA |
| Title | Посмотри ей в глаза | Look her in the eyes |
| Email | LouisaGarneau@aim.com | LouisaGarneau@aim.com |
| snype_nick | lonelyandsad | lonelyandsad |

## Bio

**RU:** as-shipped in `jazz-units/UnitData/Jazz_Buzz.lua` (роман с Рысью, нефтяная платформа, ярость).

**EN:** localization CSV for Bio id.

## Stats

| Stat | Value |
| --- | --- |
| Health | 71 |
| Agility | 85 |
| Dexterity | 64 |
| Strength | 68 |
| Wisdom | 90 |
| Will | (default / sheet ~49) |
| Leadership | 13 |
| Marksmanship | 96 |
| Mechanical | 5 |
| Explosives | 19 |
| Medical | 15 |
| MaxHitPoints | 79 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- `Jazz_Perk_Buzz`
- `HeavyWeaponsTraining`
- `AutoWeapons`
- `Psycho`
- `StressManagement`
- `ShockAndAwe`
- `LastWarning`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Buzz` |
| type | passive |
| DisplayName RU/EN | Свинцовый дождь / Lead Rain |
| Description RU/EN | Увеличивает длину очереди на 50% |
| Mechanics | Burst/auto bullet count +50% (see combat-actions docs) |

## Personality

- Quirks: Psycho
- Likes: Jazz_Lynx (complicated)
- Dislikes: (hate triggers on Lynx via chat); strong hate for Arulcans in sheet lore
- Refusal / Haggle: multiple Lynx-related refusals/haggles/mitigations in UnitData

## Hire

- Access: AIM
- MedicalDeposit: large; Haggling: high

## Inventory

- `Loot_JAZZ_Buzz` → `JAZZ_Buzz50/35/25/20`
- *50: Guardian light/legs (not VeryHard) or FlakM1955 on VeryHard; `FAMAS` + VerticalGrip + `JAZZ_Reflex_Aimpoint5000`; `JAZZ_AMMO_556_FMJ`×120

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](tosca.ja2-face.gif)

Файл: `tosca.ja2-face.gif`

## Portrait prompt

**CHARACTER_DESCRIPTION:** Match JA2 face reference `tosca.ja2-face.gif` (same face identity). Female American autorifleman mid-20s/30s, intense eyes, dark hair, tactical vest with ammo pouches and hearing protection — NO rifle. Hostile edge.

**Class kit:** ammo pouches, earpro, heavy-weapons instructor patch  
**Refs:** existing `Buzz.png` / `Buzz_Big.png`

## Phrases — AIM chat

As-shipped UnitData (Offline, Greeting, Idle, Parting, Rehire, Refusals/Haggles/Mitigations vs Lynx).

## Phrases — VoiceResponse

Full as-shipped `Jazz_Buzz` in items.lua.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Buzz |
| VoiceResponseId | Jazz_Buzz |
| pollyvoice | Amy |
| Portrait | Mod/Dv3mFVN/MercPortraits/Buzz.png |
| CustomEquipGear | Handheld A/B Firearm |
| Sources | `Jazz_Buzz.lua`, `Jazz_Perk_Buzz.lua`, `Loot_JAZZ_Buzz` |

## Open blockers

- none
