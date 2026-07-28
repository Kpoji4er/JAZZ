---
status: planned
priority: low
origin: wildfire
unit_id: Jazz_Grace
portrait_id: Grace
affiliation: AIM
role: Thrower
tier: Regular
specialization: Melee
gender: Female
nationality: USA
voice_source: wildfire
starting_level: 3
will: 45
salary:
  starting: 1600
  increase: 150
  lv1: 600
  max: 4000
medical_deposit: standard
haggling: normal
executable: false
---

# Грейс — Грациелла «Грейс» Джирелли

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Грациелла «Грейс» Джирелли | Грациелла «Грейс» Джирелли |
| Nick | Грейс | Grace |
| AllCapsNick | ГРЕЙС | GRACE |
| Title | Итальянка | Итальянка |
| Email | Grace@aim.com | Grace@aim.com |
| snype_nick | grace | grace |

## Bio

**RU:** WF. Italian marked American. Fear cockroaches, pessimist. Weak thrower stats (Str 67, Marks 69, Dex 77), Leadership 62. Likes Allik; dislikes Red, Ricochet, Lava.

**EN:** EN draft: translate Bio RU.

## Stats

| Stat | Value |
| --- | --- |
| Health | 70 |
| Agility | 75 |
| Dexterity | 77 |
| Strength | 67 |
| Wisdom | 65 |
| Will | 45 |
| Leadership | 62 |
| Marksmanship | 69 |
| Mechanical | 20 |
| Explosives | 20 |
| Medical | 25 |
| MaxHitPoints | 70 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Grace` |
| type | passive |
| DisplayName RU/EN | Броски эксперт / Броски эксперт |
| Description RU/EN | Throwing expert / Throwing expert |
| Mechanics | Throwing expert. needs-design unique. |

## Personality

- Quirks: FearInsects(cockroaches), Pessimist
- Likes: Jazz_Allik
- Dislikes: Red, Jazz_Ricochet, Lava
- National hates: —
- Refusal / Haggle notes: WF

## Hire

- Access: AIM
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Grace`
- Presets:
  - *50: throwing knives

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](grace.ja2-face.gif)

Файл: `grace.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `grace.ja2-face.gif` (same face identity). Italian-American woman, stylish but tactical, knife bandolier sheathed — NO gun. Pessimistic beauty.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Throwing knife bandolier, stylish scarf, AIM pin

## Phrases — AIM chat

### Offline
- RU: Грейс не в духе.
- EN: Grace unavailable.

### GreetingAndOffer
- RU: Grace.
- EN: Grace here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: Опять плохо. / Well?
- Part RU/EN: Ва-bene... / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: wildfire` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Grace |
| VoiceResponseId | Jazz_Grace |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Grace.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=wildfire |

## Open blockers

- unique perk needs-design
