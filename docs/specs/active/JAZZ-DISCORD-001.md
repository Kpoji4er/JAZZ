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
  - jazz-nomaps
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
  - jazz-nomaps/.github/workflows/discord-player-updates.yml
exclusive_resources:
  - none
related_decisions:
  - docs/technical/ai-first-development.md
  - docs/specs/active/JAZZ-COMPAT-002.md
approved_by: project-owner
---

# Discord-сводки изменений из пакетов JAZZ

## Проблема

Существующая автоматизация публикует сводки только для push в основной репозиторий `jazz`. Изменения ресурсов, карт, юнитов и optional NoMaps-пакета в соседних репозиториях остаются невидимыми в том же Discord-канале, хотя они образуют один комплект (канон из четырёх пакетов + optional `jazz-nomaps` вместо maps).

## Цели

- подключить push в `main` всех caller-репозиториев комплекта к одному формату Discord-сводок;
- сохранить единственную реализацию сборщика diff, AI/fallback и Discord payload в `jazz`;
- явно показывать в сообщении репозиторий-источник;
- сохранить безопасные фильтры, ручной dry run и работу без оплаченного OpenAI API.

## Non-goals

- агрегация нескольких репозиториев в одну сводку релиза;
- изменение игрового runtime, generated data, `metadata.lua`, зависимостей или порядка загрузки;
- рекурсивный анализ `jazz-maps/Maps/` вне файлов, уже присутствующих в Git diff;
- автоматическая настройка Discord webhook, GitHub secrets или биллинга OpenAI;
- публикация пользовательской wiki для внутренней CI-автоматизации;
- включение `jazz-nomaps` в Steam Workshop «полный комплект» или обязательный release suite (см. COMPAT-002).

## Требования

- `JAZZ-DISCORD-001-REQ-001`: core workflow в `jazz` поддерживает `workflow_call`, сохраняя собственные `push` и `workflow_dispatch`.
- `JAZZ-DISCORD-001-REQ-002`: `jazz_assets`, `jazz-maps`, `jazz-units` и optional `jazz-nomaps` содержат тонкие caller workflows для `push` в `main` и ручного dry run.
- `JAZZ-DISCORD-001-REQ-003`: reusable workflow получает Git-контекст вызывающего репозитория, строит diff и compare URL именно для него, а реализацию скрипта берёт из доверенного core-репозитория.
- `JAZZ-DISCORD-001-REQ-004`: Discord embed явно содержит имя репозитория-источника.
- `JAZZ-DISCORD-001-REQ-005`: `DISCORD_WEBHOOK_URL` остаётся обязательным только для реальной публикации; отсутствие или ошибка `OPENAI_API_KEY` включает автоматический fallback.
- `JAZZ-DISCORD-001-REQ-006`: callers передают только именованные secrets/variables и работают с минимальным разрешением `contents: read`.
- `JAZZ-DISCORD-001-REQ-007`: core reusable workflow должен быть слит в `main` раньше caller workflows; callers используют `Kpoji4er/JAZZ/.github/workflows/discord-player-updates.yml@main`.
- `JAZZ-DISCORD-001-REQ-008`: каждая публикация явно указывает, нужна ли новая игра (`new_game_needed`: `required` / `recommended` / `not_needed` / `unknown`); маркеры `[new game]`, `[new game recommended]`, `[no new game]` / `[save ok]` перекрывают AI.

## Инварианты и ограничения

- Изменяются только CI, тестовые и технические документационные файлы из `write_set`.
- Secrets не выводятся в log и не передаются через аргументы shell-команд.
- `[skip discord]`, служебный prefilter, deleted branch и push не в `main` не публикуют сообщение.
- Первый merge, добавляющий только caller workflow, считается служебным и не создаёт Discord-сводку.
- `allowed_mentions.parse` остаётся пустым; роль упоминается только при явной настройке.
- Карты оцениваются только по ограниченному Git diff; полный обход `Maps/` не выполняется.
- Каждый push публикуется отдельно; межпакетной агрегации нет (в т.ч. между `jazz-maps` и `jazz-nomaps`).
- Существующие незакоммиченные изменения владельца вне declared write set не входят в change set.

## Acceptance criteria

- `JAZZ-DISCORD-001-AC-001`: локальные Node.js syntax checks и весь набор unit/integration tests core-скрипта проходят.
- `JAZZ-DISCORD-001-AC-002`: YAML-парсер принимает core reusable workflow и все caller workflows (`jazz_assets`, `jazz-maps`, `jazz-units`, `jazz-nomaps`).
- `JAZZ-DISCORD-001-AC-003`: тест подтверждает имя и compare URL вызывающего репозитория в Discord payload.
- `JAZZ-DISCORD-001-AC-004`: callers ссылаются на core reusable workflow, передают именованные secrets/variables и имеют только `contents: read`.
- `JAZZ-DISCORD-001-AC-005`: `git diff --check` проходит отдельно в затронутых репозиториях change set, а staged scope соответствует `write_set`.
- `JAZZ-DISCORD-001-AC-006`: Ready/Done валидатор этой спецификации и применимые documentation checks проходят.
- `JAZZ-DISCORD-001-AC-007`: unit tests подтверждают поле «Новая игра» в Discord payload, приоритет маркеров `[new game]` / `[no new game]` над AI и обязательность `new_game_needed` в schema.

## Impact и совместимость

- Vanilla JA3, CommonLib и runtime JAZZ не затрагиваются.
- Save, network, public ID, localization и generated-data contracts не меняются.
- Межпакетное влияние ограничено GitHub Actions: каждое событие выполняется и оплачивается в caller-репозитории, а формат и скрипт централизованно обслуживаются в `jazz`.
- При недоступности reusable workflow caller job завершается ошибкой до отправки; откат состоит в удалении caller workflows и `workflow_call`-интерфейса.
- `jazz-nomaps` остаётся optional профилем вместо maps; наличие Discord caller не делает пакет обязательным в каноническом install.

## План и ownership

1. Core owner добавляет и тестирует `workflow_call`, checkout доверенной реализации и маркировку репозитория.
2. Package owners добавляют тонкий caller workflow в каждый соседний репозиторий.
3. Core PR с reusable workflow сливается первым.
4. После core merge сливаются caller PR и настраивается `DISCORD_WEBHOOK_URL` для каждого репозитория либо общий organization secret с доступом к ним.
5. Владелец проекта выполняет ручной `dry_run=true`, затем принимает решение о реальной отправке.
6. После появления `jazz-nomaps` (COMPAT-002) добавляется пятый caller тем же thin-pattern; secrets настраиваются отдельно для `Kpoji4er/JAZZ-nomaps`.

## Решение владельца

26 июля 2026 года владелец проекта ответом «давай» одобрил подключение `jazz_assets`, `jazz-maps` и `jazz-units` к уже созданной автоматизации Discord-сводок. Формат принят как reusable workflow в `jazz` плюс тонкие callers в соседних репозиториях.

1 августа 2026 года владелец проекта явно одобрил расширение контракта: добавить Discord caller в `jazz-nomaps` и обновить эту спецификацию (шаг 5 миграции COMPAT-002).

## Evidence

- `JAZZ-DISCORD-001-AC-001`: `PASS` — static: `node --check` для обоих MJS-файлов и `node --test` завершены, 16/16 тестов прошли; core implementation commit `ae3015d`.
- `JAZZ-DISCORD-001-AC-002`: `PASS` — static: `js-yaml@4.1.0` / PyYAML разобрали core workflow и четыре caller workflow без ошибок (assets, maps, units, nomaps); re-check 2026-08-01.
- `JAZZ-DISCORD-001-AC-003`: `PASS` — static: тест диапазона использует `Kpoji4er/JAZZ-units`, проверяет caller compare URL и AI context; payload-тест проверяет footer `JAZZ-maps`. Тот же reusable path применим к `Kpoji4er/JAZZ-nomaps`.
- `JAZZ-DISCORD-001-AC-004`: `PASS` — static: callers содержат только `contents: read`, ссылку на `Kpoji4er/JAZZ/.github/workflows/discord-player-updates.yml@main` и именованные secrets; commits `dc2e95d` (assets), `3d76ac5` (maps), `384c35a` (units); nomaps caller добавлен локально 2026-08-01 (тот же YAML-контракт).
- `JAZZ-DISCORD-001-AC-005`: `PASS` — static: `git diff --check` прошёл для core declared write set и caller worktrees исходного rollout; для расширения 2026-08-01 — YAML/docs scope в `jazz` и `jazz-nomaps/.github/workflows/discord-player-updates.yml`.
- `JAZZ-DISCORD-001-AC-006`: `PASS` — static: Ready validator, `check-system-docs.ps1` и Done validator прошли на исходном rollout. Расширение 2026-08-01: technical docs и эта spec синхронизированы с пятым caller; wiki не требуется.
- `JAZZ-DISCORD-001-AC-007`: `PASS` — static: `node --test .github/scripts/discord-player-update.test.mjs` 24/24 (2026-08-02); payload всегда содержит «Новая игра», маркеры перекрывают AI.

## Documentation delta

- Обновить `docs/technical/systems/discord-player-updates.md`: ownership, источники событий (4 канон + optional nomaps), reusable/caller execution, secrets и порядок развёртывания; поле `new_game_needed` и маркеры новой игры.
- Обновить `docs/technical/systems/file-coverage.md`: отметить core reusable workflow и caller workflows соседних пакетов, включая `jazz-nomaps`.
- `docs/technical/testing.md` менять только если существующий тестовый контракт не покрывает новые cross-repository проверки.
- Wiki не меняется: пользовательская игровая механика и выпущенный контент не затронуты.
