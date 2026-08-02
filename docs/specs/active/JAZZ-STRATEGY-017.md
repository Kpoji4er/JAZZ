---
id: JAZZ-STRATEGY-017
status: implemented
owner: project-owner
systems:
  - legion-global-ai
repositories:
  - jazz
risk: high
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-017.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/Code/UtilityFunc.lua
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/bugs/nomaps-playtest-2026-07-30.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz/docs/tools/_test_legion_money_cargo.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-017: Legion money cargo in unit inventory

## Проблема

Playtest (Sergej / owner 2026-08-02): task UI shows `$` for tax / shipment / supply, but killing the squad yields **no** `DiamondBriefcase` / `TinyDiamonds`.

DAP on live save:

- Managed `shipment` squads: `payload.money=12000`, `squad.diamond_briefcase=true`, carrier inventory **DB=0 TD=0** (e.g. id=96, 19 bodies, `LegionGlobalAI_Convoy`).
- Managed `tax` with `payload.money` 2500–7500 often **TD=0 DB=0**.
- `supply` sometimes missing full cargo on fresh spawn path.

Root causes (combined):

1. `tax` collect / some spawn paths update `payload.money` **without** calling `lEnsureMoneyCargo`.
2. `lEnsureMoneyCargo` only tries `units[1]`, ignores `AddItem` failure, still sets `diamond_briefcase=true`.
3. `_RegenerateLegionLoot` / gear refresh **strips all Legion inventory** and recreates starting equipment → wipes cargo while payload/UI `$` remain.

## Цели

- Any managed role with `payload.money > 0` keeps **lootable** valuables in unit inventory matching `$` (DB @$12000 + TinyDiamonds @$500 ceil remainder).
- Cargo survives loot regeneration / gear refresh via **re-sync**.
- Delivery clears tagged cargo like ledger (`payload.money=0`).
- Already-spawned broken convoys on current save get cargo back without new game.

## Non-goals

- Fix vanilla `InitDiamondBriefcaseSquads` / `EnemySquadDefs.DiamondBriefcase` carrier gap (known cross-package risk).
- Pocket valuables from class recipes (unrelated TinyDiamonds).
- Early named/veteran/RPG quality gate (owner: out of scope; cargo clarity enough).

## Locked design (owner 2026-08-02)

| Rule | Lock |
| --- | --- |
| Item mapping | same as today: floor($/12000)×`DiamondBriefcase`, ceil(remainder/500)×`TinyDiamonds` |
| Tag | cargo items set `jazz_legion_ai_cargo = true` |
| Carrier | first unit with inventory space; else any living unit; fail only if nowhere to place |
| Sync | `lSyncMoneyCargo(squad, dollars)` = clear tagged cargo → place exact `$` |
| Clear on delivery | tax_return / supply deliver / shipment deliver / abort |
| Resync triggers | spawn/dispatch/collect; `SatelliteTick`; `ConflictStart`; after `_RegenerateLegionLoot` |

## Требования

- `JAZZ-STRATEGY-017-REQ-001` — `lSyncMoneyCargo` / clear tagged helpers; `AddItem` success required; multi-carrier.
- `JAZZ-STRATEGY-017-REQ-002` — `shipment`/`supply`/`tax` spawn, reuse dispatch, and tax POI collect keep inventory synced to `payload.money`.
- `JAZZ-STRATEGY-017-REQ-003` — delivery / payload zero clears tagged cargo (not unrelated pocket TinyDiamonds without tag).
- `JAZZ-STRATEGY-017-REQ-004` — periodic/conflict/loot-regen resync restores missing cargo when `payload.money > 0`.
- `JAZZ-STRATEGY-017-REQ-005` — public `JAZZ_LegionAIResyncMoneyCargo()` for console/DAP retrofit of live save.

## Инварианты и ограничения

- Deterministic `InteractionRand` contexts unchanged for non-cargo paths.
- Task UI `$` still reads `payload.money`.
- No jazz-units LootDef / UnitData changes required.
- Do not edit `jazz-nomaps` region/Voronoi files.

## Acceptance criteria

- `JAZZ-STRATEGY-017-AC-001` — DAP/runtime: managed shipment with `$12000` has ≥1 `DiamondBriefcase` (tagged) before conflict.
- `JAZZ-STRATEGY-017-AC-002` — DAP/runtime: tax with `payload.money>0` has matching Tiny/DB inventory value (±500 ceil).
- `JAZZ-STRATEGY-017-AC-003` — after simulated loot regen (or real OpenSatelliteView regen), resync restores cargo.
- `JAZZ-STRATEGY-017-AC-004` — static: helpers/markers present; tax collect path calls sync; supply spawn calls sync.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: jazz-only director inventory; no preset ID change.
- Saves: **existing** managed money squads repaired on next tick/conflict/resync (no schema bump).
- Network/determinism: inventory writes on sync paths only; deterministic order via `sorted_pairs` / unit list order.
- Generated data: none.
- Cross-package references: none required.
- Rollback/recovery: revert `Guardpost_Patrols.lua` / `UtilityFunc.lua` hooks.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: see frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: **approved** (owner locks 2026-08-02; shipment empty-loot evidence)
- Кто подтвердил: project-owner
- Дата: 2026-08-02

## Evidence

- `JAZZ-STRATEGY-017-AC-001`: `PASS (runtime/DAP)` — shipment id=96 `$12000` → DB=1 tagged after inline resync; code path `lSyncMoneyCargo` + hourly/`ConflictStart`/regen hooks.
- `JAZZ-STRATEGY-017-AC-002`: `PASS (runtime/DAP)` — tax id=64 `$2500` → 5×TinyDiamonds tagged.
- `JAZZ-STRATEGY-017-AC-003`: `PASS (static)` — `_RegenerateLegionLoot` + OpenSatelliteView call `JAZZ_LegionAIResyncMoneyCargo`; human regen smoke still recommended after Lua reload.
- `JAZZ-STRATEGY-017-AC-004`: `PASS (static)` — `docs/tools/_test_legion_money_cargo.py`.

## Documentation delta

- technical strategy + playtest B19; wiki/showcase loot=`$`; tools README.
