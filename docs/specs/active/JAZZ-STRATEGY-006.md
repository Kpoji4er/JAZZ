---
id: JAZZ-STRATEGY-006
status: implemented
owner: project-owner
systems:
  - legion-global-ai
  - satellite-ui
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-006.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/Code/Regions_Sectors.lua
  - jazz/Localization/Strings.csv
  - jazz/Localization/EnglishManual.csv
  - jazz/Localization/RussianManual.csv
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
exclusive_resources:
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-006: money ledger ($) + cargo $ in task UI

## Проблема

STRATEGY-003 использует abstract `supply`/`reserve`. Roadmap п.0 требует единый ledger в реальных `$` с якорем full expensive garrison ≈ outpost capacity ≈ 10×$12000. Task rollover supply/shipment не показывает сумму груза.

## Цели

- `outpost.money` / `major.money` в `$` с roadmap caps/rates/costs.
- Schema v1→v2: старые abstract пулы **сбрасываются** на starting `$` (не scale).
- `diamond_stock` хранит `$` к shipment; порог/cargo = $12000.
- Flat role costs остаются, но в `$`.
- Task UI supply/shipment показывает `$` из `payload.money`.

## Non-goals

- Tax collector / local POI stock (7a).
- Per-unit spawn costs / generator (004/005).
- Произвольные TinyDiamonds-остатки в inventory (v1: один DiamondBriefcase на shipment).
- п.2–4 reinforce/retribution/patrol.

## Целевые defaults ($)

| Параметр | Property ID (сохранён) | Default |
|---|---|---:|
| Outpost start | StartingSupply | 12000 |
| Outpost capacity | SupplyCapacity | 120000 |
| Major start | MajorStartingReserve | 120000 |
| Major capacity | MajorReserveCapacity | 1200000 |
| Supply cargo | SupplyConvoyCargo | 12000 |
| Shipment threshold | DiamondShipmentThreshold | 12000 |
| Base $/h | PassiveSupplyPerHour | 0 |
| City $/h | CitySupplyBonus | 50 |
| Farm $/h | FarmSupplyBonus | 10 |
| Mine $/h → diamond_stock | MineDiamondPerHour | 250 |
| Recon/Patrol/QRF/Garrison cost | *Cost | 8000/18000/40000/120000 |
| MajorResponseCost | MajorResponseCost | 50000 |

## Требования

- `JAZZ-STRATEGY-006-REQ-001` — runtime ledger в `$`; income city/farm→money, mine→diamond_stock `$`.
- `JAZZ-STRATEGY-006-REQ-002` — schema migrate 1→2 resets pools to starting `$`.
- `JAZZ-STRATEGY-006-REQ-003` — Region property defaults/names reflect `$`; property IDs unchanged.
- `JAZZ-STRATEGY-006-REQ-004` — supply/shipment task text includes cargo `$`.
- `JAZZ-STRATEGY-006-REQ-005` — RU/EN loc updated for task strings; docs/wiki/roadmap sync.

## Инварианты и ограничения

- Need-gates и garrison pre-placed filter из 003 сохраняются.
- Supply convoy: start money ≪ 40% trigger → legal immediately; no force-spawn.
- Property IDs на Region не переименовывать.
- Не подключать `JAZZ_GetLegionUnitPrice` к spawn.

## Acceptance criteria

- `JAZZ-STRATEGY-006-AC-001` — static: money fields, defaults, no `outpost.supply` writes.
- `JAZZ-STRATEGY-006-AC-002` — static: schema migrate path 1→2.
- `JAZZ-STRATEGY-006-AC-003` — static: task strings use `<money>`; both runtime CSVs.
- `JAZZ-STRATEGY-006-AC-004` — docs/wiki/roadmap updated.
- `JAZZ-STRATEGY-006-AC-005`: `PASS (runtime/human)` — owner playtest accepted 2026-07-28.

## Impact и совместимость

- **Runtime:** GameVar field rename + economy scale.
- **Saves:** v1 Legion AI economy pools reset on load; squads/tasks otherwise kept.
- **Network:** no new RNG.
- **Rollback:** revert Lua/docs/loc; old saves already migrated stay on v2.

## План и ownership

1. `jazz` — spec, Regions_Sectors defaults, Guardpost_Patrols ledger+UI, loc, docs.
2. Runtime smoke — владелец.

## Решение владельца

28 июля 2026 — план money ledger migration утверждён (п.0 + $ в task UI).

## Evidence

- `JAZZ-STRATEGY-006-AC-001`: `PASS (static)` — `outpost.money`/`major.money`/`payload.money`; Region defaults in `$`; no `outpost.supply` writes.
- `JAZZ-STRATEGY-006-AC-002`: `PASS (static)` — `lMigrateSchemaToMoney` on schema < 2; pools reset to starting `$`.
- `JAZZ-STRATEGY-006-AC-003`: `PASS (static)` — task IDs 1444/1445 with `<money>`; RU/EN/manual/catalog updated.
- `JAZZ-STRATEGY-006-AC-004`: `PASS (static)` — technical, wiki, testing, roadmap.
- `JAZZ-STRATEGY-006-AC-005`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md`
- `docs/wiki/legion-global-ai.md`
- `docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md`
