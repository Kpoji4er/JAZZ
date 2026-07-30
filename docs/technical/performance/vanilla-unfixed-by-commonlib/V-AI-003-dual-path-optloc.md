# V-AI-003 — Dual `CombatPath:RebuildPaths` + OptLoc over all dests

| Field | Value |
| --- | --- |
| Severity | P0 — High (AI turn time) |
| CommonLib | **Not fixed** |
| Vanilla path | `Lua/Tactical/CombatAI.lua` — `AIBuildArchetypePaths` (~1009–1050), `AIEnumValidDests` / `AIFindOptimalLocation` (~1207–1315) |
| Frequency | Each AI unit think |

## Problem

AI often rebuilds two combat path graphs (move stance + preferred stance) and then scores **`context.all_destinations`** from an OptLoc slab search radius, not only AP-reachable voxels.

```lua
local move_path = CombatPath:new()
move_path:RebuildPaths(unit, ms_ap, pos, goto_stance)
...
pref_path = CombatPath:new()
pref_path:RebuildPaths(unit, ps_ap, pos, pref_stance)
```

## Why CommonLib does not cover it

CommonLib does not collapse path rebuilds or shrink OptLoc enumeration.

## Suggested vanilla / engine fix

- Single PF run when MoveStance == PrefStance (vanilla already does this partially).
- Shrink OptLoc radius under pressure.
- Score only AP-reachable voxels for end-turn positioning.

## Mod notes

JAZZ touches destination / behavior scoring; changing OptLoc radius or path counts is sync- and behavior-sensitive.
