# V-AL-001 — AmbientLife full-map sweeps on state changes

| Field | Value |
| --- | --- |
| Severity | P2 — Medium on sector enter / conflict; low in steady combat |
| CommonLib | **Not fixed** |
| Vanilla path | `Lua/AmbientLife.lua` spawn/despawn (~1965–2017), weather/conflict (~2058–2083), repulsors (~137–153) |
| Frequency | Event-driven + ~1 s repulsor pass |

## Problem

State transitions and repulsor logic use `MapForEach("map", ...)` / full-map sweeps instead of maintained marker/zone registries.

## Why CommonLib does not cover it

CommonLib map helpers are editor/tooling oriented; they do not replace AmbientLife registries.

## Suggested vanilla / engine fix

- Maintain marker/zone registries on create/destroy.
- Avoid full-map enumeration for routine spawn/despawn and repulsor ticks.

## Mod notes

Sync-sensitive for AmbientLife unit handles; patch only with identical spawn results.
