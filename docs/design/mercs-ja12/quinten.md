---
status: ready
priority: medium
origin: ja2
unit_id: Jazz_Quinten
portrait_id: Quinten
affiliation: AIM
role: Doctor
tier: Elite
specialization: Doctor
gender: Male
nationality: USA
voice_source: ja2
starting_level: 5
will: 85
salary:
  starting: 3000
  increase: 200
  lv1: 1500
  max: 7500
medical_deposit: large
haggling: normal
executable: true
---

# Дэнни — Доктор Дэниел «Дэнни» Квинтен

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Доктор Дэниел «Дэнни» Квинтен | Doctor Daniel "Danny" Quinten |
| Nick | Дэнни | Danny |
| AllCapsNick | ДЭННИ | DANNY |
| Title | Машина, не человек | Not a Man, a Machine |
| Email | Quinten@aim.com | Quinten@aim.com |
| snype_nick | parkourmd | parkourmd |

## Bio

**RU:** 99 Health, 99 Agility, около 80 Strength/Dexterity, Wisdom 91, Medical 88, Marksmanship 61. Одиночка, стреляет и лечит одинаково хорошо обеими руками. Не любит Стероида, Мясо и Биффа — считает их всех безответственными в поле.

**EN:** 99 Health, 99 Agility, roughly 80 Strength/Dexterity, 91 Wisdom, 88 Medical, 61 Marksmanship. A loner who shoots and treats wounds equally well with either hand. Doesn't get along with Steroid, Meat, or Biff — considers all three reckless in the field.

## Stats

| Stat | Value |
| --- | --- |
| Health | 99 |
| Agility | 99 |
| Dexterity | 80 |
| Strength | 80 |
| Wisdom | 91 |
| Will | 85 |
| Leadership | 20 |
| Marksmanship | 61 |
| Mechanical | 10 |
| Explosives | 10 |
| Medical | 88 |
| MaxHitPoints | 99 |
| StartingLevel | 5 |

## Perks

### StartingPerks

- `Jazz_Perk_Quinten`
- `Loner`
- `Ambidextrous`
- `Savior`
- `StressManagement`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Quinten` |
| type | passive |
| DisplayName RU/EN | Полевой реаниматор / Field Resuscitator |
| Description RU/EN | Снятие негативного эффекта или подъём упавшего товарища даёт цели +2 ОД; акробатический freemove-бонус ограничен +20% вместо обычных +50% / Removing a negative status effect or reviving a downed ally grants the target +2 AP; parkour-style freemove bonus is capped at +20% instead of the usual +50% |
| Mechanics | On successful use of a medical action that removes a negative status effect (Bleeding, Wounded, Unconscious, etc.) or wakes a Downed ally, the target immediately gains +2 AP that turn. To keep Quinten's mobility in line with a Doctor tier, his innate parkour/freemove bonus from Agility is explicitly capped at +20% rather than the higher values other high-Agility mercs can reach. |

## Personality

- Quirks: `Loner` (StartingPerk)
- Likes: —
- Dislikes: `Steroid`, `Jazz_Meat` (planned merc — Refusal wiring activates once ready), `Jazz_Biff` (medium wave — Refusal wiring live once both are generated together)
- National hates: —
- Refusal / Haggle notes: refuses if Steroid, Meat, or Biff hired; refuses on excessive death toll; standard AIM money refusal

## Hire

- Access: AIM hire
- MedicalDeposit: large; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Quinten` → `JAZZ_Quinten50/35/25/20`
- *50: `JazzArmor_PoliceVest`, `HiPower`×2 (dual-wield, ambidextrous), `JAZZ_AMMO_9x19_FMJ`×48 (Double), `Meds`×50, `FirstAidKit`, `CombatStim`×2
- *35: `JazzArmor_LeatherArmor`, `HiPower`×2, `JAZZ_AMMO_9x19_FMJ`×36 (Double), `Meds`×30, `FirstAidKit`
- *25: `JazzArmor_LeatherArmor`, `Colt1911`, `JAZZ_AMMO_45ACP_FMJ`×24 (Double), `Meds`×20
- *20: `JazzArmor_LeatherJacketBrn`, `Colt1911`, `JAZZ_AMMO_45ACP_FMJ`×20 (Double), `Meds`×10

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](quinten.ja2-face.gif)

Файл: `quinten.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `quinten.ja2-face.gif` (same face identity). Extremely athletic male doctor ~30, short hair, runner's build, olive medic vest with trauma packs, shears and dual holsters — NO weapon drawn. Confident, alert expression.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Trauma packs, shears, IV pouch, medic cross patch, dual holsters (empty)

## Phrases — AIM chat

### Offline
- RU: Доктор Квинтен недоступен. Оставьте сообщение.
- EN: This is Doctor Quinten. Leave a message.

### GreetingAndOffer
- RU: Квинтен на связи. Сколько бежать и кого латать?
- EN: Danny here. How far do I run and who am I patching up?

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Пульс ровный. У тебя — не проверял.
- EN: My pulse is steady. Haven't checked yours.

### PartingWords
- RU: Аптечка собрана, обе руки заряжены. Выхожу.
- EN: Kit's packed, both hands loaded. I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Кому-то же надо следить, чтобы вы не поубивали друг друга.
- EN: I'm staying. Someone has to make sure you don't kill each other.

### Refusals
- Steroid/Meat/Biff hired RU: Пока Стероид, Мясо или Бифф в отряде — нет. Слишком безответственно для моей практики.
- Steroid/Meat/Biff hired EN: Not while Steroid, Meat, or Biff are on the team. Too reckless for my practice.
- Death toll RU: Слишком много раненых и погибших на вашем счету. Я предпочитаю пациентов, которые выживают.
- Death toll EN: Too many wounded and dead on your record. I prefer patients who survive.
- Money RU: Мой гонорар не обсуждается по дешёвке.
- Money EN: My rate isn't up for a discount.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Дэнни готов.» / «Danny's ready.»
  - AimAttack (1): «Вижу цель.» / «Target in sight.»
  - AimAttack (2): «Обеими руками, спокойно.» / «Both hands, steady.»
  - OpponentKilled: «Чисто.» / «Clean.»
  - DeathGeneral: «Не смог откачать сам себя...» / «Couldn't resuscitate myself...»
  - Downed: «Ранен — сам себя не подниму.» / «I'm down — can't patch myself up.»
  - CombatStartPlayer: «Начинаем. Аптечка при мне.» / «Let's go. Kit's on me.»
  - LevelUp: «Практика приносит плоды.» / «Practice pays off.»
  - AmmoLow: «Патроны на исходе.» / «Running low on ammo.»
  - Idle: «Жду. Пульс в норме.» / «Waiting. Pulse is fine.»
  - MockDislike (Steroid/Meat/Biff): «Надеюсь, эти трое сегодня не рядом.» / «Hoping those three aren't nearby today.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Quinten |
| VoiceResponseId | Jazz_Quinten |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Quinten.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Quinten_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm; TryEquip Handheld B Firearm (ambidextrous dual pistols) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
