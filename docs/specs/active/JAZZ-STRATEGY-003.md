---
id: JAZZ-STRATEGY-003
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
  - jazz/docs/specs/active/JAZZ-STRATEGY-003.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/Code/Regions_Sectors.lua
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/testing.md
  - jazz/docs/wiki/legion-global-ai.md
exclusive_resources:
  - GameVar:gv_JAZZ_LegionAI
  - ModItemRegion:ErnieIsland
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-003: starting supply, outpost pool, Major cap, need-based spawn

## Проблема

Пилот `JAZZ-STRATEGY-002` спавнит regular-отряды слишком быстро (starting supply 250). Garrison выбирает любой legion key/POI без учёта уже стоящей обороны. Major reserve не имел явного capacity относительно аванпоста.

## Цели

- Starting money аванпоста ниже supply-convoy trigger → supply-конвой легален сразу, без force-spawn.
- Base passive и (исторически) POI income копятся в пуле аванпоста; hourly tick **не** пишет напрямую в Major.
- `MajorReserveCapacity` ≫ outpost; `MajorStartingReserve` ≥ одного `SupplyConvoyCargo`.
- Спавн regular-ролей только при нужде:
  - patrol — всегда, пока есть цель и слот/supply;
  - recon — Heat ≥ `ReconHeatThreshold`;
  - qrf — retake или свежий report;
  - garrison — key/POI без managed garrison и без физического Legion/enemy squad (включая pre-placed).

## Non-goals

- Force-spawn стартовых конвоев; inventory Cost sync для diamond briefcase (задача 1+).
- Изменение CommandInterval, role costs/caps, составов EnemySquad, UI icons.
- Включение Global AI вне ErnieIsland/I7.
- Generated data / localization ID changes.

## Утверждённый контракт (current runtime)

Масштаб `$` зафиксирован в [JAZZ-STRATEGY-006](JAZZ-STRATEGY-006.md); city/farm → `poi_money` + tax — в [JAZZ-STRATEGY-009](JAZZ-STRATEGY-009.md). Ниже — актуальные defaults Region:

| Параметр | Значение |
|---|---:|
| StartingSupply (outpost start `$`) | 12000 |
| SupplyCapacity (outpost) | 120000 |
| MajorReserveCapacity | 1200000 |
| MajorStartingReserve | 120000 (≥ SupplyConvoyCargo 12000) |
| Base passive $/h | 0 → `outpost.money` |
| City/farm `$` | пульс 72h → `poi_money` → tax → `outpost.money` (009) |
| Mine diamonds | hourly → `outpost.diamond_stock` → shipment → Major |

Need gates:

| Роль | Условие нужды |
|---|---|
| patrol | есть key-цель патруля |
| recon | hot sector Heat ≥ threshold |
| qrf | retake или unconsumed delivered report |
| garrison | legion key/POI без garrison-task и без Legion/enemy squad в секторе |

## Требования

- `JAZZ-STRATEGY-003-REQ-001` — starting money аванпоста = `StartingSupply` (current default 12000).
- `JAZZ-STRATEGY-003-REQ-002` — base passive → outpost pool; Major получает `$` только конвоями/shipment (city/farm path после 009 — через `poi_money`/tax).
- `JAZZ-STRATEGY-003-REQ-003` — Major money clamp к `MajorReserveCapacity` (default 1200000).
- `JAZZ-STRATEGY-003-REQ-004` — garrison не дублирует уже стоящую оборону.
- `JAZZ-STRATEGY-003-REQ-005` — recon/qrf/patrol need-gating; без нужды money не списывается.
- `JAZZ-STRATEGY-003-REQ-006` — docs/wiki/testing синхронизированы.

## Инварианты и ограничения

- Не менять GameVar schema keys (только значения/clamp).
- Не менять public EnemySquad/UnitData IDs.
- Existing save: outpost money не режется до starting; major money clamp при EnsureState.

## Acceptance criteria

- `JAZZ-STRATEGY-003-AC-001` — новый outpost стартует с `StartingSupply` (12000).
- `JAZZ-STRATEGY-003-AC-002` — base passive увеличивает только `outpost.money` (в пределах capacity); city/farm не пишут hourly в outpost после 009.
- `JAZZ-STRATEGY-003-AC-003` — `major.money` не превышает MajorReserveCapacity.
- `JAZZ-STRATEGY-003-AC-004` — key POI с pre-placed Legion squad не получает новый garrison.
- `JAZZ-STRATEGY-003-AC-005` — без Heat/report/retake recon/qrf не спавнятся.
- `JAZZ-STRATEGY-003-AC-006` — docs синхронизированы.

## Impact и совместимость

- **Runtime:** экономика и garrison filter.
- **Saves:** без schema migration; clamp reserve на ensure.
- **Network/determinism:** без новых RNG.
- **Rollback:** revert Lua + docs.

## План и ownership

1. `jazz` — code + docs.
2. Runtime smoke — владелец.

## Решение владельца

28 июля 2026 (need-gates + Major≫outpost). Масштаб `$` и start/cap пересмотрены в 006 (`12000` / `120000` / `1200000`); city/farm income path — в 009 (`poi_money` + tax).

Статус: implemented. Current-state numbers/docs sync 2026-07-29.

## Evidence

- `JAZZ-STRATEGY-003-AC-001`: `PASS (static)` — `StartingSupply` default 12000 in `Regions_Sectors.lua` / `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-STRATEGY-003-AC-002`: `PASS (static)` — base passive → `outpost.money`; city/farm → `poi_money` (009) / `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-STRATEGY-003-AC-003`: `PASS (static)` — `MajorReserveCapacity` 1200000 / `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-STRATEGY-003-AC-004`: `PASS (static)` / `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-STRATEGY-003-AC-005`: `PASS (static)` / `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-STRATEGY-003-AC-006`: `PASS (static)` — technical §pilot economy aligned with 006/009; 2026-07-29 doc sync

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md`
- `docs/technical/testing.md`
- `docs/wiki/legion-global-ai.md`
