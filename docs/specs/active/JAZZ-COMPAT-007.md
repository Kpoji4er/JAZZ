---
id: JAZZ-COMPAT-007
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
  - jazz/docs/specs/active/JAZZ-COMPAT-007.md
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

# JAZZ-COMPAT-007: NoMaps auto-regions — full surface coverage (unbounded Voronoi)

## Проблема

После **COMPAT-006** (Chebyshev **R=3** + multi-outpost Voronoi) округа стали
компактными (`#Sectors` 6…27, `foreign_gp=0`, `mop=1`), но на сат-карте остались
**сектора без региона**. DAP save `31(3)` (2026-08-02): surface land **151**,
covered **125**, **orphans=26** (периферия: `A16`, `A2`/`B2`–`B5`/`C3`, юг
`J*`/`K*`/`L*`). Owner: orphans = bug; full map coverage required.

Корневая причина: hard cap `best_dist ≤ AUTO_REGION_RADIUS` (3) оставляет
клетками без nearest-outpost assignment всё дальше R от любого Guardpost.

## Цели

- Каждый **relevant surface** сектор (не `GroundSector`, не Water/непроходимый)
  принадлежит **ровно одному** `JAZZ_Auto_*` (нет orphans).
- Сохранить `#ManagedOutposts ≤ 1` и `foreign_gp=0` (чужой Guardpost не в чужом
  `Sectors`).
- Не возвращать R=8 single-outpost blobs: модель = **unbounded nearest-outpost
  Voronoi** (естественный catchment ближайшего GP).
- Existing open saves пересобирают `Sectors` через `ai_region_rev` bump (как
  COMPAT-006).

## Non-goals

- Caps / economy / Major HQ / tax / patrol / STRATEGY-015 medic.
- Maps-профиль geography.
- Commit / push / Workshop.

## Требования

- `JAZZ-COMPAT-007-REQ-001` — `lAssignSectorsToOutposts` назначает каждый surface
  сектор ближайшему tracked outpost **без** Chebyshev radius cap
  (`AUTO_REGION_RADIUS = false` / unbounded); tie-break по `outpost_id` как сейчас.
- `JAZZ-COMPAT-007-REQ-002` — invariants: `#ManagedOutposts ≤ 1`; в `Sectors` нет
  чужого Guardpost; orphan count surface = 0 после refresh.
- `JAZZ-COMPAT-007-REQ-003` — `AI_REGION_REV = 2`; saves с `ai_region_rev < 2`
  rebuild на soft/full bootstrap; force path всегда refresh.
- `JAZZ-COMPAT-007-REQ-004` — docs: technical + wiki + showcase RU/EN (полное
  покрытие суши + Voronoi catchment); COMPAT-006 note → superseded radius by 007.

## Инварианты и ограничения

- Gate `FhNNYd` без изменений; Major HQ **A20**; prefix `JAZZ_Auto_`.
- Deterministic Voronoi tie-break.
- Water / GroundSector / непроходимые сектора остаются вне auto-regions (не «relevant»).

## Acceptance criteria

- `JAZZ-COMPAT-007-AC-001` — static: unbounded assign; `AI_REGION_REV=2`;
  multi-outpost Voronoi refresh retained; verify script OK.
- `JAZZ-COMPAT-007-AC-002` — runtime/DAP: after ReloadLua + bootstrap force,
  surface orphans=0, foreign_gp=0, mop=1 per region; sizes natural Voronoi
  (not R=8 mega-blobs).
- `JAZZ-COMPAT-007-AC-003` — docs delta applied.

## Impact и совместимость

- Saves: NoMaps existing — rebuild via `ai_region_rev=2` on LoadGame / soft /
  force bootstrap. **ReloadLua + `JAZZ_NoMapsBootstrap(true)`** on open save.
- Network: satellite membership may change after rebuild (same class as 006).
- Cross-package: runtime `jazz-nomaps`; specs/docs `jazz`.

## План и ownership

- Пакет-владелец кода: **jazz-nomaps**
- Docs/spec: **jazz**
- Reviewer: project-owner

## Решение владельца

- Статус: **approved** (задача владельца 2026-08-02: orphans bug; prefer unbounded
  nearest-outpost Voronoi; mop≤1; foreign_gp=0; no R=8 blobs; no commit)
- Кто подтвердил: project-owner (Kpoji4er)
- Дата: 2026-08-02
- Locked model: unbounded Voronoi; `AI_REGION_REV=2`.

## Evidence

- `JAZZ-COMPAT-007-AC-001`: `PASS (static)` — `python docs/tools/_verify_nomaps_region_radius.py` OK;
  DoR Ready passed.
- `JAZZ-COMPAT-007-AC-002`: `PASS (runtime/DAP)` — save open after `ReloadLua` +
  `JAZZ_NoMapsBootstrap(true)`: orphans **0** (was 26), foreign_total=0, mop=1,
  secs **9…29**, `ai_region_rev=2` (pre: surface=151 covered=125 orphans=26,
  min=6 max=27, rev=1).
- `JAZZ-COMPAT-007-AC-003`: `PASS (static)` — technical / wiki / showcase RU+EN +
  COMPAT-006 supersession note updated.

### Pre-fix DAP (save open, post-COMPAT-006 state)

```
surface=151 covered=125 orphans=26 foreign_total=0 min=6 max=27 ai_region_rev=1
JAZZ_Auto_A20 secs=9 mop=1 foreign_gp=0
JAZZ_Auto_D10 secs=27 mop=1 foreign_gp=0
JAZZ_Auto_E16 secs=12 mop=1 foreign_gp=0
JAZZ_Auto_F19 secs=9 mop=1 foreign_gp=0
JAZZ_Auto_F7 secs=23 mop=1 foreign_gp=0
JAZZ_Auto_G10 secs=20 mop=1 foreign_gp=0
JAZZ_Auto_H14 secs=19 mop=1 foreign_gp=0
JAZZ_Auto_H4 secs=6 mop=1 foreign_gp=0
orphans_sample=A16,A2,B2,B3,B4,B5,C3,J18,J19,J20,K10,K18,K19,K20,K9,L10,...
```

### Post-fix DAP (same session, ReloadLua + bootstrap force)

```
surface=151 covered=151 orphans=0 foreign_total=0 min=9 max=29 ai_region_rev=2
JAZZ_Auto_A20 secs=10 mop=1 foreign_gp=0
JAZZ_Auto_D10 secs=27 mop=1 foreign_gp=0
JAZZ_Auto_E16 secs=12 mop=1 foreign_gp=0
JAZZ_Auto_F19 secs=15 mop=1 foreign_gp=0
JAZZ_Auto_F7 secs=29 mop=1 foreign_gp=0
JAZZ_Auto_G10 secs=23 mop=1 foreign_gp=0
JAZZ_Auto_H14 secs=26 mop=1 foreign_gp=0
JAZZ_Auto_H4 secs=9 mop=1 foreign_gp=0
```

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md` — unbounded Voronoi + rev=2.
- `docs/technical/compatibility.md` / bugs B17 follow-up.
- `docs/wiki/legion-global-ai.md` + showcase RU/EN — полное покрытие суши.
- COMPAT-006: note radius superseded by COMPAT-007 (Voronoi retained).
