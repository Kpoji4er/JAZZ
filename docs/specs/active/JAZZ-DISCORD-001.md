---
id: JAZZ-DISCORD-001
status: implemented
owner: project-owner
systems:
  - discord-player-updates
repositories:
  - jazz
  - jazz_assets
  - jazz-maps
  - jazz-units
risk: medium
generated_data: false
runtime_validation: not-required
write_set:
  - jazz/.github/workflows/discord-player-updates.yml
  - jazz/.github/scripts/discord-player-update.mjs
  - jazz/.github/scripts/discord-player-update.test.mjs
  - jazz/docs/specs/active/JAZZ-DISCORD-001.md
  - jazz/docs/technical/systems/discord-player-updates.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz_assets/.github/workflows/discord-player-updates.yml
  - jazz-maps/.github/workflows/discord-player-updates.yml
  - jazz-units/.github/workflows/discord-player-updates.yml
exclusive_resources:
  - none
related_decisions:
  - docs/technical/ai-first-development.md
approved_by: project-owner
---

# Discord-сводки изменений из четырёх пакетов JAZZ

## Проблема

Существующая автоматизация публикует сводки только для push в основной репозиторий `jazz`. Изменения ресурсов, карт и юнитов в `jazz_assets`, `jazz-maps` и `jazz-units` остаются невидимыми в том же Discord-канале, хотя четыре репозитория образуют один комплект.

## Цели

- подключить push в `main` всех четырёх репозиториев к одному формату Discord-сводок;
- сохранить единственную реализацию сборщика diff, AI/fallback и Discord payload в `jazz`;
- явно показывать в сообщении репозиторий-источник;
- сохранить безопасные фильтры, ручной dry run и работу без оплаченного OpenAI API.

## Non-goals

- агрегация нескольких репозиториев в одну сводку релиза;
- изменение игрового runtime, generated data, `metadata.lua`, зависимостей или порядка загрузки;
- рекурсивный анализ `jazz-maps/Maps/` вне файлов, уже присутствующих в Git diff;
- автоматическая настройка Discord webhook, GitHub secrets или биллинга OpenAI;
- публикация пользовательской wiki для внутренней CI-автоматизации.

## Требования

- `JAZZ-DISCORD-001-REQ-001`: core workflow в `jazz` поддерживает `workflow_call`, сохраняя собственные `push` и `workflow_dispatch`.
- `JAZZ-DISCORD-001-REQ-002`: `jazz_assets`, `jazz-maps` и `jazz-units` содержат тонкие caller workflows для `push` в `main` и ручного dry run.
- `JAZZ-DISCORD-001-REQ-003`: reusable workflow получает Git-контекст вызывающего репозитория, строит diff и compare URL именно для него, а реализацию скрипта берёт из доверенного core-репозитория.
- `JAZZ-DISCORD-001-REQ-004`: Discord embed явно содержит имя репозитория-источника.
- `JAZZ-DISCORD-001-REQ-005`: `DISCORD_WEBHOOK_URL` остаётся обязательным только для реальной публикации; отсутствие или ошибка `OPENAI_API_KEY` включает автоматический fallback.
- `JAZZ-DISCORD-001-REQ-006`: callers передают только именованные secrets/variables и работают с минимальным разрешением `contents: read`.
- `JAZZ-DISCORD-001-REQ-007`: core reusable workflow должен быть слит в `main` раньше caller workflows; callers используют `Kpoji4er/JAZZ/.github/workflows/discord-player-updates.yml@main`.

## Инварианты и ограничения

- Изменяются только CI, тестовые и технические документационные файлы из `write_set`.
- Secrets не выводятся в log и не передаются через аргументы shell-команд.
- `[skip discord]`, служебный prefilter, deleted branch и push не в `main` не публикуют сообщение.
- Первый merge, добавляющий только caller workflow, считается служебным и не создаёт Discord-сводку.
- `allowed_mentions.parse` остаётся пустым; роль упоминается только при явной настройке.
- Карты оцениваются только по ограниченному Git diff; полный обход `Maps/` не выполняется.
- Существующие незакоммиченные изменения владельца во всех четырёх рабочих каталогах не входят в change set.

## Acceptance criteria

- `JAZZ-DISCORD-001-AC-001`: локальные Node.js syntax checks и весь набор unit/integration tests core-скрипта проходят.
- `JAZZ-DISCORD-001-AC-002`: YAML-парсер принимает core reusable workflow и три caller workflows.
- `JAZZ-DISCORD-001-AC-003`: тест подтверждает имя и compare URL вызывающего репозитория в Discord payload.
- `JAZZ-DISCORD-001-AC-004`: callers ссылаются на core reusable workflow, передают именованные secrets/variables и имеют только `contents: read`.
- `JAZZ-DISCORD-001-AC-005`: `git diff --check` проходит отдельно во всех четырёх репозиториях, а staged scope соответствует `write_set`.
- `JAZZ-DISCORD-001-AC-006`: Ready/Done валидатор этой спецификации и применимые documentation checks проходят.

## Impact и совместимость

- Vanilla JA3, CommonLib и runtime JAZZ не затрагиваются.
- Save, network, public ID, localization и generated-data contracts не меняются.
- Межпакетное влияние ограничено GitHub Actions: каждое событие выполняется и оплачивается в caller-репозитории, а формат и скрипт централизованно обслуживаются в `jazz`.
- При недоступности reusable workflow caller job завершается ошибкой до отправки; откат состоит в удалении трёх caller workflows и `workflow_call`-интерфейса.

## План и ownership

1. Core owner добавляет и тестирует `workflow_call`, checkout доверенной реализации и маркировку репозитория.
2. Package owners добавляют тонкий caller workflow в каждый соседний репозиторий.
3. Core PR с reusable workflow сливается первым.
4. После core merge сливаются caller PR и настраивается `DISCORD_WEBHOOK_URL` для каждого репозитория либо общий organization secret с доступом к ним.
5. Владелец проекта выполняет ручной `dry_run=true`, затем принимает решение о реальной отправке.

## Решение владельца

26 июля 2026 года владелец проекта ответом «давай» одобрил подключение `jazz_assets`, `jazz-maps` и `jazz-units` к уже созданной автоматизации Discord-сводок. Формат принят как reusable workflow в `jazz` плюс тонкие callers в соседних репозиториях.

## Evidence

- `JAZZ-DISCORD-001-AC-001`: `PASS` — static: `node --check` для обоих MJS-файлов и `node --test` завершены, 16/16 тестов прошли; core implementation commit `ae3015d`.
- `JAZZ-DISCORD-001-AC-002`: `PASS` — static: `js-yaml@4.1.0` разобрал core workflow и три caller workflow без ошибок.
- `JAZZ-DISCORD-001-AC-003`: `PASS` — static: тест диапазона использует `Kpoji4er/JAZZ-units`, проверяет caller compare URL и AI context; payload-тест проверяет footer `JAZZ-maps`.
- `JAZZ-DISCORD-001-AC-004`: `PASS` — static: callers содержат только `contents: read`, ссылку на `Kpoji4er/JAZZ/.github/workflows/discord-player-updates.yml@main` и именованные secrets; commits `dc2e95d` (assets), `3d76ac5` (maps), `384c35a` (units).
- `JAZZ-DISCORD-001-AC-005`: `PASS` — static: `git diff --check` прошёл отдельно для core declared write set и трёх caller worktrees; staged scope каждого коммита просмотрен до фиксации.
- `JAZZ-DISCORD-001-AC-006`: `PASS` — static: Ready validator, `check-system-docs.ps1` и Done validator прошли. Для CRLF-файла Done-проверка использовала session-only нормализацию строк из-за ограничения heading-regex; исходный валидатор не менялся.

## Documentation delta

- Обновить `docs/technical/systems/discord-player-updates.md`: ownership, четыре источника событий, reusable/caller execution, secrets и порядок развёртывания.
- Обновить `docs/technical/systems/file-coverage.md`: отметить core reusable workflow и caller workflows трёх соседних пакетов.
- `docs/technical/testing.md` менять только если существующий тестовый контракт не покрывает новые cross-repository проверки.
- Wiki не меняется: пользовательская игровая механика и выпущенный контент не затронуты.
