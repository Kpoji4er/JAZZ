# Автотранспорт (JAZZ Maps) — сателлит (+ тактический stub)

## Назначение и эффект для игрока

На стратегической карте появляются припаркованные машины. Отряд может сесть в транспорт в том же секторе, быстрее ехать **только по дорогам** и выйти, оставив машину в текущем секторе.

**Тактический боевой Unit сейчас выключен** (`JAZZ_VehicleCombat.tactical_enabled = false`): на карте сектора машина как юнит не спавнится. Код, UnitData и Appearance сохранены как заглушки для будущего включения.

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | `GetSectorTravelTime`, `HasRoad`, `AssignSatelliteSquadRoute`, satellite context menu; декоративный `Vehicle` (`CombatObject`) без вождения |
| CommonLib | Не пересекается напрямую |
| JAZZ core | Переопределяет `GetSectorTravelTime` в `Code/SatelliteSquad.lua` (база для satellite wrapper) |
| JAZZ Maps | Владелец механики: сателлит активен; тактический Unit — stub/dormant spawn |

## Реализация и load-state

| Файл | Пакет | Статус |
|---|---|---|
| `Code/System_JAZZ_Vehicles.lua` | jazz-maps (`FhNNYd`) | **loaded** — сателлит (board/exit/travel/hp) |
| `Code/System_JAZZ_VehicleCombat.lua` | jazz-maps (`FhNNYd`) | **loaded**, spawn/hooks **dormant** пока `tactical_enabled=false`; таблица через `rawget(_G, …)` |
| `UnitData/JAZZ_CombatHMMWV.lua` | jazz-maps | **loaded** companion stub (не спавнится) |
| Appearance `JAZZ_HMMWV_Stub` | jazz-maps items | stub `Body = Vehicle_UAZ`; runtime→`HMMWV` при будущем включении |
| `Entities/HMMWV.ent` | jazz_assets | entity stub: static `idle`/`walk`/`run`/`death` для будущего Unit |

### Сателлит (активно)

- `GameVar` `gv_JAZZ_Vehicles` — `{ next_id, list[id] = { id, type, sector_id, capacity, squad_id, unique_key, hp, max_hp, wrecked } }`
- `squad.JAZZ_vehicle_id` — отряд в машине
- `JAZZ_SpawnVehicle` / эффект `JAZZ_SpawnSatelliteVehicle` (idempotent по `UniqueKey`)
- `NetSyncEvents.JAZZ_BoardVehicle` / `JAZZ_ExitVehicle` / `JAZZ_SpawnVehicle`
- Wrapper `GetSectorTravelTime` (idempotent по identity текущего wrapper; если core заменил функцию — wrap снова): mounted + нет дороги → `false`; на дороге время × `road_time_mult` (HMMWV = 40 → ~2.5×)
- `route.JAZZ_vehicle` в wrapper `AssignSatelliteSquadRoute`
- UI: `idJAZZ_BoardVehicle` / `idJAZZ_ExitVehicle`; иконка на `SquadWindow`
- Wrecked → сесть нельзя

Тип v1: `HMMWV`, capacity 6, `max_hp` 120, `unit_template = JAZZ_CombatHMMWV` (для будущего тактического спавна).

Спавн токена: M1 `SE_OnEnterMap` → `JAZZ_SpawnSatelliteVehicle` (`UniqueKey = M1_HMMWV`).

### Тактика (stub / dormant)

Включение: `JAZZ_VehicleCombat.tactical_enabled = true` (и убрать force-assign `false` в file scope после готовности Idle/entity).

Заготовлено, но не вызывается при `tactical_enabled=false`:

- `JAZZ_SpawnTacticalVehicle` / `JAZZ_TrySpawnVehiclesForCurrentSector`
- Hooks: `GetCombatPath`, `CombatGoto`, `GotoSlab`, `EnumUIActions`, `GetIdleBaseAnim`, `Idle`, `AimIdle`
- CombatActions Pivot L/R + Turret
- Sync HP/wrecked из Unit в токен

Entity HMMWV: static states `idle` / `Idle` / `idle_Combat` / `walk` / `run` / `death` — для будущего Unit без human-анимаций.

## Межпакетные зависимости

- Maps optional dependency на `e6L4ECj` (JAZZ).
- Wrapper travel грузить после core `SatelliteSquad`.
- Jazz Assets (`pDGDhr`) optional; нужен для mesh HMMWV при будущем тактическом спавне.

## Проверка

Статический анализ + runtime (новая игра):

1. M1 → сателлит → «Сесть в транспорт» → дорога на M2 быстрее пешего.
2. Вход в сектор с машиной → **нет** отдельного боевого Unit транспорта.
3. Выход / смена сектора → токен машины на сателлите на месте.

При `tactical_enabled=true` (ещё не цель): selectable Unit, Pivot, турель — отдельный тест-контракт.

Не подтверждено в runtime — помечать как статический анализ.

## Ограничения

- Тактический юнит выключен намеренно.
- Нет посадки мерков в кабину, бензина, garage, вражеского AI на машинах.
- Wrecked с тактики пока не возникает (нет Unit); поле в токене остаётся для будущего.
