---
id: JAZZ-AI-CTX-001
status: approved
owner: project-owner
systems: [tactical-ai]
repositories: [jazz]
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-CTX-001.md
  - jazz/Code/AIContextProfiles.lua
  - jazz/Code/CombatAI.lua
  - jazz/metadata.lua
  - jazz/items.lua
exclusive_resources: [none]
related_decisions: [docs/design/tactical-ai-archetypes.md]
approved_by: project-owner
---

# JAZZ-AI-CTX-001: Urban + LowVis context profiles

## Проблема

Архетипы не меняют доктрину в городе / Night / Fog (F7/F12).

## Цели

- `JazzAI_ResolveContextProfile` + apply в AICreateContext; Night≠Fog; Urban indoor/City heuristic.

## Non-goals

- New archetype IDs; flare for Fog.

## Требования

- `JAZZ-AI-CTX-001-REQ-001` — profile on context.jazz_profile.
- `JAZZ-AI-CTX-001-REQ-002` — Night SniperHold; Fog NoFlareWait + OverwatchMinScore.
- `JAZZ-AI-CTX-001-REQ-003` — Urban TakeCoverMul↑.

## Инварианты и ограничения

- Не ломать EffectiveRange clamp.

## Acceptance criteria

- `JAZZ-AI-CTX-001-AC-001` — static AIContextProfiles.lua + metadata/items code entry.
- `JAZZ-AI-CTX-001-AC-002` — static CombatAI applies profile.
- `JAZZ-AI-CTX-001-AC-003` — runtime Night vs Fog.

## Impact и совместимость

- jazz only Code.

## План и ownership

- jazz; agent; project-owner.

## Решение владельца

- approved 2026-07-29.

## Evidence

- `JAZZ-AI-CTX-001-AC-001`: `PASS`
- `JAZZ-AI-CTX-001-AC-002`: `PASS`
- `JAZZ-AI-CTX-001-AC-003`: `BLOCKED`

## Documentation delta

- ai-awareness.md, playtest CTX.
