---
id: JAZZ-AI-POL-003
status: approved
owner: project-owner
systems:
  - tactical-ai
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-POL-003.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/design/tactical-ai-roles-playtest.md
  - jazz/Code/CombatAI.lua
  - jazz/Code/AIPolicy.lua
exclusive_resources:
  - none
related_decisions:
  - docs/design/tactical-ai-archetypes.md
approved_by: project-owner
---

# JAZZ-AI-POL-003: Anti-stack ally spacing

## Проблема

Vanilla dibs снимает только **точный** `ai_destination`. Несколько юнитов оценивают одну выгодную cover-позицию и встают **впритык** (соседние тайлы / та же клетка с другой stance).

## Цели

- Hard: при перечислении destinations исключать любые packed dest с тем же XYZ, что уже claimed ally `ai_destination` (stance не спасает).
- Soft: в `AIScoreDest` штраф за dest ближе `MinDist` тайлов к текущей/planned позиции союзника.
- Опциональный `AIPolicyAllySpacing` для editor/archetype tuning (тот же EvalDest).

## Non-goals

- Squad formation shapes / facing arcs.
- Melee dogpile exceptions (v1 одинаковый spacing).
- Generated archetype mass-edit.

## Требования

- `JAZZ-AI-POL-003-REQ-001` — dibs filter: same voxel XYZ as ally claimed dest removed.
- `JAZZ-AI-POL-003-REQ-002` — `JazzAI_AllySpacingScore(context, dest)` → negative; applied in `AIScoreDest` (MinDist=2, PenaltyPer=50 default).
- `JAZZ-AI-POL-003-REQ-003` — `AIPolicyAllySpacing` DefineClass mirrors soft math for Weightable use.
- `JAZZ-AI-POL-003-REQ-004` — deterministic; AllyPlannedPosition preferred when set.

## Инварианты и ограничения

- Не ломать medic bandage approach к союзнику сильнее необходимого (soft, не hard exclude радиуса 2).
- Exact claimed voxel остаётся hard exclude.

## Acceptance criteria

- `JAZZ-AI-POL-003-AC-001` — static: spacing helper + AIScoreDest call + dibs XYZ.
- `JAZZ-AI-POL-003-AC-002` — static: AIPolicyAllySpacing class exists.
- `JAZZ-AI-POL-003-AC-003` — runtime/human: два AI не занимают одну клетку; реже стоят shoulder-to-shoulder на одном cover.

## Impact и совместимость

- jazz CombatAI + AIPolicy only.

## План и ownership

- jazz; agent; project-owner.

## Решение владельца

- approved 2026-07-29 project-owner (вместе с REG-001).

## Evidence

- `JAZZ-AI-POL-003-AC-001`: `PASS` — static: dibs XYZ + `JazzAI_AllySpacingScore` in `AIScoreDest`.
- `JAZZ-AI-POL-003-AC-002`: `PASS` — static: `AIPolicyAllySpacing`.
- `JAZZ-AI-POL-003-AC-003`: `BLOCKED` — runtime/human.

## Documentation delta

- design archetypes + playtest.
