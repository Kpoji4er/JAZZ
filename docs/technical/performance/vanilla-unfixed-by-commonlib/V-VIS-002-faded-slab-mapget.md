# V-VIS-002 — `IsOnFadedSlab` does `MapGetFirst` per unit

| Field | Value |
| --- | --- |
| Severity | P0 — High (ApplyVisibility / FPS) |
| CommonLib | **Not fixed** |
| Vanilla path | `Lua/Tactical/Visibility.lua` (~842–862), used from ApplyVisibility (~921–1000) |
| Frequency | Every `ApplyUnitVisibility` (selection, combat apply, exploration apply) |

## Problem

```lua
local slab = uz and MapGetFirst(obj, const.SlabSizeX/2, "FloorSlab", "RoofSlab", const.efVisible,
    function(slab, uz)
        ...
    end, uz)
```

Per-unit spatial MapGet on the visual/async visibility path.

## Why CommonLib does not cover it

No faded-floor grid or replacement for `IsOnFadedSlab` in CommonLib.

## Suggested vanilla / engine fix

- Maintain a faded-floor voxel/grid cache.
- Query the grid instead of `MapGetFirst` per unit.

## Mod notes

Presentation-only if limited to highlight/fade visuals. Do not touch sync visibility tables from a mod patch.
