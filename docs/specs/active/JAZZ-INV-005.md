---
id: JAZZ-INV-005
status: approved
owner: project-owner
systems:
  - inventory-items-loot-crafting
  - armor-damage-wounds-will
repositories:
  - jazz
risk: low
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-INV-005.md
  - jazz/Code/System_JazzStackableMedicine.lua
  - jazz/docs/technical/systems/inventory-items-loot-crafting.md
  - jazz/docs/technical/systems/armor-damage-wounds-will.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz/docs/tools/_check_inv005_meds_salvage.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - none
related_decisions:
  - none
related_specs:
  - JAZZ-INV-004
  - JAZZ-MED-001
approved_by: project-owner
---

# JAZZ-INV-005: разбор бинтов и морфина на Meds (по штуке)

## Проблема

Бинты и морфин забивают инвентарь секторов ещё до midgame; аптечки редкие и тратятся. Продажи лута нет. Игрок просит утилизацию на деньги или медикаменты. Владелец в Discord: продажу лута позже; пока разбор на медикаменты по единичке.

## Цели

- Правый клик / Salvage одного `JAZZ_Bandage` или `JAZZ_Morphine` даёт `Meds` в сумку отряда (не Parts).
- Стек разбирается **по 1 штуке** за действие (не весь стек сразу).
- Аптечки (Small/Medium/Large) в эту волну не входят.

## Non-goals

- Продажа лута за деньги.
- Разбор аптечек / SurgicalKit / CombatStim.
- Оптимизация загрузки сектора от большого числа предметов (отдельный perf-scope).
- Массовый «разобрать всё».

## Требования

- `JAZZ-INV-005-REQ-001` — `JAZZ_Bandage`: salvage **1** → `Meds` × **1**.
- `JAZZ-INV-005-REQ-002` — `JAZZ_Morphine`: salvage **1** → `Meds` × **1**.
- `JAZZ-INV-005-REQ-003` — UI salvage этих предметов не даёт Parts; выход только Meds в squad bag.
- `JAZZ-INV-005-REQ-004` — стек: одно действие снимает **1** `Amount`, остаток стека остаётся.
- `JAZZ-INV-005-REQ-005` — FirstAidKit / Medkit / Reanimationsset / SurgicalKit без нового scrap-выхода.
- `JAZZ-INV-005-REQ-006` — тот же ванильный verb Salvage / Разбор, что у аптечек (отдельная строка не нужна).
- `JAZZ-INV-005-REQ-007` — wiki + showcase RU/EN описывают разбор бинтов/морфина.

## Инварианты и ограничения

- Не менять `ScrapItem` для оружия/брони.
- Bobby: новых предметов нет.
- Детерминизм: без RNG.

## Acceptance criteria

- `JAZZ-INV-005-AC-001` — runtime: salvage 1 бинта → +1 Meds, бинтов −1.
- `JAZZ-INV-005-AC-002` — runtime: salvage 1 морфина → +1 Meds, морфина −1.
- `JAZZ-INV-005-AC-003` — static: аптечки не в yield-таблице field stacks; `_check_inv005_meds_salvage.py` OK.
- `JAZZ-INV-005-AC-004` — docs: technical inventory + wiki + showcase RU/EN.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: wrap `AmountOfSalvagedMeds` / `SalvageItem` + UI condition на `InventoryContextMenu` для field stacks. Ванильный kit salvage без изменений.
- Saves: без новой схемы; старые стеки разбираются тем же действием.
- Network/determinism: нет броска; тот же `NetSquadBagAction(..., "salvage")`.
- Generated data: нет (yield в Lua-таблице, не `ScrapParts` / `max_meds_parts`).
- Rollback: снять wrap и UI patch.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (чат: 1 Meds с бинта, 1 с морфия)
- Дата: 2026-09-01

## Evidence

- `JAZZ-INV-005-AC-001`: `BLOCKED` — runtime (игра без DAP на момент сдачи)
- `JAZZ-INV-005-AC-002`: `BLOCKED` — runtime
- `JAZZ-INV-005-AC-003`: `PASS` — static: `_check_inv005_meds_salvage.py` OK (yield 1/1, kits excluded, wrap+UI patch present)
- `JAZZ-INV-005-AC-004`: `PASS` — docs: inventory + armor + wiki combat/weapons + showcase RU/EN combat/weapons

## Documentation delta

- `docs/technical/systems/inventory-items-loot-crafting.md`
- `docs/technical/systems/armor-damage-wounds-will.md`
- `docs/technical/systems/file-coverage.md`
- `docs/technical/override-matrix.md`
- `docs/wiki/combat-and-accuracy.md`, `docs/wiki/weapons-and-ammo.md`
- `docs/showcase/ru|en/combat-and-accuracy.md`, `docs/showcase/ru|en/weapons-and-ammo.md`
