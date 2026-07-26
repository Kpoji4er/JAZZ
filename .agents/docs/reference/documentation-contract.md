# Документационный контракт JAZZ

## Типы истины

- `docs/specs/` — утверждённые требования, DoR, acceptance criteria и evidence.
- `docs/decisions/` — долгоживущие архитектурные решения.
- `docs/technical/` — фактически загруженное текущее состояние реализации.

`docs/wiki/` сейчас отсутствует и не входит в Definition of Done.

## Specification → implementation

Изменение поведения, архитектуры, generated data, dependencies, load order, public ID или save/network contract начинается с spec. Technical docs обновляются после реализации и не должны выдавать approved target за current runtime.

## Что меняется вместе с реализацией

- Профильная `docs/technical/systems/*` — при изменении current-state поведения.
- `file-coverage.md` — при новом, удалённом, перемещённом, dormant или впервые загружаемом файле.
- `override-matrix.md` — при изменении пересечения vanilla/CommonLib/JAZZ.
- `compatibility.md` — при изменении dependency, save, network или public contract.
- `testing.md` — при изменении общего validation profile.
- Spec evidence — для каждого `AC-*`.

Не требовать изменения сводного документа, если его факт не изменился. Отсутствие documentation delta фиксировать в spec с причиной.

## Риск и подтверждение

- Разделять vanilla, CommonLib и JAZZ.
- Изменчивый dependency snapshot хранить канонически и ссылать, а не копировать.
- Указывать уровень подтверждения: static, editor, runtime или human.
- Не считать static evidence заменой runtime, если acceptance criterion требует игру или редактор.
- Для media contract использовать repository-relative paths; абсолютные локальные пути не сохранять.
