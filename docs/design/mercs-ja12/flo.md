---
status: planned
priority: medium
origin: ja2
unit_id: Jazz_Flo
portrait_id: Flo
affiliation: MERC
role: Support
tier: Regular
specialization: Negotiator
gender: Female
nationality: USA
voice_source: ja2
starting_level: 2
will: 40
salary:
  starting: 500
  increase: 200
  lv1: 200
  max: 1800
medical_deposit: standard
haggling: normal
executable: false
---

# Фло — Флоренс «Фло» Габриель

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Флоренс «Фло» Габриель | Флоренс «Фло» Габриель |
| Nick | Фло | Flo |
| AllCapsNick | ФЛО | FLO |
| Title | Безголовая курица | Безголовая курица |
| Email | Flo@merc.com | Flo@merc.com |
| snype_nick | bargain | bargain |

## Bio

**RU:** Статы 40–50, Dex 60, Marksmanship 38 (худшая), Wisdom 82. Трусливая. Hidden: buy −10% / sell +10%. Дружит с Biff и Lynx; боится Lava.

**EN:** EN draft: translate Bio RU at generation.

## Stats

| Stat | Value |
| --- | --- |
| Health | 48 |
| Agility | 45 |
| Dexterity | 60 |
| Strength | 40 |
| Wisdom | 82 |
| Will | 40 |
| Leadership | 40 |
| Marksmanship | 38 |
| Mechanical | 15 |
| Explosives | 5 |
| Medical | 20 |
| MaxHitPoints | 48 |
| StartingLevel | 2 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Flo`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Flo` |
| type | passive |
| DisplayName RU/EN | Барахольщица / Барахольщица |
| Description RU/EN | Скидки у торговцев / Скидки у торговцев |
| Mechanics | 10–15% shop discount + improved loot-sale operation (sheet). |

## Personality

- Quirks: Coward
- Likes: Biff, Jazz_Lynx
- Dislikes: Lava (fear)
- National hates: —
- Refusal / Haggle notes: MERC

## Hire

- Access: MERC
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Flo`
- Presets (weights ~50/35/25/20):
  - *50: purse/ledger, soft clothes, tiny first aid

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](flo.ja2-face.gif)

Файл: `flo.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `flo.ja2-face.gif` (same face identity). Frazzled American woman, messy hair, civilian-tactical hybrid, shopping ledger and radio — NO weapon. Worried look.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Ledger, radio, bargain tags, soft satchel

## Phrases — AIM chat

### Offline
- RU: Фло не может подойти!
- EN: This is Flo. Leave a message.

### GreetingAndOffer
- RU: Ой! Фло слушает...
- EN: Flo here.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Можно я постою сзади?
- EN: Waiting.

### PartingWords
- RU: Ладно, только без стрельбы...
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
  - Selection: «Фло!» / «Flo!»
  - AimAttack / OpponentKilled / DeathGeneral / Downed / CombatStartPlayer / LevelUp / AmmoLow / Idle — standard drafts + relationship slots.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Flo |
| VoiceResponseId | Jazz_Flo |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Flo.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Flo_Big.png |
| CustomEquipGear | TryEquip Handheld A/B as role requires |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
