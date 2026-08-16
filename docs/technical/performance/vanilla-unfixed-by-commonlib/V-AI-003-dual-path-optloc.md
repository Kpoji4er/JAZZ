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
- Gated log: `config.JAZZ_AIPerfLog` → `[JAZZ-AI-PERF] EnumDests ...` / `OptLoc ...` / **`RebuildPaths ...`**.
- **PERF-003 (2026-08-15):** AI-only `CombatPath:RebuildPaths` sets `restrict_area` to an AP-reach bbox (`margin` 8 tiles, hard cap 64) so `GetCombatPathPositions` does not flood a 513×513 map. `Unit:StartAI` yields `Sleep(1)` only on `IsGameTimeThread()` (not inside `RebuildPaths` — LoadGame UI pathing). Dual stance RebuildPaths when MoveStance ≠ PrefStance remains. OptLoc **radius** unchanged (sniper rooftops / PERF-002).
- **PERF-003 Dump hang (2026-08-16):** M3 freeze continued **after** cheap RebuildPaths: Dump `AIPrecalcDamageScore` dests=1, then `AIChooseSignatureAction` → `AIPickScoutLocation` `ForEachPassSlab` at **`80 * guim`** (vanilla **`5 * guim`**) plus scout-scan on every grenade/cone Precalc even when enemies already filled target points. Radius restored; AOE scout only if the point pool is empty. Gated logs: `SigPrecalc`, `ScoutLoc`.
- **PERF-003 Dump execute (2026-08-16):** After scout fix, M3 Dump PickBest hung in `AIGetAttackTargetingOptions` → `GetActionResults` → `PrepareAttackArgs` `GetLoFData` on one body-part ray (waterfall). Targeting now uses `CalcChanceToHit`. Dump execute (`jazz_ai_dump`) skips PrepareAttackArgs/GetAttackResults GetLoFData and vegetation `Collide`. Player firearms keep vanilla execute. OptLoc **radius** unchanged.
- Changing OptLoc **radius** presets or EndTurn policies remains sync-/behavior-sensitive and is out of this cap.
