---
id: JAZZ-STRATEGY-012
status: approved
owner: project-owner
systems:
  - legion-global-ai
repositories:
  - jazz
risk: high
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-012.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/Code/LegionSquadGenerator.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/Strings.csv
  - jazz/Localization/EnglishManual.csv
  - jazz/Localization/RussianManual.csv
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/docs/specs/active/JAZZ-GLOBAL-AI-MORNING-QUESTIONS.md
  - jazz/docs/technical/testing.md
exclusive_resources:
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-012: base refit, wounded retreat, idle top-up

## Проблема

Сейчас regular-отряд после mission budget возвращается и **удаляется**. Нет пополнения на базе, нет отступления раненых, idle не докупает юнитов.

## Цели

- Regular combat roles returning home **refit** instead of retire: heal, remove dead, buy toward recipe `size_max` for money+manpower.
- Heavily wounded / under `size_min` squads retreat to home; sit in state `wounded` until resources allow top-up to optimal.
- Idle `ready_for_orders` at home with spare resources may top-up toward optimal before next mission.
- After successful refit, refresh `missions_left` from Region role missions.
- Task UI texts for wounded/refitting.

## Non-goals

- Logistics roles (supply/shipment/tax/recruiter/manpower/major) refit loop (major still returns/retires as today).
- Healing over time without being at home.
- Selling surplus units.

## Locked defaults

- Retreat if living &lt; `size_min` OR wounded/low-HP (≥50% MaxHP or status Wounded) ≥ half of living.
- Optimal size = recipe `size_max`.
- Top-up uses generator soft caps + unit prices; charge outpost money+manpower.
- Heal to MaxHitPoints on entering base refit.

## Требования

- `JAZZ-STRATEGY-012-REQ-001` — regular return → refit, not retire.
- `JAZZ-STRATEGY-012-REQ-002` — wounded/understrength retreat to home → state `wounded`.
- `JAZZ-STRATEGY-012-REQ-003` — base top-up toward size_max when resources allow.
- `JAZZ-STRATEGY-012-REQ-004` — idle at home may top-up.
- `JAZZ-STRATEGY-012-REQ-005` — loc RU/EN + docs.

## Инварианты и ограничения

- Need-gates for new spawn unchanged.
- Caps still limit how many regular squads exist.
- Deterministic InteractionRand contexts for top-up picks.

## Acceptance criteria

- `JAZZ-STRATEGY-012-AC-001` — static: return path refits regulars.
- `JAZZ-STRATEGY-012-AC-002` — static: wounded retreat + wounded state.
- `JAZZ-STRATEGY-012-AC-003` — static: top-up charges money/manpower.
- `JAZZ-STRATEGY-012-AC-004` — loc/docs.
- `JAZZ-STRATEGY-012-AC-005` — runtime: `BLOCKED`.

## Impact и совместимость

- Saves: new squad_state.state `wounded`; old returning still works.
- Network: InteractionRand for top-up.
- Generated data: none.

## План и ownership

1. Owner request 28 July 2026 (refit / wounded / idle buy).
2. Implement + docs.
3. Owner runtime smoke.

## Решение владельца

28 июля 2026 — «отряды могут пополнить/докупить; раненые отступают; idle тоже докупает».

## Evidence

- `JAZZ-STRATEGY-012-AC-001`..`004`: static PASS
- `JAZZ-STRATEGY-012-AC-005`: `BLOCKED (runtime)`

## Documentation delta

- strategy-squads-sectors, wiki, roadmap, testing, morning questions note
