---
status: planned
priority: low
origin: nightops
unit_id: Jazz_Eskimo
portrait_id: Eskimo
affiliation: Locals
role: Sniper
tier: Regular
specialization: Marksmen
gender: Male
nationality: Arulco
voice_source: nightops
starting_level: 3
will: 60
salary:
  starting: 400
  increase: 150
  lv1: 150
  max: 1500
medical_deposit: none
haggling: normal
executable: false
---

# Эскимо — Эмиль «Эскимо» Кимос

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Эмиль «Эскимо» Кимос | Эмиль «Эскимо» Кимос |
| Nick | Эскимо | Eskimo |
| AllCapsNick | ЭСКИМО | ESKIMO |
| Title | Пленный снайпер | Пленный снайпер |
| Email | Eskimo@arulco.reb | Eskimo@arulco.reb |
| snype_nick | eskimo | eskimo |

## Bio

**RU:** Night Ops. Cut JA2 merc base. Rebel for Miguel, imprisoned by Deidranna in Alma. After free joins player. Hates Arabs and heat. Likes Miguel, Carlos, Gamos. Health 97, Marks 95.

**EN:** EN draft: translate Bio RU.

## Stats

| Stat | Value |
| --- | --- |
| Health | 97 |
| Agility | 68 |
| Dexterity | 70 |
| Strength | 70 |
| Wisdom | 55 |
| Will | 60 |
| Leadership | 25 |
| Marksmanship | 95 |
| Mechanical | 10 |
| Explosives | 10 |
| Medical | 15 |
| MaxHitPoints | 97 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- (map JA2 skills)`n- named perk below

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Eskimo` |
| type | passive |
| DisplayName RU/EN | Скрытный снайпер / Скрытный снайпер |
| Description RU/EN | Stealth sniper / Stealth sniper |
| Mechanics | Stealthy + sniper. needs-design unique. |

## Personality

- Quirks: FearHeat
- Likes: Miguel, Jazz_Carlos, Jazz_Gamos
- Dislikes: —
- National hates: Arabs
- Refusal / Haggle notes: NO

## Hire

- Access: Free from Alma prison then join
- MedicalDeposit: none; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Eskimo`
- Presets:
  - *50: sniper kit in loot, cold-weather scarf ironic

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](eskimo.ja2-face.gif)

Файл: `eskimo.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `eskimo.ja2-face.gif` (same face identity). Arulco rebel sniper, cold scarf nickname irony, spotting scope pouch — NO rifle. Stoic.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Spotting pouch, scarf, prison-worn clothes, rebel armband

## Phrases — AIM chat

### Offline
- RU: Эскимо в камере... шутка.
- EN: Eskimo unavailable.

### GreetingAndOffer
- RU: Эскимо свободен?
- EN: Eskimo here.

### ConversationRestart / IdleLine / PartingWords / Rehire
- Restart RU/EN: Вернёмся к делу. / Let's get back to it.
- Idle RU/EN: Холодно только в имени. / Well?
- Part RU/EN: Спасибо. Иду. / I'm in.
- RehireIntro: Контракт заканчивается. Продлеваем? / Contract's ending. Extending?
- RehireOutro: Остаюсь. / I'm staying.

### Extra
- Draft relationship lines at generation.

## Phrases — VoiceResponse

- `voice_source: nightops` — legacy VO reuse + minimum Selection/AimAttack/OpponentKilled/DeathGeneral/Downed/CombatStart/LevelUp/AmmoLow/Idle drafts.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Eskimo |
| VoiceResponseId | Jazz_Eskimo |
| pollyvoice | Matthew |
| Portrait / BigPortrait | Mod/Dv3mFVN/MercPortraits/Eskimo.png (+_Big) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet JA1/2 block; origin=nightops |

## Open blockers

- prison free gate + unique perk needs-design
