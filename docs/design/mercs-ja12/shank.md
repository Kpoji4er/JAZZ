---
status: planned
priority: low
origin: ja2
unit_id: Jazz_Shank
portrait_id: Shank
affiliation: MERC
role: Thrower
tier: Regular
specialization: Melee
gender: Male
nationality: USA
voice_source: ja2
starting_level: 1
will: 35
salary:
  starting: 50
  increase: 150
  lv1: 20
  max: 400
medical_deposit: none
haggling: normal
executable: false
---

# Шенк — Брием «Шенк» Друз

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Брием «Шенк» Друз | Брием «Шенк» Друз |
| Nick | Шенк | Shank |
| AllCapsNick | ШЕНК | SHANK |
| Title | Манчкин | Манчкин |
| Email | Shank@merc.com | Shank@merc.com |
| snype_nick | shank | shank |

## Bio

**RU:** Stats 30–35, Wisdom 80. Cannot swim, optimist. Likes Dynamo, Ivan. $20/day. Throwing expert.

**EN:** EN draft: translate Bio RU.

## Stats

| Stat | Value |
| --- | --- |
| Health | 35 |
| Agility | 35 |
| Dexterity | 40 |
| Strength | 30 |
| Wisdom | 80 |
| Will | 35 |
| Leadership | 10 |
| Marksmanship | 40 |
| Mechanical | 10 |
| Explosives | 20 |
| Medical | 10 |
| MaxHitPoints | 35 |
| StartingLevel | 1 |

## Perks

### StartingPerks

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Shank` |
| type | passive |
| DisplayName RU/EN | Не трогай меня / Не трогай меня |
| Description RU/EN | −50% CTH в melee по нему / −50% CTH в melee по нему |
| Mechanics | Enemies attacking Shank in melee take −50% CTH. |

## Personality

- Quirks: CannotSwim, Optimist
- Likes: Jazz_Dynamo, Ivan
- Dislikes: —
- National hates: —
- Refusal / Haggle notes: Joke hire

## Hire

- Access: Locals → MERC
- MedicalDeposit: none; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Shank`
- Presets:
  - *50: throwing knives, junk armor

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](shank.ja2-face.gif)

Файл: `shank.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `shank.ja2-face.gif` (same face identity). Scrawny junkie-looking thrower, oversized jacket, knife pouch — NO gun. Smug.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Knife pouch, oversized jacket, lucky charm

## Phrases — AIM chat

### Offline
- RU: Шенк... спит.
- EN: Shank unavailable.

### GreetingAndOffer
- RU: Шенк! Не трогай!
- EN: Shank here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: Ха. / Well?
- Part RU/EN: За двадцатку. / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: ja2` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Shank |
| VoiceResponseId | Jazz_Shank |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Shank.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=ja2 |

## Open blockers

- none
