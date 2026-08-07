---
id: JAZZ-WEAPONS-011
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/Code/System_OR_Weapons.lua
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz/docs/specs/active/JAZZ-WEAPONS-011.md
exclusive_resources:
  - none
related_decisions:
  - none
related_specs:
  - JAZZ-WEAPONS-001
  - JAZZ-WEAPONS-002
  - JAZZ-WEAPONS-006
  - JAZZ-WEAPONS-010
approved_by: project-owner
---

# JAZZ-WEAPONS-011: клин в середине очереди (per-shot roll)

## Проблема

`ReliabilityCheck` делает **один** бросок на всю атаку. При проке
`PrecalcAmmoUse` ставит `fired = false`, а `GetAttackResults` выходит по
`jammed` до симуляции пуль — очередь обрывается **до первого выстрела**.
Владелец хочет: шанс клина применяется **на каждый выстрел** (умножение
риска длиной очереди), а при проке уже выпущенные пули остаются в силе.

## Цели

- per-shot jam roll на JamScore атаки (после Mechanical / single-shot `/2`);
- при клине на попытке выстрела `i` выстрелы `1..i-1` считаются и наносят
  урон; оружие jam'ится; хвост очереди отменяется;
- UI `%` остаётся **за один выстрел** (как сейчас), не «шанс клина всей
  очереди».

## Non-goals

- смена формулы JamScore / WEAPONS-010 ступеней / cap 10%;
- per-pellet jam у дроби (пакет WEAPONS-006): проверка по **гильзам**
  `consumed_ammo`, не по `BuckshotProjectiles`;
- смена ordinary/crit max-loss (WEAPONS-002) и Unjam;
- prediction UI, показывающий «где клинит» в очереди.

## Требования

- `JAZZ-WEAPONS-011-REQ-001` — `ReliabilityCheck(attacker, num_shots)` для
  каждого `i = 1..num_shots` (при `num_safe_attacks <= 0`) бросает
  `attacker:Random(1000)` против **одного и того же** `jam_chance`
  (после Mechanical; при `num_shots == 1` по-прежнему `DivRound(..., 2)`).
  Первый прок на `i` → `jammed = true`, `fired_count = i - 1`; дальнейшие
  броски не делаются. Если проков нет — `fired_count = num_shots`.
- `JAZZ-WEAPONS-011-REQ-002` — `PrecalcAmmoUse`: при jam с
  `fired_count > 0` возвращает `fired = fired_count` (число), `jammed =
  true`; при jam на первом выстреле — `fired = false` (как сейчас).
  Нехватка патронов по-прежнему режет `fired` до `ammo.Amount`.
- `JAZZ-WEAPONS-011-REQ-003` — `GetAttackResults`: ранний выход только при
  `not fired` (или chance_only), **не** при `jammed` с частичным `fired`.
  `num_shots` / pellet overwrite для Shotgun остаются как сейчас; для
  DoubleBarrel частичный `fired` по гильзам ограничивает пакет
  пропорционально (1 гильза → один пакет дробин).
- `JAZZ-WEAPONS-011-REQ-004` — `Firearm:ApplyAmmoUse`: при `jammed` и
  numeric `fired > 0` сначала списывает патроны `fired`, затем `Jam`;
  vanilla `elseif` (jam без расхода) сохраняется только для
  `fired = false`.
- `JAZZ-WEAPONS-011-REQ-005` — износ `WeaponResource` в
  `ReliabilityCheck` только за фактически выпущенные выстрелы
  (`fired_count * DegradePerShot`), не за отменённый хвост.
- `JAZZ-WEAPONS-011-REQ-006` — deterministic: число RNG-вызовов jam =
  число проверенных выстрелов до первого клина включительно (1..N).

## Инварианты и ограничения

- JamScore 0..1000, display `/10`, Mechanical `/120`/`/150`, single `/2`
  без изменений шкалы;
- integer math; без новых public IDs / save schema;
- дробовый pellet_pack не получает per-pellet jam.

## Acceptance criteria

- `JAZZ-WEAPONS-011-AC-001` — static: `ReliabilityCheck` / `PrecalcAmmoUse`
  / early-exit / `ApplyAmmoUse` соответствуют REQ-001..005.
- `JAZZ-WEAPONS-011-AC-002` — static: shotgun Buckshot path всё ещё jam'ит
  по shells, не по числу дробин.
- `JAZZ-WEAPONS-011-AC-003` — runtime/human: Burst/Auto с клином в середине
  показывает несколько выстрелов, затем Jam; не «Jammed» с нулём пуль.
- `JAZZ-WEAPONS-011-AC-004` — runtime/human: одиночный выстрел с клином
  по-прежнему без выстрела (`fired = false`).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: override `ReliabilityCheck`, `PrecalcAmmoUse`,
  early-exit в `GetAttackResults`, новый `ApplyAmmoUse`.
- Saves: нет миграции; меняется только будущий combat.
- Network/determinism: больше jam-RNG на длинных очередях (до N бросков).
- Generated data: нет.
- Rollback: revert write set.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: frontmatter.
- Exclusive resources: none.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner («апрув, делай»).
- Дата: 2026-08-07.
- Баланс: per-shot полный JamScore (риск ≈ умножается длиной очереди);
  UI % = за пулю.

## Evidence

- `JAZZ-WEAPONS-011-AC-001`..`004`: `BLOCKED` — awaiting approval.

## Documentation delta

- technical weapons-ammo-components — per-shot jam + partial burst.
- wiki + showcase RU/EN — очередь может оборваться клином после части пуль.
