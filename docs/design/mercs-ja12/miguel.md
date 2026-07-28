---
status: planned
priority: medium
origin: ja2
unit_id: Jazz_Miguel
portrait_id: Miguel
affiliation: Locals
role: Commander
tier: Veteran
specialization: Leader
gender: Male
nationality: Arulco
voice_source: ja2
starting_level: 4
will: 80
salary:
  starting: 800
  increase: 200
  lv1: 400
  max: 3000
medical_deposit: standard
haggling: normal
executable: false
---

# Мигель — Мигель Кордона

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Мигель Кордона | Мигель Кордона |
| Nick | Мигель | Miguel |
| AllCapsNick | МИГЕЛЬ | MIGUEL |
| Title | Команданте | Команданте |
| Email | Miguel@arulco.reb | Miguel@arulco.reb |
| snype_nick | comandante | comandante |

## Bio

**RU:** Статы 70–80, Leadership 98. Дружит с Carlos, Ira, Shadow; не любит Iggy; не любит немцев. Сюжетно сомнителен как AIM-hire, но в каталоге.

**EN:** EN draft: translate Bio RU at generation.

## Stats

| Stat | Value |
| --- | --- |
| Health | 80 |
| Agility | 75 |
| Dexterity | 70 |
| Strength | 75 |
| Wisdom | 80 |
| Will | 80 |
| Leadership | 98 |
| Marksmanship | 70 |
| Mechanical | 30 |
| Explosives | 30 |
| Medical | 35 |
| MaxHitPoints | 80 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Miguel`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Miguel` |
| type | passive |
| DisplayName RU/EN | Команданте / Команданте |
| Description RU/EN | Лидерство повстанцев / Лидерство повстанцев |
| Mechanics | Leadership aura / militia morale (needs-design numbers). NightOps + knife skills from JA2. |

## Personality

- Quirks: —
- Likes: Carlos, Jazz_Ira, Shadow
- Dislikes: Iggy
- National hates: Germans
- Refusal / Haggle notes: Local

## Hire

- Access: Locals / story
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Miguel`
- Presets (weights ~50/35/25/20):
  - *50: officer sidearm holstered, rebel coat, radio

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](miguel.ja2-face.gif)

Файл: `miguel.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `miguel.ja2-face.gif` (same face identity). Charismatic Arulco rebel leader, mustache, command coat with radio and map — holstered pistol OK. Determined.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Command radio, map case, rebel sash, holstered pistol

## Phrases — AIM chat

### Offline
- RU: Мигель. Оставьте сообщение для дела свободы.
- EN: This is Miguel. Leave a message.

### GreetingAndOffer
- RU: Говорит Мигель.
- EN: Miguel here.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Арулько ждёт.
- EN: Waiting.

### PartingWords
- RU: Встаём.
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
  - Selection: «Мигель!» / «Miguel!»
  - AimAttack / OpponentKilled / DeathGeneral / Downed / CombatStartPlayer / LevelUp / AmmoLow / Idle — standard drafts + relationship slots.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Miguel |
| VoiceResponseId | Jazz_Miguel |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Miguel.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Miguel_Big.png |
| CustomEquipGear | TryEquip Handheld A/B as role requires |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- named perk numbers needs-design
