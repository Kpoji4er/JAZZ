---
status: planned
priority: medium
origin: ub
unit_id: Jazz_Manuel
portrait_id: Manuel
affiliation: Locals
role: Scout
tier: Regular
specialization: Stealth
gender: Male
nationality: Arulco
voice_source: nightops
starting_level: 3
will: 60
salary:
  starting: 600
  increase: 200
  lv1: 300
  max: 2000
medical_deposit: standard
haggling: normal
executable: false
---

# Мануэль — Мануэль

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Мануэль | Мануэль |
| Nick | Мануэль | Manuel |
| AllCapsNick | МАНУЭЛЬ | MANUEL |
| Title | Муж Фатимы | Муж Фатимы |
| Email | Manuel@arulco.reb | Manuel@arulco.reb |
| snype_nick | manuel | manuel |

## Bio

**RU:** UB/NO. Husband of Fatima, father of Pacos. Undercover in Arulco army for Miguel, exposed, fled. Met wandering Tracona forest. Stats 70+, Dex 91. Loner.

**EN:** EN draft: translate Bio RU at generation.

## Stats

| Stat | Value |
| --- | --- |
| Health | 72 |
| Agility | 80 |
| Dexterity | 91 |
| Strength | 70 |
| Wisdom | 65 |
| Will | 60 |
| Leadership | 30 |
| Marksmanship | 70 |
| Mechanical | 30 |
| Explosives | 25 |
| Medical | 25 |
| MaxHitPoints | 72 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Manuel`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Manuel` |
| type | passive |
| DisplayName RU/EN | Под прикрытием / Под прикрытием |
| Description RU/EN | Expert stealth / Expert stealth |
| Mechanics | Stealthy expert. Partial VO planned (same actor, not full JA3). |

## Personality

- Quirks: Loner
- Likes: —
- Dislikes: —
- National hates: —
- Refusal / Haggle notes: Local meet

## Hire

- Access: Encounter in forest / locals
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Manuel`
- Presets (weights ~50/35/25/20):
  - *50: stealth kit, binoculars, light armor

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](manuel.ja2-face.gif)

Файл: `manuel.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `manuel.ja2-face.gif` (same face identity). Lean Arulco scout, tired eyes, binoculars and forest camo — NO gun. Cautious.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Binoculars, forest camo, water skin, stealth wrap

## Phrases — AIM chat

### Offline
- RU: Мануэль... позже.
- EN: This is Manuel. Leave a message.

### GreetingAndOffer
- RU: Это Мануэль.
- EN: Manuel here.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Тише.
- EN: Waiting.

### PartingWords
- RU: Иду.
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

- `voice_source: nightops` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Мануэль!» / «Manuel!»
  - AimAttack / OpponentKilled / DeathGeneral / Downed / CombatStartPlayer / LevelUp / AmmoLow / Idle — standard drafts + relationship slots.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Manuel |
| VoiceResponseId | Jazz_Manuel |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Manuel.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Manuel_Big.png |
| CustomEquipGear | TryEquip Handheld A/B as role requires |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ub |

## Open blockers

- none
