# Техническая документация JAZZ

Раздел ориентирован на разработку, диагностику и совместимость.

Если нужен гайд по механикам для игроков, сейчас `docs/wiki` временно удалена для пересборки. До восстановления используем технические страницы как источник описания поведения.

## Единый словарь терминов

- [Глоссарий терминов](../glossary.md)

## Сводные документы

- [Архитектура](architecture.md) — пакеты, зависимости, загрузка и источники данных.
- [Разработка](development.md) — Mod Editor, исходники и рабочий процесс.
- [Синхронизация generated data](generated-data-sync.md) — транзакция `items.lua`, `metadata.lua` и companion Lua.
- [Справочник модулей](code-reference.md) — назначение основных Lua-файлов.
- [Матрица vanilla/CommonLib/JAZZ](override-matrix.md) — прямые переопределения и риски.
- [Совместимость](compatibility.md) — версии, зависимости, saves, network и ограничения.
- [Тестирование](testing.md) — статические, editor и игровые проверки.
- [Канонический каталог оружия](weapons/README.md) — тиры, характеристики, компоненты, CSV-схема и правила синхронизации.
- [Целевая модель точности](weapons/accuracy-model.md) — формулы из финальной вкладки «Пист» и открытые решения.
- [Релизы и версионирование](systems/release-versioning.md) — версия из committed metadata, manifest четырех repos, packaging и GitHub Releases.
- [Сводки изменений в Discord](systems/discord-player-updates.md) — GitHub Actions, OpenAI Structured Outputs, фильтрация diff и безопасный Discord webhook.
- [Технический долг](technical-debt.md) — результаты аудита и безопасный план рефакторинга.

## Подробный каталог систем

- [Оглавление систем](systems/README.md);
- [полное покрытие Code-файлов](systems/file-coverage.md).

Системные страницы содержат вклад установленной vanilla, последней CommonLib и JAZZ, implementation files, load-state, data model, runtime flow, риски и validation checklist.

## Контракт с игрокским слоем

Technical-раздел отвечает на «что и где реализовано».
При возращении wiki-слоя изменения, заметные игроку, дублируются туда отдельным гайдом.

CommonLib всегда проверяется по текущему upstream `main`; version/build/commit в документах — датированный снимок аудита, не pin зависимости.

