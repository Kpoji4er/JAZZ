---
status: ready
priority: medium
origin: ja2
unit_id: Jazz_Rothman
portrait_id: Rothman
affiliation: AIM
role: Commander
tier: Veteran
specialization: Leader
gender: Male
nationality: SouthAfrica
voice_source: ja2
starting_level: 4
will: 70
salary:
  starting: 2200
  increase: 200
  lv1: 900
  max: 5500
medical_deposit: small
haggling: normal
executable: true
---

# Ротман — Стефан Ротман

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Стефан Ротман | Stefan Rothman |
| Nick | Ротман | Rothman |
| AllCapsNick | РОТМАН | ROTHMAN |
| Title | Шахтёрский безопасник | The Mine Overseer |
| Email | Rothman@aim.com | Rothman@aim.com |
| snype_nick | mineboss | mineboss |

## Bio

**RU:** Статы 78–85, Health 97, Leadership 59, Explosives 66. Бывший начальник службы безопасности алмазных рудников ЮАР — умеет и охранять шахту, и подрывать её, если понадобится. Дружит с Лавой (JA2-флейвор, вне AIM-каталога); не любит Статика и Гвоздя, презирает вечно обдолбанного Ларри; недолюбливает американцев.

**EN:** Stats in the 78-85 range, 97 Health, 59 Leadership, 66 Explosives. A former head of mine security on South African diamond fields — equally comfortable guarding a mine or blowing one up if the contract calls for it. Friends with Lava (JA2 lore flavor, not an AIM-roster relationship); can't stand Static or Nails, and has zero patience for a drugged-up Larry; not fond of Americans.

## Stats

| Stat | Value |
| --- | --- |
| Health | 97 |
| Agility | 80 |
| Dexterity | 78 |
| Strength | 85 |
| Wisdom | 75 |
| Will | 70 |
| Leadership | 59 |
| Marksmanship | 80 |
| Mechanical | 40 |
| Explosives | 66 |
| Medical | 30 |
| MaxHitPoints | 97 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- `Jazz_Perk_Rothman`
- `Teacher`
- `ShoulderToShoulder`
- `DesignerExplosives`
- `HoldPosition`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Rothman` |
| type | operation |
| DisplayName RU/EN | Шахтёрский надзор / The Mine Overseer |
| Description RU/EN | Пока Ротман гарнизоном стоит в секторе с шахтой, он может провести спецоперацию, ловящую ворующих штейгеров и временно поднимающую доход шахты / While Rothman is garrisoned in a sector with an active mine, he can run a special operation that catches embezzling foremen and temporarily boosts that mine's income |
| Mechanics | New sector operation, available only in sectors with an active mine while Rothman is garrisoned there. Duration 2 days; on success grants +25% income from that mine for the following 7 days (does not stack with itself — a fresh run simply refreshes the duration). No resource cost beyond Rothman's time in the sector. |

## Personality

- Quirks: —
- Likes: Lava (JA2-lore flavor only — not a valid unit id in this mod's roster, so no Mitigation/ExtraPartingWords is wired against it)
- Dislikes: `Jazz_Static` (planned merc — Refusal wiring activates once ready), `Nails`, `Larry` (drugged persona specifically, not `Larry_Clean`)
- National hates: Americans — Haggle trigger, same pattern as Colby/Conrad
- Refusal / Haggle notes: refuses if Static, Nails, or drugged Larry hired; refuses on excessive death toll; haggles on money and on squads full of Americans

## Hire

- Access: AIM hire
- MedicalDeposit: small; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Rothman` → `JAZZ_Rothman50/35/25/20`
- *50: `JazzArmor_Uniform`, `FNFAL`, `JAZZ_AMMO_762x51_Match`×40 (Double), `ShapedCharge`×1, `FirstAidKit`
- *35: `JazzArmor_LeatherJacketBrn`, `M16A1`, `JAZZ_AMMO_556_FMJ`×60 (Double), `PipeBomb`×1
- *25: `JazzArmor_LeatherJacketBrn`, `AK47`, `JAZZ_AMMO_762x39_FMJ`×40 (Double)
- *20: `JazzArmor_LeatherArmor`, `AK47`, `JAZZ_AMMO_762x39_FMJ`×30 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](rothman.ja2-face.gif)

Файл: `rothman.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `rothman.ja2-face.gif` (same face identity). Stocky sun-worn South African security officer ~45, khaki security shirt with mine-safety badge, clipboard and radio on chest harness — NO gun. Watchful, professional expression.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Mine safety badge, clipboard, radio, hardhat clip

## Phrases — AIM chat

### Offline
- RU: Ротман. Занят на объекте. Перезвоните.
- EN: This is Rothman. On-site right now. Call back.

### GreetingAndOffer
- RU: Ротман слушает. Контракт по делу?
- EN: Rothman here. Is this a real contract?

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Время — деньги, а у меня их и так немного.
- EN: Time's money, and I don't have much of either to spare.

### PartingWords
- RU: Договорились. Беру людей и выхожу.
- EN: Deal. I'm bringing my people and moving out.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Работа ещё не закончена.
- EN: I'm staying. The job's not finished.

### Refusals
- Static/Nails/Larry hired RU: Пока Статик, Гвоздь или обдолбанный Ларри у вас — я не подписываюсь. Не тот уровень дисциплины.
- Static/Nails/Larry hired EN: Not while Static, Nails, or a drugged-out Larry are on your payroll. That's not the level of discipline I work with.
- Death toll RU: Слишком много трупов на вашем счету для нормального контракта.
- Death toll EN: Too many bodies on your ledger for a proper contract.

### Haggles
- USA mercs hired RU: Отряд из одних американцев... Ладно, но с доплатой.
- USA mercs hired EN: A squad full of Americans... Fine, but it'll cost extra.

### ExtraPartingWords
- RU: Если нужен ещё один надёжный специалист по шахтам — ищите Лаву, я о нём наслышан.
- EN: If you need another reliable mine specialist, look up Lava — I've heard good things.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Ротман на связи.» / «Rothman's up.»
  - AimAttack (1): «Цель под контролем.» / «Target's under control.»
  - AimAttack (2): «Работаю по инструкции.» / «Working it by the book.»
  - OpponentKilled: «Объект зачищен.» / «Site's clear.»
  - DeathGeneral: «Не уследил...» / «Should've seen that coming...»
  - Downed: «Ранен. Держу периметр.» / «Hit. Holding the perimeter.»
  - CombatStartDetected: «Внимание, нарушители.» / «Heads up, intruders.»
  - LevelUp: «Опыт не купишь.» / «Can't buy this kind of experience.»
  - AmmoLow: «Патроны на исходе.» / «Running low on ammo.»
  - Idle: «Жду смены.» / «Waiting for my shift to start.»
  - MockDislike (Static/Nails/Larry): «Хорошо, что эти клоуны не здесь.» / «Glad those clowns aren't here.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Rothman |
| VoiceResponseId | Jazz_Rothman |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Rothman.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Rothman_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
