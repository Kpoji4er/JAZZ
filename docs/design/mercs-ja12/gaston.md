---
status: ready
priority: medium
origin: ub
unit_id: Jazz_Gaston
portrait_id: Gaston
affiliation: MERC
role: Sniper
tier: Elite
specialization: Marksmen
gender: Male
nationality: France
voice_source: ub
starting_level: 5
will: 70
salary:
  starting: 2500
  increase: 200
  lv1: 1000
  max: 6000
medical_deposit: small
haggling: normal
executable: true
---

# Гастон — Гастон Кавалье

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Гастон Кавалье | Gaston Cavalier |
| Nick | Гастон | Gaston |
| AllCapsNick | ГАСТОН | GASTON |
| Title | Дамский снайпер | The Ladies' Sniper |
| Email | Gaston@merc.com | Gaston@merc.com |
| snype_nick | cavalier | cavalier |

## Bio

**RU:** Urban Brawl. Статы 80–90, Marksmanship 94, прочие навыки 20+. Не умеет плавать (флейвор). Работает с крыш и в темноте, флиртует с Тоской, Бансом и Лиской. Не выносит Злобного за конкуренцию по части дам и Биффа за трусость.

**EN:** Urban Brawl. Stats in the 80-90 range, 94 Marksmanship, other skills 20+. Can't swim (flavor only). Works rooftops and nighttime hours, flirts with Tosca, Buns, and Fox. Can't stand Vicious (rival for the ladies) or Biff's cowardice.

## Stats

| Stat | Value |
| --- | --- |
| Health | 85 |
| Agility | 80 |
| Dexterity | 85 |
| Strength | 75 |
| Wisdom | 70 |
| Will | 70 |
| Leadership | 40 |
| Marksmanship | 94 |
| Mechanical | 25 |
| Explosives | 20 |
| Medical | 20 |
| MaxHitPoints | 85 |
| StartingLevel | 5 |

## Perks

### StartingPerks

- `Jazz_Perk_Gaston`
- `TakeAim`
- `Deadeye`
- `NightOps`
- `SteadyBreathing`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Gaston` |
| type | passive |
| DisplayName RU/EN | Крыша / The Rooftop |
| Description RU/EN | Бонус к попаданию со стрельбы с крыш ночью / Accuracy bonus for rooftop shots at night |
| Mechanics | +15 to CTH when Gaston fires from an elevated tile (roof or 2nd floor and above). At night, he additionally ignores the reduced-visibility accuracy penalty entirely while positioned on such an elevated tile. |

## Personality

- Quirks: CannotSwim (flavor only — JA3 has no swim system, not implemented as a StartingPerk or hire condition), Womanizer
- Likes: `Jazz_Buzz`, `Buns`, `Fox` (flirts with all three)
- Dislikes: `Jazz_Vicious` (medium wave — Refusal wiring live once both are generated together), `Jazz_Biff` (medium wave — Refusal wiring live once both are generated together)
- National hates: —
- Refusal / Haggle notes: refuses if Vicious or Biff hired; standard MERC money/death-toll refusals; mitigation if Buzz, Buns, or Fox hired

## Hire

- Access: MERC roster (Urban Brawl origin)
- MedicalDeposit: small; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Gaston` → `JAZZ_Gaston50/35/25/20`
- *50: `JazzArmor_LeatherJacketBlk`, `DragunovSVD`, `JAZZ_AMMO_762x51_Match`×20 (Double), `JAZZ_CombatScope_2x`
- *35: `JazzArmor_LeatherJacketBlk`, `Springfield`, `JAZZ_AMMO_3006_Match`×20 (Double)
- *25: `JazzArmor_LeatherJacketBrn`, `Mini14`, `JAZZ_AMMO_556_FMJ`×40 (Double)
- *20: `JazzArmor_LeatherJacketBrn`, `Mini14`, `JAZZ_AMMO_556_FMJ`×30 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](gaston.ja2-face.jpg)

Файл: `gaston.ja2-face.jpg`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `gaston.ja2-face.jpg` (same face identity). Suave French sniper ~35, silk scarf, spotting scope on chest harness — NO rifle. Charming smile.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Spotting scope pouch, scarf, rooftop climbing gloves, rangefinder

## Phrases — AIM chat

### Offline
- RU: Гастон у дамы. Пишите, отвечу, когда освобожусь.
- EN: Gaston's with a lady. Leave a message, I'll answer when I'm free.

### GreetingAndOffer
- RU: Gaston à l'appareil. Слушаю ваше предложение.
- EN: Gaston à l'appareil. I'm listening to your offer.

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Ну же, время дорого — как и мой шарм.
- EN: Come on, time's precious — just like my charm.

### PartingWords
- RU: Pour vous — всегда готов. Беру винтовку.
- EN: Pour vous — always ready. Grabbing my rifle.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем, mon ami?
- EN: Contract's ending. Extending, mon ami?

### RehireOutro
- RU: Остаюсь. Крыши здесь превосходные.
- EN: I'm staying. The rooftops here are superb.

### Refusals
- Vicious/Biff hired RU: Пока Злобный или Бифф в отряде — нет. Один отбивает моих дам, другой портит настроение.
- Vicious/Biff hired EN: Not while Vicious or Biff are on the team. One steals my ladies, the other ruins the mood.
- Death toll RU: Слишком много потерь для моего вкуса.
- Death toll EN: Too many losses for my taste.

### Mitigations
- Buzz/Buns/Fox hired RU: О, Тоска, Банс или Лиска уже здесь? Тогда я определённо в деле.
- Buzz/Buns/Fox hired EN: Oh, Buzz, Buns, or Fox is already in? Then I'm definitely in.

### ExtraPartingWords
- RU: Если ищете ещё одну прекрасную даму — зовите Тоску.
- EN: If you're looking for another lovely lady — call Buzz.

## Phrases — VoiceResponse

- `voice_source: ub` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Гастон готов.» / «Gaston's ready.»
  - AimAttack (1): «Цель на мушке.» / «Target in my sights.»
  - AimAttack (2): «С крыши виднее.» / «Better view from the roof.»
  - OpponentKilled: «Voilà.» / «Voilà.»
  - DeathGeneral: «Недостойный конец для такого шарма...» / «An unworthy end for such charm...»
  - Downed: «Ранен, но всё ещё элегантен.» / «Hit, but still elegant.»
  - CombatStartDetected: «Внимание, гости прибыли.» / «Careful, we have guests.»
  - LevelUp: «Точность растёт, как и моя слава.» / «My aim improves, as does my fame.»
  - AmmoLow: «Патроны на исходе.» / «Running low on ammo.»
  - Idle: «Жду подходящего момента.» / «Waiting for the right moment.»
  - MockDislike (Vicious/Biff): «Только бы Злобный не мешал моим планам.» / «Just hope Vicious doesn't cramp my style.»
  - Praises (Buzz/Buns/Fox present): «С такой компанией и бой приятнее.» / «Even a firefight's nicer with this company.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Gaston |
| VoiceResponseId | Jazz_Gaston |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Gaston.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Gaston_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ub |

## Open blockers

- none
