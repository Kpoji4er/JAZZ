# Шаблон системной страницы

# Название системы

## Назначение и эффект для игрока

Описать, что делает система и что наблюдает игрок, моддер или автор карты.

## Владелец и runtime-слои

| Слой | Вклад |
|---|---|
| Установленная vanilla | Точные базовые функции, классы, presets или данные, которые используются или заменяются |
| CommonLib | Точные пересечения с последней upstream-версией, определённой в начале задачи, или «прямое пересечение не подтверждено»; указать дату snapshot |
| JAZZ | Точный вклад core/assets/maps/units |

Упоминать официальный source repository как историческое доказательство, если он отличается от установленного source.

## Файлы реализации и load-state

Перечислить repository-relative files. Для каждого указать loaded, generated, dormant/unlisted, empty, inert/commented или editor-only.

## Модель данных и публичные IDs

Описать classes, properties, presets, ModItems, constants, events, save fields, NetSync events, sector/unit/entity/audio IDs и межпакетные ссылки.

## Runtime flow

Описать entry points и упорядоченный путь через hooks, calculations, обновление state, UI и persistence. Добавлять небольшую Mermaid-схему только тогда, когда она заметно проясняет многостадийный процесс.

## Правила и формулы

Точно указать formulas, thresholds, randomness, AP costs, изменения damage/resource и scheduling rules. Выводы, не подтверждённые напрямую, пометить как предположения.

## Зависимости и пересечения

Описать порядок пакетов, vanilla/CommonLib collisions, потребителей из соседних пакетов и поверхность совместимости со сторонними модами.

## Чек-лист проверки

Перечислить профильные editor, tactical, strategic, UI, save/load, network и regression scenarios.

## Известные ограничения и долг

Зафиксировать dormant-файлы, placeholders, duplicated definitions, ограничения generated-файлов, legacy paths, неясное происхождение и отсутствующие тесты.

## Контракт сопровождения

Назвать файлы и документы, которые должны обновляться при изменении системы.