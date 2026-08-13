---
id: JAZZ-UNITS-006
status: approved
owner: project-owner
systems:
  - units-progression-specializations
  - localization
repositories:
  - jazz
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/CharacterEffect/Jazz_Perk_*.lua
  - jazz/CharacterEffect/Jazz_OrderCTH.lua
  - jazz/CharacterEffect/<VanillaPersonalPerkId>.lua
  - jazz/CharacterEffect/GrizzlyPerk.lua
  - jazz/CharacterEffect/GruntyPerk_JAZZ.lua
  - jazz/Code/**
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/design/mercs-ja12/_named-perks-plan.md
  - jazz/docs/design/mercs-ja12/<slug>.md
  - jazz/docs/showcase/ru/perks.md
  - jazz/docs/showcase/en/perks.md
  - jazz/docs/wiki/**
  - jazz/docs/technical/systems/**
  - jazz/docs/specs/active/JAZZ-UNITS-003.md
  - jazz-units/CharacterEffect/**
  - jazz-units/UnitData/**
  - jazz-units/items.lua
  - jazz-units/metadata.lua
exclusive_resources:
  - jazz/items.lua
  - jazz-units/items.lua
  - localization ID range 890000000006300-890000000006499
related_decisions:
  - none
approved_by: "project-owner chat 2026-08-08 (Лист2 sync + locked decisions; full approve via «делай спеку полностью»)"
source_sheet: "https://docs.google.com/spreadsheets/d/1h6Q_NXa3M1W8nQ59KQAJZIn58SNbDcR7_6IvdfpPuLY/edit?gid=1481453815#gid=1481453815 (Лист2)"
---

# uJAZZ-UNITS-006: Named perks — sync Лист2 (rewire deltas + vanilla)

## Проблема

Google Sheet **JAZZ Mercs → Лист2** задаёт целевые имена/механики именных перков (`сигна` + `JAZZ MOD`) для всего ростера: JA12/`Jazz_Perk_`* и оригинальных JA3. Часть JA12 уже зашита по `JAZZ-UNITS-003` и расходится с листом; ванильные personal часто тоже ≠ лист. Нужна единая каноническая сверка **оригинал → Лист2** и реализация батчами.

**Канон дизайна:** Лист2 + Locked decisions / Mechanics ниже.  
**Оригинал:** текущий wired эффект (vanilla CE / JAZZ override / `JAZZ-UNITS-003` / stub article).

## Цели

- Матрицы §A (JA12 wired rewire), §B (JA12 stubs), §C (оригинальные JA3), §D (Benni/Simon без CE).
- Реализация батчами после этой спеки: runtime + RU/EN + showcase/wiki/technical в каждом батче.
- `JAZZ-UNITS-003` Mechanics для Ids §A — **superseded** этой спекой.
- Ванильные personal: сохранять perk id (`UndefineClass` → `DefineClass.<SameId>`), кроме уже существующих `GruntyPerk_JAZZ`, `InnerInfo_JAZZ`.

## Non-goals

- Друзья/враги/национальность/ростер-мета Лист2 (только K/L).
- Переписывать MATCH Ids без нужды: Frag (`Jazz_Perk_00`), Buzz, Lynx, Spider, Colby, Vilde, Eskimo≈, Vicious≈.
- Soft-keep stubs (текст листа ≈ article, hook можно отложить до батча §B): Hobbit, Gamos, Devin, Gaston, Quinten, Dimitri, Cord (уже в §B если bar-city), — если Id уже в §B, §B побеждает.
- Реализация кода в approve-коммите спеки: код только по отдельному запросу на батч.

## Требования

- `JAZZ-UNITS-006-REQ-001` — канон §A/§B/§C/§D = Лист2 + Locked decisions / Mechanics.
- `JAZZ-UNITS-006-REQ-002` — §A: runtime = Mechanics; DisplayName/Description RU+EN без WIP и без Wave A текста.
- `JAZZ-UNITS-006-REQ-003` — §B: companion + generation article под Лист2/Mechanics; UI без устаревшего имени.
- `JAZZ-UNITS-006-REQ-004` — §C: Verdict≠MATCH по правилам §C; Grunty = T1 +50% AP + per-turn Morale proc.
- `JAZZ-UNITS-006-REQ-005` — sync items/CE/metadata; loc needs RU=0 / EN=0 на затронутых строках батча.
- `JAZZ-UNITS-006-REQ-006` — showcase RU|EN perks (+ wiki/technical) отражают deltas батча.
- `JAZZ-UNITS-006-REQ-007` — docs-пометка supersede в `JAZZ-UNITS-003` для Ids §A.
- `JAZZ-UNITS-006-REQ-008` — полная замена vanilla personal сохраняет perk id; StartingPerks не ломают ссылки.
- `JAZZ-UNITS-006-REQ-009` — Steiger = «Вожак стаи»; Rothman = «Я вас научу работать!» (mine); Henning = +3 AP@10.
- `JAZZ-UNITS-006-REQ-010` — §D: создать `Jazz_Perk_Benny` / `Jazz_Perk_Simon` + StartingPerks + loc + icons path per merc-create conventions.
- `JAZZ-UNITS-006-REQ-011` — Flo/Static в §B с locked числами (лист был обрезан).

## Locked decisions (chat 2026-08-08)


| Тема                        | Решение                                                                                      |
| --------------------------- | -------------------------------------------------------------------------------------------- |
| Канон                       | Эта спека supersede `JAZZ-UNITS-003` §A Mechanics                                            |
| Nervous                     | стек +пуль за хит очереди, **cap = 10**                                                      |
| Lucky                       | CTH≥**70%** miss → **reroll**                                                                |
| Grizzly                     | **микс G1:** только на `GrizzlyPerk` — WEAPONS-012 ignore + **2×** длинная очередь + полный урон + **2×** suppress |
| Meltdown                    | **CHANGE:** активка `VengefulTemperament` («Ураган Норма») — враги ≤5 от Meltdown → Panic/Berserk по Wisdom; **не** RunAndGun; **не** vanilla Hard Feelings / Vengeance mark |
| Henning / Steiger / Rothman | как на листе (см. Mechanics)                                                                 |
| §C                          | in scope; **батчи ok**                                                                       |
| §C числа                    | явные числа листа → лист; Verdict≈ → shipping vanilla/JAZZ ядро                              |
| Grunty                      | T1 +50% AP + каждый ход **10% × уровень БД (Morale)**                                        |
| Blade                       | ванильный `**Brutalize**` («Зверство»), не Wave A +20 CTH                                    |
| Cougar                      | SK → Inspired 1×/turn (не ОД)                                                                |
| Flay                        | +10% dmg per **enemy** with bleed, не по стакам                                              |
| Spike                       | CD убийством; убрать 1×/бой                                                                  |
| Flo / Static                | в scope; числа locked ниже                                                                   |
| Soft gaps                   | Vince **−25%** med cost; Madman Will drain **10**                                            |


### Mechanics (locked)


| Id                  | Целевой эффект                                                                                                                                                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Jazz_Perk_Henning` | «Полевой командир»: +**3 AP** союзникам в **10** slabs в начале их хода / aura на ход (реализация: status AP buff на allies ≤10 при OnBeginTurn Henning или эквивалент)                                                        |
| `Jazz_Perk_Steiger` | «Вожак стаи»: Night/Underground: allies ≤**10** → +**5** CTH (переименовать с «Ночной инструктор»; радиус 5→10)                                                                                                                |
| `Jazz_Perk_Rothman` | «Я вас научу работать!»: mine sector op — доход/охрана; эффект сильнее при низкой loyalty                                                                                                                                      |
| `Jazz_Perk_Nervous` | каждый хит burst/auto стекает +1 пулю на следующую очередь/авто; **cap +10**; сброс после атаки-потребителя                                                                                                                    |
| `Jazz_Perk_Lucky`   | если CTH≥70% и miss → один reroll того же shot                                                                                                                                                                                 |
| `Jazz_Perk_Laura`   | после heal/bandage союзника: Laura +**15** CTH и +**15** crit до конца следующего хода                                                                                                                                         |
| `Jazz_Perk_Dynamo`  | lockpick не триггерит lock traps                                                                                                                                                                                               |
| `Jazz_Perk_Madman`  | melee crit или kill → всем в ≤5 slabs (включая союзников) **−10 Will** (один proc на событие)                                                                                                                                  |
| `Jazz_Perk_Blade`   | модифицирует `**Brutalize**`: каждый успешный удар в цепочке → ещё один hit                                                                                                                                                    |
| `Jazz_Perk_Shank`   | 50% melee defense; при промахе melee по нему — knife throwback если цель ≤8                                                                                                                                                    |
| `Jazz_Perk_Vince`   | squad-wide **−25%** расход medkit charges / Meds на combat heal и satellite medical ops, пока Vince в отряде                                                                                                                   |
| `Jazz_Perk_Mike`    | Overwatch и PinDown: **+2** атаки; reaction/interrupt always fire when eligible                                                                                                                                                |
| `Jazz_Perk_Flo`     | «Теоретически подкована»: **−12% buy / +12% sell**; Flo в active squad; аддитивно с Negotiator                                                                                                                                 |
| `Jazz_Perk_Static`  | «Собрал на коленке»: Parts cost repair/craft Static **−5% × Level**, **cap −25%**                                                                                                                                              |
| `GrizzlyPerk`       | G1: signature only — WEAPONS-012 unsupported ignore + 2× long-burst shots + full damage + 2× suppression                                                                                                                          |
| `VengefulTemperament` | Meltdown **active** signature («Ураган Норма», CombatAction id = perk class): enemies within **≤5** slabs of Meltdown → fail Wisdom(50) → `Panicked`, else `Berserk`, then refresh AP; timed signature recharge; **not** RunAndGun; replaces vanilla Hard Feelings (Vengeance mark) |
| `GruntyPerk_JAZZ`   | (1) combat start → +50% AP first turn; (2) each later turn: proc +50% AP with chance `**10 × MoraleLevel`%** where MoraleLevel = unit personal morale integer used by JA3 UI/combat (floor 0); `InteractionRand(100) < chance` |


## §A — CHANGE vs WIRED JA12


| Merc / Id                     | Оригинал               | Цель                              |
| ----------------------------- | ---------------------- | --------------------------------- |
| Henning / `Jazz_Perk_Henning` | OrderCTH +5 @5         | +3 AP aura @10                    |
| Laura / `Jazz_Perk_Laura`     | Heal → Hidden          | +15 CTH & crit after heal         |
| Lucky / `Jazz_Perk_Lucky`     | 1×/combat miss→hit     | CTH≥70% miss → reroll             |
| Dynamo / `Jazz_Perk_Dynamo`   | Head 25% Blinded       | Lockpick skips lock traps         |
| Nervous / `Jazz_Perk_Nervous` | Autofire/burst +2      | Stack +bullets, cap 10            |
| Madman / `Jazz_Perk_Madman`   | Kill Dist≤1 → Inspired | Melee crit/kill → −10 Will ≤5 all |
| Blade / `Jazz_Perk_Blade`     | Melee +20 CTH, crit=0  | Brutalize: success → extra hit    |
| Shank / `Jazz_Perk_Shank`     | Melee vs him −50 CTH   | 50% melee def + knife counter ≤8  |
| Steiger / `Jazz_Perk_Steiger` | Night OrderCTH @5      | «Вожак стаи» night/UG +5 CTH @10  |
| Vince / `Jazz_Perk_Vince`     | Bandage → +4 AP        | −25% med cost squad               |
| Mike / `Jazz_Perk_Mike`       | Stub                   | OW/PinDown +2; reactions always   |


## §B — CHANGE stub/article JA12


| Id                   | Цель (Лист2 / locked)                                                         | Было                     |
| -------------------- | ----------------------------------------------------------------------------- | ------------------------ |
| `Jazz_Perk_Iggy`     | Mortar scatter −33%                                                           | «Совесть дезертира»      |
| `Jazz_Perk_Grom`     | GL/mortar/AT 2× suppress                                                      | «Артподготовка»          |
| `Jazz_Perk_Rothman`  | Mine op loyalty-scaled                                                        | «Шахтёрский надзор»      |
| `Jazz_Perk_Highball` | Med ±50% if ally doctor Med≥80 within 5 / sat in squad                        | «Полевой химик»          |
| `Jazz_Perk_Hitman`   | Active mark always-see; no vision CTH pen; CD kill                            | «Вырубить»               |
| `Jazz_Perk_Bull`     | Fist trauma by body part; +2 ammo/grenade slots                               | «Грудная клетка»         |
| `Jazz_Perk_Meat`     | Will never drops; WP dmg→Grit; unsuppressible                                 | «Толстокожий»            |
| `Jazz_Perk_Ricochet` | Melee splash dmg to enemy ≤1 from target                                      | «Рикошет»                |
| `Jazz_Perk_Monk`     | Active silenced SK if CTH>70% always; CD kill                                 | «Маскировка»             |
| `Jazz_Perk_Horg`     | Active perfect 40mm/AT; CD kill                                               | «Тяжёлая рука»           |
| `Jazz_Perk_Kulba`    | US autos −50% recoil (M3/Thompson/M4/M16/BAR/M60/M14/M1 carbine auto)         | «Оружейник…»             |
| `Jazz_Perk_Carlos`   | Detected 33% slower; failed SK may stay hidden                                | «Тихая тень»             |
| `Jazz_Perk_Cougar`   | Shots −33% noise; SK → Inspired 1×/turn                                       | «Мягкая лапа»            |
| `Jazz_Perk_Grace`    | First knife throw/turn auto-hit ≤12                                           | ≤4 plan                  |
| `Jazz_Perk_Allik`    | Med/Exp/Mech checks +15–25 random (not sat)                                   | XP checks                |
| `Jazz_Perk_Biggens`  | Each successive own blast +10% dmg                                            | Mines plan               |
| `Jazz_Perk_Manuel`   | Active pistol/SMG/melee guaranteed SK no reveal; CD kill                      | Stealth near             |
| `Jazz_Perk_Ira`      | Militia she trains: +20 random primary stat                                   | Training speed           |
| `Jazz_Perk_Miguel`   | Aura 30: +30 Will/+15 CTH if up; −30/−15 if downed                            | Militia AP               |
| `Jazz_Perk_Conrad`   | As trainer, Leadership treated as floor 90                                    | Teacher stacking         |
| `Jazz_Perk_Cord`     | Faster/cheaper repair in city sector with bar                                 | Generic repair           |
| `Jazz_Perk_Biff`     | Train paid MERC troopers (move/attach/guard; daily pay; mass leave if unpaid) | Same theme stub          |
| `Jazz_Perk_Flo`      | −12% buy / +12% sell                                                          | «Барахольщица» WIP       |
| `Jazz_Perk_Static`   | Parts −5%/level repair/craft, cap −25%                                        | «Экономия запчастей» WIP |


## §C — Оригинальные JA3

**Правила:** CHANGE + явный лист → лист; ≈ → shipping ядро + cosmetic name/text; MATCH → не трогать.

Aliases: Vicky→`Vicki`, Kalina→`Kalyna`, Larryclean→`Larry_Clean`, Pierre→`PierreMerc`.


| Merc                | Perk id                 | Цель                                                                              | Verdict |
| ------------------- | ----------------------- | --------------------------------------------------------------------------------- | ------- |
| Ice                 | `IcePerk`               | Пять выстрелов по конечностям                                                     | CHANGE  |
| Steroid             | `SteroidPunch`          | Passive: melee CTH from Strength; unarmed hit→vanilla `ResolveSteroidPunch` knockback; Passive hotbar; no stim tiredness; Burning DoT −30% | CHANGE  |
| Barry               | `DesignerExplosives`    | vanilla ShapedCharge 2×/168h + Craft Explosives; ammo/grenade craft −30% Parts | CHANGE  |
| Blood               | `HundredKnives`         | Run and throw knives                                                              | ≈       |
| Vicki               | `WeaponPersonalization` | Self-repair 1%/h; full-mod +dmg/+crit (vanilla magnitudes)                        | ≈       |
| Wolf                | `JackOfAllTrades`       | Any op −33% time                                                                  | CHANGE  |
| Gus                 | `WeGotThis`             | Kill → +10 Grit squad                                                             | CHANGE  |
| Nails               | `NailsPerk`             | After first kill +20% dmg                                                         | CHANGE  |
| Grizzly             | `GrizzlyPerk`           | G1: 2× long burst + full dmg + WEAPONS-012 ignore + 2× suppress (signature only) | CHANGE  |
| Reaper              | `TheGrim`               | Active; kill Panic ≤8; **recharge after 5 kills** (not 1)                          | CHANGE  |
| Ivan                | `YouSeeIgor`            | Kill → +3 AP                                                                      | CHANGE  |
| Igor                | `Nazdarovya`            | Active (2 AP, **recharge_on_kill=1**): clear Pain, heal 15–20 HP, Drunk stack≤5 (−15 CTH / +20 melee per stack); sat decay 1 stack / 3h | CHANGE  |
| Kalyna              | `KalynaPerk`            | Armor-ignore shot                                                                 | ≈       |
| Meltdown            | `VengefulTemperament`   | Active fear ≤5 Panic/Berserk (Wisdom); no RnG; not vanilla Vengeance | CHANGE  |
| Len                 | `OnMyTarget`            | Squad attacks marked target; **10 AP**                                            | CHANGE  |
| Fox                 | `FoxPerk`               | First attack no alert / free AP                                                   | ≈       |
| Scully              | `ShoulderToShoulder`    | End turn +15 Grit self+nearby                                                     | CHANGE  |
| Magic               | `SecondStoryMan`        | +50% crit from above                                                              | CHANGE  |
| MD                  | `BuildingConfidence`    | Inspired (+4 AP) turns 2/5/8…; heal ±10%/level-diff vs patient, cap ±50%, combat+sat | CHANGE  |
| Mouse               | `LightStep`             | Does not trigger OW zones                                                         | ≈       |
| Omryn               | `EyesOnTheBack`         | Active 360 OW                                                                     | ≈       |
| Raider              | `TagTeam`               | +15% CTH vs ally PinDown targets                                                  | CHANGE  |
| Red                 | `HaveABlast`            | Toggle: grenade retaliate on hit/miss; blast dmg −50% while on; hands+inventory pull | CHANGE  |
| Buns                | `BunsPerk`              | +10% CTH vs ally-damaged this turn                                                | CHANGE  |
| Sidney              | `SidneyPerk`            | +2 AP start until miss/dmg taken                                                  | CHANGE  |
| Raven               | `Spotter`               | PinDown→Marked→ next hit 100% crit                                                | CHANGE  |
| Scope               | `HawksEye`              | Sniper Overwatch 1 AP (keep leftover); PinDown min 1 AP; biscuits on hire; sniper suppress ×2 | CHANGE  |
| Hitman              | `DedicatedCamper`       | Stationary +25% dmg; ≥25 dmg → +15 Grit                                           | CHANGE  |
| Tex                 | `DanceForMe`            | Legs AoE + OW                                                                     | ≈       |
| Shadow              | `FleetingShadow`        | Stealth run; +10 Grit on SK                                                       | ≈       |
| Thor                | `NaturalHealing`        | Joints (`HerbalMedicine` / 48h); sat squad +15% trauma/burn/HP debt recovery (not infection); bandage +20–25 Will | CHANGE  |
| Livewire            | `InnerInfo_JAZZ`        | More intel from hacks; money-making op                                            | CHANGE  |
| Fauda               | `KillingWind`           | ≥2 enemies hit → +8 Grit **each**; armor FM pen ×½ (with Ironclad: still ×½ once); cumbersome keeps FreeMove | CHANGE  |
| Fidel               | `DoubleToss`            | Two grenades; hands **or** `GrenadesInventory` pockets (`DoubleTossAG–DG`, stack ≥2) | CHANGE  |
| Grunty              | `GruntyPerk_JAZZ`       | T1 +50% AP + per-turn 10%×Morale                                                  | CHANGE  |
| DrQ                 | `ExplodingPalm`         | Fist statuses by HP; sat trauma heal +30%; infection resist                       | CHANGE  |
| Flay                | `MakeThemBleed`         | Groin/animal bleed; +10%/enemy with bleed in sight cap 50%                        | CHANGE  |
| Larry / Larry_Clean | `DangerClose`           | Explosives ≤5 +40% (vanilla params); guns ≥8 +40% +2 bleed; keep rangeThreshold (grenade UI) | CHANGE  |
| PierreMerc          | `GloryHog`              | Charge not only straight +15 grit; recruit 1 enemy/combat (not bosses)            | CHANGE  |
| Smiley              | `RecklessAssault`       | Maneuver SMG/carbine/AR 4 attacks + CTH                                           | CHANGE  |
| Spike               | `BulletHell`            | AoE 15/30 (100/200% dmg) prone+suppress; **CD on kill**                           | CHANGE  |


## §D — Missing CE (create)


| Merc  | Цель с листа                                                                           | Deliverable                             |
| ----- | -------------------------------------------------------------------------------------- | --------------------------------------- |
| Benni | «Вам посылка»: active lure decoy ≤8, Will-based (or lowest Will); explosion on arrival | `Jazz_Perk_Benny` + StartingPerks + loc |
| Simon | «Абсолютный снайпер»: active perfect shot any weapon with ≥4× optic; CD kill           | `Jazz_Perk_Simon` + StartingPerks + loc |


## Батчи реализации (порядок)

1. **§A combat** — Henning, Laura, Lucky, Dynamo, Nervous, Madman, Blade, Shank, Steiger, Vince, Mike + UNITS-003 supersede note.
2. **§C combat CHANGE** — Ice, Steroid, Grizzly G1, Grunty Morale, Ivan, Nails, Gus, Wolf, Magic, Scully, … (явные боёвые).
3. **§C signatures / CD-kill** — Spike CD, Raven, Scope, Hitman, Pierre recruit, Smiley, Red, Meltdown (active fear AoE `VengefulTemperament`), …
4. **§B text+hooks** — Cougar Inspired, Flo, Static, Grace, Kulba, …
5. **HARD / satellite** — Rothman mine, Biff, Ira, Miguel, Livewire money, Barry craft, Thor NaturalHealing (joints + sat debt + bandage Will), Vince economy already in §A if cheap.
6. **§D** — Benni, Simon.

Каждый батч: CE/Code + loc + showcase RU/EN (+ wiki/technical при player-facing) + Evidence AC updates.

## Инварианты и ограничения

- Не ломать MATCH Ids без нужды.
- Пассивы без ложных HUD-кнопок `Jazz_Perk_00`.
- Deterministic: `InteractionRand` / existing attack rolls.
- HARD ops батчить; cut только с явной Evidence-пометкой владельца.
- REQ-008 id stability; exclusive `items.lua` handoff.

## Acceptance criteria

- `JAZZ-UNITS-006-AC-001` — static: §A DisplayName/Description = Mechanics; нет Wave A текста.
- `JAZZ-UNITS-006-AC-002` — static/Code: §A hooks = Mechanics (Henning AP, Steiger night@10, Nervous cap 10, Lucky reroll, Brutalize Blade, …).
- `JAZZ-UNITS-006-AC-003` — static: §B articles+CE синхронизированы в затронутых батчах (Flo/Static included).
- `JAZZ-UNITS-006-AC-004` — static/Code: §C Verdict≠MATCH; Grunty Morale proc; Spike CD kill; Flay per-enemy; Cougar Inspired.
- `JAZZ-UNITS-006-AC-005` — loc audit батча: needs RU=0, needs EN=0.
- `JAZZ-UNITS-006-AC-006` — showcase RU+EN (+ wiki/technical) покрывают deltas батча.
- `JAZZ-UNITS-006-AC-007` — runtime/human smoke per batch: ≥1 §A and/or ≥2 §C CHANGE (owner).
- `JAZZ-UNITS-006-AC-008` — §D: Benni/Simon have CE + StartingPerks + non-WIP Description when that batch ships.
- `JAZZ-UNITS-006-AC-009` — `JAZZ-UNITS-003` содержит supersede pointer на эту спеку для §A Ids.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: rewire personal CE; new statuses/buffs; signature CA changes.
- Saves: mid-campaign UI/behavior; StartingPerks id-stable.
- Network/determinism: InteractionRand only.
- Generated data: CE + items/metadata in `jazz` / `jazz-units`.
- Cross-package: do not revert `GruntyPerk_JAZZ` / `InnerInfo_JAZZ` ids.
- Rollback: revert CE/Code/loc/docs; restore UNITS-003 Mechanics for §A.

## План и ownership

- Пакет-владелец: `jazz` (+ `jazz-units` по необходимости)
- Исполнитель: agent по запросу батча
- Reviewer: project-owner
- Declared write set: frontmatter
- Exclusive resources: оба `items.lua`; loc `890000000006300-890000000006499`

## Решение владельца

- Статус: `approved`
- Кто подтвердил: project-owner chat 2026-08-08 («делай спеку полностью» + prior locked answers)
- Дата: 2026-08-08
- Зафиксировано: канон; §C in; Nervous cap 10; Lucky reroll; Grizzly G1; Steiger/Rothman/Henning as sheet; Grunty 10%×БД; Brutalize Blade; Flo/Static locked; Vince −25%; Madman −10 Will; Cougar/Flay/Spike sheet updates; §D Benni/Simon; батчи

## Evidence

- JAZZ-UNITS-006-AC-001 / AC-002 / AC-009: PASS (static) - batch1 §A + Mike PinDown +2 follow-up; **Nervous** rewired 2026-08-09 (Consume + AddHitStack, idempotent Apply).
- JAZZ-UNITS-006-AC-004 (partial): PASS (static) - batch2/3 §C + BuildingConfidence heal%-by-level; soft-cuts in notes/audit; **Meltdown** 2026-08-11: active fear AoE CombatAction (no RunAndGun).
- JAZZ-UNITS-006-AC-005 / AC-006 (batch1-4 deltas): PASS (static) - RU/EN + showcase RU|EN perks.md (incl. Meltdown row).
- JAZZ-UNITS-006-AC-003 (partial): PASS (static) - §B batch4 Flo/Static/Cougar + Grace/Kulba/Grom/...; soft-cuts _units006_batch4_notes.md.
- JAZZ-UNITS-006-AC-008: PASS partial (static) - §D CE + StartingPerks shipped; CombatAction actives soft-cut (batch6 notes).
- JAZZ-UNITS-006-AC-007: BLOCKED - owner runtime/human smoke.

## Documentation delta

- Этот файл = approved contract.
- При батче: showcase RU/EN, wiki, technical, `_named-perks-plan.md`, JA12 articles; `JAZZ-UNITS-003` supersede note (батч 1).
- Meltdown 2026-08-10: showcase `perks.md` RU|EN; `docs/tools/_units006_namedperks_notes.md`; wiki `combat-actions.md`.
- Tools snapshot: `docs/tools/_tmp_list2_perks_fresh.tsv`, `_tmp_list2_sheet_diff.md`, `_tmp_diff_list2_sheet.py` (agent tooling keep).

