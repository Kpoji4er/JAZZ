# V-UI-002 — Approach banters on every exploration visibility tick

| Field | Value |
| --- | --- |
| Severity | P1 — Medium (exploration CPU) |
| CommonLib | **Not fixed** |
| Vanilla path | `Lua/Exploration.lua` (~74–80) → `Lua/Banter.lua` `UpdateApproachBanters` (~2854–2943) |
| Frequency | Every **500 ms** in exploration |

## Problem

Exploration visibility invalidation also drives approach-banter updates: O(units × units) distance checks plus `FilterAvailableBanters`.

## Why CommonLib does not cover it

CommonLib does not throttle or spatialize approach banters.

## Suggested vanilla / engine fix

- Run banter proximity checks at 2–5 s, not every visibility tick.
- Spatial hash for approach distance.
- Keep `InteractionRand` / played-banter sync order stable if logic moves.

## Mod notes

Mostly safe if banter IDs and random-call order stay identical; otherwise multiplayer/desync risk.
