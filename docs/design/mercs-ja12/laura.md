---
status: ready
priority: low
origin: wildfire
unit_id: Jazz_Laura
portrait_id: Laura
affiliation: AIM
role: Doctor
tier: Regular
specialization: Doctor
gender: Female
nationality: Romania
voice_source: wildfire
starting_level: 3
will: 55
salary:
  starting: 1700
  increase: 150
  lv1: 600
  max: 4200
medical_deposit: small
haggling: normal
executable: true
---

# Лора — Доктор Лора Колин

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Доктор Лора Колин | Doctor Laura Colin |
| Nick | Лора | Laura |
| AllCapsNick | ЛОРА | LAURA |
| Title | Цыганский врач | The Roma Doctor |
| Email | Laura@aim.com | Laura@aim.com |
| snype_nick | laura | laura |

## Bio

**RU:** Wildfire. Румынская цыганка. Статы 70–80, Ловкость 67, Меткость 82, Медицина 57 (при этом врач!), Взрывное дело 52 (лучшее среди Wildfire). Плохо переносит жару. Любит Штайгера и Монка; недолюбливает Тоску и Фокса.

**EN:** Wildfire mercenary. A Romanian Roma woman. Stats in the 70-80 range, 67 Agility, 82 Marksmanship, 57 Medical (a doctor, at that), 52 Explosives (the highest among Wildfire recruits). Handles heat poorly. Fond of Steiger and Monk; not fond of Tosca or Fox.

## Stats

| Stat | Value |
| --- | --- |
| Health | 75 |
| Agility | 67 |
| Dexterity | 75 |
| Strength | 70 |
| Wisdom | 70 |
| Will | 55 |
| Leadership | 30 |
| Marksmanship | 82 |
| Mechanical | 20 |
| Explosives | 52 |
| Medical | 57 |
| MaxHitPoints | 75 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- `Jazz_Perk_Laura`
- `Stealthy`
- `TrueGrit`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Laura` |
| type | passive |
| DisplayName RU/EN | Скрытный врач / Silent Medic |
| Description RU/EN | Лечение и подъём союзников не выдают позицию Лоры / Healing or reviving an ally doesn't break Laura's stealth |
| Mechanics | If Laura is Hidden, healing a wounded ally or reviving a Downed ally does not reveal her position or end her Hidden status. |

## Personality

- Quirks: FearHeat
- Likes: `Jazz_Steiger`, `Jazz_Monk`
- Dislikes: `Tosca`, `Fox`
- National hates: —
- Refusal / Haggle notes: refuses if Tosca or Fox are in the active squad; mitigation and rate discount when Jazz_Steiger or Jazz_Monk are hired

## Hire

- Access: AIM
- MedicalDeposit: small; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Laura` → `JAZZ_Laura50/35/25/20`
- *50: `JazzArmor_LeatherVest`, `Meds`×25, `FirstAidKit`, `Medkit`, `PipeBomb`, `Detonator`, `MicroUZI`, `JAZZ_AMMO_9x19_FMJ`×24 (Double)
- *35: `Meds`×15, `FirstAidKit`, `TNT`, `Makarov`, `JAZZ_AMMO_9x18_FMJ`×16 (Double)
- *25: `Meds`×10, `FirstAidKit`, `SWModel10`, `JAZZ_AMMO_38special_FMJ`×12 (Double)
- *20: `Meds`×6, `Colt38Special`, `JAZZ_AMMO_38special_FMJ`×8 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](laura.ja2-face.gif)

Файл: `laura.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `laura.ja2-face.gif` (same face identity). Romanian Roma field doctor, dark hair, mixed medic and stealth pouches — NO gun. Guarded look.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Medic pouches, stealth wrap, explosive satchel small, scarf

## Phrases — AIM chat

### Offline
- RU: Лора недоступна. Перезвоните.
- EN: Laura's unavailable. Call back.

### GreetingAndOffer
- RU: Доктор Колин слушает.
- EN: Doctor Colin here.

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Жарко сегодня, но работать можно.
- EN: It's hot today, but I can still work.

### PartingWords
- RU: Аптечка собрана. Я в деле.
- EN: Kit's packed. I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Раненых меньше не станет.
- EN: I'm staying. There'll always be wounded to treat.

### Refusals
- Tosca or Fox hired RU: Пока эти двое в отряде — я не поеду.
- Tosca or Fox hired EN: Not while those two are on the team.
- Money RU: За такую сумму даже не подходите.
- Money EN: For that sum, don't even approach me.

### Haggles
- Money RU: Хорошо, но с доплатой за риск.
- Money EN: Fine, but with extra for the risk.

### Mitigations
- Steiger or Monk hired RU: Штайгер (или Монк) уже в деле? Тогда я тоже.
- Steiger or Monk hired EN: Steiger (or Monk) is already in? Then count me in too.

## Phrases — VoiceResponse

- `voice_source: wildfire` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Лора здесь.» / «Laura's here.»
  - AimAttack (1): «Точно в цель.» / «Right on target.»
  - AimAttack (2): «Спокойно, работаю.» / «Steady, I've got this.»
  - OpponentKilled: «Готово.» / «Done.»
  - DeathGeneral: «Не смогла себя спасти...» / «Couldn't save myself...»
  - Downed: «Ранена, но держусь.» / «Hit, but holding on.»
  - CombatStartDetected: «Осторожно, противник рядом.» / «Careful, enemy nearby.»
  - LevelUp: «Опыт растёт.» / «Experience grows.»
  - AmmoLow: «Патроны на исходе.» / «Running low on ammo.»
  - Idle: «Жарко, но жду.» / «Hot, but waiting.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Laura |
| VoiceResponseId | Jazz_Laura |
| pollyvoice | Amy |
| Portrait | Mod/Dv3mFVN/MercPortraits/Laura.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Laura_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm |
| FallbackMissingVR | Fox |
| Sources | AIM sheet «Наемники из JA1/2»; origin=wildfire |

## Open blockers

- none
