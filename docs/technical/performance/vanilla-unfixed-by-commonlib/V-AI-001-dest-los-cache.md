# V-AI-001 — `AIUpdateDestLosCache` dest × enemy LOS

| Field | Value |
| --- | --- |
| Severity | P0 — Critical (AI turn time) |
| CommonLib | **Not fixed** — no override / shortlist of this path |
| Vanilla path | `Lua/Tactical/CombatAI.lua` (~862–970) |
| Frequency | Once per aware AI unit at turn start (`StartAI` → `AICreateContext`) |

## Problem

Builds LOS from destinations to enemies with batched `CheckLOS` (batch size 100) and `Sleep(10)` yields. On maps with many reachable voxels and several enemies this dominates enemy-turn latency.

```lua
-- pattern
local max_los_checks = 100
...
local los_any, los_data = CheckLOS(targets, srcs, sight)
...
Sleep(10) -- yield
```

## Why CommonLib does not cover it

CommonLib `FixAI.lua` changes suspicion / action selection / RunAndGun, not destination LOS cache construction or batching.

## Suggested vanilla / engine fix

- Keep a global dest→any-enemy LOS bit, but skip enemies outside weapon/sight radius.
- Replace repeated `table.remove` compaction with a bitset or single rebuild pass.
- Raise batch size / reduce yields when the frame budget allows.
- Prefer spatial shortlists over full `all_destinations × enemies`.

## Mod notes

JAZZ `JAZZ-AI-PERF-001` (`CombatAI.lua`):
- **Enemy list:** full `context.enemies` (sorted by `handle`) — range enemy shortlist rolled back for smarter LOS.
- **Far-skip:** dest farther than sight (2D) from all enemies → cache `false`, no `CheckLOS`.
- **Dest-cap:** at most `JAZZ_AI_PERF_DESTLOS_CAP` (320) CheckLOS dests — prefer stay / `important_dests` / `destinations`, then nearest to unit; remainder stay `false`.
- Batching + `Sleep(10)` kept. Gated log: `config.JAZZ_AIPerfLog` → `[JAZZ-AI-PERF] DestLos ... capped=N`.
