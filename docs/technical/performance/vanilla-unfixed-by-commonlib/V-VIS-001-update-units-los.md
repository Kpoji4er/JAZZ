# V-VIS-001 — `UpdateUnitsLOS` builds O(n²) `CheckLOS` pairs

| Field | Value |
| --- | --- |
| Severity | P0 — Critical (FPS / combat stalls) |
| CommonLib | **Not fixed** |
| Vanilla path | `Lua/Tactical/Visibility.lua` (~521–565), `ComputeUnitsVisibility` (~568+) |
| Frequency | Combat: every visibility invalidation; Exploration: dirty + 500 ms tick |

## Problem

Vanilla appends nearly all other units as targets for each source and runs one large `CheckLOS` batch. Comment in vanilla: *“Visibility in exploration can be a big performance hit”* (throttled to 500 ms, not structurally fixed).

```lua
for i, unit1 in ipairs(player_units) do
    table_iappend(target_units, player_units)
    ...
    table_iappend(target_units, neutral_units)
    for j = idx + 1, #target_units do
        src_units[j] = unit1
    end
end
...
local los_any, result = CheckLOS(target_units, src_units)
```

## Why CommonLib does not cover it

CommonLib does not replace `UpdateUnitsLOS` / `ComputeUnitsVisibility`. Suspicion early-outs in `FixAI.lua` are a different path.

## Suggested vanilla / engine fix

- Spatial buckets / team-side filters before building pairs.
- Incremental dirty units only.
- Reuse last LOS edges when neither endpoint moved.
- Keep exploration throttle, but reduce pair count first.

## Mod notes

**Sync-hard.** Visibility tables are heavily `NetUpdateHash`'d; wrong results break stealth and combat start. Mods should not casually override this.
