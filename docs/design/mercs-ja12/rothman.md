---
status: planned
priority: medium
origin: ja2
unit_id: Jazz_Rothman
portrait_id: Rothman
affiliation: AIM
role: Commander
tier: Veteran
specialization: Leader
gender: Male
nationality: SouthAfrica
voice_source: ja2
starting_level: 4
will: 70
salary:
  starting: 2200
  increase: 200
  lv1: 900
  max: 5500
medical_deposit: standard
haggling: normal
executable: false
---

# Ротман — Стефан Ротман

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Стефан Ротман | Стефан Ротман |
| Nick | Ротман | Rothman |
| AllCapsNick | РОТМАН | ROTHMAN |
| Title | Шахтёрский безопасник | Шахтёрский безопасник |
| Email | Rothman@aim.com | Rothman@aim.com |
| snype_nick | mineboss | mineboss |

## Bio

**RU:** Статы 78–85, Health 97, Leadership 59, Explosives 66. Работал на алмазных рудниках ЮАР. Дружит с Лавой; не любит Статика, Larry drunk, Гвоздя; недолюбливает американцев.

**EN:** EN draft: translate Bio RU at generation.

## Stats

| Stat | Value |
| --- | --- |
| Health | 97 |
| Agility | 80 |
| Dexterity | 78 |
| Strength | 85 |
| Wisdom | 75 |
| Will | 70 |
| Leadership | 59 |
| Marksmanship | 80 |
| Mechanical | 40 |
| Explosives | 66 |
| Medical | 30 |
| MaxHitPoints | 97 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Rothman`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Rothman` |
| type | operation |
| DisplayName RU/EN | Шахтёрский надзор / Шахтёрский надзор |
| Description RU/EN | Доход шахты / переговоры / Доход шахты / переговоры |
| Mechanics | PREFERRED: temporary mine income operation (catch thieves, boost output). ALT: Negotiator ops cost −50%. ALT active: Mozambique drill (2 body + 1 head, not MG/shotgun). |

## Personality

- Quirks: —
- Likes: Lava
- Dislikes: Jazz_Static, Larry(drugged), Nail
- National hates: Americans
- Refusal / Haggle notes: AIM

## Hire

- Access: AIM
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Rothman`
- Presets (weights ~50/35/25/20):
  - *50: rifle, officer kit, mine ledger, light explosives

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](rothman.ja2-face.gif)

Файл: `rothman.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `rothman.ja2-face.gif` (same face identity). Stocky South African security man, sun-worn face, khaki shirt with mine-safety badge and clipboard — NO gun.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Mine safety badge, clipboard, radio, hardhat clip

## Phrases — AIM chat

### Offline
- RU: Ротман. Перезвоните.
- EN: This is Rothman. Leave a message.

### GreetingAndOffer
- RU: Ротман. Контракт?
- EN: Rothman here.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Говори по делу.
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

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Ротман!» / «Rothman!»
  - AimAttack / OpponentKilled / DeathGeneral / Downed / CombatStartPlayer / LevelUp / AmmoLow / Idle — standard drafts + relationship slots.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Rothman |
| VoiceResponseId | Jazz_Rothman |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Rothman.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Rothman_Big.png |
| CustomEquipGear | TryEquip Handheld A/B as role requires |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- choose one perk variant in impl spec (mine op preferred)
