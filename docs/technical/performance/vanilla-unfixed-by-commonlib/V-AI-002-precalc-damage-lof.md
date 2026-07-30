# V-AI-002 — `AIPrecalcDamageScore` full LoF matrix

| Field | Value |
| --- | --- |
| Severity | P0 — Critical (AI turn time) |
| CommonLib | **Not fixed** |
| Vanilla path | `Lua/Tactical/CombatAI.lua` (~1418–1705); callers in `AIBehaviors.lua` |
| Frequency | Each AI think over `context.destinations`; again on attack / retarget |

## Problem

For every destination with enough AP, vanilla calls `GetLoFData(unit, targets, lof_params)` for the full target list, then scores hits. This is the real cost behind “deal damage” positioning (`AIPolicyDealDamage` only reads precomputed scores).

```lua
if not is_melee then
    attacker_pos = point(ux, uy, uz)
    lof_params.step_pos = point_pack(ux, uy, uz)
    lof_params.stance = ustance
    targets_attack_data = GetLoFData(unit, targets, lof_params)
end
```

## Why CommonLib does not cover it

No CommonLib rewrite of `AIPrecalcDamageScore` or LoF reuse across destinations.

## Suggested vanilla / engine fix

- Score only reachable / shortlisted destinations.
- Reuse LoF per `(step_pos, stance)` when stance/AP band repeats.
- Early-out using Dest LOS cache before `GetLoFData`.
- Avoid rebuilding the full matrix after a simple move/retarget.

## Mod notes

JAZZ overrides this path and caches CTH aim grids used by `PickBestAttack`. That removes a secondary cost; the LoF matrix itself still follows vanilla structure and must stay net-deterministic (RNG / hashes).
