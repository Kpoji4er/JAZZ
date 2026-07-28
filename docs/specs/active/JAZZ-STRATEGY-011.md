---
id: JAZZ-STRATEGY-011
status: approved
owner: project-owner
systems:
  - legion-global-ai
  - sector-operations
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-011.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/Code/LegionMilitiaRecruits.lua
  - jazz/metadata.lua
  - jazz/items.lua
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/docs/specs/active/JAZZ-GLOBAL-AI-MORNING-QUESTIONS.md
exclusive_resources:
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-011: player militia ↔ recruit stock (partial)

## Проблема

Roadmap 7c: militia training should consume local recruits from the same city/farm pool. Vanilla Operation hook needs owner confirmation of exact preset/id.

## Цели

- Player-owned city/farm accrue into the same `region_state.poi_recruits`.
- Public API: `JAZZ_GetSectorRecruits`, `JAZZ_TryConsumeSectorRecruits`.
- Document Operation wrap as morning decision; do not break militia UX blindly.

## Non-goals

- Full Militia Training Operation rewrite without confirmed vanilla ID.
- Changing MaxMilitia / MilitiaTrainingCost defaults.

## Locked defaults

- Consume cost per training session: **4** recruits (morning Q if wrong).
- Accrual rates same as Legion (farm 1/day, city 2/day).

## Требования

- `JAZZ-STRATEGY-011-REQ-001` — player city/farm accrue recruits.
- `JAZZ-STRATEGY-011-REQ-002` — public get/consume API.
- `JAZZ-STRATEGY-011-REQ-003` — morning questions file lists Operation hook TBD.
- `JAZZ-STRATEGY-011-REQ-004` — docs note partial status.

## Инварианты и ограничения

- Legion recruiter still only collects Legion-side stocks.
- Militia UX remains vanilla until Operation hook approved.

## Acceptance criteria

- `JAZZ-STRATEGY-011-AC-001` — static: player accrual + API.
- `JAZZ-STRATEGY-011-AC-002` — docs + morning questions.
- `JAZZ-STRATEGY-011-AC-003` — Operation consume hook: `BLOCKED` (needs morning).
- `JAZZ-STRATEGY-011-AC-004` — runtime: `BLOCKED`.

## План и ownership

1. Overnight partial delivery.
2. Morning: confirm Operation id and finish hook.

## Решение владельца

28 июля 2026 — finish Global AI; 7c may leave Operation hook as morning Q.

## Evidence

- `JAZZ-STRATEGY-011-AC-001`..`002`: static PASS
- `JAZZ-STRATEGY-011-AC-003`..`004`: `BLOCKED` (Operation id + runtime)

## Documentation delta

- strategy docs, wiki, roadmap, morning questions
