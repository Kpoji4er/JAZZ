---
id: JAZZ-HOTFIX-006
status: approved
owner: project-owner
systems:
  - legion-global-ai
  - enemy-squads
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - Code/LegionSquadGenerator.lua
  - Code/LegionSquadComposition.lua
  - docs/specs/active/JAZZ-HOTFIX-006.md
  - docs/specs/active/JAZZ-STRATEGY-008.md
  - docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - docs/tools/_test_legion_class_caps.py
  - docs/tools/README.md
  - docs/technical/systems/strategy-squads-sectors.md
  - docs/wiki/legion-global-ai.md
  - docs/showcase/ru/legion-strategy.md
  - docs/showcase/en/legion-strategy.md
exclusive_resources:
  - none
related_decisions:
  - none
related_specs:
  - JAZZ-STRATEGY-008
  - JAZZ-STRATEGY-007
approved_by: project-owner
---

# JAZZ-HOTFIX-006: class caps so tax collectors are not sniper stacks

## Проблема

Playtest: satellite tooltip **Сборщик налогов [6]** shows three Front long-rifle portraits (1 + ×2) plus ×3 assault. STRATEGY-008 sniper cap only counts IDs with `Sniper`/`Marksman` (`n=6` → max 1 Marksman). `FrontT1_Rifleman` / `Ambusher` / `Marauder` are `"line"` and uncapped, so a 6-man tax recipe (AssaultT1/T2 + FrontT1/T2) can look like a DMR squad. Same UnitData ID can also stack ×3.

Owner: limit classes.

## Цели

- Same-id cap `min(3, max(1, floor(n×0.34)))` for classes **not** on the owner uncapped-line list (officers/medics still density-only).
- Uncapped line (owner 2026-08-13): Roughneck, Pillager, ShockTrooper, Rifleman, Marauder, Raider, Veteran — any number of copies; they do not consume the escort Front slot.
- Same-id cap is **off** on `VeryHard` (Mission Impossible). Sniper/MG/heavy/specialist buckets and Marksman deny stay.
- Logistics escorts: remaining Front specialists (Ambusher / Marksman / Sniper / Merc / MercSniper) ≤ `min(2, max(1, floor(n×0.25)))`.
- `tax`/`supply`/`shipment` deny `JAZZ_Legion_FrontT2_Marksman`.
- STRATEGY-008 MG/sniper/specialist bucket numbers unchanged.

## Non-goals

- Rewriting combat recipes (patrol/garrison Front mix).
- Applying same-id / Front caps to STRATEGY-024 support specialty fill (sniper detachments still 2–3 specialists).
- Reshuffling already spawned satellite squads (next spawn / new game).
- Changing satellite portrait glyphs.

## Требования

- `JAZZ-HOTFIX-006-REQ-001` — same-id cap in `lWouldBreakSoftCap` except officers, medics, `JAZZ_LegionUncappedLineIds`, and `VeryHard`.
- `JAZZ-HOTFIX-006-REQ-002` — escort Front-specialist cap when `JAZZ_LegionRoleIsLogisticsEscort(role)`; uncapped line IDs skipped.
- `JAZZ-HOTFIX-006-REQ-003` — `deny_ids` on tax/supply/shipment; `JAZZ_LegionUnitAllowedForRole` + `JAZZ_ResolveLegionRoleRecipe` honor it.
- `JAZZ-HOTFIX-006-REQ-004` — top-up uses the same caps with `recipe_role`.

## Инварианты и ограничения

- Locked STRATEGY-008 bucket caps stay: MG ≤ min(4, floor(n×0.35)); sniper ≤ min(3, floor(n×0.25)); specialist ≤ min(3, floor(n×0.20)).
- Officer/medic density (STRATEGY-005 / 015) not same-id-capped.
- Uncapped line list is owner-editable in `JAZZ_LegionUncappedLineIds`; adding an ID there is the intended way to exempt more classes.
- Public UnitData IDs unchanged.
- `InteractionRand` contexts unchanged.

## Acceptance criteria

- `JAZZ-HOTFIX-006-AC-001` — static: same-id + escort Front helpers; `lWouldBreakSoftCap(..., role)` on build and top-up.
- `JAZZ-HOTFIX-006-AC-002` — static: Marksman denied for tax/supply/shipment; resolve copies `deny_ids`.
- `JAZZ-HOTFIX-006-AC-003` — technical + wiki + showcase RU/EN: tax/logistics may stack uncapped line (rifleman/roughneck/…); dedicated marksmen stay rare / denied on tax.
- `JAZZ-HOTFIX-006-AC-004` — runtime/human: new tax collector of size 6 is not a Marksman/Ambusher stack; many Riflemen/Roughnecks is OK.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: generator-only; existing live tax squads keep current roster until rest/respawn.
- Saves: no schema change.
- Network: same InteractionRand contexts; candidate filters change who is picked, not the RNG key.

## План и ownership

1. Owner playtest request 2026-08-12 = approve additive caps.
2. Generator + recipe deny + docs + static test.
3. Runtime: spawn a new tax collector after mod reload.

## Решение владельца

12 августа 2026 — «наверное надо лимитировать классы» по скрину сборщика из снайперов.

## Evidence

- `JAZZ-HOTFIX-006-AC-001`..`003`: static (this change set)
- `JAZZ-HOTFIX-006-AC-004`: `BLOCKED (runtime/human)` until owner reloads and spawns a new tax squad

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md`
- `docs/wiki/legion-global-ai.md`
- `docs/showcase/ru/legion-strategy.md`, `docs/showcase/en/legion-strategy.md`
- STRATEGY-008 locked-defaults pointer; roadmap 6c one-liner
