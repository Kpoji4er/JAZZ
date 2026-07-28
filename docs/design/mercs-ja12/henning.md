---
status: planned
priority: medium
origin: wildfire
unit_id: Jazz_Henning
portrait_id: Henning
affiliation: AIM
role: Commander
tier: Elite
specialization: Leader
gender: Male
nationality: Germany
voice_source: wildfire
starting_level: 5
will: 85
salary:
  starting: 5000
  increase: 200
  lv1: 2500
  max: 10000
medical_deposit: large
haggling: high
executable: false
---

# Хеннинг — Хеннинг фон Браниц

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Хеннинг фон Браниц | Хеннинг фон Браниц |
| Nick | Хеннинг | Henning |
| AllCapsNick | ХЕННИНГ | HENNING |
| Title | Барон-гасс | Барон-гасс |
| Email | Henning@aim.com | Henning@aim.com |
| snype_nick | vonbranitz | vonbranitz |

## Bio

**RU:** Wildfire Gus replacement. Stats 70–80, Wisdom 96, Leadership 76, Marksmanship 92. Claustrophobe. Likes Rudolf, Laura; dislikes Thor, Ricochet.

**EN:** EN draft: translate Bio RU at generation.

## Stats

| Stat | Value |
| --- | --- |
| Health | 78 |
| Agility | 70 |
| Dexterity | 75 |
| Strength | 75 |
| Wisdom | 96 |
| Will | 85 |
| Leadership | 76 |
| Marksmanship | 92 |
| Mechanical | 35 |
| Explosives | 35 |
| Medical | 35 |
| MaxHitPoints | 78 |
| StartingLevel | 5 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Henning`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Henning` |
| type | passive |
| DisplayName RU/EN | Кабинетный генерал / Кабинетный генерал |
| Description RU/EN | Auto + heavy training / Auto + heavy training |
| Mechanics | AutoWeapons + HeavyWeapons. Leadership checks strong. needs-design unique. |

## Personality

- Quirks: Claustrophobic
- Likes: Jazz_Steiger, Jazz_Laura
- Dislikes: Thor, Jazz_Ricochet
- National hates: —
- Refusal / Haggle notes: Expensive AIM

## Hire

- Access: AIM
- MedicalDeposit: large; Haggling: high; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Henning`
- Presets (weights ~50/35/25/20):
  - *50: officer kit, smoking pipe, mid-heavy armor

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](henning.ja2-face.gif)

Файл: `henning.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `henning.ja2-face.gif` (same face identity). Aristocratic German commander, thin mustache, pipe and map case — NO gun. Smoker Gus energy.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Pipe, map case, officer coat, reading glasses

## Phrases — AIM chat

### Offline
- RU: Фон Браниц отсутствует.
- EN: This is Henning. Leave a message.

### GreetingAndOffer
- RU: Хеннинг слушает.
- EN: Henning here.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Ну?
- EN: Waiting.

### PartingWords
- RU: Принято.
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
  - Selection: «Хеннинг!» / «Henning!»
  - AimAttack / OpponentKilled / DeathGeneral / Downed / CombatStartPlayer / LevelUp / AmmoLow / Idle — standard drafts + relationship slots.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Henning |
| VoiceResponseId | Jazz_Henning |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Henning.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Henning_Big.png |
| CustomEquipGear | TryEquip Handheld A/B as role requires |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=wildfire |

## Open blockers

- unique perk beyond training tags needs-design
