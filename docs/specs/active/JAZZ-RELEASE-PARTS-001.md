---
id: JAZZ-RELEASE-PARTS-001
status: implemented
owner: project-owner
systems:
  - release-versioning
repositories:
  - jazz
risk: low
generated_data: false
runtime_validation: not-required
write_set:
  - docs/tools/_pack_suite_release.py
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
- `JAZZ-RELEASE-PARTS-001-AC-002`: PASS — опубликован v0.20.6232; все пять ZIP скачаны и SHA-256/размеры сверены с distribution и SHA256SUMS; приложенный manifest побайтно совпадает с Git blob тега.

## Documentation delta
Обновить release-versioning и release-contract с multipart distribution и инструкцией установки.

Владелец дополнительно явно поручил отправить ссылки на скачивание в Discord. Workflow только workflow_dispatch после проверенной публикации; автоматической рассылки для будущих релизов нет.

Проверка фактических ZIP выявила Python postprocess в NPCPortraits/newgen. Packaging исключает .py/.ps1/.fbx независимо от расположения; игровые файлы units не меняются.

Упаковка релиза закреплена за Windows / CPython 3.12.10 / zlib 1.3.1, как при расчёте manifest: разные версии zlib могут давать разные ZIP SHA при одинаковых исходных байтах. После сбоя допускается workflow_dispatch с существующим неизменяемым tag; checkout, четыре source SHA и проверки manifest сохраняются. Опубликованный release перезаписывать запрещено.

Integration evidence 29.09.2026: Windows build run 36508843762 успешно воспроизвёл четыре canonical ZIP и пять distribution ZIP; только создание draft от GITHUB_TOKEN вернуло 403. Draft создан через gh от авторизованного аккаунта, локальная проверка скачивания PASS, затем опубликован prerelease. Тег и manifest не изменялись. Public download verification: https://github.com/Kpoji4er/JAZZ/actions/runs/36510501783. Release: https://github.com/Kpoji4er/JAZZ/releases/tag/v0.20.6232.

Независимая Linux Actions проверка публичного скачивания 36510501783: SUCCESS, пять SHA-256 и tagged manifest PASS.

Discord delivery PASS: workflow 36510649832, message 1554312356530753597, channel 1378428491082502294. Отправлены release page, пять прямых ZIP ссылок, manifest, SHA256SUMS и инструкция по двум частям assets.
