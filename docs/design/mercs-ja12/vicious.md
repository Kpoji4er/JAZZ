---
status: planned
priority: medium
origin: ja2
unit_id: Jazz_Vicious
portrait_id: Vicious
affiliation: AIM
role: AllRounder
tier: Veteran
specialization: Melee
gender: Male
nationality: France
voice_source: ja2
starting_level: 4
will: 40
salary:
  starting: 1800
  increase: 200
  lv1: 700
  max: 4500
medical_deposit: standard
haggling: normal
executable: false
---

# Злобный — Жан-Пьер «Злобный» Вио

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Жан-Пьер «Злобный» Вио | Жан-Пьер «Злобный» Вио |
| Nick | Злобный | Vicious |
| AllCapsNick | ЗЛОБНЫЙ | VICIOUS |
| Title | Мачо | Мачо |
| Email | Vicious@aim.com | Vicious@aim.com |
| snype_nick | mademoiselles | mademoiselles |

## Bio

**RU:** Статы 80–90, Wisdom 55, Marksmanship 82. Агрессивный, клеится к Fox/Spider/Lava. Ненавидит британцев. Martial arts / knife.

**EN:** EN draft: translate Bio RU at generation.

## Stats

| Stat | Value |
| --- | --- |
| Health | 88 |
| Agility | 90 |
| Dexterity | 85 |
| Strength | 85 |
| Wisdom | 55 |
| Will | 40 |
| Leadership | 25 |
| Marksmanship | 82 |
| Mechanical | 10 |
| Explosives | 15 |
| Medical | 10 |
| MaxHitPoints | 88 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- (map JA2 skills to JA3 StartingPerks)
- `Jazz_Perk_Vicious`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Vicious` |
| type | passive |
| DisplayName RU/EN | Дамский угодник / Дамский угодник |
| Description RU/EN | Бонус за женщин в отряде / Бонус за женщин в отряде |
| Mechanics | Start-of-combat stacking buff per woman in squad (1:+1AP … 5: full stack). Fox/Spider/Lava present doubles. Melee kill +2 AP. |

## Personality

- Quirks: Aggressive
- Likes: Fox, Jazz_Spider, Lava (flirt)
- Dislikes: —
- National hates: British
- Refusal / Haggle notes: AIM

## Hire

- Access: AIM
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Vicious`
- Presets (weights ~50/35/25/20):
  - *50: knives, light armor, cologne joke item optional

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](vicious.ja2-face.gif)

Файл: `vicious.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `vicious.ja2-face.gif` (same face identity). Handsome arrogant French merc, open collar under vest, knife sheaths and charm bracelet — NO gun. Smirk.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Knife sheaths, cologne vial, open collar, AIM pin

## Phrases — AIM chat

### Offline
- RU: Злобный занят дамами. Пишите.
- EN: This is Vicious. Leave a message.

### GreetingAndOffer
- RU: Oui? Жан-Пьер слушает.
- EN: Vicious here.

### ConversationRestart
- RU: Вернёмся к делу.
- EN: Let's get back to it.

### IdleLine
- RU: Ну же, cherie-командир.
- EN: Waiting.

### PartingWords
- RU: Я уже еду — красиво.
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
  - Selection: «Злобный!» / «Vicious!»
  - AimAttack / OpponentKilled / DeathGeneral / Downed / CombatStartPlayer / LevelUp / AmmoLow / Idle — standard drafts + relationship slots.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Vicious |
| VoiceResponseId | Jazz_Vicious |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Vicious.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Vicious_Big.png |
| CustomEquipGear | TryEquip Handheld A/B as role requires |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
