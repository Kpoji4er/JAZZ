---
status: planned
priority: low
origin: ub
unit_id: Jazz_Biggens
portrait_id: Biggens
affiliation: Locals
role: Demolitions
tier: Regular
specialization: ExplosiveExpert
gender: Male
nationality: USA
voice_source: ub
starting_level: 3
will: 50
salary:
  starting: 900
  increase: 150
  lv1: 400
  max: 2500
medical_deposit: standard
haggling: normal
executable: false
---

# Биггенс — Полковник Фредерик Биггенс

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Полковник Фредерик Биггенс | Полковник Фредерик Биггенс |
| Nick | Биггенс | Biggens |
| AllCapsNick | БИГГЕНС | BIGGENS |
| Title | Усталый дед | Усталый дед |
| Email | Biggens@ub.mil | Biggens@ub.mil |
| snype_nick | biggens | biggens |

## Bio

**RU:** UB. Stats 55–65, Marksmanship 71, Explosives 92. Optimist, heat intolerant. Story demo expert.

**EN:** EN draft: translate Bio RU.

## Stats

| Stat | Value |
| --- | --- |
| Health | 60 |
| Agility | 55 |
| Dexterity | 55 |
| Strength | 55 |
| Wisdom | 70 |
| Will | 50 |
| Leadership | 40 |
| Marksmanship | 71 |
| Mechanical | 40 |
| Explosives | 92 |
| Medical | 20 |
| MaxHitPoints | 60 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Biggens` |
| type | passive |
| DisplayName RU/EN | Старая школа / Старая школа |
| Description RU/EN | Electronics + night ops / Electronics + night ops |
| Mechanics | Electronics/NightOps expert demolitions. needs-design unique. |

## Personality

- Quirks: Optimist, FearHeat
- Likes: —
- Dislikes: —
- National hates: —
- Refusal / Haggle notes: UB

## Hire

- Access: UB locals/story
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Biggens`
- Presets:
  - *50: demo charges, electronics

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](biggens.ja2-face.jpg)

Файл: `biggens.ja2-face.jpg`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `biggens.ja2-face.jpg` (same face identity). Elderly tired colonel, white hair, demo satchel and reading glasses — NO gun.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Demo satchel, glasses, colonel tabs

## Phrases — AIM chat

### Offline
- RU: Биггенс отдыхает.
- EN: Biggens unavailable.

### GreetingAndOffer
- RU: Полковник Биггенс.
- EN: Biggens here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: Жарковато. / Well?
- Part RU/EN: Ещё один раз... / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: ub` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Biggens |
| VoiceResponseId | Jazz_Biggens |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Biggens.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=ub |

## Open blockers

- unique perk needs-design
