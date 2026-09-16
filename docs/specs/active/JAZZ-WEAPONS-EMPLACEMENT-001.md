---
id: JAZZ-WEAPONS-EMPLACEMENT-001
status: approved
owner: project-owner
systems:
  - weapons
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - Code/System_EmplacementAmmo.lua
  - docs/tools/_check_emplacement_target_distance.py
  - docs/tools/README.md
  - docs/specs/active/JAZZ-WEAPONS-EMPLACEMENT-001.md
  - docs/technical/systems/weapons-ammo-components.md
  - docs/technical/systems/file-coverage.md
  - docs/wiki/weapons-and-ammo.md
  - docs/showcase/ru/weapons-and-ammo.md
  - docs/showcase/en/weapons-and-ammo.md
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-WEAPONS-EMPLACEMENT-001: сохранять дистанцию станкового пулемёта

## Проблема

На M1 карта EPA7FVN задаёт MachineGunEmplacement handle 1557665098 target_dist=91200. Vanilla Update при создании оружия заменяет target_dist на MinRange. После COMBAT-009 MinRange Browning стал 14 клеток вместо прежнего WeaponRange, из-за чего начальный сектор огня стал коротким.

## Цели

- Сохранять заданную на карте дистанцию автоматического MGTarget при runtime Update.

## Non-goals

- Изменение характеристик Browning, формулы CTH, минимальной дальности ручного прицеливания или Map Editor.

## Требования

- `JAZZ-WEAPONS-EMPLACEMENT-001-REQ-001` — существующий wrapper Update после vanilla вызова восстанавливает исходный target_dist, ограниченный текущими MinRange/MaxRange оружия. Только вне редактора и вне вложенного updating.
- `JAZZ-WEAPONS-EMPLACEMENT-001-REQ-002` — сохранить ammo remap, один wrapper, штатное поведение при отсутствии оружия/дистанции.

## Инварианты и ограничения

- Без новых файлов загрузки и изменений карт. При интеграции 4063af91 сохранены его helper и флаги единственного EndInteraction wrapper. Не менять editor preview и исходные предметы. target_dist не является полем DynamicData; новая загрузка карты получает authored значение.

## Acceptance criteria

- `JAZZ-WEAPONS-EMPLACEMENT-001-AC-001` — Lua-harness с vanilla Update и существующим wrapper: 91200 сохраняется, слишком малая/большая дистанция ограничивается, ammo remap работает; повторный Update не сокращает сектор.
- `JAZZ-WEAPONS-EMPLACEMENT-001-AC-002` — в игре на M1 занятие станка даёт authored сектор, ручной поворот работает; save/load сохраняет работоспособность.

## Impact и совместимость

- Vanilla MachineGunEmplacement.Update остаётся основой. JAZZ меняет runtime сохранение target_dist в уже имеющемся wrapper.
- Saves: без миграции; уже выставленный g_Overwatch не переписывается автоматически, повторное занятие станка/загрузка сектора получает корректную дистанцию.
- Network/determinism: чистый Clamp без RNG. Generated data: нет. Cross-package: чтение authored M1, без правок maps.
- Rollback: удалить сохранение target_dist из wrapper.

## План и ownership

- Пакет jazz; write set выше; exclusive resources none. Независимая игровая приёмка после Lua-harness.

## Решение владельца

- approved: project-owner, 2026-09-15, автономное исправление подтверждённых багов («начинай»). Сохраняется авторская дистанция, баланс не пересматривается.

## Evidence

- `JAZZ-WEAPONS-EMPLACEMENT-001-AC-001`: `PASS` — 2026-09-15, _check_emplacement_target_distance.py: authored distance, min/max clamp, repeated Update, ammo remap.
- `JAZZ-WEAPONS-EMPLACEMENT-001-AC-002`: `BLOCKED` — требуется игровой прогон.

## Documentation delta

- Системная страница оружия, coverage и player weapon pages.

## Интеграция upstream, 2026-09-16

Владелец разрешил объединить новые Git-изменения с локальной работой без push. Включён 4063af91: единый Jazz_EmplacementConeDist для Update, EndInteraction и reseat; занятие станка больше не обрезает сектор по видимости. Сохранены локальные ограничения: editor и вложенный Update не восстанавливают старую дистанцию.

- `JAZZ-WEAPONS-EMPLACEMENT-001-REQ-003` — уточнение REQ-001: отсутствующая или меньшая MinRange дистанция получает MaxRange согласно upstream; authored дистанция в диапазоне сохраняется, превышающая максимум ограничивается. Это заменяет прежний нижний Clamp к MinRange. EndInteraction и reseat используют тот же helper.
- `JAZZ-WEAPONS-EMPLACEMENT-001-AC-003` — offline Lua: нижний fallback MaxRange, editor/reentry guards, занятие станка без ограничения видимостью, один wrapper при повторной установке. Runtime AC-002 остаётся на ручной проверке владельца.

Интеграционная проверка 2026-09-16: AC-001 и AC-003 PASS (offline Lua с настоящим vanilla Update), upstream `_audit_emplacement_cone_range.py` PASS, wrapper audit PASS (133 sites, 2 existing allowlist). AC-002 не выполнен: живую игру проверяет владелец.
