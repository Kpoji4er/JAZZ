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

- Consume cost per training session: **4** recruits.
- Accrual rates same as Legion POI pulse (farm **2** / city **3** per pulse, **96h** / STRATEGY-016; caps 8/16). Soft gate file `LegionMilitiaRecruits.lua` **loaded**.

## Требования

- `JAZZ-STRATEGY-011-REQ-001` — player city/farm accrue recruits.
- `JAZZ-STRATEGY-011-REQ-002` — public get/consume API.
- `JAZZ-STRATEGY-011-REQ-003` — morning questions: militia Operation full contract out of scope until owner reopens.
- `JAZZ-STRATEGY-011-REQ-004` — docs note partial status (API + optional soft gate loaded; full Operation not accepted).

## Инварианты и ограничения

- Legion recruiter still only collects Legion-side stocks.
- Militia UX remains vanilla until Operation hook confirmed.
- Soft gate activates only if `SectorOperations.MilitiaTraining` or `TrainMilitia` exists at runtime.

## Acceptance criteria

- `JAZZ-STRATEGY-011-AC-001` — static: player accrual + API.
- `JAZZ-STRATEGY-011-AC-002` — docs + morning questions.
- `JAZZ-STRATEGY-011-AC-003` — Operation soft gate: static present when op exists; **full Operation contract** still `BLOCKED` / out of scope per morning Q.
- `JAZZ-STRATEGY-011-AC-004`: `PASS (runtime/human) - owner playtest accepted 2026-07-28` (partial: accrual/API)

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: optional wrap of MilitiaTraining/TrainMilitia when present (`LegionMilitiaRecruits.lua` loaded).
- Saves: uses existing schema v3 `poi_recruits`.
- Network/determinism: no new RNG.
- Generated data: none.
- Cross-package: none.
- Rollback: remove LegionMilitiaRecruits.lua registration.

## План и ownership

1. Overnight partial delivery (API + soft gate).
2. Full Operation contract — when owner reopens militia training.

## Решение владельца

28 июля 2026 — finish Global AI; 7c may leave Operation hook as morning question. Playtest: militia training out of scope. Soft gate remains loaded as optional wrap.

## Evidence

- `JAZZ-STRATEGY-011-AC-001`..`002`: static PASS
- `JAZZ-STRATEGY-011-AC-003`: soft gate loaded (`LegionMilitiaRecruits.lua` in metadata); full Operation acceptance `BLOCKED` / out of scope — docs sync 2026-07-29
- `JAZZ-STRATEGY-011-AC-004`: `PASS (runtime/human)` — owner playtest accepted 2026-07-28 (partial)

## Documentation delta

- strategy docs, wiki, roadmap, morning questions
