---
status: ready
priority: high
origin: ja2
unit_id: Jazz_Iggy
portrait_id: Iggy
affiliation: AIM
role: HeavyWeapons
tier: Veteran
specialization: HeavyWeapons
gender: Male
nationality: Russia
voice_source: ja2
starting_level: 5
will: 72
salary:
  starting: 1950
  increase: 200
  lv1: 1950
  max: 4500
medical_deposit: small
haggling: normal
executable: true
sources:
  - https://jaggedalliance.fandom.com/wiki/Igmus_%22Iggy%22_Palkov
  - JACenter RPC notes (San Mona / Wildfire)
---

# Игги — Игмус «Игги» Палков

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Игмус «Игги» Палков | Igmus "Iggy" Palkov |
| Nick | Игги | Iggy |
| AllCapsNick | ИГГИ | IGGY |
| Title | Тяжеловес из Сан-Моны | The San Mona Heavy |
| Email | Iggy@palkov.ru | Iggy@palkov.ru |
| snype_nick | iggy | iggy |

> RU-локализация Buka: «Игорь Палкин». В JAZZ канон EN-имени wiki: **Igmus "Iggy" Palkov**.

## Bio

**RU:** Русский наёмник, которого королева Дейдранна наняла в армию под командованием Майка ($2000/день). После убийства Майка и осознания режима Дейдранны дезертировал с совестью; позже сидит в баре и нанимается за $1950/день. Гордость и мораль сильные; мечтает о «Великой России». Эксперт тяжёлого оружия. Дружит с Иваном; Конрад его ценит; ненавидит Фиделя.

**EN:** A Russian merc hired into Queen Deidranna's army under Mike ($2000/day). After Mike was killed he deserted with a guilty conscience; later hireable for $1950/day. Strong pride and morality; dreams of a "Greater Russia." Heavy Weapons Expert. Likes Ivan; liked by Conrad; dislikes Fidel.

## Stats

| Stat | Value |
| --- | --- |
| Health | 88 |
| Agility | 81 |
| Dexterity | 79 |
| Strength | 85 |
| Wisdom | 71 |
| Will | 72 |
| Leadership | 15 |
| Marksmanship | 87 |
| Mechanical | 42 |
| Explosives | 21 |
| Medical | 33 |
| MaxHitPoints | 88 |
| StartingLevel | 5 |

## Perks

### StartingPerks

- `Jazz_Perk_Iggy`
- `HeavyWeaponsTraining`
- `Throwing`
- `Hardened`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Iggy` |
| type | passive |
| DisplayName RU/EN | Совесть дезертира / Deserter's Conscience |
| Description RU/EN | stub (UNITS-003 follow-up) |
| Mechanics | stub — `unit_reactions = {}` until UNITS-003 |

## Personality

- Likes: `Ivan`
- Dislikes: `Fidel`
- Liked by: `Jazz_Conrad`
- Disliked by: `Jazz_Carlos` (wired)
- Refusal: Fidel hired; Mitigation: Ivan hired

## Hire

- Access: AIM (`DaysUntilOnline` 0) — JA2 San Mona/5-towns gate TBD for Grand Chien
- Fee: 1950/day; MedicalDeposit: small; Haggling: normal

## Inventory

- Equipment loot id: `Loot_JAZZ_Iggy` → `JAZZ_Iggy50/35/25/20` (Grom-weight heavy kit: RPG7 + AK47 tiers)

## Portrait

Ship: `MercPortraits/Iggy.png`, `Iggy_Big.png` (militarized kit, IV+, TQ, IFAK).

## Phrases — AIM chat / VoiceResponse

Shipped in UnitData + minimal ModItemVoiceResponse; `FallbackMissingVR = Ice`.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | `Iggy` (clone Grom/Igor kit) |
| VoiceResponseId | `Jazz_Iggy` |
| Portrait | `Mod/Dv3mFVN/MercPortraits/Iggy.png` |
| BigPortrait | `Mod/Dv3mFVN/MercPortraits/Iggy_Big.png` |
| Perk | `jazz/CharacterEffect/Jazz_Perk_Iggy.lua` |
| UnitData | `jazz-units/UnitData/Jazz_Iggy.lua` |

## Open blockers

- none for ship; named perk combat hook = UNITS-003 follow-up
- Grand Chien RPC unlock sector (San Mona analogue) TBD — currently AIM shelf
