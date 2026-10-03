---
id: JAZZ-INV-006
status: implemented
owner: project-owner
systems:
  - inventory-items-loot-crafting
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: not-required
write_set:
  - Code/System_OR_SquadBag.lua
  - Code/InventoryUI.lua
  - docs/specs/active/JAZZ-INV-006.md
  - docs/tools/test_squad_bag_performance.py
  - docs/tools/README.md
  - .agents/docs/playbooks/assets-and-ui.md
  - docs/technical/systems/inventory-items-loot-crafting.md
  - docs/wiki/weapons-and-ammo.md
  - docs/showcase/ru/weapons-and-ammo.md
  - docs/showcase/en/weapons-and-ammo.md
exclusive_resources:
  - none
related_decisions:
  - JAZZ-INV-001
approved_by: project-owner, chat 2026-10-03
---

# JAZZ-INV-006: устранить повторную работу большой сумки

## Проблема

Владелец наблюдает задержки при десятках/сотнях отдельных предметов в SquadBag. Getter безусловно очищает и заново раскладывает сумку; merge сравнивает каждый предмет со всеми ранее сохранёнными; UI не видит локальный handle сортировки и может ставить несколько пересборок в очередь.

## Цели

- Сократить повторную работу при неизменной сумке и поиске совместимых стеков.
- Согласовать существующий engine handle сортировки с UI и объединять ожидающие UI refresh.

## Non-goals

- Переписывание XTemplates, виртуализация карточек, слоистые иконки, изменение правил стакинга, публикация.
- Запуск игры, обещание измеренного FPS или исправления известного visual-disappear бага.
- Замена штатной первичной раскладки Inventory.AddItem.

## Требования

- `JAZZ-INV-006-REQ-001` — повторный getter использует transient cache только при совпадении squad, mode, source array/order, размеров предметов и runtime slot/order/positions. Clear, изменения источника/раскладки и reload инвалидируют cache; stack context обновляется.
- `JAZZ-INV-006-REQ-002` — merge индексирует кандидатов по class и removable component identity, исключает полные стеки; сохраняет существующие amounts, object identity, удаление пустых объектов и comparator.
- `JAZZ-INV-006-REQ-003` — sorter использует существующий глобальный g_squad_bag_sort_thread; UI ставит не больше одного ожидающего respawn и сохраняет retry при активной сортировке.

## Инварианты и ограничения

- Storage max, персональные лимиты, порядок категорий, drag/drop и совместимость разных RemovableComponentId не меняются.
- Никакого Sleep внутри мутации стеков. Cache — local weak table, не save data.
- Чужие незакоммиченные правки сохраняются; metadata/items/localization не меняются.

## Acceptance criteria

- `JAZZ-INV-006-AC-001` — offline Lua: повторный getter не вызывает повторных AddItem; mutation/reorder/resize/mode/squad/Clear/runtime slot mutation дают rebuild.
- `JAZZ-INV-006-AC-002` — offline Lua: differential merge против прежнего алгоритма на mixed/overflow/removable fixtures и больших сумках сохраняет предметы и количества; счётчик сравнений демонстрирует отсутствие полного попарного перебора разных классов.
- `JAZZ-INV-006-AC-003` — offline Lua: сортировочный handle доступен UI; серия refresh даёт одну отложенную работу, retry и следующий refresh не теряются.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: штатная раскладка сохраняется, overrides изменяются на месте без дополнительных wraps.
- Saves: формат без изменений; transient cache отсутствует в объектах.
- Network/determinism: merger не yield, сортировочный comparator и порядок обхода источника сохраняются.
- Generated data: нет.
- Cross-package references: нет.
- Rollback/recovery: откат только diff этой spec; существующий Clear принудительно перестраивает сумку.

## План и ownership

- Пакет-владелец: jazz.
- Исполнитель: Codex в текущем чате; самостоятельная проверка, независимый reviewer не назначен.
- Declared write set: перечислен в frontmatter.
- Exclusive resources: none.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner, «давай правь пока без игры».
- Дата: 2026-10-03.
- Приёмка этого этапа ограничена offline/static; живые задержки, drag/drop и визуальная стабильность требуют последующей проверки в игре.

## Evidence

- `JAZZ-INV-006-AC-001`: PASS — offline Lua, `python docs/tools/test_squad_bag_performance.py`: повторные getter сумки с 1000 стаками не вызывают новых AddItem; mutation/reorder/resize/mode/squad/Clear/runtime slot mutation и reload инвалидируют cache; amount-only сохраняет раскладку и обновляет storage cap.
- `JAZZ-INV-006-AC-002`: PASS — offline Lua: 300 случайных сумок по 1–500 объектов, пустая сумка, removable fallback, overflow и полные стеки; совпали survivor identity/order, amounts, caps, source mutation и deletion. 1000 разных классов: 499500 → 0 вызовов compatibility predicate; 1000 полных стеков одного класса: 0 вызовов.
- `JAZZ-INV-006-AC-003`: PASS — offline Lua: общий handle, отмена предыдущего handle и сохранение при reload; 100 запросов → один callback; запросы во время ожидания сортировки объединяются; retry/следующее обновление работают. На fake dialog проверены однократные respawn панелей, восстановление scroll и cancel/restart drag. Полные Lua-файлы проходят syntax load; engine rendering/drag-drop этим не подтверждены.

Локальная проверка документации (четыре изменённые страницы) и `git diff --check` кодового scope прошли. Независимое ревью и human acceptance не выполнялись; статус остаётся implemented. Публикации и запуск игры не выполнялись.

## Documentation delta

- Канон: docs/technical/systems/inventory-items-loot-crafting.md; краткая оговорка об offline этапе в wiki/showcase weapons-and-ammo RU/EN. Asset contract не меняется.
