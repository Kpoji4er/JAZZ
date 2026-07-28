---
status: planned
priority: medium
origin: ja2
unit_id: Jazz_Quinten
portrait_id: Quinten
affiliation: AIM
role: Doctor
tier: Elite
specialization: Doctor
gender: Male
nationality: USA
voice_source: ja2
starting_level: 5
will: 85
salary:
  starting: 3000
  increase: 200
  lv1: 1500
  max: 7500
medical_deposit: large
haggling: normal
executable: false
---

# Дэнни — Доктор Дэниел «Дэнни» Квинтен

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Доктор Дэниел «Дэнни» Квинтен | Доктор Дэниел «Дэнни» Квинтен |
| Nick | Дэнни | Danny |
| AllCapsNick | ДЭННИ | DANNY |
| Title | Машина, не человек | Машина, не человек |
| Email | Quinten@aim.com | Quinten@aim.com |
| snype_nick | parkourmd | parkourmd |

## Bio

**RU:** 99 Health, 99 Agility, ~80 Str/Dex, Wisdom 91, Medical 88, Marksmanship 61. Одиночка. Не любит Steroid, Meat, Biff. Ambidextrous.

**EN:** EN draft: translate Bio RU at generation.

## Stats

| Stat | Value |
| --- | --- |
| Health | 99 |
| Agility | 99 |
| Dexterity | 80 |
| Strength | 80 |
| Wisdom | 91 |
| Will | 85 |
| Leadership | 20 |
| Marksmanship | 61 |
| Mechanical | 10 |
| Explosives | 10 |
| Medical | 88 |
| MaxHitPoints | 99 |
| StartingLevel | 5 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Quinten`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Quinten` |
| type | passive |
| DisplayName RU/EN | Полевой реаниматор / Полевой реаниматор |
| Description RU/EN | Лечение даёт ОД / Лечение даёт ОД |
| Mechanics | Special medkit set: removing negative effect / waking downed grants +2 AP to target. Parkour freemove bonus capped at +20% (not +50%). |

## Personality

- Quirks: Loner
- Likes: —
- Dislikes: Steroid, Jazz_Meat, Biff
- National hates: —
- Refusal / Haggle notes: AIM

## Hire

- Access: AIM
- MedicalDeposit: large; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Quinten`
- Presets (weights ~50/35/25/20):
  - *50: meds×50, advanced first aid, light armor, ambidextrous sidearms holstered

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](quinten.ja2-face.gif)

Файл: `quinten.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `quinten.ja2-face.gif` (same face identity). Extremely athletic male doctor, short hair, runner build, medic vest with trauma packs and shears — NO weapon. Confident.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Trauma packs, shears, IV pouch, medic cross patch

## Phrases — AIM chat

### Offline
- RU: Доктор Квинтен недоступен.
- EN: This is Danny. Leave a message.

### GreetingAndOffer
- RU: Квинтен. Сколько бежать?
- EN: Danny here.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Пульс ровный — твой нет.
- EN: Waiting.

### PartingWords
- RU: Аптечка собрана.
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
  - Selection: «Дэнни!» / «Danny!»
  - AimAttack / OpponentKilled / DeathGeneral / Downed / CombatStartPlayer / LevelUp / AmmoLow / Idle — standard drafts + relationship slots.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Quinten |
| VoiceResponseId | Jazz_Quinten |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Quinten.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Quinten_Big.png |
| CustomEquipGear | TryEquip Handheld A/B as role requires |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
