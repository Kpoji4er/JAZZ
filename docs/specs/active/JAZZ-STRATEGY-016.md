---
id: JAZZ-STRATEGY-016
status: implemented
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
  - jazz/docs/specs/active/JAZZ-STRATEGY-016.md
  - jazz/Code/LegionSquadComposition.lua
  - jazz/Code/LegionSquadGenerator.lua
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/Code/Regions_Sectors.lua
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz/docs/tools/_test_legion_squad_growth.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - none
related_decisions:
  - none
related_specs:
  - JAZZ-STRATEGY-009
  - JAZZ-STRATEGY-006
  - JAZZ-STRATEGY-010
approved_by: project-owner
---

# JAZZ-STRATEGY-016: Early small squads + economy scale (B+C)

## Проблема

Playtest (Sergej / owner 2026-08-02): mobile Legion density feels like full late-game from day 1. Shipment/tax escorts show **[19]** bodies; combat recipes spawn patrol 12–18 immediately. Resource pools / POI rates feed that density.

Owner lock: approaches **B+C** — longer logistics/command cadence + **small early size_min/max that grow** with time/heat/tier; resources cut by a multiplicative factor. Caps (PatrolCap etc.) may stay.

## Цели

- New combat / logistics managed spawns start **small**, then grow toward mature recipe sizes.
- Economy income + starting pools scale by locked factor so early spawn budgets cannot refill to mature sizes instantly.
- Cadence slows (command / tax / recruiter / combat spawn gate).

## Non-goals

- Separate early quality gate for named/veteran/RPG (owner: «выходит из 2»; cargo clarity from STRATEGY-017 is enough).
- Shrinking already-spawned large squads mid-save (growth applies to **new spawns** + top-up target; existing fat squads stay until retire).
- Editing `jazz-nomaps` region radius / Voronoi (COMPAT-006/007 owned elsewhere).
- Changing PatrolCap / RegularSquadCap defaults (keep).

## Locked numbers (owner mid-band 2026-08-02; tune later)

### Resource / diamond income factor (owner 2026-08-02 priority)

Owner: cut diamond/`$` income **÷3–÷4**. Locked mid-prefer **÷4**:

| Constant | Value | Rationale |
| --- | ---: | --- |
| `JAZZ_LegionEconomyScale` | **25** (%; **×0.25**) | ÷4 diamond/$ generation; owner «раза в 3–4» |

Applied to Region **defaults** (and runtime `lConfig` fallbacks) for **$ / diamond generation** feeding tax/shipment:

- `StartingSupply`, `MajorStartingReserve` (stops day-1 flood of full convoys)
- `PassiveSupplyPerHour`, `CitySupplyBonus`, `FarmSupplyBonus`, `MineDiamondPerHour`
- `PoiMoneyCap` (scaled stock waiting on POI)
- `DiamondShipmentThreshold`, `SupplyConvoyCargo`, `TaxCargoMax` — **also ×0.25** so thresholds stay in proportion to slower fill (else stock never hits old $12000)

Manpower (separate from diamond cut; keep spawnable early escorts):

- `StartingManpower`, `MajorStartingManpower` — same ×0.25 then floors below
- `FarmRecruitsPerDay`, `CityRecruitsPerDay`, `GuardpostRecruitsPerDay`, `PortRecruitsPerDay` — ×0.25 (min 1 where was >0)

**Not** scaled: combat role `$` costs, `TaxThreshold` / `RecruiterThreshold` (absolute tripwires), caps (`PatrolCap` etc.).

Manpower floors after scale (so early recipes remain spawnable):

| Pool | Floor |
| --- | ---: |
| `StartingManpower` | **8** |
| `MajorStartingManpower` | **16** |

(Garrison mature `size_min=25` still waits for recruiter fill / adopt — intentional.)

### Cadence (B)

| Field | Was | New |
| --- | ---: | ---: |
| `CommandInterval` | 6h | **12h** |
| `TaxCooldown` | 24h | **48h** |
| `RecruiterCooldown` | 24h | **48h** |
| Combat spawn gate (`lOutpostCanSpawn`) | 1 / 24h | **1 / 48h** |
| `POIGenerationInterval` | 72h | **96h** |

### Size growth (C)

Mature sizes = current recipe `size_min`/`size_max`. Early sizes:

| Role | Early min–max | Mature min–max |
| --- | ---: | ---: |
| recon | **4–6** | 8–12 |
| patrol | **5–8** | 12–18 |
| qrf | **6–10** | 12–20 |
| reinforce | **6–10** | 15–25 |
| retribution / major | **10–14** | 18–30 |
| garrison | **25–40** (no early shrink — static defense) | same |
| tax / recruiter / manpower | **4–6** | 6–12 |
| supply / shipment | **4–6** | 8–15 |

Growth progress `p ∈ [0,1]` = max of:

| Signal | Formula |
| --- | --- |
| Time | `CampaignDays / 21` |
| Heat | `region_heat / 500` |
| Gear major | `JAZZ_Legion_Tier` tens: `11→0`, `2x→0.5`, `3x→1.0` |

`size = round(lerp(early, mature, p))`, clamp to early..mature.

Logistics roles that today use only `EnemySquadDef` (**15–25** bodies) **must** pass `unit_template_ids` from composition at effective size so escorts are not day-1 `[19]`.

### NoMaps size override (owner 2026-08-02)

When `JAZZ_NoMapsIsActive()` — mainland has many more outposts; use **smaller** bands via `JAZZ_LegionRoleSizeOverrideNoMaps` (Ernie/maps unchanged):

| Role | NoMaps early | NoMaps mature |
| --- | ---: | ---: |
| recon | **3–5** | **6–9** |
| patrol | **4–6** | **8–12** |
| qrf | **4–7** | **8–14** |
| reinforce | **4–7** | **10–16** |
| retribution / major | **8–12** | **14–22** |
| garrison | **12–20** | **12–20** |
| tax / recruiter / manpower | **3–5** | **5–8** |
| supply / shipment | **3–5** | **5–10** |

## Требования

- `JAZZ-STRATEGY-016-REQ-001` — growth helpers + early/mature tables as locked above.
- `JAZZ-STRATEGY-016-REQ-002` — generator / top-up / optimal-size use effective sizes for the region’s progress.
- `JAZZ-STRATEGY-016-REQ-003` — logistics spawn uses composition templates at effective escort size (not raw full EnemySquadDef count).
- `JAZZ-STRATEGY-016-REQ-004` — economy / diamond income scale **×0.25** + cadence defaults locked above.
- `JAZZ-STRATEGY-016-REQ-005` — docs/wiki/showcase + roadmap updated; issue #3 explicitly deferred.
- `JAZZ-STRATEGY-016-REQ-006` — NoMaps uses `JAZZ_LegionRoleSizeOverrideNoMaps` locked table above; Ernie/maps keep base recipes.

## Инварианты и ограничения

- STRATEGY-015 medic density still applies to **effective** `n`.
- STRATEGY-005 officer density on effective `n`.
- Existing save: **no** forced despawn of oversized squads; new spawns + top-up targets follow curve; economy rates change from new defaults on next read (preset defaults); already-seeded `outpost.money` not mass-rewritten.
- No nomaps region file edits.

## Acceptance criteria

- `JAZZ-STRATEGY-016-AC-001` — static: at `p=0`, patrol effective 5–8; at `p=1`, 12–18.
- `JAZZ-STRATEGY-016-AC-002` — static: economy scale helper ×0.25 with manpower floors.
- `JAZZ-STRATEGY-016-AC-003` — static: logistics roles wired to composition size path markers.
- `JAZZ-STRATEGY-016-AC-004` — early campaign shipment/tax use composition escort sizes (not raw EnemySquadDef ~19); existing fat squads unchanged.
- `JAZZ-STRATEGY-016-AC-005` — static: NoMaps override table present; patrol early 4–6 / mature 8–12 when override applied.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: jazz-only defaults + generator; EnemySquadDef presets remain fallback lists.
- Saves: new spawns only for size; cadence/rates affect ongoing ticks; no schema bump.
- Network/determinism: growth from CampaignTime + heat + tier.
- Generated data: none.
- Cross-package references: none required.
- Rollback/recovery: revert composition/generator/regions/patrols defaults.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: see frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: **implemented** (B+C + diamond/$ ×0.25 ÷4; NoMaps smaller size table 2026-08-02)
- Кто подтвердил: project-owner
- Дата: 2026-08-02
- 2026-08-18: cadence lock documented on 009/006/010 (pulse **96h**, tax/recruiter cooldown **48h**, command **12h**). Runtime already matched.

## Evidence

- `JAZZ-STRATEGY-016-AC-001`: `PASS (static)` — `docs/tools/_test_legion_squad_growth.py` (patrol early 5–8 / mature 12–18).
- `JAZZ-STRATEGY-016-AC-002`: `PASS (static)` — `JAZZ_LegionEconomyScalePct` default 25 + floors.
- `JAZZ-STRATEGY-016-AC-003`: `PASS (static)` — `lEscortUnitTemplates` + logistics composition gate.
- `JAZZ-STRATEGY-016-AC-004`: `PASS (static)` — no shrink of existing squads; new logistics/combat spawn paths use `lEscortUnitTemplates` / growth-resolved sizes. Human: after Lua reload, new tax/shipment should be ~4–6 early (not ~19).
- `JAZZ-STRATEGY-016-AC-005`: `PASS (static)` — `JAZZ_LegionRoleSizeOverrideNoMaps` + resolve gate; patrol NoMaps 4–6 / 8–12.

## Documentation delta

- technical strategy page, wiki, showcase RU/EN, tools growth test; NoMaps size table.