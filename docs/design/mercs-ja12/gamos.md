---
status: ready
priority: medium
origin: ja2
unit_id: Jazz_Gamos
portrait_id: Gamos
affiliation: Locals
role: Scout
tier: Regular
specialization: Stealth
gender: Male
nationality: Arulco
voice_source: ja2
starting_level: 3
will: 55
salary:
  starting: 250
  increase: 200
  lv1: 100
  max: 1000
medical_deposit: none
haggling: normal
executable: true
---

# Гамос — Гамос

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Гамос | Gamos |
| Nick | Гамос | Gamos |
| AllCapsNick | ГАМОС | GAMOS |
| Title | Я много путешествовать | Me Travel Much |
| Email | Gamos@arulco.reb | Gamos@arulco.reb |
| snype_nick | travelmuch | travelmuch |

## Bio

**RU:** Статы 60–70, Wisdom 35, Marksmanship 78. Простой и дружелюбный местный проводник, исходивший джунгли Арулько вдоль и поперёк. Нейтрален к остальному отряду, дёшев в найме.

**EN:** Stats in the 60-70 range, 35 Wisdom, 78 Marksmanship. A simple, friendly local guide who's walked every inch of Arulco's jungle. Neutral toward the rest of the roster, cheap to hire.

## Stats

| Stat | Value |
| --- | --- |
| Health | 65 |
| Agility | 70 |
| Dexterity | 65 |
| Strength | 65 |
| Wisdom | 35 |
| Will | 55 |
| Leadership | 20 |
| Marksmanship | 78 |
| Mechanical | 15 |
| Explosives | 10 |
| Medical | 15 |
| MaxHitPoints | 65 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- `Jazz_Perk_Gamos`
- `Stealthy`
- `Flanker`
- `TrueGrit`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Gamos` |
| type | passive |
| DisplayName RU/EN | Тропы джунглей / Jungle Trails |
| Description RU/EN | Быстрее передвигается вне дорог по джунглям и болотам / Moves faster off-road through jungle and marsh terrain |
| Mechanics | −40% satellite-map travel time for squads led by Gamos when moving through sectors tagged `Jungle`, `Marshlands`, or `CursedForest` (matches the terrain GameStates already used by vanilla AppearancesList tagging). No effect on road/city travel. |

## Personality

- Quirks: Normal (no strong likes/dislikes; flavor as an easy-going neutral guide)
- Likes: —
- Dislikes: —
- National hates: —
- Refusal / Haggle notes: standard Locals money/death-toll refusals only — no relationship-based branches

## Hire

- Access: Locals — available from the local guide network once the player has liberated Gamos's home sector
- MedicalDeposit: none; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Gamos` → `JAZZ_Gamos50/35/25/20`
- *50: `JazzArmor_LeatherArmor`, `SKS`, `JAZZ_AMMO_762x39_FMJ`×30 (Double), `Machete`, `Lockpick`
- *35: `JazzArmor_LeatherArmor`, `SKS`, `JAZZ_AMMO_762x39_FMJ`×20 (Double), `Machete`
- *25: `JazzArmor_LeatherJacketBrn`, `Machete_Sharpened`
- *20: `JazzArmor_LeatherJacketBrn`, `Machete`

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](gamos.ja2-face.gif)

Файл: `gamos.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `gamos.ja2-face.gif` (same face identity). Local Arulco traveler ~35, simple clothes, huge jungle backpack and sheathed machete on hip — NO gun. Friendly, simple smile.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Jungle backpack, sheathed machete, water gourd, worn boots

## Phrases — AIM chat

### Offline
- RU: Гамос много путешествовать — сейчас нет тут. Потом.
- EN: Gamos travel much — not here now. Later.

### GreetingAndOffer
- RU: Гамос тут. Куда идти надо?
- EN: Gamos here. Where we go?

### ConversationRestart
- RU: Связь пропадать. Вернёмся к делу.
- EN: Line drop. Let's talk again.

### IdleLine
- RU: Идём? Гамос знать дорогу.
- EN: We go? Gamos know the way.

### PartingWords
- RU: Хорошо, Гамос идёт. Джунгли не страшны.
- EN: Okay, Gamos come. Jungle not scary.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Гамос остаётся. Есть ещё тропы показать.
- EN: Gamos stay. More trails to show.

### Refusals
- Death toll RU: Много люди умирать с вами. Гамос не хотеть так.
- Death toll EN: Много люди умирать с вами. Gamos not want that.
- Money RU: Мало денег. Гамос семью кормить надо.
- Money EN: Too little money. Gamos have family to feed.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Гамос здесь!» / «Gamos here!»
  - AimAttack (1): «Гамос стрелять!» / «Gamos shoot!»
  - AimAttack (2): «На мушке.» / «On target.»
  - OpponentKilled: «Готово.» / «Done.»
  - DeathGeneral: «Джунгли забирать Гамос...» / «Jungle take Gamos...»
  - Downed: «Гамос ранен!» / «Gamos hit!»
  - CombatStartDetected: «Опасность близко!» / «Danger close!»
  - LevelUp: «Гамос учиться быстро.» / «Gamos learn fast.»
  - AmmoLow: «Патроны мало!» / «Little ammo left!»
  - Idle: «Гамос ждать.» / «Gamos wait.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Gamos |
| VoiceResponseId | Jazz_Gamos |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Gamos.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Gamos_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
