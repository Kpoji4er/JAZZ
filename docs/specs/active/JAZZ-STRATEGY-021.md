---
id: JAZZ-STRATEGY-021
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
  - jazz/docs/specs/active/JAZZ-STRATEGY-021.md
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Code/Regions_Sectors.lua
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/wiki/grand-chien-map.md
  - jazz/docs/showcase/ru/grand-chien-map.md
  - jazz/docs/showcase/en/grand-chien-map.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz-maps/items.lua
  - jazz-nomaps/Code/NoMaps_Autonomy.lua
exclusive_resources:
  - ModItemRegion:GreatDesert
  - ModItemRegion:PortCacaoEnvirons
  - ModItemSector:E10
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-021: GreatDesert region + mainland late-awaken + Major need priority

## Проблема

На maps нужны ещё managed-регионы материка, но до Legion tier **T2-1** (`JAZZ_Legion_Tier` ≥ **21**) они не должны жить как полный Эрни-пилот: слишком рано заполняют карту. Major также должен кормить **самые бедные** аванпосты, а не случайные.

## Цели

1. Region **`GreatDesert`** («Великая Пустыня»), outpost **E10**, Major HQ **B28**, сектора по brief (A1–A12 / B4–B12 / C6–C12 / D7–D12 / E10 / …; западная полоса A9–A12… **не** у Горной Степи / Пантагрюэля — owner fix 2026-08-05).
2. Regions с `LateAwakenMinTier=21` (`PortCacaoEnvirons`, `GreatDesert`) до tier 21:
   - экономика ($/recruits/mine pulse) **÷10**;
   - combat spawn gate **×10** (редко, но заказывают);
   - **без QRF**;
   - `StartingSupply=0`, `StartingManpower=0` (хватит на tax escort; combat без пула);
   - **recruiter** только после первой поставки Major (`supply` или inbound `manpower`).
3. Major supply/manpower: среди нуждающихся аванпостов выбирать **с наименьшим $** (manpower inbound: `manpower==0`, tie-break по $ затем sector id).

## Non-goals

- Менять ErnieIsland / tier formula.
- Авто-регионы NoMaps.
- Баланс размеров отрядов материка.

## Требования

- `JAZZ-STRATEGY-021-REQ-001` — `GreatDesert` Region + E10 Global AI role lists (оба представления maps).
- `JAZZ-STRATEGY-021-REQ-002` — `LateAwakenMinTier` на Region; PortCacao + GreatDesert = 21; dormant ÷10 economy, ×10 spawn gate, no QRF.
- `JAZZ-STRATEGY-021-REQ-003` — StartingSupply/Manpower 0 на late-awaken regions; recruiter gated by `outpost.major_delivery_done`.
- `JAZZ-STRATEGY-021-REQ-004` — Major supply/manpower neediest-first across all managed outposts.
- `JAZZ-STRATEGY-021-REQ-005` — NoMaps disables `GreatDesert` with other maps-only regions.

## Инварианты

- ErnieIsland без LateAwaken (всегда awake).
- Sector IDs без zero-pad; E10 входит в `Sectors`.
- Deterministic ties: lower sector id wins.

## Acceptance criteria

- `JAZZ-STRATEGY-021-AC-001` — static: GreatDesert preset + metadata + E10 lists.
- `JAZZ-STRATEGY-021-AC-002` — static: dormant helpers + LateAwakenMinTier=21 on both mainland regions.
- `JAZZ-STRATEGY-021-AC-003` — static: neediest supply/manpower gates in lTry*.
- `JAZZ-STRATEGY-021-AC-004` — runtime/human: until tier 21 mainland outposts slow/rare/no QRF; after 21 full. `BLOCKED` until playtest.

## Impact

- Saves: **new game recommended** for StartingSupply=0 bootstrap.
- Cross-package: jazz Region/runtime; jazz-maps E10; jazz-nomaps disable.

## Решение владельца

- Статус: **approved** (owner brief 2026-08-05)

## Evidence

- `JAZZ-STRATEGY-021-AC-001`: `PASS (static)` — `GreatDesert` in items/metadata; E10 role lists both maps representations.
- `JAZZ-STRATEGY-021-AC-002`: `PASS (static)` — `LateAwakenMinTier=21`, StartingSupply/Manpower=0 on PortCacao+GreatDesert; dormant ÷10 / ×10 gate / no QRF in Guardpost_Patrols.
- `JAZZ-STRATEGY-021-AC-003`: `PASS (static)` — neediest supply/manpower + major_delivery_done recruiter gate.
- `JAZZ-STRATEGY-021-AC-004`: `BLOCKED` — human playtest until/after tier 21.

## Documentation delta

- strategy-squads-sectors, maps catalog, compatibility, wiki/showcase, roadmap, tools README.
