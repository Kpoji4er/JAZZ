# Техническая документация JAZZ

Раздел ориентирован на разработку, диагностику и совместимость.

## Единый словарь терминов

- [Глоссарий терминов](../glossary.md)

## Сводные документы

- [Архитектура](architecture.md) — пакеты, зависимости, загрузка и источники данных.
- [Разработка](development.md) — Mod Editor, исходники и рабочий процесс.
- [Параллельная работа агентов](multi-agent-development.md) — coordinator, worktrees, write sets и review packet.
- [Синхронизация generated data](generated-data-sync.md) — транзакция `items.lua`, `metadata.lua` и companion Lua.
- [Справочник модулей](code-reference.md) — назначение основных Lua-файлов.
- [Матрица vanilla/CommonLib/JAZZ](override-matrix.md) — прямые переопределения и риски.
- [Совместимость](compatibility.md) — версии, зависимости, saves, network и ограничения.
- [Тестирование](testing.md) — статические, editor и игровые проверки.
- [Debug и читы](debug.md) — консоль, satellite-телепорт, боевые и стратегические читы для разработки.
- [Канонический каталог оружия](weapons/README.md) — тиры, характеристики, компоненты, CSV-схема и правила синхронизации.
- [Целевая модель стрельбы и точности](weapons/accuracy-model.md) — принятый контракт навыков, дистанции, множителей, отдачи, оптики и UI.
- [Роли классов оружия](weapons/class-roles.md) — назначение одиннадцати классов, их компромиссы и контракт будущих перковых действий.
- [Стрелковые Combat Actions](weapons/combat-actions.md) — связь оружия, классов, перков и компонентов с фактическим поведением каждого действия.
- [Релизы и версионирование](systems/release-versioning.md) — версия из committed metadata, manifest четырех repos, packaging и GitHub Releases.
- [Сводки изменений в Discord](systems/discord-player-updates.md) — GitHub Actions, OpenAI Structured Outputs, фильтрация diff и безопасный Discord webhook.
- [Технический долг](technical-debt.md) — результаты аудита и безопасный план рефакторинга.

## Подробный каталог систем

- [Оглавление систем](systems/README.md);
- [полное покрытие Code-файлов](systems/file-coverage.md).

Системные страницы содержат вклад установленной vanilla, последней CommonLib и JAZZ, implementation files, load-state, data model, runtime flow, риски и validation checklist.

## Граница specs и current state

Technical-раздел отвечает на «что и где фактически реализовано». Утверждённое, но ещё не загруженное поведение находится в [`../specs/`](../specs/README.md) и не смешивается с current-state описанием.
CommonLib всегда проверяется по текущему upstream `main`; version/build/commit в документах — датированный снимок аудита, не pin зависимости.

