# Документационный контракт JAZZ

## Типы истины

- `docs/specs/` — утверждённые требования, DoR, acceptance criteria и evidence.
- `docs/decisions/` — долгоживущие архитектурные решения.
- `docs/technical/` — фактически загруженное текущее состояние реализации для разработчика и агента.
- `docs/wiki/` — игроковый справочник: наблюдаемое поведение, роли, способы чтения интерфейса и каталог контента без внутренних деталей реализации.
- `docs/showcase/` — двуязычная (RU/EN) публичная витрина аспектов мода; GitHub Wiki публикуется из неё (ADR-0003), а не является вторым каноном.

Разделение слоёв принято в `docs/decisions/ADR-0002-technical-and-player-docs.md` и `docs/decisions/ADR-0003-github-wiki-showcase.md`. Technical остаётся источником истины по реализации; wiki и showcase не должны спорить с ним или вручную дублировать generated weapon stats.

## Specification → implementation

Изменение поведения, архитектуры, generated data, dependencies, load order, public ID или save/network contract начинается с spec. Technical docs обновляются после реализации и не должны выдавать approved target за current runtime.

Если runtime уже разошёлся с active/accepted spec, или technical страница явно отстаёт от кода — **спросить владельца** до молчаливой правки контракта (см. `.cursor/rules/jazz-spec-sync.mdc`, `.cursor/rules/jazz-technical-docs-sync.mdc`).

## Что меняется вместе с реализацией

- Профильная `docs/technical/systems/*` — при изменении current-state поведения.
- `file-coverage.md` — при новом, удалённом, перемещённом, dormant или впервые загружаемом файле.
- `override-matrix.md` — при изменении пересечения vanilla/CommonLib/JAZZ.
- `compatibility.md` — при изменении dependency, save, network или public contract.
- `testing.md` — при изменении общего validation profile.
- Spec evidence — для каждого `AC-*`.
- Профильная `docs/wiki/*` — **обязательно**, если изменение заметно игроку (бой, CTH, grazing, укрытие, дым/погода, UI); generated weapon pages — через CSV + `scripts/docs/weapons-docs.mjs`.
- Соответствующие `docs/showcase/ru/*` и `docs/showcase/en/*` — **обязательно** вместе с wiki для того же аспекта; не спрашивать отдельно (`.cursor/rules/jazz-docs-wiki-sync.mdc`).

Не требовать изменения сводного документа, если его факт не изменился. Отсутствие documentation delta фиксировать в spec с причиной.

## Риск и подтверждение

- Разделять vanilla, CommonLib и JAZZ.
- Изменчивый dependency snapshot хранить канонически и ссылать, а не копировать.
- Указывать уровень подтверждения: static, editor, runtime или human.
- Не считать static evidence заменой runtime, если acceptance criterion требует игру или редактор.
- Для media contract использовать repository-relative paths; абсолютные локальные пути не сохранять.
