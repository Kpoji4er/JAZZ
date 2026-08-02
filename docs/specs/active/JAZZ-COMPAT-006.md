---
id: JAZZ-COMPAT-006
status: implemented
owner: project-owner
systems:
  - strategy-squads-sectors
  - package-architecture
repositories:
  - jazz-nomaps
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-COMPAT-006.md
  - jazz-nomaps/Code/NoMaps_Autonomy.lua
  - jazz-nomaps/metadata.lua
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/compatibility.md
  - jazz/docs/technical/bugs/nomaps-playtest-2026-07-30.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz/docs/tools/_verify_nomaps_region_radius.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - ModDef:7MsJ2Eq
  - GameVar:gv_JAZZ_NoMaps
  - Code:NoMaps_Autonomy.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMPAT-006: NoMaps auto-regions — 1 outpost, smaller catchment

## Проблема

В профиле **JAZZ Vanilla Maps** (`jazz-nomaps`) auto-regions `JAZZ_Auto_*`
выглядят огромными: на сат-карте один округ «захватывает» несколько городов и
чужие Guardpost. Playtest save `31(3)` (DAP 2026-08-02): 8 enabled regions,
`ManagedOutposts` length = 1 у каждой, но `#Sectors` = **53…132** и в списках
секторов **3–6 чужих Guardpost** (foreign_gp).

Корневые причины (static + runtime):

1. `lAssignSectorsToOutposts` — Chebyshev radius **R=8** (COMPAT-002 default) —
   слишком большой catchment (~17×17 клетка).
2. Soft-path `lRefreshTrackedAutoRegions` вызывает assign **по одному** outpost
   (`{ outpost_id }`), без конкуренции Voronoi → каждый округ забирает все
   surface-сектора в радиусе R, включая соседние Guardpost как обычные сектора.
3. Force bootstrap при уже managed Guardposts **не** пересобирал `Sectors`
   (unmanaged пуст) — migration могла пометить rev без rebuild.

## Цели

- **≤ 1** managed outpost на auto-region (сохранить текущий `ManagedOutposts={id}`).
- Catchment **~5× меньше** по площади: Chebyshev **R=3** (было 8; площадь ~`(8/3)²≈7×`).
- Soft refresh и full bootstrap используют **один** Voronoi-pass по всем tracked /
  unmanaged Guardpost; force path всегда `lRefreshTrackedAutoRegions`.
- Existing NoMaps saves (в т.ч. `31(3)`) **пересобирают** `Sectors` на load /
  soft bootstrap через `gv_JAZZ_NoMaps.ai_region_rev` (без new game).

## Non-goals

- Смена caps / economy / Major HQ A20 / tax loot / patrol density.
- Hardcoded sector lists по городам.
- Maps-профиль `ErnieIsland` / jazz-maps geography.
- Commit / push / Workshop upload.

## Требования

- `JAZZ-COMPAT-006-REQ-001` — константа `AUTO_REGION_RADIUS = 3` (Chebyshev);
  assign принимает только сектора с `best_dist ≤ AUTO_REGION_RADIUS`.
- `JAZZ-COMPAT-006-REQ-002` — каждый `JAZZ_Auto_*`: `#ManagedOutposts ≤ 1`;
  в `Sectors` нет чужого Guardpost (кроме собственного managed outpost).
- `JAZZ-COMPAT-006-REQ-003` — `lRefreshTrackedAutoRegions` строит buckets одним
  Voronoi по **всем** tracked outposts, затем пишет `Sectors` per region.
- `JAZZ-COMPAT-006-REQ-004` — `AI_REGION_REV` / `gv_JAZZ_NoMaps.ai_region_rev`:
  при rev ниже целевого — rebuild sector lists на soft/full bootstrap; force path
  всегда refresh; затем поднять rev (без сброса manpower/economy).
- `JAZZ-COMPAT-006-REQ-005` — docs: technical + wiki + showcase RU/EN (player-facing
  размер округов NoMaps).

## Инварианты и ограничения

- Не ломать maps-профиль; gate `FhNNYd` без изменений.
- Major HQ остаётся **A20**; 8 vanilla Guardpost → до 8 auto-regions.
- Deterministic Voronoi tie-break (`outpost_id < best` при равной дистанции).
- Не менять public Region id prefix `JAZZ_Auto_`.

## Acceptance criteria

- `JAZZ-COMPAT-006-AC-001` — static: radius=3; refresh uses multi-outpost Voronoi;
  `ai_region_rev` wiring present.
- `JAZZ-COMPAT-006-AC-002` — runtime/DAP: after reload/bootstrap on save `31(3)`,
  each auto-region `#ManagedOutposts≤1`, `foreign_gp=0`, median `#Sectors` roughly
  ≤ ~1/5 of pre-fix peaks (pre: 53…132).
- `JAZZ-COMPAT-006-AC-003` — docs delta applied (technical + wiki + showcase RU/EN).

## Impact и совместимость

- Vanilla/CommonLib: нет.
- Saves: NoMaps existing — sector lists rebuild via `ai_region_rev` on LoadGame /
  InitSatelliteView soft path / force bootstrap refresh; new game uses R=3 from
  first bootstrap. **ReloadLua + `JAZZ_NoMapsBootstrap(true)`** достаточно на
  open save; иначе LoadSessionData / перезагрузка сейва.
- Network: satellite region membership may change after load (same as any region
  rebuild); no new NetSync surface.
- Cross-package: runtime owner `jazz-nomaps`; specs/docs in `jazz`.

## План и ownership

- Пакет-владелец кода: **jazz-nomaps**
- Docs/spec: **jazz**
- Reviewer: project-owner

## Решение владельца

- Статус: **approved** → implemented (чат 2026-08-02: «регионы ~5× меньше, максимум
  один outpost на region»; playtest save open + DAP dump)
- Кто подтвердил: project-owner (Kpoji4er)
- Дата: 2026-08-02
- Locked defaults: `ManagedOutposts` max 1; Chebyshev **R=3**; rebuild on load.
- **Superseded radius (2026-08-02):** hard R=3 left peripheral orphans → see
  [JAZZ-COMPAT-007](JAZZ-COMPAT-007.md) (unbounded Voronoi, `AI_REGION_REV=2`).
  Multi-outpost Voronoi + mop≤1 + foreign_gp=0 from this spec remain.

## Evidence

- `JAZZ-COMPAT-006-AC-001`: `PASS (static)` — `python docs/tools/_verify_nomaps_region_radius.py` OK;
  DoR Ready passed.
- `JAZZ-COMPAT-006-AC-002`: `PASS (runtime/DAP)` — save `31(3)` after `ReloadLua` +
  `JAZZ_NoMapsBootstrap(true)`: foreign_total=0, mop=1, secs **6…27** (was 53…132;
  max ~4.9× smaller).
- `JAZZ-COMPAT-006-AC-003`: `PASS (static)` — technical / wiki / showcase RU+EN updated.

### Pre-fix DAP dump (save open, 2026-08-02)

```
JAZZ_Auto_A20 secs=53 mop=1 foreign_gp=3
JAZZ_Auto_D10 secs=131 mop=1 foreign_gp=5
JAZZ_Auto_E16 secs=117 mop=1 foreign_gp=5
JAZZ_Auto_F19 secs=83 mop=1 foreign_gp=3
JAZZ_Auto_F7 secs=111 mop=1 foreign_gp=4
JAZZ_Auto_G10 secs=131 mop=1 foreign_gp=5
JAZZ_Auto_H14 secs=132 mop=1 foreign_gp=6
JAZZ_Auto_H4 secs=90 mop=1 foreign_gp=3
```

### Post-fix DAP dump (same session, ReloadLua + bootstrap force)

```
JAZZ_Auto_A20 secs=9 mop=1 foreign_gp=0
JAZZ_Auto_D10 secs=27 mop=1 foreign_gp=0
JAZZ_Auto_E16 secs=12 mop=1 foreign_gp=0
JAZZ_Auto_F19 secs=9 mop=1 foreign_gp=0
JAZZ_Auto_F7 secs=23 mop=1 foreign_gp=0
JAZZ_Auto_G10 secs=20 mop=1 foreign_gp=0
JAZZ_Auto_H14 secs=19 mop=1 foreign_gp=0
JAZZ_Auto_H4 secs=6 mop=1 foreign_gp=0
foreign_total=0 min=6 max=27 ai_region_rev=1
```

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md` — R=3, Voronoi refresh, rev.
- `docs/technical/compatibility.md` / bugs note — symptom + fix pointer.
- `docs/wiki/legion-global-ai.md` + showcase RU/EN `legion-strategy.md` —
  компактные округа (один аванпост, локальный catchment).
