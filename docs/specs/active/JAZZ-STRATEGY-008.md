---
id: JAZZ-STRATEGY-008
status: implemented
owner: project-owner
systems:
  - legion-global-ai
  - enemy-squads
repositories:
  - jazz
risk: high
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-008.md
  - jazz/Code/LegionSquadGenerator.lua
  - jazz/Code/LegionSquadComposition.lua
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/metadata.lua
  - jazz/items.lua
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/docs/technical/testing.md
exclusive_resources:
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-008: composition generator + per-unit spawn $ costs

## Проблема

Roadmap 6c: spawn всё ещё берёт фиксированный EnemySquad preset и списывает flat role cost. Цены (004) и recipes (007) не подключены.

## Цели

- Runtime generator: recipe + unit prices + officer density + soft class caps → список UnitData ID.
- Combat regular roles + major/retribution: `money_cost` = сумма цен юнитов. Generator `false` → **не спавнить** (нет EnemySquadDef unit-list / flat Region-cost fallback). Flat Region costs остаются editor defaults, не debit боевого спавна.
- Poor/full: full к `size_max` в пределах бюджета; poor к `size_min` с дешёвыми tier; ниже min viable → не спавнить.
- Determinism: `InteractionRand` с context `role_home_serial`.
- Docs/roadmap pointer.

## Non-goals

- Manpower gate (010).
- Tax/recruiter roles.
- jazz-units EnemySquad `_Poor`/`_Full` presets (runtime builder вместо v1 presets).
- Переписывание logistics supply/shipment на generator costs (оставлены preset + cargo $).

## Locked defaults (morning Q если пересмотреть)

- Soft caps: MG ≤ min(4, floor(n×0.35)); sniper ≤ min(3, floor(n×0.25)); specialist ≤ min(3, floor(n×0.20)).
- Auto mode: try full, else poor, else fail.
- Combat roles using generator: garrison, patrol, recon, qrf, reinforce, major(retribution recipe).
- Additive [JAZZ-HOTFIX-006](JAZZ-HOTFIX-006.md) (does not change the three bucket numbers): same UnitData ID ≤ min(3, max(1, floor(n×0.34))) except `JAZZ_LegionUncappedLineIds` and except `VeryHard`; logistics escorts remaining Front specialists ≤ min(2, max(1, floor(n×0.25))); tax/supply/shipment deny Marksman.

## Требования

- `JAZZ-STRATEGY-008-REQ-001` — `JAZZ_GenerateLegionSquadComposition` returns units + money_cost or false.
- `JAZZ-STRATEGY-008-REQ-002` — soft caps reject over-skew specialists.
- `JAZZ-STRATEGY-008-REQ-003` — officers respect STRATEGY-005 density; MercCapt for T4 band.
- `JAZZ-STRATEGY-008-REQ-004` — regular combat spawn charges generated money_cost from `outpost.money`.
- `JAZZ-STRATEGY-008-REQ-005` — major spawn charges from `major.money`.
- `JAZZ-STRATEGY-008-REQ-006` — **superseded 2026-08-18**: no preset + flat cost if generator returns false. Combat/major miss → `return false` (`lSpawnRegularRole` / major spawn). EnemySquadDef остаётся **shell** (`GenerateEnemySquad` displayName/side); unit list — только generator templates.
- `JAZZ-STRATEGY-008-REQ-007` — docs updated.

## Инварианты и ограничения

- Need-gates 003 preserved.
- Public EnemySquad IDs still used as shell for GenerateEnemySquad (displayName/side).
- Schema stays v2 until 010.
- Only `JAZZ_Legion_*` unit IDs.

## Acceptance criteria

- `JAZZ-STRATEGY-008-AC-001` — static: generator file + composition helpers.
- `JAZZ-STRATEGY-008-AC-002` — static: spawn path charges sum prices for combat roles.
- `JAZZ-STRATEGY-008-AC-003` — static: MG soft cap enforced in generator.
- `JAZZ-STRATEGY-008-AC-004` — docs/roadmap.
- `JAZZ-STRATEGY-008-AC-005`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-STRATEGY-008-AC-006` — static: combat/major generator miss fail-closed (no EnemySquadDef unit fallback).

## Impact и совместимость

- Runtime: combat squads vary by budget; expensive garrison needs near-full outpost.
- Saves: no schema change.
- Network: InteractionRand contexts must stay stable.

## План и ownership

1. Spec approved via overnight roadmap completion order.
2. Implement generator + wire spawn.
3. Owner runtime smoke.

## Решение владельца

28 июля 2026 — «доделай всю задачу по глобалке до конца» = approve 008 scope from roadmap 6c with locked defaults above.

18 августа 2026 — REQ-006 (preset + flat cost if generator `false`) **superseded**. Loaded: `Guardpost_Patrols` combat/major «No free EnemySquadDef fallback»; miss → no spawn. Не возвращать fallback, пока владелец явно не попросит.

## Evidence

- `JAZZ-STRATEGY-008-AC-001`..`004`: static PASS
- `JAZZ-STRATEGY-008-AC-005`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-STRATEGY-008-AC-006`: `PASS / static` — `lSpawnRegularRole` / major: `if not composition then return false`; REQ-006 superseded. `BLOCKED / runtime` — satellite miss-spawn smoke.

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md` — combat spawn fail-closed.
- `docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md` — 6a/6c: no preset+flat fallback.
- Wiki/showcase — не трогали (не player-facing HUD).
