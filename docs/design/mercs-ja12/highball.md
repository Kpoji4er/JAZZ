---
status: planned
priority: low
origin: ja2
unit_id: Jazz_Highball
portrait_id: Highball
affiliation: AIM
role: Doctor
tier: Regular
specialization: Doctor
gender: Male
nationality: USA
voice_source: ja2
starting_level: 3
will: 40
salary:
  starting: 900
  increase: 150
  lv1: 400
  max: 2500
medical_deposit: standard
haggling: normal
executable: false
---

# Скала — Клиффорд «Скала» Хайбол

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Клиффорд «Скала» Хайбол | Клиффорд «Скала» Хайбол |
| Nick | Скала | Highball |
| AllCapsNick | СКАЛА | HIGHBALL |
| Title | Старый алкаш | Старый алкаш |
| Email | Highball@aim.com | Highball@aim.com |
| snype_nick | highball | highball |

## Bio

**RU:** Худшие статы AIM ~50–60; Wisdom 87, Marksmanship 84, Medical 84. Нейтрален к команде. Можно без уники или крафт стимуляторов.

**EN:** EN draft: translate Bio RU.

## Stats

| Stat | Value |
| --- | --- |
| Health | 55 |
| Agility | 50 |
| Dexterity | 55 |
| Strength | 55 |
| Wisdom | 87 |
| Will | 40 |
| Leadership | 20 |
| Marksmanship | 84 |
| Mechanical | 10 |
| Explosives | 10 |
| Medical | 84 |
| MaxHitPoints | 55 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Highball` |
| type | passive |
| DisplayName RU/EN | Стимуляторная / Стимуляторная |
| Description RU/EN | Крафт стимуляторов / Крафт стимуляторов |
| Mechanics | PREFERRED: craft stimulants. ALT: no unique (reference only). |

## Personality

- Quirks: Alcoholic
- Likes: —
- Dislikes: —
- National hates: —
- Refusal / Haggle notes: AIM

## Hire

- Access: AIM
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Highball`
- Presets:
  - *50: meds, flask, soft armor

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](highball.ja2-face.gif)

Файл: `highball.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `highball.ja2-face.gif` (same face identity). Elderly alcoholic doctor, red nose, stained medic coat with flask and pill bottles — NO gun.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Flask, pill bottles, medic armband, battered bag

## Phrases — AIM chat

### Offline
- RU: Хайбол... икает... позже.
- EN: Highball unavailable.

### GreetingAndOffer
- RU: Скала на линии. Ик.
- EN: Highball here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: Ещё по одной? / Well?
- Part RU/EN: Ладно, иду... / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: ja2` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Highball |
| VoiceResponseId | Jazz_Highball |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Highball.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=ja2 |

## Open blockers

- choose craft vs no-unique in impl
