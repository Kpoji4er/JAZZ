# V-AI-GC-001 — Temporary allocations in AI hot loops

| Field | Value |
| --- | --- |
| Severity | P2 — Medium (GC spikes during enemy turns) |
| CommonLib | **Not fixed** |
| Vanilla path | `AIPrecalcDamageScore` (`point(ux,uy,uz)` per dest); `CombatPath:new()`; `Cover.lua` `GetCoversAt` (~96–109); policy `table.ifilter` |
| Frequency | Per AI think / movement avatar cover |

## Problem

AI scoring allocates temporary Lua `point` wrappers, new `CombatPath` objects, and cover tables inside tight loops, producing GC spikes on large fights.

## Why CommonLib does not cover it

No shared scratch buffers or packed-position-only rewrite of these vanilla AI helpers in CommonLib.

## Suggested vanilla / engine fix

- Prefer packed positions only in LoF/score loops.
- Recycle policy filter tables and cover scratch buffers.
- Prefer `GetCoverTypes` / non-allocating cover queries where possible.

## Mod notes

Partial relief is possible inside mod overrides that already own the loop; must not change RNG call counts or hashes.
