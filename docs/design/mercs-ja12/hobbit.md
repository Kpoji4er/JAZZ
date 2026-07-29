---
status: ready
priority: low
origin: ja2
unit_id: Jazz_Hobbit
portrait_id: Hobbit
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
  starting: 700
  increase: 150
  lv1: 300
  max: 2200
medical_deposit: standard
haggling: normal
executable: true
---

# Хоббит — Тим «Хоббит» Хиллман

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Тим «Хоббит» Хиллман | Tim "Hobbit" Hillman |
| Nick | Хоббит | Hobbit |
| AllCapsNick | ХОББИТ | HOBBIT |
| Title | Несу вас | I'll Carry You |
| Email | Hobbit@merc.com | Hobbit@merc.com |
| snype_nick | frodo | frodo |

## Bio

**RU:** Статы 60–70, Agility 44, Wisdom 94, Marksmanship 44, Mechanical 0 (никогда не растёт), Explosives 56. Пессимист, боится жары. Держится нейтрально к остальному отряду.

**EN:** Stats in the 60-70 range, 44 Agility, 94 Wisdom, 44 Marksmanship, 0 Mechanical (never improves), 56 Explosives. A pessimist who's afraid of the heat. Stays neutral toward the rest of the roster.

## Stats

| Stat | Value |
| --- | --- |
| Health | 65 |
| Agility | 44 |
| Dexterity | 60 |
| Strength | 55 |
| Wisdom | 94 |
| Will | 50 |
| Leadership | 25 |
| Marksmanship | 44 |
| Mechanical | 0 |
| Explosives | 56 |
| Medical | 15 |
| MaxHitPoints | 65 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- `Jazz_Perk_Hobbit`
- `Pessimist`
- `DesignerExplosives`
- `BreachAndClear`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Hobbit` |
| type | passive |
| DisplayName RU/EN | Несу вас / I'll Carry You |
| Description RU/EN | Товарищи по отряду ставят взрывчатку и мины так же хорошо, как Хоббит / Squadmates plant explosives and mines as well as Hobbit does |
| Mechanics | While Hobbit is present in the same active squad and sector, any other merc placing an explosive device, mine, or trap uses Hobbit's Explosives skill for that action whenever their own is lower. |

## Personality

- Quirks: Pessimist, FearHeat (Pessimist wired; heat fear is bio flavor only — no matching JA3 status perk)
- Likes: —
- Dislikes: —
- National hates: —
- Refusal / Haggle notes: no relationship triggers; standard MERC money and death-toll refusals only

## Hire

- Access: MERC hire
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Hobbit` → `JAZZ_Hobbit50/35/25/20`
- *50: `JazzArmor_LeatherArmor`, `Detonator`, `PipeBomb`×2, `TNT`×2, `Combination_Detonator_Time`, `M2Carbine`, `JAZZ_AMMO_30_FMJ`×20 (Double)
- *35: `Detonator`, `PipeBomb`×1, `TNT`×2, `Winchester1894`, `JAZZ_AMMO_30_FMJ`×16 (Double)
- *25: `Detonator`, `TNT`×1, `SWModel10`, `JAZZ_AMMO_38special_FMJ`×12 (Double)
- *20: `Detonator`, `TNT`×1, `Unarmed`

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](hobbit.ja2-face.gif)

Файл: `hobbit.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `hobbit.ja2-face.gif` (same face identity). Short pessimistic demolitionist ~30, backpack almost as big as him, detonator on a strap — NO gun.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Oversize pack, detonator, electronics kit

## Phrases — AIM chat

### Offline
- RU: Хоббит недоступен. Наверное, к лучшему.
- EN: This is Hobbit. Leave a message.

### GreetingAndOffer
- RU: Хоббит на связи. Я не Фродо, если что.
- EN: Hobbit here. I'm not Frodo, by the way.

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Жарко. Всё равно ничем хорошим не кончится.
- EN: It's hot. This won't end well anyway.

### PartingWords
- RU: Ладно, могу и понести вас, если что.
- EN: Fine, I can carry you if it comes to that.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Всё равно хуже уже не будет.
- EN: I'm staying. Can't get much worse anyway.

### Refusals
- Money RU: Маловато. Такими темпами всё плохо кончится.
- Money EN: Not enough. This is going to end badly at this rate.
- Death toll RU: Слишком много смертей — я предупреждал.
- Death toll EN: Too many deaths already — I warned you.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Хоббит готов. Наверное.» / «Hobbit's ready. Probably.»
  - AimAttack (1): «Заложил заряд.» / «Charge is set.»
  - AimAttack (2): «Отходим, отходим.» / «Back away, back away.»
  - OpponentKilled: «Ну вот, как я и думал — сработало.» / «Well, worked as expected.»
  - DeathGeneral: «Я же говорил...» / «I told you so...»
  - Downed: «Меня зацепило. Конечно.» / «I'm hit. Of course.»
  - CombatStartDetected: «Началось. Как всегда, не вовремя.» / «It's starting. Bad timing, as always.»
  - LevelUp: «Хм. Неожиданно хорошо.» / «Huh. Surprisingly good.»
  - AmmoLow: «Патроны кончаются.» / «Running low on ammo.»
  - Idle: «Жарко...» / «It's hot...»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Hobbit |
| VoiceResponseId | Jazz_Hobbit |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Hobbit.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Hobbit_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
