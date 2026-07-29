---
status: ready
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
executable: true
---

# Зануда — Леннарт «Зануда» Вильде

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Леннарт «Зануда» Вильде | Lennart "Vilde" Wilde |
| Nick | Зануда | Vilde |
| AllCapsNick | ЗАНУДА | VILDE |
| Title | Тоже эстонец | Also Estonian |
| Email | Vilde@aim.com | Vilde@aim.com |
| snype_nick | vilde | vilde |

## Bio

**RU:** Wildfire. Статы ~80, Leadership 67, Marksmanship 74. Плохо переносит жару. Педантичен до занудства — отсюда прозвище. Любит Аллика и Монка; недолюбливает Доктора Кью и Линкса.

**EN:** Wildfire mercenary. Stats around 80, 67 Leadership, 74 Marksmanship. Handles heat poorly. Pedantic to the point of being tedious — hence the nickname. Fond of Allik and Monk; not fond of Dr.Q or Lynx.

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

- `Jazz_Perk_Vilde`
- `AutoWeapons`
- `NightOps`
- `LeadFromTheFront`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Vilde` |
| type | passive |
| DisplayName RU/EN | Ночной автоматчик / Night Gunner |
| Description RU/EN | Ночью автоматный огонь Вильде точнее / At night, Vilde's automatic fire is more accurate |
| Mechanics | During Nighttime missions, Full-Auto and burst attacks fired by Vilde gain +15% CTH and his Perception range for spotting is not reduced by darkness. |

## Personality

- Quirks: FearHeat
- Likes: `Jazz_Allik`, `Jazz_Monk`
- Dislikes: `DrQ`, `Jazz_Lynx`
- National hates: —
- Refusal / Haggle notes: refuses if Jazz_Lynx or DrQ are in the active squad; mitigation and rate discount when Jazz_Allik or Jazz_Monk are hired

## Hire

- Access: AIM
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Vilde` → `JAZZ_Vilde50/35/25/20`
- *50: `JazzArmor_NightCamoJacket`, `RPK`, `JAZZ_AMMO_762x39_FMJ`×80 (Double), `NVGoggles`
- *35: `M60`, `JAZZ_AMMO_762x51_FMJ`×80 (Double)
- *25: `M2Carbine`, `JAZZ_AMMO_30_FMJ`×40 (Double)
- *20: `AK47`, `JAZZ_AMMO_762x39_FMJ`×40 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](vilde.ja2-face.gif)

Файл: `vilde.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `vilde.ja2-face.gif` (same face identity). Estonian night auto-trooper, NV goggles on helmet — NO gun. Pedantic look.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** NV goggles, night camo, notebook

## Phrases — AIM chat

### Offline
- RU: Вильде недоступен. Оставьте сообщение по форме.
- EN: Vilde unavailable. Leave a properly formatted message.

### GreetingAndOffer
- RU: Вильде. По пунктам, пожалуйста.
- EN: Vilde. Point by point, please.

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу, по порядку.
- EN: Line dropped. Let's get back to it, in order.

### IdleLine
- RU: Жарко. Это не по инструкции.
- EN: It's hot. This isn't per protocol.

### PartingWords
- RU: Условия приняты. Иду.
- EN: Terms accepted. I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Всё по плану.
- EN: I'm staying. Everything's on schedule.

### Refusals
- Lynx or DrQ hired RU: Пока эти двое в отряде — я не подписываюсь.
- Lynx or DrQ hired EN: Not while those two are on the team.
- Money RU: Сумма не соответствует расчёту.
- Money EN: The sum doesn't match the calculation.

### Haggles
- Money RU: Пересчитайте ещё раз — и договоримся.
- Money EN: Recalculate once more — then we'll agree.

### Mitigations
- Allik or Monk hired RU: Аллик (или Монк) уже здесь? Тогда всё по плану.
- Allik or Monk hired EN: Allik (or Monk) is already in? Then everything's on schedule.

## Phrases — VoiceResponse

- `voice_source: wildfire` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Вильде на позиции.» / «Vilde in position.»
  - AimAttack (1): «Очередь по плану.» / «Burst, as planned.»
  - AimAttack (2): «Ночью виднее.» / «Better in the dark.»
  - OpponentKilled: «Цель нейтрализована, по инструкции.» / «Target down, per protocol.»
  - DeathGeneral: «Ошибка в расчётах...» / «Miscalculation...»
  - Downed: «Ранен. Требуется корректировка.» / «Hit. Adjustment required.»
  - CombatStartDetected: «Противник обнаружен, зафиксировано.» / «Enemy detected, logged.»
  - LevelUp: «Прогресс зафиксирован.» / «Progress logged.»
  - AmmoLow: «Патроны на исходе, как и предупреждал.» / «Ammo low, as I warned.»
  - Idle: «Жарко. Неэффективно.» / «Hot. Inefficient.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Vilde |
| VoiceResponseId | Jazz_Vilde |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Vilde.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Vilde_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm (two-handed auto) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=wildfire |

## Open blockers

- none
