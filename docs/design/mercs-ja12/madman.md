---
status: planned
priority: high
origin: ja2
unit_id: Jazz_Madman
portrait_id: Madman
affiliation: MERC
role: Mechanic
tier: Veteran
specialization: Mechanic
gender: Male
nationality: USA
voice_source: ja2
starting_level: 4
will: 50
salary:
  starting: 0
  increase: 200
  lv1: 0
  max: 500
medical_deposit: none
haggling: none
executable: false
---

# Бешеный — Кевин «Бешеный» Камерон

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Кевин «Бешеный» Камерон | Кевин «Бешеный» Камерон |
| Nick | Бешеный | Madman |
| AllCapsNick | БЕШЕНЫЙ | MADMAN |
| Title | Ржавый бампер | Ржавый бампер |
| Email | Madman@merc.com | Madman@merc.com |
| snype_nick | bumper | bumper |

## Bio

**RU:** Алмаз среди местных/MERC: 90+ физикалы, 68 механики, псих. Подкатывает к Лиске. После Арулько может уйти в MERC. Работает бесплатно в JA2 lore.

**EN:** EN draft: translate Bio RU at generation; keep tone.

## Stats

| Stat | Value |
| --- | --- |
| Health | 92 |
| Agility | 90 |
| Dexterity | 88 |
| Strength | 91 |
| Wisdom | 56 |
| Will | 50 |
| Leadership | 15 |
| Marksmanship | 70 |
| Mechanical | 68 |
| Explosives | 20 |
| Medical | 10 |
| MaxHitPoints | 92 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Madman`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Madman` |
| type | passive |
| DisplayName RU/EN | Штурм в упор / Штурм в упор |
| Description RU/EN | Упор даёт воодушевление / Упор даёт воодушевление |
| Mechanics | Enhances Assault/melee perks: point-blank ranged kill grants Inspiration (or equivalent morale buff). |

## Personality

- Quirks: Psycho
- Likes: Fox (attempt)
- Dislikes: —
- National hates: —
- Refusal / Haggle notes: Free hire quirks

## Hire

- Access: Locals → MERC after Arulco campaign gate
- MedicalDeposit: none; Haggling: none; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Madman`
- Presets (weights ~50/35/25/20):
  - *50: crowbar, lockpicks expert, light armor, bumper scrap charm

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](madman.ja2-face.gif)

Файл: `madman.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `madman.ja2-face.gif` (same face identity). Wild-eyed American bruiser-mechanic, grease-stained tank top under vest, huge crowbar and lockpick kit on belt — NO gun. Manic grin.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Crowbar, lockpick set, grease rag, dented bumper charm

## Phrases — AIM chat

### Offline
- RU: Бешеный не берёт трубку — бьёт ею.
- EN: This is Madman. Leave a message.

### GreetingAndOffer
- RU: Да я лучше бампером всех мочить! Ну?
- EN: Madman here. Talk.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Ну где драка?
- EN: Waiting on you.

### PartingWords
- RU: Ха! Поехали крушить.
- EN: I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь.
- EN: I'm staying.

### Refusals / Haggles / Mitigations / ExtraPartingWords
- Draft relationship refusals/haggles from Personality at generation time.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Бешеный!» / «Madman!»
  - AimAttack: «На мушке.» / «On target.»
  - OpponentKilled: «Готово.» / «Done.»
  - DeathGeneral: «Чёрт...» / «Damn...»
  - Downed: «Меня подбили!» / «I'm hit!»
  - CombatStartPlayer: «В бой.» / «Engage.»
  - LevelUp: «Ещё лучше.» / «Getting better.»
  - AmmoLow: «Патроны!» / «Ammo!»
  - Idle: «Жду.» / «Waiting.»
- Relationship VR slots per Likes/Dislikes when generating.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Madman |
| VoiceResponseId | Jazz_Madman |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Madman.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Madman_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm (or melee for knife mercs) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
