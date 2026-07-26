# Шаблон системной страницы

# Название системы

## Назначение и наблюдаемый эффект

Описать, что делает текущая загруженная система и что наблюдает игрок, моддер или автор карты.

## Связанные specs и decisions

Перечислить только релевантные `JAZZ-*-NNN` и `ADR-NNNN`. Approved, но ещё не реализованные specs не описывать как current state.

## Владелец и runtime-слои

| Слой | Вклад |
| --- | --- |
| Установленная vanilla | Точные базовые функции, классы, presets или данные |
| CommonLib | Точные пересечения с подтверждённым snapshot либо отсутствие прямого пересечения |
| JAZZ | Точный вклад core/assets/maps/units |

## Файлы реализации и load-state

Указать repository-relative paths и статус: loaded, generated, dormant/unlisted, empty, inert/commented или editor-only.

## Модель данных и публичные IDs

Описать classes, properties, presets, constants, events, save fields, NetSync events и межпакетные ссылки.

## Runtime flow

Описать entry points и упорядоченный путь через hooks, state, UI и persistence.

## Правила и формулы

Фиксировать только действующие formulas, thresholds, randomness и scheduling rules. Target behavior ссылать на spec.

## Зависимости и пересечения

Описать package order, vanilla/CommonLib collisions и потребителей из соседних пакетов.

## Чек-лист проверки

Перечислить editor, tactical, strategic, UI, save/load, network и regression scenarios с требуемым уровнем evidence.

## Известные ограничения и долг

Зафиксировать dormant-файлы, generated ограничения, legacy paths и отсутствующие тесты.

## Контракт сопровождения

Назвать implementation, specs, decisions и technical docs, которые меняются вместе с системой.
