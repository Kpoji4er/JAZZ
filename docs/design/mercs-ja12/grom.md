---
status: planned
priority: high
origin: nightops
unit_id: Jazz_Grom
portrait_id: Grom
affiliation: Locals
role: HeavyWeapons
tier: Veteran
specialization: HeavyWeapons
gender: Male
nationality: Russia
voice_source: nightops
starting_level: 5
will: 80
salary:
  starting: 0
  increase: 200
  lv1: 0
  max: 0
medical_deposit: none
haggling: none
executable: false
---

# Гром — Майор Сергей «Гром» Громов

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Майор Сергей «Гром» Громов | Майор Сергей «Гром» Громов |
| Nick | Гром | Grom |
| AllCapsNick | ГРОМ | GROM |
| Title | Афганец | Афганец |
| Email | Grom@vvs.ru | Grom@vvs.ru |
| snype_nick | gromov | gromov |

## Bio

**RU:** Сослуживец Ивана. Shady Job → Night Ops. Найм: захват аэропорта + ПВО → ждёт в аэропорту. Бесплатно, с собой гранатомёт. Дружит с Иваном, Игорем, Iggy; не любит Стрелка.

**EN:** EN draft: translate Bio RU at generation; keep tone.

## Stats

| Stat | Value |
| --- | --- |
| Health | 85 |
| Agility | 75 |
| Dexterity | 75 |
| Strength | 85 |
| Wisdom | 70 |
| Will | 80 |
| Leadership | 45 |
| Marksmanship | 75 |
| Mechanical | 67 |
| Explosives | 47 |
| Medical | 25 |
| MaxHitPoints | 85 |
| StartingLevel | 5 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Grom`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Grom` |
| type | passive |
| DisplayName RU/EN | Артподготовка / Артподготовка |
| Description RU/EN | Тяжёлое + броски / Тяжёлое + броски |
| Mechanics | Heavy weapons expertise + throwing. Arrives with free RPG/launcher loadout on hire. |

## Personality

- Quirks: —
- Likes: Ivan, Igor, Iggy
- Dislikes: Scope
- National hates: —
- Refusal / Haggle notes: Free after sector gate

## Hire

- Access: Capture airport + nearby AA then meet at airport
- MedicalDeposit: none; Haggling: none; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Grom`
- Presets (weights ~50/35/25/20):
  - *50: grenade launcher / RPG + ammo, Russian field kit, flak

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](grom.ja2-face.gif)

Файл: `grom.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `grom.ja2-face.gif` (same face identity). Russian major ~45, weathered face, afghanka jacket, bandolier of HE rounds and launcher tube on back as silhouette prop WITHOUT aiming — prefer ammo bandolier + rangefinder, no held launcher. Calm soldier.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** HE round bandolier, rangefinder, major shoulder boards, Afghan jacket

## Phrases — AIM chat

### Offline
- RU: Громов. Связь позже.
- EN: This is Grom. Leave a message.

### GreetingAndOffer
- RU: Майор Громов. Аэродром ваш — я ваш.
- EN: Grom here. Talk.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Жду приказа.
- EN: Waiting on you.

### PartingWords
- RU: Гранатомёт с собой.
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
  - Selection: «Гром!» / «Grom!»
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
| Appearance | Grom |
| VoiceResponseId | Jazz_Grom |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Grom.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Grom_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm (or melee for knife mercs) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=nightops |

## Open blockers

- none
