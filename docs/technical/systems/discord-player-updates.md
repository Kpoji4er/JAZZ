# Сводки изменений для игроков в Discord

## Назначение и эффект для игрока

Система публикует в Discord короткие русскоязычные заметки о подтверждённых изменениях JAZZ после push в основную ветку `main`. Она переводит технический diff на понятный игрокам язык, но не объявляет работу в репозитории уже выпущенным обновлением.

Автоматизация не меняет игровой runtime, generated data, баланс или порядок загрузки модов. Публикация выполняется только GitHub Actions; отдельный постоянно работающий бот или сервер не нужен.

## Владелец и runtime-слои

| Слой | Вклад |
|---|---|
| Установленная vanilla JA3 | Не участвует: workflow не загружается игрой и не переопределяет символы JA3 |
| CommonLib | Прямого пересечения нет. Snapshot проверки 26 июля 2026 года: CommonLib 1.11, build 1056, commit `1adf9f232680d3b011248d180fd0ad1e609a8e2c` |
| JAZZ | Core-репозиторий `jazz` владеет reusable workflow, сбором Git diff, обращением к OpenAI Responses API, fallback и формированием Discord payload; три соседних пакета владеют только своими caller workflows |

Контракт подключения четырёх репозиториев зафиксирован в `JAZZ-DISCORD-001`. Каждый push обрабатывается отдельно в контексте репозитория-источника; межрепозиторной агрегации нет.

## Файлы реализации и load-state

| Файл | Статус | Назначение |
|---|---|---|
| `jazz/.github/workflows/discord-player-updates.yml` | GitHub Actions only | Прямой запуск core, `workflow_call`, checkout caller-истории и доверенной core-реализации; минимальные `contents: read` permissions |
| `.github/scripts/discord-player-update.mjs` | CI only | Сбор диапазона, фильтрация, Structured Output, fallback и Discord payload |
| `.github/scripts/discord-player-update.test.mjs` | development/test only | Локальные тесты чистых функций и временного Git-репозитория |
| `jazz_assets/.github/workflows/discord-player-updates.yml` | GitHub Actions caller only | Push/ручной запуск для ресурсов; вызывает reusable workflow из `Kpoji4er/JAZZ@main` |
| `jazz-maps/.github/workflows/discord-player-updates.yml` | GitHub Actions caller only | Push/ручной запуск для карт; вызывает reusable workflow из `Kpoji4er/JAZZ@main` |
| `jazz-units/.github/workflows/discord-player-updates.yml` | GitHub Actions caller only | Push/ручной запуск для юнитов; вызывает reusable workflow из `Kpoji4er/JAZZ@main` |

Файлы не входят в `metadata.lua` и не должны добавляться в игровой load order.

## Настройка

### Discord Incoming Webhook

1. В Discord открыть настройки нужного канала.
2. Выбрать **Integrations → Webhooks → New Webhook**.
3. Назвать webhook, при необходимости задать аватар и скопировать URL.
4. В GitHub открыть **Settings → Secrets and variables → Actions → Secrets**.
5. Создать `DISCORD_WEBHOOK_URL` в каждом из четырёх репозиториев либо organization secret с доступом ровно к этим репозиториям.

Webhook должен принадлежать публичному каналу обновлений. Не сохранять URL в репозитории, документации, issue, Actions variables или логах.

### OpenAI API

1. Создать отдельный API key на [странице API keys](https://platform.openai.com/api-keys).
2. Ограничить его проектом и бюджетом, достаточным для коротких сводок.
3. Добавить ключ в GitHub Actions repository secret `OPENAI_API_KEY` нужных репозиториев либо выдать им доступ к ограниченному organization secret.

OpenAI является опциональным улучшением качества. Если secret отсутствует, закончился API-баланс, модель недоступна или запрос завершается любой другой ошибкой, workflow автоматически публикует безопасный fallback из заголовков коммитов.

По умолчанию используется `gpt-5.6-luna`: официальная модель для cost-sensitive workloads с поддержкой Responses API и Structured Outputs на момент реализации. Repository variable `OPENAI_MODEL` может переопределить модель без изменения workflow. Выбранная модель обязана поддерживать `text.format` с JSON Schema.

Обязательный secret:

```text
DISCORD_WEBHOOK_URL
```

Опциональный secret:

```text
OPENAI_API_KEY
```

Опциональные repository variables:

```text
OPENAI_MODEL
DISCORD_UPDATE_ROLE_ID
DISCORD_MENTION_UPDATE_ROLE
```

`DISCORD_UPDATE_ROLE_ID` сам по себе никого не упоминает. Упоминание включается только при одновременном значении `DISCORD_MENTION_UPDATE_ROLE=true`; тогда `allowed_mentions` разрешает ровно указанную роль. По умолчанию `allowed_mentions.parse` пуст.

## Поток данных

1. Push в `main` или ручной `workflow_dispatch` запускает workflow репозитория-источника.
2. В `jazz` выполняется собственный workflow; в `jazz_assets`, `jazz-maps` и `jazz-units` тонкий caller вызывает `Kpoji4er/JAZZ/.github/workflows/discord-player-updates.yml@main`.
3. Reusable workflow получает `github` context caller, а первый `actions/checkout` получает полную историю репозитория-источника (`fetch-depth: 0`). Для соседнего пакета второй checkout с `persist-credentials: false` получает доверенный скрипт из `Kpoji4er/JAZZ@main` в `.jazz-automation/`.
4. Скрипт запускается из core checkout, но Git-команды выполняются в корне caller workspace; он разрешает `before` и `after`, собирает все коммиты диапазона, авторов, changed files, line stats и compare URL источника.
5. Бинарные, generated, localization, lock, build/vendor, agent и CI-файлы остаются в списке имён, но их содержимое не передаётся модели.
6. Текстовый diff приоритизирует `Code/`, player wiki и Lua, ограничивается на файл и суммарно примерно 50 тысячами символов. Для `jazz-maps` используется только Git diff: рекурсивного обхода `Maps/` нет. Обрезка явно передаётся модели.
7. Динамические данные проходят базовую редакцию токенов, ключей, паролей, private keys и webhook URL.
8. При доступном OpenAI Responses API возвращается строгий JSON по JSON Schema: `should_publish`, заголовок, вступление, разделы, development note и confidence. Без ключа или при ошибке API формируется fallback из subject-строк коммитов.
9. AI-результат или fallback повторно валидируется, редактируется и укладывается в ограничения одного Discord embed.
10. Discord webhook получает embed с именем репозитория-источника, compare link, short SHA, количеством коммитов и файлов, line stats и timestamp.

Commit messages, имена файлов и diff считаются недоверенным вводом. Они передаются как данные, не выполняются shell и не могут изменить системную инструкцию. Git вызывается через массив аргументов без shell interpolation.

## Диапазон push

- Обычный push использует точный `before..after`, а не только последний коммит.
- Несколько коммитов и merge commit входят в один диапазон.
- Force push сравнивает снимки `before` и `after`; признак force push передаётся модели.
- Нулевой `before` первого push сравнивает `after` с empty Git tree.
- Если старый `before` недоступен даже после безопасного `git fetch` по SHA, скрипт использует родителя `after`, отмечает range как degraded и пишет причину только в Actions log.
- Ручной запуск без `before_sha` сравнивает `after_sha` с его родителем. Для root commit используется empty tree.

## Правила публикации

До обращения к API workflow успешно завершает задачу без публикации, если:

- commit содержит `[skip discord]`;
- изменены только CI, тесты, tooling или внутренняя technical/agent-документация;
- отсутствуют diff и содержательные сообщения коммитов.

После обращения к API сообщение не публикуется при `should_publish=false` или `confidence=low` без ручного override. Обычно публикуются только изменения кода, игровых данных, контента, ресурсов или player wiki, которым модель может дать подтверждённое игрокоориентированное объяснение.

Маркеры сообщений коммитов:

- `[discord]` — запросить публикацию даже для пограничного изменения;
- `[skip discord]` — ничего не публиковать;
- `[skip discord]` всегда имеет приоритет.

Маркеры регистронезависимы. В fallback они удаляются из публичного текста.

## Fallback без AI

Отсутствие `OPENAI_API_KEY` и любая ошибка OpenAI, включая исчерпанную квоту, автоматически включают fallback:

- override не требуется: после прохождения prefilter формируется нейтральный список subject-строк коммитов без технических выводов;
- fallback публикуется даже с внутренним `confidence=low`, потому что этот порог относится только к AI-оценке;
- `[skip discord]` и prefilter служебных изменений по-прежнему имеют приоритет;
- stack trace, API key, request body и чувствительные данные не отправляются в Discord;
- причина fallback записывается в Actions log в редактированном виде.

Ошибка самого Discord webhook является ошибкой workflow: публикация не состоялась и требует внимания.

## Ручная проверка

1. Открыть GitHub **Actions → Discord player updates → Run workflow**.
2. Оставить `dry_run=true`. Реальная отправка в Discord при этом невозможна.
3. Не указывать SHA, чтобы проверить последний коммит выбранной ветки, либо передать полные `before_sha` и `after_sha`.
4. Для проверки override включить `force_publish=true`.
5. Просмотреть в log причину skip/fallback или sanitized Discord payload.
6. После успешного dry run повторить с `dry_run=false` только при наличии тестового webhook или при осознанной проверке публичного канала.

Без `OPENAI_API_KEY` обычный dry run автоматически покажет sanitized fallback payload. `force_publish=true` нужен только для осознанного обхода prefilter или AI-решения `should_publish=false`.

## Пример ожидаемого сообщения

```text
JAZZ — новости разработки

Продолжается работа над поведением противников и глобальной картой.

Что изменилось
• Вражеские патрули точнее учитывают последствия недавних боёв.
• Подкрепления аккуратнее выбирают маршруты.

Исправления
• Исправлена подтверждённая ситуация, когда отряд мог застрять при смене цели.

JAZZ-maps · 5 коммитов · 17 файлов · +612 / −184 · a1b2c3d
Открыть изменения
```

## Безопасность

- Workflow использует только `contents: read` и не применяет `pull_request_target`.
- Secrets передаются через environment GitHub Actions и никогда не подставляются в shell-команды.
- OpenAI SDK и Discord `fetch` используют timeout; HTTP-ошибки проверяются.
- В логи не выводятся API key, webhook URL, request body с ключами или stack trace.
- Подозрительные secret-файлы не входят в AI diff; распространённые форматы токенов и credential-строк редактируются.
- `@everyone`, `@here` и произвольные Discord mentions нейтрализуются; `allowed_mentions.parse` пуст.
- Discord webhook URL дополнительно проверяется как HTTPS URL официального webhook host.
- Используются официальная Node.js-библиотека `openai@6.49.0`, `actions/checkout@v4` и `actions/setup-node@v4`.

Редакция секретов является последней защитой, а не заменой GitHub secret scanning и запрета коммитить credentials.

## Чек-лист проверки

```powershell
node --check .github/scripts/discord-player-update.mjs
node --check .github/scripts/discord-player-update.test.mjs
node --test .github/scripts/discord-player-update.test.mjs
git diff --check
```

Дополнительно:

- разобрать YAML workflow;
- разобрать YAML трёх caller workflows и проверить ссылку на `Kpoji4er/JAZZ/.github/workflows/discord-player-updates.yml@main`;
- проверить push range на двух коммитах и zero-before;
- проверить, что `GITHUB_REPOSITORY=Kpoji4er/JAZZ-units` создаёт compare URL caller и метку `JAZZ-units` в Discord footer;
- проверить valid/invalid JSON, `should_publish=false`, оба commit marker и автоматический fallback без ключа и при ошибке API;
- проверить Discord limits, empty `allowed_mentions.parse`, redaction и mention neutralization;
- выполнить `workflow_dispatch` с `dry_run=true`;
- не отправлять реальный webhook без доступного тестового канала.

## Известные ограничения и долг

- Каждый репозиторий создаёт отдельную сводку; автоматической агрегации одного cross-repository change set нет.
- Core reusable workflow должен попасть в `jazz/main` раньше caller workflows. До этого вызов из соседнего репозитория завершится ошибкой разрешения workflow.
- Для private/internal-репозиториев GitHub требует отдельно разрешить callers доступ к reusable workflow; для public-репозиториев достаточно разрешённого Actions policy.
- Качество формулировок и стоимость зависят от выбранной модели; изменение `OPENAI_MODEL` требует повторного dry-run теста.
- Generated и binary content виден модели только по именам файлов и сообщениям коммитов, поэтому недостаточно описанный commit может быть пропущен.
- GitHub-hosted runner должен иметь сетевой доступ к npm, OpenAI API и Discord.
- Реальная отправка и ответы внешних сервисов не проверяются локальными unit tests.

## Контракт сопровождения

При изменении workflow, схемы AI, фильтров diff, marker semantics, fallback, Discord payload или списка variables одновременно обновлять:

- `.github/workflows/discord-player-updates.yml`;
- `.github/scripts/discord-player-update.mjs`;
- `.github/scripts/discord-player-update.test.mjs`;
- эту страницу;
- `docs/technical/testing.md`, если меняется общий validation profile;
- `docs/technical/systems/file-coverage.md`.

Wiki по игровой механике не обновляется, потому что система не меняет наблюдаемое поведение мода.
