---
status: ready
priority: high
origin: ja2
unit_id: Jazz_Conrad
portrait_id: Conrad
affiliation: MERC
role: Commander
tier: Elite
specialization: Leader
gender: Male
nationality: Germany
voice_source: ja2
starting_level: 5
will: 75
salary:
  starting: 3300
  increase: 200
  lv1: 2000
  max: 8000
medical_deposit: large
haggling: high
executable: true
---

# Конрад — Лейтенант Конрад Джиллет

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Лейтенант Конрад Джиллет | Lieutenant Conrad Gillett |
| Nick | Конрад | Conrad |
| AllCapsNick | КОНРАД | CONRAD |
| Title | Дорогой лейтенант | The Costly Lieutenant |
| Email | Conrad@merc.com | Conrad@merc.com |
| snype_nick | ltgillett | ltgillett |

## Bio

**RU:** Сильнейший из доступных местных наёмников: статы 75–80, Leadership 51 и полноценный инструктор, Marksmanship 95. Дружит с Игги и Стефаном; терпеть не может пьяного Ларри; не умеет плавать (флейвор). Дорог — берёт заметно выше рынка и торгуется жёстко.

**EN:** The strongest local hire on offer: stats in the 75-80 range, Leadership 51 with a full training set, 95 Marksmanship. Friends with Iggy and Stefan; can't stand a drunk Larry; never learned to swim (flavor only). Expensive — charges well above market and haggles hard.

## Stats

| Stat | Value |
| --- | --- |
| Health | 80 |
| Agility | 69 |
| Dexterity | 78 |
| Strength | 78 |
| Wisdom | 80 |
| Will | 75 |
| Leadership | 51 |
| Marksmanship | 95 |
| Mechanical | 55 |
| Explosives | 68 |
| Medical | 40 |
| MaxHitPoints | 80 |
| StartingLevel | 5 |

## Perks

### StartingPerks

- `Jazz_Perk_Conrad`
- `Teacher`
- `TakeAim`
- `SteadyBreathing`
- `ShoulderToShoulder`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Conrad` |
| type | passive |
| DisplayName RU/EN | Строгий инструктор / The Strict Instructor |
| Description RU/EN | Конрад всегда тренирует на полной скорости и не теряет темп рядом с другими инструкторами / Conrad always trains at full speed and never loses pace next to other trainers |
| Mechanics | Resolves the vanilla multi-`Teacher` stacking penalty for Conrad specifically: when two or more `Teacher`-perk mercs share a squad/sector, Conrad's own training contribution is exempt from the diminishing-return halving that would otherwise apply to the second-and-later trainer. Other trainers in the same squad are unaffected and still halve normally. |

## Personality

- Quirks: "can't swim" — flavor only in Bio/AIM chat; JA3 has no swim system, so this is not a StartingPerk or hire condition
- Likes: Iggy, `Jazz_Rothman` (both planned mercs — Mitigation/ExtraPartingWords wiring activates once each reaches `status: ready`; Iggy specifically needs its own article added to the queue before wiring)
- Dislikes: Larry (vanilla merc, "drugged/drunk" flavor — refuses if Larry hired)
- National hates: Americans — Haggle trigger (see below), same pattern as Colby
- Refusal / Haggle notes: refuses if Larry hired; haggles hard on money and on squads full of Americans

## Hire

- Access: Locals during the Arulco campaign, transitions to MERC roster afterward once the campaign concludes (flavor-only affiliation change, same unit)
- MedicalDeposit: large; Haggling: high; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Conrad` → `JAZZ_Conrad50/35/25/20`
- *50: `JazzArmor_Uniform`, `Springfield`, `JAZZ_AMMO_3006_Match`×20 (Double), `FirstAidKit`, `Meds`×20
- *35: `JazzArmor_Uniform`, `M16A1`, `JAZZ_AMMO_556_FMJ`×60 (Double)
- *25: `JazzArmor_LeatherJacketBrn`, `FNFAL`, `JAZZ_AMMO_762x51_FMJ`×40 (Double)
- *20: `JazzArmor_LeatherJacketBrn`, `AK47`, `JAZZ_AMMO_762x39_FMJ`×60 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](conrad.ja2-face.gif)

Файл: `conrad.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `conrad.ja2-face.gif` (same face identity). Fit German ex-officer ~40, neat hair, officer field jacket with instructor tabs and binoculars on chest — NO rifle. Stern professional.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Instructor tabs, binoculars, map case, whistle

## Phrases — AIM chat

### Offline
- RU: Лейтенант Джиллет. Оставьте сообщение — отвечу, если условия того стоят.
- EN: Lieutenant Gillett. Leave a message — I'll respond if the terms are worth it.

### GreetingAndOffer
- RU: Джиллет слушает. Излагайте условия — и не жадничайте.
- EN: Gillett listening. State your terms — and don't be cheap.

### ConversationRestart
- RU: Связь прервалась. Продолжим — время дорого, как и я.
- EN: Line dropped. Let's continue — time is money, same as me.

### IdleLine
- RU: Время — деньги. Моё особенно.
- EN: Time is money. Mine especially.

### PartingWords
- RU: Контракт принят. Постройте людей — начинаем с дисциплины.
- EN: Contract accepted. Line your people up — we start with discipline.

### RehireIntro
- RU: Контракт заканчивается. У меня есть и другие предложения — решайте.
- EN: Contract's ending. I have other offers on the table — decide.

### RehireOutro
- RU: Остаюсь. Ваша дисциплина меня почти впечатлила.
- EN: I'm staying. Your discipline almost impressed me.

### Refusals
- Larry hired RU: Пока пьяный Ларри в отряде — я не подписываюсь. Это не армия, а балаган.
- Larry hired EN: Not while drunk Larry's on the roster. That's not an army, that's a circus.

### Haggles
- Money RU: Моя ставка не обсуждается — разве что в большую сторону.
- Money EN: My rate isn't negotiable — except upward.
- USA mercs hired RU: Отряд полон американцев. Ясно, доплата за акцент, который приходится терпеть.
- USA mercs hired EN: Your squad's full of Americans. Fine, surcharge for the accent I have to tolerate.

### Mitigations
- Iggy/Rothman hired RU: Игги или Ротман уже здесь? Тогда условия меня устраивают.
- Iggy/Rothman hired EN: Iggy or Rothman already in? Then the terms are acceptable.

### ExtraPartingWords
- RU: Наймите ещё Игги — с толковым напарником дисциплина держится сама.
- EN: Hire Iggy as well — discipline holds itself with a competent partner around.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Лейтенант Джиллет, к вашим услугам.» / «Lieutenant Gillett, at your service.»
  - AimAttack (1): «Цель захвачена.» / «Target acquired.»
  - AimAttack (2): «Точность прежде всего.» / «Precision above all.»
  - OpponentKilled: «Учебная цель поражена.» / «Training target eliminated.»
  - DeathGeneral: «Недостойный конец...» / «An unworthy end...»
  - Downed: «Ранен. Требую медицинской помощи.» / «Wounded. I require medical attention.»
  - CombatStartDetected: «Внимание, противник обнаружен.» / «Attention, enemy detected.»
  - LevelUp: «Дисциплина приносит плоды.» / «Discipline bears fruit.»
  - AmmoLow: «Боезапас на исходе.» / «Ammunition running low.»
  - Idle: «Жду распоряжений.» / «Awaiting orders.»
  - MockDislike (Larry): «Хоть бы Ларри протрезвел когда-нибудь.» / «I do wish Larry would sober up someday.»
  - Praises (Iggy/Rothman present): «С надёжным напарником и служба легче.» / «Service is easier with a reliable partner.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Conrad |
| VoiceResponseId | Jazz_Conrad |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Conrad.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Conrad_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
