---
id: JAZZ-AI-POL-002
status: approved
owner: project-owner
systems: [tactical-ai]
repositories: [jazz, jazz-units]
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-POL-002.md
  - jazz/Code/AIPolicy.lua
  - jazz-units/items.lua
exclusive_resources: [jazz-units/items.lua]
related_decisions: [docs/design/tactical-ai-archetypes.md]
approved_by: project-owner
---

# JAZZ-AI-POL-002: AllyRoleAnchor + AvoidPeekVoxel

## Проблема

Нет якорей «экран снайпера / свита лидера»; peek voxels не штрафуются.

## Цели

- `AIPolicyAllyRoleAnchor` (screen/retinue) + `AIPolicyAvoidPeekVoxel`; wire Front/Assault Legion+Rebels OptLoc.

## Non-goals

- Full squad pathfinding; CTX multipliers.

## Требования

- `JAZZ-AI-POL-002-REQ-001` — DefineClass AllyRoleAnchor modes screen/retinue.
- `JAZZ-AI-POL-002-REQ-002` — AvoidPeekVoxel penalty near last_attack_pos.
- `JAZZ-AI-POL-002-REQ-003` — Wired в Frontliner/Assaulter Legion+Rebels OptLoc.

## Инварианты и ограничения

- Determinism; Append/DefineClass without Undefine TakeCover.

## Acceptance criteria

- `JAZZ-AI-POL-002-AC-001` — static classes in AIPolicy.lua.
- `JAZZ-AI-POL-002-AC-002` — static PlaceObj in four archetypes.
- `JAZZ-AI-POL-002-AC-003` — runtime/human: screen/retinue читаются.

## Impact и совместимость

- jazz Code + jazz-units presets.

## План и ownership

- jazz + jazz-units; agent; project-owner.

## Решение владельца

- approved 2026-07-29 project-owner.

## Evidence

- `JAZZ-AI-POL-002-AC-001`: `PASS`
- `JAZZ-AI-POL-002-AC-002`: `PASS`
- `JAZZ-AI-POL-002-AC-003`: `BLOCKED`

## Documentation delta

- ai-awareness.md policies table.
