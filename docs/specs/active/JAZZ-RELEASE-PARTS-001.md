---
id: JAZZ-RELEASE-PARTS-001
status: approved
owner: project-owner
systems:
  - release-versioning
repositories:
  - jazz
risk: low
generated_data: false
runtime_validation: not-required
write_set:
  - docs/tools/_prepare_release_assets.py
  - docs/tools/_test_release_assets.py
  - .github/workflows/publish-suite-release.yml
  - .github/workflows/discord-suite-release.yml
  - .github/scripts/discord-suite-release.mjs
  - release/manifests/*
  - release/notes/*
  - docs/technical/systems/release-versioning.md
  - docs/tools/README.md
  - .agents/docs/index.md
  - .agents/skills/release-jazz-suite/references/release-contract.md
exclusive_resources:
  - release-manifest
approved_by: project-owner
---

# JAZZ-RELEASE-PARTS-001: доставка больших пакетов

## Проблема
Архив assets версии 657 превышает лимит GitHub 2 GiB на один файл.

## Цели
Доставить полный утверждённый комплект без потери игровых файлов.

## Non-goals
Изменение текстур, моделей, игровых данных или SHA исходных пакетов.

## Требования
- `JAZZ-RELEASE-PARTS-001-REQ-001` — четыре логических пакета сохраняют SHA и canonical ZIP checksum; oversized ZIP распространяется независимыми ZIP-частями с тем же корневым каталогом.
- `JAZZ-RELEASE-PARTS-001-REQ-002` — distribution manifest и SHA256SUMS перечисляют все загружаемые части; workflow воспроизводит и сверяет их до draft.

## Инварианты и ограничения
Ни один файл не пропускается и не дублируется. Порядок сортировки, timestamps и compression фиксированы. Каждая часть меньше 2 GiB. Пользователь распаковывает все части в Mods.

## Acceptance criteria
- `JAZZ-RELEASE-PARTS-001-AC-001` — static: тест нескольких частей, byte equality каждого файла, отсутствие дублей, повторяемость ZIP SHA и проверка лимита.
- `JAZZ-RELEASE-PARTS-001-AC-002` — integration: опубликованные assets скачаны, SHA сверены с manifest.

## Impact и совместимость
Vanilla/CommonLib/JAZZ, saves и network не затронуты. Generated data нет. Cross-package bytes неизменны. Rollback: до публикации draft; опубликованные теги не заменять.

## План и ownership
Пакет-владелец jazz. Исполнитель и reviewer текущий агент. Declared write set и exclusive resources перечислены выше.

## Решение владельца
Approved 29.09.2026: пользователь явно поручил закончить, закрыть игру, выпустить релиз и дать ссылки здесь и в Discord. Части — необходимая упаковка этого релиза, без изменения содержимого.

## Evidence
- `JAZZ-RELEASE-PARTS-001-AC-001`: PASS — `_test_release_assets.py`: byte coverage, no duplicates, deterministic parts, size guards.
- `JAZZ-RELEASE-PARTS-001-AC-002`: BLOCKED до workflow и скачивания.

## Documentation delta
Обновить release-versioning и release-contract с multipart distribution и инструкцией установки.

Владелец дополнительно явно поручил отправить ссылки на скачивание в Discord. Workflow только workflow_dispatch после проверенной публикации; автоматической рассылки для будущих релизов нет.
