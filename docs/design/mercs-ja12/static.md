---
status: planned
priority: low
origin: ja2
unit_id: Jazz_Static
portrait_id: Static
affiliation: AIM
role: Mechanic
tier: Veteran
specialization: Mechanic
gender: Male
nationality: USA
voice_source: ja2
starting_level: 4
will: 50
salary:
  starting: 1400
  increase: 150
  lv1: 600
  max: 3500
medical_deposit: standard
haggling: normal
executable: false
---

# Статик — Кирк «Статик» Стивенсон

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Кирк «Статик» Стивенсон | Кирк «Статик» Стивенсон |
| Nick | Статик | Static |
| AllCapsNick | СТАТИК | STATIC |
| Title | Хиппи-механик | Хиппи-механик |
| Email | Static@aim.com | Static@aim.com |
| snype_nick | static | static |

## Bio

**RU:** Статы 60–80, Strength 59, Dexterity 95, Wisdom 60, Mechanical 99. Боится насекомых. Дружит с Spider и Larry drunk; не любит Larry clean, Rothman, Blade; не любит швейцарцев.

**EN:** EN draft: translate Bio RU.

## Stats

| Stat | Value |
| --- | --- |
| Health | 70 |
| Agility | 75 |
| Dexterity | 95 |
| Strength | 59 |
| Wisdom | 60 |
| Will | 50 |
| Leadership | 20 |
| Marksmanship | 55 |
| Mechanical | 99 |
| Explosives | 20 |
| Medical | 15 |
| MaxHitPoints | 70 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Static` |
| type | passive |
| DisplayName RU/EN | Экономия запчастей / Экономия запчастей |
| Description RU/EN | −5% parts per level / −5% parts per level |
| Mechanics | Parts cost −5% per merc level. |

## Personality

- Quirks: FearInsects
- Likes: Jazz_Spider, Larry(drugged)
- Dislikes: Larry(clean), Jazz_Rothman, Jazz_Blade
- National hates: Swiss
- Refusal / Haggle notes: AIM

## Hire

- Access: AIM
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Static`
- Presets:
  - *50: tool kit, electronics kit, night ops goggles

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](static.ja2-face.gif)

Файл: `static.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `static.ja2-face.gif` (same face identity). Hippie mechanic, longish hair, welding goggles on forehead, toolbandolier — NO gun.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Tool bandolier, welding goggles, multimeter, AIM pin

## Phrases — AIM chat

### Offline
- RU: Статик в отключке.
- EN: Static unavailable.

### GreetingAndOffer
- RU: Йо, Статик.
- EN: Static here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: Мир... и гайки. / Well?
- Part RU/EN: Ок, чиню. / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: ja2` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Static |
| VoiceResponseId | Jazz_Static |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Static.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=ja2 |

## Open blockers

- none
