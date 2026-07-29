---
status: ready
priority: low
origin: ja2
unit_id: Jazz_Bull
portrait_id: Bull
affiliation: AIM
role: Melee
tier: Regular
specialization: Melee
gender: Male
nationality: USA
voice_source: ja2
starting_level: 2
will: 45
salary:
  starting: 400
  increase: 150
  lv1: 200
  max: 1500
medical_deposit: standard
haggling: normal
executable: true
---

# Бык — Джон «Бык» Питерс

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Джон «Бык» Питерс | John "Bull" Peters |
| Nick | Бык | Bull |
| AllCapsNick | БЫК | BULL |
| Title | Дешёвый танк | The Cheap Tank |
| Email | Bull@aim.com | Bull@aim.com |
| snype_nick | bull | bull |

## Bio

**RU:** Один из самых дешёвых наёмников AIM: Health 96, Strength 98, Agility/Dexterity ~50, Wisdom 64, Marksmanship 72. Агрессивен и бьёт первым. Дружит с Нейлсом; не любит Биффа.

**EN:** One of the cheapest mercs on AIM's roster: 96 Health, 98 Strength, roughly 50 Agility/Dexterity, 64 Wisdom, 72 Marksmanship. Aggressive and swings first. Friends with Nails; can't stand Biff.

## Stats

| Stat | Value |
| --- | --- |
| Health | 96 |
| Agility | 50 |
| Dexterity | 50 |
| Strength | 98 |
| Wisdom | 64 |
| Will | 45 |
| Leadership | 15 |
| Marksmanship | 72 |
| Mechanical | 5 |
| Explosives | 5 |
| Medical | 5 |
| MaxHitPoints | 96 |
| StartingLevel | 2 |

## Perks

### StartingPerks

- `Jazz_Perk_Bull`
- `MeleeTraining`
- `CQCTraining`
- `TrueGrit`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Bull` |
| type | passive |
| DisplayName RU/EN | Грудная клетка / Iron Ribcage |
| Description RU/EN | Ближний бой Быка может сбить дыхание или вырубить противника / Bull's melee attacks can knock the wind out of a target or knock them out cold |
| Mechanics | Unarmed and knife melee attacks by Bull against Torso have a 15% chance to inflict Off-Balance (target loses its next reaction) and a separate 5% chance to apply Unconscious for 1 turn. |

## Personality

- Quirks: Aggressive (bio flavor only — no matching JA3 status perk, not wired)
- Likes: `Nails`
- Dislikes: `Jazz_Biff` (planned merc — Refusal wiring activates once ready)
- National hates: —
- Refusal / Haggle notes: refuses if Biff hired; standard AIM money refusal; mitigation and recommendation for Nails when hired

## Hire

- Access: AIM hire
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Bull` → `JAZZ_Bull50/35/25/20`
- *50: `JazzArmor_LeatherVest`, `Knife`, `M2Carbine`, `JAZZ_AMMO_30_FMJ`×20 (Double)
- *35: `JazzArmor_LeatherArmor`, `Knife`, `Winchester1894`, `JAZZ_AMMO_30_FMJ`×16 (Double)
- *25: `Knife`, `Winchester1894`, `JAZZ_AMMO_30_P`×12 (Double)
- *20: `Knife`, `Unarmed`

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](bull.ja2-face.gif)

Файл: `bull.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `bull.ja2-face.gif` (same face identity). Massive cheap AIM bruiser ~30, bald, scarred knuckle wraps, torn sleeveless shirt — NO gun. Dumb confident grin.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Knuckle wraps, torn shirt, AIM pin

## Phrases — AIM chat

### Offline
- RU: Бык спит. Не будить.
- EN: This is Bull. Leave a message.

### GreetingAndOffer
- RU: Бык! Чо, бить будем?
- EN: Bull here. We fighting or what?

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Где враги? Хочу бить.
- EN: Where's the enemy? I wanna hit something.

### PartingWords
- RU: Угх. Иду бить.
- EN: Ugh. I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Тут есть кого бить.
- EN: I'm staying. Plenty to hit here.

### Refusals
- Biff hired RU: Пока Бифф в отряде — я пас. Он мне не нравится.
- Biff hired EN: Not while Biff's on the team. Don't like the guy.
- Money RU: Мало. Бык дёшево, но не бесплатно.
- Money EN: Not enough. Bull's cheap, not free.

### Mitigations
- Nails hired RU: О, Нейлс уже тут? Тогда порядок.
- Nails hired EN: Oh, Nails is already in? Then we're good.

### ExtraPartingWords
- RU: Если нужен ещё крепкий парень — берите Нейлса.
- EN: If you need another tough guy, grab Nails.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Бык готов.» / «Bull's ready.»
  - AimAttack (1): «Иду ломать!» / «Coming in to break stuff!»
  - AimAttack (2): «Получай!» / «Take this!»
  - OpponentKilled: «Готов.» / «Down.»
  - DeathGeneral: «Не... тот бой...» / «Not... this fight...»
  - Downed: «Меня зацепили!» / «I'm hit!»
  - CombatStartPlayer: «Наконец-то драка!» / «Finally, a fight!»
  - LevelUp: «Бык сильнее!» / «Bull's stronger!»
  - AmmoLow: «Патроны кончаются, буду бить руками.» / «Low on ammo, I'll just punch.»
  - Idle: «Ну?» / «Well?»
  - MockDislike (Biff): «Хорошо, что Биффа тут нет.» / «Good thing Biff's not here.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Bull |
| VoiceResponseId | Jazz_Bull |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Bull.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Bull_Big.png |
| CustomEquipGear | TryEquip Handheld A Melee |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
