---
id: JAZZ-STRATEGY-010
status: approved
owner: project-owner
systems:
  - legion-global-ai
  - satellite-ui
repositories:
  - jazz
risk: high
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-010.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/Code/Regions_Sectors.lua
  - jazz/Code/LegionSquadComposition.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/Strings.csv
  - jazz/Localization/EnglishManual.csv
  - jazz/Localization/RussianManual.csv
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/docs/technical/testing.md
  - jazz/docs/specs/active/JAZZ-GLOBAL-AI-MORNING-QUESTIONS.md
exclusive_resources:
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-010: manpower, recruiter, manpower convoy

## Проблема

Roadmap 7b: spawn должен тратить людей; recruits копятся на city/farm; recruiter и manpower-конвой ещё не существуют.

## Цели

- Schema **v3**: `outpost.manpower`, `major.manpower`, `region_state.poi_recruits`.
- City/farm accumulate recruits (mines never); recruiter circuit mirrors tax.
- Manpower convoy Major→outpost when outpost low and Major has cargo.
- Combat spawn already prepared: charges `manpower_cost` when pools exist.
- Icons RECRUITER + MANPOWER; RU/EN strings; docs.

## Non-goals

- Player militia Operation hook (011).
- Reverse manpower convoy outpost→Major.
- Per-tier manpower weighting.

## Locked defaults (morning Q)

- Farm +1 recruit / 24h; City +2 / 24h; sector caps farm 8 / city 20.
- Outpost manpower start 20 / capacity 60; Major start 80 / capacity 600.
- RecruiterThreshold=8, RecruiterCap=2, RecruiterCooldown=24h.
- ManpowerConvoyCargo=16; trigger at 40% of outpost capacity.

## Требования

- `JAZZ-STRATEGY-010-REQ-001` — schema migrate 2→3 with manpower defaults.
- `JAZZ-STRATEGY-010-REQ-002` — recruit accrual city/farm only.
- `JAZZ-STRATEGY-010-REQ-003` — recruiter circuit → outpost.manpower.
- `JAZZ-STRATEGY-010-REQ-004` — manpower convoy Major→outpost.
- `JAZZ-STRATEGY-010-REQ-005` — combat spawn gated by manpower when pools present.
- `JAZZ-STRATEGY-010-REQ-006` — loc + docs.

## Инварианты и ограничения

- Tax/money ledger unchanged.
- Logistics roles do not charge manpower for escort in v1.
- Deterministic InteractionRand contexts.

## Acceptance criteria

- `JAZZ-STRATEGY-010-AC-001` — static schema + accrual.
- `JAZZ-STRATEGY-010-AC-002` — static recruiter + convoy.
- `JAZZ-STRATEGY-010-AC-003` — static spawn manpower gate.
- `JAZZ-STRATEGY-010-AC-004` — loc/docs.
- `JAZZ-STRATEGY-010-AC-005` — runtime: `BLOCKED`.

## Impact и совместимость

- Saves schema 2 migrate lazily to 3.
- Early game outpost may wait for recruits/manpower convoy before large spawns.

## План и ownership

1. Overnight roadmap completion approval.
2. Implement schema + roles.
3. Owner runtime smoke.

## Решение владельца

28 июля 2026 — «доделай всю задачу по глобалке» includes 7b with locked defaults.

## Evidence

- pending

## Documentation delta

- strategy-squads-sectors, wiki, roadmap, testing, morning questions
