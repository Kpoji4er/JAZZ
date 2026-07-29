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

- Starting supply аванпоста = 50 (ниже convoy trigger → supply-конвой легален сразу, без force-spawn).
- Весь POI/base supply income копится в пуле аванпоста (локальный spend + будущая отгрузка Майору конвоями); hourly tick **не** пишет напрямую в `major.reserve`.
- `MajorReserveCapacity` на порядок выше outpost (`5000` vs `500`); `MajorStartingReserve` ≥ одного `SupplyConvoyCargo`.
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

## Утверждённый контракт

| Параметр | Значение |
|---|---:|
| StartingSupply | 50 |
| SupplyCapacity (outpost) | 500 |
| MajorReserveCapacity | 5000 |
| MajorStartingReserve | 1000 (≥ SupplyConvoyCargo 150) |
| POI/base supply income | 100% в `outpost.supply` (cap outpost) |
| Mine diamonds | в `outpost.diamond_stock` → shipment → Major |

Need gates:

| Роль | Условие нужды |
|---|---|
| patrol | есть key-цель патруля |
| recon | hot sector Heat ≥ threshold |
| qrf | retake или unconsumed delivered report |
| garrison | legion key/POI без garrison-task и без Legion/enemy squad в секторе |

## Требования

- `JAZZ-STRATEGY-003-REQ-001` — starting supply аванпоста = 50.
- `JAZZ-STRATEGY-003-REQ-002` — hourly supply income целиком в outpost pool; Major получает ресурсы только конвоями/shipment.
- `JAZZ-STRATEGY-003-REQ-003` — Major reserve clamp к `MajorReserveCapacity` (default 5000).
- `JAZZ-STRATEGY-003-REQ-004` — garrison не дублирует уже стоящую оборону.
- `JAZZ-STRATEGY-003-REQ-005` — recon/qrf/patrol need-gating; без нужды supply не списывается.
- `JAZZ-STRATEGY-003-REQ-006` — docs/wiki/testing синхронизированы.

## Инварианты и ограничения

- Не менять GameVar schema keys (только значения/clamp).
- Не менять public EnemySquad/UnitData IDs.
- Existing save: `outpost.supply` не режется до 50; major.reserve clamp при EnsureState.

## Acceptance criteria

- `JAZZ-STRATEGY-003-AC-001` — новый outpost стартует с supply 50.
- `JAZZ-STRATEGY-003-AC-002` — hourly city/farm/base income увеличивает только outpost.supply (в пределах capacity).
- `JAZZ-STRATEGY-003-AC-003` — major.reserve не превышает MajorReserveCapacity.
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

28 июля 2026:

1. StartingSupply 50; supply-конвой легален сразу, spawn не форсить.
2. POI/base → пул аванпоста; Major кормится отгрузкой; Major cap ≫ outpost (×10).
3. Major на старте имеет reserve на ≥1 supply-конвой.
4. Need-based spawn; garrison учитывает pre-placed оборону.

Статус: approved → implemented (runtime AC открыты).

## Evidence

- `JAZZ-STRATEGY-003-AC-001`: `PASS (static)` / `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-STRATEGY-003-AC-002`: `PASS (static)` / `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-STRATEGY-003-AC-003`: `PASS (static)` / `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-STRATEGY-003-AC-004`: `PASS (static)` / `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-STRATEGY-003-AC-005`: `PASS (static)` / `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-STRATEGY-003-AC-006`: `PASS (static)`

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md`
- `docs/technical/testing.md`
- `docs/wiki/legion-global-ai.md`
