---
id: JAZZ-DISCORD-002
status: implemented
owner: project-owner
systems:
  - discord-player-updates
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: not-required
write_set:
  - .github/scripts/discord-player-update.mjs
  - .github/scripts/discord-player-update.test.mjs
  - docs/specs/active/JAZZ-DISCORD-002.md
  - docs/technical/systems/discord-player-updates.md
  - docs/technical/testing.md
exclusive_resources:
  - none
related_decisions:
  - JAZZ-DISCORD-001
approved_by: project-owner
---

# JAZZ-DISCORD-002: отделить реализованные изменения от документации

## Проблема

Текущая AI-сводка принудительно называет изменения, уже добавленные в `main`,
«работой в разработке» и выводит отдельный блок «За кулисами». Одновременно
изменения в `docs/` попадают в контекст модели наравне с runtime-кодом и могут
ошибочно восприниматься как доказательство реализованного поведения.

## Цели

- Описывать runtime/data diff, уже добавленный в `main`, как изменения в коде,
  не утверждая при этом, что они выпущены в игровой сборке или релизе.
- Не считать `docs/` доказательством реализации без явного указания владельца.
- Различать игровую сводку, документационную сводку и явное подтверждение
  реализации, содержащееся в документации.

## Non-goals

- Определение даты релиза, версии мода или доступности изменений в игровой
  сборке.
- Runtime-тест игрового поведения.
- Изменение reusable workflow, секретов, Discord webhook или OpenAI-модели.
- Изменение generated data четырёх пакетов JAZZ.

## Требования

- JAZZ-DISCORD-002-REQ-001: Все пути под `docs/` классифицируются как документация и по умолчанию
   исключаются из diff-контекста модели.
- JAZZ-DISCORD-002-REQ-002: Docs-only push без явного маркера пропускается до обращения к OpenAI и
   fallback-публикации.
- JAZZ-DISCORD-002-REQ-003: Маркер `[discord]` разрешает документационную сводку, но не разрешает
   выдавать описанное в документации игровое поведение за реализованное.
- JAZZ-DISCORD-002-REQ-004: Маркер `[discord implemented]` является явным подтверждением владельца:
   документация включается в evidence и может поддерживать утверждение об уже
   реализованном изменении.
- JAZZ-DISCORD-002-REQ-005: `[skip discord]` сохраняет приоритет над обоими публикующими маркерами.
- JAZZ-DISCORD-002-REQ-006: Контекст модели отдельно передаёт implementation-файлы,
   documentation-файлы, признак docs-only и признак явного подтверждения.
- JAZZ-DISCORD-002-REQ-007: Prompt, fallback и Discord payload не должны автоматически называть
   изменения в `main` «работой в разработке» или добавлять блок
   «За кулисами».

## Инварианты и ограничения

- Изменение, попавшее в `main`, не приравнивается к опубликованному релизу.
- Факты о реализованном игровом поведении должны опираться на runtime/data diff
  либо на явный маркер `[discord implemented]`.
- Commit message и обычная документация без явного маркера не являются
  достаточным доказательством реализации.
- Существующий `[discord]` продолжает принудительно публиковать сводку, а
  `[skip discord]` продолжает отменять публикацию.
- Формат Discord embed, лимиты Discord, redaction секретов и dry-run остаются
  действующими.

## Acceptance criteria

- JAZZ-DISCORD-002-AC-001: Регрессионный диапазон `130bc49..deced41` классифицирует изменённый runtime
   Lua как implementation evidence, а все `docs/` исключает из AI diff.
- JAZZ-DISCORD-002-AC-002: Prompt описывает implementation diff как добавленный в `main`, но запрещает
   утверждать, что изменение уже выпущено в сборке или релизе.
- JAZZ-DISCORD-002-AC-003: Docs-only push без маркера получает skip reason и не доходит до генерации.
- JAZZ-DISCORD-002-AC-004: Docs-only push с `[discord]` допускает только документационную сводку.
- JAZZ-DISCORD-002-AC-005: Docs-only push с `[discord implemented]` включает документационный diff и
   устанавливает явный implementation-флаг.
- JAZZ-DISCORD-002-AC-006: `[skip discord]` побеждает при сочетании с любым публикующим маркером.
- JAZZ-DISCORD-002-AC-007: Fallback и собранный Discord payload не содержат автоматических формулировок
   «в разработке» и секции «За кулисами».
- JAZZ-DISCORD-002-AC-008: Проходят Node-тесты, YAML parse, `git diff --check`, Ready/Done-валидаторы
   спецификации и профильный documentation audit.

## Impact и совместимость

Изменение затрагивает только reusable automation репозитория `jazz`.
Тонкие callers `jazz_assets`, `jazz-maps` и `jazz-units` автоматически получают
исправление через `Kpoji4er/JAZZ@main`. Runtime JA3, saves, multiplayer,
dependencies, public IDs и generated data не меняются.

## План и ownership

1. `jazz`: изменить классификацию путей, маркеры, AI-контекст, prompt, fallback
   и payload.
2. `jazz`: добавить unit/regression-тесты для docs-only и явного маркера.
3. `jazz`: синхронизировать техническое описание и тестовый контракт.

Владелец всех файлов — репозиторий `jazz`; пересечений write set с соседними
пакетами нет.

## Решение владельца

Владелец проекта явно потребовал не считать изменения в `docs/`
реализованными, если это не указано отдельно, и подтвердил исправление
неверной семантики сводки.

## Evidence

- `JAZZ-DISCORD-002-AC-001`: `PASS` — реконструкция диапазона
  `130bc49d42a0cea7cb3387b09885135d4bbc6687..deced41b12f42e1217f5561c917b326fb0452de3`
  нашла 145 changed files, 32 документационных исключения,
  `diff_has_docs=false`, `diff_has_runtime_code=true` и
  `documentation_only=false`.
- `JAZZ-DISCORD-002-AC-002`: `PASS` — Node regression проверяет prompt;
  инструкция описывает implementation diff как добавленный в `main` и
  отдельно запрещает утверждать наличие опубликованного релиза.
- `JAZZ-DISCORD-002-AC-003`: `PASS` — dry-run тест подтверждает docs-only
  prefilter до OpenAI fallback.
- `JAZZ-DISCORD-002-AC-004`: `PASS` — dry-run с `[discord]` создаёт
  документационный fallback без выводов о реализации.
- `JAZZ-DISCORD-002-AC-005`: `PASS` — temp-repository тест с
  `[discord implemented]` включает docs diff и устанавливает explicit flag.
- `JAZZ-DISCORD-002-AC-006`: `PASS` — unit test подтверждает приоритет
  `[skip discord]` над `[discord]` и `[discord implemented]`.
- `JAZZ-DISCORD-002-AC-007`: `PASS` — fallback/payload tests подтверждают
  отсутствие автоматического «в разработке» и секции «За кулисами».
- `JAZZ-DISCORD-002-AC-008`: `PASS` — 21/21 Node tests, оба Node syntax
  checks, YAML parse, `git diff --check`, documentation audit и
  CommonLib 1.11 HEAD `1adf9f232680d3b011248d180fd0ad1e609a8e2c`.
- Требования `JAZZ-DISCORD-002-REQ-001`–`JAZZ-DISCORD-002-REQ-007`:
  `PASS` — реализованы в declared write set; generated data и runtime JA3
  не затронуты.

## Documentation delta

- Обновлена `docs/technical/systems/discord-player-updates.md`: источники
  evidence, новые маркеры, prompt и fallback.
- Обновлён Discord-раздел `docs/technical/testing.md`: docs-only,
  `[discord]`, `[discord implemented]` и приоритет `[skip discord]`.
- Wiki не меняется: это внутренняя семантика developer automation без нового
  игрового поведения.
