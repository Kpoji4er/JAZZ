---
status: planned
priority: medium
origin: wildfire
unit_id: Jazz_Allik
portrait_id: Allik
affiliation: AIM
role: AllRounder
tier: Elite
specialization: AllRounder
gender: Male
nationality: Estonia
voice_source: wildfire
starting_level: 5
will: 80
salary:
  starting: 2600
  increase: 200
  lv1: 1100
  max: 6000
medical_deposit: standard
haggling: normal
executable: false
---

# Знаток — Янно «Знаток» Аллик

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Янно «Знаток» Аллик | Янно «Знаток» Аллик |
| Nick | Знаток | Allik |
| AllCapsNick | ЗНАТОК | ALLIK |
| Title | Эстонец | Эстонец |
| Email | Allik@aim.com | Allik@aim.com |
| snype_nick | znatok | znatok |

## Bio

**RU:** Wildfire. Best stats-per-level. Marksmanship 78, Mech 76, Exp 43. Optimist. Likes Vilde and Grace; dislikes Sydney, Dr.Q. File nationality may be Russian (WF quirk).

**EN:** EN draft: translate Bio RU at generation.

## Stats

| Stat | Value |
| --- | --- |
| Health | 88 |
| Agility | 85 |
| Dexterity | 85 |
| Strength | 80 |
| Wisdom | 85 |
| Will | 80 |
| Leadership | 50 |
| Marksmanship | 78 |
| Mechanical | 76 |
| Explosives | 43 |
| Medical | 30 |
| MaxHitPoints | 88 |
| StartingLevel | 5 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Allik`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Allik` |
| type | passive |
| DisplayName RU/EN | Знаток дела / Знаток дела |
| Description RU/EN | Lockpick + heavy / Lockpick + heavy |
| Mechanics | Lockpicking + HeavyWeapons synergy / XP efficiency. needs-design. |

## Personality

- Quirks: Optimist
- Likes: Jazz_Vilde, Jazz_Grace
- Dislikes: Sidney, DrQ
- National hates: —(tagged Russian in WF files)
- Refusal / Haggle notes: AIM WF

## Hire

- Access: AIM
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Allik`
- Presets (weights ~50/35/25/20):
  - *50: lockpicks, multi-tool, mid armor

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](allik.ja2-face.gif)

Файл: `allik.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `allik.ja2-face.gif` (same face identity). Competent Estonian all-rounder, neat gear, multi-tool and lockpick case — NO gun. Optimistic calm.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Lockpick case, multi-tool, notebook, AIM pin

## Phrases — AIM chat

### Offline
- RU: Знаток занят.
- EN: This is Allik. Leave a message.

### GreetingAndOffer
- RU: Аллик слушает.
- EN: Allik here.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Готово к работе.
- EN: Waiting.

### PartingWords
- RU: Выхожу.
- EN: I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь.
- EN: I'm staying.

### Refusals / Haggles / Mitigations / ExtraPartingWords
- Draft relationship refusals/haggles from Personality at generation time.

## Phrases — VoiceResponse

- `voice_source: wildfire` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Знаток!» / «Allik!»
  - AimAttack / OpponentKilled / DeathGeneral / Downed / CombatStartPlayer / LevelUp / AmmoLow / Idle — standard drafts + relationship slots.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Allik |
| VoiceResponseId | Jazz_Allik |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Allik.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Allik_Big.png |
| CustomEquipGear | TryEquip Handheld A/B as role requires |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=wildfire |

## Open blockers

- perk numbers needs-design
