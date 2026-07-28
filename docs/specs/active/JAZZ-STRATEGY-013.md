---
id: JAZZ-STRATEGY-013
status: implemented
owner: project-owner
systems:
  - legion-global-ai
repositories:
  - jazz
risk: high
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-013.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/Code/Regions_Sectors.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/Strings.csv
  - jazz/Localization/EnglishManual.csv
  - jazz/Localization/RussianManual.csv
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/docs/technical/testing.md
  - jazz/docs/technical/debug.md
exclusive_resources:
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-013: persistent squads, mission-budget rest, patrol dwell

## Проблема

Managed отряды (tax/recruiter/logistics и частично combat) после миссии **удаляются**. Idle не усиливает гарнизоны. Патруль пролетает сектора без стоянки. Нет обязательного отдыха на базе после лимита приказов.

## Цели

- Happy-path **без RemoveSquad**; retire только при living == 0 (или abort spawn).
- После исчерпания `missions_left` → return home → **rest 12–36h** (heal+top-up) для всех ролей **кроме garrison** → refresh budget → `ready_for_orders`.
- Idle / recon-QRF garrison assist **только если нечего делать** по своей роли (после rest).
- Patrol: dwell **6–24h** в каждом секторе маршрута.
- Reuse idle same-role under caps (tax/recruiter/supply/shipment/manpower).

## Non-goals

- Merge юнитов / смена role на garrison.
- Rest для garrison.
- Снятие role caps.
- Militia training.

## Locked defaults

- `BaseRestMin`/`BaseRestMax` = 12h/36h.
- `PatrolSectorDwellMin`/`PatrolSectorDwellMax` = 6h/24h.
- Duration via InteractionRand.
- Tax/recruiter/logistics: один circuit/convoy = один «заказ» (budget 1) → return → rest.

## Требования

- `JAZZ-STRATEGY-013-REQ-001` — no despawn on mission complete; empty-only retire.
- `JAZZ-STRATEGY-013-REQ-002` — budget exhausted → return → rest (non-garrison) → refresh missions.
- `JAZZ-STRATEGY-013-REQ-003` — assign: primary → recon/QRF assist → idle; never interrupt resting/en_route/working.
- `JAZZ-STRATEGY-013-REQ-004` — patrol path dwell 6–24h per sector.
- `JAZZ-STRATEGY-013-REQ-005` — reuse idle same-role before new spawn under caps.
- `JAZZ-STRATEGY-013-REQ-007` — routes prefer `land_only`; water (`land_water_boatless`) only if no land path; exception: supply/shipment/manpower Major convoys.

## Инварианты и ограничения

- Caps still limit living managed squads.
- Deterministic InteractionRand contexts.
- Schema stays v3 (new squad_state fields `resting`/`rest_until`/`path` are additive).

## Acceptance criteria

- `JAZZ-STRATEGY-013-AC-001` — static: tax/recruiter/logistics success path parks/rests, no RemoveSquad.
- `JAZZ-STRATEGY-013-AC-002` — static: budget→rest→refresh for non-garrison.
- `JAZZ-STRATEGY-013-AC-003` — static: patrol path+hold dwell.
- `JAZZ-STRATEGY-013-AC-004` — static: recon/QRF assist only when primary request empty.
- `JAZZ-STRATEGY-013-AC-005` — loc/docs.
- `JAZZ-STRATEGY-013-AC-006` — runtime: `BLOCKED`.

## Impact и совместимость

- Saves: additive state fields; old retiring saves just stop retiring.
- Network: InteractionRand for rest/dwell.
- Generated data: none (Region props via undefine/extend).

## План и ownership

1. Owner request 28 July 2026 (no-despawn, rest, patrol dwell, assist).
2. Implement + docs.
3. Owner runtime smoke.

## Решение владельца

28 июля 2026 — отряды не деспавнятся; после лимита приказов отдых на базе; патруль задерживается в секторах; recon/QRF idle могут усиливать гарнизон.

## Evidence

- `JAZZ-STRATEGY-013-AC-001`: `PASS (static)` — tax/recruiter/logistics/shipment ConflictEnd park via `lBeginBaseRest` / `lBeginReturn`; no happy-path RemoveSquad
- `JAZZ-STRATEGY-013-AC-002`: `PASS (static)` — `missions_left<=0` → return → `resting` 12–36h → `lFinishBaseRest` refresh; garrison skips timer
- `JAZZ-STRATEGY-013-AC-003`: `PASS (static)` — patrol `task.path` + `patrol_dwell` hold 6–24h per sector
- `JAZZ-STRATEGY-013-AC-004`: `PASS (static)` — `lAssignReadySquads` primary then `lIdleAssistRequest` for recon/QRF
- `JAZZ-STRATEGY-013-AC-005`: `PASS (static)` — loc 644–646 RU/EN + strategy/wiki/roadmap/testing
- `JAZZ-STRATEGY-013-AC-006`: `BLOCKED (runtime)` — owner smoke

## Documentation delta

- strategy-squads-sectors, wiki, roadmap, testing
