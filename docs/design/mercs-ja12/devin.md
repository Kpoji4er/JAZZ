---
status: planned
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
executable: false
---

# Девин — Девин Коннелл

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Девин Коннелл | Девин Коннелл |
| Nick | Девин | Devin |
| AllCapsNick | ДЕВИН | DEVIN |
| Title | IRA | IRA |
| Email | Devin@arulco.local | Devin@arulco.local |
| snype_nick | ira | ira |

## Bio

**RU:** Статы 60–70, Dex 88, Explosives 96. Loner. Likes Red; hates British. Expensive day rate lore.

**EN:** EN draft: translate Bio RU.

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

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Devin` |
| type | passive |
| DisplayName RU/EN | IRA / IRA |
| Description RU/EN | Взрывы крушат структуры / Взрывы крушат структуры |
| Mechanics | Any explosion +100% structure damage + chance to apply Burning. |

## Personality

- Quirks: Loner
- Likes: Red
- Dislikes: —
- National hates: British
- Refusal / Haggle notes: Local expensive

## Hire

- Access: Locals hire
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Devin`
- Presets:
  - *50: heavy demo, electronics, knife

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](devin.ja2-face.gif)

Файл: `devin.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `devin.ja2-face.gif` (same face identity). Irish demolitions loner, redhead, detonator and IRA-green scarf — NO gun. Hard eyes.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Detonator, charge pack, green scarf, electronics

## Phrases — AIM chat

### Offline
- RU: Devin busy.
- EN: Devin unavailable.

### GreetingAndOffer
- RU: Connelli.
- EN: Devin here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: Aye? / Well?
- Part RU/EN: For a price. / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: ja2` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Devin |
| VoiceResponseId | Jazz_Devin |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Devin.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=ja2 |

## Open blockers

- none
