---
id: JAZZ-STRATEGY-024
status: implemented
owner: project-owner
systems:
  - legion-global-ai
  - strategy-squads
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-024.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/Code/LegionSquadComposition.lua
  - jazz/Code/LegionSquadGenerator.lua
  - jazz/Code/Regions_Sectors.lua
  - jazz/SquadsIcons/Enemy/<faction>/*_SUPPORT_squad.png
  - jazz/SquadsIcons/Enemy/ (_shields, _misc, faction subfolders)
  - jazz/docs/tools/_check_legion_support_024.py
  - jazz/docs/tools/_reorg_squad_icons_folders.py
  - jazz/docs/tools/_rewrite_squad_icon_doc_paths.py
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/systems/squad-role-icons.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz/Localization/RussianManual.csv
  - jazz/Localization/EnglishManual.csv
  - jazz/Russian.csv
  - jazz/English.csv
exclusive_resources:
  - jazz/Code/Guardpost_Patrols.lua Legion AI roles
  - localization IDs 890000000001651–890000000001653
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-024: Legion AI small specialist support pool

## Проблема

Роль `reinforce` — крупное пограничное усиление (early 6–10 → mature 15–25, `garrison_lite`). Нет отдельного пула **маленьких** уже обученных спецгрупп (снайперы / пулемёты / миномёт), которые докидываются к существующей обороне.

## Цели

- Новая regular-роль **`support`**: отдельный cap/cost/missions/иконка от `reinforce`.
- Размер **4–7** (early = mature; без growth).
- Состав **T3–T4** specialists + 1 лидер (T2/T3) + T3 escort; один archetype на отряд.
- Archetypes v1: **sniper** / **mg** / **mortar** (weighted pick при spawn).
- Триггер: Legion key/POI соседствует с player threat **и** уже есть `garrison` или `reinforce` на цели (задача/hold).
- Avoid-player routing как у `reinforce`; нет пути → spawn + hold.

## Non-goals

- RPG/GL archetypes (follow-up).
- Замена или ресайз `reinforce`.
- Новые UnitData / EnemySquadDef presets (используем существующие `JAZZ_Legion_*` + shell lists как у reinforce).
- Изменение RegularSquadCap формулы.

## Требования

- `JAZZ-STRATEGY-024-REQ-001` — Region fields: `SupportCap` default **1**, `SupportCost` default **18000**, `SupportMissions` default **2**.
- `JAZZ-STRATEGY-024-REQ-002` — `JAZZ_LegionRoleRecipes.support`: size 4–7 fixed; allow T3/T4 specialists + leaders + T3 escort prefixes; `tier_bias = "specialty"`.
- `JAZZ-STRATEGY-024-REQ-003` — Generator: pick archetype sniper|mg|mortar; force 1 leader; specialty counts (sniper/mg **2–3**, mortar **1**); fill escort; bypass soft-cap for specialty bucket; no medic reserve for n&lt;10.
- `JAZZ-STRATEGY-024-REQ-004` — Director: role tables, `lSupportTarget`, spawn after reinforce, hold_for_path like reinforce, working hold like reinforce, diagnostics caps/costs.
- `JAZZ-STRATEGY-024-REQ-005` — Store `squad_state.support_archetype`; top-up prefers same archetype.
- `JAZZ-STRATEGY-024-REQ-006` — Icon `*_SUPPORT_squad.png` all five factions; wired path; RU/EN role + task strings.
- `JAZZ-STRATEGY-024-REQ-007` — Docs: technical + wiki + showcase RU/EN + roadmap + squad-role-icons.

## Инварианты и ограничения

- `reinforce` behavior/sizes unchanged.
- Public role string `support`; NetSync/InteractionRand contexts include role + archetype.
- Only `JAZZ_Legion_*` unit IDs.
- Saves: additive role; old saves without support squads OK.

## Acceptance criteria

- `JAZZ-STRATEGY-024-AC-001` — static: role wired in caps/costs/missions/images/recipes/generator/spawn path.
- `JAZZ-STRATEGY-024-AC-002` — static: composition size ∈ [4,7]; units only T2+ leaders and T3+ specialists/escort per allow-list; archetype ∈ {sniper,mg,mortar}.
- `JAZZ-STRATEGY-024-AC-003` — static: `lSupportTarget` requires neighbor threat + existing garrison/reinforce on target; does not consume `ReinforceCap`.
- `JAZZ-STRATEGY-024-AC-004` — runtime/human: support squad appears on sat with SUPPORT icon, small elite composition, attaches to defended border sector.
- `JAZZ-STRATEGY-024-AC-005` — docs/wiki/showcase/icons catalog updated.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: Legion director + composition only; medium risk.
- Saves: additive `support` role / `support_archetype` field.
- Network/determinism: InteractionRand contexts `Support_*` / `JAZZ_LegionGen_support_*`.
- Generated data: Region property defaults in `Regions_Sectors.lua` (no items.lua Region rewrite required if defaults suffice).
- Cross-package: none (jazz only).
- Rollback: remove role wiring; orphan support squads become unmanaged.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: Guardpost_Patrols roles; loc IDs 1651–1653

## Решение владельца

- Статус: **approved** (owner: «устраивает, делай»; icon: create)
- Кто подтвердил: project-owner
- Дата: 2026-08-10
- Locks: role `support`; size 4–7; archetypes sniper+MG+mortar; SupportCap **1**/outpost; icon new SUPPORT

## Evidence

- `JAZZ-STRATEGY-024-AC-001`: `PASS (static)` — `_check_legion_support_024.py`; role/cap/cost/icon/spawn wired
- `JAZZ-STRATEGY-024-AC-002`: `PASS (static)` — recipe size 4–7 fixed; archetypes sniper/mg/mortar; specialty builder
- `JAZZ-STRATEGY-024-AC-003`: `PASS (static)` — `lSupportTarget` + `lHasDefenseAt`; separate SupportCap
- `JAZZ-STRATEGY-024-AC-004`: `BLOCKED` — runtime/human sat spawn + composition
- `JAZZ-STRATEGY-024-AC-005`: `PASS (static)` — technical/wiki/showcase/icons/roadmap updated

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md`
- `docs/technical/systems/squad-role-icons.md`
- `docs/wiki/legion-global-ai.md`
- `docs/showcase/ru|en/legion-strategy.md`
- `docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md`
