---
id: JAZZ-MED-010
status: approved
owner: project-owner
systems:
  - armor-damage-wounds-will
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - items.lua
  - CharacterEffect/Trauma*.lua
  - docs/tools/_check_trauma_ap_event.py
  - docs/specs/active/JAZZ-MED-010.md
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-MED-010: AP-событие травм только для тактического Unit

## Проблема

При JazzPushTraumaToTwin стратегический UnitData получает TraumaRibsLight. OnAdded отправляет UnitAPChanged, обработчик overwatch вызывает отсутствующий UpdateNumOverwatchAttacks. Подтверждено стеком владельца.

## Цели

Сохранить перенос травм в обе копии персонажа без тактических событий для UnitData.

## Non-goals

Не менять урон, эффекты травм, AP, лечение или vanilla обработчик.

## Требования

- `JAZZ-MED-010-REQ-001` — OnAdded/OnRemoved всех Trauma-эффектов отправляют UnitAPChanged только для IsKindOf(obj, "Unit"). UnitData сохраняет эффект без этого события.

## Инварианты и ограничения

items и companion правятся синхронно. Настоящий Unit продолжает получать ровно одно событие.

## Acceptance criteria

- `JAZZ-MED-010-AC-001` — Lua проверка всех затронутых OnAdded/OnRemoved: Unit получает событие, UnitData нет; items/companion согласованы.
- `JAZZ-MED-010-AC-002` — ручной тест травмы в бою и синхронизации после перехода на стратегическую карту без assert.

## Impact и совместимость

Только jazz, существующие CharacterEffect; metadata не меняется, миграция сейва не нужна. Vanilla/CommonLib обработчики не оборачиваются. Rollback: удалить условия у Msg в обеих формах.

## План и ownership

Текущий агент, эксклюзивный items.lua; исправить 6 эффектов и проверить оба callback каждого.

## Решение владельца

approved: project-owner, 2026-09-16: «поправь все — потом я запущу игру и проверю».

## Evidence

- `JAZZ-MED-010-AC-001`: BLOCKED — до проверки.
- `JAZZ-MED-010-AC-002`: BLOCKED — ручная проверка владельцем.

## Documentation delta

Восстановление контракта событий, без изменения игровой механики; причина и проверки здесь.

2026-09-16: исправление применено при закрытой игре. AC-001 PASS (offline Lua; структура items/metadata PASS). AC-002 ожидает ручной проверки владельца; editor round-trip не выполнялся, готовность релиза не заявляется.
