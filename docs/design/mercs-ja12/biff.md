---
status: planned
priority: medium
origin: ja2
unit_id: Jazz_Biff
portrait_id: Biff
affiliation: MERC
role: Commander
tier: Regular
specialization: Leader
gender: Male
nationality: USA
voice_source: ja2
starting_level: 2
will: 35
salary:
  starting: 600
  increase: 200
  lv1: 300
  max: 2000
medical_deposit: standard
haggling: normal
executable: false
---

# Бифф — Бифф Апскотт

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Бифф Апскотт | Бифф Апскотт |
| Nick | Бифф | Biff |
| AllCapsNick | БИФФ | BIFF |
| Title | Ссыкло MERC | Ссыкло MERC |
| Email | Biff@merc.com | Biff@merc.com |
| snype_nick | biff | biff |

## Bio

**RU:** ~70 статы, Strength 41, Wisdom 58, Marksmanship 57, Leadership 13. Трусливый. Дружит с Flo и Larry clean; не любит Larry drunk. Добавлять после квеста Биффа, если жив.

**EN:** EN draft: translate Bio RU at generation.

## Stats

| Stat | Value |
| --- | --- |
| Health | 70 |
| Agility | 65 |
| Dexterity | 60 |
| Strength | 41 |
| Wisdom | 58 |
| Will | 35 |
| Leadership | 13 |
| Marksmanship | 57 |
| Mechanical | 20 |
| Explosives | 15 |
| Medical | 25 |
| MaxHitPoints | 70 |
| StartingLevel | 2 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Biff`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Biff` |
| type | operation |
| DisplayName RU/EN | Вербовка MERC / Вербовка MERC |
| Description RU/EN | Спецоп MERC вместо ополчения / Спецоп MERC вместо ополчения |
| Mechanics | Special operation to recruit MERC troopers instead of militia (sheet). |

## Personality

- Quirks: Coward
- Likes: Flo, Larry(clean)
- Dislikes: Larry(drugged)
- National hates: —
- Refusal / Haggle notes: Post-quest

## Hire

- Access: After Biff quest if alive → MERC
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Biff`
- Presets (weights ~50/35/25/20):
  - *50: cheap pistol holstered, soft armor, MERC paperwork

## JA2 face reference

Нет файла в архиве `портировать.rar` для этого мерка. Перед генерацией портрета добавить `biff.ja2-face.*` или явно согласовать face ref.

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Nervous overweight American desk merc, sweaty, clipboard and MERC badge — holstered pistol only. Anxious smile.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Clipboard, MERC badge, soft armor, holstered pistol

## Phrases — AIM chat

### Offline
- RU: Бифф... э-э... перезвоните?
- EN: This is Biff. Leave a message.

### GreetingAndOffer
- RU: Э... Бифф. Вы серьёзно?
- EN: Biff here.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Можно без стрельбы?
- EN: Waiting.

### PartingWords
- RU: Ладно... я попробую.
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
  - Selection: «Бифф!» / «Biff!»
  - AimAttack / OpponentKilled / DeathGeneral / Downed / CombatStartPlayer / LevelUp / AmmoLow / Idle — standard drafts + relationship slots.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Biff |
| VoiceResponseId | Jazz_Biff |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Biff.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Biff_Big.png |
| CustomEquipGear | TryEquip Handheld A/B as role requires |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- quest gate wiring needs-design
