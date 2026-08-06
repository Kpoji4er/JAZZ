---
id: JAZZ-REF-002
status: implemented
owner: project-owner
systems:
  - ris-intelligence
  - ame-hiring
  - legion-tier-progression
  - pda-ui
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - Code/System_RIS_Mail.lua
  - Code/System_RIS_Combat.lua
  - Code/System_RIS_Browser.lua
  - Code/System_RIS_Content.lua
  - Code/System_AME_Browser.lua
  - Code/System_AME_Mail.lua
  - Code/System_AME_Market.lua
  - Code/LegionTierProgression.lua
  - docs/specs/active/JAZZ-REF-002.md
  - metadata.lua
exclusive_resources:
  - metadata.lua
related_decisions:
  - none
related_specs:
  - JAZZ-REF-001
  - JAZZ-UI-RIS-001
  - JAZZ-UI-AME-001
  - JAZZ-UNITS-005
approved_by: project-owner
---

# JAZZ-REF-002: Wave A — RIS / AME / LegionTier readability (implementation)

Governance: [`JAZZ-REF-001`](JAZZ-REF-001.md). Это первая кодовая волна, не big-bang по всему `Code/`.

## Проблема

Модули R.I.S. / AME и `LegionTierProgression` уже в проде и относительно спокойны по churn, но внутри есть повторяющиеся wrap-паттерны, длинные install/AAR блоки и дубли NoMaps/Maps. `JAZZ-REF-001` задал правила; этой спеке нужны concrete in-file refactors без смены поведения.

## Цели

- Упростить сопровождение RIS mail/combat/browser и AME browser/mail/market через local helpers и idempotent installs.
- Сблизить структуру NoMaps/Maps в `LegionTierProgression.lua` без сдвига tier semantics.
- Зафиксировать границу generated content в `System_RIS_Content.lua` (без правки payload).
- Behavior parity: те же письма, locks, AAR текст, market rules, tier raises.

## Non-goals

- Менять механики, формулы, пороги, delays, ID писем, тексты `T(...)`, specialist soft-guarantee, tick intervals.
- Трогать `items.lua` / CSV / карты / диалоги; `metadata.lua` меняется только обязательным revision/changelog bump коммита.
- Добавлять новый `ModItemCode` / новый загружаемый файл — только in-file local helpers.
- Править payload `System_RIS_Content.lua` (ID, strings, thresholds tables).
- Рефакторить `Guardpost_Patrols` / `CombatAI` / `AiActions` / CTH (другие волны per REF-001).

## Требования

- `JAZZ-REF-002-REQ-001` (High): В `System_RIS_Mail.lua` упростить уже существующие `lEnqueue` / `JAZZ_RIS_ProcessMailQueue` (dedupe по `key`, refresh `ready_at`, pick due): вынести pick/dispatch/constants в named local helpers; не менять политику ready time и не вводить новый public queue class.
- `JAZZ-REF-002-REQ-002` (High): В `System_RIS_Combat.lua` разбить `lBuildAARText` / `JAZZ_RIS_FinalizeBattle` на явные стадии (context → narrative blocks → persist) через local helpers; `lIntensityBand` / `lWeatherBand` оставить pure; содержимое AAR для фиксированного snap без изменений.
- `JAZZ-REF-002-REQ-003` (Medium): В `System_RIS_Browser.lua` свести template walker / host find к одному local utility block; `lInjectRisMode` — build + install; replace-on-reload preserved.
- `JAZZ-REF-002-REQ-004` (Medium): В `System_AME_Browser.lua` унифицировать install-wrap (`PDAUrl`, `DockBrowserTab`) через local `lInstallReassertWrap`; `MercCanContact` one-shot; `ModsReloaded` unwrap flow unchanged.
- `JAZZ-REF-002-REQ-005` (Medium): В `System_AME_Market.lua` единый `AME_IDS`, стадии depart/refill/specialist; thresholds без изменений.
- `JAZZ-REF-002-REQ-006` (Medium): В `System_AME_Mail.lua` shared `AME_IDS` + `lSendListingMail`; email IDs/тексты не трогать.
- `JAZZ-REF-002-REQ-007` (High): В `LegionTierProgression.lua` shared `lComputeTierSub` / `lAdvanceMajorState` / `lSubIntervalDays` для NoMaps/Maps.
- `JAZZ-REF-002-REQ-008` (Low): В `System_RIS_Content.lua` только ownership-комментарий; ноль правок payload.

## Инварианты и ограничения

- Видимый результат на тех же событиях совпадает с pre-refactor.
- Порядок `OnMsg.*` и tab lock не меняются.
- Save fields / queue item shape сохраняются.
- После `ModsReloaded` wraps без double-nest.
- Determinism mail order + AAR text as today.

### Feature freeze

Owner waiver 2026-08-06: реализация по явному запросу («Реализовывай»). Runtime smoke по AME tick / RIS PDA — human Evidence.

## Acceptance criteria

- `JAZZ-REF-002-AC-001` — REQ закрыты в коде; Evidence briefly notes before/after.
- `JAZZ-REF-002-AC-002` — RIS mail: due by `ready_at`; key dedupe + ready_at refresh; delays unchanged.
- `JAZZ-REF-002-AC-003` — RIS combat stages readable; AAR parity for fixed snap.
- `JAZZ-REF-002-AC-004` — RIS/AME browser: ModsReloaded без double-wrap.
- `JAZZ-REF-002-AC-005` — AME market behavior parity.
- `JAZZ-REF-002-AC-006` — LegionTier NoMaps/Maps same raises on same inputs.
- `JAZZ-REF-002-AC-007` — Evidence PASS/FAIL/BLOCKED with level.
- `JAZZ-REF-002-AC-008` — RIS Content payload unchanged (comments only).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: readability only.
- Saves: compatible.
- Network/determinism: preserved.
- Generated data: false.
- Cross-package references: existing runtime APIs only.
- Rollback/recovery: revert touched Code files.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель / Reviewer: project-owner
- Declared write set: frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: `implemented`
- Кто подтвердил: project-owner (explicit implement 2026-08-06)
- Дата: 2026-08-06
- Waiver feature freeze: yes

## Evidence

- `JAZZ-REF-002-AC-001`: `PASS` (static) — REQ-001…008 in-file helpers across write set.
- `JAZZ-REF-002-AC-002`: `PASS` (static) — `lRefreshQueuedItem` / `lPickDueIndex` / `lDispatchOne` / `lBumpDispatch`; constants unchanged.
- `JAZZ-REF-002-AC-003`: `PASS` (static) — AAR append/capture/persist split. `BLOCKED` (human) — one ConflictEnd AAR text check.
- `JAZZ-REF-002-AC-004`: `PASS` (static) — `lInstallReassertWrap` + RIS inject replace. `BLOCKED` (runtime) — ModsReloaded ×2 PDA.
- `JAZZ-REF-002-AC-005`: `PASS` (static) — same rolls/target/specialist; cached ids. `BLOCKED` (runtime) — +14d tick smoke.
- `JAZZ-REF-002-AC-006`: `PASS` (static) — shared sub/major helpers, same formulas. `BLOCKED` (runtime) — tier raise smoke.
- `JAZZ-REF-002-AC-007`: `PASS` (static) — Evidence filled; runtime gaps BLOCKED.
- `JAZZ-REF-002-AC-008`: `PASS` (static) — header comments only on `System_RIS_Content.lua`.

## Documentation delta

- No new Code load entry; file-coverage / wiki / showcase not required (behavior parity).
