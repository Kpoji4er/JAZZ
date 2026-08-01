---
id: JAZZ-COMPAT-004
status: implemented
owner: project-owner
systems:
  - strategy-squads-sectors
  - units-progression
  - package-architecture
repositories:
  - jazz-nomaps
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-COMPAT-004.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/docs/technical/bugs/nomaps-playtest-2026-07-30.md
  - jazz/docs/technical/compatibility.md
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz-nomaps/Code/NoMaps_Autonomy.lua
  - jazz-nomaps/items.lua
  - jazz-nomaps/metadata.lua
exclusive_resources:
  - ModDef:7MsJ2Eq
  - GameVar:gv_JAZZ_NoMaps
  - Code:NoMaps_Autonomy.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMPAT-004: NoMaps Global AI revive + UnitData remap + tiered loot

## Проблема

1. После COMPAT-003 economy Global AI на NoMaps всё ещё выглядит мёртвым: Major HQ
   latch'ится на Ernie `B28` до disable; InitialSquads блокируют garrison spawn; POI
   stock пустой → нет tax/recruiter.
2. `SQUAD_REMAP` не меняет UnitData map-маркеров → ванильные Goon/Raider на I1/I2.
3. Container inject одинаково жирный с tier 11 (оружие/средняя броня с первого сектора).

## Цели

- NoMaps: Major HQ = `A20` (force), adopt InitialSquads → managed garrison, seed POI.
- Ванильные generic Legion UnitData → random `JAZZ_Legion_*` из ролевого пула по tier.
- Container loot chance/состав от `JAZZ_Legion_Tier` (скудно на T1).

## Non-goals

- Правки `jazz-maps` / authored Ernie markers.
- Morph mid-combat; перегенерация уже `injected` секторов.
- Полный redesign mainland Global AI.

## Требования

- `JAZZ-COMPAT-004-REQ-001` — после nomaps bootstrap `gv_JAZZ_LegionAI.major.hq_sector`
  = resolved Major HQ (`A20` when present); EnsureState не latch'ит HQ с disabled /
  ErnieIsland при `JAZZ_NoMapsIsActive`.
- `JAZZ-COMPAT-004-REQ-002` — Legion squads на managed outpost adopt'ятся как managed
  garrison (без удвоения численности).
- `JAZZ-COMPAT-004-REQ-003` — auto-regions получают seed `poi_money` / `poi_recruits`
  выше tax/recruiter thresholds.
- `JAZZ-COMPAT-004-REQ-004` — generic vanilla Legion UnitData remapped to `JAZZ_Legion_*`
  pool (campaign major tier + Stronger/Elite bump); named/Hyena skip; same session_id.
- `JAZZ-COMPAT-004-REQ-005` — container inject packs/chances by `JAZZ_Legion_Tier` major
  band; T1 без mid armor / assault rifles as common drops.
- `JAZZ-COMPAT-004-REQ-006` — no-op when `FhNNYd` loaded; maps profile unaffected.

## Инварианты и ограничения

- Deterministic `InteractionRand`; stable session_id.
- Не копировать UnitData bodies в nomaps.
- L1: no mid-combat morph (recreate at spawn/enter only).

## Acceptance criteria

- `JAZZ-COMPAT-004-AC-001` — static: HQ force + Ernie skip + adopt + POI seed present.
- `JAZZ-COMPAT-004-AC-002` — runtime: NewGame NoMaps → `Major HQ=A20`; managed garrison
  within first command window; patrol/tax can appear after seed.
- `JAZZ-COMPAT-004-AC-003` — runtime/human: I1/I2 enemies are `JAZZ_Legion_*`.
- `JAZZ-COMPAT-004-AC-004` — runtime/human: tier 11 containers lack GuardianMedium/AK47
  as typical inject; T3 packs richer.
- `JAZZ-COMPAT-004-AC-005` — maps+nomaps: nomaps no-op; Ernie AI unchanged.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: jazz Guardpost_Patrols defensive HQ filter + public adopt/seed helpers.
- Saves: force HQ overwrite on LoadGame bootstrap; already-injected containers stay.
- Network/determinism: InteractionRand seeds from session/sector keys.
- Generated data: nomaps LootDef T1/T2/T3 + metadata.
- Cross-package: reads jazz-units UnitData IDs; writes nomaps state only.
- Rollback: disable nomaps / revert files.

## План и ownership

- Пакет-владелец: `jazz-nomaps` (+ точечно `jazz` Guardpost_Patrols)
- Reviewer: project-owner
- Declared write set: see frontmatter
- Exclusive resources: ModDef `7MsJ2Eq`, `NoMaps_Autonomy.lua`

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (plan execute)
- Дата: 2026-08-01

## Evidence

- `JAZZ-COMPAT-004-AC-001`: `PASS` — static: `JAZZ_LegionAIForceMajorHQ` / Ernie skip / `AdoptOutpostDefenders` / `SeedPoiEconomy` in `Guardpost_Patrols.lua`; nomaps bootstrap calls them; UnitData remap + tiered `LOOT_PACKS_BY_MAJOR` + LootDefs `_T1|_T2|_T3`.
- `JAZZ-COMPAT-004-AC-002`: `BLOCKED` — runtime NewGame NoMaps (Major HQ=A20; managed garrison).
- `JAZZ-COMPAT-004-AC-003`: `BLOCKED` — runtime/human I1/I2 `JAZZ_Legion_*`.
- `JAZZ-COMPAT-004-AC-004`: `BLOCKED` — runtime/human tier-11 containers.
- `JAZZ-COMPAT-004-AC-005`: `BLOCKED` — runtime maps+nomaps no-op.

## Documentation delta

- `docs/technical/bugs/nomaps-playtest-2026-07-30.md` — B7 reopen + COMPAT-004 causes.
- `docs/technical/compatibility.md` — COMPAT-004 note.
- `docs/technical/systems/strategy-squads-sectors.md` — NoMaps HQ/adopt/seed.
- `docs/wiki/legion-global-ai.md` + showcase RU/EN legion-strategy — NoMaps AI/loot tier.
