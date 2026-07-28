---
status: planned
priority: low
origin: ja2
unit_id: Jazz_Hobbit
portrait_id: Hobbit
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
  starting: 700
  increase: 150
  lv1: 300
  max: 2200
medical_deposit: standard
haggling: normal
executable: false
---

# Хоббит — Тим «Хоббит» Хиллман

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Тим «Хоббит» Хиллман | Тим «Хоббит» Хиллман |
| Nick | Хоббит | Hobbit |
| AllCapsNick | ХОББИТ | HOBBIT |
| Title | Несу вас | Несу вас |
| Email | Hobbit@merc.com | Hobbit@merc.com |
| snype_nick | frodo | frodo |

## Bio

**RU:** Статы 60–70, Agility 44, Wisdom 94, Marksmanship 44, Mechanical 0 forever, Explosives 56. Pessimist, heat fear. Neutral.

**EN:** EN draft: translate Bio RU.

## Stats

| Stat | Value |
| --- | --- |
| Health | 65 |
| Agility | 44 |
| Dexterity | 60 |
| Strength | 55 |
| Wisdom | 94 |
| Will | 50 |
| Leadership | 25 |
| Marksmanship | 44 |
| Mechanical | 0 |
| Explosives | 56 |
| Medical | 15 |
| MaxHitPoints | 65 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Hobbit` |
| type | passive |
| DisplayName RU/EN | Несу вас / Несу вас |
| Description RU/EN | Шаринг Explosives / Шаринг Explosives |
| Mechanics | PREFERRED: squad uses Hobbit Explosives if lower. ALT: share 50% of his Explosives. |

## Personality

- Quirks: Pessimist, FearHeat
- Likes: —
- Dislikes: —
- National hates: —
- Refusal / Haggle notes: MERC

## Hire

- Access: MERC
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Hobbit`
- Presets:
  - *50: electronics, small charges

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](hobbit.ja2-face.gif)

Файл: `hobbit.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `hobbit.ja2-face.gif` (same face identity). Short pessimistic demolitionist, backpack almost as big as him, detonator — NO gun.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Oversize pack, detonator, electronics kit

## Phrases — AIM chat

### Offline
- RU: Хоббит недоступен.
- EN: Hobbit unavailable.

### GreetingAndOffer
- RU: Хоббит. Я не Фродо.
- EN: Hobbit here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: Жарко... / Well?
- Part RU/EN: Могу нести вас. / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: ja2` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Hobbit |
| VoiceResponseId | Jazz_Hobbit |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Hobbit.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=ja2 |

## Open blockers

- choose share variant
