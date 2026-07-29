---
status: ready
priority: low
origin: ja2
unit_id: Jazz_Meat
portrait_id: Meat
affiliation: MERC
role: Demolitions
tier: Regular
specialization: ExplosiveExpert
gender: Male
nationality: USA
voice_source: ja2
starting_level: 3
will: 50
salary:
  starting: 750
  increase: 150
  lv1: 300
  max: 2200
medical_deposit: standard
haggling: normal
executable: true
---

# Мясо — Тортон «Мясо» Джонс

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Тортон «Мясо» Джонс | Thorton "Meat" Jones |
| Nick | Мясо | Meat |
| AllCapsNick | МЯСО | MEAT |
| Title | Гора | The Mountain |
| Email | Meat@merc.com | Meat@merc.com |
| snype_nick | meat | meat |

## Bio

**RU:** Dexterity 68, Agility 54, Wisdom 29, Strength 98, Mechanical 59, Explosives 64. Агрессивен и туповат, но взрывчатку носит и ставит без страха. Дружит с Быком; странно запал на Тоску. Его недолюбливают почти все местные из Арулько.

**EN:** 68 Dexterity, 54 Agility, 29 Wisdom, 98 Strength, 59 Mechanical, 64 Explosives. Aggressive and none too bright, but carries and plants explosives without a hint of fear. Friends with Bull; has a weird crush on Tosca. Widely disliked by Arulco locals.

## Stats

| Stat | Value |
| --- | --- |
| Health | 90 |
| Agility | 54 |
| Dexterity | 68 |
| Strength | 98 |
| Wisdom | 29 |
| Will | 50 |
| Leadership | 10 |
| Marksmanship | 55 |
| Mechanical | 59 |
| Explosives | 64 |
| Medical | 5 |
| MaxHitPoints | 90 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- `Jazz_Perk_Meat`
- `DesignerExplosives`
- `MeleeTraining`
- `TrueGrit`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Meat` |
| type | passive |
| DisplayName RU/EN | Толстокожий / Thick-Skinned |
| Description RU/EN | Волю Мяса ничем не сломить ниже определённого порога / Meat's Will can't be broken below a certain floor |
| Mechanics | Meat's effective Will can never be reduced below 50 by negative status effects, panic checks, or morale penalties — a brute too dim to know real fear. |

## Personality

- Quirks: Aggressive (bio flavor only — no matching JA3 status perk, not wired)
- Likes: `Jazz_Bull`, `Jazz_Buzz` (both planned mercs — Mitigation/ExtraPartingWords wiring activates once ready)
- Dislikes: —
- National hates: Arulco — Haggle trigger when the squad contains multiple Arulco-nationality locals
- Refusal / Haggle notes: haggles when squad is heavy on Arulco locals; standard MERC money and death-toll refusals; mitigation and recommendation for Bull/Buzz when hired

## Hire

- Access: MERC hire
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Meat` → `JAZZ_Meat50/35/25/20`
- *50: `JazzArmor_LeatherJacketBrn`, `TNT`×2, `PipeBomb`×2, `Detonator`, `Machete`
- *35: `TNT`×2, `PipeBomb`×1, `Detonator`, `Machete`
- *25: `TNT`×1, `Detonator`, `Knife`
- *20: `TNT`×1, `Unarmed`

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](meat.ja2-face.gif)

Файл: `meat.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `meat.ja2-face.gif` (same face identity). Huge dumb explosives bruiser ~35, stained shirt, heavy demo bag, coil of fuse over shoulder — NO gun. Meathead grin.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Demo bag, stained shirt, fuse coil

## Phrases — AIM chat

### Offline
- RU: Мясо жрёт. Перезвони.
- EN: This is Meat. Leave a message.

### GreetingAndOffer
- RU: Мясо тут. Что взрываем?
- EN: Meat here. What are we blowing up?

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Где Тоска?
- EN: Where's Tosca?

### PartingWords
- RU: Угх. Иду.
- EN: Ugh. I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Тут есть что взорвать.
- EN: I'm staying. Plenty to blow up here.

### Refusals
- Money RU: Мало денег. Мясо злится.
- Money EN: Not enough money. Meat gets angry.
- Death toll RU: Слишком много трупов даже для Мяса.
- Death toll EN: Too many bodies, even for Meat.

### Haggles
- Arulco locals hired RU: Отряд полон местных из Арулько... ладно, но за доплату.
- Arulco locals hired EN: Squad's full of Arulco locals... fine, but it'll cost extra.

### Mitigations
- Bull/Buzz hired RU: О, Бык (или Базз) уже здесь? Тогда я в деле.
- Bull/Buzz hired EN: Oh, Bull (or Buzz) is already in? Then I'm in.

### ExtraPartingWords
- RU: Если нужен ещё один здоровяк — берите Быка.
- EN: If you need another big guy, grab Bull.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Мясо готово.» / «Meat's ready.»
  - AimAttack (1): «Бабах будет!» / «Gonna go boom!»
  - AimAttack (2): «Заложено.» / «It's set.»
  - OpponentKilled: «Разнесло.» / «Blown apart.»
  - DeathGeneral: «Не... так...» / «Not... like this...»
  - Downed: «Меня зацепило!» / «I'm hit!»
  - CombatStartPlayer: «Взрываем всё!» / «Blow it all up!»
  - LevelUp: «Мясо крепче!» / «Meat's tougher now!»
  - AmmoLow: «Заряды кончаются.» / «Running low on charges.»
  - Idle: «Где Тоска...» / «Where's Tosca...»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Meat |
| VoiceResponseId | Jazz_Meat |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Meat.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Meat_Big.png |
| CustomEquipGear | TryEquip Handheld A Melee |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
