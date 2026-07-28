---
status: planned
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
executable: false
---

# Мясо — Тортон «Мясо» Джонс

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Тортон «Мясо» Джонс | Тортон «Мясо» Джонс |
| Nick | Мясо | Meat |
| AllCapsNick | МЯСО | MEAT |
| Title | Гора | Гора |
| Email | Meat@merc.com | Meat@merc.com |
| snype_nick | meat | meat |

## Bio

**RU:** Dex 68, Agility 54, Wisdom 29, Strength 98, Mech 59, Exp 64. Aggressive. Likes Bull; weird crush on Tosca. Widely hated. Hates Arulco locals.

**EN:** EN draft: translate Bio RU.

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

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Meat` |
| type | passive |
| DisplayName RU/EN | Толстокожий / Толстокожий |
| Description RU/EN | Will cap 50 / Will cap 50 |
| Mechanics | Willpower limit raised to 50 (sheet). |

## Personality

- Quirks: Aggressive
- Likes: Jazz_Bull, Jazz_Buzz (crush)
- Dislikes: many
- National hates: Arulco
- Refusal / Haggle notes: MERC

## Hire

- Access: MERC
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Meat`
- Presets:
  - *50: explosives, melee kit

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](meat.ja2-face.gif)

Файл: `meat.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `meat.ja2-face.gif` (same face identity). Huge dumb explosive bruiser, stained shirt, demo bag — NO gun. Meathead look.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Demo bag, stained apron-ish shirt, fuse coil

## Phrases — AIM chat

### Offline
- RU: Мясо жрёт.
- EN: Meat unavailable.

### GreetingAndOffer
- RU: Мясо тут.
- EN: Meat here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: Где Тоска? / Well?
- Part RU/EN: Угх. / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: ja2` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Meat |
| VoiceResponseId | Jazz_Meat |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Meat.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=ja2 |

## Open blockers

- none
