---
id: JAZZ-STRATEGY-007
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
  - jazz/docs/specs/active/JAZZ-STRATEGY-007.md
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
exclusive_resources:
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-007: convoys polish, patrol player sectors, reinforce, retribution, recon intel

## Проблема

Roadmap п.1–5 после money ledger: patrol не заходит на player Side; reinforce отсутствует; major/BASE ≠ retribution icon/контракт; recon return не показывает сектор; enemy routing нужен boatless (уже в коде); shipment только полный briefcase.

## Цели

- Enemy routes: `land_water_boatless` (уже); docs.
- Shipment valuables helper: полный рейс = DiamondBriefcase; остаток кратен TinyDiamonds@$500.
- Patrol: может в player sectors; приоритет пустым (нет player squad).
- Reinforce role + icon + cap + border trigger.
- Retribution: major response uses RETRIBUTION icon; prefers report / max player noise; distinct from QRF.
- Recon task texts name spotted sector; QRF/retribution consume reports (QRF already does).
- Role recipe allow-lists table (data only; no full generator).

## Non-goals

- Full composition generator (6c) / per-unit spawn cost wiring.
- Tax / recruiter / manpower (7).
- Player militia (7c).
- jazz-units EnemySquad preset split Poor/Full.

## Требования

- `JAZZ-STRATEGY-007-REQ-001` — Legion AI routes use `land_water_boatless`.
- `JAZZ-STRATEGY-007-REQ-002` — shipment inventory matches payload `$` (DB @12000 + TinyDiamonds @500).
- `JAZZ-STRATEGY-007-REQ-003` — patrol may target player Side; prefers no player squad.
- `JAZZ-STRATEGY-007-REQ-004` — reinforce role: icon, Region cap/cost defaults, spawn when neighbor to player, hold border key/POI.
- `JAZZ-STRATEGY-007-REQ-005` — major/retribution uses RETRIBUTION icon; targets max player noise / report.
- `JAZZ-STRATEGY-007-REQ-006` — recon return intel text includes observed sector.
- `JAZZ-STRATEGY-007-REQ-007` — `JAZZ_LegionRoleRecipes` allow-lists for core roles (data).
- `JAZZ-STRATEGY-007-REQ-008` — docs/wiki/roadmap updated; RU/EN for new strings.

## Инварианты и ограничения

- Need-gates 003 preserved for recon/qrf/garrison.
- Supply/shipment not force-spawned.
- Schema stays v2 money ledger.
- Public EnemySquad IDs unchanged.

## Acceptance criteria

- `JAZZ-STRATEGY-007-AC-001` — static: boatless in lRoutePath; docs mention it.
- `JAZZ-STRATEGY-007-AC-002` — static: valuables helper + shipment uses it.
- `JAZZ-STRATEGY-007-AC-003` — static: patrol allows player Side + empty preference.
- `JAZZ-STRATEGY-007-AC-004` — static: reinforce wired (images, caps, spawn path).
- `JAZZ-STRATEGY-007-AC-005` — static: RETRIBUTION icon; report-aware major target.
- `JAZZ-STRATEGY-007-AC-006` — static: recon return text has sector; recipes table present.
- `JAZZ-STRATEGY-007-AC-007` — docs/roadmap.
- `JAZZ-STRATEGY-007-AC-008`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`

## Impact и совместимость

- Runtime: new role reinforce; patrol/major behavior change; shipment inventory.
- Saves: new squad role strings; old saves OK.
- Loc: new/updated T IDs for reinforce + recon return.

## План и ownership

1. jazz overnight batch — owner pre-approved «делай всё, я спать».
2. Runtime smoke — owner after sleep.

## Решение владельца

28 июля 2026 — «давай сразу все, но я иду спать» = approve STRATEGY-007 scope п.1–5 + recipe data.

## Evidence

- `JAZZ-STRATEGY-007-AC-001`..`007`: static PASS (boatless; valuables helper; patrol player Side; reinforce; RETRIBUTION; recon sector text; recipes; docs/roadmap/loc)
- `JAZZ-STRATEGY-007-AC-008`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`

## Documentation delta

- strategy-squads-sectors.md, wiki, roadmap, testing notes
