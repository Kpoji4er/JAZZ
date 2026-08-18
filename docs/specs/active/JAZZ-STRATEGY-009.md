---
id: JAZZ-STRATEGY-009
status: implemented
owner: project-owner
systems:
  - legion-global-ai
  - satellite-ui
repositories:
  - jazz
risk: high
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-009.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/Code/Regions_Sectors.lua
  - jazz/Code/LegionSquadComposition.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/Strings.csv
  - jazz/Localization/EnglishManual.csv
  - jazz/Localization/RussianManual.csv
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/docs/technical/testing.md
exclusive_resources:
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
related_specs:
  - JAZZ-STRATEGY-016
approved_by: project-owner
---

# JAZZ-STRATEGY-009: tax collector role ($ from POI)

## Проблема

Roadmap 7a: city/farm `$` сейчас льются прямо в `outpost.money`. Нужен tax collector, который обходит POI и доставляет `$` на аванпост.

## Цели

- City/farm `$` копятся в `region_state.poi_money[sector_id]` (Legion-owned economic POI only) пульсом `POIGenerationInterval` (**96h**, STRATEGY-016; было 72h в этом spec).
- Mine `$` остаются в `outpost.diamond_stock` (shipment), не через tax.
- Role `tax`: icon TAX; cap 1; threshold sum ≥ $1000; cooldown **48h** (STRATEGY-016; было 24h); circuit all taxed sectors then unload at outpost.
- Task UI shows cargo `$`.
- Recipe allow-list for tax (escort band).

## Non-goals

- Manpower/recruiter (010).
- Player militia (011).
- Changing mine→shipment path.
- jazz-units new EnemySquad (reuse SupplySquads / TaxSquads fallback).

## Locked defaults

- TaxCap=1, TaxThreshold=1000, TaxCooldown=**48h** (016; было 24h), TaxCargoMax=12000 (runtime cargo × economy scale).
- POI pulse: city $2500 / farm $800; `PoiMoneyCap`=12000; interval **96h** (016; было 72h); catch-up max 1 cycle.
- TaxSquads Region list falls back to SupplySquads.
- Spawn cost: $0 unit charge (logistics); cargo only.

## Требования

- `JAZZ-STRATEGY-009-REQ-001` — city/farm income → poi_money, not direct outpost.
- `JAZZ-STRATEGY-009-REQ-002` — tax spawn gates: sum≥1000, cap, cooldown, Legion outpost.
- `JAZZ-STRATEGY-009-REQ-003` — circuit collects then delivers to outpost.money (clamped).
- `JAZZ-STRATEGY-009-REQ-004` — TAX icon + localized task texts RU/EN.
- `JAZZ-STRATEGY-009-REQ-005` — docs/wiki/roadmap.

## Инварианты и ограничения

- Schema: `poi_money` additive on region_state (introduced under v2; current Legion AI schema is **v3** after 010).
- Supply/shipment unchanged.
- Need-gates for combat roles unchanged.

## Acceptance criteria

- `JAZZ-STRATEGY-009-AC-001` — static: income path + tax role wiring.
- `JAZZ-STRATEGY-009-AC-002` — static: caps/threshold/cooldown.
- `JAZZ-STRATEGY-009-AC-003` — loc RU/EN complete.
- `JAZZ-STRATEGY-009-AC-004` — docs.
- `JAZZ-STRATEGY-009-AC-005`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`

## Impact и совместимость

- Outpost money grows slower until tax delivers (intentional).
- Existing saves: poi_money starts empty; city/farm stop direct fill after load.

## План и ownership

1. Spec approved via overnight Global AI completion order.
2. Implement tax income path + role.
3. Owner runtime smoke.

## Решение владельца

28 июля 2026 — overnight completion of Global AI roadmap 7a.
2026-08-18: cadence **superseded** [JAZZ-STRATEGY-016](JAZZ-STRATEGY-016.md) — `POIGenerationInterval` **96h**, `TaxCooldown` **48h**. Tax role/path unchanged. Не путать с STRATEGY-019 `logistics_open_at` (+72h на новый аванпост).

## Evidence

- `JAZZ-STRATEGY-009-AC-001`..`004`: static PASS — TaxCap default 1; city/farm → `poi_money` pulse; docs sync 2026-07-29
- `JAZZ-STRATEGY-009-AC-005`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`

## Documentation delta

- strategy-squads-sectors.md, wiki, roadmap, testing
