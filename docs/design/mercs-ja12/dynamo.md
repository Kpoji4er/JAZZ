---
status: planned
priority: medium
origin: ja2
unit_id: Jazz_Dynamo
portrait_id: Dynamo
affiliation: MERC
role: Mechanic
tier: Regular
specialization: Mechanic
gender: Male
nationality: Hungary
voice_source: ja2
starting_level: 3
will: 45
salary:
  starting: 50
  increase: 200
  lv1: 0
  max: 800
medical_deposit: none
haggling: normal
executable: false
---

# Динамо — Грег «Динамо» Дункан

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Грег «Динамо» Дункан | Грег «Динамо» Дункан |
| Nick | Динамо | Dynamo |
| AllCapsNick | ДИНАМО | DYNAMO |
| Title | Зек-механик | Зек-механик |
| Email | Dynamo@merc.com | Dynamo@merc.com |
| snype_nick | dynamo | dynamo |

## Bio

**RU:** Статы 55–65, Marksmanship 68, Mechanical 67, Wisdom 78. Псих. Дружит с Shank и Blood; не любит Meat. Может уйти в MERC после кампании. Дешёвый / for ideal.

**EN:** EN draft: translate Bio RU at generation.

## Stats

| Stat | Value |
| --- | --- |
| Health | 60 |
| Agility | 60 |
| Dexterity | 55 |
| Strength | 65 |
| Wisdom | 78 |
| Will | 45 |
| Leadership | 20 |
| Marksmanship | 68 |
| Mechanical | 67 |
| Explosives | 20 |
| Medical | 15 |
| MaxHitPoints | 60 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Dynamo`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Dynamo` |
| type | passive |
| DisplayName RU/EN | Вилкой в глаз / Вилкой в глаз |
| Description RU/EN | Спецэффекты ранений / Спецэффекты ранений |
| Mechanics | Head wounds cause blindness; groin wounds panic; Dynamo hit in groin → berserk. |

## Personality

- Quirks: Psycho
- Likes: Jazz_Shank, Blood
- Dislikes: Jazz_Meat
- National hates: Hungarians? (sheet: hates Hungarians — verify)
- Refusal / Haggle notes: Cheap

## Hire

- Access: Locals → MERC after campaign
- MedicalDeposit: none; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Dynamo`
- Presets (weights ~50/35/25/20):
  - *50: lockpicks expert, tools, light armor

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](dynamo.ja2-face.gif)

Файл: `dynamo.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `dynamo.ja2-face.gif` (same face identity). Prison-hardened mechanic, buzz cut, tool belt and lockpicks — NO gun. Cocky.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Lockpick set, tool belt, prison tattoo visible, wrench

## Phrases — AIM chat

### Offline
- RU: Динамо вне зоны — наверно.
- EN: This is Dynamo. Leave a message.

### GreetingAndOffer
- RU: Динамо. Чо надо?
- EN: Dynamo here.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Давай уже.
- EN: Waiting.

### PartingWords
- RU: За идею пойду — или за полтинник.
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

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Динамо!» / «Dynamo!»
  - AimAttack / OpponentKilled / DeathGeneral / Downed / CombatStartPlayer / LevelUp / AmmoLow / Idle — standard drafts + relationship slots.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Dynamo |
| VoiceResponseId | Jazz_Dynamo |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Dynamo.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Dynamo_Big.png |
| CustomEquipGear | TryEquip Handheld A/B as role requires |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
