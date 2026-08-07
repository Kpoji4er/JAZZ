---
id: JAZZ-ECON-001
status: draft
owner: project-owner
systems:
  - sector-operations
  - economy
  - perks
repositories:
  - jazz
risk: low
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-ECON-001.md
  - jazz/docs/design/economy-ops-and-trade.md
  - jazz/CharacterEffect/InnerInfo_JAZZ.lua
  - jazz/Code/System_SectorOperations.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/English.csv
  - jazz/Russian.csv
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/systems/file-coverage.md
exclusive_resources:
  - localization ID range (new op strings)
  - ModItemSectorOperation id for Livewire city income
related_decisions:
  - none
approved_by: pending
---

# JAZZ-ECON-001: Livewire city income sector operation

## Проблема

Перк `InnerInfo_JAZZ` (Livewire) обещает операцию заработка в городском секторе, но runtime отсутствует; в Description стоит «Пока недоступно». EN/RU строки перка расходятся. Игрок видит false promise.

Design backlog: [`docs/design/economy-ops-and-trade.md`](../../design/economy-ops-and-trade.md).

## Цели

- Satellite `SectorOperation`, доступная при Livewire в controlled city-секторе.
- Длительность **2** дня; ставка **~1000 $/день**; выплата **1000 × floor(days)** (complete → **2000 $**; cancel → заработанное).
- Убрать «Пока недоступно»; выровнять RU/EN Description перка.
- Задокументировать current-state в technical (+ wiki/showcase при player-facing ship).

## Non-goals

- Daily tick payout (только конец операции).
- Loyalty/heat scaling (v1 flat ~1000 $/день).
- Rothman mine op (`Jazz_Perk_Rothman`) — отдельный scope.
- Port sell-loot (ECON-002) и JA2 merchant UI (ECON-003).
- Изменение vanilla intel-реакции `OnHackIntelDsicovered`.

## Locked defaults (owner 2026-08-06)

| Параметр | Значение |
| --- | --- |
| Gate sector | `sector.City` задан и не `"none"`; сектор под контролем игрока |
| Gate unit | Livewire с `InnerInfo_JAZZ` назначена на операцию / в секторе (точный assign как у прочих personal ops — при реализации mirror ближайший vanilla/JAZZ pattern) |
| Duration | **2** дня campaign time |
| Rate | **1000** $/день (design target) |
| Payout | **1000 $ × floor(completed_days)**; полный прогон → **2000 $**; **cancel/interrupt** — та же формула за фактически отработанные целые дни (не 0) |
| Cost | только время Livewire (без Parts/Meds) |
| Cooldown | none в v1 (открыто до approve, если owner захочет) |

## Требования

- `JAZZ-ECON-001-REQ-001` — новый `SectorOperation` id (публичный, стабильный); появляется в списке ops только при gate REQ-002.
- `JAZZ-ECON-001-REQ-002` — gate: player-controlled sector с `City ~= "none"` и Livewire с перком `InnerInfo_JAZZ` доступна для assign.
- `JAZZ-ECON-001-REQ-003` — duration **2** дня; on successful complete credit **2000** $ (`1000 × 2`).
- `JAZZ-ECON-001-REQ-004` — interrupt/cancel: credit **1000 $ × floor(elapsed whole days)** (earned so far); 0 only if cancel before first whole day.
- `JAZZ-ECON-001-REQ-005` — `InnerInfo_JAZZ` Description без «Пока недоступно»; RU и EN описывают intel + city income op; CSV sync.
- `JAZZ-ECON-001-REQ-006` — combatlog / satellite log при выплате (кратко, с суммой).
- `JAZZ-ECON-001-REQ-007` — technical `strategy-squads-sectors.md` + `file-coverage.md` при новом Code file; wiki/showcase при ship.

## Инварианты и ограничения

- Не ломать vanilla/JAZZ repair/craft/medical ops.
- Не менять `GetMineIncome` / Donations / Farm формулы.
- Deterministic: fixed payout, без RNG.
- Saves: новый op id должен переживать save (preset-based); без обязательного GameVar если progress только в sector op state.
- Network: NetSyncEvent path как у существующих SectorOperation complete.

## Acceptance criteria

- `JAZZ-ECON-001-AC-001` — static: op preset + gate helpers registered; `InnerInfo_JAZZ` text updated.
- `JAZZ-ECON-001-AC-002` — editor: ModItemSectorOperation loads; loc IDs balanced RU/EN.
- `JAZZ-ECON-001-AC-003` — runtime: Livewire in player city sector → op visible; after 2 days → +2000 $; non-city / no Livewire → op hidden or disabled.
- `JAZZ-ECON-001-AC-004` — runtime: cancel after ≥1 whole day → credit **1000 × floor(days)**; cancel before day 1 → **0**; complete → **2000**.
- `JAZZ-ECON-001-AC-005` — human: Description перка без «недоступно»; EN/RU согласованы.
- `JAZZ-ECON-001-AC-006` — docs: technical (+ wiki/showcase on ship) match runtime.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: additive SectorOperation + perk text; intel reaction unchanged.
- Saves: old saves without op progress OK; mid-op cancel on mod remove — standard.
- Network/determinism: fixed credit.
- Generated data: `items.lua` / `metadata.lua` / CharacterEffect companion.
- Cross-package: none (Livewire vanilla unit id in jazz CharacterEffect override).
- Rollback: remove op preset + restore «недоступно» text if needed.

## План и ownership

- Пакет-владелец: `jazz`
- Declared write set: frontmatter `write_set`
- Exclusive: new SectorOperation id + loc range
- Validation: Ready before implement; Done with runtime AC-003..004

## Решение владельца

- Статус: **draft**
- Locked payout: **1000 $/день**; complete → **2000 $**; **cancel → earned so far** (`1000 × floor(days)`) (2026-08-06)
- До `approved`: нужен ли cooldown / loyalty / heat

## Evidence

- `JAZZ-ECON-001-AC-001`…`006`: `BLOCKED` — not implemented

## Documentation delta

- Design: `docs/design/economy-ops-and-trade.md`
- On ship: `docs/technical/systems/strategy-squads-sectors.md`, `file-coverage.md`, player wiki/showcase (perk/ops)
