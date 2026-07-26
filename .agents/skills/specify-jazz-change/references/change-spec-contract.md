# Контракт change specification JAZZ

## Lifecycle

| Статус | Значение | Допустимое расположение |
| --- | --- | --- |
| `draft` | Требования обсуждаются, реализация не начинается | `docs/specs/active/` |
| `approved` | DoR пройден, реализация разрешена | `docs/specs/active/` |
| `implemented` | Реализация готова к независимому ревью | `docs/specs/active/` |
| `accepted` | DoD, ревью и human acceptance пройдены | `docs/specs/accepted/` |
| `superseded` | Контракт заменён другим spec/ADR | `docs/specs/superseded/` |

## Definition of Ready

Для `approved` обязательны:

- уникальный `id`;
- владелец решения;
- системы и репозитории;
- problem, goals и non-goals;
- минимум один `REQ-*` и один `AC-*`;
- инварианты и ограничения;
- compatibility impact;
- declared write set;
- exclusive resources либо явное `none`;
- требуемый уровень validation;
- отсутствие `TBD`, `TODO` и открытых архитектурных вопросов;
- подтверждение владельца проекта.

## Definition of Done

Для `implemented` и `accepted` обязательны:

- каждый `REQ-*` реализован либо явно отклонён новой ревизией spec;
- каждый `AC-*` имеет evidence;
- фактический diff не выходит за declared write set;
- применимые static/generated/editor/runtime проверки выполнены;
- technical current-state docs синхронизированы с реализацией;
- cross-repo изменение фиксирует связанные SHA или явно помечено как незакоммиченное;
- независимый reviewer не обнаружил незакрытого расхождения со spec;
- для `accepted` отсутствуют `FAIL` и `BLOCKED`.

## Правила ID

- Spec: `JAZZ-<SYSTEM>-NNN`.
- Requirement: `<SPEC-ID>-REQ-NNN`.
- Acceptance criterion: `<SPEC-ID>-AC-NNN`.
- ADR: `ADR-NNNN`.

ID не переиспользовать после публикации или supersede.
