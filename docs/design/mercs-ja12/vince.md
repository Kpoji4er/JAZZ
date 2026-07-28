---
status: planned
priority: low
origin: ja2
unit_id: Jazz_Vince
portrait_id: Vince
affiliation: Locals
role: Doctor
tier: Veteran
specialization: Doctor
gender: Male
nationality: USA
voice_source: ja2
starting_level: 4
will: 70
salary:
  starting: 1200
  increase: 150
  lv1: 500
  max: 4000
medical_deposit: standard
haggling: normal
executable: false
---

# Винс — Доктор Винсент «Винс»

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Доктор Винсент «Винс» | Доктор Винсент «Винс» |
| Nick | Винс | Vince |
| AllCapsNick | ВИНС | VINCE |
| Title | Ментор | Ментор |
| Email | Vince@arulco.med | Vince@arulco.med |
| snype_nick | vince | vince |

## Bio

**RU:** Health 94, Dex 92, Agility 49, Marksmanship 35, Wisdom 94, Medical 94, Leadership 33. Fast learner. Claustrophobic. Teacher + Ambidextrous.

**EN:** EN draft: translate Bio RU.

## Stats

| Stat | Value |
| --- | --- |
| Health | 94 |
| Agility | 49 |
| Dexterity | 92 |
| Strength | 60 |
| Wisdom | 94 |
| Will | 70 |
| Leadership | 33 |
| Marksmanship | 35 |
| Mechanical | 20 |
| Explosives | 10 |
| Medical | 94 |
| MaxHitPoints | 94 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Vince` |
| type | passive |
| DisplayName RU/EN | TBD / TBD |
| Description RU/EN | needs-design / needs-design |
| Mechanics | Sheet empty — Teacher/ambidex mentoring synergy needs-design. |

## Personality

- Quirks: Claustrophobic
- Likes: —
- Dislikes: —
- National hates: —
- Refusal / Haggle notes: Local doctor

## Hire

- Access: Locals
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Vince`
- Presets:
  - *50: meds, teaching books, ambidextrous holsters

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](vince.ja2-face.gif)

Файл: `vince.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `vince.ja2-face.gif` (same face identity). Calm mentor doctor, glasses, medical satchel and textbooks — NO gun.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Medical satchel, textbooks, glasses, medic patch

## Phrases — AIM chat

### Offline
- RU: Доктор Винс на операции.
- EN: Vince unavailable.

### GreetingAndOffer
- RU: Винсент слушает.
- EN: Vince here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: Учимся? / Well?
- Part RU/EN: Готов учить. / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: ja2` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Vince |
| VoiceResponseId | Jazz_Vince |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Vince.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=ja2 |

## Open blockers

- perk: needs-design
