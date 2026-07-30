# V-AI-005 — Emplacement assignment uses unscoped `MapGet("map")`

| Field | Value |
| --- | --- |
| Severity | P0 — Medium (team AI) |
| CommonLib | **Not fixed** |
| Vanilla path | `Lua/Tactical/CombatAI.lua` (~2501–2558) |
| Frequency | Team AI / machine-gun emplacement assignment |

## Problem

```lua
function AIAssignToEmplacements(team)
    local emplacements = MapGet("map", "MachineGunEmplacement")
```

Full-map enumeration plus path-length checks for unit×emplacement pairs, with no persistent registry.

## Why CommonLib does not cover it

CommonLib has no cached emplacement list or alternate assignment path.

## Suggested vanilla / engine fix

- Cache `MachineGunEmplacement` objects on map load / object created-destroyed.
- Prefer spatial queries or a dedicated `g_` registry over `MapGet("map", ...)`.
- Avoid `pf.PosPathLen` for every unit×emplacement when a cheaper filter exists.

## Mod notes

Safe only if assignment results stay sync-identical. Prefer caching the list without changing who gets which emplacement.
