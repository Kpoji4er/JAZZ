---
status: planned
priority: low
origin: ja2
unit_id: Jazz_Carlos
portrait_id: Carlos
affiliation: Locals
role: Scout
tier: Regular
specialization: Stealth
gender: Male
nationality: Arulco
voice_source: ja2
starting_level: 3
will: 40
salary:
  starting: 450
  increase: 150
  lv1: 200
  max: 1500
medical_deposit: standard
haggling: normal
executable: false
---

# Карлос — Карлос Дасуза

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Карлос Дасуза | Карлос Дасуза |
| Nick | Карлос | Carlos |
| AllCapsNick | КАРЛОС | CARLOS |
| Title | Пессимист | Пессимист |
| Email | Carlos@arulco.reb | Carlos@arulco.reb |
| snype_nick | carlos | carlos |

## Bio

**RU:** Dex 61, Marksmanship 67, Agility 91. Pessimist. Likes Miguel, Ira, Dimitri; dislikes Iggy. Possible Drassen mole (design note).

**EN:** EN draft: translate Bio RU.

## Stats

| Stat | Value |
| --- | --- |
| Health | 70 |
| Agility | 91 |
| Dexterity | 61 |
| Strength | 65 |
| Wisdom | 55 |
| Will | 40 |
| Leadership | 30 |
| Marksmanship | 67 |
| Mechanical | 20 |
| Explosives | 25 |
| Medical | 20 |
| MaxHitPoints | 70 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Carlos` |
| type | passive |
| DisplayName RU/EN | TBD / TBD |
| Description RU/EN | needs-design / needs-design |
| Mechanics | Sheet empty — Stealth+Throwing from JA2 only until designed. |

## Personality

- Quirks: Pessimist
- Likes: Miguel, Jazz_Ira, Jazz_Dimitri
- Dislikes: Iggy
- National hates: —
- Refusal / Haggle notes: Local

## Hire

- Access: Locals
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Carlos`
- Presets:
  - *50: stealth kit, throwing knives

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](carlos.ja2-face.gif)

Файл: `carlos.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `carlos.ja2-face.gif` (same face identity). Lean pessimistic rebel scout, dark mood, binoculars — NO gun.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Binoculars, throwing knife sheath, rebel scarf

## Phrases — AIM chat

### Offline
- RU: Карлос... зачем звонить.
- EN: Carlos unavailable.

### GreetingAndOffer
- RU: Карлос. Плохие новости?
- EN: Carlos here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: Как обычно плохо. / Well?
- Part RU/EN: Ладно. / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: ja2` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Carlos |
| VoiceResponseId | Jazz_Carlos |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Carlos.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=ja2 |

## Open blockers

- perk: needs-design
