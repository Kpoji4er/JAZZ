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

JAZZ `JAZZ-AI-PERF-001` follow-up (`CombatAI.lua` / `AIPolicy.lua`):
- **`AIEnumValidDests`:** after CollapsePoints, cap to `JAZZ_AI_PERF_OPTLOC_DEST_CAP` (**200**). **PERF-002:** `JAZZ_AICapOptLocCandidates` — stay / important / destinations, then Strategy reserve (**48**: high ground / sniper-leader anchors / 8-compass farthest), then nearest threat. Hash `AIEnumValidDests_Cap` includes `strategy_kept`. DestLos/Precalc still use `JAZZ_AICapDestLosCandidates` (nearest threat).
- TakeCover far-skip of `GetCoverPercentage` was tried and **reverted** (wrong-side cover hug).
- **`AIPolicyTakeCover`:** score at most `JAZZ_AI_PERF_TAKECOVER_ENEMY_CAP` (**8**) nearest visible threats per dest (deterministic dist/handle sort) — M1 Rebel×Legion OptLoc cost cut without dropping threat-facing cover.
- Gated log: `config.JAZZ_AIPerfLog` → `[JAZZ-AI-PERF] EnumDests ...` / `OptLoc ...`.
- Changing OptLoc **radius** presets or EndTurn policies remains sync-/behavior-sensitive and is out of this cap.
