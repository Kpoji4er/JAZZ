---
id: JAZZ-AI-ACT-001
status: approved
owner: project-owner
systems: [tactical-ai]
repositories: [jazz, jazz-units]
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-ACT-001.md
  - jazz/Code/AiActions.lua
  - jazz/Code/AiAction_ThrowFlare.lua
  - jazz/Code/CombatAI.lua
  - jazz/Code/AIContextProfiles.lua
  - jazz-units/Code/AICombatStance.lua
exclusive_resources: [none]
related_decisions: [docs/design/tactical-ai-archetypes.md]
approved_by: project-owner
---

# JAZZ-AI-ACT-001: Smoke LOS-break, anti-peek OW, flare→push

## Проблема

Smoke self-favor; OW min_score 300 редко в low-vis; нет flare→Push; peek не бустит OW.

## Цели

- Smoke zone LOS-break bonus; peek streak ≥2 → lower OW min_score; flare sets one-turn Push bias; LowVis OverwatchMinScore from profile.

## Non-goals

- New grenade items.

## Требования

- `JAZZ-AI-ACT-001-REQ-001` — smoke eval bonus in AIEvalZones when AllowedAoeTypes.smoke.
- `JAZZ-AI-ACT-001-REQ-002` — peek streak MapVar + OW min_score gate.
- `JAZZ-AI-ACT-001-REQ-003` — flare Execute sets JazzAI_FlarePushUntil; stance Push.

## Инварианты и ограничения

- Determinism; CombatStart clears MapVars.

## Acceptance criteria

- `JAZZ-AI-ACT-001-AC-001` — static smoke/OW/flare hooks.
- `JAZZ-AI-ACT-001-AC-002` — runtime/human smokes S1–S3.

## Impact и совместимость

- jazz Code + stance read of flare flag.

## План и ownership

- agent; project-owner.

## Решение владельца

- approved 2026-07-29.

## Evidence

- `JAZZ-AI-ACT-001-AC-001`: `PASS`
- `JAZZ-AI-ACT-001-AC-002`: `BLOCKED`

## Documentation delta

- playtest ACT; ai-awareness.
