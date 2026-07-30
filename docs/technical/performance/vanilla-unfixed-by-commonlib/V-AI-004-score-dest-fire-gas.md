# V-AI-004 — `AIScoreDest` fire/gas voxel work per destination

| Field | Value |
| --- | --- |
| Severity | P0 — High (AI turn time) |
| CommonLib | **Not fixed** |
| Vanilla path | `Lua/Tactical/CombatAI.lua` (~1135–1170); also cover loops in generated AI policies |
| Frequency | Per scored destination × policies (often hundreds of dests) |

## Problem

Each scored destination may call `GetVisualVoxels` and `AreVoxelsInFireRange` even when the map has no fire/gas volumes. Cover policies similarly query `GetCoverFrom` per enemy per dest.

```lua
local voxels, head = context.unit:GetVisualVoxels(point_pack(x, y, z), StancesList[stance_idx], visual_voxels)
if AreVoxelsInFireRange(voxels) then
```

## Why CommonLib does not cover it

No occupancy-grid cache or “map has fire/gas” early-out for AI scoring in CommonLib.

## Suggested vanilla / engine fix

- Build a fire/smoke occupancy grid once per AI phase.
- Skip `GetVisualVoxels` when no fire/gas objects exist on the map.
- Cache cover queries for `(dest, enemy_pos, stance)` within one think.

## Mod notes

Short-circuiting policies in a mod changes AI scores and multiplayer hashes; treat as behavior change, not a free perf patch.
