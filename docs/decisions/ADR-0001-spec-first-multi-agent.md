# ADR-0001: Spec-first и координация параллельных агентов

- Статус: принято
- Дата: 26 июля 2026 года
- Решение: владелец проекта делегировал исправление process architecture

## Контекст

JAZZ состоит из четырёх Git-репозиториев и содержит монолитные editor-generated слои. Documentation-first процесс хорошо описывал реализацию, но не требовал утверждённую specification до кода, не имел формального DoR/DoD и не предотвращал пересекающиеся изменения нескольких агентов.

## Решение

1. Контрактные изменения начинаются с `docs/specs/active/<SPEC-ID>.md`.
2. Реализация разрешена после `status: approved` и успешного DoR validator.
3. Каждый исполнитель объявляет write set; generated/editor ресурсы могут быть exclusive.
4. При работе более трёх агентов, нескольких репозиториев или generated data назначается coordinator.
5. Каждый исполнитель использует отдельный worktree/branch; общий dirty working tree не является интеграционной поверхностью.
6. Техническая документация описывает current state, а spec — target state.
7. Приёмка требует evidence для каждого `AC-*`, независимое conformance review и human acceptance там, где оно заявлено.
8. `docs/wiki` отключена и не входит в gate.

## Альтернативы

- Оставить process checklist без spec IDs: отклонено из-за отсутствия traceability.
- Использовать один общий working tree: отклонено из-за конфликтов и невозможности attribution.
- Требовать полное чтение всех docs: отклонено из-за стоимости контекста.

## Последствия

- Появляется небольшой upfront-cost на specification.
- Scope expansion становится явным и проверяемым.
- Generated changes одного пакета могут сериализоваться coordinator-ом.
- Review получает узкий packet `spec + diff + evidence`, а не полный контекст проекта.
- Существующие target-model документы мигрируют в specs постепенно, без дублирования.

## Условия пересмотра

Пересмотреть ADR после появления автоматического Mod Editor orchestration, общего suite repository или независимого transactional format вместо монолитных `items.lua`/`metadata.lua`.
