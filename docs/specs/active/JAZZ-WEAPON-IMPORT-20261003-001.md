---
id: JAZZ-WEAPON-IMPORT-20261003-001
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
  - weapon-assets
repositories:
  - jazz
  - jazz_assets
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-WEAPON-*.md
  - jazz/docs/tools/*aek*
  - jazz/docs/tools/*weapon_import_20261003*
  - jazz/docs/tools/README.md
  - jazz/docs/design/weapons-import-plan-jaweapons.md
  - jazz/docs/design/weapons-import-20261003*
  - external/JaWeapons/Weapons/_weapon_import_20261003/**
exclusive_resources:
  - weapon-import-20261003
  - items.lua
  - metadata.lua
approved_by: project-owner
---

# JAZZ-WEAPON-IMPORT-20261003-001: вся новая очередь, 32 позиции

## Проблема

Предыдущий batch проверил только часть нынешних исходников и не установил предметы.
Владелец просит выполнить текущую очередь целиком, с общей игровой проверкой в конце.

## Цели

Выполнить все 32 позиции актуального раздела плана от 03.10.2026: модели, модульные
семейства, данные и проверяемый комплект. АЕК уже ведётся по JAZZ-WEAPON-AEK-001.

## Non-goals

Запуск игры до общей проверки, публикация, изменение maps/units, массовая случайная
выдача уников; повторный импорт старой очереди пистолетов и ПП вне этих 32 позиций.

## Требования

- `JAZZ-WEAPON-IMPORT-20261003-001-REQ-001`: реестр всех 32 позиций, существующих ID, альтернативных исходников, этапов и выявленных препятствий; источник без UV не объявлять готовым.
- `JAZZ-WEAPON-IMPORT-20261003-001-REQ-002`: исходники read-only, точные hashes, повторно использовать уже выполненный аудит только при совпадении SHA256; недостающие импортировать отдельно.
- `JAZZ-WEAPON-IMPORT-20261003-001-REQ-003`: каждому семейству перед регистрацией присвоить отдельную/существующую конкретную spec с ID, модулями, эффектами, миграцией и write set. Объединения сохраняют старые варианты через конфигурации и совместимость старых сохранений.
- `JAZZ-WEAPON-IMPORT-20261003-001-REQ-004`: каждый из MG3/MG4/MG5/Negev отдельный предмет; G11/OICW уникальны. SKS/Kar98/M72/R870 — существующие платформы. Не дублировать модель и предмет по числу архивов.
- `JAZZ-WEAPON-IMPORT-20261003-001-REQ-005`: source/compiled mesh, winding, UV/PBR/RM, посадка аттачей, регистрация, RU/EN и offline Lua проверяются до общей игровой проверки. Предварительные цифры явно помечены рабочими; недостающие детали дизайна фиксируются в конкретных specs до реализации.

## Инварианты и ограничения

Авторские цвета/normal maps, RM=(Rough,Rough,Metal), без custom mesh normals.
Чужие текущие правки сохранять. Не скрывать REJECT/REVIEW за общим успешным экспортом.
Существующие импорты не переустанавливать без совпадения исходного hash.

## Acceptance criteria

- `JAZZ-WEAPON-IMPORT-20261003-001-AC-001`: все 32 позиции представлены, ни один альтернативный источник не потерян; source hashes и коллизии ID проверены.
- `JAZZ-WEAPON-IMPORT-20261003-001-AC-002`: конкретные family specs и offline evidence закрывают каждую позицию либо фиксируют объективный дефект, требующий исходника/решения владельца.
- `JAZZ-WEAPON-IMPORT-20261003-001-AC-003`: весь установленный комплект проходит ссылки/регистрацию/Lua; runtime и editor round-trip остаются отдельным итоговым этапом владельца.

## Impact и совместимость

Vanilla/CommonLib/JAZZ: штатные классы оружия и компонентная система.
Saves: новые ID либо миграция/alias в конкретных specs; без массового удаления.
Network/determinism: штатные синхронные setters, без случайной миграции.
Generated data/cross-package: jazz → jazz_assets, отдельные транзакции по семействам.
Rollback: staging/backup с проверкой хэшей, никакого reset чужих правок.

## План и ownership

Текущий чат: весь проход. jazz — specs/tools/предметы, jazz_assets — визуалы.
Конкретные производственные файлы добавляются в family write set перед записью.
Никаких изменений runtime под одним лишь общим wildcard этого master-контракта.

## Решение владельца

Approved 2026-10-03: «дальше новое оружие по этому плану», затем «делай все сразу
по списку, потом проверим все». Для АЕК отдельно приняты предложенные рабочие
числа и подбор недостающих по аналогам.

Последующее решение владельца: «пока исключим mk12». №10 временно исключён;
активны 32 позиции / 38 источников, исторические файлы и диагностика сохранены.
Исправление Mk12 и его UV не требуется для завершения текущего прохода.

## Evidence

- `JAZZ-WEAPON-IMPORT-20261003-001-AC-001`: BLOCKED — source-часть PASS (static): все 32 позиции и 38 источников учтены; SHA256 проверены, существующие ID подтверждены. Окончательные новые ID ещё назначаются по family specs, проверка их коллизий впереди. Реестр: `docs/design/weapons-import-20261003-progress.md`, машинный sources.json в external build. Первичные ошибки Kar98 устранены отделением префиксов новой очереди от старых material profiles.
- `JAZZ-WEAPON-IMPORT-20261003-001-AC-002`: BLOCKED — выполнение.
- `JAZZ-WEAPON-IMPORT-20261003-001-AC-003`: BLOCKED — выполнение; runtime отложен.

## Documentation delta

План и машинный progress report; technical/wiki/showcase отражают только фактически
установленные семейства с явным указанием уровня проверки.
