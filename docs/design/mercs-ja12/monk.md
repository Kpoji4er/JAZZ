---
status: ready
priority: medium
origin: wildfire
unit_id: Jazz_Monk
portrait_id: Monk
affiliation: AIM
role: Scout
tier: Veteran
specialization: Stealth
gender: Male
nationality: Russia
voice_source: wildfire
starting_level: 4
will: 75
salary:
  starting: 2400
  increase: 200
  lv1: 1000
  max: 5500
medical_deposit: small
haggling: normal
executable: true
---

# Монк — Виктор «Монк» Колесников

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Виктор «Монк» Колесников | Viktor "Monk" Kolesnikov |
| Nick | Монк | Monk |
| AllCapsNick | МОНК | MONK |
| Title | Чеченский след | The Chechen Trail |
| Email | Monk@aim.com | Monk@aim.com |
| snype_nick | monk | monk |

## Bio

**RU:** Wildfire. Ветеран Чеченской войны, не любит вспоминать родину. Статы 80–90, Marksmanship 94, прочие навыки 20–30. Одиночка, действует лучше вдали от толпы. Симпатизирует Лоре; недолюбливает Ивана и Конрада.

**EN:** Wildfire. A Chechen war veteran who avoids talking about home. Stats in the 80-90 range, 94 Marksmanship, other skills 20-30. A loner who performs better away from a crowd. Has a soft spot for Laura; doesn't get along with Ivan or Conrad.

## Stats

| Stat | Value |
| --- | --- |
| Health | 88 |
| Agility | 85 |
| Dexterity | 80 |
| Strength | 80 |
| Wisdom | 70 |
| Will | 75 |
| Leadership | 25 |
| Marksmanship | 94 |
| Mechanical | 25 |
| Explosives | 25 |
| Medical | 20 |
| MaxHitPoints | 88 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- `Jazz_Perk_Monk`
- `Stealthy`
- `Loner`
- `NightOps`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Monk` |
| type | passive |
| DisplayName RU/EN | Маскировка / Camouflage |
| Description RU/EN | Бонус к скрытности и точности при первом выстреле из укрытия / Stealth and first-shot accuracy bonus while camouflaged in cover |
| Mechanics | While in any cover (Low or High) and unspotted, Monk gets +20% CTH on his first shot of a combat, and enemies must be within half their normal detection range to spot him — reinforces `Stealthy` for a genuine ambush specialist. |

## Personality

- Quirks: Loner (StartingPerk)
- Likes: `Jazz_Laura` (planned merc — Mitigation/ExtraPartingWords wiring activates once ready)
- Dislikes: `Ivan` (vanilla merc id, already shipped — Refusal wiring live immediately), `Jazz_Conrad` (already generated — Refusal wiring live immediately)
- National hates: none — his dislike of discussing "the motherland" is flavor-only and not tied to a nationality hire condition
- Refusal / Haggle notes: refuses if Ivan or Conrad hired; standard AIM money/death-toll refusals; mitigation if Laura hired

## Hire

- Access: AIM roster (Wildfire origin)
- MedicalDeposit: small; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Monk` → `JAZZ_Monk50/35/25/20`
- *50: `JazzArmor_SovietAssaultArmor`, `VSS`, `JAZZ_AMMO_9x39_AP`×30 (Double), `Knife_Sharpened`
- *35: `JazzArmor_SovietAssaultArmor`, `VSS`, `JAZZ_AMMO_9x39_AP`×20 (Double)
- *25: `JazzArmor_LeatherJacketBlk`, `AK74`, `JAZZ_AMMO_545_AP`×40 (Double)
- *20: `JazzArmor_LeatherJacketBlk`, `AK74`, `JAZZ_AMMO_545_AP`×30 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](monk.ja2-face.gif)

Файл: `monk.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `monk.ja2-face.gif` (same face identity). Russian special-forces look ~35, cold eyes, camo facepaint and ghillie hood down — NO rifle. Distant expression.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Camo paint, ghillie hood, suppressor pouch, sheathed combat knife

## Phrases — AIM chat

### Offline
- RU: Монк не в сети.
- EN: Monk's offline.

### GreetingAndOffer
- RU: Монк на связи.
- EN: Monk here.

### ConversationRestart
- RU: Связь прервалась. Продолжим.
- EN: Line dropped. Let's continue.

### IdleLine
- RU: ...
- EN: ...

### PartingWords
- RU: Хорошо. Иду один, как всегда.
- EN: Fine. I move alone, like always.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь.
- EN: I'm staying.

### Refusals
- Ivan/Conrad hired RU: Пока Иван или Конрад в отряде — нет. Не хочу иметь с ними дела.
- Ivan/Conrad hired EN: Not while Ivan or Conrad's on the team. I don't want to deal with them.
- Death toll RU: Слишком много смертей. Хватит с меня войны.
- Death toll EN: Too many deaths. I've had enough war.

### Mitigations
- Laura hired RU: Лора уже здесь? Тогда, пожалуй, соглашусь.
- Laura hired EN: Laura's already here? Then I suppose I'll agree.

### ExtraPartingWords
- RU: Если найдёте Лору — она надёжнее большинства.
- EN: If you find Laura — she's more reliable than most.

## Phrases — VoiceResponse

- `voice_source: wildfire` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Монк готов.» / «Monk's ready.»
  - AimAttack (1): «Цель в прицеле.» / «Target in sight.»
  - AimAttack (2): «Тихо.» / «Quiet.»
  - OpponentKilled: «Готово.» / «Done.»
  - DeathGeneral: «...» / «...»
  - Downed: «Ранен. Держусь.» / «Hit. Holding on.»
  - CombatStartDetected: «Замечен противник.» / «Enemy spotted.»
  - LevelUp: «Опыт не пропьёшь.» / «Experience doesn't fade.»
  - AmmoLow: «Патроны на исходе.» / «Running low on ammo.»
  - Idle: «Жду.» / «Waiting.»
  - MockDislike (Ivan/Conrad): «Только бы эти двое не мешали.» / «Just hope those two stay out of my way.»
  - Praises (Laura present): «С Лорой работать проще.» / «It's easier working with Laura around.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Monk |
| VoiceResponseId | Jazz_Monk |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Monk.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Monk_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=wildfire |

## Open blockers

- none
