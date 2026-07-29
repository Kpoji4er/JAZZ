---
status: ready
priority: low
origin: ja2
unit_id: Jazz_Devin
portrait_id: Devin
affiliation: Locals
role: Demolitions
tier: Veteran
specialization: ExplosiveExpert
gender: Male
nationality: Ireland
voice_source: ja2
starting_level: 4
will: 65
salary:
  starting: 2000
  increase: 150
  lv1: 800
  max: 5000
medical_deposit: standard
haggling: normal
executable: true
---

# Девин — Девин Коннелл

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Девин Коннелл | Devin Connell |
| Nick | Девин | Devin |
| AllCapsNick | ДЕВИН | DEVIN |
| Title | IRA | IRA |
| Email | Devin@arulco.local | Devin@arulco.local |
| snype_nick | ira | ira |

## Bio

**RU:** Статы 60–70, Dexterity 88, Explosives 96. Одиночка, бывший боец ИРА. Симпатизирует Реду; недолюбливает британцев.

**EN:** Stats in the 60-70 range, 88 Dexterity, 96 Explosives. A loner and former IRA fighter. Gets along with Red; not fond of the British.

## Stats

| Stat | Value |
| --- | --- |
| Health | 68 |
| Agility | 70 |
| Dexterity | 88 |
| Strength | 65 |
| Wisdom | 70 |
| Will | 65 |
| Leadership | 20 |
| Marksmanship | 60 |
| Mechanical | 40 |
| Explosives | 96 |
| Medical | 15 |
| MaxHitPoints | 68 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- `Jazz_Perk_Devin`
- `Loner`
- `DesignerExplosives`
- `BreachAndClear`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Devin` |
| type | passive |
| DisplayName RU/EN | IRA / IRA |
| Description RU/EN | Взрывы Девина крушат укрытия и поджигают всё вокруг / Devin's explosions wreck cover and set the area on fire |
| Mechanics | Any explosion triggered by Devin deals +100% damage to structures/cover and has a 25% chance to apply Burning to units caught inside the blast radius. |

## Personality

- Quirks: Loner
- Likes: `Red`
- Dislikes: —
- National hates: British — Haggle trigger when the active squad is full of British-nationality mercs
- Refusal / Haggle notes: haggles when squad is all-British; standard local money refusal; mitigation and recommendation for Red when hired

## Hire

- Access: Locals hire
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Devin` → `JAZZ_Devin50/35/25/20`
- *50: `JazzArmor_LeatherJacketBrn`, `C4`×2, `Detonator`, `Combination_Detonator_Remote`, `Wirecutter`, `Knife_Sharpened`
- *35: `TNT`×2, `Detonator`, `Wirecutter`, `Knife_Sharpened`
- *25: `TNT`×1, `Detonator`, `Knife`
- *20: `PipeBomb`×1, `Knife`

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](devin.ja2-face.gif)

Файл: `devin.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `devin.ja2-face.gif` (same face identity). Irish demolitions loner ~40, redhead, detonator in hand, green scarf — NO gun. Hard, quiet eyes.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Detonator, charge pack, green scarf, electronics kit

## Phrases — AIM chat

### Offline
- RU: Девин занят. Позже.
- EN: This is Devin. Leave a message.

### GreetingAndOffer
- RU: Коннелл слушает.
- EN: Devin here.

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Ну что, есть что взорвать?
- EN: Well? Got something for me to blow up?

### PartingWords
- RU: За такую цену — идёт.
- EN: For that price — deal.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь.
- EN: I'm staying.

### Haggles
- British mercs hired RU: Отряд полон британцев... ладно, но с доплатой.
- British mercs hired EN: Squad's full of Brits... fine, but it'll cost extra.
- Money RU: Мои заряды не бесплатные.
- Money EN: My charges aren't free.

### Mitigations
- Red hired RU: О, Ред уже здесь? Тогда порядок.
- Red hired EN: Oh, Red's already in? Then we're good.

### ExtraPartingWords
- RU: Если нужен ещё один спец по взрывчатке — зовите Реда.
- EN: If you need another demolitions man, call Red.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Девин на месте.» / «Devin's here.»
  - AimAttack (1): «Заряд заложен.» / «Charge is set.»
  - AimAttack (2): «Отходим.» / «Falling back.»
  - OpponentKilled: «Разнесло в пыль.» / «Blown to dust.»
  - DeathGeneral: «За Ирландию...» / «For Ireland...»
  - Downed: «Зацепили. Держусь.» / «I'm hit. Holding on.»
  - CombatStartDetected: «Внимание, гости.» / «Heads up, company.»
  - LevelUp: «Опыт не купишь.» / «Can't buy that kind of experience.»
  - AmmoLow: «Заряды кончаются.» / «Running low on charges.»
  - Idle: «Жду сигнала.» / «Waiting for the signal.»
  - Praises (Red present): «Хорошая компания сегодня.» / «Good company today.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Devin |
| VoiceResponseId | Jazz_Devin |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Devin.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Devin_Big.png |
| CustomEquipGear | TryEquip Handheld A Melee |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
