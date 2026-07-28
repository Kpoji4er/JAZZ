---
status: planned
priority: high
origin: ja2
unit_id: Jazz_Blade
portrait_id: Blade
affiliation: MERC
role: Scout
tier: Veteran
specialization: Melee
gender: Male
nationality: USA
voice_source: ja2
starting_level: 4
will: 55
salary:
  starting: 900
  increase: 200
  lv1: 400
  max: 2500
medical_deposit: standard
haggling: normal
executable: false
---

# Бритва — Билл «Бритва» Ламонт

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Билл «Бритва» Ламонт | Билл «Бритва» Ламонт |
| Nick | Бритва | Blade |
| AllCapsNick | БРИТВА | BLADE |
| Title | Нож не кончается | Нож не кончается |
| Email | Blade@merc.com | Blade@merc.com |
| snype_nick | sharpstuff | sharpstuff |

## Bio

**RU:** Бриллиант среди MERC. Статы 80–90, навыки около нуля — но в ноже «патроны» не кончаются. Псих. Дружит с Фиделем и Нервным; не любит Бифа, Фло, Арулько.

**EN:** EN draft: translate Bio RU at generation; keep tone.

## Stats

| Stat | Value |
| --- | --- |
| Health | 88 |
| Agility | 90 |
| Dexterity | 85 |
| Strength | 80 |
| Wisdom | 53 |
| Will | 55 |
| Leadership | 20 |
| Marksmanship | 50 |
| Mechanical | 0 |
| Explosives | 5 |
| Medical | 5 |
| MaxHitPoints | 88 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Blade`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Blade` |
| type | passive |
| DisplayName RU/EN | Ураган клинков / Ураган клинков |
| Description RU/EN | Усиленный charge и бойня / Усиленный charge и бойня |
| Mechanics | Предпочтительно оба: (1) Charge на любое оружие, увеличенная дистанция; (2) Бойня +20% CTH, 0 шанса крита. Psycho quirk. |

## Personality

- Quirks: Psycho
- Likes: Fidel, Jazz_Nervous
- Dislikes: Biff, Flo
- National hates: Arulco locals
- Refusal / Haggle notes: Aggressive hire

## Hire

- Access: MERC roster
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Blade`
- Presets (weights ~50/35/25/20):
  - *50: multiple combat knives, light stealth armor, medkit small
  - no primary firearm focus

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](blade.ja2-face.gif)

Файл: `blade.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `blade.ja2-face.gif` (same face identity). Wiry intense American knife fighter, shaved temples, manic grin held back, tactical harness with multiple sheathed knives and whetstone — NO gun. Chaotic energy.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Knife sheaths, whetstone, blood-kit pouch, MERC patch

## Phrases — AIM chat

### Offline
- RU: Бритва занят. Пиши.
- EN: This is Blade. Leave a message.

### GreetingAndOffer
- RU: Чо надо? Резать будем?
- EN: Blade here. Talk.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Ножницы тупые — ножи нет.
- EN: Waiting on you.

### PartingWords
- RU: Я уже в пути, хе-хе.
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
  - Selection: «Бритва!» / «Blade!»
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
| Appearance | Blade |
| VoiceResponseId | Jazz_Blade |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Blade.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Blade_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm (or melee for knife mercs) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
