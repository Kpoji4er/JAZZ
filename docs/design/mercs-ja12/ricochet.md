---
status: ready
priority: low
origin: ja2
unit_id: Jazz_Ricochet
portrait_id: Ricochet
affiliation: MERC
role: Melee
tier: Regular
specialization: Melee
gender: Male
nationality: USA
voice_source: ja2
starting_level: 3
will: 45
salary:
  starting: 800
  increase: 150
  lv1: 350
  max: 2400
medical_deposit: small
haggling: normal
executable: true
---

# Рикошет — Тим «Рикошет» Саттонн

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Тим «Рикошет» Саттонн | Tim "Ricochet" Sutton |
| Nick | Рикошет | Ricochet |
| AllCapsNick | РИКОШЕТ | RICOCHET |
| Title | Ближник | The Close-Quarters Man |
| Email | Ricochet@merc.com | Ricochet@merc.com |
| snype_nick | ricochet | ricochet |

## Bio

**RU:** Заниженные для ближнего боя статы (Agility 60, Strength 75), но Marksmanship 88 говорит о хорошей руке для бросков. Одиночка. Уважает Злобного; терпеть не может Сидни, Вики и Скоупа.

**EN:** Underwhelming stats for a melee specialist (60 Agility, 75 Strength), but a strong 88 Marksmanship gives his throwing arm real precision. A loner. Respects Vicious; can't stand Sidney, Vicki, or Scope.

## Stats

| Stat | Value |
| --- | --- |
| Health | 70 |
| Agility | 60 |
| Dexterity | 70 |
| Strength | 75 |
| Wisdom | 55 |
| Will | 45 |
| Leadership | 15 |
| Marksmanship | 88 |
| Mechanical | 15 |
| Explosives | 15 |
| Medical | 10 |
| MaxHitPoints | 70 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- `Jazz_Perk_Ricochet`
- `Loner`
- `Throwing`
- `MeleeTraining`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Ricochet` |
| type | passive |
| DisplayName RU/EN | Рикошет / Ricochet |
| Description RU/EN | Смертельный бросок ножа может отскочить на второго врага / A lethal thrown-knife kill can bounce to strike a second enemy |
| Mechanics | When a thrown knife or axe thrown by Ricochet kills its target, there is a 40% chance the blade ricochets to a second random enemy within 3 tiles of the target, dealing 50% of the weapon's normal damage. |

## Personality

- Quirks: Loner
- Likes: `Jazz_Vicious` (planned merc — Mitigation/ExtraPartingWords wiring activates once ready)
- Dislikes: `Sidney`, `Vicki`
- National hates: British — Haggle trigger when the active squad is full of British-nationality mercs (Scope dislike lore flavor)
- Refusal / Haggle notes: refuses if Sidney or Vicki hired; haggles when squad is all-British; standard MERC money refusal

## Hire

- Access: MERC hire
- MedicalDeposit: small; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Ricochet` → `JAZZ_Ricochet50/35/25/20`
- *50: `JazzArmor_CamoBalaclava`, `Knife_Balanced`×3, `Knife_Sharpened`×2, `Machete`
- *35: `Knife_Balanced`×2, `Knife_Sharpened`×2, `Machete`
- *25: `Knife_Balanced`×2, `Knife_Sharpened`×1
- *20: `Knife`×2

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](ricochet.ja2-face.gif)

Файл: `ricochet.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `ricochet.ja2-face.gif` (same face identity). Melee/throwing specialist ~30, night-ops headband, hand wraps, bandolier of knife sheaths — NO weapon in hand.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Hand wraps, night-ops bandana, knife-sheath bandolier

## Phrases — AIM chat

### Offline
- RU: Рикошет вне игры.
- EN: This is Ricochet. Leave a message.

### GreetingAndOffer
- RU: Рикошет слушает. Кого метать?
- EN: Ricochet here. Who am I throwing at?

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Жду цель.
- EN: Waiting for a target.

### PartingWords
- RU: Ножи наточены. Иду.
- EN: Blades are sharp. I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь.
- EN: I'm staying.

### Refusals
- Sidney/Vicki hired RU: Пока Сидни или Вики в отряде — я пас.
- Sidney/Vicki hired EN: Not while Sidney or Vicki are on the team.
- Money RU: Маловато для моих ножей.
- Money EN: Not enough for my knives.

### Haggles
- British mercs hired RU: Отряд полон британцев... ладно, но с доплатой.
- British mercs hired EN: Squad's full of Brits... fine, but it'll cost extra.

### Mitigations
- Vicious hired RU: О, Злобный уже здесь? Тогда я в деле.
- Vicious hired EN: Oh, Vicious is already in? Then I'm in.

### ExtraPartingWords
- RU: Если нужен ещё один клинок — зовите Злобного.
- EN: If you need another blade, call Vicious.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Рикошет на месте.» / «Ricochet's here.»
  - AimAttack (1): «Летит.» / «It's flying.»
  - AimAttack (2): «В цель.» / «On target.»
  - OpponentKilled: «Отскочило удачно.» / «Bounced just right.»
  - DeathGeneral: «Не отскочил в этот раз...» / «Didn't bounce this time...»
  - Downed: «Зацепили. Держусь.» / «They got me. Holding on.»
  - CombatStartDetected: «Клинки готовы.» / «Blades ready.»
  - LevelUp: «Рука твёрже.» / «Steadier hand now.»
  - AmmoLow: «Ножи заканчиваются.» / «Running low on knives.»
  - Idle: «Ну.» / «Well?»
  - MockDislike (Sidney/Vicki): «Хорошо, что их тут нет.» / «Good thing they're not here.»
  - Praises (Vicious present): «Хорошая компания сегодня.» / «Good company today.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Ricochet |
| VoiceResponseId | Jazz_Ricochet |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Ricochet.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Ricochet_Big.png |
| CustomEquipGear | TryEquip Handheld A Melee |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
