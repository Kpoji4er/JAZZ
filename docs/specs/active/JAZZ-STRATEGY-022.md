---
id: JAZZ-STRATEGY-022
status: implemented
owner: project-owner
systems:
  - legion-global-ai
  - regions
repositories:
  - jazz
  - jazz-maps
  - jazz-nomaps
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-022.md
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Code/Regions_Sectors.lua
  - jazz/Code/Guardpost_Patrols.lua
  - jazz-maps/items.lua
  - jazz-nomaps/Code/NoMaps_Autonomy.lua
exclusive_resources:
  - ModItemRegion:LaBarrier
  - ModItemSector:L15
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-022: LaBarrier region + region specializations

## Проблема

Нужен регион **Ла-Барьер** (`L15`) как коридор между джунглями/Какао/Флитауном. Материковые регионы больше не однотипны: барьер должен экспортировать патрули в соседей, держать больше гарнизонов и получать поставки Major сразу после Эрни.

## Цели

1. Region `LaBarrier` («Ла-Барьер»): сектора K9–K19, L11–L19; outpost `L15`; late-awaken 21.
2. Region props:
   - `ExportPatrolRegionIds` — патруль также по key/POI секторов указанных регионов;
   - `GarrisonCapBonus` — добавка к dynamic garrison cap;
   - `MajorSupplyPriority` — приоритет Major supply/manpower (выше = раньше; затем беднее $).
3. Authored: ErnieIsland `MajorSupplyPriority=100`; LaBarrier `80` + export `{PortCacaoEnvirons,FleatownEnvirons}` + `GarrisonCapBonus=4`, `PatrolCap=4`.

## Non-goals

- Полный doctrine DSL / faction AI.
- Управление вторым фортом L17 в том же регионе.

## Требования

- `JAZZ-STRATEGY-022-REQ-001` — LaBarrier preset + L15 Global AI lists + NoMaps disable.
- `JAZZ-STRATEGY-022-REQ-002` — patrol pool includes export region sectors.
- `JAZZ-STRATEGY-022-REQ-003` — garrison cap += GarrisonCapBonus.
- `JAZZ-STRATEGY-022-REQ-004` — Major supply/manpower sort by MajorSupplyPriority desc, then money asc.

## Acceptance criteria

- `JAZZ-STRATEGY-022-AC-001` — static: region + L15 wiring + props.
- `JAZZ-STRATEGY-022-AC-002` — static: patrol/garrison/priority helpers.
- `JAZZ-STRATEGY-022-AC-003` — runtime/human BLOCKED.

## Решение владельца

- approved 2026-08-05

## Evidence

- `JAZZ-STRATEGY-022-AC-001`: `PASS (static)` — LaBarrier + L15 lists + Ernie priority 100.
- `JAZZ-STRATEGY-022-AC-002`: `PASS (static)` — ExportPatrolRegionIds / GarrisonCapBonus / MajorSupplyPriority in runtime.
- `JAZZ-STRATEGY-022-AC-003`: `BLOCKED` — human playtest.
