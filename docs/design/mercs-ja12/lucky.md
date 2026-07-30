---
status: ready
priority: low
origin: wildfire
unit_id: Jazz_Lucky
portrait_id: Lucky
affiliation: AIM
role: Autorifleman
tier: Veteran
specialization: Autoriflemen
gender: Male
nationality: France
voice_source: wildfire
starting_level: 4
will: 55
salary:
  starting: 1900
  increase: 150
  lv1: 700
  max: 4500
medical_deposit: small
haggling: normal
executable: true
---

# Лаки — Люк «Лаки» Фабр

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Люк «Лаки» Фабр | Luc "Lucky" Fabre |
| Nick | Лаки | Lucky |
| AllCapsNick | ЛАКИ | LUCKY |
| Title | Бельгиец | The Belgian |
| Email | Lucky@aim.com | Lucky@aim.com |
| snype_nick | lucky | lucky |

## Bio

**RU:** Wildfire. Бельгиец-франкофон, ошибочно записанный французом. Статы 75–80, Лидерство 58, Меткость 88. Любит Барри; недолюбливает Вишеса и Банса.

**EN:** Wildfire mercenary. A French-speaking Belgian mistakenly filed as French. Stats in the 75-80 range, 58 Leadership, 88 Marksmanship. Fond of Barry; not fond of Vicious or Buns.

## Stats

| Stat | Value |
| --- | --- |
| Health | 78 |
| Agility | 75 |
| Dexterity | 75 |
| Strength | 75 |
| Wisdom | 70 |
| Will | 55 |
| Leadership | 58 |
| Marksmanship | 88 |
| Mechanical | 30 |
| Explosives | 25 |
| Medical | 25 |
| MaxHitPoints | 78 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- `Jazz_Perk_Lucky`
- `AutoWeapons`
- `MartialArts`
- `Hotblood`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Lucky` |
| type | passive |
| DisplayName RU/EN | Второе дыхание / Second Wind |
| Description RU/EN | Раз за бой промах Лаки превращается в попадание / Once per combat, a Lucky miss becomes a hit |
| Mechanics | Once per combat, the first time an attack roll made by Lucky would miss, it is instead treated as a hit (rolled at minimum-success damage). Recharges at the start of the next combat. |

## Personality

- Quirks: —
- Likes: `Barry`
- Dislikes: `Jazz_Vicious`, `Buns`
- National hates: —
- Refusal / Haggle notes: refuses if Jazz_Vicious or Buns are in the active squad; mitigation and rate discount when Barry is hired

## Hire

- Access: AIM
- MedicalDeposit: small; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Lucky` → `JAZZ_Lucky50/35/25/20`
- *50: `JazzArmor_LeatherJacketBrn`, `FAMAS`, `JAZZ_AMMO_556_FMJ`×60 (Double), `Knife`
- *35: `M2Carbine`, `JAZZ_AMMO_30_FMJ`×40 (Double), `Knife`
- *25: `AK47`, `JAZZ_AMMO_762x39_FMJ`×32 (Double)
- *20: `Winchester1894`, `JAZZ_AMMO_30_P`×20 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](lucky.ja2-face.gif)

Файл: `lucky.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `lucky.ja2-face.gif` (same face identity). Lucky Belgian-French auto trooper, grin, ammo pouches and knuckle wrap — NO gun.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Ammo pouches, knuckle wrap, lucky coin

## Phrases — AIM chat

### Offline
- RU: Лаки недоступен. Перезвоните.
- EN: Lucky's unavailable. Call back.

### GreetingAndOffer
- RU: Лаки на связи!
- EN: Lucky here!

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Ха! Удача любит смелых.
- EN: Ha! Fortune favors the bold.

### PartingWords
- RU: Allons-y! Я в деле.
- EN: Allons-y! I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Удача со мной.
- EN: I'm staying. Luck's on my side.

### Refusals
- Vicious or Buns hired RU: Пока эти двое в отряде — даже не звоните.
- Vicious or Buns hired EN: Not while those two are on the team.
- Money RU: За такую мелочь? Non merci.
- Money EN: For chump change? Non merci.

### Haggles
- Money RU: Договоримся, но по-честному.
- Money EN: Let's make a deal, but a fair one.

### Mitigations
- Barry hired RU: Барри уже в деле? Тогда я тоже, mon ami.
- Barry hired EN: Barry's already in? Then count me in too, mon ami.

## Phrases — VoiceResponse

- `voice_source: wildfire` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Лаки готов.» / «Lucky's ready.»
  - AimAttack (1): «Удача со мной!» / «Luck's with me!»
  - AimAttack (2): «Держись крепче!» / «Hold tight!»
  - OpponentKilled: «Voila!» / «Voila!»
  - DeathGeneral: «Удача отвернулась...» / «Luck ran out...»
  - Downed: «Ранен! Не повезло.» / «Hit! No luck this time.»
  - CombatStartDetected: «Противник заметил нас.» / «Enemy spotted us.»
  - LevelUp: «Удача плюс мастерство.» / «Luck plus skill.»
  - AmmoLow: «Патроны на исходе.» / «Running low on ammo.»
  - Idle: «Жду удачного момента.» / «Waiting for a lucky break.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Lucky |
| VoiceResponseId | Jazz_Lucky |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Lucky.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Lucky_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm (two-handed auto) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=wildfire |

## Open blockers

- none
