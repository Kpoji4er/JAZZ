---
status: planned
priority: low
origin: ja2
unit_id: Jazz_Hitman
portrait_id: Hitman
affiliation: Locals
role: Sniper
tier: Veteran
specialization: Marksmen
gender: Male
nationality: USA
voice_source: ja2
starting_level: 4
will: 55
salary:
  starting: 0
  increase: 150
  lv1: 0
  max: 3000
medical_deposit: none
haggling: none
executable: false
---

# Убийца — Ричард «Убийца» Рутвен

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Ричард «Убийца» Рутвен | Ричард «Убийца» Рутвен |
| Nick | Убийца | Hitman |
| AllCapsNick | УБИЙЦА | HITMAN |
| Title | Разыскиваемый | Разыскиваемый |
| Email | Hitman@dark.net | Hitman@dark.net |
| snype_nick | ruthven | ruthven |

## Bio

**RU:** Статы 75–80, Wisdom 59, Marksmanship 93. Wanted terrorist; free week if exposed then flees. Cannot swim. Likes Mag; hates Flo; hates Americans.

**EN:** EN draft: translate Bio RU.

## Stats

| Stat | Value |
| --- | --- |
| Health | 78 |
| Agility | 75 |
| Dexterity | 80 |
| Strength | 75 |
| Wisdom | 59 |
| Will | 55 |
| Leadership | 20 |
| Marksmanship | 93 |
| Mechanical | 20 |
| Explosives | 20 |
| Medical | 10 |
| MaxHitPoints | 78 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Hitman` |
| type | active |
| DisplayName RU/EN | Вырубить / Вырубить |
| Description RU/EN | Выстрел с knockout / Выстрел с knockout |
| Mechanics | Active: rifle shot applies Unconscious; recharges by killing another way. |

## Personality

- Quirks: CannotSwim
- Likes: Magic
- Dislikes: Flo
- National hates: Americans
- Refusal / Haggle notes: Special

## Hire

- Access: Special expose script (needs JA3 port)
- MedicalDeposit: none; Haggling: none; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Hitman`
- Presets:
  - *50: sniper kit in loot, disguise

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](hitman.ja2-face.gif)

Файл: `hitman.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `hitman.ja2-face.gif` (same face identity). Wanted sniper look, hoodie, spotting monocle — NO rifle. Cold stare.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Hoodie, spotting monocle, fake ID pouch

## Phrases — AIM chat

### Offline
- RU: ...
- EN: Hitman unavailable.

### GreetingAndOffer
- RU: Говори быстро.
- EN: Hitman here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: Время. / Well?
- Part RU/EN: Неделя. Не больше. / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: ja2` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Hitman |
| VoiceResponseId | Jazz_Hitman |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Hitman.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=ja2 |

## Open blockers

- expose/flee script needs-design for JA3
