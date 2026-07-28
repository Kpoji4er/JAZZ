---
status: planned
priority: low
origin: wildfire
unit_id: Jazz_Vilde
portrait_id: Vilde
affiliation: AIM
role: Autorifleman
tier: Veteran
specialization: Autoriflemen
gender: Male
nationality: Estonia
voice_source: wildfire
starting_level: 4
will: 60
salary:
  starting: 1800
  increase: 150
  lv1: 700
  max: 4500
medical_deposit: standard
haggling: normal
executable: false
---

# Зануда — Леннарт «Зануда» Вильде

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Леннарт «Зануда» Вильде | Леннарт «Зануда» Вильде |
| Nick | Зануда | Vilde |
| AllCapsNick | ЗАНУДА | VILDE |
| Title | Тоже эстонец | Тоже эстонец |
| Email | Vilde@aim.com | Vilde@aim.com |
| snype_nick | vilde | vilde |

## Bio

**RU:** WF. Stats ~80, Leadership 67, Marksmanship 74. Fear heat. Likes Allik, Monk; dislikes Dr.Q, Lynx.

**EN:** EN draft: translate Bio RU.

## Stats

| Stat | Value |
| --- | --- |
| Health | 80 |
| Agility | 80 |
| Dexterity | 75 |
| Strength | 75 |
| Wisdom | 70 |
| Will | 60 |
| Leadership | 67 |
| Marksmanship | 74 |
| Mechanical | 30 |
| Explosives | 30 |
| Medical | 25 |
| MaxHitPoints | 80 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Vilde` |
| type | passive |
| DisplayName RU/EN | Ночной автоматчик / Ночной автоматчик |
| Description RU/EN | Night + auto / Night + auto |
| Mechanics | NightOps + AutoWeapons. needs-design unique. |

## Personality

- Quirks: FearHeat
- Likes: Jazz_Allik, Jazz_Monk
- Dislikes: DrQ, Jazz_Lynx
- National hates: —(Russian tag quirk)
- Refusal / Haggle notes: WF

## Hire

- Access: AIM
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Vilde`
- Presets:
  - *50: night ops, auto kit

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](vilde.ja2-face.gif)

Файл: `vilde.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `vilde.ja2-face.gif` (same face identity). Estonian night auto-trooper, NV goggles on helmet — NO gun. Pedantic look.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** NV goggles, night camo, notebook

## Phrases — AIM chat

### Offline
- RU: Вильде недоступен.
- EN: Vilde unavailable.

### GreetingAndOffer
- RU: Вильде. По пунктам.
- EN: Vilde here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: Жарко. / Well?
- Part RU/EN: Принято. / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: wildfire` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Vilde |
| VoiceResponseId | Jazz_Vilde |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Vilde.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=wildfire |

## Open blockers

- unique perk needs-design
