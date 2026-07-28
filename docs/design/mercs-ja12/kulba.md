---
status: planned
priority: low
origin: ub
unit_id: Jazz_Kulba
portrait_id: Kulba
affiliation: Locals
role: Autorifleman
tier: Regular
specialization: Autoriflemen
gender: Male
nationality: USA
voice_source: ub
starting_level: 3
will: 60
salary:
  starting: 800
  increase: 150
  lv1: 350
  max: 2200
medical_deposit: standard
haggling: normal
executable: false
---

# Кульба — Джон Кульба

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Джон Кульба | Джон Кульба |
| Nick | Кульба | Kulba |
| AllCapsNick | КУЛЬБА | KULBA |
| Title | Патриот-дед | Патриот-дед |
| Email | Kulba@ub.mil | Kulba@ub.mil |
| snype_nick | kulba | kulba |

## Bio

**RU:** UB. Stats 55–60, Marksmanship 95, Mechanical 88. Wife died of cancer after Arulco rescue. Likes Gus; dislikes Ivan, Igor, Ricochet. Ultra-patriot.

**EN:** EN draft: translate Bio RU.

## Stats

| Stat | Value |
| --- | --- |
| Health | 58 |
| Agility | 55 |
| Dexterity | 55 |
| Strength | 60 |
| Wisdom | 70 |
| Will | 60 |
| Leadership | 35 |
| Marksmanship | 95 |
| Mechanical | 88 |
| Explosives | 20 |
| Medical | 25 |
| MaxHitPoints | 58 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Kulba` |
| type | passive |
| DisplayName RU/EN | Автоматы эксперт / Автоматы эксперт |
| Description RU/EN | Auto expert / Auto expert |
| Mechanics | AutoWeapons expert. needs-design unique. |

## Personality

- Quirks: Patriot
- Likes: Gus
- Dislikes: Ivan, Igor, Jazz_Ricochet
- National hates: —
- Refusal / Haggle notes: UB

## Hire

- Access: UB locals
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Kulba`
- Presets:
  - *50: auto rifle in loot, tools, US flag patch

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](kulba.ja2-face.jpg)

Файл: `kulba.ja2-face.jpg`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `kulba.ja2-face.jpg` (same face identity). Elderly American patriot, gray hair, flag patch and gunsmith tools — NO rifle in hands. Sad resolve.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** US flag patch, gunsmith tools, mourning band

## Phrases — AIM chat

### Offline
- RU: Кульба на службе.
- EN: Kulba unavailable.

### GreetingAndOffer
- RU: Кульба слушает.
- EN: Kulba here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: За свободу. / Well?
- Part RU/EN: Готов. / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: ub` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Kulba |
| VoiceResponseId | Jazz_Kulba |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Kulba.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=ub |

## Open blockers

- unique perk needs-design
