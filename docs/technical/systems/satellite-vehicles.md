# Автотранспорт (JAZZ Maps) — сателлит (+ тактический stub)

## Назначение и эффект для игрока

На стратегической карте появляются припаркованные машины. Отряд может сесть в транспорт в том же секторе, быстрее ехать **только по дорогам** и выйти, оставив машину в текущем секторе.

**Тактический боевой Unit сейчас выключен** (`JAZZ_VehicleCombat.tactical_enabled = false`): на карте сектора машина как юнит не спавнится.

**Дизайн боевого автомобиля зафиксирован в JAZZ Maps**, но **в runtime ещё не внедрён**. Канон: [`JAZZ Maps/docs/combat-vehicle-design.md`](../../../JAZZ%20Maps/docs/combat-vehicle-design.md). Suite-указатель: [combat-vehicle-design.md](combat-vehicle-design.md).

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
| `Code/System_JAZZ_VehicleCombat.lua` | jazz-maps (`FhNNYd`) | **loaded**, spawn/hooks **dormant** пока `tactical_enabled=false`; прототип flag/Pivot — **устарел** относительно [design](combat-vehicle-design.md) |
| `UnitData/JAZZ_CombatHMMWV.lua` | jazz-maps | **loaded** companion stub (не спавнится) |
| Appearance `JAZZ_HMMWV_Stub` | jazz-maps items | stub `Body = Vehicle_UAZ`; runtime→`HMMWV` при будущем включении |
| `Entities/HMMWV.ent` | jazz_assets | entity stub: static `idle`/`walk`/`run`/`death` |
| `docs/combat-vehicle-design.md` | jazz-maps | **канон спеки** — не runtime |
| `docs/technical/systems/combat-vehicle-design.md` | jazz | указатель на maps |

### Сателлит (активно)

- `GameVar` `gv_JAZZ_Vehicles` — `{ next_id, list[id] = { id, type, sector_id, capacity, squad_id, unique_key, hp, max_hp, wrecked } }`
- `squad.JAZZ_vehicle_id` — отряд в машине (весь отряд считается на транспорте)
- `JAZZ_SpawnVehicle` / эффект `JAZZ_SpawnSatelliteVehicle` (idempotent по `UniqueKey`)
- `NetSyncEvents.JAZZ_BoardVehicle` / `JAZZ_ExitVehicle` / `JAZZ_SpawnVehicle`
- Wrapper `GetSectorTravelTime` (idempotent по identity текущего wrapper; если core заменил функцию — wrap снова): mounted + нет дороги → `false`; на дороге время × `road_time_mult` (HMMWV = 40 → ~2.5×)
- `route.JAZZ_vehicle` в wrapper `AssignSatelliteSquadRoute`
- UI: `idJAZZ_BoardVehicle` / `idJAZZ_ExitVehicle`; иконка на `SquadWindow`
- Wrecked → сесть нельзя

Тип v1: `HMMWV`, поле `capacity` в данных есть, продуктовый лимит вместимости **не целевой**; `max_hp` 120, `unit_template = JAZZ_CombatHMMWV`.

Спавн токена: M1 `SE_OnEnterMap` → `JAZZ_SpawnSatelliteVehicle` (`UniqueKey = M1_HMMWV`).

Топливо в runtime **нет**; по дизайну при внедрении — заглушка always-full (канон в maps).

### Тактика (stub / dormant)

Включение `tactical_enabled=true` — только после реализации по канону maps и тест-контракта C.

Сейчас в файле заготовлены (не целевая модель): flag `JAZZ_IsVehicle`, Pivot, path-filter ±90°, test FNMinimi. Целевое: класс `JAZZ_CombatVehicle`, Drive/ArcTurn, водитель, турель look-at.

## Межпакетные зависимости

- Maps optional dependency на `e6L4ECj` (JAZZ).
- Wrapper travel грузить после core `SatelliteSquad`.
- Jazz Assets (`pDGDhr`) optional; нужен для mesh HMMWV при будущем тактическом спавне.

## Проверка

Статический анализ + runtime (новая игра):

1. M1 → сателлит → «Сесть в транспорт» → дорога на M2 быстрее пешего.
2. Вход в сектор с машиной → **нет** отдельного боевого Unit транспорта.
3. Выход / смена сектора → токен машины на сателлите на месте.

Расширенный контракт (Фаза 1 / включение тактики) — в каноне maps [`combat-vehicle-design.md`](../../../JAZZ%20Maps/docs/combat-vehicle-design.md).

Не подтверждено в runtime — помечать как статический анализ.

## Ограничения

- Тактический юнит выключен намеренно.
- Дизайн кабина/турель/cover/OOP описан, код в игру не вставлен.
- Wrecked с тактики пока не возникает (нет Unit); поле в токене остаётся для будущего.
