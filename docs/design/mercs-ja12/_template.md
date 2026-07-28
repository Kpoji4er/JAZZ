---
status: planned # ready | planned
priority: high # high | medium | low
origin: ja2 # ja2 | ub | wildfire | nightops | jazz
unit_id: Jazz_Example
portrait_id: Example
affiliation: AIM # AIM | MERC | Locals
role: Sniper # display role
tier: Elite
specialization: Marksmen
gender: Male
nationality: USA
voice_source: ja2
starting_level: 4
will: 70
salary:
  starting: 2000
  increase: 200
  lv1: 700
  max: 5000
medical_deposit: large
haggling: high
executable: false # true только без Open blockers
---

# <Nick> — <Full Name>

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | | |
| Nick | | |
| AllCapsNick | | |
| Title | | |
| Email | | |
| snype_nick | | |

## Bio

**RU:** …

**EN:** …

## Stats

| Stat | Value |
| --- | --- |
| Health | |
| Agility | |
| Dexterity | |
| Strength | |
| Wisdom | |
| Will | |
| Leadership | |
| Marksmanship | |
| Mechanical | |
| Explosives | |
| Medical | |
| MaxHitPoints | |
| StartingLevel | |

## Perks

### StartingPerks

- `PerkId`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_<Id>` |
| type | passive / active / operation |
| DisplayName RU/EN | |
| Description RU/EN | |
| Mechanics | числа и триггеры |

## Personality

- Quirks:
- Likes:
- Dislikes:
- National hates:
- Refusal / Haggle notes:

## Hire

- Access: AIM / MERC / local unlock / quest gate
- MedicalDeposit / Haggling / DaysUntilOnline:

## JA2 face reference

Лицо в портрете должно быть **похоже на JA2-референс**:

![JA2 face](<slug>.ja2-face.gif)

Файл: ``<slug>.ja2-face.gif`` (или `.jpg`) рядом со статьёй.

## Inventory

- Equipment loot id: `Loot_JAZZ_<Id>`
- Presets (weights 50/35/25/20): list items per tier

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role shown via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference ``<slug>.ja2-face.*`` (same face identity). …

**Preferred refs:** local ``<slug>.ja2-face.*`` + `MercPortraits/References/...`

**Class kit:** …

## Phrases — AIM chat

### Offline
- RU: …
- EN: …

### GreetingAndOffer / ConversationRestart / IdleLine / PartingWords / RehireIntro / RehireOutro
(same RU/EN pairs)

### Refusals / Haggles / Mitigations / ExtraPartingWords
(as needed)

## Phrases — VoiceResponse

Minimum slots from `_phrase-checklist.md`. For legacy VO: note reuse + RU subtitle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | |
| VoiceResponseId | |
| pollyvoice | |
| Portrait / BigPortrait paths | `Mod/Dv3mFVN/MercPortraits/<Id>.png` |
| CustomEquipGear | |
| FallbackMissingVR | |

## Open blockers

- none — or `perk: needs-design` / missing stats / …
