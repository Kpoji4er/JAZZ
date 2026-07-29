---
status: ready
priority: low
origin: ja2
unit_id: Jazz_Cord
portrait_id: Cord
affiliation: MERC
role: Mechanic
tier: Regular
specialization: Mechanic
gender: Male
nationality: USA
voice_source: ja2
starting_level: 3
will: 40
salary:
  starting: 550
  increase: 150
  lv1: 250
  max: 1800
medical_deposit: standard
haggling: normal
executable: true
---

# Кардан — Даг «Кардан» Милтон

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Даг «Кардан» Милтон | Doug "Cord" Milton |
| Nick | Кардан | Cord |
| AllCapsNick | КАРДАН | CORD |
| Title | Забывчивый механик | The Forgetful Mechanic |
| Email | Cord@merc.com | Cord@merc.com |
| snype_nick | cardan | cardan |

## Bio

**RU:** Статы 60–70, Dexterity 89, Wisdom 49, Marksmanship 44, Mechanical 82. Забывчив — по слухам из JA2, забывает часть навыков после долгой работы, но JAZZ не реализует это механически, только в биографии. Неровно дышит к Вики; не любит Ивана и Игоря; недолюбливает русских.

**EN:** Stats in the 60-70 range, 89 Dexterity, 49 Wisdom, 44 Marksmanship, 82 Mechanical. Forgetful — JA2 rumor has him losing bits of skill after long jobs, but JAZZ keeps that as flavor only, not a mechanic. Has an unrequited crush on Vicki; can't stand Ivan or Igor; not fond of Russians.

## Stats

| Stat | Value |
| --- | --- |
| Health | 65 |
| Agility | 60 |
| Dexterity | 89 |
| Strength | 60 |
| Wisdom | 49 |
| Will | 40 |
| Leadership | 15 |
| Marksmanship | 44 |
| Mechanical | 82 |
| Explosives | 15 |
| Medical | 10 |
| MaxHitPoints | 65 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- `Jazz_Perk_Cord`
- `MrFixit`
- `JackOfAllTrades`
- `Scoundrel`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Cord` |
| type | passive |
| DisplayName RU/EN | Тихий ремонт / Quiet Repair |
| Description RU/EN | Ремонт обходится быстрее и дешевле / Repairs go faster and cost less |
| Mechanics | Repair actions performed by Cord cost 15% less time and 10% fewer Parts. |

## Personality

- Quirks: Forgetful (bio flavor only — reverse-skill-drain JA2 quirk not implemented mechanically)
- Likes: `Vicki` (one-sided, unrequited)
- Dislikes: `Ivan`, `Igor`
- National hates: Russians — Haggle trigger when the active squad is full of Russian-nationality mercs
- Refusal / Haggle notes: refuses if Ivan or Igor hired; haggles when squad is all-Russian; standard AIM money refusal

## Hire

- Access: MERC hire
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Cord` → `JAZZ_Cord50/35/25/20`
- *50: `JazzArmor_LeatherArmor`, `Lockpick`, `Wirecutter`, `TT33`, `JAZZ_AMMO_762x25_FMJ`×24 (Double), `Parts`×15
- *35: `Lockpick`, `Makarov`, `JAZZ_AMMO_9x18_FMJ`×16 (Double), `Parts`×10
- *25: `Lockpick`, `SWModel10`, `JAZZ_AMMO_38special_FMJ`×12 (Double)
- *20: `Lockpick`, `Unarmed`

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](cord.ja2-face.gif)

Файл: `cord.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `cord.ja2-face.gif` (same face identity). Forgetful mechanic ~35, grease-stained coveralls, blank distracted look, worn toolbag — NO gun.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Toolbag, lockpicks, grease rag

## Phrases — AIM chat

### Offline
- RU: Кардан... куда я дел телефон... перезвоните.
- EN: This is Cord. Leave a message.

### GreetingAndOffer
- RU: А? Кардан слушает. Что чинить?
- EN: Cord here. What needs fixing?

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Что мы вообще делали?
- EN: What were we doing again?

### PartingWords
- RU: Кажется, я согласился. Иду.
- EN: I think I agreed. I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Кажется.
- EN: I'm staying. I think.

### Refusals
- Ivan/Igor hired RU: Пока Иван или Игорь в отряде — я пас.
- Ivan/Igor hired EN: Not while Ivan or Igor are on the team.
- Money RU: Маловато будет.
- Money EN: That's not quite enough.

### Haggles
- Russian mercs hired RU: Отряд полон русских... ладно, но с доплатой.
- Russian mercs hired EN: Squad's full of Russians... fine, but it'll cost extra.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Кардан на месте.» / «Cord's here.»
  - AimAttack (1): «Ну, попробуем.» / «Well, let's try.»
  - AimAttack (2): «Куда я целился?» / «What was I aiming at?»
  - OpponentKilled: «О, получилось.» / «Oh, that worked.»
  - DeathGeneral: «Забыл увернуться...» / «Forgot to dodge...»
  - Downed: «Меня зацепило, кажется.» / «I think I'm hit.»
  - CombatStartDetected: «О, кто-то пришёл.» / «Oh, someone's here.»
  - LevelUp: «О, я что-то запомнил!» / «Oh, I remembered something!»
  - AmmoLow: «Патроны кончаются.» / «Running low on ammo.»
  - Idle: «Что дальше?» / «What now?»
  - MockDislike (Ivan/Igor): «Хорошо, что этих двоих тут нет.» / «Good thing those two aren't here.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Cord |
| VoiceResponseId | Jazz_Cord |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Cord.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Cord_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
