---
id: JAZZ-WEAPON-AK47-001
status: implemented
owner: project-owner
systems:
  - weapons-ammo-components
repositories:
  - jazz
risk: low
generated_data: true
runtime_validation: not-required
write_set:
  - InventoryItem/AK47.lua
  - items.lua
  - docs/technical/weapons/data/weapons.csv
  - docs/wiki/weapons/**
  - docs/technical/systems/weapons-ammo-components.md
  - docs/showcase/ru/weapons-and-ammo.md
  - docs/showcase/en/weapons-and-ammo.md
  - docs/design/weapon-balance-audit-2026-09-15.md
  - docs/specs/active/JAZZ-WEAPON-AK47-001.md
exclusive_resources:
  - items.lua
approved_by: project-owner
---

# JAZZ-WEAPON-AK47-001: АК-47 — 600 RPM и очереди 3/6

## Проблема

АК-47 имеет 700 RPM и очереди 4/7, хотя принятый номинальный темп для АК и АКМ — 600. Правило владельца: короткая очередь RPM/200, длинная RPM/100.

## Цели

Привести исходные данные АК-47 к 600 RPM и 3/6 пулям.

## Non-goals

Не менять АКМ, отдачу, урон, AP, другие стволы и механику стрельбы.

## Требования

- JAZZ-WEAPON-AK47-001-REQ-001 — CyclicRPM=600, BurstShots=3, AutoShots=6 в AK47 companion и ModItem; отразить числа в документации.

## Инварианты и ограничения

Сохранить ID, регистрацию metadata, порядок загрузки и посторонние изменения рабочего дерева. Asset contract без изменений.

## Acceptance criteria

- JAZZ-WEAPON-AK47-001-AC-001 — три значения совпадают в companion, items.lua и CSV; Lua проходит статическую проверку.

## Impact и совместимость

Только данные JAZZ; API vanilla/CommonLib, сетевые алгоритмы и структура сохранений не меняются. Metadata уже регистрирует InventoryItem/AK47.lua и не требует правки. Откат — вернуть 700/4/7 в двух игровых представлениях и каталоге. Поведение существующих экземпляров в сохранении и editor round-trip отдельно не подтверждены.

## План и ownership

Владелец и исполнитель: jazz / текущая задача. Exclusive resource: items.lua. Независимое ревью не проводилось; статус accepted не заявляется.

## Решение владельца

Подтверждено владельцем в текущей беседе: «угу» после предложения 600 RPM и 3/6, затем «закрыл» для применения подготовленного патча. Дата: 2026-09-15.

## Evidence

- JAZZ-WEAPON-AK47-001-AC-001: PASS — static: companion исполнен через lupa, CyclicRPM/BurstShots/AutoShots проверены как 600/3/6 и сопоставлены с точной записью ModItem и CSV. Регистрация InventoryItem/AK47.lua в metadata сохранена. `_validate_items_quick.py`, `weapons-docs.mjs check` и `git diff --check` затронутых файлов завершились успешно.

Общий `check-generated-sync.ps1 -Package jazz` не прошёл: 891 диагностическая ошибка и 835 предупреждений, в том числе обход tmp/suite-release-stage и существующие проблемы других InventoryItem. Общий `check-system-docs.ps1` также не прошёл на посторонних документах/skill manifests. Эти результаты не объявляются успешными; они не исправлялись в узкой транзакции АК-47. Полный strict-аудит комплекта и независимое ревью остаются за рамками готовности к релизу.

Игра была закрыта перед записью. Editor save/reload и бой не выполнялись; round-trip не подтверждён, готовность к релизу не заявляется.

## Documentation delta

CSV и производные оружейные страницы, краткая technical/showcase запись; аудит сохраняет исходные измерения с пометкой последующего исправления.
