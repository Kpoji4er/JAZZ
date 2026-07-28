---
status: planned
priority: high
origin: ja2
unit_id: Jazz_Colby
portrait_id: Colby
affiliation: AIM
role: Demolitions
tier: Elite
specialization: ExplosiveExpert
gender: Male
nationality: Canada
voice_source: ja2
starting_level: 5
will: 80
salary:
  starting: 2800
  increase: 200
  lv1: 1200
  max: 7000
medical_deposit: large
haggling: normal
executable: false
---

# Колби — Тревор Колби

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Тревор Колби | Тревор Колби |
| Nick | Колби | Colby |
| AllCapsNick | КОЛБИ | COLBY |
| Title | Ловушечник | Ловушечник |
| Email | Colby@aim.com | Colby@aim.com |
| snype_nick | tripwire | tripwire |

## Bio

**RU:** Боевой подрывник и ловушечник AIM. Лютые физикалы (кроме силы/подвижности), 99 механики, 88 взрывчатки. Дружит с Тором, не дружит с Фиделем; не любит американцев.

**EN:** EN draft: translate Bio RU at generation; keep tone.

## Stats

| Stat | Value |
| --- | --- |
| Health | 96 |
| Agility | 72 |
| Dexterity | 95 |
| Strength | 70 |
| Wisdom | 97 |
| Will | 80 |
| Leadership | 40 |
| Marksmanship | 78 |
| Mechanical | 99 |
| Explosives | 88 |
| Medical | 20 |
| MaxHitPoints | 96 |
| StartingLevel | 5 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Colby`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Colby` |
| type | passive |
| DisplayName RU/EN | Цепная паника / Цепная паника |
| Description RU/EN | Взрывы Колби сеют панику / Взрывы Колби сеют панику |
| Mechanics | Каждый взрыв, инициированный Колби (граната/миномёт/C4/бочка/мина/чужая бомба выстрелом): 20% шанс паники у раненых врагов в радиусе; +20% к радиусу взрывов. |

## Personality

- Quirks: —
- Likes: Thor
- Dislikes: Fidel
- National hates: Americans
- Refusal / Haggle notes: Standard AIM

## Hire

- Access: AIM hire
- MedicalDeposit: large; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Colby`
- Presets (weights ~50/35/25/20):
  - *50: demo satchel, shaped charges×2, lockpick set, smoke×2, light armor, secondary SMG family
  - lower tiers: fewer charges / lighter kit

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](colby.ja2-face.gif)

Файл: `colby.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `colby.ja2-face.gif` (same face identity). Male athletic Canadian demolitions expert ~35, short cropped hair, scarred hands, olive field vest with demolitions pouches and detonator clacker on chest — NO firearm. Focused calm look.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Demo satchel, detonator clacker, wire cutters, charge pouches, EOD patch

## Phrases — AIM chat

### Offline
- RU: Колби. Меня нет. Оставьте сообщение — перезвоню, если не взорвусь.
- EN: This is Colby. Leave a message.

### GreetingAndOffer
- RU: Колби на линии. Что взрываем?
- EN: Colby here. Talk.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Время тикает.
- EN: Waiting on you.

### PartingWords
- RU: Беру зарядку и выхожу.
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
  - Selection: «Колби!» / «Colby!»
  - AimAttack: «На мушке.» / «On target.»
  - OpponentKilled: «Готово.» / «Done.»
  - DeathGeneral: «Чёрт...» / «Damn...»
  - Downed: «Меня подбили!» / «I'm hit!»
  - CombatStartPlayer: «В бой.» / «Engage.»
  - LevelUp: «Ещё лучше.» / «Getting better.»
  - AmmoLow: «Патроны!» / «Ammo!»
  - Idle: «Жду.» / «Waiting.»
- Relationship VR slots per Likes/Dislikes when generating.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Colby |
| VoiceResponseId | Jazz_Colby |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Colby.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Colby_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm (or melee for knife mercs) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
