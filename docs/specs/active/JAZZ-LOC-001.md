---
id: JAZZ-LOC-001
status: approved
owner: project-owner
systems:
  - localization
repositories:
  - jazz
  - jazz-maps
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - scripts/localization/migrate-localization-ids.ps1
  - Localization/IdMigration.csv
  - Localization/Strings.csv
  - Localization/Collisions.csv
  - Russian.csv
  - items.lua
  - Code/*.lua
  - InventoryItem/*.lua
  - CharacterEffect/*.lua
  - XTemplate/*.lua
  - ../jazz-maps/items.lua
  - ../jazz-units/items.lua
  - ../jazz-units/UnitData/*.lua
  - docs/specs/active/JAZZ-LOC-001.md
  - docs/technical/systems/localization.md
  - docs/technical/compatibility.md
  - docs/technical/testing.md
exclusive_resources:
  - localization-id-range-890000000000000-890000000099999
  - jazz/Russian.csv
  - jazz/items.lua
  - jazz-maps/items.lua
  - jazz-units/items.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-LOC-001: устранение коллизий localization ID

## Проблема

Статический аудит обнаружил 2 651 активный localization ID JAZZ, который либо
использует другой исходный текст, чем vanilla `Game.csv`, либо обозначает
несколько разных текстов внутри JAZZ. Один глобальный ID поэтому способен
подменить чужую строку. Текущий `Russian.csv` не содержит полного набора
mod-only ID и имеет широкий legacy-формат, не совпадающий с объявленными пятью
колонками.

## Цели

- Выдать каждому конфликтующему варианту `старый ID + SourceText` отдельный
  свободный numeric ID.
- Синхронно заменить ID во всех активных и связанных non-map Lua-представлениях.
- Сохранить трассируемую карту миграции.
- Создать нормализованный `Russian.csv` для активных ID JAZZ, отсутствующих в
  оригинальном `Game.csv`.
- Довести статический localization-аудит до отсутствия внутренних и vanilla-ID
  коллизий.

## Non-goals

- Полный английский перевод и создание готового `English.csv`.
- Рекурсивное изменение `jazz-maps/Maps/`.
- Изменение текста, баланса, class/preset/entity ID или порядка загрузки.
- Массовая перегенерация Mod Editor и косметическое форматирование Lua.
- Исправление существующих dormant/orphan warning generated-аудита.

## Требования

- `JAZZ-LOC-001-REQ-001` — для каждого активного
  `active-id-collision`/`game-id-collision` назначить уникальный ID из
  подтверждённо свободного диапазона, меньший `2^53`.
- `JAZZ-LOC-001-REQ-002` — одну пару `старый ID + SourceText` заменять одним
  новым ID во всех найденных non-map `T(...)`/`T{...}`; разные тексты старого ID
  не объединять.
- `JAZZ-LOC-001-REQ-003` — одновременно менять `items.lua`, активный generated
  companion и ручной Lua, если они содержат одну строку.
- `JAZZ-LOC-001-REQ-004` — сохранить
  `Localization/IdMigration.csv` с old/new ID, исходным текстом и изменёнными
  местами.
- `JAZZ-LOC-001-REQ-005` — нормализовать `Russian.csv` в UTF-8 и официальную
  схему `ID,Text,Translation,VoiceActor,Context`, сохранив приоритет существующих
  переводов и добавив активные mod-only ID.
- `JAZZ-LOC-001-REQ-006` — не использовать пустую или заведомо чужую vanilla
  строку как русский перевод; технические имена и токены могут совпадать с
  `SourceText`.
- `JAZZ-LOC-001-REQ-007` — повторный запуск миграции должен быть идемпотентным и
  не назначать новые ID уже мигрированным строкам.

## Инварианты и ограничения

- Numeric ID хранить и сравнивать как строку цифр, не через IEEE-754.
- Использовать диапазон `890000000000000..890000000099999` только после проверки
  против оригинального `Game.csv`, всех non-map Lua JAZZ, каталога и CSV.
- Сохранять точный `SourceText`, кавычки, переносы, placeholders и игровые теги.
- Не менять `jazz-maps/Maps/`.
- Не откатывать и не форматировать посторонние незакоммиченные изменения.
- CommonLib snapshot для реализации: upstream `main` commit
  `1adf9f232680d3b011248d180fd0ad1e609a8e2c`, version 1.11 build 1056.

## Acceptance criteria

- `JAZZ-LOC-001-AC-001` — localization-аудит сообщает
  `active=0`, `against Game.csv=0`, `Russian.csv=0`.
- `JAZZ-LOC-001-AC-002` — каждый `NewID` из карты уникален, отсутствует в
  исходном `Game.csv` и меньше `2^53`.
- `JAZZ-LOC-001-AC-003` — для каждой записи карты найдено и изменено хотя бы одно
  место, а выбранные старые конфликтующие пары отсутствуют в non-map Lua.
- `JAZZ-LOC-001-AC-004` — generated sync-аудит не добавляет новых ошибок или
  warning относительно preflight: 0 errors, 20 известных warnings.
- `JAZZ-LOC-001-AC-005` — `Russian.csv` разбирается без широких/повреждённых
  записей и содержит по одной строке на каждый активный mod-only ID.
- `JAZZ-LOC-001-AC-006` — `git diff --check` проходит отдельно в трёх изменённых
  репозиториях.
- `JAZZ-LOC-001-AC-007` — Mod Editor загружает, сохраняет и повторно загружает
  три изменённых пакета без ignored mod, load/runtime error или assert.
- `JAZZ-LOC-001-AC-008` — новая игра и существующее сохранение показывают
  проверенные русские строки без `<missing translation>` и чужих подмен.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: новые ID устраняют пересечения; определения CommonLib
  и порядок загрузки не меняются.
- Saves: localization ID не является class/preset ID, но уже сохранённые
  сериализованные T-значения требуют проверки существующего сохранения.
- Network/determinism: игровая логика и RNG не меняются.
- Generated data: правятся editor-state `items.lua` и соответствующие companion;
  требуется Mod Editor round-trip.
- Cross-package references: одинаковые строки синхронизируются по тексту между
  `jazz`, `jazz-maps` и `jazz-units`.
- Rollback/recovery: карта миграции позволяет сопоставить каждый новый ID со
  старой парой; возврат выполняется только согласованным revert трёх репозиториев.

## План и ownership

- Пакет-владелец: каждый пакет владеет своими T-вызовами; `jazz` владеет
  `Russian.csv`, каталогом и инструментами.
- Исполнитель: Codex.
- Reviewer: project-owner.
- Declared write set: только пути из frontmatter и конкретные Lua-файлы,
  перечисленные в `Localization/IdMigration.csv`.
- Exclusive resources: зарезервированный диапазон ID, `Russian.csv` и три
  `items.lua`.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner прямым запросом устранить коллизии и обновить
  `Russian.csv`.
- Дата: 2026-07-26.

## Evidence

- `JAZZ-LOC-001-AC-001`: `BLOCKED` — будет заполнено после миграции.
- `JAZZ-LOC-001-AC-002`: `BLOCKED` — будет заполнено после генерации карты.
- `JAZZ-LOC-001-AC-003`: `BLOCKED` — будет заполнено после применения.
- `JAZZ-LOC-001-AC-004`: `BLOCKED` — preflight: 0 errors, 20 warnings.
- `JAZZ-LOC-001-AC-005`: `BLOCKED` — будет заполнено после экспорта.
- `JAZZ-LOC-001-AC-006`: `BLOCKED` — будет заполнено после diff.
- `JAZZ-LOC-001-AC-007`: `BLOCKED` — требуется Mod Editor.
- `JAZZ-LOC-001-AC-008`: `BLOCKED` — требуется игра.

## Documentation delta

- Обновить `docs/technical/systems/localization.md`.
- Обновить `docs/technical/compatibility.md` для миграции public localization ID.
- Уточнить localization validation в `docs/technical/testing.md`.
- `file-coverage.md` не меняется: новые runtime-файлы и load-state не добавляются.
