---
status: ready
priority: low
origin: wildfire
unit_id: Jazz_Steiger
portrait_id: Steiger
affiliation: AIM
role: Commander
tier: Elite
specialization: Leader
gender: Male
nationality: Germany
voice_source: wildfire
starting_level: 5
will: 70
salary:
  starting: 5500
  increase: 150
  lv1: 2500
  max: 11000
medical_deposit: large
haggling: high
executable: true
---

# Штайгер — Рудольф Штайгер

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Рудольф Штайгер | Rudolf Steiger |
| Nick | Штайгер | Steiger |
| AllCapsNick | ШТАЙГЕР | STEIGER |
| Title | Дорогой немец | The Expensive German |
| Email | Steiger@aim.com | Steiger@aim.com |
| snype_nick | steiger | steiger |

## Bio

**RU:** Wildfire. Статы 75–85, Сила 69, Мудрость 90, Лидерство 69, Меткость 94. Плохо переносит жару. Любит Хеннинга, Лору и Гранти; недолюбливает Корда и Булла. Очень дорогой специалист.

**EN:** Wildfire mercenary. Stats in the 75-85 range, 69 Strength, 90 Wisdom, 69 Leadership, 94 Marksmanship. Handles heat poorly. Fond of Henning, Laura, and Grunty; not fond of Cord or Bull. A very expensive specialist.

## Stats

| Stat | Value |
| --- | --- |
| Health | 80 |
| Agility | 75 |
| Dexterity | 75 |
| Strength | 69 |
| Wisdom | 90 |
| Will | 70 |
| Leadership | 69 |
| Marksmanship | 94 |
| Mechanical | 35 |
| Explosives | 35 |
| Medical | 30 |
| MaxHitPoints | 80 |
| StartingLevel | 5 |

## Perks

### StartingPerks

- `Jazz_Perk_Steiger`
- `NightOps`
- `Teacher`
- `LeadFromTheFront`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Steiger` |
| type | passive |
| DisplayName RU/EN | Ночной инструктор / Night Instructor |
| Description RU/EN | Ночью Штайгер обучает соседних союзников лучше стрелять / At night, Steiger's coaching sharpens nearby allies' aim |
| Mechanics | During Nighttime missions, allies within 5 tiles of Steiger gain +5% CTH, reflecting his career as a night-operations instructor. |

## Personality

- Quirks: FearHeat
- Likes: `Jazz_Henning`, `Jazz_Laura`, `Grunty`
- Dislikes: `Jazz_Cord`, `Jazz_Bull`
- National hates: —
- Refusal / Haggle notes: refuses if Jazz_Cord or Jazz_Bull are in the active squad; haggles high by default (expensive specialist); mitigation and rate discount when Jazz_Henning or Jazz_Laura are hired

## Hire

- Access: AIM
- MedicalDeposit: large; Haggling: high; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Steiger` → `JAZZ_Steiger50/35/25/20`
- *50: `JazzArmor_PoliceVest`, `HK G3`, `JAZZ_AMMO_308_Match`×40 (Double), `NVGoggles`, `Radio`
- *35: `FNFAL`, `JAZZ_AMMO_308_FMJ`×32 (Double)
- *25: `M14`, `JAZZ_AMMO_308_FMJ`×24 (Double)
- *20: `M1Garand`, `JAZZ_AMMO_3006_FMJ`×20 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](steiger.ja2-face.gif)

Файл: `steiger.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `steiger.ja2-face.gif` (same face identity). Expensive German commander, neat, instructor tabs and night-ops monocle — NO gun.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Instructor tabs, monocle case, officer coat

## Phrases — AIM chat

### Offline
- RU: Штайгер занят. Перезвоните.
- EN: Steiger's busy. Call back.

### GreetingAndOffer
- RU: Штайгер слушает. Условия обсуждаются заранее.
- EN: Steiger here. Terms are discussed up front.

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Жарко. Не для меня климат.
- EN: It's hot. Not my kind of climate.

### PartingWords
- RU: Дорого — но да. Я в деле.
- EN: Expensive — but yes. I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. По прежней ставке, разумеется.
- EN: I'm staying. At the same rate, naturally.

### Refusals
- Cord or Bull hired RU: Пока эти двое в отряде — переговоров не будет.
- Cord or Bull hired EN: No negotiations while those two are on the team.
- Money RU: Моя квалификация стоит дороже.
- Money EN: My expertise is worth more than that.

### Haggles
- Money RU: Стандартная ставка для специалиста моего уровня — не ниже.
- Money EN: Standard rate for a specialist of my caliber — not a cent less.

### Mitigations
- Henning or Laura hired RU: Хеннинг (или Лора) уже здесь? Тогда сделаем скидку.
- Henning or Laura hired EN: Henning (or Laura) is already in? Then we'll make an exception on price.

## Phrases — VoiceResponse

- `voice_source: wildfire` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Штайгер к вашим услугам.» / «Steiger at your service.»
  - AimAttack (1): «Дисциплина и точность.» / «Discipline and precision.»
  - AimAttack (2): «По учебнику.» / «By the book.»
  - OpponentKilled: «Урок усвоен.» / «Lesson learned.»
  - DeathGeneral: «Недостойный конец...» / «An unworthy end...»
  - Downed: «Ранен. Неприемлемо.» / «Hit. Unacceptable.»
  - CombatStartDetected: «Противник обнаружен. Внимание.» / «Enemy detected. Attention.»
  - LevelUp: «Прогресс налицо.» / «Progress is evident.»
  - AmmoLow: «Боеприпасы на исходе.» / «Ammunition running low.»
  - Idle: «Жарко. Жду тени.» / «Hot. Waiting for shade.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Steiger |
| VoiceResponseId | Jazz_Steiger |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Steiger.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Steiger_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm (two-handed rifle) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=wildfire |

## Open blockers

- none
