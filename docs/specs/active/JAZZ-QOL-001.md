---
id: JAZZ-QOL-001
status: implemented
owner: project-owner
systems:
  - tactical-ai
  - combat-camera
repositories:
  - jazz
risk: low
generated_data: true
runtime_validation: required
write_set:
  - Code/AiFastForward.lua
  - Code/AiActions.lua
  - items.lua
  - metadata.lua
  - docs/specs/active/JAZZ-QOL-001.md
  - docs/technical/systems/ai-awareness.md
exclusive_resources:
  - items.lua
  - metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-QOL-001: авто-ускорение скрытых врагов и свободная камера на чужом ходе

## Проблема

Авто-ускорение (`AutoFastForward`) вшито грязно в `AIExecuteUnitBehavior`:

- дублируется дважды (до behavior / до атак) с копипастой;
- видимость считается через обход `CanSee` по `player1`, а не через `HasVisibilityTo(GetPoVTeam(), unit)` как в vanilla AI camera;
- глобальный `IsUnitHiddenFromPlayer` засоряет namespace;
- скорость перезаписывается даже если значение не менялось.

На ходе ИИ vanilla блокирует pan/zoom через `LockCameraMovement` (`AIExecutionController` / `CombatCamera`). Игрок не может свободно крутить камеру.

## Цели

- Чистый QoL-модуль авто-ускорения с тем же смыслом опции `Off` / `Running` / `Always`.
- Свободная камера (pan/zoom) на ходе врага/союзника (не player control), без отключения action/cinematic snaps по умолчанию.
- Visibility через PoV team API.

## Non-goals

- Не менять AI Commit/Dump/Disengage (`JAZZ-AI-002`).
- Не отключать action camera / cinematic combat camera целиком.
- Не трогать co-op sync сверх того, что уже делает `UpdateFastForwardGameSpeed`.

## Требования

- `JAZZ-QOL-001-REQ-001` — `AutoFastForward=Off`: JAZZ не меняет `g_FastForwardGameSpeed`.
- `JAZZ-QOL-001-REQ-002` — `Running`: перед `behavior:Play` выставить Fast, если PoV team не видит юнита (`HasVisibilityTo`), иначе Normal; перед атаками не переключать повторно.
- `JAZZ-QOL-001-REQ-003` — `Always` (default): то же перед behavior и повторная проверка перед `AIPlayAttacks`.
- `JAZZ-QOL-001-REQ-004` — смена скорости только если новое значение ≠ текущему; вызов `UpdateFastForwardGameSpeed()`.
- `JAZZ-QOL-001-REQ-005` — опция `EnemyTurnFreeCamera` (bool, default on): пока активен AI execution / `g_Combat` без `is_player_control`, `LockCameraMovement` не блокирует pan/zoom; при Activate снимаются уже поставленные movement-locks.
- `JAZZ-QOL-001-REQ-006` — логика вынесена в `Code/AiFastForward.lua`; из `AiActions.lua` убраны dirty helper и копипаста.
- `JAZZ-QOL-001-REQ-007` — `const.Combat.FastForwardGameSpeed` = 300% (было 200% = vanilla), чтобы auto/manual FF давали заметное ускорение.

## Инварианты и ограничения

- Семантика `Off`/`Running`/`Always` сохраняется.
- Не ломать `JAZZ-AI-002` FastForward hook (сохранить вызовы, только почистить).
- Save schema без изменений.
- Generated data: одна транзакция `items.lua` + `metadata.lua` + companion `Code/AiFastForward.lua`.

## Acceptance criteria

- `JAZZ-QOL-001-AC-001` — static: нет `IsUnitHiddenFromPlayer`; нет дубля FF-блоков в `AIExecuteUnitBehavior`; есть вызовы модуля.
- `JAZZ-QOL-001-AC-002` — static: visibility через `HasVisibilityTo(GetPoVTeam(), unit)`.
- `JAZZ-QOL-001-AC-003` — static: `EnemyTurnFreeCamera` в options + override `LockCameraMovement` / activate unlock.
- `JAZZ-QOL-001-AC-004` — sync-audit: items/metadata/companion согласованы для нового code + option.
- `JAZZ-QOL-001-AC-005` — human/runtime: скрытый враг ускоряется по режиму; видимый — Normal; на чужом ходе камера крутится руками. `BLOCKED` до прогона.

## Impact и совместимость

- Vanilla/CLib/JAZZ: last-writer override `LockCameraMovement` + хук в уже заменённом `AIExecuteUnitBehavior`.
- Saves: нет.
- Network: `UpdateFastForwardGameSpeed` уже hashed; free camera — клиентский input, без sync state.
- Generated data: да (option + ModItemCode).
- Cross-package: нет.
- Rollback: revert write set.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: items.lua, metadata.lua

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner («апрув если оно быстрее станет в итоге»)
- Дата: 2026-07-28
- Условие: скрытые враги реально идут на Fast (const FastForwardGameSpeed); видимые — Normal.

## Evidence

- `JAZZ-QOL-001-AC-001`: `PASS` — static: `IsUnitHiddenFromPlayer` удалён; `AIExecuteUnitBehavior` вызывает `JAZZ_UpdateAutoFastForward`.
- `JAZZ-QOL-001-AC-002`: `PASS` — static: visibility через `HasVisibilityTo(GetPoVTeam(), unit)` в `Code/AiFastForward.lua`.
- `JAZZ-QOL-001-AC-003`: `PASS` — static: опция `EnemyTurnFreeCamera`; wrap `LockCameraMovement`; unlock на `ExecutionControllerActivate`.
- `JAZZ-QOL-001-AC-004`: `PASS` — sync: `Code/AiFastForward.lua` в items+metadata.code; options в default_options; pre-existing orphan warnings only.
- `JAZZ-QOL-001-AC-005`: `BLOCKED` — human/runtime: прогон боя (скрытый ×3, камера на чужом ходе).

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — модуль `AiFastForward`, PoV visibility, free camera на чужом ходе, опции.
