# AI-система: что читать перед изменением

Цель playbook: быстро дать минимально достаточный набор справки для изменений, связанных с AI, CTH, tactical behavior.

## Перед правкой

1. Прочитать `.agents/docs/reference/project-scope.md`.
2. Прочитать `.agents/docs/reference/runtime-model.md`.
3. Если есть изменения сгенерированных данных, дополнительно `.agents/docs/reference/generated-data-sync.md`.

## Особые акценты для AI

- Проверить порядок загрузки и обработчики `OnMsg` в окнах, где завязано состояние AI.
- Сравнить сигнатуры/локальный diff для функций с vanilla и CommonLib.
- Не вводить non-deterministic RNG в ветки, влияющие на бой/позиции/приоритеты.
- Переносить тяжёлые обходы и оценки в срезы с минимальными областями.

## Проверка после правки

- Сигнатуры всех изменённых hooks/перегрузок.
- `docs/technical/systems/combat-cth-actions.md` и релевантные соседние страницы.
- Приоритетно: profile/replay сценарии для AI-цепочки, если есть возможность локального рантайма.

## Минимум проверок для AI-issues

- Детально: deterministic behavior при одинаковом save/seed.
- Наличие side effects по `GameVar/MapVar` и сохранения.
- Корректная реакция на reload и неустаревшие globals после `ReloadLua`.
