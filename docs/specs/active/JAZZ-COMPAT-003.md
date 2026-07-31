---
id: JAZZ-COMPAT-003
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
  - jazz/docs/specs/active/JAZZ-COMPAT-003.md
  - jazz/Code/LegionTierProgression.lua
  - jazz/Code/Regions_Sectors.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/technical/compatibility.md
  - jazz/docs/technical/bugs/nomaps-playtest-2026-07-30.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-units.md
  - jazz/docs/showcase/en/legion-units.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz/docs/patches/jazz-nomaps-0.4/**
  - jazz-nomaps/Code/NoMaps_Autonomy.lua
  - jazz-nomaps/metadata.lua
exclusive_resources:
  - ModDef:7MsJ2Eq
  - GameVar:gv_JAZZ_NoMaps
  - Code:NoMaps_Autonomy.lua
  - Quest:JAZZ_LegionTier
  - Code:LegionTierProgression.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMPAT-003: NoMaps Global AI + Legion tier (mines/sectors)

## Проблема

1. **Global AI в профиле NoMaps выглядит мёртвым.** Auto-regions `JAZZ_Auto_*` создаются с
   `StartingManpower=12` при `garrison.size_min=25`, `TaxCap=0` / `RecruiterCap=0` (нет
   пополнения), а disabled `ErnieIsland` сохраняет `Sectors` (I2–I7…), которые совпадают с
   vanilla HotDiamonds ID → `GetRegionForSector` может вернуть disabled region раньше auto-region.
2. **Прогрессия снаряжения Легиона** на материке завязана на Ernie-сетку `PlayerControlSectors`
   (TCE в `JAZZ_LegionTier`). На HotDiamonds это слишком быстро/не про шахты. Владелец:
   в NoMaps **крупный тир ← шахты**, **подтир ← сектора**.

## Цели

- NoMaps Legion Global AI спавнит роли (garrison/patrol/…) и крутит tax/recruiter на vanilla
  guardposts после bootstrap / load.
- `GetRegionForSector` предпочитает `LegionAIEnabled` region при коллизии списков.
- Disabled maps-only regions очищают `Sectors` / `ManagedOutposts`.
- При активном NoMaps `JAZZ_Legion_Tier` считается формулой mines→major, sectors→sub; Ernie TCE
  не перетирают значение.
- С maps (без активного NoMaps) Ernie TCE-сетка без регрессии.

## Non-goals

- Смена LootDef band / UNITS-003 generator.
- Переписывание authored Ernie thresholds для maps-профиля.
- Полный mainland Global AI design вне NoMaps auto-regions.
- Workshop upload / Steam `last_changes` full replace.

## Требования

- `JAZZ-COMPAT-003-REQ-001` — `JAZZ_Auto_*` стартуют с manpower ≥ garrison `size_min` (25) и
  `TaxCap≥1`, `RecruiterCap≥1`; tax/recruiter fallback на `SupplySquads` допустим.
- `JAZZ-COMPAT-003-REQ-002` — при disable maps-only region: `LegionAIEnabled=false`,
  `ManagedOutposts={}`, `Sectors={}`.
- `JAZZ-COMPAT-003-REQ-003` — `GetRegionForSector` возвращает enabled Legion AI region при
  нескольких совпадениях; иначе любой match (legacy).
- `JAZZ-COMPAT-003-REQ-004` — NoMaps-only progression: major I→II от player-owned `Mine`
  (≥1 → II); major III от WorldFlip (`04_Betrayal.TriggerWorldFlip` или `WorldFlipDone`,
  тот же сигнал что Bobby Ray shop T3); sub от числа player-owned surface sectors;
  encoding `major*10+sub` в `{11,12,13,21..25,31,32,33}`; только вверх.
- `JAZZ-COMPAT-003-REQ-005` — TCE `JAZZ_LegionTier` не срабатывают, пока `JAZZ_NoMapsIsActive()`.
- `JAZZ-COMPAT-003-REQ-006` — смена tier → `RegenerateLegionLoot()` как у TCE.
- `JAZZ-COMPAT-003-REQ-007` — existing NoMaps save: one-shot economy rev поднимает outpost
  manpower до нового StartingManpower floor и применяет caps на auto-regions.
- `JAZZ-COMPAT-003-REQ-008` — docs: technical + wiki/showcase RU/EN для player-facing tier/AI.

### Формула tier (NoMaps)

| Условие | Major |
| --- | ---: |
| иначе (0 mines, до WorldFlip) | 1 |
| ≥1 player mine, до WorldFlip | 2 |
| `04_Betrayal` `TriggerWorldFlip` **или** `WorldFlipDone` | 3 |

| Major | Player sectors → sub |
| ---: | --- |
| 1 | ≤1→1, ≤3→2, else→3 |
| 2 | ≤2→1, ≤4→2, ≤6→3, ≤8→4, else→5 |
| 3 | ≤4→1, ≤7→2, else→3 |

Считаются surface sectors (`not GroundSector`, Passability не Water/Blocked) со `Side` player1/player2.
Mine = `sector.Mine` и тот же side-фильтр. WorldFlip перекрывает mines (III даже при 0 шахт).

## Инварианты и ограничения

- Не ломать maps-профиль Ernie AI / TCE.
- Не менять public quest/var IDs.
- Deterministic; без лишнего NetSync.
- Push в `JAZZ-nomaps` может быть недоступен cloud agent → patch kit в jazz обязателен.

## Acceptance criteria

- `JAZZ-COMPAT-003-AC-001` — static: auto-region defaults manpower≥25, TaxCap/RecruiterCap≥1;
  disable clears Sectors.
- `JAZZ-COMPAT-003-AC-002` — static: `GetRegionForSector` prefers `LegionAIEnabled`.
- `JAZZ-COMPAT-003-AC-003` — static: `JAZZ_ComputeLegionTierNoMaps` / update hook + TCE gate.
- `JAZZ-COMPAT-003-AC-004` — static unit: table of (mines,sectors)→tier matches formula.
- `JAZZ-COMPAT-003-AC-005` — runtime/human: NoMaps new game — managed squads появляются;
  захват шахты поднимает major; сектора — sub; maps profile TCE unchanged.
- `JAZZ-COMPAT-003-AC-006` — generated sync jazz (+ nomaps если доступен) errors=0.

## Impact и совместимость

- Vanilla/CommonLib: только JAZZ Region lookup preference.
- Saves: NoMaps `gv_JAZZ_NoMaps.ai_economy_rev`; quest tier may jump upward once on load.
- Network: satellite hour / side change already synced paths.
- Cross-package: nomaps economy; jazz progression + GetRegionForSector.

## План и ownership

- Пакет-владелец AI economy: **jazz-nomaps**
- Пакет-владелец tier formula / GetRegionForSector: **jazz**
- Reviewer: project-owner

## Решение владельца

- Статус: **approved** (чат 2026-07-31: «Global AI в no maps не работает» + «тиры легиона в no maps привяжем к шахтам, а подтиры к секторам»)
- Кто подтвердил: project-owner
- Дата: 2026-07-31

## Evidence

- `JAZZ-COMPAT-003-AC-001`: `PASS (static)` — `NoMaps_Autonomy.lua` StartingManpower=40, TaxCap/RecruiterCap=1, disable clears Sectors; patch kit 0.7.
- `JAZZ-COMPAT-003-AC-002`: `PASS (static)` — `Regions_Sectors.lua` prefers `LegionAIEnabled`.
- `JAZZ-COMPAT-003-AC-003`: `PASS (static)` — `LegionTierProgression.lua` + 11 TCE `CheckExpression` gates in `items.lua`.
- `JAZZ-COMPAT-003-AC-004`: `PASS (static)` — formula cases (mines,sectors,world_flip)→tier; III only when world_flip.
- `JAZZ-COMPAT-003-AC-005`: `BLOCKED (runtime/human)` — NoMaps new game / mine capture / maps TCE smoke.
- `JAZZ-COMPAT-003-AC-006`: `PASS (static)` — ModItemCode + metadata.code wired; editor round-trip still open.

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md` — NoMaps economy + Ernie Sectors clear.
- `docs/technical/systems/legion-units-equipment-tiers.md` — NoMaps mines/sectors formula.
- `docs/technical/systems/file-coverage.md` — `LegionTierProgression.lua`.
- `docs/technical/compatibility.md` / bugs note — AI freeze root cause.
- `docs/wiki/legion-global-ai.md` + showcase RU/EN legion-units/strategy — player-facing.
