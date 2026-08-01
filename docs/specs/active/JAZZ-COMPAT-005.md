---
id: JAZZ-COMPAT-005
status: implemented
owner: project-owner
systems:
  - strategy-squads-sectors
  - units-progression
  - package-architecture
repositories:
  - jazz-nomaps
  - jazz-units
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-COMPAT-005.md
  - jazz/docs/technical/compatibility.md
  - jazz/docs/technical/bugs/nomaps-playtest-2026-07-30.md
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/systems/maps-quests-content-catalog.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-units.md
  - jazz/docs/showcase/en/legion-units.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - jazz-nomaps/Code/NoMaps_Autonomy.lua
  - jazz-nomaps/metadata.lua
exclusive_resources:
  - ModDef:7MsJ2Eq
  - ModDef:Dv3mFVN
  - Code:NoMaps_Autonomy.lua
  - EnemySquads:LegionJAZZSquadT1_Early
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMPAT-005: NoMaps early Legion weight class (true T1)

## Проблема

Discord (2026-08-02): на профиле **JAZZ Vanilla Maps** игрок на **дне 1** в Жестянке (I6)
видит «совсем другую весовую категорию». Подозревали ускоренный gear tier; на дне 1
`JAZZ_Legion_Tier` по COMPAT-003 должен оставаться major I (`11`).

Фактический источник: NoMaps `SQUAD_REMAP` / prefix heuristic ведёт почти все vanilla
Legion/Thug squad ID в `LegionJAZZSquadT1`, а этот пресет (comment «лайтовый») содержит
**T2–T4** UnitData (Headsman, Sniper, Mortarman, Ranger…). Параллельно UnitData remap
поднимает `*_Stronger` / `*_Elite` / `*_Stronger_Elite` (последний → всегда T4) даже при
gear major I.

## Цели

- Добавить `LegionJAZZSquadT1_Early` — EnemySquad **только** из `JAZZ_Legion_*T1_*`.
- NoMaps default remap (и alias `LegionJAZZSquadT1_Early`) резолвит squad по gear major:
  I → Early, II → `LegionJAZZSquadT2`, III → `LegionJAZZSquadT3` (с fallback вниз).
- UnitData remap на gear major I всегда class T1; `Stronger_Elite`→T4 только с major III.
- Не ломать maps-профиль и существующий mixed `LegionJAZZSquadT1`.

## Non-goals

- Пересборка всех Ernie maps squads (`LegionRustIni`, `LegionErnieVillage`, …).
- Смена формулы `JAZZ_Legion_Tier` / COMPAT-003 timers.
- Морф уже заспавненных юнитов при росте тира.

## Требования

- `JAZZ-COMPAT-005-REQ-001` — `jazz-units`: preset `LegionJAZZSquadT1_Early`, все
  `unitType` содержат `T1_`; зарегистрирован в `metadata.lua`.
- `JAZZ-COMPAT-005-REQ-002` — NoMaps `SQUAD_REMAP` / prefix default → Early alias;
  `lRemapSquadId` расширяет alias по `lTierMajor(JAZZ_Legion_Tier)`.
- `JAZZ-COMPAT-005-REQ-003` — UnitData remap: major I → class_tier 1; major II cap 3;
  `Stronger_Elite` → 4 только при major ≥ 3.
- `JAZZ-COMPAT-005-REQ-004` — docs: technical + wiki + showcase RU/EN (player-facing).
- `JAZZ-COMPAT-005-REQ-005` — `LegionJAZZSquadT1` composition на maps не менять этим change.

## Инварианты и ограничения

- Public ID `LegionJAZZSquadT1` сохраняет прежнее (mixed) значение для maps.
- Deterministic InteractionRand; без лишнего NetSync.
- Named NPC skip (`_Jose` / Hyena) и WeakFlagHill/Tutorial → T1 без изменений.

## Acceptance criteria

- `JAZZ-COMPAT-005-AC-001` — static: Early squad unitTypes all `T1_`; metadata Id present.
- `JAZZ-COMPAT-005-AC-002` — static: NoMaps remap/alias + class-tier cap logic present.
- `JAZZ-COMPAT-005-AC-003` — runtime/human: NoMaps day-1 I6 — только T1 class Legion;
  gear tier остаётся 11 до шахты+3д.
- `JAZZ-COMPAT-005-AC-004` — generated sync jazz-units (+ nomaps metadata) errors=0.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: только NoMaps autonomy + units EnemySquad add.
- Saves: уже заспавненные mixed T2–T4 на Early секторах не откатываются; новые spawn —
  по новому правилу. GEAR_REV не поднимаем (состав squad, не inventory sanitize).
- Network/determinism: InteractionRand seed keys unchanged shape.
- Generated data: `jazz-units` items+metadata transaction.
- Cross-package: nomaps читает новый EnemySquad Id из units.
- Rollback: удалить Early + вернуть remap на `LegionJAZZSquadT1`.

## План и ownership

- Пакет-владелец: `jazz-nomaps` (runtime remap), `jazz-units` (EnemySquad), `jazz` (docs/spec).
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: см. frontmatter

## Решение владельца

- Статус: approved (ship)
- Кто подтвердил: project-owner («как разберешься запушь», Discord bug I6 day-1)
- Дата: 2026-08-02

## Evidence

- `JAZZ-COMPAT-005-AC-001`: `PASS` — static: `docs/tools/_verify_nomaps_early_squad.py`.
- `JAZZ-COMPAT-005-AC-002`: `PASS` — static: same verifier + `NoMaps_Autonomy.lua` review.
- `JAZZ-COMPAT-005-AC-003`: `BLOCKED` — runtime/human (day-1 I6 smoke).
- `JAZZ-COMPAT-005-AC-004`: `PASS` — `_validate_items_quick.py` on jazz-units; Early Id in metadata.

## Documentation delta

- `docs/technical/compatibility.md`, `strategy-squads-sectors.md`, `maps-quests-content-catalog.md`,
  `bugs/nomaps-playtest-2026-07-30.md` (B14).
- `docs/wiki/legion-global-ai.md` + showcase RU/EN legion-units / legion-strategy.
