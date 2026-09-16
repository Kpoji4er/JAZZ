---
id: JAZZ-UI-CONDITION-001
status: approved
owner: project-owner
systems:
  - inventory-ui
repositories:
  - jazz
risk: low
generated_data: true
runtime_validation: required
write_set:
  - items.lua
  - docs/specs/active/JAZZ-UI-CONDITION-001.md
  - docs/tools/_check_hud_condition_context.py
  - docs/tools/README.md
  - docs/technical/systems/ui-audio-fx.md
  - docs/wiki/weapons-and-ammo.md
  - docs/showcase/ru/weapons-and-ammo.md
  - docs/showcase/en/weapons-and-ammo.md
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-UI-CONDITION-001: одинаковое состояние оружия в HUD и инвентаре

## Проблема

Игрок сообщил о разных процентах у Монка с Gewehr 98. `UIWeaponDisplay.idCondText` читает `Condition`, тогда как инвентарь использует `GetConditionPercent()` на основе текущего и максимального ресурса.

## Цели

- Отображать один расчётный процент состояния в обоих местах.

## Non-goals

- Баланс износа, ремонт, изменение данных оружия, новая локализация.

## Требования

- `JAZZ-UI-CONDITION-001-REQ-001` — контекст idCondText получает Condition из GetConditionPercent(), не меняя исходный предмет.

## Инварианты и ограничения

- Сохранить локализацию, стиль, расположение и условие Repairable. Исходный Condition и WeaponResource остаются неизменными.

## Acceptance criteria

- `JAZZ-UI-CONDITION-001-AC-001` — Lua-harness: при Condition=100 и GetConditionPercent()=43 текстовый контекст содержит 43, исходный предмет сохраняет 100; крайние значения 0/100 также совпадают.
- `JAZZ-UI-CONDITION-001-AC-002` — UI в игре показывает одинаковое состояние в HUD/инвентаре после выстрела и ремонта; editor round-trip сохраняет callback.

## Impact и совместимость

- Vanilla/JAZZ: штатный XTemplate idCondText сохраняет формат, получает локальный SubContext.
- Saves: миграция не нужна; состояние не записывается. Network/determinism: только UI.
- Generated data: ModItemXTemplate в items.lua, отдельного companion нет; metadata/load order не меняются.
- Cross-package: нет. Rollback: удалить __context только у idCondText.

## План и ownership

- Владелец: jazz. Declared write set и exclusive resources указаны выше.
- Исполнитель: текущая задача. Reviewer: итоговый просмотр diff, игровая приёмка отдельно.

## Решение владельца

- approved: project-owner, 2026-09-15, «начинай» после согласованного плана автономного исправления подтверждённых багов. Восстановление согласованности UI без смены игрового поведения.

## Evidence

- `JAZZ-UI-CONDITION-001-AC-001`: `PASS` — `_check_hud_condition_context.py`: Lua-harness 0/43/100, исходный Condition=87 и WeaponResource=430 не изменены. `_validate_items_quick.py` PASS.
- `JAZZ-UI-CONDITION-001-AC-002`: `BLOCKED` — JA3Debug не запускается; editor/runtime недоступны.

## Documentation delta

- UI system page и player weapon pages: единый процент состояния, без изменения баланса.
