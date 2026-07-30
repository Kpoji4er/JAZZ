# V-SAT-001 — `GenerateRouteDijkstra` uncached + O(n²) extract

| Field | Value |
| --- | --- |
| Severity | P1 — High (satellite FPS) |
| CommonLib | **Not fixed** |
| Vanilla path | `Lua/Satellite/SatelliteSquad.lua` (~2566–2747); UI hover `XSatelliteMap.lua` / `SatelliteTravel.lua` |
| Frequency | Sector rollover while choosing destination; squad travel, join, retreat, guardpost |

## Problem

Main Dijkstra path rebuilds unvisited sets over `gv_Sectors` and extracts the minimum with `sorted_pairs` (linear scan per extract). `GenerateRouteDijkstraSimplified` in `DiamondBriefcase.lua` already documents caches; the main path does not. Hover routing can invoke Dijkstra twice (normal + `"all"`).

```lua
local function GetMinUnvisitedPathSizeSector(unvisited, sector_path_size)
    for sector, _ in sorted_pairs(unvisited) do
        if sector_path_size[sector] < min then
            ...
```

## Why CommonLib does not cover it

CommonLib does not ship satellite route caches or a heap/bucket extract for this function.

## Suggested vanilla / engine fix

- Reuse the same caches as `GenerateRouteDijkstraSimplified` (start/end/pass_mode/side).
- Replace linear min-extract with a heap or bucket queue.
- Memoize UI preview routes; avoid double Dijkstra on hover.

## Mod notes

Real travel results are sync-sensitive. Safest mod follow-up is **UI preview memoization** only, not changing committed travel routes.
