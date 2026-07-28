---
status: planned
priority: medium
origin: ub
unit_id: Jazz_Gaston
portrait_id: Gaston
affiliation: MERC
role: Sniper
tier: Elite
specialization: Marksmen
gender: Male
nationality: France
voice_source: ub
starting_level: 5
will: 70
salary:
  starting: 2500
  increase: 200
  lv1: 1000
  max: 6000
medical_deposit: standard
haggling: normal
executable: false
---

# Гастон — Гастон Кавалье

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Гастон Кавалье | Гастон Кавалье |
| Nick | Гастон | Gaston |
| AllCapsNick | ГАСТОН | GASTON |
| Title | Дамский снайпер | Дамский снайпер |
| Email | Gaston@merc.com | Gaston@merc.com |
| snype_nick | cavalier | cavalier |

## Bio

**RU:** UB. Статы 80–90, Marksmanship 94, skills ~20+. Cannot swim. Flirts with Tosca/Buns/Fox. Dislikes Foxbuns?, Vicious, Biff.

**EN:** EN draft: translate Bio RU at generation.

## Stats

| Stat | Value |
| --- | --- |
| Health | 85 |
| Agility | 80 |
| Dexterity | 85 |
| Strength | 75 |
| Wisdom | 70 |
| Will | 70 |
| Leadership | 40 |
| Marksmanship | 94 |
| Mechanical | 25 |
| Explosives | 20 |
| Medical | 20 |
| MaxHitPoints | 85 |
| StartingLevel | 5 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Gaston`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Gaston` |
| type | passive |
| DisplayName RU/EN | Крыша / Крыша |
| Description RU/EN | Стрельба с крыш / ночка / Стрельба с крыш / ночка |
| Mechanics | NightOps + rooftop shooting expertise (map to JA3 height/CTH). needs-design exact. |

## Personality

- Quirks: CannotSwim, Womanizer
- Likes: Jazz_Buzz, Buns, Fox (flirt)
- Dislikes: Jazz_Vicious, Biff
- National hates: —
- Refusal / Haggle notes: UB MERC

## Hire

- Access: MERC (UB origin)
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Gaston`
- Presets (weights ~50/35/25/20):
  - *50: sniper kit in loot, fancy scarf, spotting scope pouch

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](gaston.ja2-face.jpg)

Файл: `gaston.ja2-face.jpg`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `gaston.ja2-face.jpg` (same face identity). Suave French sniper, scarf, spotting scope on chest harness — NO rifle. Charming smile.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Spotting scope pouch, scarf, rooftop gloves, rangefinder

## Phrases — AIM chat

### Offline
- RU: Гастон у дамы. Пишите.
- EN: This is Gaston. Leave a message.

### GreetingAndOffer
- RU: Gaston à l'appareil.
- EN: Gaston here.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Ну же.
- EN: Waiting.

### PartingWords
- RU: Pour vous — всегда.
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

- `voice_source: ub` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Гастон!» / «Gaston!»
  - AimAttack / OpponentKilled / DeathGeneral / Downed / CombatStartPlayer / LevelUp / AmmoLow / Idle — standard drafts + relationship slots.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Gaston |
| VoiceResponseId | Jazz_Gaston |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Gaston.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Gaston_Big.png |
| CustomEquipGear | TryEquip Handheld A/B as role requires |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ub |

## Open blockers

- named perk numbers needs-design
