---
status: planned
priority: low
origin: ja2
unit_id: Jazz_Cord
portrait_id: Cord
affiliation: MERC
role: Mechanic
tier: Regular
specialization: Mechanic
gender: Male
nationality: USA
voice_source: ja2
starting_level: 3
will: 40
salary:
  starting: 550
  increase: 150
  lv1: 250
  max: 1800
medical_deposit: standard
haggling: normal
executable: false
---

# Кардан — Даг «Кардан» Милтон

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Даг «Кардан» Милтон | Даг «Кардан» Милтон |
| Nick | Кардан | Cord |
| AllCapsNick | КАРДАН | CORD |
| Title | Забывчивый механик | Забывчивый механик |
| Email | Cord@merc.com | Cord@merc.com |
| snype_nick | cardan | cardan |

## Bio

**RU:** Статы 60–70, Dex 89, Wisdom 49, Marksmanship 44, Mechanical 82. Forgetful; reverse skill drain. Hits on Vicki; dislikes Ivan/Igor/Russians.

**EN:** EN draft: translate Bio RU.

## Stats

| Stat | Value |
| --- | --- |
| Health | 65 |
| Agility | 60 |
| Dexterity | 89 |
| Strength | 60 |
| Wisdom | 49 |
| Will | 40 |
| Leadership | 15 |
| Marksmanship | 44 |
| Mechanical | 82 |
| Explosives | 15 |
| Medical | 10 |
| MaxHitPoints | 65 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Cord` |
| type | passive |
| DisplayName RU/EN | Тихий ремонт / Тихий ремонт |
| Description RU/EN | −15% время ремонта / −15% время ремонта |
| Mechanics | Repair time −15% (or craft focus). |

## Personality

- Quirks: Forgetful, reverse leveling
- Likes: Vicki (one-sided)
- Dislikes: Ivan, Igor
- National hates: Russians
- Refusal / Haggle notes: MERC

## Hire

- Access: MERC
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Cord`
- Presets:
  - *50: lockpicks, tool kit

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](cord.ja2-face.gif)

Файл: `cord.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `cord.ja2-face.gif` (same face identity). Forgetful mechanic, grease, blank look, toolbag — NO gun.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Toolbag, lockpicks, grease rag

## Phrases — AIM chat

### Offline
- RU: Кардан... куда я?
- EN: Cord unavailable.

### GreetingAndOffer
- RU: А? Кардан.
- EN: Cord here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: Что мы делали? / Well?
- Part RU/EN: Кажется, я в деле. / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: ja2` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Cord |
| VoiceResponseId | Jazz_Cord |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Cord.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=ja2 |

## Open blockers

- none
