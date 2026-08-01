---
status: ready
priority: medium
origin: wildfire
unit_id: Jazz_Allik
portrait_id: Allik
affiliation: AIM
role: AllRounder
tier: Elite
specialization: AllRounder
gender: Male
nationality: Estonia
voice_source: wildfire
starting_level: 5
will: 80
salary:
  starting: 2600
  increase: 200
  lv1: 1100
  max: 6000
medical_deposit: small
haggling: normal
executable: true
---

# Знаток — Янно «Знаток» Аллик

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Янно «Знаток» Аллик | Jaano "Allik" Allikas |
| Nick | Знаток | Allik |
| AllCapsNick | ЗНАТОК | ALLIK |
| Title | Эстонец | The Estonian |
| Email | Allik@aim.com | Allik@aim.com |
| snype_nick | znatok | znatok |

## Bio

**RU:** Wildfire. Один из лучших показателей статов на уровень в игре. Marksmanship 78, Mechanical 76, Explosives 43. Неисправимый оптимист, ко всему подходит с расчётом инженера. Дружит с Вильде и Грейс; не ладит с Сидни и Доктором Кью. В некоторых файлах WF указан русским по ошибке — считается артефактом данных, национальность эстонская.

**EN:** Wildfire. One of the best stat-per-level ratios in the game. 78 Marksmanship, 76 Mechanical, 43 Explosives. An incurable optimist who approaches everything like an engineer. Friends with Vilde and Grace; doesn't get along with Sidney or Dr.Q. Some Wildfire files mislabel him as Russian — treated as a data artifact; his actual nationality is Estonian.

## Stats

| Stat | Value |
| --- | --- |
| Health | 88 |
| Agility | 85 |
| Dexterity | 85 |
| Strength | 80 |
| Wisdom | 85 |
| Will | 80 |
| Leadership | 50 |
| Marksmanship | 78 |
| Mechanical | 76 |
| Explosives | 43 |
| Medical | 30 |
| MaxHitPoints | 88 |
| StartingLevel | 5 |

## Perks

### StartingPerks

- `Jazz_Perk_Allik`
- `MrFixit`
- `TrueGrit`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Allik` |
| type | passive |
| DisplayName RU/EN | Знаток дела / Jack of All Trades |
| Description RU/EN | Быстрее прокачивается благодаря разностороннему опыту / Levels up faster thanks to well-rounded experience |
| Mechanics | Allik gains +15% experience from any non-combat skill check he succeeds (Mechanical, Explosives, Medical), on top of normal combat XP, reflecting his balanced stat spread and engineer's mindset. |

## Personality

- Quirks: Optimist
- Likes: `Jazz_Vilde`, `Jazz_Grace` (both already generated — Mitigation/ExtraPartingWords wiring live immediately)
- Dislikes: `Sidney`, `DrQ` (both vanilla merc ids, already shipped — Refusal wiring live immediately)
- National hates: none — the WF-sheet "Russian" tag is treated as a data artifact and dropped in favor of his documented Estonian nationality
- Refusal / Haggle notes: refuses if Sidney or DrQ hired; standard AIM money/death-toll refusals; mitigation if Vilde or Grace hired

## Hire

- Access: AIM roster (Wildfire origin)
- MedicalDeposit: small; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Allik` → `JAZZ_Allik50/35/25/20`
- *50: `JazzArmor_LeatherArmor`, `Sig550`, `JAZZ_AMMO_556_FMJ`×60 (Double), `Lockpick`, `Parts`×10, `ShapedCharge`×1
- *35: `JazzArmor_LeatherArmor`, `Sig550`, `JAZZ_AMMO_556_FMJ`×40 (Double), `Parts`×5
- *25: `JazzArmor_LeatherJacketBrn`, `Mini14`, `JAZZ_AMMO_556_FMJ`×40 (Double)
- *20: `JazzArmor_LeatherJacketBrn`, `Mini14`, `JAZZ_AMMO_556_FMJ`×30 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](allik.ja2-face.gif)

Файл: `allik.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `allik.ja2-face.gif` (same face identity). Competent Estonian all-rounder ~35, neat gear, multi-tool and lockpick case — NO gun. Calm, optimistic expression.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Lockpick case, multi-tool, small notebook, AIM pin

## Phrases — AIM chat

### Offline
- RU: Знаток занят делом. Позже.
- EN: Allik's busy with something. Later.

### GreetingAndOffer
- RU: Аллик слушает. Что за задача?
- EN: Allik here. What's the job?

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Готов к работе, только скажите.
- EN: Ready to work, just say the word.

### PartingWords
- RU: Выхожу. Будет интересно.
- EN: Moving out. This'll be interesting.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Тут ещё многому можно научиться.
- EN: I'm staying. Still a lot to learn here.

### Refusals
- Sidney/DrQ hired RU: Пока Сидни или Доктор Кью в отряде — нет. С ними не сработаемся.
- Sidney/DrQ hired EN: Not while Sidney or Dr.Q's on the team. We wouldn't work well together.
- Death toll RU: Слишком много потерь — даже оптимизм имеет предел.
- Death toll EN: Too many losses — even optimism has its limits.

### Mitigations
- Vilde/Grace hired RU: Вильде или Грейс уже здесь? Тогда я определённо в деле.
- Vilde/Grace hired EN: Vilde or Grace already in? Then I'm definitely in.

### ExtraPartingWords
- RU: Возьмите ещё Вильде — вместе мы вдвое эффективнее.
- EN: Grab Vilde too — together we're twice as effective.

## Phrases — VoiceResponse

- `voice_source: wildfire` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Знаток готов.» / «Allik's ready.»
  - AimAttack (1): «Цель рассчитана.» / «Target calculated.»
  - AimAttack (2): «Точно по плану.» / «Right on plan.»
  - OpponentKilled: «Задача выполнена.» / «Task complete.»
  - DeathGeneral: «Не по расчёту вышло...» / «Didn't go according to plan...»
  - Downed: «Ранен, но справлюсь.» / «Hit, but I'll manage.»
  - CombatStartDetected: «Внимание, контакт!» / «Attention, contact!»
  - LevelUp: «Опыт копится быстро.» / «Experience is piling up fast.»
  - AmmoLow: «Патроны на исходе.» / «Running low on ammo.»
  - Idle: «Жду задачу.» / «Waiting for a task.»
  - MockDislike (Sidney/DrQ): «Только бы Сидни или Доктор Кью не мешали.» / «Just hope Sidney or Dr.Q don't get in the way.»
  - Praises (Vilde/Grace present): «С такой командой любая задача по плечу.» / «With this team, any task is manageable.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Allik |
| VoiceResponseId | Jazz_Allik |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Allik.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Allik_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=wildfire |

## Open blockers

- none
