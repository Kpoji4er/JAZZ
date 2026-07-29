---
id: JAZZ-AI-001
status: implemented
owner: project-owner
systems:
  - tactical-ai
repositories:
  - jazz
  - jazz-units
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - metadata.lua
  - Code/AiActions.lua
  - Code/*CustomSeekCover.lua
  - Code/*TryNotToBeFlanked.lua
  - Code/*MGSetupPosScore.lua
  - Code/*MGSetupAP.lua
  - Code/*GrenadeRange.lua
  - ../jazz-units/items.lua
  - docs/specs/active/JAZZ-AI-001.md
  - docs/specs/active/JAZZ-CTH-001.md
  - docs/technical/code-reference.md
  - docs/technical/systems/ai-awareness.md
  - docs/technical/systems/explosives-traps-heavy-weapons.md
  - docs/technical/systems/file-coverage.md
  - docs/technical/systems/runtime-editor-integration.md
exclusive_resources:
  - jazz/metadata.lua
  - jazz-units/items.lua
related_decisions:
  - none
approved_by: SsAnd
---

# JAZZ-AI-001: удаление заимствованного AI policy-слоя

## Проблема

В core загружаются пять заимствованных AI policy-модулей, не принадлежащих дизайну JAZZ. Четыре policy-класса не используются текущими generated archetypes, а один класс дважды встроен в `GuardArea`. Current-state документация ошибочно представляет этот слой как часть настройки мода.

## Цели

- Полностью удалить пять сторонних policy-модулей из runtime graph и файловой системы.
- Перевести две policy-позиции `GuardArea` на существующий `AIPolicyTakeCover` JAZZ.
- Удалить текущие документальные упоминания старого слоя.

## Non-goals

- Переписывать остальные `AIPolicy.lua`, `AiActions.lua`, `CombatAI.lua` или awareness.
- Менять public ID `GuardArea`, его custom behavior, fallback или tactical area integration.
- Исправлять остальные AI-риски, перечисленные в current-state документации.
- Выполнять массовую регенерацию `jazz-units/items.lua`.

## Требования

- `JAZZ-AI-001-REQ-001` — пять сторонних policy-файлов удалены, а их пять записей исключены из `jazz/metadata.lua.code`.
- `JAZZ-AI-001-REQ-002` — обе policy-позиции `GuardArea` используют `AIPolicyTakeCover` с `visibility_mode = "team"`.
- `JAZZ-AI-001-REQ-003` — остальные свойства и inline-функции generated preset `GuardArea` не меняются.
- `JAZZ-AI-001-REQ-004` — current-state документация описывает только оставшийся vanilla/JAZZ AI-слой.

## Инварианты и ограничения

- `GuardArea` сохраняет public ID, `CustomAI`, `FallbackAction = "overwatch"` и assigned-area callbacks.
- Порядок оставшихся AI-файлов в `metadata.lua.code` сохраняется.
- Изменение не добавляет RNG, persistent state, network events или dependencies.
- Сторонние dirty-изменения в обоих репозиториях сохраняются.
- Asset contract не меняется.

## Acceptance criteria

- `JAZZ-AI-001-AC-001` — удаляемые файлы отсутствуют, а runtime metadata не содержит их путей.
- `JAZZ-AI-001-AC-002` — generated `GuardArea` содержит ровно две `AIPolicyTakeCover` с team visibility и не ссылается на удалённый policy-класс.
- `JAZZ-AI-001-AC-003` — narrow cross-package search вне `jazz-maps/Maps/` не находит прежний filename prefix или удалённые class/helper IDs.
- `JAZZ-AI-001-AC-004` — generated-data аудит не обнаруживает новых blocking errors; documentation contract проходит.
- `JAZZ-AI-001-AC-005` — после cold load `GuardArea` выбирает позицию в назначенной области без Lua error и сохраняет возможность искать укрытие.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: удаляются только отдельные новые глобальные классы/helpers; пересечения vanilla/CommonLib не меняются.
- Saves: public archetype ID сохраняется; существующая сериализованная policy-таблица в спящем thread теоретически может продолжить старый байткод до завершения.
- Network/determinism: новый RNG и network state не добавляются.
- Generated data: ручная узкая транзакция только двух вложенных policy-объектов в `jazz-units/items.lua`; companion для `ModItemAIArchetype` отсутствует.
- Cross-package references: core перестаёт предоставлять удалённый класс; units перестаёт его потреблять.
- Rollback/recovery: вернуть пять файлов и metadata entries, затем восстановить две прежние policy-записи `GuardArea`.

## План и ownership

- Пакет-владелец runtime: `jazz`.
- Пакет-владелец archetype: `jazz-units`.
- Исполнитель: Codex.
- Reviewer: project-owner.
- Declared write set: front matter этой spec.
- Exclusive resources: `jazz/metadata.lua`, `jazz-units/items.lua`.

## Решение владельца

- Статус: approved.
- Кто подтвердил: SsAnd — «вообще желательно убрать и их и упоминания».
- Дата: 2026-07-26.

## Evidence

- `JAZZ-AI-001-AC-001`: `PASS` — static: пять файлов отсутствуют, пять metadata entries удалены, оставшийся AI load order непрерывен.
- `JAZZ-AI-001-AC-002`: `PASS` — static: slice `GuardArea` содержит две `AIPolicyTakeCover`, две `visibility_mode = "team"` и ноль ссылок на удалённый класс.
- `JAZZ-AI-001-AC-003`: `PASS` — static: narrow search по core, units, assets и maps root/code вернул `legacy_hits=0`; `jazz-maps/Maps/` не обходился.
- `JAZZ-AI-001-AC-004`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-AI-001-AC-005`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`

Связанные commits: `jazz-units` — `575e541`; `jazz` — текущий commit этой spec.

## Documentation delta

- Обновлены `ai-awareness.md`, `file-coverage.md`, `code-reference.md`, `explosives-traps-heavy-weapons.md` и `runtime-editor-integration.md`; asset contract не изменён.
