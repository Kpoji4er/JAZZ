---
status: ready
priority: high
origin: nightops
unit_id: Jazz_Mike
portrait_id: Mike
affiliation: AIM
role: AllRounder
tier: Elite
specialization: AllRounder
gender: Male
nationality: USA
voice_source: nightops
starting_level: 6
will: 85
salary:
  starting: 4000
  increase: 200
  lv1: 2000
  max: 9000
medical_deposit: large
haggling: normal
executable: true
---

# Майк — Майк

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Майк | Mike |
| Nick | Майк | Mike |
| AllCapsNick | МАЙК | MIKE |
| Title | Старый друг | Old Friend |
| Email | Mike@aim.com | Mike@aim.com |
| snype_nick | oldfriend | oldfriend |

## Bio

**RU:** Классика JA1. В Night Ops — перевербовка вражеского солдата в бою в AIM-специалиста; в модах для JA2 (1.13) — прямой найм через AIM. Одиночка по натуре, но именно поэтому надёжен один на один. Дружит со Стероидом; JA2-байки про вражду с Гасом и Иваном остаются флейвором, пока эти отношения не подтверждены отдельным дизайном.

**EN:** A JA1 classic. In Night Ops he's a battlefield conversion — an enemy soldier flipped mid-fight into an AIM-grade specialist; JA2 mod scenes (1.13) hire him straight through AIM instead. A loner by nature, which is exactly why he's dependable one-on-one. Friends with Steroid (vanilla AIM merc); the old JA2 rumors about beef with Gus and Ivan stay flavor-only until that relationship gets its own confirmed design pass.

## Stats

| Stat | Value |
| --- | --- |
| Health | 90 |
| Agility | 85 |
| Dexterity | 85 |
| Strength | 85 |
| Wisdom | 80 |
| Will | 85 |
| Leadership | 50 |
| Marksmanship | 90 |
| Mechanical | 40 |
| Explosives | 40 |
| Medical | 40 |
| MaxHitPoints | 90 |
| StartingLevel | 6 |

## Perks

### StartingPerks

- `Jazz_Perk_Mike`
- `Loner`
- `NightOps`
- `AutoWeapons`
- `TakeAim`
- `Counterfire`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Mike` |
| type | passive |
| DisplayName RU/EN | Быстрая реакция / Quick Reaction |
| Description RU/EN | Первым замечает угрозу и получает свободное действие при обнаружении врага вне боя / First to spot a threat: gains a free action the instant an enemy is detected outside of combat |
| Mechanics | When Mike (not the squad) is the unit that triggers enemy detection outside active combat, he immediately receives 4000 AP worth of free action (equivalent to one extra move/attack tick) before initiative order is rolled — mechanically distinct from `Counterfire`/`NightOps` already on the sheet, which cover the reactive/vision side. |

## Personality

- Quirks: `Loner` (StartingPerk; performs better solo or with few nearby mercs)
- Likes: `Steroid` (vanilla AIM merc, already shipped in this mod's UnitData overrides — Mitigation/ExtraPartingWords wiring is live immediately, no dependency on other planned articles)
- Dislikes: none confirmed — Gus/Ivan mentions are JA2-lore flavor in Bio only; both exist as vanilla merc ids (`Gus`, `Ivan`) in this mod, but no Dislike/Refusal is implemented until a dedicated design pass confirms the relationship (avoids inventing an unapproved hire penalty against two already-shipped vanilla mercs)
- National hates: none
- Refusal / Haggle notes: standard AIM recruit, no special refusal triggers beyond the vanilla money/death-toll defaults

## Hire

- Access: AIM roster (JA3-native hire; no battlefield-conversion encounter exists in JAZZ's current scope, so the Night Ops "flip an enemy mid-fight" hook stays a Bio reference only, not an implemented recruit path)
- MedicalDeposit: large; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Mike` → `JAZZ_Mike50/35/25/20`
- *50: `JazzArmor_PASGT`, `M16A1`, `JAZZ_AMMO_556_EPR`×40 (Double), `FirstAidKit`, `SmokeGrenade`×1
- *35: `JazzArmor_PoliceVest`, `Galil`, `JAZZ_AMMO_556_FMJ`×60 (Double)
- *25: `JazzArmor_PoliceVest`, `AK47`, `JAZZ_AMMO_762x39_FMJ`×60 (Double)
- *20: `JazzArmor_LeatherJacketBrn`, `AK47`, `JAZZ_AMMO_762x39_FMJ`×30 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](mike.ja2-face.gif)

Файл: `mike.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `mike.ja2-face.gif` (same face identity). Grizzled American AIM veteran, short hair, confident half-smile, night-ops goggles on helmet and reaction timer watch — NO weapon in hands. Classic merc look.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** NV goggles on helmet, chronometer, AIM pin

## Phrases — AIM chat

### Offline
- RU: Майк. Перезвоните — если срочно, я перезвоню первым.
- EN: This is Mike. Call back — if it's urgent, I'll call you first.

### GreetingAndOffer
- RU: Старый друг на линии. Ну, что у тебя за дело?
- EN: Old friend on the line. So, what's the job?

### ConversationRestart
- RU: Пропала связь. Ладно, продолжаем — я никуда не спешу.
- EN: Line dropped. Fine, let's continue — I'm not in a hurry.

### IdleLine
- RU: Говори. Я слушаю, но недолго.
- EN: Talk. I'm listening, but not for long.

### PartingWords
- RU: Как в старые добрые. Я в деле.
- EN: Just like the old days. I'm in.

### RehireIntro
- RU: Контракт заканчивается. Обычно я ухожу тихо — но спрошу: продлеваем?
- EN: Contract's ending. Normally I'd just slip away — but I'll ask: extending?

### RehireOutro
- RU: Остаюсь. Одному веселее, но и тут ничего.
- EN: I'm staying. Solo's more fun, but this'll do.

### Mitigations
- Steroid hired RU: Стероид уже в отряде? Тогда ладно, с ним сработаемся.
- Steroid hired EN: Steroid's already on the team? Then fine, we work well together.

### ExtraPartingWords
- RU: Если нужен ещё один надёжный ствол — зовите Стероида.
- EN: If you need another dependable gun — call Steroid.

## Phrases — VoiceResponse

- `voice_source: nightops` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Майк на месте.» / «Mike's in position.»
  - AimAttack (1): «Вижу цель.» / «Target in sight.»
  - AimAttack (2): «Работаю спокойно.» / «Working it calm.»
  - OpponentKilled: «Чисто.» / «Clean.»
  - DeathGeneral: «Не в этот раз...» / «Not this time...»
  - Downed: «Подбили — но я держусь.» / «I'm hit — but holding.»
  - CombatStartDetected: «Вижу их первым.» / «I see them first.»
  - LevelUp: «Опыт не пропьёшь.» / «Experience doesn't fade.»
  - AmmoLow: «Патроны на исходе.» / «Running low on ammo.»
  - Idle: «Жду сигнала — один, как обычно.» / «Waiting on the signal — alone, as usual.»
  - Praises (Steroid present): «Хорошо, что Стероид рядом.» / «Good to have Steroid around.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Mike |
| VoiceResponseId | Jazz_Mike |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Mike.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Mike_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=nightops |

## Open blockers

- none
