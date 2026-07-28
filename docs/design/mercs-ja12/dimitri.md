---
status: planned
priority: high
origin: ja2
unit_id: Jazz_Dimitri
portrait_id: Dimitri
affiliation: Locals
role: Thrower
tier: Regular
specialization: ExplosiveExpert
gender: Male
nationality: Russia
voice_source: ja2
starting_level: 3
will: 60
salary:
  starting: 500
  increase: 200
  lv1: 250
  max: 1800
medical_deposit: standard
haggling: normal
executable: false
---

# Димитрий — Димитрий Газзо

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Димитрий Газзо | Димитрий Газзо |
| Nick | Димитрий | Dimitri |
| AllCapsNick | ДИМИТРИЙ | DIMITRI |
| Title | Я забыл опять | Я забыл опять |
| Email | Dima@arulco.reb | Dima@arulco.reb |
| snype_nick | forgotagain | forgotagain |

## Bio

**RU:** Статы ~70, агила 50, механика 71. Забывчивый — может забыть маршрут посреди хода. Дружит с Мигелем и Карлосом; не любит Стефана. Крафтит суперметательные ножи (+20 к ведущему навыку броска).

**EN:** EN draft: translate Bio RU at generation; keep tone.

## Stats

| Stat | Value |
| --- | --- |
| Health | 70 |
| Agility | 50 |
| Dexterity | 65 |
| Strength | 70 |
| Wisdom | 56 |
| Will | 60 |
| Leadership | 30 |
| Marksmanship | 60 |
| Mechanical | 71 |
| Explosives | 40 |
| Medical | 15 |
| MaxHitPoints | 70 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Dimitri`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Dimitri` |
| type | passive |
| DisplayName RU/EN | Точильщик / Точильщик |
| Description RU/EN | Суперметательные ножи / Суперметательные ножи |
| Mechanics | Crafts/carries superior throwing knives (finite, not Blood infinite). +20 to governing throw skill check. |

## Personality

- Quirks: Forgetful (may cancel move mid-path)
- Likes: Miguel, Carlos
- Dislikes: Jazz_Rothman
- National hates: —
- Refusal / Haggle notes: Local

## Hire

- Access: Locals
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Dimitri`
- Presets (weights ~50/35/25/20):
  - *50: throwing knives stack, sharpening kit, light armor

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](dimitri.ja2-face.gif)

Файл: `dimitri.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `dimitri.ja2-face.gif` (same face identity). Stocky forgetful Russian rebel, messy hair, sheepish smile, bandolier of throwing knives and sharpening stone — knives as tools sheathed, not mid-throw pose with intent to shoot. Soft eyes.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Throwing knife bandolier (sheathed), whetstone, tool roll

## Phrases — AIM chat

### Offline
- RU: Дима... э-э... перезвоните. Я забыл зачем телефон.
- EN: This is Dimitri. Leave a message.

### GreetingAndOffer
- RU: А? Это я. Димитрий. Кажется.
- EN: Dimitri here. Talk.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Стой... куда я шёл?
- EN: Waiting on you.

### PartingWords
- RU: Так, ножи с собой... вроде все.
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
  - Selection: «Димитрий!» / «Dimitri!»
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
| Appearance | Dimitri |
| VoiceResponseId | Jazz_Dimitri |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Dimitri.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Dimitri_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm (or melee for knife mercs) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
