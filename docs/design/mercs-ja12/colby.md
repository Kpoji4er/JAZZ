---
status: ready
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
executable: true
---

# Колби — Тревор Колби

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Тревор Колби | Trevor Colby |
| Nick | Колби | Colby |
| AllCapsNick | КОЛБИ | COLBY |
| Title | Ловушечник | The Tripwire |
| Email | Colby@aim.com | Colby@aim.com |
| snype_nick | tripwire | tripwire |

## Bio

**RU:** Боевой подрывник и ловушечник AIM. Лютые физикалы (кроме силы/подвижности), 99 механики, 88 взрывчатки. Дружит с Тором, не дружит с Фиделем; не любит американцев.

**EN:** AIM combat demolitions and trap specialist. Brutal physicals (except Strength/Agility), 99 Mechanical, 88 Explosives. Friends with Thor, clashes with Fidel; does not like Americans.

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

- `Jazz_Perk_Colby`
- `MrFixit`
- `Throwing`
- `BreachAndClear`
- `HitTheDeck`
- `DesignerExplosives`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Colby` |
| type | passive |
| DisplayName RU/EN | Цепная паника / Chain Panic |
| Description RU/EN | Взрывы Колби сеют панику: +20% к радиусу и 20% шанс паники у раненых врагов в зоне / Colby's blasts sow panic: +20% blast radius and 20% chance to panic wounded enemies in the blast |
| Mechanics | Каждый взрыв, инициированный Колби (граната/миномёт/C4/бочка/мина/чужая бомба выстрелом): 20% шанс паники у раненых врагов в радиусе; +20% к радиусу взрывов. |

## Personality

- Quirks: —
- Likes: Thor
- Dislikes: Fidel
- National hates: Americans (Haggle when hired USA-nationality mercs present)
- Refusal / Haggle notes: Fidel hired; death toll; money; USA-nationality haggle; Thor mitigation

## Hire

- Access: AIM hire
- MedicalDeposit: large; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Colby` → `JAZZ_Colby50/35/25/20` (weights 50k/35k/25k/20k)
- *50: `ShapedCharge`×2, `C4`×2, `Lockpick`, `SmokeGrenade`×2, `JazzArmor_LeatherVest`, `MP5A4`, `JAZZ_AMMO_9x19_FMJ`×60, `Combination_Detonator_Remote`
- *35: `ShapedCharge`×1, `C4`×1, `Lockpick`, `SmokeGrenade`×1, `JazzArmor_LeatherVest`, `MPL`, `JAZZ_AMMO_9x19_FMJ`×40, `Combination_Detonator_Time`
- *25: `C4`×1, `SmokeGrenade`×1, `JazzArmor_PoliceVest`, `UZI`, `JAZZ_AMMO_9x19_FMJ`×30
- *20: `PipeBomb`×1, `JazzArmor_PoliceVest`, `UZI`, `JAZZ_AMMO_9x19_FMJ`×20

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
- EN: This is Colby. Leave a message. I'll call back if I don't blow myself up.

### GreetingAndOffer
- RU: Колби на линии. Что взрываем?
- EN: Colby here. What are we blowing up?

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Время тикает.
- EN: Waiting on you. Clock's ticking.

### PartingWords
- RU: Беру зарядку и выхожу.
- EN: Grabbing charges. I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь.
- EN: I'm staying.

### Refusals
- Fidel hired RU: Нет. Пока Фидель на контракте — я пас. Не хочу делить периметр с психом.
- Fidel hired EN: No. Not while Fidel's on the payroll. I don't share a perimeter with that psycho.
- Death toll RU: Слишком много трупов на вашем счету. Наймите кого-то другого.
- Death toll EN: Too many bodies on your ledger. Hire someone else.
- Money RU: Кошелёк тонкий. Перезвоните, когда будет бюджет на нормальную зарядку.
- Money EN: Wallet's light. Call when you can afford a proper charge kit.

### Haggles
- USA mercs hired RU: Американцы в отряде… Ладно, но надбавка за нервы.
- USA mercs hired EN: Americans on the squad… Fine, but I want a hazard bump for my nerves.

### Mitigations
- Thor hired RU: Тор уже с вами? Тогда ок. С ним я работаю.
- Thor hired EN: Thor's already with you? Then I'm in. I work with him.

### ExtraPartingWords
- RU: Если нужен ещё один спокойный спец — берите Тора.
- EN: If you need another steady specialist — grab Thor.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts:
  - Selection: «Колби!» / «Colby!»
  - AimAttack: «На мушке.» / «On target.»
  - OpponentKilled: «Готово.» / «Done.»
  - DeathGeneral: «Чёрт...» / «Damn...»
  - Downed: «Меня подбили!» / «I'm hit!»
  - CombatStartPlayer: «В бой.» / «Engage.»
  - LevelUp: «Ещё лучше.» / «Getting better.»
  - AmmoLow: «Патроны!» / «Ammo!»
  - Idle: «Жду.» / «Waiting.»
  - DeathBuddy (Thor): «Тор!..» / «Thor!..»
  - MockDislike (Fidel): «Как обычно, Фидель.» / «Typical Fidel.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Colby |
| VoiceResponseId | Jazz_Colby |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Colby.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Colby_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none

## Shipped paths

- UnitData: `jazz-units/UnitData/Jazz_Colby.lua`
- Named perk: `jazz/CharacterEffect/Jazz_Perk_Colby.lua`
- Loot: `Loot_JAZZ_Colby` / `JAZZ_Colby50/35/25/20` (`jazz-units/items.lua`)
- Appearance: `Colby` (`jazz-units/items.lua`)
- Portraits: `jazz-units/MercPortraits/Colby.png`, `Colby_Big.png`
- Localization: `890000000001700`–`890000000001732` (`jazz/Russian.csv`, `jazz/English.csv`)
- Combat hooks: `jazz/Code/System_OR_Grenade.lua` (+20% radius), perk `OnCalcDamageAndEffects` (20% Panicked on wounded enemies in explosion)
