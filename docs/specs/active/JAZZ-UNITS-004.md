---
id: JAZZ-UNITS-004
status: implemented
owner: project-owner
systems:
  - legion-units-equipment
  - inventory-items-loot
  - ai-awareness
repositories:
  - jazz
  - jazz-units
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/UtilityFunc.lua
  - jazz/Code/CombatAI.lua
  - jazz/scripts/legion-loadouts/generate.py
  - jazz/scripts/legion-loadouts/run_static_tests.py
  - jazz/scripts/legion-loadouts/TESTING.md
  - jazz/scripts/legion-loadouts/data/recipes.json
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - jazz-units/UnitData/JAZZ_Legion_FrontT3_Veteran.lua
  - jazz-units/UnitData/JAZZ_Legion_FrontT4_Mercenary.lua
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
  - jazz/docs/design/legion-loadouts.md
  - jazz/docs/specs/active/JAZZ-UNITS-003.md
  - jazz/docs/specs/active/JAZZ-UNITS-004.md
  - jazz/docs/showcase/ru/legion-units.md
  - jazz/docs/showcase/en/legion-units.md
exclusive_resources:
  - jazz-units/items.lua
related_decisions:
  - none
approved_by: project-owner chat 2026-07-31 — update specs for bugfix; Legion no weapons / save / regen; 2026-08-01 — M72 LAW in Legion_GL + restore Veteran/Mercenary gl_5pc
related:
  - JAZZ-UNITS-003
  - JAZZ-WEAPONS-005
---

# JAZZ-UNITS-004: Legion loot load + regen scope + AI unarmed guard

## Проблема

После legacy Legion loadout generator (markers `JAZZ-UNITS-003-GENERATED-*`; ID later reused for named perks):

1. `generate.py` `find_moditem_block` оставлял хвост `),` → stacked `}),),),),`, `items.lua` paren imbalance (−222) → chunk не парсится → **пустые инвентари** (Легион без оружия, AIM loot тоже).
2. `_RegenerateLegionLoot` чистит/`CreateStartingEquipment` **всем** `gv_Squads` (Legion guard только на tactical `unit`); technical уже помечал это как дефект.
3. JAZZ `AICreateContext` индексирует `weapon.BulletDropRange` без nil-check → assert при безоружном юните.
4. Pre-generator `LegionGL_5pc` на Veteran/Mercenary был потерян; disposable **M72 LAW** не входил в Legion launcher pools.

## Цели

- Идемпотентный replace LootDef без stacked closers; static guard paren/brace balance.
- `_RegenerateLegionLoot` трогает только Legion (strategic + tactical), с nil-safe `unitdata`.
- `AICreateContext` не падает без active weapon (early return / unarmed-safe path).
- Firearm pools: unconditional low-weight fallback entry (как pre-003 `LegionT1_PistolList`), если quest conditions не сматчились.
- Frontliner secondary launcher chance restored; **M72 LAW** in Legion GL/rocketeer pools.

## Non-goals

- Смена quest TCE / starting `JAZZ_Legion_Tier` (=11).
- Полный rewrite AI context scoring.
- Миграция уже пустых юнитов в save без regen/respawn (после фикса — OpenSatellite regen или новый сектор).
- Disposable runtime contract (spent tube / Reload block) — `JAZZ-WEAPONS-005`.
- Rename of generated markers `JAZZ-UNITS-003-GENERATED-*` (historical; not the named-perks SPEC-ID).

## Требования

- `JAZZ-UNITS-004-REQ-001` — `find_moditem_block` consume full `}),`; static tests fail on `}),),` or paren/brace ≠ 0.
- `JAZZ-UNITS-004-REQ-002` — `_RegenerateLegionLoot` only Legion Affiliation; no `unitdata.Items={}` outside nil/affiliation guard; supersedes legacy loadout REQ «не менять regen» for this bugfix.
- `JAZZ-UNITS-004-REQ-003` — `AICreateContext`: no index of nil `weapon`.
- `JAZZ-UNITS-004-REQ-004` — each generated `*_Firearm` includes ≥1 unconditional fallback `LootEntryLootDef` (weight low vs tiered pool) pointing at a valid arch1 combo.
- `JAZZ-UNITS-004-REQ-005` — recipes `utility.gl_5pc` on `FrontT3_Veteran` and `FrontT4_Mercenary` emit `LegionGL_5pc` into `*_Inventory`; pool `Legion_GL` includes LootDef `M72LAW` (item `M72LAW`) alongside M79 / ChinaLake.
- `JAZZ-UNITS-004-REQ-006` — Veteran/Mercenary `CustomEquipGear` TryEquip Handheld B: `GrenadeLauncher`, then `HeavyWeapon` (M72), then melee; `Rocketeer_Launcher` weights RPG (~70%) and `M72LAW` (~30%).

## Acceptance criteria

- `JAZZ-UNITS-004-AC-001` — static: `run_static_tests.py` PASS incl. paren/stacked closer checks; regenerate idempotent (no new `}),),`).
- `JAZZ-UNITS-004-AC-002` — static: UtilityFunc Legion-only regen; no out-of-guard wipe.
- `JAZZ-UNITS-004-AC-003` — static: CombatAI nil-safe before `weapon.*`.
- `JAZZ-UNITS-004-AC-004` — static: Roughneck_Firearm (and all recipe firearms) contain unconditional fallback entry.
- `JAZZ-UNITS-004-AC-005` — runtime/human: Legion on Ernie has firearm after reload+regen/new fight; AI StartAI without assert when unarmed edge case.
- `JAZZ-UNITS-004-AC-006` — static: `Veteran_Inventory` / `Mercenary_Inventory` reference `LegionGL_5pc`; `Legion_GL` lists `M72LAW`; `Rocketeer_Launcher` has both `RPG` and `M72LAW` weights.
- `JAZZ-UNITS-004-AC-007` — static: Veteran/Mercenary UnitData + items ModItem `CustomEquipGear` include `HeavyWeapon` after `GrenadeLauncher`.

## Evidence

- `JAZZ-UNITS-004-AC-001` — `PASS` (static): `run_static_tests.py` PASS; paren balance 0; no `}),),`; generate 37/37.
- `JAZZ-UNITS-004-AC-002` — `PASS` (static): `UtilityFunc.lua` `_RegenerateLegionLoot` / `___RegenerateLegionLoot` Legion-only via `IsLegionUnitData`.
- `JAZZ-UNITS-004-AC-003` — `PASS` (static): `CombatAI.lua` early-return when `GetActiveWeapons()` nil.
- `JAZZ-UNITS-004-AC-004` — `PASS` (static): 37 `*_Firearm` contain `JAZZ-UNITS-004 unconditional fallback`.
- `JAZZ-UNITS-004-AC-005` — `BLOCKED` (runtime/human): owner — reload mods, OpenSatellite / new fight; Legion armed; no StartAI assert.
- `JAZZ-UNITS-004-AC-006` — `PASS` (static): `LegionGL_5pc` on Veteran/Mercenary inventories; `Legion_GL` + `Rocketeer_Launcher` include `M72LAW`.
- `JAZZ-UNITS-004-AC-007` — `PASS` (static): companions + items.lua CustomEquipGear TryEquip `HeavyWeapon`.

## Documentation delta

- `legion-units-equipment-tiers.md` — regen Legion-only; generator replace / fallback notes; `gl_5pc` / M72 pools.
- `docs/design/legion-loadouts.md` — Veteran/Mercenary GL/LAW%; Rocketeer RPG/LAW mix.
- Named-perks `JAZZ-UNITS-003.md` — not the loadout contract; historical generated markers still say `JAZZ-UNITS-003-GENERATED-*`.
- `docs/showcase/ru|en/legion-units.md` — regen Legion-only; Veteran/Mercenary/Rocketeer launcher note.
- `scripts/legion-loadouts/TESTING.md` — parse health + GL/LAW spot check.