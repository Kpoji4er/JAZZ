---
id: JAZZ-REF-001
status: draft
owner: project-owner
systems:
  - architecture
  - maintainability
repositories:
  - jazz
risk: low
generated_data: false
runtime_validation: not-required
write_set:
  - docs/specs/active/JAZZ-REF-001.md
exclusive_resources:
  - none
related_decisions:
  - none
related_specs:
  - JAZZ-REF-002
approved_by: pending
---

# JAZZ-REF-001: Refactor governance — readability and safety (analysis only)

**Тип:** аналитика + правила внедрения. Код в этом SPEC-ID не меняется.

## Проблема

В `Code/*.lua` пакета `jazz` есть зоны с высокой когнитивной нагрузкой: длинные функции, смешение compute/side-effects, дубли условий, UI+логика в одном блоке. Это замедляет доработки и повышает риск регрессий. Нужен управляемый рефакторинг без смены игрового поведения, с узкими implementation-волнами.

## Цели

- Зафиксировать правила, приоритеты и baseline hotspots для безопасного рефакторинга.
- Снизить риск регрессий за счёт phased rollout и stop-триггеров.
- Направить кодовые правки в отдельные specs (`JAZZ-REF-002` и далее), по одной волне / узкому write set.
- Сохранить публичные ID и runtime behavior parity.

## Non-goals

- Любые правки `Code/*.lua`, `items.lua`, `metadata.lua`, локализаций, карт/диалогов в рамках этого SPEC-ID.
- Mass cleanup стиля / форматирования без привязки к конкретной волне.
- Изменение игровых механик, формул, порогов, текстов.

## Требования

- `JAZZ-REF-001-REQ-001` — вести baseline file matrix (ниже) и обновлять при появлении новых high-churn зон.
- `JAZZ-REF-001-REQ-002` — паттерны рефакторинга: early-return/guards; разрез длинных функций; compute vs apply; named locals вместо magic; extract дублей в local helpers; нормализация OnMsg install/unwrap.
- `JAZZ-REF-001-REQ-003` — приоритет P0→P3 (WSJF-like); не делать big-bang по всему `Code/`.
- `JAZZ-REF-001-REQ-004` — каждая кодовая волна = отдельный `JAZZ-REF-00x` с `write_set`, AC behavior-parity, Evidence, rollback.
- `JAZZ-REF-001-REQ-005` — первая кодовая волна: [`JAZZ-REF-002`](JAZZ-REF-002.md) (AME/RIS + LegionTier). Дальнейшие волны — отдельные specs по матрице ниже.

## Инварианты и ограничения

- Этот документ — governance. Реализация только через follow-up `JAZZ-REF-00x` со статусом `approved`.
- Одна implementation-спека = один файл или один extract-модуль (in-file helpers предпочтительнее нового `ModItemCode`, пока не доказана нужда).
- Пока на файле висит незакрытый feature-spec (`approved` с BLOCKED runtime AC или активный playtest) — рефактор этого файла заморожен, кроме явного разрешения owner.
- Stop: любой gameplay delta → откат chunk и отдельный behavior-spec.

### Приоритизация

| P | Критерий | Действие |
|---|---|---|
| P0 | Высокий churn + сложная логика + feature-конфликт | Не резать целиком; opportunistic extract только с owner; ждать паузы feature |
| P1 | Средний churn / крупные функции, feature стабилен | Отдельная REF-волна после playtest |
| P2 | Низкий churn, ясный дубль / wrap-шум | Подходит для ранних волн (см. REF-002) |
| P3 | Косметика, dormant clutter | Последняя очередь |

Категории зон: Safety-first · Complexity-high · Boundary-cleanup · Duplication.

### Baseline hotspots (`jazz/Code`, срез 2026-08-06)

Оценка: размер + ~коммиты/60д + пересечение с active feature specs. Не полный audit каждой функции.

| Файл | ~строк | Churn | Заметные узлы | Feature-конфликт | Волна |
|---|---:|---:|---|---|---|
| `Guardpost_Patrols.lua` | ~4700 | высокий | `lOnSquadArrived`, economy/heat tick | STRATEGY-*, COMPAT, HOTFIX | later (P0 freeze) |
| `System_OR_Unit.lua` | ~3300 | высокий | два `Unit:CalcChanceToHit`; `RecalcUIActions` | CTH / COMBAT / IMP | later / dead-code wave |
| `AiActions.lua` | ~2100 | высокий | `AIPrecalcDamageScore` ~500L | AI-ACT / MED / PERF | later (P0) |
| `CombatAI.lua` | ~2600 | высокий | `AICreateContext`, dest scoring | AI-SNIPER / CMD / PERF | later (P0) |
| `Systems_Medicine.lua` | ~2000 | средний | hook installers | MED-001 | after MED playtest |
| `SatelliteSquad.lua` | ~4400 | средний | reach/route/net sync | UNITS / IMP / STRATEGY | later |
| `System_OR_Weapons.lua` | ~2000 | средний | `GetAttackResults` ~870L | WEAPONS / CTH | after WEAPONS/CTH stabilize |
| `POI Extension.lua` | ~1100 | низкий | GED filter ~460L | — | candidate later wave |
| `System_RIS_*.lua` / `System_AME_*.lua` | 150–600 | низкий | mail queue, AAR, wrap installs | UI-RIS / UI-AME / UNITS-005 | Wave A → REF-002 |
| `LegionTierProgression.lua` | ~500 | средний | NoMaps/Maps dual path | COMPAT-003/008, UI-RIS | Wave A → REF-002 |

Sibling packages (`jazz-maps` / `jazz-units` / `jazz-nomaps` Code) малы относительно `jazz`; в baseline не входят, пока не появится отдельный hotspot.

### Implementation waves (roadmap)

| Wave | Spec | Scope | Статус |
|---|---|---|---|
| A | [`JAZZ-REF-002`](JAZZ-REF-002.md) | RIS mail/combat/browser, AME browser/mail/market, LegionTier; RIS content boundary only | implemented (runtime smoke pending) |
| B | (open later as `JAZZ-REF-003`) | dead / duplicate `CalcChanceToHit` в `System_OR_Unit.lua` + мелкий safe extract | not opened |
| C | (open later) | medicine hooks extract после закрытия MED runtime | not opened |
| D | (open later) | weapons `GetAttackResults` helpers после WEAPONS/CTH pause | not opened |
| E+ | (open later) | AI / Guardpost / Satellite — только в окне низкого churn | not opened |

Правило старта волны: feature-specs на write set не имеют BLOCKED runtime AC или owner явно разрешил refactor-only window.

### REQ pattern catalogue (для follow-up specs)

| ID | Паттерн | Фаза типичной волны | Риск | Stop |
|---|---|---|---|---|
| G-01 | Split large function → named steps | 1 | H | behavior drift / order-of-checks change |
| G-02 | Guard / early-return | 1 | H | changed short-circuit semantics |
| G-03 | Compute vs apply | 2 | H | new mutable state |
| G-04 | Explicit adapters | 2 | M | new public globals without need |
| G-05 | Dedupe conditions → local helper | 3 | M | helper used with different edge cases |
| G-06 | UI vs data boundary | 2 | M | tab/lock lifecycle change |
| G-07 | Rename locals only | 1 | L | public API / save field rename |
| G-08 | Pre/post invariants in review | 4 | H | skip smoke |
| G-09 | Magic → named local/const | 1 | L | numeric formula change |
| G-10 | Shared helper module | 3 | M | cross-file hard-coupling / metadata without sync |
| G-11 | Simplify collection passes | 2 | M | perf / alloc change |
| G-12 | OnMsg install/unwrap idempotent | 2 | M | double-wrap after ModsReloaded |
| G-13 | Governance / Evidence | 5 | L | — |

## Acceptance criteria

- `JAZZ-REF-001-AC-001` — в change set этого SPEC-ID нет правок игрового кода.
- `JAZZ-REF-001-AC-002` — документ содержит baseline hotspots + порядок волн + ссылку на implementation specs.
- `JAZZ-REF-001-AC-003` — для REQ-паттернов указаны риск и stop/rollback на уровне governance.
- `JAZZ-REF-001-AC-004` — зафиксирован follow-up `JAZZ-REF-002` как Wave A.
- `JAZZ-REF-001-AC-005` — описаны зависимости/freeze относительно feature-specs на тех же файлах.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: нет (docs-only).
- Saves: нет.
- Network/determinism: нет.
- Generated data: нет.
- Cross-package references: нет.
- Rollback/recovery: N/A для этого документа; у implementation waves — revert file chunk.
- Risks: R-1 extraction меняет порядок проверок; R-2 oversсope без волн; R-3 конфликт write set с feature-spec.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: project-owner
- Reviewer: project-owner
- Declared write set: только эта спека (+ согласованные ссылки в `JAZZ-REF-002`)
- Exclusive resources: none
- Definition of Ready: owner согласен с baseline matrix и Wave A = REF-002; статус можно поднять в `approved` как governance (код всё ещё запрещён); `test-change-spec.ps1 -Phase Ready` после approval.
- Definition of Done (governance): AC-001…005 закрыты Evidence; Wave A открыта в `JAZZ-REF-002`; код в рамках REF-001 не менялся.

## Решение владельца

- Статус: `draft` — ждёт approval owner как governance.
- Кто подтвердил: pending
- Дата: 2026-08-06

## Evidence

- `JAZZ-REF-001-AC-001`: `PASS` (static) — write set docs-only; код не в scope.
- `JAZZ-REF-001-AC-002`: `PASS` (static) — baseline table + waves section present.
- `JAZZ-REF-001-AC-003`: `PASS` (static) — pattern catalogue + stop column.
- `JAZZ-REF-001-AC-004`: `PASS` (static) — link to `JAZZ-REF-002.md`.
- `JAZZ-REF-001-AC-005`: `PASS` (static) — freeze rule + conflict column in matrix.

## Documentation delta

- Только `docs/specs/active/JAZZ-REF-001.md` (+ согласованные правки `JAZZ-REF-002.md`).
- `docs/technical/` / wiki / showcase не требуются (нет runtime change).
