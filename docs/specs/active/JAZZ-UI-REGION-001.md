---
id: JAZZ-UI-REGION-001
status: approved
owner: project-owner
systems:
  - strategy-squads-sectors
repositories:
  - jazz
risk: low
generated_data: false
runtime_validation: required
write_set:
  - Code/Regions_Sectors.lua
  - docs/specs/active/JAZZ-UI-REGION-001.md
  - docs/specs/active/JAZZ-FEEDBACK-001.md
  - docs/tools/_check_region_description_translation.py
  - docs/tools/README.md
  - docs/technical/systems/strategy-squads-sectors.md
  - docs/wiki/grand-chien-map.md
  - docs/showcase/ru/grand-chien-map.md
  - docs/showcase/en/grand-chien-map.md
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-UI-REGION-001: plain text в описании региона

## Проблема

Пользователь загрузил gosp и получил runtime assert AppendTTranslate: обычное описание авто-региона nomaps попадает в T{Description=...}. Стек указывает items.lua:117284, Region:GetRolloverHint. Поле Region.Description — обычный text, не обязательно T-value.

## Цели

Открытие информации о секторе принимает plain string из старого сейва без assert.

## Non-goals

Госпитализация и K4 quest logic, исправление кодировки старого сохранения, изменение описаний или баланса.

## Требования

- `JAZZ-UI-REGION-001-REQ-001` — непустой Description типа string оборачивается Untranslated перед вставкой в T. Уже локализованный объект сохраняется без изменений, nil/пустая строка не выводятся.

## Инварианты и ограничения

Сохранение/Region.Description не мутируются. Новых T-ID, globals и wraps нет; generated data без изменений.

## Acceptance criteria

- `JAZZ-UI-REGION-001-AC-001` — harness реального метода: plain string становится T-value, готовое T остаётся тем же объектом, nil/empty пропускаются, source не меняется.
- `JAZZ-UI-REGION-001-AC-002` — gosp загружается и панель региона не вызывает этот assert в живой игре.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: использование штатного Untranslated для динамического текста.
- Saves: действует на старые строки без перезаписи сейва.
- Network/determinism: UI only.
- Generated data: нет.
- Cross-package references: номапс-производитель не меняется, исправляется общий потребитель.
- Rollback/recovery: откат собственного изменения метода.

## План и ownership

- Пакет-владелец: jazz.
- Исполнитель: текущий агент; reviewer: владелец.
- Declared write set: frontmatter.
- Exclusive resources: none.

## Решение владельца

- Статус: approved, автономная обработка игрового фидбека и живой тест разрешены ранее; текущий скриншот уточняет воспроизведённый дефект.
- Кто подтвердил: project-owner.
- Дата: 2026-09-15.

## Evidence

- `JAZZ-UI-REGION-001-AC-001`: `PASS` — isolated Lua harness реального метода, 2026-09-15; не live runtime.
- `JAZZ-UI-REGION-001-AC-002`: `BLOCKED` — после фикса live ещё не проверен; до фикса есть скриншот пользователя со стеком.

## Documentation delta

Профильная technical-страница и краткое уточнение wiki/showcase; без изменения игрового контракта регионов.
