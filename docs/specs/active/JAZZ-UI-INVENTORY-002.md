---
id: JAZZ-UI-INVENTORY-002
status: approved
owner: project-owner
systems:
  - ui
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - docs/tools/_check_inventory_portrait_container.py
  - items.lua
  - docs/specs/active/JAZZ-UI-INVENTORY-002.md
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-UI-INVENTORY-002: восстановить список портретов инвентаря

## Проблема

После интеграции upstream удалены три внутренних idContainer в SquadsAndMercs. Внешняя обёртка сохранила этот ID: её дети — окна компоновки, а не портреты. Inventory.OnContextUpdate вызывает SetSelected на обёртке; HighlightWeaponsForAmmo вызывает SetHighlighted. Оба отсутствуют, что подтверждено скриншотами пользователя. Recursive mouse target update может быть вторичным следствием.

## Цели

Восстановить прямой доступ потребителей idParty.idContainer к кнопкам наёмников.

## Non-goals

Не откатывать исправления пустых патронов/chips, K4, медицины или прочие изменения UI.

## Требования

- `JAZZ-UI-INVENTORY-002-REQ-001` — внутренний список портретов в каждой из трёх взаимоисключающих ветвей SquadsAndMercs имеет Id=idContainer, как до upstream.
- `JAZZ-UI-INVENTORY-002-REQ-002` — внешний контейнер получает отдельный Id=idPartyLayout, чтобы не перекрывать список портретов.

## Инварианты и ограничения

Состав, порядок и обработчики портретов не меняются. Нельзя маскировать неверный список проверкой наличия SetSelected: это оставит выбор и подсветку сломанными.

## Acceptance criteria

- `JAZZ-UI-INVENTORY-002-AC-001` — offline проверка дерева: три внутренних списка, один внешний layout, прежние кнопки и обработчики; воспроизведение ошибочной структуры и успешный вызов выбора/подсветки после исправления.
- `JAZZ-UI-INVENTORY-002-AC-002` — владелец открывает инвентарь/схрон, переключает наёмника и наводит/убирает мышь с патронов без assert; отдельно проверяет портреты на тактической и стратегической карте.

## Impact и совместимость

Пакет jazz, ModItemXTemplate SquadsAndMercs в items.lua. Отдельного companion нет; metadata/load order не меняются. Сейвы и сеть не меняются. Rollback — вернуть одну внешнюю запись ID и удалить три внутренних.

## План и ownership

Исполнитель — текущий агент. items.lua эксклюзивен на время применения. До закрытия игры готовится только отдельный патч; затем scoped замена и проверка структуры. Живую игру тестирует владелец.

## Решение владельца

approved: project-owner, 2026-09-16. Продолжение исправления подтверждённого регресса после разрешённого объединения; наши багфиксы приоритетны.

## Evidence

- `JAZZ-UI-INVENTORY-002-AC-001`: BLOCKED — подготовка патча и проверки.
- `JAZZ-UI-INVENTORY-002-AC-002`: BLOCKED — ручной тест после применения.

## Documentation delta

Исправление восстанавливает существующий контракт UI; новая игровая механика отсутствует. Причина и проверка фиксируются здесь.

2026-09-16: исправление применено при закрытой игре. AC-001 PASS (offline Lua; структура items/metadata PASS). AC-002 ожидает ручной проверки владельца; editor round-trip не выполнялся, готовность релиза не заявляется.
