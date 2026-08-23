---
id: JAZZ-COMBAT-008
status: implemented
owner: project-owner
systems:
  - armor-damage-wounds-will
  - strategy-squads-sectors
  - satellite-vehicles
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - Code/System_EnergyLadder.lua
  - Code/SatelliteSquad.lua
  - metadata.lua
  - English.csv
  - Russian.csv
  - docs/specs/active/JAZZ-COMBAT-008.md
  - docs/technical/systems/armor-damage-wounds-will.md
  - docs/technical/systems/file-coverage.md
  - docs/wiki/combat-and-accuracy.md
  - docs/showcase/ru/combat-and-accuracy.md
  - docs/showcase/en/combat-and-accuracy.md
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMBAT-008: Trauma → пеший travel; Ribs не режут энергию

## Проблема

HP-мод travel-усталости непредсказуемо тормозит отряд. Травмы должны влиять на стратегию без двойного «уже калека в бою + стоп travel».

## Цели

- **Ноги:** замедляют только **пеший** переход (кап 30%); не тачка / вода / shortcut(air/tunnel).
- **Рёбра:** travel-усталость **не** ускоряют (owner 2026-08-23). Цена рёбер на глобалке — **долг макс. ОЗ** (MED-006/007), не набор Tired.
- HP-мод `GetHPAdditionalTiredTime` → **0** (порог travel считает `JazzGetTirednessTravelThreshold`).

## Non-goals

- Прямой ChangeTired от травм; замедление mounted/water/air; новые CE.

## Требования

- `JAZZ-COMBAT-008-REQ-001` — Legs Light/Medium/Heavy → squad foot travel time +10/+20/+30% (худший в отряде). Skip if water terrain, shortcut, river special, or `JAZZ_vehicle` mounted.
- `JAZZ-COMBAT-008-REQ-002` — **Superseded 2026-08-23:** Ribs no longer multiply the travel tiredness threshold. Combat AP/Pain stay; satellite cost is max-HP debt (MED-006/007).
- `JAZZ-COMBAT-008-REQ-003` — `GetHPAdditionalTiredTime` always returns 0. **Superseded by [JAZZ-MED-007](JAZZ-MED-007.md) REQ-009**: current `HitPoints` vs **100** adjusts the travel threshold; this function stays 0 to avoid double-apply.
- `JAZZ-COMBAT-008-REQ-004` — Docs wiki/showcase/technical.

## Acceptance

- `JAZZ-COMBAT-008-AC-001` — Static: Legs slow table + wrap skips vehicle/water/shortcut.
- `JAZZ-COMBAT-008-AC-002` — Static: no `RIBS_TIREDNESS_MUL`; HP additional = 0; ReachSectorCenter uses Jazz threshold (HitPoints vs 100).
- `JAZZ-COMBAT-008-AC-003` — Runtime/human: Heavy Legs foot slower; vehicle unchanged. Ribs travel-tiredness check **superseded** (max-HP debt only).
- `JAZZ-COMBAT-008-AC-004` — Docs updated.

## Evidence

- AC-001/002/004: PASS (static + docs in change set; AC-002 = no ribs mul)
- AC-003: BLOCKED runtime/human for Legs; ribs Winded-sooner **superseded**

## Documentation delta

- `docs/technical/systems/armor-damage-wounds-will.md` — COMBAT-008 section
- `docs/technical/systems/file-coverage.md` — EnergyLadder blurb
- `docs/wiki/combat-and-accuracy.md` + showcase RU/EN