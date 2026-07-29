---
status: ready
priority: low
origin: wildfire
unit_id: Jazz_Grace
portrait_id: Grace
affiliation: AIM
role: Thrower
tier: Regular
specialization: Melee
gender: Female
nationality: USA
voice_source: wildfire
starting_level: 3
will: 45
salary:
  starting: 1600
  increase: 150
  lv1: 600
  max: 4000
medical_deposit: standard
haggling: normal
executable: true
---

# Грейс — Грациелла «Грейс» Джирелли

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Грациелла «Грейс» Джирелли | Graziella "Grace" Girelli |
| Nick | Грейс | Grace |
| AllCapsNick | ГРЕЙС | GRACE |
| Title | Итальянка | The Italian |
| Email | Grace@aim.com | Grace@aim.com |
| snype_nick | grace | grace |

## Bio

**RU:** Wildfire. Итальянка, записанная американкой. Боится тараканов, пессимистка. Средние статы броска (Сила 67, Меткость 69, Ловкость рук 77), Лидерство 62. Любит Аллика; недолюбливает Реда, Рикошета и Лаву.

**EN:** Wildfire mercenary. Italian-born, filed as American. Afraid of cockroaches, a pessimist. Modest throwing stats (67 Strength, 69 Marksmanship, 77 Dexterity), 62 Leadership. Fond of Allik; not fond of Red, Ricochet, or Lava.

## Stats

| Stat | Value |
| --- | --- |
| Health | 70 |
| Agility | 75 |
| Dexterity | 77 |
| Strength | 67 |
| Wisdom | 65 |
| Will | 45 |
| Leadership | 62 |
| Marksmanship | 69 |
| Mechanical | 20 |
| Explosives | 20 |
| Medical | 25 |
| MaxHitPoints | 70 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- `Jazz_Perk_Grace`
- `Throwing`
- `Pessimist`
- `FirstThrow`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Grace` |
| type | passive |
| DisplayName RU/EN | Точный бросок / Precise Toss |
| Description RU/EN | Первый брошенный за ход нож никогда не промахивается по ближней цели / The first knife Grace throws each turn never misses a nearby target |
| Mechanics | The first thrown-knife attack Grace makes each of her turns against a target within 4 tiles cannot miss (auto-hit), though it can still be Grazed by cover/armor as normal. |

## Personality

- Quirks: Zoophobic (cockroaches — nearest matching JA3 status), Pessimist
- Likes: `Jazz_Allik`
- Dislikes: `Red`, `Jazz_Ricochet`, `Lava`
- National hates: —
- Refusal / Haggle notes: refuses if Red or Jazz_Ricochet are in the active squad; haggles down (nervous, jumpy) when a live insect/vermin encounter has happened recently in-fiction — flavor only, no mechanical trigger; mitigation and rate discount when Jazz_Allik is hired

## Hire

- Access: AIM
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Grace` → `JAZZ_Grace50/35/25/20`
- *50: `JazzArmor_LeatherJacketBrn`, `Knife_Balanced`×3, `Knife_Sharpened`×2, `Machete`, `Knife`×2
- *35: `Knife_Balanced`×2, `Knife`×3, `MicroUZI`, `JAZZ_AMMO_9x19_FMJ`×16 (Double)
- *25: `Knife`×3, `Makarov`, `JAZZ_AMMO_9x18_FMJ`×12 (Double)
- *20: `Knife`×2, `SWModel10`, `JAZZ_AMMO_38special_FMJ`×8 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](grace.ja2-face.gif)

Файл: `grace.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `grace.ja2-face.gif` (same face identity). Italian-American woman, stylish but tactical, knife bandolier sheathed — NO gun. Pessimistic beauty.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Throwing knife bandolier, stylish scarf, AIM pin

## Phrases — AIM chat

### Offline
- RU: Грейс не в духе. Перезвоните.
- EN: Grace isn't in the mood. Call back.

### GreetingAndOffer
- RU: Грейс. Надеюсь, без тараканов.
- EN: Grace here. No cockroaches, I hope.

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Опять что-то пойдёт не так, вот увидите.
- EN: Something's bound to go wrong, you'll see.

### PartingWords
- RU: Ва-бене... я в деле.
- EN: Va bene... I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Хоть какая-то стабильность.
- EN: I'm staying. At least it's some stability.

### Refusals
- Red or Ricochet hired RU: Пока эти двое в отряде — забудьте.
- Red or Ricochet hired EN: Not while those two are on the team.
- Money RU: За эти деньги? Даже не думайте.
- Money EN: For that money? Don't even think about it.

### Haggles
- Money RU: Ладно, но с доплатой за нервы.
- Money EN: Fine, but with extra for my nerves.

### Mitigations
- Allik hired RU: Аллик уже здесь? Тогда, так и быть.
- Allik hired EN: Allik's already in? Then, fine, I'm in.

## Phrases — VoiceResponse

- `voice_source: wildfire` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Грейс готова.» / «Grace's ready.»
  - AimAttack (1): «Лови нож.» / «Catch the knife.»
  - AimAttack (2): «Прямо в цель.» / «Right on target.»
  - OpponentKilled: «Готово. Как и предчувствовала.» / «Done. Just as I feared.»
  - DeathGeneral: «Я так и знала...» / «I knew it...»
  - Downed: «Ранена! Ну конечно.» / «Hit! Of course.»
  - CombatStartDetected: «Началось. Как всегда некстати.» / «Here we go. Never good timing.»
  - LevelUp: «Может, не всё так плохо.» / «Maybe it's not all bad.»
  - AmmoLow: «Ножи заканчиваются.» / «Running low on knives.»
  - Idle: «Жду худшего.» / «Waiting for the worst.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Grace |
| VoiceResponseId | Jazz_Grace |
| pollyvoice | Amy |
| Portrait | Mod/Dv3mFVN/MercPortraits/Grace.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Grace_Big.png |
| CustomEquipGear | TryEquip Handheld A Melee/Throwing |
| FallbackMissingVR | Fox |
| Sources | AIM sheet «Наемники из JA1/2»; origin=wildfire |

## Open blockers

- none
